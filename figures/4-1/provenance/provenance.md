# Figure 4-1 Provenance

## Evidence

- Title: Tone of the news, 1945-2010
- Primary visual/source reference: Supplemental Graphics PDF page 2.
- Source line: Leetaru 2011. Plotted by month, beginning in January.
- Visible series: New York Times, 1945-2005, and Summary of World Broadcasts, 1979-2010, plotted monthly in standard deviations.
- Kindle-specific confirmation: not performed in this executor session; no artifact is named as a Kindle reference.

## Source Recovery Result

The cited publication is Kalev Leetaru's 2011 First Monday paper, "Culturomics 2.0: Forecasting large-scale human behavior using global news media tone in time and space." The GDELT blog mirrors the original high-resolution Figure 10 and Figure 11 images for the New York Times and Summary of World Broadcasts monthly tone charts. Those files are plot images, not the underlying monthly data.

No inspectable monthly data table for the two series was recovered in this pass or in the 2026-07-09 re-audit. No Pinker or Leetaru plotted values were digitized.

## Targeted Recovery Findings

- First Monday article HTML: Article contains embedded journal JPEGs for Figures 10 and 11 but no supplementary CSV/XLS/ZIP/table link. URLs checked: https://firstmonday.org/ojs/index.php/fm/article/view/3663/3040, https://firstmonday.org/ojs/index.php/fm/article/download/3663/3040?inline=1.
- First Monday landing metadata: Galley points to fulltext HTML; citation metadata exposes DOI 10.5210/fm.v16i9.3663 and no data supplement. URLs checked: https://firstmonday.org/ojs/index.php/fm/article/view/3663.
- GDELT high-resolution mirror: Mirror states original high-resolution figures were externally hosted and mirrors PNG files only; Figure 10 and Figure 11 are images, not data. URLs checked: https://blog.gdeltproject.org/culturomics-2-0-high-resolution-figures/.
- GDELT public data host exact sidecars: PNG files returned 200; candidate CSV/TSV/XLS/XLSX/ZIP/README sidecars returned 404. HTTPS curl failed certificate validation for data.gdeltproject.org. URLs checked: http://data.gdeltproject.org/blog/2011-culturomics-20/figure10.png, http://data.gdeltproject.org/blog/2011-culturomics-20/figure11.png, http://data.gdeltproject.org/blog/2011-culturomics-20/figure10.csv, http://data.gdeltproject.org/blog/2011-culturomics-20/figure11.csv, http://data.gdeltproject.org/blog/2011-culturomics-20/figure10.tsv, http://data.gdeltproject.org/blog/2011-culturomics-20/figure11.tsv, http://data.gdeltproject.org/blog/2011-culturomics-20/figure10.xls, http://data.gdeltproject.org/blog/2011-culturomics-20/figure11.xls, http://data.gdeltproject.org/blog/2011-culturomics-20/figure10.xlsx, http://data.gdeltproject.org/blog/2011-culturomics-20/figure11.xlsx, http://data.gdeltproject.org/blog/2011-culturomics-20/figure10.zip, http://data.gdeltproject.org/blog/2011-culturomics-20/figure11.zip, http://data.gdeltproject.org/blog/2011-culturomics-20/data.zip, http://data.gdeltproject.org/blog/2011-culturomics-20/README.txt.
- Internet Archive: old Culturomics20 host: Archived index advertises Figures 12-18 media assets only; CDX lists movies/civilization/bin Laden files but no Figure 10/11 tables or data sidecars. URLs checked: https://web.archive.org/web/20111003133001id_/http://contentanalysis.ichass.illinois.edu:80/Culturomics20/, https://web.archive.org/cdx?url=contentanalysis.ichass.illinois.edu/Culturomics20/*&output=json&fl=timestamp,original,statuscode,mimetype,digest&filter=statuscode:200&collapse=urlkey.
- Internet Archive: First Monday snapshots: Snapshots inspected at 20130730022936, 20140504052209, 20191122035146, and 20250419132206; same HTML/image pattern, no data supplement link. URLs checked: https://web.archive.org/cdx?url=firstmonday.org/ojs/index.php/fm/article/view/3663/3040&output=json&fl=timestamp,original,statuscode,mimetype,digest&filter=statuscode:200&collapse=digest.
- Repository and data catalog searches: GitHub unauthenticated code search returned 401 Requires authentication; public web searches found no matching dataset; Dataverse targeted API calls timed out and a broad SWB/tone query returned high-volume irrelevant results. URLs checked: https://api.github.com/search/code, https://dataverse.harvard.edu/api/search.

## 2026-07-09 Re-Audit

- Supplemental Graphics PDF page 2 was re-read with `pdftotext`; the visible source line remains: "Leetaru 2011. Plotted by month, beginning in January." The visible chart combines New York Times and Summary of World Broadcasts tone as standard deviations, with the book title range 1945-2010.
- Crossref DOI metadata for `10.5210/fm.v16i9.3663` resolves to Leetaru's 2011 First Monday article and lists HTML full-text links only; no related data object or supplementary data relation is exposed. DataCite search for the DOI returned no records.
- Live GDELT high-resolution page was rechecked. Figures 10 and 11 are listed as PNG links only, with captions matching the New York Times 1945-2005 and Summary of World Broadcasts January 1979-July 2010 monthly tone series.
- Internet Archive CDX for `contentanalysis.ichass.illinois.edu/Culturomics20/*` returned only the archived index and media assets: bin Laden PNG, civilizations PDF/PNG files, and NYT/SWB movie GIFs. It did not list Figure 10/11 data tables or sidecars.
- Internet Archive CDX for `data.gdeltproject.org/blog/2011-culturomics-20/*` returned only an archived SWB movie GIF, not Figure 10/11 tables.
- Authenticated GitHub code search returned no matches for the exact Figure 10 caption, `figure10.png` with `2011-culturomics-20`, `"Summary of World Broadcasts" "Leetaru" "tone"`, or `"Culturomics 2.0" "Leetaru"`.
- Public web search found Leetaru-authored Forbes articles and later commentary that reuse or discuss the NYT/SWB tone timelines. These are evidence-only plot/commentary sources, not downloadable monthly data and not a comparable successor series for reconstruction.

## Reconstruction

No reconstruction data file was accepted. The generated comparison images include a Supplemental PDF reference crop and a source-recovery status panel only.

## Next Action

Recover the underlying monthly Leetaru 2011 tone data for New York Times and Summary of World Broadcasts, or a reproducible corpus/sentiment extraction matching Leetaru's method. If available, confirm the same source line in Kindle during a separate audit.
