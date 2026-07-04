from __future__ import annotations

import argparse
import os
from pathlib import Path

from .adapters import GenericCsvAdapter, PinkerChartsAdapter
from .config import OrchestratorConfig, load_config
from .config import ExecutorConfig, ReviewerConfig
from .executors import CodexCLIExecutor, GitHubIssueExecutor, NoopExecutor
from .github_client import GitHubClient
from .issue_queue import build_issue_draft
from .models import AnthropicReviewer, NoopReviewer, OpenAIReviewer
from .review_gate import latest_run_dir, run_review_gate
from .schemas import ExecutionResult, SupervisorDecision, Task
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


def run_once(config: OrchestratorConfig, mode: str, latest_run: bool = False) -> SupervisorDecision:
    adapter = build_adapter(config)
    state = adapter.read_state()
    task = adapter.select_next_task(state)
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
            run_dir=run_dir,
            dry_run=config.dry_run,
            push_branch=not config.dry_run,
        )
    executor = build_executor(config, mode)
    execution = executor.execute(task)
    if mode == "local-loop" and not config.dry_run and execution.artifacts:
        reviewer = build_reviewer(config)
        return run_review_gate(
            config.project.root,
            config.executor.runs_dir or config.project.root / "orchestrator/runs",
            task,
            reviewer,
            dry_run=config.dry_run,
            push_branch=True,
        )
    if mode in {"issue-only", "local-loop"}:
        return SupervisorDecision(action="executed", reason=execution.message, task=task, execution=execution)
    return SupervisorDecision(action="simulated", reason=execution.message, task=task, execution=execution)


def run_loop(config: OrchestratorConfig, mode: str, max_iterations: int | None = None, latest_run: bool = False) -> list[SupervisorDecision]:
    decisions: list[SupervisorDecision] = []
    iterations = max(1, max_iterations if max_iterations is not None else config.loop_budget)
    for _ in range(iterations):
        decision = run_once(config, mode, latest_run=latest_run)
        append_decision(config.project.root / ".orchestrator/supervisor.log", decision, dry_run=config.dry_run)
        decisions.append(decision)
        if mode in {"plan-only", "issue-only", "review-only"} or decision.action == "stop":
            break
    return decisions


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the GitHub-backed orchestration supervisor.")
    parser.add_argument("--config", required=True)
    parser.add_argument("--mode", choices=["plan-only", "issue-only", "review-only", "loop-dry-run", "local-loop"], default="plan-only")
    parser.add_argument("--max-iterations", type=int)
    parser.add_argument("--latest-run", action="store_true", help="Review the latest run directory instead of selecting a new task.")
    parser.add_argument("--non-dry-run", action="store_true", help="Allow external side effects where the selected mode supports them.")
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
            loop_budget=config.loop_budget,
            dry_run=False,
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
