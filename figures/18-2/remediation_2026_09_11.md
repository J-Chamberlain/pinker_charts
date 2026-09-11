# September 11 recovery and review

This audit supersedes earlier statements that neither numeric component is available.
Status: **partial_match**, blocked and publication-incomplete. The college fitted line
is now reconstructed from published coefficients, not digitized pixels.

## Sources investigated

The authorized supplemental PDF and recreated comparison were opened and inspected.
Clark, Loxton and Tobin (2015), DOI 10.1177/0146167214557007, is the exact cited work.
The QUT landing page https://eprints.qut.edu.au/124698/ returned 403, but the legitimate
institutional manuscript download succeeded:
https://eprints.qut.edu.au/124698/1/Clark_decling%20loneliness.pdf .
Download attempts/hashes are retained in `data/raw/recovery_downloads_2026_09_11.json`.
The full PDF is local-only because its notice does not authorize redistribution.
The numerical coefficients and transformed data are committed and rebuildable offline.

Publisher supplementary download attempted again:
https://journals.sagepub.com/doi/suppl/10.1177/0146167214557007/suppl_file/10.1177_0146167214557007_online_supplementary_material_1.pdf
returned 403. This is an access failure, not proof that data no longer exist.
Search query `"0146167214557007" "figshare"` found no identified mirror.
The manuscript explicitly places study-level means and citations in the supplement.
Pooled Table 2 and factor loadings are not substitutes for the triennial grade means.

## College component

Printed page 8 gives slope -0.082 and intercept 199.989, with fitted endpoints
37.793 (1978) and 35.251 (2009). `scripts/reconstruct_18_2.py` extracts the coefficient
sentence and evaluates that equation. The output's 32 rows are fitted values, NOT 32
independent annual observations. No plotted coordinates were used. The sample is 48
studies, N=13,041; this pass does not re-estimate their sample-size-weighted regression.
The paper reports average individual SD 9.85, not between-study SD.

## MTF recovery specification

The manuscript resolves previously uncertain forms: grade 12 form 5 (1977-2012);
grades 8/10 form 1 (1991-2004), form 3 (1997-2012), combining both in overlap years.
Six agreement items use a 1-5 scale: three isolation items retain direction; the
three support/friendship items are reversed. Survey sampling weights are required.
Recover item IDs and missing-value rules from each public-use codebook before computing
respondent scores and triennial grade means. Do not average grade/form means equally.
The 2012 citations identify ICPSR 34574.v1 (8/10) and 34861.v1 (12), not the older
2011 package 34409. Official route: https://www.icpsr.umich.edu/sites/icpsr/view/collections/35 .
Sample-count inconsistencies within the accepted manuscript must be resolved against
the final supplement before claiming replication; its abstract says 385,153.

## Visual and editorial review

College decline is similar but starts lower/earlier than the book and ends in 2009
rather than the book's apparent 2010 placement. The source equation is retained as
reported, not shifted to achieve a match. Source-version/rounding and x-coordinate
choices need checking against the final paper. All three school-grade curves are
missing; their unrelated right axis is intentionally omitted and absence labeled.
Minor panel/font differences remain. No fabricated extended plot was generated.
The comparison is a genuine but incomplete reconstruction, not publication-ready.

## Reviewer challenge and next action

- Author: does this rerun the meta-analysis? No, only its reported fitted equation.
- Journalist: are interpolated rows annual measurements? No, they are labeled fits.
- Peer reviewer: can the six-item score be rebuilt? Forms are now known; item-level
  extraction, version reconciliation and aggregation remain to be done.
- Reader: why three missing curves? Exact tables/microdata are not recovered yet.

Overall confidence: medium. Book reconstruction: partial. Extension: unavailable.
Source provenance: high for printed coefficients. Outstanding risks: publication
version and school-grade harmonization. Next action: recover final supplementary
tables through normal institutional access or author request, then MTF fallback.
No outreach was sent. Do not classify a 403 response as exhaustive source recovery.

## Acceptance checklist

- [x] Original figure, citation and institutional manuscript inspected.
- [x] Published numeric coefficients extracted and tested against printed endpoints.
- [x] Book comparison inspected; omitted series and date differences explained.
- [ ] Meta-analysis inputs/supplement recovered.
- [ ] All school-grade curves reconstructed.
- [ ] Comparable extension recovered.
- [ ] Publication acceptance (not claimed).
