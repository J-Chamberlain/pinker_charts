"""Extract numeric tables, never plotted coordinates, for Figure 17-2.

Costa: https://www.nber.org/system/files/chapters/c6108/c6108.pdf, p29.
BLS: https://www.bls.gov/cps/aa2010/cpsaat3.pdf, page 1, Men 65+.
Full Costa chapter remains in ignored working storage; its hash is verified.
"""
import argparse
import hashlib
import re
import subprocess
from pathlib import Path

import pandas as pd
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "figures/17-2/data/raw"
COSTA_HASH = "64be14ad115220a5f88a4161715878d198edff7dc43ab3622613e666e9d96018"


def extract_costa(path):
    if hashlib.sha256(path.read_bytes()).hexdigest() != COSTA_HASH:
        raise ValueError("Costa PDF version changed; inspect before extraction")
    text = PdfReader(path).pages[24].extract_text()
    table = text.split("Year Gainful Current Gainful Current", 1)[1].split("Sources:", 1)[0]
    rows = []
    for line in table.splitlines():
        tokens = line.split()
        if not tokens:
            continue
        # Printed 1880 is extracted as I880; values are not altered.
        year = int(tokens[0].replace("I", "1"))
        rows.append({"year": year, "gainful_percent": float(tokens[1]),
                     "current_definition_percent": float(tokens[2]) if year >= 1940 else None})
    result = pd.DataFrame(rows)
    if result.year.tolist() != [1850, 1860, *range(1880, 1991, 10)]:
        raise ValueError("Unexpected Costa table coverage")
    return result


def extract_bls_2010():
    text = subprocess.check_output(["pdftotext", "-f", "1", "-l", "1", "-layout",
                                    str(RAW / "bls_2010_table3.pdf"), "-"], text=True)
    men = text.split("Men", 1)[1].split("Women", 1)[0]
    rows = [line for line in men.splitlines() if "65 years and over" in line]
    if len(rows) != 1:
        raise ValueError("Cannot uniquely locate all-races Men 65+ row")
    values = re.findall(r"\d[\d,]*(?:\.\d+)?", rows[0].split("over", 1)[1])
    if len(values) != 8:
        raise ValueError("Unexpected BLS columns")
    return pd.DataFrame([{"year": 2010, "population_thousands": int(values[0].replace(",", "")),
                          "labor_force_thousands": int(values[1].replace(",", "")),
                          "lfpr_percent": float(values[2])}])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--costa-pdf", type=Path, required=True)
    args = parser.parse_args()
    extract_costa(args.costa_pdf).to_csv(RAW / "costa_1998_table_2a1.csv", index=False)
    extract_bls_2010().to_csv(RAW / "bls_2010_men65.csv", index=False)
