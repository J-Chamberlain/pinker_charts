from __future__ import annotations

import base64
import csv
import json
import mimetypes
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .schemas import ProjectState, Task


TEXT_LIMIT = 12000
SCRIPT_LIMIT = 18000
CSV_PREVIEW_ROWS = 12


@dataclass(frozen=True)
class SubmissionPackage:
    package_dir: Path
    markdown_path: Path
    manifest_path: Path
    manifest: dict[str, Any]


def _git(repo_root: Path, args: list[str]) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(["git", *args], cwd=repo_root, capture_output=True, check=False)


def _git_text(repo_root: Path, ref: str, path: str) -> str | None:
    proc = _git(repo_root, ["show", f"{ref}:{path}"])
    if proc.returncode != 0:
        return None
    return proc.stdout.decode("utf-8", errors="replace")


def _git_bytes(repo_root: Path, ref: str, path: str) -> bytes | None:
    proc = _git(repo_root, ["show", f"{ref}:{path}"])
    if proc.returncode != 0:
        return None
    return proc.stdout


def _truncate(text: str, limit: int = TEXT_LIMIT) -> tuple[str, bool]:
    if len(text) <= limit:
        return text, False
    return text[:limit] + "\n\n[TRUNCATED]\n", True


def _write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, default=str) + "\n")


def _copy_blob(repo_root: Path, ref: str, source_path: str, target_dir: Path) -> dict[str, Any] | None:
    data = _git_bytes(repo_root, ref, source_path)
    if data is None:
        return None
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / Path(source_path).name
    target.write_bytes(data)
    mime_type = mimetypes.guess_type(source_path)[0] or "application/octet-stream"
    return {
        "source_path": source_path,
        "package_path": str(target),
        "bytes": len(data),
        "mime_type": mime_type,
    }


def _text_entry(repo_root: Path, ref: str, source_path: str, package_dir: Path, limit: int = TEXT_LIMIT) -> dict[str, Any]:
    text = _git_text(repo_root, ref, source_path)
    entry: dict[str, Any] = {"source_path": source_path, "found": text is not None}
    if text is None:
        return entry
    truncated, was_truncated = _truncate(text, limit)
    target = package_dir / "files" / source_path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(truncated)
    entry.update({"package_path": str(target), "truncated": was_truncated, "characters": len(text), "content": truncated})
    return entry


def _csv_preview(text: str) -> dict[str, Any]:
    rows = list(csv.reader(text.splitlines()))
    return {"rows": rows[:CSV_PREVIEW_ROWS], "total_rows": len(rows)}


def _registry_row(task: Task, project_state: ProjectState | None) -> dict[str, str] | None:
    if not project_state:
        return None
    for row in project_state.registry_rows:
        if row.get("figure_id") == task.id or row.get("task_id") == task.id or row.get("id") == task.id:
            return row
    return None


def _manifest_entry(task: Task, project_state: ProjectState | None) -> dict[str, Any] | None:
    if not project_state or not project_state.review_manifest:
        return None
    entries = project_state.review_manifest.get("figures") or project_state.review_manifest.get("entries") or project_state.review_manifest.get("items") or project_state.review_manifest
    if isinstance(entries, list):
        for entry in entries:
            if isinstance(entry, dict) and entry.get("figure_id") == task.id:
                return entry
    return None


def _worker_manifest_entry(repo_root: Path, ref: str, task: Task) -> dict[str, Any] | None:
    text = _git_text(repo_root, ref, "output/pdf/recreated_figures_review_scroll.manifest.json")
    if text is None:
        return None
    try:
        manifest = json.loads(text)
    except json.JSONDecodeError:
        return None
    entries = manifest.get("figures") or manifest.get("entries") or manifest.get("items") or manifest if isinstance(manifest, dict) else manifest
    if isinstance(entries, list):
        for entry in entries:
            if isinstance(entry, dict) and entry.get("figure_id") == task.id:
                return entry
    return None


def _image_data_url(path: Path, mime_type: str) -> str:
    return f"data:{mime_type};base64,{base64.b64encode(path.read_bytes()).decode('ascii')}"


def build_submission_package(
    *,
    repo_root: Path,
    run_dir: Path,
    task: Task,
    worker_ref: str,
    worker_commit: str | None,
    changed_files: list[str],
    project_state: ProjectState | None,
    review_packet: str,
    include_git_blobs: bool = True,
) -> SubmissionPackage:
    package_dir = run_dir / "submission_package"
    package_dir.mkdir(parents=True, exist_ok=True)
    figure_dir = f"figures/{task.id}"
    text_paths = [
        f"{figure_dir}/provenance/provenance.md",
        f"{figure_dir}/source_logs/source_log.md",
        f"{figure_dir}/discrepancy_logs/discrepancy_log.md",
        f"{figure_dir}/anomaly_reviews/anomaly_review.md",
        f"{figure_dir}/captions/caption.txt",
        f"{figure_dir}/review_checklist.md",
        f"{figure_dir}/metadata/metadata.json",
        f"scripts/reconstruct_{task.id.replace('-', '_')}.py",
    ]
    image_paths = {
        "original_reference_crop": f"{figure_dir}/plots/comparisons/pdf_reference_figure_{task.id.replace('-', '_')}.png",
        "book_period_comparison": f"{figure_dir}/plots/comparisons/figure_{task.id.replace('-', '_')}_book_period_comparison.png",
        "extended_comparison": f"{figure_dir}/plots/comparisons/figure_{task.id.replace('-', '_')}_extended_comparison.png",
    }
    clean_data_paths = [path for path in changed_files if path.startswith(f"{figure_dir}/data/clean/")]
    text_entries = (
        [_text_entry(repo_root, worker_ref, path, package_dir, SCRIPT_LIMIT if path.endswith(".py") else TEXT_LIMIT) for path in text_paths]
        if include_git_blobs
        else [{"source_path": path, "found": False, "skipped_reason": "worker_made_no_commit"} for path in text_paths]
    )
    clean_data_entries: list[dict[str, Any]] = []
    for path in clean_data_paths:
        text = _git_text(repo_root, worker_ref, path) if include_git_blobs else None
        entry: dict[str, Any] = {"source_path": path, "found": text is not None}
        if text is not None:
            target = package_dir / "files" / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text)
            entry.update({"package_path": str(target), "preview": _csv_preview(text)})
        elif not include_git_blobs:
            entry["skipped_reason"] = "worker_made_no_commit"
        clean_data_entries.append(entry)
    image_entries: list[dict[str, Any]] = []
    for role, path in image_paths.items():
        copied = _copy_blob(repo_root, worker_ref, path, package_dir / "images") if include_git_blobs else None
        if copied:
            copied["role"] = role
            copied["data_url"] = _image_data_url(Path(copied["package_path"]), copied["mime_type"])
            image_entries.append(copied)
        else:
            image_entries.append({"role": role, "source_path": path, "found": False, **({"skipped_reason": "worker_made_no_commit"} if not include_git_blobs else {})})
    state_excerpt = ""
    if project_state:
        state_excerpt, _ = _truncate(project_state.raw_state, 10000)
    manifest = {
        "task": task.__dict__,
        "registry_row": _registry_row(task, project_state),
        "project_state_excerpt": state_excerpt,
        "worker_branch": worker_ref,
        "worker_commit": worker_commit,
        "package_source": "committed_worker_tree" if include_git_blobs else "uncommitted_worktree_not_packaged",
        "package_warning": None if include_git_blobs else "Worker made no commit. File contents and images are intentionally omitted to avoid presenting stale branch evidence.",
        "changed_files": changed_files,
        "text_files": [{k: v for k, v in entry.items() if k != "content"} for entry in text_entries],
        "clean_data": clean_data_entries,
        "images": [{k: v for k, v in entry.items() if k != "data_url"} for entry in image_entries],
        "review_pdf_manifest_entry": _manifest_entry(task, project_state) or _worker_manifest_entry(repo_root, worker_ref, task),
        "review_packet_path": str(run_dir / "review_packet.md"),
    }
    manifest_path = package_dir / "submission_manifest.json"
    _write_json(manifest_path, manifest)
    sections = [
        f"# Submission Package: {task.id} - {task.title}",
        "## Task Metadata",
        "```json\n" + json.dumps(task.__dict__, indent=2, default=str) + "\n```",
        "## Registry Row",
        "```json\n" + json.dumps(manifest["registry_row"], indent=2, default=str) + "\n```",
        "## Worker Run",
        f"- Worker ref: `{worker_ref}`\n- Worker commit: `{worker_commit}`",
        "## Changed Files",
        "\n".join(f"- `{path}`" for path in changed_files) or "- None",
        "## Review Packet",
        review_packet,
    ]
    for entry in text_entries:
        sections.append(f"## File: {entry['source_path']}")
        sections.append(entry.get("content", "[missing]"))
    for entry in clean_data_entries:
        sections.append(f"## Clean Data Preview: {entry['source_path']}")
        sections.append("```json\n" + json.dumps(entry.get("preview"), indent=2, default=str) + "\n```")
    sections.append("## Visual Evidence")
    for entry in image_entries:
        sections.append(f"- {entry['role']}: `{entry['source_path']}` found={entry.get('found', True)} package_path=`{entry.get('package_path', '')}`")
    sections.append("## Review PDF Manifest Entry")
    sections.append("```json\n" + json.dumps(manifest["review_pdf_manifest_entry"], indent=2, default=str) + "\n```")
    markdown_path = package_dir / "submission_package.md"
    markdown_path.write_text("\n\n".join(sections) + "\n")
    return SubmissionPackage(package_dir=package_dir, markdown_path=markdown_path, manifest_path=manifest_path, manifest={**manifest, "image_inputs": image_entries})
