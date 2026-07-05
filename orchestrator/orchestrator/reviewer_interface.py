from __future__ import annotations

from abc import ABC, abstractmethod

from .schemas import ExecutionResult, ReviewResult


REVIEW_PROMPT = """You are a skeptical scientific reviewer for the Pinker Charts reconstruction project.

Project objective:
Produce faithful, reproducible, transparently sourced, and clearly extended
reconstructions of the original figures.

Completion is not assumed. Ask:
- Does the evidence justify the claimed status?
- Is there a reasonable next step that could materially improve this result?

If yes, require remediation unless the work is clearly a documented blocker
where automated progress is unlikely.

Review the submission package substantively. Do not merely check that files
exist. Score:
- data fidelity
- visual fidelity
- extension quality
- source recovery
- documentation accuracy
- status calibration
- remaining search opportunities

Return only valid JSON with these fields:
- decision: accept | remediate | blocked | needs_manual_review
- confidence: low | medium | high
- visual_review_performed: true | false
- data_review_performed: true | false
- documentation_review_performed: true | false
- scores: object with integer scores 1-5 for data_fidelity, visual_fidelity, extension_quality, source_recovery, documentation_accuracy, status_calibration
- missing_evidence
- strengths
- issues
- reasonable_next_steps
- required_remediation
- rationale
"""


class Reviewer(ABC):
    @abstractmethod
    def review(self, execution: ExecutionResult) -> ReviewResult:
        raise NotImplementedError
