# Figure 16-1 provenance

## Original reference
Authorized Supplemental Graphics PDF, page 30 upper panel. Title: Literacy,
1475-2010. Eight series visually inspected directly, not inferred from metadata.
Source: Our World in Data, Roser & Ortiz-Ospina 2016b; before 1800 Buringh & Van
Zanden 2009; World van Zanden et al. 2014; US NCES; after 2000 CIA 2016.
The supplemental file has the caption and source, but not surrounding book prose.
No claim that the complete book discussion has been reviewed.

## Exact archival dataset
The January 1, 2017 [archived OWID topic](https://web.archive.org/web/20170101130054id_/https://ourworldindata.org/literacy/)
links an older interactive chart. Its [November 19, 2016 HTML](https://web.archive.org/web/20161119120506id_/https://ourworldindata.org/roser/graphs/LiteracyRatesGlobalLongRun/LiteracyRatesGlobalLongRun.html)
explicitly loads `LiteracyRatesGlobalLongRun.csv`. The recovered
[CSV](https://web.archive.org/web/20160325002542id_/http://ourworldindata.org/roser/graphs/LiteracyRatesGlobalLongRun/LiteracyRatesGlobalLongRun.csv)
is a March 25, 2016 capture, not a newly digitized chart. SHA256:
`08301aedb7469da9c2ae19a915a65b69fb7b2bf81f132f49f167d03fea4b2be9`.
All eight book series are present. The date requested and actual redirected
timestamp differ; both are preserved in `source_logs/downloads.json`.

Select World, Netherlands, Great Britain, Germany, Italy, USA, Chile and Mexico;
drop blank observations, melt to long form, retain years through 2010, rename
display labels only. No numerical adjustment, smoothing, densification or
digitization. Lines join sparse source observations exactly as the book does.
Early dates are period midpoints in the OWID source, not exact survey dates.

## Source chain
- Buringh, Eltjo, and Jan Luiten van Zanden (2009), Charting the Rise of the West:
  Manuscripts and Printed Books in Europe, A Long-Term Perspective from the Sixth
  through Eighteenth Centuries, Journal of Economic History 69(2), 409-445.
  Historical literacy is estimated; it is not the contemporary adult test measure.
- Broadberry and O'Rourke (2010), The Cambridge Economic History of Modern Europe,
  supplies additional nineteenth-century national points in OWID's archived notes.
- Van Zanden et al., editors (2014), How Was Life? Global Well-being since 1820,
  OECD, is the cited World source. The recovered OWID assembly includes anomalous
  1940-1980 values that subsequent OWID versions revise. Their ultimate cause is
  not established; reproducing them does not endorse them as current best estimates.
- [NCES historical literacy table](https://nces.ed.gov/naal/lit_history.asp),
  prepared September 1992, citing Census Historical Statistics and Current
  Population Reports P-23. Fourteen US 1870-1979 observations agree exactly with
  100 minus its total illiteracy rate. Population: age 14+, ability to read/write
  any language; not contemporary functional literacy.
- Latin America: Oxford Latin American Economic History Database (OxLAD), as
  documented by the archived OWID page. The separate archived illiteracy CSV is
  retained for audit; it is not an alternative plot input.
- CIA World Factbook: source for modern endpoints in the 2016 OWID assembly.
  Direct 2016 CIA country-table verification remains an upstream audit task.
  It is not needed to invent or substitute values: the original assembly is saved.

## Successor and revisions
[Current cross-country export](https://ourworldindata.org/grapher/cross-country-literacy-rates.csv)
and `.metadata.json` retained with download date 2026-09-10 UTC. OWID May 2026
revision, UNESCO UIS 2026, generally adult age 15+ and census/self-reported basic
literacy. Different historical definitions, age groups and source revisions
prevent a seamless splice into the book-era assembly.

The extension is a separate panel: revised overlap 2000-2010 dotted; observed
post-2010 records dashed with markers. Italy ends 2019, Chile 2017, Mexico and
World 2024. Do not carry these forward or fabricate US/UK/Germany/Netherlands
updates. A gap separates pre/post-2010 segments where necessary; lines between
observations are display interpolation only, never added database observations.

The pinned 2018 cross-country dataset and 2019 global series are retained as
revision candidates. Neither replaces the original book-period data. A diagnostic
compares World vintages and explicitly selects the literacy, not illiteracy, column.

## Reproduction and refresh
`python scripts/reconstruct_16_1.py` is offline. Lineage records exact raw inputs,
clean outputs and plots; checksums identify all retained versions. The database
ingests clean rows and file hashes. A future refresh must download a new version
under a new filename and compare definitions/overlap before changing the successor.
Never overwrite the archived 2016 book input or present a revision as observed growth.

## Additional upstream evidence from Figure16-2 recovery
The original OECD Figure5.1 StatLink XLS was subsequently recovered as
`figures/16-2/data/raw/oecd_figure_5_1.xls` through
https://doi.org/10.1787/888933095666. Its literacy column contains the same unusual
1950/1960/1970/1980 values, at unrounded precision. Thus those anomalies are already
in the cited OECD2014 source, not introduced by this reconstruction or uniquely by
OWID. The reason for later historical revisions remains unresolved. This is
additional source evidence, not a change to the frozen literacy plot input.

Overall confidence: high for reproducing the cited OWID assembly; medium for
comparability across centuries. Book reconstruction: strong visual/source match.
Extension: explicitly revised, not exact continuation. Source provenance: archived
original plus direct NCES cross-check. Outstanding risks: World anomalies, CIA
upstream verification, unavailable surrounding discussion. Next action: independent
publication review and upstream World-source audit without altering frozen history.
