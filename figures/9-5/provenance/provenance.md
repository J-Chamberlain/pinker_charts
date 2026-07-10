# Figure 9-5 Provenance

## Evidence

- Title: Income gains, 1988-2008
- Source line: Milanovic 2016, fig. 1.3.
- Figure/source inspected from: Supplemental Graphics PDF page 11.
- Surrounding text: Pinker describes the graph as a growth incidence curve that sorts the world's population from poor to rich and plots real income gains from 1988 to 2008.

## Bibliographic Resolution

- Pinker's source resolves to Branko Milanovic, *Global Inequality: A New Approach for the Age of Globalization* (2016), figure 1.3/nearby chapter figure text.
- The Milanovic book chapter identifies the underlying source family as Lakner and Milanovic data. A publicly posted chapter scan labels the comparable figure's data source as Lakner and Milanovic (2015).
- The World Bank Open Knowledge Repository entry for Lakner and Milanovic's working paper links to a dataset node that has moved or no longer resolves as an inspectable catalog page.
- The CUNY Stone Center page for the Lakner-Milanovic World Panel Income Distribution provides the downloadable LM-WPID Stata dataset and a variable-description PDF.

## Source Recovery Result

Recovered inspectable source-family data:

- `figures/9-5/data/raw/lm_wpid_web.dta`
- `figures/9-5/data/raw/lm_wpid_description.pdf`
- `figures/9-5/data/raw/lakner_milanovic_world_bank_wps6719.pdf`
- saved provenance pages under `figures/9-5/data/raw/`

Unresolved exact source:

- Milanovic 2016 figure 1.3's exact plotted spreadsheet, repeatedly referenced in presentations as `summary_data.xls`, was not recovered as an inspectable file.
- The recovered LM-WPID file covers the correct 1988-2008 period and source family, but it is not the final plotted `summary_data.xls`/Lakner-Milanovic 2015 figure-data file.

## Reconstruction Method

- Read LM-WPID `lm_wpid_web.dta`.
- Kept the authors' main sample (`mysample == 1`) and benchmark years 1988 and 2008.
- Excluded rows with missing `RRinc` or `pop`; this removes one Switzerland 2008 decile row with missing income from the recovered file.
- Sorted country-decile observations by `RRinc` within each year and used population weights (`pop`).
- Computed mean income for plotted fractile bins ending at 5, 10, ..., 95, 99, and 100 percent of the global distribution.
- Computed cumulative growth as `100 * (mean_2008 / mean_1988 - 1)`.

## Data Fidelity

The recovered source-family curve peaks at percentile 55 with 77.3% growth and bottoms at percentile 80 with 1.0% growth. The visible book/Pinker curve has the same elephant-shaped qualitative pattern but differs at some plotted points, especially the low and middle fractiles. Because the exact source spreadsheet was not recovered, no numeric tolerance against Milanovic 2016 figure 1.3 is asserted.

## Extension

No successor extension was plotted. The task's acceptance rule requires a genuinely comparable successor series; no same-methodology post-2008/2011 successor file was recovered in this run.
