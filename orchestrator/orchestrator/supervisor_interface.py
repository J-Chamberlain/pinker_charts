from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from .schemas import SupervisorEngineResult, Task


SUPERVISOR_PROMPT = """You are the supervisor for a GitHub-backed research/code agent loop.

Decide what should happen after a worker run and reviewer result.

Evaluate:
- whether the worker completed the assigned task or documented a blocker
- whether the reviewer result supports accepting the work
- whether registry and project state updates are present when expected
- whether status labels are calibrated
- whether remediation can be automated safely
- whether the loop may continue to another task

Distinguish these cases:
- accepted because the scientific objective is met
- accepted as a documented blocker
- remediated because evidence is insufficient
- blocked because automated progress is unlikely

Return only valid JSON with these fields:
- decision: accept | remediate | blocked | needs_manual_review
- confidence: low | medium | high
- decision_basis: scientific_objective_met | documented_blocker | evidence_insufficient | automated_progress_unlikely | manual_review_required
- rationale
- registry_update
- next_action
- followup_task_prompt
- continue_loop: true | false
"""


class DecisionEngine(ABC):
    @abstractmethod
    def decide(self, task: Task, context: dict[str, Any]) -> SupervisorEngineResult:
        raise NotImplementedError
