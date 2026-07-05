# Figure 4-1 Source Log

Date: 2026-07-05

## Accepted For Reconstruction

- None.

## Accepted As Evidence Only

- Supplemental Graphics PDF page 2, figure/source crop.
- Leetaru 2011 First Monday article: https://firstmonday.org/ojs/index.php/fm/article/view/3663/3040
- GDELT high-resolution figure mirror: https://blog.gdeltproject.org/culturomics-2-0-high-resolution-figures/
- Candidate visual files stored locally:
  - `figures/4-1/data/candidates/leetaru_2011_figure10_nyt_tone.png`
  - `figures/4-1/data/candidates/leetaru_2011_figure11_swb_tone.png`
- Supplemental PDF crop stored locally:
  - `figures/4-1/plots/comparisons/supplemental_pdf_reference_figure_4_1.png`

## Rejected Or Unresolved

- Pinker's plotted values: not digitized and not used.
- Leetaru/GDELT PNG plots: rejected as reconstruction data because they are plotted images, not original monthly data.
- Underlying monthly NYT/SWB tone series: not recovered as an inspectable table.
- Corpus-level reproduction: not attempted because the original licensed/proprietary corpora and exact sentiment-processing pipeline were not recovered.

## Targeted Recovery

- First Monday article HTML: Article contains embedded journal JPEGs for Figures 10 and 11 but no supplementary CSV/XLS/ZIP/table link. URLs checked: https://firstmonday.org/ojs/index.php/fm/article/view/3663/3040, https://firstmonday.org/ojs/index.php/fm/article/download/3663/3040?inline=1.
- First Monday landing metadata: Galley points to fulltext HTML; citation metadata exposes DOI 10.5210/fm.v16i9.3663 and no data supplement. URLs checked: https://firstmonday.org/ojs/index.php/fm/article/view/3663.
- GDELT high-resolution mirror: Mirror states original high-resolution figures were externally hosted and mirrors PNG files only; Figure 10 and Figure 11 are images, not data. URLs checked: https://blog.gdeltproject.org/culturomics-2-0-high-resolution-figures/.
- GDELT public data host exact sidecars: PNG files returned 200; candidate CSV/TSV/XLS/XLSX/ZIP/README sidecars returned 404. HTTPS curl failed certificate validation for data.gdeltproject.org. URLs checked: http://data.gdeltproject.org/blog/2011-culturomics-20/figure10.png, http://data.gdeltproject.org/blog/2011-culturomics-20/figure11.png, http://data.gdeltproject.org/blog/2011-culturomics-20/figure10.csv, http://data.gdeltproject.org/blog/2011-culturomics-20/figure11.csv, http://data.gdeltproject.org/blog/2011-culturomics-20/figure10.tsv, http://data.gdeltproject.org/blog/2011-culturomics-20/figure11.tsv, http://data.gdeltproject.org/blog/2011-culturomics-20/figure10.xls, http://data.gdeltproject.org/blog/2011-culturomics-20/figure11.xls, http://data.gdeltproject.org/blog/2011-culturomics-20/figure10.xlsx, http://data.gdeltproject.org/blog/2011-culturomics-20/figure11.xlsx, http://data.gdeltproject.org/blog/2011-culturomics-20/figure10.zip, http://data.gdeltproject.org/blog/2011-culturomics-20/figure11.zip, http://data.gdeltproject.org/blog/2011-culturomics-20/data.zip, http://data.gdeltproject.org/blog/2011-culturomics-20/README.txt.
- Internet Archive: old Culturomics20 host: Archived index advertises Figures 12-18 media assets only; CDX lists movies/civilization/bin Laden files but no Figure 10/11 tables or data sidecars. URLs checked: https://web.archive.org/web/20111003133001id_/http://contentanalysis.ichass.illinois.edu:80/Culturomics20/, https://web.archive.org/cdx?url=contentanalysis.ichass.illinois.edu/Culturomics20/*&output=json&fl=timestamp,original,statuscode,mimetype,digest&filter=statuscode:200&collapse=urlkey.
- Internet Archive: First Monday snapshots: Snapshots inspected at 20130730022936, 20140504052209, 20191122035146, and 20250419132206; same HTML/image pattern, no data supplement link. URLs checked: https://web.archive.org/cdx?url=firstmonday.org/ojs/index.php/fm/article/view/3663/3040&output=json&fl=timestamp,original,statuscode,mimetype,digest&filter=statuscode:200&collapse=digest.
- Repository and data catalog searches: GitHub unauthenticated code search returned 401 Requires authentication; public web searches found no matching dataset; Dataverse targeted API calls timed out and a broad SWB/tone query returned high-volume irrelevant results. URLs checked: https://api.github.com/search/code, https://dataverse.harvard.edu/api/search.

## Durable Blocker Rationale

The only recovered Figure 10/11 objects are plot images embedded in First Monday or mirrored by GDELT. The project rule forbids digitizing Pinker's chart or Leetaru/GDELT plot images as source data. The original corpora are not included in the public article package, and no inspectable monthly table or reproducible extraction package was recovered.
