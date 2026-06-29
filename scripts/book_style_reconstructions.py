#!/usr/bin/env python3
"""
Book-style reconstruction and post-publication extension plots.

The outputs in outputs/book_style/ are publication-facing views:
- book_period: visual match to the book period
- extended: book-period data solid, post-book data dashed/dotted
- validation: original reference crop beside book-period and extended reconstructions
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import textwrap
from datetime import date
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
CLEAN = ROOT / "data" / "clean"
RAW = ROOT / "data" / "raw"
CANDIDATES = ROOT / "data" / "candidates"
ORIGINALS = ROOT / "outputs" / "original_reference"
BOOK_STYLE = ROOT / "outputs" / "book_style"
BOOK_PERIOD = BOOK_STYLE / "book_period"
EXTENDED = BOOK_STYLE / "extended"
VALIDATION = BOOK_STYLE / "validation"
CAPTIONS = BOOK_STYLE / "captions"
ANOMALIES = BOOK_STYLE / "anomaly_reviews"
FIGURE_METADATA = ROOT / "outputs" / "figure_metadata"
PROVENANCE = ROOT / "outputs" / "provenance"
REPORT = ROOT / "outputs" / "report"
CHECKSUMS = ROOT / "data" / "raw_file_checksums.csv"


def ensure_dirs() -> None:
    for path in [BOOK_STYLE, BOOK_PERIOD, EXTENDED, VALIDATION, CAPTIONS, ANOMALIES]:
        path.mkdir(parents=True, exist_ok=True)


def book_axes(ax: plt.Axes) -> None:
    ax.grid(False)
    ax.tick_params(axis="both", colors="#555555", length=6, width=1)
    for side in ["top"]:
        ax.spines[side].set_visible(False)
    for side in ["left", "bottom", "right"]:
        ax.spines[side].set_color("#777777")
        ax.spines[side].set_linewidth(1.1)


def add_note(fig: plt.Figure, text: str) -> None:
    fig.text(0.01, 0.01, text, ha="left", va="bottom", fontsize=7.5, color="#555555")


def wrap_caption(text: str, width: int = 118) -> str:
    return "\n".join(textwrap.fill(paragraph, width=width) for paragraph in text.strip().split("\n\n"))


def load_oil_spills_extended() -> pd.DataFrame:
    raw = pd.read_csv(RAW / "owid_number_oil_spills.csv")
    raw = raw[(raw["Entity"].eq("World")) & raw["Year"].between(1970, 2025)].copy()
    raw["oil_spills_7_plus_tonnes"] = raw["Large oil spills (>700 tonnes)"] + raw["Medium oil spills (7–700 tonnes)"]
    out = raw.rename(columns={"Year": "year"})[
        ["year", "Large oil spills (>700 tonnes)", "Medium oil spills (7–700 tonnes)", "oil_spills_7_plus_tonnes"]
    ].rename(
        columns={
            "Large oil spills (>700 tonnes)": "large_spills_gt_700_tonnes",
            "Medium oil spills (7–700 tonnes)": "medium_spills_7_to_700_tonnes",
        }
    )
    out.to_csv(CLEAN / "figure_10_5_book_style_extended.csv", index=False)
    return out


def load_rmt() -> pd.DataFrame:
    rmt = pd.read_csv(CANDIDATES / "unctad_rmt2020_tanker_trade_selected_years.csv")
    rmt["tanker_trade_billion_tons"] = rmt["tanker_trade_million_tons"] / 1000.0
    return rmt


def load_unctad_annual_tanker_trade() -> pd.DataFrame:
    """Parse the recovered annual UNCTADStat-style tanker-trade mirror.

    The public mirror preserves World rows for `Crude oil loaded` and
    `Other tanker trade loaded`, 1970-2020. Values are in million metric tons.
    """
    path = CANDIDATES / "kaggle_maritime_trading_volumes" / "maritime_volume.csv"
    if not path.exists():
        raise FileNotFoundError(
            "Missing annual tanker-trade mirror at "
            "data/candidates/kaggle_maritime_trading_volumes/maritime_volume.csv"
        )

    raw = pd.read_csv(path, dtype=str)
    year_row = raw.iloc[0]
    year_columns = []
    for col in raw.columns[2:]:
        value = year_row[col]
        if pd.isna(value):
            continue
        try:
            year = int(float(value))
        except ValueError:
            continue
        year_columns.append((col, year))

    rows = raw[
        (raw["Unnamed: 0"].str.strip() == "World")
        & raw["Unnamed: 1"].isin(["Crude oil loaded", "Other tanker trade loaded"])
    ]
    long_rows = []
    for _, row in rows.iterrows():
        for col, year in year_columns:
            value = row[col]
            if pd.isna(value) or str(value).strip() in {"", ".."}:
                continue
            long_rows.append(
                {
                    "year": year,
                    "series": row["Unnamed: 1"],
                    "million_metric_tons": float(value),
                }
            )

    long = pd.DataFrame(long_rows)
    wide = long.pivot_table(index="year", columns="series", values="million_metric_tons", aggfunc="sum").reset_index()
    wide["tanker_trade_million_tons"] = wide["Crude oil loaded"] + wide["Other tanker trade loaded"]
    wide["tanker_trade_billion_tons"] = wide["tanker_trade_million_tons"] / 1000.0
    wide["source"] = "UNCTADStat annual mirror; World crude oil loaded + other tanker trade loaded"
    out = CLEAN / "figure_10_5_annual_tanker_trade_clean.csv"
    wide[
        [
            "year",
            "Crude oil loaded",
            "Other tanker trade loaded",
            "tanker_trade_million_tons",
            "tanker_trade_billion_tons",
            "source",
        ]
    ].to_csv(out, index=False)
    return wide.sort_values("year")


def load_current_wdi_series(path: Path) -> pd.DataFrame:
    row = pd.read_csv(path).iloc[0]
    points = []
    for col in row.index:
        if re.fullmatch(r"\d{4}", str(col)) and pd.notna(row[col]):
            points.append({"year": int(col), "value": float(row[col])})
    return pd.DataFrame(points).sort_values("year")


def load_protected_extended() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    book = pd.read_csv(CLEAN / "figure_10_6_protected_areas_clean.csv")
    land = load_current_wdi_series(CANDIDATES / "world_bank_ER.LND.PTLD.ZS_wld_indicator_row.csv")
    marine = load_current_wdi_series(CANDIDATES / "world_bank_ER.MRN.PTMR.ZS_wld_indicator_row.csv")
    merged = book.copy()
    merged.to_csv(CLEAN / "figure_10_6_book_style_book_period.csv", index=False)
    pd.DataFrame(
        {
            "year": land["year"],
            "current_wdi_terrestrial_protected_area_pct_land": land["value"],
        }
    ).merge(
        pd.DataFrame(
            {
                "year": marine["year"],
                "current_wdi_marine_protected_area_pct_territorial_waters": marine["value"],
            }
        ),
        on="year",
        how="outer",
    ).sort_values("year").to_csv(CLEAN / "figure_10_6_book_style_current_wdi_extension.csv", index=False)
    return book, land, marine


def plot_10_5_book() -> Path:
    spills = pd.read_csv(CLEAN / "figure_10_5_book_style_extended.csv")
    trade = load_unctad_annual_tanker_trade()
    spills_book = spills[spills["year"].between(1970, 2016)]
    trade_book = trade[trade["year"].between(1970, 2016)]

    fig, ax = plt.subplots(figsize=(8.1, 5.0), dpi=180)
    ax.plot(spills_book["year"], spills_book["oil_spills_7_plus_tonnes"], color="#111111", linewidth=2.2)
    ax.set_xlim(1970, 2020)
    ax.set_ylim(0, 125)
    ax.set_xticks([1970, 1975, 1980, 1985, 1990, 1995, 2000, 2005, 2010, 2015, 2020])
    ax.set_yticks([0, 25, 50, 75, 100, 125])
    ax.set_ylabel("Number of oil spills")
    book_axes(ax)

    ax2 = ax.twinx()
    ax2.plot(trade_book["year"], trade_book["tanker_trade_billion_tons"], color="#9a9a9a", linewidth=2.0)
    ax2.set_ylim(1.4, 3.1)
    ax2.set_yticks([1.4, 1.8, 2.2, 2.6, 3.0])
    ax2.set_ylabel("Billion metric tons")
    book_axes(ax2)
    ax2.spines["top"].set_visible(False)

    ax2.text(2004.7, 2.6, "Oil shipped by sea", color="#555555", fontsize=10)
    ax.text(2008, 12, "Oil spills", color="#111111", fontsize=10)
    add_note(fig, "Sources: ITOPF/OWID spill counts; UNCTADStat annual mirror, World crude oil loaded + other tanker trade loaded.")
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    out = BOOK_PERIOD / "figure_10_5_book_period_reconstruction.png"
    fig.savefig(out)
    plt.close(fig)
    return out


def plot_10_5_extended() -> Path:
    spills = pd.read_csv(CLEAN / "figure_10_5_book_style_extended.csv")
    trade = load_unctad_annual_tanker_trade()
    fig, ax = plt.subplots(figsize=(8.6, 5.0), dpi=180)
    spills_book = spills[spills["year"].between(1970, 2016)]
    spills_ext = spills[spills["year"].between(2016, 2025)]
    ax.plot(spills_book["year"], spills_book["oil_spills_7_plus_tonnes"], color="#111111", linewidth=2.2)
    ax.plot(spills_ext["year"], spills_ext["oil_spills_7_plus_tonnes"], color="#111111", linewidth=2.0, linestyle=(0, (2, 2)))
    ax.set_xlim(1970, 2025)
    ax.set_ylim(0, 125)
    ax.set_xticks([1970, 1980, 1990, 2000, 2010, 2020, 2025])
    ax.set_yticks([0, 25, 50, 75, 100, 125])
    ax.set_ylabel("Number of oil spills")
    book_axes(ax)

    ax2 = ax.twinx()
    trade_book = trade[trade["year"].between(1970, 2016)]
    trade_ext = trade[trade["year"].between(2016, 2020)]
    ax2.plot(trade_book["year"], trade_book["tanker_trade_billion_tons"], color="#9a9a9a", linewidth=2.0)
    ax2.plot(trade_ext["year"], trade_ext["tanker_trade_billion_tons"], color="#9a9a9a", linewidth=2.0, linestyle=(0, (2, 2)))
    ax2.set_ylim(1.4, 3.3)
    ax2.set_yticks([1.4, 1.8, 2.2, 2.6, 3.0, 3.2])
    ax2.set_ylabel("Billion metric tons")
    book_axes(ax2)
    ax2.spines["top"].set_visible(False)

    ax2.text(2005, 2.62, "Oil shipped by sea", color="#555555", fontsize=10)
    ax.text(2008, 12, "Oil spills", color="#111111", fontsize=10)
    ax.text(2017.1, 22, "dotted: post-book updates", color="#555555", fontsize=8)
    add_note(fig, "Solid: book period through 2016. Dotted: post-book updates; tanker-trade mirror extends to 2020, spill counts to 2025.")
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    out = EXTENDED / "figure_10_5_extended_reconstruction.png"
    fig.savefig(out)
    plt.close(fig)
    return out


def plot_10_6_book() -> Path:
    book, _, _ = load_protected_extended()
    fig, ax = plt.subplots(figsize=(7.2, 4.7), dpi=180)
    ax.plot(book["year"], book["terrestrial_protected_area_pct_land"], color="#9a9a9a", linewidth=2.0)
    ax.plot(book["year"], book["marine_protected_area_pct_territorial_waters"], color="#111111", linewidth=2.0)
    ax.set_xlim(1990, 2015)
    ax.set_ylim(0, 15.5)
    ax.set_xticks([1990, 1995, 2000, 2005, 2010, 2015])
    ax.set_yticks([0, 5, 10, 15])
    ax.set_ylabel("Percentage of land or water")
    book_axes(ax)
    ax.text(1999.5, 13.8, "Terrestrial protected areas", color="#555555", fontsize=10)
    ax.text(2006.5, 8.7, "Marine protected areas", color="#111111", fontsize=10)
    add_note(fig, "Source: archived World Bank WDI bulk ZIP, 2017-10-12 Wayback snapshot.")
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    out = BOOK_PERIOD / "figure_10_6_book_period_reconstruction.png"
    fig.savefig(out)
    plt.close(fig)
    return out


def plot_10_6_extended() -> Path:
    book, land, marine = load_protected_extended()
    fig, ax = plt.subplots(figsize=(8.4, 4.9), dpi=180)
    ax.plot(book["year"], book["terrestrial_protected_area_pct_land"], color="#9a9a9a", linewidth=2.0)
    ax.plot(book["year"], book["marine_protected_area_pct_territorial_waters"], color="#111111", linewidth=2.0)
    land_ext = land[land["year"].between(2015, 2025)]
    marine_ext = marine[marine["year"].between(2015, 2025)]
    ax.plot(land_ext["year"], land_ext["value"], color="#9a9a9a", linewidth=2.0, linestyle=(0, (2, 2)))
    ax.plot(marine_ext["year"], marine_ext["value"], color="#111111", linewidth=2.0, linestyle=(0, (2, 2)))
    archived_2014 = float(book.loc[book["year"].eq(2014), "marine_protected_area_pct_territorial_waters"].iloc[0])
    current_2015 = float(marine_ext.loc[marine_ext["year"].eq(2015), "value"].iloc[0])
    ax.plot([2014, 2015], [archived_2014, current_2015], color="#111111", linewidth=1.0, linestyle=(0, (1, 4)), alpha=0.45)
    ax.annotate(
        "source revision / rebasing break",
        xy=(2015, current_2015),
        xytext=(2016.1, 6.6),
        fontsize=7.5,
        color="#555555",
        arrowprops={"arrowstyle": "-", "color": "#777777", "linewidth": 0.8},
    )
    ax.set_xlim(1990, 2025)
    ax.set_ylim(0, 18)
    ax.set_xticks([1990, 1995, 2000, 2005, 2010, 2015, 2020, 2025])
    ax.set_yticks([0, 5, 10, 15])
    ax.set_ylabel("Percentage of land or water")
    book_axes(ax)
    ax.text(1999.5, 13.8, "Terrestrial protected areas", color="#555555", fontsize=10)
    ax.text(2005.8, 8.7, "Marine protected areas", color="#111111", fontsize=10)
    ax.text(2017.0, 3.0, "dotted: current WDI successor series", color="#555555", fontsize=8)
    add_note(fig, "Solid: archived WDI 2017 book period. Dotted: current WDI successor values; marine break reflects source revision/rebasing, not plotting error.")
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    out = EXTENDED / "figure_10_6_extended_reconstruction.png"
    fig.savefig(out)
    plt.close(fig)
    return out


def make_comparison(figure_id: str, original: Path, recreated: Path, label: str, suffix: str) -> Path:
    left = Image.open(original).convert("RGB")
    right = Image.open(recreated).convert("RGB")
    panel_w, panel_h = 760, 560
    canvas = Image.new("RGB", (panel_w * 2, panel_h + 56), "white")
    draw = ImageDraw.Draw(canvas)
    draw.text((18, 18), f"Figure {figure_id} original reference", fill="black")
    draw.text((panel_w + 18, 18), label, fill="black")
    left_fit = ImageOps.contain(left, (panel_w - 26, panel_h - 70))
    right_fit = ImageOps.contain(right, (panel_w - 26, panel_h - 70))
    canvas.paste(left_fit, (13, 52))
    canvas.paste(right_fit, (panel_w + 13, 52))
    out = VALIDATION / f"figure_{figure_id.replace('-', '_')}_{suffix}.png"
    canvas.save(out)
    return out


def default_font(size: int) -> ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/Supplemental/Times New Roman.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size=size)
        except OSError:
            continue
    return ImageFont.load_default()


def wrap_text_pixels(text: str, font: ImageFont.ImageFont, max_width: int) -> list[str]:
    lines = []
    for paragraph in text.strip().split("\n\n"):
        words = paragraph.split()
        current = ""
        for word in words:
            candidate = f"{current} {word}".strip()
            bbox = font.getbbox(candidate)
            if bbox[2] - bbox[0] <= max_width or not current:
                current = candidate
            else:
                lines.append(current)
                current = word
        if current:
            lines.append(current)
        lines.append("")
    if lines and lines[-1] == "":
        lines.pop()
    return lines


def add_caption_to_image(image_path: Path, caption: str) -> Path:
    image = Image.open(image_path).convert("RGB")
    width, height = image.size
    margin_x = 28
    margin_y = 18
    title_font = default_font(18)
    body_font = default_font(15)
    label = "Caption"
    body_lines = wrap_text_pixels(caption, body_font, width - (margin_x * 2))
    line_height = 21
    caption_height = margin_y * 2 + 24 + len(body_lines) * line_height
    canvas = Image.new("RGB", (width, height + caption_height), "white")
    canvas.paste(image, (0, 0))
    draw = ImageDraw.Draw(canvas)
    y = height + margin_y
    draw.text((margin_x, y), label, fill="#111111", font=title_font)
    y += 28
    for line in body_lines:
        if line:
            draw.text((margin_x, y), line, fill="#333333", font=body_font)
        y += line_height if line else int(line_height * 0.55)
    out = image_path.with_name(image_path.stem + "_captioned.png")
    canvas.save(out)
    return out


CAPTION_TEXT = {
    "10-5": wrap_caption(
        """
        Figure 10-5: Oil spills, 1970-2016, with post-publication updates. The solid black line shows oil spills of at least 7 tonnes during the book period; the solid gray line shows oil shipped by sea / tanker trade during the book period. Book-period spill data come from ITOPF via OWID/Roser, and tanker-trade data come from a recovered annual UNCTADStat-style mirror for World crude oil loaded plus other tanker trade loaded. Dotted segments show post-publication updates: spill counts extend through 2025 and tanker-trade evidence extends through 2020. The tanker-trade extension is continuous with the recovered annual mirror through 2020, but ITOPF's current source trail indicates UNCTADStat data are available through 2023; the accessible live UNCTAD API was not used for 2021-2023 because its overlap values do not match the book/RMT scale. Remaining uncertainty: the exact Roser 2016r/ITOPF data snapshot and a validated 2021-2023 same-scale UNCTAD export remain unresolved.
        """
    ),
    "10-6": wrap_caption(
        """
        Figure 10-6: Protected areas, 1990-2014, with post-publication updates. Solid lines reproduce the book period from the archived World Bank WDI bulk ZIP captured by the Internet Archive on 2017-10-12; gray is terrestrial protected areas and black is marine protected areas. Dotted lines show current World Bank WDI successor values after the book period, based on newer Protected Planet / WDPA / WD-OECM source metadata. The dotted extension is not continuous with the archived book-period source: the marine series visibly jumps downward because archived WDI reports 12.18% for 2014, while current WDI reports 8.30% for 2014 and 9.01% for 2015. This discontinuity reflects source revision or rebasing, not a plotting error. Remaining uncertainty: a post-2014 release that is methodologically continuous with the archived 2017 WDI book-period values has not been recovered.
        """
    ),
}


ANOMALY_TEXT = {
    "10-5": [
        "Visual review date: " + date.today().isoformat(),
        "",
        "Reviewer-visible issues:",
        "- The extended reconstruction has two different update horizons: spill counts continue through 2025, while validated same-scale tanker-trade evidence stops at 2020.",
        "- ITOPF's current Figure 4 source trail says UNCTADStat tanker-trade data are available through 2023, but the accessible live UNCTAD endpoint fails overlap validation against the book/RMT scale.",
        "- The right-axis series is an updated-equivalent reconstruction rather than a proven exact Roser 2016r data snapshot.",
        "- Solid-to-dotted transition at 2016 is intentional and marks the end of Pinker's book period.",
        "",
        "Disposition:",
        "- Keep the 2021-2023 live UNCTAD candidate out of the publication-facing line until a same-scale source is recovered.",
        "- Caption explicitly states the different update horizons and unresolved exact-source uncertainty.",
    ],
    "10-6": [
        "Visual review date: " + date.today().isoformat(),
        "",
        "Reviewer-visible issues:",
        "- The dotted marine protected-area extension starts below the archived 2014 book-period endpoint.",
        "- The break is caused by source-version disagreement: archived WDI 2017 reports 2014 marine protected areas as 12.18%, while current WDI reports 2014 as 8.30% and 2015 as 9.01%.",
        "- Current WDI metadata uses newer Protected Planet / WDPA / WD-OECM source metadata, so the extension is a successor series rather than a continuous same-source continuation.",
        "- The terrestrial series is much closer across the break, but it still uses current WDI successor metadata after the book period.",
        "",
        "Disposition:",
        "- Do not connect the marine series as a smooth same-source continuation.",
        "- Show a visible break and label the dotted segment as current WDI successor series.",
        "- Caption explicitly says the discontinuity reflects source revision/rebasing, not plotting error.",
    ],
}


def write_caption_and_anomaly_files(outputs: dict[str, dict[str, Path]]) -> None:
    for fig_id in ["10-5", "10-6"]:
        caption_path = CAPTIONS / f"figure_{fig_id.replace('-', '_')}_caption.txt"
        anomaly_path = ANOMALIES / f"figure_{fig_id.replace('-', '_')}_anomaly_review.md"
        caption_path.write_text(CAPTION_TEXT[fig_id] + "\n", encoding="utf-8")
        anomaly_path.write_text("\n".join(ANOMALY_TEXT[fig_id]).rstrip() + "\n", encoding="utf-8")
        outputs[fig_id]["caption"] = caption_path
        outputs[fig_id]["anomaly_review"] = anomaly_path


def update_json_metadata(outputs: dict[str, str]) -> None:
    for fig_id in ["10-5", "10-6"]:
        path = FIGURE_METADATA / f"figure_{fig_id.replace('-', '_')}.json"
        payload = json.loads(path.read_text(encoding="utf-8"))
        payload["book_style_outputs"] = {
            key: str(value).replace(str(ROOT) + "/", "")
            for key, value in outputs[fig_id].items()
        }
        payload["caption_text_file"] = str(outputs[fig_id]["caption"].relative_to(ROOT))
        payload["anomaly_review_file"] = str(outputs[fig_id]["anomaly_review"].relative_to(ROOT))
        payload["caption"] = CAPTION_TEXT[fig_id]
        payload["visual_anomaly_review"] = ANOMALY_TEXT[fig_id]
        if fig_id == "10-6":
            payload["extension_continuity"] = "successor_series_not_continuous"
            payload["extension_caveat"] = (
                "The post-2014 marine protected-area extension visibly jumps downward because the book-period "
                "reconstruction uses archived WDI 2017 values, while the dotted extension uses current WDI successor "
                "data with newer Protected Planet / WDPA / WD-OECM source metadata. The discontinuity reflects source "
                "revision or rebasing, not a plotting error."
            )
            payload.setdefault("unresolved_issues", []).append(
                "Current WDI post-2014 extension is shown as a visibly separated successor series; marine values are not continuous with the archived 2014 book-period release."
            )
        if fig_id == "10-5":
            payload["extension_continuity"] = "continuous_through_validated_source_limit"
            payload["extension_caveat"] = (
                "Post-book spill counts extend through 2025, while validated same-scale tanker-trade evidence extends "
                "through 2020. The accessible live UNCTAD 2021-2023 endpoint is excluded because it does not match the "
                "book/RMT scale on overlapping years."
            )
            payload.setdefault("unresolved_issues", []).append(
                "Annual UNCTADStat mirror recovers tanker trade through 2020; ITOPF-cited 2021-2023 UNCTADStat extension was not admitted because the accessible live API series does not match the book/RMT scale on overlap."
            )
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def append_md(path: Path, heading: str, lines: list[str]) -> None:
    current = path.read_text(encoding="utf-8") if path.exists() else ""
    marker = f"\n## {heading}\n"
    if marker in current:
        current = current.split(marker)[0].rstrip() + "\n"
    current += marker + "\n".join(lines).rstrip() + "\n"
    path.write_text(current, encoding="utf-8")


def update_docs(outputs: dict[str, dict[str, Path]]) -> None:
    today = date.today().isoformat()
    append_md(
        PROVENANCE / "figure_10_5.md",
        "Book-Style Reconstruction Update",
        [
            f"- Date: {today}",
            f"- Book-period reconstruction: `{outputs['10-5']['book_period'].relative_to(ROOT)}`.",
            f"- Extended reconstruction: `{outputs['10-5']['extended'].relative_to(ROOT)}`.",
            f"- Original-vs-book comparison: `{outputs['10-5']['book_comparison'].relative_to(ROOT)}`.",
            f"- Original-vs-extended comparison: `{outputs['10-5']['extended_comparison'].relative_to(ROOT)}`.",
            f"- Captioned original-vs-book comparison: `{outputs['10-5']['book_comparison_captioned'].relative_to(ROOT)}`.",
            f"- Captioned original-vs-extended comparison: `{outputs['10-5']['extended_comparison_captioned'].relative_to(ROOT)}`.",
            f"- Caption: `{outputs['10-5']['caption'].relative_to(ROOT)}`.",
            f"- Visual anomaly review: `{outputs['10-5']['anomaly_review'].relative_to(ROOT)}`.",
            "- The main reconstruction now uses ITOPF/OWID spill counts and an annual UNCTADStat mirror for World crude oil loaded plus other tanker trade loaded.",
            "- Update period: book-period solid lines run through 2016; post-book dotted lines show tanker trade through 2020 and spill counts through 2025.",
            "- ITOPF's current Figure 4 source trail says 1970-1999 tanker trade comes from UNCTADStat updated 2022 and 2000-2023 from UNCTADStat updated 2025. The public mirror recovers annual values through 2020. The accessible live UNCTAD API was investigated for 2021-2023 but rejected from the main plot because overlap values are not on the same scale as ITOPF/RMT/book values.",
        ],
    )
    append_md(
        PROVENANCE / "figure_10_6.md",
        "Book-Style Reconstruction Update",
        [
            f"- Date: {today}",
            f"- Book-period reconstruction: `{outputs['10-6']['book_period'].relative_to(ROOT)}`.",
            f"- Extended reconstruction: `{outputs['10-6']['extended'].relative_to(ROOT)}`.",
            f"- Original-vs-book comparison: `{outputs['10-6']['book_comparison'].relative_to(ROOT)}`.",
            f"- Original-vs-extended comparison: `{outputs['10-6']['extended_comparison'].relative_to(ROOT)}`.",
            f"- Captioned original-vs-book comparison: `{outputs['10-6']['book_comparison_captioned'].relative_to(ROOT)}`.",
            f"- Captioned original-vs-extended comparison: `{outputs['10-6']['extended_comparison_captioned'].relative_to(ROOT)}`.",
            f"- Caption: `{outputs['10-6']['caption'].relative_to(ROOT)}`.",
            f"- Visual anomaly review: `{outputs['10-6']['anomaly_review'].relative_to(ROOT)}`.",
            "- The book-period reconstruction preserves the archived WDI source and restyles the chart to match the book.",
            "- Update period: book-period solid lines run through 2014; post-book dotted lines use current WDI successor values through 2025 and are dashed to avoid implying book-period provenance.",
            "- The marine extension is visibly separated and labeled as a current WDI successor series because current WDI revises/rebases the 2014 marine value downward relative to the archived WDI book-period release.",
        ],
    )
    append_md(
        REPORT / "enlightenment_now_poc_report.md",
        "Book-Style Reconstruction Addendum",
        [
            f"Generated: {today}",
            "",
            "- Figure 10-5 now has a book-style dual-axis reconstruction using oil-spill counts and annual UNCTADStat mirror tanker-trade evidence.",
            "- Figure 10-5 post-book extension uses dashed spill data through 2025 and dashed annual tanker-trade evidence through 2020. The live UNCTAD 2021-2023 endpoint remains excluded because it fails overlap validation.",
            "- Figure 10-6 now has a grayscale direct-label book-style reconstruction from archived WDI.",
            "- Figure 10-6 post-book extension uses dashed current WDI successor values after 2014; the marine series has a visible release discontinuity and is labeled as a current WDI successor series.",
            f"- Latest book-period comparisons: `{outputs['10-5']['book_comparison'].relative_to(ROOT)}` and `{outputs['10-6']['book_comparison'].relative_to(ROOT)}`.",
            f"- Latest extended comparisons: `{outputs['10-5']['extended_comparison'].relative_to(ROOT)}` and `{outputs['10-6']['extended_comparison'].relative_to(ROOT)}`.",
            f"- Captioned comparison images: `{outputs['10-5']['extended_comparison_captioned'].relative_to(ROOT)}` and `{outputs['10-6']['extended_comparison_captioned'].relative_to(ROOT)}`.",
            f"- Captions: `{outputs['10-5']['caption'].relative_to(ROOT)}` and `{outputs['10-6']['caption'].relative_to(ROOT)}`.",
            f"- Visual anomaly reviews: `{outputs['10-5']['anomaly_review'].relative_to(ROOT)}` and `{outputs['10-6']['anomaly_review'].relative_to(ROOT)}`.",
        ],
    )


def refresh_checksums() -> None:
    rows = []
    for base in [ROOT / "data" / "raw", CANDIDATES, CLEAN]:
        for path in sorted(base.glob("*")):
            if not path.is_file():
                continue
            digest = hashlib.sha256()
            with path.open("rb") as handle:
                for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                    digest.update(chunk)
            rows.append(
                {
                    "path": str(path.relative_to(ROOT)),
                    "sha256": digest.hexdigest(),
                    "bytes": path.stat().st_size,
                    "modified_date": date.fromtimestamp(path.stat().st_mtime).isoformat(),
                }
            )
    with CHECKSUMS.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["path", "sha256", "bytes", "modified_date"])
        writer.writeheader()
        writer.writerows(rows)
    (ROOT / "data" / "raw_file_checksums.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")


def main() -> None:
    ensure_dirs()
    load_oil_spills_extended()
    outputs = {
        "10-5": {
            "book_period": plot_10_5_book(),
            "extended": plot_10_5_extended(),
        },
        "10-6": {
            "book_period": plot_10_6_book(),
            "extended": plot_10_6_extended(),
        },
    }
    outputs["10-5"]["book_comparison"] = make_comparison(
        "10-5",
        ORIGINALS / "figure_10_5_original_crop.png",
        outputs["10-5"]["book_period"],
        "Book-period reconstruction",
        "book_style_comparison",
    )
    outputs["10-5"]["extended_comparison"] = make_comparison(
        "10-5",
        ORIGINALS / "figure_10_5_original_crop.png",
        outputs["10-5"]["extended"],
        "Extended reconstruction",
        "extended_comparison",
    )
    outputs["10-6"]["book_comparison"] = make_comparison(
        "10-6",
        ORIGINALS / "figure_10_6_original_crop.png",
        outputs["10-6"]["book_period"],
        "Book-period reconstruction",
        "book_style_comparison",
    )
    outputs["10-6"]["extended_comparison"] = make_comparison(
        "10-6",
        ORIGINALS / "figure_10_6_original_crop.png",
        outputs["10-6"]["extended"],
        "Extended reconstruction",
        "extended_comparison",
    )
    write_caption_and_anomaly_files(outputs)
    for fig_id in ["10-5", "10-6"]:
        outputs[fig_id]["book_comparison_captioned"] = add_caption_to_image(
            outputs[fig_id]["book_comparison"],
            CAPTION_TEXT[fig_id],
        )
        outputs[fig_id]["extended_comparison_captioned"] = add_caption_to_image(
            outputs[fig_id]["extended_comparison"],
            CAPTION_TEXT[fig_id],
        )
    update_json_metadata(outputs)
    update_docs(outputs)
    refresh_checksums()
    print("Book-style reconstructions complete")
    for fig_id, paths in outputs.items():
        print(fig_id, {key: str(value.relative_to(ROOT)) for key, value in paths.items()})


if __name__ == "__main__":
    main()
