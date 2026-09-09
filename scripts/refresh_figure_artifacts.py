"""Refresh one explicitly edited figure's hashes; never infer scientific status."""
import argparse

from project_state import ROOT, dumps, file_record, safe_path
import json

VISUAL = ("original_reference", "book_period_reconstruction", "extended_reconstruction",
          "book_period_comparison", "extended_comparison", "diagnostic_plot")


def refresh(fid, record_inspection=False):
    path = safe_path(ROOT, f"figures/{fid}/figure.json")
    record = json.loads(path.read_text())
    artifacts = record["artifacts"]
    old = dict(artifacts)
    for role, artifact in artifacts.items():
        if not artifact.get("self"):
            artifacts[role] = file_record(ROOT, artifact["path"])
    if any(old.get(role) != artifacts.get(role) for role in VISUAL):
        record["visual_review"].update(status="pending", inspected_artifacts=[])
        if record["publication_status"] == "ready":
            record["publication_status"] = "not_reviewed"
    if record_inspection:
        required = VISUAL[:5]
        if any(role not in artifacts for role in required):
            raise ValueError("Cannot record both comparisons inspected when essential artifacts are missing")
        record["visual_review"].update(status="inspected", reference_basis="original",
                                       inspected_artifacts=[artifacts[r] for r in VISUAL if r in artifacts])
    path.write_text(dumps(record))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--figure", required=True)
    parser.add_argument("--record-inspection", action="store_true", help="Only after actually opening and inspecting these exact images")
    args = parser.parse_args()
    refresh(args.figure, args.record_inspection)
