import json
from pathlib import Path

from orchestrator.config import ExecutorConfig, LoopConfig, OrchestratorConfig, ProjectConfig, SupervisorEngineConfig, load_config
from orchestrator.review_gate import run_review_gate
from orchestrator.review_gate import dirty_files_from_status, reviewer_status, supervisor_reliance, supervisor_status
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
    (repo / "output/pdf").mkdir(parents=True)
    (repo / "output/pdf/recreated_figures_review_scroll.manifest.json").write_text(json.dumps([{"figure_id": "x", "status": "partial_match"}]))
    subprocess.run(["git", "add", "worker.txt", "output/pdf/recreated_figures_review_scroll.manifest.json"], cwd=repo, check=True)
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
        final_decision = json.loads((run_dir / "final_loop_decision.json").read_text())
        package_dir = run_dir / "submission_package"
        assert (package_dir / "submission_package.md").exists()
        assert (package_dir / "submission_manifest.json").exists()
        package_manifest = json.loads((package_dir / "submission_manifest.json").read_text())
        assert package_manifest["review_pdf_manifest_entry"]["figure_id"] == "x"
        assert "submission_package" in final_decision
        assert final_decision["reviewer_status"] == "success"
        assert final_decision["supervisor_status"] == "success"
        assert final_decision["final_action"] == action
        assert "successful_reviewer_output" in final_decision["supervisor_relied_on"]
        assert "direct_supervisor_inspection" in final_decision["supervisor_relied_on"]
        if action == "remediate":
            assert (run_dir / "remediation_prompt.md").exists()


def test_reviewer_supervisor_status_helpers_distinguish_failure_manual_and_noop():
    task = Task(id="x", title="Example", status="not_started")
    failed_review = ReviewResult(task=task, reviewer="openai-unavailable", decision="needs_manual_review", summary="failed", raw={"error": "parse"})
    manual_review = ReviewResult(task=task, reviewer="openai", decision="needs_manual_review", summary="manual")
    noop_review = ReviewResult(task=task, reviewer="noop", decision="needs_manual_review", summary="noop")
    assert reviewer_status(failed_review) == "failed"
    assert reviewer_status(manual_review) == "manual_review"
    assert reviewer_status(noop_review) == "noop"

    failed_supervisor = SupervisorEngineResult(
        task=task,
        supervisor="openai-unavailable",
        decision="needs_manual_review",
        confidence="low",
        rationale="failed",
        registry_update="",
        next_action="manual",
        followup_task_prompt="",
        continue_loop=False,
        raw={"error": "api"},
    )
    assert supervisor_status(failed_supervisor) == "failed"
    assert supervisor_reliance("failed", "success") == ["failed_reviewer_fallback", "direct_supervisor_inspection"]


def test_local_loop_dry_run_can_iterate_multiple_tasks():
    config = load_config(ROOT / "orchestrator/examples/pinker_charts.config.example.yaml")
    decisions = run_loop(config, "local-loop", max_iterations=3)
    assert len(decisions) == 3
    task_ids = [decision.task.id for decision in decisions if decision.task]
    assert len(set(task_ids)) == 3
    assert task_ids[0] == "4-1"
    assert all(decision.action == "executed" for decision in decisions)


def test_allow_remediation_resumes_latest_remediate_task_before_registry_selection(tmp_path: Path):
    (tmp_path / "PROJECT_STATE.md").write_text("# State\n")
    registry = tmp_path / "registry.csv"
    registry.write_text("id,title,status\n4-1,Tone,not_started\n10-2,Sustainability,not_started\n")
    runs_dir = tmp_path / "runs"
    run_dir = runs_dir / "20260705T000000Z_10_2"
    run_dir.mkdir(parents=True)
    (run_dir / "metadata.json").write_text(json.dumps({"task_id": "10-2", "branch": "codex/10-2-sustainability"}))
    (run_dir / "final_loop_decision.json").write_text(
        json.dumps(
            {
                "task_id": "10-2",
                "task_title": "Sustainability",
                "worker_branch": "codex/10-2-sustainability",
                "final_action": "remediate",
                "decision_basis": "evidence_insufficient",
                "reviewer_status": "success",
                "supervisor_status": "success",
            }
        )
    )
    (run_dir / "review_result.json").write_text(
        json.dumps(
            {
                "raw": {
                    "parsed_result": {
                        "required_remediation": ["Inspect the comparison images."],
                        "reasonable_next_steps": ["Verify the clean CSV against source data."],
                        "rationale": "Evidence is insufficient.",
                    }
                }
            }
        )
    )
    (run_dir / "parsed_supervisor_decision.json").write_text(
        json.dumps({"followup_task_prompt": "Remediate Figure 10-2 only.", "rationale": "Do not start another figure."})
    )
    config = OrchestratorConfig(
        project=ProjectConfig(name="test", adapter="generic_csv", root=tmp_path, state_file=tmp_path / "PROJECT_STATE.md", registry_file=registry),
        executor=ExecutorConfig(kind="codex_cli", command="codex", runs_dir=runs_dir, dry_run=True),
        loop=LoopConfig(max_iterations=1, allow_remediation=True),
        dry_run=True,
    )
    decisions = run_loop(config, "local-loop", max_iterations=1)
    assert len(decisions) == 1
    decision = decisions[0]
    assert decision.task is not None
    assert decision.task.id == "10-2"
    assert "Would switch to `codex/10-2-sustainability`" in decision.reason
    assert "Inspect the comparison images." in decision.reason
    assert "4-1" not in decision.reason


def test_remediation_review_uses_child_commit_not_parent_metadata(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "PROJECT_STATE.md").write_text("# State\n")
    import subprocess

    subprocess.run(["git", "init", "-b", "main"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=repo, check=True)
    (repo / "figures/10-2").mkdir(parents=True)
    (repo / "figures/10-2/provenance.md").write_text("before\n")
    subprocess.run(["git", "add", "."], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-m", "base"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "switch", "-c", "worker"], cwd=repo, check=True, capture_output=True)
    base_commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo, text=True, capture_output=True, check=True).stdout.strip()
    (repo / "figures/10-2/provenance.md").write_text("after\n")
    subprocess.run(["git", "add", "."], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-m", "remediate 10-2"], cwd=repo, check=True, capture_output=True)

    run_dir = tmp_path / "runs/child"
    run_dir.mkdir(parents=True)
    (run_dir / "metadata.json").write_text(
        json.dumps({"branch": "worker", "base_branch": base_commit, "task_id": "10-2", "remediation": True, "parent_run_id": "parent"})
    )
    (run_dir / "git_status.txt").write_text("## worker\n")
    task = Task(id="10-2", title="Sustainability", status="not_started")
    decision = run_review_gate(repo, tmp_path / "runs", task, StaticReviewer(), decision_engine=StaticSupervisor("accept"), run_dir=run_dir)
    final_decision = json.loads((run_dir / "final_loop_decision.json").read_text())
    assert decision.action == "accept"
    assert final_decision["worker_made_commit"] is True
    assert final_decision["worker_made_no_commit"] is False
    assert len(final_decision["commit_summary"]) == 1
    assert "remediate 10-2" in final_decision["commit_summary"][0]
    assert final_decision["changed_files"] == ["figures/10-2/provenance.md"]


def test_remediation_review_reports_dirty_files_when_no_child_commit(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "PROJECT_STATE.md").write_text("# State\n")
    import subprocess

    subprocess.run(["git", "init", "-b", "main"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=repo, check=True)
    (repo / "figures/10-2").mkdir(parents=True)
    (repo / "figures/10-2/provenance.md").write_text("before\n")
    subprocess.run(["git", "add", "."], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-m", "base"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "switch", "-c", "worker"], cwd=repo, check=True, capture_output=True)
    base_commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo, text=True, capture_output=True, check=True).stdout.strip()

    run_dir = tmp_path / "runs/dirty"
    run_dir.mkdir(parents=True)
    (run_dir / "metadata.json").write_text(
        json.dumps({"branch": "worker", "base_branch": base_commit, "task_id": "10-2", "remediation": True, "parent_run_id": "parent"})
    )
    (run_dir / "git_status.txt").write_text("## worker\n M figures/10-2/provenance.md\n?? figures/10-2/new.csv\n")
    task = Task(id="10-2", title="Sustainability", status="not_started")
    run_review_gate(repo, tmp_path / "runs", task, StaticReviewer(), decision_engine=StaticSupervisor("remediate"), run_dir=run_dir)
    packet = (run_dir / "review_packet.md").read_text()
    final_decision = json.loads((run_dir / "final_loop_decision.json").read_text())
    package_manifest = json.loads((run_dir / "submission_package/submission_manifest.json").read_text())
    assert dirty_files_from_status((run_dir / "git_status.txt").read_text()) == ["figures/10-2/provenance.md", "figures/10-2/new.csv"]
    assert "No worker commit detected" in packet
    assert final_decision["worker_made_commit"] is False
    assert final_decision["worker_made_no_commit"] is True
    assert final_decision["changed_files"] == ["figures/10-2/provenance.md", "figures/10-2/new.csv"]
    assert package_manifest["package_source"] == "uncommitted_worktree_not_packaged"
