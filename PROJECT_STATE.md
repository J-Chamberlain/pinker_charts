# Project State

Generated from `figures/<id>/figure.json` by `scripts/project_state.py generate`.
Do not edit generated figure tables. The approved plan and progress ledger are in
[docs/completion_plan.md](docs/completion_plan.md).

## Mission

Reconstruct all 75 Enlightenment Now figures from legitimate source data, with
reproducible transformations, original-reference visual review, and defensible extensions.
Scientific status, execution outcome, and publication readiness are separate.

## Current Work

Integration branch: `production-loop`.
Read the completion-plan ledger for the current phase, exit evidence, and next action.
[Consolidation evidence](reports/consolidation/README.md) preserves both histories.
[Execution checkpoint](reports/completion_checkpoint_2026_09_09.md) records validation and remaining gates.
Historical classifications are retained as claims until independently re-reviewed.
A completed source search or accepted worker run is not a completed reconstruction.

## Reference And Review

- [Supplemental Graphics PDF](references/enlightenment_now_supplemental_graphics.pdf)
- [Registry](data/figure_registry.csv) and [JSON mirror](data/figure_registry.json)
- [Workflow](docs/workflow.md), [research review](docs/review_protocol.md), [editorial gate](docs/editorial_review_gate.md)
- [Canonical artifact index](data/canonical_artifacts.json)

- [Reusable data library](data/database/README.md) and [coverage catalog](data/database/catalog.json)
- [Original reference index](references/figure_index.json)
- [Consolidated visual audit gallery](reports/review_baseline/index.html)
- [Current review PDF](output/pdf/recreated_figures_review_scroll.pdf) and [manifest](output/pdf/recreated_figures_review_scroll.manifest.json)

Every future figure run must inspect and display actual book-period and extended
comparisons where available. Record exact inspected hashes and unresolved issues.
Do not digitize plotted values for reconstruction or promote weak source matches.
Update the canonical record and regenerate its views whenever an artifact changes.

## Scientific Inventory

| Status | Count |
| --- | ---: |
| blocked_external_source | 1 |
| manual_review_needed | 4 |
| needs_targeted_source_recovery | 1 |
| not_started | 11 |
| partial_match | 33 |
| source_chain_recovered | 2 |
| source_unavailable | 1 |
| updated_equivalent | 10 |
| verified_reproduction | 12 |

## Figure Queue

| Figure | Title | Scientific status | Execution | Publication |
| --- | --- | --- | --- | --- |
| 4-1 | Tone of the news, 1945-2010 | source_unavailable | blocked | incomplete |
| 5-1 | Life expectancy, 1771-2015 | verified_reproduction | processed | not_reviewed |
| 5-2 | Child mortality, 1751-2013 | partial_match | blocked | not_reviewed |
| 5-3 | Maternal mortality, 1751-2013 | partial_match | accepted | not_reviewed |
| 5-4 | Life expectancy, UK, 1701-2013 | partial_match | blocked | incomplete |
| 6-1 | Childhood deaths from infectious disease, 2000-2013 | blocked_external_source | processed | incomplete |
| 7-1 | Calories, 1700-2013 | partial_match | blocked | not_reviewed |
| 7-2 | Childhood stunting, 1966-2014 | partial_match | processed | not_reviewed |
| 7-3 | Undernourishment, 1970-2015 | partial_match | accepted | not_reviewed |
| 7-4 | Famine deaths, 1860-2016 | partial_match | blocked | not_reviewed |
| 8-1 | Gross World Product, 1-2015 | updated_equivalent | processed | not_reviewed |
| 8-2 | GDP per capita, 1600-2015 | updated_equivalent | processed | not_reviewed |
| 8-3 | World income distribution, 1800, 1975, and 2015 | updated_equivalent | processed | not_reviewed |
| 8-4 | Extreme poverty (proportion), 1820-2015 | verified_reproduction | processed | not_reviewed |
| 8-5 | Extreme poverty (number), 1820-2015 | verified_reproduction | processed | not_reviewed |
| 9-1 | International inequality, 1820-2013 | manual_review_needed | blocked | incomplete |
| 9-2 | Global inequality, 1820-2011 | manual_review_needed | blocked | incomplete |
| 9-3 | Inequality, UK and US, 1688-2013 | manual_review_needed | blocked | incomplete |
| 9-4 | Social spending, OECD countries, 1880-2016 | updated_equivalent | processed | not_reviewed |
| 9-5 | Income gains, 1988-2008 | partial_match | blocked | not_reviewed |
| 9-6 | Poverty, US, 1960-2016 | verified_reproduction | processed | not_reviewed |
| 10-1 | Population and population growth, 1750-2015 and projected to 2100 | updated_equivalent | processed | not_reviewed |
| 10-2 | Sustainability, 1955-2109 | updated_equivalent | processed | not_reviewed |
| 10-3 | Pollution, energy, and growth, US, 1970-2015 | verified_reproduction | processed | not_reviewed |
| 10-4 | Deforestation, 1700-2010 | manual_review_needed | blocked | incomplete |
| 10-5 | Oil spills, 1970-2016 | partial_match | blocked | not_reviewed |
| 10-6 | Protected areas, 1990-2014 | verified_reproduction | processed | not_reviewed |
| 10-7 | Carbon intensity (CO2 emissions per dollar of GDP), 1820-2014 | verified_reproduction | processed | not_reviewed |
| 10-8 | CO2 emissions, 1960-2015 | verified_reproduction | processed | not_reviewed |
| 11-1 | Great power war, 1500-2015 | partial_match | processed | incomplete |
| 11-2 | Battle deaths, 1946-2016 | partial_match | processed | incomplete |
| 11-3 | Genocide deaths, 1956-2016 | partial_match | processed | not_reviewed |
| 12-1 | Homicide deaths, Western Europe, US, and Mexico, 1300-2015 | partial_match | processed | not_reviewed |
| 12-2 | Homicide deaths, 1967-2015 | partial_match | processed | not_reviewed |
| 12-3 | Motor vehicle accident deaths, US, 1921-2015 | source_chain_recovered | processed | incomplete |
| 12-4 | Pedestrian deaths, US, 1927-2015 | source_chain_recovered | processed | incomplete |
| 12-5 | Plane crash deaths, 1970-2015 | partial_match | blocked | not_reviewed |
| 12-6 | Deaths from falls, fire, drowning, and poison, US, 1903-2014 | updated_equivalent | processed | not_reviewed |
| 12-7 | Occupational accident deaths, US, 1913-2015 | partial_match | processed | not_reviewed |
| 12-8 | Natural disaster deaths, 1900-2015 | updated_equivalent | processed | not_reviewed |
| 12-9 | Lightning strike deaths, US, 1900-2015 | verified_reproduction | processed | not_reviewed |
| 13-1 | Terrorism deaths, 1970-2015 | updated_equivalent | processed | not_reviewed |
| 14-1 | Democracy versus autocracy, 1800-2015 | partial_match | processed | incomplete |
| 14-2 | Human rights, 1949-2014 | partial_match | processed | incomplete |
| 14-3 | Death penalty abolitions, 1863-2016 | partial_match | processed | incomplete |
| 14-4 | Executions, US, 1780-2016 | partial_match | processed | incomplete |
| 15-1 | Racist, sexist, and homophobic opinions, US, 1987-2012 | partial_match | processed | not_reviewed |
| 15-2 | Racist, sexist, and homophobic Web searches, US, 2004-2017 | partial_match | processed | not_reviewed |
| 15-3 | Hate crimes, US, 1996-2015 | updated_equivalent | processed | not_reviewed |
| 15-4 | Rape and domestic violence, US, 1993-2014 | not_started | not_started | incomplete |
| 15-5 | Decriminalization of homosexuality, 1791-2016 | not_started | not_started | incomplete |
| 15-6 | Liberal values across time and generations, developed countries, 1980-2005 | not_started | not_started | incomplete |
| 15-7 | Liberal values across time (extrapolated), world's culture zones, 1960-2006 | not_started | not_started | incomplete |
| 15-8 | Victimization of children, US, 1993-2012 | not_started | not_started | incomplete |
| 15-9 | Child labor, 1850-2012 | not_started | not_started | incomplete |
| 16-1 | Literacy, 1475-2010 | verified_reproduction | processed | incomplete |
| 16-2 | Basic education, 1820-2010 | partial_match | processed | incomplete |
| 16-3 | Years of schooling, 1870-2010 | verified_reproduction | processed | incomplete |
| 16-4 | Female literacy, 1750-2014 | partial_match | processed | incomplete |
| 16-5 | IQ gains, 1909-2013 | partial_match | processed | incomplete |
| 16-6 | Global well-being, 1820-2015 | partial_match | processed | incomplete |
| 17-1 | Work hours, Western Europe and US, 1870-2000 | partial_match | processed | incomplete |
| 17-2 | Retirement, US, 1880-2010 | partial_match | processed | incomplete |
| 17-3 | Utilities, appliances, and housework, US, 1900-2015 | partial_match | processed | incomplete |
| 17-4 | Cost of light, England, 1300-2006 | verified_reproduction | processed | not_reviewed |
| 17-5 | Spending on necessities, US, 1929-2016 | partial_match | processed | incomplete |
| 17-6 | Leisure time, US, 1965-2015 | partial_match | processed | incomplete |
| 17-7 | Cost of air travel, US, 1979-2015 | needs_targeted_source_recovery | blocked | incomplete |
| 17-8 | International tourism, 1995-2015 | partial_match | processed | incomplete |
| 18-1 | Life satisfaction and income, 2006 | not_started | not_started | incomplete |
| 18-2 | Loneliness, US students, 1978-2011 | not_started | not_started | incomplete |
| 18-3 | Suicide, England, Switzerland, and US, 1860-2014 | not_started | not_started | incomplete |
| 18-4 | Happiness and excitement, US, 1972-2016 | not_started | not_started | incomplete |
| 19-1 | Nuclear weapons, 1945-2015 | partial_match | blocked | not_reviewed |
| 20-1 | Populist support across generations, 2016 | not_started | not_started | incomplete |

## Canonical Figure Artifacts

### Figure 4-1 - Tone of the news, 1945-2010

Status: `source_unavailable`. Artifact kind: `source_recovery`.

- Original reference: [references/figures/figure_4_1.png](references/figures/figure_4_1.png)
- Caption: [figures/4-1/captions/caption.txt](figures/4-1/captions/caption.txt)
- Provenance: [figures/4-1/provenance/provenance.md](figures/4-1/provenance/provenance.md)
- Anomaly review: [figures/4-1/anomaly_reviews/anomaly_review.md](figures/4-1/anomaly_reviews/anomaly_review.md)
- Review checklist: [figures/4-1/review_checklist.md](figures/4-1/review_checklist.md)
- Source log: [figures/4-1/source_logs/source_log.md](figures/4-1/source_logs/source_log.md)
- Search log: [figures/4-1/search_iterations/search_iterations.md](figures/4-1/search_iterations/search_iterations.md)
- Discrepancy log: [figures/4-1/discrepancy_logs/discrepancy_log.md](figures/4-1/discrepancy_logs/discrepancy_log.md)
- Legacy metadata: [figures/4-1/metadata/metadata.json](figures/4-1/metadata/metadata.json)
- Metadata: [figures/4-1/figure.json](figures/4-1/figure.json)

### Figure 5-1 - Life expectancy, 1771-2015

Status: `verified_reproduction`. Artifact kind: `reconstruction`.

- Original reference: [references/figures/figure_5_1.png](references/figures/figure_5_1.png)
- Book period reconstruction: [figures/5-1/plots/book_period/figure_5_1_book_period_reconstruction.png](figures/5-1/plots/book_period/figure_5_1_book_period_reconstruction.png)
- Extended reconstruction: [figures/5-1/plots/book_period/figure_5_1_book_period_reconstruction.png](figures/5-1/plots/book_period/figure_5_1_book_period_reconstruction.png)
- Book period comparison: [figures/5-1/plots/comparisons/figure_5_1_book_period_review.png](figures/5-1/plots/comparisons/figure_5_1_book_period_review.png)
- Extended comparison: [figures/5-1/plots/comparisons/figure_5_1_extended_review.png](figures/5-1/plots/comparisons/figure_5_1_extended_review.png)
- Caption: [figures/5-1/captions/caption.txt](figures/5-1/captions/caption.txt)
- Provenance: [figures/5-1/provenance/provenance.md](figures/5-1/provenance/provenance.md)
- Anomaly review: [figures/5-1/anomaly_reviews/anomaly_review.md](figures/5-1/anomaly_reviews/anomaly_review.md)
- Review checklist: [figures/5-1/review_checklist.md](figures/5-1/review_checklist.md)
- Source log: [figures/5-1/source_logs/source_log.md](figures/5-1/source_logs/source_log.md)
- Search log: [figures/5-1/search_iterations/search_iterations.md](figures/5-1/search_iterations/search_iterations.md)
- Discrepancy log: [figures/5-1/discrepancy_logs/discrepancy_log.md](figures/5-1/discrepancy_logs/discrepancy_log.md)
- Legacy metadata: [figures/5-1/metadata/metadata.json](figures/5-1/metadata/metadata.json)
- Metadata: [figures/5-1/figure.json](figures/5-1/figure.json)

### Figure 5-2 - Child mortality, 1751-2013

Status: `partial_match`. Artifact kind: `reconstruction`.

- Original reference: [references/figures/figure_5_2.png](references/figures/figure_5_2.png)
- Book period reconstruction: [figures/5-2/plots/book_period/figure_5_2_book_period_reconstruction.png](figures/5-2/plots/book_period/figure_5_2_book_period_reconstruction.png)
- Extended reconstruction: [figures/5-2/plots/book_period/figure_5_2_book_period_reconstruction.png](figures/5-2/plots/book_period/figure_5_2_book_period_reconstruction.png)
- Book period comparison: [figures/5-2/plots/comparisons/figure_5_2_book_period_review.png](figures/5-2/plots/comparisons/figure_5_2_book_period_review.png)
- Extended comparison: [figures/5-2/plots/comparisons/figure_5_2_extended_review.png](figures/5-2/plots/comparisons/figure_5_2_extended_review.png)
- Caption: [figures/5-2/captions/caption.txt](figures/5-2/captions/caption.txt)
- Provenance: [figures/5-2/provenance/provenance.md](figures/5-2/provenance/provenance.md)
- Anomaly review: [figures/5-2/anomaly_reviews/anomaly_review.md](figures/5-2/anomaly_reviews/anomaly_review.md)
- Review checklist: [figures/5-2/review_checklist.md](figures/5-2/review_checklist.md)
- Source log: [figures/5-2/source_logs/source_log.md](figures/5-2/source_logs/source_log.md)
- Search log: [figures/5-2/search_iterations/search_iterations.md](figures/5-2/search_iterations/search_iterations.md)
- Discrepancy log: [figures/5-2/discrepancy_logs/discrepancy_log.md](figures/5-2/discrepancy_logs/discrepancy_log.md)
- Legacy metadata: [figures/5-2/metadata/metadata.json](figures/5-2/metadata/metadata.json)
- Metadata: [figures/5-2/figure.json](figures/5-2/figure.json)

### Figure 5-3 - Maternal mortality, 1751-2013

Status: `partial_match`. Artifact kind: `reconstruction`.

- Original reference: [references/figures/figure_5_3.png](references/figures/figure_5_3.png)
- Book period reconstruction: [figures/5-3/plots/book_period/figure_5_3_book_period_reconstruction.png](figures/5-3/plots/book_period/figure_5_3_book_period_reconstruction.png)
- Extended reconstruction: [figures/5-3/plots/extended/figure_5_3_same_source_continuation.png](figures/5-3/plots/extended/figure_5_3_same_source_continuation.png)
- Book period comparison: [figures/5-3/plots/comparisons/figure_5_3_book_period_review.png](figures/5-3/plots/comparisons/figure_5_3_book_period_review.png)
- Extended comparison: [figures/5-3/plots/comparisons/figure_5_3_extended_review.png](figures/5-3/plots/comparisons/figure_5_3_extended_review.png)
- Caption: [figures/5-3/captions/caption.txt](figures/5-3/captions/caption.txt)
- Provenance: [figures/5-3/provenance/provenance.md](figures/5-3/provenance/provenance.md)
- Anomaly review: [figures/5-3/anomaly_reviews/anomaly_review.md](figures/5-3/anomaly_reviews/anomaly_review.md)
- Review checklist: [figures/5-3/review_checklist.md](figures/5-3/review_checklist.md)
- Source log: [figures/5-3/source_logs/source_log.md](figures/5-3/source_logs/source_log.md)
- Search log: [figures/5-3/search_iterations/search_iterations.md](figures/5-3/search_iterations/search_iterations.md)
- Discrepancy log: [figures/5-3/discrepancy_logs/discrepancy_log.md](figures/5-3/discrepancy_logs/discrepancy_log.md)
- Legacy metadata: [figures/5-3/metadata/metadata.json](figures/5-3/metadata/metadata.json)
- Metadata: [figures/5-3/figure.json](figures/5-3/figure.json)
- Source validation: [figures/5-3/provenance/early_sweden_validation.json](figures/5-3/provenance/early_sweden_validation.json)
- Reconstruction script: [scripts/reconstruct_5_3.py](scripts/reconstruct_5_3.py)
- Book period clean: [figures/5-3/data/clean/figure_5_3_book_period_clean.csv](figures/5-3/data/clean/figure_5_3_book_period_clean.csv)
- Extended clean: [figures/5-3/data/clean/figure_5_3_same_source_continuation_clean.csv](figures/5-3/data/clean/figure_5_3_same_source_continuation_clean.csv)
- Original source table: [figures/5-3/data/raw/gapminder_gd010_gapdata010.xls](figures/5-3/data/raw/gapminder_gd010_gapdata010.xls)
- Preserved source table: [figures/5-3/data/raw/owid_522_maternal_mortality.tab](figures/5-3/data/raw/owid_522_maternal_mortality.tab)
- Lineage: [figures/5-3/lineage/consolidated_lineage.json](figures/5-3/lineage/consolidated_lineage.json)

### Figure 5-4 - Life expectancy, UK, 1701-2013

Status: `partial_match`. Artifact kind: `source_recovery`.

- Original reference: [references/figures/figure_5_4.png](references/figures/figure_5_4.png)
- Caption: [figures/5-4/captions/caption.txt](figures/5-4/captions/caption.txt)
- Provenance: [figures/5-4/provenance/provenance.md](figures/5-4/provenance/provenance.md)
- Anomaly review: [figures/5-4/anomaly_reviews/anomaly_review.md](figures/5-4/anomaly_reviews/anomaly_review.md)
- Review checklist: [figures/5-4/review_checklist.md](figures/5-4/review_checklist.md)
- Source log: [figures/5-4/source_logs/source_log.md](figures/5-4/source_logs/source_log.md)
- Search log: [figures/5-4/search_iterations/search_iterations.md](figures/5-4/search_iterations/search_iterations.md)
- Discrepancy log: [figures/5-4/discrepancy_logs/discrepancy_log.md](figures/5-4/discrepancy_logs/discrepancy_log.md)
- Legacy metadata: [figures/5-4/metadata/metadata.json](figures/5-4/metadata/metadata.json)
- Metadata: [figures/5-4/figure.json](figures/5-4/figure.json)

### Figure 6-1 - Childhood deaths from infectious disease, 2000-2013

Status: `blocked_external_source`. Artifact kind: `source_recovery`.

- Original reference: [references/figures/figure_6_1.png](references/figures/figure_6_1.png)
- Caption: [figures/6-1/captions/caption.txt](figures/6-1/captions/caption.txt)
- Provenance: [figures/6-1/provenance/provenance.md](figures/6-1/provenance/provenance.md)
- Anomaly review: [figures/6-1/anomaly_reviews/anomaly_review.md](figures/6-1/anomaly_reviews/anomaly_review.md)
- Review checklist: [figures/6-1/review_checklist.md](figures/6-1/review_checklist.md)
- Source log: [figures/6-1/source_logs/source_log.md](figures/6-1/source_logs/source_log.md)
- Search log: [figures/6-1/search_iterations/search_iterations.md](figures/6-1/search_iterations/search_iterations.md)
- Discrepancy log: [figures/6-1/discrepancy_logs/discrepancy_log.md](figures/6-1/discrepancy_logs/discrepancy_log.md)
- Legacy metadata: [figures/6-1/metadata/metadata.json](figures/6-1/metadata/metadata.json)
- Metadata: [figures/6-1/figure.json](figures/6-1/figure.json)

### Figure 7-1 - Calories, 1700-2013

Status: `partial_match`. Artifact kind: `reconstruction`.

- Original reference: [references/figures/figure_7_1.png](references/figures/figure_7_1.png)
- Book period reconstruction: [figures/7-1/plots/book_period/figure_7_1_book_period_reconstruction.png](figures/7-1/plots/book_period/figure_7_1_book_period_reconstruction.png)
- Extended reconstruction: [figures/7-1/plots/extended/figure_7_1_extended_reconstruction.png](figures/7-1/plots/extended/figure_7_1_extended_reconstruction.png)
- Book period comparison: [figures/7-1/plots/comparisons/figure_7_1_book_period_review.png](figures/7-1/plots/comparisons/figure_7_1_book_period_review.png)
- Extended comparison: [figures/7-1/plots/comparisons/figure_7_1_extended_review.png](figures/7-1/plots/comparisons/figure_7_1_extended_review.png)
- Caption: [figures/7-1/captions/caption.txt](figures/7-1/captions/caption.txt)
- Provenance: [figures/7-1/provenance/provenance.md](figures/7-1/provenance/provenance.md)
- Anomaly review: [figures/7-1/anomaly_reviews/anomaly_review.md](figures/7-1/anomaly_reviews/anomaly_review.md)
- Review checklist: [figures/7-1/review_checklist.md](figures/7-1/review_checklist.md)
- Source log: [figures/7-1/source_logs/source_log.md](figures/7-1/source_logs/source_log.md)
- Search log: [figures/7-1/search_iterations/search_iterations.md](figures/7-1/search_iterations/search_iterations.md)
- Discrepancy log: [figures/7-1/discrepancy_logs/discrepancy_log.md](figures/7-1/discrepancy_logs/discrepancy_log.md)
- Legacy metadata: [figures/7-1/metadata/metadata.json](figures/7-1/metadata/metadata.json)
- Metadata: [figures/7-1/figure.json](figures/7-1/figure.json)

### Figure 7-2 - Childhood stunting, 1966-2014

Status: `partial_match`. Artifact kind: `reconstruction`.

- Original reference: [references/figures/figure_7_2.png](references/figures/figure_7_2.png)
- Book period reconstruction: [figures/7-2/plots/book_period/figure_7_2_book_period_reconstruction.png](figures/7-2/plots/book_period/figure_7_2_book_period_reconstruction.png)
- Extended reconstruction: [figures/7-2/plots/extended/figure_7_2_extended_reconstruction.png](figures/7-2/plots/extended/figure_7_2_extended_reconstruction.png)
- Book period comparison: [figures/7-2/plots/comparisons/figure_7_2_book_period_review.png](figures/7-2/plots/comparisons/figure_7_2_book_period_review.png)
- Extended comparison: [figures/7-2/plots/comparisons/figure_7_2_extended_review.png](figures/7-2/plots/comparisons/figure_7_2_extended_review.png)
- Caption: [figures/7-2/captions/caption.txt](figures/7-2/captions/caption.txt)
- Provenance: [figures/7-2/provenance/provenance.md](figures/7-2/provenance/provenance.md)
- Anomaly review: [figures/7-2/anomaly_reviews/anomaly_review.md](figures/7-2/anomaly_reviews/anomaly_review.md)
- Review checklist: [figures/7-2/review_checklist.md](figures/7-2/review_checklist.md)
- Source log: [figures/7-2/source_logs/source_log.md](figures/7-2/source_logs/source_log.md)
- Search log: [figures/7-2/search_iterations/search_iterations.md](figures/7-2/search_iterations/search_iterations.md)
- Discrepancy log: [figures/7-2/discrepancy_logs/discrepancy_log.md](figures/7-2/discrepancy_logs/discrepancy_log.md)
- Legacy metadata: [figures/7-2/metadata/metadata.json](figures/7-2/metadata/metadata.json)
- Metadata: [figures/7-2/figure.json](figures/7-2/figure.json)

### Figure 7-3 - Undernourishment, 1970-2015

Status: `partial_match`. Artifact kind: `reconstruction`.

- Original reference: [references/figures/figure_7_3.png](references/figures/figure_7_3.png)
- Book period reconstruction: [figures/7-3/plots/book_period/figure_7_3_book_period_reconstruction.png](figures/7-3/plots/book_period/figure_7_3_book_period_reconstruction.png)
- Extended reconstruction: [figures/7-3/plots/book_period/figure_7_3_book_period_reconstruction.png](figures/7-3/plots/book_period/figure_7_3_book_period_reconstruction.png)
- Book period comparison: [figures/7-3/plots/comparisons/figure_7_3_book_period_review.png](figures/7-3/plots/comparisons/figure_7_3_book_period_review.png)
- Extended comparison: [figures/7-3/plots/comparisons/figure_7_3_extended_review.png](figures/7-3/plots/comparisons/figure_7_3_extended_review.png)
- Caption: [figures/7-3/captions/caption.txt](figures/7-3/captions/caption.txt)
- Provenance: [figures/7-3/provenance/provenance.md](figures/7-3/provenance/provenance.md)
- Anomaly review: [figures/7-3/anomaly_reviews/anomaly_review.md](figures/7-3/anomaly_reviews/anomaly_review.md)
- Review checklist: [figures/7-3/review_checklist.md](figures/7-3/review_checklist.md)
- Source log: [figures/7-3/source_logs/source_log.md](figures/7-3/source_logs/source_log.md)
- Search log: [figures/7-3/search_iterations/search_iterations.md](figures/7-3/search_iterations/search_iterations.md)
- Discrepancy log: [figures/7-3/discrepancy_logs/discrepancy_log.md](figures/7-3/discrepancy_logs/discrepancy_log.md)
- Legacy metadata: [figures/7-3/metadata/metadata.json](figures/7-3/metadata/metadata.json)
- Metadata: [figures/7-3/figure.json](figures/7-3/figure.json)

### Figure 7-4 - Famine deaths, 1860-2016

Status: `partial_match`. Artifact kind: `reconstruction`.

- Original reference: [references/figures/figure_7_4.png](references/figures/figure_7_4.png)
- Book period reconstruction: [figures/7-4/plots/book_period/figure_7_4_book_period_reconstruction.png](figures/7-4/plots/book_period/figure_7_4_book_period_reconstruction.png)
- Extended reconstruction: [figures/7-4/plots/extended/figure_7_4_extended_reconstruction.png](figures/7-4/plots/extended/figure_7_4_extended_reconstruction.png)
- Book period comparison: [figures/7-4/plots/comparisons/figure_7_4_book_period_review.png](figures/7-4/plots/comparisons/figure_7_4_book_period_review.png)
- Extended comparison: [figures/7-4/plots/comparisons/figure_7_4_extended_review.png](figures/7-4/plots/comparisons/figure_7_4_extended_review.png)
- Caption: [figures/7-4/captions/caption.txt](figures/7-4/captions/caption.txt)
- Provenance: [figures/7-4/provenance/provenance.md](figures/7-4/provenance/provenance.md)
- Anomaly review: [figures/7-4/anomaly_reviews/anomaly_review.md](figures/7-4/anomaly_reviews/anomaly_review.md)
- Review checklist: [figures/7-4/review_checklist.md](figures/7-4/review_checklist.md)
- Source log: [figures/7-4/source_logs/source_log.md](figures/7-4/source_logs/source_log.md)
- Search log: [figures/7-4/search_iterations/search_iterations.md](figures/7-4/search_iterations/search_iterations.md)
- Discrepancy log: [figures/7-4/discrepancy_logs/discrepancy_log.md](figures/7-4/discrepancy_logs/discrepancy_log.md)
- Legacy metadata: [figures/7-4/metadata/metadata.json](figures/7-4/metadata/metadata.json)
- Metadata: [figures/7-4/figure.json](figures/7-4/figure.json)

### Figure 8-1 - Gross World Product, 1-2015

Status: `updated_equivalent`. Artifact kind: `reconstruction`.

- Original reference: [references/figures/figure_8_1.png](references/figures/figure_8_1.png)
- Book period reconstruction: [figures/8-1/plots/book_period/figure_8_1_book_period_reconstruction.png](figures/8-1/plots/book_period/figure_8_1_book_period_reconstruction.png)
- Extended reconstruction: [figures/8-1/plots/extended/figure_8_1_extended_reconstruction.png](figures/8-1/plots/extended/figure_8_1_extended_reconstruction.png)
- Book period comparison: [figures/8-1/plots/comparisons/figure_8_1_book_period_review.png](figures/8-1/plots/comparisons/figure_8_1_book_period_review.png)
- Extended comparison: [figures/8-1/plots/comparisons/figure_8_1_extended_review.png](figures/8-1/plots/comparisons/figure_8_1_extended_review.png)
- Caption: [figures/8-1/captions/caption.txt](figures/8-1/captions/caption.txt)
- Provenance: [figures/8-1/provenance/provenance.md](figures/8-1/provenance/provenance.md)
- Anomaly review: [figures/8-1/anomaly_reviews/anomaly_review.md](figures/8-1/anomaly_reviews/anomaly_review.md)
- Review checklist: [figures/8-1/review_checklist.md](figures/8-1/review_checklist.md)
- Source log: [figures/8-1/source_logs/source_log.md](figures/8-1/source_logs/source_log.md)
- Search log: [figures/8-1/search_iterations/search_iterations.md](figures/8-1/search_iterations/search_iterations.md)
- Discrepancy log: [figures/8-1/discrepancy_logs/discrepancy_log.md](figures/8-1/discrepancy_logs/discrepancy_log.md)
- Legacy metadata: [figures/8-1/metadata/metadata.json](figures/8-1/metadata/metadata.json)
- Metadata: [figures/8-1/figure.json](figures/8-1/figure.json)

### Figure 8-2 - GDP per capita, 1600-2015

Status: `updated_equivalent`. Artifact kind: `reconstruction`.

- Original reference: [references/figures/figure_8_2.png](references/figures/figure_8_2.png)
- Book period reconstruction: [figures/8-2/plots/book_period/figure_8_2_book_period_reconstruction.png](figures/8-2/plots/book_period/figure_8_2_book_period_reconstruction.png)
- Extended reconstruction: [figures/8-2/plots/extended/figure_8_2_extended_reconstruction.png](figures/8-2/plots/extended/figure_8_2_extended_reconstruction.png)
- Book period comparison: [figures/8-2/plots/comparisons/figure_8_2_book_period_review.png](figures/8-2/plots/comparisons/figure_8_2_book_period_review.png)
- Extended comparison: [figures/8-2/plots/comparisons/figure_8_2_extended_review.png](figures/8-2/plots/comparisons/figure_8_2_extended_review.png)
- Caption: [figures/8-2/captions/caption.txt](figures/8-2/captions/caption.txt)
- Provenance: [figures/8-2/provenance/provenance.md](figures/8-2/provenance/provenance.md)
- Anomaly review: [figures/8-2/anomaly_reviews/anomaly_review.md](figures/8-2/anomaly_reviews/anomaly_review.md)
- Review checklist: [figures/8-2/review_checklist.md](figures/8-2/review_checklist.md)
- Source log: [figures/8-2/source_logs/source_log.md](figures/8-2/source_logs/source_log.md)
- Search log: [figures/8-2/search_iterations/search_iterations.md](figures/8-2/search_iterations/search_iterations.md)
- Discrepancy log: [figures/8-2/discrepancy_logs/discrepancy_log.md](figures/8-2/discrepancy_logs/discrepancy_log.md)
- Legacy metadata: [figures/8-2/metadata/metadata.json](figures/8-2/metadata/metadata.json)
- Metadata: [figures/8-2/figure.json](figures/8-2/figure.json)

### Figure 8-3 - World income distribution, 1800, 1975, and 2015

Status: `updated_equivalent`. Artifact kind: `reconstruction`.

- Original reference: [references/figures/figure_8_3.png](references/figures/figure_8_3.png)
- Book period reconstruction: [figures/8-3/plots/book_period/figure_8_3_book_period_reconstruction.png](figures/8-3/plots/book_period/figure_8_3_book_period_reconstruction.png)
- Extended reconstruction: [figures/8-3/plots/book_period/figure_8_3_book_period_reconstruction.png](figures/8-3/plots/book_period/figure_8_3_book_period_reconstruction.png)
- Book period comparison: [figures/8-3/plots/comparisons/figure_8_3_book_period_review.png](figures/8-3/plots/comparisons/figure_8_3_book_period_review.png)
- Extended comparison: [figures/8-3/plots/comparisons/figure_8_3_extended_review.png](figures/8-3/plots/comparisons/figure_8_3_extended_review.png)
- Caption: [figures/8-3/captions/caption.txt](figures/8-3/captions/caption.txt)
- Provenance: [figures/8-3/provenance/provenance.md](figures/8-3/provenance/provenance.md)
- Anomaly review: [figures/8-3/anomaly_reviews/anomaly_review.md](figures/8-3/anomaly_reviews/anomaly_review.md)
- Review checklist: [figures/8-3/review_checklist.md](figures/8-3/review_checklist.md)
- Source log: [figures/8-3/source_logs/source_log.md](figures/8-3/source_logs/source_log.md)
- Search log: [figures/8-3/search_iterations/search_iterations.md](figures/8-3/search_iterations/search_iterations.md)
- Discrepancy log: [figures/8-3/discrepancy_logs/discrepancy_log.md](figures/8-3/discrepancy_logs/discrepancy_log.md)
- Legacy metadata: [figures/8-3/metadata/metadata.json](figures/8-3/metadata/metadata.json)
- Metadata: [figures/8-3/figure.json](figures/8-3/figure.json)

### Figure 8-4 - Extreme poverty (proportion), 1820-2015

Status: `verified_reproduction`. Artifact kind: `reconstruction`.

- Original reference: [references/figures/figure_8_4.png](references/figures/figure_8_4.png)
- Book period reconstruction: [figures/8-4/plots/book_period/figure_8_4_book_period_reconstruction.png](figures/8-4/plots/book_period/figure_8_4_book_period_reconstruction.png)
- Extended reconstruction: [figures/8-4/plots/book_period/figure_8_4_book_period_reconstruction.png](figures/8-4/plots/book_period/figure_8_4_book_period_reconstruction.png)
- Book period comparison: [figures/8-4/plots/comparisons/figure_8_4_book_period_review.png](figures/8-4/plots/comparisons/figure_8_4_book_period_review.png)
- Extended comparison: [figures/8-4/plots/comparisons/figure_8_4_extended_review.png](figures/8-4/plots/comparisons/figure_8_4_extended_review.png)
- Caption: [figures/8-4/captions/caption.txt](figures/8-4/captions/caption.txt)
- Provenance: [figures/8-4/provenance/provenance.md](figures/8-4/provenance/provenance.md)
- Anomaly review: [figures/8-4/anomaly_reviews/anomaly_review.md](figures/8-4/anomaly_reviews/anomaly_review.md)
- Review checklist: [figures/8-4/review_checklist.md](figures/8-4/review_checklist.md)
- Source log: [figures/8-4/source_logs/source_log.md](figures/8-4/source_logs/source_log.md)
- Search log: [figures/8-4/search_iterations/search_iterations.md](figures/8-4/search_iterations/search_iterations.md)
- Discrepancy log: [figures/8-4/discrepancy_logs/discrepancy_log.md](figures/8-4/discrepancy_logs/discrepancy_log.md)
- Legacy metadata: [figures/8-4/metadata/metadata.json](figures/8-4/metadata/metadata.json)
- Metadata: [figures/8-4/figure.json](figures/8-4/figure.json)

### Figure 8-5 - Extreme poverty (number), 1820-2015

Status: `verified_reproduction`. Artifact kind: `reconstruction`.

- Original reference: [references/figures/figure_8_5.png](references/figures/figure_8_5.png)
- Book period reconstruction: [figures/8-5/plots/book_period/figure_8_5_book_period_reconstruction.png](figures/8-5/plots/book_period/figure_8_5_book_period_reconstruction.png)
- Extended reconstruction: [figures/8-5/plots/book_period/figure_8_5_book_period_reconstruction.png](figures/8-5/plots/book_period/figure_8_5_book_period_reconstruction.png)
- Book period comparison: [figures/8-5/plots/comparisons/figure_8_5_book_period_review.png](figures/8-5/plots/comparisons/figure_8_5_book_period_review.png)
- Extended comparison: [figures/8-5/plots/comparisons/figure_8_5_extended_review.png](figures/8-5/plots/comparisons/figure_8_5_extended_review.png)
- Caption: [figures/8-5/captions/caption.txt](figures/8-5/captions/caption.txt)
- Provenance: [figures/8-5/provenance/provenance.md](figures/8-5/provenance/provenance.md)
- Anomaly review: [figures/8-5/anomaly_reviews/anomaly_review.md](figures/8-5/anomaly_reviews/anomaly_review.md)
- Review checklist: [figures/8-5/review_checklist.md](figures/8-5/review_checklist.md)
- Source log: [figures/8-5/source_logs/source_log.md](figures/8-5/source_logs/source_log.md)
- Search log: [figures/8-5/search_iterations/search_iterations.md](figures/8-5/search_iterations/search_iterations.md)
- Discrepancy log: [figures/8-5/discrepancy_logs/discrepancy_log.md](figures/8-5/discrepancy_logs/discrepancy_log.md)
- Legacy metadata: [figures/8-5/metadata/metadata.json](figures/8-5/metadata/metadata.json)
- Metadata: [figures/8-5/figure.json](figures/8-5/figure.json)

### Figure 9-1 - International inequality, 1820-2013

Status: `manual_review_needed`. Artifact kind: `source_recovery`.

- Original reference: [references/figures/figure_9_1.png](references/figures/figure_9_1.png)
- Caption: [figures/9-1/captions/caption.txt](figures/9-1/captions/caption.txt)
- Provenance: [figures/9-1/provenance/provenance.md](figures/9-1/provenance/provenance.md)
- Anomaly review: [figures/9-1/anomaly_reviews/anomaly_review.md](figures/9-1/anomaly_reviews/anomaly_review.md)
- Review checklist: [figures/9-1/review_checklist.md](figures/9-1/review_checklist.md)
- Source log: [figures/9-1/source_logs/source_log.md](figures/9-1/source_logs/source_log.md)
- Search log: [figures/9-1/search_iterations/search_iterations.md](figures/9-1/search_iterations/search_iterations.md)
- Discrepancy log: [figures/9-1/discrepancy_logs/discrepancy_log.md](figures/9-1/discrepancy_logs/discrepancy_log.md)
- Legacy metadata: [figures/9-1/metadata/metadata.json](figures/9-1/metadata/metadata.json)
- Metadata: [figures/9-1/figure.json](figures/9-1/figure.json)

### Figure 9-2 - Global inequality, 1820-2011

Status: `manual_review_needed`. Artifact kind: `source_recovery`.

- Original reference: [references/figures/figure_9_2.png](references/figures/figure_9_2.png)
- Caption: [figures/9-2/captions/caption.txt](figures/9-2/captions/caption.txt)
- Provenance: [figures/9-2/provenance/provenance.md](figures/9-2/provenance/provenance.md)
- Anomaly review: [figures/9-2/anomaly_reviews/anomaly_review.md](figures/9-2/anomaly_reviews/anomaly_review.md)
- Review checklist: [figures/9-2/review_checklist.md](figures/9-2/review_checklist.md)
- Source log: [figures/9-2/source_logs/source_log.md](figures/9-2/source_logs/source_log.md)
- Search log: [figures/9-2/search_iterations/search_iterations.md](figures/9-2/search_iterations/search_iterations.md)
- Discrepancy log: [figures/9-2/discrepancy_logs/discrepancy_log.md](figures/9-2/discrepancy_logs/discrepancy_log.md)
- Legacy metadata: [figures/9-2/metadata/metadata.json](figures/9-2/metadata/metadata.json)
- Metadata: [figures/9-2/figure.json](figures/9-2/figure.json)

### Figure 9-3 - Inequality, UK and US, 1688-2013

Status: `manual_review_needed`. Artifact kind: `source_recovery`.

- Original reference: [references/figures/figure_9_3.png](references/figures/figure_9_3.png)
- Caption: [figures/9-3/captions/caption.txt](figures/9-3/captions/caption.txt)
- Provenance: [figures/9-3/provenance/provenance.md](figures/9-3/provenance/provenance.md)
- Anomaly review: [figures/9-3/anomaly_reviews/anomaly_review.md](figures/9-3/anomaly_reviews/anomaly_review.md)
- Review checklist: [figures/9-3/review_checklist.md](figures/9-3/review_checklist.md)
- Source log: [figures/9-3/source_logs/source_log.md](figures/9-3/source_logs/source_log.md)
- Search log: [figures/9-3/search_iterations/search_iterations.md](figures/9-3/search_iterations/search_iterations.md)
- Discrepancy log: [figures/9-3/discrepancy_logs/discrepancy_log.md](figures/9-3/discrepancy_logs/discrepancy_log.md)
- Legacy metadata: [figures/9-3/metadata/metadata.json](figures/9-3/metadata/metadata.json)
- Metadata: [figures/9-3/figure.json](figures/9-3/figure.json)

### Figure 9-4 - Social spending, OECD countries, 1880-2016

Status: `updated_equivalent`. Artifact kind: `reconstruction`.

- Original reference: [references/figures/figure_9_4.png](references/figures/figure_9_4.png)
- Book period reconstruction: [figures/9-4/plots/book_period/figure_9_4_book_period_reconstruction.png](figures/9-4/plots/book_period/figure_9_4_book_period_reconstruction.png)
- Extended reconstruction: [figures/9-4/plots/extended/figure_9_4_extended_reconstruction.png](figures/9-4/plots/extended/figure_9_4_extended_reconstruction.png)
- Book period comparison: [figures/9-4/plots/comparisons/figure_9_4_book_period_review.png](figures/9-4/plots/comparisons/figure_9_4_book_period_review.png)
- Extended comparison: [figures/9-4/plots/comparisons/figure_9_4_extended_review.png](figures/9-4/plots/comparisons/figure_9_4_extended_review.png)
- Caption: [figures/9-4/captions/caption.txt](figures/9-4/captions/caption.txt)
- Provenance: [figures/9-4/provenance/provenance.md](figures/9-4/provenance/provenance.md)
- Anomaly review: [figures/9-4/anomaly_reviews/anomaly_review.md](figures/9-4/anomaly_reviews/anomaly_review.md)
- Review checklist: [figures/9-4/review_checklist.md](figures/9-4/review_checklist.md)
- Source log: [figures/9-4/source_logs/source_log.md](figures/9-4/source_logs/source_log.md)
- Search log: [figures/9-4/search_iterations/search_iterations.md](figures/9-4/search_iterations/search_iterations.md)
- Discrepancy log: [figures/9-4/discrepancy_logs/discrepancy_log.md](figures/9-4/discrepancy_logs/discrepancy_log.md)
- Legacy metadata: [figures/9-4/metadata/metadata.json](figures/9-4/metadata/metadata.json)
- Metadata: [figures/9-4/figure.json](figures/9-4/figure.json)

### Figure 9-5 - Income gains, 1988-2008

Status: `partial_match`. Artifact kind: `reconstruction`.

- Original reference: [references/figures/figure_9_5.png](references/figures/figure_9_5.png)
- Book period reconstruction: [figures/9-5/plots/book_period/figure_9_5_book_period_reconstruction.png](figures/9-5/plots/book_period/figure_9_5_book_period_reconstruction.png)
- Extended reconstruction: [figures/9-5/plots/book_period/figure_9_5_book_period_reconstruction.png](figures/9-5/plots/book_period/figure_9_5_book_period_reconstruction.png)
- Book period comparison: [figures/9-5/plots/comparisons/figure_9_5_book_period_review.png](figures/9-5/plots/comparisons/figure_9_5_book_period_review.png)
- Extended comparison: [figures/9-5/plots/comparisons/figure_9_5_extended_review.png](figures/9-5/plots/comparisons/figure_9_5_extended_review.png)
- Caption: [figures/9-5/captions/caption.txt](figures/9-5/captions/caption.txt)
- Provenance: [figures/9-5/provenance/provenance.md](figures/9-5/provenance/provenance.md)
- Anomaly review: [figures/9-5/anomaly_reviews/anomaly_review.md](figures/9-5/anomaly_reviews/anomaly_review.md)
- Review checklist: [figures/9-5/review_checklist.md](figures/9-5/review_checklist.md)
- Source log: [figures/9-5/source_logs/source_log.md](figures/9-5/source_logs/source_log.md)
- Search log: [figures/9-5/search_iterations/search_iterations.md](figures/9-5/search_iterations/search_iterations.md)
- Discrepancy log: [figures/9-5/discrepancy_logs/discrepancy_log.md](figures/9-5/discrepancy_logs/discrepancy_log.md)
- Legacy metadata: [figures/9-5/metadata/metadata.json](figures/9-5/metadata/metadata.json)
- Metadata: [figures/9-5/figure.json](figures/9-5/figure.json)

### Figure 9-6 - Poverty, US, 1960-2016

Status: `verified_reproduction`. Artifact kind: `reconstruction`.

- Original reference: [references/figures/figure_9_6.png](references/figures/figure_9_6.png)
- Book period reconstruction: [figures/9-6/plots/book_period/figure_9_6_book_period_reconstruction.png](figures/9-6/plots/book_period/figure_9_6_book_period_reconstruction.png)
- Extended reconstruction: [figures/9-6/plots/extended/figure_9_6_extended_reconstruction.png](figures/9-6/plots/extended/figure_9_6_extended_reconstruction.png)
- Book period comparison: [figures/9-6/plots/comparisons/figure_9_6_book_period_review.png](figures/9-6/plots/comparisons/figure_9_6_book_period_review.png)
- Extended comparison: [figures/9-6/plots/comparisons/figure_9_6_extended_review.png](figures/9-6/plots/comparisons/figure_9_6_extended_review.png)
- Caption: [figures/9-6/captions/caption.txt](figures/9-6/captions/caption.txt)
- Provenance: [figures/9-6/provenance/provenance.md](figures/9-6/provenance/provenance.md)
- Anomaly review: [figures/9-6/anomaly_reviews/anomaly_review.md](figures/9-6/anomaly_reviews/anomaly_review.md)
- Review checklist: [figures/9-6/review_checklist.md](figures/9-6/review_checklist.md)
- Source log: [figures/9-6/source_logs/source_log.md](figures/9-6/source_logs/source_log.md)
- Search log: [figures/9-6/search_iterations/search_iterations.md](figures/9-6/search_iterations/search_iterations.md)
- Discrepancy log: [figures/9-6/discrepancy_logs/discrepancy_log.md](figures/9-6/discrepancy_logs/discrepancy_log.md)
- Legacy metadata: [figures/9-6/metadata/metadata.json](figures/9-6/metadata/metadata.json)
- Metadata: [figures/9-6/figure.json](figures/9-6/figure.json)

### Figure 10-1 - Population and population growth, 1750-2015 and projected to 2100

Status: `updated_equivalent`. Artifact kind: `reconstruction`.

- Original reference: [references/figures/figure_10_1.png](references/figures/figure_10_1.png)
- Book period reconstruction: [figures/10-1/plots/book_period/figure_10_1_book_period_reconstruction.png](figures/10-1/plots/book_period/figure_10_1_book_period_reconstruction.png)
- Extended reconstruction: [figures/10-1/plots/extended/figure_10_1_extended_reconstruction.png](figures/10-1/plots/extended/figure_10_1_extended_reconstruction.png)
- Book period comparison: [figures/10-1/plots/comparisons/figure_10_1_book_period_review.png](figures/10-1/plots/comparisons/figure_10_1_book_period_review.png)
- Extended comparison: [figures/10-1/plots/comparisons/figure_10_1_extended_review.png](figures/10-1/plots/comparisons/figure_10_1_extended_review.png)
- Caption: [figures/10-1/captions/caption.txt](figures/10-1/captions/caption.txt)
- Provenance: [figures/10-1/provenance/provenance.md](figures/10-1/provenance/provenance.md)
- Anomaly review: [figures/10-1/anomaly_reviews/anomaly_review.md](figures/10-1/anomaly_reviews/anomaly_review.md)
- Review checklist: [figures/10-1/review_checklist.md](figures/10-1/review_checklist.md)
- Source log: [figures/10-1/source_logs/source_log.md](figures/10-1/source_logs/source_log.md)
- Search log: [figures/10-1/search_iterations/search_iterations.md](figures/10-1/search_iterations/search_iterations.md)
- Discrepancy log: [figures/10-1/discrepancy_logs/discrepancy_log.md](figures/10-1/discrepancy_logs/discrepancy_log.md)
- Legacy metadata: [figures/10-1/metadata/metadata.json](figures/10-1/metadata/metadata.json)
- Metadata: [figures/10-1/figure.json](figures/10-1/figure.json)

### Figure 10-2 - Sustainability, 1955-2109

Status: `updated_equivalent`. Artifact kind: `reconstruction`.

- Original reference: [references/figures/figure_10_2.png](references/figures/figure_10_2.png)
- Book period reconstruction: [figures/10-2/plots/book_period/figure_10_2_book_period_reconstruction.png](figures/10-2/plots/book_period/figure_10_2_book_period_reconstruction.png)
- Extended reconstruction: [figures/10-2/plots/extended/figure_10_2_extended_reconstruction.png](figures/10-2/plots/extended/figure_10_2_extended_reconstruction.png)
- Book period comparison: [figures/10-2/plots/comparisons/figure_10_2_book_period_review.png](figures/10-2/plots/comparisons/figure_10_2_book_period_review.png)
- Extended comparison: [figures/10-2/plots/comparisons/figure_10_2_extended_review.png](figures/10-2/plots/comparisons/figure_10_2_extended_review.png)
- Caption: [figures/10-2/captions/caption.txt](figures/10-2/captions/caption.txt)
- Provenance: [figures/10-2/provenance/provenance.md](figures/10-2/provenance/provenance.md)
- Anomaly review: [figures/10-2/anomaly_reviews/anomaly_review.md](figures/10-2/anomaly_reviews/anomaly_review.md)
- Review checklist: [figures/10-2/review_checklist.md](figures/10-2/review_checklist.md)
- Source log: [figures/10-2/source_logs/source_log.md](figures/10-2/source_logs/source_log.md)
- Search log: [figures/10-2/search_iterations/search_iterations.md](figures/10-2/search_iterations/search_iterations.md)
- Discrepancy log: [figures/10-2/discrepancy_logs/discrepancy_log.md](figures/10-2/discrepancy_logs/discrepancy_log.md)
- Legacy metadata: [figures/10-2/metadata/metadata.json](figures/10-2/metadata/metadata.json)
- Metadata: [figures/10-2/figure.json](figures/10-2/figure.json)

### Figure 10-3 - Pollution, energy, and growth, US, 1970-2015

Status: `verified_reproduction`. Artifact kind: `reconstruction`.

- Original reference: [references/figures/figure_10_3.png](references/figures/figure_10_3.png)
- Book period reconstruction: [figures/10-3/plots/book_period/figure_10_3_book_period_reconstruction.png](figures/10-3/plots/book_period/figure_10_3_book_period_reconstruction.png)
- Extended reconstruction: [figures/10-3/plots/extended/figure_10_3_extended_reconstruction.png](figures/10-3/plots/extended/figure_10_3_extended_reconstruction.png)
- Book period comparison: [figures/10-3/plots/comparisons/figure_10_3_book_period_review.png](figures/10-3/plots/comparisons/figure_10_3_book_period_review.png)
- Extended comparison: [figures/10-3/plots/comparisons/figure_10_3_extended_review.png](figures/10-3/plots/comparisons/figure_10_3_extended_review.png)
- Caption: [figures/10-3/captions/caption.txt](figures/10-3/captions/caption.txt)
- Provenance: [figures/10-3/provenance/provenance.md](figures/10-3/provenance/provenance.md)
- Anomaly review: [figures/10-3/anomaly_reviews/anomaly_review.md](figures/10-3/anomaly_reviews/anomaly_review.md)
- Review checklist: [figures/10-3/review_checklist.md](figures/10-3/review_checklist.md)
- Source log: [figures/10-3/source_logs/source_log.md](figures/10-3/source_logs/source_log.md)
- Search log: [figures/10-3/search_iterations/search_iterations.md](figures/10-3/search_iterations/search_iterations.md)
- Discrepancy log: [figures/10-3/discrepancy_logs/discrepancy_log.md](figures/10-3/discrepancy_logs/discrepancy_log.md)
- Legacy metadata: [figures/10-3/metadata/metadata.json](figures/10-3/metadata/metadata.json)
- Metadata: [figures/10-3/figure.json](figures/10-3/figure.json)

### Figure 10-4 - Deforestation, 1700-2010

Status: `manual_review_needed`. Artifact kind: `source_recovery`.

- Original reference: [references/figures/figure_10_4.png](references/figures/figure_10_4.png)
- Caption: [figures/10-4/captions/caption.txt](figures/10-4/captions/caption.txt)
- Provenance: [figures/10-4/provenance/provenance.md](figures/10-4/provenance/provenance.md)
- Anomaly review: [figures/10-4/anomaly_reviews/anomaly_review.md](figures/10-4/anomaly_reviews/anomaly_review.md)
- Review checklist: [figures/10-4/review_checklist.md](figures/10-4/review_checklist.md)
- Source log: [figures/10-4/source_logs/source_log.md](figures/10-4/source_logs/source_log.md)
- Search log: [figures/10-4/search_iterations/search_iterations.md](figures/10-4/search_iterations/search_iterations.md)
- Discrepancy log: [figures/10-4/discrepancy_logs/discrepancy_log.md](figures/10-4/discrepancy_logs/discrepancy_log.md)
- Legacy metadata: [figures/10-4/metadata/metadata.json](figures/10-4/metadata/metadata.json)
- Metadata: [figures/10-4/figure.json](figures/10-4/figure.json)

### Figure 10-5 - Oil spills, 1970-2016

Status: `partial_match`. Artifact kind: `reconstruction`.

- Original reference: [references/figures/figure_10_5.png](references/figures/figure_10_5.png)
- Book period reconstruction: [figures/10-5/plots/book_period/figure_10_5_book_period_reconstruction.png](figures/10-5/plots/book_period/figure_10_5_book_period_reconstruction.png)
- Extended reconstruction: [figures/10-5/plots/extended/figure_10_5_extended_reconstruction.png](figures/10-5/plots/extended/figure_10_5_extended_reconstruction.png)
- Book period comparison: [figures/10-5/plots/comparisons/figure_10_5_book_period_review.png](figures/10-5/plots/comparisons/figure_10_5_book_period_review.png)
- Extended comparison: [figures/10-5/plots/comparisons/figure_10_5_extended_review.png](figures/10-5/plots/comparisons/figure_10_5_extended_review.png)
- Caption: [figures/10-5/captions/caption.txt](figures/10-5/captions/caption.txt)
- Provenance: [figures/10-5/provenance/provenance.md](figures/10-5/provenance/provenance.md)
- Anomaly review: [figures/10-5/anomaly_reviews/anomaly_review.md](figures/10-5/anomaly_reviews/anomaly_review.md)
- Source log: [figures/10-5/source_logs/source_log.md](figures/10-5/source_logs/source_log.md)
- Search log: [figures/10-5/search_iterations/search_iterations.md](figures/10-5/search_iterations/search_iterations.md)
- Discrepancy log: [figures/10-5/discrepancy_logs/discrepancy_log.md](figures/10-5/discrepancy_logs/discrepancy_log.md)
- Legacy metadata: [figures/10-5/metadata/metadata.json](figures/10-5/metadata/metadata.json)
- Metadata: [figures/10-5/figure.json](figures/10-5/figure.json)

### Figure 10-6 - Protected areas, 1990-2014

Status: `verified_reproduction`. Artifact kind: `reconstruction`.

- Original reference: [references/figures/figure_10_6.png](references/figures/figure_10_6.png)
- Book period reconstruction: [figures/10-6/plots/book_period/figure_10_6_book_period_reconstruction.png](figures/10-6/plots/book_period/figure_10_6_book_period_reconstruction.png)
- Extended reconstruction: [figures/10-6/plots/extended/figure_10_6_extended_reconstruction.png](figures/10-6/plots/extended/figure_10_6_extended_reconstruction.png)
- Book period comparison: [figures/10-6/plots/comparisons/figure_10_6_book_period_review.png](figures/10-6/plots/comparisons/figure_10_6_book_period_review.png)
- Extended comparison: [figures/10-6/plots/comparisons/figure_10_6_extended_review.png](figures/10-6/plots/comparisons/figure_10_6_extended_review.png)
- Caption: [figures/10-6/captions/caption.txt](figures/10-6/captions/caption.txt)
- Provenance: [figures/10-6/provenance/provenance.md](figures/10-6/provenance/provenance.md)
- Anomaly review: [figures/10-6/anomaly_reviews/anomaly_review.md](figures/10-6/anomaly_reviews/anomaly_review.md)
- Source log: [figures/10-6/source_logs/source_log.md](figures/10-6/source_logs/source_log.md)
- Search log: [figures/10-6/search_iterations/search_iterations.md](figures/10-6/search_iterations/search_iterations.md)
- Discrepancy log: [figures/10-6/discrepancy_logs/discrepancy_log.md](figures/10-6/discrepancy_logs/discrepancy_log.md)
- Legacy metadata: [figures/10-6/metadata/metadata.json](figures/10-6/metadata/metadata.json)
- Metadata: [figures/10-6/figure.json](figures/10-6/figure.json)

### Figure 10-7 - Carbon intensity (CO2 emissions per dollar of GDP), 1820-2014

Status: `verified_reproduction`. Artifact kind: `reconstruction`.

- Original reference: [references/figures/figure_10_7.png](references/figures/figure_10_7.png)
- Book period reconstruction: [figures/10-7/plots/book_period/figure_10_7_book_period_reconstruction.png](figures/10-7/plots/book_period/figure_10_7_book_period_reconstruction.png)
- Extended reconstruction: [figures/10-7/plots/extended/figure_10_7_extended_reconstruction.png](figures/10-7/plots/extended/figure_10_7_extended_reconstruction.png)
- Book period comparison: [figures/10-7/plots/comparisons/figure_10_7_book_period_review.png](figures/10-7/plots/comparisons/figure_10_7_book_period_review.png)
- Extended comparison: [figures/10-7/plots/comparisons/figure_10_7_extended_review.png](figures/10-7/plots/comparisons/figure_10_7_extended_review.png)
- Caption: [figures/10-7/captions/caption.txt](figures/10-7/captions/caption.txt)
- Provenance: [figures/10-7/provenance/provenance.md](figures/10-7/provenance/provenance.md)
- Anomaly review: [figures/10-7/anomaly_reviews/anomaly_review.md](figures/10-7/anomaly_reviews/anomaly_review.md)
- Review checklist: [figures/10-7/review_checklist.md](figures/10-7/review_checklist.md)
- Source log: [figures/10-7/source_logs/source_log.md](figures/10-7/source_logs/source_log.md)
- Search log: [figures/10-7/search_iterations/search_iterations.md](figures/10-7/search_iterations/search_iterations.md)
- Discrepancy log: [figures/10-7/discrepancy_logs/discrepancy_log.md](figures/10-7/discrepancy_logs/discrepancy_log.md)
- Legacy metadata: [figures/10-7/metadata/metadata.json](figures/10-7/metadata/metadata.json)
- Metadata: [figures/10-7/figure.json](figures/10-7/figure.json)

### Figure 10-8 - CO2 emissions, 1960-2015

Status: `verified_reproduction`. Artifact kind: `reconstruction`.

- Original reference: [references/figures/figure_10_8.png](references/figures/figure_10_8.png)
- Book period reconstruction: [figures/10-8/plots/book_period/figure_10_8_book_period_reconstruction.png](figures/10-8/plots/book_period/figure_10_8_book_period_reconstruction.png)
- Extended reconstruction: [figures/10-8/plots/extended/figure_10_8_extended_reconstruction.png](figures/10-8/plots/extended/figure_10_8_extended_reconstruction.png)
- Book period comparison: [figures/10-8/plots/comparisons/figure_10_8_book_period_review.png](figures/10-8/plots/comparisons/figure_10_8_book_period_review.png)
- Extended comparison: [figures/10-8/plots/comparisons/figure_10_8_extended_review.png](figures/10-8/plots/comparisons/figure_10_8_extended_review.png)
- Caption: [figures/10-8/captions/caption.txt](figures/10-8/captions/caption.txt)
- Provenance: [figures/10-8/provenance/provenance.md](figures/10-8/provenance/provenance.md)
- Anomaly review: [figures/10-8/anomaly_reviews/anomaly_review.md](figures/10-8/anomaly_reviews/anomaly_review.md)
- Review checklist: [figures/10-8/review_checklist.md](figures/10-8/review_checklist.md)
- Source log: [figures/10-8/source_logs/source_log.md](figures/10-8/source_logs/source_log.md)
- Search log: [figures/10-8/search_iterations/search_iterations.md](figures/10-8/search_iterations/search_iterations.md)
- Discrepancy log: [figures/10-8/discrepancy_logs/discrepancy_log.md](figures/10-8/discrepancy_logs/discrepancy_log.md)
- Legacy metadata: [figures/10-8/metadata/metadata.json](figures/10-8/metadata/metadata.json)
- Metadata: [figures/10-8/figure.json](figures/10-8/figure.json)

### Figure 11-1 - Great power war, 1500-2015

Status: `partial_match`. Artifact kind: `reconstruction`.

- Metadata: [figures/11-1/figure.json](figures/11-1/figure.json)
- Original reference: [references/figures/figure_11_1.png](references/figures/figure_11_1.png)
- Provenance: [figures/11-1/provenance/provenance.md](figures/11-1/provenance/provenance.md)
- Caption: [figures/11-1/captions/caption.txt](figures/11-1/captions/caption.txt)
- Source log: [figures/11-1/source_logs/source_log.md](figures/11-1/source_logs/source_log.md)
- Search log: [figures/11-1/search_iterations/search_iterations.md](figures/11-1/search_iterations/search_iterations.md)
- Anomaly review: [figures/11-1/anomaly_reviews/anomaly_review.md](figures/11-1/anomaly_reviews/anomaly_review.md)
- Discrepancy log: [figures/11-1/discrepancy_logs/discrepancy_log.md](figures/11-1/discrepancy_logs/discrepancy_log.md)
- Review checklist: [figures/11-1/review_checklist.md](figures/11-1/review_checklist.md)
- Book period reconstruction: [figures/11-1/plots/book_period/figure_11_1_book_period.png](figures/11-1/plots/book_period/figure_11_1_book_period.png)
- Extended reconstruction: [figures/11-1/plots/extended/figure_11_1_extended.png](figures/11-1/plots/extended/figure_11_1_extended.png)
- Book period clean: [figures/11-1/data/clean/figure_11_1_book_period.csv](figures/11-1/data/clean/figure_11_1_book_period.csv)
- Successor clean: [figures/11-1/data/clean/figure_11_1_successor.csv](figures/11-1/data/clean/figure_11_1_successor.csv)
- Lineage: [figures/11-1/lineage/lineage.json](figures/11-1/lineage/lineage.json)
- Lineage csv: [figures/11-1/lineage/lineage.csv](figures/11-1/lineage/lineage.csv)
- Reconstruction script: [scripts/reconstruct_11_1.py](scripts/reconstruct_11_1.py)
- Book period comparison: [figures/11-1/plots/comparisons/figure_11_1_book_period_review.png](figures/11-1/plots/comparisons/figure_11_1_book_period_review.png)
- Extended comparison: [figures/11-1/plots/comparisons/figure_11_1_extended_review.png](figures/11-1/plots/comparisons/figure_11_1_extended_review.png)

### Figure 11-2 - Battle deaths, 1946-2016

Status: `partial_match`. Artifact kind: `reconstruction`.

- Metadata: [figures/11-2/figure.json](figures/11-2/figure.json)
- Original reference: [references/figures/figure_11_2.png](references/figures/figure_11_2.png)
- Provenance: [figures/11-2/provenance/provenance.md](figures/11-2/provenance/provenance.md)
- Caption: [figures/11-2/captions/caption.txt](figures/11-2/captions/caption.txt)
- Source log: [figures/11-2/source_logs/source_log.md](figures/11-2/source_logs/source_log.md)
- Download log: [figures/11-2/source_logs/downloads.json](figures/11-2/source_logs/downloads.json)
- Search log: [figures/11-2/search_iterations/search_iterations.md](figures/11-2/search_iterations/search_iterations.md)
- Anomaly review: [figures/11-2/anomaly_reviews/anomaly_review.md](figures/11-2/anomaly_reviews/anomaly_review.md)
- Discrepancy log: [figures/11-2/discrepancy_logs/discrepancy_log.md](figures/11-2/discrepancy_logs/discrepancy_log.md)
- Review checklist: [figures/11-2/review_checklist.md](figures/11-2/review_checklist.md)
- Book period reconstruction: [figures/11-2/plots/book_period/figure_11_2_book_period.png](figures/11-2/plots/book_period/figure_11_2_book_period.png)
- Extended reconstruction: [figures/11-2/plots/extended/figure_11_2_extended.png](figures/11-2/plots/extended/figure_11_2_extended.png)
- Book period clean: [figures/11-2/data/clean/figure_11_2_book_period.csv](figures/11-2/data/clean/figure_11_2_book_period.csv)
- Successor clean: [figures/11-2/data/clean/figure_11_2_successor.csv](figures/11-2/data/clean/figure_11_2_successor.csv)
- Lineage: [figures/11-2/lineage/lineage.json](figures/11-2/lineage/lineage.json)
- Lineage csv: [figures/11-2/lineage/lineage.csv](figures/11-2/lineage/lineage.csv)
- Reconstruction script: [scripts/reconstruct_11_2.py](scripts/reconstruct_11_2.py)
- Book period comparison: [figures/11-2/plots/comparisons/figure_11_2_book_period_review.png](figures/11-2/plots/comparisons/figure_11_2_book_period_review.png)
- Extended comparison: [figures/11-2/plots/comparisons/figure_11_2_extended_review.png](figures/11-2/plots/comparisons/figure_11_2_extended_review.png)

### Figure 11-3 - Genocide deaths, 1956-2016

Status: `partial_match`. Artifact kind: `reconstruction`.

- Metadata: [figures/11-3/figure.json](figures/11-3/figure.json)
- Original reference: [references/figures/figure_11_3.png](references/figures/figure_11_3.png)
- Book period reconstruction: [figures/11-3/plots/figure_11_3_book_period.png](figures/11-3/plots/figure_11_3_book_period.png)
- Extended reconstruction: [figures/11-3/plots/figure_11_3_extended.png](figures/11-3/plots/figure_11_3_extended.png)
- Book period clean: [figures/11-3/data/clean/figure_11_3_book_period.csv](figures/11-3/data/clean/figure_11_3_book_period.csv)
- Successor clean: [figures/11-3/data/clean/figure_11_3_successor.csv](figures/11-3/data/clean/figure_11_3_successor.csv)
- Caption: [figures/11-3/captions/caption.txt](figures/11-3/captions/caption.txt)
- Provenance: [figures/11-3/provenance/provenance.md](figures/11-3/provenance/provenance.md)
- Source log: [figures/11-3/source_logs/source_log.md](figures/11-3/source_logs/source_log.md)
- Anomaly review: [figures/11-3/anomaly_reviews/anomaly_review.md](figures/11-3/anomaly_reviews/anomaly_review.md)
- Discrepancy log: [figures/11-3/discrepancy_logs/discrepancy_log.md](figures/11-3/discrepancy_logs/discrepancy_log.md)
- Review checklist: [figures/11-3/review_checklist.md](figures/11-3/review_checklist.md)
- Lineage: [figures/11-3/lineage/lineage.json](figures/11-3/lineage/lineage.json)
- Lineage csv: [figures/11-3/lineage/lineage.csv](figures/11-3/lineage/lineage.csv)
- Reconstruction script: [scripts/reconstruct_11_3.py](scripts/reconstruct_11_3.py)
- Book period comparison: [figures/11-3/plots/comparisons/figure_11_3_book_period_review.png](figures/11-3/plots/comparisons/figure_11_3_book_period_review.png)
- Extended comparison: [figures/11-3/plots/comparisons/figure_11_3_extended_review.png](figures/11-3/plots/comparisons/figure_11_3_extended_review.png)

### Figure 12-1 - Homicide deaths, Western Europe, US, and Mexico, 1300-2015

Status: `partial_match`. Artifact kind: `reconstruction`.

- Metadata: [figures/12-1/figure.json](figures/12-1/figure.json)
- Original reference: [references/figures/figure_12_1.png](references/figures/figure_12_1.png)
- Book period reconstruction: [figures/12-1/plots/figure_12_1_book_period.png](figures/12-1/plots/figure_12_1_book_period.png)
- Extended reconstruction: [figures/12-1/plots/figure_12_1_extended.png](figures/12-1/plots/figure_12_1_extended.png)
- Book period clean: [figures/12-1/data/clean/figure_12_1_book_period.csv](figures/12-1/data/clean/figure_12_1_book_period.csv)
- Successor clean: [figures/12-1/data/clean/figure_12_1_successor.csv](figures/12-1/data/clean/figure_12_1_successor.csv)
- Caption: [figures/12-1/captions/caption.txt](figures/12-1/captions/caption.txt)
- Provenance: [figures/12-1/provenance/provenance.md](figures/12-1/provenance/provenance.md)
- Source log: [figures/12-1/source_logs/source_log.md](figures/12-1/source_logs/source_log.md)
- Anomaly review: [figures/12-1/anomaly_reviews/anomaly_review.md](figures/12-1/anomaly_reviews/anomaly_review.md)
- Discrepancy log: [figures/12-1/discrepancy_logs/discrepancy_log.md](figures/12-1/discrepancy_logs/discrepancy_log.md)
- Review checklist: [figures/12-1/review_checklist.md](figures/12-1/review_checklist.md)
- Lineage: [figures/12-1/lineage/lineage.json](figures/12-1/lineage/lineage.json)
- Reconstruction script: [scripts/reconstruct_12_1.py](scripts/reconstruct_12_1.py)
- Book period comparison: [figures/12-1/plots/comparisons/figure_12_1_book_period_review.png](figures/12-1/plots/comparisons/figure_12_1_book_period_review.png)
- Extended comparison: [figures/12-1/plots/comparisons/figure_12_1_extended_review.png](figures/12-1/plots/comparisons/figure_12_1_extended_review.png)

### Figure 12-2 - Homicide deaths, 1967-2015

Status: `partial_match`. Artifact kind: `reconstruction`.

- Metadata: [figures/12-2/figure.json](figures/12-2/figure.json)
- Original reference: [references/figures/figure_12_2.png](references/figures/figure_12_2.png)
- Book period reconstruction: [figures/12-2/plots/figure_12_2_book_period.png](figures/12-2/plots/figure_12_2_book_period.png)
- Extended reconstruction: [figures/12-2/plots/figure_12_2_extended.png](figures/12-2/plots/figure_12_2_extended.png)
- Book period clean: [figures/12-2/data/clean/figure_12_2_book_period.csv](figures/12-2/data/clean/figure_12_2_book_period.csv)
- Successor clean: [figures/12-2/data/clean/figure_12_2_successor.csv](figures/12-2/data/clean/figure_12_2_successor.csv)
- Caption: [figures/12-2/captions/caption.txt](figures/12-2/captions/caption.txt)
- Provenance: [figures/12-2/provenance/provenance.md](figures/12-2/provenance/provenance.md)
- Source log: [figures/12-2/source_logs/source_log.md](figures/12-2/source_logs/source_log.md)
- Anomaly review: [figures/12-2/anomaly_reviews/anomaly_review.md](figures/12-2/anomaly_reviews/anomaly_review.md)
- Discrepancy log: [figures/12-2/discrepancy_logs/discrepancy_log.md](figures/12-2/discrepancy_logs/discrepancy_log.md)
- Review checklist: [figures/12-2/review_checklist.md](figures/12-2/review_checklist.md)
- Lineage: [figures/12-2/lineage/lineage.json](figures/12-2/lineage/lineage.json)
- Reconstruction script: [scripts/reconstruct_12_2.py](scripts/reconstruct_12_2.py)
- Book period comparison: [figures/12-2/plots/comparisons/figure_12_2_book_period_review.png](figures/12-2/plots/comparisons/figure_12_2_book_period_review.png)
- Extended comparison: [figures/12-2/plots/comparisons/figure_12_2_extended_review.png](figures/12-2/plots/comparisons/figure_12_2_extended_review.png)

### Figure 12-3 - Motor vehicle accident deaths, US, 1921-2015

Status: `source_chain_recovered`. Artifact kind: `source_recovery`.

- Original reference: [references/figures/figure_12_3.png](references/figures/figure_12_3.png)
- Caption: [figures/12-3/captions/caption.txt](figures/12-3/captions/caption.txt)
- Provenance: [figures/12-3/provenance/provenance.md](figures/12-3/provenance/provenance.md)
- Anomaly review: [figures/12-3/anomaly_reviews/anomaly_review.md](figures/12-3/anomaly_reviews/anomaly_review.md)
- Review checklist: [figures/12-3/review_checklist.md](figures/12-3/review_checklist.md)
- Source log: [figures/12-3/source_logs/source_log.md](figures/12-3/source_logs/source_log.md)
- Search log: [figures/12-3/search_iterations/search_iterations.md](figures/12-3/search_iterations/search_iterations.md)
- Discrepancy log: [figures/12-3/discrepancy_logs/discrepancy_log.md](figures/12-3/discrepancy_logs/discrepancy_log.md)
- Legacy metadata: [figures/12-3/metadata/metadata.json](figures/12-3/metadata/metadata.json)
- Metadata: [figures/12-3/figure.json](figures/12-3/figure.json)

### Figure 12-4 - Pedestrian deaths, US, 1927-2015

Status: `source_chain_recovered`. Artifact kind: `source_recovery`.

- Original reference: [references/figures/figure_12_4.png](references/figures/figure_12_4.png)
- Caption: [figures/12-4/captions/caption.txt](figures/12-4/captions/caption.txt)
- Provenance: [figures/12-4/provenance/provenance.md](figures/12-4/provenance/provenance.md)
- Anomaly review: [figures/12-4/anomaly_reviews/anomaly_review.md](figures/12-4/anomaly_reviews/anomaly_review.md)
- Review checklist: [figures/12-4/review_checklist.md](figures/12-4/review_checklist.md)
- Source log: [figures/12-4/source_logs/source_log.md](figures/12-4/source_logs/source_log.md)
- Search log: [figures/12-4/search_iterations/search_iterations.md](figures/12-4/search_iterations/search_iterations.md)
- Discrepancy log: [figures/12-4/discrepancy_logs/discrepancy_log.md](figures/12-4/discrepancy_logs/discrepancy_log.md)
- Legacy metadata: [figures/12-4/metadata/metadata.json](figures/12-4/metadata/metadata.json)
- Metadata: [figures/12-4/figure.json](figures/12-4/figure.json)

### Figure 12-5 - Plane crash deaths, 1970-2015

Status: `partial_match`. Artifact kind: `reconstruction`.

- Original reference: [references/figures/figure_12_5.png](references/figures/figure_12_5.png)
- Book period reconstruction: [figures/12-5/plots/book_period/figure_12_5_book_period_reconstruction.png](figures/12-5/plots/book_period/figure_12_5_book_period_reconstruction.png)
- Extended reconstruction: [figures/12-5/plots/extended/figure_12_5_extended_reconstruction.png](figures/12-5/plots/extended/figure_12_5_extended_reconstruction.png)
- Book period comparison: [figures/12-5/plots/comparisons/figure_12_5_book_period_review.png](figures/12-5/plots/comparisons/figure_12_5_book_period_review.png)
- Extended comparison: [figures/12-5/plots/comparisons/figure_12_5_extended_review.png](figures/12-5/plots/comparisons/figure_12_5_extended_review.png)
- Caption: [figures/12-5/captions/caption.txt](figures/12-5/captions/caption.txt)
- Provenance: [figures/12-5/provenance/provenance.md](figures/12-5/provenance/provenance.md)
- Anomaly review: [figures/12-5/anomaly_reviews/anomaly_review.md](figures/12-5/anomaly_reviews/anomaly_review.md)
- Review checklist: [figures/12-5/review_checklist.md](figures/12-5/review_checklist.md)
- Source log: [figures/12-5/source_logs/source_log.md](figures/12-5/source_logs/source_log.md)
- Search log: [figures/12-5/search_iterations/search_iterations.md](figures/12-5/search_iterations/search_iterations.md)
- Discrepancy log: [figures/12-5/discrepancy_logs/discrepancy_log.md](figures/12-5/discrepancy_logs/discrepancy_log.md)
- Legacy metadata: [figures/12-5/metadata/metadata.json](figures/12-5/metadata/metadata.json)
- Metadata: [figures/12-5/figure.json](figures/12-5/figure.json)

### Figure 12-6 - Deaths from falls, fire, drowning, and poison, US, 1903-2014

Status: `updated_equivalent`. Artifact kind: `reconstruction`.

- Metadata: [figures/12-6/figure.json](figures/12-6/figure.json)
- Original reference: [references/figures/figure_12_6.png](references/figures/figure_12_6.png)
- Book period reconstruction: [figures/12-6/plots/figure_12_6_book_period.png](figures/12-6/plots/figure_12_6_book_period.png)
- Extended reconstruction: [figures/12-6/plots/figure_12_6_extended.png](figures/12-6/plots/figure_12_6_extended.png)
- Book period clean: [figures/12-6/data/clean/figure_12_6_book_period.csv](figures/12-6/data/clean/figure_12_6_book_period.csv)
- Successor clean: [figures/12-6/data/clean/figure_12_6_successor.csv](figures/12-6/data/clean/figure_12_6_successor.csv)
- Book period comparison: [figures/12-6/plots/comparisons/figure_12_6_book_period_review.png](figures/12-6/plots/comparisons/figure_12_6_book_period_review.png)
- Extended comparison: [figures/12-6/plots/comparisons/figure_12_6_extended_review.png](figures/12-6/plots/comparisons/figure_12_6_extended_review.png)
- Caption: [figures/12-6/captions/caption.txt](figures/12-6/captions/caption.txt)
- Provenance: [figures/12-6/provenance/provenance.md](figures/12-6/provenance/provenance.md)
- Source log: [figures/12-6/source_logs/source_log.md](figures/12-6/source_logs/source_log.md)
- Anomaly review: [figures/12-6/anomaly_reviews/anomaly_review.md](figures/12-6/anomaly_reviews/anomaly_review.md)
- Discrepancy log: [figures/12-6/discrepancy_logs/discrepancy_log.md](figures/12-6/discrepancy_logs/discrepancy_log.md)
- Review checklist: [figures/12-6/review_checklist.md](figures/12-6/review_checklist.md)
- Lineage: [figures/12-6/lineage/lineage.json](figures/12-6/lineage/lineage.json)
- Reconstruction script: [scripts/reconstruct_12_6.py](scripts/reconstruct_12_6.py)

### Figure 12-7 - Occupational accident deaths, US, 1913-2015

Status: `partial_match`. Artifact kind: `reconstruction`.

- Metadata: [figures/12-7/figure.json](figures/12-7/figure.json)
- Original reference: [references/figures/figure_12_7.png](references/figures/figure_12_7.png)
- Book period reconstruction: [figures/12-7/plots/figure_12_7_book_period.png](figures/12-7/plots/figure_12_7_book_period.png)
- Extended reconstruction: [figures/12-7/plots/figure_12_7_extended.png](figures/12-7/plots/figure_12_7_extended.png)
- Book period clean: [figures/12-7/data/clean/figure_12_7_book_period.csv](figures/12-7/data/clean/figure_12_7_book_period.csv)
- Successor clean: [figures/12-7/data/clean/figure_12_7_successor.csv](figures/12-7/data/clean/figure_12_7_successor.csv)
- Book period comparison: [figures/12-7/plots/comparisons/figure_12_7_book_period_review.png](figures/12-7/plots/comparisons/figure_12_7_book_period_review.png)
- Extended comparison: [figures/12-7/plots/comparisons/figure_12_7_extended_review.png](figures/12-7/plots/comparisons/figure_12_7_extended_review.png)
- Caption: [figures/12-7/captions/caption.txt](figures/12-7/captions/caption.txt)
- Provenance: [figures/12-7/provenance/provenance.md](figures/12-7/provenance/provenance.md)
- Source log: [figures/12-7/source_logs/source_log.md](figures/12-7/source_logs/source_log.md)
- Anomaly review: [figures/12-7/anomaly_reviews/anomaly_review.md](figures/12-7/anomaly_reviews/anomaly_review.md)
- Discrepancy log: [figures/12-7/discrepancy_logs/discrepancy_log.md](figures/12-7/discrepancy_logs/discrepancy_log.md)
- Review checklist: [figures/12-7/review_checklist.md](figures/12-7/review_checklist.md)
- Lineage: [figures/12-7/lineage/lineage.json](figures/12-7/lineage/lineage.json)
- Reconstruction script: [scripts/reconstruct_12_7.py](scripts/reconstruct_12_7.py)

### Figure 12-8 - Natural disaster deaths, 1900-2015

Status: `updated_equivalent`. Artifact kind: `reconstruction`.

- Original reference: [references/figures/figure_12_8.png](references/figures/figure_12_8.png)
- Book period reconstruction: [figures/12-8/plots/book_period/figure_12_8_book_period_reconstruction.png](figures/12-8/plots/book_period/figure_12_8_book_period_reconstruction.png)
- Extended reconstruction: [figures/12-8/plots/extended/figure_12_8_extended_reconstruction.png](figures/12-8/plots/extended/figure_12_8_extended_reconstruction.png)
- Book period comparison: [figures/12-8/plots/comparisons/figure_12_8_book_period_review.png](figures/12-8/plots/comparisons/figure_12_8_book_period_review.png)
- Extended comparison: [figures/12-8/plots/comparisons/figure_12_8_extended_review.png](figures/12-8/plots/comparisons/figure_12_8_extended_review.png)
- Caption: [figures/12-8/captions/caption.txt](figures/12-8/captions/caption.txt)
- Provenance: [figures/12-8/provenance/provenance.md](figures/12-8/provenance/provenance.md)
- Anomaly review: [figures/12-8/anomaly_reviews/anomaly_review.md](figures/12-8/anomaly_reviews/anomaly_review.md)
- Review checklist: [figures/12-8/review_checklist.md](figures/12-8/review_checklist.md)
- Source log: [figures/12-8/source_logs/source_log.md](figures/12-8/source_logs/source_log.md)
- Search log: [figures/12-8/search_iterations/search_iterations.md](figures/12-8/search_iterations/search_iterations.md)
- Discrepancy log: [figures/12-8/discrepancy_logs/discrepancy_log.md](figures/12-8/discrepancy_logs/discrepancy_log.md)
- Legacy metadata: [figures/12-8/metadata/metadata.json](figures/12-8/metadata/metadata.json)
- Metadata: [figures/12-8/figure.json](figures/12-8/figure.json)

### Figure 12-9 - Lightning strike deaths, US, 1900-2015

Status: `verified_reproduction`. Artifact kind: `reconstruction`.

- Original reference: [references/figures/figure_12_9.png](references/figures/figure_12_9.png)
- Book period reconstruction: [figures/12-9/plots/book_period/figure_12_9_book_period_reconstruction.png](figures/12-9/plots/book_period/figure_12_9_book_period_reconstruction.png)
- Extended reconstruction: [figures/12-9/plots/book_period/figure_12_9_book_period_reconstruction.png](figures/12-9/plots/book_period/figure_12_9_book_period_reconstruction.png)
- Book period comparison: [figures/12-9/plots/comparisons/figure_12_9_book_period_review.png](figures/12-9/plots/comparisons/figure_12_9_book_period_review.png)
- Extended comparison: [figures/12-9/plots/comparisons/figure_12_9_extended_review.png](figures/12-9/plots/comparisons/figure_12_9_extended_review.png)
- Caption: [figures/12-9/captions/caption.txt](figures/12-9/captions/caption.txt)
- Provenance: [figures/12-9/provenance/provenance.md](figures/12-9/provenance/provenance.md)
- Anomaly review: [figures/12-9/anomaly_reviews/anomaly_review.md](figures/12-9/anomaly_reviews/anomaly_review.md)
- Review checklist: [figures/12-9/review_checklist.md](figures/12-9/review_checklist.md)
- Source log: [figures/12-9/source_logs/source_log.md](figures/12-9/source_logs/source_log.md)
- Search log: [figures/12-9/search_iterations/search_iterations.md](figures/12-9/search_iterations/search_iterations.md)
- Discrepancy log: [figures/12-9/discrepancy_logs/discrepancy_log.md](figures/12-9/discrepancy_logs/discrepancy_log.md)
- Legacy metadata: [figures/12-9/metadata/metadata.json](figures/12-9/metadata/metadata.json)
- Metadata: [figures/12-9/figure.json](figures/12-9/figure.json)

### Figure 13-1 - Terrorism deaths, 1970-2015

Status: `updated_equivalent`. Artifact kind: `reconstruction`.

- Metadata: [figures/13-1/figure.json](figures/13-1/figure.json)
- Original reference: [references/figures/figure_13_1.png](references/figures/figure_13_1.png)
- Book period reconstruction: [figures/13-1/plots/figure_13_1_book_period.png](figures/13-1/plots/figure_13_1_book_period.png)
- Extended reconstruction: [figures/13-1/plots/figure_13_1_extended.png](figures/13-1/plots/figure_13_1_extended.png)
- Book period clean: [figures/13-1/data/clean/figure_13_1_book_period.csv](figures/13-1/data/clean/figure_13_1_book_period.csv)
- Successor clean: [figures/13-1/data/clean/figure_13_1_successor.csv](figures/13-1/data/clean/figure_13_1_successor.csv)
- Book period comparison: [figures/13-1/plots/comparisons/figure_13_1_book_period_review.png](figures/13-1/plots/comparisons/figure_13_1_book_period_review.png)
- Extended comparison: [figures/13-1/plots/comparisons/figure_13_1_extended_review.png](figures/13-1/plots/comparisons/figure_13_1_extended_review.png)
- Caption: [figures/13-1/captions/caption.txt](figures/13-1/captions/caption.txt)
- Provenance: [figures/13-1/provenance/provenance.md](figures/13-1/provenance/provenance.md)
- Source log: [figures/13-1/source_logs/source_log.md](figures/13-1/source_logs/source_log.md)
- Anomaly review: [figures/13-1/anomaly_reviews/anomaly_review.md](figures/13-1/anomaly_reviews/anomaly_review.md)
- Discrepancy log: [figures/13-1/discrepancy_logs/discrepancy_log.md](figures/13-1/discrepancy_logs/discrepancy_log.md)
- Review checklist: [figures/13-1/review_checklist.md](figures/13-1/review_checklist.md)
- Lineage: [figures/13-1/lineage/lineage.json](figures/13-1/lineage/lineage.json)
- Reconstruction script: [scripts/reconstruct_13_1.py](scripts/reconstruct_13_1.py)

### Figure 14-1 - Democracy versus autocracy, 1800-2015

Status: `partial_match`. Artifact kind: `reconstruction`.

- Metadata: [figures/14-1/figure.json](figures/14-1/figure.json)
- Original reference: [references/figures/figure_14_1.png](references/figures/figure_14_1.png)
- Provenance: [figures/14-1/provenance/provenance.md](figures/14-1/provenance/provenance.md)
- Caption: [figures/14-1/captions/caption.txt](figures/14-1/captions/caption.txt)
- Source log: [figures/14-1/source_logs/source_log.md](figures/14-1/source_logs/source_log.md)
- Search log: [figures/14-1/search_iterations/search_iterations.md](figures/14-1/search_iterations/search_iterations.md)
- Download log: [figures/14-1/source_logs/downloads.json](figures/14-1/source_logs/downloads.json)
- Anomaly review: [figures/14-1/anomaly_reviews/anomaly_review.md](figures/14-1/anomaly_reviews/anomaly_review.md)
- Discrepancy log: [figures/14-1/discrepancy_logs/discrepancy_log.md](figures/14-1/discrepancy_logs/discrepancy_log.md)
- Review checklist: [figures/14-1/review_checklist.md](figures/14-1/review_checklist.md)
- Book period reconstruction: [figures/14-1/plots/book_period/figure_14_1_book_period.png](figures/14-1/plots/book_period/figure_14_1_book_period.png)
- Extended reconstruction: [figures/14-1/plots/extended/figure_14_1_extended.png](figures/14-1/plots/extended/figure_14_1_extended.png)
- Diagnostic: [figures/14-1/plots/diagnostics/aggregation_and_coverage.png](figures/14-1/plots/diagnostics/aggregation_and_coverage.png)
- Book period clean: [figures/14-1/data/clean/figure_14_1_book_period.csv](figures/14-1/data/clean/figure_14_1_book_period.csv)
- Extended clean: [figures/14-1/data/clean/figure_14_1_successor.csv](figures/14-1/data/clean/figure_14_1_successor.csv)
- Diagnostic clean: [figures/14-1/data/clean/figure_14_1_diagnostic.csv](figures/14-1/data/clean/figure_14_1_diagnostic.csv)
- Lineage: [figures/14-1/lineage/lineage.json](figures/14-1/lineage/lineage.json)
- Lineage csv: [figures/14-1/lineage/lineage.csv](figures/14-1/lineage/lineage.csv)
- Source manifest: [figures/14-1/data/raw/source_manifest.json](figures/14-1/data/raw/source_manifest.json)
- Reconstruction script: [scripts/reconstruct_14_1.py](scripts/reconstruct_14_1.py)
- Recovery script: [scripts/recover_14_1.py](scripts/recover_14_1.py)
- Book period comparison: [figures/14-1/plots/comparisons/figure_14_1_book_period_review.png](figures/14-1/plots/comparisons/figure_14_1_book_period_review.png)
- Extended comparison: [figures/14-1/plots/comparisons/figure_14_1_extended_review.png](figures/14-1/plots/comparisons/figure_14_1_extended_review.png)

### Figure 14-2 - Human rights, 1949-2014

Status: `partial_match`. Artifact kind: `reconstruction`.

- Metadata: [figures/14-2/figure.json](figures/14-2/figure.json)
- Provenance: [figures/14-2/provenance/provenance.md](figures/14-2/provenance/provenance.md)
- Caption: [figures/14-2/captions/caption.txt](figures/14-2/captions/caption.txt)
- Source log: [figures/14-2/source_logs/source_log.md](figures/14-2/source_logs/source_log.md)
- Search log: [figures/14-2/search_iterations/search_iterations.md](figures/14-2/search_iterations/search_iterations.md)
- Download log: [figures/14-2/source_logs/downloads.json](figures/14-2/source_logs/downloads.json)
- Anomaly review: [figures/14-2/anomaly_reviews/anomaly_review.md](figures/14-2/anomaly_reviews/anomaly_review.md)
- Discrepancy log: [figures/14-2/discrepancy_logs/discrepancy_log.md](figures/14-2/discrepancy_logs/discrepancy_log.md)
- Review checklist: [figures/14-2/review_checklist.md](figures/14-2/review_checklist.md)
- Book period reconstruction: [figures/14-2/plots/book_period/figure_14_2_book_period.png](figures/14-2/plots/book_period/figure_14_2_book_period.png)
- Extended reconstruction: [figures/14-2/plots/extended/figure_14_2_extended.png](figures/14-2/plots/extended/figure_14_2_extended.png)
- Diagnostic: [figures/14-2/plots/diagnostics/world_aggregation.png](figures/14-2/plots/diagnostics/world_aggregation.png)
- Book period clean: [figures/14-2/data/clean/figure_14_2_book_period.csv](figures/14-2/data/clean/figure_14_2_book_period.csv)
- Successor clean: [figures/14-2/data/clean/figure_14_2_successor.csv](figures/14-2/data/clean/figure_14_2_successor.csv)
- Diagnostic clean: [figures/14-2/data/clean/figure_14_2_diagnostic.csv](figures/14-2/data/clean/figure_14_2_diagnostic.csv)
- Lineage: [figures/14-2/lineage/lineage.json](figures/14-2/lineage/lineage.json)
- Lineage csv: [figures/14-2/lineage/lineage.csv](figures/14-2/lineage/lineage.csv)
- Reconstruction script: [scripts/reconstruct_14_2.py](scripts/reconstruct_14_2.py)
- Original reference: [references/figures/figure_14_2.png](references/figures/figure_14_2.png)
- Book period comparison: [figures/14-2/plots/comparisons/figure_14_2_book_period_review.png](figures/14-2/plots/comparisons/figure_14_2_book_period_review.png)
- Extended comparison: [figures/14-2/plots/comparisons/figure_14_2_extended_review.png](figures/14-2/plots/comparisons/figure_14_2_extended_review.png)

### Figure 14-3 - Death penalty abolitions, 1863-2016

Status: `partial_match`. Artifact kind: `reconstruction`.

- Metadata: [figures/14-3/figure.json](figures/14-3/figure.json)
- Original reference: [references/figures/figure_14_3.png](references/figures/figure_14_3.png)
- Provenance: [figures/14-3/provenance/provenance.md](figures/14-3/provenance/provenance.md)
- Caption: [figures/14-3/captions/caption.txt](figures/14-3/captions/caption.txt)
- Source log: [figures/14-3/source_logs/source_log.md](figures/14-3/source_logs/source_log.md)
- Search log: [figures/14-3/search_iterations/search_iterations.md](figures/14-3/search_iterations/search_iterations.md)
- Download log: [figures/14-3/source_logs/downloads.json](figures/14-3/source_logs/downloads.json)
- Anomaly review: [figures/14-3/anomaly_reviews/anomaly_review.md](figures/14-3/anomaly_reviews/anomaly_review.md)
- Discrepancy log: [figures/14-3/discrepancy_logs/discrepancy_log.md](figures/14-3/discrepancy_logs/discrepancy_log.md)
- Review checklist: [figures/14-3/review_checklist.md](figures/14-3/review_checklist.md)
- Book period reconstruction: [figures/14-3/plots/book_period/figure_14_3_book_period.png](figures/14-3/plots/book_period/figure_14_3_book_period.png)
- Extended reconstruction: [figures/14-3/plots/extended/figure_14_3_extended.png](figures/14-3/plots/extended/figure_14_3_extended.png)
- Diagnostic: [figures/14-3/plots/diagnostics/source_counts.png](figures/14-3/plots/diagnostics/source_counts.png)
- Book period clean: [figures/14-3/data/clean/figure_14_3_book_period.csv](figures/14-3/data/clean/figure_14_3_book_period.csv)
- Successor clean: [figures/14-3/data/clean/figure_14_3_successor.csv](figures/14-3/data/clean/figure_14_3_successor.csv)
- Diagnostic clean: [figures/14-3/data/clean/figure_14_3_source_anomalies.csv](figures/14-3/data/clean/figure_14_3_source_anomalies.csv)
- Lineage: [figures/14-3/lineage/lineage.json](figures/14-3/lineage/lineage.json)
- Lineage csv: [figures/14-3/lineage/lineage.csv](figures/14-3/lineage/lineage.csv)
- Reconstruction script: [scripts/reconstruct_14_3.py](scripts/reconstruct_14_3.py)
- Book period comparison: [figures/14-3/plots/comparisons/figure_14_3_book_period_review.png](figures/14-3/plots/comparisons/figure_14_3_book_period_review.png)
- Extended comparison: [figures/14-3/plots/comparisons/figure_14_3_extended_review.png](figures/14-3/plots/comparisons/figure_14_3_extended_review.png)

### Figure 14-4 - Executions, US, 1780-2016

Status: `partial_match`. Artifact kind: `reconstruction`.

- Metadata: [figures/14-4/figure.json](figures/14-4/figure.json)
- Original reference: [references/figures/figure_14_4.png](references/figures/figure_14_4.png)
- Provenance: [figures/14-4/provenance/provenance.md](figures/14-4/provenance/provenance.md)
- Caption: [figures/14-4/captions/caption.txt](figures/14-4/captions/caption.txt)
- Source log: [figures/14-4/source_logs/source_log.md](figures/14-4/source_logs/source_log.md)
- Search log: [figures/14-4/search_iterations/search_iterations.md](figures/14-4/search_iterations/search_iterations.md)
- Download log: [figures/14-4/source_logs/downloads.json](figures/14-4/source_logs/downloads.json)
- Anomaly review: [figures/14-4/anomaly_reviews/anomaly_review.md](figures/14-4/anomaly_reviews/anomaly_review.md)
- Discrepancy log: [figures/14-4/discrepancy_logs/discrepancy_log.md](figures/14-4/discrepancy_logs/discrepancy_log.md)
- Review checklist: [figures/14-4/review_checklist.md](figures/14-4/review_checklist.md)
- Book period reconstruction: [figures/14-4/plots/book_period/figure_14_4_book_period.png](figures/14-4/plots/book_period/figure_14_4_book_period.png)
- Extended reconstruction: [figures/14-4/plots/extended/figure_14_4_extended.png](figures/14-4/plots/extended/figure_14_4_extended.png)
- Diagnostic: [figures/14-4/plots/diagnostics/temporal_aggregation.png](figures/14-4/plots/diagnostics/temporal_aggregation.png)
- Book period clean: [figures/14-4/data/clean/figure_14_4_book_period.csv](figures/14-4/data/clean/figure_14_4_book_period.csv)
- Successor clean: [figures/14-4/data/clean/figure_14_4_successor.csv](figures/14-4/data/clean/figure_14_4_successor.csv)
- Diagnostic clean: [figures/14-4/data/clean/figure_14_4_diagnostic.csv](figures/14-4/data/clean/figure_14_4_diagnostic.csv)
- Historical records: [figures/14-4/data/clean/figure_14_4_historical_records.csv](figures/14-4/data/clean/figure_14_4_historical_records.csv)
- Archive agreement: [figures/14-4/data/clean/figure_14_4_archive_agreement.csv](figures/14-4/data/clean/figure_14_4_archive_agreement.csv)
- Population clean: [figures/14-4/data/clean/figure_14_4_population.csv](figures/14-4/data/clean/figure_14_4_population.csv)
- Lineage: [figures/14-4/lineage/lineage.json](figures/14-4/lineage/lineage.json)
- Lineage csv: [figures/14-4/lineage/lineage.csv](figures/14-4/lineage/lineage.csv)
- Reconstruction script: [scripts/reconstruct_14_4.py](scripts/reconstruct_14_4.py)
- Book period comparison: [figures/14-4/plots/comparisons/figure_14_4_book_period_review.png](figures/14-4/plots/comparisons/figure_14_4_book_period_review.png)
- Extended comparison: [figures/14-4/plots/comparisons/figure_14_4_extended_review.png](figures/14-4/plots/comparisons/figure_14_4_extended_review.png)

### Figure 15-1 - Racist, sexist, and homophobic opinions, US, 1987-2012

Status: `partial_match`. Artifact kind: `reconstruction`.

- Metadata: [figures/15-1/figure.json](figures/15-1/figure.json)
- Original reference: [references/figures/figure_15_1.png](references/figures/figure_15_1.png)
- Book period reconstruction: [figures/15-1/plots/figure_15_1_book_period.png](figures/15-1/plots/figure_15_1_book_period.png)
- Extended reconstruction: [figures/15-1/plots/figure_15_1_extended.png](figures/15-1/plots/figure_15_1_extended.png)
- Book period clean: [figures/15-1/data/clean/figure_15_1_book_period.csv](figures/15-1/data/clean/figure_15_1_book_period.csv)
- Successor clean: [figures/15-1/data/clean/figure_15_1_successor.csv](figures/15-1/data/clean/figure_15_1_successor.csv)
- Book period comparison: [figures/15-1/plots/comparisons/figure_15_1_book_period_review.png](figures/15-1/plots/comparisons/figure_15_1_book_period_review.png)
- Extended comparison: [figures/15-1/plots/comparisons/figure_15_1_extended_review.png](figures/15-1/plots/comparisons/figure_15_1_extended_review.png)
- Caption: [figures/15-1/captions/caption.txt](figures/15-1/captions/caption.txt)
- Provenance: [figures/15-1/provenance/provenance.md](figures/15-1/provenance/provenance.md)
- Source log: [figures/15-1/source_logs/source_log.md](figures/15-1/source_logs/source_log.md)
- Anomaly review: [figures/15-1/anomaly_reviews/anomaly_review.md](figures/15-1/anomaly_reviews/anomaly_review.md)
- Discrepancy log: [figures/15-1/discrepancy_logs/discrepancy_log.md](figures/15-1/discrepancy_logs/discrepancy_log.md)
- Review checklist: [figures/15-1/review_checklist.md](figures/15-1/review_checklist.md)
- Lineage: [figures/15-1/lineage/lineage.json](figures/15-1/lineage/lineage.json)
- Reconstruction script: [scripts/reconstruct_15_1.py](scripts/reconstruct_15_1.py)

### Figure 15-2 - Racist, sexist, and homophobic Web searches, US, 2004-2017

Status: `partial_match`. Artifact kind: `reconstruction`.

- Metadata: [figures/15-2/figure.json](figures/15-2/figure.json)
- Original reference: [references/figures/figure_15_2.png](references/figures/figure_15_2.png)
- Book period reconstruction: [figures/15-2/plots/figure_15_2_book_period.png](figures/15-2/plots/figure_15_2_book_period.png)
- Extended reconstruction: [figures/15-2/plots/figure_15_2_extended.png](figures/15-2/plots/figure_15_2_extended.png)
- Book period clean: [figures/15-2/data/clean/figure_15_2_book_period.csv](figures/15-2/data/clean/figure_15_2_book_period.csv)
- Successor clean: [figures/15-2/data/clean/figure_15_2_successor.csv](figures/15-2/data/clean/figure_15_2_successor.csv)
- Book period comparison: [figures/15-2/plots/comparisons/figure_15_2_book_period_review.png](figures/15-2/plots/comparisons/figure_15_2_book_period_review.png)
- Extended comparison: [figures/15-2/plots/comparisons/figure_15_2_extended_review.png](figures/15-2/plots/comparisons/figure_15_2_extended_review.png)
- Caption: [figures/15-2/captions/caption.txt](figures/15-2/captions/caption.txt)
- Provenance: [figures/15-2/provenance/provenance.md](figures/15-2/provenance/provenance.md)
- Source log: [figures/15-2/source_logs/source_log.md](figures/15-2/source_logs/source_log.md)
- Anomaly review: [figures/15-2/anomaly_reviews/anomaly_review.md](figures/15-2/anomaly_reviews/anomaly_review.md)
- Discrepancy log: [figures/15-2/discrepancy_logs/discrepancy_log.md](figures/15-2/discrepancy_logs/discrepancy_log.md)
- Review checklist: [figures/15-2/review_checklist.md](figures/15-2/review_checklist.md)
- Lineage: [figures/15-2/lineage/lineage.json](figures/15-2/lineage/lineage.json)
- Reconstruction script: [scripts/reconstruct_15_2.py](scripts/reconstruct_15_2.py)

### Figure 15-3 - Hate crimes, US, 1996-2015

Status: `updated_equivalent`. Artifact kind: `reconstruction`.

- Metadata: [figures/15-3/figure.json](figures/15-3/figure.json)
- Original reference: [references/figures/figure_15_3.png](references/figures/figure_15_3.png)
- Book period reconstruction: [figures/15-3/plots/figure_15_3_book_period.png](figures/15-3/plots/figure_15_3_book_period.png)
- Extended reconstruction: [figures/15-3/plots/figure_15_3_extended.png](figures/15-3/plots/figure_15_3_extended.png)
- Book period clean: [figures/15-3/data/clean/figure_15_3_book_period.csv](figures/15-3/data/clean/figure_15_3_book_period.csv)
- Successor clean: [figures/15-3/data/clean/figure_15_3_successor.csv](figures/15-3/data/clean/figure_15_3_successor.csv)
- Book period comparison: [figures/15-3/plots/comparisons/figure_15_3_book_period_review.png](figures/15-3/plots/comparisons/figure_15_3_book_period_review.png)
- Extended comparison: [figures/15-3/plots/comparisons/figure_15_3_extended_review.png](figures/15-3/plots/comparisons/figure_15_3_extended_review.png)
- Caption: [figures/15-3/captions/caption.txt](figures/15-3/captions/caption.txt)
- Provenance: [figures/15-3/provenance/provenance.md](figures/15-3/provenance/provenance.md)
- Source log: [figures/15-3/source_logs/source_log.md](figures/15-3/source_logs/source_log.md)
- Anomaly review: [figures/15-3/anomaly_reviews/anomaly_review.md](figures/15-3/anomaly_reviews/anomaly_review.md)
- Discrepancy log: [figures/15-3/discrepancy_logs/discrepancy_log.md](figures/15-3/discrepancy_logs/discrepancy_log.md)
- Review checklist: [figures/15-3/review_checklist.md](figures/15-3/review_checklist.md)
- Lineage: [figures/15-3/lineage/lineage.json](figures/15-3/lineage/lineage.json)
- Reconstruction script: [scripts/reconstruct_15_3.py](scripts/reconstruct_15_3.py)

### Figure 16-1 - Literacy, 1475-2010

Status: `verified_reproduction`. Artifact kind: `reconstruction`.

- Metadata: [figures/16-1/figure.json](figures/16-1/figure.json)
- Original reference: [references/figures/figure_16_1.png](references/figures/figure_16_1.png)
- Provenance: [figures/16-1/provenance/provenance.md](figures/16-1/provenance/provenance.md)
- Caption: [figures/16-1/captions/caption.txt](figures/16-1/captions/caption.txt)
- Source log: [figures/16-1/source_logs/source_log.md](figures/16-1/source_logs/source_log.md)
- Search log: [figures/16-1/search_iterations/search_iterations.md](figures/16-1/search_iterations/search_iterations.md)
- Download log: [figures/16-1/source_logs/downloads.json](figures/16-1/source_logs/downloads.json)
- Anomaly review: [figures/16-1/anomaly_reviews/anomaly_review.md](figures/16-1/anomaly_reviews/anomaly_review.md)
- Discrepancy log: [figures/16-1/discrepancy_logs/discrepancy_log.md](figures/16-1/discrepancy_logs/discrepancy_log.md)
- Review checklist: [figures/16-1/review_checklist.md](figures/16-1/review_checklist.md)
- Book period reconstruction: [figures/16-1/plots/book_period/figure_16_1_book_period.png](figures/16-1/plots/book_period/figure_16_1_book_period.png)
- Extended reconstruction: [figures/16-1/plots/extended/figure_16_1_extended.png](figures/16-1/plots/extended/figure_16_1_extended.png)
- Diagnostic plot: [figures/16-1/plots/diagnostics/world_vintages.png](figures/16-1/plots/diagnostics/world_vintages.png)
- Book period clean: [figures/16-1/data/clean/figure_16_1_book_period.csv](figures/16-1/data/clean/figure_16_1_book_period.csv)
- Extended clean: [figures/16-1/data/clean/figure_16_1_successor.csv](figures/16-1/data/clean/figure_16_1_successor.csv)
- Diagnostic clean: [figures/16-1/data/clean/figure_16_1_world_vintages.csv](figures/16-1/data/clean/figure_16_1_world_vintages.csv)
- Crosscheck clean: [figures/16-1/data/clean/figure_16_1_nces_check.csv](figures/16-1/data/clean/figure_16_1_nces_check.csv)
- Lineage: [figures/16-1/lineage/lineage.json](figures/16-1/lineage/lineage.json)
- Lineage csv: [figures/16-1/lineage/lineage.csv](figures/16-1/lineage/lineage.csv)
- Reconstruction script: [scripts/reconstruct_16_1.py](scripts/reconstruct_16_1.py)
- Book period comparison: [figures/16-1/plots/comparisons/figure_16_1_book_period_review.png](figures/16-1/plots/comparisons/figure_16_1_book_period_review.png)
- Extended comparison: [figures/16-1/plots/comparisons/figure_16_1_extended_review.png](figures/16-1/plots/comparisons/figure_16_1_extended_review.png)

### Figure 16-2 - Basic education, 1820-2010

Status: `partial_match`. Artifact kind: `reconstruction`.

- Metadata: [figures/16-2/figure.json](figures/16-2/figure.json)
- Original reference: [references/figures/figure_16_2.png](references/figures/figure_16_2.png)
- Provenance: [figures/16-2/provenance/provenance.md](figures/16-2/provenance/provenance.md)
- Caption: [figures/16-2/captions/caption.txt](figures/16-2/captions/caption.txt)
- Source log: [figures/16-2/source_logs/source_log.md](figures/16-2/source_logs/source_log.md)
- Search log: [figures/16-2/search_iterations/search_iterations.md](figures/16-2/search_iterations/search_iterations.md)
- Download log: [figures/16-2/source_logs/downloads.json](figures/16-2/source_logs/downloads.json)
- Anomaly review: [figures/16-2/anomaly_reviews/anomaly_review.md](figures/16-2/anomaly_reviews/anomaly_review.md)
- Discrepancy log: [figures/16-2/discrepancy_logs/discrepancy_log.md](figures/16-2/discrepancy_logs/discrepancy_log.md)
- Review checklist: [figures/16-2/review_checklist.md](figures/16-2/review_checklist.md)
- Book period reconstruction: [figures/16-2/plots/book_period/figure_16_2_book_period.png](figures/16-2/plots/book_period/figure_16_2_book_period.png)
- Extended reconstruction: [figures/16-2/plots/extended/figure_16_2_extended.png](figures/16-2/plots/extended/figure_16_2_extended.png)
- Diagnostic plot: [figures/16-2/plots/diagnostics/rejected_projection_successor.png](figures/16-2/plots/diagnostics/rejected_projection_successor.png)
- Book period clean: [figures/16-2/data/clean/figure_16_2_book_period.csv](figures/16-2/data/clean/figure_16_2_book_period.csv)
- Crosscheck clean: [figures/16-2/data/clean/figure_16_2_oecd_crosscheck.csv](figures/16-2/data/clean/figure_16_2_oecd_crosscheck.csv)
- Diagnostic clean: [figures/16-2/data/clean/figure_16_2_rejected_successor.csv](figures/16-2/data/clean/figure_16_2_rejected_successor.csv)
- Lineage: [figures/16-2/lineage/lineage.json](figures/16-2/lineage/lineage.json)
- Lineage csv: [figures/16-2/lineage/lineage.csv](figures/16-2/lineage/lineage.csv)
- Reconstruction script: [scripts/reconstruct_16_2.py](scripts/reconstruct_16_2.py)
- Book period comparison: [figures/16-2/plots/comparisons/figure_16_2_book_period_review.png](figures/16-2/plots/comparisons/figure_16_2_book_period_review.png)
- Extended comparison: [figures/16-2/plots/comparisons/figure_16_2_extended_review.png](figures/16-2/plots/comparisons/figure_16_2_extended_review.png)

### Figure 16-3 - Years of schooling, 1870-2010

Status: `verified_reproduction`. Artifact kind: `reconstruction`.

- Metadata: [figures/16-3/figure.json](figures/16-3/figure.json)
- Original reference: [references/figures/figure_16_3.png](references/figures/figure_16_3.png)
- Provenance: [figures/16-3/provenance/provenance.md](figures/16-3/provenance/provenance.md)
- Caption: [figures/16-3/captions/caption.txt](figures/16-3/captions/caption.txt)
- Source log: [figures/16-3/source_logs/source_log.md](figures/16-3/source_logs/source_log.md)
- Search log: [figures/16-3/search_iterations/search_iterations.md](figures/16-3/search_iterations/search_iterations.md)
- Download log: [figures/16-3/source_logs/downloads.json](figures/16-3/source_logs/downloads.json)
- Anomaly review: [figures/16-3/anomaly_reviews/anomaly_review.md](figures/16-3/anomaly_reviews/anomaly_review.md)
- Discrepancy log: [figures/16-3/discrepancy_logs/discrepancy_log.md](figures/16-3/discrepancy_logs/discrepancy_log.md)
- Review checklist: [figures/16-3/review_checklist.md](figures/16-3/review_checklist.md)
- Book period reconstruction: [figures/16-3/plots/book_period/figure_16_3_book_period.png](figures/16-3/plots/book_period/figure_16_3_book_period.png)
- Extended reconstruction: [figures/16-3/plots/extended/figure_16_3_extended.png](figures/16-3/plots/extended/figure_16_3_extended.png)
- Diagnostic plot: [figures/16-3/plots/diagnostics/vintage_difference.png](figures/16-3/plots/diagnostics/vintage_difference.png)
- Book period clean: [figures/16-3/data/clean/figure_16_3_book_period.csv](figures/16-3/data/clean/figure_16_3_book_period.csv)
- Extended clean: [figures/16-3/data/clean/figure_16_3_successor.csv](figures/16-3/data/clean/figure_16_3_successor.csv)
- Crosscheck clean: [figures/16-3/data/clean/figure_16_3_archive_check.csv](figures/16-3/data/clean/figure_16_3_archive_check.csv)
- Diagnostic clean: [figures/16-3/data/clean/figure_16_3_vintage_difference.csv](figures/16-3/data/clean/figure_16_3_vintage_difference.csv)
- Lineage: [figures/16-3/lineage/lineage.json](figures/16-3/lineage/lineage.json)
- Lineage csv: [figures/16-3/lineage/lineage.csv](figures/16-3/lineage/lineage.csv)
- Reconstruction script: [scripts/reconstruct_16_3.py](scripts/reconstruct_16_3.py)
- Book period comparison: [figures/16-3/plots/comparisons/figure_16_3_book_period_review.png](figures/16-3/plots/comparisons/figure_16_3_book_period_review.png)
- Extended comparison: [figures/16-3/plots/comparisons/figure_16_3_extended_review.png](figures/16-3/plots/comparisons/figure_16_3_extended_review.png)

### Figure 16-4 - Female literacy, 1750-2014

Status: `partial_match`. Artifact kind: `reconstruction`.

- Metadata: [figures/16-4/figure.json](figures/16-4/figure.json)
- Original reference: [references/figures/figure_16_4.png](references/figures/figure_16_4.png)
- Provenance: [figures/16-4/provenance/provenance.md](figures/16-4/provenance/provenance.md)
- Caption: [figures/16-4/captions/caption.txt](figures/16-4/captions/caption.txt)
- Source log: [figures/16-4/source_logs/source_log.md](figures/16-4/source_logs/source_log.md)
- Search log: [figures/16-4/search_iterations/search_iterations.md](figures/16-4/search_iterations/search_iterations.md)
- Download log: [figures/16-4/source_logs/downloads.json](figures/16-4/source_logs/downloads.json)
- Anomaly review: [figures/16-4/anomaly_reviews/anomaly_review.md](figures/16-4/anomaly_reviews/anomaly_review.md)
- Discrepancy log: [figures/16-4/discrepancy_logs/discrepancy_log.md](figures/16-4/discrepancy_logs/discrepancy_log.md)
- Review checklist: [figures/16-4/review_checklist.md](figures/16-4/review_checklist.md)
- Book period reconstruction: [figures/16-4/plots/book_period/figure_16_4_book_period.png](figures/16-4/plots/book_period/figure_16_4_book_period.png)
- Extended reconstruction: [figures/16-4/plots/extended/figure_16_4_extended.png](figures/16-4/plots/extended/figure_16_4_extended.png)
- Diagnostic plot: [figures/16-4/plots/diagnostics/vintage_difference.png](figures/16-4/plots/diagnostics/vintage_difference.png)
- Book period clean: [figures/16-4/data/clean/figure_16_4_book_period.csv](figures/16-4/data/clean/figure_16_4_book_period.csv)
- Extended clean: [figures/16-4/data/clean/figure_16_4_successor.csv](figures/16-4/data/clean/figure_16_4_successor.csv)
- Diagnostic clean: [figures/16-4/data/clean/figure_16_4_rejected_world_mean.csv](figures/16-4/data/clean/figure_16_4_rejected_world_mean.csv)
- Revision clean: [figures/16-4/data/clean/figure_16_4_vintage_difference.csv](figures/16-4/data/clean/figure_16_4_vintage_difference.csv)
- Lineage: [figures/16-4/lineage/lineage.json](figures/16-4/lineage/lineage.json)
- Lineage csv: [figures/16-4/lineage/lineage.csv](figures/16-4/lineage/lineage.csv)
- Reconstruction script: [scripts/reconstruct_16_4.py](scripts/reconstruct_16_4.py)
- Book period comparison: [figures/16-4/plots/comparisons/figure_16_4_book_period_review.png](figures/16-4/plots/comparisons/figure_16_4_book_period_review.png)
- Extended comparison: [figures/16-4/plots/comparisons/figure_16_4_extended_review.png](figures/16-4/plots/comparisons/figure_16_4_extended_review.png)

### Figure 16-5 - IQ gains, 1909-2013

Status: `partial_match`. Artifact kind: `reconstruction`.

- Metadata: [figures/16-5/figure.json](figures/16-5/figure.json)
- Original reference: [references/figures/figure_16_5.png](references/figures/figure_16_5.png)
- Provenance: [figures/16-5/provenance/provenance.md](figures/16-5/provenance/provenance.md)
- Caption: [figures/16-5/captions/caption.txt](figures/16-5/captions/caption.txt)
- Source log: [figures/16-5/source_logs/source_log.md](figures/16-5/source_logs/source_log.md)
- Search log: [figures/16-5/search_iterations/search_iterations.md](figures/16-5/search_iterations/search_iterations.md)
- Download log: [figures/16-5/source_logs/downloads.json](figures/16-5/source_logs/downloads.json)
- Anomaly review: [figures/16-5/anomaly_reviews/anomaly_review.md](figures/16-5/anomaly_reviews/anomaly_review.md)
- Discrepancy log: [figures/16-5/discrepancy_logs/discrepancy_log.md](figures/16-5/discrepancy_logs/discrepancy_log.md)
- Review checklist: [figures/16-5/review_checklist.md](figures/16-5/review_checklist.md)
- Book period reconstruction: [figures/16-5/plots/book_period/figure_16_5_book_period.png](figures/16-5/plots/book_period/figure_16_5_book_period.png)
- Extended reconstruction: [figures/16-5/plots/extended/figure_16_5_extended.png](figures/16-5/plots/extended/figure_16_5_extended.png)
- Book period clean: [figures/16-5/data/clean/figure_16_5_book_period.csv](figures/16-5/data/clean/figure_16_5_book_period.csv)
- Diagnostic clean: [figures/16-5/data/clean/figure_16_5_segments.csv](figures/16-5/data/clean/figure_16_5_segments.csv)
- Lineage: [figures/16-5/lineage/lineage.json](figures/16-5/lineage/lineage.json)
- Lineage csv: [figures/16-5/lineage/lineage.csv](figures/16-5/lineage/lineage.csv)
- Reconstruction script: [scripts/reconstruct_16_5.py](scripts/reconstruct_16_5.py)
- Book period comparison: [figures/16-5/plots/comparisons/figure_16_5_book_period_review.png](figures/16-5/plots/comparisons/figure_16_5_book_period_review.png)
- Extended comparison: [figures/16-5/plots/comparisons/figure_16_5_extended_review.png](figures/16-5/plots/comparisons/figure_16_5_extended_review.png)

### Figure 16-6 - Global well-being, 1820-2015

Status: `partial_match`. Artifact kind: `reconstruction`.

- Metadata: [figures/16-6/figure.json](figures/16-6/figure.json)
- Original reference: [references/figures/figure_16_6.png](references/figures/figure_16_6.png)
- Provenance: [figures/16-6/provenance/provenance.md](figures/16-6/provenance/provenance.md)
- Caption: [figures/16-6/captions/caption.txt](figures/16-6/captions/caption.txt)
- Source log: [figures/16-6/source_logs/source_log.md](figures/16-6/source_logs/source_log.md)
- Search log: [figures/16-6/search_iterations/search_iterations.md](figures/16-6/search_iterations/search_iterations.md)
- Download log: [figures/16-6/source_logs/downloads.json](figures/16-6/source_logs/downloads.json)
- Additional download log: [figures/16-6/source_logs/downloads.jsonl](figures/16-6/source_logs/downloads.jsonl)
- Anomaly review: [figures/16-6/anomaly_reviews/anomaly_review.md](figures/16-6/anomaly_reviews/anomaly_review.md)
- Discrepancy log: [figures/16-6/discrepancy_logs/discrepancy_log.md](figures/16-6/discrepancy_logs/discrepancy_log.md)
- Review checklist: [figures/16-6/review_checklist.md](figures/16-6/review_checklist.md)
- Book period reconstruction: [figures/16-6/plots/book_period/figure_16_6_book_period.png](figures/16-6/plots/book_period/figure_16_6_book_period.png)
- Extended reconstruction: [figures/16-6/plots/extended/figure_16_6_extended.png](figures/16-6/plots/extended/figure_16_6_extended.png)
- Book period clean: [figures/16-6/data/clean/figure_16_6_book_period.csv](figures/16-6/data/clean/figure_16_6_book_period.csv)
- Lineage: [figures/16-6/lineage/lineage.json](figures/16-6/lineage/lineage.json)
- Lineage csv: [figures/16-6/lineage/lineage.csv](figures/16-6/lineage/lineage.csv)
- Reconstruction script: [scripts/reconstruct_16_6.py](scripts/reconstruct_16_6.py)
- Table extraction script: [scripts/recover_16_6_table.py](scripts/recover_16_6_table.py)
- Book period comparison: [figures/16-6/plots/comparisons/figure_16_6_book_period_review.png](figures/16-6/plots/comparisons/figure_16_6_book_period_review.png)
- Extended comparison: [figures/16-6/plots/comparisons/figure_16_6_extended_review.png](figures/16-6/plots/comparisons/figure_16_6_extended_review.png)

### Figure 17-1 - Work hours, Western Europe and US, 1870-2000

Status: `partial_match`. Artifact kind: `reconstruction`.

- Metadata: [figures/17-1/figure.json](figures/17-1/figure.json)
- Original reference: [references/figures/figure_17_1.png](references/figures/figure_17_1.png)
- Provenance: [figures/17-1/provenance/provenance.md](figures/17-1/provenance/provenance.md)
- Caption: [figures/17-1/captions/caption.txt](figures/17-1/captions/caption.txt)
- Source log: [figures/17-1/source_logs/source_log.md](figures/17-1/source_logs/source_log.md)
- Search log: [figures/17-1/search_iterations/search_iterations.md](figures/17-1/search_iterations/search_iterations.md)
- Download log: [figures/17-1/source_logs/downloads.json](figures/17-1/source_logs/downloads.json)
- Anomaly review: [figures/17-1/anomaly_reviews/anomaly_review.md](figures/17-1/anomaly_reviews/anomaly_review.md)
- Discrepancy log: [figures/17-1/discrepancy_logs/discrepancy_log.md](figures/17-1/discrepancy_logs/discrepancy_log.md)
- Review checklist: [figures/17-1/review_checklist.md](figures/17-1/review_checklist.md)
- Book period reconstruction: [figures/17-1/plots/book_period/figure_17_1_book_period.png](figures/17-1/plots/book_period/figure_17_1_book_period.png)
- Extended reconstruction: [figures/17-1/plots/extended/figure_17_1_extended.png](figures/17-1/plots/extended/figure_17_1_extended.png)
- Diagnostic plot: [figures/17-1/plots/diagnostics/weighting.png](figures/17-1/plots/diagnostics/weighting.png)
- Book period clean: [figures/17-1/data/clean/figure_17_1_book_period.csv](figures/17-1/data/clean/figure_17_1_book_period.csv)
- Diagnostic clean: [figures/17-1/data/clean/figure_17_1_weighting_diagnostic.csv](figures/17-1/data/clean/figure_17_1_weighting_diagnostic.csv)
- Reconstruction script: [scripts/reconstruct_17_1.py](scripts/reconstruct_17_1.py)
- Lineage: [figures/17-1/lineage/lineage.json](figures/17-1/lineage/lineage.json)
- Lineage csv: [figures/17-1/lineage/lineage.csv](figures/17-1/lineage/lineage.csv)
- Book period comparison: [figures/17-1/plots/comparisons/figure_17_1_book_period_review.png](figures/17-1/plots/comparisons/figure_17_1_book_period_review.png)
- Extended comparison: [figures/17-1/plots/comparisons/figure_17_1_extended_review.png](figures/17-1/plots/comparisons/figure_17_1_extended_review.png)

### Figure 17-2 - Retirement, US, 1880-2010

Status: `partial_match`. Artifact kind: `reconstruction`.

- Metadata: [figures/17-2/figure.json](figures/17-2/figure.json)
- Provenance: [figures/17-2/provenance/provenance.md](figures/17-2/provenance/provenance.md)
- Caption: [figures/17-2/captions/caption.txt](figures/17-2/captions/caption.txt)
- Source log: [figures/17-2/source_logs/source_log.md](figures/17-2/source_logs/source_log.md)
- Search log: [figures/17-2/search_iterations/search_iterations.md](figures/17-2/search_iterations/search_iterations.md)
- Download log: [figures/17-2/source_logs/downloads.json](figures/17-2/source_logs/downloads.json)
- Anomaly review: [figures/17-2/anomaly_reviews/anomaly_review.md](figures/17-2/anomaly_reviews/anomaly_review.md)
- Discrepancy log: [figures/17-2/discrepancy_logs/discrepancy_log.md](figures/17-2/discrepancy_logs/discrepancy_log.md)
- Review checklist: [figures/17-2/review_checklist.md](figures/17-2/review_checklist.md)
- Book period reconstruction: [figures/17-2/plots/book_period/figure_17_2_book_period.png](figures/17-2/plots/book_period/figure_17_2_book_period.png)
- Extended reconstruction: [figures/17-2/plots/extended/figure_17_2_extended.png](figures/17-2/plots/extended/figure_17_2_extended.png)
- Diagnostic plot: [figures/17-2/plots/diagnostics/definitions.png](figures/17-2/plots/diagnostics/definitions.png)
- Book period clean: [figures/17-2/data/clean/figure_17_2_book_period.csv](figures/17-2/data/clean/figure_17_2_book_period.csv)
- Extended clean: [figures/17-2/data/clean/figure_17_2_extended.csv](figures/17-2/data/clean/figure_17_2_extended.csv)
- Diagnostic clean: [figures/17-2/data/clean/figure_17_2_definitions.csv](figures/17-2/data/clean/figure_17_2_definitions.csv)
- Reconstruction script: [scripts/reconstruct_17_2.py](scripts/reconstruct_17_2.py)
- Lineage: [figures/17-2/lineage/lineage.json](figures/17-2/lineage/lineage.json)
- Lineage csv: [figures/17-2/lineage/lineage.csv](figures/17-2/lineage/lineage.csv)
- Original reference: [references/figures/figure_17_2.png](references/figures/figure_17_2.png)
- Book period comparison: [figures/17-2/plots/comparisons/figure_17_2_book_period_review.png](figures/17-2/plots/comparisons/figure_17_2_book_period_review.png)
- Extended comparison: [figures/17-2/plots/comparisons/figure_17_2_extended_review.png](figures/17-2/plots/comparisons/figure_17_2_extended_review.png)

### Figure 17-3 - Utilities, appliances, and housework, US, 1900-2015

Status: `partial_match`. Artifact kind: `reconstruction`.

- Provenance: [figures/17-3/provenance/provenance.md](figures/17-3/provenance/provenance.md)
- Caption: [figures/17-3/captions/caption.txt](figures/17-3/captions/caption.txt)
- Source log: [figures/17-3/source_logs/source_log.md](figures/17-3/source_logs/source_log.md)
- Search log: [figures/17-3/search_iterations/search_iterations.md](figures/17-3/search_iterations/search_iterations.md)
- Download log: [figures/17-3/source_logs/downloads.json](figures/17-3/source_logs/downloads.json)
- Anomaly review: [figures/17-3/anomaly_reviews/anomaly_review.md](figures/17-3/anomaly_reviews/anomaly_review.md)
- Discrepancy log: [figures/17-3/discrepancy_logs/discrepancy_log.md](figures/17-3/discrepancy_logs/discrepancy_log.md)
- Review checklist: [figures/17-3/review_checklist.md](figures/17-3/review_checklist.md)
- Book period reconstruction: [figures/17-3/plots/book_period/figure_17_3_book_period.png](figures/17-3/plots/book_period/figure_17_3_book_period.png)
- Extended reconstruction: [figures/17-3/plots/extended/figure_17_3_extended.png](figures/17-3/plots/extended/figure_17_3_extended.png)
- Diagnostic plot: [figures/17-3/plots/diagnostics/housework_definition_candidates.png](figures/17-3/plots/diagnostics/housework_definition_candidates.png)
- Book period clean: [figures/17-3/data/clean/figure_17_3_book_period.csv](figures/17-3/data/clean/figure_17_3_book_period.csv)
- Housework clean: [figures/17-3/data/clean/figure_17_3_housework_anchors.csv](figures/17-3/data/clean/figure_17_3_housework_anchors.csv)
- Census clean: [figures/17-3/data/clean/figure_17_3_census_detail.csv](figures/17-3/data/clean/figure_17_3_census_detail.csv)
- Diagnostic clean: [figures/17-3/data/clean/figure_17_3_bls_candidates.csv](figures/17-3/data/clean/figure_17_3_bls_candidates.csv)
- Reconstruction script: [scripts/reconstruct_17_3.py](scripts/reconstruct_17_3.py)
- Recovery script: [scripts/recover_17_3_tables.py](scripts/recover_17_3_tables.py)
- Lineage: [figures/17-3/lineage/lineage.json](figures/17-3/lineage/lineage.json)
- Lineage csv: [figures/17-3/lineage/lineage.csv](figures/17-3/lineage/lineage.csv)
- Metadata: [figures/17-3/figure.json](figures/17-3/figure.json)
- Original reference: [references/figures/figure_17_3.png](references/figures/figure_17_3.png)
- Book period comparison: [figures/17-3/plots/comparisons/figure_17_3_book_period_review.png](figures/17-3/plots/comparisons/figure_17_3_book_period_review.png)
- Extended comparison: [figures/17-3/plots/comparisons/figure_17_3_extended_review.png](figures/17-3/plots/comparisons/figure_17_3_extended_review.png)

### Figure 17-4 - Cost of light, England, 1300-2006

Status: `verified_reproduction`. Artifact kind: `reconstruction`.

- Metadata: [figures/17-4/figure.json](figures/17-4/figure.json)
- Original reference: [references/figures/figure_17_4.png](references/figures/figure_17_4.png)
- Provenance: [figures/17-4/provenance/provenance.md](figures/17-4/provenance/provenance.md)
- Source log: [figures/17-4/source_logs/source_log.md](figures/17-4/source_logs/source_log.md)
- Search log: [figures/17-4/search_iterations/search_iterations.md](figures/17-4/search_iterations/search_iterations.md)
- Caption: [figures/17-4/captions/caption.txt](figures/17-4/captions/caption.txt)
- Anomaly review: [figures/17-4/anomaly_reviews/anomaly_review.md](figures/17-4/anomaly_reviews/anomaly_review.md)
- Discrepancy log: [figures/17-4/discrepancy_logs/discrepancy_log.md](figures/17-4/discrepancy_logs/discrepancy_log.md)
- Review checklist: [figures/17-4/review_checklist.md](figures/17-4/review_checklist.md)
- Download log: [figures/17-4/source_logs/downloads.json](figures/17-4/source_logs/downloads.json)
- Book period reconstruction: [figures/17-4/plots/book_period/figure_17_4_book_period.png](figures/17-4/plots/book_period/figure_17_4_book_period.png)
- Extended reconstruction: [figures/17-4/plots/extended/figure_17_4_extended.png](figures/17-4/plots/extended/figure_17_4_extended.png)
- Diagnostic plot: [figures/17-4/plots/diagnostics/source_versions.png](figures/17-4/plots/diagnostics/source_versions.png)
- Book period clean: [figures/17-4/data/clean/figure_17_4_book_period.csv](figures/17-4/data/clean/figure_17_4_book_period.csv)
- Extended clean: [figures/17-4/data/clean/figure_17_4_extended.csv](figures/17-4/data/clean/figure_17_4_extended.csv)
- Diagnostic clean: [figures/17-4/data/clean/figure_17_4_source_versions.csv](figures/17-4/data/clean/figure_17_4_source_versions.csv)
- Reconstruction script: [scripts/reconstruct_17_4.py](scripts/reconstruct_17_4.py)
- Book period comparison: [figures/17-4/plots/comparisons/figure_17_4_book_period_review.png](figures/17-4/plots/comparisons/figure_17_4_book_period_review.png)
- Extended comparison: [figures/17-4/plots/comparisons/figure_17_4_extended_review.png](figures/17-4/plots/comparisons/figure_17_4_extended_review.png)
- Lineage: [figures/17-4/lineage/lineage.json](figures/17-4/lineage/lineage.json)
- Lineage csv: [figures/17-4/lineage/lineage.csv](figures/17-4/lineage/lineage.csv)

### Figure 17-5 - Spending on necessities, US, 1929-2016

Status: `partial_match`. Artifact kind: `reconstruction`.

- Metadata: [figures/17-5/figure.json](figures/17-5/figure.json)
- Provenance: [figures/17-5/provenance/provenance.md](figures/17-5/provenance/provenance.md)
- Caption: [figures/17-5/captions/caption.txt](figures/17-5/captions/caption.txt)
- Source log: [figures/17-5/source_logs/source_log.md](figures/17-5/source_logs/source_log.md)
- Search log: [figures/17-5/search_iterations/search_iterations.md](figures/17-5/search_iterations/search_iterations.md)
- Download log: [figures/17-5/source_logs/downloads.json](figures/17-5/source_logs/downloads.json)
- Anomaly review: [figures/17-5/anomaly_reviews/anomaly_review.md](figures/17-5/anomaly_reviews/anomaly_review.md)
- Discrepancy log: [figures/17-5/discrepancy_logs/discrepancy_log.md](figures/17-5/discrepancy_logs/discrepancy_log.md)
- Review checklist: [figures/17-5/review_checklist.md](figures/17-5/review_checklist.md)
- Book period reconstruction: [figures/17-5/plots/book_period/figure_17_5_book_period.png](figures/17-5/plots/book_period/figure_17_5_book_period.png)
- Extended reconstruction: [figures/17-5/plots/extended/figure_17_5_extended.png](figures/17-5/plots/extended/figure_17_5_extended.png)
- Diagnostic plot: [figures/17-5/plots/diagnostics/basket_and_vintage.png](figures/17-5/plots/diagnostics/basket_and_vintage.png)
- Book period clean: [figures/17-5/data/clean/figure_17_5_book_period.csv](figures/17-5/data/clean/figure_17_5_book_period.csv)
- Extended clean: [figures/17-5/data/clean/figure_17_5_revised_successor.csv](figures/17-5/data/clean/figure_17_5_revised_successor.csv)
- Diagnostic clean: [figures/17-5/data/clean/figure_17_5_diagnostic.csv](figures/17-5/data/clean/figure_17_5_diagnostic.csv)
- Components clean: [figures/17-5/data/clean/figure_17_5_components.csv](figures/17-5/data/clean/figure_17_5_components.csv)
- Reconstruction script: [scripts/reconstruct_17_5.py](scripts/reconstruct_17_5.py)
- Source parser: [scripts/alfred_labels.py](scripts/alfred_labels.py)
- Lineage: [figures/17-5/lineage/lineage.json](figures/17-5/lineage/lineage.json)
- Lineage csv: [figures/17-5/lineage/lineage.csv](figures/17-5/lineage/lineage.csv)
- Original reference: [references/figures/figure_17_5.png](references/figures/figure_17_5.png)
- Book period comparison: [figures/17-5/plots/comparisons/figure_17_5_book_period_review.png](figures/17-5/plots/comparisons/figure_17_5_book_period_review.png)
- Extended comparison: [figures/17-5/plots/comparisons/figure_17_5_extended_review.png](figures/17-5/plots/comparisons/figure_17_5_extended_review.png)

### Figure 17-6 - Leisure time, US, 1965-2015

Status: `partial_match`. Artifact kind: `reconstruction`.

- Metadata: [figures/17-6/figure.json](figures/17-6/figure.json)
- Provenance: [figures/17-6/provenance/provenance.md](figures/17-6/provenance/provenance.md)
- Caption: [figures/17-6/captions/caption.txt](figures/17-6/captions/caption.txt)
- Source log: [figures/17-6/source_logs/source_log.md](figures/17-6/source_logs/source_log.md)
- Search log: [figures/17-6/search_iterations/search_iterations.md](figures/17-6/search_iterations/search_iterations.md)
- Download log: [figures/17-6/source_logs/downloads.json](figures/17-6/source_logs/downloads.json)
- Anomaly review: [figures/17-6/anomaly_reviews/anomaly_review.md](figures/17-6/anomaly_reviews/anomaly_review.md)
- Discrepancy log: [figures/17-6/discrepancy_logs/discrepancy_log.md](figures/17-6/discrepancy_logs/discrepancy_log.md)
- Review checklist: [figures/17-6/review_checklist.md](figures/17-6/review_checklist.md)
- Book period reconstruction: [figures/17-6/plots/book_period/figure_17_6_book_period.png](figures/17-6/plots/book_period/figure_17_6_book_period.png)
- Extended reconstruction: [figures/17-6/plots/extended/figure_17_6_extended.png](figures/17-6/plots/extended/figure_17_6_extended.png)
- Diagnostic plot: [figures/17-6/plots/diagnostics/pet_care_sensitivity.png](figures/17-6/plots/diagnostics/pet_care_sensitivity.png)
- Book period clean: [figures/17-6/data/clean/figure_17_6_book_period.csv](figures/17-6/data/clean/figure_17_6_book_period.csv)
- Extended clean: [figures/17-6/data/clean/figure_17_6_extended.csv](figures/17-6/data/clean/figure_17_6_extended.csv)
- Activities clean: [figures/17-6/data/clean/figure_17_6_activities.csv](figures/17-6/data/clean/figure_17_6_activities.csv)
- Author cells clean: [figures/17-6/data/clean/figure_17_6_author_cells.csv](figures/17-6/data/clean/figure_17_6_author_cells.csv)
- Reconstruction script: [scripts/reconstruct_17_6.py](scripts/reconstruct_17_6.py)
- Recovery script: [scripts/recover_17_6_tables.py](scripts/recover_17_6_tables.py)
- Lineage: [figures/17-6/lineage/lineage.json](figures/17-6/lineage/lineage.json)
- Lineage csv: [figures/17-6/lineage/lineage.csv](figures/17-6/lineage/lineage.csv)
- Original reference: [references/figures/figure_17_6.png](references/figures/figure_17_6.png)
- Book period comparison: [figures/17-6/plots/comparisons/figure_17_6_book_period_review.png](figures/17-6/plots/comparisons/figure_17_6_book_period_review.png)
- Extended comparison: [figures/17-6/plots/comparisons/figure_17_6_extended_review.png](figures/17-6/plots/comparisons/figure_17_6_extended_review.png)

### Figure 17-7 - Cost of air travel, US, 1979-2015

Status: `needs_targeted_source_recovery`. Artifact kind: `source_recovery`.

- Metadata: [figures/17-7/figure.json](figures/17-7/figure.json)
- Original reference: [references/figures/figure_17_7.png](references/figures/figure_17_7.png)
- Provenance: [figures/17-7/provenance/provenance.md](figures/17-7/provenance/provenance.md)
- Source log: [figures/17-7/source_logs/source_log.md](figures/17-7/source_logs/source_log.md)
- Download log: [figures/17-7/source_logs/downloads.json](figures/17-7/source_logs/downloads.json)
- Search log: [figures/17-7/search_iterations/search_iterations.md](figures/17-7/search_iterations/search_iterations.md)
- Caption: [figures/17-7/captions/caption.txt](figures/17-7/captions/caption.txt)
- Anomaly review: [figures/17-7/anomaly_reviews/anomaly_review.md](figures/17-7/anomaly_reviews/anomaly_review.md)
- Discrepancy log: [figures/17-7/discrepancy_logs/discrepancy_log.md](figures/17-7/discrepancy_logs/discrepancy_log.md)
- Review checklist: [figures/17-7/review_checklist.md](figures/17-7/review_checklist.md)

### Figure 17-8 - International tourism, 1995-2015

Status: `partial_match`. Artifact kind: `reconstruction`.

- Anomaly review: [figures/17-8/anomaly_reviews/anomaly_review.md](figures/17-8/anomaly_reviews/anomaly_review.md)
- Discrepancy log: [figures/17-8/discrepancy_logs/discrepancy_log.md](figures/17-8/discrepancy_logs/discrepancy_log.md)
- Review checklist: [figures/17-8/review_checklist.md](figures/17-8/review_checklist.md)
- Lineage: [figures/17-8/lineage/lineage.json](figures/17-8/lineage/lineage.json)
- Book period reconstruction: [figures/17-8/plots/book_period/figure_17_8_book_period.png](figures/17-8/plots/book_period/figure_17_8_book_period.png)
- Extended reconstruction: [figures/17-8/plots/extended/figure_17_8_extended.png](figures/17-8/plots/extended/figure_17_8_extended.png)
- Diagnostic plot: [figures/17-8/plots/diagnostics/source_versions.png](figures/17-8/plots/diagnostics/source_versions.png)
- Caption: [figures/17-8/captions/caption.txt](figures/17-8/captions/caption.txt)
- Provenance: [figures/17-8/provenance/provenance.md](figures/17-8/provenance/provenance.md)
- Source log: [figures/17-8/source_logs/source_log.md](figures/17-8/source_logs/source_log.md)
- Download log: [figures/17-8/source_logs/downloads.json](figures/17-8/source_logs/downloads.json)
- Search log: [figures/17-8/search_iterations/search_iterations.md](figures/17-8/search_iterations/search_iterations.md)
- Reconstruction script: [scripts/reconstruct_17_8.py](scripts/reconstruct_17_8.py)
- Source extraction script: [scripts/recover_17_8_tables.py](scripts/recover_17_8_tables.py)
- Book period clean: [figures/17-8/data/clean/figure_17_8_book_period.csv](figures/17-8/data/clean/figure_17_8_book_period.csv)
- Extended clean: [figures/17-8/data/clean/figure_17_8_extended.csv](figures/17-8/data/clean/figure_17_8_extended.csv)
- Diagnostic clean: [figures/17-8/data/clean/figure_17_8_source_version_diagnostic.csv](figures/17-8/data/clean/figure_17_8_source_version_diagnostic.csv)
- Metadata: [figures/17-8/figure.json](figures/17-8/figure.json)
- Original reference: [references/figures/figure_17_8.png](references/figures/figure_17_8.png)
- Book period comparison: [figures/17-8/plots/comparisons/figure_17_8_book_period_review.png](figures/17-8/plots/comparisons/figure_17_8_book_period_review.png)
- Extended comparison: [figures/17-8/plots/comparisons/figure_17_8_extended_review.png](figures/17-8/plots/comparisons/figure_17_8_extended_review.png)
- Lineage csv: [figures/17-8/lineage/lineage.csv](figures/17-8/lineage/lineage.csv)

### Figure 19-1 - Nuclear weapons, 1945-2015

Status: `partial_match`. Artifact kind: `reconstruction`.

- Original reference: [references/figures/figure_19_1.png](references/figures/figure_19_1.png)
- Book period reconstruction: [figures/19-1/plots/book_period/figure_19_1_book_period_reconstruction.png](figures/19-1/plots/book_period/figure_19_1_book_period_reconstruction.png)
- Extended reconstruction: [figures/19-1/plots/book_period/figure_19_1_book_period_reconstruction.png](figures/19-1/plots/book_period/figure_19_1_book_period_reconstruction.png)
- Book period comparison: [figures/19-1/plots/comparisons/figure_19_1_book_period_review.png](figures/19-1/plots/comparisons/figure_19_1_book_period_review.png)
- Extended comparison: [figures/19-1/plots/comparisons/figure_19_1_extended_review.png](figures/19-1/plots/comparisons/figure_19_1_extended_review.png)
- Caption: [figures/19-1/captions/caption.txt](figures/19-1/captions/caption.txt)
- Provenance: [figures/19-1/provenance/provenance.md](figures/19-1/provenance/provenance.md)
- Anomaly review: [figures/19-1/anomaly_reviews/anomaly_review.md](figures/19-1/anomaly_reviews/anomaly_review.md)
- Review checklist: [figures/19-1/review_checklist.md](figures/19-1/review_checklist.md)
- Source log: [figures/19-1/source_logs/source_log.md](figures/19-1/source_logs/source_log.md)
- Search log: [figures/19-1/search_iterations/search_iterations.md](figures/19-1/search_iterations/search_iterations.md)
- Discrepancy log: [figures/19-1/discrepancy_logs/discrepancy_log.md](figures/19-1/discrepancy_logs/discrepancy_log.md)
- Legacy metadata: [figures/19-1/metadata/metadata.json](figures/19-1/metadata/metadata.json)
- Metadata: [figures/19-1/figure.json](figures/19-1/figure.json)

