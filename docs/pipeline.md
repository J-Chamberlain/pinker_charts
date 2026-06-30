# Figure Reconstruction Pipeline

This document defines the full reconstruction lifecycle. It is written for
human researchers and future AI collaborators.

## 1. Discovery

Discovery begins with the book's List of Figures and source lines. The goal is
to identify candidate figures, capture figure identifiers and titles, and avoid
guessing beyond visible evidence.

Artifacts:

- List-of-figures extraction.
- Figure metadata skeleton.
- Candidate figure queue.

## 2. Kindle Extraction Using Computer Use

Kindle is used only as a visual reference for figure titles, source lines, and
book-period visual comparison. Do not export or inspect the Kindle file itself.

Required outputs:

- Confirmed figure title.
- Short source/citation line.
- Optional cropped reference image for audit and visual validation.
- Explicit uncertainty notes.

## 3. Bibliography Resolution

Resolve the book citation into source papers, institution pages, data portals,
archive captures, and dataset identifiers. Bibliographic resolution should
separate academic literature from institutional data release chains.

Required outputs:

- Bibliography mapping.
- Dataset reference catalog.
- Archive index.
- Citation key lookup where applicable.

## 4. Source Recovery

Search for original data first, then archival copies, then successor releases.
Every search query and source decision must be logged. A source is accepted only
when the variables, dates, units, geography, and source institution plausibly
match the book figure.

Accepted source classes:

- Exact original dataset.
- Exact archival copy.
- Same-institution historical release.
- Same-institution successor series.
- Diagnostic-only candidate.

## 5. Book-Period Reconstruction

The book-period reconstruction should use only evidence that plausibly existed
at the time of publication. If an exact source is not found, the plot may still
be produced, but its status cannot be `verified_reproduction`.

Required outputs:

- Clean analysis-ready data.
- Scripted transformation.
- Book-period plot.
- Caption with source caveats.

## 6. Post-Publication Extension

Extensions are optional and must be visually and semantically separated from
book-period reconstructions. Use dotted or otherwise distinct styling and label
successor data clearly.

Never imply that successor data is methodologically continuous unless the
source chain proves it.

## 7. Visual Review

Place the original reference and recreated figure side by side. Review axis
scales, line directions, relative magnitudes, series colors, and endpoint
locations. Compute simple metrics when feasible, but do not let metrics replace
human source reasoning.

Required outputs:

- Comparison image.
- Visual validation classification: `excellent`, `good`, `acceptable`, or
  `poor`.
- Written reasoning.

## 8. Discrepancy Analysis

Every major visual or numeric mismatch should drive source recovery. Record
whether the discrepancy is caused by wrong data, wrong transformation, source
revision, missing data, or plotting style.

Required outputs:

- Discrepancy log.
- Rejected-source rationale.
- Remaining uncertainties.

## 9. Iterative Improvement

Source recovery, plotting, and validation are iterative. Each iteration should
leave enough evidence for another researcher to continue without repeating
unlogged searches.

Required outputs:

- Search iteration log.
- Updated metadata.
- Updated source log.
- Updated project state.

## 10. Editorial Review Gate

The Editorial Review Gate is the final publication-quality scan before a batch
is committed and marked complete. It is separate from source recovery and
scientific validation.

Open every book-period and extended comparison image and ask what would
immediately catch the eye of a journal editor, website visitor, book reader, or
principal investigator. Do not analyze individual data points during this scan.
Look for missing artifacts, poor crops, tiny plots, bad scaling, misleading
extensions, awkward labels, excessive whitespace, and captions that fail to
explain obvious discrepancies.

Required outputs:

- Editorial Review Summary.
- Critical, Major, and Minor issue classifications.
- Corrections for all automatically fixable Critical or Major issues.
- Explicit explanations for any remaining Major issue.
- Cross-figure judgment identifying the weakest figure in the batch.

A batch may not complete while any Critical issue exists or any unexplained
Major issue exists. Minor issues may remain only if documented.

## 11. Publication Package

Before website publication, each figure directory must be independently
reviewable.

Required package:

- Metadata.
- Provenance.
- Source log.
- Search iterations.
- Discrepancy log.
- Anomaly review.
- Caption.
- Lineage.
- Raw data or raw data references.
- Clean data.
- Checksums.
- Book-period reconstruction.
- Extended reconstruction if applicable.
- Diagnostic plots.
- Side-by-side validation.
