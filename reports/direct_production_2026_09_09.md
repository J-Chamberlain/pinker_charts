# Direct production checkpoint, 2026-09-09

Owner direction: set paid API orchestration aside. Research, source preservation,
plotting and actual visual review are performed directly in the continuing task.
No model API calls, new agent branches, or main merges.

| Figure | Scientific status | Evidence and remaining issue |
| --- | --- | --- |
| 17-8 International tourism | partial_match | 2016 WDI history recovered; missing original-vintage 2015 endpoint explicitly uses later source. Dashed UN Tourism extension to provisional 2025; version gaps and pandemic scale change explained. |
| 17-7 Cost of air travel | needs_targeted_source_recovery | Thompson/A4A citation chain and archived pages recovered. Numeric Tableau export not recovered; fare versus cost-per-mile, CPI and fee definitions must be validated. No fake comparison. |
| 17-4 Cost of light | verified_reproduction | Original source dataset, 706 observations, 2016 identity and exact legacy CSV/API equality. Full line matches book. Revised 2026 source extends to 2023 without a forced join. |
| 17-1 Work hours | partial_match | Original paper table/OWID recovered; small visual level differences remain. No comparable post-2000 extension, explicitly labeled. |
| 17-2 Retirement | partial_match | Costa original table and BLS 2010 archive recovered; Short 2000 release/author assembly unresolved. Dashed BLS extension to 2024; historical definitions disclosed. |

## Data Deliverable

`data/database/pinker_data.sqlite` retains immutable snapshots, original clean
cell values and row data. Current catalog: 394 retained files, 76 clean CSV
tables, 37,308 rows. Counts include source-vintage overlap and diagnostics,
not just unique observations. Raw files stay in Git; the database indexes them.
New reconstructed figures declare exact raw -> clean -> script -> plot mappings
in per-figure lineage JSON and CSV with file checksums. Legacy mappings still
require audit; file presence is not proof of use in a current plot.

## Visual And Scientific QA

Actual original PDF crop beside each recreation, not a facsimile. Both new
reconstruction packages' book/extended pages inspected; lighting diagnostic
and tourism source-version diagnostic also inspected. Original scales and
variables preserved. Extension differences explained, not hidden. Lighting
inset clipping corrected automatically. Neither new figure uses digitized
chart values. This is direct self-review, not independent external approval.

Review gallery and PDF now contain 30 real figure packages / 60 pages. New pages
51-54 (work hours/retirement) rendered from the final PDF and inspected for clipping and legibility.
No new Critical visual issue remains in those four pages. Air travel has a
Critical absence of data/reconstruction and is explicitly blocked from the
gallery. Other legacy packages retain their earlier unresolved QA findings.

## Validation

63 project tests pass using `.venv/bin/pytest -q`. A test initially compared a
rounded display value to the exact retained successor value; corrected the
test to 2.1665275, without changing any source data. Added root pytest path
configuration so direct pytest and python -m pytest resolve scripts equally.
Canonical checks cover all 75 figure records; SQLite integrity/current-snapshot
checks pass. No paid API needed. Source download failures remain in logs.

## Remaining Work

35 figures have not started. Source-only packages and legacy partials are not
finished reconstructions. Continue remaining Chapter 17 sources, preserving source-family
continuity. Full-project data-use audit, portable dependency rebuilds, provider
refresh adapters, unresolved-source recovery and final publication review are
still pending. This checkpoint is not a completion claim.
