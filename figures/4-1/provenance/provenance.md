# Figure 4-1 Provenance

## Evidence

- Title: Tone of the news, 1945-2010
- Primary visual/source reference: Supplemental Graphics PDF page 2.
- Source line: Leetaru 2011. Plotted by month, beginning in January.
- Visible series: New York Times, 1945-2005, and Summary of World Broadcasts, 1979-2010, plotted monthly in standard deviations.
- Kindle-specific confirmation: not performed in this executor session; no artifact is named as a Kindle reference.

## Source Recovery Result

The cited publication is Kalev Leetaru's 2011 First Monday paper, "Culturomics 2.0: Forecasting large-scale human behavior using global news media tone in time and space." The GDELT blog mirrors the original high-resolution Figure 10 and Figure 11 images for the New York Times and Summary of World Broadcasts monthly tone charts. Those files are plot images, not the underlying monthly data.

No inspectable monthly data table for the two series was recovered in this pass. No Pinker or Leetaru plotted values were digitized.

## Targeted Recovery Findings

- First Monday article HTML: Article contains embedded journal JPEGs for Figures 10 and 11 but no supplementary CSV/XLS/ZIP/table link. URLs checked: https://firstmonday.org/ojs/index.php/fm/article/view/3663/3040, https://firstmonday.org/ojs/index.php/fm/article/download/3663/3040?inline=1.
- First Monday landing metadata: Galley points to fulltext HTML; citation metadata exposes DOI 10.5210/fm.v16i9.3663 and no data supplement. URLs checked: https://firstmonday.org/ojs/index.php/fm/article/view/3663.
- GDELT high-resolution mirror: Mirror states original high-resolution figures were externally hosted and mirrors PNG files only; Figure 10 and Figure 11 are images, not data. URLs checked: https://blog.gdeltproject.org/culturomics-2-0-high-resolution-figures/.
- GDELT public data host exact sidecars: PNG files returned 200; candidate CSV/TSV/XLS/XLSX/ZIP/README sidecars returned 404. HTTPS curl failed certificate validation for data.gdeltproject.org. URLs checked: http://data.gdeltproject.org/blog/2011-culturomics-20/figure10.png, http://data.gdeltproject.org/blog/2011-culturomics-20/figure11.png, http://data.gdeltproject.org/blog/2011-culturomics-20/figure10.csv, http://data.gdeltproject.org/blog/2011-culturomics-20/figure11.csv, http://data.gdeltproject.org/blog/2011-culturomics-20/figure10.tsv, http://data.gdeltproject.org/blog/2011-culturomics-20/figure11.tsv, http://data.gdeltproject.org/blog/2011-culturomics-20/figure10.xls, http://data.gdeltproject.org/blog/2011-culturomics-20/figure11.xls, http://data.gdeltproject.org/blog/2011-culturomics-20/figure10.xlsx, http://data.gdeltproject.org/blog/2011-culturomics-20/figure11.xlsx, http://data.gdeltproject.org/blog/2011-culturomics-20/figure10.zip, http://data.gdeltproject.org/blog/2011-culturomics-20/figure11.zip, http://data.gdeltproject.org/blog/2011-culturomics-20/data.zip, http://data.gdeltproject.org/blog/2011-culturomics-20/README.txt.
- Internet Archive: old Culturomics20 host: Archived index advertises Figures 12-18 media assets only; CDX lists movies/civilization/bin Laden files but no Figure 10/11 tables or data sidecars. URLs checked: https://web.archive.org/web/20111003133001id_/http://contentanalysis.ichass.illinois.edu:80/Culturomics20/, https://web.archive.org/cdx?url=contentanalysis.ichass.illinois.edu/Culturomics20/*&output=json&fl=timestamp,original,statuscode,mimetype,digest&filter=statuscode:200&collapse=urlkey.
- Internet Archive: First Monday snapshots: Snapshots inspected at 20130730022936, 20140504052209, 20191122035146, and 20250419132206; same HTML/image pattern, no data supplement link. URLs checked: https://web.archive.org/cdx?url=firstmonday.org/ojs/index.php/fm/article/view/3663/3040&output=json&fl=timestamp,original,statuscode,mimetype,digest&filter=statuscode:200&collapse=digest.
- Repository and data catalog searches: GitHub unauthenticated code search returned 401 Requires authentication; public web searches found no matching dataset; Dataverse targeted API calls timed out and a broad SWB/tone query returned high-volume irrelevant results. URLs checked: https://api.github.com/search/code, https://dataverse.harvard.edu/api/search.

## Reconstruction

No reconstruction data file was accepted. The generated comparison images include a Supplemental PDF reference crop and a source-recovery status panel only.

## Next Action

Recover the underlying monthly Leetaru 2011 tone data for New York Times and Summary of World Broadcasts, or a reproducible corpus/sentiment extraction matching Leetaru's method. If available, confirm the same source line in Kindle during a separate audit.
