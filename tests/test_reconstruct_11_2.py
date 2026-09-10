import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures/11-2"


def test_cited_source_files_and_book_period_are_present():
    assert (FIG / "data/raw/PRIO_Battle_Deaths_Dataset_31.xls").stat().st_size > 100_000
    assert (FIG / "data/raw/ucdp_brd_conf_50_2016.csv").stat().st_size > 100_000
    book = pd.read_csv(FIG / "data/clean/figure_11_2_book_period.csv")
    assert book["year"].min() == 1946
    assert book["year"].max() == 2015
    assert len(book) == 70
    assert book["rate_per_100k"].notna().all()


def test_successor_series_is_separate_and_refreshable():
    successor = pd.read_csv(FIG / "data/clean/figure_11_2_successor.csv")
    assert successor["year"].min() == 2016
    assert successor["year"].max() == 2023
    assert successor["source_series"].eq(
        "UCDP Battle-Related Deaths Dataset v26.1"
    ).all()


def test_no_plotted_pixel_values_are_used_as_the_source():
    script = (ROOT / "scripts/reconstruct_11_2.py").read_text()
    assert "Image.open" not in script
    assert "PRIO_Battle_Deaths_Dataset_31.xls" in script
    assert "ucdp_brd_conf_50_2016.csv" in script
    assert "pd.read_excel" in script
    assert "pd.read_csv" in script


def test_visual_artifacts_and_partial_status_are_recorded():
    record = json.loads((FIG / "figure.json").read_text())
    assert record["scientific_status"] == "partial_match"
    assert record["visual_review"]["status"] == "inspected"
    for role in [
        "book_period_reconstruction",
        "extended_reconstruction",
        "book_period_comparison",
        "extended_comparison",
    ]:
        assert (ROOT / record["artifacts"][role]["path"]).exists()
