"""Reconcile the two inspected research histories without discarding either parent.

This is a one-time, evidence-specific migration, not a generic 'newest wins' merge.
Default mode prints the inventory; --apply writes the documented resolutions.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
LOCAL = "efca126"
REMOTE = "9a19519494ec20f45b3ac3e6b3122d38a2bc0892"
RECOVERIES = {
    "4-1": "More complete Leetaru publication and source-availability evidence; no numeric reconstruction claimed.",
    "5-2": "Recovered immutable CME Info 2016 component and explicitly clipped successor; remains partial.",
    "5-3": "Recovered OWID 522 raw table and exact conversion; facsimile comparisons require replacement with retained original PDF pixels.",
    "5-4": "Recovered Clio birth component and ONS diagnostic; no exact multi-age reconstruction claimed. Local original references retained.",
    "10-5": "Recovered and rejected current UNCTAD bulk series; the unsupported image-derived oil-shipping line is not canonical reconstruction input.",
    "19-1": "Recovered archived HumanProgress principal-country values and stacked-area reconstruction; minor-country vintage remains partial.",
}


def git(*args: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(ROOT), *args])


def blob(ref: str, path: str) -> bytes | None:
    result = subprocess.run(["git", "-C", str(ROOT), "show", f"{ref}:{path}"], capture_output=True)
    return result.stdout if result.returncode == 0 else None


def csv_rows(ref: str, path: str) -> tuple[list[str], list[dict]]:
    reader = csv.DictReader(io.StringIO((blob(ref, path) or b"").decode()))
    rows = list(reader)
    for row in rows:
        # Preserve pre-existing malformed trailing fields as explicit notes.
        extras = row.pop(None, None)
        if extras:
            row["notes"] = (row.get("notes") or "") + " | Legacy extra CSV fields: " + json.dumps(extras)
    return list(reader.fieldnames or []), rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    local = git("rev-parse", LOCAL).decode().strip()
    remote = git("rev-parse", REMOTE).decode().strip()
    base = git("merge-base", local, remote).decode().strip()
    changed = git("diff", "--name-only", base, remote).decode().splitlines()
    resolutions = []

    def write(path: str, data: bytes, origin: str, reason: str) -> None:
        old = blob(local, path)
        resolutions.append({"path": path, "origin": origin, "reason": reason,
                            "local_sha256": hashlib.sha256(old).hexdigest() if old else None,
                            "selected_sha256": hashlib.sha256(data).hexdigest()})
        if args.apply:
            target = ROOT / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)

    def write_csv(path: str, fields: list[str], rows: list[dict], reason: str) -> None:
        out = io.StringIO(newline="")
        writer = csv.DictWriter(out, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
        write(path, out.getvalue().encode(), "structured_union", reason)

    for label, ref in [("local", local), ("github_main", remote)]:
        for path in ["PROJECT_STATE.md", "data/figure_registry.csv", "data/figure_registry.json",
                     "data/metadata/figure_metadata.csv"]:
            content = blob(ref, path)
            if content is not None:
                write(f"reports/consolidation/snapshots/{label}/{path}", content, ref,
                      "Immutable pre-consolidation evidence; scientific claims are historical.")

    scripts = {"scripts/reconstruct_5_1_5_2_8_4_19_1.py", "scripts/reconstruct_5_3.py",
               "scripts/reconstruct_5_4.py", "scripts/reconstruct_figure_5_2.py",
               "scripts/build_figure_4_1_evidence.py", "scripts/reconstruct_10_5_source_recovery.py"}
    for path in changed:
        parts = Path(path).parts
        fid = parts[1] if len(parts) > 2 and parts[0] == "figures" else None
        if fid not in RECOVERIES and path not in scripts:
            continue
        content = blob(remote, path)
        if content is None:
            raise ValueError(f"Unexpected deletion: {path}")
        old = blob(local, path)
        if old and old != content and any(part in parts for part in ["source_logs", "search_iterations"]):
            content = (f"# Consolidated Research History: Figure {fid}\n\n"
                       "These are historical search records, not the current acceptance decision.\n\n"
                       f"## Local Work At {local}\n\n").encode() + old + (
                           f"\n\n## GitHub Recovery At {remote}\n\n").encode() + content
            write(path, content, "both_parents", "Preserve both search histories; do not repeat exhausted searches.")
        else:
            write(path, content, remote, RECOVERIES.get(fid, "Plot/transformation code paired with imported source data; not executed during import."))

    for name, key in [("bibliography_database", "citation_key"), ("citation_key_lookup", "citation_key"),
                      ("dataset_reference_catalog", "dataset_id"), ("figure_bibliography_mapping", "figure_id"),
                      ("archive_index", "archive_id")]:
        path = f"data/bibliography/{name}.csv"
        fields, ours = csv_rows(local, path)
        _, theirs = csv_rows(remote, path)
        _, ancestors = csv_rows(base, path)
        if key not in fields:
            # Archive rows have no universal key; preserve exact distinct records.
            rows = list(ours)
            rows.extend(row for row in theirs if row not in rows)
        else:
            before = {row[key]: row for row in ancestors}
            merged = {row[key]: row for row in ours}
            for row in theirs:
                if row[key] not in merged or row != before.get(row[key]):
                    merged[row[key]] = row
            rows = list(merged.values())
        write_csv(path, fields, rows, "Union by documented catalog key; retain remote additions/changed recovery records and all local-only records.")
        write(f"data/bibliography/{name}.json", (json.dumps(rows, indent=2, ensure_ascii=False) + "\n").encode(),
              "structured_union", "JSON mirror generated from the exact reconciled CSV rows.")

    for path in ["data/figure_registry.csv", "data/metadata/figure_metadata.csv"]:
        fields, ours = csv_rows(local, path)
        _, theirs = csv_rows(remote, path)
        replacements = {row["figure_id"]: row for row in theirs if row["figure_id"] in RECOVERIES}
        rows = [replacements.get(row["figure_id"], row) for row in ours]
        write_csv(path, fields, rows, "Preserve local inventory; import six reviewed remote package claims pending scientific/scheduling separation.")

    write("PROJECT_STATE.md", blob(local, "PROJECT_STATE.md"), local,
          "Keep complete local inventory and approved plan; regenerate stale summary after state migration.")
    lessons = blob(local, "docs/lessons_learned.md") or b""
    addition = blob(remote, "docs/lessons_learned.md") or b""
    write("docs/lessons_learned.md", lessons + b"\n\n## Additional GitHub Recovery History\n\n" + addition,
          "both_parents", "Retain both histories; deduplication can follow evidence review.")
    # All conflicts must have an explicit policy above; do not silently pick a side.
    unresolved = git("diff", "--name-only", "--diff-filter=U").decode().splitlines()
    handled = {row["path"] for row in resolutions}
    unknown = set(unresolved) - handled
    if unknown:
        raise ValueError(f"No resolution policy for {sorted(unknown)}")
    manifest = {"schema_version": 1, "local_parent": local, "remote_parent": remote,
                "merge_base": base, "figure_policies": RECOVERIES, "resolutions": resolutions,
                "limitations": ["No scientific statuses promoted by import.",
                                "5-3 facsimile comparisons retained as historical evidence; original-pixel comparison pending.",
                                "Historical PROJECT_STATE/registry views require the next structured-state migration."]}
    if args.apply:
        report = ROOT / "reports/consolidation/import_manifest.json"
        report.write_text(json.dumps(manifest, indent=2) + "\n")
        subprocess.run(["git", "-C", str(ROOT), "add", "--", *unresolved], check=True)
    print(json.dumps({"apply": args.apply, "resolution_count": len(resolutions),
                      "conflicts_covered": len(unresolved), "figure_policies": RECOVERIES}, indent=2))


if __name__ == "__main__":
    main()
