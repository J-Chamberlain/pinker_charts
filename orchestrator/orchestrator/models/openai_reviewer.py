from __future__ import annotations

import json
import os
import re
from collections.abc import Callable
from pathlib import Path
from typing import Any

import requests

from ..openai_diagnostics import OpenAIDiagnosticError, call_openai_with_diagnostics
from ..reviewer_interface import REVIEW_PROMPT, Reviewer
from ..schemas import ExecutionResult, ReviewResult


ALLOWED_DECISIONS = {"accept", "remediate", "blocked", "needs_manual_review"}
ALLOWED_CONFIDENCE = {"low", "medium", "high"}


def _as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value]
    return [str(value)]


def _strip_json_fence(text: str) -> str:
    stripped = text.strip()
    match = re.fullmatch(r"```(?:json)?\s*(.*?)\s*```", stripped, flags=re.DOTALL)
    return match.group(1).strip() if match else stripped


def normalize_review_payload(payload: dict[str, Any]) -> dict[str, Any]:
    decision = payload.get("decision")
    confidence = payload.get("confidence")
    normalized = {
        "decision": decision if decision in ALLOWED_DECISIONS else "needs_manual_review",
        "confidence": confidence if confidence in ALLOWED_CONFIDENCE else "low",
        "summary": str(payload.get("summary") or "Reviewer did not provide a summary."),
        "strengths": _as_list(payload.get("strengths")),
        "issues": _as_list(payload.get("issues")),
        "required_remediation": _as_list(payload.get("required_remediation")),
        "next_action": str(payload.get("next_action") or "Manual supervisor review required."),
    }
    if normalized["decision"] != decision:
        normalized["issues"].append("Reviewer returned an invalid or missing decision.")
        normalized["required_remediation"].append("Inspect the raw reviewer response and classify manually.")
    if normalized["confidence"] != confidence:
        normalized["issues"].append("Reviewer returned an invalid or missing confidence value.")
    return normalized


def parse_review_json(text: str) -> dict[str, Any]:
    parsed = json.loads(_strip_json_fence(text))
    if not isinstance(parsed, dict):
        raise ValueError("Reviewer response JSON must be an object.")
    return normalize_review_payload(parsed)


class OpenAIReviewer(Reviewer):
    def __init__(
        self,
        model: str | None = None,
        dry_run: bool = True,
        api_key: str | None = None,
        post: Callable[..., Any] | None = None,
        timeout_seconds: int = 120,
    ) -> None:
        self.model = model or os.environ.get("OPENAI_REVIEWER_MODEL") or "gpt-5"
        self.dry_run = dry_run
        self.api_key = api_key if api_key is not None else os.environ.get("OPENAI_API_KEY")
        self.post = post or requests.post
        self.timeout_seconds = timeout_seconds

    def review(self, execution: ExecutionResult) -> ReviewResult:
        if self.dry_run:
            return self._manual_result(execution, "OpenAI reviewer is configured in dry-run mode.")
        if not self.api_key:
            return self._manual_result(execution, "OPENAI_API_KEY is not configured.")
        try:
            raw_text = self._call_openai(execution)
            parsed = parse_review_json(raw_text)
        except OpenAIDiagnosticError as exc:
            return self._manual_result(
                execution,
                exc.summary,
                raw={"error": exc.summary, "model": self.model, "openai_error": exc.diagnostic},
            )
        except Exception as exc:  # noqa: BLE001 - fail-safe reviewer gate
            return self._manual_result(
                execution,
                f"OpenAI reviewer failed safely: {exc}",
                raw={"error": str(exc), "model": self.model},
            )
        return ReviewResult(
            task=execution.task,
            reviewer="openai",
            decision=parsed["decision"],
            summary=parsed["summary"],
            findings=tuple(parsed["issues"]),
            confidence=parsed["confidence"],
            raw={
                "model": self.model,
                "raw_model_response": raw_text,
                "parsed_result": parsed,
            },
        )

    def _manual_result(self, execution: ExecutionResult, summary: str, raw: dict[str, Any] | None = None) -> ReviewResult:
        parsed = {
            "decision": "needs_manual_review",
            "confidence": "low",
            "summary": summary,
            "strengths": [],
            "issues": [summary],
            "required_remediation": ["Run a configured reviewer or inspect review_packet.md manually."],
            "next_action": "Manual supervisor review required.",
        }
        return ReviewResult(
            task=execution.task,
            reviewer="openai-unavailable",
            decision="needs_manual_review",
            summary=summary,
            findings=tuple(parsed["issues"]),
            confidence="low",
            raw={"model": self.model, "parsed_result": parsed, **(raw or {})},
        )

    def _call_openai(self, execution: ExecutionResult) -> str:
        payload = {
            "model": self.model,
            "input": [
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "input_text",
                            "text": REVIEW_PROMPT,
                        }
                    ],
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": self._build_user_prompt(execution),
                        }
                    ],
                },
            ],
        }
        run_dir = self._run_dir(execution)
        response = call_openai_with_diagnostics(
            component="reviewer",
            endpoint="https://api.openai.com/v1/responses",
            model=self.model,
            payload=payload,
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            timeout_seconds=self.timeout_seconds,
            post=self.post,
            run_dir=run_dir,
        )
        return self._extract_response_text(response.json())

    def _run_dir(self, execution: ExecutionResult) -> Path | None:
        if not execution.artifacts:
            return None
        return Path(execution.artifacts[0]).parent

    def _build_user_prompt(self, execution: ExecutionResult) -> str:
        return f"""Task id: {execution.task.id}
Task title: {execution.task.title}
Execution mode: {execution.mode}
Execution success flag: {execution.success}
Worker branch: {execution.branch or "not reported"}
Worker commit: {execution.commit or "not reported"}

Review packet:
{execution.message}
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
