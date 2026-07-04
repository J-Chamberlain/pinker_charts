import json
from pathlib import Path

from orchestrator.config import OrchestratorConfig, ProjectConfig, SupervisorEngineConfig, load_config
from orchestrator.review_gate import run_review_gate
from orchestrator.schemas import ReviewResult, SupervisorEngineResult, Task
from orchestrator.supervisor import build_decision_engine, run_loop
from orchestrator.supervisor_interface import DecisionEngine
from orchestrator.supervisors import NoopSupervisor, OpenAISupervisor
from orchestrator.supervisors.openai_supervisor import parse_supervisor_json


ROOT = Path(__file__).resolve().parents[2]


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self.payload


class StaticReviewer:
    def __init__(self, decision="accept"):
        self.decision = decision

    def review(self, execution):
        return ReviewResult(task=execution.task, reviewer="static", decision=self.decision, summary=f"review {self.decision}", confidence="high")


class StaticSupervisor(DecisionEngine):
    def __init__(self, result_decision: str):
        self.result_decision = result_decision

    def decide(self, task: Task, context):
        return SupervisorEngineResult(
            task=task,
            supervisor="static",
            decision=self.result_decision,
            confidence="high",
            rationale=f"static {self.result_decision}",
            registry_update="No registry update.",
            next_action=self.result_decision,
            followup_task_prompt="Fix the documented issue." if self.result_decision == "remediate" else "",
            continue_loop=self.result_decision in {"accept", "blocked"},
            raw={"parsed_result": {"decision": self.result_decision}},
        )


def test_noop_supervisor_requires_manual_review():
    task = Task(id="x", title="Example", status="not_started")
    result = NoopSupervisor().decide(task, {"reviewer_result": {}})
    assert result.decision == "needs_manual_review"
    assert not result.continue_loop


def test_openai_supervisor_uses_mocked_response():
    def fake_post(*args, **kwargs):
        return FakeResponse(
            {
                "output_text": json.dumps(
                    {
                        "decision": "accept",
                        "confidence": "high",
                        "rationale": "Worker and reviewer evidence are sufficient.",
                        "registry_update": "No direct registry edit by supervisor.",
                        "next_action": "Continue loop.",
                        "followup_task_prompt": "",
                        "continue_loop": True,
                    }
                )
            }
        )

    task = Task(id="x", title="Example", status="not_started")
    result = OpenAISupervisor(model="test", dry_run=False, api_key="test-key", post=fake_post).decide(task, {"reviewer_result": {}})
    assert result.decision == "accept"
    assert result.confidence == "high"
    assert result.continue_loop
    assert "raw_model_response" in result.raw


def test_openai_supervisor_fails_safely_on_invalid_json():
    def fake_post(*args, **kwargs):
        return FakeResponse({"output_text": "not json"})

    task = Task(id="x", title="Example", status="not_started")
    result = OpenAISupervisor(model="test", dry_run=False, api_key="test-key", post=fake_post).decide(task, {})
    assert result.decision == "needs_manual_review"
    assert result.confidence == "low"


def test_parse_supervisor_json_forces_manual_review_on_bad_decision():
    parsed = parse_supervisor_json(
        json.dumps(
            {
                "decision": "merge",
                "confidence": "high",
                "rationale": "bad action",
                "registry_update": "",
                "next_action": "",
                "followup_task_prompt": "",
                "continue_loop": True,
            }
        )
    )
    assert parsed["decision"] == "needs_manual_review"
    assert not parsed["continue_loop"]


def test_build_decision_engine_uses_noop_without_key(monkeypatch, tmp_path):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    config = OrchestratorConfig(
        project=ProjectConfig(name="test", adapter="generic_csv", root=tmp_path, state_file=tmp_path / "PROJECT_STATE.md"),
        supervisor=SupervisorEngineConfig(kind="openai", dry_run=False),
        dry_run=False,
    )
    assert isinstance(build_decision_engine(config), NoopSupervisor)


def test_review_gate_persists_accept_remediate_block_manual(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "PROJECT_STATE.md").write_text("# State\n")
    import subprocess

    subprocess.run(["git", "init", "-b", "main"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=repo, check=True)
    subprocess.run(["git", "add", "PROJECT_STATE.md"], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-m", "init"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "switch", "-c", "worker"], cwd=repo, check=True, capture_output=True)
    (repo / "worker.txt").write_text("work\n")
    subprocess.run(["git", "add", "worker.txt"], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-m", "work"], cwd=repo, check=True, capture_output=True)

    for action in ("accept", "remediate", "blocked", "needs_manual_review"):
        run_dir = tmp_path / f"runs/{action}"
        run_dir.mkdir(parents=True)
        (run_dir / "metadata.json").write_text(json.dumps({"branch": "worker", "base_branch": "main", "task_id": "x"}))
        task = Task(id="x", title="Example", status="not_started")
        decision = run_review_gate(repo, tmp_path / "runs", task, StaticReviewer(), decision_engine=StaticSupervisor(action), run_dir=run_dir)
        assert decision.action == action
        assert (run_dir / "parsed_supervisor_decision.json").exists()
        assert (run_dir / "final_loop_decision.json").exists()
        if action == "remediate":
            assert (run_dir / "remediation_prompt.md").exists()


def test_local_loop_dry_run_can_iterate_multiple_tasks():
    config = load_config(ROOT / "orchestrator/examples/pinker_charts.config.example.yaml")
    decisions = run_loop(config, "local-loop", max_iterations=3)
    assert len(decisions) == 3
    task_ids = [decision.task.id for decision in decisions if decision.task]
    assert len(set(task_ids)) == 3
    assert task_ids[0] == "4-1"
    assert all(decision.action == "executed" for decision in decisions)
