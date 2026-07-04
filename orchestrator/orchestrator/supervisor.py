from __future__ import annotations

import argparse
import os
from pathlib import Path

from .adapters import GenericCsvAdapter, PinkerChartsAdapter
from .config import OrchestratorConfig, load_config
from .config import ExecutorConfig, LoopConfig, ReviewerConfig, SupervisorEngineConfig
from .executors import CodexCLIExecutor, GitHubIssueExecutor, NoopExecutor
from .github_client import GitHubClient
from .issue_queue import build_issue_draft
from .models import AnthropicReviewer, NoopReviewer, OpenAIReviewer
from .review_gate import latest_run_dir, run_review_gate
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


def run_once(config: OrchestratorConfig, mode: str, latest_run: bool = False, skip_task_ids: set[str] | None = None) -> SupervisorDecision:
    task, adapter, state = select_task(config, skip_task_ids)
    if not task:
        return SupervisorDecision(action="stop", reason="No eligible task found.")
    if mode == "plan-only":
        return SupervisorDecision(action="plan", reason=plan_task(task), task=task)
    if mode == "review-only":
        runs_dir = config.executor.runs_dir or config.project.root / "orchestrator/runs"
        run_dir = latest_run_dir(runs_dir) if latest_run else None
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
        decision = run_review_gate(
            config.project.root,
            config.executor.runs_dir or config.project.root / "orchestrator/runs",
            task,
            reviewer,
            decision_engine=build_decision_engine(config),
            project_state=adapter.read_state(),
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
                    config.executor.runs_dir or config.project.root / "orchestrator/runs",
                    task,
                    reviewer,
                    decision_engine=build_decision_engine(config),
                    project_state=adapter.read_state(),
                    dry_run=config.dry_run,
                    push_branch=True,
                    allow_remediation=False,
                )
            return SupervisorDecision(action="blocked", reason=remediation.message, task=task, execution=remediation)
        return decision
    if mode in {"issue-only", "local-loop"}:
        return SupervisorDecision(action="executed", reason=execution.message, task=task, execution=execution)
    return SupervisorDecision(action="simulated", reason=execution.message, task=task, execution=execution)


def run_loop(config: OrchestratorConfig, mode: str, max_iterations: int | None = None, latest_run: bool = False) -> list[SupervisorDecision]:
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
        decision = run_once(config, mode, latest_run=latest_run, skip_task_ids=skip_task_ids)
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
    decisions = run_loop(config, args.mode, args.max_iterations, latest_run=args.latest_run)
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
