from scripts.reconstruct_15_4 import build_data


def test_bjs_reconstruction_has_book_and_successor_periods():
    book, successor = build_data()
    assert set(book.series) == {
        "Rape and sexual assault",
        "Intimate partner violence, female victims",
    }
    assert book.year.min() == 1993
    assert book.year.max() == 2014
    assert successor.year.min() == 2015
    assert successor.year.max() >= 2024


def test_bjs_rates_match_reference_landmarks():
    book, _ = build_data()
    rape_1993 = book.query("series == 'Rape and sexual assault' and year == 1993").rate_per_100000.iloc[0]
    ipv_1994 = book.query("series == 'Intimate partner violence, female victims' and year == 1994").rate_per_100000.iloc[0]
    rape_2005 = book.query("series == 'Rape and sexual assault' and year == 2005").rate_per_100000.iloc[0]
    assert 760 < rape_1993 < 775
    assert 1665 < ipv_1994 < 1685
    assert 145 < rape_2005 < 160
