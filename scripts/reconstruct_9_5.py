from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from datetime import date
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
FIG_ID = "9-5"
BASE = ROOT / "figures" / FIG_ID
SUPPLEMENTAL_PDF = ROOT / "references" / "enlightenment_now_supplemental_graphics.pdf"
RAW_DTA = BASE / "data/raw/lm_wpid_web.dta"
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
        "data/raw",
        "data/clean",
        "checksums",
    ]:
        (BASE / part).mkdir(parents=True, exist_ok=True)


def crop_reference() -> Path:
    tmp_dir = ROOT / "tmp/pdfs/figure_9_5"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    prefix = tmp_dir / "supplemental_page"
    subprocess.run(
        [
            "pdftoppm",
            "-f",
            "11",
            "-l",
            "11",
            "-png",
            "-r",
            "180",
            str(SUPPLEMENTAL_PDF),
            str(prefix),
        ],
        check=True,
    )
    page = Image.open(tmp_dir / "supplemental_page-11.png").convert("RGB")
    out = BASE / "plots/comparisons/supplemental_pdf_reference_figure_9_5.png"
    page.crop((155, 880, 980, 1590)).save(out)
    return out


def weighted_fractile_means(df: pd.DataFrame, endpoints: list[int]) -> pd.DataFrame:
    df = df.sort_values("RRinc")
    total_pop = float(df["pop"].sum())
    rows = list(df[["RRinc", "pop"]].itertuples(index=False, name=None))
    records: list[dict[str, float]] = []
    lower_pct = 0
    for upper_pct in endpoints:
        lower = lower_pct / 100 * total_pop
        upper = upper_pct / 100 * total_pop
        numerator = 0.0
        denominator = 0.0
        cumulative = 0.0
        for income, pop in rows:
            start = cumulative
            end = cumulative + float(pop)
            cumulative = end
            overlap = max(0.0, min(end, upper) - max(start, lower))
            if overlap > 1e-9:
                numerator += overlap * float(income)
                denominator += overlap
        records.append(
            {
                "percentile": upper_pct,
                "lower_percentile": lower_pct,
                "upper_percentile": upper_pct,
                "mean_income": numerator / denominator,
            }
        )
        lower_pct = upper_pct
    return pd.DataFrame(records)


def reconstruct_data() -> pd.DataFrame:
    source = pd.read_stata(RAW_DTA)
    main = source[(source["mysample"] == 1) & (source["bin_year"].isin([1988, 2008]))].copy()
    main = main.dropna(subset=["RRinc", "pop"])
    endpoints = list(range(5, 100, 5)) + [99, 100]
    p1988 = weighted_fractile_means(main[main["bin_year"] == 1988], endpoints)
    p2008 = weighted_fractile_means(main[main["bin_year"] == 2008], endpoints)
    data = p1988.merge(
        p2008,
        on=["percentile", "lower_percentile", "upper_percentile"],
        suffixes=("_1988", "_2008"),
    )
    data["growth_pct"] = 100 * (data["mean_income_2008"] / data["mean_income_1988"] - 1)
    data["source_sample"] = "LM-WPID mysample==1; 2005 PPP dollars"
    data.to_csv(BASE / "data/clean/figure_9_5_book_period_clean.csv", index=False)
    return data


def plot_reconstruction(data: pd.DataFrame, out: Path, extended: bool = False) -> None:
    fig, ax = plt.subplots(figsize=(6.9, 4.5), dpi=180)
    ax.plot(
        data["percentile"],
        data["growth_pct"],
        color="0.14",
        linewidth=2.4,
        solid_joinstyle="round",
        solid_capstyle="round",
    )
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 85)
    ax.set_xticks(range(10, 101, 10))
    ax.set_yticks(range(0, 81, 10))
    ax.set_xlabel("Percentile of global income distribution", fontsize=11, labelpad=12)
    ax.set_ylabel("Cumulative gain in real income 1988-2008 (%)", fontsize=11, labelpad=12)
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    ax.spines["left"].set_color("0.25")
    ax.spines["bottom"].set_color("0.25")
    ax.tick_params(axis="both", labelsize=10, length=7, width=1.1, color="0.25")
    ax.grid(False)
    note = "Source-family reconstruction from LM-WPID; exact Milanovic 2016 figure-data not recovered."
    if extended:
        note += " No comparable successor extension is plotted."
    ax.text(0, -0.25, note, transform=ax.transAxes, fontsize=7.5, va="top")
    fig.tight_layout()
    fig.savefig(out, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def side_by_side(reference: Path, recreated: Path, output: Path, title: str) -> None:
    def load_trim(path: Path) -> Image.Image:
        im = Image.open(path).convert("RGB")
        bg = Image.new("RGB", im.size, "white")
        bbox = ImageChops.difference(im, bg).getbbox()
        return im.crop(bbox) if bbox else im

    ref = load_trim(reference)
    rec = load_trim(recreated)
    panel_w, panel_h = 900, 620
    margin, gap, header_h, title_h = 42, 44, 54, 56
    canvas = Image.new("RGB", (margin * 2 + panel_w * 2 + gap, title_h + header_h + panel_h + margin), "white")
    draw = ImageDraw.Draw(canvas)
    try:
        title_font = ImageFont.truetype("Arial.ttf", 28)
        label_font = ImageFont.truetype("Arial.ttf", 22)
    except OSError:
        title_font = label_font = None

    def paste_fit(im: Image.Image, x: int, y: int) -> None:
        fitted = ImageOps.contain(im, (panel_w, panel_h), method=Image.Resampling.LANCZOS)
        canvas.paste(fitted, (x + (panel_w - fitted.width) // 2, y + (panel_h - fitted.height) // 2))
        draw.rectangle([x, y, x + panel_w, y + panel_h], outline=(230, 230, 230), width=1)

    draw.text((canvas.width // 2, 16), title, fill="black", anchor="ma", font=title_font)
    left_x = margin
    right_x = margin + panel_w + gap
    label_y = title_h + 8
    draw.text((left_x + panel_w // 2, label_y), "Supplemental PDF reference", fill="black", anchor="ma", font=label_font)
    draw.text((right_x + panel_w // 2, label_y), "LM-WPID reconstruction", fill="black", anchor="ma", font=label_font)
    paste_fit(ref, left_x, title_h + header_h)
    paste_fit(rec, right_x, title_h + header_h)
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output)


def write_docs(data: pd.DataFrame) -> None:
    max_row = data.loc[data["growth_pct"].idxmax()]
    min_row = data.loc[data["growth_pct"].idxmin()]
    metadata = {
        "figure_id": FIG_ID,
        "title": "Income gains, 1988-2008",
        "chapter": "9",
        "book_page": "Supplemental Graphics PDF page 11",
        "year_range": "1988-2008",
        "claim_summary": "The global growth-incidence curve from 1988 to 2008 has the elephant shape: strong middle-percentile gains, weak upper-middle gains, and renewed top-percentile gains.",
        "book_citation": "Milanovic 2016, fig. 1.3.",
        "original_dataset": "Exact Milanovic 2016 figure 1.3/Lakner-Milanovic 2015 summary_data.xls was not recovered. CUNY Stone Center LM-WPID Stata dataset was recovered as the closest inspectable source-family dataset.",
        "dataset_url": "https://stonecenter.gc.cuny.edu/publications/lakner-milanovic-world-panel-income-distribution/",
        "archive_url": "https://openknowledge.worldbank.org/entities/publication/16065899-c37d-5750-af68-e9742cec9456",
        "download_date": TODAY,
        "reproduction_status": "partial_match",
        "confidence_score": 0.68,
        "visual_validation": "partial_source_family_match",
        "notes": "Values are computed from LM-WPID country-decile data, not digitized from Pinker's chart. Because the exact Milanovic 2016 figure-data spreadsheet was not recovered and the recovered source-family curve differs visibly at some fractiles, this is not a verified reproduction.",
        "canonical_artifacts": {
            "supplemental_pdf_reference": "figures/9-5/plots/comparisons/supplemental_pdf_reference_figure_9_5.png",
            "book_period_reconstruction": "figures/9-5/plots/book_period/figure_9_5_book_period_reconstruction.png",
            "extended_reconstruction": "figures/9-5/plots/extended/figure_9_5_extended_reconstruction.png",
            "book_period_comparison": "figures/9-5/plots/comparisons/figure_9_5_book_period_comparison.png",
            "extended_comparison": "figures/9-5/plots/comparisons/figure_9_5_extended_comparison.png",
            "clean_data": "figures/9-5/data/clean/figure_9_5_book_period_clean.csv",
        },
    }
    (BASE / "metadata/metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")

    (BASE / "captions/caption.txt").write_text(
        "Figure 9-5: Income gains, 1988-2008. Source note inspected from the Supplemental Graphics PDF: "
        "Milanovic 2016, fig. 1.3. This run recovered the CUNY Stone Center LM-WPID Stata dataset and "
        "reconstructed a source-family anonymous growth-incidence curve from 1988 and 2008 weighted "
        "fractile means. The exact Milanovic 2016 figure 1.3 spreadsheet was not recovered, so this is "
        "classified as a partial source-family match, not a verified reproduction or extension.\n"
    )

    (BASE / "provenance/provenance.md").write_text(
        "# Figure 9-5 Provenance\n\n"
        "## Evidence\n\n"
        "- Title: Income gains, 1988-2008\n"
        "- Source line: Milanovic 2016, fig. 1.3.\n"
        "- Figure/source inspected from: Supplemental Graphics PDF page 11.\n"
        "- Surrounding text: Pinker describes the graph as a growth incidence curve that sorts the world's population from poor to rich and plots real income gains from 1988 to 2008.\n\n"
        "## Bibliographic Resolution\n\n"
        "- Pinker's source resolves to Branko Milanovic, *Global Inequality: A New Approach for the Age of Globalization* (2016), figure 1.3/nearby chapter figure text.\n"
        "- The Milanovic book chapter identifies the underlying source family as Lakner and Milanovic data. A publicly posted chapter scan labels the comparable figure's data source as Lakner and Milanovic (2015).\n"
        "- The World Bank Open Knowledge Repository entry for Lakner and Milanovic's working paper links to a dataset node that has moved or no longer resolves as an inspectable catalog page.\n"
        "- The CUNY Stone Center page for the Lakner-Milanovic World Panel Income Distribution provides the downloadable LM-WPID Stata dataset and a variable-description PDF.\n\n"
        "## Source Recovery Result\n\n"
        "Recovered inspectable source-family data:\n\n"
        "- `figures/9-5/data/raw/lm_wpid_web.dta`\n"
        "- `figures/9-5/data/raw/lm_wpid_description.pdf`\n"
        "- `figures/9-5/data/raw/lakner_milanovic_world_bank_wps6719.pdf`\n"
        "- saved provenance pages under `figures/9-5/data/raw/`\n\n"
        "Unresolved exact source:\n\n"
        "- Milanovic 2016 figure 1.3's exact plotted spreadsheet, repeatedly referenced in presentations as `summary_data.xls`, was not recovered as an inspectable file.\n"
        "- The recovered LM-WPID file covers the correct 1988-2008 period and source family, but it is not the final plotted `summary_data.xls`/Lakner-Milanovic 2015 figure-data file.\n\n"
        "## Reconstruction Method\n\n"
        "- Read LM-WPID `lm_wpid_web.dta`.\n"
        "- Kept the authors' main sample (`mysample == 1`) and benchmark years 1988 and 2008.\n"
        "- Excluded rows with missing `RRinc` or `pop`; this removes one Switzerland 2008 decile row with missing income from the recovered file.\n"
        "- Sorted country-decile observations by `RRinc` within each year and used population weights (`pop`).\n"
        "- Computed mean income for plotted fractile bins ending at 5, 10, ..., 95, 99, and 100 percent of the global distribution.\n"
        "- Computed cumulative growth as `100 * (mean_2008 / mean_1988 - 1)`.\n\n"
        "## Data Fidelity\n\n"
        f"The recovered source-family curve peaks at percentile {int(max_row['percentile'])} with {max_row['growth_pct']:.1f}% growth and bottoms at percentile {int(min_row['percentile'])} with {min_row['growth_pct']:.1f}% growth. "
        "The visible book/Pinker curve has the same elephant-shaped qualitative pattern but differs at some plotted points, especially the low and middle fractiles. "
        "Because the exact source spreadsheet was not recovered, no numeric tolerance against Milanovic 2016 figure 1.3 is asserted.\n\n"
        "## Extension\n\n"
        "No successor extension was plotted. The task's acceptance rule requires a genuinely comparable successor series; no same-methodology post-2008/2011 successor file was recovered in this run.\n"
    )

    (BASE / "source_logs/source_log.md").write_text(
        "# Figure 9-5 Source Log\n\n"
        f"Date: {TODAY}\n\n"
        "## Accepted For Source-Family Reconstruction\n\n"
        "- CUNY Stone Center, Lakner-Milanovic World Panel Income Distribution page.\n"
        "- `lm_wpid_web.dta`, downloaded from the Stone Center page's Dropbox dataset link.\n"
        "- LM-WPID description PDF from the Stone Center.\n"
        "- Lakner and Milanovic, World Bank Policy Research Working Paper 6719 PDF.\n\n"
        "## Not Recovered\n\n"
        "- Milanovic 2016 figure 1.3 exact underlying `summary_data.xls`/figure-data spreadsheet.\n"
        "- Any author/publisher supplementary file exposing the exact book figure values.\n\n"
        "## Archive And Moved-Source Notes\n\n"
        "- World Bank Open Knowledge Repository page for the paper was saved locally and records a dataset link to `https://datacatalog.worldbank.org/node/140634`.\n"
        "- The old World Bank data catalog node no longer resolves to a direct inspectable dataset in this run.\n"
        "- CUNY Stone Center currently hosts the best verifiable successor/source-family data page.\n\n"
        "## Search Iterations\n\n"
        "- Searched for Milanovic 2016 figure 1.3 data, Lakner-Milanovic growth-incidence spreadsheet, `summary_data.xls`, `twenty_years/final/summary_data`, `final_complete7.dta`, and `combine88_08_11_new.dta`.\n"
        "- Inspected World Bank, CUNY Stone Center, CEPR/VoxEU, Brookings, public Milanovic slide decks, and publicly posted Milanovic book chapter scans.\n\n"
        "## Status\n\n"
        "Source-chain substantially improved, but exact figure-data recovery remains unresolved. The reconstruction is therefore a partial source-family match only.\n"
    )

    (BASE / "search_iterations/search_iterations.md").write_text(
        "# Figure 9-5 Search Iterations\n\n"
        f"Date: {TODAY}\n\n"
        "- Opened Supplemental Graphics PDF page 11 and captured the figure/source line.\n"
        "- Resolved the source to Milanovic 2016 and Lakner-Milanovic global growth-incidence data.\n"
        "- Located World Bank Open Knowledge Repository page for Lakner and Milanovic WPS 6719; it documents a moved dataset node.\n"
        "- Located CUNY Stone Center LM-WPID page with downloadable `.dta` data and description PDF.\n"
        "- Searched exact spreadsheet/code names: `summary_data.xls`, `twenty_years/final/summary_data`, `final_complete7.dta`, `combine88_08_11_new.dta`, and related presentation references.\n"
        "- Did not recover the exact Milanovic 2016 figure 1.3 plotted spreadsheet.\n"
    )

    (BASE / "discrepancy_logs/discrepancy_log.md").write_text(
        "# Figure 9-5 Discrepancy Log\n\n"
        "- Source discrepancy: the exact Milanovic 2016 figure 1.3 spreadsheet was not recovered; LM-WPID is a documented source-family dataset rather than the exact plotted figure-data file.\n"
        "- Visual discrepancy: the reconstructed curve has the same broad elephant shape but not the exact book trace. The middle peak and low-percentile points differ visibly from the Supplemental PDF reference.\n"
        "- Axis discrepancy: the book reference uses a 0-70 y-axis; the source-family reconstruction extends above 70 at the median, so its y-axis is 0-85 to avoid clipping recovered data.\n"
        "- Extension: no post-2008 extension is shown because no same-methodology successor file was recovered.\n"
    )

    (BASE / "anomaly_reviews/anomaly_review.md").write_text(
        "# Figure 9-5 Anomaly Review\n\n"
        "## Editorial Review\n\n"
        "- Critical question: Was the exact Milanovic 2016 figure-data file recovered? No. The recovered LM-WPID `.dta` is source-family evidence, not the final plotted `summary_data.xls` referenced in Milanovic presentations.\n"
        "- Data-integrity question: Were book chart pixels digitized? No.\n"
        "- Visual question: Does the recreated chart match the book figure exactly? No. It matches the elephant-curve concept and source family but differs at several fractiles.\n"
        "- Extension question: Is a comparable successor extension available? Not in this run; none is plotted.\n\n"
        "## Confidence\n\n"
        "- Overall confidence: medium for source-family provenance, low-to-medium for exact visual reproduction.\n"
        "- Recommended status: `partial_match`, not `verified_reproduction`.\n"
        "- Recommended next action: recover Milanovic/Lakner final `summary_data.xls` or author/publisher data for figure 1.3; alternatively obtain documented code that derives the exact 2016 book values from LM-WPID.\n"
    )

    checklist = (
        "# Figure Acceptance Checklist\n\n"
        "## Figure\n\n"
        "- Figure ID: 9-5\n"
        "- Title: Income gains, 1988-2008\n"
        "- Reviewer: Codex\n"
        f"- Review date: {TODAY}\n"
        "- Current status: partial_match\n\n"
        "## Phase 1 - Evidence Review\n\n"
        "- [x] Supplemental PDF figure inspected.\n"
        "- [x] Title extracted.\n"
        "- [x] Caption/source note extracted.\n"
        "- [x] Surrounding explanatory text reviewed.\n"
        "- [x] Bibliography/source mapping documented.\n\n"
        "## Phase 2 - Source Review\n\n"
        "- [ ] Exact Milanovic 2016 figure-data recovered.\n"
        "- [x] Closest inspectable source-family dataset recovered.\n"
        "- [x] Dataset provenance documented.\n"
        "- [x] Archive/moved-source notes documented.\n"
        "- [x] Successor extension evaluated and declined.\n\n"
        "## Phase 3 - Reconstruction Review\n\n"
        "- [x] Reconstruction uses legitimate source-family data.\n"
        "- [x] No digitized figure values used as reconstruction data.\n"
        "- [x] Transformation code is reproducible.\n"
        "- [x] Book-period comparison generated.\n"
        "- [x] Remaining book-period discrepancies explained.\n\n"
        "## Phase 4 - Extension Review\n\n"
        "- [x] Later data searched and documented.\n"
        "- [x] Extension left out because no genuinely comparable successor series was recovered.\n\n"
        "## Phase 5 - Reviewer Challenge\n\n"
        "- [x] Reviewer questions answered in anomaly review.\n\n"
        "## Final Decision\n\n"
        "- [ ] Accepted as `verified_reproduction`.\n"
        "- [x] Classified as `partial_match` pending exact figure-data recovery.\n"
    )
    (BASE / "review_checklist.md").write_text(checklist)

    (BASE / "README.md").write_text(
        "# Figure 9-5: Income gains, 1988-2008\n\n"
        "Status: `partial_match`\n\n"
        "This run recovered the CUNY Stone Center LM-WPID source-family Stata dataset and rebuilt a book-period growth-incidence curve from weighted 1988 and 2008 fractile means. "
        "The exact Milanovic 2016 figure 1.3 plotted spreadsheet was not recovered, so the result is not a verified reproduction.\n"
    )


def write_lineage_and_checksums() -> None:
    lineage_rows = [
        {
            "figure_id": FIG_ID,
            "artifact": "supplemental_pdf_reference_figure_9_5.png",
            "source": "references/enlightenment_now_supplemental_graphics.pdf page 11",
            "method": "pdftoppm render and deterministic crop",
        },
        {
            "figure_id": FIG_ID,
            "artifact": "figure_9_5_book_period_clean.csv",
            "source": "figures/9-5/data/raw/lm_wpid_web.dta",
            "method": "population-weighted fractile means, 1988 vs 2008",
        },
    ]
    csv_path = BASE / "lineage/figure_lineage.csv"
    with csv_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(lineage_rows[0]))
        writer.writeheader()
        writer.writerows(lineage_rows)
    (BASE / "lineage/figure_lineage.json").write_text(json.dumps(lineage_rows, indent=2) + "\n")

    checksum_targets = [
        *sorted((BASE / "data/raw").glob("*")),
        *sorted((BASE / "data/clean").glob("*")),
        *sorted((BASE / "plots").glob("*/*.png")),
        BASE / "metadata/metadata.json",
        BASE / "provenance/provenance.md",
    ]
    lines = []
    for path in checksum_targets:
        if path.is_file():
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            lines.append(f"{digest}  {path.relative_to(ROOT)}")
    (BASE / "checksums/sha256sums.txt").write_text("\n".join(lines) + "\n")


def main() -> None:
    ensure_dirs()
    reference = crop_reference()
    data = reconstruct_data()
    book_plot = BASE / "plots/book_period/figure_9_5_book_period_reconstruction.png"
    extended_plot = BASE / "plots/extended/figure_9_5_extended_reconstruction.png"
    plot_reconstruction(data, book_plot, extended=False)
    plot_reconstruction(data, extended_plot, extended=True)
    side_by_side(
        reference,
        book_plot,
        BASE / "plots/comparisons/figure_9_5_book_period_comparison.png",
        "Figure 9-5: Income gains, 1988-2008",
    )
    side_by_side(
        reference,
        extended_plot,
        BASE / "plots/comparisons/figure_9_5_extended_comparison.png",
        "Figure 9-5: Income gains, 1988-2008 - no comparable extension",
    )
    write_docs(data)
    write_lineage_and_checksums()


if __name__ == "__main__":
    main()
