# Figure Review Protocol v1.0

This protocol is the permanent review standard for every figure in the
project. A figure is not complete until it passes this review or its failures
are explicitly documented as unresolved research tasks.

The protocol exists to prevent premature stopping. Finding a plausible source
or generating a visually decent plot is not enough.

## Burden Of Proof

The working assumption is that the original underlying data exist unless
substantial evidence suggests otherwise.

Codex should attempt to prove or disprove this assumption before accepting a
proxy dataset. Absence of immediate search results is not sufficient evidence
that the original data are unavailable.

Proxy or successor datasets may be used only when the source log explains:

- What original data were sought.
- Which archives, repositories, supplements, and institutional paths were
  checked.
- Why the original data could not be confirmed.
- Why the substitute is the best available evidence.
- How the substitute differs from the likely original.

## Phase 1 - Evidence Review

Confirm:

- Original Kindle figure inspected.
- Title extracted.
- Caption extracted.
- Source note extracted.
- Surrounding discussion reviewed.
- Bibliography resolved.

If any item is missing, return to Discovery.

Required evidence:

- Kindle extraction notes.
- Figure title and source/citation line.
- Bibliography mapping or unresolved-bibliography note.
- Source log entry describing what was and was not visible.

## Phase 2 - Source Review

Confirm:

- Original publication located.
- Source chain reconstructed.
- Dataset provenance documented.
- Archive search completed.
- Successor datasets evaluated.

If a modern proxy was substituted, explain exactly why.

Required evidence:

- Source discovery log with accepted and rejected sources.
- Archive URLs or archive-search notes where applicable.
- Download URLs and retrieval dates.
- Dataset checksums where files are stored.
- Clear classification of original, archival, successor, proxy, or diagnostic
  source status.

## Phase 3 - Reconstruction Review

Confirm:

- Reconstruction uses legitimate data.
- No digitized figure values are used as reconstruction data.
- Styling reasonably matches the book.
- Scales and labels are correct.
- Book-period comparison generated.

If reconstruction quality is inadequate, return to Source Recovery.

Required evidence:

- Raw or referenced data.
- Clean analysis-ready data.
- Transformation or plotting script.
- Book-period reconstruction.
- Book-period side-by-side comparison.
- Notes explaining any deviations from book styling.

Digitized figure values may be used only for validation or measurement of
visual discrepancy, never as the underlying reconstruction dataset.

## Phase 4 - Extension Review

Confirm:

- Later data searched.
- Later data documented.
- Extension clearly distinguished.
- Methodological changes explained.
- Successor-series discontinuities explained.

If the extension introduces unexplained artifacts, return to Source Recovery.

Required evidence:

- Extension source notes.
- Extended reconstruction, if later data are available.
- Extended side-by-side comparison, if an extension is plotted.
- Caption language distinguishing book-period data from later data.
- Anomaly review covering discontinuities, source revisions, and endpoint
  differences.

If no extension is possible, document why and classify the missing extension as
unavailable, not silently absent.

## Phase 5 - Reviewer Challenge

This phase is mandatory. Codex must review the completed figure as though it
were an independent reviewer.

Answer:

1. What would Steven Pinker likely question?
2. What would a data journalist question?
3. What would a peer reviewer question?
4. What would a skeptical reader notice immediately?

Every identified issue becomes one of:

- Resolved.
- Documented.
- New research task.

The answers should appear in the anomaly review, the figure README, or a
figure-specific completed checklist.

## Reviewer Confidence

Every figure review should conclude with:

- Overall confidence:
- Book reconstruction:
- Extension:
- Source provenance:
- Outstanding risks:
- Recommended next action:

Use plain-language confidence descriptions such as `high`, `medium`, `low`, or
`blocked`, and explain the reason. Do not let a single numeric score hide a
major unresolved source issue.

## Acceptance Rule

A figure is complete only when:

- Reconstruction is satisfactory.
- Extension is satisfactory or its absence is explained.
- Discrepancies have been reviewed.
- Reviewer questions have been answered.
- Repository files are updated.
- Registry row is updated.
- `PROJECT_STATE.md` is updated.

Only then may Codex begin another figure.

## Stopping Criteria

Codex may stop only when one of the following is true:

- The figure is visually and evidentially satisfactory.
- Remaining discrepancies are explained in the caption and anomaly review.
- The source search space has been exhaustively documented.
- Manual input is genuinely required.

Codex should not stop merely because it found a plausible source or generated a
plot.

## Required Repository Updates

Before a figure advances, update:

- Figure directory files.
- Per-figure metadata.
- Source logs and search iterations.
- Provenance and discrepancy logs.
- Caption and anomaly review.
- Side-by-side visual artifacts.
- `data/figure_registry.csv`.
- `data/figure_registry.json`.
- `PROJECT_STATE.md`.
- `docs/lessons_learned.md` when a reusable lesson emerges.

## Relationship To The Checklist

[review_checklist.md](review_checklist.md) is the operational checklist derived
from this protocol. Each figure directory should eventually include a completed
copy or equivalent figure-specific review file.
