import numpy as np

from scripts.reconstruct_17_5 import load_data


def test_archived_basket_crosscheck_and_version_separation():
    old, current, diagnostic, long = load_data()
    assert old.year.tolist() == list(range(1929, 2016))
    assert current.year.tolist() == list(range(1929, 2026))
    assert old.loc[old.excluded_from_book, "year"].tolist() == list(range(1941, 1947))
    assert np.allclose(old.basics_percent, old.humanprogress_basics_percent, atol=5e-9, rtol=0)
    assert len(long) == 8 * (87 + 97)
    assert not long.duplicated(["component", "year", "vintage"]).any()
    assert diagnostic.revised_minus_original_pp.abs().max() > .5
    assert old.necessities_percent.iloc[0] > old.narrow_fuel_percent.iloc[0]
    assert current.necessities_percent.iloc[-1] > 30
