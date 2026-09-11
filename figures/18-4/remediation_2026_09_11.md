# Figure 18-4 remediation, 2026-09-11

## Correction to previous review

The earlier review overlooked a fixed x-axis ending in 2018, hiding 2021,
2022 and 2024. It also mistook line breaks at missing LIFE survey years for an
unavoidable data limitation. That review is superseded. Differences cannot
simply be attributed to vintage: weighting had not been investigated.

## Evidence and transformations

Retained official report, downloaded September 11:
https://www.norc.org/content/dam/norc-org/pdfs/GSS_PsyWellBeing15_final_formatted.pdf

Printed tables 1/5 (PDF pages 7/11) yield 55 numerical observations via
pdftotext and validated row extraction. These are tables, not digitized chart
values. They do not establish the book's later Data Explorer configuration.

Current GSS release 3a is unchanged. Each year's valid HAPPY/LIFE responses
(codes 1,2,3) are summarized unweighted, with WTSSALL, and with WTSSPS.
Weighted denominators exclude missing/nonpositive weights and invalid responses.
All alternatives and differences from report tables are retained as CSVs.
WTSSALL closely reproduces most cells, but 1982/1987 are exceptions: the largest
difference is -2.77 percentage points. Estimator and version effects are distinct.

The unweighted series remains the explicitly labelled book-period candidate.
It visually tracks the book more closely, but this does not prove the historical
estimator. No weight was tuned to plotted coordinates. Observed LIFE points are
connected, as in the book; absent years remain missing in CSVs.

The successor uses WTSSPS, with an explicit 2016 overlap rather than a silent
splice. NORC recommends weights and identifies recent multi-mode designs:
https://gss.norc.org/faq.html and https://gss.norc.org/get-the-data.html.
No line joins 2018 to 2021. Dashed observations through 2024 are now visible.
This is descriptive successor evidence, not a homogeneous continuation.

## Actual visual/editorial review

Opened original reference and both regenerated comparison PNGs.
Critical clipping: fixed. Major artificial LIFE gaps: fixed. Major estimator
and mode comparability: disclosed, not scientifically resolved. Minor overlapping
extension labels: removed. The book candidate now has the same two continuous
observed-point trajectories, ranges and recognizable turns. Small differences
remain. The extension shows lower recent values and the survey break.
Panel plot areas are similar in width, with modest vertical alignment differences.

## Reviewer challenge and disposition

- Pinker: Exact export? No; configuration unresolved.
- Journalist: Recent decline hidden? No; all later years visible.
- Peer reviewer: Estimators/modes interchangeable? No; explicitly separated.
- Skeptical reader: Why the gap? Survey-mode change, not invented continuity.

Overall confidence: medium. Book reconstruction: close candidate, not verified.
Extension: documented weighted successor, comparability limited.
Source provenance: high for NORC downloads; exact book extract unknown.
Outstanding risks: weighting, original extract, 1982/1987 sample/version changes.
Next action: resolve Data Explorer configuration and those exceptions.
Status remains updated_equivalent; publication is not certified.

Reproduction: scripts/reconstruct_18_4.py, with --report pointing to the retained
PDF and canonical raw/clean/plot/comparison paths in figure.json. Tests cover
weights, invalid responses, table counts, last year and no 2018/2021 bridge.
