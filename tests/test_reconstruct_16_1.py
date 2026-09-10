import pandas as pd
from scripts.reconstruct_16_1 import RAW, load_data


def test_archived_literacy_and_separate_successor():
    book, current, check = load_data()
    assert book.series.nunique() == 8
    assert book.year.min() == 1475 and book.year.max() == 2010
    assert book.query("series == 'World' and year == 1950").value.item() == 36
    assert book.query("series == 'World' and year == 1980").value.item() == 56
    assert len(check) == 14 and check.difference_pp.abs().max() < 1e-10
    assert current.groupby("series").year.max().to_dict() == {"Chile": 2017, "Italy": 2019, "Mexico": 2024, "World": 2024}
    assert current.query("role == 'post_book_successor'").year.min() > 2010
    revised = pd.read_csv(RAW / "owid_global_2019.csv")
    literacy = "Literate world population (OWID based on OECD & UNESCO (2019))"
    assert revised.loc[revised.Year.eq(1800), literacy].item() < 20
