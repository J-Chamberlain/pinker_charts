import importlib.util
import json
from pathlib import Path
import sqlite3
import subprocess

import pytest

spec = importlib.util.spec_from_file_location("data_database", Path(__file__).resolve().parents[1] / "scripts/build_data_database.py")
database = importlib.util.module_from_spec(spec)
spec.loader.exec_module(database)


@pytest.fixture
def root(tmp_path):
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-q", "--allow-empty", "-m", "fixture"], check=True)
    folder = tmp_path / "figures/5-3"
    (folder / "data/clean").mkdir(parents=True)
    (folder / "data/raw").mkdir()
    (folder / "data/candidates").mkdir()
    (folder / "data/clean/book.csv").write_text('Entity,Year,value,note\nSweden,1751,001.250,"comma, and text"\nSweden,1752,,missing\n')
    (folder / "data/raw/source.csv").write_text('Year,value\n1751,1.25\n')
    (folder / "data/candidates/rejected.csv").write_text('Year,value\n1751,999\n')
    (folder / "figure.json").write_text(json.dumps({"figure_id":"5-3", "title":"Maternal mortality", "scientific_status":"partial_match", "artifact_kind":"reconstruction", "artifacts":{}}))
    return tmp_path


def test_lossless_values_and_idempotence(root):
    db = root / database.DB_PATH
    report = database.build(root, db)
    assert report["clean_rows"] == 2 and report["saved_files"] == 3
    before = db.read_bytes()
    assert database.build(root, db)["snapshot_id"] == report["snapshot_id"]
    assert db.read_bytes() == before
    database.check(root, db)
    with sqlite3.connect(db) as conn:
        row = conn.execute("SELECT values_json FROM current_clean_rows WHERE row_number=1").fetchone()[0]
        assert json.loads(row)["value"] == "001.250"
        assert conn.execute("SELECT count(*) FROM snapshots").fetchone()[0] == 1
        assert conn.execute("SELECT usage_status FROM current_files WHERE storage_role='candidates'").fetchone()[0] == "candidate_unverified"


def test_new_snapshot_preserves_old_values(root):
    db = root / database.DB_PATH
    first = database.build(root, db)
    path = root / "figures/5-3/data/clean/book.csv"
    path.write_text(path.read_text().replace("001.250", "1.300"))
    with pytest.raises(ValueError, match="stale"):
        database.check(root, db)
    second = database.build(root, db)
    assert first["snapshot_id"] != second["snapshot_id"]
    with sqlite3.connect(db) as conn:
        assert conn.execute("SELECT count(*) FROM snapshots").fetchone()[0] == 2
        assert conn.execute("SELECT count(*) FROM clean_rows").fetchone()[0] == 4
    database.check(root, db)


@pytest.mark.parametrize("content", ['x,x\n1,2\n', 'x,y\n1,2,3\n'])
def test_malformed_table_is_explicit_not_silently_truncated(root, content):
    (root / "figures/5-3/data/clean/book.csv").write_text(content)
    report = database.build(root, root / database.DB_PATH)
    assert len(report["parse_errors"]) == 1 and report["clean_rows"] == 0


def test_table_tampering_detected(root):
    db = root / database.DB_PATH
    database.build(root, db)
    with sqlite3.connect(db) as conn:
        conn.execute("UPDATE clean_rows SET values_json='{}' WHERE row_number=1")
    with pytest.raises(ValueError, match="differ"):
        database.check(root, db)


def test_unsafe_data_does_not_replace_database(root):
    db = root / database.DB_PATH
    database.build(root, db)
    before = db.read_bytes()
    (root / "figures/5-3/data/raw/secret.txt").symlink_to("/etc/passwd")
    with pytest.raises(ValueError, match="Unsafe data"):
        database.build(root, db)
    assert db.read_bytes() == before
