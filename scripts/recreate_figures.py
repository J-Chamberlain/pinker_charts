#!/usr/bin/env python3
"""
Hardened provenance pipeline for Enlightenment Now figures 10-5 and 10-6.

The pipeline is intentionally conservative: missing legacy datasets are recorded
as evidence-chain gaps, not runtime failures.
"""

from __future__ import annotations

import csv
import io
import json
import math
import shutil
import zipfile
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import quote_plus
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import pandas as pd
import requests
from PIL import Image, ImageChops, ImageDraw, ImageOps


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
CLEAN = ROOT / "data" / "clean"
PLOTS = ROOT / "outputs" / "plots"
REPORT = ROOT / "outputs" / "report"
SOURCE_LOGS = ROOT / "outputs" / "source_logs"
LINEAGE = ROOT / "outputs" / "lineage"
VALIDATION = ROOT / "outputs" / "validation"
ORIGINALS = ROOT / "outputs" / "original_reference"
METADATA = ROOT / "data" / "figure_metadata.csv"
KINDLE_TMP = ROOT.parent / "tmp_kindle_figures"

OWID_OIL_CSV = "https://ourworldindata.org/grapher/number-oil-spills.csv"
OWID_OIL_META = "https://ourworldindata.org/grapher/number-oil-spills.metadata.json"
OWID_OIL_PAGE = "https://ourworldindata.org/grapher/number-oil-spills"
OWID_GITHUB = "https://github.com/owid/owid-grapher-svgs"
ITOPF_STATS_PAGE = "https://www.itopf.org/knowledge-resources/data-statistics/oil-tanker-spill-statistics-2025/"
ITOPF_PDF = "https://www.itopf.org/fileadmin/uploads/itopf/data/Stats/Oil_Spill_Stats_brochure_2025_lo.pdf"
UNCTAD_VIEWER = "https://unctadstat.unctad.org/datacentre/dataviewer/us.seabornetrade"
UNCTAD_FACTS_ATTEMPT = "https://unctadstat-api.unctad.org/datamart-api/US.SeaborneTrade/cur/Facts?culture=en"
WB_API = "https://api.worldbank.org/v2/country/WLD/indicator/{indicator}?format=json&per_page=20000"
WB_BULK = "https://databank.worldbank.org/source/world-development-indicators"
WB_LAND = "ER.LND.PTLD.ZS"
WB_MARINE = "ER.MRN.PTMR.ZS"
PROTECTED_PLANET = "https://www.protectedplanet.net/en"
GITHUB_SEARCH_API = "https://api.github.com/search/repositories?q={query}&per_page=5"
GITHUB_CODE_SEARCH_API = "https://api.github.com/search/code?q={query}&per_page=5"
INTERNET_ARCHIVE_CDX = (
    "https://web.archive.org/cdx?url={url}&output=json&fl=timestamp,original,statuscode,"
    "mimetype,digest&filter=statuscode:200&collapse=digest&limit=10"
)
WORLDBANK_INDICATOR_CSV = "https://api.worldbank.org/v2/en/indicator/{indicator}?downloadformat=csv"
WORLDBANK_SOURCE_BULK = "https://api.worldbank.org/v2/en/source/2?downloadformat=csv"
WORLDBANK_ARCHIVES_PAGE = "https://datacatalog.worldbank.org/search/dataset/0037712/World-Development-Indicators"

VALID_STATUSES = {
    "verified_reproduction",
    "updated_equivalent",
    "partial_match",
    "source_unavailable",
    "manual_review_needed",
}


@dataclass(frozen=True)
class FigureConfig:
    figure_id: str
    chapter: str
    title: str
    book_page: str
    claim_summary: str
    book_citation: str
    book_reference_image: Path
    book_crop_box: tuple[int, int, int, int]
    plot_file: str
    clean_file: str
    reproduction_status: str
    confidence_score: float
    visual_validation: str
    visual_reasoning: str
    notes: str
    search_queries: list[str]
    investigated_sources: list[dict[str, str]]
    lineage: list[dict[str, str]]


FIGURES: dict[str, FigureConfig] = {
    "10-5": FigureConfig(
        figure_id="10-5",
        chapter="Chapter 10: The Environment",
        title="Oil spills, 1970-2016",
        book_page="Page 131 of 556; 20%",
        claim_summary="Annual tanker oil spills declined sharply while oil shipped by sea increased.",
        book_citation=(
            "Source: Our World in Data, Roser 2016r, based on data (updated) "
            "from the International Tanker Owners Pollution Federation."
        ),
        book_reference_image=KINDLE_TMP / "fig_4_1_landing2.png",
        book_crop_box=(1300, 285, 2095, 875),
        plot_file="outputs/plots/figure_10_5_oil_spills.png",
        clean_file="data/clean/figure_10_5_oil_spills_clean.csv",
        reproduction_status="partial_match",
        confidence_score=0.58,
        visual_validation="acceptable",
        visual_reasoning=(
            "The recreated spill-count line follows the Kindle figure's main downward trend, "
            "but the gray oil-shipped-by-sea line is missing."
        ),
        notes=(
            "Spill-count data is available from current OWID/ITOPF sources. "
            "The historical UNCTAD oil-shipped-by-sea series remains unresolved."
        ),
        search_queries=[
            "Our World in Data oil spills Roser 2016r International Tanker Owners Pollution Federation oil shipped by sea data",
            "Our World in Data oil spills from tankers csv oil shipped by sea csv",
            "site:ourworldindata.org/grapher oil shipped by sea billion metric tons grapher",
            "\"Oil shipped by sea\" \"Our World in Data\" grapher",
            "\"Oil shipped by sea\" \"billion metric tons\" data",
            "Internet Archive Our World in Data number-oil-spills csv Roser 2016",
            "github ourworldindata grapher number-oil-spills csv historical commit",
            "UNCTAD seaborne trade oil loaded total crude petroleum gas 1970 2016 csv",
            "UNCTADstat API seaborne trade US.SeaborneTrade CSV download",
        ],
        investigated_sources=[
            {
                "source": "Kindle figure caption/source line",
                "url": "local Kindle app",
                "decision": "accepted",
                "reason": "Confirmed figure title and visible source line during prior Computer Use pass.",
            },
            {
                "source": "Our World in Data grapher: number-oil-spills",
                "url": OWID_OIL_CSV,
                "decision": "accepted_partial",
                "reason": "Provides annual medium and large tanker oil-spill counts; current metadata cites ITOPF.",
            },
            {
                "source": "OWID grapher metadata",
                "url": OWID_OIL_META,
                "decision": "accepted_context",
                "reason": "Documents current variable definitions and source citation; not the exact Roser 2016r archive.",
            },
            {
                "source": "ITOPF oil tanker spill statistics",
                "url": ITOPF_STATS_PAGE,
                "decision": "accepted_context",
                "reason": "Institutional source behind the spill counts; current public page/PDF is a modern release.",
            },
            {
                "source": "UNCTADStat seaborne trade data viewer",
                "url": UNCTAD_VIEWER,
                "decision": "rejected_for_now",
                "reason": "Current viewer is public, but the exact oil-shipped-by-sea export route was not located.",
            },
            {
                "source": "UNCTADStat unauthenticated Facts endpoint",
                "url": UNCTAD_FACTS_ATTEMPT,
                "decision": "rejected",
                "reason": "Probe returned HTTP 400 without the report parameters/authentication needed for a CSV download.",
            },
            {
                "source": "GitHub/OWID historical mirrors",
                "url": OWID_GITHUB,
                "decision": "manual_review_needed",
                "reason": "Likely useful for historical commits, but no exact Roser 2016r data snapshot was integrated in this pass.",
            },
            {
                "source": "Internet Archive",
                "url": "https://web.archive.org/",
                "decision": "manual_review_needed",
                "reason": "Should be checked for archived OWID grapher CSV/UNCTAD tables before claiming exact reproduction.",
            },
        ],
        lineage=[
            {"stage": "Book Figure", "value": "Figure 10-5: Oil spills, 1970-2016", "status": "confirmed"},
            {"stage": "Book Citation", "value": "OWID/Roser 2016r based on ITOPF", "status": "confirmed"},
            {"stage": "Original Paper", "value": "Not cited as a paper in Kindle source line", "status": "not_applicable"},
            {"stage": "Original Dataset", "value": "Roser 2016r OWID figure data plus ITOPF/UNCTAD inputs", "status": "not_located"},
            {"stage": "Modern Dataset", "value": OWID_OIL_CSV, "status": "located_partial"},
            {"stage": "Downloaded File", "value": "data/raw/owid_number_oil_spills.csv", "status": "downloaded"},
            {"stage": "Transformation Script", "value": "scripts/recreate_figures.py", "status": "implemented"},
            {"stage": "Generated Plot", "value": "outputs/plots/figure_10_5_oil_spills.png", "status": "generated"},
        ],
    ),
    "10-6": FigureConfig(
        figure_id="10-6",
        chapter="Chapter 10: The Environment",
        title="Protected areas, 1990-2014",
        book_page="Page 133 of 556; 21%",
        claim_summary="Terrestrial and marine protected areas increased from 1990 to 2014.",
        book_citation=(
            "Source: World Bank 2016h and 2017, based on data from the United "
            "Nations Environment Programme and the World Conservation Monitoring Centre."
        ),
        book_reference_image=KINDLE_TMP / "fig_10_6_page_forward.png",
        book_crop_box=(465, 360, 1260, 965),
        plot_file="outputs/plots/figure_10_6_protected_areas.png",
        clean_file="data/clean/figure_10_6_protected_areas_clean.csv",
        reproduction_status="partial_match",
        confidence_score=0.42,
        visual_validation="poor",
        visual_reasoning=(
            "The variables are plausible, but the current World Bank API only returns "
            "2013-2014 observations inside the 1990-2014 book window."
        ),
        notes=(
            "Modern WDI endpoints locate the right concepts but not the full historical World aggregate used in the book."
        ),
        search_queries=[
            "World Bank 2016h 2017 protected areas United Nations Environment Programme World Conservation Monitoring Centre data",
            "\"Protected areas, 1990-2014\" \"World Bank\" \"World Resources Institute\"",
            "\"Terrestrial protected areas\" \"1990\" \"2014\" \"World\" \"World Bank\"",
            "\"Marine protected areas\" \"1990\" \"2014\" \"World\" \"World Bank\"",
            "World Bank bulk download WDI protected areas 1990 2014 ER.LND.PTLD.ZS ER.MRN.PTMR.ZS",
            "Protected Planet WDPA historical terrestrial marine protected areas 1990 2014 csv",
            "World Resources Institute protected areas 1990 2014 data",
            "Internet Archive World Bank WDI protected areas ER.MRN.PTMR.ZS 2016",
        ],
        investigated_sources=[
            {
                "source": "Kindle figure caption/source line",
                "url": "local Kindle app",
                "decision": "accepted",
                "reason": "Confirmed figure title and visible source line during prior Computer Use pass.",
            },
            {
                "source": "World Bank API: terrestrial protected areas",
                "url": WB_API.format(indicator=WB_LAND),
                "decision": "accepted_partial",
                "reason": "Right WDI concept, but World aggregate is populated only for 2013 onward in current API.",
            },
            {
                "source": "World Bank API: marine protected areas",
                "url": WB_API.format(indicator=WB_MARINE),
                "decision": "accepted_partial",
                "reason": "Right WDI concept, but World aggregate is populated only for 2013 onward in current API.",
            },
            {
                "source": "World Bank DataBank bulk WDI",
                "url": WB_BULK,
                "decision": "manual_review_needed",
                "reason": "Likely path to historical WDI releases, but exact 2016h/2017 archived files were not integrated.",
            },
            {
                "source": "World Bank indicator CSV ZIP downloads",
                "url": f"{WORLDBANK_INDICATOR_CSV.format(indicator=WB_LAND)} and {WORLDBANK_INDICATOR_CSV.format(indicator=WB_MARINE)}",
                "decision": "accepted_partial",
                "reason": "Downloadable ZIPs provide reproducible raw CSV files, but World rows still only cover 2013 onward.",
            },
            {
                "source": "Protected Planet / UNEP-WCMC",
                "url": PROTECTED_PLANET,
                "decision": "manual_review_needed",
                "reason": "Original institutional source named by WDI metadata; historical snapshots may require archive/API follow-up.",
            },
            {
                "source": "World Resources Institute",
                "url": "https://www.wri.org/",
                "decision": "manual_review_needed",
                "reason": "Book caption says compiled by WRI; no exact compilation file was located in this pass.",
            },
            {
                "source": "Internet Archive",
                "url": "https://web.archive.org/",
                "decision": "manual_review_needed",
                "reason": "Needed for archived WDI/Protected Planet releases before exact reproduction can be claimed.",
            },
        ],
        lineage=[
            {"stage": "Book Figure", "value": "Figure 10-6: Protected areas, 1990-2014", "status": "confirmed"},
            {"stage": "Book Citation", "value": "World Bank 2016h/2017 based on UNEP-WCMC; compiled by WRI", "status": "confirmed"},
            {"stage": "Original Paper", "value": "Not cited as a paper in Kindle source line", "status": "not_applicable"},
            {"stage": "Original Dataset", "value": "World Bank 2016h/2017 historical WDI release", "status": "not_located"},
            {"stage": "Modern Dataset", "value": f"{WORLDBANK_INDICATOR_CSV.format(indicator=WB_LAND)}; {WORLDBANK_INDICATOR_CSV.format(indicator=WB_MARINE)}", "status": "located_partial"},
            {"stage": "Downloaded File", "value": "data/raw/world_bank_terrestrial_protected_areas_csv.zip; data/raw/world_bank_marine_protected_areas_csv.zip; JSON API evidence files also saved", "status": "downloaded_partial"},
            {"stage": "Transformation Script", "value": "scripts/recreate_figures.py", "status": "implemented"},
            {"stage": "Generated Plot", "value": "outputs/plots/figure_10_6_protected_areas.png", "status": "generated"},
        ],
    ),
}


def ensure_dirs() -> None:
    for path in [RAW, CLEAN, PLOTS, REPORT, SOURCE_LOGS, LINEAGE, VALIDATION, ORIGINALS]:
        path.mkdir(parents=True, exist_ok=True)


def request_get(url: str, timeout: Any = 45) -> requests.Response:
    return requests.get(url, timeout=timeout, headers={"User-Agent": "enlightenment-now-poc/0.2"})


def download_text(url: str, path: Path) -> str:
    response = request_get(url)
    response.raise_for_status()
    path.write_text(response.text, encoding="utf-8")
    return response.text


def download_binary(url: str, path: Path) -> bytes:
    response = request_get(url)
    response.raise_for_status()
    path.write_bytes(response.content)
    return response.content


def safe_probe(url: str, timeout: Any = (2, 3)) -> dict[str, Any]:
    try:
        response = requests.get(
            url,
            timeout=timeout,
            headers={"User-Agent": "enlightenment-now-poc/0.2"},
            stream=True,
        )
        try:
            return {
                "url": url,
                "status_code": response.status_code,
                "content_type": response.headers.get("content-type", ""),
                "content_length": response.headers.get("content-length", ""),
                "final_url": response.url,
            }
        finally:
            response.close()
    except Exception as exc:
        return {"url": url, "error": repr(exc)}


def archive_cdx_probe(url: str) -> dict[str, Any]:
    api_url = INTERNET_ARCHIVE_CDX.format(url=quote_plus(url))
    try:
        response = request_get(api_url, timeout=(2, 3))
        result = {
            "url": api_url,
            "status_code": response.status_code,
            "content_type": response.headers.get("content-type", ""),
            "final_url": response.url,
            "adapter": "internet_archive_cdx",
            "target_url": url,
        }
        if response.status_code == 200:
            payload = response.json()
            headers = payload[0] if payload else []
            rows = payload[1:] if len(payload) > 1 else []
            result["capture_count_returned"] = len(rows)
            result["captures"] = [dict(zip(headers, row)) for row in rows[:5]]
        return result
    except Exception as exc:
        return {"url": api_url, "adapter": "internet_archive_cdx", "target_url": url, "error": repr(exc)}


def github_repo_search(query: str) -> dict[str, Any]:
    api_url = GITHUB_SEARCH_API.format(query=quote_plus(query))
    result = safe_probe(api_url)
    result["adapter"] = "github_repository_search"
    result["query"] = query
    if result.get("status_code") == 200:
        try:
            payload = request_get(api_url, timeout=(2, 4)).json()
            result["total_count"] = payload.get("total_count")
            result["items"] = [
                {
                    "full_name": item.get("full_name"),
                    "html_url": item.get("html_url"),
                    "description": item.get("description"),
                }
                for item in payload.get("items", [])[:5]
            ]
        except Exception as exc:
            result["parse_error"] = repr(exc)
    return result


def github_code_search(query: str) -> dict[str, Any]:
    return {
        "adapter": "github_code_search",
        "query": query,
        "status": "skipped",
        "reason": "Skipped in default pipeline because GitHub code search is often auth-gated and slow; run manually during deep discovery.",
    }


def run_parallel(fn, items: list[str], max_workers: int = 6) -> list[Any]:
    if not items:
        return []
    workers = min(max_workers, len(items))
    with ThreadPoolExecutor(max_workers=workers) as executor:
        return list(executor.map(fn, items))


def build_discovery_bundle(figure_id: str) -> dict[str, Any]:
    if figure_id == "10-5":
        archive_targets = [OWID_OIL_CSV, OWID_OIL_META, OWID_OIL_PAGE, UNCTAD_VIEWER, ITOPF_STATS_PAGE, ITOPF_PDF]
        github_queries = [
            "number-oil-spills ourworldindata",
            "Roser 2016r oil spills",
            "oil shipped by sea UNCTAD",
        ]
        direct_probes = [UNCTAD_VIEWER, UNCTAD_FACTS_ATTEMPT, ITOPF_STATS_PAGE, ITOPF_PDF]
    else:
        archive_targets = [
            WB_API.format(indicator=WB_LAND),
            WB_API.format(indicator=WB_MARINE),
            WORLDBANK_INDICATOR_CSV.format(indicator=WB_LAND),
            WORLDBANK_INDICATOR_CSV.format(indicator=WB_MARINE),
            WB_BULK,
            WORLDBANK_ARCHIVES_PAGE,
            PROTECTED_PLANET,
        ]
        github_queries = [
            "ER.MRN.PTMR.ZS protected areas",
            "ER.LND.PTLD.ZS protected areas",
            "World Bank 2016h protected areas",
            "Protected Planet 1990 2014 CSV",
        ]
        direct_probes = [
            WB_BULK,
            WORLDBANK_SOURCE_BULK,
            WORLDBANK_INDICATOR_CSV.format(indicator=WB_LAND),
            WORLDBANK_INDICATOR_CSV.format(indicator=WB_MARINE),
            WORLDBANK_ARCHIVES_PAGE,
            PROTECTED_PLANET,
        ]

    return {
        "figure_id": figure_id,
        "generated": date.today().isoformat(),
        "direct_probes": run_parallel(safe_probe, direct_probes),
        "internet_archive_cdx": run_parallel(archive_cdx_probe, archive_targets),
        "github_repository_search": run_parallel(github_repo_search, github_queries),
        "github_code_search": run_parallel(github_code_search, github_queries[:2]),
    }


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def download_oil_data() -> pd.DataFrame | None:
    try:
        raw_csv = RAW / "owid_number_oil_spills.csv"
        raw_meta = RAW / "owid_number_oil_spills.metadata.json"
        download_binary(OWID_OIL_CSV, raw_csv)
        download_text(OWID_OIL_META, raw_meta)

        probes = [
            safe_probe(UNCTAD_VIEWER),
            safe_probe(UNCTAD_FACTS_ATTEMPT),
            safe_probe(ITOPF_STATS_PAGE),
            safe_probe(ITOPF_PDF),
        ]
        write_json(RAW / "figure_10_5_source_probe.json", probes)
        write_json(RAW / "figure_10_5_discovery_bundle.json", build_discovery_bundle("10-5"))

        oil = pd.read_csv(raw_csv)
        oil = oil[(oil["Entity"] == "World") & (oil["Year"].between(1970, 2016))].copy()
        oil["oil_spills_7_plus_tonnes"] = (
            oil["Large oil spills (>700 tonnes)"] + oil["Medium oil spills (7–700 tonnes)"]
        )
        clean = oil[
            [
                "Year",
                "Large oil spills (>700 tonnes)",
                "Medium oil spills (7–700 tonnes)",
                "oil_spills_7_plus_tonnes",
            ]
        ].rename(
            columns={
                "Year": "year",
                "Large oil spills (>700 tonnes)": "large_spills_gt_700_tonnes",
                "Medium oil spills (7–700 tonnes)": "medium_spills_7_to_700_tonnes",
            }
        )
        clean.to_csv(CLEAN / "figure_10_5_oil_spills_clean.csv", index=False)
        return clean
    except Exception as exc:
        write_json(RAW / "figure_10_5_error.json", {"error": repr(exc)})
        return None


def download_world_bank_indicator(indicator: str, raw_name: str) -> pd.DataFrame:
    url = WB_API.format(indicator=indicator)
    raw_json = download_text(url, RAW / raw_name)
    parsed = json.loads(raw_json)
    rows = parsed[1] if isinstance(parsed, list) and len(parsed) > 1 else []
    records = [
        {
            "year": int(row["date"]),
            "indicator": row["indicator"]["id"],
            "indicator_label": row["indicator"]["value"],
            "value": row["value"],
        }
        for row in rows
        if row.get("value") is not None
    ]
    return pd.DataFrame(records)


def download_world_bank_indicator_zip(indicator: str, raw_name: str) -> pd.DataFrame:
    url = WORLDBANK_INDICATOR_CSV.format(indicator=indicator)
    raw_path = RAW / raw_name
    content = download_binary(url, raw_path)
    with zipfile.ZipFile(io.BytesIO(content)) as archive:
        data_names = [name for name in archive.namelist() if name.startswith("API_") and name.endswith(".csv")]
        if not data_names:
            raise ValueError(f"No API CSV found in {raw_name}")
        with archive.open(data_names[0]) as handle:
            data = pd.read_csv(handle, skiprows=4)
    world = data[data["Country Code"] == "WLD"].copy()
    year_columns = [column for column in data.columns if column.isdigit()]
    long = world.melt(
        id_vars=["Country Name", "Country Code", "Indicator Name", "Indicator Code"],
        value_vars=year_columns,
        var_name="year",
        value_name="value",
    )
    long = long.dropna(subset=["value"])
    long["year"] = long["year"].astype(int)
    return long.rename(
        columns={
            "Indicator Code": "indicator",
            "Indicator Name": "indicator_label",
        }
    )[["year", "indicator", "indicator_label", "value"]]


def download_protected_area_data() -> pd.DataFrame | None:
    try:
        download_world_bank_indicator(WB_LAND, "world_bank_terrestrial_protected_areas.json")
        download_world_bank_indicator(WB_MARINE, "world_bank_marine_protected_areas.json")
        land = download_world_bank_indicator_zip(WB_LAND, "world_bank_terrestrial_protected_areas_csv.zip")
        marine = download_world_bank_indicator_zip(WB_MARINE, "world_bank_marine_protected_areas_csv.zip")
        probes = [
            safe_probe(WB_BULK),
            safe_probe(PROTECTED_PLANET),
            safe_probe("https://api.worldbank.org/v2/indicator/ER.MRN.PTMR.ZS?format=json"),
        ]
        write_json(RAW / "figure_10_6_source_probe.json", probes)
        write_json(RAW / "figure_10_6_discovery_bundle.json", build_discovery_bundle("10-6"))
        combined = pd.concat([land, marine], ignore_index=True)
        combined = combined[combined["year"].between(1990, 2014)].copy()
        if combined.empty:
            return None
        wide = (
            combined.pivot(index="year", columns="indicator", values="value")
            .reset_index()
            .rename(
                columns={
                    WB_LAND: "terrestrial_protected_area_pct_land",
                    WB_MARINE: "marine_protected_area_pct_territorial_waters",
                }
            )
            .sort_values("year")
        )
        wide.to_csv(CLEAN / "figure_10_6_protected_areas_clean.csv", index=False)
        return wide
    except Exception as exc:
        write_json(RAW / "figure_10_6_error.json", {"error": repr(exc)})
        return None


def add_source_note(fig: plt.Figure, note: str) -> None:
    fig.text(0.01, 0.01, note, ha="left", va="bottom", fontsize=8, color="#555555")


def plot_missing(fig_id: str, title: str, reason: str, output_name: str) -> None:
    fig, ax = plt.subplots(figsize=(10, 6), dpi=160)
    ax.axis("off")
    ax.text(0.5, 0.62, f"Figure {fig_id}: {title}", ha="center", fontsize=16, weight="bold")
    ax.text(0.5, 0.48, "Plot not fully reproducible from available data", ha="center", fontsize=13)
    ax.text(0.5, 0.38, reason, ha="center", va="center", wrap=True, fontsize=10)
    fig.tight_layout()
    fig.savefig(PLOTS / output_name)
    plt.close(fig)


def plot_oil(clean: pd.DataFrame | None) -> None:
    output = "figure_10_5_oil_spills.png"
    if clean is None or clean.empty:
        plot_missing("10-5", FIGURES["10-5"].title, "OWID/ITOPF spill-count data could not be downloaded.", output)
        return
    plt.style.use("seaborn-v0_8-whitegrid")
    fig, ax = plt.subplots(figsize=(10, 6), dpi=160)
    ax.plot(clean["year"], clean["oil_spills_7_plus_tonnes"], color="#111111", linewidth=2.5, label="Oil spills of at least 7 tonnes")
    ax.plot(clean["year"], clean["large_spills_gt_700_tonnes"], color="#777777", linewidth=1.5, linestyle="--", label="Large spills (>700 tonnes)")
    ax.set_title("Figure 10-5 recreation: Oil spills, 1970-2016", fontsize=14, pad=12)
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of oil spills")
    ax.set_xlim(1970, 2016)
    ax.set_ylim(bottom=0)
    ax.legend(loc="upper right", frameon=True)
    y2002 = clean.loc[clean["year"].eq(2002), "oil_spills_7_plus_tonnes"]
    if not y2002.empty:
        ax.annotate(
            "Book also plots oil shipped by sea;\nthat UNCTAD series was not downloaded.",
            xy=(2002, y2002.iloc[0]),
            xytext=(1993, 92),
            arrowprops={"arrowstyle": "->", "color": "#555555"},
            fontsize=9,
            color="#333333",
        )
    add_source_note(fig, "Source: OWID grapher number-oil-spills.csv; OWID cites ITOPF. Cleaned to 1970-2016; total = medium + large spills.")
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(PLOTS / output)
    plt.close(fig)


def plot_protected(clean: pd.DataFrame | None) -> None:
    output = "figure_10_6_protected_areas.png"
    if clean is None or clean.empty:
        plot_missing("10-6", FIGURES["10-6"].title, "World Bank protected-area data could not be downloaded.", output)
        return
    plt.style.use("seaborn-v0_8-whitegrid")
    fig, ax = plt.subplots(figsize=(10, 6), dpi=160)
    ax.plot(clean["year"], clean["terrestrial_protected_area_pct_land"], color="#9a9a9a", linewidth=2.5, label="Terrestrial protected areas")
    ax.plot(clean["year"], clean["marine_protected_area_pct_territorial_waters"], color="#111111", linewidth=2.5, label="Marine protected areas")
    ax.set_title("Figure 10-6 recreation: Protected areas, 1990-2014", fontsize=14, pad=12)
    ax.set_xlabel("Year")
    ax.set_ylabel("Percent")
    ax.set_xlim(1990, 2014)
    ax.set_ylim(0, 16)
    ax.legend(loc="upper left", frameon=True)
    if clean["year"].min() > 1990:
        ax.annotate(
            "Current WDI API returned World values\nonly from 2013 onward.",
            xy=(2013, clean["marine_protected_area_pct_territorial_waters"].iloc[0]),
            xytext=(1994, 5),
            arrowprops={"arrowstyle": "->", "color": "#555555"},
            fontsize=9,
            color="#333333",
        )
    add_source_note(fig, "Source: World Bank API, indicators ER.LND.PTLD.ZS and ER.MRN.PTMR.ZS. Filtered to World, 1990-2014.")
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(PLOTS / output)
    plt.close(fig)


def crop_original_reference(config: FigureConfig) -> Path | None:
    if not config.book_reference_image.exists():
        return None
    img = Image.open(config.book_reference_image).convert("RGB")
    crop = img.crop(config.book_crop_box)
    out = ORIGINALS / f"figure_{config.figure_id.replace('-', '_')}_original_crop.png"
    crop.save(out)
    return out


def image_metrics(original: Image.Image, recreated: Image.Image) -> dict[str, float]:
    size = (600, 420)
    a = ImageOps.grayscale(original.resize(size))
    b = ImageOps.grayscale(recreated.resize(size))
    diff = ImageChops.difference(a, b)
    hist = diff.histogram()
    sq = sum(value * ((idx % 256) ** 2) for idx, value in enumerate(hist))
    rms = math.sqrt(sq / float(size[0] * size[1]))
    mean_abs = sum(value * (idx % 256) for idx, value in enumerate(hist)) / float(size[0] * size[1])
    a_data = a.get_flattened_data() if hasattr(a, "get_flattened_data") else a.getdata()
    b_data = b.get_flattened_data() if hasattr(b, "get_flattened_data") else b.getdata()
    a_vals = list(a_data)
    b_vals = list(b_data)
    ma = sum(a_vals) / len(a_vals)
    mb = sum(b_vals) / len(b_vals)
    numerator = sum((x - ma) * (y - mb) for x, y in zip(a_vals, b_vals))
    den_a = math.sqrt(sum((x - ma) ** 2 for x in a_vals))
    den_b = math.sqrt(sum((y - mb) ** 2 for y in b_vals))
    corr = numerator / (den_a * den_b) if den_a and den_b else 0.0
    return {"mean_abs_diff": round(mean_abs, 2), "rms_diff": round(rms, 2), "pixel_correlation": round(corr, 4)}


def make_comparison(config: FigureConfig) -> dict[str, Any]:
    original_path = crop_original_reference(config)
    recreated_path = ROOT / config.plot_file
    if original_path is None or not recreated_path.exists():
        return {
            "figure_id": config.figure_id,
            "comparison_image": "",
            "metrics": {},
            "visual_validation": "poor",
            "reasoning": "Original reference crop or recreated plot was unavailable.",
        }
    original = Image.open(original_path).convert("RGB")
    recreated = Image.open(recreated_path).convert("RGB")
    metrics = image_metrics(original, recreated)

    panel_w, panel_h = 800, 560
    canvas = Image.new("RGB", (panel_w * 2, panel_h + 62), "white")
    draw = ImageDraw.Draw(canvas)
    draw.text((20, 18), f"Figure {config.figure_id} original reference", fill="black")
    draw.text((panel_w + 20, 18), "Recreated plot", fill="black")
    left = ImageOps.contain(original, (panel_w - 30, panel_h - 80))
    right = ImageOps.contain(recreated, (panel_w - 30, panel_h - 80))
    canvas.paste(left, (15, 55))
    canvas.paste(right, (panel_w + 15, 55))
    out = VALIDATION / f"figure_{config.figure_id.replace('-', '_')}_comparison.png"
    canvas.save(out)
    return {
        "figure_id": config.figure_id,
        "comparison_image": str(out.relative_to(ROOT)),
        "metrics": metrics,
        "visual_validation": config.visual_validation,
        "reasoning": config.visual_reasoning,
    }


def summarize_discovery_bundle(config: FigureConfig) -> list[str]:
    path = RAW / f"figure_{config.figure_id.replace('-', '_')}_discovery_bundle.json"
    if not path.exists():
        return ["- Discovery bundle not generated."]
    try:
        bundle = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return [f"- Discovery bundle could not be parsed: {exc!r}"]

    lines = [
        f"- Machine-readable bundle: `data/raw/{path.name}`",
        f"- Direct probes recorded: {len(bundle.get('direct_probes', []))}",
        f"- Internet Archive CDX targets checked: {len(bundle.get('internet_archive_cdx', []))}",
        f"- GitHub repository searches recorded: {len(bundle.get('github_repository_search', []))}",
        f"- GitHub code searches recorded: {len(bundle.get('github_code_search', []))}",
    ]
    archive_hits = []
    archive_errors = 0
    for item in bundle.get("internet_archive_cdx", []):
        count = item.get("capture_count_returned", 0)
        if count:
            archive_hits.append(f"{item.get('target_url')} ({count} returned)")
        elif item.get("error"):
            archive_errors += 1
    if archive_hits:
        lines.append("- Archive candidates returned:")
        lines.extend(f"  - {hit}" for hit in archive_hits[:8])
    else:
        if archive_errors:
            lines.append(f"- Archive candidates returned: none; {archive_errors} CDX probes errored or timed out under the default speed budget.")
        else:
            lines.append("- Archive candidates returned: none in the limited CDX sample.")

    direct_downloads = []
    for item in bundle.get("direct_probes", []):
        content_type = item.get("content_type", "")
        if item.get("status_code") == 200 and ("zip" in content_type or "pdf" in content_type or "csv" in content_type):
            direct_downloads.append(f"{item.get('url')} ({content_type})")
    if direct_downloads:
        lines.append("- Direct downloadable candidates:")
        lines.extend(f"  - {item}" for item in direct_downloads[:8])

    github_hits = []
    for item in bundle.get("github_repository_search", []):
        total = item.get("total_count")
        if isinstance(total, int) and total > 0:
            github_hits.append(f"{item.get('query')} ({total} repository hits)")
    if github_hits:
        lines.append("- GitHub repository candidates returned:")
        lines.extend(f"  - {hit}" for hit in github_hits[:8])
    else:
        lines.append("- GitHub repository candidates returned: none or API unavailable.")
    return lines


def write_source_logs() -> None:
    for config in FIGURES.values():
        lines = [
            f"# Source Discovery Log: Figure {config.figure_id}",
            "",
            f"- Figure number: {config.figure_id}",
            f"- Figure title: {config.title}",
            f"- Original book citation: {config.book_citation}",
            f"- Reproduction status: {config.reproduction_status}",
            f"- Confidence score: {config.confidence_score}",
            "",
            "## Search Queries Attempted",
            "",
        ]
        lines.extend(f"- {query}" for query in config.search_queries)
        lines.extend(["", "## Sources Investigated", ""])
        for source in config.investigated_sources:
            lines.extend(
                [
                    f"### {source['source']}",
                    "",
                    f"- URL: {source['url']}",
                    f"- Decision: {source['decision']}",
                    f"- Rationale: {source['reason']}",
                    "",
                ]
            )
        lines.extend(["## Automated Discovery Adapter Results", ""])
        lines.extend(summarize_discovery_bundle(config))
        lines.append("")
        download_urls = [
            s["url"]
            for s in config.investigated_sources
            if s["decision"].startswith("accepted") and s["url"].startswith("http")
        ]
        lines.extend(["## Download URLs", ""])
        lines.extend(f"- {url}" for url in download_urls)
        lines.extend(
            [
                "",
                "## Archive URLs",
                "",
                "- Not yet pinned. Recommended: capture exact OWID grapher CSV, World Bank API JSON, and any located historical institutional files via Internet Archive or perma.cc before publication.",
                "",
                "## Remaining Uncertainties",
                "",
                f"- {config.notes}",
                "",
                "## Recommended Next Steps",
                "",
            ]
        )
        if config.figure_id == "10-5":
            lines.extend(
                [
                    "- Search Internet Archive CDX for historical OWID grapher CSV snapshots around 2016-2018.",
                    "- Inspect OWID historical commits or grapher metadata for `Roser 2016r` and oil-shipped-by-sea source data.",
                    "- Locate UNCTAD seaborne trade oil cargo table or archived CSV used by the book.",
                    "- Replot with dual axes only after the oil-shipped-by-sea series is independently downloaded.",
                ]
            )
        else:
            lines.extend(
                [
                    "- Locate the World Bank 2016h/2017 bulk WDI files or archived indicator downloads.",
                    "- Check UNEP-WCMC/Protected Planet historical WDPA snapshots and WRI compilation files.",
                    "- Confirm whether the book used terrestrial percent of land area, terrestrial+inland water, or another WDI indicator variant.",
                    "- Replot only after the 1990-2014 annual series is recovered.",
                ]
            )
        (SOURCE_LOGS / f"figure_{config.figure_id.replace('-', '_')}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_lineage() -> None:
    rows = []
    json_rows = []
    for config in FIGURES.values():
        chain = []
        for index, item in enumerate(config.lineage, start=1):
            row = {
                "figure_id": config.figure_id,
                "figure_title": config.title,
                "stage_order": index,
                "stage": item["stage"],
                "value": item["value"],
                "stage_status": item["status"],
            }
            rows.append(row)
            chain.append(row)
        json_rows.append({"figure_id": config.figure_id, "figure_title": config.title, "lineage": chain})
    with (LINEAGE / "figure_lineage.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    write_json(LINEAGE / "figure_lineage.json", json_rows)


def write_metadata(validations: dict[str, dict[str, Any]]) -> None:
    rows = []
    today = date.today().isoformat()
    for config in FIGURES.values():
        validation = validations.get(config.figure_id, {})
        if config.figure_id == "10-5":
            original_dataset = "Roser 2016r / OWID historical figure data; ITOPF and UNCTAD inputs"
            dataset_url = OWID_OIL_CSV
            archive_url = ""
        else:
            original_dataset = "World Bank 2016h/2017 WDI historical protected-area indicators"
            dataset_url = f"{WORLDBANK_INDICATOR_CSV.format(indicator=WB_LAND)}; {WORLDBANK_INDICATOR_CSV.format(indicator=WB_MARINE)}"
            archive_url = ""
        rows.append(
            {
                "figure_id": config.figure_id,
                "chapter": config.chapter,
                "title": config.title,
                "book_page": config.book_page,
                "claim_summary": config.claim_summary,
                "book_citation": config.book_citation,
                "original_dataset": original_dataset,
                "dataset_url": dataset_url,
                "archive_url": archive_url,
                "download_date": today,
                "reproduction_status": config.reproduction_status,
                "confidence_score": config.confidence_score,
                "visual_validation": validation.get("visual_validation", config.visual_validation),
                "visual_similarity_metrics": json.dumps(validation.get("metrics", {}), sort_keys=True),
                "comparison_image": validation.get("comparison_image", ""),
                "notes": config.notes,
            }
        )
    with METADATA.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_report(validations: dict[str, dict[str, Any]]) -> None:
    md = [
        "# Enlightenment Now Figure-Reproduction Pipeline Report",
        "",
        f"Generated: {date.today().isoformat()}",
        "",
        "## Design Decisions",
        "",
        "- The pipeline now separates source discovery, data download, cleaning, plotting, visual validation, metadata, and lineage outputs.",
        "- Missing legacy data is represented as a provenance/status problem rather than a plotting exception.",
        "- Status values use the hardened vocabulary: verified_reproduction, updated_equivalent, partial_match, source_unavailable, manual_review_needed.",
        "- Visual validation is simple by design: original Kindle reference crops and recreated plots are placed side-by-side, with pixel-level metrics recorded only as rough diagnostics.",
        "- Source logs are written as researcher-facing markdown so another pass can continue discovery without replaying the whole conversation.",
        "- Discovery adapters now record Internet Archive CDX candidates, GitHub repository/code-search probes, World Bank bulk-download probes, and institutional source probes as raw JSON evidence.",
        "",
        "## Figure Status Summary",
        "",
    ]
    for config in FIGURES.values():
        validation = validations.get(config.figure_id, {})
        metrics = validation.get("metrics", {})
        md.extend(
            [
                f"### Figure {config.figure_id}: {config.title}",
                "",
                f"- Book citation: {config.book_citation}",
                f"- Reproduction status: {config.reproduction_status}",
                f"- Confidence score: {config.confidence_score}",
                f"- Visual validation: {validation.get('visual_validation', config.visual_validation)}",
                f"- Visual metrics: `{json.dumps(metrics, sort_keys=True)}`",
                f"- Comparison image: `{validation.get('comparison_image', '')}`",
                f"- Source log: `outputs/source_logs/figure_{config.figure_id.replace('-', '_')}.md`",
                f"- Lineage table: `outputs/lineage/figure_lineage.csv` and `outputs/lineage/figure_lineage.json`",
                f"- Notes: {config.notes}",
                "",
            ]
        )
    md.extend(
        [
            "## What Must Change Before Chapter-Scale Work",
            "",
            "- Promote discovery-adapter candidates into curated source decisions after human review.",
            "- Store archive/perma URLs and file hashes as required fields before any figure can be upgraded to `verified_reproduction`.",
            "- Add a human review checklist for dual-axis charts and charts where modern APIs expose only current snapshots.",
            "- Keep plotting scripts tolerant of missing variables and produce explicit placeholder/partial plots.",
            "- Track exact downloaded file hashes before publication.",
            "",
        ]
    )
    report_md = "\n".join(md)
    (REPORT / "enlightenment_now_poc_report.md").write_text(report_md, encoding="utf-8")
    html = "<!doctype html><html><head><meta charset='utf-8'><title>Enlightenment Now POC Report</title><style>body{font-family:Arial,sans-serif;max-width:960px;margin:40px auto;line-height:1.55}code{background:#f2f2f2;padding:2px 4px}</style></head><body>"
    for line in report_md.splitlines():
        if line.startswith("# "):
            html += f"<h1>{line[2:]}</h1>\n"
        elif line.startswith("## "):
            html += f"<h2>{line[3:]}</h2>\n"
        elif line.startswith("### "):
            html += f"<h3>{line[4:]}</h3>\n"
        elif line.startswith("- "):
            html += f"<li>{line[2:]}</li>\n"
        elif line.strip():
            html += f"<p>{line}</p>\n"
    html += "</body></html>\n"
    (REPORT / "enlightenment_now_poc_report.html").write_text(html, encoding="utf-8")


def write_readme() -> None:
    readme = """# Enlightenment Now Figure Reconstruction POC

Hardened vertical-slice pipeline for figures 10-5 and 10-6 from Steven Pinker's
*Enlightenment Now*.

Run:

```bash
/Users/alfred/Documents/MIsc/.venv/bin/python scripts/recreate_figures.py
```

Key outputs:

- `data/figure_metadata.csv`
- `outputs/source_logs/`
- `outputs/lineage/figure_lineage.csv`
- `outputs/lineage/figure_lineage.json`
- `outputs/validation/`
- `outputs/report/enlightenment_now_poc_report.md`
"""
    (ROOT / "README.md").write_text(readme, encoding="utf-8")


def clean_previous_outputs() -> None:
    for directory in [RAW, CLEAN, PLOTS, REPORT, SOURCE_LOGS, LINEAGE, VALIDATION, ORIGINALS]:
        directory.mkdir(parents=True, exist_ok=True)
        for item in directory.iterdir():
            if item.is_file():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)


def main() -> None:
    ensure_dirs()
    clean_previous_outputs()
    oil = download_oil_data()
    protected = download_protected_area_data()
    plot_oil(oil)
    plot_protected(protected)
    validations = {config.figure_id: make_comparison(config) for config in FIGURES.values()}
    write_source_logs()
    write_lineage()
    write_metadata(validations)
    write_report(validations)
    write_readme()
    print(f"Wrote hardened project to {ROOT}")


if __name__ == "__main__":
    invalid = {cfg.reproduction_status for cfg in FIGURES.values()} - VALID_STATUSES
    if invalid:
        raise SystemExit(f"Invalid statuses configured: {sorted(invalid)}")
    main()
