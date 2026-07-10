# Provenance Summary: Figure 10-5

- Best-current reconstruction: spill counts only, plotted on the book axes.
- Candidate diagnostic: current UNCTADStat `US.SeaborneTrade` bulk file, explicitly labeled "From 2000 to 2024".
- Why separated: the current UNCTAD bulk file does not cover 1970-1999 and its World cargo 11+12 values do not match the RMT/book tanker-trade scale on overlapping selected years.
- Status: partial_match.
- Source fidelity: B/C. Spill-count source is an exact-publication candidate; oil-shipping source remains unrecovered.
- Regeneration command: `/Users/alfred/Documents/MIsc/.venv/bin/python scripts/reconstruct_10_5_source_recovery.py`.

## Targeted Source-Recovery Update
- Date: 2026-07-09
- Confirmed the book source line and definition from the available figure/page evidence: Roser 2016r based on updated ITOPF data; oil shipped consists of total crude oil, petroleum product, and gas loaded.
- Recovered live UNCTADStat metadata for `US.SeaborneTrade`: title `World seaborne trade by type of cargo, annual (analytical)` and publication date `2026-03-17T15:55:00`.
- Recovered live UNCTADStat bulk-file metadata: one public file, `US_SeaborneTrade`, labeled `From 2000 to 2024`.
- Downloaded `https://unctadstat-api.unctad.org/bulkdownload/US.SeaborneTrade/US_SeaborneTrade`; response header names `US_SeaborneTrade.csv.7z`. Extracted CSV is saved as `figures/10-5/data/candidates/unctad_us_seaborne_trade_bulk_2000_2024.csv`.
- Rejected the current bulk file as a book-line substitute. The 2000 and 2016 World cargo 11+12 sums are 2.983940 and 4.085502 billion tons, while RMT 2020 selected-year tanker-trade values are 2.163 and 3.058 billion tons. Overlap differences are documented in `figures/10-5/data/candidates/unctad_current_bulk_vs_rmt_scale_check.csv`.
- The previously referenced `US.SeaborneTrade_585_20231104_101924.csv` remains a useful public clue from a 2023 reproduction article, but this run did not recover that file or any archived equivalent. Current UNCTAD metadata endpoints reject version `585` as an invalid report/version combination.
- Because the annual 1970-2016 oil-shipped-by-sea source is not recovered, the regenerated book-period and extended figures intentionally do not plot that series.

## Research Mode Provenance Update
- Added `data/candidates/unctad_rmt2020_tanker_trade_selected_years.csv`.
- Added `outputs/diagnostics/figure_10_5_rmt_tanker_trade_selected_years_diagnostic.png`.
- RMT selected-year values are diagnostic evidence only and are not used in the side-by-side validation plot.

## Book-Style Reconstruction Update
- Date: 2026-06-28
- Superseded by the 2026-07-09 targeted source-recovery update above.
- The earlier book-style outputs plotted an annual UNCTADStat-style mirror that is not present as a recoverable checked-in source in this repository. This run therefore replaced the main artifacts with a more conservative spill-count-only partial reconstruction and documented the unresolved oil-shipping source explicitly.
