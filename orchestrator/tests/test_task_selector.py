from orchestrator.schemas import Task
from orchestrator.task_selector import select_by_priority, select_first_unprocessed


def test_select_first_unprocessed():
    tasks = [
        Task(id="1", title="Done", status="verified_reproduction"),
        Task(id="2", title="Next", status="not_started"),
    ]
    assert select_first_unprocessed(tasks).id == "2"


def test_select_by_priority_prefers_source_family():
    tasks = [
        Task(id="1", title="A", status="not_started", metadata={"source_type_guess": "media"}),
        Task(id="2", title="B", status="not_started", metadata={"source_type_guess": "economic"}),
    ]
    assert select_by_priority(tasks, {"economic"}).id == "2"
