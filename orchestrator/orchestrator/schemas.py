from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any


class TaskStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    VERIFIED_REPRODUCTION = "verified_reproduction"
    UPDATED_EQUIVALENT = "updated_equivalent"
    PARTIAL_MATCH = "partial_match"
    SOURCE_CHAIN_RECOVERED = "source_chain_recovered"
    NEEDS_TARGETED_SOURCE_RECOVERY = "needs_targeted_source_recovery"
    BLOCKED_EXTERNAL_SOURCE = "blocked_external_source"
    MANUAL_REVIEW_NEEDED = "manual_review_needed"
    SOURCE_UNAVAILABLE = "source_unavailable"


COMPLETED_STATUSES = {
    TaskStatus.VERIFIED_REPRODUCTION.value,
    TaskStatus.UPDATED_EQUIVALENT.value,
    TaskStatus.PARTIAL_MATCH.value,
    TaskStatus.SOURCE_CHAIN_RECOVERED.value,
    TaskStatus.NEEDS_TARGETED_SOURCE_RECOVERY.value,
    TaskStatus.BLOCKED_EXTERNAL_SOURCE.value,
    TaskStatus.MANUAL_REVIEW_NEEDED.value,
    TaskStatus.SOURCE_UNAVAILABLE.value,
}


@dataclass(frozen=True)
class ProjectPaths:
    root: Path
    state_file: Path
    registry_file: Path | None = None
    review_manifest: Path | None = None

    def resolve(self, path: Path | str | None) -> Path | None:
        if path is None:
            return None
        p = Path(path)
        return p if p.is_absolute() else self.root / p


@dataclass(frozen=True)
class Task:
    id: str
    title: str
    status: str
    lifecycle_stage: str = ""
    priority: str = ""
    source_reference: str = ""
    next_action: str = ""
    files_to_update: tuple[str, ...] = ()
    acceptance_criteria: tuple[str, ...] = ()
    review_requirements: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ExecutionResult:
    task: Task
    mode: str
    success: bool
    message: str
    branch: str | None = None
    commit: str | None = None
    pr_url: str | None = None
    issue_url: str | None = None
    artifacts: tuple[str, ...] = ()


@dataclass(frozen=True)
class ReviewResult:
    task: Task
    reviewer: str
    decision: str
    summary: str
    findings: tuple[str, ...] = ()
    confidence: float | None = None
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class SupervisorDecision:
    action: str
    reason: str
    task: Task | None = None
    execution: ExecutionResult | None = None
    review: ReviewResult | None = None


@dataclass(frozen=True)
class IssueDraft:
    title: str
    body: str
    labels: tuple[str, ...] = ()
    assignees: tuple[str, ...] = ()


@dataclass(frozen=True)
class ProjectState:
    raw_state: str
    registry_rows: tuple[dict[str, str], ...] = ()
    review_manifest: dict[str, Any] | None = None
