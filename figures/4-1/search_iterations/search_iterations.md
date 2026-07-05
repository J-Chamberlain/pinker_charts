# Figure 4-1 Search Iterations

Date: 2026-07-05

## Queries And URLs Checked

Search terms included:

- `Leetaru 2011 Culturomics 2.0 Figure 10 New York Times tone data CSV`
- `"Summary of World Broadcasts" "tone" "Leetaru" "data"`
- `"Culturomics 2.0" "Figure 10" "New York Times" "tone"`
- `"gdelt" "Figure 11" "Summary of World Broadcasts" "tone"`
- `"contentanalysis.ichass.illinois.edu/Culturomics20"`
- `"Culturomics20" "figure10"`
- `"Average monthly tone of New York Times news content 1945-2005" "csv"`
- `site:github.com Leetaru Culturomics 2.0 figure10`
- `site:dataverse.harvard.edu Leetaru Culturomics 2.0`
- `site:gdeltproject.org Summary World Broadcasts tone monthly`

Archive timestamps inspected:

- First Monday article CDX examples: 20130730022936, 20140504052209, 20191122035146, 20250419132206.
- Old `contentanalysis.ichass.illinois.edu/Culturomics20/` index: 20111003133001.
- Old `contentanalysis.ichass.illinois.edu/Culturomics20/*` CDX captures: 20111114173938, 20120119004300, 20120119020351, 20120119062451, 20120119203428, 20120120003341, 20120120035719, 20120120072028.

Findings:

- First Monday article HTML: Article contains embedded journal JPEGs for Figures 10 and 11 but no supplementary CSV/XLS/ZIP/table link. URLs checked: https://firstmonday.org/ojs/index.php/fm/article/view/3663/3040, https://firstmonday.org/ojs/index.php/fm/article/download/3663/3040?inline=1.
- First Monday landing metadata: Galley points to fulltext HTML; citation metadata exposes DOI 10.5210/fm.v16i9.3663 and no data supplement. URLs checked: https://firstmonday.org/ojs/index.php/fm/article/view/3663.
- GDELT high-resolution mirror: Mirror states original high-resolution figures were externally hosted and mirrors PNG files only; Figure 10 and Figure 11 are images, not data. URLs checked: https://blog.gdeltproject.org/culturomics-2-0-high-resolution-figures/.
- GDELT public data host exact sidecars: PNG files returned 200; candidate CSV/TSV/XLS/XLSX/ZIP/README sidecars returned 404. HTTPS curl failed certificate validation for data.gdeltproject.org. URLs checked: http://data.gdeltproject.org/blog/2011-culturomics-20/figure10.png, http://data.gdeltproject.org/blog/2011-culturomics-20/figure11.png, http://data.gdeltproject.org/blog/2011-culturomics-20/figure10.csv, http://data.gdeltproject.org/blog/2011-culturomics-20/figure11.csv, http://data.gdeltproject.org/blog/2011-culturomics-20/figure10.tsv, http://data.gdeltproject.org/blog/2011-culturomics-20/figure11.tsv, http://data.gdeltproject.org/blog/2011-culturomics-20/figure10.xls, http://data.gdeltproject.org/blog/2011-culturomics-20/figure11.xls, http://data.gdeltproject.org/blog/2011-culturomics-20/figure10.xlsx, http://data.gdeltproject.org/blog/2011-culturomics-20/figure11.xlsx, http://data.gdeltproject.org/blog/2011-culturomics-20/figure10.zip, http://data.gdeltproject.org/blog/2011-culturomics-20/figure11.zip, http://data.gdeltproject.org/blog/2011-culturomics-20/data.zip, http://data.gdeltproject.org/blog/2011-culturomics-20/README.txt.
- Internet Archive: old Culturomics20 host: Archived index advertises Figures 12-18 media assets only; CDX lists movies/civilization/bin Laden files but no Figure 10/11 tables or data sidecars. URLs checked: https://web.archive.org/web/20111003133001id_/http://contentanalysis.ichass.illinois.edu:80/Culturomics20/, https://web.archive.org/cdx?url=contentanalysis.ichass.illinois.edu/Culturomics20/*&output=json&fl=timestamp,original,statuscode,mimetype,digest&filter=statuscode:200&collapse=urlkey.
- Internet Archive: First Monday snapshots: Snapshots inspected at 20130730022936, 20140504052209, 20191122035146, and 20250419132206; same HTML/image pattern, no data supplement link. URLs checked: https://web.archive.org/cdx?url=firstmonday.org/ojs/index.php/fm/article/view/3663/3040&output=json&fl=timestamp,original,statuscode,mimetype,digest&filter=statuscode:200&collapse=digest.
- Repository and data catalog searches: GitHub unauthenticated code search returned 401 Requires authentication; public web searches found no matching dataset; Dataverse targeted API calls timed out and a broad SWB/tone query returned high-volume irrelevant results. URLs checked: https://api.github.com/search/code, https://dataverse.harvard.edu/api/search.
