import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures/12-2"


def test_book_and_successor_data_cover_declared_ranges():
    book = pd.read_csv(FIG / "data/clean/figure_12_2_book_period.csv")
    successor = pd.read_csv(FIG / "data/clean/figure_12_2_successor.csv")
    assert book.year.min() == 1967
    assert book.year.max() == 2015
    assert {"United States", "England", "World"} <= set(book.series)
    assert successor.year.min() == 2016
    assert successor.year.max() == 2023


def test_public_source_pipeline_does_not_digitize_reference_image():
    script = (ROOT / "scripts/reconstruct_12_2.py").read_text()
    assert "Image.open" not in script
    assert "cv2" not in script.lower()
    assert "pdftotext" in script
    assert "ourworldindata.org/grapher/homicide-rate-unodc.csv" in script


def test_partial_status_and_review_artifacts_exist():
    record = json.loads((FIG / "figure.json").read_text())
    assert record["scientific_status"] == "partial_match"
    assert record["visual_review"]["status"] == "inspected"
    for role in [
        "book_period_reconstruction",
        "extended_reconstruction",
        "book_period_comparison",
        "extended_comparison",
        "caption",
        "provenance",
        "source_log",
        "anomaly_review",
        "discrepancy_log",
        "lineage",
    ]:
        assert (ROOT / record["artifacts"][role]["path"]).exists()
