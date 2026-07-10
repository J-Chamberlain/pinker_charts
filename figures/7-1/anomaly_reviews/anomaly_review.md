# Anomaly Review: Figure 7-1

## Visible Differences
- Styling, typography, label placement, and crop geometry are approximate.
- The regenerated 2026-07-09 book-period comparison includes all six book
  series, but labels remain crowded near 2000 for United States, France, China,
  World, and England/UK.
- The reconstructed long-run England/UK, France, and United States line shapes
  do not fully match the book chart.
- The extension is clearly dashed after 2013 and stops in 2018; no 2026 live
  OWID values were appended because the live series has revised values and
  broader 1274-2023 coverage.

## Cause Assessment
- Current status: `partial_match`.
- Source fidelity: updated-equivalent only. A 2018 archived chart page was
  recovered, but the underlying 2016/2018 OWID variable data were not.
- The current raw file is a post-publication OWID dataset-repository vintage
  added in 2022 and is not a recovered book-era export.
- The `England/UK` line is transparent labeling of a source substitution, not
  proof that the exact book England series was recovered.

## Reviewer Challenge
- Pinker would likely ask whether the exact Roser 2016d/FAO data export was
  recovered. Answer: no; only chart-page configuration and later successor
  data were recovered.
- A data journalist would ask for archival URLs and machine-readable source
  files. Answer: the archived chart page is stored under
  `data/candidates/archives/`; direct Wayback checks for machine-readable
  variable endpoints were negative.
- A peer reviewer would ask whether successor data are separated from
  book-period data. Answer: yes; values after 2013 are dashed and are from the
  same 2022 OWID successor file through 2018.
- A skeptical reader would notice visible label and line-shape differences in
  the side-by-side. Answer: documented as unresolved source-vintage mismatch.

Overall confidence:
- Book reconstruction: 0.72
- Extension: medium for 2014-2018 same-file continuation, not for the newer
  2026 live series.
- Source provenance: partial; source family confirmed but exact vintage
  unrecovered.
- Outstanding risks: exact source-vintage recovery remains incomplete; visual
  shape mismatch remains.
- Recommended next action: targeted source recovery before status promotion.
