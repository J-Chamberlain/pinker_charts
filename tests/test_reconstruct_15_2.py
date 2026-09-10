from scripts.reconstruct_15_2 import TERMS, build_data


def test_google_trends_reconstruction_has_book_and_successor_periods():
    book, successor = build_data()
    assert set(book.series) == set(TERMS)
    assert book.year.min() == 2004
    assert book.year.max() == 2017
    assert successor.year.min() == 2018
    assert successor.year.max() >= 2026


def test_annual_smoothing_is_numeric_and_bounded():
    book, successor = build_data()
    values = book.percentage_of_peak.tolist() + successor.percentage_of_peak.tolist()
    assert all(0 <= value <= 100 for value in values)
