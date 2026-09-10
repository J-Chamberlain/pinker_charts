from pathlib import Path

import pandas as pd
import pytest

from scripts.reconstruct_18_4 import summarize


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
