# Anomaly Review: Figure 5-2

## Visible Differences
- The revised curves better align with the Kindle scale and starting levels than the prior Gapminder proxy.
- Some country trajectories and endpoint label positions still differ visibly from the book.
- The South Korea, Ethiopia, Chile, and Canada labels crowd the lower-right corner more than in the Kindle figure.
## Cause Assessment
- Current status: `partial_match`.
- The remaining mismatch is most likely source-vintage and country-series construction, with minor styling/layout differences. The unit error in the successor series was corrected.
- 2026-07-09 source recovery found the archived OWID article and old Chart
  Builder view 58 lead, but not the dynamic data payload behind that chart.
- Recovered OWID Gapminder/UN IGME/HMD source-family candidates explain the
  source chain but do not exactly reproduce the book-era data coverage.

## Reviewer Challenge
- Pinker would likely ask whether the cited source chain has been reconstructed exactly.
- A data journalist would ask for raw download URLs and reproducible scripts.
- A peer reviewer would ask whether successor data have been separated from book-period data.
- A skeptical reader would notice any label or curve-shape mismatch in the side-by-side.

Overall confidence:
- Book reconstruction: 0.72
- Extension: medium-low; current OWID successor extension, not exact book vintage
- Source provenance: see source log.
- Outstanding risks: The exact Roser 2016a UN Child Mortality/Human Mortality
  Database assembled file, old Chart Builder view 58 data/config, or archival
  OWID export remains the blocker for verification.
- Recommended next action: Continue source recovery for Chart Builder view 58
  data/config or an equivalent book-era OWID export before promoting status.
