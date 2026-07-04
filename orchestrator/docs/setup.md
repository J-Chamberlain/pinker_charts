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

Run several local Codex tasks with supervisor decisions:

```bash
python -m orchestrator.supervisor \
  --config examples/pinker_charts.config.example.yaml \
  --mode local-loop \
  --max-iterations 3 \
  --non-dry-run
```

Each iteration selects one eligible task, launches Codex, generates a review packet, runs the configured reviewer, runs the configured supervisor decision engine, and saves the final loop decision under the run directory. The loop stops on `needs_manual_review` or `remediate` unless `--allow-remediation` is passed.

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

Use GPT supervision:

```yaml
supervisor:
  kind: openai
  model: gpt-5.5-thinking
```

The config must select `supervisor.kind: openai` and `OPENAI_API_KEY` must be present. Without both, NoopSupervisor returns `needs_manual_review`. A supervisor `accept` does not merge the worker branch; it only marks the run metadata.
