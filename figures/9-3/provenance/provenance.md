# Figure 9-3 Provenance

## Evidence

- Title: Inequality, UK and US, 1688-2013
- Book page: Supplemental Graphics PDF page 10
- Source line: Milanovic 2016, fig. 2.1, disposable income per capita.
- Claim summary: Long-run UK and US Gini series rose, fell in the mid-twentieth century, and rose again in recent decades.

## Provenance Trail

Supplemental Graphics PDF page 10 -> Milanovic 2016 Figure 2.1 -> Milanovic slide-deck evidence naming `US_and_uk.xls / uk_and_usa.xls` -> source-recovery audit in `figures/9-3/data/candidates/source_recovery_audit.csv` -> source-recovery-blocked status panels.

## Source Recovery Result

The likely original data workbook is identified but not recovered. The recovered evidence names the workbook and documents the component-source families, but no inspectable source table exposes the UK/England and US disposable-income-per-capita Gini series used in Pinker's 1688-2013 chart.

## Reconstruction

No reconstruction data file was accepted. The generated comparison images are source-recovery/status panels only, not reconstructed charts. This is intentional: the project rule forbids using digitized values from the book chart or slide images as reconstruction data.

## Extension

No extension is plotted. Current World Bank, ONS, LIS/SWIID, or WID-style Gini series are not a verifiably comparable continuation of Milanovic's stitched disposable-income-per-capita workbook series across the full UK/US book period.

## Next Action

Recover `US_and_uk.xls` / `uk_and_usa.xls` from Milanovic, a publisher supplement, archived CUNY/LIS storage, or an equivalent author-supplied table.
