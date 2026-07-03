from pathlib import Path

from orchestrator.adapters.pinker_charts import PinkerChartsAdapter
from orchestrator.issue_queue import build_issue_draft
from orchestrator.supervisor import run_once
from orchestrator.config import load_config


ROOT = Path(__file__).resolve().parents[2]


def test_pinker_adapter_reads_registry():
    adapter = PinkerChartsAdapter(ROOT)
    state = adapter.read_state()
    assert len(state.registry_rows) >= 70
    task = adapter.select_next_task(state)
    assert task is not None
    assert task.status == "not_started"


def test_issue_body_generation_for_pinker_task():
    adapter = PinkerChartsAdapter(ROOT)
    task = adapter.select_next_task()
    draft = build_issue_draft(task)
    assert task.id in draft.title
    assert "Acceptance Criteria" in draft.body
    assert "PROJECT_STATE.md" in draft.body


def test_supervisor_plan_only_dry_run():
    config = load_config(ROOT / "orchestrator/examples/pinker_charts.config.example.yaml")
    decision = run_once(config, "plan-only")
    assert decision.action == "plan"
    assert decision.task is not None
    assert "Acceptance Criteria" in decision.reason
