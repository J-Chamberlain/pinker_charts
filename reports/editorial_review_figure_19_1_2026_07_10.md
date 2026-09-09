# Editorial Review: Figure 19-1

Date: 2026-07-10

Disposition: `partial_match`; acceptable for source-recovery review, not eligible for `verified_reproduction`.

## Evidence gate

- Primary recovery passes: Internet Archive capture `20160814144251` exposes HumanProgress dataset 2927 and 138 non-generated U.S./USSR-Russia observations for 1945-2015.
- Numeric fidelity passes for the recovered series: 138/138 values compare exactly after transformation; maximum absolute error is 0 warheads.
- Bibliography resolution passes: the source line is resolved to Kristensen and Norris's 2016 Russian-forces article and the archived FAS Status of World Nuclear Forces update.
- Minor-series vintage does not pass exact-source verification: the archive payload has no France, China, UK, Pakistan, India, or Israel records. The current FAS-derived OWID values are visibly small and institutionally related, but are not represented as exact 2016 values.

## Visual gate

- X-axis passes: 1945-2015.
- Y-axis passes: 0-70,000 with 10,000 increments.
- Encoding passes: stacked areas replace the former three-line proxy.
- Principal geometry passes: U.S. and USSR/Russia peaks, crossover, and post-1990 decline align closely with the Kindle reference.
- Labels pass with a disclosed styling approximation. The six minor layers are labeled at right; typography and connector placement are not pixel-identical.

## Extension gate

No post-2015 segment is plotted. Although the successor is FAS-derived, the recovered book source is a fixed 2015 HumanProgress vintage and revision continuity is not documented closely enough to imply a seamless extension.

## Documentation gate

PROJECT_STATE, per-figure metadata, caption, provenance, source/discrepancy logs, lineage, checklist, script, clean data, plots, and checksums describe the same hybrid reconstruction and retain `partial_match`. The figure registry is intentionally untouched under the run operating rules.

## Ten-second review

No unexplained critical or major visual defect remains. The remaining minor-series source-vintage limitation is conspicuous in the caption and plot note. Promotion to verified status would be misleading and is rejected.
