from __future__ import annotations

from collections.abc import Iterable

from .schemas import COMPLETED_STATUSES, Task


def is_unprocessed(status: str) -> bool:
    return status == "not_started" or status == ""


def status_class(status: str) -> str:
    if is_unprocessed(status):
        return "unprocessed"
    if status in COMPLETED_STATUSES:
        return "terminal_or_documented"
    return "active"


def select_first_unprocessed(tasks: Iterable[Task]) -> Task | None:
    for task in tasks:
        if is_unprocessed(task.status):
            return task
    return None


def select_by_priority(tasks: Iterable[Task], preferred_source_families: set[str] | None = None) -> Task | None:
    candidates = [task for task in tasks if is_unprocessed(task.status)]
    if not candidates:
        return None
    if preferred_source_families:
        for task in candidates:
            if task.metadata.get("source_type_guess") in preferred_source_families:
                return task
    return candidates[0]
