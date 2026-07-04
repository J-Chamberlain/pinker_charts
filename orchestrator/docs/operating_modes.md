# Operating Modes

## plan-only

Reads repository state, selects the next task, and prints the proposed issue/card. No external calls.

## issue-only

Creates or dry-runs a GitHub issue for the next task. Non-dry-run requires `GITHUB_TOKEN` and `--non-dry-run`.

## review-only

Runs the configured reviewer against a latest task execution artifact when
`--latest-run` is supplied. The supervisor generates:

- `review_packet.md`
- `review_result.json`
- `supervisor_decision.json`
- `final_loop_decision.json`
- `raw_model_response.txt`, when an external model response is available
- `parsed_reviewer_result.json`, when a reviewer returns normalized JSON
- `raw_supervisor_response.txt`, when an external supervisor response is available
- `parsed_supervisor_decision.json`, when a supervisor returns normalized JSON
- `remediation_prompt.md`, when supervisor requests remediation

Dry-run review-only does not push worker branches. With `--non-dry-run`, the
supervisor may push the detected worker branch, but still does not merge or
mark the result accepted.

Noop review is the default. OpenAI review runs only when the config selects
`reviewer.kind: openai`, `OPENAI_API_KEY` is present, and the command is run
with `--non-dry-run`. The required reviewer decisions are `accept`,
`remediate`, `blocked`, and `needs_manual_review`.

Noop supervision is the default. OpenAI supervision runs only when the config
selects `supervisor.kind: openai`, `OPENAI_API_KEY` is present, and the command
is run with `--non-dry-run`. The supervisor decision controls the loop.

## loop-dry-run

Simulates several supervisor iterations without external calls.

## local-loop

Runs one local executor task at a time. Dry-run mode emits the branch name and `codex exec ...` command without side effects.

Non-dry-run local-loop requires:

- `--non-dry-run`
- `--max-iterations` with a positive integer
- a clean git worktree

For each task, the loop:

1. Creates a per-task branch such as `codex/4-1-tone-of-the-news-1945-2010`.
2. Runs `codex exec -C <repo> <generated prompt>`.
3. Captures stdout, stderr, metadata, summary, and git status in `orchestrator/runs/<run-id>/`.
4. Builds a review packet.
5. Runs the configured reviewer.
6. Runs the configured supervisor decision engine.
7. Records the final loop decision and never merges automatically.

`accept` and `blocked` may continue to the next task if the worktree is clean
and iteration budget remains. `remediate` writes `remediation_prompt.md` and
stops unless `--allow-remediation` is passed. `needs_manual_review` always
stops.

## Recommended Pinker Charts Use

Start with:

```bash
python -m orchestrator.supervisor --config examples/pinker_charts.config.example.yaml --mode plan-only
```

Then use `issue-only` to queue one figure at a time for a worker agent.
