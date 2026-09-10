from scripts.reconstruct_15_3 import SERIES, build_data


def test_fbi_incident_data_has_expected_periods_and_series():
    book, successor = build_data()
    assert set(book.series) == set(SERIES)
    assert book.year.min() == 1996
    assert book.year.max() == 2015
    assert successor.year.min() == 2016
    assert successor.year.max() == 2017


def test_known_fbi_incident_endpoints():
    book, _ = build_data()
    assert book.query("series == 'Anti-black' and year == 1996").incidents.iloc[0] == 3674
    assert book.query("series == 'Anti-Islamic' and year == 2001").incidents.iloc[0] == 481
    assert book.query("series == 'Anti-black' and year == 2015").incidents.iloc[0] == 1745
