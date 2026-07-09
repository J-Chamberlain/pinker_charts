# Figure 9-2 Search Iterations

Date: 2026-06-30; updated 2026-07-09

- Inspected Chapter 9 preview PDF page image and source line.
- Searched public web for exact title/source and likely data family.
- For 9-4, located current OWID grapher successor and metadata.
- For Milanovic/Clio Infra figures, found source references but did not recover an inspectable raw spreadsheet/table in this batch.

## 2026-07-09 Targeted Milanovic Figure 3.1 Recovery

- Inspected Supplemental Graphics PDF page 10 and rendered the canonical reference page to `figures/9-2/plots/comparisons/supplemental_pdf_page_10_figure_9_2.png`.
- Confirmed the source note: Milanovic 2016, figure 3.1; left curve in 1990 international dollars of disposable income per capita; right curve in 2005 international dollars combining household surveys of per capita disposable income and consumption.
- Resolved the bibliography entry to Branko Milanovic, *Global Inequality: A New Approach for the Age of Globalization*, Belknap Press of Harvard University Press, 2016, ISBN 9780674737136.
- Searched the public web for exact and near-exact combinations of `Milanovic 2016 figure 3.1`, `Global inequality 1820 2011 data spreadsheet`, `supplementary material`, `xls`, `xlsx`, and `thepast.xls`.
- Checked the LIS book page. It confirms the book but exposes no supplement or data file.
- Checked the Harvard University Press ISBN URL. It returned a CloudFront/WAF challenge from this environment and no data links were inspectable.
- Queried Wayback CDX for tested Harvard ISBN URLs; no 200 captures were returned. Broader archived xls queries for likely HUP, Branko Milanovic, and old World Bank paths did not recover the workbook.
- Found successor/source-family evidence in Milanovic 2024, including a Stone Center working paper and 2024 slides. The slides label the long-run chart data as `History/thepast.xls`, but only the slide/PDF was public, not the workbook.
- Determined that Milanovic 2024 is not a comparable extension for Pinker's book-period figure because it uses revised 2011 PPP historical estimates and later household-survey/unpublished updates rather than the 1990/2005-dollar split in the Supplemental PDF source note.
