# Operating Modes

## plan-only

Reads repository state, selects the next task, and prints the proposed issue/card. No external calls.

## issue-only

Creates or dry-runs a GitHub issue for the next task. Non-dry-run requires `GITHUB_TOKEN` and `--non-dry-run`.

## review-only

Runs the configured reviewer against a placeholder/latest task execution artifact. Current reviewer implementations are no-op or safe stubs.

## loop-dry-run

Simulates several supervisor iterations without external calls.

## local-loop

Reserved for environments where executor and reviewer CLIs are explicitly configured. Safe defaults prevent unreviewed executor calls; the Codex executor currently emits a `codex exec ...` command in dry-run mode.

## Recommended Pinker Charts Use

Start with:

```bash
python -m orchestrator.supervisor --config examples/pinker_charts.config.example.yaml --mode plan-only
```

Then use `issue-only` to queue one figure at a time for a worker agent.
