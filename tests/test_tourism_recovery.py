import sys
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from recover_17_8_tables import extract_barometer
from reconstruct_17_8 import load_data


def test_table_parser_rejects_wrong_units_and_header():
    text = "International Tourist Arrivals by (Sub)region\n(millions)\n2019 2020*\nWorld 1,469 409 100 20\n"
    assert extract_barometer(text, [2019, 2020])[1]["arrivals_millions"] == 409
    with pytest.raises(ValueError):
        extract_barometer(text.replace("(millions)", "(percent)"), [2019, 2020])
    with pytest.raises(ValueError):
        extract_barometer(text, [2020, 2021])
    with pytest.raises(ValueError):
        extract_barometer(text + "World 2 3\n", [2019, 2020])


def test_retained_source_to_clean_lineage():
    book, extended, diagnostic = load_data()
    assert book.year.tolist() == list(range(1995, 2016))
    assert len(book[book.role.eq("revised_endpoint")]) == 1
    assert len(extended) == 32  # 21 book, 4 regional overlap/extension, 7 recent.
    assert extended[extended.source_version.eq("UN Tourism January 2026")].year.max() == 2025
    assert diagnostic.current_to_2016_ratio.min() > 1.5
    assert (book.arrivals_billions * 1e9 - book.arrivals).abs().max() < 1e-6
    old = pd.read_csv(ROOT / "figures/17-8/data/raw/wdi_2016_world_row.csv")
    jan = pd.read_csv(ROOT / "figures/17-8/data/raw/wdi_2017_january_world_row.csv")
    assert old.iloc[0]["1995"] == jan.iloc[0]["1995"]
    assert pd.isna(old.iloc[0]["2015"]) and pd.isna(jan.iloc[0]["2015"])
