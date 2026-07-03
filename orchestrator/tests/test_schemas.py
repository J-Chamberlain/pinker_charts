from orchestrator.schemas import IssueDraft, Task, TaskStatus
from orchestrator.task_selector import is_unprocessed, status_class


def test_task_status_values():
    assert TaskStatus.NOT_STARTED.value == "not_started"
    assert status_class("verified_reproduction") == "terminal_or_documented"
    assert status_class("not_started") == "unprocessed"


def test_task_and_issue_draft_dataclasses():
    task = Task(id="10-2", title="Sustainability", status="not_started")
    draft = IssueDraft(title="Example", body="Body")
    assert task.id == "10-2"
    assert draft.title == "Example"
    assert is_unprocessed(task.status)
