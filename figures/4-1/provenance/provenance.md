# Provenance: Figure 4-1

- Figure: 4-1, Tone of the news, 1945-2010
- Canonical visual reference: `references/enlightenment_now_supplemental_graphics.pdf`, page 2
- Source line: "Leetaru 2011. Plotted by month, beginning in January."
- Current status: `blocked_external_source`

## Source Recovery Result

The Supplemental Graphics PDF confirms the title, year span, units, and source
line. The figure combines two monthly sentiment/tone source families:

- New York Times, 1945-2005.
- Summary of World Broadcasts, 1979-July 2010.

The GDELT project hosts high-resolution mirrors of Leetaru's original
Culturomics 2.0 figures. These mirror Figure 10 for New York Times average
monthly tone and Figure 11 for Summary of World Broadcasts average monthly
tone. They are accepted as source-visual evidence only.

## Data Fidelity

No inspectable month-level data table was recovered in this pass. The obvious
candidate companion files under the GDELT figure mirror paths, including CSV
and XLS names matching `figure10` and `figure11`, returned HTTP 404.

No values were digitized from Pinker's plotted figure. The recovered source PNGs
were not digitized either, because the acceptance criteria require original data
recovery first and honest blocker documentation when source data are missing.

## Reconstruction And Extension

No book-period reconstruction was generated from source data. No extended
comparison was generated, because a valid extension requires either the original
Leetaru monthly data or a documented same-method successor series.

The comparison artifacts in `plots/comparisons/` are source-recovery review
artifacts. They place the Supplemental Graphics reference beside the recovered
Leetaru/GDELT source figures to document why the figure is blocked.

## Next Recovery Steps

1. Contact Kalev Leetaru or GDELT for the original monthly NYT and SWB tone
   tables behind Culturomics 2.0 Figures 10 and 11.
2. Search institutional or author archives for `figure10` or `figure11`
   spreadsheet/source-data companions not exposed on the public mirror.
3. If original data are confirmed unavailable, decide whether the project will
   admit a separately documented same-method rerun using an available corpus.
