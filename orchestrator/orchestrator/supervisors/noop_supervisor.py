from __future__ import annotations

from typing import Any

from ..schemas import SupervisorEngineResult, Task
from ..supervisor_interface import DecisionEngine


class NoopSupervisor(DecisionEngine):
    def decide(self, task: Task, context: dict[str, Any]) -> SupervisorEngineResult:
        return SupervisorEngineResult(
            task=task,
            supervisor="noop",
            decision="needs_manual_review",
            confidence="low",
            rationale="Noop supervisor did not make an autonomous acceptance decision.",
            registry_update="No registry update performed by supervisor.",
            next_action="Manual supervisor review required.",
            followup_task_prompt="",
            continue_loop=False,
            raw={"context_keys": sorted(context.keys())},
        )
