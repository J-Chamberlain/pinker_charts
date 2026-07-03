from __future__ import annotations

import argparse
from pathlib import Path

from .adapters import GenericCsvAdapter, PinkerChartsAdapter
from .config import OrchestratorConfig, load_config
from .config import ExecutorConfig, ReviewerConfig
from .executors import CodexCLIExecutor, GitHubIssueExecutor, NoopExecutor
from .github_client import GitHubClient
from .issue_queue import build_issue_draft
from .models import AnthropicReviewer, NoopReviewer, OpenAIReviewer
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
    if config.executor.kind == "codex_cli":
        return CodexCLIExecutor(command=config.executor.command, dry_run=config.dry_run or config.executor.dry_run)
    return NoopExecutor()


def build_reviewer(config: OrchestratorConfig):
    if config.reviewer.kind == "openai":
        return OpenAIReviewer(model=config.reviewer.model, dry_run=config.dry_run or config.reviewer.dry_run)
    if config.reviewer.kind == "anthropic":
        return AnthropicReviewer(model=config.reviewer.model, dry_run=config.dry_run or config.reviewer.dry_run)
    return NoopReviewer()


def plan_task(task: Task) -> str:
    draft = build_issue_draft(task)
    return f"{draft.title}\n\n{draft.body}"


def run_once(config: OrchestratorConfig, mode: str) -> SupervisorDecision:
    adapter = build_adapter(config)
    state = adapter.read_state()
    task = adapter.select_next_task(state)
    if not task:
        return SupervisorDecision(action="stop", reason="No eligible task found.")
    if mode == "plan-only":
        return SupervisorDecision(action="plan", reason=plan_task(task), task=task)
    executor = build_executor(config, mode)
    execution = executor.execute(task)
    if mode in {"issue-only", "local-loop"}:
        return SupervisorDecision(action="executed", reason=execution.message, task=task, execution=execution)
    if mode == "review-only":
        review = build_reviewer(config).review(ExecutionResult(task=task, mode="review-placeholder", success=True, message="review-only"))
        return SupervisorDecision(action="reviewed", reason=review.summary, task=task, review=review)
    return SupervisorDecision(action="simulated", reason=execution.message, task=task, execution=execution)


def run_loop(config: OrchestratorConfig, mode: str) -> list[SupervisorDecision]:
    decisions: list[SupervisorDecision] = []
    iterations = max(1, config.loop_budget)
    for _ in range(iterations):
        decision = run_once(config, mode)
        append_decision(config.project.root / ".orchestrator/supervisor.log", decision, dry_run=config.dry_run)
        decisions.append(decision)
        if mode in {"plan-only", "issue-only", "review-only"} or decision.action == "stop":
            break
    return decisions


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the GitHub-backed orchestration supervisor.")
    parser.add_argument("--config", required=True)
    parser.add_argument("--mode", choices=["plan-only", "issue-only", "review-only", "loop-dry-run", "local-loop"], default="plan-only")
    parser.add_argument("--non-dry-run", action="store_true", help="Allow external side effects where the selected mode supports them.")
    args = parser.parse_args(argv)
    config = load_config(Path(args.config))
    if args.non_dry_run:
        config = OrchestratorConfig(
            project=config.project,
            github=config.github,
            executor=ExecutorConfig(kind=config.executor.kind, command=config.executor.command, dry_run=False),
            reviewer=ReviewerConfig(kind=config.reviewer.kind, model=config.reviewer.model, dry_run=False),
            loop_budget=config.loop_budget,
            dry_run=False,
        )
    decisions = run_loop(config, args.mode)
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
