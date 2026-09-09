"""Recover numeric source tables, not graph coordinates.

Author PDFs: https://www.markaguiar.com/files/leisuretrends.pdf and the 2006
revision linked in source_logs. Retain numeric extracts; full papers stay local.
BLS source URLs are recorded in data/raw/bls_table_urls.json.
"""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import zipfile

import pandas as pd
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "figures/17-6/data/raw"


def paper_rows(path, page, panels, version):
    expected = {"2007 published Table III": "7298e81315cd74c6f9ce642890bf2fede33294b5c980fcbd179efab13057df01",
                "2006 revision Table 3": "144c8dffa73b0908bffe4ae4074144a1018b0797c8c54b90810e330289b0616d"}
    if hashlib.sha256(path.read_bytes()).hexdigest() != expected[version]:
        raise ValueError("Paper version changed; inspect before extracting")
    text = PdfReader(path).pages[page].extract_text()
    rows = []
    for sex, panel in panels.items():
        block = text.split(panel, 1)[1]
        match = re.search(r"Leisure Measure 1\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)", block)
        if not match:
            raise ValueError(f"Missing paper row {panel}")
        values = [float(x) for x in match.groups()]
        if abs(values[4] - values[0] - values[5]) > .011:
            raise ValueError("Published difference does not cross-check")
        for year, value in zip([1965, 1975, 1985, 1993, 2003], values[:5]):
            rows.append({"year": year, "sex": sex, "hours_per_week": value,
                         "version": version, "population": "21-65, nonretired nonstudents, fixed demographics",
                         "measure": "Leisure Measure 1", "pdf_page": page + 1})
    return pd.DataFrame(rows)


def bls_rows(path, year):
    text = subprocess.check_output(["pdftotext", "-layout", str(path), "-"], text=True)
    if not re.search(rf"by sex,\s+{year}\s+annual averages", text):
        raise ValueError(f"Wrong BLS year/table: {path}")
    rows = []
    for category in ["Leisure and sports", "Lawn and garden care", "Volunteering (organizational and civic activities)", "Animals and pets"]:
        matches = [line for line in text.splitlines() if line.strip().startswith(category)]
        if len(matches) != 1:
            raise ValueError(f"Ambiguous BLS category: {category}, {year}")
        numbers = re.findall(r"\b\d+\.\d+\b", matches[0][matches[0].index(category) + len(category):])
        if len(numbers) != 9:
            raise ValueError(f"Suppressed or malformed BLS row: {category}, {year}")
        for sex, value in zip(["total", "men", "women"], numbers[:3]):
            rows.append({"year": year, "sex": sex, "activity": category, "hours_per_day": value,
                         "population": "civilian noninstitutional population 15+", "source_file": path.name})
    return rows


def main():
    archive = ROOT / "tmp/source_cache/aguiar_timeuse_data.zip"
    with zipfile.ZipFile(archive) as bundle:
        names = ["cells.dta", "merged_datasets.zip"]
        entries = []
        for item in bundle.infolist():
            if item.is_dir() or item.filename == "/":
                continue
            data = bundle.read(item.filename)
            entries.append({"name": item.filename, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(),
                            "retained_in_repository": item.filename in names})
            if item.filename in names:
                (RAW / item.filename).write_bytes(data)
    (RAW / "replication_archive_manifest.json").write_text(json.dumps({
        "source_url": "https://www.dropbox.com/scl/fo/g3mi6dmg2ehwljty1l0ld/AG25K690ppAR-qRUCncFdAE?rlkey=v05wqn6v0hd9md0xy3s5n8t9i&dl=1",
        "discovery_url": "https://www.markaguiar.com/",
        "retrieved_date": "2026-09-09", "archive_sha256": hashlib.sha256(archive.read_bytes()).hexdigest(),
        "entries": entries, "note": "Only numeric analysis datasets retained in Git. Full archive remains a local retrieval cache; not required to replot. Author code inspected, not executed or redistributed."}, indent=2) + "\n")
    published = paper_rows(ROOT / "tmp/source_cache/aguiar_hurst_2007.pdf", 8,
                           {"men": "Panel 2: Men", "women": "Panel 3: Women"}, "2007 published Table III")
    earlier = paper_rows(ROOT / "tmp/source_cache/aguiar_hurst_2006_revision.pdf", 37,
                         {"men": "Panel B: Men", "women": "Panel C: Women"}, "2006 revision Table 3")
    if not published[["year", "sex", "hours_per_week"]].equals(earlier[["year", "sex", "hours_per_week"]]):
        raise ValueError("Paper versions disagree")
    published.to_csv(RAW / "aguiar_hurst_2007_table_iii.csv", index=False)
    earlier.to_csv(RAW / "aguiar_hurst_2006_table3.csv", index=False)
    rows = []
    for path in sorted(RAW.glob("bls_a1_*.pdf")):
        rows.extend(bls_rows(path, int(path.stem.rsplit("_", 1)[1])))
    frame = pd.DataFrame(rows)
    if sorted(frame.year.unique()) != [2015, 2016, 2017, 2018, 2019, 2021, 2022, 2023, 2024, 2025]:
        raise ValueError("Missing available annual BLS tables; 2020 intentionally unavailable")
    frame.to_csv(RAW / "bls_activity_tables.csv", index=False)


if __name__ == "__main__":
    main()
