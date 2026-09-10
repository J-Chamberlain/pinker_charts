import pytest

from scripts.reconstruct_16_5 import load_data


def test_regional_not_country_values_or_levels():
    book, segments = load_data()
    assert len(book) == 36 and len(segments) == 30
    assert book[book.series.eq("World")].iloc[-1].gain_iq_points == pytest.approx(29.49)
    assert book[book.series.eq("Asia")].year.min() == 1951
    assert book[book.series.eq("Africa")].year.min() == 1963
    assert book[book.series.eq("Australia & NZ")].year.max() == 1995
    assert "United States" not in set(book.series)
