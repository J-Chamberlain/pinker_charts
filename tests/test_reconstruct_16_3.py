from scripts.reconstruct_16_3 import load_data


def test_schooling_author_archive_and_successor():
    book, successor, check, overlap = load_data()
    assert len(book) == 203 and len(check) == 203
    assert book.groupby('series').year.nunique().eq(29).all()
    assert check.difference.abs().max() == 0
    assert overlap.difference.abs().max() < .005001
    assert successor.query('year == 2015').shape[0] == 7
    assert successor.query("series == 'United States' and year == 2015").value.item() == 13.275
    assert successor.query("series == 'Cambodia' and year == 2015").value.item() == 4.873
