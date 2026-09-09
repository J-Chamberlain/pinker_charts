from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path
from urllib.request import Request, urlopen

import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
sys.setrecursionlimit(10000)
FIG = ROOT / "figures" / "5-3"
TMP = ROOT / "tmp" / "figure_5_3_pdf"
RAW = FIG / "data" / "raw"
CLEAN = FIG / "data" / "clean"
PLOTS = FIG / "plots"

GAPDATA_URL = "https://www.gapminder.org/documentation/documentation/gapdata010.xls"
GAPDOC_URL = "https://www.gapminder.org/documentation/documentation/gapdoc010.pdf"
OWID_CURRENT_URL = "https://ourworldindata.org/grapher/maternal-mortality.csv?v=1&csvType=full&useColumnShortNames=false"
OWID_CURRENT_META_URL = "https://ourworldindata.org/grapher/maternal-mortality.metadata.json?v=1&csvType=full&useColumnShortNames=false"
OWID_2018_ARTICLE_ARCHIVE = "https://web.archive.org/web/20180202002318/https://ourworldindata.org/maternal-mortality"
OWID_2018_SVG_ARCHIVE = (
    "https://web.archive.org/web/20180202002318im_/https://d33wubrfki0l68.cloudfront.net/"
    "44cbd8ac71281683078b5b8890d82d911aea8f10/7b38b/exports/"
    "maternal-mortality-b547af73f0299ddf379f1ab25daa3f14_v1_850x600.svg"
)


def ensure_dirs() -> None:
    for path in [
        RAW,
        CLEAN,
        FIG / "metadata",
        FIG / "provenance",
        FIG / "source_logs",
        FIG / "search_iterations",
        FIG / "discrepancy_logs",
        FIG / "anomaly_reviews",
        FIG / "captions",
        FIG / "lineage",
        PLOTS / "book_period",
        PLOTS / "extended",
        PLOTS / "comparisons",
        PLOTS / "diagnostics",
        FIG / "checksums",
        TMP,
    ]:
        path.mkdir(parents=True, exist_ok=True)


def download(url: str, dest: Path) -> Path:
    if dest.exists() and dest.stat().st_size > 0:
        return dest
    req = Request(url, headers={"User-Agent": "pinker-figure-5-3-source-recovery/1.0"})
    with urlopen(req, timeout=60) as response:
        dest.write_bytes(response.read())
    return dest


def copy_or_download(tmp_name: str, url: str, dest_name: str) -> Path:
    src = TMP / tmp_name
    if not src.exists():
        download(url, src)
    dest = RAW / dest_name
    shutil.copy2(src, dest)
    return dest


def clean_gapminder(gapdata: Path) -> pd.DataFrame:
    df = pd.read_excel(gapdata, sheet_name="Tabelle1")
    df = df[["Country", "year", "MMR", "Source MMR, maternal death and Live birth", "Comment"]].copy()
    df = df.dropna(subset=["Country", "year", "MMR"]).copy()
    df = df.assign(year_numeric=pd.to_numeric(df["year"], errors="coerce"))

    range_years = df["year"].astype(str).str.extract(r"^(\d{4})-(?:\d{2}|\d{4})$")[0]
    df.loc[df["year_numeric"].isna(), "year_numeric"] = pd.to_numeric(range_years, errors="coerce")
    df = df.dropna(subset=["year_numeric"]).copy()
    df = df.assign(Year=df["year_numeric"].astype(int), MMR=pd.to_numeric(df["MMR"], errors="coerce"))
    df = df.dropna(subset=["MMR"]).copy()
    df = df.rename(columns={"Country": "Entity", "MMR": "maternal_mortality_ratio"})
    df["source_component"] = "Gapminder GD010 gapdata010.xls"
    df["provenance_url"] = GAPDATA_URL
    return df[["Entity", "Year", "maternal_mortality_ratio", "source_component", "provenance_url"]]


def load_current_successor(current_csv: Path) -> pd.DataFrame:
    df = pd.read_csv(current_csv)
    value = "Maternal mortality ratio"
    if value not in df.columns:
        value = "Maternal Mortality Ratio (Gapminder (2010) and World Bank (2015))"
    df = df.rename(columns={value: "maternal_mortality_ratio"})
    df["source_component"] = "OWID current grapher successor (downloaded 2026-07-09)"
    df["provenance_url"] = OWID_CURRENT_URL
    return df[["Entity", "Year", "maternal_mortality_ratio", "source_component", "provenance_url"]]


def build_book_period(gap: pd.DataFrame, current: pd.DataFrame) -> pd.DataFrame:
    parts = []
    for country, end in [("Sweden", 2007), ("United States", 2003), ("Malaysia", 1997)]:
        parts.append(gap[(gap["Entity"].eq(country)) & (gap["Year"].between(1751, end))].copy())

    # The book-era OWID machine-readable 2015 World Bank/IHME supplement was not recovered.
    # These rows keep the visual comparison honest while preserving source-component labels.
    successor_windows = {
        "Sweden": (2008, 2013),
        "United States": (2004, 2013),
        "Malaysia": (1998, 2013),
        "Ethiopia": (1985, 2013),
    }
    for country, (start, end) in successor_windows.items():
        sub = current[(current["Entity"].eq(country)) & (current["Year"].between(start, end))].copy()
        sub["source_component"] = "OWID current successor fill; exact 2015 World Bank/IHME vintage not recovered"
        parts.append(sub)

    out = pd.concat(parts, ignore_index=True)
    out = out.dropna(subset=["maternal_mortality_ratio"]).copy()
    out = out.assign(percent_mothers_dying=out["maternal_mortality_ratio"] / 1000.0)
    out = out.sort_values(["Entity", "Year"])
    return out


def crop_reference() -> Path:
    page = TMP / "page-03.png"
    if not page.exists():
        page = ROOT / "tmp" / "track_a_pdf_pages" / "page-03.png"
    out = PLOTS / "comparisons" / "kindle_reference_figure_5_3.png"
    if page.exists():
        Image.open(page).convert("RGB").crop((145, 835, 1000, 1535)).save(out)
    return out


def plot_book(data: pd.DataFrame, out: Path) -> None:
    countries = ["Sweden", "United States", "Malaysia", "Ethiopia"]
    colors = {
        "Sweden": "#202020",
        "United States": "#666666",
        "Malaysia": "#9a9a9a",
        "Ethiopia": "#d0d0d0",
    }
    fig, ax = plt.subplots(figsize=(7.2, 4.6), dpi=220)
    for country in countries:
        sub = data[data["Entity"].eq(country)].sort_values("Year")
        ax.plot(
            sub["Year"],
            sub["percent_mothers_dying"],
            color=colors[country],
            linewidth=2.2 if country == "Sweden" else 2.0,
        )

    labels = {
        "Sweden": (1846, 0.24),
        "United States": (1889, 0.53),
        "Malaysia": (1936, 1.04),
        "Ethiopia": (1988, 1.23),
    }
    for country, (x, y) in labels.items():
        ax.text(x, y, country, color="#222222", fontsize=10)

    ax.set_xlim(1750, 2020)
    ax.set_ylim(0, 1.5)
    ax.axis("off")

    axis_color = "#444444"
    ax.plot([1750, 2020], [0, 0], color=axis_color, linewidth=1.2, clip_on=False)
    ax.plot([1750, 1750], [0, 1.5], color=axis_color, linewidth=1.2, clip_on=False)
    xticks = [1750, 1770, 1790, 1810, 1830, 1850, 1870, 1890, 1910, 1930, 1950, 1970, 1990, 2010]
    for x in xticks:
        ax.plot([x, x], [0, -0.045], color=axis_color, linewidth=1.0, clip_on=False)
        ax.text(x, -0.06, str(x), rotation=50, ha="right", va="top", fontsize=9, color="#222222", clip_on=False)
    yticks = [(0, "0"), (0.25, "0.25"), (0.5, "0.5"), (0.75, "0.75"), (1.0, "1.0"), (1.25, "1.25"), (1.5, "1.5")]
    for y, label in yticks:
        ax.plot([1743, 1750], [y, y], color=axis_color, linewidth=1.0, clip_on=False)
        ax.text(1741, y, label, ha="right", va="center", fontsize=9, color="#222222", clip_on=False)
    ax.text(
        1720,
        0.75,
        "Percentage of mothers dying in childbirth",
        rotation=90,
        ha="center",
        va="center",
        fontsize=10,
        clip_on=False,
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
        canvas.paste(fitted, (x + (panel_w - fitted.width) // 2, y + (panel_h - fitted.height) // 2))
        draw.rectangle([x, y, x + panel_w, y + panel_h], outline=(230, 230, 230), width=1)

    draw.text((canvas.width // 2, 18), title, fill="black", anchor="ma", font=title_font)
    left_x = margin
    right_x = margin + panel_w + gap
    draw.text((left_x + panel_w // 2, title_h + 8), "PDF chart reference", fill="black", anchor="ma", font=label_font)
    draw.text((right_x + panel_w // 2, title_h + 8), "Recreated", fill="black", anchor="ma", font=label_font)
    paste_fit(ref, left_x, title_h + header_h)
    paste_fit(rec, right_x, title_h + header_h)
    canvas.save(output)


def write_reports(book: pd.DataFrame, gap: pd.DataFrame, current: pd.DataFrame) -> None:
    comparison_rows = []
    for country in ["Sweden", "United States", "Malaysia"]:
        g = gap[gap["Entity"].eq(country)][["Year", "maternal_mortality_ratio"]]
        c = current[current["Entity"].eq(country)][["Year", "maternal_mortality_ratio"]]
        merged = g.merge(c, on="Year", suffixes=("_gapdata010", "_owid_current")).copy()
        if not merged.empty:
            diff = (
                merged["maternal_mortality_ratio_gapdata010"] - merged["maternal_mortality_ratio_owid_current"]
            ).abs()
            merged = merged.assign(absolute_difference_mmr=diff)
            comparison_rows.append(merged.assign(Entity=country))
    if comparison_rows:
        pd.concat(comparison_rows, ignore_index=True).to_csv(CLEAN / "figure_5_3_gapminder_vs_owid_current_audit.csv", index=False)

    lineage = [
        {"stage": "Book Figure", "value": "Figure 5-3: Maternal mortality, 1751-2013"},
        {"stage": "Book Citation", "value": "Our World in Data, Roser 2016p, based partly on data from Claudia Hanson of Gapminder."},
        {"stage": "Recovered Original Source Component", "value": "Gapminder GD010 gapdata010.xls and gapdoc010.pdf"},
        {"stage": "Unrecovered Source Component", "value": "Book-era OWID/World Bank 2015 machine-readable supplement for Ethiopia and post-Gapminder tails"},
        {"stage": "Generated Plot", "value": "figures/5-3/plots/comparisons/figure_5_3_book_period_comparison.png"},
    ]
    (FIG / "lineage" / "figure_lineage.json").write_text(json.dumps(lineage, indent=2) + "\n")
    pd.DataFrame(lineage).to_csv(FIG / "lineage" / "figure_lineage.csv", index=False)


def main() -> None:
    ensure_dirs()
    gapdata = copy_or_download("gapdata010.xls", GAPDATA_URL, "gapminder_gd010_gapdata010.xls")
    copy_or_download("gapdoc010.pdf", GAPDOC_URL, "gapminder_gd010_gapdoc010.pdf")
    current_csv = copy_or_download("owid_maternal_current.csv", OWID_CURRENT_URL, "owid_maternal_mortality_ratio_current_2026_07_09.csv")
    copy_or_download("owid_maternal_current.metadata.json", OWID_CURRENT_META_URL, "owid_maternal_mortality_ratio_current_2026_07_09.metadata.json")
    copy_or_download("owid_2018_maternal_mortality.svg", OWID_2018_SVG_ARCHIVE, "owid_maternal_mortality_2018_archived_export.svg")

    gap = clean_gapminder(gapdata)
    current = load_current_successor(current_csv)
    book = build_book_period(gap, current)
    book.to_csv(CLEAN / "figure_5_3_book_period_clean.csv", index=False)
    book.to_csv(CLEAN / "figure_5_3_extended_clean.csv", index=False)

    plot_path = PLOTS / "book_period" / "figure_5_3_book_period_reconstruction.png"
    plot_book(book, plot_path)
    shutil.copy2(plot_path, PLOTS / "extended" / "figure_5_3_extended_reconstruction.png")
    ref = crop_reference()
    side_by_side(ref, plot_path, PLOTS / "comparisons" / "figure_5_3_book_period_comparison.png", "Figure 5-3 book-period comparison")
    side_by_side(ref, plot_path, PLOTS / "comparisons" / "figure_5_3_extended_comparison.png", "Figure 5-3 extended/status comparison")
    write_reports(book, gap, current)


if __name__ == "__main__":
    main()
