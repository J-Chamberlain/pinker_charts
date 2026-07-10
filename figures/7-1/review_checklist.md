# Figure Acceptance Checklist

Copy this checklist into a figure directory when a figure enters active
reconstruction. A figure is not complete until every item is checked or marked
`N/A` with an explanation.

Recommended destination:

`figures/<figure_id>/review_checklist.md`

## Figure

- Figure ID:
- Title:
- Reviewer:
- Review date:
- Current status:

## Phase 1 - Evidence Review

- [ ] Kindle figure inspected.
- [ ] Title extracted.
- [ ] Caption extracted.
- [ ] Source note extracted.
- [ ] Surrounding discussion reviewed.
- [ ] Bibliography resolved or unresolved bibliography documented.
- [ ] Missing evidence returned to Discovery or documented.

## Phase 2 - Source Review

- [ ] Original publication located.
- [ ] Source chain reconstructed.
- [ ] Dataset provenance documented.
- [ ] Archive search completed.
- [ ] Successor datasets evaluated.
- [ ] Modern proxy or successor substitution explained, if used.
- [ ] Download URLs recorded.
- [ ] Archive URLs recorded where applicable.
- [ ] Checksums recorded for stored files.

## Phase 3 - Reconstruction Review

- [ ] Reconstruction uses legitimate data.
- [ ] No digitized figure values used as reconstruction data.
- [ ] Transformation code is reproducible.
- [ ] Scales and labels are correct.
- [ ] Styling reasonably matches the book.
- [ ] Book-period reconstruction completed.
- [ ] Book-period side-by-side comparison generated.
- [ ] Every visible book-period discrepancy investigated.
- [ ] Remaining book-period discrepancies explained.

## Phase 4 - Extension Review

- [ ] Later data searched.
- [ ] Later data documented.
- [ ] Extension completed or absence explained.
- [ ] Extension clearly distinguished from book-period reconstruction.
- [ ] Methodological changes explained.
- [ ] Successor-series discontinuities explained.
- [ ] Extended side-by-side comparison generated where available.
- [ ] Extension artifacts investigated.
- [ ] Remaining extension discrepancies explained.

## Phase 5 - Reviewer Challenge

- [ ] Answered: What would Steven Pinker likely question?
- [ ] Answered: What would a data journalist question?
- [ ] Answered: What would a peer reviewer question?
- [ ] Answered: What would a skeptical reader notice immediately?
- [ ] Each reviewer issue marked resolved, documented, or new research task.

## Final Gate - Editorial Review

- [ ] Every book-period comparison image opened and visually scanned.
- [ ] Every extended comparison image opened and visually scanned, where
  available.
- [ ] Completeness checked: Kindle reference, reconstruction, extension or
  absence explanation, caption, and labels.
- [ ] Layout checked: scaling, cropping, whitespace, margins, label placement,
  overlap, and plot size.
- [ ] Visual similarity checked: original and recreated figures visibly
  resemble the same figure or discrepancy is explained.
- [ ] Extension clarity checked: dashed or otherwise marked transition is clear
  and successor data are not misleadingly continuous.
- [ ] Caption checked: every obvious visual discrepancy is explained before a
  reader has to ask.
- [ ] Every ten-second-obvious issue corrected or explicitly explained.
- [ ] Issues classified as `Critical`, `Major`, or `Minor`.
- [ ] No `Critical` issues remain.
- [ ] No unexplained `Major` issues remain.
- [ ] Remaining `Minor` issues documented.
- [ ] Cross-figure review completed.
- [ ] Weakest figure identified.
- [ ] Most reviewer-concerning figure identified.
- [ ] Weakest figure judged publishable or documented as requiring manual input
  or further source recovery.
- [ ] Editorial Review Summary written.

## Repository Updates

- [ ] Caption written or updated.
- [ ] Anomaly review written or updated.
- [ ] Provenance file updated.
- [ ] Source log updated.
- [ ] Search iteration log updated.
- [ ] Discrepancy log updated.
- [ ] Metadata updated.
- [ ] Registry CSV updated.
- [ ] Registry JSON updated.
- [ ] `PROJECT_STATE.md` updated.
- [ ] Canonical artifact paths updated in `PROJECT_STATE.md`.
- [ ] Latest side-by-side images rendered in final Codex response.
- [ ] Editorial Review Summary included in final Codex response.

## Reviewer Confidence

- Overall confidence:
- Book reconstruction:
- Extension:
- Source provenance:
- Outstanding risks:
- Recommended next action:

## Final Decision

- [ ] Accepted as `verified_reproduction`.
- [ ] Accepted as `updated_equivalent`.
- [ ] Accepted as `partial_match`.
- [ ] Classified as `source_unavailable`.
- [ ] Classified as `manual_review_needed`.
- [ ] Returned to Discovery.
- [ ] Returned to Source Recovery.

Decision notes:


## Track A Completion Notes

Current status: `partial_match`.

2026-07-09 targeted rerun status: `partial_match`.

- Supplemental PDF page 5 was inspected for figure image, source note, and
  surrounding explanatory text.
- Bibliography/source family was resolved to OWID/Roser 2016d "Food Supply" /
  daily caloric supply material, with Fogel 2004 and FAO/FAOSTAT cited by the
  book.
- Archived 2018 OWID Grapher chart-page configuration was recovered and stored
  under `data/candidates/archives/`.
- Exact book-era machine-readable OWID variable data were not recovered. Direct
  Wayback/CDX checks for CSV/JSON and `/grapher/data/variables/3590*` endpoints
  failed.
- The 2022 OWID successor dataset is used for reconstruction; its raw CSV is
  byte-identical to the public `owid/owid-datasets` named dataset.
- The previous missing England-line issue was corrected by including the
  available `United Kingdom` source series and labeling it `England/UK`.
- Book-period and extended comparisons were regenerated. The extended segment
  uses same-file successor values through 2018 and is dashed.
- Editorial review found no critical layout issue after note wrapping, but
  major evidentiary issues remain: exact Roser 2016d data are unrecovered and
  the historical line shapes visibly differ from the book.
- Checklist is not fully complete for verified publication; unresolved items
  are documented in anomaly/source/discrepancy logs.
