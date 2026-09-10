from scripts.reconstruct_14_3 import load_data


def test_dated_chronology_and_institutional_continuation():
    book, successor = load_data()
    assert book.source_revision.eq(734519509).all()
    assert book.value.iloc[-1] == 105
    assert book.loc[book.count_discrepancy.ne(0), "year"].tolist() == [2009, 2012]
    assert book.cumulative_listed.iloc[-1] == 102
    assert successor.year.tolist() == list(range(2016, 2026))
    assert successor.value.iloc[0] == 104
    assert successor.value.iloc[-1] == 113
