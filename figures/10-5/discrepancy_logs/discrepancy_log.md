# Discrepancy Log: Figure 10-5

Accessed: 2026-06-28

## Current Discrepancies

- Missing years: oil-shipped-by-sea series is available from the live UNCTADStat API only for 2000-2016; the book figure covers 1970-2016.
- Missing exact source version: Roser 2016r / OWID historical figure data was not recovered as an archived CSV.
- Validation policy correction: the main recreated plot excludes the incomplete right-side oil-shipping candidate because it covers only 2000-2016.
- Diagnostic evidence: the partial UNCTAD oil-shipping series is visualized separately under `outputs/diagnostics/`.
- Numeric gap: spill-count series is numeric and reproducible; oil-shipping values before 2000 are unresolved.

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
