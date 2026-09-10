from scripts.reconstruct_17_3 import load_data


def test_appliances_and_definition_break():
    book, anchors, census, candidates = load_data()
    assert book.series.nunique() == 8
    stove = book[book.series.eq("Stove")]
    assert set(stove[stove.year.lt(2000)].definition) == {"electric range only"}
    assert set(stove[stove.year.ge(2000)].definition) == {"Gas or electric stove"}
    assert census.query("series == 'Washing machine' and year == 2005").value.item() == 84.2
    assert anchors.year.tolist() == [1900, 1975]
    assert candidates.query("sex == 'women' and year == 2015").broad_household_weekly.round(2).item() == 15.61
    assert 2020 not in candidates.year.values
    assert candidates.role.str.startswith("diagnostic only").all()
