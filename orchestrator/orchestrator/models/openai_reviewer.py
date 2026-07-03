from __future__ import annotations

import os

from ..reviewer_interface import REVIEW_PROMPT, Reviewer
from ..schemas import ExecutionResult, ReviewResult


class OpenAIReviewer(Reviewer):
    def __init__(self, model: str | None = None, dry_run: bool = True) -> None:
        self.model = model or "gpt-5"
        self.dry_run = dry_run

    def review(self, execution: ExecutionResult) -> ReviewResult:
        if self.dry_run or not os.environ.get("OPENAI_API_KEY"):
            return ReviewResult(
                task=execution.task,
                reviewer="openai-dry-run",
                decision="manual_review_needed",
                summary=f"Would call OpenAI model {self.model} with the standard review prompt.",
                findings=(REVIEW_PROMPT,),
                confidence=0.0,
            )
        return ReviewResult(
            task=execution.task,
            reviewer="openai-stub",
            decision="manual_review_needed",
            summary="OpenAI API call is intentionally not implemented in the scaffold; wire this to the preferred SDK in deployment.",
        )
