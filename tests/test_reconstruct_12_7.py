import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures/12-7"


def test_book_and_successor_ranges_are_saved():
    book = pd.read_csv(FIG / "data/clean/figure_12_7_book_period.csv")
    successor = pd.read_csv(FIG / "data/clean/figure_12_7_successor.csv")
    assert book.year.min() == 1913
    assert book.year.max() == 2015
    assert successor.year.min() == 2016
    assert "rate_per_100k" in book


def test_source_transcription_is_labeled_and_not_reference_digitization():
    raw = pd.read_csv(FIG / "data/raw/source_transcribed_rates.csv")
    script = (ROOT / "scripts/reconstruct_12_7.py").read_text()
    assert raw.source_url.notna().all()
    assert "Image.open" not in script
    assert "source_transcribed_rates.csv" in script


def test_status_and_comparisons_are_recorded():
    record = json.loads((FIG / "figure.json").read_text())
    assert record["scientific_status"] == "partial_match"
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
