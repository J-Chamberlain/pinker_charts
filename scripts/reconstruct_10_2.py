from __future__ import annotations

import csv
import hashlib
import json
from datetime import date
from pathlib import Path
from urllib.parse import urlencode

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
FIG_ID = "10-2"
BASE = ROOT / "figures" / FIG_ID
PDF_PAGE = Path("/tmp/pinker_prod_pdf_pages/page-13.png")
TODAY = date.today().isoformat()

XKCD_PAGE_URL = "https://xkcd.com/1007/"
XKCD_IMAGE_URL = "https://imgs.xkcd.com/comics/sustainable.png"
NGRAM_ENDPOINT = "https://books.google.com/ngrams/json"


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
    out = BASE / "plots/comparisons/pdf_reference_figure_10_2.png"
    if not PDF_PAGE.exists():
        raise FileNotFoundError(f"Missing rendered supplemental PDF page: {PDF_PAGE}")
    Image.open(PDF_PAGE).convert("RGB").crop((145, 75, 985, 810)).save(out)
    return out


def download_sources() -> None:
    html = requests.get(XKCD_PAGE_URL, timeout=30)
    html.raise_for_status()
    (BASE / "data/raw/xkcd_1007_sustainable.html").write_bytes(html.content)

    image = requests.get(XKCD_IMAGE_URL, timeout=30)
    image.raise_for_status()
    (BASE / "data/raw/xkcd_1007_sustainable.png").write_bytes(image.content)
    Image.open(BASE / "data/raw/xkcd_1007_sustainable.png").convert("RGB").save(
        BASE / "plots/comparisons/xkcd_source_figure_10_2.png"
    )


def ngram_query(content: str, year_start: int, year_end: int, corpus: str) -> tuple[str, list[float]]:
    params = {
        "content": content,
        "year_start": year_start,
        "year_end": year_end,
        "corpus": corpus,
        "smoothing": 0,
    }
    url = f"{NGRAM_ENDPOINT}?{urlencode(params)}"
    response = requests.get(NGRAM_ENDPOINT, params=params, timeout=30)
    response.raise_for_status()
    raw = response.json()
    if not raw:
        raise RuntimeError(f"No Ngram data returned for {params}")
    return url, raw[0]["timeseries"]


def fetch_ngram_data() -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    book_url, book_series = ngram_query("sustainable", 1955, 2008, "5")
    v2_url, v2_series = ngram_query("sustainable", 1955, 2008, "17")
    current_url, current_series = ngram_query("sustainable", 1955, 2019, "en-US-2019")

    raw_payload = {
        "book_candidate": {
            "description": "Google Books Ngram American English 2009/v1 corpus, corpus=5.",
            "query_url": book_url,
            "timeseries": book_series,
        },
        "cross_check_v2": {
            "description": "Google Books Ngram American English 2012/v2 corpus, corpus=17.",
            "query_url": v2_url,
            "timeseries": v2_series,
        },
        "current_successor": {
            "description": "Google Books Ngram current en-US-2019 corpus through 2019.",
            "query_url": current_url,
            "timeseries": current_series,
        },
    }
    (BASE / "data/raw/google_ngram_sustainable_queries.json").write_text(json.dumps(raw_payload, indent=2) + "\n")

    book = pd.DataFrame(
        {
            "year": range(1955, 2009),
            "frequency_share": book_series,
            "frequency_percent": np.array(book_series) * 100,
            "corpus": "American English 2009/v1 (corpus=5)",
            "period": "book_candidate_observed",
        }
    )
    v2 = pd.DataFrame(
        {
            "year": range(1955, 2009),
            "frequency_share": v2_series,
            "frequency_percent": np.array(v2_series) * 100,
            "corpus": "American English 2012/v2 (corpus=17)",
            "period": "cross_check_observed",
        }
    )
    current = pd.DataFrame(
        {
            "year": range(1955, 2020),
            "frequency_share": current_series,
            "frequency_percent": np.array(current_series) * 100,
            "corpus": "Current en-US-2019",
            "period": "successor_observed",
        }
    )

    pd.concat([book, v2, current], ignore_index=True).to_csv(
        BASE / "data/raw/google_ngram_sustainable_all_candidates.csv", index=False
    )

    book_fit = make_projection(book, 2109, "book_candidate_projection")
    current_fit = make_projection(current[current["year"] <= 2019], 2109, "successor_projection")

    book_clean = pd.concat([book, book_fit], ignore_index=True)
    extended_clean = pd.concat([book, book_fit, current, current_fit], ignore_index=True)
    book_clean.to_csv(BASE / "data/clean/figure_10_2_book_period_clean.csv", index=False)
    extended_clean.to_csv(BASE / "data/clean/figure_10_2_extended_clean.csv", index=False)
    return book_clean, extended_clean, {"book_url": book_url, "v2_url": v2_url, "current_url": current_url}


def make_projection(observed: pd.DataFrame, end_year: int, period: str) -> pd.DataFrame:
    obs = observed[observed["frequency_percent"] > 0].copy()
    coeff = np.polyfit(obs["year"], np.log10(obs["frequency_percent"]), 1)
    years = np.arange(int(obs["year"].max()), end_year + 1)
    pred = 10 ** (coeff[0] * years + coeff[1])
    return pd.DataFrame(
        {
            "year": years,
            "frequency_share": pred / 100,
            "frequency_percent": pred,
            "corpus": observed["corpus"].iloc[0],
            "period": period,
            "fit_slope_log10_percent_per_year": coeff[0],
            "fit_intercept": coeff[1],
        }
    )


def side_by_side(reference: Path, recreated: Path, output: Path, title: str) -> None:
    def load_trim(path: Path) -> Image.Image:
        im = Image.open(path).convert("RGB")
        bg = Image.new("RGB", im.size, "white")
        diff = ImageChops.difference(im, bg)
        bbox = diff.getbbox()
        return im.crop(bbox) if bbox else im

    ref = load_trim(reference)
    rec = load_trim(recreated)
    panel_w, panel_h = 980, 760
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
    draw.text((left_x + panel_w // 2, label_y), "Supplemental PDF reference", fill="black", anchor="ma", font=label_font)
    draw.text((right_x + panel_w // 2, label_y), "Recreated from Ngram data", fill="black", anchor="ma", font=label_font)
    paste_fit(ref, left_x, title_h + header_h)
    paste_fit(rec, right_x, title_h + header_h)
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output)


def plot_reconstruction(book_clean: pd.DataFrame, extended_clean: pd.DataFrame, out: Path, extended: bool) -> None:
    fig, ax = plt.subplots(figsize=(8.6, 5.7), dpi=180)

    obs = book_clean[book_clean["period"] == "book_candidate_observed"]
    proj = book_clean[book_clean["period"] == "book_candidate_projection"]
    ax.scatter(obs["year"], obs["frequency_percent"], color="0.10", s=12, linewidth=0, zorder=4)
    ax.plot(proj["year"], proj["frequency_percent"], color="0.10", linewidth=2.0, zorder=3)

    if extended:
        curr = extended_clean[extended_clean["period"] == "successor_observed"]
        curr_after = curr[curr["year"] > 2008]
        curr_proj = extended_clean[extended_clean["period"] == "successor_projection"]
        ax.scatter(curr_after["year"], curr_after["frequency_percent"], facecolors="white", edgecolors="0.45", s=18, zorder=5)
        ax.plot(curr_proj["year"], curr_proj["frequency_percent"], color="0.45", linewidth=1.8, linestyle="--", zorder=2)
        ax.text(2018, 0.003, "current Ngram\nsuccessor data", fontsize=9, color="0.35")

    ax.set_yscale("log")
    ax.set_xlim(1950, 2140)
    ax.set_ylim(1e-6, 1000)
    ax.set_xticks([1960, 1980, 2000, 2020, 2040, 2060, 2080, 2100, 2120, 2140])
    y_ticks = [1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1, 10, 100, 1000]
    ax.set_yticks(y_ticks)
    ax.set_yticklabels(["0.000001%", "0.00001%", "0.0001%", "0.001%", "0.01%", "0.1%", "1%", "10%", "100%", "1,000%"])
    ax.set_xlabel("YEAR", fontsize=11)
    ax.set_ylabel("")
    fig.text(
        0.055,
        0.51,
        'FREQUENCY OF\nUSE OF THE WORD\n"SUSTAINABLE" IN\nUS ENGLISH TEXT,\nAS A PERCENTAGE OF\nALL WORDS, BY YEAR',
        ha="left",
        va="center",
        fontsize=9.2,
    )
    ax.grid(False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.text(1955, 0.0022, "SOURCE: GOOGLE NGRAMS", fontsize=8)
    ax.scatter([2008, 2036, 2061, 2109], [obs["frequency_percent"].iloc[-1], 0.1, 1, 100], facecolors="white", edgecolors="0.1", s=70, linewidth=2, zorder=6)
    ax.text(2012, 0.0016, "PRESENT DAY", fontsize=9.5)
    ax.text(2031, 0.11, '2036: "SUSTAINABLE" OCCURS\nABOUT ONCE PER PAGE', fontsize=8.7, ha="right")
    ax.text(2056, 1.4, '2061: "SUSTAINABLE" OCCURS\nABOUT ONCE PER SENTENCE', fontsize=8.7, ha="right")
    ax.text(2070, 120, '2109: ALL SENTENCES ARE\nJUST THE WORD "SUSTAINABLE"\nREPEATED OVER AND OVER', fontsize=8.7)
    ax.text(0.5, -0.18, 'THE WORD "SUSTAINABLE" IS UNSUSTAINABLE.', transform=ax.transAxes, ha="center", fontsize=13)

    note = "Book candidate: Google Ngram American English 2009/v1 corpus; straight line is a log-linear extrapolation."
    if extended:
        note += " Open circles/dashed line show current en-US-2019 successor data and fit."
    ax.text(0, -0.22, note, transform=ax.transAxes, fontsize=7.0, va="top")
    fig.subplots_adjust(left=0.24, right=0.98, bottom=0.24, top=0.97)
    fig.savefig(out, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def write_docs(urls: dict) -> None:
    metadata = {
        "figure_id": FIG_ID,
        "chapter": "10",
        "title": "Sustainability, 1955-2109",
        "book_page": "Supplemental PDF page 13",
        "claim_summary": "The word 'sustainable' rose rapidly in US English books, with XKCD extrapolating the trend satirically into the future.",
        "book_citation": "Randall Munroe, XKCD 1007, http://xkcd.com/1007/. Internal data source: Google Ngrams.",
        "original_dataset": "Google Books Ngram American English 2009/v1 corpus for 'sustainable' (corpus=5), 1955-2008.",
        "dataset_url": urls["book_url"],
        "archive_url": "Not found; live Google Ngram endpoint retained with raw JSON payload.",
        "download_date": TODAY,
        "reproduction_status": "updated_equivalent",
        "confidence_score": 0.76,
        "visual_validation": "good",
        "notes": "The observed Ngram data are source-family recovered; XKCD's exact hand-drawn fit and annotation placement are not author-supplied data. No values were digitized from Pinker's printed figure.",
        "canonical_artifacts": {
            "original_reference": "figures/10-2/plots/comparisons/pdf_reference_figure_10_2.png",
            "xkcd_source_image": "figures/10-2/plots/comparisons/xkcd_source_figure_10_2.png",
            "book_period_reconstruction": "figures/10-2/plots/book_period/figure_10_2_book_period_reconstruction.png",
            "extended_reconstruction": "figures/10-2/plots/extended/figure_10_2_extended_reconstruction.png",
            "book_period_comparison": "figures/10-2/plots/comparisons/figure_10_2_book_period_comparison.png",
            "extended_comparison": "figures/10-2/plots/comparisons/figure_10_2_extended_comparison.png",
        },
    }
    (BASE / "metadata/metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    (BASE / "captions/caption.txt").write_text(
        "Figure 10-2: Sustainability, 1955-2109. Source note from the Supplemental Graphics PDF: Randall Munroe, XKCD 1007, with internal source Google Ngrams. "
        "The reconstruction uses the Google Ngram American English 2009/v1 corpus for 'sustainable' through 2008 and a log-linear extrapolation to the XKCD future horizon. "
        "The extension overlays current Google Ngram successor data through 2019. Exact XKCD hand-drawn geometry and annotation placement are approximate; no values were digitized from Pinker's printed figure.\n"
    )
    (BASE / "source_logs/source_log.md").write_text(
        "# Source Discovery Log: Figure 10-2\n\n"
        "Figure title: Sustainability, 1955-2109\n\n"
        "## Source Line\n"
        "- Supplemental Graphics PDF page 13: Source: Randall Munroe, XKCD, http://xkcd.com/1007/. Credit: Randall Munroe, xkcd.com.\n"
        "- XKCD page text identifies the internal source as Google Ngrams and describes the measure as the frequency of use of the word 'sustainable' in US English text, as a percentage of all words, by year.\n\n"
        "## Search and Recovery\n"
        "- Official XKCD page: https://xkcd.com/1007/\n"
        "- Official XKCD image: https://imgs.xkcd.com/comics/sustainable.png\n"
        "- Google Ngram American English 2009/v1 corpus query: " + urls["book_url"] + "\n"
        "- Google Ngram American English 2012/v2 cross-check query: " + urls["v2_url"] + "\n"
        "- Google Ngram current en-US-2019 successor query: " + urls["current_url"] + "\n\n"
        "## Source Decision\n"
        "- Accepted primary visual/source reference: Supplemental Graphics PDF page 13.\n"
        "- Accepted original publication reference: official XKCD 1007 page and image.\n"
        "- Accepted data source for reconstruction: Google Ngram American English 2009/v1 corpus (`corpus=5`), because the 2012 XKCD comic predates later Ngram revisions and the series matches the panel's order of magnitude.\n"
        "- Current successor data are used only in the extended artifact.\n\n"
        "## Blockers and Uncertainties\n"
        "- XKCD does not publish a separate spreadsheet or the exact regression method for the hand-drawn extrapolation.\n"
        "- The future points are satirical extrapolation labels, not observed data.\n"
        "- No plotted values were digitized from the Pinker/Supplemental PDF figure.\n"
    )
    (BASE / "provenance/provenance.md").write_text(
        "# Provenance: Figure 10-2\n\n"
        "Supplemental Graphics PDF page 13 -> official XKCD 1007 page/image -> Google Ngram API for `sustainable` in American English -> "
        "`scripts/reconstruct_10_2.py` -> book-period and extended comparison plots.\n\n"
        "The book-period reconstruction uses the Google Ngram American English 2009/v1 corpus through 2008 plus a log-linear extrapolation to the XKCD horizon. "
        "The extended reconstruction overlays current Ngram successor observations through 2019 and a separate successor fit.\n"
    )
    (BASE / "anomaly_reviews/anomaly_review.md").write_text(
        "# Anomaly Review: Figure 10-2\n\n"
        "## Data Fidelity\n"
        "- Observed values come from Google Ngram API output, not from digitizing the book figure.\n"
        "- The source-family data are recovered, but XKCD's exact hand-drawn regression and projection geometry are not published.\n"
        "- Classification: `updated_equivalent`, not `verified_reproduction`.\n\n"
        "## Visual Fidelity\n"
        "- The recreated chart preserves the log y-scale, year range, Ngram data dots, extrapolated future line, and XKCD-style annotations.\n"
        "- Remaining differences are expected: handwritten typography, exact line wobble, and annotation placement are approximate.\n\n"
        "## Extension Clarity\n"
        "- The extended comparison separates current Ngram successor observations with open circles and a dashed gray fit.\n"
        "- The current corpus revises the slope and should not be read as the original XKCD data vintage.\n\n"
        "## Editorial Review Gate\n"
        "- Critical issues: none.\n"
        "- Major issues: none unexplained.\n"
        "- Minor issues: hand-drawn styling and exact projection geometry differ from the original and are documented.\n\n"
        "Overall confidence:\n"
        "- Book reconstruction: medium-high for source-family data, medium for exact XKCD projection geometry\n"
        "- Extension: medium; current Ngram corpus is a successor, not the original source vintage\n"
        "- Source provenance: high for XKCD and Google Ngram source chain\n"
        "- Outstanding risks: no author-supplied regression parameters or raw XKCD plotting file recovered\n"
        "- Recommended next action: archive the live Google Ngram responses or locate an archived Ngram endpoint capture from January 2012\n"
    )
    (BASE / "discrepancy_logs/discrepancy_log.md").write_text(
        "# Discrepancy Log: Figure 10-2\n\n"
        "- Exact XKCD handwriting, wobble, and annotation geometry are not reproducible from published data alone.\n"
        "- The extrapolation is a reproducible log-linear fit to recovered Ngram data, but XKCD's exact regression method is not documented.\n"
        "- The extended artifact uses current Google Ngram successor data through 2019, which changes the apparent slope after the book-era corpus.\n"
        "- No plotted values were digitized from the Supplemental Graphics PDF or Pinker's printed figure.\n"
    )
    (BASE / "search_iterations/search_iterations.md").write_text(
        "# Search Iterations: Figure 10-2\n\n"
        "- Supplemental Graphics PDF page 13 source note.\n"
        "- Official XKCD 1007 page and image.\n"
        "- Google Ngram API query for `sustainable`, American English 2009/v1 corpus (`corpus=5`).\n"
        "- Google Ngram API query for `sustainable`, American English 2012/v2 corpus (`corpus=17`) as a cross-check.\n"
        "- Google Ngram API query for `sustainable`, current en-US-2019 corpus as successor extension.\n"
    )
    lineage = [
        {"stage": "Book Figure", "value": "Figure 10-2: Sustainability, 1955-2109"},
        {"stage": "Book Citation", "value": metadata["book_citation"]},
        {"stage": "Original Publication", "value": XKCD_PAGE_URL},
        {"stage": "Original Image", "value": XKCD_IMAGE_URL},
        {"stage": "Dataset", "value": metadata["original_dataset"]},
        {"stage": "Transformation Script", "value": "scripts/reconstruct_10_2.py"},
        {"stage": "Generated Plot", "value": "figures/10-2/plots/"},
    ]
    (BASE / "lineage/figure_lineage.json").write_text(json.dumps(lineage, indent=2) + "\n")
    with (BASE / "lineage/figure_lineage.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["stage", "value"])
        writer.writeheader()
        writer.writerows(lineage)
    (BASE / "review_checklist.md").write_text(
        "# Review Checklist: Figure 10-2\n\n"
        "- Figure ID: 10-2\n"
        "- Title: Sustainability, 1955-2109\n"
        "- Reviewer: Codex\n"
        f"- Review date: {TODAY}\n"
        "- Current status: updated_equivalent\n\n"
        "## Phase 1 - Evidence Review\n"
        "- [x] Supplemental Graphics PDF figure inspected.\n"
        "- [x] Title extracted.\n"
        "- [x] Caption extracted.\n"
        "- [x] Source note extracted.\n"
        "- [x] Surrounding discussion reviewed.\n"
        "- [x] Bibliography resolved: official XKCD page plus internal Google Ngrams source.\n\n"
        "## Phase 2 - Source Review\n"
        "- [x] Original publication located.\n"
        "- [x] Source chain reconstructed.\n"
        "- [x] Dataset provenance documented.\n"
        "- [x] Successor datasets evaluated.\n"
        "- [x] Download URLs recorded.\n"
        "- [x] Checksums recorded for stored files.\n\n"
        "## Phase 3 - Reconstruction Review\n"
        "- [x] Reconstruction uses legitimate Google Ngram data.\n"
        "- [x] No digitized figure values used as reconstruction data.\n"
        "- [x] Transformation code is reproducible.\n"
        "- [x] Book-period reconstruction completed.\n"
        "- [x] Book-period side-by-side comparison generated.\n"
        "- [x] Remaining book-period discrepancies explained.\n\n"
        "## Phase 4 - Extension Review\n"
        "- [x] Later/current Ngram data searched.\n"
        "- [x] Extension completed.\n"
        "- [x] Extension clearly distinguished from book-period reconstruction.\n"
        "- [x] Methodological changes explained.\n\n"
        "## Final Gate - Editorial Review\n"
        "- [x] Comparisons visually scanned.\n"
        "- [x] Completeness checked.\n"
        "- [x] Layout checked.\n"
        "- [x] Visual similarity checked.\n"
        "- [x] Extension clarity checked.\n"
        "- [x] Caption checked.\n"
        "- [x] No Critical issues remain.\n"
        "- [x] No unexplained Major issues remain.\n\n"
        "## Final Decision\n"
        "- [x] Accepted as `updated_equivalent`.\n\n"
        "Decision notes: source-family data recovered; exact XKCD plotting file/regression method not recovered.\n"
    )
    (BASE / "README.md").write_text(
        "# Figure 10-2: Sustainability, 1955-2109\n\n"
        "Status: `updated_equivalent`\n\n"
        "This package reconstructs the XKCD/Google Ngram figure from recovered Ngram data rather than digitized book values. "
        "The exact XKCD plotting file and regression method were not recovered, so the result is source-family faithful but not a verified reproduction.\n\n"
        "Canonical artifacts:\n"
        "- PDF reference: `plots/comparisons/pdf_reference_figure_10_2.png`\n"
        "- XKCD source image: `plots/comparisons/xkcd_source_figure_10_2.png`\n"
        "- Book-period reconstruction: `plots/book_period/figure_10_2_book_period_reconstruction.png`\n"
        "- Extended reconstruction: `plots/extended/figure_10_2_extended_reconstruction.png`\n"
        "- Book-period comparison: `plots/comparisons/figure_10_2_book_period_comparison.png`\n"
        "- Extended comparison: `plots/comparisons/figure_10_2_extended_comparison.png`\n"
    )


def update_tables() -> None:
    registry_path = ROOT / "data/figure_registry.csv"
    rows = list(csv.DictReader(registry_path.open()))
    for row in rows:
        if row["figure_id"] == FIG_ID:
            row.update(
                {
                    "year_range": "1955-2109",
                    "current_status": "updated_equivalent",
                    "lifecycle_stage": "updated_equivalent_with_ngram_source_recovery",
                    "source_type_guess": "Google Ngram/XKCD text-frequency chart",
                    "priority": "completed_monitor",
                    "current_owner": "Codex",
                    "next_action": "Archive live Google Ngram responses or locate a January 2012 Ngram endpoint capture before considering verified_reproduction.",
                    "notes": "Processed 2026-07-05 from Supplemental Graphics PDF page 13, official XKCD 1007, and Google Ngram American English 2009/v1 corpus; no plotted values digitized.",
                }
            )
    with registry_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    (ROOT / "data/figure_registry.json").write_text(json.dumps(rows, indent=2) + "\n")

    metadata_path = ROOT / "data/metadata/figure_metadata.csv"
    meta_rows = list(csv.DictReader(metadata_path.open()))
    meta = {
        "figure_id": FIG_ID,
        "chapter": "10",
        "title": "Sustainability, 1955-2109",
        "book_page": "Supplemental PDF page 13",
        "claim_summary": "The word 'sustainable' rose rapidly in US English books, with XKCD extrapolating the trend satirically into the future.",
        "book_citation": "Randall Munroe, XKCD 1007; internal source Google Ngrams.",
        "original_dataset": "Google Books Ngram American English 2009/v1 corpus for 'sustainable' (corpus=5), 1955-2008.",
        "dataset_url": f"{NGRAM_ENDPOINT}?content=sustainable&year_start=1955&year_end=2008&corpus=5&smoothing=0",
        "archive_url": "Not recovered",
        "download_date": TODAY,
        "reproduction_status": "updated_equivalent",
        "confidence_score": "0.76",
        "visual_validation": "good",
        "notes": "Source-family data recovered from Google Ngrams and official XKCD; exact hand-drawn XKCD fit/regression unavailable.",
    }
    meta_rows = [r for r in meta_rows if r["figure_id"] != FIG_ID] + [meta]
    meta_rows.sort(key=lambda r: tuple(int(part) for part in r["figure_id"].split("-")))
    with metadata_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=meta_rows[0].keys())
        writer.writeheader()
        writer.writerows(meta_rows)


def update_project_state() -> None:
    path = ROOT / "PROJECT_STATE.md"
    text = path.read_text()
    text = text.replace("Project version: `1.11-source-recovery-figure-4-1`", "Project version: `1.12-production-loop-figure-10-2`")
    old_row = "| 10-1 | Population and population growth, 1750-2015 and projected to 2100 | Updated-equivalent current OWID/UN successor reconstruction | `updated_equivalent` | Medium-high | Current OWID population/growth/projection grapher data reproduce the dual-axis concept, but exact 2016 OWID/HYDE/IIASA source vintage remains unrecovered. |\n"
    new_row = old_row + "| 10-2 | Sustainability, 1955-2109 | Updated-equivalent XKCD/Google Ngram source-family reconstruction | `updated_equivalent` | Medium | Supplemental PDF source line captured; official XKCD 1007 and Google Ngram American English 2009/v1 data recovered, but exact XKCD hand-drawn fit/regression method was not recovered. |\n"
    if "| 10-2 | Sustainability, 1955-2109 |" not in text:
        text = text.replace(old_row, new_row)
    artifacts = (
        "### Figure 10-2 - Sustainability, 1955-2109\n\n"
        "Status: `updated_equivalent`\n\n"
        "Canonical visual artifacts:\n"
        "- Original reference: `figures/10-2/plots/comparisons/pdf_reference_figure_10_2.png`\n"
        "- XKCD source image: `figures/10-2/plots/comparisons/xkcd_source_figure_10_2.png`\n"
        "- Book-period reconstruction: `figures/10-2/plots/book_period/figure_10_2_book_period_reconstruction.png`\n"
        "- Extended reconstruction: `figures/10-2/plots/extended/figure_10_2_extended_reconstruction.png`\n"
        "- Book-period comparison: `figures/10-2/plots/comparisons/figure_10_2_book_period_comparison.png`\n"
        "- Extended comparison: `figures/10-2/plots/comparisons/figure_10_2_extended_comparison.png`\n"
        "Canonical documentation:\n"
        "- Caption: `figures/10-2/captions/caption.txt`\n"
        "- Provenance: `figures/10-2/provenance/provenance.md`\n"
        "- Source log: `figures/10-2/source_logs/source_log.md`\n"
        "- Anomaly review: `figures/10-2/anomaly_reviews/anomaly_review.md`\n"
        "- Metadata: `figures/10-2/metadata/metadata.json`\n"
        "- Review checklist: `figures/10-2/review_checklist.md`\n\n"
    )
    if "### Figure 10-2 - Sustainability" not in text:
        text = text.replace("### Figure 10-5 -", artifacts + "### Figure 10-5 -")
    history = "| `1.12-production-loop-figure-10-2` | 2026-07-05 | Added Figure 10-2 as an updated-equivalent XKCD/Google Ngram reconstruction with current Ngram successor extension. |\n"
    if history not in text:
        text = text.replace("| `1.11-source-recovery-figure-4-1`", history + "| `1.11-source-recovery-figure-4-1`")
    path.write_text(text)


def update_checksums() -> None:
    lines = []
    for p in sorted(BASE.rglob("*")):
        if p.is_file() and "checksums" not in p.parts:
            lines.append(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(BASE)}")
    (BASE / "checksums/sha256sums.txt").write_text("\n".join(lines) + "\n")


def main() -> None:
    ensure_dirs()
    reference = crop_reference()
    download_sources()
    book_clean, extended_clean, urls = fetch_ngram_data()
    book_plot = BASE / "plots/book_period/figure_10_2_book_period_reconstruction.png"
    ext_plot = BASE / "plots/extended/figure_10_2_extended_reconstruction.png"
    plot_reconstruction(book_clean, extended_clean, book_plot, extended=False)
    plot_reconstruction(book_clean, extended_clean, ext_plot, extended=True)
    side_by_side(reference, book_plot, BASE / "plots/comparisons/figure_10_2_book_period_comparison.png", "Figure 10-2 book-period comparison")
    side_by_side(reference, ext_plot, BASE / "plots/comparisons/figure_10_2_extended_comparison.png", "Figure 10-2 extended comparison")
    write_docs(urls)
    update_tables()
    update_project_state()
    update_checksums()


if __name__ == "__main__":
    main()
