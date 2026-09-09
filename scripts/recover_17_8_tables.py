"""Extract source TABLE cells, never plotted coordinates, for Figure 17-8.

WDI archive: https://web.archive.org/web/20161119172134id_/http://databank.worldbank.org/data/download/WDI_csv.zip
UN Tourism: source URL in source_logs/downloads.json, January 2026, page 6.
Full UN reports remain local because their terms disallow public redistribution.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import zipfile
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures/17-8"


def extract_wdi(path: Path) -> tuple[dict, dict]:
    with zipfile.ZipFile(path) as archive:
        member = next(n for n in archive.namelist() if n.lower().replace("_", "") == "wdidata.csv")
        with archive.open(member) as handle:
            prefix = handle.read(3)
            handle.seek(0)
            encoding = "utf-8-sig" if prefix == b"\xef\xbb\xbf" else "cp1252"
            reader = csv.DictReader(io.TextIOWrapper(handle, encoding=encoding))
            rows = [r for r in reader if r["Country Code"] == "WLD" and r["Indicator Code"] == "ST.INT.ARVL"]
        if len(rows) != 1:
            raise ValueError("Expected exactly one WLD/ST.INT.ARVL row")
        series_member = next(n for n in archive.namelist() if n.lower().replace("_", "") == "wdiseries.csv")
        content = archive.read(series_member)
        try:
            text = content.decode("utf-8-sig")
        except UnicodeDecodeError:
            text = content.decode("cp1252")
        metadata = [r for r in csv.DictReader(io.StringIO(text)) if "ST.INT.ARVL" in r.values()]
    return rows[0], {"archive_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                     "member": member, "selection": "Country Code=WLD; Indicator Code=ST.INT.ARVL",
                     "series_metadata": metadata, "extraction": "CSV parser; original cell strings preserved"}


def extract_barometer(text: str, years: list[int]) -> list[dict]:
    if "International Tourist Arrivals by (Sub)region" not in text or "(millions)" not in text:
        raise ValueError("Unexpected source table or units")
    if not re.search(r"\s+".join(str(y) + r"\*?" for y in years), text):
        raise ValueError("Unexpected year header")
    matches = re.findall(r"^World\s+(.+)$", text, flags=re.MULTILINE)
    if len(matches) != 1:
        raise ValueError("Expected exactly one World table row")
    tokens = matches[0].split()[:len(years)]
    if len(tokens) != len(years) or any(not re.fullmatch(r"[\d,]+", t) for t in tokens):
        raise ValueError("Missing or nonnumeric World observations")
    return [{"year": year, "arrivals_millions": int(t.replace(",", "")),
             "provisional": year == years[-1]} for year, t in zip(years, tokens)]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--barometer-pdf", type=Path, default=ROOT / "tmp/source_cache/un_tourism_barometer_2026_01.pdf")
    args = parser.parse_args()
    sources = {
        "wdi_2016_world_row": FIG / "data/raw/WDI_csv_20161119172134.zip",
        "wdi_2017_january_world_row": FIG / "data/raw/WDI_csv_20170119005005.zip",
        "wdi_2017_october_world_row": ROOT / "figures/10-6/data/raw/wayback_WDI_csv_20171012170642.zip",
        "wdi_2017_may_world_row": ROOT / "tmp/source_cache/WDI_csv_20170508232524.zip",
    }
    for name, path in sources.items():
        row, evidence = extract_wdi(path)
        output = FIG / f"data/raw/{name}.csv"
        with output.open("w", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(row), lineterminator="\n")
            writer.writeheader()
            writer.writerow(row)
        evidence["archive_path_at_extraction"] = str(path.relative_to(ROOT))
        (FIG / f"data/raw/{name}.metadata.json").write_text(json.dumps(evidence, indent=2) + "\n")
    path = args.barometer_pdf
    text = PdfReader(path).pages[5].extract_text()
    rows = extract_barometer(text, list(range(2019, 2026)))
    output = FIG / "data/raw/un_tourism_2026_01_world_table.csv"
    with output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    evidence = {"source_pdf_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "pdf_page": 6, "table": "International Tourist Arrivals by (Sub)region", "row": "World",
                "release": "January 2026", "units": "millions of arrivals", "years": list(range(2019, 2026)),
                "extraction": "pypdf text table cells; not chart digitization; rendered page visually checked",
                "source_url": "https://pre-webunwto.s3.eu-west-1.amazonaws.com/s3fs-public/2026-01/World_Tourism%20Barometer_Jan26_excerpt_v2.pdf?VersionId=u75u9KWPa6Dzc2CUHld7AvQ49FYrDTQC",
                "rights": "Full PDF retained in ignored local cache only; source permits attributed quotations. Seven numeric observations redistributed, not the report."}
    (FIG / "data/raw/un_tourism_2026_01_world_table.metadata.json").write_text(json.dumps(evidence, indent=2) + "\n")


if __name__ == "__main__":
    main()
