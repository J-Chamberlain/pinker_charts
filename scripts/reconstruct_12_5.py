from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import date
from pathlib import Path

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import pandas as pd
import requests
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "figures" / "12-5"
PDF = ROOT / "references" / "enlightenment_now_supplemental_graphics.pdf"
TODAY = date.today().isoformat()

OWID_CSV = "https://ourworldindata.org/grapher/aviation-fatalities-per-million-passengers.csv?v=1&csvType=full&useColumnShortNames=false"
OWID_METADATA = "https://ourworldindata.org/grapher/aviation-fatalities-per-million-passengers.metadata.json?v=1&csvType=full&useColumnShortNames=false"
OWID_INDICATOR_METADATA = "https://api.ourworldindata.org/v1/indicators/930564.metadata.json"
ASN_SHEET = "https://docs.google.com/spreadsheets/d/1SDp7p1y6m7N5xD5_fpOkYOrJvd68V7iy6etXy2cetb8/gviz/tq?tqx=out:csv&sheet=Accidents+and+fatalities+per+year"
ASN_WAYBACK_2017 = "https://web.archive.org/web/20171007141946/https://aviation-safety.net/statistics/"
ASN_WAYBACK_2017_CDX = "https://web.archive.org/cdx?url=aviation-safety.net/statistics/&from=2017&to=2018&output=json&fl=timestamp,original,statuscode,mimetype&filter=statuscode:200&limit=10"


def get(url: str) -> bytes:
    response = requests.get(url, headers={"User-Agent": "pinker-figure-12-5"}, timeout=60)
    response.raise_for_status()
    return response.content


def ensure_dirs() -> None:
    for rel in [
        "data/raw",
        "data/clean",
        "plots/book_period",
        "plots/extended",
        "plots/comparisons",
        "captions",
        "provenance",
        "source_logs",
        "search_iterations",
        "discrepancy_logs",
        "anomaly_reviews",
        "metadata",
        "lineage",
        "checksums",
    ]:
        (BASE / rel).mkdir(parents=True, exist_ok=True)
    (ROOT / "tmp/pdfs").mkdir(parents=True, exist_ok=True)


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n")


def strip_trailing_whitespace(path: Path) -> None:
    text = path.read_text(errors="replace")
    cleaned = []
    for line in text.splitlines():
        line = line.rstrip()
        while line.startswith(" \t"):
            line = line[1:]
        cleaned.append(line)
    path.write_text("\n".join(cleaned) + "\n")


def render_pdf_reference() -> Path:
    page = ROOT / "tmp/pdfs" / "figure_12_5_page-20.png"
    if not page.exists():
        subprocess.run(
            [
                "pdftoppm",
                "-f",
                "20",
                "-l",
                "20",
                "-png",
                "-r",
                "180",
                str(PDF),
                str(ROOT / "tmp/pdfs" / "figure_12_5_page"),
            ],
            check=True,
        )
    image = Image.open(page)
    out = BASE / "plots/comparisons/supplemental_pdf_reference_figure_12_5.png"
    image.crop((25, 115, 985, 810)).save(out)
    return out


def download_sources() -> tuple[Path, Path, Path, Path, Path]:
    raw = BASE / "data/raw"
    owid_csv = raw / "aviation-fatalities-per-million-passengers_owid_2024.csv"
    owid_meta = raw / "aviation-fatalities-per-million-passengers_owid_metadata_2026-07-09.json"
    indicator_meta = raw / "owid_indicator_930564_metadata_2026-07-09.json"
    asn_csv = raw / "asn_accidents_and_fatalities_per_year_google_sheet_2026-07-09.csv"
    cdx_json = raw / "asn_statistics_wayback_cdx_2017_2018.json"
    archive_html = raw / "asn_statistics_wayback_20171007141946.html"

    owid_csv.write_bytes(get(OWID_CSV))
    owid_meta.write_bytes(get(OWID_METADATA))
    indicator_meta.write_bytes(get(OWID_INDICATOR_METADATA))
    asn_csv.write_bytes(get(ASN_SHEET))
    cdx_json.write_bytes(get(ASN_WAYBACK_2017_CDX))
    archive_html.write_bytes(get(ASN_WAYBACK_2017))
    strip_trailing_whitespace(asn_csv)
    strip_trailing_whitespace(archive_html)
    return owid_csv, owid_meta, indicator_meta, asn_csv, cdx_json


def build_clean_data(owid_csv: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    df = pd.read_csv(owid_csv)
    df = df[df["Entity"].eq("World")].copy()
    df = df.rename(columns={"Fatalities per million passengers": "deaths_per_million_passengers"})
    df = df[["Year", "deaths_per_million_passengers"]]
    book = df[df["Year"].between(1970, 2015)].copy()
    extended = df[df["Year"].between(1970, 2022)].copy()
    book.to_csv(BASE / "data/clean/figure_12_5_book_period_clean.csv", index=False)
    extended.to_csv(BASE / "data/clean/figure_12_5_extended_clean.csv", index=False)
    return book, extended


def draw_series(data: pd.DataFrame, out: Path, extended: bool) -> None:
    fig, ax = plt.subplots(figsize=(7.0, 4.8), dpi=180)
    solid = data[data["Year"] <= 2015]
    ax.plot(solid["Year"], solid["deaths_per_million_passengers"], color="#242424", lw=2.4)
    if extended:
        ext = data[data["Year"] >= 2015]
        ax.plot(ext["Year"], ext["deaths_per_million_passengers"], color="#242424", lw=2.4, ls="--")
    ax.set_xlim(1970, 2022 if extended else 2015)
    ax.set_ylim(0, 7)
    ax.set_ylabel("Deaths per million passengers per year")
    ax.set_xticks([1970, 1975, 1980, 1985, 1990, 1995, 2000, 2005, 2010, 2015])
    if extended:
        ax.set_xticks([1970, 1975, 1980, 1985, 1990, 1995, 2000, 2005, 2010, 2015, 2020])
    ax.set_yticks(range(0, 8))
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_color("#666666")
    ax.spines["left"].set_color("#666666")
    ax.tick_params(colors="#333333")
    note = "Source-family successor: OWID processed ASN annual fatalities / World Bank passengers."
    if extended:
        note = "Solid: book period to 2015. Dashed: comparable OWID/ASN/World Bank successor through 2022."
    ax.text(0, -0.18, note, transform=ax.transAxes, fontsize=7.2, va="top")
    fig.tight_layout()
    fig.savefig(out, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def side_by_side(reference: Path, recreated: Path, output: Path, title: str) -> None:
    ref = mpimg.imread(reference)
    rec = mpimg.imread(recreated)
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.2), dpi=180)
    for ax, image, label in zip(axes, [ref, rec], ["Supplemental PDF reference", "Recreated"]):
        ax.imshow(image)
        ax.set_title(label, fontsize=10)
        ax.axis("off")
    fig.suptitle(title, fontsize=12)
    fig.tight_layout()
    fig.savefig(output, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def write_docs(book: pd.DataFrame, extended: pd.DataFrame) -> None:
    source_note = (
        "Supplemental PDF cites Aviation Safety Network 2017, with passengers from World Bank 2016b. "
        "The exact 2017 ASN extraction has not been recovered. This run replaces the prior flight-phase proxy "
        "with OWID's processed aviation-fatalities-per-million-passengers indicator, which uses ASN annual "
        "airliner fatalities and World Bank passenger counts and documents the same calculation."
    )
    fidelity = (
        f"Current OWID successor values used directly: 1970={book.iloc[0]['deaths_per_million_passengers']:.6g}, "
        f"1973={book.loc[book['Year'].eq(1973), 'deaths_per_million_passengers'].iloc[0]:.6g}, "
        f"2015={book.loc[book['Year'].eq(2015), 'deaths_per_million_passengers'].iloc[0]:.6g}. "
        "Tolerance to recovered successor CSV is exact to CSV precision because the clean data are a column rename/filter. "
        "Tolerance to the unrecovered 2017 book source is not asserted."
    )
    write(
        BASE / "captions/caption.txt",
        "Figure 12-5: Plane crash deaths, 1970-2015. Source-family successor reconstruction from "
        "OWID processed ASN annual fatalities divided by World Bank passengers. Exact ASN 2017 book "
        "extraction remains unrecovered; status: partial_match.",
    )
    write(
        BASE / "source_logs/source_log.md",
        f"""# Figure 12-5 Source Log

- 2026-06-30: Captured Kindle figure/source-note evidence; prior reconstruction used OWID-hosted ASN 2019 flight-phase data plus World Bank passengers.
- {TODAY}: Supplemental Graphics PDF page 20 inspected. Figure title is `Plane crash deaths, 1970-2015`; source line is `Aviation Safety Network 2017. Data on the number of passengers are from World Bank 2016b.`
- {TODAY}: Located current OWID grapher indicator `aviation-fatalities-per-million-passengers`. Its metadata says it is calculated by dividing Aviation Safety Network fatalities by World Bank worldwide passengers and multiplying by 1,000,000.
- {TODAY}: Downloaded OWID grapher CSV/metadata, OWID indicator metadata, current ASN Google Sheet export for `Accidents and fatalities per year`, and a 2017 Wayback capture of ASN's statistics landing page.
- {TODAY}: The 2017 ASN landing-page archive confirms ASN statistics existed and was last updated 7 March 2017, but it exposes infographics and navigation, not the exact underlying CSV used by Pinker.
- {TODAY}: Source decision: use the current OWID processed indicator as the closest verifiable successor for reconstruction/discrepancy analysis. Do not mark verified reproduction because the ASN 2017 extraction and World Bank 2016b vintage are still not recovered.
""",
    )
    write(
        BASE / "provenance/provenance.md",
        f"""# Figure 12-5 Provenance

Title: Plane crash deaths, 1970-2015

Canonical reference: Supplemental Graphics PDF page 20. The source note cites Aviation Safety Network 2017 and says passenger counts come from World Bank 2016b.

Recovered source trail:

- Supplemental PDF: `references/enlightenment_now_supplemental_graphics.pdf`, page 20.
- ASN archived source page: 2017-10-07 Wayback capture of `https://aviation-safety.net/statistics/`, stored as `data/raw/asn_statistics_wayback_20171007141946.html`.
- Current ASN successor data: public Google Sheet export linked by OWID indicator metadata, stored as `data/raw/asn_accidents_and_fatalities_per_year_google_sheet_2026-07-09.csv`.
- Current processed successor: OWID grapher CSV `aviation-fatalities-per-million-passengers`, stored as `data/raw/aviation-fatalities-per-million-passengers_owid_2024.csv`.
- Current World Bank passenger provenance: OWID metadata cites WDI indicator `IS.AIR.PSGR`.

{source_note}

{fidelity}

The early-1970s discrepancy in the previous artifact is explained by source substitution: the prior reconstruction used the ASN 2019 flight-phase table, which includes corporate jet and military transport accidents and omits 1972 after merging to World Bank passenger data. OWID's processed indicator uses ASN annual airliner fatalities, including passenger and cargo flights with sabotage/hijacking events, and gives the book-consistent 1970 value just below five deaths per million passengers.

No digitized chart values were used as reconstruction data.
""",
    )
    write(
        BASE / "search_iterations/search_iterations.md",
        f"""# Figure 12-5 Search Iterations

- Supplemental PDF inspection: located figure on page 20 with surrounding text saying the passenger fatality risk fell from less than five in a million in 1970 to about one hundredth of that risk by 2015.
- Bibliography resolution: the figure's source line is the operative bibliographic evidence available in this repository: Aviation Safety Network 2017 and World Bank 2016b. No separate bibliography row for these keys exists in `data/bibliography/`.
- Live successor search: found OWID grapher `aviation-fatalities-per-million-passengers`, whose metadata names ASN annual fatalities and World Bank WDI passenger counts and documents the same formula.
- ASN source search: downloaded current ASN annual accidents/fatalities Google Sheet through the URL exposed in OWID indicator metadata.
- Archive search: checked Wayback CDX for `aviation-safety.net/statistics/` in 2017-2018 and saved the 2017-10-07 capture. The page confirms the ASN statistics section and `Last updated: 7 March 2017`, but does not expose a CSV or table equivalent to the current Google Sheet.
- Discrepancy analysis: prior baseline used ASN 2019 flight-phase casualties. The replacement source uses the annual airliner fatality series that OWID now uses for this exact derived indicator.
- Outcome: closest verifiable successor recovered; exact ASN 2017 extraction remains unrecovered, so status remains `partial_match`.
""",
    )
    write(
        BASE / "discrepancy_logs/discrepancy_log.md",
        f"""# Figure 12-5 Discrepancy Log

Status: `partial_match`

Resolved discrepancy from the prior baseline:

- The earlier reconstruction under-matched the early-1970s peak because it used `Aviation accidents and fatalities by flight phase (ASN, 2019)`, a different ASN table whose metadata includes corporate jet and military transport accidents.
- The current reconstruction uses OWID's processed `Fatalities per million passengers` indicator, whose metadata documents the book formula: ASN annual fatalities divided by World Bank passengers, multiplied by 1,000,000.
- The current successor gives 1970 = {book.iloc[0]['deaths_per_million_passengers']:.6f}, consistent with the chapter text's `less than five in a million`.

Remaining discrepancy/blocker:

- Exact ASN 2017 data extraction and World Bank 2016b passenger vintage were not recovered. Current ASN/OWID/World Bank successor values are not silently treated as the book vintage.
- The 1972 ASN fatality spike is visible in the ASN annual sheet, but the World Bank passenger series used by OWID has no 1972 World observation, so the processed rate series jumps from 1971 to 1973. The book figure visually has a sharp early-1970s peak; current successor data reproduce that shape with a missing 1972 point.

Visual fidelity:

- Axis range and y-scale match the book: 1970-2015 and 0-7 deaths per million passengers per year.
- Typography and exact point placement are approximate; source-vintage uncertainty prevents verified reproduction.
""",
    )
    write(
        BASE / "anomaly_reviews/anomaly_review.md",
        f"""# Figure 12-5 Anomaly Review

Status: `partial_match`

Editorial self-review:

- Source recovery: partial. The closest verifiable successor is identified and preserved, but the exact ASN 2017 extraction is not.
- Data fidelity: clean data are a direct filter/rename of the recovered OWID successor CSV. No values are invented or digitized.
- Visual fidelity: the new plot matches the book axes and early-1970s magnitude better than the previous flight-phase proxy, but cannot be labeled verified because the source vintage differs.
- Extension quality: a dashed 2016-2022 segment is included only in the extended artifact because OWID metadata documents the same ASN/World Bank source family. It is labeled successor, not book-period evidence.
- Status calibration: keep `partial_match`; do not promote to `verified_reproduction`.

Reviewer challenge:

- Pinker would likely ask for the 2017 ASN export used at production time.
- A data journalist would ask why 1972 is missing in the rate series; the answer is absent World Bank passenger data for 1972 in the OWID/WDI series.
- A peer reviewer would ask whether current ASN revisions changed 1970-2015 values; this remains possible and is why the figure is not verified.
""",
    )
    write(
        BASE / "review_checklist.md",
        f"""# Figure 12-5 Acceptance Checklist

- Figure ID: 12-5
- Title: Plane crash deaths, 1970-2015
- Reviewer: Codex
- Review date: {TODAY}
- Current status: partial_match

## Phase Summary

- [x] Supplemental PDF figure inspected.
- [x] Figure image/source note/surrounding text captured.
- [x] Bibliography/source keys resolved as far as repository evidence allows.
- [x] Live source successor recovered and archived locally.
- [x] Wayback source page checked for 2017 ASN statistics.
- [x] Book-period reconstruction generated from legitimate successor data.
- [x] Extension limited to same documented ASN/World Bank source family.
- [x] Editorial self-review completed.
- [x] Registry intentionally not updated in this orchestrated run.

## Decision

Partial match. The current successor fixes the early-1970s source-family mismatch, but the exact ASN 2017/World Bank 2016b vintage remains unrecovered.
""",
    )
    metadata = {
        "figure_id": "12-5",
        "title": "Plane crash deaths, 1970-2015",
        "status": "partial_match",
        "lifecycle_stage": "source_recovery_and_discrepancy_analysis",
        "confidence": "medium",
        "review_date": TODAY,
        "source_note": source_note,
        "book_period_source": "Current OWID processed ASN/World Bank successor, not exact ASN 2017 vintage",
        "extension_source": "Same OWID processed ASN/World Bank successor through 2022",
        "exact_original_recovered": False,
        "registry_updated": False,
    }
    (BASE / "metadata/metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    lineage = pd.DataFrame(
        [
            {"figure_id": "12-5", "artifact": "supplemental_pdf_reference", "source": "Supplemental Graphics PDF page 20", "status": "captured"},
            {"figure_id": "12-5", "artifact": "asn_2017_wayback_page", "source": ASN_WAYBACK_2017, "status": "captured_no_data_table"},
            {"figure_id": "12-5", "artifact": "owid_successor_indicator", "source": OWID_CSV, "status": "used_for_partial_match"},
            {"figure_id": "12-5", "artifact": "asn_current_sheet", "source": ASN_SHEET, "status": "provenance_support"},
            {"figure_id": "12-5", "artifact": "world_bank_passengers", "source": "WDI IS.AIR.PSGR via OWID metadata", "status": "provenance_support"},
        ]
    )
    lineage.to_csv(BASE / "lineage/figure_lineage.csv", index=False)
    (BASE / "lineage/figure_lineage.json").write_text(lineage.to_json(orient="records", indent=2) + "\n")


def sha256s() -> None:
    rows = []
    for rel_root in ["data/raw", "data/clean", "plots"]:
        for path in sorted((BASE / rel_root).rglob("*")):
            if path.is_file():
                rows.append(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.relative_to(BASE)}")
    write(BASE / "checksums/sha256sums.txt", "\n".join(rows))


def main() -> None:
    ensure_dirs()
    reference = render_pdf_reference()
    owid_csv, *_ = download_sources()
    book, extended = build_clean_data(owid_csv)
    book_plot = BASE / "plots/book_period/figure_12_5_book_period_reconstruction.png"
    ext_plot = BASE / "plots/extended/figure_12_5_extended_reconstruction.png"
    draw_series(book, book_plot, extended=False)
    draw_series(extended, ext_plot, extended=True)
    side_by_side(reference, book_plot, BASE / "plots/comparisons/figure_12_5_book_period_comparison.png", "Figure 12-5 book-period comparison")
    side_by_side(reference, ext_plot, BASE / "plots/comparisons/figure_12_5_extended_comparison.png", "Figure 12-5 extended comparison")
    write_docs(book, extended)
    sha256s()


if __name__ == "__main__":
    main()
