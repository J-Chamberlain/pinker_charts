"""Canonical figure records and deterministic, validated project-state projections.

Use bootstrap once after history reconciliation, then edit figure.json records
and run generate. check is read-only and fails on stale mirrors or file hashes.
"""
from __future__ import annotations

import argparse
from collections import Counter
import csv
import hashlib
import io
import json
import os
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SCIENTIFIC = {"not_started", "verified_reproduction", "updated_equivalent", "partial_match",
              "source_chain_recovered", "needs_targeted_source_recovery", "blocked_external_source",
              "source_unavailable", "manual_review_needed"}
EXECUTION = {"not_started", "in_progress", "accepted", "blocked", "remediation_needed", "processed"}
NON_RECONSTRUCTIONS = {"4-1", "5-4", "6-1", "9-1", "9-2", "9-3", "10-4", "12-3", "12-4"}
FIELDS = ["figure_id", "book", "chapter", "title", "page", "year_range", "current_status",
          "lifecycle_stage", "source_type_guess", "priority", "current_owner", "next_action", "notes",
          "execution_status", "publication_status", "artifact_kind"]
DOCUMENTS = {"caption": "captions/caption.txt", "provenance": "provenance/provenance.md",
             "anomaly_review": "anomaly_reviews/anomaly_review.md", "review_checklist": "review_checklist.md",
             "source_log": "source_logs/source_log.md", "search_log": "search_iterations/search_iterations.md",
             "discrepancy_log": "discrepancy_logs/discrepancy_log.md", "legacy_metadata": "metadata/metadata.json"}
RESEARCH_FIELDS = ["book_page", "claim_summary", "original_dataset", "dataset_url", "archive_url", "download_date", "confidence_score"]
ALIASES = {"original_reference": ["original_reference", "supplemental_pdf_reference", "kindle_reference",
                                  "kindle_reference_image", "original_reference_image"],
           "book_period_reconstruction": ["book_period_reconstruction", "best_current_reconstruction"],
           "extended_reconstruction": ["extended_reconstruction", "same_source_continuation"],
           "book_period_comparison": ["book_period_comparison", "comparison_image"],
           "extended_comparison": ["extended_comparison"]}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def safe_path(root: Path, value: str) -> Path:
    path = Path(value)
    if path.is_absolute() or ".." in path.parts or not path.parts:
        raise ValueError(f"Not a repository-relative path: {value}")
    target = (root / path).resolve()
    if not target.is_relative_to(root.resolve()):
        raise ValueError(f"Path escapes repository: {value}")
    return target


def file_record(root: Path, relative: str) -> dict:
    path = safe_path(root, relative)
    if not path.is_file():
        raise ValueError(f"Missing artifact: {relative}")
    return {"path": relative, "sha256": sha(path)}


def sort_id(value: str):
    return tuple(int(x) for x in value.split("-"))


def dumps(value) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2) + "\n"


def imported_status(metadata: dict, fallback: str) -> str:
    for key in ["reproduction_status", "status", "current_status"]:
        if metadata.get(key) in SCIENTIFIC:
            return metadata[key]
    if fallback in SCIENTIFIC:
        return fallback
    raise ValueError("No evidence-backed scientific status; scheduling state cannot substitute")


def infer_artifacts(root: Path, fid: str, metadata: dict, kind: str) -> dict:
    prefix = f"figures/{fid}/"
    token = fid.replace("-", "_")
    candidates = dict(metadata)
    candidates.update(metadata.get("canonical_artifacts", {}))
    found = {}
    for role, aliases in ALIASES.items():
        options = [candidates[k] for k in aliases if isinstance(candidates.get(k), str)]
        if role == "original_reference":
            options.extend(prefix + "plots/comparisons/" + name for name in [
                f"supplemental_pdf_reference_figure_{token}.png", f"pdf_reference_figure_{token}.png",
                f"kindle_reference_figure_{token}.png", f"corrected_figure_{token}_book_crop.png"])
        elif fid in {"10-5", "10-6"} and role.endswith("comparison"):
            label = "book_style" if role.startswith("book") else "extended"
            options.append(prefix + f"plots/comparisons/figure_{token}_{label}_comparison_captioned.png")
        else:
            folder = "comparisons" if role.endswith("comparison") else "book_period" if role.startswith("book") else "extended"
            options.append(prefix + f"plots/{folder}/figure_{token}_{role}.png")
        for candidate in options:
            if candidate.startswith(prefix) and safe_path(root, candidate).is_file():
                if kind == "reconstruction" or role == "original_reference":
                    found[role] = file_record(root, candidate)
                break
    for role, suffix in DOCUMENTS.items():
        if (root / prefix / suffix).is_file():
            found[role] = file_record(root, prefix + suffix)
    found["metadata"] = {"path": prefix + "figure.json", "self": True}
    return found


def bootstrap(root: Path) -> None:
    rows = list(csv.DictReader((root / "data/figure_registry.csv").open()))
    if len({row["figure_id"] for row in rows}) != len(rows):
        raise ValueError("Duplicate registry IDs")
    existing = list((root / "figures").glob("*/figure.json"))
    if existing:
        raise ValueError("Canonical records already exist; bootstrap will not overwrite research decisions")
    commit = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
    for row in rows:
        fid = row["figure_id"]
        legacy_path = root / "figures" / fid / "metadata/metadata.json"
        legacy = json.loads(legacy_path.read_text()) if legacy_path.exists() else {}
        status = imported_status(legacy, row["current_status"])
        kind = "not_started" if status == "not_started" else "source_recovery" if fid in NON_RECONSTRUCTIONS else "reconstruction"
        old = row["current_status"]
        execution = old.removeprefix("orchestrator_") if old.startswith("orchestrator_") else "not_started" if status == "not_started" else "processed"
        next_action = legacy.get("recommended_next_action") or legacy.get("next_action") or row["next_action"]
        if old.startswith("orchestrator_"):
            next_action = "Review consolidated source evidence and remaining limitations; do not repeat status-only remediation."
        record = {"schema_version": 1, **{k: row[k] for k in ["figure_id", "book", "chapter", "title", "page", "year_range", "source_type_guess", "priority", "current_owner"]},
                  "scientific_status": status, "execution_status": execution,
                  "publication_status": "not_reviewed" if kind == "reconstruction" else "incomplete",
                  "lifecycle_stage": legacy.get("lifecycle_stage", row["lifecycle_stage"]),
                  "next_action": next_action, "notes": legacy.get("notes", row["notes"]),
                  "artifact_kind": kind,
                  "book_citation": legacy.get("book_citation", legacy.get("source_note", legacy.get("original_source_line", ""))),
                  "research": {key: legacy.get(key, "") for key in RESEARCH_FIELDS},
                  "status_evidence": {"basis": "imported historical scientific claim; not newly verified",
                                      "commit": commit, "previous_registry_status": old},
                  "visual_review": {"status": "pending", "reference_basis": "facsimile" if fid == "5-3" else "original_reference_unconfirmed",
                                    "inspected_artifacts": [], "issues": []},
                  "extension": {"status": "pending_methodology_review", "notes": "An extended filename alone does not establish an extension."},
                  "artifacts": infer_artifacts(root, fid, legacy, kind)}
        if fid == "7-4":
            record["visual_review"]["issues"].append("Worker chart-label-derived candidate quarantined in reports/consolidation/worker_candidates/7-4; current legitimate successor remains partial.")
        target = root / "figures" / fid / "figure.json"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(dumps(record))


def read_records(root: Path) -> list[dict]:
    records = [json.loads(p.read_text()) for p in (root / "figures").glob("*/figure.json")]
    records.sort(key=lambda r: sort_id(r["figure_id"]))
    return records


def validate_record(root: Path, record: dict) -> list[str]:
    errors = []
    fid = record.get("figure_id", "?")
    if not re.fullmatch(r"\d+-\d+", fid) or not record.get("title"):
        errors.append(f"{fid}: missing title or invalid figure ID")
    if record.get("scientific_status") not in SCIENTIFIC or record.get("execution_status") not in EXECUTION:
        errors.append(f"{fid}: invalid scientific or execution status")
    if record.get("artifact_kind") != "reconstruction" and record.get("publication_status") == "ready":
        errors.append(f"{fid}: non-reconstruction cannot be publication ready")
    if record.get("publication_status") == "ready":
        review = record.get("visual_review", {})
        if review.get("status") != "passed" or review.get("reference_basis") != "original" or not review.get("inspected_artifacts"):
            errors.append(f"{fid}: publication readiness lacks original-pixel review evidence")
        if not record.get("scientific_review", {}).get("passed") or not record.get("editorial_review", {}).get("passed"):
            errors.append(f"{fid}: publication readiness lacks scientific/editorial acceptance")
        needed = {"original_reference", "book_period_reconstruction", "book_period_comparison"}
        if record.get("extension", {}).get("status") in {"same_source", "comparable_successor"}:
            needed |= {"extended_reconstruction", "extended_comparison"}
        for role in needed:
            artifact = record.get("artifacts", {}).get(role)
            if not artifact or artifact not in review.get("inspected_artifacts", []):
                errors.append(f"{fid}: missing current inspected evidence for {role}")
    for role, artifact in record.get("artifacts", {}).items():
        try:
            if artifact.get("self") and (role != "metadata" or artifact.get("path") != f"figures/{fid}/figure.json"):
                errors.append(f"{fid}: invalid self-reference for {role}")
            path = safe_path(root, artifact["path"])
            if not path.is_file():
                errors.append(f"{fid}: missing {role}: {artifact['path']}")
            elif not artifact.get("self") and sha(path) != artifact.get("sha256"):
                errors.append(f"{fid}: stale checksum for {role}")
        except (ValueError, KeyError) as exc:
            errors.append(f"{fid}: {exc}")
    return errors


def projections(records: list[dict]) -> dict[str, str]:
    rows = []
    for record in records:
        row = {key: record.get(key, "") for key in FIELDS}
        row["current_status"] = record["scientific_status"]
        rows.append({key: str(value) for key, value in row.items()})
    out = io.StringIO(newline="")
    writer = csv.DictWriter(out, fieldnames=FIELDS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    counts = Counter(r["scientific_status"] for r in records)
    lines = ["# Project State", "", "Generated from `figures/<id>/figure.json` by `scripts/project_state.py generate`.",
             "Do not edit generated figure tables. The approved plan and progress ledger are in",
             "[docs/completion_plan.md](docs/completion_plan.md).", "", "## Mission", "",
             "Reconstruct all 75 Enlightenment Now figures from legitimate source data, with",
             "reproducible transformations, original-reference visual review, and defensible extensions.",
             "Scientific status, execution outcome, and publication readiness are separate.", "",
             "## Current Work", "", "Integration branch: `production-loop`.",
             "Read the completion-plan ledger for the current phase, exit evidence, and next action.",
             "[Consolidation evidence](reports/consolidation/README.md) preserves both histories.",
             "[Execution checkpoint](reports/completion_checkpoint_2026_09_09.md) records validation and remaining gates.",
             "Historical classifications are retained as claims until independently re-reviewed.",
             "A completed source search or accepted worker run is not a completed reconstruction.", "",
             "## Reference And Review", "",
             "- [Supplemental Graphics PDF](references/enlightenment_now_supplemental_graphics.pdf)",
             "- [Registry](data/figure_registry.csv) and [JSON mirror](data/figure_registry.json)",
             "- [Workflow](docs/workflow.md), [research review](docs/review_protocol.md), [editorial gate](docs/editorial_review_gate.md)",
             "- [Canonical artifact index](data/canonical_artifacts.json)", "",
             "- [Original reference index](references/figure_index.json)",
             "- [Consolidated visual audit gallery](reports/review_baseline/index.html)",
             "- [Current review PDF](output/pdf/recreated_figures_review_scroll.pdf) and [manifest](output/pdf/recreated_figures_review_scroll.manifest.json)", "",
             "Every future figure run must inspect and display actual book-period and extended",
             "comparisons where available. Record exact inspected hashes and unresolved issues.",
             "Do not digitize plotted values for reconstruction or promote weak source matches.",
             "Update the canonical record and regenerate its views whenever an artifact changes.", "",
             "## Scientific Inventory", "", "| Status | Count |", "| --- | ---: |"]
    lines.extend(f"| {s} | {c} |" for s, c in sorted(counts.items()))
    lines += ["", "## Figure Queue", "", "| Figure | Title | Scientific status | Execution | Publication |", "| --- | --- | --- | --- | --- |"]
    for r in records:
        title = r["title"].replace("|", "\\|")
        lines.append(f"| {r['figure_id']} | {title} | {r['scientific_status']} | {r['execution_status']} | {r['publication_status']} |")
    lines += ["", "## Canonical Figure Artifacts", ""]
    for r in records:
        if r["artifact_kind"] == "not_started":
            continue
        lines += [f"### Figure {r['figure_id']} - {r['title']}", "", f"Status: `{r['scientific_status']}`. Artifact kind: `{r['artifact_kind']}`.", ""]
        for role, artifact in r["artifacts"].items():
            lines.append(f"- {role.replace('_', ' ').capitalize()}: [{artifact['path']}]({artifact['path']})")
        lines.append("")
    index = {r["figure_id"]: {"scientific_status": r["scientific_status"], "artifact_kind": r["artifact_kind"], "artifacts": r["artifacts"]} for r in records}
    metadata_out = io.StringIO(newline="")
    metadata_fields = ["figure_id", "chapter", "title", *RESEARCH_FIELDS, "book_citation", "reproduction_status",
                       "execution_status", "publication_status", "visual_validation", "notes"]
    metadata_writer = csv.DictWriter(metadata_out, fieldnames=metadata_fields, lineterminator="\n")
    metadata_writer.writeheader()
    for r in records:
        values = {**r.get("research", {}), **{k: r.get(k, "") for k in ["figure_id", "chapter", "title", "book_citation", "execution_status", "publication_status", "notes"]},
                  "reproduction_status": r["scientific_status"], "visual_validation": r.get("visual_review", {}).get("status", "pending")}
        metadata_writer.writerow({k: values.get(k, "") for k in metadata_fields})
    return {"data/figure_registry.csv": out.getvalue(), "data/figure_registry.json": dumps(rows),
            "data/metadata/figure_metadata.csv": metadata_out.getvalue(),
            "data/canonical_artifacts.json": dumps(index), "PROJECT_STATE.md": "\n".join(lines) + "\n"}


def readme_projection(root: Path, record: dict) -> str:
    fid = record["figure_id"]
    path = root / "figures" / fid / "README.md"
    old = path.read_text() if path.exists() else ""
    start, end = "<!-- canonical-state:start -->", "<!-- canonical-state:end -->"
    old = re.sub(re.escape(start) + r".*?" + re.escape(end) + r"\n*", "", old, flags=re.S)
    lines = [start, f"# Figure {fid}: {record['title']}", "",
             f"Scientific status: `{record['scientific_status']}`. Execution: `{record['execution_status']}`.",
             f"Publication: `{record['publication_status']}`. Artifact kind: `{record['artifact_kind']}`.", "",
             "This generated summary and [figure.json](figure.json) supersede historical status claims below.",
             "A historical verified classification is not a fresh publication review.", ""]
    for role, artifact in record["artifacts"].items():
        relative = Path(os.path.relpath(root / artifact["path"], path.parent)).as_posix()
        lines.append(f"- {role.replace('_', ' ').capitalize()}: [{relative}]({relative})")
    lines += ["", end, "", old]
    return "\n".join(lines).rstrip() + "\n"


def synchronize(root: Path, check: bool) -> list[str]:
    records = read_records(root)
    errors = []
    if len(records) != 75 or len({r["figure_id"] for r in records}) != 75:
        errors.append("Expected exactly 75 unique canonical records")
    for record in records:
        errors.extend(validate_record(root, record))
    if errors:
        return errors
    outputs = projections(records)
    outputs.update({f"figures/{r['figure_id']}/README.md": readme_projection(root, r) for r in records})
    for record in records:
        fid = record["figure_id"]
        hashes = {a["path"]: sha(safe_path(root, a["path"])) for a in record["artifacts"].values()}
        readme = f"figures/{fid}/README.md"
        hashes[readme] = hashlib.sha256(outputs[readme].encode()).hexdigest()
        outputs[f"figures/{fid}/checksums/canonical_sha256sums.txt"] = "".join(f"{value}  {path}\n" for path, value in sorted(hashes.items()))
    for relative, text in outputs.items():
        path = root / relative
        if check:
            if not path.is_file() or path.read_text() != text:
                errors.append(f"Stale generated view: {relative}")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            temporary = path.with_suffix(path.suffix + ".tmp")
            temporary.write_text(text)
            temporary.replace(path)
    return errors


def record_execution(root: Path, fid: str, status: str, run_id: str, next_action=None, note=None) -> dict:
    """Integration-owned scheduling write. Scientific/publication state is immutable here."""
    if not re.fullmatch(r"\d+-\d+", fid) or status not in EXECUTION or not run_id.strip():
        raise ValueError("Invalid figure ID, execution status, or empty run ID")
    errors = synchronize(root, check=True)
    if errors:
        raise ValueError("Cannot update inconsistent state: " + "; ".join(errors))
    path = root / "figures" / fid / "figure.json"
    previous = path.read_bytes()
    record = json.loads(previous)
    history = record.setdefault("execution_history", [])
    if any(event["run_id"] == run_id for event in history):
        raise ValueError(f"Run {run_id} already recorded; no duplicate write-back")
    history.append({"run_id": run_id, "previous_status": record["execution_status"],
                    "status": status, "next_action": next_action, "note": note})
    record["execution_status"] = status
    # Preserve the research next_action; scheduling advice lives in its own history.
    try:
        path.write_text(dumps(record))
        errors = synchronize(root, check=False)
        if errors:
            raise ValueError("; ".join(errors))
    except Exception:
        path.write_bytes(previous)
        synchronize(root, check=False)
        raise
    return {"figure_id": fid, "run_id": run_id, "execution_status": status,
            "scientific_status": record["scientific_status"], "publication_status": record["publication_status"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["bootstrap", "generate", "check", "record-execution"])
    parser.add_argument("--figure-id")
    parser.add_argument("--execution-status", choices=sorted(EXECUTION))
    parser.add_argument("--run-id")
    parser.add_argument("--next-action")
    parser.add_argument("--note")
    args = parser.parse_args()
    if args.command == "record-execution":
        if not all([args.figure_id, args.execution_status, args.run_id]):
            parser.error("record-execution requires --figure-id, --execution-status and --run-id")
        print(dumps(record_execution(ROOT, args.figure_id, args.execution_status, args.run_id, args.next_action, args.note)))
        return
    if args.command == "bootstrap":
        bootstrap(ROOT)
    errors = synchronize(ROOT, check=args.command == "check")
    print(dumps({"figures": len(read_records(ROOT)), "errors": errors}).strip())
    raise SystemExit(bool(errors))


if __name__ == "__main__":
    main()
