# Consolidated Research History: Figure 4-1

These are historical search records, not the current acceptance decision.

## Local Work At efca1264944eabab2f733bc399027e22b8df6381

# Figure 4-1 Search Iterations

Date: 2026-07-09

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

## 2026-07-09 Additional Queries And Checks

Additional public web queries:

- `"Leetaru" "New York Times" "1945" "2005" "tone"`
- `"Average monthly tone" "New York Times" "1945" "2005"`
- `"Average monthly tone" "Summary of World Broadcasts"`
- `"figure11.png" "culturomics-20"`
- `"Sentiment Mining 500 Years Of History" "Average tone of all New York Times"`
- `"The timeline below shows the standardized" "BBC Monitoring" "January 1979" "July 2010"`

Additional endpoint and archive checks:

- Crossref API for DOI `10.5210/fm.v16i9.3663`: article metadata only, no supplement relation.
- DataCite API query for DOI `10.5210/fm.v16i9.3663`: zero records.
- Internet Archive CDX for `contentanalysis.ichass.illinois.edu/Culturomics20/*`: archived index and media assets only.
- Internet Archive CDX for `data.gdeltproject.org/blog/2011-culturomics-20/*`: one archived SWB movie GIF only.
- GDELT guessed sidecars `figure10.dat`, `figure11.dat`, `figure10.txt`, and `figure11.txt`: 404 responses.

Authenticated GitHub code searches:

- `"Average monthly tone of New York Times news content"`
- `"figure10.png" "2011-culturomics-20"`
- `"Summary of World Broadcasts" "Leetaru" "tone"`
- `"Culturomics 2.0" "Leetaru"`

Result: no public GitHub code/data matches. Public web results surfaced Leetaru Forbes articles and media commentary that quote or reuse the timelines, but no downloadable monthly NYT/SWB table or reproducible extraction package.


## GitHub Recovery At 9a19519494ec20f45b3ac3e6b3122d38a2bc0892

# Search iterations - Figure 4-1

## 2026-07-10

1. Searched for the Supplemental Graphics PDF and exact figure title. Located
   an indexed 39-page supplemental document page exposing page-1 text and the
   complete Figure 4-1 source line, but not an unauthenticated PDF download.
2. Resolved "Leetaru 2011" to the First Monday article by DOI and downloaded
   its legacy HTML.
3. Read the method, corpus descriptions, Figure 10/11 captions, and surrounding
   results. Confirmed that Pinker's lines are those two monthly series.
4. Located GDELT's 2019 restoration of the author-supplied high-resolution
   figures and downloaded both originals.
5. Searched for CSV, spreadsheet, supplemental data, code, monthly values, and
   filenames on GDELT and the web. None were found.
6. Queried the Internet Archive for the old ICHASS host. The wildcard CDX
   request returned HTTP 503; exact-name and broader indexed searches did not
   reveal numeric data.
7. Evaluated current GDELT products and rejected them as a successor because
   they do not preserve the same source population or sentiment method.
