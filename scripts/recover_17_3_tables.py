"""Extract source numbers, never graph coordinates, for Figure 17-3.

Original author workbook: https://hdl.handle.net/1802/206
Census: https://www2.census.gov/library/publications/2013/demo/p70-136.pdf
BLS A-1 PDFs already retained by Figure 17-6 (see its URL manifest).
"""
from pathlib import Path
import hashlib
import re
import subprocess

import pandas as pd
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "figures/17-3/data/raw"


def main():
    paper = ROOT / "tmp/source_cache/greenwood_engines.pdf"
    if hashlib.sha256(paper.read_bytes()).hexdigest() != "b02f5f322c17bb949377c0ab07921d7c317f9dd9c6f310e41bd7ac365d32611e":
        raise ValueError("Original paper changed")
    text = PdfReader(paper).pages[4].extract_text()
    match = re.search(r"In (\d{4}) the average household spent (\d+) h a week.*?just (\d+) in (\d{4})", text, re.S)
    if not match:
        raise ValueError("Published numeric housework anchors absent")
    y1, v1, v2, y2 = map(int, match.groups())
    pd.DataFrame([{"year": y1, "value": v1}, {"year": y2, "value": v2}]).assign(
        series="Housework", unit="hours per week per household", source="Greenwood et al. 2005 p113, prose; Lebergott 1993 Table 8.1",
        extraction="numeric statements, not graph digitization").to_csv(RAW / "housework_published_anchors.csv", index=False)
    text = subprocess.check_output(["pdftotext", "-f", "10", "-l", "10", "-layout", str(RAW / "census_p70_136.pdf"), "-"], text=True)
    rows = []
    for category in ["Washing machine", "Dishwasher", "Refrigerator", "Gas or electric stove", "Microwave"]:
        line, = [s for s in text.splitlines() if s.strip().startswith(category)]
        values = re.findall(r"\b\d+\.\d+\b", line[len(category):])
        if len(values) != 12:
            raise ValueError(f"Unexpected Census table row {category}")
        for i, year in enumerate([1992, 1998, 2003, 2005, 2010, 2011]):
            rows.append({"series": category, "year": year, "value": values[2*i], "margin_of_error": values[2*i+1],
                         "unit": "percent of households", "source": "Siebens 2013, Table 3, p10"})
    pd.DataFrame(rows).to_csv(RAW / "census_2013_table3.csv", index=False)
    rows = []
    for path in sorted((ROOT / "figures/17-6/data/raw").glob("bls_a1_*.pdf")):
        year = int(path.stem.rsplit("_", 1)[1])
        text = subprocess.check_output(["pdftotext", "-layout", str(path), "-"], text=True)
        if not re.search(rf"by sex,\s+{year}\s+annual averages", text):
            raise ValueError("BLS year mismatch")
        for category in ["Household activities", "Housework", "Food preparation and cleanup"]:
            line, = [s for s in text.splitlines() if s.strip().startswith(category)]
            values = re.findall(r"\b\d+\.\d+\b", line[line.index(category)+len(category):])
            if len(values) != 9:
                raise ValueError("BLS suppressed/malformed row")
            for sex, value in zip(["total", "men", "women"], values[:3]):
                rows.append({"year": year, "sex": sex, "activity": category, "hours_per_day": value,
                             "source_path": path.relative_to(ROOT).as_posix(), "population": "civilian noninstitutional population 15+"})
    pd.DataFrame(rows).to_csv(RAW / "bls_housework_candidates.csv", index=False)


if __name__ == "__main__":
    main()
