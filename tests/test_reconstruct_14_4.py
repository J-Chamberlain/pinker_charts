import pytest
from scripts.reconstruct_14_4 import load_data


def test_execution_sources_aggregation_and_complete_year_extension():
    book, successor, diagnostic, records, overlap, population = load_data()
    assert len(records) == 15296
    assert population.query("year==1780").population.item() == 2780369
    assert overlap.difference.eq(0).all()
    assert book.query("year==1780").executions.item() == 285
    assert book.query("year==1780").value.item() == pytest.approx(.849531, abs=.00001)
    assert book.query("year==2016").executions.item() == 20
    assert successor.year.max() == 2025
    assert successor.query("year==2025").executions.item() == 47
    assert successor.query("year==2025").population.item() == 341784857
    assert diagnostic.single_year_rate.ne(diagnostic.value).all()
