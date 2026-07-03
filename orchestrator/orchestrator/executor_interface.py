from __future__ import annotations

from abc import ABC, abstractmethod

from .schemas import ExecutionResult, Task


class Executor(ABC):
    @abstractmethod
    def execute(self, task: Task) -> ExecutionResult:
        raise NotImplementedError
