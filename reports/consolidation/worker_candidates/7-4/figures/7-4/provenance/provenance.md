# Provenance: Figure 7-4

Status: `partial_match`. Confidence: `medium`. Source status: `source_family_static_source_image_labels_recovered_denominator_output_unresolved`. Extension status: `no_comparable_successor_extension_plotted`.

Book/Supplemental Graphics PDF figure -> source note -> Hasell & Roser 2017 OWID article -> downloadable OWID famine event table -> 2018 Wayback topic-page footnote and static source image -> `scripts/reconstruct_7_4.py`.

Book source note: Our World in Data, Hasell & Roser 2017, based on data from Devereux 2000; O Grada 2009; White 2011; EM-DAT; and other sources.

Recovered source trail:

- Supplemental Graphics PDF page 6 gives the figure title, axis label, and source note.
- `https://ourworldindata.org/the-our-world-in-data-dataset-of-famines` preserves the Hasell & Roser article and cites the 2017 OWID dataset.
- The article links a downloadable spreadsheet at `https://docs.google.com/spreadsheets/d/1nxOsUE9gtdi_q177Bx1JaazfI0l1M6BA7xKYFbG8IAg/`.
- The 2018 Wayback capture of `https://ourworldindata.org/famines` contains the chart heading, chart image, and calculation footnote.
- Wayback/CDX searches found no 2017-2018 capture of a decadal-rate grapher CSV/config; the live `death-rate-from-famines-by-decade` grapher first appears in 2025 captures and uses the World Peace Foundation successor source.

Canonical book-period values are transcribed from the printed labels in the archived static OWID source image. The event-table/denominator recomputation is retained as a diagnostic because it follows the archived footnote rule but does not exactly reproduce the static image when using the current preserved event table and current OWID World population. The exact 2017 rate output and denominator vintage remain unresolved.

Transcription audit: the canonical decadal values are exact integer label transcriptions from the archived static OWID image. Each label was checked against the visible bar label in the image after zoomed visual review. Expected tolerance is 0 label units for transcription; +/-0.5 deaths per 100,000 people per decade is only the implied rounding tolerance if comparing against the unrecovered continuous underlying rates.

The remediation state is that no comparable successor extension is plotted. `figure_7_4_extended_clean.csv`, `plots/extended/figure_7_4_extended_reconstruction.png`, and `plots/comparisons/figure_7_4_extended_comparison.png` are retained as no-successor/book-period-duplicate status artifacts. They are not a real post-2016 extension and must not be cited as one.

`plots/comparisons/kindle_reference_figure_7_4.png` is a legacy filename. Current documentation treats it as the book/Supplemental Graphics PDF reference crop; the filename is retained to avoid breaking existing artifact links.
