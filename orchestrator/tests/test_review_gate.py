from pathlib import Path

from orchestrator.review_gate import build_review_packet, classify_decision, latest_run_dir
from orchestrator.schemas import ReviewResult, Task


def test_latest_run_dir(tmp_path: Path):
    (tmp_path / "20200101T000000Z_a").mkdir()
    (tmp_path / "20200101T000000Z_a" / "metadata.json").write_text("{}")
    (tmp_path / "20210101T000000Z_b").mkdir()
    (tmp_path / "20210101T000000Z_b" / "metadata.json").write_text("{}")
    assert latest_run_dir(tmp_path).name == "20210101T000000Z_b"


def test_review_packet_contains_required_sections(tmp_path: Path):
    task = Task(id="4-1", title="Tone", status="not_started", files_to_update=("PROJECT_STATE.md",), acceptance_criteria=("Update registry",))
    packet = build_review_packet(task, tmp_path, "codex/4-1-tone", "abc123", ["abc123 message"], ["PROJECT_STATE.md"], {"dry_run": True})
    assert "Commit Summary" in packet
    assert "Changed Files" in packet
    assert "Reviewer Questions" in packet


def test_classify_decision_defaults_to_manual_review():
    task = Task(id="4-1", title="Tone", status="not_started")
    review = ReviewResult(task=task, reviewer="noop", decision="unknown", summary="stub")
    assert classify_decision(review, "abc123", ["PROJECT_STATE.md"]) == "needs_manual_review"
