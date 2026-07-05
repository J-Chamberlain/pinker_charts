from __future__ import annotations

import json
import shlex
import subprocess
from datetime import UTC, datetime
from pathlib import Path
import re

from ..executor_interface import Executor
from ..schemas import ExecutionResult, Task


class CodexCLIExecutor(Executor):
    def __init__(
        self,
        command: str | None = None,
        dry_run: bool = True,
        repo_root: Path | None = None,
        branch_prefix: str = "codex",
        runs_dir: Path | None = None,
        timeout_seconds: int | None = None,
    ) -> None:
        self.command = command or "codex"
        self.dry_run = dry_run
        self.repo_root = repo_root or Path.cwd()
        self.branch_prefix = branch_prefix.strip("/") or "codex"
        self.runs_dir = runs_dir or self.repo_root / "orchestrator/runs"
        self.timeout_seconds = timeout_seconds

    def _slug(self, text: str) -> str:
        slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
        return slug[:48] or "task"

    def branch_name(self, task: Task) -> str:
        return f"{self.branch_prefix}/{task.id}-{self._slug(task.title)}"

    def build_prompt(self, task: Task) -> str:
        files = "\n".join(f"- {path}" for path in task.files_to_update)
        criteria = "\n".join(f"- {item}" for item in task.acceptance_criteria)
        review = "\n".join(f"- {item}" for item in task.review_requirements)
        return f"""You are an executor agent working on one isolated task.

Repository workflow rules:
- Work only on the current branch.
- Do not merge to main or production-loop.
- Do not mark the task accepted; reviewer/supervisor acceptance is separate.
- Commit one clean unit if work is completed or blocked in a documented way.
- If the figure/task becomes difficult, document the blocker honestly and stop with a useful source-recovery artifact.

Task:
- id: {task.id}
- title: {task.title}
- current status: {task.status}
- source reference: {task.source_reference}
- next action: {task.next_action}

Acceptance criteria:
{criteria}

Files expected to update:
{files}

Review requirements:
{review}
"""

    def build_command(self, task: Task) -> str:
        prompt = self.build_prompt(task)
        return f"{shlex.quote(self.command)} exec -C {shlex.quote(str(self.repo_root))} {shlex.quote(prompt)}"

    def _run_git(self, args: list[str]) -> subprocess.CompletedProcess[str]:
        return subprocess.run(["git", *args], cwd=self.repo_root, text=True, capture_output=True, check=False)

    def _ensure_clean_worktree(self) -> str | None:
        status = self._run_git(["status", "--short"])
        if status.returncode != 0:
            return status.stderr or status.stdout or "git status failed"
        if status.stdout.strip():
            return f"Worktree is not clean:\n{status.stdout}"
        return None

    def _create_task_branch(self, task: Task) -> str:
        base = self.branch_name(task)
        name = base
        existing = self._run_git(["rev-parse", "--verify", "--quiet", name])
        if existing.returncode == 0:
            stamp = datetime.now(UTC).strftime("%Y%m%d%H%M%S")
            name = f"{base}-{stamp}"
        created = self._run_git(["switch", "-c", name])
        if created.returncode != 0:
            raise RuntimeError(created.stderr or created.stdout or f"failed to create branch {name}")
        return name

    def _current_branch(self) -> str:
        branch = self._run_git(["branch", "--show-current"])
        return branch.stdout.strip() if branch.returncode == 0 else ""

    def _switch_branch(self, branch: str) -> None:
        switched = self._run_git(["switch", branch])
        if switched.returncode != 0:
            raise RuntimeError(switched.stderr or switched.stdout or f"failed to switch to branch {branch}")

    def execute(self, task: Task) -> ExecutionResult:
        command = self.build_command(task)
        branch = self.branch_name(task)
        if self.dry_run:
            return ExecutionResult(task=task, mode="codex-cli-dry-run", success=True, branch=branch, message=f"Would create/switch branch `{branch}` and run: {command}")

        dirty = self._ensure_clean_worktree()
        if dirty:
            return ExecutionResult(task=task, mode="codex-cli", success=False, branch=branch, message=dirty)

        run_id = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ") + f"_{task.id.replace('-', '_')}"
        run_dir = self.runs_dir / run_id
        run_dir.mkdir(parents=True, exist_ok=True)
        base_branch = self._current_branch()
        actual_branch = self._create_task_branch(task)
        prompt = self.build_prompt(task)
        argv = [self.command, "exec", "-C", str(self.repo_root), prompt]
        metadata = {
            "task_id": task.id,
            "task_title": task.title,
            "branch": actual_branch,
            "base_branch": base_branch,
            "argv": argv,
            "started_at": datetime.now(UTC).isoformat(),
            "timeout_seconds": self.timeout_seconds,
        }
        (run_dir / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
        try:
            proc = subprocess.run(
                argv,
                cwd=self.repo_root,
                text=True,
                capture_output=True,
                timeout=self.timeout_seconds,
                check=False,
            )
            timed_out = False
        except subprocess.TimeoutExpired as exc:
            proc = subprocess.CompletedProcess(argv, returncode=124, stdout=exc.stdout or "", stderr=exc.stderr or "")
            timed_out = True
        (run_dir / "stdout.log").write_text(proc.stdout or "")
        (run_dir / "stderr.log").write_text(proc.stderr or "")
        status = self._run_git(["status", "--short", "--branch"])
        (run_dir / "git_status.txt").write_text((status.stdout or "") + (status.stderr or ""))
        summary = {
            **metadata,
            "finished_at": datetime.now(UTC).isoformat(),
            "returncode": proc.returncode,
            "timed_out": timed_out,
            "git_status_returncode": status.returncode,
        }
        (run_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
        message = f"Codex execution finished with return code {proc.returncode}. Logs: {run_dir}. Git status inspected and saved."
        if timed_out:
            message = f"Codex execution timed out. Logs: {run_dir}. Git status inspected and saved."
        return ExecutionResult(
            task=task,
            mode="codex-cli",
            success=proc.returncode == 0,
            branch=actual_branch,
            message=message,
            artifacts=tuple(str(path) for path in [run_dir / "stdout.log", run_dir / "stderr.log", run_dir / "git_status.txt", run_dir / "summary.json"]),
        )

    def execute_remediation(
        self,
        task: Task,
        branch: str,
        prompt: str,
        parent_run_id: str | None = None,
        remediation_reason: str | None = None,
        remediation_items: tuple[str, ...] = (),
    ) -> ExecutionResult:
        command = f"{shlex.quote(self.command)} exec -C {shlex.quote(str(self.repo_root))} {shlex.quote(prompt)}"
        if self.dry_run:
            linkage = ""
            if parent_run_id:
                linkage = f"\nParent run: `{parent_run_id}`\nRemediation reason: {remediation_reason or ''}\n"
            return ExecutionResult(task=task, mode="codex-cli-remediation-dry-run", success=True, branch=branch, message=f"Would switch to `{branch}` and run remediation: {command}{linkage}")

        dirty = self._ensure_clean_worktree()
        if dirty:
            return ExecutionResult(task=task, mode="codex-cli-remediation", success=False, branch=branch, message=dirty)
        if self._current_branch() != branch:
            self._switch_branch(branch)

        run_id = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ") + f"_{task.id.replace('-', '_')}_remediation"
        run_dir = self.runs_dir / run_id
        run_dir.mkdir(parents=True, exist_ok=True)
        argv = [self.command, "exec", "-C", str(self.repo_root), prompt]
        metadata = {
            "task_id": task.id,
            "task_title": task.title,
            "branch": branch,
            "base_branch": branch,
            "argv": argv,
            "remediation": True,
            "parent_run_id": parent_run_id,
            "remediates_task_id": task.id,
            "remediation_reason": remediation_reason,
            "remediation_items": list(remediation_items),
            "started_at": datetime.now(UTC).isoformat(),
            "timeout_seconds": self.timeout_seconds,
        }
        (run_dir / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
        try:
            proc = subprocess.run(
                argv,
                cwd=self.repo_root,
                text=True,
                capture_output=True,
                timeout=self.timeout_seconds,
                check=False,
            )
            timed_out = False
        except subprocess.TimeoutExpired as exc:
            proc = subprocess.CompletedProcess(argv, returncode=124, stdout=exc.stdout or "", stderr=exc.stderr or "")
            timed_out = True
        (run_dir / "stdout.log").write_text(proc.stdout or "")
        (run_dir / "stderr.log").write_text(proc.stderr or "")
        status = self._run_git(["status", "--short", "--branch"])
        (run_dir / "git_status.txt").write_text((status.stdout or "") + (status.stderr or ""))
        summary = {
            **metadata,
            "finished_at": datetime.now(UTC).isoformat(),
            "returncode": proc.returncode,
            "timed_out": timed_out,
            "git_status_returncode": status.returncode,
        }
        (run_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
        message = f"Codex remediation finished with return code {proc.returncode}. Logs: {run_dir}. Git status inspected and saved."
        if timed_out:
            message = f"Codex remediation timed out. Logs: {run_dir}. Git status inspected and saved."
        return ExecutionResult(
            task=task,
            mode="codex-cli-remediation",
            success=proc.returncode == 0,
            branch=branch,
            message=message,
            artifacts=tuple(str(path) for path in [run_dir / "stdout.log", run_dir / "stderr.log", run_dir / "git_status.txt", run_dir / "summary.json"]),
        )
