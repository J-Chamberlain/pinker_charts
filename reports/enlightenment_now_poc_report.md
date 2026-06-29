# Enlightenment Now Figure-Reproduction Pipeline Report

Generated: 2026-06-28

## Design Decisions

- The pipeline now separates source discovery, data download, cleaning, plotting, visual validation, metadata, and lineage outputs.
- Missing legacy data is represented as a provenance/status problem rather than a plotting exception.
- Status values use the hardened vocabulary: verified_reproduction, updated_equivalent, partial_match, source_unavailable, manual_review_needed.
- Visual validation is simple by design: original Kindle reference crops and recreated plots are placed side-by-side, with pixel-level metrics recorded only as rough diagnostics.
- Source logs are written as researcher-facing markdown so another pass can continue discovery without replaying the whole conversation.
- Discovery adapters now record Internet Archive CDX candidates, GitHub repository/code-search probes, World Bank bulk-download probes, and institutional source probes as raw JSON evidence.

## Figure Status Summary

### Figure 10-5: Oil spills, 1970-2016

- Book citation: Source: Our World in Data, Roser 2016r, based on data (updated) from the International Tanker Owners Pollution Federation.
- Reproduction status: partial_match
- Confidence score: 0.58
- Visual validation: acceptable
- Visual metrics: `{"mean_abs_diff": 78.45, "pixel_correlation": -0.0131, "rms_diff": 133.37}`
- Comparison image: `outputs/validation/figure_10_5_comparison.png`
- Source log: `outputs/source_logs/figure_10_5.md`
- Lineage table: `outputs/lineage/figure_lineage.csv` and `outputs/lineage/figure_lineage.json`
- Notes: Spill-count data is available from current OWID/ITOPF sources. The historical UNCTAD oil-shipped-by-sea series remains unresolved.

### Figure 10-6: Protected areas, 1990-2014

- Book citation: Source: World Bank 2016h and 2017, based on data from the United Nations Environment Programme and the World Conservation Monitoring Centre.
- Reproduction status: partial_match
- Confidence score: 0.42
- Visual validation: poor
- Visual metrics: `{"mean_abs_diff": 64.5, "pixel_correlation": -0.0159, "rms_diff": 121.74}`
- Comparison image: `outputs/validation/figure_10_6_comparison.png`
- Source log: `outputs/source_logs/figure_10_6.md`
- Lineage table: `outputs/lineage/figure_lineage.csv` and `outputs/lineage/figure_lineage.json`
- Notes: Modern WDI endpoints locate the right concepts but not the full historical World aggregate used in the book.

## What Must Change Before Chapter-Scale Work

- Promote discovery-adapter candidates into curated source decisions after human review.
- Store archive/perma URLs and file hashes as required fields before any figure can be upgraded to `verified_reproduction`.
- Add a human review checklist for dual-axis charts and charts where modern APIs expose only current snapshots.
- Keep plotting scripts tolerant of missing variables and produce explicit placeholder/partial plots.
- Track exact downloaded file hashes before publication.
