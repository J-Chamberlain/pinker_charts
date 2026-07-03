from __future__ import annotations

from abc import ABC, abstractmethod

from .schemas import ExecutionResult, ReviewResult


REVIEW_PROMPT = """Review this completed unit of work.

Evaluate:
- data fidelity
- visual fidelity
- extension quality
- documentation accuracy
- status calibration

Return a decision: accept, remediate, or reject.
"""


class Reviewer(ABC):
    @abstractmethod
    def review(self, execution: ExecutionResult) -> ReviewResult:
        raise NotImplementedError
