from scripts.reconstruct_15_1 import SERIES, YEARS, build_data


def test_public_table_reconstruction_has_three_series_and_expected_years():
    book, successor = build_data()
    assert len(book) == 42
    assert set(book.series) == set(SERIES)
    assert sorted(book.year.unique()) == YEARS
    assert successor.empty


def test_source_questions_are_preserved_for_auditing():
    book, _ = build_data()
    assert book.source_question.notna().all()
    assert book.source_type.eq("official Pew topline table transcription").all()


def test_known_public_topline_endpoints():
    book, _ = build_data()
    women_visual = book[book.series.str.startswith("Agree: Women")]
    school_visual = book[book.series.str.startswith("Agree: School")]
    interracial = book[book.series.str.startswith("Disagree:")]
    assert women_visual.query("year == 1987").percentage.iloc[0] == 51
    assert women_visual.query("year == 2012").percentage.iloc[0] == 21
    assert school_visual.query("year == 1987").percentage.iloc[0] == 30
    assert interracial.query("year == 2012").percentage.iloc[0] == 10
