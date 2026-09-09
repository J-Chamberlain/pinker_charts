# Figure 17-6 Provenance

## Book Evidence

"Leisure time, US, 1965-2015", supplied Supplemental Graphics PDF p35 lower
panel. Title, axes, source note and both series visually inspected. Book source:
Aguiar and Hurst 2007 Table III, Leisure Measure 1, for 1965-2003; BLS 2016c
ATUS 2015 for the endpoint, adding leisure/sports, lawn/garden care and
volunteering. Kindle surrounding discussion and the author's final plotting
file were not recovered in this pass.

## Original Numeric Evidence

Aguiar, Mark, and Erik Hurst. 2007. Measuring Trends in Leisure: The Allocation
of Time Over Five Decades. Quarterly Journal of Economics 122(3): 969-1006.
https://doi.org/10.1162/qjec.122.3.969

Author-hosted paper: https://www.markaguiar.com/files/leisuretrends.pdf
Table III: PDF page 9, printed page 977. Extracted the five Measure 1 values
for each sex, not graph coordinates. The September 2006 manuscript Table 3
on PDF page 38 has the same ten values. Both table extracts are retained.
Full publisher/manuscript PDFs stay in local retrieval cache, identified by
SHA-256 in the download log and extraction script; no full-paper redistribution.

The author's current research page links the original replication archive:
https://www.markaguiar.com/
https://www.dropbox.com/scl/fo/g3mi6dmg2ehwljty1l0ld/AG25K690ppAR-qRUCncFdAE?rlkey=v05wqn6v0hd9md0xy3s5n8t9i&dl=1

The archive was downloaded (158,690,888 bytes). Its full entry manifest and
hashes are retained. `cells.dta` (360 demographic cells, 53 variables) and
`merged_datasets.zip` (compact original analysis microdata, not needed to
replot) are preserved unchanged in `data/raw/`. The author Stata code was
inspected, not executed or redistributed. Its Table 3 regression on year
indicators without a constant and with analytic `cell_weight` weights reduces
to a weighted mean for each year/sex. The Python reconstruction implements
that weighted mean independently, retaining unrounded values and rounding to
two decimals to cross-check every published Table III entry exactly. Float64
arithmetic avoids accidental float32 comparison discrepancies.

The historical population is nonretired, nonstudent adults 21-65 with fixed
demographic weights. The paper's Measure 1 includes pet care. The BLS endpoint
is civilian noninstitutional population 15+, not fixed-demographic adjusted,
and the book's three-category BLS calculation does not add pet care. These
differences prevent a homogeneous long-run interpretation. The source's
post-1993 childcare measurement change also complicates the female decline.

## BLS Endpoint And Continuation

Original June 24, 2016 release:
https://www.bls.gov/news.release/archives/atus_06242016.htm

Direct HTML returned 403; the public browser table worked. Table 1 is retained
as HTML. Its six selected male/female component values independently agree
with the official 2015 A-1 PDF. Multiply the daily sum by seven: 2015 men
41.93 hours/week, women 35.98. These are all-person means, not means conditional
on participating in the activities. No observations are adjusted to match
Pinker visually.

Continuation: https://www.bls.gov/tus/tables.htm . Actual annual PDF links
and retrieval date are in `data/raw/bls_table_urls.json`; all ten available
2015-2025 A-1 PDFs are retained. 2020 is absent because collection stopped
for two months; BLS says an annual estimate cannot be produced. The script
inserts a plotting gap, not an interpolation. 2025 endpoints: men 41.65,
women 35.07 hours/week. The retained detailed table extracts also preserve
total-sex estimates and pet-care values for reuse/diagnostics.

## Transformations And Figure Decisions

Book line: original weighted analysis-cell means, rounded to published two
decimals, for 1965/1975/1985/1993/2003, then the original 2015 BLS basket.
Scale is 29-43 hours/week. Male light gray and female black. The 2003-2015
connector is intentionally dotted to disclose the population change, unlike
the book's uninterrupted solid connector. Subsequent BLS estimates are dashed;
no annual 2020 is invented. Diagnostic adds pet care to show the activity
definition sensitivity; it is not substituted for the book basket.

The original publication, manuscript and author data agree. Small remaining
book-level differences cannot be fixed by changing source values or styling.
Status `partial_match` reflects those differences and the unresolved author
assembly. Source fidelity is high; faithful homogeneous-trend interpretation
is not established. A targeted next step is recovering Pinker's final table
or reproducing matched-population ATUS estimates as a distinct diagnostic.

## Reuse, Reproduction, Rights

`python scripts/reconstruct_17_6.py` works offline from retained datasets and
tables. `python scripts/recover_17_6_tables.py` regenerates numeric extracts
when the three hashed source archives/PDFs in its documented local cache are
available. The plot has no dependency on those temporary caches. Lineage maps
author cells, table cross-checks, BLS PDFs, extracted observations and outputs.
The shared SQLite library includes all clean cells/activities and plot data.

Freeze author data and the 2015 release. Append a new BLS A-1 release only
after verifying labels, all-person columns, coverage and missing-year rules.
No paid model API is required. BLS attribution is retained. Author replication
data have a public research download, but no blanket redistribution license
was found; resolve publication licensing before exposing the full analysis
microdata on a website. Numeric tables and our own transformations remain
separately inspectable. No claim of permission for unrestricted book images.
