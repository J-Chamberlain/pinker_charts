from __future__ import annotations

from ..reviewer_interface import Reviewer
from ..schemas import ExecutionResult, ReviewResult


class NoopReviewer(Reviewer):
    def review(self, execution: ExecutionResult) -> ReviewResult:
        return ReviewResult(
            task=execution.task,
            reviewer="noop",
            decision="accept",
            summary="Dry-run reviewer did not call an external model.",
            findings=("No external review performed.",),
            confidence=0.0,
        )
