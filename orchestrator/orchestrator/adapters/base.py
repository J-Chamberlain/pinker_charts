from __future__ import annotations

from abc import ABC, abstractmethod

from ..schemas import ProjectState, Task


class ProjectAdapter(ABC):
    """Interface every project adapter should implement."""

    @abstractmethod
    def read_state(self) -> ProjectState:
        raise NotImplementedError

    @abstractmethod
    def tasks(self, state: ProjectState | None = None) -> list[Task]:
        raise NotImplementedError

    @abstractmethod
    def select_next_task(self, state: ProjectState | None = None) -> Task | None:
        raise NotImplementedError
