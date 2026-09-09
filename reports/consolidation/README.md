# Consolidation Evidence

Date: 2026-09-09. Integration branch: `production-loop`.

The merge retains both the local production history at `efca126` and GitHub
main at `9a19519`. [import_manifest.json](import_manifest.json) records exact
parent commits, 152 file resolutions, hashes, and reasons. All 83 Git conflicts
have explicit resolutions in [the migration script](../../scripts/consolidate_history.py).
The original parent versions remain in Git; selected state snapshots are also
preserved under `snapshots/` for audit. Those snapshots are historical claims,
not current figure state.

[worker_import_manifest.json](worker_import_manifest.json) records a further
116 worker-delta file decisions. The 7-3 and 12-5 packages now include recovered
archived FAO regional data and a better ASN/World Bank successor indicator.
Missing 5-3 source files were added while retaining the newer OWID 522 package.
The 7-4 worker reconstruction used transcribed source-chart labels: its work is
quarantined under `worker_candidates/7-4`, and its plots are not canonical.
This prevents a visually convincing but insufficiently independent input from
being accepted as a reconstruction. Usable source/event-table evidence is retained.

## Figure Decisions

| Figure | Retained improvement | Limitations |
| --- | --- | --- |
| 4-1 | More complete publication/source recovery from GitHub; local PDF reference retained | Monthly numeric data remain unavailable. |
| 5-2 | Immutable CME Info 2016 component and clipped successor package | Full book-vintage assembly unresolved. |
| 5-3 | Preserved OWID 522 table, transformation, and continuation | Imported comparison uses a facsimile; restore actual local PDF reference before visual acceptance. |
| 5-4 | Clio birth component and ONS diagnostic; local reference and prior recovery files retained | Exact combined-population multi-age series unresolved; diagnostic is not a reconstruction. |
| 10-5 | Current UNCTAD bulk recovery and rejection evidence | Unsupported image-derived shipping values are not accepted reconstruction data. |
| 19-1 | Archived HumanProgress principal series and stacked-area encoding | Six minor-country layers remain a disclosed successor vintage. |

Both source-log and search-iteration histories are preserved for overlapping
packages. Bibliography catalogs use a keyed union; JSON mirrors are generated
from the same rows. New historical records from either branch are retained.

## Validation At Import

- Every merge conflict is covered by an explicit policy; no conflicts remain.
- All merged per-figure metadata and bibliography JSON files parse.
- All plots in the nine previously verified packages are byte-for-byte identical
  to the local parent: 5-1, 8-4, 8-5, 9-6, 10-3, 10-6, 10-7, 10-8, 12-9.
- No scientific status was promoted by import and no reconstruction script ran.

## Next Checkpoint

Separate scientific classifications from scheduling outcomes, generate consistent
state views, validate canonical paths, and rebuild the review manifest so it
cannot include status panels or facsimile comparisons as visual validation.
This import checkpoint alone does not establish publication readiness.
