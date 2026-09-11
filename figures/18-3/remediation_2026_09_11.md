# September 11 recovery and review

Status: **partial_match**, blocked, publication-incomplete. The earlier source-only
assessment is superseded by a numeric US reconstruction and a Swiss alternative.
The authorized original and both comparisons were opened and inspected.

## Source recovery and citation corrections

Download URLs/timestamps/hashes, including rejected candidates, are preserved in
`data/raw/recovery_downloads_2026_09_11.json`. This pass investigated official CDC
historical tables, Swiss institutional historical workbooks, Cambridge historical
statistics, and the cited journal sources. Exact-source access remains unresolved.

- Swiss HSSO D.50a https://hsso.ch/get/D.50a.xlsx supplies annual suicide counts
  1876-1995. B.42 https://hsso.ch/get/B.42.xlsx supplies year-end permanent residents
  in thousands. Accepted as a transparent alternative, NOT as Ajdacic-Gross's exact rate.
- CDC https://www.cdc.gov/nchs/nvss/mortality/hist290.htm links six historical PDFs
  yielding complete total/all-races/both-sexes crude rates 1900-1998. Extraction keeps
  the first BOTH SEXES block, never male-only rows. Source PDF page is retained per row.
- CDC Data Brief 241 table https://www.cdc.gov/nchs/data/databriefs/db241_table.pdf
  supplies age-adjusted rates 1999-2014. It was published April 2016, NOT 2015;
  consequently it is a recoverable candidate, not a proven exact bibliographic vintage.
- CDC Data Brief 541 https://www.cdc.gov/nchs/data/databriefs/db541.pdf supplies
  the comparable US2000 age-adjusted series 2003-2023. Overlap rates agree but
  the 2014 count changes from 42,773 to 42,826, a 53-death revision.
- CDC archived leading-causes PDF retained but rejected for a complete historical
  series: early top-ten tables can omit suicide and mix sex-specific sections.
- Cambridge https://hsus.cambridge.org/HSUSWeb/toc/treeTablePathIdAb929-951.html
  identifies Ab950. The original image reads **Ab950**, not the old OCR's Abg50.
  Accessible headings did not supply the numeric table; no access claim is made.
- Thomas/Gunnell https://doi.org/10.1093/ije/dyq094 and Ajdacic-Gross
  https://doi.org/10.1007/s00406-005-0627-1 remain exact-source recovery targets.

## Transformations and reproducibility

Run `.venv/bin/python scripts/reconstruct_18_3.py`. Numeric tables, not chart traces,
provide 120 Swiss observations, 99 US historical rates, 16 book-endpoint candidate
rates and 21 successor observations. Swiss rate = deaths / (population_thousands
* 1000) * 100000. This denominator choice is explicit and may differ from the paper.
US pre-1933 coverage is death-registration states, not the full nation. Crude rates
through 1998 and age-adjusted rates from 1999 are not joined across the definition break.
Only the compatible US age-adjusted continuation is dashed beyond 2014. Swiss and
English extensions are not invented. Full clean series and overlap diagnostic retained.

## Visual and editorial findings

Critical for publication: England/Wales is absent. Major: the Swiss alternative has
more annual variability, a higher 1920-era peak and lower mid-century rates than the
original; coverage ends 1995, before the original 2013 endpoint. This cannot be fixed
honestly by smoothing or rescaling to the picture. Major: US source/definition changes
need exact-vintage confirmation although its broad historical shape is similar.
Corrections made: honest labeling, separate definition segments, actual post-2014
dashed extension, explicit missing-series note and comparable axis range.
Minor: fonts and label placement differ. These are research comparisons, not a
publication acceptance. Further source work, not cosmetic manipulation, is needed.

## Reviewer challenge and next action

- Author: where is the supplied English series? Not recovered; request the original
  male/female rates and verify the specified arithmetic averaging.
- Journalist: does early US mean national? No; geographic coverage caveat preserved.
- Peer reviewer: is Swiss rate definition identical? No; alternative clearly labeled.
- Reader: why differing curves/absent line? Caption explains coverage and definitions.

Overall confidence: medium. Book reconstruction: partial. US extension: medium-high.
Source provenance: high for recovered official tables, incomplete for exact citation chain.
Next action: recover author-supplied England/Wales table; reconcile Swiss denominators,
standardization and WHO/OECD version; verify Carter Ab950 and cited CDC2015 vintage.
No outreach sent. These searches are targeted blockers, not exhausted possibilities.

## Acceptance checklist

- [x] Original source inspected; OCR citation corrected.
- [x] Official numeric sources preserved with URLs/hashes and clean transformations.
- [x] Book and extended comparisons opened and inspected.
- [x] US overlap revision tested and extension definition documented.
- [ ] English series recovered and Swiss exact definition reproduced.
- [ ] Full citation-vintage equivalence established.
- [ ] Publication acceptance (not claimed).
