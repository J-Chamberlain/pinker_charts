from pathlib import Path
import re
import numpy as np
import pytest
from scripts.reconstruct_18_1 import recover, decode_serset
from scripts.reconstruct_18_2 import coefficients
from scripts.reconstruct_18_3 import swiss, us_historical, us_recent

ROOT = Path(__file__).resolve().parents[1]


def test_original_numerical_cache():
    fit, points = recover(ROOT / "figures/18-1/data/raw/original_fig11.gph")
    assert len(points) == 132
    assert len(points.dropna(subset=["gdp", "sat_current_hat"])) == 129
    assert len(points.dropna(subset=["satlow", "ylow", "sathigh", "yhigh"])) == 112
    assert fit.sat_current_fit.max() < 2


def test_cache_rejects_corruption():
    data = (ROOT / "figures/18-1/data/raw/original_fig11.gph").read_bytes()
    section = re.findall(rb"<BeginSerset>\r\n(.*?)<EndSerset>\r\n", data, re.S)[0]
    with pytest.raises(ValueError):
        decode_serset(section.replace(b"sersetreadwrite", b"unknownversion"))
    with pytest.raises(ValueError):
        decode_serset(section.replace(b"\r\n<EndSersetData>", b"extra\r\n<EndSersetData>"))


def test_reported_equation():
    b, c = coefficients("regression equation (B = -0.082, constant = 199.989)")
    assert b * 1978 + c == pytest.approx(37.793)
    assert b * 2009 + c == pytest.approx(35.251)
    with pytest.raises(ValueError):
        coefficients("no coefficients here")


def test_mortality_definitions_and_coverage():
    ch, us = swiss(), us_historical()
    assert len(ch) == 120 and len(us) == 99
    assert np.allclose(ch.rate, ch.deaths / ch.population_thousands * 100)
    assert us.definition.str.startswith("crude").all()
    old = us_recent("cdc_db241_table_2016.pdf", 1999, 2014).set_index("year")
    new = us_recent("cdc_db541_2025.pdf", 2003, 2023).set_index("year")
    assert old.loc[2014, "rate"] == new.loc[2014, "rate"] == 13
    assert new.loc[2014, "deaths"] - old.loc[2014, "deaths"] == 53
