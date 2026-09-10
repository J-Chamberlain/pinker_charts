#!/usr/bin/env python3
"""Offline, version-preserving catalog of retained data and exact clean CSV rows."""
from __future__ import annotations

import argparse
import csv
import fcntl
import gzip
import hashlib
import io
import json
import os
import sqlite3
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = Path("data/database/pinker_data.sqlite")
SCHEMA_VERSION = 1
SCHEMA = """
PRAGMA foreign_keys=ON;
CREATE TABLE IF NOT EXISTS snapshots (
  snapshot_id TEXT PRIMARY KEY, captured_at TEXT NOT NULL,
  repository_commit TEXT NOT NULL, input_fingerprint TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS figures (
  snapshot_id TEXT REFERENCES snapshots, figure_id TEXT, title TEXT,
  scientific_status TEXT, artifact_kind TEXT, metadata_json TEXT,
  PRIMARY KEY(snapshot_id, figure_id));
CREATE TABLE IF NOT EXISTS file_versions (
  version_id TEXT PRIMARY KEY, repository_path TEXT NOT NULL,
  sha256 TEXT NOT NULL, byte_size INTEGER NOT NULL, format TEXT NOT NULL,
  table_status TEXT NOT NULL, table_error TEXT,
  columns_json TEXT, row_count INTEGER, original_csv_gzip BLOB);
CREATE TABLE IF NOT EXISTS figure_files (
  snapshot_id TEXT, figure_id TEXT, version_id TEXT REFERENCES file_versions,
  storage_role TEXT, usage_status TEXT, canonical_roles_json TEXT,
  PRIMARY KEY(snapshot_id, figure_id, version_id),
  FOREIGN KEY(snapshot_id, figure_id) REFERENCES figures);
CREATE TABLE IF NOT EXISTS clean_rows (
  version_id TEXT REFERENCES file_versions, row_number INTEGER,
  values_json TEXT NOT NULL, PRIMARY KEY(version_id, row_number));
CREATE TABLE IF NOT EXISTS references_metadata (
  snapshot_id TEXT, figure_id TEXT, evidence_path TEXT, sha256 TEXT,
  metadata_json TEXT, PRIMARY KEY(snapshot_id, figure_id, evidence_path),
  FOREIGN KEY(snapshot_id, figure_id) REFERENCES figures);
CREATE TABLE IF NOT EXISTS database_state (key TEXT PRIMARY KEY, value TEXT NOT NULL);
CREATE VIEW IF NOT EXISTS current_files AS
  SELECT ff.*, fv.repository_path, fv.sha256, fv.byte_size, fv.format,
         fv.table_status, fv.table_error, fv.columns_json, fv.row_count
  FROM figure_files ff JOIN file_versions fv USING(version_id)
  WHERE snapshot_id=(SELECT value FROM database_state WHERE key='current_snapshot');
CREATE VIEW IF NOT EXISTS current_clean_rows AS
  SELECT cf.figure_id, cf.repository_path, cf.version_id, cf.usage_status,
         cr.row_number, cr.values_json
  FROM current_files cf JOIN clean_rows cr USING(version_id);
"""


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def json_text(value) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def inventory(root: Path) -> tuple[list, list, list, str]:
    records, files, references = [], [], []
    for path in sorted(root.glob("figures/*/figure.json")):
        record = json.loads(path.read_text())
        fid = record["figure_id"]
        if path.parent.name != fid:
            raise ValueError(f"Figure identity mismatch: {path}")
        records.append(record)
        canonical = {}
        for role, art in record.get("artifacts", {}).items():
            canonical.setdefault(art["path"], []).append(role)
        for file in sorted((path.parent / "data").rglob("*")):
            if not file.is_file():
                continue
            if file.is_symlink() or not file.resolve().is_relative_to(root.resolve()):
                raise ValueError(f"Unsafe data path: {file}")
            relative = file.relative_to(root).as_posix()
            storage = file.relative_to(path.parent / "data").parts[0]
            roles = canonical.get(relative, [])
            # Folder names indicate storage, NOT that a file drove the current plot.
            usage = "canonical_declared" if roles else "candidate_unverified" if storage == "candidates" else "historical_or_unverified"
            files.append({"figure_id": fid, "path": relative, "sha256": digest(file.read_bytes()),
                          "byte_size": file.stat().st_size, "storage_role": storage,
                          "usage_status": usage, "canonical_roles": roles})
        for evidence in sorted(path.parent.glob("**/*.json")):
            if evidence == path or "data" in evidence.relative_to(path.parent).parts:
                continue
            if "metadata" not in evidence.parts and "lineage" not in evidence.parts:
                continue
            content = json.loads(evidence.read_text())
            references.append({"figure_id": fid, "path": evidence.relative_to(root).as_posix(),
                               "sha256": digest(evidence.read_bytes()), "metadata": content})
    fingerprint = digest(json_text({"schema": SCHEMA_VERSION, "figures": records, "files": files, "references": references}).encode())
    return records, files, references, fingerprint


def parse_clean_csv(data: bytes) -> tuple[list[str], list[dict]]:
    reader = csv.reader(io.StringIO(data.decode("utf-8-sig"), newline=""), strict=True)
    columns = next(reader, [])
    if not columns or any(not name for name in columns) or len(set(columns)) != len(columns):
        raise ValueError("Empty or duplicate column names require explicit schema mapping")
    rows = []
    for number, values in enumerate(reader, 2):
        if len(values) != len(columns):
            raise ValueError(f"CSV line {number}: expected {len(columns)} fields, got {len(values)}")
        rows.append(dict(zip(columns, values)))
    return columns, rows


def insert_version(conn: sqlite3.Connection, root: Path, file: dict) -> str:
    version = digest((file["path"] + "\0" + file["sha256"]).encode())
    if conn.execute("SELECT 1 FROM file_versions WHERE version_id=?", (version,)).fetchone():
        return version
    path = root / file["path"]
    status, error, columns, rows, compressed = "file_reference_only", None, [], [], None
    if file["storage_role"] == "clean" and path.suffix.lower() == ".csv":
        data = path.read_bytes()
        if digest(data) != file["sha256"]:
            raise ValueError(f"Input changed during import: {path}")
        compressed = gzip.compress(data, mtime=0)
        try:
            columns, rows = parse_clean_csv(data)
            status = "rows_imported"
        except (ValueError, UnicodeError, csv.Error) as exc:
            status, error = "parse_error", str(exc)
    conn.execute("INSERT INTO file_versions VALUES (?,?,?,?,?,?,?,?,?,?)",
                 (version, file["path"], file["sha256"], file["byte_size"], path.suffix.lower(), status, error,
                  json_text(columns), len(rows) if status == "rows_imported" else None, compressed))
    conn.executemany("INSERT INTO clean_rows VALUES (?,?,?)",
                     ((version, number, json_text(row)) for number, row in enumerate(rows, 1)))
    return version


def build(root: Path, destination: Path) -> dict:
    # Advisory lock lives in Git's common directory, not the research archive.
    common = subprocess.run(["git", "-C", str(root), "rev-parse", "--git-common-dir"], capture_output=True, text=True, check=True).stdout.strip()
    lock_path = Path(common) if Path(common).is_absolute() else root / common
    with (lock_path / "data-database-build.lock").open("a") as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        return _build(root, destination)


def _build(root: Path, destination: Path) -> dict:
    records, files, references, fingerprint = inventory(root)
    if destination.exists():
        with sqlite3.connect(f"file:{destination.resolve()}?mode=ro", uri=True) as previous:
            if previous.execute("PRAGMA user_version").fetchone()[0] != SCHEMA_VERSION:
                raise ValueError("Unsupported database schema")
            current = previous.execute("SELECT value FROM database_state WHERE key='current_snapshot'").fetchone()
            if current and current[0] == fingerprint:
                return check(root, destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=".database-", suffix=".sqlite", dir=destination.parent)
    os.close(fd)
    temporary = Path(name)
    conn = None
    try:
        if destination.exists():
            # SQLite backup includes committed WAL contents without mutating the source.
            with sqlite3.connect(f"file:{destination.resolve()}?mode=ro", uri=True) as source:
                with sqlite3.connect(temporary) as target:
                    source.backup(target)
        conn = sqlite3.connect(temporary)
        version = conn.execute("PRAGMA user_version").fetchone()[0]
        if version not in (0, SCHEMA_VERSION):
            raise ValueError(f"Unsupported database schema: {version}")
        conn.executescript(SCHEMA)
        snapshot = fingerprint
        if not conn.execute("SELECT 1 FROM snapshots WHERE snapshot_id=?", (snapshot,)).fetchone():
            commit = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
            conn.execute("INSERT INTO snapshots VALUES (?,?,?,?)", (snapshot, datetime.now(timezone.utc).isoformat(), commit, fingerprint))
            for record in records:
                conn.execute("INSERT INTO figures VALUES (?,?,?,?,?,?)", (snapshot, record["figure_id"], record["title"], record["scientific_status"], record["artifact_kind"], json_text(record)))
            for file in files:
                version_id = insert_version(conn, root, file)
                conn.execute("INSERT INTO figure_files VALUES (?,?,?,?,?,?)", (snapshot, file["figure_id"], version_id, file["storage_role"], file["usage_status"], json_text(file["canonical_roles"])))
            for ref in references:
                conn.execute("INSERT INTO references_metadata VALUES (?,?,?,?,?)", (snapshot, ref["figure_id"], ref["path"], ref["sha256"], json_text(ref["metadata"])))
        conn.execute("INSERT OR REPLACE INTO database_state VALUES ('current_snapshot',?)", (snapshot,))
        conn.execute(f"PRAGMA user_version={SCHEMA_VERSION}")
        conn.commit()
        if conn.execute("PRAGMA integrity_check").fetchone()[0] != "ok" or conn.execute("PRAGMA foreign_key_check").fetchall():
            raise ValueError("Database integrity validation failed")
        # Refuse a mixed-time snapshot if any source or metadata changed during import.
        if inventory(root)[3] != fingerprint:
            raise ValueError("Source inventory changed during import; previous database preserved")
        report = summary(conn)
        conn.close()
        conn = None
        temporary.replace(destination)
        return report
    finally:
        if conn is not None:
            conn.close()
        temporary.unlink(missing_ok=True)


def summary(conn: sqlite3.Connection) -> dict:
    current = conn.execute("SELECT value FROM database_state WHERE key='current_snapshot'").fetchone()[0]
    coverage = []
    for fid, title, status, kind in conn.execute("SELECT figure_id,title,scientific_status,artifact_kind FROM figures WHERE snapshot_id=? ORDER BY figure_id", (current,)):
        rows = conn.execute("SELECT storage_role,table_status,usage_status,row_count FROM current_files WHERE figure_id=?", (fid,)).fetchall()
        coverage.append({"figure_id": fid, "title": title, "scientific_status": status, "artifact_kind": kind,
                         "saved_files": len(rows), "raw_files": sum(r[0] == "raw" for r in rows),
                         "clean_tables": sum(r[1] == "rows_imported" for r in rows),
                         "canonical_declared_clean_tables": sum(r[1] == "rows_imported" and r[2] == "canonical_declared" for r in rows),
                         "clean_rows": sum(r[3] or 0 for r in rows),
                         "lineage_status": "needs_per_plot_mapping_review" if kind == "reconstruction" else "no_reconstruction_claim"})
    return {"schema_version": SCHEMA_VERSION, "snapshot_id": current,
            "figures": len(coverage), "saved_files": conn.execute("SELECT count(*) FROM current_files").fetchone()[0],
            "clean_tables": conn.execute("SELECT count(*) FROM current_files WHERE table_status='rows_imported'").fetchone()[0],
            "clean_rows": conn.execute("SELECT count(*) FROM current_clean_rows").fetchone()[0],
            "parse_errors": conn.execute("SELECT repository_path,table_error FROM current_files WHERE table_status='parse_error'").fetchall(),
            "figure_coverage": coverage,
            "limitations": ["File presence does not prove use in the current plot.", "Candidate and legacy files are not promoted to accepted data.", "Database row queries cover clean CSVs only. Full raw sources may be local-only where redistribution is restricted; consult source manifests.", "Units and source versions are not automatically harmonized."]}


def check(root: Path, destination: Path) -> dict:
    with sqlite3.connect(f"file:{destination.resolve()}?mode=ro", uri=True) as conn:
        if conn.execute("PRAGMA integrity_check").fetchone()[0] != "ok" or conn.execute("PRAGMA foreign_key_check").fetchall():
            raise ValueError("Database integrity validation failed")
        report = summary(conn)
        if report["snapshot_id"] != inventory(root)[3]:
            raise ValueError("Database snapshot is stale; run build")
        for version, packed, expected_hash, expected_count in conn.execute("SELECT version_id,original_csv_gzip,sha256,row_count FROM file_versions WHERE table_status='rows_imported'"):
            data = gzip.decompress(packed)
            if digest(data) != expected_hash:
                raise ValueError(f"Archived CSV hash mismatch: {version}")
            _, rows = parse_clean_csv(data)
            stored = [json.loads(row[0]) for row in conn.execute("SELECT values_json FROM clean_rows WHERE version_id=? ORDER BY row_number", (version,))]
            if len(rows) != expected_count or stored != rows:
                raise ValueError(f"Database values differ from archived CSV: {version}")
        return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["build", "check"])
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    root = args.root.resolve()
    destination = root / DB_PATH
    report = build(root, destination) if args.command == "build" else check(root, destination)
    if args.command == "build":
        (destination.parent / "catalog.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({key: value for key, value in report.items() if key != "figure_coverage"}, indent=2))


if __name__ == "__main__":
    main()
