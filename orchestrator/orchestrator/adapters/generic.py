from __future__ import annotations

from pathlib import Path

from .base import ProjectAdapter
from ..schemas import ProjectState, Task
from ..state_reader import read_project_state
from ..task_selector import select_first_unprocessed


class GenericCsvAdapter(ProjectAdapter):
    """Minimal CSV-backed adapter for future projects.

    Expected registry columns: `id` or `figure_id`, `title`, and `status` or
    `current_status`. Extra columns are carried through in task metadata.
    """

    def __init__(self, root: Path, state_file: Path, registry_file: Path | None = None, review_manifest: Path | None = None) -> None:
        self.root = root
        self.state_file = state_file
        self.registry_file = registry_file
        self.review_manifest = review_manifest

    def read_state(self) -> ProjectState:
        return read_project_state(self.state_file, self.registry_file, self.review_manifest)

    def tasks(self, state: ProjectState | None = None) -> list[Task]:
        state = state or self.read_state()
        tasks: list[Task] = []
        for row in state.registry_rows:
            task_id = row.get("id") or row.get("figure_id") or row.get("task_id") or ""
            title = row.get("title") or row.get("name") or task_id
            status = row.get("status") or row.get("current_status") or "not_started"
            tasks.append(Task(id=task_id, title=title, status=status, metadata=row))
        return tasks

    def select_next_task(self, state: ProjectState | None = None) -> Task | None:
        return select_first_unprocessed(self.tasks(state))
