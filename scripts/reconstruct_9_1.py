from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path

import matplotlib.pyplot as plt
from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures" / "9-1"
PDF = ROOT / "references" / "enlightenment_now_supplemental_graphics.pdf"


OECD_TABLE_11_4 = [
    # Source: OECD/IISH, How Was Life? Global Well-being Since 1820,
    # Chapter 11, Table 11.4. Values are Gini points; scaled below to 0-1.
    (1820, 16),
    (1850, 23),
    (1870, 32),
    (1890, 38),
    (1910, 44),
    (1929, 49),
    (1950, 55),
    (1960, 54),
    (1970, 56),
    (1980, 56),
    (1990, 56),
    (2000, 54),
]


def ensure_dirs() -> None:
    for rel in [
        "data/clean",
        "plots/book_period",
        "plots/extended",
        "plots/comparisons",
        "checksums",
    ]:
        (FIG / rel).mkdir(parents=True, exist_ok=True)


def write_clean_csv() -> Path:
    out = FIG / "data/clean/figure_9_1_oecd_table_11_4_between_country_inequality.csv"
    with out.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "year",
                "gini_index",
                "gini_points",
                "series",
                "source",
                "notes",
            ]
        )
        for year, gini_points in OECD_TABLE_11_4:
            writer.writerow(
                [
                    year,
                    f"{gini_points / 100:.2f}",
                    gini_points,
                    "International inequality (unweighted/between-country)",
                    "OECD/IISH How Was Life? 2014, Chapter 11, Table 11.4",
                    "Recovered source table for Pinker's unweighted line; population-weighted Milanovic 2012/2013 line not recovered as inspectable data.",
                ]
            )
    return out


def crop_pdf_reference() -> Path:
    tmp_prefix = Path("/tmp/figure_9_1_supplemental_page")
    subprocess.run(
        [
            "pdftoppm",
            "-png",
            "-f",
            "9",
            "-l",
            "9",
            "-r",
            "180",
            str(PDF),
            str(tmp_prefix),
        ],
        check=True,
    )
    page = Path(f"{tmp_prefix}-09.png")
    out = FIG / "plots/comparisons/supplemental_pdf_reference_figure_9_1.png"
    Image.open(page).convert("RGB").crop((90, 790, 1040, 1525)).save(out)
    return out


def save_partial_status_plot(out: Path, title_suffix: str) -> None:
    years = [year for year, _ in OECD_TABLE_11_4]
    values = [gini / 100 for _, gini in OECD_TABLE_11_4]

    fig, ax = plt.subplots(figsize=(8.4, 5.2), dpi=180)
    ax.plot(years, values, color="#a8a8a8", linewidth=3.0)
    ax.scatter(years, values, color="#a8a8a8", s=18, zorder=3)

    ax.set_xlim(1820, 2020)
    ax.set_ylim(0.10, 0.75)
    ax.set_xticks(range(1820, 2021, 20))
    ax.set_yticks([x / 100 for x in range(10, 76, 5)])
    ax.set_ylabel("Gini index")
    ax.set_title(f"Figure 9-1 source-recovery status{title_suffix}", loc="left", fontsize=13)
    ax.grid(False)
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)

    ax.text(
        1870,
        0.255,
        "Recovered from OECD/Clio Table 11.4:\n"
        "unweighted / between-country inequality\n"
        "1820-2000",
        color="#555555",
        fontsize=9.5,
    )
    ax.text(
        1953,
        0.68,
        "Not plotted: Milanovic population-weighted\n"
        "series through 2013 remains unrecovered\n"
        "as an inspectable data file.",
        color="#222222",
        fontsize=9.5,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "pad": 5},
    )
    ax.text(
        1822,
        0.115,
        "This is not a full reconstruction of the book figure.",
        color="#8a1f11",
        fontsize=9,
        weight="bold",
    )
    fig.tight_layout()
    fig.savefig(out)
    plt.close(fig)


def trim_image(path: Path) -> Image.Image:
    image = Image.open(path).convert("RGB")
    bg = Image.new("RGB", image.size, "white")
    diff = ImageChops.difference(image, bg)
    bbox = diff.getbbox()
    return image.crop(bbox) if bbox else image


def save_side_by_side(reference: Path, status: Path, output: Path, title: str) -> None:
    ref = trim_image(reference)
    rec = trim_image(status)
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
    draw.text((left_x + panel_w // 2, label_y), "Supplemental PDF reference", fill="black", anchor="ma", font=label_font)
    draw.text((right_x + panel_w // 2, label_y), "Recovered source/status", fill="black", anchor="ma", font=label_font)
    paste_fit(ref, left_x, title_h + header_h)
    paste_fit(rec, right_x, title_h + header_h)
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output)


def write_checksums() -> None:
    files = sorted(
        [
            *list((FIG / "data/raw").glob("*")),
            *list((FIG / "data/clean").glob("*")),
            *list((FIG / "plots").glob("*/*.png")),
        ]
    )
    out = FIG / "checksums/sha256sums.txt"
    with out.open("w") as f:
        for path in files:
            if path.is_file():
                digest = hashlib.sha256(path.read_bytes()).hexdigest()
                f.write(f"{digest}  {path.relative_to(ROOT)}\n")


def main() -> None:
    ensure_dirs()
    write_clean_csv()
    reference = crop_pdf_reference()
    book_status = FIG / "plots/book_period/figure_9_1_book_period_reconstruction.png"
    extended_status = FIG / "plots/extended/figure_9_1_extended_reconstruction.png"
    save_partial_status_plot(book_status, "")
    save_partial_status_plot(extended_status, " (no comparable extension)")
    save_side_by_side(
        reference,
        book_status,
        FIG / "plots/comparisons/figure_9_1_book_period_comparison.png",
        "Figure 9-1: International inequality, 1820-2013",
    )
    save_side_by_side(
        reference,
        extended_status,
        FIG / "plots/comparisons/figure_9_1_extended_comparison.png",
        "Figure 9-1: International inequality, 1820-2013",
    )
    write_checksums()


if __name__ == "__main__":
    main()
