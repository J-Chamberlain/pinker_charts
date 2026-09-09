"""Numerical checks use retained source tables, never pixels from a chart."""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("lighting", ROOT / "scripts/reconstruct_17_4.py")
lighting = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lighting)


def test_original_values_and_coverage_preserved():
    book, extended, diagnostic = lighting.load_data()
    assert len(book) == 706
    assert book.year.min() == 1301
    assert book.loc[book.year.eq(2006), "value"].item() == 2.89
    assert book.loc[book.year.eq(1800), "value"].item() == 9539.93
    assert len(diagnostic) == 706
    assert set(book.unit) == {lighting.UNIT}


def test_extension_preserves_vintage_overlap_without_rebasing():
    book, extended, _ = lighting.load_data()
    current = extended[extended.role.eq("successor")]
    assert current.year.tolist() == list(range(1995, 2024))
    assert len(extended) == 735
    assert current.loc[current.year.eq(2006), "value"].item() == 2.1665275
    assert current.loc[current.year.eq(2023), "value"].item() == 2.148248
    assert not extended[["source_version", "year"]].duplicated().any()
