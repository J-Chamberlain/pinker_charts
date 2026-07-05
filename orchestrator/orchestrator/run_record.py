from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def utc_now() -> str:
    return datetime.now(UTC).isoformat()


@dataclass
class RunRecord:
    run_id: str
    task_id: str
    task_title: str
    base_branch: str
    base_sha: str
    worker_branch: str
    head_sha: str | None = None
    parent_run_id: str | None = None
    run_type: str = "initial"
    executor_status: str = "pending"
    worker_made_commit: bool = False
    dirty_worktree_files: list[str] = field(default_factory=list)
    changed_files: list[str] = field(default_factory=list)
    reviewer_status: str = "pending"
    supervisor_status: str = "pending"
    final_action: str = "pending"
    created_at: str = field(default_factory=utc_now)
    completed_at: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "RunRecord":
        return cls(
            run_id=str(payload.get("run_id") or ""),
            task_id=str(payload.get("task_id") or ""),
            task_title=str(payload.get("task_title") or ""),
            base_branch=str(payload.get("base_branch") or ""),
            base_sha=str(payload.get("base_sha") or ""),
            worker_branch=str(payload.get("worker_branch") or ""),
            head_sha=payload.get("head_sha"),
            parent_run_id=payload.get("parent_run_id"),
            run_type=str(payload.get("run_type") or "initial"),
            executor_status=str(payload.get("executor_status") or "pending"),
            worker_made_commit=bool(payload.get("worker_made_commit")),
            dirty_worktree_files=list(payload.get("dirty_worktree_files") or []),
            changed_files=list(payload.get("changed_files") or []),
            reviewer_status=str(payload.get("reviewer_status") or "pending"),
            supervisor_status=str(payload.get("supervisor_status") or "pending"),
            final_action=str(payload.get("final_action") or "pending"),
            created_at=str(payload.get("created_at") or utc_now()),
            completed_at=payload.get("completed_at"),
        )

    def save(self, run_dir: Path) -> Path:
        path = run_dir / "run_record.json"
        path.write_text(json.dumps(self.to_dict(), indent=2, default=str) + "\n")
        return path


def load_run_record(run_dir: Path) -> RunRecord | None:
    path = run_dir / "run_record.json"
    if not path.exists():
        return None
    return RunRecord.from_dict(json.loads(path.read_text()))


def is_reviewable(record: RunRecord) -> tuple[bool, str]:
    if not record.base_sha:
        return False, "missing_base_sha"
    if not record.head_sha:
        return False, "missing_head_sha"
    if record.dirty_worktree_files:
        return False, "dirty_worktree_after_executor"
    if record.head_sha == record.base_sha:
        return False, "head_sha_equals_base_sha"
    if not record.worker_made_commit:
        return False, "worker_made_no_commit"
    if not record.changed_files:
        return False, "empty_changed_files"
    return True, "reviewable"


def update_run_record(run_dir: Path, **updates: Any) -> RunRecord | None:
    record = load_run_record(run_dir)
    if record is None:
        return None
    for key, value in updates.items():
        if hasattr(record, key):
            setattr(record, key, value)
    record.save(run_dir)
    return record
