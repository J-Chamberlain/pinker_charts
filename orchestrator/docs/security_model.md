# Security Model

This file intentionally duplicates the security principles in the README in more operational detail.

1. Dry-run is the default.
2. API keys are read only from environment variables.
3. No secrets are committed.
4. Executors work on branches or GitHub issues, never directly on `main`.
5. Reviewers can be read-only.
6. Supervisor is the only component allowed to mark work accepted.
7. Destructive actions require explicit configuration and are not implemented in the scaffold.
8. Supervisor logs are written only in non-dry-run modes.
9. Local-loop refuses to launch Codex unless the worktree is clean.
10. Local-loop creates a per-task branch and never auto-merges.
11. Local-loop captures execution logs under `orchestrator/runs/`; these logs are ignored by git by default.
12. Review-only may push a worker branch only when explicitly run with `--non-dry-run`; acceptance still requires a reviewer result.

Required environment variables:

- `GITHUB_TOKEN`: only for non-dry-run GitHub issue creation.
- `OPENAI_API_KEY`: only for non-dry-run OpenAI reviewer calls when config selects `reviewer.kind: openai`.
- `OPENAI_REVIEWER_MODEL`: optional OpenAI reviewer model override.
- `ANTHROPIC_API_KEY`: only for future Anthropic reviewer implementation.

Noop review is the default. The OpenAI reviewer fails closed to `needs_manual_review` if credentials are missing, the API call fails, or the model response cannot be parsed as valid JSON. Anthropic review remains a safe stub.
