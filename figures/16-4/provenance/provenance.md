# Figure 16-4 provenance

Original: supplied Supplemental Graphics PDF, page 31 lower panel. Title,
caption and source note inspected at full resolution. England represents adults;
the three modern lines represent youth aged 15-24. These populations must not be
treated as a continuous national series. Full surrounding Pinker text is pending.

Book citation: Clark (2007), *A Farewell to Alms*, p.179, for England;
HumanProgress dataset 2101, UNESCO UIS via World Bank 2016f, for World, Pakistan
and Afghanistan. The book explicitly says country membership varies by year.

## Accepted Numeric Evidence

The already retained [November 2016 WDI archive](../../17-8/data/raw/WDI_csv_20161119172134.zip)
contains `WDI_Data.csv`, `WDI_Country.csv`, source definitions and footnotes.
Original download/capture URLs and hashes are in
[the shared download log](../../17-8/source_logs/downloads.json). It is reused
without duplicating the 2016 bulk archive. Select `SE.ADT.1524.LT.FM.ZS`, Afghanistan
and Pakistan, nonmissing years through 2014. Units are a ratio, NOT percent.
Twelve observations recover two of four curves; joins are straight between
observations, with no annual or extrapolated data invented.

The [current indicator definition](https://api.worldbank.org/v2/indicator/SE.ADT.1524.LT.FM.ZS?format=json)
confirms female/male youth literacy rates and cites UIS February 2026 data,
accessed March 19, 2026. The downloaded all-country response has WDI last update
July 13, 2026. [Exact query](https://api.worldbank.org/v2/country/all/indicator/SE.ADT.1524.LT.FM.ZS?format=json&per_page=30000)
is retained in `data/candidates/wdi_ratio.json`; both API payloads are cached.
Afghanistan ends 2022 and Pakistan 2021, not 2026. The extension is a separate
revised series, not spliced onto the frozen 2016 vintage. Current Afghanistan
2015 is about .44 versus .66416 in the older release. This is a vintage revision,
not evidence that literacy dropped between those two values in 2015.

## Missing Or Rejected Evidence

World: WDI 2016 has no WLD observation for this indicator. A simple unweighted
mean of available countries produces a jagged series, unlike the book. Its
country counts and values are retained in a diagnostic CSV, but it is NOT plotted
as a reconstructed World line. No interpolation or country carry-forward was
chosen merely to force the book's smooth trajectory.

England: [Clark's official teaching chapter](https://faculty.econ.ucdavis.edu/faculty/gclark/ecn110a/readings/Chapter10.pdf)
identifies Schofield (1973), marriage signatures, for 1750s-1920s. Clark's data
index does not list this workbook. Schofield, *Dimensions of illiteracy,
1750-1850*, *Explorations in Economic History* 10(4),437-454,
[DOI](https://doi.org/10.1016/0014-4983(73)90026-0), is subscriber access at the
publisher. No access controls were bypassed. The pinned OWID England-by-sex
dataset misleadingly names Schofield but actually contains only Houston (1982)
Northern England court deponents, 1640-1740, all before this figure's period.
Its metadata and numbers are retained as a rejected candidate, not substituted.
Floud and Harris's [NBER chapter](https://www.nber.org/system/files/chapters/c7429/c7429.pdf)
documents the original Schofield/Registrar-General chain, but the cited figure
combines sexes and does not supply the needed gender ratio. Charts were not digitized.

## Rebuild And Refresh

Run `python scripts/reconstruct_16_4.py` from a dependency-installed checkout.
No network is used to rebuild. Then run the lineage export, artifact refresh,
comparison builder, state generator and database builder documented in the root
workflow. Future WDI refreshes must be saved under NEW versioned names, compared
on overlapping years, and reviewed before changing plot inputs. Keep the frozen
2016 series. All four clean CSVs and raw-file references enter the SQLite library.

Status: `partial_match`. Two legitimate country curves are useful, but the
missing England and World lines prevent publication acceptance. No exact-vintage
claim is made for the unlocated HumanProgress export.
