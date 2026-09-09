import hashlib
import json
from pathlib import Path

import pytest

from scripts.project_state import imported_status, projections, safe_path, validate_record


def test_scheduling_outcome_cannot_be_scientific_evidence():
    with pytest.raises(ValueError):
        imported_status({}, "orchestrator_accepted")
    assert imported_status({"reproduction_status": "partial_match"}, "orchestrator_accepted") == "partial_match"


@pytest.mark.parametrize("path", ["../secret", "/tmp/secret", "data/../../secret"])
def test_artifact_paths_cannot_escape_repository(tmp_path, path):
    with pytest.raises(ValueError):
        safe_path(tmp_path, path)


def test_symlink_cannot_escape_repository(tmp_path):
    (tmp_path / "escape").symlink_to(tmp_path.parent, target_is_directory=True)
    with pytest.raises(ValueError):
        safe_path(tmp_path, "escape/secret")


def record():
    return {"figure_id": "5-3", "title": "Maternal mortality", "scientific_status": "partial_match",
            "execution_status": "accepted", "publication_status": "not_reviewed", "artifact_kind": "reconstruction",
            "artifacts": {}}


def test_accepting_a_run_does_not_promote_scientific_status():
    r = record()
    rows = json.loads(projections([r])["data/figure_registry.json"])
    assert rows[0]["current_status"] == "partial_match"
    assert rows[0]["execution_status"] == "accepted"


def test_facsimile_cannot_pass_publication_review(tmp_path):
    r = record()
    r.update(publication_status="ready", visual_review={"status": "passed", "reference_basis": "facsimile", "inspected_artifacts": ["dummy"]})
    assert any("original-pixel" in e for e in validate_record(tmp_path, r))


def test_diagnostic_cannot_be_publication_ready(tmp_path):
    r = record()
    r.update(artifact_kind="source_recovery", publication_status="ready")
    assert any("non-reconstruction" in e for e in validate_record(tmp_path, r))


def test_artifact_changes_invalidate_record(tmp_path):
    r = record()
    p = tmp_path / "plot.png"
    p.write_bytes(b"original")
    r["artifacts"]["comparison"] = {"path": "plot.png", "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
    assert not validate_record(tmp_path, r)
    p.write_bytes(b"changed")
    assert any("stale checksum" in e for e in validate_record(tmp_path, r))


def test_generated_views_are_deterministic():
    assert projections([record()]) == projections([record()])


def test_review_booleans_without_inspected_images_cannot_pass(tmp_path):
    r = record()
    r.update(publication_status="ready", visual_review={"status": "passed", "reference_basis": "original", "inspected_artifacts": ["claimed"]},
             scientific_review={"passed": True}, editorial_review={"passed": True})
    assert any("missing current inspected evidence" in e for e in validate_record(tmp_path, r))


def test_self_reference_cannot_skip_plot_hash_verification(tmp_path):
    r = record()
    (tmp_path / "plot.png").write_bytes(b"x")
    r["artifacts"]["comparison"] = {"path": "plot.png", "self": True}
    assert any("invalid self-reference" in e for e in validate_record(tmp_path, r))
