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
- Provides no-op, Codex CLI command emitter, GitHub issue, optional OpenAI reviewer, and Anthropic reviewer stub interfaces.
- Runs one-task-at-a-time local Codex execution in explicit non-dry-run mode, with per-task branches and run logs.
- Runs tests without API keys.

## What Is Stubbed

- Non-interactive Codex execution requires `local-loop --non-dry-run --max-iterations N`; dry-run remains the default.
- Anthropic reviewer is a safe stub. OpenAI reviewer is optional and only calls the API when `reviewer.kind: openai`, `OPENAI_API_KEY` is set, and the run is non-dry-run.
- Supervisor acceptance/remediation decisions are represented in schemas but not yet persisted to GitHub labels or project boards.

## Optional OpenAI Review Gate

Noop review remains the default. To use OpenAI for review-only or local-loop gates:

1. Set `OPENAI_API_KEY` in the environment.
2. Set `reviewer.kind: openai` in the YAML config.
3. Run with `--non-dry-run` when external calls are intended.

The reviewer writes normalized output to `review_result.json`. When a model call is made, the gate also saves `raw_model_response.txt` and `parsed_reviewer_result.json` under the same `orchestrator/runs/<run-id>/` directory.

## Package Layout

- `orchestrator/adapters/`: project-specific adapters.
- `orchestrator/executors/`: worker-launch or issue-creation implementations.
- `orchestrator/models/`: reviewer implementations.
- `orchestrator/supervisor.py`: CLI and loop coordinator.
- `docs/`: architecture, setup, security model, and operating modes.
