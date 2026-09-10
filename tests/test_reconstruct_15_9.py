from scripts.reconstruct_15_9 import SERIES, build_data


def test_owid_child_labor_table_has_expected_series_and_period():
    book, successor = build_data()
    assert set(book.series) == set(SERIES)
    assert book.year.min() == 1851
    assert book.year.max() == 2012
    assert successor.empty


def test_known_historical_endpoints():
    book, _ = build_data()
    assert book.query("series == 'England' and year == 1851").percent_children_working.iloc[0] == 28.25
    assert book.query("series == 'World, ILO-IPEC' and year == 2012").percent_children_working.iloc[0] == 10.6
