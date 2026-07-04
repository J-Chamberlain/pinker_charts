# Architecture

The orchestration scaffold uses GitHub as both durable state and coordination surface.

## Loop

1. Supervisor reads repository state.
2. Project adapter converts repository state into tasks.
3. Task selector chooses the next eligible unit.
4. Executor creates a GitHub issue, opens a branch/PR, or emits a dry-run command.
5. Reviewer audits the resulting work artifact.
6. Supervisor decision engine reads the task, worker commit, changed files, review packet, reviewer result, and current project state.
7. Supervisor decides whether to accept, remediate, block, require manual review, or continue.
8. State is committed back to the repository by workers only; supervisor decisions are saved as run artifacts unless a future integration explicitly updates GitHub labels or boards.

In non-dry-run modes, supervisor decisions can be appended to
`.orchestrator/supervisor.log` inside the target repository. Dry-run modes do
not write this log.

## Core Concepts

- **Adapter**: project-specific bridge from files to task objects.
- **Task**: model-agnostic work unit with acceptance criteria and review requirements.
- **Executor**: worker launcher or task queue writer.
- **Reviewer**: model or no-op auditor that evaluates the worker output.
- **Supervisor**: model or no-op decision engine. It is the only component allowed to mark a run accepted, and acceptance is currently limited to run metadata.

## Model Agnosticism

Executor, reviewer, and supervisor interfaces intentionally do not depend on one vendor. Implementations can wrap Codex CLI, Claude Code, OpenAI, Anthropic, GitHub issues, or local shell workflows.

## Decision Engine

The decision engine returns structured JSON:

```json
{
  "decision": "accept | remediate | blocked | needs_manual_review",
  "confidence": "low | medium | high",
  "rationale": "...",
  "registry_update": "...",
  "next_action": "...",
  "followup_task_prompt": "...",
  "continue_loop": true
}
```

`accept` records acceptance in the run directory only. `remediate` writes a remediation prompt and stops by default. `blocked` records the blocker and allows the loop to move to another eligible task if budget remains. `needs_manual_review` stops the loop.

## Pinker Charts Adapter

The included adapter reads:

- `PROJECT_STATE.md`
- `data/figure_registry.csv`
- `output/pdf/recreated_figures_review_scroll.manifest.json`

It selects the next `not_started` figure and emits a task package that includes required repository updates and review criteria.

## Generic CSV Adapter

The `generic_csv` adapter supports a minimal registry with columns such as
`id`, `title`, and `status`. It is intended as a starter adapter for future
projects before they grow project-specific evidence and review rules.
