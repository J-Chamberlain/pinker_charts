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
| 17-5 Spending on necessities | partial_match | Original 2016 HumanProgress five-component values cross-check BEA to numerical precision; adding energy recovers the book concept. Historical 2015 and revised 2025 data kept distinct; exact book component/endpoint remains unresolved. |
| 17-6 Leisure | partial_match | Original author analysis cells reproduce all ten published means at two decimals. BLS continuation to 2025 has no annual 2020 estimate. Population/activity changes and small book-level differences prevent verification. |
| 17-3 Utilities/appliances/housework | partial_match | Eight adoption curves from original author workbook and cited Census table. Housework only two confirmed numeric anchors; no fabricated trajectory. Stove definition changes; no comparable extension claimed. |
| 16-1 Literacy | verified_reproduction | Actual 2016 archived CSV recovers all eight curves; 14 US records independently match NCES. Revised UIS extension kept separate, with historical World anomalies explained. |
| 16-2 Basic education | partial_match | Original OWID archive and OECD StatLinks recover nine curves and133 exact table matches. XLS year-label defect documented; small visual offsets remain. Modern projections rejected as observed extension. |
| 16-3 Years of schooling | verified_reproduction | All203 original observations match archived author workbook. Seven curves visually close; author v3 updated2015 estimates provide a comparable dashed extension, not OWID's older forecasts. |
| 16-4 Female literacy | partial_match | Original WDI country observations recovered; England and World remain missing. Revised extension is separate and clearly dashed after 2014. |
| 16-5 IQ gains | partial_match | All six regional/World curves recovered from July 2015 OWID numerical data. Original supplement weights not independently verified; no comparable extension. |
| 16-6 Global well-being | partial_match | Both original numerical tables recovered. HIHD stops in 2007; its 2015 update and finer annual detail remain missing. Methodologically different successors not spliced. |
| 14-4 Executions, US | partial_match | Archived DPIC/Espy records and Census populations recovered; decade-average aggregation is inferred and small low-rate differences remain. Same-definition annual successor through 2025 is clearly separated. |
| 11-1 Great power war | partial_match | Archived Human Progress export recovers the Levy/Thompson 25-year trajectory. The 1988 cell is blank, 2000-2015 is a separate documented interval, and the post-2015 zero continuation is derived evidence; exact original table remains targeted recovery. |

## Data Deliverable

`data/database/pinker_data.sqlite` retains immutable snapshots, original clean
cell values and row data. Current catalog: 591 retained files, 123 clean CSV
tables, 58,997 rows. Counts include source-vintage overlap and diagnostics,
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

Review gallery and PDF now contain 43 real figure packages / 86 pages. Earlier
work hours/retirement and utilities/lighting/necessities/leisure pages were
inspected at their preceding checkpoints. Pages 51-56 contain literacy,
basic education and schooling. New pages 57-62 contain female literacy, IQ gains
and global well-being; all six final PDF pages were rendered and inspected
for clipping and legibility, in addition to original comparison PNG inspection.
Missing female-literacy curves remain an explicit publication blocker, not a
layout fix or an implied complete reconstruction. Air travel has a
Critical absence of data/reconstruction and is explicitly blocked from the
gallery. Other legacy packages retain their earlier unresolved QA findings.

## Validation

82 project tests pass using `.venv/bin/pytest -q`. A test initially compared a
rounded display value to the exact retained successor value; corrected the
test to 2.1665275, without changing any source data. Added root pytest path
configuration so direct pytest and python -m pytest resolve scripts equally.
Canonical checks cover all 75 figure records; SQLite integrity/current-snapshot
checks pass. No paid API needed. Source download failures remain in logs.

## Remaining Work

21 figures have not started. Source-only packages and legacy partials are not
finished reconstructions. All Chapter 17 figures now have reconstruction or recovery
packages, but only lighting is verified. Literacy/basic education/schooling add
three real comparison packages; the global PDF now includes these.
Next: continue the untouched queue after Figures 14-4 and 11-1. Full-project
data-use audit, portable dependency rebuilds, provider refresh adapters, unresolved-source recovery and final publication review are
still pending. This checkpoint is not a completion claim.

2026-09-10 Figure 11-2 checkpoint: PRIO 3.1 and UCDP v5.0 source files recover
the cited battle-deaths source family for 1946-2015; UCDP v26.1 supplies a
separate 2016-2023 successor. The original PDF chart and both comparison pages
were inspected. The trajectory is close, but the cited Census/McEvedy population
denominator and exact aggregation remain unresolved, so status is partial_match.
The next untouched candidate is Figure 11-3.

2026-09-10 Figure 11-3 checkpoint: the official PITF GenoPoliticide workbook
and historical UCDP v17.1 workbook were preserved and transformed into a
61-row book-period series; UCDP v26.1 supplies a separate 2017-2023 successor.
The original PDF and both comparison pages were inspected. The PITF ordinal
DEATHMAG decode materially under-reproduces the book's large historical peaks,
and the cited Census/McEvedy denominator is unresolved, so status is
partial_match. The data library now catalogs 608 files, 127 clean tables, and
59,143 clean rows. Nineteen figures remain untouched; the next candidate is
Figure 12-1.
