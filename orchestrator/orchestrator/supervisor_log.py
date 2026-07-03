from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from .schemas import SupervisorDecision


def format_decision(decision: SupervisorDecision) -> str:
    task = f"{decision.task.id} — {decision.task.title}" if decision.task else "none"
    return f"{datetime.now(UTC).isoformat()} | action={decision.action} | task={task} | reason={decision.reason.splitlines()[0]}"


def append_decision(log_file: Path, decision: SupervisorDecision, dry_run: bool = True) -> None:
    if dry_run:
        return
    log_file.parent.mkdir(parents=True, exist_ok=True)
    with log_file.open("a") as handle:
        handle.write(format_decision(decision) + "\n")
