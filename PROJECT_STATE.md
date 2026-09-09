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
Historical classifications are retained as claims until independently re-reviewed.
A completed source search or accepted worker run is not a completed reconstruction.

## Reference And Review

- [Supplemental Graphics PDF](references/enlightenment_now_supplemental_graphics.pdf)
- [Registry](data/figure_registry.csv) and [JSON mirror](data/figure_registry.json)
- [Workflow](docs/workflow.md), [research review](docs/review_protocol.md), [editorial gate](docs/editorial_review_gate.md)
- [Canonical artifact index](data/canonical_artifacts.json)

Every future figure run must inspect and display actual book-period and extended
comparisons where available. Record exact inspected hashes and unresolved issues.
Do not digitize plotted values for reconstruction or promote weak source matches.
Update the canonical record and regenerate its views whenever an artifact changes.

## Scientific Inventory

| Status | Count |
| --- | ---: |
| blocked_external_source | 1 |
| manual_review_needed | 4 |
| not_started | 40 |
| partial_match | 11 |
| source_chain_recovered | 2 |
| source_unavailable | 1 |
| updated_equivalent | 7 |
| verified_reproduction | 9 |

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
| 11-1 | Great power war, 1500-2015 | not_started | not_started | incomplete |
| 11-2 | Battle deaths, 1946-2016 | not_started | not_started | incomplete |
| 11-3 | Genocide deaths, 1956-2016 | not_started | not_started | incomplete |
| 12-1 | Homicide deaths, Western Europe, US, and Mexico, 1300-2015 | not_started | not_started | incomplete |
| 12-2 | Homicide deaths, 1967-2015 | not_started | not_started | incomplete |
| 12-3 | Motor vehicle accident deaths, US, 1921-2015 | source_chain_recovered | processed | incomplete |
| 12-4 | Pedestrian deaths, US, 1927-2015 | source_chain_recovered | processed | incomplete |
| 12-5 | Plane crash deaths, 1970-2015 | partial_match | blocked | not_reviewed |
| 12-6 | Deaths from falls, fire, drowning, and poison, US, 1903-2014 | not_started | not_started | incomplete |
| 12-7 | Occupational accident deaths, US, 1913-2015 | not_started | not_started | incomplete |
| 12-8 | Natural disaster deaths, 1900-2015 | updated_equivalent | processed | not_reviewed |
| 12-9 | Lightning strike deaths, US, 1900-2015 | verified_reproduction | processed | not_reviewed |
| 13-1 | Terrorism deaths, 1970-2015 | not_started | not_started | incomplete |
| 14-1 | Democracy versus autocracy, 1800-2015 | not_started | not_started | incomplete |
| 14-2 | Human rights, 1949-2014 | not_started | not_started | incomplete |
| 14-3 | Death penalty abolitions, 1863-2016 | not_started | not_started | incomplete |
| 14-4 | Executions, US, 1780-2016 | not_started | not_started | incomplete |
| 15-1 | Racist, sexist, and homophobic opinions, US, 1987-2012 | not_started | not_started | incomplete |
| 15-2 | Racist, sexist, and homophobic Web searches, US, 2004-2017 | not_started | not_started | incomplete |
| 15-3 | Hate crimes, US, 1996-2015 | not_started | not_started | incomplete |
| 15-4 | Rape and domestic violence, US, 1993-2014 | not_started | not_started | incomplete |
| 15-5 | Decriminalization of homosexuality, 1791-2016 | not_started | not_started | incomplete |
| 15-6 | Liberal values across time and generations, developed countries, 1980-2005 | not_started | not_started | incomplete |
| 15-7 | Liberal values across time (extrapolated), world's culture zones, 1960-2006 | not_started | not_started | incomplete |
| 15-8 | Victimization of children, US, 1993-2012 | not_started | not_started | incomplete |
| 15-9 | Child labor, 1850-2012 | not_started | not_started | incomplete |
| 16-1 | Literacy, 1475-2010 | not_started | not_started | incomplete |
| 16-2 | Basic education, 1820-2010 | not_started | not_started | incomplete |
| 16-3 | Years of schooling, 1870-2010 | not_started | not_started | incomplete |
| 16-4 | Female literacy, 1750-2014 | not_started | not_started | incomplete |
| 16-5 | IQ gains, 1909-2013 | not_started | not_started | incomplete |
| 16-6 | Global well-being, 1820-2015 | not_started | not_started | incomplete |
| 17-1 | Work hours, Western Europe and US, 1870-2000 | not_started | not_started | incomplete |
| 17-2 | Retirement, US, 1880-2010 | not_started | not_started | incomplete |
| 17-3 | Utilities, appliances, and housework, US, 1900-2015 | not_started | not_started | incomplete |
| 17-4 | Cost of light, England, 1300-2006 | not_started | not_started | incomplete |
| 17-5 | Spending on necessities, US, 1929-2016 | not_started | not_started | incomplete |
| 17-6 | Leisure time, US, 1965-2015 | not_started | not_started | incomplete |
| 17-7 | Cost of air travel, US, 1979-2015 | not_started | not_started | incomplete |
| 17-8 | International tourism, 1995-2015 | not_started | not_started | incomplete |
| 18-1 | Life satisfaction and income, 2006 | not_started | not_started | incomplete |
| 18-2 | Loneliness, US students, 1978-2011 | not_started | not_started | incomplete |
| 18-3 | Suicide, England, Switzerland, and US, 1860-2014 | not_started | not_started | incomplete |
| 18-4 | Happiness and excitement, US, 1972-2016 | not_started | not_started | incomplete |
| 19-1 | Nuclear weapons, 1945-2015 | partial_match | blocked | not_reviewed |
| 20-1 | Populist support across generations, 2016 | not_started | not_started | incomplete |

## Canonical Figure Artifacts

### Figure 4-1 - Tone of the news, 1945-2010

Status: `source_unavailable`. Artifact kind: `source_recovery`.

- Original reference: [figures/4-1/plots/comparisons/supplemental_pdf_reference_figure_4_1.png](figures/4-1/plots/comparisons/supplemental_pdf_reference_figure_4_1.png)
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

- Original reference: [figures/5-1/plots/comparisons/kindle_reference_figure_5_1.png](figures/5-1/plots/comparisons/kindle_reference_figure_5_1.png)
- Book period reconstruction: [figures/5-1/plots/book_period/figure_5_1_book_period_reconstruction.png](figures/5-1/plots/book_period/figure_5_1_book_period_reconstruction.png)
- Extended reconstruction: [figures/5-1/plots/extended/figure_5_1_extended_reconstruction.png](figures/5-1/plots/extended/figure_5_1_extended_reconstruction.png)
- Book period comparison: [figures/5-1/plots/comparisons/figure_5_1_book_period_comparison.png](figures/5-1/plots/comparisons/figure_5_1_book_period_comparison.png)
- Extended comparison: [figures/5-1/plots/comparisons/figure_5_1_extended_comparison.png](figures/5-1/plots/comparisons/figure_5_1_extended_comparison.png)
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

- Original reference: [figures/5-2/plots/comparisons/kindle_reference_figure_5_2.png](figures/5-2/plots/comparisons/kindle_reference_figure_5_2.png)
- Book period reconstruction: [figures/5-2/plots/book_period/figure_5_2_book_period_reconstruction.png](figures/5-2/plots/book_period/figure_5_2_book_period_reconstruction.png)
- Extended reconstruction: [figures/5-2/plots/extended/figure_5_2_extended_reconstruction.png](figures/5-2/plots/extended/figure_5_2_extended_reconstruction.png)
- Book period comparison: [figures/5-2/plots/comparisons/figure_5_2_book_period_comparison.png](figures/5-2/plots/comparisons/figure_5_2_book_period_comparison.png)
- Extended comparison: [figures/5-2/plots/comparisons/figure_5_2_extended_comparison.png](figures/5-2/plots/comparisons/figure_5_2_extended_comparison.png)
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

- Original reference: [figures/5-3/plots/comparisons/kindle_reference_figure_5_3.png](figures/5-3/plots/comparisons/kindle_reference_figure_5_3.png)
- Book period reconstruction: [figures/5-3/plots/book_period/figure_5_3_book_period_reconstruction.png](figures/5-3/plots/book_period/figure_5_3_book_period_reconstruction.png)
- Extended reconstruction: [figures/5-3/plots/extended/figure_5_3_same_source_continuation.png](figures/5-3/plots/extended/figure_5_3_same_source_continuation.png)
- Book period comparison: [figures/5-3/plots/comparisons/figure_5_3_book_period_comparison.png](figures/5-3/plots/comparisons/figure_5_3_book_period_comparison.png)
- Extended comparison: [figures/5-3/plots/comparisons/figure_5_3_extended_comparison.png](figures/5-3/plots/comparisons/figure_5_3_extended_comparison.png)
- Caption: [figures/5-3/captions/caption.txt](figures/5-3/captions/caption.txt)
- Provenance: [figures/5-3/provenance/provenance.md](figures/5-3/provenance/provenance.md)
- Anomaly review: [figures/5-3/anomaly_reviews/anomaly_review.md](figures/5-3/anomaly_reviews/anomaly_review.md)
- Review checklist: [figures/5-3/review_checklist.md](figures/5-3/review_checklist.md)
- Source log: [figures/5-3/source_logs/source_log.md](figures/5-3/source_logs/source_log.md)
- Search log: [figures/5-3/search_iterations/search_iterations.md](figures/5-3/search_iterations/search_iterations.md)
- Discrepancy log: [figures/5-3/discrepancy_logs/discrepancy_log.md](figures/5-3/discrepancy_logs/discrepancy_log.md)
- Legacy metadata: [figures/5-3/metadata/metadata.json](figures/5-3/metadata/metadata.json)
- Metadata: [figures/5-3/figure.json](figures/5-3/figure.json)

### Figure 5-4 - Life expectancy, UK, 1701-2013

Status: `partial_match`. Artifact kind: `source_recovery`.

- Original reference: [figures/5-4/plots/comparisons/supplemental_pdf_reference_figure_5_4.png](figures/5-4/plots/comparisons/supplemental_pdf_reference_figure_5_4.png)
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

- Original reference: [figures/6-1/plots/comparisons/kindle_reference_figure_6_1.png](figures/6-1/plots/comparisons/kindle_reference_figure_6_1.png)
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

- Original reference: [figures/7-1/plots/comparisons/kindle_reference_figure_7_1.png](figures/7-1/plots/comparisons/kindle_reference_figure_7_1.png)
- Book period reconstruction: [figures/7-1/plots/book_period/figure_7_1_book_period_reconstruction.png](figures/7-1/plots/book_period/figure_7_1_book_period_reconstruction.png)
- Extended reconstruction: [figures/7-1/plots/extended/figure_7_1_extended_reconstruction.png](figures/7-1/plots/extended/figure_7_1_extended_reconstruction.png)
- Book period comparison: [figures/7-1/plots/comparisons/figure_7_1_book_period_comparison.png](figures/7-1/plots/comparisons/figure_7_1_book_period_comparison.png)
- Extended comparison: [figures/7-1/plots/comparisons/figure_7_1_extended_comparison.png](figures/7-1/plots/comparisons/figure_7_1_extended_comparison.png)
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

- Original reference: [figures/7-2/plots/comparisons/kindle_reference_figure_7_2.png](figures/7-2/plots/comparisons/kindle_reference_figure_7_2.png)
- Book period reconstruction: [figures/7-2/plots/book_period/figure_7_2_book_period_reconstruction.png](figures/7-2/plots/book_period/figure_7_2_book_period_reconstruction.png)
- Extended reconstruction: [figures/7-2/plots/extended/figure_7_2_extended_reconstruction.png](figures/7-2/plots/extended/figure_7_2_extended_reconstruction.png)
- Book period comparison: [figures/7-2/plots/comparisons/figure_7_2_book_period_comparison.png](figures/7-2/plots/comparisons/figure_7_2_book_period_comparison.png)
- Extended comparison: [figures/7-2/plots/comparisons/figure_7_2_extended_comparison.png](figures/7-2/plots/comparisons/figure_7_2_extended_comparison.png)
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

- Original reference: [figures/7-3/plots/comparisons/supplemental_pdf_reference_figure_7_3.png](figures/7-3/plots/comparisons/supplemental_pdf_reference_figure_7_3.png)
- Book period reconstruction: [figures/7-3/plots/book_period/figure_7_3_book_period_reconstruction.png](figures/7-3/plots/book_period/figure_7_3_book_period_reconstruction.png)
- Extended reconstruction: [figures/7-3/plots/extended/figure_7_3_extended_reconstruction.png](figures/7-3/plots/extended/figure_7_3_extended_reconstruction.png)
- Book period comparison: [figures/7-3/plots/comparisons/figure_7_3_book_period_comparison.png](figures/7-3/plots/comparisons/figure_7_3_book_period_comparison.png)
- Extended comparison: [figures/7-3/plots/comparisons/figure_7_3_extended_comparison.png](figures/7-3/plots/comparisons/figure_7_3_extended_comparison.png)
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

- Original reference: [figures/7-4/plots/comparisons/kindle_reference_figure_7_4.png](figures/7-4/plots/comparisons/kindle_reference_figure_7_4.png)
- Book period reconstruction: [figures/7-4/plots/book_period/figure_7_4_book_period_reconstruction.png](figures/7-4/plots/book_period/figure_7_4_book_period_reconstruction.png)
- Extended reconstruction: [figures/7-4/plots/extended/figure_7_4_extended_reconstruction.png](figures/7-4/plots/extended/figure_7_4_extended_reconstruction.png)
- Book period comparison: [figures/7-4/plots/comparisons/figure_7_4_book_period_comparison.png](figures/7-4/plots/comparisons/figure_7_4_book_period_comparison.png)
- Extended comparison: [figures/7-4/plots/comparisons/figure_7_4_extended_comparison.png](figures/7-4/plots/comparisons/figure_7_4_extended_comparison.png)
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

- Original reference: [figures/8-1/plots/comparisons/kindle_reference_figure_8_1.png](figures/8-1/plots/comparisons/kindle_reference_figure_8_1.png)
- Book period reconstruction: [figures/8-1/plots/book_period/figure_8_1_book_period_reconstruction.png](figures/8-1/plots/book_period/figure_8_1_book_period_reconstruction.png)
- Extended reconstruction: [figures/8-1/plots/extended/figure_8_1_extended_reconstruction.png](figures/8-1/plots/extended/figure_8_1_extended_reconstruction.png)
- Book period comparison: [figures/8-1/plots/comparisons/figure_8_1_book_period_comparison.png](figures/8-1/plots/comparisons/figure_8_1_book_period_comparison.png)
- Extended comparison: [figures/8-1/plots/comparisons/figure_8_1_extended_comparison.png](figures/8-1/plots/comparisons/figure_8_1_extended_comparison.png)
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

- Original reference: [figures/8-2/plots/comparisons/kindle_reference_figure_8_2.png](figures/8-2/plots/comparisons/kindle_reference_figure_8_2.png)
- Book period reconstruction: [figures/8-2/plots/book_period/figure_8_2_book_period_reconstruction.png](figures/8-2/plots/book_period/figure_8_2_book_period_reconstruction.png)
- Extended reconstruction: [figures/8-2/plots/extended/figure_8_2_extended_reconstruction.png](figures/8-2/plots/extended/figure_8_2_extended_reconstruction.png)
- Book period comparison: [figures/8-2/plots/comparisons/figure_8_2_book_period_comparison.png](figures/8-2/plots/comparisons/figure_8_2_book_period_comparison.png)
- Extended comparison: [figures/8-2/plots/comparisons/figure_8_2_extended_comparison.png](figures/8-2/plots/comparisons/figure_8_2_extended_comparison.png)
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

- Original reference: [figures/8-3/plots/comparisons/kindle_reference_figure_8_3.png](figures/8-3/plots/comparisons/kindle_reference_figure_8_3.png)
- Book period reconstruction: [figures/8-3/plots/book_period/figure_8_3_book_period_reconstruction.png](figures/8-3/plots/book_period/figure_8_3_book_period_reconstruction.png)
- Extended reconstruction: [figures/8-3/plots/extended/figure_8_3_extended_reconstruction.png](figures/8-3/plots/extended/figure_8_3_extended_reconstruction.png)
- Book period comparison: [figures/8-3/plots/comparisons/figure_8_3_book_period_comparison.png](figures/8-3/plots/comparisons/figure_8_3_book_period_comparison.png)
- Extended comparison: [figures/8-3/plots/comparisons/figure_8_3_extended_comparison.png](figures/8-3/plots/comparisons/figure_8_3_extended_comparison.png)
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

- Original reference: [figures/8-4/plots/comparisons/kindle_reference_figure_8_4.png](figures/8-4/plots/comparisons/kindle_reference_figure_8_4.png)
- Book period reconstruction: [figures/8-4/plots/book_period/figure_8_4_book_period_reconstruction.png](figures/8-4/plots/book_period/figure_8_4_book_period_reconstruction.png)
- Extended reconstruction: [figures/8-4/plots/extended/figure_8_4_extended_reconstruction.png](figures/8-4/plots/extended/figure_8_4_extended_reconstruction.png)
- Book period comparison: [figures/8-4/plots/comparisons/figure_8_4_book_period_comparison.png](figures/8-4/plots/comparisons/figure_8_4_book_period_comparison.png)
- Extended comparison: [figures/8-4/plots/comparisons/figure_8_4_extended_comparison.png](figures/8-4/plots/comparisons/figure_8_4_extended_comparison.png)
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

- Original reference: [figures/8-5/plots/comparisons/kindle_reference_figure_8_5.png](figures/8-5/plots/comparisons/kindle_reference_figure_8_5.png)
- Book period reconstruction: [figures/8-5/plots/book_period/figure_8_5_book_period_reconstruction.png](figures/8-5/plots/book_period/figure_8_5_book_period_reconstruction.png)
- Extended reconstruction: [figures/8-5/plots/extended/figure_8_5_extended_reconstruction.png](figures/8-5/plots/extended/figure_8_5_extended_reconstruction.png)
- Book period comparison: [figures/8-5/plots/comparisons/figure_8_5_book_period_comparison.png](figures/8-5/plots/comparisons/figure_8_5_book_period_comparison.png)
- Extended comparison: [figures/8-5/plots/comparisons/figure_8_5_extended_comparison.png](figures/8-5/plots/comparisons/figure_8_5_extended_comparison.png)
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

- Original reference: [figures/9-1/plots/comparisons/supplemental_pdf_reference_figure_9_1.png](figures/9-1/plots/comparisons/supplemental_pdf_reference_figure_9_1.png)
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

- Original reference: [figures/9-2/plots/comparisons/supplemental_pdf_page_10_figure_9_2.png](figures/9-2/plots/comparisons/supplemental_pdf_page_10_figure_9_2.png)
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

- Original reference: [figures/9-3/plots/comparisons/supplemental_pdf_reference_figure_9_3.png](figures/9-3/plots/comparisons/supplemental_pdf_reference_figure_9_3.png)
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

- Original reference: [figures/9-4/plots/comparisons/kindle_reference_figure_9_4.png](figures/9-4/plots/comparisons/kindle_reference_figure_9_4.png)
- Book period reconstruction: [figures/9-4/plots/book_period/figure_9_4_book_period_reconstruction.png](figures/9-4/plots/book_period/figure_9_4_book_period_reconstruction.png)
- Extended reconstruction: [figures/9-4/plots/extended/figure_9_4_extended_reconstruction.png](figures/9-4/plots/extended/figure_9_4_extended_reconstruction.png)
- Book period comparison: [figures/9-4/plots/comparisons/figure_9_4_book_period_comparison.png](figures/9-4/plots/comparisons/figure_9_4_book_period_comparison.png)
- Extended comparison: [figures/9-4/plots/comparisons/figure_9_4_extended_comparison.png](figures/9-4/plots/comparisons/figure_9_4_extended_comparison.png)
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

- Original reference: [figures/9-5/plots/comparisons/supplemental_pdf_reference_figure_9_5.png](figures/9-5/plots/comparisons/supplemental_pdf_reference_figure_9_5.png)
- Book period reconstruction: [figures/9-5/plots/book_period/figure_9_5_book_period_reconstruction.png](figures/9-5/plots/book_period/figure_9_5_book_period_reconstruction.png)
- Extended reconstruction: [figures/9-5/plots/extended/figure_9_5_extended_reconstruction.png](figures/9-5/plots/extended/figure_9_5_extended_reconstruction.png)
- Book period comparison: [figures/9-5/plots/comparisons/figure_9_5_book_period_comparison.png](figures/9-5/plots/comparisons/figure_9_5_book_period_comparison.png)
- Extended comparison: [figures/9-5/plots/comparisons/figure_9_5_extended_comparison.png](figures/9-5/plots/comparisons/figure_9_5_extended_comparison.png)
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

- Original reference: [figures/9-6/plots/comparisons/pdf_reference_figure_9_6.png](figures/9-6/plots/comparisons/pdf_reference_figure_9_6.png)
- Book period reconstruction: [figures/9-6/plots/book_period/figure_9_6_book_period_reconstruction.png](figures/9-6/plots/book_period/figure_9_6_book_period_reconstruction.png)
- Extended reconstruction: [figures/9-6/plots/extended/figure_9_6_extended_reconstruction.png](figures/9-6/plots/extended/figure_9_6_extended_reconstruction.png)
- Book period comparison: [figures/9-6/plots/comparisons/figure_9_6_book_period_comparison.png](figures/9-6/plots/comparisons/figure_9_6_book_period_comparison.png)
- Extended comparison: [figures/9-6/plots/comparisons/figure_9_6_extended_comparison.png](figures/9-6/plots/comparisons/figure_9_6_extended_comparison.png)
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

- Original reference: [figures/10-1/plots/comparisons/pdf_reference_figure_10_1.png](figures/10-1/plots/comparisons/pdf_reference_figure_10_1.png)
- Book period reconstruction: [figures/10-1/plots/book_period/figure_10_1_book_period_reconstruction.png](figures/10-1/plots/book_period/figure_10_1_book_period_reconstruction.png)
- Extended reconstruction: [figures/10-1/plots/extended/figure_10_1_extended_reconstruction.png](figures/10-1/plots/extended/figure_10_1_extended_reconstruction.png)
- Book period comparison: [figures/10-1/plots/comparisons/figure_10_1_book_period_comparison.png](figures/10-1/plots/comparisons/figure_10_1_book_period_comparison.png)
- Extended comparison: [figures/10-1/plots/comparisons/figure_10_1_extended_comparison.png](figures/10-1/plots/comparisons/figure_10_1_extended_comparison.png)
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

- Original reference: [figures/10-2/plots/comparisons/pdf_reference_figure_10_2.png](figures/10-2/plots/comparisons/pdf_reference_figure_10_2.png)
- Book period reconstruction: [figures/10-2/plots/book_period/figure_10_2_book_period_reconstruction.png](figures/10-2/plots/book_period/figure_10_2_book_period_reconstruction.png)
- Extended reconstruction: [figures/10-2/plots/extended/figure_10_2_extended_reconstruction.png](figures/10-2/plots/extended/figure_10_2_extended_reconstruction.png)
- Book period comparison: [figures/10-2/plots/comparisons/figure_10_2_book_period_comparison.png](figures/10-2/plots/comparisons/figure_10_2_book_period_comparison.png)
- Extended comparison: [figures/10-2/plots/comparisons/figure_10_2_extended_comparison.png](figures/10-2/plots/comparisons/figure_10_2_extended_comparison.png)
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

- Original reference: [figures/10-3/plots/comparisons/pdf_reference_figure_10_3.png](figures/10-3/plots/comparisons/pdf_reference_figure_10_3.png)
- Book period reconstruction: [figures/10-3/plots/book_period/figure_10_3_book_period_reconstruction.png](figures/10-3/plots/book_period/figure_10_3_book_period_reconstruction.png)
- Extended reconstruction: [figures/10-3/plots/extended/figure_10_3_extended_reconstruction.png](figures/10-3/plots/extended/figure_10_3_extended_reconstruction.png)
- Book period comparison: [figures/10-3/plots/comparisons/figure_10_3_book_period_comparison.png](figures/10-3/plots/comparisons/figure_10_3_book_period_comparison.png)
- Extended comparison: [figures/10-3/plots/comparisons/figure_10_3_extended_comparison.png](figures/10-3/plots/comparisons/figure_10_3_extended_comparison.png)
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

- Original reference: [figures/10-4/plots/comparisons/supplemental_pdf_reference_figure_10_4.png](figures/10-4/plots/comparisons/supplemental_pdf_reference_figure_10_4.png)
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

- Original reference: [figures/10-5/plots/comparisons/corrected_figure_10_5_book_crop.png](figures/10-5/plots/comparisons/corrected_figure_10_5_book_crop.png)
- Book period reconstruction: [figures/10-5/plots/book_period/figure_10_5_book_period_reconstruction.png](figures/10-5/plots/book_period/figure_10_5_book_period_reconstruction.png)
- Extended reconstruction: [figures/10-5/plots/extended/figure_10_5_extended_reconstruction.png](figures/10-5/plots/extended/figure_10_5_extended_reconstruction.png)
- Book period comparison: [figures/10-5/plots/comparisons/figure_10_5_book_style_comparison_captioned.png](figures/10-5/plots/comparisons/figure_10_5_book_style_comparison_captioned.png)
- Extended comparison: [figures/10-5/plots/comparisons/figure_10_5_extended_comparison_captioned.png](figures/10-5/plots/comparisons/figure_10_5_extended_comparison_captioned.png)
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

- Original reference: [figures/10-6/plots/comparisons/corrected_figure_10_6_book_crop.png](figures/10-6/plots/comparisons/corrected_figure_10_6_book_crop.png)
- Book period reconstruction: [figures/10-6/plots/book_period/figure_10_6_book_period_reconstruction.png](figures/10-6/plots/book_period/figure_10_6_book_period_reconstruction.png)
- Extended reconstruction: [figures/10-6/plots/extended/figure_10_6_extended_reconstruction.png](figures/10-6/plots/extended/figure_10_6_extended_reconstruction.png)
- Book period comparison: [figures/10-6/plots/comparisons/figure_10_6_book_style_comparison_captioned.png](figures/10-6/plots/comparisons/figure_10_6_book_style_comparison_captioned.png)
- Extended comparison: [figures/10-6/plots/comparisons/figure_10_6_extended_comparison_captioned.png](figures/10-6/plots/comparisons/figure_10_6_extended_comparison_captioned.png)
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

- Original reference: [figures/10-7/plots/comparisons/kindle_reference_figure_10_7.png](figures/10-7/plots/comparisons/kindle_reference_figure_10_7.png)
- Book period reconstruction: [figures/10-7/plots/book_period/figure_10_7_book_period_reconstruction.png](figures/10-7/plots/book_period/figure_10_7_book_period_reconstruction.png)
- Extended reconstruction: [figures/10-7/plots/extended/figure_10_7_extended_reconstruction.png](figures/10-7/plots/extended/figure_10_7_extended_reconstruction.png)
- Book period comparison: [figures/10-7/plots/comparisons/figure_10_7_book_period_comparison.png](figures/10-7/plots/comparisons/figure_10_7_book_period_comparison.png)
- Extended comparison: [figures/10-7/plots/comparisons/figure_10_7_extended_comparison.png](figures/10-7/plots/comparisons/figure_10_7_extended_comparison.png)
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

- Original reference: [figures/10-8/plots/comparisons/kindle_reference_figure_10_8.png](figures/10-8/plots/comparisons/kindle_reference_figure_10_8.png)
- Book period reconstruction: [figures/10-8/plots/book_period/figure_10_8_book_period_reconstruction.png](figures/10-8/plots/book_period/figure_10_8_book_period_reconstruction.png)
- Extended reconstruction: [figures/10-8/plots/extended/figure_10_8_extended_reconstruction.png](figures/10-8/plots/extended/figure_10_8_extended_reconstruction.png)
- Book period comparison: [figures/10-8/plots/comparisons/figure_10_8_book_period_comparison.png](figures/10-8/plots/comparisons/figure_10_8_book_period_comparison.png)
- Extended comparison: [figures/10-8/plots/comparisons/figure_10_8_extended_comparison.png](figures/10-8/plots/comparisons/figure_10_8_extended_comparison.png)
- Caption: [figures/10-8/captions/caption.txt](figures/10-8/captions/caption.txt)
- Provenance: [figures/10-8/provenance/provenance.md](figures/10-8/provenance/provenance.md)
- Anomaly review: [figures/10-8/anomaly_reviews/anomaly_review.md](figures/10-8/anomaly_reviews/anomaly_review.md)
- Review checklist: [figures/10-8/review_checklist.md](figures/10-8/review_checklist.md)
- Source log: [figures/10-8/source_logs/source_log.md](figures/10-8/source_logs/source_log.md)
- Search log: [figures/10-8/search_iterations/search_iterations.md](figures/10-8/search_iterations/search_iterations.md)
- Discrepancy log: [figures/10-8/discrepancy_logs/discrepancy_log.md](figures/10-8/discrepancy_logs/discrepancy_log.md)
- Legacy metadata: [figures/10-8/metadata/metadata.json](figures/10-8/metadata/metadata.json)
- Metadata: [figures/10-8/figure.json](figures/10-8/figure.json)

### Figure 12-3 - Motor vehicle accident deaths, US, 1921-2015

Status: `source_chain_recovered`. Artifact kind: `source_recovery`.

- Original reference: [figures/12-3/plots/comparisons/kindle_reference_figure_12_3.png](figures/12-3/plots/comparisons/kindle_reference_figure_12_3.png)
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

- Original reference: [figures/12-4/plots/comparisons/kindle_reference_figure_12_4.png](figures/12-4/plots/comparisons/kindle_reference_figure_12_4.png)
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

- Original reference: [figures/12-5/plots/comparisons/supplemental_pdf_reference_figure_12_5.png](figures/12-5/plots/comparisons/supplemental_pdf_reference_figure_12_5.png)
- Book period reconstruction: [figures/12-5/plots/book_period/figure_12_5_book_period_reconstruction.png](figures/12-5/plots/book_period/figure_12_5_book_period_reconstruction.png)
- Extended reconstruction: [figures/12-5/plots/extended/figure_12_5_extended_reconstruction.png](figures/12-5/plots/extended/figure_12_5_extended_reconstruction.png)
- Book period comparison: [figures/12-5/plots/comparisons/figure_12_5_book_period_comparison.png](figures/12-5/plots/comparisons/figure_12_5_book_period_comparison.png)
- Extended comparison: [figures/12-5/plots/comparisons/figure_12_5_extended_comparison.png](figures/12-5/plots/comparisons/figure_12_5_extended_comparison.png)
- Caption: [figures/12-5/captions/caption.txt](figures/12-5/captions/caption.txt)
- Provenance: [figures/12-5/provenance/provenance.md](figures/12-5/provenance/provenance.md)
- Anomaly review: [figures/12-5/anomaly_reviews/anomaly_review.md](figures/12-5/anomaly_reviews/anomaly_review.md)
- Review checklist: [figures/12-5/review_checklist.md](figures/12-5/review_checklist.md)
- Source log: [figures/12-5/source_logs/source_log.md](figures/12-5/source_logs/source_log.md)
- Search log: [figures/12-5/search_iterations/search_iterations.md](figures/12-5/search_iterations/search_iterations.md)
- Discrepancy log: [figures/12-5/discrepancy_logs/discrepancy_log.md](figures/12-5/discrepancy_logs/discrepancy_log.md)
- Legacy metadata: [figures/12-5/metadata/metadata.json](figures/12-5/metadata/metadata.json)
- Metadata: [figures/12-5/figure.json](figures/12-5/figure.json)

### Figure 12-8 - Natural disaster deaths, 1900-2015

Status: `updated_equivalent`. Artifact kind: `reconstruction`.

- Original reference: [figures/12-8/plots/comparisons/kindle_reference_figure_12_8.png](figures/12-8/plots/comparisons/kindle_reference_figure_12_8.png)
- Book period reconstruction: [figures/12-8/plots/book_period/figure_12_8_book_period_reconstruction.png](figures/12-8/plots/book_period/figure_12_8_book_period_reconstruction.png)
- Extended reconstruction: [figures/12-8/plots/extended/figure_12_8_extended_reconstruction.png](figures/12-8/plots/extended/figure_12_8_extended_reconstruction.png)
- Book period comparison: [figures/12-8/plots/comparisons/figure_12_8_book_period_comparison.png](figures/12-8/plots/comparisons/figure_12_8_book_period_comparison.png)
- Extended comparison: [figures/12-8/plots/comparisons/figure_12_8_extended_comparison.png](figures/12-8/plots/comparisons/figure_12_8_extended_comparison.png)
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

- Original reference: [figures/12-9/plots/comparisons/kindle_reference_figure_12_9.png](figures/12-9/plots/comparisons/kindle_reference_figure_12_9.png)
- Book period reconstruction: [figures/12-9/plots/book_period/figure_12_9_book_period_reconstruction.png](figures/12-9/plots/book_period/figure_12_9_book_period_reconstruction.png)
- Extended reconstruction: [figures/12-9/plots/extended/figure_12_9_extended_reconstruction.png](figures/12-9/plots/extended/figure_12_9_extended_reconstruction.png)
- Book period comparison: [figures/12-9/plots/comparisons/figure_12_9_book_period_comparison.png](figures/12-9/plots/comparisons/figure_12_9_book_period_comparison.png)
- Extended comparison: [figures/12-9/plots/comparisons/figure_12_9_extended_comparison.png](figures/12-9/plots/comparisons/figure_12_9_extended_comparison.png)
- Caption: [figures/12-9/captions/caption.txt](figures/12-9/captions/caption.txt)
- Provenance: [figures/12-9/provenance/provenance.md](figures/12-9/provenance/provenance.md)
- Anomaly review: [figures/12-9/anomaly_reviews/anomaly_review.md](figures/12-9/anomaly_reviews/anomaly_review.md)
- Review checklist: [figures/12-9/review_checklist.md](figures/12-9/review_checklist.md)
- Source log: [figures/12-9/source_logs/source_log.md](figures/12-9/source_logs/source_log.md)
- Search log: [figures/12-9/search_iterations/search_iterations.md](figures/12-9/search_iterations/search_iterations.md)
- Discrepancy log: [figures/12-9/discrepancy_logs/discrepancy_log.md](figures/12-9/discrepancy_logs/discrepancy_log.md)
- Legacy metadata: [figures/12-9/metadata/metadata.json](figures/12-9/metadata/metadata.json)
- Metadata: [figures/12-9/figure.json](figures/12-9/figure.json)

### Figure 19-1 - Nuclear weapons, 1945-2015

Status: `partial_match`. Artifact kind: `reconstruction`.

- Original reference: [figures/19-1/plots/comparisons/kindle_reference_figure_19_1.png](figures/19-1/plots/comparisons/kindle_reference_figure_19_1.png)
- Book period reconstruction: [figures/19-1/plots/book_period/figure_19_1_book_period_reconstruction.png](figures/19-1/plots/book_period/figure_19_1_book_period_reconstruction.png)
- Extended reconstruction: [figures/19-1/plots/extended/figure_19_1_extended_reconstruction.png](figures/19-1/plots/extended/figure_19_1_extended_reconstruction.png)
- Book period comparison: [figures/19-1/plots/comparisons/figure_19_1_book_period_comparison.png](figures/19-1/plots/comparisons/figure_19_1_book_period_comparison.png)
- Extended comparison: [figures/19-1/plots/comparisons/figure_19_1_extended_comparison.png](figures/19-1/plots/comparisons/figure_19_1_extended_comparison.png)
- Caption: [figures/19-1/captions/caption.txt](figures/19-1/captions/caption.txt)
- Provenance: [figures/19-1/provenance/provenance.md](figures/19-1/provenance/provenance.md)
- Anomaly review: [figures/19-1/anomaly_reviews/anomaly_review.md](figures/19-1/anomaly_reviews/anomaly_review.md)
- Review checklist: [figures/19-1/review_checklist.md](figures/19-1/review_checklist.md)
- Source log: [figures/19-1/source_logs/source_log.md](figures/19-1/source_logs/source_log.md)
- Search log: [figures/19-1/search_iterations/search_iterations.md](figures/19-1/search_iterations/search_iterations.md)
- Discrepancy log: [figures/19-1/discrepancy_logs/discrepancy_log.md](figures/19-1/discrepancy_logs/discrepancy_log.md)
- Legacy metadata: [figures/19-1/metadata/metadata.json](figures/19-1/metadata/metadata.json)
- Metadata: [figures/19-1/figure.json](figures/19-1/figure.json)

