import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures/11-1"


def test_archived_source_and_clean_points_are_present():
    raw = FIG / "data/raw/humanprogress_20201024.csv"
    clean = pd.read_csv(FIG / "data/clean/figure_11_1_book_period.csv")
    assert raw.stat().st_size > 1000
    assert clean["period_midpoint"].tolist()[:2] == [1513, 1538]
    assert clean["period_midpoint"].tolist()[-2:] == [1988, 2008]
    assert clean.loc[clean["period_midpoint"].eq(1988), "percentage_years_at_war"].iat[0] == 0


def test_no_plotted_pixel_values_are_used_as_the_source():
    script = (ROOT / "scripts/reconstruct_11_1.py").read_text()
    assert "Image.open" not in script
    assert "pd.read_csv(RAW" not in script
    assert "humanprogress_20201024.csv" in script


def test_visual_artifacts_and_status_are_recorded():
    record = json.loads((FIG / "figure.json").read_text())
    assert record["scientific_status"] == "partial_match"
    assert record["visual_review"]["status"] == "inspected"
    assert "book_period_comparison" in record["artifacts"]
    assert "extended_comparison" in record["artifacts"]
    for role in ["book_period_reconstruction", "extended_reconstruction", "book_period_comparison", "extended_comparison"]:
        assert (ROOT / record["artifacts"][role]["path"]).exists()
