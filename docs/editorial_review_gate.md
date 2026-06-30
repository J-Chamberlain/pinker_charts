# Editorial Review Gate

The Editorial Review Gate is the final publication-quality check for every
figure batch. It is separate from source recovery, scientific validation, and
the reviewer challenge. Its purpose is to prevent an otherwise well-documented
batch from being marked complete while obvious presentation problems remain.

This gate occurs after reconstruction, extension, captions, anomaly review, and
the figure review checklist, but before final commit, `PROJECT_STATE.md`
completion language, and batch completion.

## Reviewer Posture

For this gate, stop acting as the researcher. Review the batch as:

- The journal editor.
- The website visitor.
- The book reader.
- The principal investigator.

Assume no prior context. Judge only what is visible on the comparison pages and
in the adjacent caption/anomaly language.

## Rapid Scan

Imagine the batch has already been published. Open every book-period and
extended comparison image and ask:

> If I opened this report for the first time, what would immediately catch my
> eye?

Do not analyze individual data points during this scan. The goal is to catch
obvious visual, layout, labeling, caption, and presentation failures.

Any issue obvious within approximately ten seconds of viewing the page must be
corrected automatically or explicitly explained. No exceptions.

## Mandatory Questions Per Figure

### Completeness

Is anything obviously missing?

Examples:

- Missing Kindle reference image.
- Missing reconstruction.
- Missing extension or explanation of absence.
- Missing caption.
- Missing labels.

### Layout

Does anything look visually wrong?

Examples:

- Tiny recreated plot.
- Poor scaling.
- Poor cropping.
- Excessive whitespace.
- Inconsistent margins.
- Awkward label placement.
- Overlapping labels.

### Visual Similarity

Does the reconstruction resemble the original enough that a human would
immediately say, "Those look like the same figure"?

If not, continue iterating unless the mismatch is source-related and already
explicitly explained in the caption and anomaly review.

### Extensions

If an extension exists:

- Is it visually clear?
- Does it appear continuous when it should not?
- Is the dashed or otherwise marked transition obvious?
- Are successor-series changes explained?

### Captions

Does the caption explain every obvious visual discrepancy?

If a reader would notice something unusual, the caption or anomaly review should
answer the question before they ask it.

## Severity Classification

Classify every issue as `Critical`, `Major`, or `Minor`.

### Critical

Critical issues block batch completion.

Examples:

- Missing Kindle reference.
- Missing comparison image.
- Wrong source.
- Wrong figure.
- Missing reconstruction.

### Major

Major issues block batch completion unless corrected or explicitly explained.

Examples:

- Obvious visual mismatch.
- Wrong scale.
- Poor layout.
- Misleading extension.
- Caption does not explain a conspicuous discrepancy.

### Minor

Minor issues may remain if documented.

Examples:

- Typography.
- Label placement.
- Line thickness.
- Spacing.

## Acceptance Rule

A batch may not complete while:

- Any `Critical` issue exists.
- Any unexplained `Major` issue exists.

Minor issues may remain only when they are documented in the editorial review
summary, caption, anomaly review, or discrepancy log.

## Cross-Figure Review

After reviewing each figure individually, perform a second review across the
entire batch:

- Which figure looks weakest?
- Which figure would most concern a reviewer?
- Is the weakest figure good enough to publish?

If the weakest figure is not good enough to publish, continue improving it or
document why manual input or further source recovery is genuinely required.

## Editorial Review Summary

Every batch must conclude with an Editorial Review Summary before final commit.
Include:

- Critical issues found.
- Major issues found.
- Minor issues found.
- Issues automatically corrected.
- Issues remaining.
- Why the batch is acceptable for publication or why it remains a documented
  partial/blocked batch.

This summary should appear in the final Codex response and, when figure files
change, in the relevant anomaly review, discrepancy log, or batch/report notes.
