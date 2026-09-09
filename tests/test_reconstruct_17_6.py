import pytest

from scripts.reconstruct_17_6 import load_data
from scripts.recover_17_6_tables import bls_rows, RAW


def test_original_tables_and_explicit_population_break():
    old, book, current, activities = load_data()
    assert len(old) == 10 and len(book) == 12 and len(current) == 20
    assert len(activities) == 120
    assert 2020 not in current.year.values
    assert book.loc[book.year.eq(2015) & book.sex.eq("men"), "hours_per_week"].item() == pytest.approx(41.93)
    assert book.loc[book.year.eq(2015) & book.sex.eq("women"), "hours_per_week"].item() == pytest.approx(35.98)
    assert old.population.str.contains("21-65").all()
    assert current.population.str.contains("15+").all()
    assert current.with_pet_care_hours_per_week.gt(current.hours_per_week).all()


def test_bls_original_pdf_extraction():
    rows = bls_rows(RAW / "bls_a1_2025.pdf", 2025)
    assert len(rows) == 12
    assert next(r for r in rows if r["activity"] == "Leisure and sports" and r["sex"] == "women")["hours_per_day"] == "4.76"
    with pytest.raises(ValueError, match="Wrong BLS year"):
        bls_rows(RAW / "bls_a1_2025.pdf", 2024)
