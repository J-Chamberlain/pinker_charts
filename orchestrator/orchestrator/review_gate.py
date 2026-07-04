from __future__ import annotations

import json
import subprocess
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .reviewer_interface import Reviewer
from .schemas import ExecutionResult, ReviewResult, SupervisorDecision, Task


def latest_run_dir(runs_dir: Path) -> Path | None:
    if not runs_dir.exists():
        return None
    candidates = [path for path in runs_dir.iterdir() if path.is_dir() and (path / "metadata.json").exists()]
    return sorted(candidates)[-1] if candidates else None


def load_run_json(run_dir: Path, name: str) -> dict[str, Any]:
    path = run_dir / name
    return json.loads(path.read_text()) if path.exists() else {}


def _git(repo_root: Path, args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=repo_root, text=True, capture_output=True, check=False)


def _ok_text(proc: subprocess.CompletedProcess[str]) -> str:
    return proc.stdout.strip() if proc.returncode == 0 else (proc.stderr or proc.stdout).strip()


def branch_exists(repo_root: Path, branch: str) -> bool:
    return _git(repo_root, ["rev-parse", "--verify", "--quiet", branch]).returncode == 0


def detect_worker_commit(repo_root: Path, branch: str, base_ref: str = "HEAD") -> tuple[str | None, list[str], list[str]]:
    if not branch or not branch_exists(repo_root, branch):
        return None, [], []
    merge_base = _git(repo_root, ["merge-base", base_ref, branch])
    base = merge_base.stdout.strip() if merge_base.returncode == 0 else base_ref
    head = _git(repo_root, ["rev-parse", "--short", branch])
    log = _git(repo_root, ["log", "--oneline", f"{base}..{branch}"])
    changed = _git(repo_root, ["diff", "--name-only", f"{base}..{branch}"])
    commits = [line for line in log.stdout.splitlines() if line.strip()]
    files = [line for line in changed.stdout.splitlines() if line.strip()]
    return (_ok_text(head) or None), commits, files


def push_worker_branch(repo_root: Path, branch: str, dry_run: bool = True) -> dict[str, Any]:
    if dry_run:
        return {"pushed": False, "dry_run": True, "message": f"Would push branch {branch}."}
    proc = _git(repo_root, ["push", "-u", "origin", branch])
    return {
        "pushed": proc.returncode == 0,
        "dry_run": False,
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    }


def build_review_packet(
    task: Task,
    run_dir: Path,
    branch: str,
    worker_commit: str | None,
    commits: list[str],
    changed_files: list[str],
    push_result: dict[str, Any],
) -> str:
    files = "\n".join(f"- `{path}`" for path in changed_files) or "- None detected"
    commit_lines = "\n".join(f"- {line}" for line in commits) or "- None detected"
    required = "\n".join(f"- `{path}`" for path in task.files_to_update)
    criteria = "\n".join(f"- {item}" for item in task.acceptance_criteria)
    return f"""# Review Packet: {task.id} — {task.title}

Generated: {datetime.now(UTC).isoformat()}

## Worker Run

- Run directory: `{run_dir}`
- Worker branch: `{branch}`
- Worker commit: `{worker_commit or "not detected"}`
- Push result: `{push_result.get("message") or push_result.get("pushed")}`

## Commit Summary

{commit_lines}

## Changed Files

{files}

## Expected Files

{required}

## Acceptance Criteria

{criteria}

## Reviewer Questions

- Was the task completed or honestly blocked?
- Were registry and PROJECT_STATE updated if task state changed?
- Were comparison artifacts created where applicable?
- Is status calibration appropriate?
- Should the next action be accept, remediate, or blocked?
"""


def classify_decision(review: ReviewResult, worker_commit: str | None, changed_files: list[str]) -> str:
    if review.decision in {"accept", "remediate", "blocked", "needs_manual_review"}:
        return review.decision
    if not worker_commit:
        return "blocked"
    if not changed_files:
        return "blocked"
    return "needs_manual_review"


def run_review_gate(
    repo_root: Path,
    runs_dir: Path,
    task: Task,
    reviewer: Reviewer,
    run_dir: Path | None = None,
    dry_run: bool = True,
    push_branch: bool = True,
) -> SupervisorDecision:
    run_dir = run_dir or latest_run_dir(runs_dir)
    if run_dir is None:
        return SupervisorDecision(action="blocked", reason="No run directory found for review.", task=task)
    metadata = load_run_json(run_dir, "metadata.json")
    summary = load_run_json(run_dir, "summary.json")
    branch = metadata.get("branch") or summary.get("branch") or ""
    base_ref = metadata.get("base_branch") or "HEAD"
    worker_commit, commits, changed_files = detect_worker_commit(repo_root, branch, base_ref=base_ref)
    push_result = (
        push_worker_branch(repo_root, branch, dry_run=dry_run)
        if push_branch and branch
        else {"pushed": False, "message": "Worker branch push skipped."}
    )
    packet = build_review_packet(task, run_dir, branch, worker_commit, commits, changed_files, push_result)
    (run_dir / "review_packet.md").write_text(packet)
    execution = ExecutionResult(
        task=task,
        mode="review-gate",
        success=bool(worker_commit),
        message=packet,
        branch=branch,
        commit=worker_commit,
        artifacts=(str(run_dir / "review_packet.md"),),
    )
    review = reviewer.review(execution)
    decision = classify_decision(review, worker_commit, changed_files)
    review_payload = asdict(review)
    (run_dir / "review_result.json").write_text(json.dumps(review_payload, indent=2, default=str) + "\n")
    decision_payload = {
        "task_id": task.id,
        "task_title": task.title,
        "run_dir": str(run_dir),
        "worker_branch": branch,
        "worker_commit": worker_commit,
        "base_ref": base_ref,
        "commit_summary": commits,
        "changed_files": changed_files,
        "push_result": push_result,
        "reviewer": review.reviewer,
        "review_decision": review.decision,
        "supervisor_decision": decision,
        "accepted": decision == "accept",
        "next_action": decision,
        "generated_at": datetime.now(UTC).isoformat(),
    }
    (run_dir / "supervisor_decision.json").write_text(json.dumps(decision_payload, indent=2, default=str) + "\n")
    return SupervisorDecision(action=decision, reason=review.summary, task=task, execution=execution, review=review)
