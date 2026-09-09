# Source Discovery Log: Figure 7-3

Editorial remediation date: 2026-06-30

- Rechecked the original crop for the regional inventory: Developing world, Sub-Saharan Africa, Southeast Asia, South Asia, East Asia, and Latin America.
- Rechecked local OWID FAO datasets and the current OWID `prevalence-of-undernourishment` grapher.
- Recovered current FAO successor entities for each named region, but only for 2000 onward: `Sub-Saharan Africa (FAO)`, `South-eastern Asia (FAO)`, `Southern Asia (FAO)`, `Eastern Asia (FAO)`, and `Latin America and the Caribbean (FAO)`.
- The exact Roser 2016j / FAO 2014 regional file with early-1990s coverage was not recovered; this remains a research task.

Primary public source URLs used during remediation:

- https://ourworldindata.org/grapher/prevalence-of-undernourishment.csv
- https://ourworldindata.org/grapher/death-rate-from-famines-by-decade.csv
- https://ourworldindata.org/grapher/world-gdp-over-the-last-two-millennia.csv
- https://ourworldindata.org/grapher/gdp-per-capita-maddison-2020.csv
- https://ourworldindata.org/grapher/world-population-in-extreme-poverty-absolute.csv


## Worker Recovery At d4682dabe9fa46f369dd041cfc6ec8d09eeffef9

# Source Discovery Log: Figure 7-3

Update date: 2026-07-09

- Opened the Supplemental Graphics PDF and located Figure 7-3 on PDF page 6 / book page 72.
- Captured a Supplemental PDF crop at `figures/7-3/plots/comparisons/supplemental_pdf_reference_figure_7_3.png`; the legacy `kindle_reference_figure_7_3.png` path now contains the same PDF-derived crop for compatibility with existing comparison code.
- Confirmed the source note: Our World in Data, Roser 2016j, based on data from the Food and Agriculture Organization 2014, also reported in FAOSTAT.
- Internet Archive snapshots of `http://www.fao.org/economic/ess/ess-fs/ess-fadata/en/` were checked. The November 23, 2014 snapshot includes a "Download data" link (`http://bit.ly/14FRxGV`), states "Last updated: 17 November 2014", and lists "Prevalence of undernourishment" coverage as 1990-2014.
- The archived `bit.ly/14FRxGV` target resolves to FAO's `Food_Security_Indicators.xlsx`. Internet Archive preserved the workbook at a February 8, 2015 capture and a March 17, 2016 capture.
- Parsed the March 17, 2016 archived workbook directly from XLSX XML. Sheet `V_2.6 - Prevalence of undernourishment` contains the book's named regional curves: `Sub-Saharan Africa`, `South-Eastern Asia`, `Southern Asia`, `Eastern Asia`, and `Latin America`, plus `Developing countries`.
- Extracted `V_2.6` to `figures/7-3/data/candidates/fao_food_security_indicators_archived_20160317_v_2_6_extracted.csv`.
- Rebuilt `figures/7-3/data/clean/figure_7_3_book_period_clean.csv`: regional values cover 1991-2015, and developing-world values cover 1970, 1980, and 1991-2015.
- No post-2015 extension is plotted. OWID's current metadata says FAO has adapted its methodology and no longer updates the long-term developing-country series from the 1970s, so successor values are not treated as a comparable extension.

Remaining caveat: the complete regional reconstruction uses the archived 2016 FAO workbook. The November 2014 workbook was recovered as source-chain evidence but does not extend through the book's 2015 endpoint, so this remains a partial match rather than a verified Roser 2016j / FAO 2014 reproduction.

Primary public source URLs used during remediation:

- https://ourworldindata.org/grapher/prevalence-of-undernourishment.csv
- https://ourworldindata.org/grapher/prevalence-of-undernourishment-in-developing-countries-since-1970
- https://web.archive.org/web/20141123184334/http://www.fao.org/economic/ess/ess-fs/ess-fadata/en/
- https://web.archive.org/web/20150208144716/http://www.fao.org/fileadmin/templates/ess/foodsecurity/Food_Security_Indicators.xlsx
- https://web.archive.org/web/20160317090710/http://www.fao.org/fileadmin/templates/ess/foodsecurity/Food_Security_Indicators.xlsx
- https://ourworldindata.org/grapher/death-rate-from-famines-by-decade.csv
- https://ourworldindata.org/grapher/world-gdp-over-the-last-two-millennia.csv
- https://ourworldindata.org/grapher/gdp-per-capita-maddison-2020.csv
- https://ourworldindata.org/grapher/world-population-in-extreme-poverty-absolute.csv
