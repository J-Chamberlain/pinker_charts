from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class GitHubConfig:
    owner: str
    repo: str
    base_branch: str = "main"
    token_env: str = "GITHUB_TOKEN"
    api_url: str = "https://api.github.com"

    @property
    def token(self) -> str | None:
        return os.environ.get(self.token_env)


@dataclass(frozen=True)
class ExecutorConfig:
    kind: str = "noop"
    command: str | None = None
    dry_run: bool = True
    branch_prefix: str = "codex"
    runs_dir: Path | None = None
    timeout_seconds: int | None = None


@dataclass(frozen=True)
class ReviewerConfig:
    kind: str = "noop"
    model: str | None = None
    dry_run: bool = True


@dataclass(frozen=True)
class SupervisorEngineConfig:
    kind: str = "noop"
    model: str | None = None
    dry_run: bool = True


@dataclass(frozen=True)
class LoopConfig:
    max_iterations: int = 1
    allow_remediation: bool = False


@dataclass(frozen=True)
class ProjectConfig:
    name: str
    adapter: str
    root: Path
    state_file: Path
    registry_file: Path | None = None
    review_manifest: Path | None = None
    default_labels: tuple[str, ...] = ()
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class OrchestratorConfig:
    project: ProjectConfig
    github: GitHubConfig | None = None
    executor: ExecutorConfig = field(default_factory=ExecutorConfig)
    reviewer: ReviewerConfig = field(default_factory=ReviewerConfig)
    supervisor: SupervisorEngineConfig = field(default_factory=SupervisorEngineConfig)
    loop: LoopConfig = field(default_factory=LoopConfig)
    loop_budget: int = 1
    dry_run: bool = True


def _as_path(value: str | None, base: Path) -> Path | None:
    if value is None:
        return None
    path = Path(value).expanduser()
    return path if path.is_absolute() else base / path


def load_config(path: str | Path) -> OrchestratorConfig:
    config_path = Path(path).expanduser().resolve()
    data = yaml.safe_load(config_path.read_text()) or {}
    project_data = data.get("project", {})
    project_root = _as_path(project_data.get("root", "."), config_path.parent) or config_path.parent
    project = ProjectConfig(
        name=project_data.get("name", "unnamed-project"),
        adapter=project_data.get("adapter", "generic"),
        root=project_root.resolve(),
        state_file=_as_path(project_data.get("state_file", "PROJECT_STATE.md"), project_root) or project_root / "PROJECT_STATE.md",
        registry_file=_as_path(project_data.get("registry_file"), project_root),
        review_manifest=_as_path(project_data.get("review_manifest"), project_root),
        default_labels=tuple(project_data.get("default_labels", ())),
        extra={k: v for k, v in project_data.items() if k not in {"name", "adapter", "root", "state_file", "registry_file", "review_manifest", "default_labels"}},
    )
    github_data = data.get("github")
    github = None
    if github_data:
        github = GitHubConfig(
            owner=github_data["owner"],
            repo=github_data["repo"],
            base_branch=github_data.get("base_branch", "main"),
            token_env=github_data.get("token_env", "GITHUB_TOKEN"),
            api_url=github_data.get("api_url", "https://api.github.com"),
        )
    executor_data = data.get("executor", {})
    reviewer_data = data.get("reviewer", {})
    supervisor_data = data.get("supervisor", {})
    loop_data = data.get("loop", {})
    dry_run = bool(data.get("dry_run", True))
    loop_budget = int(loop_data.get("max_iterations", data.get("loop_budget", 1)))
    return OrchestratorConfig(
        project=project,
        github=github,
        executor=ExecutorConfig(
            kind=executor_data.get("kind", "noop"),
            command=executor_data.get("command") or os.environ.get("CODEX_CLI_COMMAND"),
            dry_run=bool(executor_data.get("dry_run", dry_run)),
            branch_prefix=executor_data.get("branch_prefix", "codex"),
            runs_dir=_as_path(executor_data.get("runs_dir"), project_root),
            timeout_seconds=executor_data.get("timeout_seconds"),
        ),
        reviewer=ReviewerConfig(
            kind=reviewer_data.get("kind", "noop"),
            model=reviewer_data.get("model"),
            dry_run=bool(reviewer_data.get("dry_run", dry_run)),
        ),
        supervisor=SupervisorEngineConfig(
            kind=supervisor_data.get("kind", "noop"),
            model=supervisor_data.get("model"),
            dry_run=bool(supervisor_data.get("dry_run", dry_run)),
        ),
        loop=LoopConfig(
            max_iterations=loop_budget,
            allow_remediation=bool(loop_data.get("allow_remediation", False)),
        ),
        loop_budget=loop_budget,
        dry_run=dry_run,
    )
