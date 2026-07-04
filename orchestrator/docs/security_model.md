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

Required environment variables:

- `GITHUB_TOKEN`: only for non-dry-run GitHub issue creation.
- `OPENAI_API_KEY`: only for future OpenAI reviewer implementation.
- `ANTHROPIC_API_KEY`: only for future Anthropic reviewer implementation.

The current reviewer classes are safe stubs. They do not call external model APIs.
