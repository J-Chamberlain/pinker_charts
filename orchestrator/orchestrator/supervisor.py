from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

from .adapters import GenericCsvAdapter, PinkerChartsAdapter
from .config import OrchestratorConfig, load_config
from .config import ExecutorConfig, LoopConfig, ReviewerConfig, SupervisorEngineConfig
from .executors import CodexCLIExecutor, GitHubIssueExecutor, NoopExecutor
from .github_client import GitHubClient
from .issue_queue import build_issue_draft
from .models import AnthropicReviewer, NoopReviewer, OpenAIReviewer
from .review_gate import latest_run_dir, run_review_gate
from .run_record import load_run_record
from .schemas import COMPLETED_STATUSES
from .schemas import ExecutionResult, SupervisorDecision, Task
from .supervisors import NoopSupervisor, OpenAISupervisor
from .supervisor_log import append_decision


def build_adapter(config: OrchestratorConfig):
    if config.project.adapter == "pinker_charts":
        return PinkerChartsAdapter(config.project.root)
    if config.project.adapter == "generic_csv":
        return GenericCsvAdapter(config.project.root, config.project.state_file, config.project.registry_file, config.project.review_manifest)
    raise ValueError(f"Unsupported adapter: {config.project.adapter}")


def build_executor(config: OrchestratorConfig, mode: str):
    if mode == "issue-only" or config.executor.kind == "github_issue":
        client = GitHubClient(config.github) if config.github else None
        return GitHubIssueExecutor(client, labels=config.project.default_labels, dry_run=config.dry_run or config.executor.dry_run)
    if mode == "local-loop" or config.executor.kind == "codex_cli":
        return CodexCLIExecutor(
            command=config.executor.command,
            dry_run=config.dry_run or config.executor.dry_run,
            repo_root=config.project.root,
            branch_prefix=config.executor.branch_prefix,
            runs_dir=config.executor.runs_dir,
            timeout_seconds=config.executor.timeout_seconds,
        )
    return NoopExecutor()


def build_reviewer(config: OrchestratorConfig):
    if config.reviewer.kind == "openai" and os.environ.get("OPENAI_API_KEY"):
        return OpenAIReviewer(model=config.reviewer.model, dry_run=config.dry_run or config.reviewer.dry_run)
    if config.reviewer.kind == "anthropic":
        return AnthropicReviewer(model=config.reviewer.model, dry_run=config.dry_run or config.reviewer.dry_run)
    return NoopReviewer()


def build_decision_engine(config: OrchestratorConfig):
    if config.supervisor.kind == "openai" and os.environ.get("OPENAI_API_KEY"):
        return OpenAISupervisor(model=config.supervisor.model, dry_run=config.dry_run or config.supervisor.dry_run)
    return NoopSupervisor()


def _is_unprocessed(task: Task) -> bool:
    return task.status in {"", "not_started"} or task.status not in COMPLETED_STATUSES and task.status != "in_progress"


def select_task(config: OrchestratorConfig, skip_task_ids: set[str] | None = None) -> tuple[Task | None, object, object]:
    adapter = build_adapter(config)
    state = adapter.read_state()
    skip_task_ids = skip_task_ids or set()
    for task in adapter.tasks(state):
        if task.id not in skip_task_ids and _is_unprocessed(task):
            return task, adapter, state
    return None, adapter, state


def _git(repo_root: Path, args: list[str]):
    import subprocess

    return subprocess.run(["git", *args], cwd=repo_root, text=True, capture_output=True, check=False)


def _worktree_clean(repo_root: Path) -> bool:
    status = _git(repo_root, ["status", "--short"])
    return status.returncode == 0 and not status.stdout.strip()


def _current_branch(repo_root: Path) -> str:
    branch = _git(repo_root, ["branch", "--show-current"])
    return branch.stdout.strip() if branch.returncode == 0 else ""


def _switch_branch(repo_root: Path, branch: str) -> bool:
    switched = _git(repo_root, ["switch", branch])
    return switched.returncode == 0


def plan_task(task: Task) -> str:
    draft = build_issue_draft(task)
    return f"{draft.title}\n\n{draft.body}"


def _task_for_run(config: OrchestratorConfig, run_dir: Path | None) -> Task | None:
    adapter = build_adapter(config)
    if run_dir:
        metadata_path = run_dir / "metadata.json"
        if metadata_path.exists():
            import json

            metadata = json.loads(metadata_path.read_text())
            task_id = metadata.get("task_id")
            for task in adapter.tasks(adapter.read_state()):
                if task.id == task_id:
                    return task
    return adapter.select_next_task(adapter.read_state())


def _run_dir_from_execution(execution: ExecutionResult) -> Path | None:
    for artifact in execution.artifacts:
        path = Path(artifact)
        if path.exists():
            return path.parent
    return None


def _runs_dir(config: OrchestratorConfig) -> Path:
    return config.executor.runs_dir or config.project.root / "orchestrator/runs"


def _task_by_id(config: OrchestratorConfig, task_id: str) -> Task | None:
    adapter = build_adapter(config)
    for task in adapter.tasks(adapter.read_state()):
        if task.id == task_id:
            return task
    return None


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text())


def _matches_review_selector(run_dir: Path, *, run_id: str | None = None, branch: str | None = None, commit: str | None = None) -> bool:
    if run_id and run_dir.name == run_id:
        return True
    record = load_run_record(run_dir)
    metadata = _read_json(run_dir / "metadata.json")
    summary = _read_json(run_dir / "summary.json")
    run_branch = record.worker_branch if record else metadata.get("branch") or summary.get("branch")
    run_head = record.head_sha if record else summary.get("head_sha")
    return bool((branch and run_branch == branch) or (commit and run_head and str(run_head).startswith(commit)))


def resolve_review_run_dir(
    config: OrchestratorConfig,
    *,
    latest_run: bool = False,
    run_id: str | None = None,
    branch: str | None = None,
    commit: str | None = None,
    confirm_latest_run: bool = False,
) -> tuple[Path | None, str | None]:
    runs_dir = _runs_dir(config)
    if run_id or branch or commit:
        if not runs_dir.exists():
            return None, "No run directory exists."
        for candidate in sorted([path for path in runs_dir.iterdir() if path.is_dir()], reverse=True):
            if _matches_review_selector(candidate, run_id=run_id, branch=branch, commit=commit):
                return candidate, None
        return None, "No run matched the explicit review selector."
    if latest_run:
        selected = latest_run_dir(runs_dir)
        if not selected:
            return None, "No latest run directory found."
        if not confirm_latest_run:
            return selected, f"Latest run is `{selected.name}`. Rerun with `--run-id {selected.name}` or `--confirm-latest-run` to review it."
        return selected, None
    return None, None


def _latest_pending_remediation(config: OrchestratorConfig) -> dict[str, Any] | None:
    runs_dir = config.executor.runs_dir or config.project.root / "orchestrator/runs"
    run_dir = latest_run_dir(runs_dir)
    if not run_dir:
        return None
    decision = _read_json(run_dir / "final_loop_decision.json") or _read_json(run_dir / "supervisor_decision.json")
    action = decision.get("final_action") or decision.get("supervisor_decision") or decision.get("next_action")
    if action != "remediate":
        return None
    task_id = decision.get("task_id")
    task = _task_by_id(config, task_id) if task_id else None
    if not task:
        return None
    review = _read_json(run_dir / "review_result.json")
    parsed_review = review.get("raw", {}).get("parsed_result") or _read_json(run_dir / "parsed_reviewer_result.json")
    parsed_supervisor = _read_json(run_dir / "parsed_supervisor_decision.json")
    remediation_items = _remediation_items(parsed_review, parsed_supervisor, decision)
    return {
        "run_dir": run_dir,
        "run_id": run_dir.name,
        "task": task,
        "branch": decision.get("worker_branch") or "",
        "reason": decision.get("decision_basis") or decision.get("supervisor_decision") or "remediation_requested",
        "items": remediation_items,
        "prompt": _build_remediation_prompt(task, decision, parsed_review, parsed_supervisor, remediation_items),
    }


def _as_string_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    return [str(value)] if str(value).strip() else []


def _remediation_items(parsed_review: dict[str, Any], parsed_supervisor: dict[str, Any], decision: dict[str, Any]) -> tuple[str, ...]:
    items: list[str] = []
    items.extend(_as_string_list(parsed_review.get("required_remediation")))
    items.extend(_as_string_list(parsed_review.get("reasonable_next_steps")))
    items.extend(_as_string_list(parsed_review.get("issues")))
    items.extend(_as_string_list(parsed_supervisor.get("required_remediation")))
    items.extend(_as_string_list(parsed_supervisor.get("reasonable_next_steps")))
    items.extend(_as_string_list(parsed_supervisor.get("followup_task_prompt")))
    items.extend(_as_string_list(decision.get("remediation_reason")))
    deduped: list[str] = []
    for item in items:
        if item not in deduped:
            deduped.append(item)
    return tuple(deduped)


def _build_remediation_prompt(
    task: Task,
    decision: dict[str, Any],
    parsed_review: dict[str, Any],
    parsed_supervisor: dict[str, Any],
    remediation_items: tuple[str, ...],
) -> str:
    items = "\n".join(f"- {item}" for item in remediation_items) or "- Reinspect the latest reviewer and supervisor decision artifacts and address the remediation request."
    return f"""You are remediating a previously reviewed task. Do not start a different figure.

Task:
- id: {task.id}
- title: {task.title}

Parent review decision:
- final_action: {decision.get("final_action") or decision.get("supervisor_decision")}
- decision_basis: {decision.get("decision_basis")}
- reviewer_status: {decision.get("reviewer_status")}
- supervisor_status: {decision.get("supervisor_status")}

Remediation items:
{items}

Reviewer rationale:
{parsed_review.get("rationale") or parsed_review.get("summary") or ""}

Supervisor rationale:
{parsed_supervisor.get("rationale") or ""}

Rules:
- Work only on the existing worker branch.
- Do not switch to a different figure.
- Do not merge to main or production-loop.
- Commit one clean remediation unit if you make changes.
- If remediation cannot be completed automatically, document the blocker clearly and commit that documentation.
"""


def run_once(
    config: OrchestratorConfig,
    mode: str,
    latest_run: bool = False,
    skip_task_ids: set[str] | None = None,
    review_run_id: str | None = None,
    review_branch: str | None = None,
    review_commit: str | None = None,
    confirm_latest_run: bool = False,
) -> SupervisorDecision:
    if mode == "local-loop" and config.loop.allow_remediation:
        pending = _latest_pending_remediation(config)
        if pending:
            executor = build_executor(config, mode)
            if isinstance(executor, CodexCLIExecutor):
                execution = executor.execute_remediation(
                    pending["task"],
                    pending["branch"],
                    pending["prompt"],
                    parent_run_id=pending["run_id"],
                    remediation_reason=pending["reason"],
                    remediation_items=pending["items"],
                )
                if config.dry_run or not execution.artifacts:
                    return SupervisorDecision(action="remediate", reason=execution.message, task=pending["task"], execution=execution)
                run_dir = _run_dir_from_execution(execution)
                if not execution.success and not run_dir:
                    return SupervisorDecision(action="blocked", reason=execution.message, task=pending["task"], execution=execution)
                return run_review_gate(
                    config.project.root,
                    _runs_dir(config),
                    pending["task"],
                    build_reviewer(config),
                    decision_engine=build_decision_engine(config),
                    project_state=build_adapter(config).read_state(),
                    run_dir=run_dir,
                    dry_run=config.dry_run,
                    push_branch=True,
                    allow_remediation=config.loop.allow_remediation,
                )
    task, adapter, state = select_task(config, skip_task_ids)
    if not task:
        return SupervisorDecision(action="stop", reason="No eligible task found.")
    if mode == "plan-only":
        return SupervisorDecision(action="plan", reason=plan_task(task), task=task)
    if mode == "review-only":
        runs_dir = _runs_dir(config)
        run_dir, selector_message = resolve_review_run_dir(
            config,
            latest_run=latest_run,
            run_id=review_run_id,
            branch=review_branch,
            commit=review_commit,
            confirm_latest_run=confirm_latest_run,
        )
        if selector_message:
            return SupervisorDecision(action="needs_manual_review", reason=selector_message)
        review_task = _task_for_run(config, run_dir) or task
        return run_review_gate(
            config.project.root,
            runs_dir,
            review_task,
            build_reviewer(config),
            decision_engine=build_decision_engine(config),
            project_state=adapter.read_state(),
            run_dir=run_dir,
            dry_run=config.dry_run,
            push_branch=not config.dry_run,
            allow_remediation=config.loop.allow_remediation,
        )
    executor = build_executor(config, mode)
    execution = executor.execute(task)
    if mode == "local-loop" and not config.dry_run and not execution.success and not execution.artifacts:
        return SupervisorDecision(action="blocked", reason=execution.message, task=task, execution=execution)
    if mode == "local-loop" and not config.dry_run and execution.artifacts:
        reviewer = build_reviewer(config)
        run_dir = _run_dir_from_execution(execution)
        decision = run_review_gate(
            config.project.root,
            _runs_dir(config),
            task,
            reviewer,
            decision_engine=build_decision_engine(config),
            project_state=adapter.read_state(),
            run_dir=run_dir,
            dry_run=config.dry_run,
            push_branch=True,
            allow_remediation=config.loop.allow_remediation,
        )
        if (
            decision.action == "remediate"
            and config.loop.allow_remediation
            and isinstance(executor, CodexCLIExecutor)
            and decision.engine_result
            and decision.engine_result.followup_task_prompt
            and execution.branch
        ):
            remediation = executor.execute_remediation(task, execution.branch, decision.engine_result.followup_task_prompt)
            if remediation.success:
                return run_review_gate(
                    config.project.root,
                    _runs_dir(config),
                    task,
                    reviewer,
                    decision_engine=build_decision_engine(config),
                    project_state=adapter.read_state(),
                    run_dir=_run_dir_from_execution(remediation),
                    dry_run=config.dry_run,
                    push_branch=True,
                    allow_remediation=False,
                )
            return SupervisorDecision(action="blocked", reason=remediation.message, task=task, execution=remediation)
        return decision
    if mode in {"issue-only", "local-loop"}:
        return SupervisorDecision(action="executed", reason=execution.message, task=task, execution=execution)
    return SupervisorDecision(action="simulated", reason=execution.message, task=task, execution=execution)


def run_loop(
    config: OrchestratorConfig,
    mode: str,
    max_iterations: int | None = None,
    latest_run: bool = False,
    review_run_id: str | None = None,
    review_branch: str | None = None,
    review_commit: str | None = None,
    confirm_latest_run: bool = False,
) -> list[SupervisorDecision]:
    decisions: list[SupervisorDecision] = []
    iterations = max(1, max_iterations if max_iterations is not None else config.loop.max_iterations)
    skip_task_ids: set[str] = set()
    starting_branch = _current_branch(config.project.root)
    for _ in range(iterations):
        if mode == "local-loop" and not config.dry_run and not _worktree_clean(config.project.root):
            decision = SupervisorDecision(action="needs_manual_review", reason="Worktree is not clean; stopping before next iteration.")
            decisions.append(decision)
            break
        if mode == "local-loop" and not config.dry_run and starting_branch and _current_branch(config.project.root) != starting_branch:
            if not _switch_branch(config.project.root, starting_branch):
                decision = SupervisorDecision(action="needs_manual_review", reason=f"Could not switch back to starting branch `{starting_branch}`.")
                decisions.append(decision)
                break
        decision = run_once(
            config,
            mode,
            latest_run=latest_run,
            skip_task_ids=skip_task_ids,
            review_run_id=review_run_id,
            review_branch=review_branch,
            review_commit=review_commit,
            confirm_latest_run=confirm_latest_run,
        )
        append_decision(config.project.root / ".orchestrator/supervisor.log", decision, dry_run=config.dry_run)
        decisions.append(decision)
        if decision.task and decision.action in {"accept", "blocked", "executed", "simulated"}:
            skip_task_ids.add(decision.task.id)
        if mode in {"plan-only", "issue-only", "review-only"} or decision.action in {"stop", "needs_manual_review", "remediate"}:
            break
    return decisions


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the GitHub-backed orchestration supervisor.")
    parser.add_argument("--config", required=True)
    parser.add_argument("--mode", choices=["plan-only", "issue-only", "review-only", "loop-dry-run", "local-loop"], default="plan-only")
    parser.add_argument("--max-iterations", type=int)
    parser.add_argument("--latest-run", action="store_true", help="Review the latest run directory instead of selecting a new task.")
    parser.add_argument("--confirm-latest-run", action="store_true", help="Permit --latest-run to perform review after printing would otherwise stop.")
    parser.add_argument("--run-id", help="Review a specific run id.")
    parser.add_argument("--branch", help="Review the run for a specific worker branch.")
    parser.add_argument("--commit", help="Review the run for a specific worker head commit.")
    parser.add_argument("--non-dry-run", action="store_true", help="Allow external side effects where the selected mode supports them.")
    parser.add_argument("--allow-remediation", action="store_true", help="Allow one automated Codex remediation pass when supervisor requests it.")
    args = parser.parse_args(argv)
    if args.mode == "local-loop" and args.non_dry_run and (args.max_iterations is None or args.max_iterations < 1):
        parser.error("local-loop with --non-dry-run requires --max-iterations >= 1")
    config = load_config(Path(args.config))
    if args.non_dry_run:
        config = OrchestratorConfig(
            project=config.project,
            github=config.github,
            executor=ExecutorConfig(
                kind=config.executor.kind,
                command=config.executor.command,
                dry_run=False,
                branch_prefix=config.executor.branch_prefix,
                runs_dir=config.executor.runs_dir,
                timeout_seconds=config.executor.timeout_seconds,
            ),
            reviewer=ReviewerConfig(kind=config.reviewer.kind, model=config.reviewer.model, dry_run=False),
            supervisor=SupervisorEngineConfig(kind=config.supervisor.kind, model=config.supervisor.model, dry_run=False),
            loop=LoopConfig(max_iterations=config.loop.max_iterations, allow_remediation=config.loop.allow_remediation or args.allow_remediation),
            loop_budget=config.loop_budget,
            dry_run=False,
        )
    elif args.allow_remediation:
        config = OrchestratorConfig(
            project=config.project,
            github=config.github,
            executor=config.executor,
            reviewer=config.reviewer,
            supervisor=config.supervisor,
            loop=LoopConfig(max_iterations=config.loop.max_iterations, allow_remediation=True),
            loop_budget=config.loop_budget,
            dry_run=config.dry_run,
        )
    decisions = run_loop(
        config,
        args.mode,
        args.max_iterations,
        latest_run=args.latest_run,
        review_run_id=args.run_id,
        review_branch=args.branch,
        review_commit=args.commit,
        confirm_latest_run=args.confirm_latest_run,
    )
    for decision in decisions:
        print(f"action: {decision.action}")
        if decision.task:
            print(f"task: {decision.task.id} — {decision.task.title}")
        print(decision.reason)
        if decision.execution and decision.execution.issue_url:
            print(f"issue: {decision.execution.issue_url}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
