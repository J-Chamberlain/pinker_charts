# Discrepancy Log: Figure 10-5

Accessed: 2026-06-28

## Current Discrepancies

- Missing years: the current public UNCTADStat bulk file for `US.SeaborneTrade` is labeled `From 2000 to 2024`; the book figure requires an annual oil-shipped-by-sea series for 1970-2016.
- Missing exact source version: Roser 2016r / OWID historical figure data was not recovered as an archived CSV.
- Validation policy correction: the main recreated plot excludes the right-side oil-shipping line because the annual 1970-2016 source is unrecovered.
- Diagnostic evidence: UNCTAD RMT selected-year tanker-trade values and current UNCTADStat bulk/API values are retained as source-family evidence only.
- Numeric gap: spill-count series is numeric and reproducible; oil-shipping values before 2000 are unresolved.
- Scale gap: current UNCTADStat World cargo 11+12 values differ from RMT 2020 selected-year tanker trade by roughly 31-48 percent on overlap, so the current bulk file is not a comparable substitute for the book gray line.

## Search Hypotheses Triggered

- The gray series may be UNCTADStat `US.SeaborneTrade` cargo types 11 and 12 summed.
- An old UNCTAD report version or exported CSV may contain 1970-2016.
- OWID/Roser 2016r may have bundled the UNCTAD values in an archived grapher CSV or historical repository commit.
- ITOPF 2017 may have plotted UNCTAD values without publishing the underlying table.

## Research Mode Discrepancy Update
- Improved: historical UNCTAD/RMT selected-year tanker trade evidence now covers the concept back to 1970.
- Improved: RMT selected-year values match the book's right-axis scale better than the live UNCTADStat v2231 cargo-sum candidate.
- Still unresolved: exact annual 1970-2016 oil-shipped-by-sea series behind the original gray line has not been recovered.
- Current best hypothesis: the original gray line used a retired UNCTADStat export/report version or ITOPF/UNCTAD chart data, not a currently public annual API endpoint.

## Targeted 2026-07-09 Update
- Recovered current UNCTADStat metadata and bulk archive for `US.SeaborneTrade`.
- Recovered bulk-file metadata states the public file is `From 2000 to 2024`, confirming that the live public bulk release cannot fill the 1970-1999 gap.
- Current metadata endpoints reject report version `585`; the observed 2023 filename `US.SeaborneTrade_585_20231104_101924.csv` was not recovered from live UNCTAD, web search, or current bulk-file routes.
- Regenerated book-period and extended comparison artifacts now show the verified oil-spill line only and explicitly label the missing oil-shipped-by-sea source.
