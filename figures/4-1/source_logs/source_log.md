# Source Discovery Log: Figure 4-1

- Figure number: 4-1
- Figure title: Tone of the news, 1945-2010
- Original book citation: Leetaru 2011. Plotted by month, beginning in January.
- Reproduction status: blocked_external_source
- Confidence score: 0.22

## Search Queries Attempted

- Leetaru 2011 Tone of news coverage standard deviations 1945 2010 data
- "Tone of news coverage" "Leetaru"
- "Culturomics 2.0" "tone" data
- site:data.gdeltproject.org culturomics figure 10 csv "Average monthly tone"
- "Average monthly tone of New York Times news content" csv
- "Figure 10" "Average monthly tone" "New York Times" "data.gdeltproject.org"

## Sources Investigated

### Supplemental Graphics PDF

- Path: `references/enlightenment_now_supplemental_graphics.pdf`
- Decision: accepted_reference
- Rationale: Primary visual reference. Page 2 confirms title, year range,
  plotted units, and source line.

### First Monday article: Culturomics 2.0

- URL: https://firstmonday.org/ojs/index.php/fm/article/view/3663/3040
- Decision: accepted_context
- Rationale: Cited Leetaru 2011 article. The article context supports the
  source family but did not expose a month-level source-data table during this
  pass.

### GDELT Culturomics 2.0 high-resolution figure mirror

- URL: https://blog.gdeltproject.org/culturomics-2-0-high-resolution-figures/
- Decision: accepted_source_visual_only
- Rationale: The mirror identifies Figure 10 as average monthly tone of New
  York Times news content, 1945-2005, and Figure 11 as average monthly tone of
  Summary of World Broadcasts news content, January 1979-July 2010. These match
  the two series shown in Pinker's figure but are plotted images, not data.

### GDELT Figure 10 PNG

- URL: http://data.gdeltproject.org/blog/2011-culturomics-20/figure10.png
- Local path: `data/candidates/gdelt_culturomics_figure10_nyt_1945_2005.png`
- Decision: accepted_source_visual_only
- Rationale: Source visual for NYT monthly tone. Not used as data.

### GDELT Figure 11 PNG

- URL: http://data.gdeltproject.org/blog/2011-culturomics-20/figure11.png
- Local path: `data/candidates/gdelt_culturomics_figure11_swb_1979_2010.png`
- Decision: accepted_source_visual_only
- Rationale: Source visual for SWB monthly tone. Not used as data.

### Obvious GDELT CSV/XLS companion paths

- URLs checked:
  - http://data.gdeltproject.org/blog/2011-culturomics-20/figure10.csv
  - http://data.gdeltproject.org/blog/2011-culturomics-20/figure11.csv
  - http://data.gdeltproject.org/blog/2011-culturomics-20/figure10.xls
  - http://data.gdeltproject.org/blog/2011-culturomics-20/figure11.xls
- Decision: rejected_not_found
- Rationale: Each returned HTTP 404.

### Internet Archive CDX

- Local paths:
  - `data/candidates/wayback_gdelt_figure10_cdx.json`
  - `data/candidates/wayback_gdelt_figure11_cdx.json`
- Decision: accepted_context
- Rationale: Recorded archive evidence for the source images. No archived
  source-data table was located.

## Downloaded Files

- `data/raw/gdelt_culturomics_high_res_figures.html`
- `data/raw/leetaru_2011_first_monday.html`
- `data/candidates/gdelt_culturomics_figure10_nyt_1945_2005.png`
- `data/candidates/gdelt_culturomics_figure11_swb_1979_2010.png`
- `data/candidates/wayback_gdelt_figure10_cdx.json`
- `data/candidates/wayback_gdelt_figure11_cdx.json`

## Remaining Uncertainties

- The original monthly numeric values behind Leetaru 2011 Figures 10 and 11
  remain unrecovered.
- Pinker's combined plotting transform may include visual rescaling or
  restyling relative to the source figures; this cannot be validated without
  numeric data.
