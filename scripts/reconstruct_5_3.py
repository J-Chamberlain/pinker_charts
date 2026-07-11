#!/usr/bin/env python3
"""Reconstruct Figure 5-3 from preserved OWID dataset 522.

The preserved table combines Gapminder (2010) historical observations with
World Bank (2015) estimates without adjustment. Values are ratios per 100,000
live births; the book axis is percent, so percent = ratio / 1,000.
"""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import matplotlib.pyplot as plt
from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures" / "5-3"
RAW = FIG / "data" / "raw"
CLEAN = FIG / "data" / "clean"
PLOTS = FIG / "plots"
COUNTRIES = ["Malaysia", "Sweden", "United States", "Ethiopia"]
COLORS = {
    "Malaysia": "#7F7F7F",
    "Sweden": "#111111",
    "United States": "#B0B0B0",
    "Ethiopia": "#555555",
}


def load_preserved() -> tuple[dict, list[dict]]:
    payload = json.loads((RAW / "owid_522_maternal_mortality.tab").read_text())
    rows = [
        {"Entity": entity, "Year": int(year), "mmr_per_100000": float(value)}
        for entity, year, value in payload["data"]
        if entity in COUNTRIES
    ]
    return payload, rows


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["Entity", "Year", "mmr_per_100000", "maternal_mortality_percent"],
        )
        writer.writeheader()
        for row in sorted(rows, key=lambda item: (item["Entity"], item["Year"])):
            writer.writerow(
                {
                    **row,
                    "maternal_mortality_percent": f'{row["mmr_per_100000"] / 1000:.6f}',
                }
            )


def validate_clean(path: Path, source_rows: list[dict], tolerance: float = 5e-7) -> None:
    expected = {(row["Entity"], row["Year"]): row["mmr_per_100000"] / 1000 for row in source_rows}
    with path.open(newline="") as handle:
        observed = {
            (row["Entity"], int(row["Year"])): float(row["maternal_mortality_percent"])
            for row in csv.DictReader(handle)
        }
    if set(observed) != set(expected):
        raise ValueError(f"Row keys differ for {path}")
    max_error = max(abs(observed[key] - expected[key]) for key in expected)
    if max_error > tolerance:
        raise ValueError(f"Maximum error {max_error} exceeds {tolerance} for {path}")


def draw_chart(rows: list[dict], output: Path, end_year: int, extension: bool = False) -> None:
    fig, ax = plt.subplots(figsize=(8.2, 4.7), dpi=200)
    for country in COUNTRIES:
        series = sorted(
            (row for row in rows if row["Entity"] == country and row["Year"] <= end_year),
            key=lambda row: row["Year"],
        )
        x = [row["Year"] for row in series]
        y = [row["mmr_per_100000"] / 1000 for row in series]
        historical = [i for i, year in enumerate(x) if year <= 2013]
        if historical:
            last = historical[-1] + 1
            ax.plot(x[:last], y[:last], color=COLORS[country], linewidth=2.1)
        later = [i for i, year in enumerate(x) if year >= 2013]
        if extension and len(later) > 1:
            first = later[0]
            ax.plot(x[first:], y[first:], color=COLORS[country], linewidth=2.1, linestyle="--")

    labels = {
        "Malaysia": (1934, 1.13),
        "Sweden": (1800, 0.74),
        "United States": (1911, 0.93),
        "Ethiopia": (1992, 1.24),
    }
    for country, (x, y) in labels.items():
        ax.text(x, y, country, color=COLORS[country], fontsize=10)
    ax.set_xlim(1750, 2020)
    ax.set_ylim(0, 1.5)
    ax.set_xticks(list(range(1750, 2011, 20)))
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5])
    ax.set_yticklabels(["0", "0.25", "0.5", "0.75", "1.0", "1.25", "1.5"])
    ax.set_ylabel("Percentage of mothers dying in childbirth")
    ax.set_title(
        "Figure 5-3: Maternal mortality, 1751-2013"
        + (" (same-source continuation to 2015)" if extension else ""),
        loc="left",
        fontsize=12,
    )
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(False)
    ax.tick_params(labelsize=8)
    if extension:
        ax.axvline(2013, color="#777777", linewidth=0.8, linestyle=":")
        ax.text(2014, 1.45, "2014-15: same recovered source", fontsize=7, color="#555555")
    fig.tight_layout()
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def draw_reference_facsimile(rows: list[dict], output: Path) -> None:
    """Render a clearly labeled facsimile from the indexed supplemental layout.

    This is visual evidence only, never an independent data source.
    """
    fig, ax = plt.subplots(figsize=(8.2, 5.4), dpi=200)
    for country in COUNTRIES:
        series = sorted(
            (row for row in rows if row["Entity"] == country and row["Year"] <= 2013),
            key=lambda row: row["Year"],
        )
        ax.plot(
            [row["Year"] for row in series],
            [row["mmr_per_100000"] / 1000 for row in series],
            color=COLORS[country],
            linewidth=1.7,
        )
    for country, (x, y) in {
        "Malaysia": (1934, 1.13),
        "Sweden": (1800, 0.74),
        "United States": (1911, 0.93),
        "Ethiopia": (1992, 1.24),
    }.items():
        ax.text(x, y, country, color=COLORS[country], fontsize=9)
    ax.set(xlim=(1750, 2020), ylim=(0, 1.5))
    ax.set_xticks(list(range(1750, 2011, 20)))
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5])
    ax.set_yticklabels(["0", "0.25", "0.5", "0.75", "1.0", "1.25", "1.5"])
    ax.set_ylabel("Percentage of mothers dying in childbirth")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=8)
    fig.subplots_adjust(left=0.12, right=0.98, top=0.95, bottom=0.25)
    fig.text(0.12, 0.145, "Figure 5-3: Maternal mortality, 1751-2013", fontsize=11)
    fig.text(
        0.12,
        0.075,
        "Source: Our World in Data, Roser 2016p, based partly on data from Claudia Hanson of Gapminder.",
        fontsize=7,
    )
    fig.text(0.99, 0.01, "Evidence-based facsimile; original PDF pixels unavailable in this run", ha="right", fontsize=6, color="#666666")
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, facecolor="white")
    plt.close(fig)


def comparison(reference: Path, recreated: Path, output: Path, right_label: str) -> None:
    def trim(path: Path) -> Image.Image:
        image = Image.open(path).convert("RGB")
        diff = ImageChops.difference(image, Image.new("RGB", image.size, "white"))
        return image.crop(diff.getbbox()) if diff.getbbox() else image

    left, right = trim(reference), trim(recreated)
    panel_w, panel_h, margin, gap = 960, 620, 40, 40
    canvas = Image.new("RGB", (2 * panel_w + 2 * margin + gap, panel_h + 135), "white")
    draw = ImageDraw.Draw(canvas)
    try:
        heading = ImageFont.truetype("Arial.ttf", 25)
        label = ImageFont.truetype("Arial.ttf", 20)
    except OSError:
        heading = label = None
    draw.text((canvas.width // 2, 18), "Figure 5-3 visual comparison", fill="black", anchor="ma", font=heading)
    draw.text((margin + panel_w // 2, 62), "Supplemental-layout facsimile", fill="black", anchor="ma", font=label)
    draw.text((margin + panel_w + gap + panel_w // 2, 62), right_label, fill="black", anchor="ma", font=label)
    for image, x in ((left, margin), (right, margin + panel_w + gap)):
        fitted = ImageOps.contain(image, (panel_w, panel_h), Image.Resampling.LANCZOS)
        px = x + (panel_w - fitted.width) // 2
        py = 100 + (panel_h - fitted.height) // 2
        canvas.paste(fitted, (px, py))
        draw.rectangle((x, 100, x + panel_w, 100 + panel_h), outline="#DDDDDD")
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output)


def write_checksums() -> None:
    paths = [path for path in FIG.rglob("*") if path.is_file() and "checksums" not in path.parts]
    lines = [f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.relative_to(FIG)}" for path in sorted(paths)]
    (FIG / "checksums" / "sha256sums.txt").write_text("\n".join(lines) + "\n")


def main() -> None:
    _, rows = load_preserved()
    book = [row for row in rows if 1751 <= row["Year"] <= 2013]
    continuation = [row for row in rows if 1751 <= row["Year"] <= 2015]
    book_csv = CLEAN / "figure_5_3_book_period_clean.csv"
    extension_csv = CLEAN / "figure_5_3_same_source_continuation_clean.csv"
    write_csv(book_csv, book)
    write_csv(extension_csv, continuation)
    validate_clean(book_csv, book)
    validate_clean(extension_csv, continuation)
    book_plot = PLOTS / "book_period" / "figure_5_3_book_period_reconstruction.png"
    ext_plot = PLOTS / "extended" / "figure_5_3_same_source_continuation.png"
    draw_chart(book, book_plot, 2013)
    draw_chart(continuation, ext_plot, 2015, extension=True)
    reference = PLOTS / "comparisons" / "supplemental_reference_facsimile_figure_5_3.png"
    draw_reference_facsimile(book, reference)
    comparison(reference, book_plot, PLOTS / "comparisons" / "figure_5_3_book_period_comparison.png", "Recovered-data reconstruction")
    comparison(reference, ext_plot, PLOTS / "comparisons" / "figure_5_3_extended_comparison.png", "Same-source continuation")
    write_checksums()


if __name__ == "__main__":
    main()
