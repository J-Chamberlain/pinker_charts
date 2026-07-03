# Orchestrator Scaffold

This package is a reusable supervisor-worker orchestration scaffold for GitHub-backed research and code projects.

It is intentionally conservative:

- GitHub is the shared state and message bus.
- Dry-run is the default.
- API keys are read only from environment variables.
- Executors work on branches or issues, not directly on `main`.
- Reviewers can run in no-op mode with no paid APIs.

## Quick Start

From this directory:

```bash
python -m orchestrator.supervisor \
  --config examples/pinker_charts.config.example.yaml \
  --mode plan-only
```

To draft a GitHub issue without creating it:

```bash
python -m orchestrator.supervisor \
  --config examples/pinker_charts.config.example.yaml \
  --mode issue-only
```

To actually create an issue, set `GITHUB_TOKEN` and pass `--non-dry-run`.

```bash
GITHUB_TOKEN=... python -m orchestrator.supervisor \
  --config examples/pinker_charts.config.example.yaml \
  --mode issue-only \
  --non-dry-run
```

## What Works Now

- Reads project state, registry CSV, and optional review manifest.
- Selects the next eligible Pinker Charts figure.
- Generates a full GitHub issue body for the selected task.
- Supports dry-run supervisor modes.
- Provides no-op, Codex CLI command emitter, GitHub issue, OpenAI reviewer stub, and Anthropic reviewer stub interfaces.
- Runs tests without API keys.

## What Is Stubbed

- Non-interactive Codex execution is represented by a dry-run `codex exec ...` command emitter, but not launched automatically.
- OpenAI and Anthropic reviewer classes are safe stubs until wired to the preferred SDK.
- Supervisor acceptance/remediation decisions are represented in schemas but not yet persisted to GitHub labels or project boards.

## Package Layout

- `orchestrator/adapters/`: project-specific adapters.
- `orchestrator/executors/`: worker-launch or issue-creation implementations.
- `orchestrator/models/`: reviewer implementations.
- `orchestrator/supervisor.py`: CLI and loop coordinator.
- `docs/`: architecture, setup, security model, and operating modes.
