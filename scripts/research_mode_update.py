#!/usr/bin/env python3
"""
Research-mode provenance update for figures 10-5 and 10-6.

This layer preserves the reconstruction outputs while adding historical-source
evidence, search metrics, institutional retrieval notes, and a selected-year
UNCTAD Review of Maritime Transport diagnostic candidate.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
from datetime import date
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import requests


ROOT = Path(__file__).resolve().parents[1]
CANDIDATES = ROOT / "data" / "candidates"
CLEAN = ROOT / "data" / "clean"
DIAGNOSTICS = ROOT / "outputs" / "diagnostics"
METRICS = ROOT / "outputs" / "search_metrics"
SOURCE_LOGS = ROOT / "outputs" / "source_logs"
ITERATIONS = ROOT / "outputs" / "search_iterations"
DISCREPANCIES = ROOT / "outputs" / "discrepancy_logs"
PROVENANCE = ROOT / "outputs" / "provenance"
REPORT = ROOT / "outputs" / "report"
FIGURE_METADATA = ROOT / "outputs" / "figure_metadata"
DOCS = ROOT / "docs"
CHECKSUMS = ROOT / "data" / "raw_file_checksums.csv"

RMT_URLS = {
    "rmt2016_en.pdf": "https://unctad.org/system/files/official-document/rmt2016_en.pdf",
    "rmt2019_en.pdf": "https://unctad.org/system/files/official-document/rmt2019_en.pdf",
    "rmt2020_en.pdf": "https://unctad.org/system/files/official-document/rmt2020_en.pdf",
}


def ensure_dirs() -> None:
    for path in [CANDIDATES, CLEAN, DIAGNOSTICS, METRICS, DOCS]:
        path.mkdir(parents=True, exist_ok=True)


def download(url: str, path: Path) -> None:
    if path.exists() and path.stat().st_size > 0:
        return
    response = requests.get(url, timeout=120, headers={"User-Agent": "enlightenment-now-poc/research-mode"})
    response.raise_for_status()
    path.write_bytes(response.content)


def ensure_rmt_texts() -> None:
    for filename, url in RMT_URLS.items():
        pdf = CANDIDATES / filename
        txt = pdf.with_suffix(".txt")
        download(url, pdf)
        if not txt.exists():
            subprocess.run(["pdftotext", "-layout", str(pdf), str(txt)], check=True)


def parse_rmt2020_selected_years() -> pd.DataFrame:
    text = (CANDIDATES / "rmt2020_en.txt").read_text(encoding="utf-8", errors="replace").splitlines()
    rows = []
    for line in text:
        match = re.match(r"\s*((?:19|20)\d{2})\s+", line)
        if not match:
            continue
        year = int(match.group(1))
        if year not in {1970, 1980, 1990, 2000, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019}:
            continue
        tokens = line.split()[1:]
        values = []
        index = 0
        while index < len(tokens) and len(values) < 4:
            token = tokens[index]
            if not token.isdigit():
                break
            if index + 1 < len(tokens) and tokens[index + 1].isdigit() and len(tokens[index + 1]) == 3 and len(token) <= 2:
                values.append(int(token + tokens[index + 1]))
                index += 2
            else:
                values.append(int(token))
                index += 1
        if len(values) != 4:
            continue
        if values[0] == year or values[3] < 2500:
            continue
        rows.append(
            {
                "year": year,
                "tanker_trade_million_tons": values[0],
                "main_bulk_million_tons": values[1],
                "other_dry_cargo_million_tons": values[2],
                "total_all_cargo_million_tons": values[3],
                "source": "UNCTAD Review of Maritime Transport 2020, Table 1.1",
                "note": "Tanker trade includes crude oil, refined petroleum products, gas and chemicals; selected years only.",
            }
        )
    frame = pd.DataFrame(rows).sort_values("year")
    frame.to_csv(CANDIDATES / "unctad_rmt2020_tanker_trade_selected_years.csv", index=False)
    return frame


def plot_rmt_diagnostic(rmt: pd.DataFrame) -> None:
    spills = pd.read_csv(CLEAN / "figure_10_5_oil_spills_clean.csv")
    unctad_live = spills.dropna(subset=["oil_shipped_by_sea_billion_tonnes"])
    plt.style.use("seaborn-v0_8-whitegrid")
    fig, ax = plt.subplots(figsize=(10, 6), dpi=160)
    ax.plot(spills["year"], spills["oil_spills_7_plus_tonnes"], color="#111111", linewidth=2.2, label="Oil spills of at least 7 tonnes")
    ax.set_xlim(1970, 2016)
    ax.set_ylim(0, 125)
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of oil spills")
    ax2 = ax.twinx()
    ax2.plot(
        rmt[rmt["year"].between(1970, 2016)]["year"],
        rmt[rmt["year"].between(1970, 2016)]["tanker_trade_million_tons"] / 1000,
        color="#8a8a8a",
        marker="o",
        linewidth=2.0,
        label="RMT selected-year tanker trade",
    )
    ax2.plot(
        unctad_live["year"],
        unctad_live["oil_shipped_by_sea_billion_tonnes"],
        color="#555555",
        linestyle="--",
        linewidth=1.8,
        label="Live UNCTADStat 2000-2016 candidate",
    )
    ax2.set_ylim(1.3, 3.3)
    ax2.set_ylabel("Billion metric tons")
    handles1, labels1 = ax.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(handles1 + handles2, labels1 + labels2, loc="upper right", frameon=True)
    ax.set_title("Figure 10-5 diagnostic: historical UNCTAD/RMT tanker-trade evidence", fontsize=14)
    ax.annotate(
        "RMT recovers concept back to 1970,\nbut only selected years.",
        xy=(1980, 1.87),
        xycoords=ax2.transData,
        xytext=(1988, 2.35),
        textcoords=ax2.transData,
        arrowprops={"arrowstyle": "->", "color": "#555555"},
        fontsize=9,
    )
    fig.text(
        0.01,
        0.01,
        "Diagnostic only. Source: UNCTAD Review of Maritime Transport 2020 Table 1.1; live UNCTADStat v2231 for 2000-2016.",
        fontsize=8,
        color="#555555",
    )
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    fig.savefig(DIAGNOSTICS / "figure_10_5_rmt_tanker_trade_selected_years_diagnostic.png")
    plt.close(fig)


def write_metrics() -> None:
    rows = [
        {
            "figure_id": "10-5",
            "search_iterations": 18,
            "institutions_searched": "OWID; ITOPF; UNCTAD; Internet Archive; GitHub; Medium; Clarksons via RMT references",
            "institution_count": 7,
            "archive_systems_searched": "Internet Archive CDX; Wayback id snapshots; Git repositories",
            "archive_system_count": 3,
            "repositories_searched": "owid-datasets; owid-grapher-svgs",
            "repository_count": 2,
            "reports_inspected": "ITOPF Oil Spill Statistics 2017; RMT 2016; RMT 2017; RMT 2019; RMT 2020",
            "report_count": 5,
            "datasets_tested": "OWID oil-spills CSV; live UNCTADStat US.SeaborneTrade v2231; RMT 2020 selected-year tanker trade",
            "dataset_test_count": 3,
            "datasets_rejected": "live UNCTADStat as faithful plot input because it is short-period and numerically inconsistent with RMT/book scale; current OWID/OWID repos for missing oil-shipping series",
            "candidate_datasets_remaining": "RMT selected-year tanker trade; possible retired UNCTADStat report 585 export; possible ITOPF/UNCTAD chart source table",
            "current_confidence": 0.74,
            "estimated_completeness": "0.76",
            "search_continues_or_stops": "continues",
        },
        {
            "figure_id": "10-6",
            "search_iterations": 8,
            "institutions_searched": "World Bank; UNEP-WCMC/Protected Planet; WRI; UNSD; Internet Archive",
            "institution_count": 5,
            "archive_systems_searched": "Internet Archive CDX; Wayback archived WDI ZIP",
            "archive_system_count": 2,
            "repositories_searched": "none newly required",
            "repository_count": 0,
            "reports_inspected": "Protected Planet Report 2014",
            "report_count": 1,
            "datasets_tested": "archived WDI 2017 ZIP; current WDI bulk ZIP; current WDI indicator ZIPs; UNSD combined protected areas XLS",
            "dataset_test_count": 4,
            "datasets_rejected": "current WDI for exact reproduction; UNSD combined workbook for this figure",
            "candidate_datasets_remaining": "none needed for reconstruction; bibliography wording still needs confirmation",
            "current_confidence": 0.9,
            "estimated_completeness": "0.82",
            "search_continues_or_stops": "stops for reconstruction; bibliographic cleanup remains",
        },
    ]
    with (METRICS / "search_metrics.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    (METRICS / "search_metrics.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")


def write_checksums() -> None:
    rows = []
    for base in [ROOT / "data" / "raw", CANDIDATES]:
        for path in sorted(base.glob("*")):
            if not path.is_file():
                continue
            digest = hashlib.sha256()
            with path.open("rb") as handle:
                for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                    digest.update(chunk)
            rows.append(
                {
                    "path": str(path.relative_to(ROOT)),
                    "sha256": digest.hexdigest(),
                    "bytes": path.stat().st_size,
                    "modified_date": date.fromtimestamp(path.stat().st_mtime).isoformat(),
                }
            )
    with CHECKSUMS.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["path", "sha256", "bytes", "modified_date"])
        writer.writeheader()
        writer.writerows(rows)
    (ROOT / "data" / "raw_file_checksums.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")


def append_md(path: Path, heading: str, lines: list[str]) -> None:
    current = path.read_text(encoding="utf-8") if path.exists() else ""
    marker = f"\n## {heading}\n"
    if marker in current:
        current = current.split(marker)[0].rstrip() + "\n"
    current += marker + "\n".join(lines).rstrip() + "\n"
    path.write_text(current, encoding="utf-8")


def write_research_notes() -> None:
    today = date.today().isoformat()
    append_md(
        SOURCE_LOGS / "figure_10_5.md",
        "Research Mode Addendum",
        [
            f"- Date accessed: {today}",
            "- New evidence: UNCTAD Review of Maritime Transport 2020 Table 1.1 gives selected-year `Tanker trade` values for 1970, 1980, 1990, 2000, 2005-2019.",
            "- Definition match: RMT footnote defines tanker trade as crude oil, refined petroleum products, gas and chemicals.",
            "- Acceptance: accepted as historical diagnostic support, not faithful reconstruction input, because the original chart appears annual and RMT Table 1.1 is selected-year only.",
            "- Important mismatch: live UNCTADStat v2231 cargo-type sum gives 2000 = 2.984 and 2016 = 4.086 billion tons, while RMT Table 1.1 gives 2000 = 2.163 and 2016 = 3.058 billion tons. The RMT values better match the book/ITOPF axis scale.",
            "- OWID repository search: `owid-datasets` contains ITOPF spill data only; `owid-grapher-svgs` contains modern ITOPF oil-spill grapher artifacts but no recovered oil-shipped-by-sea series.",
            "- GitHub code search API returned 401 without authentication; local clone/file search substituted where possible.",
            "- Legacy UNCTAD route testing: current OData exposes version 2231; version 585 metadata route returns 404; legacy WDS URLs redirect to modern data centre.",
            "- Medium reproduction page clue: public search snippet indicates old export filename `US.SeaborneTrade_585_20231104_101924.csv`, but direct page retrieval was blocked and no archived/downloadable file was recovered.",
        ],
    )
    append_md(
        ITERATIONS / "figure_10_5.md",
        "Research Mode Iterations",
        [
            "| Iteration | Query or URL | Result | Accepted or Rejected | Resolved discrepancy |",
            "| --- | --- | --- | --- | --- |",
            "| 10 | `https://unctad.org/system/files/official-document/rmt2020_en.pdf` | Downloaded and extracted RMT 2020 Table 1.1 selected-year tanker trade, 1970-2019. | Accepted diagnostic | Recovers historical source concept back to 1970, but not annual series. |",
            "| 11 | RMT 2016/2019/2020 PDF text searches | Confirmed table/source wording and footnotes for tanker trade. | Accepted context | Strengthens UNCTAD/Clarksons evidence chain. |",
            "| 12 | RMT-vs-live-UNCTAD numeric comparison | RMT 2000/2016 = 2.163/3.058 billion tons; live UNCTAD cargo sum = 2.984/4.086 billion tons. | Accepted diagnostic | Shows live v2231 is not a faithful substitute for the book line. |",
            "| 13 | OWID `owid-datasets` clone and file search | Found ITOPF oil-spills dataset, no oil-shipping series. | Rejected for missing series | Negative evidence for OWID dataset trail. |",
            "| 14 | OWID `owid-grapher-svgs` clone and file search | Found modern oil-spill grapher artifacts, no matching oil-shipping series. | Rejected for missing series | Negative evidence for public grapher artifact trail. |",
            "| 15 | GitHub code search API | Returned 401 authentication requirement. | Incomplete | Requires authenticated GitHub code search for further automation. |",
            "| 16 | UNCTAD legacy WDS/export endpoint probes | Version 585 not addressable; legacy WDS URLs redirect or 404. | Rejected | Retired export route not recovered. |",
        ],
    )
    append_md(
        DISCREPANCIES / "figure_10_5.md",
        "Research Mode Discrepancy Update",
        [
            "- Improved: historical UNCTAD/RMT selected-year tanker trade evidence now covers the concept back to 1970.",
            "- Improved: RMT selected-year values match the book's right-axis scale better than the live UNCTADStat v2231 cargo-sum candidate.",
            "- Still unresolved: exact annual 1970-2016 oil-shipped-by-sea series behind the original gray line has not been recovered.",
            "- Current best hypothesis: the original gray line used a retired UNCTADStat export/report version or ITOPF/UNCTAD chart data, not a currently public annual API endpoint.",
        ],
    )
    append_md(
        PROVENANCE / "figure_10_5.md",
        "Research Mode Provenance Update",
        [
            "- Added `data/candidates/unctad_rmt2020_tanker_trade_selected_years.csv`.",
            "- Added `outputs/diagnostics/figure_10_5_rmt_tanker_trade_selected_years_diagnostic.png`.",
            "- RMT selected-year values are diagnostic evidence only and are not used in the side-by-side validation plot.",
        ],
    )
    append_md(
        PROVENANCE / "figure_10_6.md",
        "Research Mode Provenance Update",
        [
            "- No regression to reconstruction. Archived WDI 2017 remains the accepted source.",
            "- Current WDI and UNSD candidates remain diagnostic/rejected for exact reproduction.",
        ],
    )


def write_institution_notes() -> None:
    (DOCS / "institution_retrieval_notes.md").write_text(
        """# Institution Retrieval Notes

Generated: {today}

## UNCTAD

- Current data centre reports expose metadata at `https://unctadstat-api.unctad.org/api/reportMetadata/<report>/en`.
- Current OData facts endpoints use `https://unctadstat-api.unctad.org/datamart-api/<report>/<version>/Facts`.
- `US.SeaborneTrade` current version observed: 2231, last updated 2026-03-17, with years 2000-2024.
- Historical clue: a 2023 reproduction snippet names `US.SeaborneTrade_585_20231104_101924.csv`, suggesting retired report/export version 585.
- Current API no longer exposes version 585 metadata; legacy WDS table viewer URLs redirect to the new data centre.
- Review of Maritime Transport PDFs preserve selected-year tanker trade tables and definitions; these are reliable context but not necessarily annual data exports.

## OWID

- Current grapher CSV endpoint works for spill counts: `/grapher/number-oil-spills.csv`.
- Exact 2016 Roser data snapshot was not found via exact Wayback grapher CSV probes.
- `owid-datasets` contains a 2021 ITOPF oil-spills dataset, but no oil-shipped-by-sea series.
- `owid-grapher-svgs` contains modern grapher artifacts for oil-spill charts, but no recovered oil-shipping companion series in the checked file tree.

## ITOPF

- Oil Spill Statistics 2017 contains the chart concept and explicitly labels the gray line as total crude oil, petroleum product and gas loaded, data source UNCTADStat.
- Public PDF provides chart evidence but no machine-readable table for the gray line.

## World Bank

- Current WDI API/ZIP can differ from historical releases.
- For Figure 10-6, archived WDI bulk ZIP from Wayback 2017-10-12 preserves the book-range World values.
- Search archived bulk downloads before accepting current API limitations.
""".format(today=date.today().isoformat()),
        encoding="utf-8",
    )


def update_figure_metadata_json() -> None:
    path = FIGURE_METADATA / "figure_10_5.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload.setdefault("candidate_evidence", [])
    payload["candidate_evidence"].append(
        {
            "path": "data/candidates/unctad_rmt2020_tanker_trade_selected_years.csv",
            "source": "UNCTAD Review of Maritime Transport 2020 Table 1.1",
            "role": "historical selected-year diagnostic support",
            "status": "accepted_diagnostic_only",
            "limitation": "selected years only; not the exact annual 1970-2016 series",
        }
    )
    payload["search_metrics"] = "outputs/search_metrics/search_metrics.csv"
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    path = FIGURE_METADATA / "figure_10_6.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["search_metrics"] = "outputs/search_metrics/search_metrics.csv"
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def update_csv_metadata() -> None:
    path = ROOT / "data" / "figure_metadata.csv"
    rows = list(csv.DictReader(path.open(newline="", encoding="utf-8")))
    for row in rows:
        if row["figure_id"] == "10-5":
            row["confidence_score"] = "0.74"
            row["notes"] = (
                "Best-current reconstruction remains spill-count-only. RMT 2020 selected-year tanker-trade values now support the "
                "historical oil-shipping concept back to 1970, but exact annual 1970-2016 data remains unresolved. Live UNCTADStat "
                "v2231 is diagnostic only and is numerically inconsistent with the RMT/book scale."
            )
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def update_report() -> None:
    path = REPORT / "enlightenment_now_poc_report.md"
    report = path.read_text(encoding="utf-8") if path.exists() else "# Iterative Source Recovery Report\n"
    marker = "\n## Research Mode Historical Recovery Addendum\n"
    if marker in report:
        report = report.split(marker)[0].rstrip() + "\n"
    addendum = f"""
## Research Mode Historical Recovery Addendum

Generated: {date.today().isoformat()}

### New Evidence

- Figure 10-5: UNCTAD Review of Maritime Transport 2020 Table 1.1 was downloaded and parsed. It gives selected-year `Tanker trade` values for 1970, 1980, 1990, 2000, 2005-2019.
- The RMT footnote defines tanker trade as crude oil, refined petroleum products, gas and chemicals, matching the book/ITOPF concept.
- Numeric check: RMT gives 2000 = 2.163 and 2016 = 3.058 billion tons. The live UNCTADStat v2231 cargo-sum candidate gives 2000 = 2.984 and 2016 = 4.086 billion tons, so live v2231 is not a faithful substitute.
- OWID repository checks found ITOPF spill data and modern oil-spill grapher artifacts, but no recovered oil-shipped-by-sea series.

### Did The Figure Improve?

- Figure 10-5: provenance improved materially, but the best-current reconstruction did not change. The RMT evidence is diagnostic selected-year support, not the exact annual series.
- Figure 10-6: no regression. The archived WDI reconstruction remains the accepted verified reproduction.

### Remaining Unresolved

- Figure 10-5 still needs the exact annual historical oil-shipped-by-sea series for approximately 1970-2016.
- Strongest remaining hypothesis: a retired UNCTADStat export/report version, likely related to the observed `US.SeaborneTrade_585_...csv` clue, or an ITOPF/UNCTAD chart source table.

### Search Metrics

- Metrics table: `outputs/search_metrics/search_metrics.csv`
- Metrics JSON: `outputs/search_metrics/search_metrics.json`
- Institution retrieval notes: `docs/institution_retrieval_notes.md`
"""
    path.write_text(report.rstrip() + marker + addendum.split(marker, 1)[1], encoding="utf-8")


def main() -> None:
    ensure_dirs()
    ensure_rmt_texts()
    rmt = parse_rmt2020_selected_years()
    plot_rmt_diagnostic(rmt)
    write_metrics()
    write_research_notes()
    write_institution_notes()
    update_figure_metadata_json()
    update_csv_metadata()
    update_report()
    write_checksums()
    print("Research-mode update complete")
    print(f"RMT selected-year rows: {len(rmt)}")


if __name__ == "__main__":
    main()
