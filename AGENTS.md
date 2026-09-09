# Project Instructions

For this repository, start with:

1. [PROJECT_STATE.md](PROJECT_STATE.md).
2. [The approved completion plan](docs/completion_plan.md), including its progress ledger.
3. [The figure registry](data/figure_registry.csv) and the relevant figure package.
4. [Workflow](docs/workflow.md), [research review](docs/review_protocol.md), and
   [editorial review](docs/editorial_review_gate.md), as applicable to the task.

Follow the approved phases and their exit evidence. Complete the current
consolidation and validation gates before starting another production batch.
Use current repository evidence; do not assume a prior conversation's branch,
credentials, status labels, or reviewer capabilities are still accurate.

Do not equate execution acceptance with scientific verification. Inspect actual
original-reference and comparison images before claiming visual validation.
Never use digitized plotted values as reconstruction input.

Canonical state is `figures/<id>/figure.json`. Follow
[the state contract](docs/canonical_state.md); do not hand-edit generated registry
mirrors or PROJECT_STATE tables. Run `scripts/project_state.py generate` and
`scripts/project_state.py check` after canonical record changes.

Preserve existing work. At a meaningful checkpoint, update the plan's progress
ledger and PROJECT_STATE with evidence, remaining blockers, and the exact next
action. Unimplemented plan requirements must remain labeled as pending.
