from __future__ import annotations

import csv
import hashlib
import json
import shutil
import subprocess
from datetime import date
from pathlib import Path
from urllib.request import Request, urlopen

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
TODAY = date.today().isoformat()
PDF_SOURCE = Path("/tmp/enlightenment_now_cloudfront.pdf")
PDF_PAGES = Path("/tmp/pinker_pages")
TMP_SOURCES = Path("/tmp/track_c_sources")


FIGURES = {
    "9-1": {
        "title": "International inequality, 1820-2013",
        "chapter": "9",
        "year_range": "1820-2013",
        "status": "manual_review_needed",
        "confidence": 0.35,
        "visual_validation": "blocked",
        "source": (
            "International inequality: OECD Clio Infra Project, Moatsos et al. 2014; "
            "data are for market household income across countries. Population-weighted "
            "international inequality: Milanovic 2012; data for 2012 and 2013 provided "
            "by Branko Milanovic, personal communication."
        ),
        "page": "Preview PDF page image page-09; Kindle-equivalent figure/source inspected",
        "claim": "Unweighted international inequality rose historically while population-weighted international inequality fell after the late twentieth century.",
        "source_status": "Original Clio Infra/Moatsos and Milanovic personal-communication data were not recovered as inspectable files.",
        "next_action": "Recover OECD Clio Infra Moatsos et al. 2014 market household income Gini data and Milanovic 2012 weighted international inequality update through 2013.",
        "reference_page": "page-09.png",
        "crop": (80, 675, 955, 1390),
    },
    "9-2": {
        "title": "Global inequality, 1820-2011",
        "chapter": "9",
        "year_range": "1820-2011",
        "status": "manual_review_needed",
        "confidence": 0.35,
        "visual_validation": "blocked",
        "source": (
            "Milanovic 2016, fig. 3.1. The left-hand curve shows 1990 "
            "international dollars of disposable income per capita; the right-hand "
            "curve shows 2005 international dollars, and combines household surveys "
            "of per capita disposable income and consumption."
        ),
        "page": "Preview PDF page image page-10; Kindle-equivalent figure/source inspected",
        "claim": "Estimated global interpersonal Gini rose into the mid-twentieth century and declined in the 2005-dollar household-survey series after about 2000.",
        "source_status": "Milanovic 2016 figure 3.1 underlying table was not recovered as an inspectable data file.",
        "next_action": "Recover Milanovic 2016 figure 3.1 spreadsheet or publisher/author supplementary data.",
        "reference_page": "page-10.png",
        "crop": (65, 95, 940, 725),
    },
    "9-3": {
        "title": "Inequality, UK and US, 1688-2013",
        "chapter": "9",
        "year_range": "1688-2013",
        "status": "manual_review_needed",
        "confidence": 0.35,
        "visual_validation": "blocked",
        "source": "Milanovic 2016, fig. 2.1, disposable income per capita.",
        "page": "Preview PDF page image page-10; Kindle-equivalent figure/source inspected",
        "claim": "Long-run UK and US Gini series rose, fell in the mid-twentieth century, and rose again in recent decades.",
        "source_status": "Milanovic 2016 figure 2.1 underlying table was not recovered as an inspectable data file.",
        "next_action": "Recover Milanovic 2016 figure 2.1 spreadsheet, including UK/England and US disposable-income-per-capita Gini series.",
        "reference_page": "page-10.png",
        "crop": (65, 750, 940, 1385),
    },
    "9-4": {
        "title": "Social spending, OECD countries, 1880-2016",
        "chapter": "9",
        "year_range": "1880-2016",
        "status": "updated_equivalent",
        "confidence": 0.78,
        "visual_validation": "good",
        "source": (
            "Our World in Data, Ortiz-Ospina & Roser 2016b, based on data from "
            "Lindert 2004 and OECD 1985, 2014, 2017."
        ),
        "page": "Preview PDF page image page-11; Kindle-equivalent figure/source inspected",
        "claim": "Public social spending rose across market-democratic OECD countries from near-zero late nineteenth-century levels to substantial shares of GDP.",
        "source_status": "Current OWID grapher successor located; exact 2016b/2017 OWID source snapshot was not recovered.",
        "next_action": "For verification, recover the exact OWID Ortiz-Ospina & Roser 2016b/2017 chart data snapshot; otherwise keep updated_equivalent status.",
        "reference_page": "page-11.png",
        "crop": (90, 90, 930, 710),
    },
    "9-5": {
        "title": "Income gains, 1988-2008",
        "chapter": "9",
        "year_range": "1988-2008",
        "status": "manual_review_needed",
        "confidence": 0.35,
        "visual_validation": "blocked",
        "source": "Milanovic 2016, fig. 1.3.",
        "page": "Preview PDF page image page-11; Kindle-equivalent figure/source inspected",
        "claim": "The global growth-incidence curve from 1988 to 2008 has the familiar elephant shape: strong middle-percentile gains, weak upper-middle gains, and high top-percentile gains.",
        "source_status": "Milanovic 2016 figure 1.3 underlying percentile-growth data were not recovered as an inspectable data file.",
        "next_action": "Recover Milanovic 2016 figure 1.3 or Lakner-Milanovic global growth-incidence spreadsheet for 1988-2008.",
        "reference_page": "page-11.png",
        "crop": (65, 720, 940, 1385),
    },
}


def download(url: str, dest: Path) -> None:
    if dest.exists() and dest.stat().st_size > 0:
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = Request(url, headers={"User-Agent": "Mozilla/5.0 pinker-charts-reconstruction"})
    with urlopen(req, timeout=60) as response:
        dest.write_bytes(response.read())


def ensure_dirs(fig_id: str) -> Path:
    base = ROOT / "figures" / fig_id
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
        (base / part).mkdir(parents=True, exist_ok=True)
    return base


def crop_reference(fig_id: str) -> Path:
    info = FIGURES[fig_id]
    page = PDF_PAGES / info["reference_page"]
    out = ensure_dirs(fig_id) / f"plots/comparisons/kindle_reference_figure_{fig_id.replace('-', '_')}.png"
    Image.open(page).convert("RGB").crop(info["crop"]).save(out)
    return out


def trim_image(path: Path) -> Image.Image:
    image = Image.open(path).convert("RGB")
    bg = Image.new("RGB", image.size, "white")
    diff = ImageChops.difference(image, bg)
    bbox = diff.getbbox()
    return image.crop(bbox) if bbox else image


def save_side_by_side(reference: Path, recreated: Path, output: Path, title: str) -> None:
    ref = trim_image(reference)
    rec = trim_image(recreated)
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
    draw.text((left_x + panel_w // 2, label_y), "Book reference", fill="black", anchor="ma", font=label_font)
    draw.text((right_x + panel_w // 2, label_y), "Recreated/status", fill="black", anchor="ma", font=label_font)
    paste_fit(ref, left_x, title_h + header_h)
    paste_fit(rec, right_x, title_h + header_h)
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output)


def placeholder_plot(fig_id: str, extended: bool) -> Path:
    info = FIGURES[fig_id]
    base = ensure_dirs(fig_id)
    folder = "extended" if extended else "book_period"
    suffix = "extended_reconstruction" if extended else "book_period_reconstruction"
    out = base / f"plots/{folder}/figure_{fig_id.replace('-', '_')}_{suffix}.png"
    fig, ax = plt.subplots(figsize=(8.4, 5.2), dpi=180)
    ax.axis("off")
    title = f"Figure {fig_id}: {info['title']}"
    ax.text(0.02, 0.88, title, fontsize=15, weight="bold", transform=ax.transAxes)
    ax.text(
        0.02,
        0.70,
        "No reconstruction plotted.",
        fontsize=13,
        weight="bold",
        transform=ax.transAxes,
    )
    ax.text(
        0.02,
        0.55,
        "Original underlying data were not recovered in this batch.\n"
        "The project rule forbids reconstructing from digitized chart values,\n"
        "so this panel records a targeted source-recovery blocker.",
        fontsize=11,
        transform=ax.transAxes,
        linespacing=1.35,
    )
    ax.text(0.02, 0.29, f"Needed: {info['next_action']}", fontsize=9.5, transform=ax.transAxes, wrap=True)
    ax.text(0.02, 0.12, f"Source line inspected: {info['source']}", fontsize=8.5, transform=ax.transAxes, wrap=True)
    fig.tight_layout()
    fig.savefig(out, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return out


def plot_9_4() -> tuple[Path, Path]:
    base = ensure_dirs("9-4")
    raw_csv = base / "data/raw/social-spending-oecd-longrun.csv"
    meta_json = base / "data/raw/social-spending-oecd-longrun.metadata.json"
    if not raw_csv.exists():
        shutil.copy2(TMP_SOURCES / "social-spending-oecd-longrun.csv", raw_csv)
    if not meta_json.exists():
        shutil.copy2(TMP_SOURCES / "social-spending-oecd-longrun.metadata.json", meta_json)

    df = pd.read_csv(raw_csv)
    value_col = "Public social expenditure as a share of GDP"
    selected = [
        "Greece",
        "Canada",
        "Australia",
        "Japan",
        "United States",
        "Sweden",
        "Italy",
        "Germany",
        "Netherlands",
        "France",
        "United Kingdom",
    ]
    clean = df[df["Entity"].isin(selected)].rename(columns={value_col: "public_social_expenditure_pct_gdp"})
    clean.to_csv(base / "data/clean/figure_9_4_extended_clean.csv", index=False)
    clean[clean["Year"] <= 2016].to_csv(base / "data/clean/figure_9_4_book_period_clean.csv", index=False)

    styles = {
        "France": dict(color="0.65", linestyle="-", linewidth=2.3),
        "Italy": dict(color="0.10", linestyle=":", linewidth=2.2),
        "Germany": dict(color="0.55", linestyle="-.", linewidth=2.1),
        "Netherlands": dict(color="0.72", linestyle="-", linewidth=2.0),
        "Greece": dict(color="0.20", linestyle="--", linewidth=2.0),
        "United Kingdom": dict(color="0.28", linestyle="-", linewidth=2.1),
        "United States": dict(color="0.35", linestyle="-", linewidth=2.0),
        "Australia": dict(color="0.55", linestyle="-", linewidth=2.0),
        "Canada": dict(color="0.45", linestyle="-", linewidth=2.0),
        "Japan": dict(color="0.15", linestyle="-", linewidth=2.1),
        "Sweden": dict(color="0.05", linestyle="-", linewidth=2.3),
    }

    labels = {
        "Sweden": (1972, 28.0, "Sweden"),
        "France": (2009, 33.0, "France"),
        "Italy": (2014, 29.3, "Italy"),
        "Germany": (2012, 26.0, "Germany"),
        "Netherlands": (2014, 24.7, "Netherlands"),
        "Greece": (2011, 22.9, "Greece"),
        "United Kingdom": (2014, 21.4, "UK"),
        "United States": (2014, 19.6, "US"),
        "Australia": (2014, 18.2, "Australia"),
        "Canada": (2011, 15.6, "Canada"),
        "Japan": (1992, 11.0, "Japan"),
    }

    def draw(out: Path, extended: bool) -> None:
        fig, ax = plt.subplots(figsize=(8.4, 5.2), dpi=180)
        for entity in selected:
            sub = clean[clean["Entity"] == entity].sort_values("Year")
            book = sub[sub["Year"] <= 2016]
            ax.plot(book["Year"], book["public_social_expenditure_pct_gdp"], **styles[entity])
            if extended:
                ext = sub[sub["Year"] > 2016]
                if len(ext):
                    style = styles[entity].copy()
                    style["linestyle"] = "--"
                    style["linewidth"] = max(1.4, style["linewidth"] - 0.3)
                    style["alpha"] = 0.75
                    ax.plot(ext["Year"], ext["public_social_expenditure_pct_gdp"], **style)
        ax.set_xlim(1880, 2025 if extended else 2020)
        ax.set_ylim(0, 35)
        ax.set_yticks(range(0, 36, 5))
        ax.set_xticks(list(range(1880, 2021, 10)))
        ax.set_ylabel("Percentage of GDP")
        ax.set_xlabel("")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.grid(False)
        for _, (x, y, text) in labels.items():
            if x <= (2024 if extended else 2016):
                ax.text(x, y, text, fontsize=9.3, color="0.15")
        note = (
            "Current OWID successor data through 2016; exact Ortiz-Ospina & Roser 2016b snapshot not recovered."
            if not extended
            else "Solid segments show book period through 2016; dashed segments use current OWID/OECD successor data after 2016."
        )
        ax.text(0, -0.18, note, transform=ax.transAxes, fontsize=7.4, va="top")
        fig.tight_layout()
        fig.savefig(out, bbox_inches="tight", facecolor="white")
        plt.close(fig)

    book_out = base / "plots/book_period/figure_9_4_book_period_reconstruction.png"
    ext_out = base / "plots/extended/figure_9_4_extended_reconstruction.png"
    draw(book_out, extended=False)
    draw(ext_out, extended=True)
    return book_out, ext_out


def write_text_files(fig_id: str) -> None:
    info = FIGURES[fig_id]
    base = ensure_dirs(fig_id)
    caption = (
        f"Figure {fig_id}: {info['title']}. Source line inspected from the Chapter 9 preview PDF: "
        f"{info['source']} "
    )
    if fig_id == "9-4":
        caption += (
            "The reconstruction uses the current Our World in Data grapher successor "
            "`social-spending-oecd-longrun`, downloaded 2026-06-30, and is classified "
            "as an updated equivalent because the exact 2016b/2017 OWID snapshot was not recovered. "
            "Dashed segments in the extended plot show post-2016 successor data."
        )
    else:
        caption += (
            "No recreated data series is plotted because the original underlying data file was not recovered, "
            "and this project does not reconstruct from digitized chart values."
        )
    (base / "captions/caption.txt").write_text(caption + "\n", encoding="utf-8")

    provenance = f"""# Figure {fig_id} Provenance

## Evidence

- Title: {info['title']}
- Source line: {info['source']}
- Figure/source inspected from: {info['page']}
- Claim summary: {info['claim']}

## Source Recovery Result

{info['source_status']}

## Reconstruction

"""
    if fig_id == "9-4":
        provenance += """The book-period reconstruction uses the current Our World in Data grapher `social-spending-oecd-longrun` with values through 2016. The current metadata cites OECD (2025), OECD (1985), and Lindert (2004), and describes the same broad source family as Pinker's cited Ortiz-Ospina & Roser 2016b chart. Because the exact book-era OWID snapshot was not recovered, the status is `updated_equivalent`, not `verified_reproduction`.

The extension plots post-2016 values available in the current grapher as dashed successor segments.
"""
    else:
        provenance += """No reconstruction data file was accepted. The generated comparison images include a status panel instead of a reconstructed chart. This is intentional: the source-recovery rule forbids using digitized values from the book chart as reconstruction data.
"""
    provenance += f"\n## Next Action\n\n{info['next_action']}\n"
    (base / "provenance/provenance.md").write_text(provenance, encoding="utf-8")

    source_log = f"""# Figure {fig_id} Source Log

Date: {TODAY}

## Accepted Sources

"""
    if fig_id == "9-4":
        source_log += """- Current OWID grapher: `https://ourworldindata.org/grapher/social-spending-oecd-longrun.csv?v=1&csvType=full&useColumnShortNames=false`
- Current OWID grapher metadata: `https://ourworldindata.org/grapher/social-spending-oecd-longrun.metadata.json?v=1&csvType=full&useColumnShortNames=false`

Accepted as successor/update only. The book-era chart source was Ortiz-Ospina & Roser 2016b based on Lindert 2004 and OECD 1985/2014/2017; the current file cites OECD 2025, OECD 1985, and Lindert 2004.
"""
    else:
        source_log += "- None accepted for reconstruction.\n"
    source_log += f"""
## Rejected Or Unresolved

- The book/reference chart itself was not digitized and was not used as data.
- Exact original source data remain unresolved where noted.

## Targeted Recovery

{info['next_action']}
"""
    (base / "source_logs/source_log.md").write_text(source_log, encoding="utf-8")

    search_iterations = f"""# Figure {fig_id} Search Iterations

Date: {TODAY}

- Inspected Chapter 9 preview PDF page image and source line.
- Searched public web for exact title/source and likely data family.
- For 9-4, located current OWID grapher successor and metadata.
- For Milanovic/Clio Infra figures, found source references but did not recover an inspectable raw spreadsheet/table in this batch.
"""
    (base / "search_iterations/search_iterations.md").write_text(search_iterations, encoding="utf-8")

    discrepancy = f"""# Figure {fig_id} Discrepancy Log

"""
    if fig_id == "9-4":
        discrepancy += """- Book-period plot uses current OWID successor data, not the exact 2016b/2017 source snapshot.
- Styling, line labels, and grayscale/dash choices are approximate.
- Post-2016 extension is methodologically continuous with current OWID but may reflect OECD/SOCX revisions.
"""
    else:
        discrepancy += """- Critical source blocker: no accepted underlying data file was recovered.
- Comparison image therefore shows a source-recovery status panel instead of a recreated chart.
- This avoids the prohibited use of digitized values from the book chart as reconstruction data.
"""
    (base / "discrepancy_logs/discrepancy_log.md").write_text(discrepancy, encoding="utf-8")

    anomaly = f"""# Figure {fig_id} Anomaly Review

## Visible Differences

"""
    if fig_id == "9-4":
        anomaly += """- The recreated chart visually resembles the book figure, including the multi-country upward trajectories and crowded right-edge labels.
- Some line endpoints and styles differ because the current OWID successor data include later OECD revisions.
- The extended comparison clearly uses dashed post-2016 successor segments.

## Reviewer Challenge

- Pinker would likely ask whether the exact Ortiz-Ospina & Roser 2016b source snapshot has been recovered. It has not.
- A data journalist would ask whether post-2016 values are revised OECD data. They are current OWID/OECD successor values.
- A peer reviewer would ask for an archived 2017 OWID file before verification. That remains the next action.
- A skeptical reader would notice small endpoint/label differences; these are documented as source-version and styling differences.
"""
    else:
        anomaly += """- The book reference appears on the left, but the recreated/status panel on the right is not a chart.
- This is a deliberate publication blocker marker: accepted raw data were not recovered and digitized chart values were not used.

## Reviewer Challenge

- Pinker would likely ask why the original Milanovic/Clio Infra data were not used. They were sought but not recovered as inspectable files in this batch.
- A data journalist would ask whether the chart was digitized. It was not.
- A peer reviewer would require the original spreadsheet/table before accepting a reconstruction.
- A skeptical reader would immediately notice the missing recreated line; the caption and panel explain the source blocker.
"""
    anomaly += f"""
## Confidence

- Overall confidence: {'medium' if fig_id == '9-4' else 'low/source-blocked'}
- Book reconstruction: {'updated equivalent' if fig_id == '9-4' else 'not attempted without accepted data'}
- Extension: {'current OWID successor after 2016' if fig_id == '9-4' else 'not available'}
- Source provenance: {info['source_status']}
- Recommended next action: {info['next_action']}
"""
    (base / "anomaly_reviews/anomaly_review.md").write_text(anomaly, encoding="utf-8")

    checklist_status = "updated_equivalent" if fig_id == "9-4" else "manual_review_needed"
    checklist = f"""# Figure Acceptance Checklist

## Figure

- Figure ID: {fig_id}
- Title: {info['title']}
- Reviewer: Codex
- Review date: {TODAY}
- Current status: {checklist_status}

## Phase 1 - Evidence Review

- [x] Kindle/preview figure inspected.
- [x] Title extracted.
- [x] Caption/source note extracted.
- [x] Surrounding discussion reviewed at the figure page level.
- [x] Bibliography/source mapping documented or unresolved.

## Phase 2 - Source Review

- [{'x' if fig_id == '9-4' else ' '}] Original/successor publication located.
- [{'x' if fig_id == '9-4' else ' '}] Dataset provenance documented.
- [x] Archive/search notes documented.
- [{'x' if fig_id == '9-4' else ' '}] Successor datasets evaluated.
- [x] Substitution or source blocker explained.

## Phase 3 - Reconstruction Review

- [{'x' if fig_id == '9-4' else ' '}] Reconstruction uses legitimate data.
- [x] No digitized figure values used as reconstruction data.
- [{'x' if fig_id == '9-4' else ' '}] Transformation code is reproducible.
- [{'x' if fig_id == '9-4' else ' '}] Book-period comparison generated.
- [x] Remaining book-period discrepancies explained.

## Phase 4 - Extension Review

- [{'x' if fig_id == '9-4' else ' '}] Later data searched and documented.
- [{'x' if fig_id == '9-4' else 'N/A'}] Extension completed or absence explained.
- [{'x' if fig_id == '9-4' else 'N/A'}] Extended comparison generated where available.

## Phase 5 - Reviewer Challenge

- [x] Reviewer questions answered in anomaly review.

## Final Gate - Editorial Review

- [x] Comparison image opened and visually scanned.
- [x] Ten-second-obvious issues corrected or explicitly explained.
- [x] No unexplained Critical/Major issues remain; source blockers are explicit.

## Repository Updates

- [x] Caption written.
- [x] Anomaly review written.
- [x] Provenance/source/discrepancy/search logs updated.
- [x] Metadata updated.

## Final Decision

- [{'x' if fig_id == '9-4' else ' '}] Accepted as `updated_equivalent`.
- [{'x' if fig_id != '9-4' else ' '}] Classified as `manual_review_needed`.
"""
    (base / "review_checklist.md").write_text(checklist, encoding="utf-8")

    readme = f"""# Figure {fig_id}: {info['title']}

Status: `{info['status']}`

This directory was created for Track C on {TODAY}. See `provenance/provenance.md`,
`source_logs/source_log.md`, and `anomaly_reviews/anomaly_review.md` for the source
recovery result and visual review.
"""
    (base / "README.md").write_text(readme, encoding="utf-8")


def write_metadata_and_lineage(fig_id: str) -> None:
    info = FIGURES[fig_id]
    base = ensure_dirs(fig_id)
    metadata = {
        "figure_id": fig_id,
        "title": info["title"],
        "chapter": info["chapter"],
        "book_page": info["page"],
        "year_range": info["year_range"],
        "claim_summary": info["claim"],
        "book_citation": info["source"],
        "original_dataset": info["source_status"],
        "dataset_url": (
            "https://ourworldindata.org/grapher/social-spending-oecd-longrun.csv?v=1&csvType=full&useColumnShortNames=false"
            if fig_id == "9-4"
            else ""
        ),
        "archive_url": "",
        "download_date": TODAY,
        "reproduction_status": info["status"],
        "confidence_score": info["confidence"],
        "visual_validation": info["visual_validation"],
        "notes": info["next_action"],
        "canonical_artifacts": {
            "kindle_reference": f"figures/{fig_id}/plots/comparisons/kindle_reference_figure_{fig_id.replace('-', '_')}.png",
            "book_period_reconstruction": f"figures/{fig_id}/plots/book_period/figure_{fig_id.replace('-', '_')}_book_period_reconstruction.png",
            "extended_reconstruction": f"figures/{fig_id}/plots/extended/figure_{fig_id.replace('-', '_')}_extended_reconstruction.png",
            "book_period_comparison": f"figures/{fig_id}/plots/comparisons/figure_{fig_id.replace('-', '_')}_book_period_comparison.png",
            "extended_comparison": f"figures/{fig_id}/plots/comparisons/figure_{fig_id.replace('-', '_')}_extended_comparison.png",
        },
    }
    (base / "metadata/metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")

    lineage_rows = [
        {
            "figure_id": fig_id,
            "artifact": "book_reference",
            "source": "Chapter 9 preview PDF page crop",
            "status": "reference_only",
        }
    ]
    if fig_id == "9-4":
        lineage_rows.extend(
            [
                {
                    "figure_id": fig_id,
                    "artifact": "book_period_reconstruction",
                    "source": "current OWID social-spending-oecd-longrun values through 2016",
                    "status": "updated_equivalent",
                },
                {
                    "figure_id": fig_id,
                    "artifact": "extended_reconstruction",
                    "source": "current OWID social-spending-oecd-longrun values through 2024",
                    "status": "successor_extension",
                },
            ]
        )
    else:
        lineage_rows.append(
            {
                "figure_id": fig_id,
                "artifact": "status_panel",
                "source": "no accepted reconstruction data",
                "status": "manual_review_needed",
            }
        )
    with (base / "lineage/figure_lineage.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["figure_id", "artifact", "source", "status"])
        writer.writeheader()
        writer.writerows(lineage_rows)
    (base / "lineage/figure_lineage.json").write_text(json.dumps(lineage_rows, indent=2) + "\n", encoding="utf-8")


def update_registry() -> None:
    registry_path = ROOT / "data/figure_registry.csv"
    rows = list(csv.DictReader(registry_path.open(encoding="utf-8")))
    by_id = {row["figure_id"]: row for row in rows}
    for fig_id, info in FIGURES.items():
        row = by_id[fig_id]
        row["current_status"] = info["status"]
        row["lifecycle_stage"] = (
            "updated_equivalent_with_successor_extension"
            if fig_id == "9-4"
            else "source_recovery_blocked_no_reconstruction"
        )
        row["priority"] = "active_high" if fig_id != "9-4" else "completed_monitor"
        row["current_owner"] = "Codex"
        row["next_action"] = info["next_action"]
        row["notes"] = (
            "Processed in Track C on 2026-06-30. "
            + info["source_status"]
            + " No digitized chart values were used."
        )
    with registry_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    (ROOT / "data/figure_registry.json").write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")


def update_metadata_csv() -> None:
    path = ROOT / "data/metadata/figure_metadata.csv"
    rows = list(csv.DictReader(path.open(encoding="utf-8")))
    by_id = {row["figure_id"]: row for row in rows}
    fieldnames = list(rows[0].keys())
    for fig_id, info in FIGURES.items():
        row = by_id.get(fig_id, {k: "" for k in fieldnames})
        row.update(
            {
                "figure_id": fig_id,
                "chapter": info["chapter"],
                "title": info["title"],
                "book_page": info["page"],
                "claim_summary": info["claim"],
                "book_citation": info["source"],
                "original_dataset": info["source_status"],
                "dataset_url": (
                    "https://ourworldindata.org/grapher/social-spending-oecd-longrun.csv?v=1&csvType=full&useColumnShortNames=false"
                    if fig_id == "9-4"
                    else ""
                ),
                "archive_url": "",
                "download_date": TODAY,
                "reproduction_status": info["status"],
                "confidence_score": str(info["confidence"]),
                "visual_validation": info["visual_validation"],
                "notes": info["next_action"],
            }
        )
        by_id[fig_id] = row
    ordered = rows + [by_id[fig_id] for fig_id in FIGURES if fig_id not in {r["figure_id"] for r in rows}]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(ordered)


def write_report() -> None:
    path = ROOT / "reports/track_c_inequality_social_spending_summary.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Track C: Inequality and Social Spending Summary",
        "",
        f"Date: {TODAY}",
        "Branch: `track-c-inequality-social-spending`",
        "",
        "## Results",
        "",
        "| Figure | Status | Result |",
        "| --- | --- | --- |",
    ]
    for fig_id, info in FIGURES.items():
        result = (
            "Current OWID successor reconstructed through 2016 with dashed post-2016 extension; exact book-era OWID snapshot still unresolved."
            if fig_id == "9-4"
            else "Source line and reference crop captured; no reconstruction plotted because accepted raw data were not recovered."
        )
        lines.append(f"| {fig_id} | `{info['status']}` | {result} |")
    lines.extend(
        [
            "",
            "## Editorial Review Summary",
            "",
            "- Critical issues found: missing accepted reconstruction data for Figures 9-1, 9-2, 9-3, and 9-5. These are explicit source-recovery blockers, not silent failures.",
            "- Major issues found: Figure 9-4 uses current successor data rather than the exact Ortiz-Ospina & Roser 2016b/2017 snapshot; the status remains `updated_equivalent`.",
            "- Minor issues found: Figure 9-4 label placement and line styles are approximate.",
            "- Issues automatically corrected: comparison panels were generated for every figure; blocked figures use explicit status panels to avoid unauthorized digitized reconstructions.",
            "- Issues remaining: targeted source recovery for Milanovic/Clio Infra source spreadsheets and archived OWID 2016b social-spending data.",
            "- Publication decision: the batch is acceptable as a documented partial/source-recovery batch, not as five verified reproductions.",
            "",
            "## Source-Recovery Targets",
            "",
            "- 9-1: OECD Clio Infra Project/Moatsos et al. 2014 market household income international inequality data; Milanovic 2012 weighted international inequality plus 2012-2013 personal-communication update.",
            "- 9-2: Milanovic 2016 figure 3.1 underlying global inequality table.",
            "- 9-3: Milanovic 2016 figure 2.1 UK/England and US disposable-income-per-capita Gini table.",
            "- 9-4: archived OWID Ortiz-Ospina & Roser 2016b/2017 social-spending chart data.",
            "- 9-5: Milanovic 2016 figure 1.3 global growth-incidence curve data, or Lakner-Milanovic 1988-2008 percentile spreadsheet.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_project_state() -> None:
    path = ROOT / "PROJECT_STATE.md"
    text = path.read_text(encoding="utf-8")
    text = text.replace(
        "Last update: 2026-06-29 19:29 America/Los_Angeles",
        "Last update: 2026-06-30 Track C inequality/social-spending batch",
    )
    text = text.replace("Project version: `1.4-four-figure-remediation`", "Project version: `1.5-track-c-inequality-social-spending`")
    insert = """| 9-1 | International inequality, 1820-2013 | Source recovery blocked; reference captured | `manual_review_needed` | Low | Source line captured from Chapter 9 preview PDF; original OECD Clio Infra/Moatsos and Milanovic weighted data not recovered, so no digitized reconstruction was made. |
| 9-2 | Global inequality, 1820-2011 | Source recovery blocked; reference captured | `manual_review_needed` | Low | Source line captured; Milanovic 2016 fig. 3.1 underlying table not recovered, so no digitized reconstruction was made. |
| 9-3 | Inequality, UK and US, 1688-2013 | Source recovery blocked; reference captured | `manual_review_needed` | Low | Source line captured; Milanovic 2016 fig. 2.1 underlying UK/US table not recovered, so no digitized reconstruction was made. |
| 9-4 | Social spending, OECD countries, 1880-2016 | Updated-equivalent reconstruction with successor extension | `updated_equivalent` | Medium | Current OWID social-spending-oecd-longrun successor reconstructs the figure concept through 2016 and extends after 2016; exact Ortiz-Ospina & Roser 2016b/2017 source snapshot remains unrecovered. |
| 9-5 | Income gains, 1988-2008 | Source recovery blocked; reference captured | `manual_review_needed` | Low | Source line captured; Milanovic 2016 fig. 1.3 growth-incidence data not recovered, so no digitized reconstruction was made. |
"""
    marker = "| 10-5 | Oil spills, 1970-2016 |"
    if "| 9-1 | International inequality" not in text:
        text = text.replace(marker, insert + marker)
    artifacts = """
### Figure 9-1 - International inequality, 1820-2013

Status: `manual_review_needed`

Canonical visual artifacts:

- Original reference: `figures/9-1/plots/comparisons/kindle_reference_figure_9_1.png`
- Book-period status panel: `figures/9-1/plots/book_period/figure_9_1_book_period_reconstruction.png`
- Extended status panel: `figures/9-1/plots/extended/figure_9_1_extended_reconstruction.png`
- Book-period comparison: `figures/9-1/plots/comparisons/figure_9_1_book_period_comparison.png`
- Extended comparison: `figures/9-1/plots/comparisons/figure_9_1_extended_comparison.png`

Canonical documentation:

- Caption: `figures/9-1/captions/caption.txt`
- Provenance: `figures/9-1/provenance/provenance.md`
- Anomaly review: `figures/9-1/anomaly_reviews/anomaly_review.md`
- Metadata: `figures/9-1/metadata/metadata.json`
- Review checklist: `figures/9-1/review_checklist.md`

### Figure 9-2 - Global inequality, 1820-2011

Status: `manual_review_needed`

Canonical visual artifacts:

- Original reference: `figures/9-2/plots/comparisons/kindle_reference_figure_9_2.png`
- Book-period status panel: `figures/9-2/plots/book_period/figure_9_2_book_period_reconstruction.png`
- Extended status panel: `figures/9-2/plots/extended/figure_9_2_extended_reconstruction.png`
- Book-period comparison: `figures/9-2/plots/comparisons/figure_9_2_book_period_comparison.png`
- Extended comparison: `figures/9-2/plots/comparisons/figure_9_2_extended_comparison.png`

Canonical documentation:

- Caption: `figures/9-2/captions/caption.txt`
- Provenance: `figures/9-2/provenance/provenance.md`
- Anomaly review: `figures/9-2/anomaly_reviews/anomaly_review.md`
- Metadata: `figures/9-2/metadata/metadata.json`
- Review checklist: `figures/9-2/review_checklist.md`

### Figure 9-3 - Inequality, UK and US, 1688-2013

Status: `manual_review_needed`

Canonical visual artifacts:

- Original reference: `figures/9-3/plots/comparisons/kindle_reference_figure_9_3.png`
- Book-period status panel: `figures/9-3/plots/book_period/figure_9_3_book_period_reconstruction.png`
- Extended status panel: `figures/9-3/plots/extended/figure_9_3_extended_reconstruction.png`
- Book-period comparison: `figures/9-3/plots/comparisons/figure_9_3_book_period_comparison.png`
- Extended comparison: `figures/9-3/plots/comparisons/figure_9_3_extended_comparison.png`

Canonical documentation:

- Caption: `figures/9-3/captions/caption.txt`
- Provenance: `figures/9-3/provenance/provenance.md`
- Anomaly review: `figures/9-3/anomaly_reviews/anomaly_review.md`
- Metadata: `figures/9-3/metadata/metadata.json`
- Review checklist: `figures/9-3/review_checklist.md`

### Figure 9-4 - Social spending, OECD countries, 1880-2016

Status: `updated_equivalent`

Canonical visual artifacts:

- Original reference: `figures/9-4/plots/comparisons/kindle_reference_figure_9_4.png`
- Book-period reconstruction: `figures/9-4/plots/book_period/figure_9_4_book_period_reconstruction.png`
- Extended reconstruction: `figures/9-4/plots/extended/figure_9_4_extended_reconstruction.png`
- Book-period comparison: `figures/9-4/plots/comparisons/figure_9_4_book_period_comparison.png`
- Extended comparison: `figures/9-4/plots/comparisons/figure_9_4_extended_comparison.png`

Canonical documentation:

- Caption: `figures/9-4/captions/caption.txt`
- Provenance: `figures/9-4/provenance/provenance.md`
- Anomaly review: `figures/9-4/anomaly_reviews/anomaly_review.md`
- Metadata: `figures/9-4/metadata/metadata.json`
- Review checklist: `figures/9-4/review_checklist.md`

### Figure 9-5 - Income gains, 1988-2008

Status: `manual_review_needed`

Canonical visual artifacts:

- Original reference: `figures/9-5/plots/comparisons/kindle_reference_figure_9_5.png`
- Book-period status panel: `figures/9-5/plots/book_period/figure_9_5_book_period_reconstruction.png`
- Extended status panel: `figures/9-5/plots/extended/figure_9_5_extended_reconstruction.png`
- Book-period comparison: `figures/9-5/plots/comparisons/figure_9_5_book_period_comparison.png`
- Extended comparison: `figures/9-5/plots/comparisons/figure_9_5_extended_comparison.png`

Canonical documentation:

- Caption: `figures/9-5/captions/caption.txt`
- Provenance: `figures/9-5/provenance/provenance.md`
- Anomaly review: `figures/9-5/anomaly_reviews/anomaly_review.md`
- Metadata: `figures/9-5/metadata/metadata.json`
- Review checklist: `figures/9-5/review_checklist.md`

"""
    marker2 = "### Figure 10-5 - Oil spills, 1970-2016"
    if "### Figure 9-1 - International inequality" not in text:
        text = text.replace(marker2, artifacts + marker2)
    history = "| `1.4-four-figure-remediation` |"
    new_history = "| `1.5-track-c-inequality-social-spending` | 2026-06-30 | Processed Figures 9-1 through 9-5. Figure 9-4 reached updated-equivalent reconstruction using current OWID successor data; Figures 9-1, 9-2, 9-3, and 9-5 remain manual-review/source-recovery blockers with no digitized reconstructions. |\n"
    if "`1.5-track-c-inequality-social-spending`" not in text:
        text = text.replace(history, new_history + history)
    path.write_text(text, encoding="utf-8")


def write_checksums(fig_id: str) -> None:
    base = ensure_dirs(fig_id)
    files = [
        p
        for p in base.rglob("*")
        if p.is_file() and "checksums" not in p.parts and not p.name.startswith(".")
    ]
    lines = []
    for p in sorted(files):
        h = hashlib.sha256(p.read_bytes()).hexdigest()
        lines.append(f"{h}  {p.relative_to(base)}")
    (base / "checksums/sha256sums.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    download(
        "https://d2fahduf2624mg.cloudfront.net/pre_purchase_docs/BK_PAUK_001109/2020-06-24-08-06-37/bk_pauk_001109.pdf",
        PDF_SOURCE,
    )
    if not (PDF_PAGES / "page-09.png").exists():
        PDF_PAGES.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            ["pdftoppm", "-png", "-r", "160", str(PDF_SOURCE), str(PDF_PAGES / "page")],
            check=True,
        )
    TMP_SOURCES.mkdir(parents=True, exist_ok=True)
    download(
        "https://ourworldindata.org/grapher/social-spending-oecd-longrun.csv?v=1&csvType=full&useColumnShortNames=false",
        TMP_SOURCES / "social-spending-oecd-longrun.csv",
    )
    download(
        "https://ourworldindata.org/grapher/social-spending-oecd-longrun.metadata.json?v=1&csvType=full&useColumnShortNames=false",
        TMP_SOURCES / "social-spending-oecd-longrun.metadata.json",
    )

    for fig_id in FIGURES:
        ref = crop_reference(fig_id)
        if fig_id == "9-4":
            book, ext = plot_9_4()
        else:
            book = placeholder_plot(fig_id, extended=False)
            ext = placeholder_plot(fig_id, extended=True)
        save_side_by_side(
            ref,
            book,
            ensure_dirs(fig_id) / f"plots/comparisons/figure_{fig_id.replace('-', '_')}_book_period_comparison.png",
            f"Figure {fig_id} book-period comparison",
        )
        save_side_by_side(
            ref,
            ext,
            ensure_dirs(fig_id) / f"plots/comparisons/figure_{fig_id.replace('-', '_')}_extended_comparison.png",
            f"Figure {fig_id} extended comparison",
        )
        write_text_files(fig_id)
        write_metadata_and_lineage(fig_id)
        write_checksums(fig_id)

    update_registry()
    update_metadata_csv()
    update_project_state()
    write_report()


if __name__ == "__main__":
    main()
