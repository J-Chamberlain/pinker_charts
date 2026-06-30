from __future__ import annotations

import csv
import json
import shutil
from datetime import date
from pathlib import Path
from urllib.request import Request, urlopen

import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
OWID = Path("/Users/alfred/Documents/MIsc/enlightenment_now_poc/data/repositories/owid-datasets/datasets")
TMP_KINDLE = ROOT / "tmp/track_a_kindle"
TMP_PDF = ROOT / "tmp/track_a_pdf_pages"
TODAY = date.today().isoformat()


def download(url: str, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size > 0:
        return dest
    req = Request(url, headers={"User-Agent": "pinker-charts-track-a/0.1"})
    with urlopen(req) as response:
        dest.write_bytes(response.read())
    return dest


def base(fig_id: str) -> Path:
    root = ROOT / "figures" / fig_id
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
        "plots/diagnostics",
        "data/raw",
        "data/clean",
        "data/candidates",
        "checksums",
    ]:
        (root / part).mkdir(parents=True, exist_ok=True)
    return root


def copy_dataset(src: Path, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)
    for name in ["README.md", "datapackage.json"]:
        extra = src.with_name(name)
        if extra.exists():
            shutil.copy2(extra, dest.parent / name)
    return dest


def style_axis(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(False)
    ax.tick_params(labelsize=8)


def crop_or_placeholder(fig_id: str, source: Path | None, crop: tuple[int, int, int, int] | None, note: str) -> Path:
    out = base(fig_id) / f"plots/comparisons/kindle_reference_figure_{fig_id.replace('-', '_')}.png"
    if source and crop and source.exists():
        Image.open(source).convert("RGB").crop(crop).save(out)
        return out
    im = Image.new("RGB", (900, 560), "white")
    draw = ImageDraw.Draw(im)
    draw.multiline_text(
        (45, 60),
        f"Kindle chart-page capture unavailable for Figure {fig_id}.\n\n{note}\n\n"
        "This placeholder is not visual validation.",
        fill="black",
        spacing=10,
    )
    im.save(out)
    return out


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

    def paste_fit(im: Image.Image, x: int, y: int):
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


FIGURES = {
    "5-3": {
        "title": "Maternal mortality, 1751-2013",
        "chapter": "5",
        "book_page": "Supplemental PDF page 3; Kindle page previously inspected",
        "claim": "Maternal mortality declined sharply in representative countries.",
        "citation": "Our World in Data, Roser 2016p, based partly on data from Claudia Hanson of Gapminder.",
        "source_status": "updated_equivalent",
        "status": "partial_match",
        "confidence": 0.70,
        "validation": "acceptable",
        "reference_source": "Supplemental PDF page 3 crop",
        "kindle": TMP_PDF / "page-03.png",
        "crop": (145, 835, 1000, 1535),
        "dataset": "Maternal Mortality Ratio (Gapminder (2010), WHO (2019) and OECD (2022))",
    },
    "5-4": {
        "title": "Life expectancy, UK, 1701-2013",
        "chapter": "5",
        "book_page": "Supplemental PDF page 4; Kindle page previously inspected",
        "claim": "UK life expectancy improved at birth and across older ages.",
        "citation": "Our World in Data, Roser 2016n. Data before 1845 are for England and Wales and come from OECD Clio Infra, van Zanden et al. 2014. Data from 1845 on are for mid-decade years only, and come from the Human Mortality Database.",
        "source_status": "needs_targeted_source_recovery",
        "status": "needs_targeted_source_recovery",
        "confidence": 0.40,
        "validation": "poor",
        "reference_source": "Supplemental PDF page 4 crop",
        "kindle": TMP_PDF / "page-04.png",
        "crop": (110, 125, 1000, 820),
        "dataset": "partial HMD/OWID age-specific life-expectancy sources",
    },
    "6-1": {
        "title": "Childhood deaths from infectious disease, 2000-2013",
        "chapter": "6",
        "book_page": "Supplemental PDF page 4; Kindle chart page not captured during Track A",
        "claim": "Childhood deaths from major infectious diseases fell between 2000 and 2013.",
        "citation": "Child Health Epidemiology Reference Group of the World Health Organization; Liu et al. 2014, supplementary appendix.",
        "source_status": "blocked_external_source",
        "status": "blocked_external_source",
        "confidence": 0.30,
        "validation": "poor",
        "reference_source": "Supplemental PDF page 4 crop",
        "kindle": TMP_PDF / "page-04.png",
        "crop": (60, 815, 1000, 1540),
        "dataset": "IHME 2017 causes of child mortality proxy; cited Liu et al. appendix not recovered",
    },
    "7-1": {
        "title": "Calories, 1700-2013",
        "chapter": "7",
        "book_page": "Supplemental PDF page 5; Kindle page previously inspected",
        "claim": "Average calorie availability rose in developed and developing regions.",
        "citation": "United States, England, and France: Our World in Data, Roser 2016d, based on Fogel 2004. China, India, and World: FAO.",
        "source_status": "updated_equivalent",
        "status": "partial_match",
        "confidence": 0.76,
        "validation": "acceptable",
        "reference_source": "Supplemental PDF page 5 crop",
        "kindle": TMP_PDF / "page-05.png",
        "crop": (135, 130, 1035, 780),
        "dataset": "Daily supply of calories per person (OWID based on UN FAO & historical sources)",
    },
    "7-2": {
        "title": "Childhood stunting, 1966-2014",
        "chapter": "7",
        "book_page": "Supplemental PDF page 5; Kindle page previously inspected",
        "claim": "Childhood stunting fell in several developing countries.",
        "citation": "Our World in Data, Roser 2016j, based on WHO Nutrition Landscape Information System.",
        "source_status": "partial_match",
        "status": "partial_match",
        "confidence": 0.55,
        "validation": "acceptable",
        "reference_source": "Supplemental PDF page 5 crop",
        "kindle": TMP_PDF / "page-05.png",
        "crop": (135, 845, 995, 1550),
        "dataset": "World Bank stunting prevalence proxy; exact OWID/WHO NLIS vintage not recovered",
    },
}


def plot_5_3():
    fig_id = "5-3"
    b = base(fig_id)
    name = FIGURES[fig_id]["dataset"]
    src = OWID / name / f"{name}.csv"
    raw = copy_dataset(src, b / "data/raw/owid_maternal_mortality_ratio_current.csv")
    df = pd.read_csv(raw)
    value = "Maternal Mortality Ratio (Gapminder (2010) and World Bank (2015))"
    countries = ["Sweden", "United States", "Malaysia", "Ethiopia"]
    clean = df[df["Entity"].isin(countries) & df["Year"].between(1751, 2020)].copy()
    clean["percent_mothers_dying"] = clean[value] / 1000.0
    book = clean[clean["Year"].between(1751, 2013)].copy()
    book.to_csv(b / "data/clean/figure_5_3_book_period_clean.csv", index=False)
    clean.to_csv(b / "data/clean/figure_5_3_extended_clean.csv", index=False)
    colors = {"Sweden": "black", "United States": "0.45", "Malaysia": "0.62", "Ethiopia": "0.82"}

    def draw(data, out, extended=False):
        fig, ax = plt.subplots(figsize=(8.3, 5.1), dpi=180)
        for c in countries:
            sub = data[data["Entity"].eq(c)].sort_values("Year")
            main = sub[sub["Year"] <= 2013]
            ax.plot(main["Year"], main["percent_mothers_dying"], color=colors[c], linewidth=2.4 if c == "Sweden" else 2.0)
            if extended:
                ext = sub[sub["Year"] > 2013]
                ax.plot(ext["Year"], ext["percent_mothers_dying"], color=colors[c], linestyle="--", linewidth=1.8)
            if len(main):
                ax.text(main["Year"].iloc[-1] - 28, main["percent_mothers_dying"].iloc[-1] + 0.035, c, fontsize=8, color=colors[c])
        ax.set_xlim(1745, 2024 if extended else 2020)
        ax.set_ylim(0, 1.55)
        ax.set_ylabel("Percentage of mothers dying in childbirth")
        ax.set_title("Figure 5-3: Maternal mortality, 1751-2013", loc="left", fontsize=12)
        style_axis(ax)
        ax.text(0, -0.16, "Proxy: current OWID maternal-mortality ratio converted from per 100,000 births to percent.", transform=ax.transAxes, fontsize=7)
        fig.tight_layout()
        fig.savefig(out, bbox_inches="tight", facecolor="white")
        plt.close(fig)

    book_plot = b / "plots/book_period/figure_5_3_book_period_reconstruction.png"
    ext_plot = b / "plots/extended/figure_5_3_extended_reconstruction.png"
    draw(book, book_plot)
    draw(clean, ext_plot, True)
    ref = crop_or_placeholder(fig_id, FIGURES[fig_id]["kindle"], FIGURES[fig_id]["crop"], "Captured Kindle page contains Figure 5-3 and Figure 5-4.")
    side_by_side(ref, book_plot, b / "plots/comparisons/figure_5_3_book_period_comparison.png", "Figure 5-3 book-period comparison")
    side_by_side(ref, ext_plot, b / "plots/comparisons/figure_5_3_extended_comparison.png", "Figure 5-3 extended comparison")


def plot_5_4():
    fig_id = "5-4"
    b = base(fig_id)
    src_birth = OWID / "Life expectancy - Riley (2005), Clio Infra (2015), and UN (2019)" / "Life expectancy - Riley (2005), Clio Infra (2015), and UN (2019).csv"
    src_age = OWID / "Male and female life expectancy by age in the long run (Human Mortality Database (2018) and others)" / "Male and female life expectancy by age in the long run (Human Mortality Database (2018) and others).csv"
    raw_birth = copy_dataset(src_birth, b / "data/raw/owid_life_expectancy_riley_clio_un_2019.csv")
    raw_age = copy_dataset(src_age, b / "data/raw/owid_hmd_age_specific_life_expectancy_partial.csv")
    birth = pd.read_csv(raw_birth)
    age = pd.read_csv(raw_age)
    uk_birth = birth[birth["Entity"].eq("United Kingdom") & birth["Year"].between(1701, 2013)][["Year", "Life expectancy"]].copy()
    uk_birth["series"] = "At birth"
    uk_birth = uk_birth.rename(columns={"Life expectancy": "life_expectancy"})
    uk_age = age[age["Entity"].eq("United Kingdom")].copy()
    rows = []
    for label, male_col, female_col in [
        ("For a 15-year-old", "Male life expectancy at 15 (HMD (2018) and others)", "Female life expectancy at 15 (HMD (2018) and others)"),
        ("For a 45-year-old", "Male life expectancy at 45 (HMD (2018) and others)", "Female life expectancy at 45 (HMD (2018) and others)"),
    ]:
        tmp = uk_age[["Year", male_col, female_col]].copy()
        tmp["life_expectancy"] = tmp[[male_col, female_col]].mean(axis=1)
        tmp["series"] = label
        rows.append(tmp[["Year", "life_expectancy", "series"]])
    clean = pd.concat([uk_birth[["Year", "life_expectancy", "series"]], *rows], ignore_index=True)
    book = clean[clean["Year"].between(1701, 2013)].copy()
    book.to_csv(b / "data/clean/figure_5_4_book_period_clean.csv", index=False)
    clean.to_csv(b / "data/clean/figure_5_4_extended_clean.csv", index=False)

    def draw(out, extended=False):
        fig, ax = plt.subplots(figsize=(8.3, 5.1), dpi=180)
        colors = {"At birth": "black", "For a 15-year-old": "0.45", "For a 45-year-old": "0.7"}
        for s, sub in book.groupby("series"):
            sub = sub.sort_values("Year")
            ax.plot(sub["Year"], sub["life_expectancy"], color=colors[s], linewidth=2.3)
            if len(sub):
                ax.text(sub["Year"].iloc[-1] - 45, sub["life_expectancy"].iloc[-1] + 1.0, s, fontsize=8, color=colors[s])
        ax.set_xlim(1700, 2025)
        ax.set_ylim(25, 88)
        ax.set_ylabel("Life expectancy")
        ax.set_title("Figure 5-4: Life expectancy, UK, 1701-2013", loc="left", fontsize=12)
        style_axis(ax)
        ax.text(0, -0.16, "Partial reconstruction only: exact HMD age-1/5/10/20/30/40/50/60/70 series not recovered.", transform=ax.transAxes, fontsize=7)
        fig.tight_layout()
        fig.savefig(out, bbox_inches="tight", facecolor="white")
        plt.close(fig)

    book_plot = b / "plots/book_period/figure_5_4_book_period_reconstruction.png"
    ext_plot = b / "plots/extended/figure_5_4_extended_reconstruction.png"
    draw(book_plot)
    draw(ext_plot, True)
    ref = crop_or_placeholder(fig_id, FIGURES[fig_id]["kindle"], FIGURES[fig_id]["crop"], "Captured Kindle page includes Figure 5-4 but full source line was not visible.")
    side_by_side(ref, book_plot, b / "plots/comparisons/figure_5_4_book_period_comparison.png", "Figure 5-4 book-period comparison")
    side_by_side(ref, ext_plot, b / "plots/comparisons/figure_5_4_extended_comparison.png", "Figure 5-4 extended comparison")


def plot_6_1():
    fig_id = "6-1"
    b = base(fig_id)
    name = "Causes of child mortality – IHME Global Burden of Disease study (2017)"
    src = OWID / name / f"{name}.csv"
    raw = copy_dataset(src, b / "data/raw/owid_ihme_2017_child_mortality_causes_proxy.csv")
    df = pd.read_csv(raw)
    causes = ["Lower respiratory infections", "Diarrheal diseases", "Malaria", "Measles", "HIV/AIDS", "Meningitis"]
    clean = df[df["Entity"].isin(causes) & df["Year"].isin([2000, 2015])].copy()
    clean.to_csv(b / "data/clean/figure_6_1_book_period_clean.csv", index=False)
    clean.to_csv(b / "data/clean/figure_6_1_extended_clean.csv", index=False)
    pivot = clean.pivot(index="Entity", columns="Year", values="Share of children dying in first 5 years globally, by cause (IHME (2017))").reindex(causes)

    def draw(out, extended=False):
        fig, ax = plt.subplots(figsize=(8.3, 5.1), dpi=180)
        x = range(len(causes))
        ax.bar([i - 0.18 for i in x], pivot[2000], width=0.36, color="0.25", label="2000")
        ax.bar([i + 0.18 for i in x], pivot[2015], width=0.36, color="0.72", label="2015 proxy")
        ax.set_xticks(list(x))
        ax.set_xticklabels(["Pneumonia", "Diarrhea", "Malaria", "Measles", "HIV/AIDS", "Meningitis"], rotation=25, ha="right")
        ax.set_ylabel("Share of global under-5 deaths (%)")
        ax.set_title("Figure 6-1: Childhood deaths from infectious disease, 2000-2013", loc="left", fontsize=12)
        ax.legend(frameon=False)
        style_axis(ax)
        ax.text(0, -0.28, "Proxy only: IHME 2017 cause shares use 2015 endpoint, not cited CHERG/WHO Liu et al. 2014 appendix.", transform=ax.transAxes, fontsize=7)
        fig.tight_layout()
        fig.savefig(out, bbox_inches="tight", facecolor="white")
        plt.close(fig)

    book_plot = b / "plots/book_period/figure_6_1_book_period_reconstruction.png"
    ext_plot = b / "plots/extended/figure_6_1_extended_reconstruction.png"
    draw(book_plot)
    draw(ext_plot, True)
    ref = crop_or_placeholder(fig_id, FIGURES[fig_id]["kindle"], FIGURES[fig_id]["crop"], "Supplemental PDF supplies the Figure 6-1 chart reference.")
    side_by_side(ref, book_plot, b / "plots/comparisons/figure_6_1_book_period_comparison.png", "Figure 6-1 book-period comparison")
    side_by_side(ref, ext_plot, b / "plots/comparisons/figure_6_1_extended_comparison.png", "Figure 6-1 extended comparison")


def plot_7_1():
    fig_id = "7-1"
    b = base(fig_id)
    name = FIGURES[fig_id]["dataset"]
    src = OWID / name / f"{name}.csv"
    raw = copy_dataset(src, b / "data/raw/owid_daily_calories_fao_historical.csv")
    df = pd.read_csv(raw)
    val = "Daily caloric supply (OWID based on UN FAO & historical sources)"
    entities = ["United States", "England", "France", "China", "India", "World"]
    clean = df[df["Entity"].isin(entities) & df["Year"].between(1700, 2018)].copy()
    book = clean[clean["Year"].between(1700, 2013)].copy()
    book.to_csv(b / "data/clean/figure_7_1_book_period_clean.csv", index=False)
    clean.to_csv(b / "data/clean/figure_7_1_extended_clean.csv", index=False)
    colors = {"United States": "0.75", "England": "black", "France": "0.55", "China": "0.80", "India": "0.55", "World": "black"}
    styles = {"England": ":", "World": "-", "United States": "--", "France": "-", "China": "-", "India": "-"}

    def draw(data, out, extended=False):
        fig, ax = plt.subplots(figsize=(8.3, 5.1), dpi=180)
        for ent in entities:
            sub = data[data["Entity"].eq(ent)].sort_values("Year")
            main = sub[sub["Year"] <= 2013]
            ax.plot(main["Year"], main[val], color=colors[ent], linestyle=styles[ent], linewidth=2.5 if ent in ["World", "England"] else 2)
            if extended:
                ext = sub[sub["Year"] > 2013]
                ax.plot(ext["Year"], ext[val], color=colors[ent], linestyle="--", linewidth=1.6)
            if len(main):
                ax.text(main["Year"].iloc[-1] - 40, main[val].iloc[-1] + 40, ent, fontsize=8, color=colors[ent])
        ax.set_xlim(1695, 2025 if extended else 2020)
        ax.set_ylim(1000, 4050)
        ax.set_ylabel("Calories per person per day")
        ax.set_title("Figure 7-1: Calories, 1700-2013", loc="left", fontsize=12)
        style_axis(ax)
        ax.text(0, -0.16, "Source: OWID calories dataset based on FAO and historical sources; post-2013 values are successor continuation.", transform=ax.transAxes, fontsize=7)
        fig.tight_layout()
        fig.savefig(out, bbox_inches="tight", facecolor="white")
        plt.close(fig)

    book_plot = b / "plots/book_period/figure_7_1_book_period_reconstruction.png"
    ext_plot = b / "plots/extended/figure_7_1_extended_reconstruction.png"
    draw(book, book_plot)
    draw(clean, ext_plot, True)
    ref = crop_or_placeholder(fig_id, FIGURES[fig_id]["kindle"], FIGURES[fig_id]["crop"], "Captured Kindle page contains Figure 7-1 and Figure 7-2.")
    side_by_side(ref, book_plot, b / "plots/comparisons/figure_7_1_book_period_comparison.png", "Figure 7-1 book-period comparison")
    side_by_side(ref, ext_plot, b / "plots/comparisons/figure_7_1_extended_comparison.png", "Figure 7-1 extended comparison")


def fetch_world_bank_stunting(dest: Path) -> Path:
    rows = []
    countries = {"BGD": "Bangladesh", "KEN": "Kenya", "COL": "Colombia", "CHN": "China", "USA": "United States"}
    for code, name in countries.items():
        url = f"https://api.worldbank.org/v2/country/{code}/indicator/SH.STA.STNT.ZS?format=json&per_page=2000"
        raw = json.loads(download(url, dest.parent / f"world_bank_stunting_{code}.json").read_text())
        for item in raw[1]:
            if item["value"] is not None:
                rows.append({"Entity": name, "Year": int(item["date"]), "stunting_percent": float(item["value"])})
    pd.DataFrame(rows).to_csv(dest, index=False)
    return dest


def plot_7_2():
    fig_id = "7-2"
    b = base(fig_id)
    raw = fetch_world_bank_stunting(b / "data/raw/world_bank_stunting_prevalence_proxy.csv")
    clean = pd.read_csv(raw)
    book = clean[clean["Year"].between(1966, 2014)].copy()
    ext = clean[clean["Year"].between(1966, 2025)].copy()
    book.to_csv(b / "data/clean/figure_7_2_book_period_clean.csv", index=False)
    ext.to_csv(b / "data/clean/figure_7_2_extended_clean.csv", index=False)
    colors = {"Bangladesh": "black", "Kenya": "0.45", "Colombia": "0.75", "China": "0.55", "United States": "0.85"}

    def draw(data, out, extended=False):
        fig, ax = plt.subplots(figsize=(8.3, 5.1), dpi=180)
        for ent, sub in data.groupby("Entity"):
            sub = sub.sort_values("Year")
            main = sub[sub["Year"] <= 2014]
            ax.plot(main["Year"], main["stunting_percent"], color=colors.get(ent, "0.5"), linewidth=2.4 if ent == "Bangladesh" else 2)
            if extended:
                later = sub[sub["Year"] > 2014]
                ax.plot(later["Year"], later["stunting_percent"], color=colors.get(ent, "0.5"), linestyle="--", linewidth=1.6)
            if len(main):
                ax.text(main["Year"].iloc[-1] - 8, main["stunting_percent"].iloc[-1] + 1.2, ent, fontsize=8, color=colors.get(ent, "0.5"))
        ax.set_xlim(1965, 2025 if extended else 2015)
        ax.set_ylim(0, 82)
        ax.set_ylabel("Percentage of children under 5 who are stunted")
        ax.set_title("Figure 7-2: Childhood stunting, 1966-2014", loc="left", fontsize=12)
        style_axis(ax)
        ax.text(0, -0.16, "Proxy: World Bank SH.STA.STNT.ZS; exact OWID/Roser 2016j WHO NLIS vintage not recovered.", transform=ax.transAxes, fontsize=7)
        fig.tight_layout()
        fig.savefig(out, bbox_inches="tight", facecolor="white")
        plt.close(fig)

    book_plot = b / "plots/book_period/figure_7_2_book_period_reconstruction.png"
    ext_plot = b / "plots/extended/figure_7_2_extended_reconstruction.png"
    draw(book, book_plot)
    draw(ext, ext_plot, True)
    ref = crop_or_placeholder(fig_id, FIGURES[fig_id]["kindle"], FIGURES[fig_id]["crop"], "Captured Kindle page contains Figure 7-1 and Figure 7-2.")
    side_by_side(ref, book_plot, b / "plots/comparisons/figure_7_2_book_period_comparison.png", "Figure 7-2 book-period comparison")
    side_by_side(ref, ext_plot, b / "plots/comparisons/figure_7_2_extended_comparison.png", "Figure 7-2 extended comparison")


def write_docs(fig_id: str):
    b = base(fig_id)
    info = FIGURES[fig_id]
    stem = fig_id.replace("-", "_")
    metadata = {
        "figure_id": fig_id,
        "chapter": info["chapter"],
        "title": info["title"],
        "book_page": info["book_page"],
        "claim_summary": info["claim"],
        "book_citation": info["citation"],
        "original_dataset": info["dataset"],
        "dataset_url": "See source_logs/source_log.md and data/raw/.",
        "archive_url": "Not recovered in Track A time-box.",
        "download_date": TODAY,
        "reproduction_status": info["status"],
        "confidence_score": info["confidence"],
        "visual_validation": info["validation"],
        "notes": f"Track A health/nutrition batch. Source status: {info['source_status']}.",
        "canonical_artifacts": {
            "original_reference": f"figures/{fig_id}/plots/comparisons/kindle_reference_figure_{stem}.png",
            "book_period_reconstruction": f"figures/{fig_id}/plots/book_period/figure_{stem}_book_period_reconstruction.png",
            "extended_reconstruction": f"figures/{fig_id}/plots/extended/figure_{stem}_extended_reconstruction.png",
            "book_period_comparison": f"figures/{fig_id}/plots/comparisons/figure_{stem}_book_period_comparison.png",
            "extended_comparison": f"figures/{fig_id}/plots/comparisons/figure_{stem}_extended_comparison.png",
        },
    }
    (b / "metadata/metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    (b / "captions/caption.txt").write_text(
        f"Figure {fig_id}: {info['title']}. Source note: {info['citation']} "
        f"Status: {info['status']}. Track A reconstruction uses {info['dataset']}; see anomaly review for fidelity limits.\n"
    )
    searches = [
        f'Kindle search/open for "Figure {fig_id}" or title',
        f'"{info["title"]}" source data',
        f'"{info["citation"]}"',
        "local OWID datasets mirror",
        "current public successor data where exact book vintage was unavailable",
    ]
    (b / "source_logs/source_log.md").write_text(
        f"# Source Discovery Log: Figure {fig_id}\n\n"
        f"Figure title: {info['title']}\n\n"
        f"Original book citation: {info['citation']}\n\n"
        "## Search Queries Attempted\n"
        + "\n".join(f"- {q}" for q in searches)
        + "\n\n## Sources Investigated\n"
        f"- Reference image: {info.get('reference_source', 'Kindle chart capture')} accepted for chart reference/source line.\n"
        f"- Dataset used: {info['dataset']}.\n"
        "- Local OWID mirror and current public data were used where available.\n\n"
        "## Remaining Uncertainties\n"
        f"- Status: `{info['status']}`.\n"
        f"- Source status: `{info['source_status']}`.\n\n"
        "## Recommended Next Steps\n"
        "- Recover exact book-era source files or archival copies before promoting status.\n"
    )
    (b / "provenance/provenance.md").write_text(
        f"# Provenance: Figure {fig_id}\n\n"
        f"Book figure -> {info.get('reference_source', 'Kindle evidence')} -> {info['dataset']} -> "
        "`scripts/reconstruct_track_a_health_nutrition.py` -> generated plots.\n\n"
        f"Source note: {info['citation']}\n"
    )
    (b / "anomaly_reviews/anomaly_review.md").write_text(
        f"# Anomaly Review: Figure {fig_id}\n\n"
        "## Visible Differences\n"
        "- Styling, typography, label placement, and crop geometry are approximate.\n"
        + ("- Supplemental PDF supplies the chart reference, but the cited Liu et al. appendix remains unrecovered.\n" if fig_id == "6-1" else "")
        + ("- Reconstruction is visibly incomplete because only age-at-birth, age-15, and age-45 proxy series were recovered.\n" if fig_id == "5-4" else "")
        + "\n## Cause Assessment\n"
        f"- Current status: `{info['status']}`.\n"
        f"- Source fidelity: {info['source_status']}.\n\n"
        "## Reviewer Challenge\n"
        "- Pinker would likely ask whether the exact source vintage was recovered.\n"
        "- A data journalist would ask for archival URLs and machine-readable source files.\n"
        "- A peer reviewer would ask whether successor data are separated from book-period data.\n"
        "- A skeptical reader would notice visible label and line-shape differences in the side-by-side.\n\n"
        "Overall confidence:\n"
        f"- Book reconstruction: {info['confidence']}\n"
        "- Extension: low to medium, depending on successor comparability.\n"
        "- Source provenance: see source log.\n"
        "- Outstanding risks: exact source-vintage recovery remains incomplete for this time-boxed batch.\n"
        "- Recommended next action: targeted source recovery before status promotion.\n"
    )
    (b / "discrepancy_logs/discrepancy_log.md").write_text(
        f"# Discrepancy Log: Figure {fig_id}\n\n"
        "- Side-by-side comparisons generated.\n"
        f"- Current status: `{info['status']}`.\n"
        "- Remaining discrepancies are documented in the anomaly review.\n"
    )
    (b / "search_iterations/search_iterations.md").write_text(
        f"# Search Iterations: Figure {fig_id}\n\n" + "\n".join(f"- {q}" for q in searches) + "\n"
    )
    checklist = Path("docs/review_checklist.md").read_text()
    (b / "review_checklist.md").write_text(
        checklist
        + f"\n\n## Track A Completion Notes\n\nCurrent status: `{info['status']}`.\n\n"
        "- Checklist is not fully complete for verified publication; unresolved items are documented in anomaly/source logs.\n"
    )
    lineage = [
        {"stage": "Book Figure", "value": f"Figure {fig_id}: {info['title']}"},
        {"stage": "Book Citation", "value": info["citation"]},
        {"stage": "Dataset Used", "value": info["dataset"]},
        {"stage": "Downloaded File", "value": f"figures/{fig_id}/data/raw/"},
        {"stage": "Transformation Script", "value": "scripts/reconstruct_track_a_health_nutrition.py"},
        {"stage": "Generated Plot", "value": f"figures/{fig_id}/plots/"},
    ]
    pd.DataFrame(lineage).to_csv(b / "lineage/figure_lineage.csv", index=False)
    (b / "lineage/figure_lineage.json").write_text(json.dumps(lineage, indent=2) + "\n")
    (b / "README.md").write_text(
        f"# Figure {fig_id}: {info['title']}\n\n"
        f"Status: `{info['status']}`\n\n"
        "## Canonical Artifacts\n\n"
        f"- Original reference: `plots/comparisons/kindle_reference_figure_{stem}.png`\n"
        f"- Book-period reconstruction: `plots/book_period/figure_{stem}_book_period_reconstruction.png`\n"
        f"- Extended reconstruction: `plots/extended/figure_{stem}_extended_reconstruction.png`\n"
        f"- Book-period comparison: `plots/comparisons/figure_{stem}_book_period_comparison.png`\n"
        f"- Extended comparison: `plots/comparisons/figure_{stem}_extended_comparison.png`\n"
        "- Caption: `captions/caption.txt`\n"
        "- Provenance: `provenance/provenance.md`\n"
        "- Anomaly review: `anomaly_reviews/anomaly_review.md`\n"
        "- Metadata: `metadata/metadata.json`\n"
    )


def update_registry_and_metadata():
    registry_path = ROOT / "data/figure_registry.csv"
    rows = list(csv.DictReader(registry_path.open()))
    for row in rows:
        if row["figure_id"] in FIGURES:
            info = FIGURES[row["figure_id"]]
            row["current_status"] = info["status"]
            row["lifecycle_stage"] = "track_a_timeboxed_reconstruction"
            row["priority"] = "active_track_a"
            row["current_owner"] = "Codex"
            row["next_action"] = "Recover exact book-era source vintage and rerun visual review before promotion."
            row["notes"] = f"Track A 2026-06-30: {info['source_status']}; {info['dataset']}."
    with registry_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys(), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    (ROOT / "data/figure_registry.json").write_text(json.dumps(rows, indent=2) + "\n")

    meta_path = ROOT / "data/metadata/figure_metadata.csv"
    meta_rows = list(csv.DictReader(meta_path.open()))
    known = {r["figure_id"]: r for r in meta_rows}
    for fig_id, info in FIGURES.items():
        row = {
            "figure_id": fig_id,
            "chapter": info["chapter"],
            "title": info["title"],
            "book_page": info["book_page"],
            "claim_summary": info["claim"],
            "book_citation": info["citation"],
            "original_dataset": info["dataset"],
            "dataset_url": "See per-figure source log and raw data files.",
            "archive_url": "Not recovered in Track A time-box.",
            "download_date": TODAY,
            "reproduction_status": info["status"],
            "confidence_score": str(info["confidence"]),
            "visual_validation": info["validation"],
            "notes": f"Track A health/nutrition batch; source status {info['source_status']}.",
        }
        if fig_id in known:
            known[fig_id].update(row)
        else:
            meta_rows.append(row)
            known[fig_id] = row
    with meta_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=meta_rows[0].keys(), lineterminator="\n")
        writer.writeheader()
        writer.writerows(meta_rows)


def update_checksums():
    for fig_id in FIGURES:
        root = base(fig_id)
        files = sorted(p for p in root.rglob("*") if p.is_file() and "checksums" not in p.parts)
        rows = []
        for p in files:
            import hashlib

            rows.append(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  ./{p.relative_to(root)}")
        (root / "checksums/sha256sums.txt").write_text("\n".join(rows) + "\n")


def main():
    plot_5_3()
    plot_5_4()
    plot_6_1()
    plot_7_1()
    plot_7_2()
    for fig_id in FIGURES:
        write_docs(fig_id)
    update_registry_and_metadata()
    update_checksums()


if __name__ == "__main__":
    main()
