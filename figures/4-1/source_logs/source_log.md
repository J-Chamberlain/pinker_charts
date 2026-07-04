# Figure 4-1 Source Log

Date: 2026-07-04

## Confirmed Reference

- Supplemental Graphics PDF page 2: top chart inspected and cropped.
- Source line: Leetaru 2011. Plotted by month, beginning in January.
- The task requested Kindle confirmation before source recovery; the local workflow now designates the Supplemental Graphics PDF as the primary reference. No Kindle artifact was available in this workspace, so the PDF source line is the confirmed source evidence for this pass.

## Accepted Evidence, Not Reconstruction Data

- Leetaru 2011 First Monday article: `https://firstmonday.org/ojs/index.php/fm/article/download/3663/3040`.
- GDELT mirror, Leetaru Figure 10 NYT plotted image: `https://data.gdeltproject.org/blog/2011-culturomics-20/figure10.png`.
- GDELT mirror, Leetaru Figure 11 SWB plotted image: `https://data.gdeltproject.org/blog/2011-culturomics-20/figure11.png`.
- Wayback CDX for old Culturomics20 host: `https://web.archive.org/cdx?url=contentanalysis.ichass.illinois.edu/Culturomics20/*&output=json&fl=timestamp,original,statuscode,mimetype,digest&filter=statuscode:200&collapse=urlkey`.

These artifacts support the source chain and visual reference but are not accepted as reconstruction data because they do not expose the underlying monthly values.

## Rejected Or Unavailable Paths

- Direct old host checks for likely CSV names under `contentanalysis.ichass.illinois.edu/Culturomics20/` failed because the host no longer resolves.
- Wayback CDX listing for the old directory returned only the root HTML, map/movie images, and a network PDF; no monthly NYT/SWB tone CSV, TXT, XLS, or JSON tables were listed.
- GDELT's 2019 mirror explicitly republishes high-resolution images for article figures 10 and 11, not data tables.
- The First Monday article text includes method details and plotted figures, but no supplemental dataset link or table.

## Blocker

Original monthly tone tables remain unrecovered. Do not digitize Pinker's plotted values or Leetaru's plotted values to create a data series.
