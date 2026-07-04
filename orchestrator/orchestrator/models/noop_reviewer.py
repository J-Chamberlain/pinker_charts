from __future__ import annotations

from ..reviewer_interface import Reviewer
from ..schemas import ExecutionResult, ReviewResult


class NoopReviewer(Reviewer):
    def review(self, execution: ExecutionResult) -> ReviewResult:
        return ReviewResult(
            task=execution.task,
            reviewer="noop",
            decision="needs_manual_review",
            summary="Noop reviewer generated a manual-review decision without calling an external model.",
            findings=(
                "No external review performed.",
                "Supervisor must not accept until a configured reviewer or human has reviewed the packet.",
            ),
            confidence=0.0,
        )
