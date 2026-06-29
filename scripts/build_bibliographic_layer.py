#!/usr/bin/env python3
"""
Build a bibliographic intelligence layer for the current Enlightenment Now POC.

This script does not download datasets. It resolves the citation keys already
encountered in the two proof-of-concept figures and records the remaining
bibliographic gaps explicitly.
"""

from __future__ import annotations

import csv
import json
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BIB = ROOT / "outputs" / "bibliography"
DOCS = ROOT / "docs"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def ensure_dirs() -> None:
    BIB.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)


def build_records() -> dict[str, list[dict[str, Any]]]:
    bibliography = [
        {
            "citation_key": "Roser 2016r",
            "resolution_status": "candidate",
            "authors": "Roser, Max",
            "publication_year": "2016",
            "title": "Oil spills / Global number of oil spills from tankers",
            "journal_or_publisher": "Our World in Data",
            "report_series": "",
            "volume_issue": "",
            "pages": "",
            "doi": "",
            "isbn": "",
            "jstor_id": "",
            "worldcat_record": "",
            "url": "https://ourworldindata.org/grapher/number-oil-spills",
            "publisher_website": "https://ourworldindata.org/",
            "evidence_note": "Book figure source line cites Our World in Data, Roser 2016r, based on ITOPF. Current OWID grapher metadata cites ITOPF but is not proven to be the exact 2016r version.",
        },
        {
            "citation_key": "World Bank 2016h",
            "resolution_status": "candidate",
            "authors": "World Bank",
            "publication_year": "2016",
            "title": "World Development Indicators: protected areas indicators",
            "journal_or_publisher": "World Bank",
            "report_series": "World Development Indicators",
            "volume_issue": "",
            "pages": "",
            "doi": "",
            "isbn": "",
            "jstor_id": "",
            "worldcat_record": "",
            "url": "http://data.worldbank.org/indicator/ER.PTD.TOTL.ZS",
            "publisher_website": "https://data.worldbank.org/",
            "evidence_note": "Book source line cites World Bank 2016h. Current metadata for protected-area WDI indicators points to Protected Planet/UNEP-WCMC. Exact 2016h bibliography entry still needs confirmation from the book bibliography.",
        },
        {
            "citation_key": "World Bank 2017",
            "resolution_status": "candidate",
            "authors": "World Bank",
            "publication_year": "2017",
            "title": "World Development Indicators",
            "journal_or_publisher": "World Bank",
            "report_series": "World Development Indicators",
            "volume_issue": "",
            "pages": "",
            "doi": "",
            "isbn": "",
            "jstor_id": "",
            "worldcat_record": "",
            "url": "https://databank.worldbank.org/source/world-development-indicators",
            "publisher_website": "https://www.worldbank.org/",
            "evidence_note": "Book source line cites World Bank 2016h and 2017. This record represents the 2017 WDI source family; exact bibliography wording remains to be verified.",
        },
    ]

    lookup = [
        {
            "citation_key": row["citation_key"],
            "bibliography_record_id": row["citation_key"].replace(" ", "_"),
            "authors": row["authors"],
            "year": row["publication_year"],
            "title": row["title"],
            "url": row["url"],
            "resolution_status": row["resolution_status"],
        }
        for row in bibliography
    ]

    datasets = [
        {
            "dataset_id": "owid_itopf_oil_spills",
            "citation_key": "Roser 2016r",
            "dataset_name": "Global number of oil spills from tankers",
            "dataset_type": "compiled dataset",
            "owning_institution": "Our World in Data; original data from ITOPF",
            "publication_year": "2016/current continuation",
            "update_frequency": "Annual or irregular; current OWID metadata last updated 2026-05-06",
            "current_availability": "Current OWID grapher CSV available; exact 2016r snapshot not located",
            "likely_successor_dataset": "OWID grapher number-oil-spills; ITOPF Oil tanker spill statistics",
            "persistent_identifiers": "",
            "source_fidelity": "B",
            "fidelity_label": "Exact publication candidate; exact dataset version not confirmed",
            "notes": "Covers spill counts but not the oil-shipped-by-sea line.",
        },
        {
            "dataset_id": "unctad_seaborne_oil_trade",
            "citation_key": "Roser 2016r",
            "dataset_name": "Oil shipped by sea / seaborne trade oil cargo",
            "dataset_type": "institutional statistical database",
            "owning_institution": "UNCTADStat",
            "publication_year": "unknown",
            "update_frequency": "Annual",
            "current_availability": "Public viewer found; exact unauthenticated CSV export not located",
            "likely_successor_dataset": "UNCTADStat seaborne trade data viewer",
            "persistent_identifiers": "",
            "source_fidelity": "C",
            "fidelity_label": "Institutional successor",
            "notes": "Needed for the gray right-axis line in Figure 10-5.",
        },
        {
            "dataset_id": "world_bank_wdi_protected_areas",
            "citation_key": "World Bank 2016h",
            "dataset_name": "World Development Indicators protected-area indicators",
            "dataset_type": "compiled institutional database",
            "owning_institution": "World Bank; underlying source Protected Planet / UNEP-WCMC and IUCN",
            "publication_year": "2016/2017",
            "update_frequency": "Annual or periodic",
            "current_availability": "Current World Bank API available, but World aggregate does not expose full 1990-2014 series",
            "likely_successor_dataset": "World Bank WDI indicators ER.LND.PTLD.ZS, ER.MRN.PTMR.ZS, ER.PTD.TOTL.ZS",
            "persistent_identifiers": "",
            "source_fidelity": "C",
            "fidelity_label": "Institutional successor",
            "notes": "Exact WDI 2016h/2017 bulk release or archive is needed for source fidelity A/B.",
        },
        {
            "dataset_id": "protected_planet_wdpa",
            "citation_key": "World Bank 2016h",
            "dataset_name": "World Database on Protected Areas",
            "dataset_type": "compiled institutional database",
            "owning_institution": "UNEP-WCMC / IUCN Protected Planet",
            "publication_year": "various",
            "update_frequency": "Periodic/monthly in modern service",
            "current_availability": "Current website available; historical 1990-2014 extract not located",
            "likely_successor_dataset": "Protected Planet WDPA / WD-OECM releases",
            "persistent_identifiers": "",
            "source_fidelity": "C",
            "fidelity_label": "Institutional successor",
            "notes": "Named in World Bank indicator metadata as underlying source.",
        },
    ]

    archives = [
        {
            "archive_id": "itopf_20161218",
            "target_url": "http://www.itopf.com/knowledge-resources/data-statistics/statistics/",
            "archive_url": "http://web.archive.org/web/20161218101412/http://www.itopf.com/knowledge-resources/data-statistics/statistics/",
            "timestamp": "2016-12-18",
            "related_citation_key": "Roser 2016r",
            "status": "located",
            "notes": "Internet Archive closest snapshot to 2017-01-01 for ITOPF statistics page.",
        },
        {
            "archive_id": "worldbank_er_ptd_totl_zs_20161006",
            "target_url": "http://data.worldbank.org/indicator/ER.PTD.TOTL.ZS",
            "archive_url": "http://web.archive.org/web/20161006192316/http://data.worldbank.org:80/indicator/ER.PTD.TOTL.ZS",
            "timestamp": "2016-10-06",
            "related_citation_key": "World Bank 2016h",
            "status": "located",
            "notes": "Internet Archive closest snapshot to 2017-01-01 for a combined protected-areas indicator page.",
        },
        {
            "archive_id": "owid_number_oil_spills_20170101",
            "target_url": "https://ourworldindata.org/grapher/number-oil-spills.csv",
            "archive_url": "",
            "timestamp": "2017-01-01 probe",
            "related_citation_key": "Roser 2016r",
            "status": "not_located",
            "notes": "Wayback availability probe returned no closest snapshot for this exact CSV URL.",
        },
    ]

    figure_mapping = [
        {
            "figure_id": "10-5",
            "figure_title": "Oil spills, 1970-2016",
            "bibliography_keys": "Roser 2016r",
            "bibliography_entries": "Roser, Max. Oil spills / Global number of oil spills from tankers. Our World in Data, 2016.",
            "datasets": "owid_itopf_oil_spills; unctad_seaborne_oil_trade",
            "source_fidelity": "B/C",
            "initial_estimate": "Exact OWID publication candidate for spill counts; institutional successor only for UNCTAD oil-shipped series.",
            "mapping_status": "partial",
        },
        {
            "figure_id": "10-6",
            "figure_title": "Protected areas, 1990-2014",
            "bibliography_keys": "World Bank 2016h; World Bank 2017",
            "bibliography_entries": "World Bank. World Development Indicators protected-area indicators, 2016/2017.",
            "datasets": "world_bank_wdi_protected_areas; protected_planet_wdpa",
            "source_fidelity": "C",
            "initial_estimate": "Institutional successor identified; exact historical WDI release not yet located.",
            "mapping_status": "partial",
        },
    ]

    coverage_manifest = [
        {
            "scope": "complete_book_bibliography",
            "status": "not_extracted",
            "reason": "No complete machine-readable bibliography source was available in the workspace, and Kindle keystroke automation was blocked by macOS accessibility permissions during this run.",
            "next_step": "Use Kindle/Computer Use OCR on the Bibliography section or locate an authorized bibliography export, then append all records to bibliography_database.csv/json.",
        },
        {
            "scope": "current_poc_figure_citations",
            "status": "partial_resolved",
            "reason": "The current two figures cite Roser 2016r, World Bank 2016h, and World Bank 2017. Candidate bibliographic records and dataset references were created for those keys.",
            "next_step": "Verify exact bibliography wording against the book bibliography before marking any record resolved.",
        },
    ]

    return {
        "bibliography": bibliography,
        "lookup": lookup,
        "datasets": datasets,
        "archives": archives,
        "figure_mapping": figure_mapping,
        "coverage_manifest": coverage_manifest,
    }


def write_docs(records: dict[str, list[dict[str, Any]]]) -> None:
    md = f"""# Bibliographic Intelligence Layer

Generated: {date.today().isoformat()}

## Purpose

This layer separates bibliographic provenance from plotting and dataset recovery.
Future source discovery should start from citation keys and full references, not
from ad hoc keyword searches.

## Current Coverage

- Complete book bibliography: **not yet extracted**.
- Current POC figure citation keys: **partially resolved**.
- Figures covered: `10-5`, `10-6`.

## Fidelity Scores

- `A`: Exact source, exact publication and exact dataset version used by the book.
- `B`: Exact publication located, but only newer dataset version available.
- `C`: Institutional successor with methodological continuity.
- `D`: Closely related dataset with methodological differences.
- `E`: Conceptual proxy only.

## Important Limitation

This pass did not complete the requested full bibliography extraction. It created
the database schema and populated the records required by the current POC figures.
The complete bibliography should be added before chapter-scale processing.

## Files

- `outputs/bibliography/bibliography_database.csv`
- `outputs/bibliography/bibliography_database.json`
- `outputs/bibliography/citation_key_lookup.csv`
- `outputs/bibliography/citation_key_lookup.json`
- `outputs/bibliography/dataset_reference_catalog.csv`
- `outputs/bibliography/dataset_reference_catalog.json`
- `outputs/bibliography/archive_index.csv`
- `outputs/bibliography/archive_index.json`
- `outputs/bibliography/figure_bibliography_mapping.csv`
- `outputs/bibliography/figure_bibliography_mapping.json`
- `outputs/bibliography/bibliography_coverage_manifest.csv`
- `outputs/bibliography/bibliography_coverage_manifest.json`
"""
    (DOCS / "bibliographic_intelligence_layer.md").write_text(md, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    records = build_records()
    outputs = {
        "bibliography_database": records["bibliography"],
        "citation_key_lookup": records["lookup"],
        "dataset_reference_catalog": records["datasets"],
        "archive_index": records["archives"],
        "figure_bibliography_mapping": records["figure_mapping"],
        "bibliography_coverage_manifest": records["coverage_manifest"],
    }
    for name, rows in outputs.items():
        write_csv(BIB / f"{name}.csv", rows)
        write_json(BIB / f"{name}.json", rows)
    write_docs(records)
    print(f"Wrote bibliographic layer to {BIB}")


if __name__ == "__main__":
    main()
