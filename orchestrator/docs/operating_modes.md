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

Runs one local executor task at a time. Dry-run mode emits the branch name and `codex exec ...` command without side effects.

Non-dry-run local-loop requires:

- `--non-dry-run`
- `--max-iterations` with a positive integer
- a clean git worktree

For each task, the executor:

1. Creates a per-task branch such as `codex/4-1-tone-of-the-news-1945-2010`.
2. Runs `codex exec -C <repo> <generated prompt>`.
3. Captures stdout, stderr, metadata, summary, and git status in `orchestrator/runs/<run-id>/`.
4. Stops after execution and does not merge or mark accepted.

## Recommended Pinker Charts Use

Start with:

```bash
python -m orchestrator.supervisor --config examples/pinker_charts.config.example.yaml --mode plan-only
```

Then use `issue-only` to queue one figure at a time for a worker agent.
