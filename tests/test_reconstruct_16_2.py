from scripts.reconstruct_16_2 import load_data


def test_education_archive_and_oecd_year_error():
    book, check, current = load_data()
    assert len(book) == 134 and book.series.nunique() == 9
    assert book.query("year == 1820").method.item() == "OECD regression-based backcast"
    assert len(check) == 133 and check.difference_pp.abs().max() < 1e-10
    assert set(check.query("year == 2000").source_year) == {2010}
    assert set(check.query("year == 2010").source_year) == {2000}
    assert book.query("series == 'Eastern Europe'").year.max() == 1990
    assert current.query("role == 'projection_not_observed_extension'").year.min() == 2015
    assert book.query("series == 'World' and year == 2010").value.item() == 81.5
