# Figure 17-5 Provenance

## Reference And Citation

Original: supplied Supplemental Graphics PDF, page 35 upper panel, title
"Spending on necessities, US, 1929-2016". Original crop was inspected at full
resolution. Source: HumanProgress dataset 1937, adapted from Mark Perry using
BEA data. The source note lists food at home, cars, clothing, household
furnishings, housing, utilities and gasoline; it omits 1941-1946 for wartime
rationing and soldiers' salaries. No Kindle context or author calculation
workbook was recovered in this pass. The source is an institutional data chain,
not an academic paper whose appendix has been silently substituted.

## Source Chain

Book -> HumanProgress / Mark Perry -> BEA NIPA components and disposable
personal income -> ALFRED archival releases -> retained numeric labels ->
`scripts/reconstruct_17_5.py` -> clean CSVs -> plots -> original-PDF comparisons.

Archived HumanProgress page:
https://web.archive.org/web/20170117185627id_/http://humanprogress.org/static/1937

The page's embedded JSON identifies dataset 1937, source BEA via Mark Perry,
updated 2016-09-06, and 87 annual observations, 1929-2015. Its basket omits
gasoline. JSON is decoded as data, not executed. Each observation is explicitly
not generated. The archived percentages are independently cross-checked against
the original-vintage BEA components; maximum absolute difference is below
5e-9 percentage points (the archive rounds percentages to eight decimals).

## BEA Inputs

All series are annual, not seasonally adjusted, billions of current dollars.
Official component identities were inspected and retained from
https://fred.stlouisfed.org/release/tables?rid=53&eid=44183#snid=44219

| Component | ALFRED/FRED series | Historical vintage | Current vintage |
| --- | --- | --- | --- |
| Food and beverages, off-premises | DFXARC1A027NBEA | 2016-07-29 | 2026-04-09 |
| Motor vehicles and parts | DMOTRC1A027NBEA | 2016-07-29 | 2026-04-09 |
| Furnishings and durable household equipment | DFDHRC1A027NBEA | 2016-07-29 | 2026-04-09 |
| Clothing and footwear | DCLORC1A027NBEA | 2016-07-29 | 2026-04-09 |
| Housing and utilities | DHUTRC1A027NBEA | 2016-07-29 | 2026-04-09 |
| Gasoline and other energy goods | DGOERC1A027NBEA | 2016-07-29 | 2026-04-09 |
| Disposable personal income | A067RC1A027NBEA | 2016-07-29 | 2026-05-28 |
| Motor fuels, lubricants and fluids (diagnostic only) | DMFLRC1A027NBEA | 2016-08-03 | 2026-04-09 |

Per-series URLs are in each raw JSON and every row of the long clean component
table. Numeric accessibility labels were read through the public ALFRED UI
after selecting the vintage and full date range. No pixels, line coordinates,
or plotted Pinker values were converted to observations. Raw labels and
display precision are retained: historical values typically 0.1 billion,
current values 0.001 billion. Failed direct CSV downloads are logged.

## Transformations And Limits

Sum the first five expenditure categories, divide by disposable personal
income and multiply by 100. This exactly cross-checks HumanProgress's baseline
at displayed precision. Add the energy-goods component using the same 2016
income vintage. The broad energy category is an explicit inference from the
book's abbreviated gasoline description and visual agreement, not a proven
copy of Pinker's workbook. A narrower motor-fuels-only alternative materially
misses historical levels and is retained as a diagnostic, not selected by
fitting numerical values to book pixels.

Keep all 87 historical observations in the clean file, flag 1941-1946 as
excluded, and mask them only in the plot. No interpolation crosses that gap.
The source ends 2015 despite the book's 2016 title. No original 2016 value is
invented. Revised 2026 components yield a separate 1929-2025 clean table;
the extension plot shows 2005-2015 dotted overlap and 2016-2025 dashed data
with the revised 2015 anchor, not a forced splice onto the old line. The two
2015 estimates are approximately 33.93 and 34.15 percent. Revisions over the
full overlap reach about 0.52 percentage points. Current income and spending
release dates differ as recorded above.

This ratio of national aggregates includes imputed expenditure, notably
owner-occupied rent. It does not establish the experience of a median or
low-income household. Pandemic-era income and spending changes affect the
ratio; no causal explanation is asserted from the chart alone.

Scientific status: `partial_match`. Overall confidence: medium; numeric
provenance: high; exact book adaptation: medium. Recover the author's final
basket/workbook or a later archived HumanProgress release before promotion.

## Reproduction And Refresh

Run `python scripts/reconstruct_17_5.py` offline with the retained files.
Run `python scripts/export_figure_lineage.py --figure 17-5` after a deliberate
source/script revision. The lineage names every active input and diagnostic.
Raw observations, clean components, ratios and source-version differences are
included in the shared SQLite library. Preserve the 2016 release permanently;
refresh current components and income together into new versioned files, test
coverage/units/overlap, and review revisions before replacing the continuation.
The browser retrieval is documented, but an unattended BEA downloader is not
yet implemented. BEA/FRED institutional data attribution is retained; no broad
license grant for the HumanProgress page or book image is assumed.
