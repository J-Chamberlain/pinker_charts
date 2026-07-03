from __future__ import annotations

from ..executor_interface import Executor
from ..schemas import ExecutionResult, Task


class NoopExecutor(Executor):
    def execute(self, task: Task) -> ExecutionResult:
        return ExecutionResult(task=task, mode="noop", success=True, message=f"Dry-run executor selected task {task.id}.")
