from pathlib import Path

import pandas as pd
import pytest

from scripts.reconstruct_18_4 import summarize, plot, report_tables


def test_summarize_excludes_missing_values():
    source = pd.DataFrame(
        {
            "year": [2016, 2016, 2016, 2016],
            "happy": [1.0, 2.0, None, 1.0],
            "life": [1.0, 2.0, None, 3.0],
        }
    )
    result = summarize(source).iloc[0]
    assert result["very_happy_pct"] == pytest.approx(66.66666666666667)
    assert result["exciting_pct"] == pytest.approx(33.33333333333333)
    assert result["very_happy_pct_n"] == 3
    assert result["exciting_pct_n"] == 3


def test_norc_raw_release_is_documented():
    script = Path("scripts/reconstruct_18_4.py").read_text()
    assert "gss.norc.org" in script


def test_weighted_denominator_excludes_invalid_answers_and_weights():
    data = pd.DataFrame({"year": [2024]*5, "happy": [1, 2, 9, 1, 1],
                         "life": [1, 3, 9, 1, 1], "w": [1, 3, 100, None, -1]})
    result = summarize(data, "w").iloc[0]
    assert result.very_happy_pct == 25
    assert result.exciting_pct == 25
    assert result.very_happy_pct_n == 2


def test_extension_visible_and_not_bridged_across_mode_change(tmp_path, monkeypatch):
    import matplotlib.pyplot as plt
    data = pd.DataFrame({"year": [2014, 2016, 2018, 2021, 2024],
                         "very_happy_pct": [31, 28, 30, 19, 21],
                         "exciting_pct": [50, 50, 49, 36, 38]})
    monkeypatch.setattr(plt, "close", lambda *args: None)
    plot(data, tmp_path / "extension.png", "", True, data)
    ax = plt.gcf().axes[0]
    assert ax.get_xlim()[1] > 2024
    assert all(not (2018 in line.get_xdata() and 2021 in line.get_xdata()) for line in ax.lines)
    assert any(2024 in line.get_xdata() for line in ax.lines)


def test_original_report_table_extraction():
    data = report_tables(Path("figures/18-4/data/raw/GSS_PsyWellBeing15_final_formatted.pdf"))
    assert len(data) == 55
    row = data[(data.year == 2014) & (data.variable == "very_happy_pct")].iloc[0]
    assert row.report_pct == 32.5
