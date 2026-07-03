from __future__ import annotations

from .github_client import GitHubClient
from .schemas import IssueDraft, Task


def build_issue_draft(task: Task, labels: tuple[str, ...] = ()) -> IssueDraft:
    body = "\n".join(
        [
            f"## Task",
            f"- Figure/task id: `{task.id}`",
            f"- Title: {task.title}",
            f"- Current status: `{task.status}`",
            f"- Source reference: {task.source_reference or 'See project adapter output.'}",
            "",
            "## Expected Workflow",
            "1. Read PROJECT_STATE.md and the task registry.",
            "2. Inspect the canonical source/reference material.",
            "3. Recover source data or document the blocker.",
            "4. Produce one clean unit of work on a branch.",
            "5. Update metadata, provenance, review notes, registry, and project state.",
            "6. Commit or open a PR.",
            "",
            "## Acceptance Criteria",
            *[f"- {item}" for item in task.acceptance_criteria],
            "",
            "## Files To Update",
            *[f"- `{item}`" for item in task.files_to_update],
            "",
            "## Review Requirements",
            *[f"- {item}" for item in task.review_requirements],
            "",
            "## Next Action",
            task.next_action or "Proceed according to the project workflow.",
        ]
    )
    return IssueDraft(title=f"Reconstruct Figure {task.id} — {task.title}", body=body, labels=labels)


def create_issue(client: GitHubClient, draft: IssueDraft, dry_run: bool = True) -> dict[str, str]:
    if dry_run:
        return {"dry_run": "true", "title": draft.title, "body": draft.body}
    issue = client.create_issue(draft.title, draft.body, draft.labels, draft.assignees)
    return {"dry_run": "false", "url": issue.get("html_url", ""), "number": str(issue.get("number", ""))}
