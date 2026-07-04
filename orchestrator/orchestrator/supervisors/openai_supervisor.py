from __future__ import annotations

import json
import os
import re
from collections.abc import Callable
from pathlib import Path
from typing import Any

import requests

from ..openai_diagnostics import OpenAIDiagnosticError, call_openai_with_diagnostics
from ..schemas import SupervisorEngineResult, Task
from ..supervisor_interface import SUPERVISOR_PROMPT, DecisionEngine


ALLOWED_DECISIONS = {"accept", "remediate", "blocked", "needs_manual_review"}
ALLOWED_CONFIDENCE = {"low", "medium", "high"}


def _strip_json_fence(text: str) -> str:
    stripped = text.strip()
    match = re.fullmatch(r"```(?:json)?\s*(.*?)\s*```", stripped, flags=re.DOTALL)
    return match.group(1).strip() if match else stripped


def normalize_supervisor_payload(payload: dict[str, Any]) -> dict[str, Any]:
    decision = payload.get("decision")
    confidence = payload.get("confidence")
    continue_loop = payload.get("continue_loop")
    normalized = {
        "decision": decision if decision in ALLOWED_DECISIONS else "needs_manual_review",
        "confidence": confidence if confidence in ALLOWED_CONFIDENCE else "low",
        "rationale": str(payload.get("rationale") or "Supervisor did not provide a rationale."),
        "registry_update": str(payload.get("registry_update") or "No registry update specified."),
        "next_action": str(payload.get("next_action") or "Manual supervisor review required."),
        "followup_task_prompt": str(payload.get("followup_task_prompt") or ""),
        "continue_loop": bool(continue_loop) if isinstance(continue_loop, bool) else False,
    }
    if normalized["decision"] != decision:
        normalized["decision"] = "needs_manual_review"
        normalized["continue_loop"] = False
        normalized["rationale"] += " Invalid or missing decision forced manual review."
    if normalized["confidence"] != confidence:
        normalized["confidence"] = "low"
    if normalized["decision"] in {"remediate", "needs_manual_review"}:
        normalized["continue_loop"] = False
    return normalized


def parse_supervisor_json(text: str) -> dict[str, Any]:
    parsed = json.loads(_strip_json_fence(text))
    if not isinstance(parsed, dict):
        raise ValueError("Supervisor response JSON must be an object.")
    return normalize_supervisor_payload(parsed)


class OpenAISupervisor(DecisionEngine):
    def __init__(
        self,
        model: str | None = None,
        dry_run: bool = True,
        api_key: str | None = None,
        post: Callable[..., Any] | None = None,
        timeout_seconds: int = 120,
    ) -> None:
        self.model = model or os.environ.get("OPENAI_SUPERVISOR_MODEL") or "gpt-5"
        self.dry_run = dry_run
        self.api_key = api_key if api_key is not None else os.environ.get("OPENAI_API_KEY")
        self.post = post or requests.post
        self.timeout_seconds = timeout_seconds

    def decide(self, task: Task, context: dict[str, Any]) -> SupervisorEngineResult:
        if self.dry_run:
            return self._manual_result(task, "OpenAI supervisor is configured in dry-run mode.")
        if not self.api_key:
            return self._manual_result(task, "OPENAI_API_KEY is not configured.")
        try:
            raw_text = self._call_openai(task, context)
            parsed = parse_supervisor_json(raw_text)
        except OpenAIDiagnosticError as exc:
            return self._manual_result(
                task,
                exc.summary,
                raw={"error": exc.summary, "model": self.model, "openai_error": exc.diagnostic},
            )
        except Exception as exc:  # noqa: BLE001 - fail-safe decision engine
            return self._manual_result(
                task,
                f"OpenAI supervisor failed safely: {exc}",
                raw={"error": str(exc), "model": self.model},
            )
        return SupervisorEngineResult(
            task=task,
            supervisor="openai",
            decision=parsed["decision"],
            confidence=parsed["confidence"],
            rationale=parsed["rationale"],
            registry_update=parsed["registry_update"],
            next_action=parsed["next_action"],
            followup_task_prompt=parsed["followup_task_prompt"],
            continue_loop=parsed["continue_loop"],
            raw={"model": self.model, "raw_model_response": raw_text, "parsed_result": parsed},
        )

    def _manual_result(self, task: Task, rationale: str, raw: dict[str, Any] | None = None) -> SupervisorEngineResult:
        parsed = {
            "decision": "needs_manual_review",
            "confidence": "low",
            "rationale": rationale,
            "registry_update": "No registry update performed by supervisor.",
            "next_action": "Manual supervisor review required.",
            "followup_task_prompt": "",
            "continue_loop": False,
        }
        return SupervisorEngineResult(
            task=task,
            supervisor="openai-unavailable",
            decision="needs_manual_review",
            confidence="low",
            rationale=rationale,
            registry_update=parsed["registry_update"],
            next_action=parsed["next_action"],
            followup_task_prompt="",
            continue_loop=False,
            raw={"model": self.model, "parsed_result": parsed, **(raw or {})},
        )

    def _call_openai(self, task: Task, context: dict[str, Any]) -> str:
        payload = {
            "model": self.model,
            "input": [
                {"role": "system", "content": [{"type": "input_text", "text": SUPERVISOR_PROMPT}]},
                {"role": "user", "content": [{"type": "input_text", "text": self._build_user_prompt(task, context)}]},
            ],
        }
        response = call_openai_with_diagnostics(
            component="supervisor",
            endpoint="https://api.openai.com/v1/responses",
            model=self.model,
            payload=payload,
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            timeout_seconds=self.timeout_seconds,
            post=self.post,
            run_dir=self._run_dir(context),
        )
        return self._extract_response_text(response.json())

    def _run_dir(self, context: dict[str, Any]) -> Path | None:
        run_dir = context.get("run_dir")
        return Path(run_dir) if run_dir else None

    def _build_user_prompt(self, task: Task, context: dict[str, Any]) -> str:
        return f"""Task id: {task.id}
Task title: {task.title}

Supervisor context JSON:
{json.dumps(context, indent=2, default=str)}
"""

    def _extract_response_text(self, data: dict[str, Any]) -> str:
        if isinstance(data.get("output_text"), str):
            return data["output_text"]
        chunks: list[str] = []
        for item in data.get("output", []):
            for content in item.get("content", []):
                if isinstance(content, dict) and isinstance(content.get("text"), str):
                    chunks.append(content["text"])
        if chunks:
            return "\n".join(chunks)
        choices = data.get("choices", [])
        if choices and isinstance(choices[0], dict):
            message = choices[0].get("message", {})
            if isinstance(message, dict) and isinstance(message.get("content"), str):
                return message["content"]
        raise ValueError("OpenAI response did not contain text output.")
