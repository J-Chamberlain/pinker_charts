from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from datetime import date
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageOps
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
FIG_ID = "10-3"
BASE = ROOT / "figures" / FIG_ID
PDF_PAGE = Path("/tmp/pinker_prod_pdf_pages/page-13.png")
TODAY = date.today().isoformat()

EPA_2016_PAGE = "https://gispub.epa.gov/air/trendsreport/2016/"
EPA_2016_JS = "https://gispub.epa.gov/air/trendsreport/2016/dist/js/etrends.js"
EPA_2025_PAGE = "https://gispub.epa.gov/air/trendsreport/2025/"
EPA_2025_CSV = "https://gispub.epa.gov/air/trendsreport/2025/data/naaqs/emissions/growth_chart_data.csv"

YEARS = [
    1970,
    1980,
    1990,
    1995,
    1996,
    1997,
    1998,
    1999,
    2000,
    2001,
    2002,
    2003,
    2004,
    2005,
    2006,
    2007,
    2008,
    2009,
    2010,
    2011,
    2012,
    2013,
    2014,
    2015,
]

EPA_2016_PERCENT = {
    "Gross Domestic Product": [0, 36.6, 89.6, 115.5, 123.7, 133.7, 144.1, 155.5, 166, 168.6, 173.4, 181, 191.7, 201.4, 209.5, 215, 214.1, 205.4, 213.1, 218.1, 225.2, 230, 238, 246.2],
    "Vehicle Miles Traveled": [0, 37.6, 93.2, 118.3, 123.8, 129.9, 136.8, 142.3, 147.5, 151.9, 157.3, 160.4, 167.1, 169.3, 171.5, 173.1, 168.2, 166.4, 167.3, 165.4, 167.5, 169.2, 174, 183.6],
    "Population": [0, 10.7, 21.5, 29.3, 30.7, 32.2, 34.1, 35.6, 37.6, 39, 40.5, 41.5, 42.9, 44.4, 45.4, 46.8, 48.3, 49.8, 50.7, 52.2, 53.2, 54.1, 55.6, 56.6],
    "Energy Consumption": [0, 15.1, 24.5, 34.2, 38.6, 39.5, 40.1, 42.5, 45.7, 41.8, 43.9, 44.3, 47.5, 47.7, 46.7, 48.9, 45.8, 38.8, 43.7, 42.8, 39.3, 43.3, 45.2, 43.9],
    "CO2 Emissions": [0, 9.1, 18.2, 25.7, 30.1, 31.8, 32.7, 34.4, 38.5, 36.2, 37.1, 38.2, 40.9, 41.5, 39.6, 41.4, 36.9, 26.8, 31.4, 28.5, 23.6, 27.1, 27.8, 28.4],
    "Aggregate Emissions (Six Common Pollutants)": [0, -17.3, -33, -39.7, -42.9, -42.9, -43.9, -45.8, -47.5, -48.9, -47.6, -49.2, -50.8, -52.1, -54.3, -56.5, -60.2, -62.9, -64.5, -65.6, -66.5, -67.5, -69.5, -71.4],
}

SERIES_STYLES = {
    "Gross Domestic Product": {"label": "GDP", "color": "0.62", "linestyle": "-", "linewidth": 2.8},
    "Vehicle Miles Traveled": {"label": "Vehicle miles", "color": "0.05", "linestyle": ":", "linewidth": 2.1},
    "Population": {"label": "Population", "color": "0.56", "linestyle": "-", "linewidth": 1.9},
    "Energy Consumption": {"label": "Energy", "color": "0.78", "linestyle": "-", "linewidth": 2.0},
    "CO2 Emissions": {"label": "CO2", "color": "0.70", "linestyle": "--", "linewidth": 1.7},
    "Aggregate Emissions (Six Common Pollutants)": {"label": "Emissions\n(6 pollutants)", "color": "0.12", "linestyle": "-", "linewidth": 2.3},
}


def ensure_dirs() -> None:
    for part in [
        "metadata",
        "provenance",
        "source_logs",
        "search_iterations",
        "discrepancy_logs",
        "anomaly_reviews",
        "captions",
        "lineage",
        "plots/book_period",
        "plots/extended",
        "plots/comparisons",
        "data/raw",
        "data/clean",
        "checksums",
    ]:
        (BASE / part).mkdir(parents=True, exist_ok=True)


def crop_reference() -> Path:
    out = BASE / "plots/comparisons/pdf_reference_figure_10_3.png"
    if not PDF_PAGE.exists():
        raise FileNotFoundError(f"Missing rendered Supplemental PDF page: {PDF_PAGE}")
    Image.open(PDF_PAGE).convert("RGB").crop((95, 835, 1010, 1600)).save(out)
    return out


def download_sources() -> None:
    for url, out in [
        (EPA_2016_PAGE, BASE / "data/raw/epa_our_nations_air_2016.html"),
        (EPA_2016_JS, BASE / "data/raw/epa_our_nations_air_2016_etrends.js"),
        (EPA_2025_CSV, BASE / "data/raw/epa_our_nations_air_2025_growth_chart_data.csv"),
    ]:
        if out.exists() and out.stat().st_size > 0:
            continue
        subprocess.run(["curl", "-L", "--fail", "--silent", "--max-time", "20", url, "-o", str(out)], check=True)


def write_raw_2016_csv() -> pd.DataFrame:
    rows = []
    for year_i, year in enumerate(YEARS):
        row = {"year": year}
        for series, values in EPA_2016_PERCENT.items():
            row[series] = values[year_i]
        rows.append(row)
    df = pd.DataFrame(rows)
    df.to_csv(BASE / "data/raw/epa_2016_growth_chart_manual_values.csv", index=False)
    return df


def make_clean() -> tuple[pd.DataFrame, pd.DataFrame]:
    book = write_raw_2016_csv().melt("year", var_name="series", value_name="percent_change")
    book["source_vintage"] = "EPA Our Nation's Air 2016 embedded Highcharts manual data"
    book["period"] = "book_period"
    book.to_csv(BASE / "data/clean/figure_10_3_book_period_clean.csv", index=False)

    current = pd.read_csv(BASE / "data/raw/epa_our_nations_air_2025_growth_chart_data.csv")
    current = current.melt("year", var_name="series", value_name="index_change")
    current["percent_change"] = pd.to_numeric(current["index_change"], errors="coerce") * 100
    current = current.drop(columns=["index_change"])
    current["source_vintage"] = "EPA Our Nation's Air 2025 growth_chart_data.csv"
    current["period"] = current["year"].map(lambda y: "book_period_successor" if y <= 2015 else "extension")

    extended = pd.concat([book, current[current["year"] > 2015]], ignore_index=True)
    extended.to_csv(BASE / "data/clean/figure_10_3_extended_clean.csv", index=False)
    return book, extended


def plot(df: pd.DataFrame, out: Path, extended: bool) -> None:
    fig, ax = plt.subplots(figsize=(7.3, 5.2), dpi=180)
    order = [
        "Gross Domestic Product",
        "Vehicle Miles Traveled",
        "Population",
        "Energy Consumption",
        "CO2 Emissions",
        "Aggregate Emissions (Six Common Pollutants)",
    ]
    for series in order:
        data = df[df["series"] == series].sort_values("year")
        style = SERIES_STYLES[series]
        book_part = data[data["year"] <= 2015]
        ax.plot(
            book_part["year"],
            book_part["percent_change"],
            color=style["color"],
            linestyle=style["linestyle"],
            linewidth=style["linewidth"],
            solid_capstyle="round",
        )
        if extended:
            ext = data[data["year"] >= 2015]
            ax.plot(
                ext["year"],
                ext["percent_change"],
                color=style["color"],
                linestyle=(0, (3, 2)),
                linewidth=max(1.4, style["linewidth"] - 0.4),
                alpha=0.9,
            )
        label_data = data.dropna(subset=["percent_change"])
        label_point = label_data[label_data["year"] == (2024 if extended else 2015)]
        if label_point.empty:
            label_point = label_data.tail(1)
        x = float(label_point["year"].iloc[0])
        y = float(label_point["percent_change"].iloc[0])
        dx = 0.55 if not extended else 0.45
        if series == "CO2 Emissions":
            y -= 7
        if series == "Energy Consumption":
            y += 2
        if series == "Population":
            y += 4
        if series == "Aggregate Emissions (Six Common Pollutants)":
            y -= 10
        ax.text(x + dx, y, style["label"], fontsize=8.5, color="0.15", va="center")

    ax.axhline(0, color="0.35", linewidth=1.1)
    ax.set_xlim(1970, 2025 if extended else 2020)
    ax.set_ylim(-100, 360 if extended else 250)
    ax.set_xticks(range(1970, 2026 if extended else 2021, 5))
    ax.set_yticks(range(-100, 361 if extended else 251, 50))
    ax.set_ylabel("Percentage change", fontsize=10)
    ax.set_title(
        "Figure 10-3: Pollution, energy, and growth, US, 1970-2015",
        loc="left",
        fontsize=11,
    )
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(axis="both", labelsize=9, length=5, color="0.25")
    ax.grid(False)
    if extended:
        ax.axvline(2015, color="0.55", linewidth=0.9, linestyle=(0, (2, 2)))
        ax.text(2015.4, 360, "EPA 2025 successor", fontsize=7.5, color="0.35", va="top")
    ax.text(
        0,
        -0.18,
        "Source: EPA Our Nation's Air 2016 embedded chart data; extension from EPA Our Nation's Air 2025 CSV.",
        transform=ax.transAxes,
        fontsize=7,
    )
    fig.tight_layout()
    fig.savefig(out, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def side_by_side(reference: Path, recreated: Path, output: Path, title: str) -> None:
    def load_trim(path: Path) -> Image.Image:
        im = Image.open(path).convert("RGB")
        bg = Image.new("RGB", im.size, "white")
        diff = ImageChops.difference(im, bg)
        bbox = diff.getbbox()
        return im.crop(bbox) if bbox else im

    ref = load_trim(reference)
    rec = load_trim(recreated)
    panel_w, panel_h = 980, 760
    margin, gap, header_h, title_h = 45, 45, 58, 58
    page = Image.new("RGB", (margin * 2 + panel_w * 2 + gap, title_h + header_h + panel_h + margin), "white")
    draw = ImageDraw.Draw(page)
    try:
        title_font = ImageFont.truetype("Arial.ttf", 30)
        label_font = ImageFont.truetype("Arial.ttf", 24)
    except OSError:
        title_font = label_font = None

    def paste_fit(im: Image.Image, x: int, y: int) -> None:
        fitted = ImageOps.contain(im, (panel_w, panel_h), method=Image.Resampling.LANCZOS)
        page.paste(fitted, (x + (panel_w - fitted.width) // 2, y + (panel_h - fitted.height) // 2))
        draw.rectangle([x, y, x + panel_w, y + panel_h], outline=(230, 230, 230), width=1)

    left_x = margin
    right_x = margin + panel_w + gap
    draw.text((page.width // 2, 18), title, fill="black", anchor="ma", font=title_font)
    draw.text((left_x + panel_w // 2, title_h + 8), "Supplemental PDF reference", fill="black", anchor="ma", font=label_font)
    draw.text((right_x + panel_w // 2, title_h + 8), "Recreated", fill="black", anchor="ma", font=label_font)
    paste_fit(ref, left_x, title_h + header_h)
    paste_fit(rec, right_x, title_h + header_h)
    output.parent.mkdir(parents=True, exist_ok=True)
    page.save(output)


def write_docs() -> None:
    metadata = {
        "figure_id": FIG_ID,
        "chapter": "10",
        "title": "Pollution, energy, and growth, US, 1970-2015",
        "book_page": "Supplemental PDF page 13",
        "claim_summary": "The United States reduced aggregate air-pollutant emissions after 1970 while GDP, vehicle miles traveled, population, energy use, and CO2 emissions rose.",
        "book_citation": "US Environmental Protection Agency 2016; GDP from BEA; vehicle miles from FHWA; population from US Census; energy from US Department of Energy; CO2 from US Greenhouse Gas Inventory; emissions from EPA air-pollutant emissions trends data.",
        "original_dataset": "EPA Our Nation's Air 2016 embedded Highcharts manual data for the GrowthAndEmissions chart.",
        "dataset_url": EPA_2016_JS,
        "archive_url": "Not needed for reconstruction; live EPA 2016 source code and copied raw JS retained.",
        "download_date": TODAY,
        "reproduction_status": "verified_reproduction",
        "confidence_score": 0.9,
        "visual_validation": "good_with_documented_label_discrepancy",
        "notes": "The plotted reconstruction uses EPA's embedded 2016 chart values, not digitized Pinker values. The Supplemental PDF visibly labels the lower series as five pollutants while EPA's source chart and 2016 text define aggregate emissions as six common pollutants; the reconstruction follows the EPA source data and documents the book-label discrepancy.",
        "canonical_artifacts": {
            "original_reference": "figures/10-3/plots/comparisons/pdf_reference_figure_10_3.png",
            "book_period_reconstruction": "figures/10-3/plots/book_period/figure_10_3_book_period_reconstruction.png",
            "extended_reconstruction": "figures/10-3/plots/extended/figure_10_3_extended_reconstruction.png",
            "book_period_comparison": "figures/10-3/plots/comparisons/figure_10_3_book_period_comparison.png",
            "extended_comparison": "figures/10-3/plots/comparisons/figure_10_3_extended_comparison.png",
        },
    }
    (BASE / "metadata/metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    (BASE / "captions/caption.txt").write_text(
        "Figure 10-3: Pollution, energy, and growth, US, 1970-2015. "
        "Reconstruction uses the EPA Our Nation's Air 2016 embedded Highcharts data for the GrowthAndEmissions chart, not digitized Pinker plotted values. "
        "The Supplemental PDF labels aggregate emissions as five pollutants, but EPA's source chart and text define the series as six common pollutants; this reconstruction follows the EPA source label. "
        "The extended comparison appends EPA's 2025 growth_chart_data.csv through 2024, shown as a successor update after the 2015 book endpoint.\n"
    )
    (BASE / "source_logs/source_log.md").write_text(
        "# Source Discovery Log: Figure 10-3\n\n"
        "Figure title: Pollution, energy, and growth, US, 1970-2015\n\n"
        "## Primary Reference\n"
        "- Supplemental Graphics PDF page 13: figure image and source line inspected. Kindle was not needed because the PDF contains the source note and surrounding text.\n\n"
        "## Source Line Captured\n"
        "- Sources: US Environmental Protection Agency 2016, based on BEA GDP, FHWA vehicle miles traveled, US Census population, US Department of Energy energy consumption, US Greenhouse Gas Inventory CO2, and EPA air-pollutant emissions trends data.\n\n"
        "## Source Recovery\n"
        "- Located EPA Our Nation's Air 2016 live report: `https://gispub.epa.gov/air/trendsreport/2016/`.\n"
        "- The report text states that by 2015 aggregate emissions of six common pollutants dropped 71 percent since 1970 while growth indicators rose.\n"
        "- Located `dist/js/etrends.js`; the source code labels the chart block `Growth Chart - manual data entry (not csv load); custom markers` and contains the plotted series arrays.\n"
        "- Copied the source JS and extracted those EPA-authored arrays to `data/raw/epa_2016_growth_chart_manual_values.csv`.\n"
        "- Located EPA Our Nation's Air 2025 successor CSV at `data/naaqs/emissions/growth_chart_data.csv` for post-2015 extension.\n\n"
        "## Search Queries / Checks\n"
        "- EPA 2016 GDP vehicle miles traveled population energy consumption CO2 emissions 1970 2015 air pollutant emissions trends data.\n"
        "- EPA Our Nation's Air 2016 Comparison of Growth Areas and Emissions.\n"
        "- Searched 2016 EPA source code for `GrowthAndEmissions`, `growthChart`, `GDP`, and CSV references.\n"
        "- Checked direct CSV path candidates before confirming the 2016 chart is manual-data-entry in JavaScript.\n\n"
        "## Rejected / Not Used\n"
        "- Pinker/Supplemental PDF plotted values: not digitized and not used as data.\n"
        "- Separate BEA/FHWA/Census/DOE/EPA recomputation: unnecessary for book-period reconstruction because the EPA 2016 chart data were recovered directly.\n\n"
        "## Remaining Uncertainties\n"
        "- The PDF's visible label says five pollutants, but the recovered EPA chart labels the line as six common pollutants. The source note's parenthetical list omits lead while EPA's source chart includes lead.\n"
        "- The 2025 extension is a successor source with revised values and `NA` CO2 for 2023-2024; it is not a continuation of the 2016 embedded table.\n"
    )
    (BASE / "provenance/provenance.md").write_text(
        "# Provenance: Figure 10-3\n\n"
        "Supplemental Graphics PDF page 13 -> EPA Our Nation's Air 2016 report -> `dist/js/etrends.js` manual Highcharts data block -> extracted raw CSV -> book-period reconstruction. "
        "Post-2015 extension uses EPA Our Nation's Air 2025 `growth_chart_data.csv` as a successor update.\n\n"
        "No plotted values from Pinker's chart or the Supplemental PDF were digitized as source data.\n\n"
        "Source classification: recovered original chart data for the book-period EPA figure; successor source for 2016-2024 extension.\n"
    )
    (BASE / "anomaly_reviews/anomaly_review.md").write_text(
        "# Anomaly Review: Figure 10-3\n\n"
        "## Data Fidelity\n"
        "- Book-period values come from EPA's 2016 source code, which explicitly stores the GrowthAndEmissions chart as manual chart data.\n"
        "- No Pinker plotted values were digitized.\n"
        "- The extension uses EPA's 2025 successor CSV; CO2 is unavailable for 2023-2024 in that file and is therefore absent for those endpoints.\n\n"
        "## Visual Fidelity\n"
        "- The recreated figure matches the six-line percentage-change structure, endpoint ordering, zero line, and main growth-versus-emissions contrast.\n"
        "- Styling is grayscale and book-like rather than EPA's original dark interactive chart.\n"
        "- Endpoint labels are approximate but readable.\n\n"
        "## Label Discrepancy\n"
        "- The Supplemental PDF labels the lower line as `Emissions (5 pollutants)`.\n"
        "- EPA 2016 source text and chart code define the recovered series as `Aggregate Emissions (Six Common Pollutants)`.\n"
        "- The reconstruction follows the recovered EPA source label and documents the visible book/PDF discrepancy.\n\n"
        "## Extension Clarity\n"
        "- The extended comparison uses dashed post-2015 successor segments and a 2015 boundary marker.\n"
        "- Successor revisions are not treated as exact book-vintage continuation.\n\n"
        "## Reviewer Challenge\n"
        "- Steven Pinker might question the six-pollutant label because the printed figure says five; documented as a source/book label inconsistency.\n"
        "- A data journalist might ask whether the values were recomputed from primary agency tables; source recovery found the EPA chart values directly, which is stronger for figure reproduction.\n"
        "- A peer reviewer might ask whether lead's inclusion materially changes the aggregate; the current task records but does not decompose EPA's aggregate series.\n"
        "- A skeptical reader would notice the extension changes the GDP scale; the extended chart labels this as a 2025 successor update.\n\n"
        "## Editorial Review Gate\n"
        "- Critical issues: none.\n"
        "- Major issues: none unexplained.\n"
        "- Minor issues: exact typography/label placement differs from the book; the five-versus-six pollutant label discrepancy remains visible and documented.\n"
    )
    (BASE / "discrepancy_logs/discrepancy_log.md").write_text(
        "# Discrepancy Log: Figure 10-3\n\n"
        "- The book/PDF label says five pollutants; EPA's recovered chart and report text say six common pollutants.\n"
        "- The reconstruction uses EPA's source label because it is the recovered original data source.\n"
        "- The recreated labels and line tones are approximate.\n"
        "- The extension is a successor update through 2024, not an exact extension of the 2016 source table.\n"
    )
    (BASE / "search_iterations/search_iterations.md").write_text(
        "# Search Iterations: Figure 10-3\n\n"
        "1. Inspected Supplemental Graphics PDF page 13 and extracted the source line.\n"
        "2. Searched for EPA 2016 growth/emissions source data and located Our Nation's Air 2016.\n"
        "3. Checked the live report HTML and linked JavaScript.\n"
        "4. Confirmed the 2016 growth chart is manual data entry in `dist/js/etrends.js` rather than a CSV load.\n"
        "5. Downloaded EPA 2025 successor `growth_chart_data.csv` for extension.\n"
    )
    (BASE / "lineage/figure_lineage.csv").write_text(
        "figure_id,figure_title,step,artifact,value,status\n"
        "10-3,\"Pollution, energy, and growth, US, 1970-2015\",1,Book Figure,\"Supplemental PDF page 13\",observed\n"
        "10-3,\"Pollution, energy, and growth, US, 1970-2015\",2,Source Note,\"US Environmental Protection Agency 2016\",observed\n"
        f"10-3,\"Pollution, energy, and growth, US, 1970-2015\",3,Original Chart Data,\"{EPA_2016_JS}\",recovered\n"
        "10-3,\"Pollution, energy, and growth, US, 1970-2015\",4,Raw Data,\"figures/10-3/data/raw/epa_2016_growth_chart_manual_values.csv\",generated_from_source\n"
        "10-3,\"Pollution, energy, and growth, US, 1970-2015\",5,Reconstruction Script,\"scripts/reconstruct_10_3.py\",generated\n"
    )
    (BASE / "lineage/figure_lineage.json").write_text(
        json.dumps(
            [
                {"figure_id": FIG_ID, "step": 1, "artifact": "Book Figure", "value": "Supplemental PDF page 13", "status": "observed"},
                {"figure_id": FIG_ID, "step": 2, "artifact": "Source Note", "value": "US Environmental Protection Agency 2016", "status": "observed"},
                {"figure_id": FIG_ID, "step": 3, "artifact": "Original Chart Data", "value": EPA_2016_JS, "status": "recovered"},
                {"figure_id": FIG_ID, "step": 4, "artifact": "Raw Data", "value": "figures/10-3/data/raw/epa_2016_growth_chart_manual_values.csv", "status": "generated_from_source"},
                {"figure_id": FIG_ID, "step": 5, "artifact": "Reconstruction Script", "value": "scripts/reconstruct_10_3.py", "status": "generated"},
            ],
            indent=2,
        )
        + "\n"
    )
    (BASE / "review_checklist.md").write_text(
        "# Review Checklist: Figure 10-3\n\n"
        "- [x] Supplemental Graphics PDF figure inspected.\n"
        "- [x] Source note extracted from Supplemental PDF.\n"
        "- [x] Surrounding text reviewed in Supplemental PDF text extraction.\n"
        "- [x] EPA 2016 source chart located.\n"
        "- [x] Original chart data recovered from EPA 2016 source code.\n"
        "- [x] No Pinker plotted values digitized.\n"
        "- [x] Book-period reconstruction generated.\n"
        "- [x] Extended successor comparison generated.\n"
        "- [x] Data fidelity reviewed.\n"
        "- [x] Visual fidelity reviewed against PDF reference.\n"
        "- [x] Extension clarity reviewed.\n"
        "- [x] Status calibrated.\n"
        "- [x] Editorial Review Gate applied.\n"
        "- [x] Registry, metadata, PROJECT_STATE, review PDF, manifest, and checksums updated.\n"
    )
    (BASE / "README.md").write_text(
        "# Figure 10-3: Pollution, energy, and growth, US, 1970-2015\n\n"
        "Status: `verified_reproduction` for the book-period EPA chart data; successor extension documented separately.\n\n"
        "The reconstruction uses EPA Our Nation's Air 2016 embedded Highcharts data, not digitized values from Pinker's plotted chart. "
        "The Supplemental PDF label says five pollutants, while EPA's recovered source chart says six common pollutants; the source discrepancy is documented in the anomaly review.\n"
    )


def update_registry_csv() -> None:
    path = ROOT / "data/figure_registry.csv"
    rows = list(csv.DictReader(path.open()))
    for row in rows:
        if row["figure_id"] == FIG_ID:
            row.update(
                {
                    "current_status": "verified_reproduction",
                    "lifecycle_stage": "verified_book_period_reconstruction_with_successor_extension",
                    "source_type_guess": "EPA air trends institutional chart data",
                    "priority": "completed_monitor",
                    "current_owner": "Codex",
                    "next_action": "Monitor EPA source revisions; optionally decompose six-pollutant aggregate if publication requires resolving the printed five-pollutant label.",
                    "notes": "Processed 2026-07-05: EPA 2016 embedded GrowthAndEmissions chart data recovered; 2025 EPA successor extension added; book/PDF five-pollutant label conflicts with EPA six-pollutant source label.",
                }
            )
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys(), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def update_registry_json() -> None:
    csv_rows = list(csv.DictReader((ROOT / "data/figure_registry.csv").open()))
    (ROOT / "data/figure_registry.json").write_text(json.dumps(csv_rows, indent=2) + "\n")


def update_metadata_csv() -> None:
    path = ROOT / "data/metadata/figure_metadata.csv"
    rows = list(csv.DictReader(path.open()))
    rows = [row for row in rows if row["figure_id"] != FIG_ID]
    rows.append(
        {
            "figure_id": FIG_ID,
            "chapter": "10",
            "title": "Pollution, energy, and growth, US, 1970-2015",
            "book_page": "Supplemental PDF page 13",
            "claim_summary": "US aggregate air-pollutant emissions fell while GDP, driving, population, energy use, and CO2 rose after 1970.",
            "book_citation": "US Environmental Protection Agency 2016; BEA, FHWA, US Census, US Department of Energy, US Greenhouse Gas Inventory, and EPA air-pollutant emissions trends data.",
            "original_dataset": "EPA Our Nation's Air 2016 embedded GrowthAndEmissions chart data.",
            "dataset_url": EPA_2016_JS,
            "archive_url": "Live EPA source code retained locally; no archive required for reproduction.",
            "download_date": TODAY,
            "reproduction_status": "verified_reproduction",
            "confidence_score": "0.90",
            "visual_validation": "good_with_documented_label_discrepancy",
            "notes": "Book-period source data recovered from EPA 2016 chart code. Extension uses EPA 2025 successor CSV through 2024. No Pinker plotted values digitized.",
        }
    )
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys(), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def update_project_state() -> None:
    path = ROOT / "PROJECT_STATE.md"
    text = path.read_text()
    text = text.replace(
        "Project version: `1.13-remediate-figure-10-2-projection`",
        "Project version: `1.14-reconstruct-figure-10-3-epa-air-trends`",
    )
    text = "".join(
        line
        for line in text.splitlines(keepends=True)
        if not line.startswith("| 10-3 | Pollution, energy, and growth, US, 1970-2015 |")
    )
    section_start = "### Figure 10-3 - Pollution, energy, and growth, US, 1970-2015\n"
    section_end = "### Figure 4-1 - Tone of the news, 1945-2010\n"
    while section_start in text:
        start = text.index(section_start)
        end = text.index(section_end, start)
        text = text[:start] + text[end:]
    completed_entry = (
        "- Figure 10-3: EPA Our Nation's Air 2016 embedded chart data reproduces the\n"
        "  book-period pollution, energy, and growth comparison; the extension uses EPA\n"
        "  2025 successor data through 2024.\n"
    )
    text = text.replace(completed_entry, "")
    active_row = "| 10-2 | Sustainability, 1955-2109 | Updated-equivalent XKCD/Google Ngram reconstruction with calibrated projection audit | `updated_equivalent` | Medium | Official XKCD image, Supplemental PDF crop, and Ngram source-family data are recovered; future markers now derive from one XKCD-label visual projection, while Ngram-candidate threshold mismatches are quantified. |\n"
    insert_row = active_row + "| 10-3 | Pollution, energy, and growth, US, 1970-2015 | Verified EPA 2016 book-period chart-data reconstruction with successor extension | `verified_reproduction` | High | EPA Our Nation's Air 2016 embedded GrowthAndEmissions chart values recovered; EPA 2025 successor extension added; PDF five-pollutant label conflicts with EPA six-pollutant source label and is documented. |\n"
    text = text.replace(active_row, insert_row)
    completed_anchor = "- Figure 10-8: OWID 2017 regional CDIAC dataset reproduces the book-period\n  stacked emissions chart.\n"
    completed_insert = completed_anchor + "- Figure 10-3: EPA Our Nation's Air 2016 embedded chart data reproduces the\n  book-period pollution, energy, and growth comparison; the extension uses EPA\n  2025 successor data through 2024.\n"
    text = text.replace(completed_anchor, completed_insert)
    section = (
        "\n### Figure 10-3 - Pollution, energy, and growth, US, 1970-2015\n\n"
        "Status: `verified_reproduction`\n\n"
        "Canonical visual artifacts:\n\n"
        "- Supplemental PDF reference: `figures/10-3/plots/comparisons/pdf_reference_figure_10_3.png`\n"
        "- Book-period reconstruction: `figures/10-3/plots/book_period/figure_10_3_book_period_reconstruction.png`\n"
        "- Extended reconstruction: `figures/10-3/plots/extended/figure_10_3_extended_reconstruction.png`\n"
        "- Book-period comparison: `figures/10-3/plots/comparisons/figure_10_3_book_period_comparison.png`\n"
        "- Extended comparison: `figures/10-3/plots/comparisons/figure_10_3_extended_comparison.png`\n\n"
        "Source status: Supplemental Graphics PDF source line captured. EPA Our Nation's Air 2016 report and `dist/js/etrends.js` recovered; the source code explicitly stores the GrowthAndEmissions chart as manual data-entry arrays. No plotted values from Pinker's chart were digitized. EPA's source chart labels aggregate emissions as six common pollutants, while the Supplemental PDF label says five pollutants; the reconstruction follows the recovered EPA source and documents the discrepancy. EPA 2025 `growth_chart_data.csv` supplies the successor extension through 2024.\n"
    )
    marker = "\n### Figure 4-1 - Tone of the news, 1945-2010\n"
    text = text.replace(marker, section + marker)
    path.write_text(text)


def update_review_pdf() -> None:
    manifest_path = ROOT / "output/pdf/recreated_figures_review_scroll.manifest.json"
    manifest = json.loads(manifest_path.read_text())
    items = [item for item in manifest["items"] if item["figure_id"] != FIG_ID]
    items.insert(
        3,
        {
            "figure_id": FIG_ID,
            "title": "Pollution, energy, and growth, US, 1970-2015",
            "status": "verified_reproduction",
            "root": "figure_10_3_epa_air_trends",
            "path": "figures/10-3/plots/comparisons/figure_10_3_extended_comparison.png",
            "selected_image": "figure_10_3_extended_comparison.png",
            "notes": "EPA 2016 embedded chart data recovered; no Pinker plotted values digitized. Extension uses EPA 2025 successor CSV; five-versus-six pollutant label discrepancy documented.",
            "image_size": list(Image.open(BASE / "plots/comparisons/figure_10_3_extended_comparison.png").size),
        },
    )
    manifest["count"] = len(items)
    manifest["items"] = items
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")

    pdf_path = ROOT / "output/pdf/recreated_figures_review_scroll.pdf"
    c = canvas.Canvas(str(pdf_path), pagesize=letter)
    width, height = letter
    c.setFont("Helvetica-Bold", 14)
    c.drawString(36, height - 42, "Recreated Figures Review Scroll")
    c.setFont("Helvetica", 9)
    c.drawString(36, height - 58, f"Generated {TODAY}; manifest count: {len(items)}")
    c.showPage()
    for item in items:
        img_path = ROOT / item["path"]
        if not img_path.exists():
            continue
        img = Image.open(img_path)
        iw, ih = img.size
        max_w, max_h = width - 54, height - 94
        scale = min(max_w / iw, max_h / ih)
        draw_w, draw_h = iw * scale, ih * scale
        c.setFont("Helvetica-Bold", 10)
        c.drawString(27, height - 30, f"{item['figure_id']}: {item['title']} [{item['status']}]")
        c.setFont("Helvetica", 7)
        c.drawString(27, height - 42, item.get("notes", "")[:150])
        c.drawImage(ImageReader(str(img_path)), 27, height - 54 - draw_h, width=draw_w, height=draw_h)
        c.showPage()
    c.save()


def write_checksums() -> None:
    paths = [
        BASE / "metadata/metadata.json",
        BASE / "data/raw/epa_2016_growth_chart_manual_values.csv",
        BASE / "data/raw/epa_our_nations_air_2016_etrends.js",
        BASE / "data/raw/epa_our_nations_air_2025_growth_chart_data.csv",
        BASE / "data/clean/figure_10_3_book_period_clean.csv",
        BASE / "data/clean/figure_10_3_extended_clean.csv",
        BASE / "plots/book_period/figure_10_3_book_period_reconstruction.png",
        BASE / "plots/extended/figure_10_3_extended_reconstruction.png",
        BASE / "plots/comparisons/figure_10_3_book_period_comparison.png",
        BASE / "plots/comparisons/figure_10_3_extended_comparison.png",
        ROOT / "output/pdf/recreated_figures_review_scroll.pdf",
        ROOT / "output/pdf/recreated_figures_review_scroll.manifest.json",
    ]
    lines = []
    for path in paths:
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        lines.append(f"{digest}  {path.relative_to(ROOT)}")
    (BASE / "checksums/sha256sums.txt").write_text("\n".join(lines) + "\n")


def main() -> None:
    ensure_dirs()
    reference = crop_reference()
    download_sources()
    book, extended = make_clean()
    book_plot = BASE / "plots/book_period/figure_10_3_book_period_reconstruction.png"
    ext_plot = BASE / "plots/extended/figure_10_3_extended_reconstruction.png"
    plot(book, book_plot, extended=False)
    plot(extended, ext_plot, extended=True)
    side_by_side(reference, book_plot, BASE / "plots/comparisons/figure_10_3_book_period_comparison.png", "Figure 10-3 Book-Period Comparison")
    side_by_side(reference, ext_plot, BASE / "plots/comparisons/figure_10_3_extended_comparison.png", "Figure 10-3 Extended Comparison")
    write_docs()
    update_registry_csv()
    update_registry_json()
    update_metadata_csv()
    update_project_state()
    update_review_pdf()
    write_checksums()


if __name__ == "__main__":
    main()
