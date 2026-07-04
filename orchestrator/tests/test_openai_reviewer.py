import json

import requests

from orchestrator.models.openai_reviewer import OpenAIReviewer, parse_review_json
from orchestrator.models.noop_reviewer import NoopReviewer
from orchestrator.schemas import ExecutionResult, Task
from orchestrator.supervisor import build_reviewer
from orchestrator.config import OrchestratorConfig, ProjectConfig, ReviewerConfig


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self.payload


class FakeHTTPErrorResponse:
    status_code = 400
    text = '{"error":{"message":"Bad request for diagnostics","type":"invalid_request_error","code":"invalid_model"}}'

    def json(self):
        return {"error": {"message": "Bad request for diagnostics", "type": "invalid_request_error", "code": "invalid_model"}}

    def raise_for_status(self):
        raise requests.HTTPError("400 Client Error: Bad Request", response=self)


def execution_result():
    task = Task(id="4-1", title="Tone of the News", status="not_started")
    return ExecutionResult(task=task, mode="review-gate", success=True, message="review packet")


def execution_result_with_run_dir(tmp_path):
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    packet = run_dir / "review_packet.md"
    packet.write_text("packet")
    task = Task(id="4-1", title="Tone of the News", status="not_started")
    return ExecutionResult(task=task, mode="review-gate", success=True, message="review packet", artifacts=(str(packet),)), run_dir


def test_parse_review_json_normalizes_valid_payload():
    parsed = parse_review_json(
        json.dumps(
            {
                "decision": "remediate",
                "confidence": "medium",
                "summary": "Almost complete.",
                "strengths": ["State updated"],
                "issues": ["Missing one artifact"],
                "required_remediation": ["Add comparison image"],
                "next_action": "Remediate and rerun review.",
            }
        )
    )
    assert parsed["decision"] == "remediate"
    assert parsed["confidence"] == "medium"
    assert parsed["issues"] == ["Missing one artifact"]


def test_parse_review_json_accepts_first_json_object_with_trailing_output():
    parsed = parse_review_json(
        json.dumps(
            {
                "decision": "blocked",
                "confidence": "medium",
                "summary": "Blocker documented.",
                "strengths": [],
                "issues": [],
                "required_remediation": [],
                "next_action": "Continue later.",
            }
        )
        + "\n"
        + json.dumps({"extra": "second object"})
    )
    assert parsed["decision"] == "blocked"
    assert parsed["summary"] == "Blocker documented."


def test_openai_reviewer_uses_mocked_response():
    def fake_post(*args, **kwargs):
        return FakeResponse(
            {
                "output_text": json.dumps(
                    {
                        "decision": "accept",
                        "confidence": "high",
                        "summary": "Task is complete.",
                        "strengths": ["Artifacts exist"],
                        "issues": [],
                        "required_remediation": [],
                        "next_action": "Supervisor may accept.",
                    }
                )
            }
        )

    reviewer = OpenAIReviewer(model="test-model", dry_run=False, api_key="test-key", post=fake_post)
    result = reviewer.review(execution_result())
    assert result.decision == "accept"
    assert result.confidence == "high"
    assert result.raw["parsed_result"]["next_action"] == "Supervisor may accept."
    assert "raw_model_response" in result.raw


def test_openai_reviewer_fails_safely_on_bad_json():
    def fake_post(*args, **kwargs):
        return FakeResponse({"output_text": "not json"})

    reviewer = OpenAIReviewer(model="test-model", dry_run=False, api_key="test-key", post=fake_post)
    result = reviewer.review(execution_result())
    assert result.decision == "needs_manual_review"
    assert result.confidence == "low"
    assert "failed safely" in result.summary


def test_openai_reviewer_missing_key_does_not_call_api():
    def fake_post(*args, **kwargs):
        raise AssertionError("OpenAI API should not be called without an API key")

    reviewer = OpenAIReviewer(model="test-model", dry_run=False, api_key="", post=fake_post)
    result = reviewer.review(execution_result())
    assert result.decision == "needs_manual_review"
    assert result.raw["parsed_result"]["decision"] == "needs_manual_review"


def test_openai_reviewer_persists_http_error_diagnostics(tmp_path):
    def fake_post(*args, **kwargs):
        return FakeHTTPErrorResponse()

    execution, run_dir = execution_result_with_run_dir(tmp_path)
    reviewer = OpenAIReviewer(model="bad-model", dry_run=False, api_key="test-key", post=fake_post)
    result = reviewer.review(execution)
    assert result.decision == "needs_manual_review"
    assert "HTTP status:\n400" in result.summary

    request = json.loads((run_dir / "openai_request.json").read_text())
    response = json.loads((run_dir / "openai_response.json").read_text())
    error_md = (run_dir / "openai_error.md").read_text()

    assert request["component"] == "reviewer"
    assert request["model"] == "bad-model"
    assert "Authorization" not in request["headers"]
    assert response["http_status"] == 400
    assert response["error_type"] == "invalid_request_error"
    assert response["error_code"] == "invalid_model"
    assert response["error_message"] == "Bad request for diagnostics"
    assert "Stack Trace" in error_md


def test_supervisor_uses_noop_when_openai_key_missing(monkeypatch, tmp_path):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    config = OrchestratorConfig(
        project=ProjectConfig(name="test", adapter="generic_csv", root=tmp_path, state_file=tmp_path / "PROJECT_STATE.md"),
        reviewer=ReviewerConfig(kind="openai", dry_run=False),
        dry_run=False,
    )
    assert isinstance(build_reviewer(config), NoopReviewer)
