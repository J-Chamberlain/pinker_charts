from __future__ import annotations

import csv
import hashlib
import json
import re
import shutil
import urllib.request
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures" / "7-4"
RAW = FIG / "data" / "raw"
CLEAN = FIG / "data" / "clean"
PLOTS = FIG / "plots"

GOOGLE_SHEET_CSV = (
    "https://docs.google.com/spreadsheets/d/"
    "1nxOsUE9gtdi_q177Bx1JaazfI0l1M6BA7xKYFbG8IAg/export?format=csv&gid=0"
)
LIVE_DATASET_ARTICLE = "https://ourworldindata.org/the-our-world-in-data-dataset-of-famines"
WAYBACK_TOPIC_PAGE = "https://web.archive.org/web/20180103225041/https://ourworldindata.org/famines"
WAYBACK_RATE_IMAGE = (
    "https://web.archive.org/web/20180103225041im_/"
    "https://ourworldindata.org/wp-content/uploads/2017/05/Famine-death-rate-since-1860s.png"
)
ARCHIVED_SOURCE_IMAGE_VALUES = {
    1860: 301,
    1870: 1426,
    1880: 196,
    1890: 605,
    1900: 313,
    1910: 149,
    1920: 823,
    1930: 559,
    1940: 785,
    1950: 324,
    1960: 504,
    1970: 88,
    1980: 28,
    1990: 52,
    2000: 43,
    2010: 3,
}


def fetch(url: str, path: Path) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 figure-source-recovery"})
    with urllib.request.urlopen(request) as response:
        data = response.read()
    if path.suffix in {".csv", ".html"}:
        text = data.decode("utf-8", errors="replace")
        path.write_text("\n".join(line.rstrip() for line in text.splitlines()) + "\n")
    else:
        path.write_bytes(data)


def parse_float(value: str) -> float | None:
    value = value.strip().replace(",", "")
    if not value or value == "-":
        return None
    return float(value)


def load_world_population(path: Path) -> dict[int, float]:
    out: dict[int, float] = {}
    with path.open(newline="") as f:
        for row in csv.DictReader(f):
            if row["Entity"] == "World":
                out[int(row["Year"])] = float(row["Population"])
    return out


def compute_decadal_rates(events_path: Path, population_path: Path) -> list[dict[str, float | int | str]]:
    annual_deaths: dict[int, float] = defaultdict(float)
    with events_path.open(newline="") as f:
        for row in csv.DictReader(f):
            start = int(row["year_start"])
            end = int(row["year_end"])
            midpoint = parse_float(row["excess_mortality_mid"])
            if midpoint is None or midpoint < 1000:
                continue
            annual = midpoint / (end - start + 1)
            for year in range(start, end + 1):
                if 1860 <= year <= 2016:
                    annual_deaths[year] += annual

    population = load_world_population(population_path)
    rows: list[dict[str, float | int | str]] = []
    for decade in range(1860, 2020, 10):
        deaths = sum(v for year, v in annual_deaths.items() if (year // 10) * 10 == decade)
        pop = population[decade]
        rows.append(
            {
                "Year": decade,
                "decade_label": f"{decade}s" if decade < 2010 else "2010-2016",
                "allocated_famine_deaths": round(deaths, 3),
                "world_population_denominator": int(pop),
                "deaths_per_100k_per_decade": round(deaths / pop * 100000, 6),
            }
        )
    return rows


def archived_source_rows() -> list[dict[str, float | int | str]]:
    rows: list[dict[str, float | int | str]] = []
    for decade, value in ARCHIVED_SOURCE_IMAGE_VALUES.items():
        rows.append(
            {
                "Year": decade,
                "decade_label": f"{decade}s" if decade < 2010 else "2010-2016",
                "deaths_per_100k_per_decade": value,
                "value_source": "printed_label_in_archived_owid_static_source_image_20180103",
            }
        )
    return rows


def write_csv(path: Path, rows: list[dict[str, float | int | str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def plot_book_period(rows: list[dict[str, float | int | str]], path: Path) -> None:
    years = [int(r["Year"]) for r in rows]
    rates = [float(r["deaths_per_100k_per_decade"]) for r in rows]
    fig, ax = plt.subplots(figsize=(7.8, 4.9), dpi=180)
    ax.plot(years, rates, color="#252525", linewidth=2.2)
    ax.set_xlim(1858, 2020)
    ax.set_ylim(0, 1600)
    ax.set_xticks(years)
    ax.set_xticklabels([f"{y}s" if y < 2010 else "2010-\n2016" for y in years], rotation=90)
    ax.set_yticks(range(0, 1601, 200))
    ax.set_ylabel("Famine deaths per 100,000 people per decade")
    ax.set_title("Famine deaths, 1860-2016", loc="left", fontsize=13, pad=12)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(False)
    ax.tick_params(labelsize=8)
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, facecolor="white", bbox_inches="tight")
    plt.close(fig)


def trim(im: Image.Image) -> Image.Image:
    bg = Image.new("RGB", im.size, "white")
    bbox = ImageChops.difference(im.convert("RGB"), bg).getbbox()
    return im.crop(bbox) if bbox else im


def side_by_side(
    reference: Path,
    recreated: Path,
    output: Path,
    title: str,
    left: str,
    right: str = "Recreated",
) -> None:
    ref = trim(Image.open(reference).convert("RGB"))
    rec = trim(Image.open(recreated).convert("RGB"))
    panel_w, panel_h = 980, 720
    margin, gap, header_h, title_h = 45, 45, 58, 58
    canvas = Image.new("RGB", (margin * 2 + panel_w * 2 + gap, title_h + header_h + panel_h + margin), "white")
    draw = ImageDraw.Draw(canvas)
    try:
        title_font = ImageFont.truetype("Arial.ttf", 30)
        label_font = ImageFont.truetype("Arial.ttf", 24)
    except OSError:
        title_font = label_font = None

    def paste_fit(im: Image.Image, x: int, y: int) -> None:
        fitted = ImageOps.contain(im, (panel_w, panel_h), method=Image.Resampling.LANCZOS)
        canvas.paste(fitted, (x + (panel_w - fitted.width) // 2, y + (panel_h - fitted.height) // 2))
        draw.rectangle([x, y, x + panel_w, y + panel_h], outline=(230, 230, 230), width=1)

    left_x = margin
    right_x = margin + panel_w + gap
    draw.text((canvas.width // 2, 18), title, fill="black", anchor="ma", font=title_font)
    draw.text((left_x + panel_w // 2, title_h + 8), left, fill="black", anchor="ma", font=label_font)
    draw.text((right_x + panel_w // 2, title_h + 8), right, fill="black", anchor="ma", font=label_font)
    paste_fit(ref, left_x, title_h + header_h)
    paste_fit(rec, right_x, title_h + header_h)
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output)


def write_metadata(rows: list[dict[str, float | int | str]]) -> None:
    meta = {
        "figure_id": "7-4",
        "chapter": "7",
        "title": "Famine deaths, 1860-2016",
        "book_page": "Supplemental Graphics PDF page 6",
        "claim_summary": "Famine deaths per 100,000 people per decade fell sharply after the mid-twentieth century.",
        "book_citation": "Our World in Data, Hasell & Roser 2017, based on data from Devereux 2000; O Grada 2009; White 2011; EM-DAT; and other sources.",
        "reproduction_status": "partial_match",
        "confidence_score": "medium",
        "source_status": "source_family_static_source_image_labels_recovered_denominator_output_unresolved",
        "extension_status": "no_comparable_successor_extension_plotted",
        "visual_validation": "partial; archived 2018 OWID static source image with printed decadal-rate values recovered, but the underlying 2017 machine-readable rate output and denominator metadata were not recovered",
        "source_recovery": {
            "recovered": [
                "Hasell & Roser 2017 OWID article preserved at ourworldindata.org/the-our-world-in-data-dataset-of-famines",
                "Downloadable Google Sheet event table linked from the preserved OWID article",
                "2018 Wayback capture of the OWID famines topic page with the rate-chart footnote",
                "2018 Wayback capture of the static OWID chart image Famine-death-rate-since-1860s.png",
            ],
            "not_recovered": "No archived 2017 grapher CSV/config for a decadal famine-death-rate series was found; Wayback captures for the current death-rate-from-famines-by-decade grapher begin in 2025.",
        },
        "reconstruction_method": "Canonical book-period values are transcribed from the printed bar labels in the archived OWID static source image. The linked Hasell-Roser event table and archived page footnote document the source family and calculation rule.",
        "fidelity_limits": "No 2017 machine-readable decadal-rate CSV/config or exact population-denominator metadata was recovered. Recomputing from the current preserved event table with current OWID World population does not exactly match the archived static chart, so that calculation is retained only as a diagnostic proxy.",
        "transcription_audit": {
            "source_image": "figures/7-4/plots/comparisons/owid_archived_famine_death_rate_source_20180103.png",
            "method": "Exact integer decadal values were transcribed from the printed bar labels in the archived static OWID image and checked against the visible labels after zoomed visual review.",
            "expected_tolerance": "0 label units for label transcription; +/-0.5 deaths per 100,000 people per decade is the implied rounding tolerance only if comparing against unrecovered underlying continuous values.",
            "checked_values": ARCHIVED_SOURCE_IMAGE_VALUES,
        },
        "book_period_rows": len(rows),
        "canonical_artifacts": {
            "supplemental_pdf_reference_legacy_filename": "figures/7-4/plots/comparisons/kindle_reference_figure_7_4.png",
            "archived_owid_source_image": "figures/7-4/plots/comparisons/owid_archived_famine_death_rate_source_20180103.png",
            "book_period_reconstruction": "figures/7-4/plots/book_period/figure_7_4_book_period_reconstruction.png",
            "book_period_comparison": "figures/7-4/plots/comparisons/figure_7_4_book_period_comparison.png",
            "source_image_comparison": "figures/7-4/plots/comparisons/figure_7_4_archived_source_comparison.png",
            "no_successor_duplicate_clean_csv": "figures/7-4/data/clean/figure_7_4_extended_clean.csv",
            "no_successor_duplicate_reconstruction": "figures/7-4/plots/extended/figure_7_4_extended_reconstruction.png",
            "no_successor_status_comparison": "figures/7-4/plots/comparisons/figure_7_4_extended_comparison.png",
        },
        "artifact_notes": {
            "kindle_reference_figure_7_4.png": "Legacy filename retained for compatibility; the current reference crop is treated as the book/Supplemental Graphics PDF reference, not as a Kindle-only source assertion.",
            "figure_7_4_extended_clean.csv": "Book-period duplicate retained only as a no-successor status artifact. It is not a post-2016 extension.",
            "figure_7_4_extended_reconstruction.png": "Book-period duplicate retained only as a no-successor status artifact. It is not a post-2016 extension.",
            "figure_7_4_extended_comparison.png": "Status comparison showing no comparable successor extension is plotted.",
        },
    }
    (FIG / "metadata").mkdir(parents=True, exist_ok=True)
    (FIG / "metadata" / "metadata.json").write_text(json.dumps(meta, indent=2) + "\n")


def write_docs(rows: list[dict[str, float | int | str]]) -> None:
    note = (
        "Recovered the Hasell & Roser 2017 OWID famine event table, the 2018 Wayback "
        "topic-page footnote describing the decadal-rate calculation, and the archived "
        "static OWID source image with printed decadal-rate values. No archived 2017 "
        "grapher CSV/config for the decadal rate was found; recomputing from the current "
        "preserved event table with current OWID World population does not exactly match "
        "the static image, so the figure remains partial_match with medium confidence "
        "rather than verified; no comparable successor extension is plotted."
    )
    audit = (
        "Transcription audit: the canonical decadal values are exact integer label "
        "transcriptions from the archived static OWID image. Each label was checked "
        "against the visible bar label in the image after zoomed visual review. Expected "
        "tolerance is 0 label units for transcription; +/-0.5 deaths per 100,000 people "
        "per decade is only the implied rounding tolerance if comparing against the "
        "unrecovered continuous underlying rates."
    )
    extension_note = (
        "`figure_7_4_extended_clean.csv`, "
        "`plots/extended/figure_7_4_extended_reconstruction.png`, and "
        "`plots/comparisons/figure_7_4_extended_comparison.png` are retained as "
        "no-successor/book-period-duplicate status artifacts. They are not a real "
        "post-2016 extension and must not be cited as one."
    )
    naming_note = (
        "`plots/comparisons/kindle_reference_figure_7_4.png` is a legacy filename. "
        "Current documentation treats it as the book/Supplemental Graphics PDF reference "
        "crop; the filename is retained to avoid breaking existing artifact links."
    )
    (FIG / "README.md").write_text(
        "# Figure 7-4: Famine deaths, 1860-2016\n\n"
        "Status: `partial_match`.\n"
        "Confidence: `medium`.\n"
        "Source status: `source_family_static_source_image_labels_recovered_denominator_output_unresolved`.\n"
        "Extension status: `no_comparable_successor_extension_plotted`.\n\n"
        f"{note}\n\n{audit}\n\n{extension_note}\n\n{naming_note}\n"
    )
    (FIG / "provenance" / "provenance.md").write_text(
        "# Provenance: Figure 7-4\n\n"
        "Book/Supplemental Graphics PDF figure -> source note -> Hasell & Roser 2017 OWID article -> "
        "downloadable OWID famine event table -> 2018 Wayback topic-page footnote and "
        "static source image -> `scripts/reconstruct_7_4.py`.\n\n"
        "Book source note: Our World in Data, Hasell & Roser 2017, based on data from "
        "Devereux 2000; O Grada 2009; White 2011; EM-DAT; and other sources.\n\n"
        "Recovered source trail:\n\n"
        "- Supplemental Graphics PDF page 6 gives the figure title, axis label, and source note.\n"
        "- `https://ourworldindata.org/the-our-world-in-data-dataset-of-famines` preserves the "
        "Hasell & Roser article and cites the 2017 OWID dataset.\n"
        "- The article links a downloadable spreadsheet at "
        "`https://docs.google.com/spreadsheets/d/1nxOsUE9gtdi_q177Bx1JaazfI0l1M6BA7xKYFbG8IAg/`.\n"
        "- The 2018 Wayback capture of `https://ourworldindata.org/famines` contains the chart "
        "heading, chart image, and calculation footnote.\n"
        "- Wayback/CDX searches found no 2017-2018 capture of a decadal-rate grapher CSV/config; "
        "the live `death-rate-from-famines-by-decade` grapher first appears in 2025 captures and "
        "uses the World Peace Foundation successor source.\n\n"
        "Canonical book-period values are transcribed from the printed labels in the archived "
        "static OWID source image. The event-table/denominator recomputation is retained as a "
        "diagnostic because it follows the archived footnote rule but does not exactly reproduce "
        "the static image when using the current preserved event table and current OWID World "
        "population. The exact 2017 rate output and denominator vintage remain unresolved.\n"
        f"\n{audit}\n\n"
        f"{extension_note}\n\n"
        f"{naming_note}\n"
    )
    (FIG / "source_logs" / "source_log.md").write_text(
        "# Source Discovery Log: Figure 7-4\n\n"
        "- Read Supplemental Graphics PDF page 6: title `Famine deaths, 1860-2016`; y-axis "
        "`Famine deaths per 100,000 people per decade`; source note cites OWID Hasell & Roser 2017.\n"
        "- Recovered live OWID preservation page for `The Our World in Data Dataset of Famines`, "
        "which says the old dataset covers famine deaths from the 1860s through 2016 and is now "
        "outdated relative to WPF successor data.\n"
        "- Recovered the linked Google Sheet event table with parsed `year_start` and `year_end` fields.\n"
        "- Recovered 2018 Wayback page text for the original OWID famines topic page. The rate-chart "
        "footnote says to use the table, average upper/lower estimates, split straddling famines "
        "proportionately by years in each decade, and exclude missing/sub-1,000 death events.\n"
        "- Recovered the archived static chart image `Famine-death-rate-since-1860s.png`.\n"
        "- CDX searches for `death-rate-from-famines-by-decade` found captures only from 2025 onward; "
        "wildcard 2017-2018 grapher searches for famine charts found no decadal-rate grapher CSV.\n"
        "- Transcribed the printed decadal-rate values from the archived static chart image for the "
        "canonical book-period clean data.\n"
        "- Audited the transcription as exact integer label transcription from the static image; "
        "expected tolerance is 0 label units for transcription, with +/-0.5 only as the implied "
        "rounding tolerance against unrecovered continuous rates.\n"
        "- Conclusion: the original source family, calculation rules, and plotted values are recovered "
        "from the static chart, but not a machine-readable 2017 decadal-rate output with denominator metadata.\n"
    )
    (FIG / "discrepancy_logs" / "discrepancy_log.md").write_text(
        "# Discrepancy Log: Figure 7-4\n\n"
        "Status: `partial_match`\n\n"
        "The archived OWID static source image was recovered and its printed bar labels are used "
        "for the canonical book-period clean data. The remaining discrepancy is source-data "
        "recoverability: the exact 2017 machine-readable rate output and population denominator "
        "used by OWID's static chart are not exposed in the archived page or as a recovered grapher "
        "CSV/config. A recomputation from the current preserved event table and current OWID World "
        "population is retained only as a diagnostic proxy because it differs from the printed labels.\n\n"
        "The 2025 WPF/OWID grapher series is retained only as successor context and is not used as "
        "the book-period reconstruction. No comparable successor extension is plotted; the extended "
        "CSV and PNG artifacts are no-successor/book-period duplicates retained only for status "
        "compatibility.\n"
    )
    (FIG / "anomaly_reviews" / "anomaly_review.md").write_text(
        "# Anomaly Review: Figure 7-4\n\n"
        "- **Status:** `partial_match`; confidence `medium`; source status "
        "`source_family_static_source_image_labels_recovered_denominator_output_unresolved`.\n"
        "- **Source vintage:** original Hasell-Roser event table, calculation footnote, static source "
        "image, and printed plotted values recovered; 2017 decadal-rate grapher output not recovered.\n"
        "- **Data treatment:** canonical values are transcribed from the archived source image labels. "
        "The event-table/current-population recomputation is a diagnostic and does not match exactly. "
        "Transcription tolerance is 0 label units, with +/-0.5 only as implied rounding tolerance "
        "against unrecovered continuous rates.\n"
        "- **Extension:** no comparable successor extension is plotted because the available WPF 2025 successor "
        "uses a revised source family and is not comparable enough to append silently. The extended "
        "CSV/PNG artifacts are no-successor/book-period duplicates, not a real extension.\n"
        "- **Classification:** keep `partial_match`; do not call this a verified reproduction.\n"
    )
    (FIG / "review_checklist.md").write_text(
        "# Editorial Review Checklist: Figure 7-4\n\n"
        "- [x] Supplemental PDF figure/source note reviewed.\n"
        "- [x] Bibliographic source resolved to Hasell & Roser 2017 OWID article.\n"
        "- [x] Archived OWID topic page and static source image recovered.\n"
        "- [x] Source data and calculation footnote recovered.\n"
        "- [x] Reconstructed values transcribed from archived source image labels.\n"
        "- [x] Transcription audit documented with 0-label-unit expected tolerance.\n"
        "- [x] Event-table/current-denominator proxy retained as diagnostic only.\n"
        "- [x] Extended artifacts documented as no-successor/book-period duplicates, not a real extension.\n"
        "- [x] No non-comparable successor extension plotted.\n"
        "- [x] Final classification kept at `partial_match`.\n"
    )
    (FIG / "captions" / "caption.txt").write_text(
        "Figure 7-4: Famine deaths, 1860-2016. `partial_match` reconstruction from printed "
        "decadal-rate labels in the archived 2018 OWID static source image, supported by "
        "the Hasell & Roser 2017 OWID famine event table and archived chart-rule footnote. "
        "The exact 2017 OWID machine-readable decadal-rate output/denominator metadata was "
        "not recovered. Confidence is medium; no comparable successor extension is plotted. "
        "Extended artifacts are book-period duplicate status artifacts only.\n"
    )
    (FIG / "search_iterations" / "search_iterations.md").write_text(
        "# Search Iterations: Figure 7-4\n\n"
        "- Read Supplemental Graphics PDF text around Figure 7-4.\n"
        "- Opened live OWID Hasell-Roser preserved dataset article and extracted the linked Google Sheet.\n"
        "- Queried Wayback CDX for 2017-2018 OWID grapher famine slugs; no decadal-rate CSV/config found.\n"
        "- Opened 2018 Wayback capture of the OWID famines topic page and recovered the rate-chart footnote and PNG.\n"
        "- Compared the 2025 `death-rate-from-famines-by-decade` grapher metadata and excluded it from the book-period reconstruction.\n"
        "- Checked the archived static image labels as exact integer transcriptions; no post-2016 successor extension was plotted.\n"
    )
    lineage_csv = FIG / "lineage" / "figure_lineage.csv"
    lineage_csv.write_text(
        "figure_id,title,step,evidence,value,status\n"
        '7-4,"Famine deaths, 1860-2016",1,Supplemental PDF,"Figure title, y-axis label, source note",observed\n'
        '7-4,"Famine deaths, 1860-2016",2,OWID preserved article,"Hasell & Roser 2017 dataset covers 1860s-2016",recovered\n'
        '7-4,"Famine deaths, 1860-2016",3,OWID Google Sheet,"Parsed famine event table",recovered\n'
        '7-4,"Famine deaths, 1860-2016",4,Wayback 2018 topic page,"Decadal allocation footnote and static source PNG",recovered\n'
        '7-4,"Famine deaths, 1860-2016",5,Reconstruction,"Plotted values recovered from static image; denominator output unresolved",partial_match\n'
    )
    (FIG / "lineage" / "figure_lineage.json").write_text(
        json.dumps(
            [
                {"step": 1, "evidence": "Supplemental PDF", "status": "observed"},
                {"step": 2, "evidence": "OWID Hasell & Roser 2017 article", "status": "recovered"},
                {"step": 3, "evidence": "OWID Google Sheet event table", "status": "recovered"},
                {"step": 4, "evidence": "2018 Wayback topic page and PNG", "status": "recovered"},
                {"step": 5, "evidence": "printed archived static source image labels", "status": "partial_match"},
            ],
            indent=2,
        )
        + "\n"
    )


def write_checksums() -> None:
    lines = []
    for path in sorted(p for p in FIG.rglob("*") if p.is_file() and "checksums" not in p.parts):
        rel = path.relative_to(FIG)
        lines.append(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {rel}\n")
    (FIG / "checksums" / "sha256sums.txt").write_text("".join(lines))


def main() -> None:
    for path in [RAW, CLEAN, PLOTS / "book_period", PLOTS / "extended", PLOTS / "comparisons"]:
        path.mkdir(parents=True, exist_ok=True)

    fetch(GOOGLE_SHEET_CSV, RAW / "owid_hasell_roser_famine_event_table_google_sheet.csv")
    fetch(LIVE_DATASET_ARTICLE, RAW / "owid_hasell_roser_famine_article.html")
    fetch(WAYBACK_TOPIC_PAGE, RAW / "owid_famines_topic_page_wayback_20180103.html")
    fetch(WAYBACK_RATE_IMAGE, RAW / "owid_archived_famine_death_rate_source_20180103.png")
    shutil.copyfile(
        RAW / "owid_archived_famine_death_rate_source_20180103.png",
        PLOTS / "comparisons" / "owid_archived_famine_death_rate_source_20180103.png",
    )

    proxy_rows = compute_decadal_rates(
        RAW / "owid_hasell_roser_famine_event_table_google_sheet.csv",
        RAW / "owid_population.csv",
    )
    rows = archived_source_rows()
    write_csv(CLEAN / "figure_7_4_book_period_clean.csv", rows)
    # Repository convention expects an extended/status artifact. For Figure 7-4
    # this is deliberately a book-period duplicate because no comparable
    # successor extension is plotted.
    write_csv(CLEAN / "figure_7_4_extended_clean.csv", rows)
    write_csv(CLEAN / "figure_7_4_event_table_current_population_proxy.csv", proxy_rows)
    plot_book_period(rows, PLOTS / "book_period" / "figure_7_4_book_period_reconstruction.png")
    shutil.copyfile(
        PLOTS / "book_period" / "figure_7_4_book_period_reconstruction.png",
        PLOTS / "extended" / "figure_7_4_extended_reconstruction.png",
    )
    side_by_side(
        PLOTS / "comparisons" / "kindle_reference_figure_7_4.png",
        PLOTS / "book_period" / "figure_7_4_book_period_reconstruction.png",
        PLOTS / "comparisons" / "figure_7_4_book_period_comparison.png",
        "Figure 7-4 book-period comparison",
        "Book/Supplemental PDF reference",
    )
    side_by_side(
        PLOTS / "comparisons" / "owid_archived_famine_death_rate_source_20180103.png",
        PLOTS / "book_period" / "figure_7_4_book_period_reconstruction.png",
        PLOTS / "comparisons" / "figure_7_4_archived_source_comparison.png",
        "Figure 7-4 archived OWID source comparison",
        "Archived OWID 2018 source image",
    )
    side_by_side(
        PLOTS / "comparisons" / "kindle_reference_figure_7_4.png",
        PLOTS / "extended" / "figure_7_4_extended_reconstruction.png",
        PLOTS / "comparisons" / "figure_7_4_extended_comparison.png",
        "Figure 7-4 no-successor status comparison",
        "Book/Supplemental PDF reference",
        "Book-period duplicate; no successor extension",
    )
    write_metadata(rows)
    write_docs(rows)
    write_checksums()


if __name__ == "__main__":
    main()
