# Pinker Charts Completion Plan

Approved direction: 2026-09-09.
Plan version: 1.0.
Current checkpoint: owner authorized direct in-task production and set API orchestration aside. Consolidation and the reusable data library are established; complete figures and data lineage directly, retaining scientific and editorial checks.

This is the canonical execution plan approved by the project owner. It records
the route from the fragmented July project state to a reproducible research
release. Read [PROJECT_STATE.md](../PROJECT_STATE.md) first, then this plan.
Consult the progress ledger below before choosing the next action.

## Objective And Completion Standard

Reconstruct all 75 registered figures from Steven Pinker's *Enlightenment Now*
as faithfully as recoverable source data allow. Add clearly distinguished
post-publication extensions where the data are comparable. Deliver a repository
that an unfamiliar researcher can reproduce and audit, together with a visual
review gallery and a continuous comparison PDF.

Owner clarification, 2026-09-09: underlying data are a long-lived deliverable
for independent analysis and future refreshes. Preserve original releases,
versioned clean observations and per-plot lineage in the
[data library](data_library.md), not just the rendered figures.

The scientific target is 75 faithful reconstructions. A complete source search,
an accepted worker commit, or an empty scheduling queue does not establish that
a figure has been reconstructed. Unrecoverable figures remain explicitly
incomplete. A release may document those exceptions, but its completion report
must distinguish release preparation from achievement of the scientific target.

Existing [research review](review_protocol.md),
[figure checklists](review_checklist.md), and
[editorial review](editorial_review_gate.md) remain required. This plan changes
execution and state management; it does not weaken their evidence standards.

## Starting Evidence

The read-only planning review inspected the local Pinker Charts repository,
the separate Agent Orchestrator Lab repository, the July audit and contact
sheet, the current reviewer implementation, and live GitHub main.

| July audit classification | Figures |
| --- | ---: |
| Classified as verified reproductions | 9 |
| Updated equivalents | 7 |
| Partial reconstructions | 11 |
| Source-recovery or documentation packages | 8 |
| Untouched | 40 |
| Total | 75 |

These are provisional inventory classifications, not a fresh scientific
endorsement. The audit is currently an untracked local artifact in
`agent_orchestrator_lab/audit/pinker_output_audit.md`; do not assume a fresh
clone includes it. Preserve useful audit evidence during consolidation.

Observed repository coordinates at planning time:

| Repository or reference | Commit |
| --- | --- |
| Local Pinker branch `codex/10-4-deforestation-1700-2010` | `3f65300288c15c452a4d493895e8dbc9807c0d91` |
| GitHub Pinker `main` | `9a19519494ec20f45b3ac3e6b3122d38a2bc0892` |
| GitHub Pinker `production-loop` | `8f7803316427d26f876d76e67e9d0d15ef6d109c` |
| Agent Orchestrator Lab `main` | `35830bddb28215325f4c77dda02d6e8a3925ed36` |

These coordinates identify the inspected state, not permanent branch tips.
Refresh them before reconciliation. The local Pinker branch was 45 commits
ahead of its tracked remote branch. No reconciliation or merge was performed
during planning.

Findings that determine the order of work:

- The local branch contains many figure packages absent from GitHub main.
  GitHub main contains newer recoveries, including Figures 5-3 and 19-1,
  that are absent from the local production checkout.
- GitHub's Figure 5-3 recovery used a labeled facsimile because it lacked
  original pixels. The local repository has the Supplemental Graphics PDF and
  a reference crop. Combining these is a research opportunity, not grounds
  for automatic status promotion.
- Both local registry formats contain 75 unique figure IDs, but 14 scientific
  status fields disagree. The runner writes scheduling outcomes such as
  `orchestrator_blocked` into `current_status`.
- The local review manifest contains 28 entries. The July audit identified
  three status/diagnostic entries and two genuine reconstructed figures missing
  from that manifest. Rebuild it from reconciled evidence.
- The active Agent Orchestrator Lab API reviewer sends text, image filenames,
  and dimensions, not image inputs. It cannot establish visual acceptance.
- Historical scripts include absolute paths and temporary-file dependencies.

Remote evidence inspected:

- [GitHub project state at the inspected commit](https://github.com/J-Chamberlain/pinker_charts/blob/9a19519494ec20f45b3ac3e6b3122d38a2bc0892/PROJECT_STATE.md).
- [Figure 5-3 source recovery](https://github.com/J-Chamberlain/pinker_charts/blob/9a19519494ec20f45b3ac3e6b3122d38a2bc0892/figures/5-3/provenance/provenance.md).
- [Figure 19-1 source recovery](https://github.com/J-Chamberlain/pinker_charts/blob/9a19519494ec20f45b3ac3e6b3122d38a2bc0892/figures/19-1/provenance/provenance.md).

## 1. Consolidate All Existing Evidence

Inventory local and remote branches, worker commits, figure artifacts, source
data, original references, and run decisions. Resolve conflicts figure by
figure using source evidence, content hashes, and review findings. Neither
the latest timestamp nor a branch name is sufficient to choose a winner.

Preserve the best source recoveries and the genuine references, including work
that was accepted as a documented blocker. Do not overwrite sound validated
figures merely to standardize their presentation. Record the origin commit of
each retained package and the reason for each resolution.

Establish `production-loop` as the integration branch after reconciliation.
Keep temporary worktrees only where needed for execution isolation. Preserve
recoverable history; do not reset, force-push, or delete unresolved work.

Exit evidence: one reconciled inventory of 75 IDs; branch-resolution record;
canonical artifact paths verified; reviewed baseline available on GitHub.

## 2. Make Project State Consistent By Construction

Maintain one authoritative record per figure. Separate scientific status,
execution status, and publication readiness. Preserve historical classifications
and the evidence for any change. Do not reinterpret `orchestrator_accepted` as
`verified_reproduction`, or an API failure as a missing scientific source.

Generate registry CSV/JSON mirrors, artifact indexes, PROJECT_STATE summary
tables, and the review manifest from the authoritative records. Retain useful
human research notes separately from generated summaries. Give one component
ownership of integration-time registry updates so workers cannot be penalized
for obeying contradictory write restrictions.

Exit evidence: schema and consistency checks pass for all 75 figures; generated
views agree; worker and reviewer instructions agree on ownership and acceptance.
Until this migration is implemented, do not assume automatic synchronization.

## 3. Build A Shared Reference And Source Library

Index all 75 original PDF figures with page numbers, crop coordinates, title,
source note, bibliography keys, visible variables, units, and relevant context.
Use the Supplemental Graphics PDF first and Kindle for missing context. Keep
original reference pixels distinct from facsimiles and source-owner charts.

Build on existing [source-adapter knowledge](source_adapters.md) and recovered
files. Implement reusable retrieval for OWID archives, institutional historical
releases, GitHub history, and academic supplements as the queue requires them.
Cache source versions, URLs, capture dates, checksums, metadata, and licensing
notes. Log accepted and rejected candidates and unsuccessful searches so related
figures share what has already been learned.

Exit evidence: reference coverage for all 75 figures, with explicit gaps;
reusable source bundles and tested retrieval adapters for the first source
families; no repeated search without a recorded reason or new lead.

## 4. Make Reconstructions Portable And Reproducible

Separate fetching, cleaning, plotting, and comparison generation. Remove
machine-specific paths and dependencies on disposable temporary files. Pin
software dependencies and data snapshots. Make rebuilding from retained data
independent of current source-site availability.

Test series identities, date coverage, units, denominators, transformations,
and numerical agreement with recovered source tables. Record interpolation,
aggregation, exclusions, revisions, and missingness explicitly. Never use
digitized plotted values as reconstruction input or tune data to force a visual
match. Any necessary source-table transcription must identify the table and
include a verification record.

Exit evidence: a documented clean-checkout rebuild command; checksum and data
tests; existing sound outputs preserved or changes justified by an audited diff.

## 5. Implement Scientific And Visual Acceptance

Submit the full figure package at an exact commit, including unchanged evidence
needed to understand the result, alongside the exact base/head diff. Include
raw-source references, clean data, code, provenance, limitations, original crop,
book-period comparison, and extended comparison where applicable.

The independent reviewer must actually receive and inspect the images.
Record which artifact hashes were inspected. If image inspection is unavailable,
record `visual_review_unavailable` and prohibit visual acceptance. Filenames,
dimensions, facsimiles, and worker assertions are insufficient evidence.

Check chart type, series coverage, axes, scale, labels, geometry, source fidelity,
and extension continuity. Document specific discrepancies, their likely causes,
what was corrected, and what remains. Inspect regenerated comparisons again.
Use image similarity only as supporting diagnostics, never as proof of source
fidelity. Require the scientific review and Editorial Review Gate before
publication readiness can pass.

Exit evidence: substantive review records grounded in actual data and pixels;
negative tests for missing/wrong references, text-only panels, missing series,
misleading extensions, and unsupported status claims.

## 6. Validate Unattended Operation

Retain the existing transactional runner's known base/head commits, clean
worktree requirement, remediation linkage, and immutable evidence. Test
interruption recovery, API failures, branch integration, exact-commit review,
registry write-back, and budget enforcement before production.

Distinguish research blockers from infrastructure failures. Resume review of a
successful worker commit after a reviewer failure instead of recreating the
figure. Permit remediation only for a concrete defect with a plausible remedy;
compare each new review with previously resolved findings to prevent churn.

Use a calibration set consisting of an existing strong figure, an incomplete
figure, and one new figure. Audit the strong figure without needless rewriting.
Measure cost, elapsed time, scientific improvement, and review reliability.
Use those observations to set the remaining schedule within the approved
budget. Continue once gates pass without routine per-figure approvals.

Exit evidence: offline lifecycle tests pass; controlled calibration passes;
actual execution credentials, budgets, model capabilities, and resumption
behavior are verified. A model name alone is not evidence of capability.

## 7. Repair Existing Incomplete Work

Prioritize improvements unlocked by consolidation and shared sources. Compare
the GitHub 5-3 recovery against the local original PDF and inspect the newer
19-1 recovery before repeating historical searches. Review the other existing
partial and source-recovery packages for actionable scientific defects.

Preserve sound verified work. Apply adapters and deeper targeted recovery where
a concrete lead could improve fidelity. An accepted blocker report is useful
research evidence, but the reconstruction remains incomplete. Record the exact
dependency and continue other work when progress requires external access.

Exit evidence: each previously attempted figure is either satisfactory with
supporting review or has a specific unresolved issue and justified next action;
no old problem is hidden behind a scheduling label.

## 8. Process The Untouched Figures Systematically

Confirm the untouched set from the reconciled registry; the provisional count
is 40. Group research by source family while completing and integrating figure
packages individually. Carry each through original-source recovery, archived
source checks, book-period reconstruction, comparable extension, visual review,
correction, and evidence-backed classification.

Use a bounded research effort tied to promising leads, not a requirement to
produce a plot at any cost. Preserve useful partial recovery and continue the
queue when a figure is externally blocked. Never put placeholder panels in the
reconstructed-figure gallery. Regenerate the review PDF after coherent groups
of accepted artifacts and retain its exact-commit manifest.

Exit evidence: every registry figure has been investigated, with a real reviewed
reconstruction or an explicit incomplete disposition. Report these separately.

## 9. Conduct Final Recovery And Consistency Review

Apply newly recovered sources and adapters to deferred figures. Revisit a
blocked source only when a new lead, capability, or access change makes progress
plausible. Check consistency across chapters: units, geography, source vintage,
extension cutoffs, missing years, captions, and status calibration.

Complete a full-resolution visual scan across all reconstructed comparisons.
Correct fixable issues and document remaining source limitations. For external
blockers, specify the missing file, table, permission, or owner response needed.
Author outreach and paid access require authorization; drafting a recovery
request does not authorize sending it.

Exit evidence: cross-figure review record, no unresolved critical publication
issues in released reconstructions, no unexplained major discrepancies, and an
actionable list of figures still scientifically incomplete.

## 10. Produce And Independently Test The Release

Deliver a searchable visual gallery, downloadable plots and clean data,
provenance and lineage, the continuous comparison PDF, and reproducibility
instructions. Separate research-only reference material from assets suitable
for redistribution. Do not assume public deployment is authorized by approval
of the research plan.

Test from a fresh checkout as a researcher with no chat history. Verify figure
links, data checksums, source identities, plotted values, rebuild behavior,
registry consistency, and gallery/PDF coverage. Publish an exact-commit release
manifest and an honest completion report with outstanding scientific gaps.

Exit evidence: reproducible release candidate, passing validation report,
complete artifact index, and separate counts for verified, updated, partial,
and unreconstructed figures. Public deployment remains a distinct scope choice.

## Operating Agreement

Owner direction, 2026-09-09: no further API-process work is required. Continue
research and reconstruction directly in the continuing Codex task. API budget,
worker-branch integration and paid reviewer calibration are not prerequisites
for this execution route. Conduct a separate skeptical self-review of actual
images and source evidence; label it honestly as in-task review, not an external
independent reviewer. Do not weaken data provenance or promote uncertain figures.

- One continuing lead retains scientific context. Use narrowly scoped workers
  where they help; keep independent review of meaningful scientific submissions.
- Use deterministic code for bookkeeping, invariants, and routine validation.
  Avoid additional model calls merely to reconcile administrative wording.
- Use one integration branch, with temporary execution isolation as needed.
  Integrate only reviewed work. Do not auto-merge to main or force-push.
- Commit coherent progress and preserve resumable checkpoints. A runtime limit
  must leave an exact next action, not a claim of completion or an implicit
  background run. Verify any unattended scheduling mechanism before relying on it.
- Follow the user's credential requirement: do not start OpenAI-backed
  production unless OPENAI_API_KEY is available through the configured loader
  and passes preflight. Check required GitHub authentication before writes.
  Never print keys. A previous session's authentication is not current evidence.
- External-API spending ceiling is not specified. Do not infer unlimited paid
  execution from approval of the plan. Local consolidation, offline tests, and
  other work that does not require that decision can proceed.
- The API reviewer is optional unattended infrastructure. Its paid calibration
  is not a prerequisite for in-session source research, data-library work or
  actual visual inspection. Do not let API setup displace those deliverables.
- Public deployment versus a publication-ready release is not yet selected.
  Prepare the release candidate while leaving that external action pending.
- Report meaningful milestones and consolidated blockers. Ask the owner only
  for external decisions that cannot be resolved within existing authorization.
- Preserve the existing requirement to display actual book-period and extended
  comparison images when reporting figure work. Do not report image inspection
  that did not occur.

## Progress Ledger

Update this ledger and PROJECT_STATE at meaningful checkpoints. Link the
validation evidence before marking a phase complete. Do not copy a full second
ledger into the orchestrator repository.

| Phase | State | Evidence or next action |
| --- | --- | --- |
| 1. Consolidation | Reconciled baseline built | [Import evidence](../reports/consolidation/README.md); both histories and stranded workers preserved; 75 records and [26-figure/52-page visual baseline](../reports/review_baseline/index.html). [Triage](../reports/review_baseline/triage.md) is not publication approval. |
| 2. Consistent state | Implemented; writer bridge tested offline | [State contract](canonical_state.md); 75 canonical records and generated views, 14 state tests. Active orchestrator commits `303518a`/`b7a5ef9` preserve scientific status and enforce worker isolation. Full branch integration remains a Phase 6 gate. |
| 3. Shared source library | Reference coverage implemented; source adapters pending | [Reference library](reference_library.md): 75 original crops, PDF coordinates/hashes and OCR title/source. Full-resolution source-note verification and reusable retrieval adapters remain. |
| 4. Portable reproduction | First isolated rebuild checked | Figure 5-3 clean CSVs and both plots reproduce four canonical hashes using existing environment at `7759c56`; fresh dependency install and remaining scripts not yet validated. |
| 5. Scientific/visual gate | Direct evidence and visual review active | Original-PDF comparisons for new Figures 17-4 and 17-8 inspected at full resolution; explicit source-vintage distinctions preserved. No external reviewer approval claimed. |
| 6. Unattended calibration | API track superseded by owner direction | Direct in-task research now proceeds without paid calibration or model API credentials. Historical lab tests remain useful infrastructure evidence, not a dependency for figure completion. |
| 7. Existing incomplete figures | First consolidation-enabled repair | Figure 5-3 regained 49 early Sweden years from original GD010 table; exact count/overlap tests pass, both comparisons visually inspected. Remains partial pending independent review. |
| 8. Untouched figures | Direct production active | All Chapter 17 figures have a package; education adds 16-1 and 16-3 verified, 16-2 partial. 29 untouched figures remain. No paid reviewer dependency. |
| 9. Final recovery/review | Not started | Apply new evidence to deferred work and audit all released comparisons. |
| 10. Release | Not started | Fresh-checkout validation, gallery, PDF, release manifest, and completion accounting. |

2026-09-09 checkpoint: approved plan recorded and linked from repository startup
documents. No figures reconstructed, statuses promoted, paid production calls
made, or branches merged as part of this documentation checkpoint.

2026-09-09 execution checkpoint: [validation and exact next actions](../reports/completion_checkpoint_2026_09_09.md).
Consolidation and a source-supported Figure 5-3 repair are now committed; the
earlier paragraph describes plan documentation only, not subsequent execution.

2026-09-09 data-library checkpoint: [SQLite library](../data/database/README.md)
catalogs 321 retained files and imports 65 clean tables / 34,968 rows. All 75
figures have coverage entries. Original files are untouched; exact per-plot input
mapping and automated provider refreshes remain incomplete. Prioritize this
reusable-data work alongside reconstruction, without requiring paid API review.

2026-09-09 direct-production checkpoint: Figure 17-8 adds 21 book-period and
32 version-labelled extended observations (including overlap), plus a 20-row
source-vintage diagnostic. SQLite now retains 345 files, 68 clean tables and
35,041 clean rows. Full-resolution side-by-side inspection is recorded; exact
original-vintage 2015 tourism data remain a targeted recovery task. Archive
searches and rejected data are retained, not silently discarded. The next action
is another untouched figure; the global review PDF will refresh after the next
coherent group. No external API review or new orchestrator work performed.

2026-09-09 next checkpoint: Figure 17-4 recovered the original 706-observation
source series, with numeric cross-checks and actual original-PDF comparisons.
Its revised successor is separate, not silently substituted. Figure 17-7 has
archived source-chain evidence but no usable numeric export; it is excluded
from the visual gallery. The gallery/PDF now contain 28 figures / 56 real
comparison pages. New PDF pages 51-54 were rendered and visually inspected.
SQLite now catalogs 369 files / 71 clean tables / 37,188 rows, retaining earlier
snapshots. All 60 project tests and canonical-state/data-library checks pass.
Next: Figure 17-1, work hours, using the same historical OWID recovery path.
This is a progress checkpoint, not completion of the 75-figure objective.

2026-09-09 work/retirement checkpoint: 17-1 and 17-2 use recovered original
numeric publications, not digitized values. Both remain partial because small
book-level differences remain. 17-1 has no defensible comparable extension;
17-2 adds BLS annual 2011-2024 data with a verified original 2010 anchor and
explicit historical definition caveat. Current library: 394 retained files,
76 clean tables / 37,308 rows. All 63 tests pass. Review PDF: 30 figures,
60 comparison pages; new pages 51-54 rendered and inspected. Next: remaining
Chapter 17 source families, then continue the untouched queue and deferred
recovery. Legacy data-use audit and portable refresh layer remain pending.

2026-09-09 necessities/leisure/appliance checkpoint: 17-5, 17-6 and 17-3 are
partial reconstructions with original numeric evidence, not visual approximations
of missing values. 17-6 replication cells reproduce the original published means;
17-3 has a documented missing housework trajectory and separated stove definitions.
Current library: 446 retained files, 88 clean tables, 39,811 rows. All 68 tests and
canonical-state/library checks pass. Review PDF now 33 figures / 66 pages.
32 untouched figures remain. Next: 16-1 literacy; legacy recovery and typed refresh
library still pending. No paid model APIs or background executor processes used.

2026-09-09 education checkpoint: original archived numerical data support
16-1 literacy and 16-3 schooling as verified reproductions; 16-2 basic education
remains partial. The original OECD spreadsheet has reversed 2000/2010 labels;
its printed table and archived OWID CSV establish the correction, preserved in
the audit data. Schooling's 203 book-period observations exactly match the
archived author workbook. The revised 2015 schooling extension is not the older
forecast. All six new PDF pages (51-56) rendered and visually inspected.
Current library: 493 retained files, 99 clean tables, 41,072 rows. All 71 tests
pass. Review PDF: 36 figures / 72 pages. Next: 16-4 female literacy; 29 untouched
figures and the final recovery, portability, refresh and publication gates remain.

2026-09-09 second education checkpoint: 16-4, 16-5 and 16-6 add three partial
reconstruction packages with real original-reference comparisons. Missing
female-literacy series and the HIHD2015 update remain explicit source gaps;
IQ sample weights remain unaudited. New PDF pages57-62 actually rendered and
inspected, not assumed correct. Review PDF:39 figures/78pages. Library:521
retained files,106 clean tables,41,258 rows. All74 tests and canonical/data
checks pass.26 untouched figures remain. Next:14-1 democracy/autocracy,
then continue the queue and return to targeted recovery and the data-use audit.

2026-09-10 direct-production checkpoint: Figure 14-4 was committed as a
partial reconstruction with archived DPIC/Espy records, Census population
sources, explicit inferred decade averaging, and a 2017-2025 annual successor.
Figure 11-1 was then processed as a partial reconstruction from the archived
Human Progress publication-layer CSV of the Levy and Thompson series. The
recovered 25-year trajectory was visually inspected against the original PDF;
the blank 1988 cell, separately described 2000-2015 interval, and derived
zero-war continuation are disclosed rather than treated as exact source rows.
The data library now catalogs 591 retained files, 123 clean tables, and 58,997
clean rows. The visual baseline is 43 figures / 86 real comparison pages. All
82 tests and canonical-state/data-library checks pass. Twenty-one figures remain
untouched. Next: continue with the next public-source candidate, while retaining
the exact Levy/Thompson table and successor export as targeted recovery work.
