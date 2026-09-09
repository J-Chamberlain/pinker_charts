# Provenance: Figure 7-3

Book/PDF figure -> source note -> archived FAO page and workbook recovery -> `scripts/reconstruct_7_3.py` -> regenerated review artifacts.

Book source note: Our World in Data, Roser 2016j, based on data from the Food and Agriculture Organization 2014, also reported in FAOSTAT.

Recovered source trail:

- Supplemental PDF page 6 gives the figure image, title, and source note.
- Internet Archive snapshots of `http://www.fao.org/economic/ess/ess-fs/ess-fadata/en/` show the FAO Food Security Indicators page. The November 23, 2014 snapshot links `http://bit.ly/14FRxGV` as "Download data" and states "Last updated: 17 November 2014"; the page lists "Prevalence of undernourishment" coverage as 1990-2014.
- The archived `bit.ly/14FRxGV` target resolves to `http://www.fao.org/fileadmin/templates/ess/foodsecurity/Food_Security_Indicators.xlsx`. Internet Archive preserved a February 8, 2015 capture of that workbook and a March 17, 2016 capture.
- The March 17, 2016 archived workbook, sheet `V_2.6 - Prevalence of undernourishment`, contains `Developing countries`, `Sub-Saharan Africa`, `South-Eastern Asia`, `Southern Asia`, `Eastern Asia`, and `Latin America` through `2014-16`. Three-year windows are plotted at midpoint years, so `2014-16` is plotted as 2015.
- The 1970 and 1980 developing-world values are from OWID's long-run developing-country FAO chart. OWID metadata says these two values are averages of FAO SOFI 2006 and 2010 estimates; all later developing-country values are from FAO Food Security Indicators.

Editorial decision: `partial_match` with `medium` confidence.

The source recovery is much stronger than the previous remediation because the named regional curves and early-1990s coverage are now recovered from an archived FAO workbook. It is still not a verified reproduction: the complete 1991-2015 regional reconstruction uses the archived 2016 workbook, while the book source note cites Roser 2016j based on FAO 2014. The recovered November 2014 workbook is citable provenance but does not itself extend to the 2015 endpoint.
