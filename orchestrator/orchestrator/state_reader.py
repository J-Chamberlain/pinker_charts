from __future__ import annotations

import csv
import json
from pathlib import Path

from .schemas import ProjectState


def read_project_state(state_file: Path, registry_file: Path | None = None, review_manifest: Path | None = None) -> ProjectState:
    raw_state = state_file.read_text() if state_file.exists() else ""
    rows: tuple[dict[str, str], ...] = ()
    if registry_file and registry_file.exists():
        with registry_file.open(newline="") as handle:
            rows = tuple(dict(row) for row in csv.DictReader(handle))
    manifest = None
    if review_manifest and review_manifest.exists():
        manifest = json.loads(review_manifest.read_text())
    return ProjectState(raw_state=raw_state, registry_rows=rows, review_manifest=manifest)
