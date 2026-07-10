# Source Log: Figure 10-4

## Supplemental PDF Evidence
- Inspected `references/enlightenment_now_supplemental_graphics.pdf`, page 14.
- Title: `Deforestation, 1700-2010`.
- Source note: `United Nations Food and Agriculture Organization 2012, p. 9.`
- Visible series: `Temperate forest` and `Tropical forest`, plotted in million hectares.
- Surrounding discussion links the figure to environmental rebound and the shift from temperate to tropical forest loss.

## Source Recovery
- Downloaded FAO, *State of the World's Forests 2012*, from `https://www.fao.org/4/i3010e/i3010e.pdf` on 2026-07-09.
- Downloaded the FAO Chapter 2 PDF from `https://www.fao.org/4/i3010e/i3010e02.pdf` on 2026-07-09.
- Located printed page 9, Figure 2: `Estimated deforestation, by type of forest and time period`.
- FAO Figure 2 source note: `Estimates based on Williams, 2002; FAO, 2010b.`
- Extracted PDF text around Figure 2. The period labels and source note are exposed, but the bar heights are not exposed as a numerical table.
- Exact FAO 2010b citation identified in SOFO 2012 references: FAO. 2010b. *Global Forest Resources Assessment 2010 - main report*. FAO Forestry Paper No. 163. Rome. `https://www.fao.org/4/i1757e/i1757e.pdf`.
- Downloaded the FRA 2010 main report and official FRA 2010 Global Tables from the current FAO FRA 2010 page `https://www.fao.org/forest-resources-assessment/past-assessments/fra-2010/en`. The global tables expose 1990, 2000, 2005, and 2010 forest-area and annual net-change values by country/region, but not the SOFO Figure 2 tropical/temperate 1996-2010 production split.
- Retrieved archived FRA 2010 Global Tables from Wayback captures `https://web.archive.org/web/20220121214738if_/http://foris.fao.org/static/data/fra2010/FRA2010Globaltables_English.xls` and `https://web.archive.org/web/20121018091514if_/http://foris.fao.org/static/data/fra2010/FRA2010GlobaltablesEnJune29.xls`. These older workbooks have the same sheet structure and no tropical/temperate/domain field for SOFO Figure 2's final period.
- Retrieved archived FRA 2010 remote-sensing reports `https://web.archive.org/web/20220119130530/http://foris.fao.org/static/data/fra2010/RSS2010update.pdf` and `https://web.archive.org/web/20130304232017/http://foris.fao.org/static/data/fra2010/RSS_Summary_Report_lowres.pdf`. They report forest land-use change by climatic domain for 1990-2005 and 1990-2010, including tropical and temperate domains, but they do not provide the Williams/SOFO period bins or a 1996-2010 tropical/temperate production split for Figure 2.
- Probed the archived `fra2010.zip` static bundle. The Wayback response reports a 569 MB ZIP but warns that content is truncated by time; the partial download could not be unzipped and is not retained as evidence.
- Recovered Williams Table 12.2 values for 1700-1995 from accessible book/snippet text and corroborating reuse: `figures/10-4/data/clean/figure_10_4_williams_recovered_1700_1995.csv`.
- Downloaded the OWID-hosted 2013 FAO image asset from `https://ourworldindata.org/uploads/2013/11/estimated-deforestation-by-type-of-forest-and-time-period-pre-1700-2000-fao-20120-645x422.png`. It is a reused image, not a table.

## Blocker
The Williams component is recovered through 1995, but the FAO 2010b/FRA 2010 calculation that turns FRA data into the 1996-2010 tropical/temperate Figure 2 bar was not recovered. The live and archived FAO materials checked do not provide a production spreadsheet or a table matching SOFO Figure 2. The FRA remote-sensing domain series is methodologically adjacent but not the same period-bar source. Reconstructing from Pinker's plotted values remains prohibited. Digitizing the FAO source graphic, not Pinker's chart, would be an explicitly approximate secondary reconstruction only; it is not treated here as recovered original data.

## Search and Access Attempts
- Query: `"Estimated deforestation, by type of forest and time period" data`; URL checked: FAO SOFO PDF and search results; access date: 2026-07-09; result: source graphic/PDF only, non-tabular.
- Query: `"State of the World's Forests 2012" "Figure 2" "Estimated deforestation"`; URL checked: `https://www.fao.org/4/i3010e/i3010e.pdf` and `https://www.fao.org/4/i3010e/i3010e02.pdf`; access date: 2026-07-09; result: source figure recovered, no values table.
- Query: `"FAO 2010b" "Global Forest Resources Assessment 2010" "main report"`; URL checked: `https://www.fao.org/4/i1757e/i1757e.pdf` and `https://www.fao.org/forest-resources-assessment/past-assessments/fra-2010/en`; access date: 2026-07-09; result: exact citation and official global tables recovered, but only FRA 1990-2010 forest-area/net-change tables.
- Query: `"Deforesting the Earth" "Table 12.2"`; URLs checked: University of Chicago Press page, WorldCat, Google/search snippets, `https://dokumen.pub/deforesting-the-earth-from-prehistory-to-global-crisis-an-abridgment-9780226899053.html`; access date: 2026-07-09; result: publisher/library pages non-tabular, accessible snippet/table recovers Williams 1700-1995 values; not a FAO 1996-2010 table.
- Query: `"Deforesting the Earth" "temperate forest" "tropical forest" "1700" "1849"`; URLs checked: Google/search snippets, Stop Fossil Fuels reuse page, ResearchGate dissertation snippet; access date: 2026-07-09; result: corroborates Williams table/reuse, but secondary/reused or snippet access.
- Query: `site:ourworldindata.org/uploads "estimated-deforestation-by-type-of-forest-and-time-period"`; URL checked: `https://ourworldindata.org/uploads/2013/11/estimated-deforestation-by-type-of-forest-and-time-period-pre-1700-2000-fao-20120-645x422.png`; access date: 2026-07-09; result: image asset only, no data file.
- Query: `site:fao.org/forestry "Estimated deforestation" "xls"` and Wayback CDX probes for `foris.fao.org/static/data/fra2010/*`; access date: 2026-07-09; result: current and archived FRA global tables, remote-sensing reports, maps, and images found, but no SOFO Figure 2 production asset or spreadsheet.
- Query: archived `fra2010.zip` bundle at Wayback capture `20211010084324`; access date: 2026-07-09; result: server reports a 569 MB ZIP but Wayback truncates the response before the central directory, so the bundle could not be verified or used.

## Next Recovery Targets
- Inspect a full authorized copy of Williams, M. 2002, *Deforesting the Earth: From Prehistory to Global Crisis*, to confirm the Table 12.2 values against the original edition rather than accessible snippets/reuses.
- Inspect additional FAO FRA 2010b annexes, FORIS exports, or staff production files for the 1996-2010 components used in Figure 2.
- Search FAO production files, chart source assets, and archived SOFO 2012 supporting files for Figure 2 data.
- If no table exists, document whether digitizing the FAO source graphic, not Pinker's chart, is acceptable for a future approximate reconstruction.
