from scripts.reconstruct_15_5 import build_data


def test_legalization_reconstruction_has_book_and_successor_periods():
    book, successor = build_data()
    assert book.year.min() == 1791
    assert book.year.max() == 2016
    assert successor.year.min() == 2017
    assert successor.year.max() >= 2025


def test_known_transition_counts_are_monotonic_and_close_to_reference():
    book, _ = build_data()
    values = book.decriminalized_countries.tolist()
    assert values == sorted(values)
    assert book.query("year == 1791").decriminalized_countries.iloc[0] == 1
    assert 88 <= book.query("year == 2016").decriminalized_countries.iloc[0] <= 94
