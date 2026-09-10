"""Extract the published numerical Table 1, not plotted values, from Prados 2015.

Source: https://www.roiw.org/2015/n2/02%20-%2012104.pdf (printed p230).
The full copyrighted paper is a temporary download; only table data are retained.
"""
import argparse
import hashlib
from pathlib import Path

import pandas as pd
from pypdf import PdfReader

SHA256 = "c0fbef0f85b322eeb1d3ee7a14c0bc39e0b0d9ff9cc12e29a078dd0eb40827a8"
ROOT = Path(__file__).resolve().parents[1]


def extract(path):
    if hashlib.sha256(path.read_bytes()).hexdigest() != SHA256:
        raise ValueError("Unexpected paper version; inspect before extraction")
    text = PdfReader(path).pages[10].extract_text()
    block = text.split("Panel A: Levels", 1)[1].split("Panel B:", 1)[0]
    rows = [line.split() for line in block.splitlines() if line.strip()]
    if len(rows) != 14 or any(len(row) != 4 for row in rows):
        raise ValueError("Unexpected Table 1 layout")
    return pd.DataFrame(rows, columns=["year", "hihd", "hybrid_hdi", "old_hdi"]).astype(
        {"year": int, "hihd": float, "hybrid_hdi": float, "old_hdi": float})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    args = parser.parse_args()
    extract(args.pdf).to_csv(ROOT / "figures/16-6/data/raw/prados_2015_table1.csv", index=False)
