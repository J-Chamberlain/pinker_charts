# Anomaly Review: Figure 19-1

## Visible Differences
- The Kindle figure is a stacked-area chart while the current reconstruction is a three-line chart.
- The recreated series captures the broad rise and post-Cold-War decline but does not match the original visual encoding.
- The cited HumanProgress/FAS 2016 table remains unrecovered.
## Cause Assessment
- Current status: `partial_match`.
- The major discrepancy is caused by both source and chart-type mismatch: the source is a current OWID successor, and the transformation does not recreate the stacked-area composition.

## Reviewer Challenge
- Pinker would likely ask whether the cited source chain has been reconstructed exactly.
- A data journalist would ask for raw download URLs and reproducible scripts.
- A peer reviewer would ask whether successor data have been separated from book-period data.
- A skeptical reader would notice any label or curve-shape mismatch in the side-by-side.

Overall confidence:
- Book reconstruction: 0.62
- Extension: low; successor OWID extension only
- Source provenance: see source log.
- Outstanding risks: Recovering the HumanProgress static 2927/FAS 2016 table is required before the figure can move beyond partial_match.
- Recommended next action: Recover cited HumanProgress/FAS table or archival copy, then reconstruct as stacked area before visual validation can pass.
