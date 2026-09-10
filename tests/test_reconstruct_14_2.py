import pytest

from scripts.reconstruct_14_2 import load_data


def test_human_rights_uses_archived_world_not_naive_average():
    book, successor, diagnostic = load_data()
    assert len(book) == 330
    assert book.groupby("series").year.nunique().eq(66).all()
    assert book.query("series == 'World' and year == 2014").value.item() == pytest.approx(.8440988933)
    assert diagnostic.query("year == 2014").difference.item() > .5
    assert successor.year.max() == 2021
    assert "World" not in successor.series.unique()
    assert successor.lower_95.le(successor.value).all()
    assert successor.upper_95.ge(successor.value).all()
