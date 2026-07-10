# Figure 9-1 Provenance

## Evidence

- Title: International inequality, 1820-2013
- Source line: International inequality: OECD Clio Infra Project, Moatsos et al. 2014; data are for market household income across countries. Population-weighted international inequality: Milanovic 2012; data for 2012 and 2013 provided by Branko Milanovic, personal communication.
- Figure/source inspected from: Supplemental Graphics PDF page 9.
- Surrounding text: Pinker states that the international Gini rose from 0.16 in 1820 to 0.56 in 1970, then plateaued and began to droop in the 1980s; he then contrasts this with a population-weighted international Gini calculated by Branko Milanovic.
- Claim summary: Unweighted international inequality rose historically while population-weighted international inequality fell after the late twentieth century.

## Source Recovery Result

Partial source recovery only.

- Recovered for the unweighted/between-country line: OECD/IISH, *How Was Life? Global Well-being Since 1820* (2014), Chapter 11, Table 11.4, "Gini coefficients of within-country and between-country inequality, 1820-2000." The table gives between-country inequality values of 16, 23, 32, 38, 44, 49, 55, 54, 56, 56, 56, and 54 Gini points for 1820 through 2000. These values match Pinker's surrounding-text anchors of 0.16 in 1820 and 0.56 by 1970 after scaling by 100.
- Recovered source-input dataset: Clio Infra/IISH Dataverse handle `hdl:10622/6OHMDS`, "Income Inequality," version 1.1, public CC0 files `income_inequality-historical.xlsx` and `income_inequality.docx`. The XLSX contains country gross household-income Ginis for benchmark years 1820-2000; it is source input/provenance, not itself the plotted aggregate line.
- Not recovered: the inspectable Milanovic 2012 population-weighted international inequality series, including the 2012 and 2013 personal-communication update used by Pinker. Public searches found Milanovic papers and slide decks with Concept 2 chart images and data-file names such as `gdppppreg.dta` / `gdppppreg5.dta`, but not a downloadable source table for Pinker's weighted line.

## Reconstruction

No full reconstruction is accepted. The generated comparison images show a source-recovery/status panel that plots only the recovered OECD/Clio between-country series from Table 11.4 for 1820-2000 and explicitly omits the unrecovered Milanovic population-weighted series. This is intentional: the source-recovery rule forbids using digitized values from the book chart or Milanovic chart images as reconstruction data.

Clean recovered values are stored at `figures/9-1/data/clean/figure_9_1_oecd_table_11_4_between_country_inequality.csv`.

## Bibliography Resolution

- Moatsos, Michalis, Joerg Baten, Peter Foldvari, Bas van Leeuwen, and Jan Luiten van Zanden. 2014. "Income inequality since 1820." In Jan Luiten van Zanden et al., eds., *How Was Life?: Global Well-being since 1820*, OECD Publishing, pp. 199-215. DOI: `10.1787/9789264214262-15-en`.
- Moatsos, Michalis, Jan Luiten van Zanden, Joerg Baten, Peter Foldvari, and Bas van Leeuwen. 2015. "Income Inequality." IISH Data Collection / Clio Infra, version 1.1. Handle: `https://hdl.handle.net/10622/6OHMDS`.
- Milanovic, Branko. 2012. *All the Ginis dataset*, cited in OECD/IISH as `http://go.worldbank.org/YOW9ERU7G0`; current public successor located at the Stone Center as *All the Ginis (ALG) Dataset*, version February 2019. This is a country Gini compilation, not the recovered Concept 2 aggregate line.
- Milanovic, Branko. 2012/2013. "Global Income Inequality by the Numbers: in History and Now" / "Global Income Inequality in Numbers: In History and Now." These sources define Concepts 1-3 and show the population-weighted Concept 2 chart, but this run did not recover the underlying Concept 2 table.

## Archive Search

- Wayback CDX for `https://clio-infra.eu/Indicators/IncomeInequality.html` shows multiple 200 captures from 2020-12-30 through 2026-02-18. The CDX output is retained in `figures/9-1/data/raw/wayback_cdx_clio_income_inequality.json`.
- Wayback CDX for the `www.clio-infra.eu` variant mostly shows redirects to the non-`www` URL; the CDX output is retained in `figures/9-1/data/raw/wayback_cdx_www_clio_income_inequality.json`.
- The live Clio Infra download URLs and IISH Dataverse API were available in this run, so no archived file substitution was needed for the recovered Clio source-input files.

## Next Action

Recover the inspectable Milanovic population-weighted international inequality source table through 2013, or obtain a citable statement that the 2012-2013 values exist only as Pinker/Milanovic personal communication. Do not mark this figure as reconstructed or verified until both plotted series are source-backed.
