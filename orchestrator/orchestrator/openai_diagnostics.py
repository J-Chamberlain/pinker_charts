from __future__ import annotations

import json
import traceback
from collections.abc import Callable
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import requests


class OpenAIDiagnosticError(RuntimeError):
    def __init__(self, summary: str, diagnostic: dict[str, Any]) -> None:
        super().__init__(summary)
        self.summary = summary
        self.diagnostic = diagnostic


def _redact(value: Any) -> Any:
    if isinstance(value, dict):
        redacted = {}
        for key, item in value.items():
            lowered = str(key).lower()
            if lowered in {"authorization", "api_key", "apikey"} or "api_key" in lowered:
                redacted[key] = "[redacted]"
            else:
                redacted[key] = _redact(item)
        return redacted
    if isinstance(value, list):
        return [_redact(item) for item in value]
    return value


def _sanitize_headers(headers: dict[str, str]) -> dict[str, str]:
    return {key: value for key, value in headers.items() if key.lower() != "authorization"}


def _safe_response_body(response: Any) -> Any:
    try:
        return response.json()
    except Exception:  # noqa: BLE001 - diagnostic fallback
        return {"raw_text": getattr(response, "text", "")}


def _openai_error_fields(body: Any) -> tuple[str | None, str | None, str | None]:
    if isinstance(body, dict) and isinstance(body.get("error"), dict):
        error = body["error"]
        return error.get("type"), error.get("code"), error.get("message")
    return None, None, None


def _endpoint_path(endpoint: str) -> str:
    parsed = urlparse(endpoint)
    return parsed.path or endpoint


def _write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, default=str) + "\n")


def _write_error_markdown(path: Path, diagnostic: dict[str, Any]) -> None:
    path.write_text(
        f"""# OpenAI API Request Failed

- Component: `{diagnostic.get("component")}`
- HTTP status: `{diagnostic.get("http_status")}`
- Model: `{diagnostic.get("model")}`
- Endpoint: `{diagnostic.get("endpoint_path")}`
- Error type: `{diagnostic.get("error_type")}`
- Error code: `{diagnostic.get("error_code")}`
- Error message: {diagnostic.get("error_message")}

## Stack Trace

```text
{diagnostic.get("stack_trace")}
```
"""
    )


def format_openai_failure(diagnostic: dict[str, Any]) -> str:
    return f"""OpenAI API request failed
HTTP status:
{diagnostic.get("http_status")}
Model:
{diagnostic.get("model")}
Endpoint:
{diagnostic.get("endpoint_path")}
Error type:
{diagnostic.get("error_type")}
Error code:
{diagnostic.get("error_code")}
Error message:
{diagnostic.get("error_message")}"""


def call_openai_with_diagnostics(
    *,
    component: str,
    endpoint: str,
    model: str,
    payload: dict[str, Any],
    headers: dict[str, str],
    timeout_seconds: int,
    post: Callable[..., Any],
    run_dir: Path | None,
) -> Any:
    endpoint_path = _endpoint_path(endpoint)
    print(f"Selected {component}: openai")
    print(f"Configured model: {model}")
    print(f"OpenAI endpoint: {endpoint_path}")
    request_payload = {
        "component": component,
        "endpoint": endpoint,
        "endpoint_path": endpoint_path,
        "model": model,
        "headers": _sanitize_headers(headers),
        "payload": _redact(payload),
    }
    if run_dir:
        _write_json(run_dir / "openai_request.json", request_payload)
    try:
        response = post(endpoint, headers=headers, json=payload, timeout=timeout_seconds)
        response.raise_for_status()
        return response
    except Exception as exc:  # noqa: BLE001 - preserve full diagnostics
        response = getattr(exc, "response", None)
        status = getattr(response, "status_code", None)
        response_body = _safe_response_body(response) if response is not None else {"error": str(exc)}
        error_type, error_code, error_message = _openai_error_fields(response_body)
        diagnostic = {
            "component": component,
            "http_status": status,
            "response_body": response_body,
            "error_type": error_type,
            "error_code": error_code,
            "error_message": error_message or str(exc),
            "endpoint": endpoint,
            "endpoint_path": endpoint_path,
            "model": model,
            "request": request_payload,
            "stack_trace": traceback.format_exc(),
        }
        if run_dir:
            _write_json(run_dir / "openai_response.json", diagnostic)
            _write_error_markdown(run_dir / "openai_error.md", diagnostic)
        summary = format_openai_failure(diagnostic)
        print(summary)
        raise OpenAIDiagnosticError(summary, diagnostic) from exc
