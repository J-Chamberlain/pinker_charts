from scripts.reconstruct_17_2 import load_data
from scripts.recover_17_2_tables import extract_bls_2010


def test_retirement_original_tables_and_no_definition_substitution():
    book, extended, diagnostic = load_data()
    assert book.year.tolist() == list(range(1880, 2011, 10))
    values = book.set_index("year").lfpr_percent
    assert values[1880] == 78.0
    assert values[1960] == 40.8
    assert values[2000] == 17.5
    assert values[2010] == 22.1
    assert len(extended) == 29  # explicit shared 2010 anchor, not a new observation
    assert extended.iloc[-1].year == 2024
    assert extended.iloc[-1].lfpr_percent == 23.4
    assert diagnostic.set_index("year").loc[1960, "lfpr_percent_cps_2025"] == 33.1


def test_retirement_original_bls_sex_and_column_selection():
    row = extract_bls_2010().iloc[0]
    assert row.population_thousands == 16769
    assert row.labor_force_thousands == 3701
    assert row.lfpr_percent == 22.1
