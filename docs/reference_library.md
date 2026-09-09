# Original Reference Library

The supplied 39-page Supplemental Graphics PDF contains all 75 registered
figures. `references/figure_index.json` records each figure's PDF page, panel,
pixel/PDF-point crop bounds, original PDF checksum, crop checksum, OCR title
and short source note. PDF page coordinates must not be confused with printed
book page numbers. No plotted numerical values are extracted as data.

Run `python scripts/index_references.py --update-records` with Poppler,
Tesseract, and Pillow installed. It renders actual visible pixels, finds a
white gutter between figures, trims outer whitespace, and requires OCR to
identify exactly the expected figure ID. The PDF text layer contains clipped
or invisible material, so text extraction alone is not sufficient authority.

All 75 IDs were machine-confirmed on 2026-09-09. Contact-sheet visual inspection
identified midpoint-crop contamination; gutter-based cropping corrected it.
This establishes reference coverage, not scientific review. Each source-note
transcription still requires verification at full resolution when used; OCR
misspellings are explicitly retained as unverified machine output.

The library is research reference material. No public redistribution clearance
is asserted. A public release must separate original book graphics from
licensed/generated assets and settle permissions before deployment.

## Review Baseline

`scripts/build_review_baseline.py --update-records` makes actual-original versus
reconstructed comparisons. It checks input hashes and excludes source-only,
diagnostic, and not-started packages. It does not modify reconstruction data or
plots. Its output is an audit baseline, not an acceptance decision. Regenerated
comparisons invalidate previous visual review and require inspection again.

`scripts/publish_review_baseline.py` creates the local gallery and continuous
PDF from the hash-verified manifest. There are currently 26 reconstructed
figures and 52 book-period/extension-candidate pages. An extended filename does
not establish a scientifically comparable extension; pending methodology
review is labeled explicitly. Historical captions can contain obsolete claims
and must be reconciled in the scientific review phase.

`python scripts/project_state.py generate` then refreshes registries, state,
README links and canonical checksums. Run `check` before committing.
