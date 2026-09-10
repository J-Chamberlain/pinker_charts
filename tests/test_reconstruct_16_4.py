import pytest

from scripts.reconstruct_16_4 import load_data


def test_preserve_original_values_and_missing_series():
    book, current, diagnostic, revisions = load_data()
    assert set(book.code) == {"AFG", "PAK"}
    assert len(book) == 12
    assert book[book.code.eq("AFG")].year.tolist() == [1979, 2011]
    assert book[book.code.eq("AFG")].ratio.tolist() == pytest.approx([.24331, .518967])
    assert current[current.code.eq("AFG")].year.max() == 2022
    afghan = revisions[revisions.code.eq("AFG") & revisions.year.eq(2015)].iloc[0]
    assert afghan.difference < -.22
    assert diagnostic["count"].min() == 1
    assert "World" not in set(book.country)
