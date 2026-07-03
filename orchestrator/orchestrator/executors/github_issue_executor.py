from __future__ import annotations

from ..executor_interface import Executor
from ..github_client import GitHubClient
from ..issue_queue import build_issue_draft, create_issue
from ..schemas import ExecutionResult, Task


class GitHubIssueExecutor(Executor):
    def __init__(self, client: GitHubClient | None, labels: tuple[str, ...] = (), dry_run: bool = True) -> None:
        self.client = client
        self.labels = labels
        self.dry_run = dry_run

    def execute(self, task: Task) -> ExecutionResult:
        draft = build_issue_draft(task, labels=self.labels)
        if self.client is None and not self.dry_run:
            return ExecutionResult(task=task, mode="github-issue", success=False, message="GitHub client is not configured.")
        if self.client is not None and not self.dry_run and not self.client.config.token:
            return ExecutionResult(
                task=task,
                mode="github-issue",
                success=False,
                message=f"Missing GitHub token in {self.client.config.token_env}; refusing to create issue.",
            )
        result = create_issue(self.client, draft, dry_run=self.dry_run) if self.client else {"dry_run": "true", "title": draft.title, "body": draft.body}
        return ExecutionResult(
            task=task,
            mode="github-issue-dry-run" if self.dry_run else "github-issue",
            success=True,
            message=result.get("body", result.get("title", "issue created")),
            issue_url=result.get("url"),
        )
