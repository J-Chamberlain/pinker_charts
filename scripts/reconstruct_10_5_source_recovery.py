#!/usr/bin/env python3
"""Rebuild Figure 10-5 artifacts after targeted source-recovery review.

The recovered evidence supports the oil-spill count line. The annual
1970-2016 oil-shipped-by-sea line remains unrecovered, so the publication
artifact intentionally leaves that series out instead of plotting a proxy.
"""

from __future__ import annotations

import csv
import hashlib
import textwrap
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image, ImageDraw, ImageOps


ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures" / "10-5"
BOOK = FIG / "plots" / "book_period" / "figure_10_5_book_period_reconstruction.png"
EXT = FIG / "plots" / "extended" / "figure_10_5_extended_reconstruction.png"
COMP = FIG / "plots" / "comparisons" / "figure_10_5_book_style_comparison.png"
COMP_CAP = FIG / "plots" / "comparisons" / "figure_10_5_book_style_comparison_captioned.png"
EXT_COMP = FIG / "plots" / "comparisons" / "figure_10_5_extended_comparison.png"
EXT_COMP_CAP = FIG / "plots" / "comparisons" / "figure_10_5_extended_comparison_captioned.png"
ORIG = FIG / "plots" / "comparisons" / "corrected_figure_10_5_book_crop.png"


def load_spills() -> pd.DataFrame:
    raw = pd.read_csv(FIG / "data" / "raw" / "owid_number_oil_spills.csv")
    raw = raw[raw["Entity"].eq("World")].copy()
    raw["oil_spills_7_plus_tonnes"] = raw["Large oil spills (>700 tonnes)"] + raw["Medium oil spills (7–700 tonnes)"]
    return raw.rename(columns={"Year": "year"})


def plot_book() -> None:
    spills = load_spills()
    book = spills[spills["year"].between(1970, 2016)]
    plt.style.use("seaborn-v0_8-whitegrid")
    fig, ax = plt.subplots(figsize=(9.8, 5.2), dpi=180)
    ax.plot(book["year"], book["oil_spills_7_plus_tonnes"], color="#111111", linewidth=2.4)
    ax.set_title("Oil spills, 1970-2016", fontsize=17, loc="left", pad=10)
    ax.set_xlim(1970, 2020)
    ax.set_ylim(0, 125)
    ax.set_xticks(range(1970, 2021, 5))
    ax.set_yticks(range(0, 126, 25))
    ax.set_ylabel("Number of oil spills")
    ax.set_xlabel("")
    ax.text(2006, 14, "Oil spills", fontsize=11, color="#111111")

    ax2 = ax.twinx()
    ax2.set_ylim(1.4, 3.4)
    ax2.set_yticks([1.4, 1.8, 2.2, 2.6, 3.0, 3.4])
    ax2.set_ylabel("Billion metric tons")
    ax2.text(
        1972,
        3.22,
        "Oil-shipped-by-sea line not plotted:\nannual 1970-2016 source not recovered",
        fontsize=9,
        color="#666666",
        va="top",
    )

    fig.text(
        0.01,
        0.01,
        "Verified input: OWID/ITOPF spill counts. Missing input: exact Roser 2016r/ITOPF annual oil-shipped-by-sea series.",
        fontsize=7.5,
        color="#555555",
    )
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(BOOK)
    plt.close(fig)


def plot_extended() -> None:
    spills = load_spills()
    book = spills[spills["year"].between(1970, 2016)]
    ext = spills[spills["year"].between(2016, 2025)]
    plt.style.use("seaborn-v0_8-whitegrid")
    fig, ax = plt.subplots(figsize=(9.8, 5.2), dpi=180)
    ax.plot(book["year"], book["oil_spills_7_plus_tonnes"], color="#111111", linewidth=2.4)
    ax.plot(ext["year"], ext["oil_spills_7_plus_tonnes"], color="#111111", linewidth=2.4, linestyle=(0, (2, 2)))
    ax.set_title("Oil spills, 1970-2025", fontsize=17, loc="left", pad=10)
    ax.set_xlim(1970, 2026)
    ax.set_ylim(0, 125)
    ax.set_xticks(range(1970, 2026, 5))
    ax.set_yticks(range(0, 126, 25))
    ax.set_ylabel("Number of oil spills")
    ax.set_xlabel("")
    ax.text(2007, 14, "Oil spills", fontsize=11, color="#111111")

    ax2 = ax.twinx()
    ax2.set_ylim(1.4, 3.4)
    ax2.set_yticks([1.4, 1.8, 2.2, 2.6, 3.0, 3.4])
    ax2.set_ylabel("Billion metric tons")
    ax2.text(
        1972,
        3.22,
        "No oil-shipping extension plotted:\ncurrent UNCTAD bulk starts in 2000 and fails RMT scale check",
        fontsize=9,
        color="#666666",
        va="top",
    )

    fig.text(
        0.01,
        0.01,
        "Solid: book-period spill counts through 2016. Dotted: same OWID/ITOPF successor spill-count series through 2025.",
        fontsize=7.5,
        color="#555555",
    )
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(EXT)
    plt.close(fig)


def comparison(reconstruction: Path, output: Path, captioned: Path, caption: str) -> None:
    left = Image.open(ORIG).convert("RGB")
    right = Image.open(reconstruction).convert("RGB")
    height = max(left.height, right.height)

    def fit(img: Image.Image) -> Image.Image:
        canvas = Image.new("RGB", (img.width, height), "white")
        canvas.paste(img, (0, (height - img.height) // 2))
        return canvas

    left = fit(left)
    right = fit(right)
    gap = 30
    label_h = 34
    canvas = Image.new("RGB", (left.width + right.width + gap, height + label_h), "white")
    draw = ImageDraw.Draw(canvas)
    draw.text((10, 8), "Book reference", fill=(0, 0, 0))
    draw.text((left.width + gap + 10, 8), "Current repository reconstruction", fill=(0, 0, 0))
    canvas.paste(left, (0, label_h))
    canvas.paste(right, (left.width + gap, label_h))
    canvas.save(output)

    wrapped = textwrap.fill(caption, width=145)
    cap_h = 74
    cap_canvas = Image.new("RGB", (canvas.width, canvas.height + cap_h), "white")
    cap_canvas.paste(canvas, (0, 0))
    ImageDraw.Draw(cap_canvas).multiline_text((12, canvas.height + 10), wrapped, fill=(40, 40, 40), spacing=4)
    cap_canvas.save(captioned)


def write_checksums() -> None:
    files = [
        *(FIG / "data" / "raw").glob("*"),
        *(FIG / "data" / "clean").glob("*"),
        *(FIG / "data" / "candidates").glob("*"),
    ]
    with (FIG / "checksums" / "sha256sums.txt").open("w", encoding="utf-8") as handle:
        for path in sorted(p for p in files if p.is_file()):
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            handle.write(f"{digest}  {path.relative_to(ROOT)}\n")

    plot_files = [
        *(FIG / "plots" / "book_period").glob("*.png"),
        *(FIG / "plots" / "extended").glob("*.png"),
        *(FIG / "plots" / "comparisons").glob("*.png"),
        *(FIG / "plots" / "diagnostics").glob("*.png"),
    ]
    with (FIG / "checksums" / "plot_sha256sums.txt").open("w", encoding="utf-8") as handle:
        for path in sorted(plot_files):
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            handle.write(f"{digest}  {path.relative_to(ROOT)}\n")


def write_clean_successor() -> None:
    """Summarize the rejected current UNCTAD bulk overlap for quick review."""
    bulk = FIG / "data" / "candidates" / "unctad_us_seaborne_trade_bulk_2000_2024.csv"
    out = FIG / "data" / "clean" / "figure_10_5_current_unctad_bulk_oil_cargo_2000_2024.csv"
    rows: dict[int, float] = {}
    with bulk.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row["Economy"] == "0000" and row["CargoType"] in {"11", "12"}:
                year = int(row["Year"])
                rows[year] = rows.get(year, 0.0) + float(row["Metric tons in thousands"]) / 1_000_000
    with out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["year", "current_unctad_oil_cargo_billion_tons", "status"])
        for year in sorted(rows):
            writer.writerow([year, f"{rows[year]:.6f}", "rejected_for_book_line_scale_mismatch"])


def main() -> None:
    write_clean_successor()
    plot_book()
    plot_extended()
    comparison(
        BOOK,
        COMP,
        COMP_CAP,
        "Partial reconstruction: the verified oil-spill count line is plotted on the book axes; the oil-shipped-by-sea line is not plotted because the annual 1970-2016 source has not been recovered.",
    )
    comparison(
        EXT,
        EXT_COMP,
        EXT_COMP_CAP,
        "Partial extension: same OWID/ITOPF spill counts are extended through 2025; no oil-shipping successor line is plotted because the current UNCTAD bulk series starts in 2000 and fails the RMT scale check.",
    )
    write_checksums()


if __name__ == "__main__":
    main()
