# Repository Bootstrap Review

Date: 2026-06-29

Question: Could another researcher understand the project, reproduce the current
figures, and continue the work without reading the ChatGPT conversation?

Answer: Mostly yes, with known script cleanup still required.

## What Is Now Self-Contained

- Canonical project status in `PROJECT_STATE.md`.
- Research workflow and pipeline documentation in `docs/`.
- Figure-level packages for 10-5 and 10-6.
- Per-figure metadata, provenance, source logs, search iterations, discrepancy
  logs, anomaly reviews, captions, lineage, plots, source data, processed data,
  and checksums.
- Cross-figure bibliography and lineage artifacts.
- Initial Kindle List of Figures extraction.

## Remaining Gaps

- Scripts are imported from the proof of concept and still need
  repository-relative path cleanup before they can serve as polished production
  commands.
- Figure 10-5 remains unresolved because the exact historical oil-shipping
  series has not been proven.
- Figure 10-6 still needs final bibliographic cleanup around the WRI/World Bank
  source chain.
- Visual comparison assets include cropped book-reference material and require
  publication review before use on a public website.

## Validation Performed

- Confirmed all required top-level project documents exist.
- Confirmed both figure directories include the expected review package files.
- Confirmed each figure has book-period, extended, comparison, and diagnostic
  plot directories populated.
- Confirmed no imported file exceeds 95 MB.
- Removed duplicate top-level copies of per-figure data to keep repository size
  reasonable.
