"""Rebuild the documented Figure 5-2 partial match.

The exact Roser (2016a) UN/HMD chart export has not been recovered.  The
current OWID ``child-mortality`` export retains trajectories that closely
match the book, but it also includes earlier Gapminder segments that are not
drawn in the book and incorporates later UN-IGME revisions.  This script uses
the live export only as a versioned-in-repository successor proxy, clips each
country to the first year visibly present in the book, and never treats the
result as an exact reconstruction.
"""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "figures/5-2"
RAW = BASE / "data/raw/owid_current_child_mortality.csv"
BOOK_CLEAN = BASE / "data/clean/figure_5_2_book_period_clean.csv"
EXT_CLEAN = BASE / "data/clean/figure_5_2_extended_clean.csv"

# Source cutovers read from the Kindle chart. They prevent unrelated earlier
# Gapminder segments in the successor export from being silently substituted.
# The image does not support exact subannual/source-boundary inference; these
# are deliberately documented as visual cutovers, not recovered source facts.
START_YEAR = {
    "Sweden": 1751,
    "Canada": 1921,
    "South Korea": 1950,
    "Chile": 1955,
    "Ethiopia": 1966,
}
ORDER = ["Sweden", "Canada", "South Korea", "Chile", "Ethiopia"]
COLORS = {
    "Sweden": "#111111",
    "Canada": "#777777",
    "South Korea": "#a3a3a3",
    "Chile": "#bdbdbd",
    "Ethiopia": "#e0e0e0",
}


def load_proxy() -> list[dict[str, object]]:
    with RAW.open(newline="", encoding="utf-8") as handle:
        source = list(csv.DictReader(handle))
    rows: list[dict[str, object]] = []
    for row in source:
        entity = row["Entity"]
        year = int(row["Year"])
        if entity in START_YEAR and START_YEAR[entity] <= year <= 2013:
            rows.append(
                {
                    "Entity": entity,
                    "Code": row["Code"],
                    "Year": year,
                    "under5_mortality_percent": float(
                        row["Under-five mortality rate (selected)"]
                    ),
                    "source_role": "current_owid_successor_proxy",
                }
            )
    return rows


def write_clean(rows: list[dict[str, object]]) -> None:
    fields = [
        "Entity",
        "Code",
        "Year",
        "under5_mortality_percent",
        "source_role",
    ]
    for path in (BOOK_CLEAN, EXT_CLEAN):
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)


def plot(rows: list[dict[str, object]], output: Path, extension_notice: bool) -> None:
    fig, ax = plt.subplots(figsize=(8.3, 5.1), dpi=180)
    label_positions = {
        "Sweden": (1885, 6.2),
        "Canada": (1902, 15.2),
        "South Korea": (1898, 30.8),
        "Chile": (1935, 10.8),
        "Ethiopia": (1938, 25.8),
    }
    for entity in ORDER:
        selected = sorted(
            (r for r in rows if r["Entity"] == entity), key=lambda r: r["Year"]
        )
        years = [r["Year"] for r in selected]
        values = [r["under5_mortality_percent"] for r in selected]
        ax.plot(years, values, color=COLORS[entity], linewidth=2.2)
        x, y = label_positions[entity]
        ax.text(x, y, entity, fontsize=9.5, color=COLORS[entity])

    ax.set_xlim(1750, 2020)
    ax.set_ylim(0, 50)
    ax.set_xticks(range(1750, 2021, 10))
    ax.set_yticks(range(0, 51, 5))
    ax.tick_params(axis="x", rotation=45, labelsize=8)
    ax.tick_params(axis="y", labelsize=8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_ylabel("Percentage of children dying before the age of 5")
    ax.set_title("Figure 5-2: Child mortality, 1751–2013", loc="left", fontsize=12)
    note = (
        "Partial match: current OWID successor values, clipped to book-visible "
        "starts; exact Roser 2016a UN/HMD export unrecovered."
    )
    if extension_notice:
        ax.text(
            0.99,
            0.95,
            "No comparable post-2013 extension plotted",
            transform=ax.transAxes,
            ha="right",
            fontsize=8,
            weight="bold",
        )
    ax.text(0, -0.23, note, transform=ax.transAxes, fontsize=7, va="top")
    fig.tight_layout()
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def side_by_side(reference: Path, recreated: Path, output: Path, title: str) -> None:
    def trim(path: Path) -> Image.Image:
        image = Image.open(path).convert("RGB")
        diff = ImageChops.difference(image, Image.new("RGB", image.size, "white"))
        return image.crop(diff.getbbox()) if diff.getbbox() else image

    ref, rec = trim(reference), trim(recreated)
    panel_w, panel_h, margin, gap, title_h, header_h = 980, 700, 45, 45, 58, 58
    canvas = Image.new(
        "RGB",
        (margin * 2 + panel_w * 2 + gap, title_h + header_h + panel_h + margin),
        "white",
    )
    draw = ImageDraw.Draw(canvas)
    try:
        title_font = ImageFont.truetype("Arial.ttf", 30)
        label_font = ImageFont.truetype("Arial.ttf", 24)
    except OSError:
        title_font = label_font = None

    def paste(image: Image.Image, x: int, y: int) -> None:
        fitted = ImageOps.contain(image, (panel_w, panel_h), Image.Resampling.LANCZOS)
        canvas.paste(fitted, (x + (panel_w - fitted.width) // 2, y + (panel_h - fitted.height) // 2))
        draw.rectangle([x, y, x + panel_w, y + panel_h], outline=(230, 230, 230))

    draw.text((canvas.width // 2, 18), title, fill="black", anchor="ma", font=title_font)
    left, right, y = margin, margin + panel_w + gap, title_h + header_h
    draw.text((left + panel_w // 2, title_h + 8), "Kindle reference", fill="black", anchor="ma", font=label_font)
    draw.text((right + panel_w // 2, title_h + 8), "Documented partial match", fill="black", anchor="ma", font=label_font)
    paste(ref, left, y)
    paste(rec, right, y)
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output)


def main() -> None:
    rows = load_proxy()
    write_clean(rows)
    book = BASE / "plots/book_period/figure_5_2_book_period_reconstruction.png"
    extended = BASE / "plots/extended/figure_5_2_extended_reconstruction.png"
    plot(rows, book, False)
    plot(rows, extended, True)
    reference = BASE / "plots/comparisons/kindle_reference_figure_5_2.png"
    side_by_side(
        reference,
        book,
        BASE / "plots/comparisons/figure_5_2_book_period_comparison.png",
        "Figure 5-2 book-period comparison",
    )
    side_by_side(
        reference,
        extended,
        BASE / "plots/comparisons/figure_5_2_extended_comparison.png",
        "Figure 5-2 extension review",
    )


if __name__ == "__main__":
    main()
