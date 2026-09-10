import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures/12-1"


def test_public_components_and_successor_are_saved():
    assert (FIG / "data/raw/owid_homicide_rates_western_europe.csv").stat().st_size > 10_000
    assert (FIG / "data/raw/owid_homicide_rate_unodc.csv").stat().st_size > 100_000
    book = pd.read_csv(FIG / "data/clean/figure_12_1_book_period.csv")
    successor = pd.read_csv(FIG / "data/clean/figure_12_1_successor.csv")
    assert {"England", "Italy", "Netherlands & Belgium", "Mexico"} <= set(book["series"])
    assert book.year.min() >= 1300
    assert book.year.max() == 2015
    assert successor.year.min() == 2016
    assert successor.year.max() == 2023


def test_missing_components_are_not_digitized():
    script = (ROOT / "scripts/reconstruct_12_1.py").read_text()
    assert "Image.open" not in script
    assert "Roth" in script
    assert "personal-communication" in script


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
        "anomaly_review",
    ]:
        assert (ROOT / record["artifacts"][role]["path"]).exists()
