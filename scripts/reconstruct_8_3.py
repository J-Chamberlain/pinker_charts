from __future__ import annotations

import csv
import hashlib
import json
from datetime import date
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
FIG_ID = "8-3"
BASE = ROOT / "figures" / FIG_ID
PDF_PAGE = Path("/tmp/pinker_prod_pdf_pages/page-08.png")
TODAY = date.today().isoformat()


def ensure_dirs() -> None:
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
        "checksums",
    ]:
        (BASE / part).mkdir(parents=True, exist_ok=True)


def crop_reference() -> Path:
    out = BASE / "plots/comparisons/kindle_reference_figure_8_3.png"
    if not PDF_PAGE.exists():
        raise FileNotFoundError(f"Missing rendered supplemental PDF page: {PDF_PAGE}")
    # Supplemental PDF page 8, top chart plus caption/source line.
    Image.open(PDF_PAGE).convert("RGB").crop((115, 125, 1005, 790)).save(out)
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

    def paste_fit(im: Image.Image, x: int, y: int) -> None:
        fitted = ImageOps.contain(im, (panel_w, panel_h), method=Image.Resampling.LANCZOS)
        canvas.paste(fitted, (x + (panel_w - fitted.width) // 2, y + (panel_h - fitted.height) // 2))
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


def income_share_columns(df: pd.DataFrame) -> list[tuple[str, float]]:
    # The workbook repeats income-bracket labels. Pandas appends ".1" to the
    # share-of-population block, which starts at column 141.
    cols: list[tuple[str, float]] = []
    for col in df.columns[141:236]:
        label = str(col)
        if label.endswith(".1"):
            label = label[:-2]
        try:
            cols.append((col, float(label)))
        except ValueError:
            continue
    return cols


def load_clean_data() -> pd.DataFrame:
    raw = BASE / "data/raw/gapminder_income_mountains_v2.xlsx"
    df = pd.read_excel(raw, sheet_name="Data world by year", header=1)
    cols = income_share_columns(df)
    rows = []
    for year in [1800, 1975, 2015]:
        row = df.loc[(df["geo"] == "world") & (df["year"] == year)].iloc[0]
        population = float(row["population"])
        for col, income in cols:
            if 0.18 <= income <= 260:
                share = float(row[col])
                rows.append(
                    {
                        "year": year,
                        "income_2011_int_dollars_per_day": income,
                        "share": share,
                        "population": population,
                        "people_millions": share * population / 1_000_000,
                    }
                )
    clean = pd.DataFrame(rows)
    clean.to_csv(BASE / "data/clean/figure_8_3_book_period_clean.csv", index=False)
    clean.to_csv(BASE / "data/clean/figure_8_3_extended_clean.csv", index=False)
    return clean


def style_axis(ax) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", left=False, labelleft=False)
    ax.tick_params(axis="x", labelsize=9)
    ax.grid(False)


def plot(clean: pd.DataFrame, out: Path, extended: bool = False) -> None:
    fig, ax = plt.subplots(figsize=(8.3, 5.1), dpi=180)
    colors = {1800: "0.72", 1975: "0.58", 2015: "0.12"}
    widths = {1800: 2.4, 1975: 2.4, 2015: 2.8}
    for year in [1800, 1975, 2015]:
        sub = clean[clean["year"] == year].sort_values("income_2011_int_dollars_per_day")
        ax.plot(
            sub["income_2011_int_dollars_per_day"],
            sub["people_millions"],
            color=colors[year],
            linewidth=widths[year],
        )
    ax.axvline(1.9, color="0.72", linestyle=":", linewidth=1.2)
    ax.text(1.75, 365, "Extreme poverty", rotation=90, va="top", ha="right", fontsize=10)
    ax.annotate("", xy=(0.78, 145), xytext=(0.72, 45), arrowprops={"arrowstyle": "-|>", "color": "0.8", "lw": 1.8})
    ax.text(0.60, 155, "1975", fontsize=10)
    ax.text(0.52, 45, "1800", fontsize=10)
    ax.annotate("", xy=(4.8, 310), xytext=(0.75, 125), arrowprops={"arrowstyle": "-|>", "color": "0.8", "lw": 1.8})
    ax.text(5.2, 315, "2015", fontsize=10)
    ax.set_xscale("log")
    ax.set_xlim(0.18, 260)
    ax.set_ylim(0, 430)
    xticks = [0.2, 0.5, 1, 2, 5, 10, 20, 50, 100, 200]
    ax.set_xticks(xticks)
    ax.set_xticklabels(["0.2", "0.5", "1", "2", "5", "10", "20", "50", "100", "200"])
    ax.set_xlabel("2011 international dollars per day")
    ax.set_title("Figure 8-3: World income distribution, 1800, 1975, and 2015", loc="left", fontsize=12)
    style_axis(ax)
    note = "Source: Gapminder Income Mountains v2; book source is Gapminder mountain via Ola Rosling."
    if extended:
        note += " No post-2015 extension plotted."
    ax.text(0, -0.16, note, transform=ax.transAxes, fontsize=7)
    fig.tight_layout()
    fig.savefig(out, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def write_docs() -> None:
    metadata = {
        "figure_id": FIG_ID,
        "chapter": "8",
        "title": "World income distribution, 1800, 1975, and 2015",
        "book_page": "Supplemental PDF page 8",
        "claim_summary": "World income distribution shifted rightward from 1800 to 2015, with the 1975 twin-hump distribution collapsing into a richer 2015 single-hump distribution.",
        "book_citation": "Gapminder, via Ola Rosling, http://www.gapminder.org/tools/mountain. The scale is in 2011 international dollars.",
        "original_dataset": "Gapminder Income Mountains dataset v2",
        "dataset_url": "https://docs.google.com/spreadsheets/d/1939CzZ5HHoLreb0YyopaWfNjJ9mnN27IhywI6-TuwZs/export?format=xlsx",
        "archive_url": "Not captured in this pass.",
        "download_date": TODAY,
        "reproduction_status": "updated_equivalent",
        "confidence_score": 0.78,
        "visual_validation": "good",
        "notes": "Same Gapminder source family and variables were located, but the downloaded v2 workbook is a 2018 successor rather than a proven book-era snapshot. Shares were multiplied by workbook population to plot people in each income bin, matching the visible figure geometry more closely than normalized shares.",
        "canonical_artifacts": {
            "original_reference": "figures/8-3/plots/comparisons/kindle_reference_figure_8_3.png",
            "book_period_reconstruction": "figures/8-3/plots/book_period/figure_8_3_book_period_reconstruction.png",
            "extended_reconstruction": "figures/8-3/plots/extended/figure_8_3_extended_reconstruction.png",
            "book_period_comparison": "figures/8-3/plots/comparisons/figure_8_3_book_period_comparison.png",
            "extended_comparison": "figures/8-3/plots/comparisons/figure_8_3_extended_comparison.png",
        },
    }
    (BASE / "metadata/metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    (BASE / "captions/caption.txt").write_text(
        "Figure 8-3: World income distribution, 1800, 1975, and 2015. "
        "Source note: Gapminder via Ola Rosling, mountain tool; scale in 2011 international dollars. "
        "Status: updated_equivalent because Gapminder Income Mountains v2 was recovered, but not a proven book-era snapshot. "
        "The reconstruction plots population-weighted income-bin counts, not normalized shares; no post-2015 extension is plotted.\n"
    )
    (BASE / "source_logs/source_log.md").write_text(
        "# Source Discovery Log: Figure 8-3\n\n"
        "Figure title: World income distribution, 1800, 1975, and 2015\n\n"
        "Original book citation: Gapminder, via Ola Rosling, http://www.gapminder.org/tools/mountain. The scale is in 2011 international dollars.\n\n"
        "## Search Queries Attempted\n"
        "- Supplemental PDF page 8 Figure 8-3 source note\n"
        "- Gapminder mountain chart data income distribution 1800 1975 2015 csv\n"
        "- site:github.com gapminder mountain income distribution 1800 1975 2015\n"
        "- Gapminder Income Mountains dataset v2\n\n"
        "## Sources Investigated\n"
        "- Supplemental Graphics PDF page 8: accepted as visual/source reference.\n"
        "- Gapminder Income Mountains dataset v2 Google Sheets/Excel export: accepted as updated-equivalent source-family data.\n"
        "- Exact book-era Gapminder mountain snapshot: not recovered in this pass.\n\n"
        "## Download URLs\n"
        "- https://docs.google.com/spreadsheets/d/1939CzZ5HHoLreb0YyopaWfNjJ9mnN27IhywI6-TuwZs/export?format=xlsx\n\n"
        "## Remaining Uncertainties\n"
        "- The workbook is v2, updated May 2018, after the book production date.\n"
        "- The book figure may have used the live mountain tool rendering rather than this exact workbook export.\n\n"
        "## Recommended Next Steps\n"
        "- Search for an archived 2017 Gapminder mountain tool/data snapshot before considering verified_reproduction.\n"
    )
    (BASE / "provenance/provenance.md").write_text(
        "# Provenance: Figure 8-3\n\n"
        "Book Figure -> Supplemental PDF page 8 -> Gapminder Income Mountains v2 workbook -> "
        "`scripts/reconstruct_8_3.py` -> generated book-period and comparison plots.\n"
    )
    (BASE / "anomaly_reviews/anomaly_review.md").write_text(
        "# Anomaly Review: Figure 8-3\n\n"
        "## Visible Differences\n"
        "- The recreated plot captures the log-scaled income distribution, the 1800/1975/2015 ordering, relative population-weighted curve heights, and the poverty cutoff.\n"
        "- The exact curve smoothing and arrow/label placement differ from the book.\n"
        "- The 1975 camel-shape is source-family similar but not pixel-identical, and its left peak is lower relative to 2015 than in the PDF reference.\n\n"
        "## Cause Assessment\n"
        "- Status: `updated_equivalent`.\n"
        "- Main limitation is source vintage: Gapminder Income Mountains v2 is a successor workbook, not a proven book-era export.\n"
        "- An initial normalized-share rendering made the 1800 curve visibly too tall; the pipeline corrected this by multiplying income-bin shares by workbook population.\n\n"
        "## Reviewer Challenge\n"
        "- Pinker would likely ask whether the exact Ola Rosling mountain snapshot was recovered.\n"
        "- A data journalist would ask for the workbook and transformation script, both included.\n"
        "- A peer reviewer would ask whether the y-axis normalization matches the mountain tool rendering.\n"
        "- A skeptical reader would notice small differences in curve smoothing and label geometry.\n\n"
        "Overall confidence:\n"
        "- Book reconstruction: medium-high\n"
        "- Extension: none plotted\n"
        "- Source provenance: medium-high source-family match, not exact snapshot\n"
        "- Outstanding risks: exact 2017 data/rendering snapshot unrecovered\n"
        "- Recommended next action: archive search for the original mountain tool data snapshot\n"
    )
    (BASE / "discrepancy_logs/discrepancy_log.md").write_text(
        "# Discrepancy Log: Figure 8-3\n\n"
        "- Chart type, x-axis scale, years, and poverty cutoff align with the PDF reference.\n"
        "- Remaining discrepancies are curve smoothing, y-axis normalization, and label/arrow placement.\n"
        "- No plotted values were digitized from the book figure.\n"
    )
    (BASE / "search_iterations/search_iterations.md").write_text(
        "# Search Iterations: Figure 8-3\n\n"
        "- Supplemental PDF page 8 Figure 8-3 source note\n"
        "- Gapminder mountain chart data income distribution 1800 1975 2015 csv\n"
        "- site:github.com gapminder mountain income distribution 1800 1975 2015\n"
        "- Gapminder Income Mountains dataset v2\n"
    )
    lineage = [
        {"stage": "Book Figure", "value": "Figure 8-3: World income distribution, 1800, 1975, and 2015"},
        {"stage": "Book Citation", "value": metadata["book_citation"]},
        {"stage": "Original Dataset", "value": "Exact 2017 Gapminder mountain snapshot not recovered"},
        {"stage": "Modern Dataset", "value": "Gapminder Income Mountains v2 workbook"},
        {"stage": "Downloaded File", "value": "figures/8-3/data/raw/gapminder_income_mountains_v2.xlsx"},
        {"stage": "Transformation Script", "value": "scripts/reconstruct_8_3.py"},
        {"stage": "Generated Plot", "value": "figures/8-3/plots/"},
    ]
    pd.DataFrame(lineage).to_csv(BASE / "lineage/figure_lineage.csv", index=False)
    (BASE / "lineage/figure_lineage.json").write_text(json.dumps(lineage, indent=2) + "\n")
    (BASE / "README.md").write_text(
        "# Figure 8-3: World income distribution, 1800, 1975, and 2015\n\n"
        "Status: `updated_equivalent`\n\n"
        "## Canonical Artifacts\n\n"
        "- Original reference: `plots/comparisons/kindle_reference_figure_8_3.png`\n"
        "- Book-period reconstruction: `plots/book_period/figure_8_3_book_period_reconstruction.png`\n"
        "- Extended reconstruction: `plots/extended/figure_8_3_extended_reconstruction.png`\n"
        "- Book-period comparison: `plots/comparisons/figure_8_3_book_period_comparison.png`\n"
        "- Extended comparison: `plots/comparisons/figure_8_3_extended_comparison.png`\n"
        "- Caption: `captions/caption.txt`\n"
        "- Provenance: `provenance/provenance.md`\n"
        "- Anomaly review: `anomaly_reviews/anomaly_review.md`\n"
        "- Metadata: `metadata/metadata.json`\n"
        "- Review checklist: `review_checklist.md`\n"
    )
    checklist = (ROOT / "docs/review_checklist.md").read_text()
    (BASE / "review_checklist.md").write_text(
        checklist
        + "\n\n## Figure 8-3 Completion Notes\n\n"
        "Current status: `updated_equivalent`.\n\n"
        "- Supplemental PDF figure inspected.\n"
        "- Gapminder Income Mountains v2 workbook downloaded and transformed.\n"
        "- Exact book-era mountain tool snapshot not recovered; do not promote to verified without archive evidence.\n"
    )


def update_tables() -> None:
    registry_path = ROOT / "data/figure_registry.csv"
    rows = list(csv.DictReader(registry_path.open()))
    for row in rows:
        if row["figure_id"] == FIG_ID:
            row["current_status"] = "updated_equivalent"
            row["lifecycle_stage"] = "updated_equivalent_with_gapminder_successor_workbook"
            row["priority"] = "completed_monitor"
            row["current_owner"] = "Codex"
            row["next_action"] = "Search for archived 2017 Gapminder mountain tool/data snapshot before promoting to verified_reproduction."
            row["notes"] = "Processed in production loop on 2026-07-01 using Gapminder Income Mountains v2 workbook; exact book-era snapshot not recovered."
    with registry_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys(), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    (ROOT / "data/figure_registry.json").write_text(json.dumps(rows, indent=2) + "\n")

    meta_path = ROOT / "data/metadata/figure_metadata.csv"
    meta_rows = list(csv.DictReader(meta_path.open()))
    row = {
        "figure_id": FIG_ID,
        "chapter": "8",
        "title": "World income distribution, 1800, 1975, and 2015",
        "book_page": "Supplemental PDF page 8",
        "claim_summary": "World income distribution shifted rightward from 1800 to 2015.",
        "book_citation": "Gapminder, via Ola Rosling, http://www.gapminder.org/tools/mountain. The scale is in 2011 international dollars.",
        "original_dataset": "Gapminder Income Mountains v2 successor workbook; exact book-era snapshot unrecovered",
        "dataset_url": "https://docs.google.com/spreadsheets/d/1939CzZ5HHoLreb0YyopaWfNjJ9mnN27IhywI6-TuwZs/export?format=xlsx",
        "archive_url": "Not recovered",
        "download_date": TODAY,
        "reproduction_status": "updated_equivalent",
        "confidence_score": "0.78",
        "visual_validation": "good",
        "notes": "Production loop 2026-07-01: same Gapminder source family, but v2 workbook is not a proven book-era snapshot.",
    }
    existing = False
    for existing_row in meta_rows:
        if existing_row["figure_id"] == FIG_ID:
            existing_row.update(row)
            existing = True
            break
    if not existing:
        meta_rows.append(row)
    with meta_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=meta_rows[0].keys(), lineterminator="\n")
        writer.writeheader()
        writer.writerows(meta_rows)


def update_project_state() -> None:
    path = ROOT / "PROJECT_STATE.md"
    text = path.read_text()
    row = "| 8-3 | World income distribution, 1800, 1975, and 2015 | Gapminder successor workbook reconstruction | `updated_equivalent` | Medium-high | Gapminder Income Mountains v2 source-family workbook reproduces the concept and shape, but exact book-era mountain tool snapshot remains unrecovered. |"
    if "| 8-3 |" not in text:
        marker = "| 8-2 | GDP per capita, 1600-2015"
        idx = text.index(marker)
        next_line = text.index("\n", idx) + 1
        text = text[:next_line] + row + "\n" + text[next_line:]
    section = (
        "\n### Figure 8-3 - World income distribution, 1800, 1975, and 2015\n\n"
        "Status: `updated_equivalent`\n\n"
        "Canonical visual artifacts:\n\n"
        "- Original reference: `figures/8-3/plots/comparisons/kindle_reference_figure_8_3.png`\n"
        "- Book-period reconstruction: `figures/8-3/plots/book_period/figure_8_3_book_period_reconstruction.png`\n"
        "- Extended reconstruction: `figures/8-3/plots/extended/figure_8_3_extended_reconstruction.png`\n"
        "- Book-period comparison: `figures/8-3/plots/comparisons/figure_8_3_book_period_comparison.png`\n"
        "- Extended comparison: `figures/8-3/plots/comparisons/figure_8_3_extended_comparison.png`\n\n"
        "Canonical documentation:\n\n"
        "- Caption: `figures/8-3/captions/caption.txt`\n"
        "- Provenance: `figures/8-3/provenance/provenance.md`\n"
        "- Anomaly review: `figures/8-3/anomaly_reviews/anomaly_review.md`\n"
        "- Metadata: `figures/8-3/metadata/metadata.json`\n"
        "- Review checklist: `figures/8-3/review_checklist.md`\n"
    )
    if "### Figure 8-3 -" not in text:
        insert = text.index("### Figure 8-4 -")
        text = text[:insert] + section + "\n" + text[insert:]
    text = text.replace("Project version: `1.7-production-loop-consolidation`", "Project version: `1.8-production-loop-figure-8-3`")
    text = text.replace("Last update: 2026-07-01 America/Los_Angeles", "Last update: 2026-07-01 America/Los_Angeles")
    history = "| `1.8-production-loop-figure-8-3` | 2026-07-01 | Added Figure 8-3 as an updated-equivalent Gapminder Income Mountains v2 reconstruction with PDF side-by-side comparisons and full provenance package. |"
    if history not in text:
        marker = "| `1.7-production-loop-consolidation`"
        text = text.replace(marker, history + "\n" + marker)
    path.write_text(text)


def update_checksums() -> None:
    files = sorted(p for p in BASE.rglob("*") if p.is_file() and "checksums" not in p.parts)
    rows = [f"{hashlib.sha256(p.read_bytes()).hexdigest()}  ./{p.relative_to(BASE)}" for p in files]
    (BASE / "checksums/sha256sums.txt").write_text("\n".join(rows) + "\n")


def main() -> None:
    ensure_dirs()
    clean = load_clean_data()
    book_plot = BASE / "plots/book_period/figure_8_3_book_period_reconstruction.png"
    ext_plot = BASE / "plots/extended/figure_8_3_extended_reconstruction.png"
    plot(clean, book_plot, False)
    plot(clean, ext_plot, True)
    ref = crop_reference()
    side_by_side(ref, book_plot, BASE / "plots/comparisons/figure_8_3_book_period_comparison.png", "Figure 8-3 book-period comparison")
    side_by_side(ref, ext_plot, BASE / "plots/comparisons/figure_8_3_extended_comparison.png", "Figure 8-3 extended comparison")
    write_docs()
    update_tables()
    update_project_state()
    update_checksums()


if __name__ == "__main__":
    main()
