# Figure 16-5 provenance

Original supplied PDF page 32 upper panel inspected: *IQ gains, 1909-2013*.
Six lines show changes, not absolute IQ. The caption warns that tests and start
dates differ, so trajectories cannot be compared to one another as IQ levels.
Full surrounding Pinker prose remains unreviewed.

Book citation: Pietschnig & Voracek (2015), supplemental online material.
Full citation: *One Century of Global IQ Gains: A Formal Meta-Analysis of the
Flynn Effect (1909-2013)*, *Perspectives on Psychological Science* 10(3),282-306.
[DOI](https://doi.org/10.1177/1745691615577701). The study pools 271 independent
samples from 31 countries; it is not a census of every person in these regions.

## Numeric Source

`data/raw/owid_iq.csv` and `owid_iq.json` are downloaded from OWID's dataset
repository pinned to `6155d4ca1ea14ef30e753010a25521eeb416e8a2`. The metadata
identifies July 21, 2015 as the original data retrieval and explicitly cites the
paper. Exact file URLs, hashes and retrieval time are in the download log.
An [April 2016 archived OWID page](https://web.archive.org/web/20160424225937id_/http://ourworldindata.org/intelligence/)
confirms the paper/graph association and its interpretive limitations.

Select the regional fullscale-change column, NOT the separate country-change
column. Keep 36 numeric observations (six each for Africa, America, Asia, Europe,
Global, Oceania). Rename Global to World, America to Americas, Oceania to
Australia & NZ for the book's labels. No averaging, smoothing, slope extrapolation
or digitization. Europe's initial 1912 zero anchor is retained in data but not
drawn, since the visible book curve starts at the next observation in 1933;
`shown_in_book_plot` exposes this display choice. Other zeros stay visible.
The 30 inter-knot slopes are derived diagnostic data, not independent measurements.

## Evidence Boundary

The original publisher supplement could not yet be independently recovered.
The present publisher request returns 403; a real 2015 archive of the supplement
landing page is an access/login page, not numeric evidence. Figshare DOI and
title searches return empty arrays. The archive wildcard index returns 503.
Thus the study's sample weighting, regional pooling and breakpoint calculations
have NOT been independently reproduced. The six curves closely match the book,
but `partial_match` remains appropriate until this source gap is closed.

## Extension

No comparable global six-region continuation recovered. Later studies of Raven's
SPM, Austrian pilots, older adults or US online samples use different tests and
populations and cannot be spliced into these trajectories. University records
identify a promising 1909-2025 ability-specific meta-analysis presentation,
but no reviewed numeric release for this exact regional statistic was located.
The extended artifact therefore repeats history with an explicit no-extension
notice. Do not extrapolate the historical slopes or interpret absence of an
extension as continuing IQ gains everywhere.

Rebuild: `python scripts/reconstruct_16_5.py`. Retained files suffice offline.
Future source recovery should add the original supplement and recompute pooled
trajectories; future releases must preserve original baselines and clearly
separate changed test composition. Country levels/racial rankings are not an
output of this dataset or this reconstruction.
