import importlib.util
import sys
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
spec = importlib.util.spec_from_file_location("publish_review", ROOT / "scripts/publish_review_baseline.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_book_only_manifest_does_not_invent_extension(tmp_path, monkeypatch):
    path = tmp_path / "image.png"
    path.write_bytes(b"fixture")
    artifact = {"path": "image.png", "sha256": module.sha(path)}
    record = {"figure_id": "18-1", "artifact_kind": "reconstruction", "scientific_status": "partial_match",
              "artifacts": {k: artifact for k in ["original_reference", "book_period_reconstruction", "book_period_comparison"]}}
    monkeypatch.setattr(module, "read_records", lambda root: [record])
    monkeypatch.setattr(module.subprocess, "check_output", lambda *a, **kw: "abc123\n")
    result = module.collect_existing(tmp_path)
    assert result["figure_count"] == result["comparison_count"] == 1
    assert result["figures"][0]["comparisons"][0]["mode"] == "book_period"
    path.write_bytes(b"changed")
    with pytest.raises(ValueError, match="Unreviewed artifact change"):
        module.collect_existing(tmp_path)
