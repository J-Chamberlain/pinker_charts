from __future__ import annotations

import json
import subprocess
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .reviewer_interface import Reviewer
from .run_record import RunRecord, is_reviewable, load_run_record, update_run_record, utc_now
from .schemas import ExecutionResult, ProjectState, ReviewResult, SupervisorDecision, SupervisorEngineResult, Task
from .submission_package import build_submission_package
from .supervisor_interface import DecisionEngine


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


def dirty_files_from_status(status_text: str) -> list[str]:
    files: list[str] = []
    for line in status_text.splitlines():
        if not line or line.startswith("##") or len(line) < 4:
            continue
        path = line[3:].strip()
        if " -> " in path:
            path = path.split(" -> ", 1)[1].strip()
        if path:
            files.append(path)
    return files


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
    *,
    base_sha: str | None = None,
    head_sha: str | None = None,
    run_type: str | None = None,
    reviewable: bool = True,
    reviewable_reason: str = "reviewable",
    dirty_worktree_files: list[str] | None = None,
) -> str:
    files = "\n".join(f"- `{path}`" for path in changed_files) or "- None detected"
    commit_lines = "\n".join(f"- {line}" for line in commits) or "- None detected"
    required = "\n".join(f"- `{path}`" for path in task.files_to_update)
    criteria = "\n".join(f"- {item}" for item in task.acceptance_criteria)
    return f"""# Review Packet: {task.id} — {task.title}

Generated: {datetime.now(UTC).isoformat()}

## Worker Run

- Run directory: `{run_dir}`
- Run type: `{run_type or "unknown"}`
- Worker branch: `{branch}`
- Base SHA: `{base_sha or "not recorded"}`
- Head SHA: `{head_sha or "not recorded"}`
- Worker commit: `{worker_commit or "not detected"}`
- Transaction reviewable: `{reviewable}` ({reviewable_reason})
- Dirty worktree files: `{", ".join(dirty_worktree_files or []) or "none"}`
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


def _engine_context(
    task: Task,
    run_dir: Path,
    branch: str,
    worker_commit: str | None,
    commits: list[str],
    changed_files: list[str],
    packet: str,
    review_payload: dict[str, Any],
    project_state: ProjectState | None,
) -> dict[str, Any]:
    state_excerpt = ""
    registry_rows: list[dict[str, str]] = []
    if project_state:
        state_excerpt = project_state.raw_state[:12000]
        registry_rows = [row for row in project_state.registry_rows if row.get("figure_id") == task.id or row.get("task_id") == task.id]
    return {
        "task": {
            "id": task.id,
            "title": task.title,
            "status": task.status,
            "lifecycle_stage": task.lifecycle_stage,
            "next_action": task.next_action,
            "files_to_update": task.files_to_update,
            "acceptance_criteria": task.acceptance_criteria,
        },
        "run_dir": str(run_dir),
        "worker_branch": branch,
        "worker_commit": worker_commit,
        "commit_summary": commits,
        "changed_files": changed_files,
        "review_packet": packet,
        "reviewer_result": review_payload,
        "project_state_excerpt": state_excerpt,
        "registry_rows_for_task": registry_rows,
    }


def _write_engine_artifacts(run_dir: Path, engine_result: SupervisorEngineResult) -> None:
    payload = asdict(engine_result)
    (run_dir / "parsed_supervisor_decision.json").write_text(json.dumps(payload, indent=2, default=str) + "\n")
    if "raw_model_response" in engine_result.raw:
        (run_dir / "raw_supervisor_response.txt").write_text(str(engine_result.raw["raw_model_response"]) + "\n")
    if engine_result.decision == "remediate" and engine_result.followup_task_prompt:
        (run_dir / "remediation_prompt.md").write_text(engine_result.followup_task_prompt.rstrip() + "\n")


def reviewer_status(review: ReviewResult) -> str:
    if review.reviewer == "noop":
        return "noop"
    if review.reviewer.endswith("unavailable") or "error" in review.raw or "openai_error" in review.raw:
        return "failed"
    if review.decision == "needs_manual_review":
        return "manual_review"
    return "success"


def supervisor_status(engine_result: SupervisorEngineResult | None) -> str:
    if engine_result is None:
        return "noop"
    if engine_result.supervisor == "noop":
        return "noop"
    if engine_result.supervisor.endswith("unavailable") or "error" in engine_result.raw or "openai_error" in engine_result.raw:
        return "failed"
    return "success"


def supervisor_reliance(review_status: str, engine_status: str) -> list[str]:
    relied_on: list[str] = []
    if review_status == "success":
        relied_on.append("successful_reviewer_output")
    elif review_status == "failed":
        relied_on.append("failed_reviewer_fallback")
    elif review_status == "manual_review":
        relied_on.append("reviewer_manual_review")
    elif review_status == "noop":
        relied_on.append("noop_reviewer")
    if engine_status == "success":
        relied_on.append("direct_supervisor_inspection")
    return relied_on


def decision_basis(decision: str, review_status: str, engine_result: SupervisorEngineResult | None = None) -> str:
    parsed_basis = None
    if engine_result and isinstance(engine_result.raw.get("parsed_result"), dict):
        parsed_basis = engine_result.raw["parsed_result"].get("decision_basis")
    if parsed_basis:
        return str(parsed_basis)
    if decision == "accept":
        return "accepted_scientific_objective_met" if review_status == "success" else "accepted_without_successful_review"
    if decision == "blocked":
        return "accepted_as_documented_blocker"
    if decision == "remediate":
        return "remediated_evidence_insufficient"
    return "manual_review_required"


def _commits_between(repo_root: Path, base_sha: str, head_sha: str) -> list[str]:
    if not base_sha or not head_sha or base_sha == head_sha:
        return []
    log = _git(repo_root, ["log", "--oneline", f"{base_sha}..{head_sha}"])
    return [line for line in log.stdout.splitlines() if line.strip()] if log.returncode == 0 else []


def _transaction_from_record(repo_root: Path, record: RunRecord) -> tuple[str | None, list[str], list[str], list[str], bool, str]:
    reviewable, reason = is_reviewable(record)
    commits = _commits_between(repo_root, record.base_sha, record.head_sha or "") if record.head_sha else []
    return (
        record.head_sha if reviewable else record.head_sha,
        commits,
        list(record.changed_files),
        list(record.dirty_worktree_files),
        reviewable,
        reason,
    )


def _write_not_reviewable_decision(
    *,
    repo_root: Path,
    run_dir: Path,
    task: Task,
    branch: str,
    worker_commit: str | None,
    commits: list[str],
    changed_files: list[str],
    dirty_files: list[str],
    push_result: dict[str, Any],
    packet: str,
    record: RunRecord | None,
    reviewable_reason: str,
    project_state: ProjectState | None,
) -> SupervisorDecision:
    submission_package = build_submission_package(
        repo_root=repo_root,
        run_dir=run_dir,
        task=task,
        worker_ref=worker_commit or branch or "HEAD",
        worker_commit=worker_commit,
        changed_files=[],
        project_state=project_state,
        review_packet=packet,
        include_git_blobs=False,
    )
    payload = {
        "task_id": task.id,
        "task_title": task.title,
        "run_dir": str(run_dir),
        "worker_branch": branch,
        "worker_commit": worker_commit,
        "base_sha": record.base_sha if record else None,
        "head_sha": record.head_sha if record else worker_commit,
        "commit_summary": commits,
        "changed_files": changed_files,
        "worker_made_commit": bool(record.worker_made_commit) if record else False,
        "worker_made_no_commit": not bool(record.worker_made_commit) if record else True,
        "dirty_worktree_files": dirty_files,
        "push_result": push_result,
        "submission_package": {
            "directory": str(submission_package.package_dir),
            "markdown": str(submission_package.markdown_path),
            "manifest": str(submission_package.manifest_path),
        },
        "reviewer": None,
        "reviewer_status": "not_run",
        "review_decision": None,
        "review_gate_decision": "needs_manual_review",
        "supervisor_engine": None,
        "supervisor_status": "not_run",
        "supervisor_relied_on": [],
        "supervisor_decision": "needs_manual_review",
        "final_action": "needs_manual_review",
        "decision_basis": f"run_not_reviewable:{reviewable_reason}",
        "accepted": False,
        "next_action": "needs_manual_review",
        "allow_remediation": False,
        "continue_loop": False,
        "generated_at": datetime.now(UTC).isoformat(),
    }
    (run_dir / "review_result.json").write_text(json.dumps({"reviewer": None, "decision": "not_run", "summary": reviewable_reason}, indent=2) + "\n")
    (run_dir / "supervisor_decision.json").write_text(json.dumps(payload, indent=2, default=str) + "\n")
    (run_dir / "final_loop_decision.json").write_text(json.dumps(payload, indent=2, default=str) + "\n")
    if record:
        update_run_record(
            run_dir,
            reviewer_status="not_run",
            supervisor_status="not_run",
            final_action="needs_manual_review",
            completed_at=utc_now(),
        )
    execution = ExecutionResult(
        task=task,
        mode="review-gate-not-reviewable",
        success=False,
        message=packet,
        branch=branch,
        commit=worker_commit,
        artifacts=(str(run_dir / "review_packet.md"), str(submission_package.markdown_path), str(submission_package.manifest_path)),
    )
    return SupervisorDecision(action="needs_manual_review", reason=f"Run is not reviewable: {reviewable_reason}", task=task, execution=execution)


def run_review_gate(
    repo_root: Path,
    runs_dir: Path,
    task: Task,
    reviewer: Reviewer,
    run_dir: Path | None = None,
    dry_run: bool = True,
    push_branch: bool = True,
    decision_engine: DecisionEngine | None = None,
    project_state: ProjectState | None = None,
    allow_remediation: bool = False,
) -> SupervisorDecision:
    run_dir = run_dir or latest_run_dir(runs_dir)
    if run_dir is None:
        return SupervisorDecision(action="blocked", reason="No run directory found for review.", task=task)
    record = load_run_record(run_dir)
    metadata = load_run_json(run_dir, "metadata.json")
    summary = load_run_json(run_dir, "summary.json")
    git_status_text = (run_dir / "git_status.txt").read_text() if (run_dir / "git_status.txt").exists() else ""
    if record:
        branch = record.worker_branch
        base_ref = record.base_sha
        worker_commit, commits, changed_files, dirty_files, transaction_reviewable, reviewable_reason = _transaction_from_record(repo_root, record)
        has_worker_commit = transaction_reviewable
        worker_made_no_commit = not record.worker_made_commit
    else:
        branch = metadata.get("branch") or summary.get("branch") or ""
        base_ref = metadata.get("base_sha") or metadata.get("base_branch") or "HEAD"
        worker_commit, commits, changed_files = detect_worker_commit(repo_root, branch, base_ref=base_ref)
        has_worker_commit = bool(commits)
        dirty_files = dirty_files_from_status(git_status_text)
        worker_made_no_commit = bool(metadata.get("remediation")) and not has_worker_commit
        transaction_reviewable = has_worker_commit and not dirty_files
        reviewable_reason = "reviewable" if transaction_reviewable else ("dirty_worktree_after_executor" if dirty_files else "worker_made_no_commit")
    push_result = (
        push_worker_branch(repo_root, branch, dry_run=dry_run)
        if push_branch and branch and (not record or transaction_reviewable)
        else {"pushed": False, "message": "Worker branch push skipped."}
    )
    packet = build_review_packet(
        task,
        run_dir,
        branch,
        worker_commit,
        commits,
        changed_files,
        push_result,
        base_sha=record.base_sha if record else str(base_ref),
        head_sha=record.head_sha if record else worker_commit,
        run_type=record.run_type if record else ("remediation" if metadata.get("remediation") else "legacy"),
        reviewable=transaction_reviewable,
        reviewable_reason=reviewable_reason,
        dirty_worktree_files=dirty_files,
    )
    (run_dir / "review_packet.md").write_text(packet)
    if not transaction_reviewable:
        return _write_not_reviewable_decision(
            repo_root=repo_root,
            run_dir=run_dir,
            task=task,
            branch=branch,
            worker_commit=worker_commit,
            commits=commits,
            changed_files=changed_files,
            dirty_files=dirty_files,
            push_result=push_result,
            packet=packet,
            record=record,
            reviewable_reason=reviewable_reason,
            project_state=project_state,
        )
    submission_package = build_submission_package(
        repo_root=repo_root,
        run_dir=run_dir,
        task=task,
        worker_ref=(record.head_sha if record and record.head_sha else branch or worker_commit or "HEAD"),
        worker_commit=worker_commit,
        changed_files=changed_files,
        project_state=project_state,
        review_packet=packet,
        include_git_blobs=has_worker_commit,
    )
    submission_text = submission_package.markdown_path.read_text()
    execution = ExecutionResult(
        task=task,
        mode="review-gate",
        success=bool(worker_commit),
        message=f"{packet}\n\n{submission_text}",
        branch=branch,
        commit=worker_commit,
        artifacts=(str(run_dir / "review_packet.md"), str(submission_package.markdown_path), str(submission_package.manifest_path)),
    )
    review = reviewer.review(execution)
    review_payload = asdict(review)
    (run_dir / "review_result.json").write_text(json.dumps(review_payload, indent=2, default=str) + "\n")
    if "raw_model_response" in review.raw:
        (run_dir / "raw_model_response.txt").write_text(str(review.raw["raw_model_response"]) + "\n")
    if "parsed_result" in review.raw:
        (run_dir / "parsed_reviewer_result.json").write_text(json.dumps(review.raw["parsed_result"], indent=2, default=str) + "\n")
    review_decision = classify_decision(review, worker_commit, changed_files)
    engine_result = None
    if decision_engine:
        context = _engine_context(task, run_dir, branch, worker_commit, commits, changed_files, packet, review_payload, project_state)
        engine_result = decision_engine.decide(task, context)
        _write_engine_artifacts(run_dir, engine_result)
        decision = engine_result.decision
    else:
        decision = review_decision
    review_status = reviewer_status(review)
    engine_status = supervisor_status(engine_result)
    relied_on = supervisor_reliance(review_status, engine_status)
    decision_payload = {
        "task_id": task.id,
        "task_title": task.title,
        "run_dir": str(run_dir),
        "worker_branch": branch,
        "worker_commit": worker_commit,
        "base_sha": record.base_sha if record else str(base_ref),
        "head_sha": record.head_sha if record else worker_commit,
        "run_record": record.to_dict() if record else None,
        "base_ref": base_ref,
        "commit_summary": commits,
        "changed_files": changed_files,
        "worker_made_commit": has_worker_commit,
        "worker_made_no_commit": worker_made_no_commit,
        "dirty_worktree_files": dirty_files,
        "push_result": push_result,
        "submission_package": {
            "directory": str(submission_package.package_dir),
            "markdown": str(submission_package.markdown_path),
            "manifest": str(submission_package.manifest_path),
        },
        "reviewer": review.reviewer,
        "reviewer_status": review_status,
        "review_decision": review.decision,
        "review_gate_decision": review_decision,
        "supervisor_engine": engine_result.supervisor if engine_result else None,
        "supervisor_status": engine_status,
        "supervisor_relied_on": relied_on,
        "supervisor_decision": decision,
        "final_action": decision,
        "decision_basis": decision_basis(decision, review_status, engine_result),
        "accepted": decision == "accept",
        "next_action": decision,
        "allow_remediation": allow_remediation,
        "remediation_prompt": str(run_dir / "remediation_prompt.md") if engine_result and engine_result.decision == "remediate" and engine_result.followup_task_prompt else None,
        "continue_loop": bool(engine_result.continue_loop) if engine_result else decision in {"accept", "blocked"},
        "generated_at": datetime.now(UTC).isoformat(),
    }
    if decision == "accept":
        metadata["supervisor_acceptance"] = {
            "accepted": True,
            "decision": decision,
            "generated_at": decision_payload["generated_at"],
            "worker_commit": worker_commit,
        }
        (run_dir / "metadata.json").write_text(json.dumps(metadata, indent=2, default=str) + "\n")
    if decision == "remediate" and engine_result and engine_result.followup_task_prompt and allow_remediation:
        decision_payload["remediation_launch"] = "allowed_pending_local_loop_executor"
    (run_dir / "supervisor_decision.json").write_text(json.dumps(decision_payload, indent=2, default=str) + "\n")
    (run_dir / "final_loop_decision.json").write_text(json.dumps(decision_payload, indent=2, default=str) + "\n")
    if record:
        update_run_record(
            run_dir,
            reviewer_status=review_status,
            supervisor_status=engine_status,
            final_action=decision,
            completed_at=utc_now(),
        )
    reason = engine_result.rationale if engine_result else review.summary
    return SupervisorDecision(action=decision, reason=reason, task=task, execution=execution, review=review, engine_result=engine_result)
