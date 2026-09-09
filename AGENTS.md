# Project Instructions

For this repository, start with:

1. [PROJECT_STATE.md](PROJECT_STATE.md).
2. [The approved completion plan](docs/completion_plan.md), including its progress ledger.
3. [The figure registry](data/figure_registry.csv) and the relevant figure package.
4. [Workflow](docs/workflow.md), [research review](docs/review_protocol.md), and
   [editorial review](docs/editorial_review_gate.md), as applicable to the task.

Follow the approved phases and their exit evidence. Complete the current
consolidation and validation gates before starting another production batch.
Owner direction (2026-09-09): proceed directly in the continuing Codex task;
set API orchestration/calibration aside. Do not block research on that optional
infrastructure. Preserve source validation, actual visual review and data history.
Use current repository evidence; do not assume a prior conversation's branch,
credentials, status labels, or reviewer capabilities are still accurate.

Do not equate execution acceptance with scientific verification. Inspect actual
original-reference and comparison images before claiming visual validation.
Never use digitized plotted values as reconstruction input.

Canonical state is `figures/<id>/figure.json`. Follow
[the state contract](docs/canonical_state.md); do not hand-edit generated registry
mirrors or PROJECT_STATE tables. Run `scripts/project_state.py generate` and
`scripts/project_state.py check` after canonical record changes.

Data are a long-lived deliverable. Follow [docs/data_library.md](docs/data_library.md):
preserve dated raw releases, versioned clean tables and exact per-plot lineage.
After data or canonical metadata changes, run `scripts/build_data_database.py build`
and `scripts/build_data_database.py check`. Do not overwrite book-era data with
successor releases or assume every retained table was used in a current plot.
API-review calibration is optional infrastructure, not a blocker for local research.

Preserve existing work. At a meaningful checkpoint, update the plan's progress
ledger and PROJECT_STATE with evidence, remaining blockers, and the exact next
action. Unimplemented plan requirements must remain labeled as pending.
