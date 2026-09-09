<!-- canonical-state:start -->
# Figure 5-3: Maternal mortality, 1751-2013

Scientific status: `partial_match`. Execution: `accepted`.
Publication: `not_reviewed`. Artifact kind: `reconstruction`.

This generated summary and [figure.json](figure.json) supersede historical status claims below.
A historical verified classification is not a fresh publication review.

- Original reference: [../../references/figures/figure_5_3.png](../../references/figures/figure_5_3.png)
- Book period reconstruction: [plots/book_period/figure_5_3_book_period_reconstruction.png](plots/book_period/figure_5_3_book_period_reconstruction.png)
- Extended reconstruction: [plots/extended/figure_5_3_same_source_continuation.png](plots/extended/figure_5_3_same_source_continuation.png)
- Book period comparison: [plots/comparisons/figure_5_3_book_period_review.png](plots/comparisons/figure_5_3_book_period_review.png)
- Extended comparison: [plots/comparisons/figure_5_3_extended_review.png](plots/comparisons/figure_5_3_extended_review.png)
- Caption: [captions/caption.txt](captions/caption.txt)
- Provenance: [provenance/provenance.md](provenance/provenance.md)
- Anomaly review: [anomaly_reviews/anomaly_review.md](anomaly_reviews/anomaly_review.md)
- Review checklist: [review_checklist.md](review_checklist.md)
- Source log: [source_logs/source_log.md](source_logs/source_log.md)
- Search log: [search_iterations/search_iterations.md](search_iterations/search_iterations.md)
- Discrepancy log: [discrepancy_logs/discrepancy_log.md](discrepancy_logs/discrepancy_log.md)
- Legacy metadata: [metadata/metadata.json](metadata/metadata.json)
- Metadata: [figure.json](figure.json)
- Source validation: [provenance/early_sweden_validation.json](provenance/early_sweden_validation.json)
- Reconstruction script: [../../scripts/reconstruct_5_3.py](../../scripts/reconstruct_5_3.py)
- Book period clean: [data/clean/figure_5_3_book_period_clean.csv](data/clean/figure_5_3_book_period_clean.csv)
- Extended clean: [data/clean/figure_5_3_same_source_continuation_clean.csv](data/clean/figure_5_3_same_source_continuation_clean.csv)
- Original source table: [data/raw/gapminder_gd010_gapdata010.xls](data/raw/gapminder_gd010_gapdata010.xls)
- Preserved source table: [data/raw/owid_522_maternal_mortality.tab](data/raw/owid_522_maternal_mortality.tab)
- Lineage: [lineage/consolidated_lineage.json](lineage/consolidated_lineage.json)

<!-- canonical-state:end -->

# Figure 5-3: Maternal mortality, 1751-2013

Status: `partial_match` -- strong book-period data reconstruction (exact conversion validation); visual comparison uses a disclosed facsimile reference, not original book pixels.

The reconstruction uses the preserved Our World in Data dataset 522, which
combines Gapminder's 2010 historical compilation with World Bank 2015 values
without adjustment. The supplemental PDF was located through its indexed
College Sidekick record, but its original pixels could not be downloaded in
this run because the host returned a Cloudflare denial. The reference image in
this package is therefore explicitly labeled as an evidence-based facsimile,
not an original page capture.

Run with:

```sh
PYTHONPATH=tmp/pydeps python3 scripts/reconstruct_5_3.py
```

The script assumes `matplotlib` and `Pillow` are available. It never uses
digitized chart values.
