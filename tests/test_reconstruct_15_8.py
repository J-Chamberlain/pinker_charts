from scripts.reconstruct_15_8 import build_data


def test_school_subset_has_book_and_successor_periods():
    book, successor = build_data()
    assert book.year.min() == 1993
    assert book.year.max() == 2012
    assert successor.year.min() == 2013
    assert successor.year.max() == 2015
    assert book.rate_per_100000.iloc[0] == 1210

