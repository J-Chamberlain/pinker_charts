import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures/12-6"


def test_structured_nsc_workbook_produces_declared_ranges():
    book = pd.read_csv(FIG / "data/clean/figure_12_6_book_period.csv")
    successor = pd.read_csv(FIG / "data/clean/figure_12_6_successor.csv")
    assert book.year.min() == 1903
    assert book.year.max() == 2014
    assert successor.year.min() == 2015
    assert successor.year.max() == 2024
    assert {"Falls", "Fire", "Drowning", "Poison (solid or liquid)", "Poison (gas or vapor)"} <= set(book.series)
    assert book.loc[(book.series == "Falls"), "year"].max() == 1992


def test_source_pipeline_uses_workbook_not_reference_digitization():
    script = (ROOT / "scripts/reconstruct_12_6.py").read_text()
    assert "read_excel" in script
    assert "Image.open" not in script
    assert "digitiz" in script.lower()  # documentation records the prohibition


def test_status_and_comparison_artifacts_are_present():
    record = json.loads((FIG / "figure.json").read_text())
    assert record["scientific_status"] == "updated_equivalent"
    assert record["visual_review"]["status"] == "inspected"
    for role in [
        "original_reference",
        "book_period_reconstruction",
        "extended_reconstruction",
        "book_period_comparison",
        "extended_comparison",
        "caption",
        "provenance",
        "source_log",
        "anomaly_review",
        "discrepancy_log",
        "review_checklist",
        "lineage",
    ]:
        assert (ROOT / record["artifacts"][role]["path"]).exists()
