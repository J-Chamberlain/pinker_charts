from __future__ import annotations

from pathlib import Path

from .base import ProjectAdapter
from ..schemas import ProjectState, Task
from ..state_reader import read_project_state
from ..task_selector import select_first_unprocessed


class PinkerChartsAdapter(ProjectAdapter):
    """Project adapter for the Pinker Charts repository."""

    completion_files = (
        "metadata/metadata.json",
        "provenance/provenance.md",
        "source_logs/source_log.md",
        "anomaly_reviews/anomaly_review.md",
        "captions/caption.txt",
        "review_checklist.md",
    )

    def __init__(self, root: Path) -> None:
        self.root = root
        self.state_file = root / "PROJECT_STATE.md"
        self.registry_file = root / "data/figure_registry.csv"
        self.review_manifest = root / "output/pdf/recreated_figures_review_scroll.manifest.json"

    def read_state(self) -> ProjectState:
        return read_project_state(self.state_file, self.registry_file, self.review_manifest)

    def tasks(self, state: ProjectState | None = None) -> list[Task]:
        state = state or self.read_state()
        tasks: list[Task] = []
        for row in state.registry_rows:
            figure_id = row.get("figure_id", "")
            title = row.get("title", "")
            chapter = row.get("chapter", "")
            files = tuple(f"figures/{figure_id}/{suffix}" for suffix in self.completion_files)
            files += (
                "data/figure_registry.csv",
                "data/figure_registry.json",
                "data/metadata/figure_metadata.csv",
                "PROJECT_STATE.md",
                "output/pdf/recreated_figures_review_scroll.pdf",
                "output/pdf/recreated_figures_review_scroll.manifest.json",
            )
            tasks.append(
                Task(
                    id=figure_id,
                    title=title,
                    status=row.get("current_status", ""),
                    lifecycle_stage=row.get("lifecycle_stage", ""),
                    priority=row.get("priority", ""),
                    source_reference="Supplemental Graphics PDF unless PROJECT_STATE specifies otherwise.",
                    next_action=row.get("next_action", ""),
                    files_to_update=files,
                    acceptance_criteria=(
                        "Do not digitize Pinker's plotted values as source data.",
                        "Use the Supplemental Graphics PDF as the primary visual/source reference.",
                        "Recover original data first; document blockers honestly.",
                        "Generate book-period and extended comparisons where applicable.",
                        "Update registry, metadata, PROJECT_STATE, provenance, captions, anomaly review, checksums, and review PDF.",
                    ),
                    review_requirements=(
                        "Review data fidelity.",
                        "Review visual fidelity against the PDF reference.",
                        "Review extension clarity.",
                        "Review status calibration.",
                        "Apply the Editorial Review Gate.",
                    ),
                    metadata=row,
                )
            )
        return tasks

    def select_next_task(self, state: ProjectState | None = None) -> Task | None:
        return select_first_unprocessed(self.tasks(state))
