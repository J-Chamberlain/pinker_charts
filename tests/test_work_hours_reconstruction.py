import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("work_hours", ROOT / "scripts/reconstruct_17_1.py")
work_hours = importlib.util.module_from_spec(spec)
spec.loader.exec_module(work_hours)


def test_table_values_and_sex_average_not_adjusted_to_book():
    book, diagnostic = work_hours.load_data()
    assert len(book) == 26
    assert len(diagnostic) == 39
    us = book[book.entity.eq("United States")].set_index("year")
    assert us.loc[1870, "weekly_hours"] == 62
    assert us.loc[1938, "weekly_hours"] == 37.3
    assert us.loc[2000, "weekly_hours"] == 40.25
    eu = book[book.entity.eq("Western Europe")].set_index("year")
    assert eu.loc[1870, "weekly_hours"] == 65.9
    assert eu.loc[2000, "weekly_hours"] == (39.2 + 36.1) / 2
    assert not book[["entity", "year"]].duplicated().any()
