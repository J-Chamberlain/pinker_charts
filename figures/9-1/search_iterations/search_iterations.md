# Figure 9-1 Search Iterations

Dates: 2026-06-30, updated 2026-07-09

- Inspected Chapter 9 preview PDF page image and source line.
- Searched public web for exact title/source and likely data family.
- For 9-4, located current OWID grapher successor and metadata.
- For Milanovic/Clio Infra figures, found source references but did not recover an inspectable raw spreadsheet/table in this batch.

## 2026-07-09 Targeted Recovery

- Inspected Supplemental Graphics PDF page 9. Located Figure 9-1, source note, and surrounding text. Surrounding text gives unweighted international Gini anchors of 0.16 in 1820 and 0.56 in 1970.
- Searched for `Moatsos et al. 2014 OECD Clio Infra Project market household income Gini international inequality data`, `"Income inequality since 1820" "Moatsos" "data"`, and Clio Infra indicator pages.
- Located the live Clio Infra `Income Inequality` indicator page. It describes gross household-income Gini benchmark data for 1820-2000, production date 2014-06-15, and links compact/broad downloads plus IISH Dataverse.
- Downloaded live Clio Infra compact/broad XLSX files and IISH Dataverse files. The Dataverse API reports handle `hdl:10622/6OHMDS`, publication date 2015-12-13, version 1.1, CC0, file IDs 84 and 85, and MD5 checksums matching the local downloads.
- Downloaded the official OECD PDF for *How Was Life? Global Well-being Since 1820*. Chapter 11, Table 11.4 contains the aggregate between-country inequality values for 1820-2000. These were accepted for the unweighted line because they match Pinker's text anchors after scaling Gini points to a 0-1 index.
- Queried Wayback CDX for both `clio-infra.eu/Indicators/IncomeInequality.html` and `www.clio-infra.eu/Indicators/IncomeInequality.html`. Multiple non-`www` captures exist from 2020 onward; `www` mostly redirects.
- Searched for Milanovic `All the Ginis`, `YOW9ERU7G0`, `population-weighted international inequality`, `Concept 2`, `gdppppreg.dta`, `gdppppreg5.dta`, and `key_variables_calcul3.do`. Found papers and slide decks that define/show Concept 2 population-weighted inequality and cite internal Stata files, but no inspectable data table for Pinker's population-weighted series through 2013.
- Evaluated Stone Center *All the Ginis* successor. It is a country Gini compilation, not a direct table of the plotted population-weighted international inequality series, so it was not accepted as a replacement.
