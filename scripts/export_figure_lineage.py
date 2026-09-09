"""Export explicitly declared per-plot mappings; do not infer use from presence."""
import argparse
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def export(figure_id):
    directory = ROOT / "figures" / figure_id / "lineage"
    data = json.loads((directory / "lineage.json").read_text())
    if data["figure_id"] != figure_id:
        raise ValueError("Figure identity mismatch")
    rows = []
    for mapping in data["mappings"]:
        for raw in mapping["raw_inputs"]:
            row = {"figure_id": figure_id, "book_citation": data["book_citation"],
                   "role": mapping["role"], "raw": raw, "script": data["script"],
                   **{key: mapping[key] for key in ["selection", "transformation", "clean", "plot"]}}
            for role in ["raw", "script", "clean", "plot"]:
                path = (ROOT / row[role]).resolve()
                if not path.is_relative_to(ROOT.resolve()):
                    raise ValueError("Lineage path escapes repository")
                row[role + "_sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
            rows.append(row)
    if not rows:
        raise ValueError("No numeric mappings declared")
    with (directory / "lineage.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--figure", required=True)
    export(parser.parse_args().figure)
