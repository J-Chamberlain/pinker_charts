# Figure 5-3 Review Checklist

## Figure

- Figure ID: 5-3
- Title: Maternal mortality, 1751-2013
- Reviewer: Codex source-recovery run
- Review date: 2026-07-09
- Current status: `partial_match`

## Phase 1 - Evidence Review

- [x] Supplemental PDF figure inspected.
- [x] Title extracted.
- [x] Source note extracted.
- [x] Surrounding discussion reviewed.
- [x] Bibliography resolved to Roser 2016p, *Maternal Mortality*, Our World in Data.

## Phase 2 - Source Review

- [x] Original Gapminder GD010 source component located.
- [x] Source chain documented.
- [x] Dataset provenance documented.
- [x] Archive search completed for OWID article/grapher targets.
- [x] Modern successor substitution explained where used.
- [x] Download URLs recorded.
- [x] Checksums recorded.
- [ ] Complete book-era OWID/World Bank 2015 machine-readable source recovered.

## Phase 3 - Reconstruction Review

- [x] Reconstruction uses legitimate data.
- [x] No digitized figure values used as reconstruction data.
- [x] Transformation code is reproducible in `scripts/reconstruct_5_3.py`.
- [x] Scales and labels are correct for the book figure.
- [x] Book-period reconstruction completed.
- [x] Book-period side-by-side comparison generated.
- [x] Major visible discrepancy from missing Malaysia history corrected.
- [x] Remaining discrepancies explained.

## Phase 4 - Extension Review

- [x] Later/current data searched.
- [x] Later/current data documented.
- [x] No verified comparable extension asserted.
- [x] Current OWID fill is distinguished from recovered Gapminder rows in the clean CSV.

## Phase 5 - Reviewer Challenge

- [x] Pinker challenge answered: exact complete OWID source vintage remains unrecovered.
- [x] Data journalist challenge answered: citable files/checksums recorded; archived OWID CSV missing.
- [x] Peer reviewer challenge answered: source components are separated by row.
- [x] Skeptical-reader challenge answered: Ethiopia and tails remain weaker than recovered long-run lines.

## Final Gate

- [x] Book-period comparison visually scanned.
- [x] Extended/status comparison visually scanned.
- [x] Completeness checked.
- [x] Layout checked.
- [x] Extension clarity checked: no extension beyond book period is claimed.
- [x] Caption checked.
- [x] No critical issue remains beyond documented source-vintage gap.

## Final Decision

- [x] Accepted as `partial_match`.
- [ ] Accepted as `verified_reproduction`.
- [ ] Accepted as `updated_equivalent`.

Decision notes: Source recovery improved substantially by recovering the cited Gapminder workbook and documentation. Do not promote until the exact Roser 2016p/World Bank 2015 OWID dataset vintage is recovered or a stronger non-recovery proof is documented.
