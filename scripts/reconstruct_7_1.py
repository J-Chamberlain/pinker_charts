from __future__ import annotations

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures" / "7-1"
RAW = FIG / "data" / "raw" / "owid_daily_calories_fao_historical.csv"
VALUE = "Daily caloric supply (OWID based on UN FAO & historical sources)"


SERIES = [
    ("United States", "United States", "0.62", "-"),
    ("United Kingdom", "England/UK", "black", ":"),
    ("France", "France", "0.42", "-"),
    ("China", "China", "0.78", "-"),
    ("India", "India", "0.55", "-"),
    ("World", "World", "black", "-"),
]


def trim(path: Path) -> Image.Image:
    im = Image.open(path).convert("RGB")
    bg = Image.new("RGB", im.size, "white")
    bbox = ImageChops.difference(im, bg).getbbox()
    return im.crop(bbox) if bbox else im


def side_by_side(reference: Path, recreated: Path, output: Path, title: str) -> None:
    ref = trim(reference)
    rec = trim(recreated)
    panel_w, panel_h = 980, 700
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
        px = x + (panel_w - fitted.width) // 2
        py = y + (panel_h - fitted.height) // 2
        canvas.paste(fitted, (px, py))
        draw.rectangle([x, y, x + panel_w, y + panel_h], outline=(230, 230, 230), width=1)

    draw.text((canvas.width // 2, 18), title, fill="black", anchor="ma", font=title_font)
    left_x = margin
    right_x = margin + panel_w + gap
    label_y = title_h + 8
    draw.text((left_x + panel_w // 2, label_y), "PDF chart reference", fill="black", anchor="ma", font=label_font)
    draw.text((right_x + panel_w // 2, label_y), "Recreated", fill="black", anchor="ma", font=label_font)
    paste_fit(ref, left_x, title_h + header_h)
    paste_fit(rec, right_x, title_h + header_h)
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output)


def draw(data: pd.DataFrame, out: Path, extended: bool = False) -> None:
    fig, ax = plt.subplots(figsize=(8.3, 5.1), dpi=180)
    for source_entity, label, color, linestyle in SERIES:
        sub = data[data["source_entity"].eq(source_entity)].sort_values("Year")
        main = sub[sub["Year"] <= 2013]
        ax.plot(
            main["Year"],
            main[VALUE],
            color=color,
            linestyle=linestyle,
            linewidth=2.5 if label in {"England/UK", "World"} else 2.0,
        )
        if extended:
            later = sub[sub["Year"] > 2013]
            ax.plot(later["Year"], later[VALUE], color=color, linestyle="--", linewidth=1.6)
        if not main.empty:
            x = main["Year"].iloc[-1]
            y = main[VALUE].iloc[-1]
            dx = -42
            dy = {
                "United States": 70,
                "England/UK": -70,
                "France": -35,
                "China": -120,
                "India": 15,
                "World": 55,
            }.get(label, 40)
            ax.text(x + dx, y + dy, label, fontsize=8, color=color)

    ax.set_xlim(1700, 2030)
    ax.set_ylim(1000, 4000)
    ax.set_xticks(range(1700, 2031, 30))
    ax.set_yticks(range(1000, 4001, 500))
    ax.set_ylabel("Calories per person per day")
    ax.set_title("Figure 7-1: Calories, 1700-2013", loc="left", fontsize=12)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(False)
    ax.tick_params(labelsize=8)
    note = (
        "Source: OWID 2022 dataset based on FAO and historical sources.\n"
        "UK series shown as England/UK; exact Roser 2016d England vintage was not recovered."
    )
    if extended:
        note += "\nDashed segments show same-dataset successor values after 2013."
    ax.text(0, -0.22, note, transform=ax.transAxes, fontsize=7)
    fig.tight_layout()
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def main() -> None:
    raw = pd.read_csv(RAW)
    wanted = [source for source, _, _, _ in SERIES]
    clean = raw[raw["Entity"].isin(wanted) & raw["Year"].between(1700, 2018)].copy()
    label_map = {source: label for source, label, _, _ in SERIES}
    clean.insert(0, "source_entity", clean["Entity"])
    clean.insert(1, "display_entity", clean["Entity"].map(label_map))
    clean = clean.drop(columns=["Entity"])

    book = clean[clean["Year"].between(1700, 2013)].copy()
    book.to_csv(FIG / "data" / "clean" / "figure_7_1_book_period_clean.csv", index=False)
    clean.to_csv(FIG / "data" / "clean" / "figure_7_1_extended_clean.csv", index=False)

    book_plot = FIG / "plots" / "book_period" / "figure_7_1_book_period_reconstruction.png"
    ext_plot = FIG / "plots" / "extended" / "figure_7_1_extended_reconstruction.png"
    draw(book, book_plot, extended=False)
    draw(clean, ext_plot, extended=True)

    reference = FIG / "plots" / "comparisons" / "kindle_reference_figure_7_1.png"
    side_by_side(reference, book_plot, FIG / "plots" / "comparisons" / "figure_7_1_book_period_comparison.png", "Figure 7-1 book-period comparison")
    side_by_side(reference, ext_plot, FIG / "plots" / "comparisons" / "figure_7_1_extended_comparison.png", "Figure 7-1 extended comparison")


if __name__ == "__main__":
    main()
