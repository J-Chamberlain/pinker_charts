# Provenance - Figure 4-1

## Status and scope

Status: `source_unavailable`. This run identified the original analysis and the
specific reason the numeric source cannot presently be recovered. It did not
reconstruct, extend, or verify the book figure.

## Book evidence

The indexed first page of Steven Pinker's *Enlightenment Now: Supplemental
Graphics* gives:

- title: "Figure 4-1: Tone of the news, 1945-2010";
- y-axis: "Tone of news coverage (standard deviations)", -3 to 3;
- x-axis: 1945-2010;
- series: "New York Times" and "Summary of World Broadcasts";
- note: "Source: Leetaru 2011. Plotted by month, beginning in January."

The same indexed page shows the NYT line beginning in 1945 and ending in 2005,
and the SWB line beginning in 1979 and ending in 2010. The downloadable PDF was
not exposed without an account by the available host; therefore this evidence is
text-indexed rather than a locally stored PDF page. This limitation is explicit
and prevents claiming a direct Kindle/PDF visual verification.

Pinker's surrounding discussion, also published as an adapted excerpt in *The
Guardian*, says that Kalev Leetaru applied sentiment mining to every *New York
Times* article from 1945-2005 and to translated articles and broadcasts from 130
countries from 1979-2010. Pinker describes the NYT as becoming more negative
from the early 1960s into the early 1970s, partially recovering, then worsening
again in the 2000s; he describes the international archive as becoming gloomier.

## Resolved bibliography

Leetaru, Kalev H. 2011. "Culturomics 2.0: Forecasting Large-Scale Human
Behavior Using Global News Media Tone in Time and Space." *First Monday* 16
(9). DOI: https://doi.org/10.5210/fm.v16i9.3663.

The publisher article is stored as
`data/candidates/leetaru_2011_article_legacy.html`. Its Figures 10 and 11 are the
two component series Pinker combined. GDELT's 2019 mirror states that it hosts
the original high-resolution figures after the earlier external host disappeared.
Those files are stored as `leetaru_2011_figure10_nyt.png` and
`leetaru_2011_figure11_swb.png`.

## Original data and method

Leetaru identifies the input populations precisely:

- complete full text of 5.9 million NYT articles, 1 January 1945 through
  31 December 2005, totaling 2.9 billion words;
- 3.9 million SWB articles, January 1979 through July 2010; and
- monthly aggregation, displayed as standard deviations from each series mean.

The article says sentiment mining counted words in precompiled positive and
negative dictionaries and that the algorithms were adapted from the Carbon
Capture Report. It also says more than 1,500 dictionary categories were tested,
but does not identify a fixed final word list, publish code, or provide the
monthly aggregate values. The article page offers HTML and figures only. The
2019 GDELT mirror offers original high-resolution images only. Targeted web and
archive searches found no CSV, spreadsheet, repository, supplement, or machine-
readable table for Figures 10-11.

Thus the original dataset is identified as two derived monthly series computed
from the licensed NYT and SWB corpora, but the derived values are unpublished.
Recomputing them would additionally require the unreleased exact sentiment
configuration. The stored PNGs are citable primary-source visual evidence, not
a numeric dataset.

## Archive and successor review

The original `contentanalysis.ichass.illinois.edu/Culturomics20/` figure host is
no longer live. GDELT restored the author-supplied high-resolution figures at:

- https://blog.gdeltproject.org/culturomics-2-0-high-resolution-figures/
- https://data.gdeltproject.org/blog/2011-culturomics-20/figure10.png
- https://data.gdeltproject.org/blog/2011-culturomics-20/figure11.png

Internet Archive wildcard/CDX lookup of the former host returned a service
error during this run; ordinary indexed archive and web searches found images
but no data files. Current GDELT event/GKG products are not accepted as a
successor extension: they use different source collections, coverage rules,
and tone variables, and do not continue the licensed NYT/SWB monthly series
under Leetaru's 2011 method.

## Reconstruction decision

No values were digitized from either source plot. That would create approximate
pixel measurements rather than recovered data and would violate the project's
data-fidelity rule. Consequently there is no book-period reconstruction, no
fidelity tolerance claim, and no extension. The source-evidence panel preserves
the original component plots at their published axes and labels without
presenting them as a recreated Figure 4-1.
