# Completion Execution Checkpoint: 2026-09-09

This is a progress report, not a completion claim or publication approval.
The [approved completion plan](../docs/completion_plan.md) remains authoritative.

## Consolidated Research State

- All 75 figures have canonical records with separate scientific, execution and
  publication status. CSV/JSON registries and PROJECT_STATE are generated views.
- Two divergent histories and stranded worker results were reconciled with
  recorded file-level decisions. Conflicting candidates remain recoverable.
- 26 packages contain actual reconstructions; nine contain source-recovery or
  diagnostic evidence; 40 figures remain untouched. Historical verified claims
  are retained, not newly certified. No scientific status was promoted this run.
- All 75 original figures have indexed crops from the supplied Supplemental
  Graphics PDF, with coordinates, hashes and OCR identity checks. Source-note
  transcription still needs human/model verification; OCR is not a bibliography.
- The current [gallery](review_baseline/index.html) and
  [52-page PDF](../output/pdf/recreated_figures_review_scroll.pdf) show actual
  original pixels beside the 26 reconstructed packages. Diagnostic/status panels
  are excluded. Missing comparable extensions are labeled as not plotted.
- All 52 comparison panels were scanned via contact sheets; selected problem
  panels were examined full resolution. The [triage](review_baseline/triage.md)
  records visible issues. This is not a full independent scientific review.

## Figure 5-3 Repair

Recovered 49 missing Sweden observations (1751-1799) from the original Hanson
GD010 Excel source table. The maternal-death/live-birth ratios validate to
floating-point precision. The 1800-1949 overlap agrees with the preserved OWID
table within its one-decimal rounding. Later vintage differences remain and
were not substituted merely to force the lines to match.

Existing OWID observations were retained. Corrected grayscale ordering, labels
and year ticks, then inspected both actual-PDF comparisons. The 2014-2015
same-source extension is necessarily short on the historical time scale.
Figure 5-3 remains `partial_match`, pending independent provenance and trajectory
review. No digitized plot values or facsimile were used as reconstruction data.

An isolated checkout at `7759c56` regenerated both clean CSVs and both plots
byte-for-byte against their canonical hashes. This used the existing Python
environment, not a fresh dependency installation. Standalone comparison
generation still needs separation from plotting before claiming a complete
portable rebuild; the canonical comparison builder remains a separate step.

## Orchestrator Work

The active implementation is the separate
[Agent Orchestrator Lab](https://github.com/J-Chamberlain/agent-orchestrator-lab)
on `codex/pinker-completion`, not this repository's historical embedded scaffold.

- Commit `303518a`: canonical execution write-back delegates to this repository's
  state writer under a lock; it preserves scientific/publication status and
  research next actions. API failures cannot become scientific source blockers.
- Commit `b7a5ef9`: immutable submission packages include unchanged evidence,
  original/comparison pixels, clean data previews, code, lineage and sources.
  The OpenAI request now includes actual image inputs rather than dimensions.
- Missing evidence, corrupt hashes, unsafe paths, malformed responses and false
  visual-review claims fail closed. Rule-based checks cannot approve scientific
  figures. A supervisor cannot override unresolved scientific remediation with
  acceptance. Workers cannot set execution/publication status or generated views.
- An offline Figure 5-3 package at `677e27f` included 21 files and three image
  inputs without missing declared evidence. This was a packaging test, not a
  worker run or scientific verdict. No paid API calls were made.

## Validation

| Check | Result |
| --- | --- |
| Pinker test suite | 50 passed |
| Canonical records/views/hash validation | 75 records consistent |
| Original reference identity coverage | 75 of 75 |
| Review PDF input coverage | 26 figures, 52 real comparison pages |
| Active orchestrator suite | 283 passed, no API keys needed |
| Focused scientific-package/write-back tests | 26 passed |
| Figure 5-3 clean data and plot rebuild | Four hashes reproduced in isolated checkout |
| Real paid scientific reviewer calibration | Not run |
| Complete unattended production lifecycle | Not yet validated |

## Next Actions

1. Finish atomic integration of a reviewed worker record with regenerated views;
   test whole-run locking, interruptions and review-only resumption without
   rerunning a successful worker. Never merge to main automatically.
2. Pin dependencies and separate source retrieval, transformation, plotting and
   comparison generation; expand clean-checkout tests beyond Figure 5-3.
3. Complete missing canonical script/data descriptors and verify source notes.
   Build reusable source adapters around concrete recovery needs.
4. After a spending ceiling is approved and credentials pass preflight, calibrate
   the independent image reviewer on strong, partial, wrong-reference and
   placeholder examples before any unattended production.
5. Repair existing packages, then process the 40 untouched figures through the
   plan's scientific and editorial gates. Produce a fresh-checkout release only
   after cross-figure review and explicit reporting of incomplete reconstructions.

Paid API budget remains unspecified. Public deployment, paid source access and
author outreach remain unapproved. No scheduled background production is active.

## Milestone Commits

Pinker integration branch `production-loop`:

- `84c41f4`: reconcile local and remote histories.
- `4d7a72a`: preserve worker evidence and introduce canonical state.
- `677e27f`: original-reference library, 52-page baseline and Figure 5-3 repair.
- `7759c56`: science-preserving execution-writer contract.

The enclosing checkpoint commit records this report and the plan-ledger update.
No temporary smoke-test commit is part of production history.
