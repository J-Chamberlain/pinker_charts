# Setup

Install locally:

```bash
cd orchestrator
python -m venv .venv
. .venv/bin/activate
pip install -e ".[test]"
```

Plan the next Pinker Charts task:

```bash
python -m orchestrator.supervisor \
  --config examples/pinker_charts.config.example.yaml \
  --mode plan-only
```

Dry-run a GitHub issue:

```bash
python -m orchestrator.supervisor \
  --config examples/pinker_charts.config.example.yaml \
  --mode issue-only
```

Create a GitHub issue:

```bash
export GITHUB_TOKEN=...
python -m orchestrator.supervisor \
  --config examples/pinker_charts.config.example.yaml \
  --mode issue-only \
  --non-dry-run
```

If direct Codex execution becomes available in a target environment, configure:

```yaml
executor:
  kind: codex_cli
  command: codex
  dry_run: true
```

The scaffold prints the intended `codex exec ...` command in dry-run mode. Non-dry-run execution requires an explicit iteration budget and a clean worktree.

Run one local Codex task:

```bash
python -m orchestrator.supervisor \
  --config examples/pinker_charts.config.example.yaml \
  --mode local-loop \
  --max-iterations 1 \
  --non-dry-run
```

This creates a task branch, captures stdout/stderr/status logs under `orchestrator/runs/`, inspects git status after Codex exits, and does not merge or mark the task accepted.

Review the latest run without external calls:

```bash
python -m orchestrator.supervisor \
  --config examples/pinker_charts.config.example.yaml \
  --mode review-only \
  --latest-run
```

Review the latest run with OpenAI:

```bash
export OPENAI_API_KEY=...
python -m orchestrator.supervisor \
  --config examples/pinker_charts.config.example.yaml \
  --mode review-only \
  --latest-run \
  --non-dry-run
```

The config must select `reviewer.kind: openai`. If the key is missing, the supervisor keeps the run in Noop/manual-review mode. If the API call fails or the model returns invalid JSON, the OpenAI reviewer fails closed to `needs_manual_review`.
