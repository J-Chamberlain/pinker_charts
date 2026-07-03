from __future__ import annotations

import os

from ..reviewer_interface import REVIEW_PROMPT, Reviewer
from ..schemas import ExecutionResult, ReviewResult


class AnthropicReviewer(Reviewer):
    def __init__(self, model: str | None = None, dry_run: bool = True) -> None:
        self.model = model or "claude-sonnet"
        self.dry_run = dry_run

    def review(self, execution: ExecutionResult) -> ReviewResult:
        if self.dry_run or not os.environ.get("ANTHROPIC_API_KEY"):
            return ReviewResult(
                task=execution.task,
                reviewer="anthropic-dry-run",
                decision="manual_review_needed",
                summary=f"Would call Anthropic model {self.model} with the standard review prompt.",
                findings=(REVIEW_PROMPT,),
                confidence=0.0,
            )
        return ReviewResult(
            task=execution.task,
            reviewer="anthropic-stub",
            decision="manual_review_needed",
            summary="Anthropic API call is intentionally not implemented in the scaffold; wire this to the preferred SDK in deployment.",
        )
