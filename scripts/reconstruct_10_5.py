#!/usr/bin/env python3
"""Reconstruct Figure 10-5 from recovered public source-family evidence.

The oil-spill counts are tabular ITOPF/OWID data. The oil-shipped line is
digitized from an archived ITOPF 2016 chart image because the original annual
UNCTADStat table behind Pinker's gray line has not been recovered.
"""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import textwrap
from pathlib import Path
from urllib.request import urlretrieve

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures" / "10-5"
RAW = FIG / "data" / "raw"
CANDIDATES = FIG / "data" / "candidates"
CLEAN = FIG / "data" / "clean"
BOOK = FIG / "plots" / "book_period"
EXTENDED = FIG / "plots" / "extended"
COMPARISONS = FIG / "plots" / "comparisons"
DIAGNOSTICS = FIG / "plots" / "diagnostics"
CHECKSUMS = FIG / "checksums"

ITOPF_ARCHIVE_PAGE = (
    "https://web.archive.org/web/20170119015939/"
    "http://www.itopf.com:80/knowledge-resources/data-statistics/statistics/"
)
ITOPF_SEABORNE_IMAGE = (
    "https://web.archive.org/web/20170119015939im_/"
    "http://www.itopf.com/fileadmin/data/Photos/Statistics/seaborne_16.JPG"
)
ITOPF_2017_STATS_PDF = (
    "https://tcrsudestuairemoyen.org/wp-content/uploads/2018/12/"
    "oil_spill_stats_2017.pdf"
)


def ensure_dirs() -> None:
    for path in [RAW, CANDIDATES, CLEAN, BOOK, EXTENDED, COMPARISONS, DIAGNOSTICS, CHECKSUMS]:
        path.mkdir(parents=True, exist_ok=True)


def download(url: str, path: Path) -> None:
    if not path.exists() or path.stat().st_size == 0:
        urlretrieve(url, path)


def capture_text_pdf(pdf_path: Path, txt_path: Path) -> None:
    if txt_path.exists() and txt_path.stat().st_size:
        return
    result = subprocess.run(["pdftotext", str(pdf_path), "-"], check=True, capture_output=True, text=True)
    txt_path.write_text(result.stdout, encoding="utf-8")


def load_spills_robust() -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    with (RAW / "owid_number_oil_spills.csv").open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        medium_col = next(col for col in reader.fieldnames or [] if col.startswith("Medium oil spills"))
        large_col = next(col for col in reader.fieldnames or [] if col.startswith("Large oil spills"))
        for row in reader:
            if row["Entity"] != "World":
                continue
            year = int(row["Year"])
            if 1970 <= year <= 2016:
                large = int(float(row[large_col]))
                medium = int(float(row[medium_col]))
                rows.append(
                    {
                        "year": year,
                        "large_spills_gt_700_tonnes": large,
                        "medium_spills_7_to_700_tonnes": medium,
                        "oil_spills_7_plus_tonnes": large + medium,
                    }
                )
    return rows


def digitize_itopf_oil_line(image_path: Path) -> list[dict[str, float | str]]:
    image = Image.open(image_path).convert("RGB")
    arr = np.array(image)
    mask = (
        (arr[:, :, 2] > 60)
        & (arr[:, :, 0] < 90)
        & (arr[:, :, 1] < 130)
        & ((arr[:, :, 2] - arr[:, :, 1]) > 8)
        & ((arr[:, :, 2] - arr[:, :, 0]) > 20)
    )
    ys, xs = np.where(mask)

    # Calibrated from the printed plot area in seaborne_16.JPG.
    x_left, x_right = 50.0, 559.0
    y_zero, y_top = 344.0, 70.0
    rows: list[dict[str, float | str]] = []
    for year in range(1970, 2017):
        x_center = x_left + (year - 1970) * (x_right - x_left) / (2016 - 1970)
        hits = (np.abs(xs - x_center) <= 3) & (ys >= y_top) & (ys <= y_zero)
        if not hits.any():
            hits = (np.abs(xs - x_center) <= 5) & (ys >= y_top) & (ys <= y_zero)
        if not hits.any():
            value = ""
        else:
            y = float(np.median(ys[hits]))
            value = round((y_zero - y) / (y_zero - y_top) * 3.5, 3)
        rows.append(
            {
                "year": year,
                "digitized_oil_loaded_billion_metric_tons": value,
                "source_image": "Wayback 2017-01-19 ITOPF seaborne_16.JPG",
                "calibration_note": "Image-derived diagnostic; x 1970-2016, y 0-3500 million metric tons",
            }
        )
    return rows


def write_csv(path: Path, rows: list[dict[str, float | str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def load_digitized() -> list[dict[str, float]]:
    path = CANDIDATES / "itopf_archived_seaborne_16_digitized_oil_loaded.csv"
    rows = []
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            rows.append(
                {
                    "year": int(row["year"]),
                    "digitized_oil_loaded_billion_metric_tons": float(row["digitized_oil_loaded_billion_metric_tons"]),
                }
            )
    return rows


def write_selected_year_validation(oil: list[dict[str, float]]) -> tuple[float, float]:
    rmt_path = CANDIDATES / "unctad_rmt2020_tanker_trade_selected_years.csv"
    if not rmt_path.exists():
        return 0.0, 0.0
    rmt: dict[int, float] = {}
    with rmt_path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            rmt[int(row["year"])] = float(row["tanker_trade_million_tons"]) / 1000.0
    oil_by_year = {int(row["year"]): float(row["digitized_oil_loaded_billion_metric_tons"]) for row in oil}
    rows = []
    diffs = []
    for year in sorted(set(rmt).intersection(oil_by_year)):
        diff = oil_by_year[year] - rmt[year]
        diffs.append(abs(diff))
        rows.append(
            {
                "year": year,
                "itopf_image_digitized_billion_metric_tons": round(oil_by_year[year], 3),
                "unctad_rmt2020_selected_year_billion_metric_tons": round(rmt[year], 3),
                "difference_billion_metric_tons": round(diff, 3),
            }
        )
    if rows:
        write_csv(CANDIDATES / "itopf_digitized_vs_unctad_rmt2020_selected_year_validation.csv", rows)
    return (sum(diffs) / len(diffs), max(diffs)) if diffs else (0.0, 0.0)


def plot_book(spills: list[dict[str, float]], oil: list[dict[str, float]]) -> Path:
    years = [row["year"] for row in spills]
    spill_values = [row["oil_spills_7_plus_tonnes"] for row in spills]
    oil_years = [row["year"] for row in oil]
    oil_values = [row["digitized_oil_loaded_billion_metric_tons"] for row in oil]

    fig, ax = plt.subplots(figsize=(8.1, 5.0), dpi=180)
    ax.plot(years, spill_values, color="#111111", linewidth=2.6)
    ax.set_xlim(1970, 2020)
    ax.set_ylim(0, 125)
    ax.set_xticks([1970, 1975, 1980, 1985, 1990, 1995, 2000, 2005, 2010, 2015, 2020])
    ax.set_yticks([0, 25, 50, 75, 100, 125])
    ax.set_ylabel("Number of oil spills")
    ax.grid(False)
    for side in ["top"]:
        ax.spines[side].set_visible(False)
    for side in ["left", "bottom"]:
        ax.spines[side].set_color("#666666")

    ax2 = ax.twinx()
    ax2.plot(oil_years, oil_values, color="#a8a8a8", linewidth=2.6)
    ax2.set_ylim(1.4, 3.0)
    ax2.set_yticks([1.4, 1.8, 2.2, 2.6, 3.0])
    ax2.set_ylabel("Billion metric tons")
    ax2.grid(False)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_color("#666666")

    ax2.text(2007.0, 2.53, "Oil shipped by sea", color="#444444", fontsize=10)
    ax.text(2008.2, 15.5, "Oil spills", color="#111111", fontsize=10)
    fig.text(
        0.01,
        0.01,
        "Sources: ITOPF/OWID spill counts; oil-loaded line digitized from archived ITOPF/UNCTADStat chart image.",
        ha="left",
        va="bottom",
        fontsize=7.5,
        color="#555555",
    )
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    out = BOOK / "figure_10_5_book_period_reconstruction.png"
    fig.savefig(out)
    plt.close(fig)
    return out


def make_status_panel() -> Path:
    out = EXTENDED / "figure_10_5_extended_reconstruction.png"
    image = Image.new("RGB", (1450, 850), "white")
    draw = ImageDraw.Draw(image)
    try:
        title_font = ImageFont.truetype("Arial.ttf", 44)
        body_font = ImageFont.truetype("Arial.ttf", 28)
    except OSError:
        title_font = ImageFont.load_default()
        body_font = ImageFont.load_default()
    draw.text((70, 70), "Figure 10-5 extension not plotted", fill="#111111", font=title_font)
    text = (
        "A same-method annual successor for the oil-shipped-by-sea line was not recovered.\n\n"
        "The book-period spill-count line is tabular ITOPF/OWID data. The oil-shipped line is an "
        "image-derived diagnostic from an archived 2016 ITOPF chart whose caption cites UNCTADStat. "
        "Because the annual UNCTADStat table behind that line remains unavailable, no post-2016 "
        "extension is shown here."
    )
    y = 170
    for paragraph in text.split("\n\n"):
        for line in textwrap.wrap(paragraph, width=78):
            draw.text((70, y), line, fill="#333333", font=body_font)
            y += 42
        y += 28
    image.save(out)
    return out


def combine_side_by_side(book_plot: Path, status_plot: Path) -> tuple[Path, Path]:
    ref = COMPARISONS / "corrected_figure_10_5_book_crop.png"
    for right, out, plain_out in [
        (
            book_plot,
            COMPARISONS / "figure_10_5_book_style_comparison_captioned.png",
            COMPARISONS / "figure_10_5_book_style_comparison.png",
        ),
        (
            status_plot,
            COMPARISONS / "figure_10_5_extended_comparison_captioned.png",
            COMPARISONS / "figure_10_5_extended_comparison.png",
        ),
    ]:
        left_img = Image.open(ref).convert("RGB")
        right_img = Image.open(right).convert("RGB")
        target_h = 680
        left_img = left_img.resize((int(left_img.width * target_h / left_img.height), target_h))
        right_img = right_img.resize((int(right_img.width * target_h / right_img.height), target_h))
        plain = Image.new("RGB", (left_img.width + right_img.width + 36, target_h), "white")
        plain.paste(left_img, (0, 0))
        plain.paste(right_img, (left_img.width + 36, 0))
        plain.save(plain_out)

        caption_h = 90
        canvas = Image.new("RGB", (left_img.width + right_img.width + 36, target_h + caption_h), "white")
        canvas.paste(left_img, (0, caption_h))
        canvas.paste(right_img, (left_img.width + 36, caption_h))
        draw = ImageDraw.Draw(canvas)
        try:
            font = ImageFont.truetype("Arial.ttf", 28)
        except OSError:
            font = ImageFont.load_default()
        draw.text((20, 25), "Book figure", fill="#111111", font=font)
        draw.text((left_img.width + 56, 25), "Run artifact", fill="#111111", font=font)
        canvas.save(out)
    return (
        COMPARISONS / "figure_10_5_book_style_comparison_captioned.png",
        COMPARISONS / "figure_10_5_extended_comparison_captioned.png",
    )


def write_checksums() -> None:
    paths = [
        *(RAW.glob("*.csv")),
        *(RAW.glob("*.json")),
        *(CANDIDATES.glob("itopf_archived*")),
        *(CANDIDATES.glob("itopf_digitized_vs_unctad*.csv")),
        *(CANDIDATES.glob("itopf_statistics_20170119_wayback.html")),
        *(CANDIDATES.glob("oil_spill_stats_2017*")),
        *(CLEAN.glob("figure_10_5*.csv")),
    ]
    with (CHECKSUMS / "sha256sums.txt").open("w", encoding="utf-8") as handle:
        for path in sorted(paths):
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            handle.write(f"{digest}  {path.relative_to(ROOT)}\n")

    plot_paths = [*BOOK.glob("*.png"), *EXTENDED.glob("*.png"), *COMPARISONS.glob("*.png"), *DIAGNOSTICS.glob("*.png")]
    with (CHECKSUMS / "plot_sha256sums.txt").open("w", encoding="utf-8") as handle:
        for path in sorted(plot_paths):
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            handle.write(f"{digest}  {path.relative_to(ROOT)}\n")


def main() -> None:
    ensure_dirs()
    image_path = CANDIDATES / "itopf_archived_seaborne_16.JPG"
    page_path = CANDIDATES / "itopf_statistics_20170119_wayback.html"
    pdf_path = CANDIDATES / "oil_spill_stats_2017.pdf"
    download(ITOPF_SEABORNE_IMAGE, image_path)
    download(ITOPF_ARCHIVE_PAGE, page_path)
    download(ITOPF_2017_STATS_PDF, pdf_path)
    capture_text_pdf(pdf_path, CANDIDATES / "oil_spill_stats_2017.txt")

    spills = load_spills_robust()
    write_csv(CLEAN / "figure_10_5_oil_spills_clean.csv", spills)
    oil_rows = digitize_itopf_oil_line(image_path)
    write_csv(CANDIDATES / "itopf_archived_seaborne_16_digitized_oil_loaded.csv", oil_rows)
    oil = load_digitized()
    mae, max_abs = write_selected_year_validation(oil)
    book = plot_book(spills, oil)
    status = make_status_panel()
    combine_side_by_side(book, status)

    metadata = {
        "figure_id": "10-5",
        "title": "Oil spills, 1970-2016",
        "status": "partial_match",
        "source_fidelity": "B/C",
        "run_update": "Recovered archived ITOPF 2016 chart image and digitized oil-loaded line as diagnostic; annual UNCTADStat table remains unrecovered.",
        "book_period_reconstruction": str(book.relative_to(ROOT)),
        "extension": "not_plotted_no_validated_same_method_successor",
        "digitization_tolerance": f"Visual/image-derived tolerance; selected-year comparison to UNCTAD RMT 2020 MAE {mae:.3f} billion metric tons, max {max_abs:.3f}.",
        "unresolved_issues": [
            "Exact Roser 2016r OWID snapshot not recovered.",
            "Annual UNCTADStat oil-loaded table behind the gray line not recovered.",
            "Oil-loaded values are digitized from a source chart image and should not be treated as original tabular data.",
        ],
    }
    (FIG / "metadata" / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    write_checksums()


if __name__ == "__main__":
    main()
