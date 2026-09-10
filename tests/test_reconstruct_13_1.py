import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures/13-1"


def test_gtd_derived_data_cover_book_and_successor_periods():
    book = pd.read_csv(FIG / "data/clean/figure_13_1_book_period.csv")
    successor = pd.read_csv(FIG / "data/clean/figure_13_1_successor.csv")
    assert book.year.min() == 1970
    assert book.year.max() == 2015
    assert successor.year.min() == 2016
    assert successor.year.max() == 2021
    assert {"United States", "Western Europe", "World"} <= set(book.series)


def test_book_exclusions_are_implemented_in_reproducible_script():
    script = (ROOT / "scripts/reconstruct_13_1.py").read_text()
    assert "Afghanistan" in script
    assert "EXCLUSIONS" in script
    assert "Image.open" not in script


def test_status_and_comparison_artifacts_exist():
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
