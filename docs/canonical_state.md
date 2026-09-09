# Canonical Figure State

`figures/<id>/figure.json` is the current authority for each of the 75 figures.
The previous `metadata/metadata.json` files remain as attributed historical
research snapshots. Their old classifications do not override the canonical
record. The import source commits and conflicts are recorded in
[consolidation evidence](../reports/consolidation/README.md).

## Separate Decisions

- `scientific_status`: strength of the reconstruction/source evidence. Existing
  verified labels are imported claims until fresh review, as `status_evidence`
  makes explicit. Never infer this value from an executor or supervisor outcome.
- `execution_status`: queue state such as processed, accepted, blocked, or not
  started. An accepted source-recovery report can still lack a reconstruction.
- `publication_status`: incomplete, not reviewed, or ready. Ready requires
  scientific and editorial acceptance plus inspection of exact original-reference
  and comparison artifact hashes. Facsimiles cannot satisfy that requirement.
- `artifact_kind`: reconstruction, source recovery, or not started. Status panels
  and partial diagnostics belong to source recovery and are not gallery plots.
- `extension`: methodology decision, independent of the presence of a filename
  containing the word extended.

## Update And Validate

Edit the canonical record when a figure changes. Update its artifact paths and
SHA-256 hashes and invalidate any review of changed evidence. Then run:

```bash
.venv/bin/python scripts/project_state.py generate
.venv/bin/python scripts/project_state.py check
.venv/bin/python -m pytest -q tests/test_project_state.py
```

`generate` validates all records before replacing the generated views. `check`
is read-only and detects missing artifacts, changed hashes, invalid statuses,
escaping paths, and stale views. Individual files are replaced atomically;
multi-file publication still requires the transactional integration commit.
A crash between replacements is detected by `check` and repaired by `generate`.

Generated views are PROJECT_STATE, registry CSV and JSON, the aggregate metadata
CSV, the canonical artifact index, and marked summaries in each figure README.
The rest of each README is preserved. Do not edit those generated fields by hand.
The registry's compatibility field `current_status` always equals scientific
status; scheduling consumers must read `execution_status` separately.

`bootstrap` is a one-time migration and refuses to overwrite existing canonical
records. Import scripts and historical snapshots are not regular build commands.
The active orchestrator must implement this ownership contract before another
production batch; its old registry writer is not compatible with these views.
