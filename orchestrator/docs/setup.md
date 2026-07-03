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

The scaffold currently prints the intended `codex exec ...` command in dry-run mode. Non-dry-run execution remains guarded until branch, sandbox, and authentication behavior are explicitly configured for the target environment.
