import pytest

from scripts.reconstruct_14_1 import load_data


def test_original_provider_values_and_generated_flags_retained():
    old, _, _ = load_data()
    assert len(old) == 216
    assert old.provider_generated.sum() == 132
    assert old.score.iloc[0] == pytest.approx(-6.944444444444445)
    assert old.score.iloc[-1] == pytest.approx(4.233128834355829)


def test_isolated_us_update_is_not_a_world_extension():
    _, current, diagnostic = load_data()
    assert current.year.max() == 2018
    assert current[current.year.ge(2015)].n_polity2.min() >= 150
    assert diagnostic.polity2_minus_hp.abs().max() > 1
    assert not current.duplicated(["release", "year"]).any()
