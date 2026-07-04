from orchestrator.schemas import IssueDraft, Task, TaskStatus
from orchestrator.task_selector import is_unprocessed, status_class
from orchestrator.executors.codex_cli_executor import CodexCLIExecutor
from orchestrator.models.noop_reviewer import NoopReviewer
from orchestrator.schemas import ExecutionResult


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


def test_codex_executor_dry_run_command_has_exec_and_branch():
    task = Task(id="10-2", title="Sustainability", status="not_started")
    executor = CodexCLIExecutor(command="codex", dry_run=True)
    result = executor.execute(task)
    assert result.success
    assert "codex exec" in result.message
    assert result.branch == "codex/10-2-sustainability"


def test_noop_reviewer_requires_manual_review():
    task = Task(id="10-2", title="Sustainability", status="not_started")
    result = NoopReviewer().review(ExecutionResult(task=task, mode="test", success=True, message="packet"))
    assert result.decision == "needs_manual_review"
