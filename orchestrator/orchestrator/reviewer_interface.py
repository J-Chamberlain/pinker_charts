from __future__ import annotations

from abc import ABC, abstractmethod

from .schemas import ExecutionResult, ReviewResult


REVIEW_PROMPT = """Review this completed unit of work.

Evaluate:
- whether Codex completed the assigned task
- whether project state and registry files were updated when required
- whether generated artifacts exist where applicable
- whether status labels are calibrated to the evidence
- data fidelity
- visual fidelity
- extension quality
- documentation accuracy

Return only valid JSON with these fields:
- decision: accept | remediate | blocked | needs_manual_review
- confidence: low | medium | high
- summary
- strengths
- issues
- required_remediation
- next_action
"""


class Reviewer(ABC):
    @abstractmethod
    def review(self, execution: ExecutionResult) -> ReviewResult:
        raise NotImplementedError
