import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures/11-3"


def test_official_source_files_and_periods_are_present():
    assert (FIG / "data/raw/PITF_GenoPoliticide_2018.xls").stat().st_size > 50_000
    assert (FIG / "data/raw/ucdp_onesided_171.xlsx").stat().st_size > 50_000
    book = pd.read_csv(FIG / "data/clean/figure_11_3_book_period.csv")
    successor = pd.read_csv(FIG / "data/clean/figure_11_3_successor.csv")
    assert book["year"].min() == 1956
    assert book["year"].max() == 2016
    assert len(book) == 61
    assert successor["year"].tolist() == list(range(2017, 2024))


def test_ordinal_decode_is_explicit_and_does_not_digitize_reference():
    script = (ROOT / "scripts/reconstruct_11_3.py").read_text()
    assert "PITF_DEATHMAG_TO_COUNT" in script
    assert "pd.read_excel" in script
    assert "Image.open" not in script


def test_partial_status_and_comparisons_are_recorded():
    record = json.loads((FIG / "figure.json").read_text())
    assert record["scientific_status"] == "partial_match"
    assert record["visual_review"]["status"] == "inspected"
    assert record["artifact_kind"] == "reconstruction"
    for role in [
        "book_period_reconstruction",
        "extended_reconstruction",
        "book_period_comparison",
        "extended_comparison",
        "caption",
        "provenance",
    ]:
        assert (ROOT / record["artifacts"][role]["path"]).exists()
