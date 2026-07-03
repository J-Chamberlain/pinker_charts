from __future__ import annotations

import shlex

from ..executor_interface import Executor
from ..schemas import ExecutionResult, Task


class CodexCLIExecutor(Executor):
    def __init__(self, command: str | None = None, dry_run: bool = True) -> None:
        self.command = command or "codex"
        self.dry_run = dry_run

    def build_command(self, task: Task) -> str:
        prompt = f"Process task {task.id}: {task.title}. Follow repository workflow and commit one clean unit."
        return f"{shlex.quote(self.command)} exec {shlex.quote(prompt)}"

    def execute(self, task: Task) -> ExecutionResult:
        command = self.build_command(task)
        if self.dry_run:
            return ExecutionResult(task=task, mode="codex-cli-dry-run", success=True, message=f"Would run: {command}")
        return ExecutionResult(task=task, mode="codex-cli", success=False, message="Direct Codex CLI execution is intentionally stubbed; dry-run emits the verified `codex exec` command form.")
