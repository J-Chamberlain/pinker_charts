# Figure Registry

The figure registry is the project-wide queue and status table for all figures
captured from the *Enlightenment Now* front-matter List of Figures.

Canonical files:

- [../data/figure_registry.csv](../data/figure_registry.csv)
- [../data/figure_registry.json](../data/figure_registry.json)

The registry is the first place to look when choosing future work. It prevents
figure state from living only in chat history, screenshots, or scattered notes.

## Fields

- `figure_id`: book figure number.
- `book`: source book.
- `chapter`: chapter number from the List of Figures.
- `title`: figure title from the List of Figures.
- `page`: book page if known. Blank means not yet available.
- `year_range`: year or range visible in the title.
- `current_status`: current reconstruction status.
- `lifecycle_stage`: current workflow stage.
- `source_type_guess`: initial guess about likely source family.
- `priority`: queue priority.
- `current_owner`: who or what currently owns the next action.
- `next_action`: immediate next step.
- `notes`: provenance and caveats for the registry row.

## Statuses

- `not_started`: listed in the book but not processed.
- `verified_reproduction`: original dataset or exact archival copy located and
  visual/evidential validation is satisfactory.
- `updated_equivalent`: same-institution successor data reproduces the concept
  but not the exact historical figure.
- `partial_match`: plausible data found, but important variables, years,
  transformations, or source vintage remain unresolved.
- `source_unavailable`: no usable public dataset found.
- `manual_review_needed`: evidence is ambiguous or multiple plausible sources
  require human judgment.

## Choosing The Next Batch

Future Codex runs should select small batches from the registry rather than
starting a whole chapter by default.

Recommended order:

1. Read [../PROJECT_STATE.md](../PROJECT_STATE.md).
2. Read this registry documentation.
3. Inspect `data/figure_registry.csv` for rows with `current_status =
   not_started`.
4. Prefer figures with clear titles, visible year ranges, likely institutional
   source families, or direct relevance to the current chapter goal.
5. Keep batches small enough that source discovery, plotting, visual review,
   discrepancy analysis, and metadata updates can all finish in one coherent
   pass.

Small batches make failures legible. They keep source searches from becoming
unbounded, make visual discrepancies easier to diagnose, and reduce the chance
that project state is left half-updated.

## Updating The Registry

Each completed or attempted figure must update its registry row before the run
finishes.

Update at least:

- `current_status`
- `lifecycle_stage`
- `priority`
- `current_owner`
- `next_action`
- `notes`

If a figure becomes active, add or update the corresponding figure directory.
If a figure is verified, make sure `PROJECT_STATE.md`, per-figure metadata,
provenance, anomaly review, captions, and canonical artifact paths agree.

## Relationship To PROJECT_STATE.md

`PROJECT_STATE.md` summarizes the active and completed project state. The
registry is the full table of all known figure work. When they disagree,
consider the repository inconsistent and reconcile both files before doing new
figure reconstruction.
