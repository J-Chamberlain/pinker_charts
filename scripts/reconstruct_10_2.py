from __future__ import annotations

import csv
import hashlib
import json
import math
import subprocess
from datetime import date
from pathlib import Path
from textwrap import wrap

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageOps
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
FIG_ID = "10-2"
BASE = ROOT / "figures" / FIG_ID
TODAY = date.today().isoformat()

PDF = ROOT / "references/enlightenment_now_supplemental_graphics.pdf"
PDF_RENDER = Path("/tmp/pinker_10_2_pdf/page13.png")
XKCD_INFO_URL = "https://xkcd.com/1007/info.0.json"
XKCD_PAGE_URL = "https://xkcd.com/1007/"
XKCD_IMAGE_URL = "https://imgs.xkcd.com/comics/sustainable.png"
NGRAM_URL = "https://books.google.com/ngrams/json"


def ensure_dirs() -> None:
    for part in [
        "metadata",
        "provenance",
        "source_logs",
        "anomaly_reviews",
        "captions",
        "plots/book_period",
        "plots/extended",
        "plots/comparisons",
        "data/raw",
        "data/clean",
        "checksums",
    ]:
        (BASE / part).mkdir(parents=True, exist_ok=True)


def get(url: str, **kwargs) -> requests.Response:
    resp = requests.get(url, timeout=60, **kwargs)
    resp.raise_for_status()
    return resp


def render_pdf_page() -> None:
    PDF_RENDER.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "pdftoppm",
            "-png",
            "-r",
            "220",
            "-f",
            "13",
            "-singlefile",
            str(PDF),
            str(PDF_RENDER.with_suffix("")),
        ],
        check=True,
    )


def crop_reference() -> Path:
    render_pdf_page()
    out = BASE / "plots/comparisons/pdf_reference_figure_10_2.png"
    Image.open(PDF_RENDER).convert("RGB").crop((170, 95, 1175, 1055)).save(out)
    return out


def download_sources() -> dict[str, Path]:
    raw = BASE / "data/raw"
    info = get(XKCD_INFO_URL).json()
    (raw / "xkcd_1007_info.json").write_text(json.dumps(info, indent=2) + "\n")
    (raw / "xkcd_1007_page.html").write_text(get(XKCD_PAGE_URL).text)
    (raw / "xkcd_sustainable.png").write_bytes(get(XKCD_IMAGE_URL).content)

    for corpus, year_end, name in [
        ("en-US-2012", 2008, "google_ngram_sustainable_en_us_2012.json"),
        ("en-US-2019", 2022, "google_ngram_sustainable_en_us_2019.json"),
    ]:
        params = {
            "content": "sustainable",
            "year_start": 1950,
            "year_end": year_end,
            "corpus": corpus,
            "smoothing": 3,
        }
        (raw / name).write_text(json.dumps(get(NGRAM_URL, params=params).json(), indent=2) + "\n")

    return {
        "xkcd_info": raw / "xkcd_1007_info.json",
        "xkcd_image": raw / "xkcd_sustainable.png",
        "ngram_2012": raw / "google_ngram_sustainable_en_us_2012.json",
        "ngram_2019": raw / "google_ngram_sustainable_en_us_2019.json",
    }


def parse_ngram(path: Path, start_year: int, end_year: int, corpus: str) -> pd.DataFrame:
    data = json.loads(path.read_text())
    series = data[0]["timeseries"]
    years = list(range(start_year, end_year + 1))
    df = pd.DataFrame({"year": years, "frequency_share": series})
    df["frequency_percent"] = df["frequency_share"] * 100
    df["term"] = "sustainable"
    df["corpus"] = corpus
    return df


def clean_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    book = parse_ngram(BASE / "data/raw/google_ngram_sustainable_en_us_2012.json", 1950, 2008, "en-US-2012")
    book = book[book["year"].between(1955, 2008)].copy()
    book["data_role"] = "recovered_google_ngram_actual"

    # These are not recovered Ngram observations. They are the future annotation
    # anchors stated by xkcd's own transcript and are kept separate in clean data.
    anchors = pd.DataFrame(
        [
            {"year": 2036, "frequency_percent": 0.1, "label": "once per page"},
            {"year": 2061, "frequency_percent": 1.0, "label": "once per sentence"},
            {"year": 2109, "frequency_percent": 100.0, "label": "all sentences are sustainable"},
        ]
    )
    anchors["term"] = "sustainable"
    anchors["corpus"] = "xkcd transcript annotation"
    anchors["frequency_share"] = anchors["frequency_percent"] / 100
    anchors["data_role"] = "xkcd_transcript_future_anchor"

    current = parse_ngram(BASE / "data/raw/google_ngram_sustainable_en_us_2019.json", 1950, 2022, "en-US-2019")
    current = current[(current["year"].between(2009, 2019)) & (current["frequency_percent"] > 0)].copy()
    current["data_role"] = "successor_google_ngram_actual"

    book_out = pd.concat([book, anchors], ignore_index=True, sort=False)
    book_out.to_csv(BASE / "data/clean/figure_10_2_book_period_clean.csv", index=False)
    pd.concat([book, anchors, current], ignore_index=True, sort=False).to_csv(
        BASE / "data/clean/figure_10_2_extended_clean.csv", index=False
    )
    return book, anchors, current


def xkcd_anchor_curve(book: pd.DataFrame, anchors: pd.DataFrame) -> pd.DataFrame:
    last = book.loc[book["year"].idxmax()]
    pts = pd.concat(
        [
            pd.DataFrame([{"year": int(last["year"]), "frequency_percent": float(last["frequency_percent"])}]),
            anchors[["year", "frequency_percent"]],
        ],
        ignore_index=True,
    )
    x = pts["year"].to_numpy()
    y = np.log10(pts["frequency_percent"].to_numpy())
    xi = np.arange(int(x.min()), 2141)
    yi = np.interp(xi, x, y)
    return pd.DataFrame({"year": xi, "frequency_percent": 10**yi})


def style_xkcd_axis(ax: plt.Axes) -> None:
    ax.set_yscale("log")
    ax.set_xlim(1950, 2140)
    ax.set_ylim(0.000001, 1000)
    ax.set_xticks([1960, 1980, 2000, 2020, 2040, 2060, 2080, 2100, 2120, 2140])
    ticks = [0.000001, 0.00001, 0.0001, 0.001, 0.01, 0.1, 1, 10, 100, 1000]
    ax.set_yticks(ticks)
    ax.set_yticklabels(["0.000001%", "0.00001%", "0.0001%", "0.001%", "0.01%", "0.1%", "1%", "10%", "100%", "1,000%"])
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(False)
    ax.tick_params(axis="both", labelsize=8)
    ax.set_xlabel("Year", fontsize=11)
    ax.set_ylabel('Frequency of "sustainable" in US English text\n(percent of all words)', fontsize=10)


def plot_reconstruction(book: pd.DataFrame, anchors: pd.DataFrame, current: pd.DataFrame, out: Path, extended: bool) -> None:
    curve = xkcd_anchor_curve(book, anchors)
    fig, ax = plt.subplots(figsize=(8.2, 5.4), dpi=180)
    style_xkcd_axis(ax)

    ax.scatter(book["year"], book["frequency_percent"], s=13, color="0.15", alpha=0.9, label="Google Ngram actual, en-US 2012")
    curve_part = curve[curve["year"].between(2008, 2109)]
    ax.plot(curve_part["year"], curve_part["frequency_percent"], color="0.1", linewidth=2.0, label="xkcd transcript-anchor interpolation")
    ax.scatter(anchors["year"], anchors["frequency_percent"], s=52, facecolors="white", edgecolors="0.1", linewidths=1.8, zorder=4)

    if extended:
        ax.scatter(
            current["year"],
            current["frequency_percent"],
            s=22,
            color="#2f6f9f",
            alpha=0.95,
            label="Successor actual, en-US 2019",
            zorder=5,
        )

    ax.axhline(100, color="0.2", linewidth=1.0)
    ax.text(2037, 0.14, "2036: once per page", fontsize=8)
    ax.text(2062, 1.35, "2061: once per sentence", fontsize=8)
    ax.text(2072, 135, "2109: all sentences are\njust the word sustainable", fontsize=8)
    if extended:
        ax.text(2017, 0.0011, "successor actuals stay far below\nthe comic extrapolation", fontsize=8, color="#2f6f9f")
    ax.set_title("Figure 10-2: Sustainability, 1955-2109", loc="left", fontsize=12)
    ax.legend(loc="lower right", frameon=False, fontsize=8)
    note = "Source data: Google Books Ngram API. Future anchors are from xkcd 1007 transcript, not observed Ngram data."
    if extended:
        note += " Blue points use a newer Ngram corpus through 2019."
    ax.text(0, -0.18, note, transform=ax.transAxes, fontsize=7)
    fig.tight_layout()
    out.parent.mkdir(parents=True, exist_ok=True)
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
    panel_w, panel_h = 980, 720
    margin, gap, header_h, title_h = 45, 45, 58, 58
    canvas_im = Image.new("RGB", (margin * 2 + panel_w * 2 + gap, title_h + header_h + panel_h + margin), "white")
    draw = ImageDraw.Draw(canvas_im)
    try:
        title_font = ImageFont.truetype("Arial.ttf", 30)
        label_font = ImageFont.truetype("Arial.ttf", 24)
    except OSError:
        title_font = label_font = None

    def paste_fit(im: Image.Image, x: int, y: int) -> None:
        fitted = ImageOps.contain(im, (panel_w, panel_h), method=Image.Resampling.LANCZOS)
        canvas_im.paste(fitted, (x + (panel_w - fitted.width) // 2, y + (panel_h - fitted.height) // 2))
        draw.rectangle([x, y, x + panel_w, y + panel_h], outline=(230, 230, 230), width=1)

    left_x = margin
    right_x = margin + panel_w + gap
    draw.text((canvas_im.width // 2, 18), title, fill="black", anchor="ma", font=title_font)
    draw.text((left_x + panel_w // 2, title_h + 8), "Supplemental PDF reference", fill="black", anchor="ma", font=label_font)
    draw.text((right_x + panel_w // 2, title_h + 8), "Recreated from recovered source data", fill="black", anchor="ma", font=label_font)
    paste_fit(ref, left_x, title_h + header_h)
    paste_fit(rec, right_x, title_h + header_h)
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas_im.save(output)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_checksums() -> None:
    rows = []
    for path in sorted((BASE).rglob("*")):
        if path.is_file() and "checksums" not in path.parts:
            rows.append(f"{sha256(path)}  {path.relative_to(ROOT)}")
    (BASE / "checksums/review_scroll_sha256sums.txt").write_text("\n".join(rows) + "\n")


def write_docs() -> None:
    metadata = {
        "figure_id": "10-2",
        "chapter": "10",
        "title": "Sustainability, 1955-2109",
        "book_page": "Supplemental PDF page 13",
        "claim_summary": "A humorous xkcd extrapolation shows the word 'sustainable' rising in Google Ngram frequency until all sentences become the word sustainable.",
        "book_citation": "Randall Munroe, XKCD, http://xkcd.com/1007/. Credit: Randall Munroe, xkcd.com.",
        "original_dataset": "Google Books Ngram Viewer US English 2012 corpus for the word sustainable; xkcd future annotation anchors from comic 1007 transcript.",
        "dataset_url": f"{XKCD_INFO_URL}; {XKCD_IMAGE_URL}; {NGRAM_URL}?content=sustainable&year_start=1950&year_end=2008&corpus=en-US-2012&smoothing=3",
        "archive_url": "Not captured; original xkcd page and current Google Ngram API were available directly.",
        "download_date": TODAY,
        "reproduction_status": "updated_equivalent",
        "confidence_score": 0.74,
        "visual_validation": "good_with_documented_fit_difference",
        "notes": "The source comic and Google Ngram data were recovered. xkcd did not publish its exact extrapolation/fitting method, so the reconstruction uses recovered Ngram actuals and separately labeled xkcd transcript future anchors rather than digitized Pinker values.",
        "canonical_artifacts": {
            "original_reference": "figures/10-2/plots/comparisons/pdf_reference_figure_10_2.png",
            "book_period_reconstruction": "figures/10-2/plots/book_period/figure_10_2_book_period_reconstruction.png",
            "extended_reconstruction": "figures/10-2/plots/extended/figure_10_2_extended_reconstruction.png",
            "book_period_comparison": "figures/10-2/plots/comparisons/figure_10_2_book_period_comparison.png",
            "extended_comparison": "figures/10-2/plots/comparisons/figure_10_2_extended_comparison.png",
        },
    }
    (BASE / "metadata/metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    (BASE / "captions/caption.txt").write_text(
        "Figure 10-2: Sustainability, 1955-2109. The Supplemental Graphics PDF reproduces xkcd 1007 by Randall Munroe. "
        "The reconstruction uses Google Books Ngram API data for the word sustainable in the US English 2012 corpus, plus future anchor annotations stated in the xkcd transcript. "
        "Because xkcd did not publish a numeric fitting formula, this is classified as an updated_equivalent/source-chain reconstruction rather than a verified recreation of every hand-drawn mark. "
        "The extended comparison overlays the newer US English 2019 corpus through 2019 and shows it separately from the comic extrapolation.\n"
    )
    (BASE / "source_logs/source_log.md").write_text(
        "# Source Discovery Log: Figure 10-2\n\n"
        "Figure title: Sustainability, 1955-2109\n\n"
        "## PDF Reference\n\n"
        "- Supplemental Graphics PDF page 13 inspected.\n"
        "- Source line: Randall Munroe, XKCD, http://xkcd.com/1007/. Credit: Randall Munroe, xkcd.com.\n"
        "- Surrounding text reviewed: Pinker uses the comic while discussing environmental pessimism and rebound/improvement claims.\n\n"
        "## Sources Investigated\n\n"
        f"- xkcd comic page: {XKCD_PAGE_URL} accepted as original visual/source page.\n"
        f"- xkcd JSON metadata: {XKCD_INFO_URL} accepted for title, image URL, transcript, and alt text.\n"
        f"- xkcd image: {XKCD_IMAGE_URL} downloaded as original source visual.\n"
        "- Google Books Ngram API, `sustainable`, corpus `en-US-2012`, smoothing 3: accepted as recovered book-era source data family named by xkcd.\n"
        "- Google Books Ngram API, `sustainable`, corpus `en-US-2019`, smoothing 3: accepted only as successor extension data through 2019; 2020-2022 zero outputs were excluded as incomplete/invalid API tail values.\n"
        "- Exact xkcd fitting formula: not located. The comic transcript states future anchors at 2036, 2061, and 2109, but does not publish the fitted line parameters.\n\n"
        "## Search Queries/Checks\n\n"
        "- xkcd 1007 sustainable Google Ngrams data sustainable\n"
        "- Google Ngram Viewer API corpus 17 sustainable 1950 2008\n"
        "- xkcd sustainable source Google NGrams Randall Munroe data\n"
        "- Direct probes of `books.google.com/ngrams/json` with `en-US-2012`, numeric corpus `17`, and `en-US-2019`.\n\n"
        "## Data Use Decision\n\n"
        "No values were digitized from Pinker's plotted figure. The observed series comes from Google Ngram API responses. Future annotation anchors come from xkcd's own transcript and are labeled separately in the clean data.\n"
    )
    (BASE / "provenance/provenance.md").write_text(
        "# Provenance: Figure 10-2\n\n"
        "- Primary visual reference: `references/enlightenment_now_supplemental_graphics.pdf`, page 13.\n"
        "- Original source visual: xkcd 1007, `Sustainable`, downloaded from xkcd's image URL.\n"
        "- Underlying observed data: Google Books Ngram API query for `sustainable`, US English 2012 corpus, years 1950-2008, smoothing 3.\n"
        "- Successor extension data: Google Books Ngram API query for `sustainable`, US English 2019 corpus, years 1950-2022, smoothing 3; only nonzero 2009-2019 extension observations are plotted.\n"
        "- Transformation: `scripts/reconstruct_10_2.py` parses the API JSON, converts shares to percentages, keeps xkcd future anchors as a separate role, and plots side-by-side comparisons.\n\n"
        "## Limitations\n\n"
        "xkcd did not publish the exact extrapolation/fitting method. The reconstruction therefore preserves data roles rather than forcing a false exact match: observed Ngram values are source data; future points are xkcd transcript annotations; the connecting future line is an interpolation through those annotations.\n"
    )
    (BASE / "anomaly_reviews/anomaly_review.md").write_text(
        "# Anomaly Review: Figure 10-2\n\n"
        f"- Review date: {TODAY}\n"
        "- Status: `updated_equivalent`\n\n"
        "## Data Fidelity\n\n"
        "The original source chain was recovered: xkcd 1007 names Google Ngrams, and Google Ngram API data for `sustainable` in the US English 2012 corpus were downloaded. No Pinker plotted values were digitized.\n\n"
        "Known limitation: xkcd's exact future extrapolation formula is not published. Future anchors are taken from the xkcd transcript and stored separately from observed Ngram data.\n\n"
        "## Visual Fidelity\n\n"
        "The recreated plot uses the same log-percent concept, year span, and main future annotations. It is not a hand-drawn comic replica; the purpose is source-data fidelity and comparison clarity.\n\n"
        "## Extension Clarity\n\n"
        "The extended comparison overlays newer US English 2019 Ngram observations through 2019 in blue. These points are visually distinct from the comic extrapolation and show that successor actuals do not follow the comic's humorous projection.\n\n"
        "## Reviewer Challenge\n\n"
        "- Pinker would likely ask whether the image is the same xkcd figure; the PDF crop and original xkcd image are preserved.\n"
        "- A data journalist would ask whether the future line is observed data; the caption and clean data distinguish observed Ngram values from transcript anchors.\n"
        "- A peer reviewer would ask for the exact fit; this remains unavailable from xkcd and is documented as the main limitation.\n"
        "- A skeptical reader would notice the typography mismatch; this is intentional because the reconstruction is a data plot, not a traced comic.\n\n"
        "## Editorial Review Gate\n\n"
        "- Critical issues found: none. Primary PDF reference, source image, source data, reconstruction, extension, and comparisons are present.\n"
        "- Major issues found: the recreated plot is not a hand-drawn xkcd replica; this is explained in caption/provenance and is source-related rather than an unaddressed layout failure.\n"
        "- Minor issues found: typography and annotation placement differ from the comic.\n"
        "- Issues corrected: source roles separated; successor extension colored distinctly; PDF page corrected from page 12 text offset to actual page 13 render.\n"
        "- Issues remaining: exact xkcd fitting formula not recovered.\n"
        "- Disposition: acceptable as an updated-equivalent/source-chain reconstruction, not as a verified exact visual reproduction.\n"
    )
    (BASE / "review_checklist.md").write_text(
        "# Review Checklist: Figure 10-2\n\n"
        "- [x] Supplemental Graphics PDF reference located.\n"
        "- [x] Figure title, range, units, and source line confirmed from PDF.\n"
        "- [x] Original xkcd source page and image recovered.\n"
        "- [x] Google Ngram source data recovered for the observed series.\n"
        "- [x] Pinker plotted values not digitized.\n"
        "- [x] Book-period reconstruction generated from source data and xkcd transcript anchors.\n"
        "- [x] Extended comparison generated with newer Ngram successor actuals where applicable.\n"
        "- [x] Fitting/formula blocker documented honestly.\n"
        "- [x] Registry, metadata, provenance, caption, anomaly review, checksums, and review PDF updated.\n"
        "- [x] Editorial Review Gate applied with updated_equivalent disposition.\n"
    )


def update_registry() -> None:
    csv_path = ROOT / "data/figure_registry.csv"
    rows = list(csv.DictReader(csv_path.open()))
    for row in rows:
        if row["figure_id"] == FIG_ID:
            row.update(
                {
                    "page": "Supplemental PDF page 13",
                    "year_range": "1955-2109",
                    "current_status": "updated_equivalent",
                    "lifecycle_stage": "updated_equivalent_with_google_ngram_source_and_xkcd_anchor_reconstruction",
                    "source_type_guess": "Google Ngram/xkcd source comic",
                    "priority": "completed_monitor",
                    "current_owner": "Codex",
                    "next_action": "Recover exact xkcd fitting method only if a publication audit requires exact hand-drawn projection geometry.",
                    "notes": "Processed 2026-07-04: Supplemental PDF page 13 source line confirmed; xkcd source page/image and Google Ngram source data recovered; no Pinker plotted values digitized.",
                }
            )
    with csv_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    (ROOT / "data/figure_registry.json").write_text(json.dumps(rows, indent=2) + "\n")


def update_figure_metadata_csv() -> None:
    path = ROOT / "data/metadata/figure_metadata.csv"
    rows = list(csv.DictReader(path.open()))
    row = {
        "figure_id": "10-2",
        "chapter": "10",
        "title": "Sustainability, 1955-2109",
        "book_page": "Supplemental PDF page 13",
        "claim_summary": "A humorous xkcd/Google Ngram extrapolation of the word sustainable rises to absurd future frequencies.",
        "book_citation": "Randall Munroe, XKCD, http://xkcd.com/1007/. Credit: Randall Munroe, xkcd.com.",
        "original_dataset": "Google Books Ngram US English 2012 corpus for sustainable; xkcd transcript future anchors.",
        "dataset_url": f"{XKCD_INFO_URL}; {NGRAM_URL}?content=sustainable&year_start=1950&year_end=2008&corpus=en-US-2012&smoothing=3",
        "archive_url": "Not captured",
        "download_date": TODAY,
        "reproduction_status": "updated_equivalent",
        "confidence_score": "0.74",
        "visual_validation": "good_with_documented_fit_difference",
        "notes": "Source comic and Ngram data recovered; exact xkcd extrapolation formula not published, so future anchors are transcript-derived and separately labeled.",
    }
    rows = [r for r in rows if r["figure_id"] != FIG_ID]
    rows.append(row)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        writer.writeheader()
        writer.writerows(rows)


def update_project_state() -> None:
    path = ROOT / "PROJECT_STATE.md"
    text = path.read_text()
    text = text.replace("Project version: `1.11-source-recovery-figure-4-1`", "Project version: `1.12-source-recovery-figure-10-2`")
    old_row = "| 10-1 | Population and population growth, 1750-2015 and projected to 2100 | Updated-equivalent current OWID/UN successor reconstruction | `updated_equivalent` | Medium-high | Current OWID population/growth/projection grapher data reproduce the dual-axis concept, but exact 2016 OWID/HYDE/IIASA source vintage remains unrecovered. |\n"
    new_row = old_row + "| 10-2 | Sustainability, 1955-2109 | Updated-equivalent xkcd/Google Ngram source-chain reconstruction | `updated_equivalent` | Medium | Supplemental PDF page 13 source line confirmed; xkcd source page/image and Google Ngram data recovered. Exact xkcd extrapolation formula is unpublished, so future anchors are transcript-derived and separately labeled. |\n"
    if "| 10-2 | Sustainability, 1955-2109 |" not in text:
        text = text.replace(old_row, new_row)
    text = text.replace(
        "Figures 4-1, 5-1, 5-2, 5-3, 5-4, 6-1, 7-1, 7-2, 8-4, 10-5, 10-6, 10-7, 10-8, and 19-1 have been carried",
        "Figures 4-1, 5-1, 5-2, 5-3, 5-4, 6-1, 7-1, 7-2, 8-4, 10-2, 10-5, 10-6, 10-7, 10-8, and 19-1 have been carried",
    )
    insert = """### Figure 10-2 - Sustainability, 1955-2109

Status: `updated_equivalent`

Canonical visual artifacts:
- Original reference: `figures/10-2/plots/comparisons/pdf_reference_figure_10_2.png`
- Book-period reconstruction: `figures/10-2/plots/book_period/figure_10_2_book_period_reconstruction.png`
- Extended reconstruction: `figures/10-2/plots/extended/figure_10_2_extended_reconstruction.png`
- Book-period comparison: `figures/10-2/plots/comparisons/figure_10_2_book_period_comparison.png`
- Extended comparison: `figures/10-2/plots/comparisons/figure_10_2_extended_comparison.png`
Canonical documentation:
- Caption: `figures/10-2/captions/caption.txt`
- Provenance: `figures/10-2/provenance/provenance.md`
- Anomaly review: `figures/10-2/anomaly_reviews/anomaly_review.md`
- Metadata: `figures/10-2/metadata/metadata.json`
- Review checklist: `figures/10-2/review_checklist.md`

"""
    marker = "### Figure 10-5 - Oil spills, 1970-2016"
    if "### Figure 10-2 - Sustainability, 1955-2109" not in text:
        text = text.replace(marker, insert + marker)
    version_row = "| `1.12-source-recovery-figure-10-2` | 2026-07-04 | Processed Figure 10-2. Supplemental PDF, xkcd source page/image, and Google Ngram data were recovered; no Pinker plotted values were digitized; exact xkcd fit remains unpublished and documented. |\n"
    if version_row not in text:
        text = text.replace("| `1.11-source-recovery-figure-4-1` | 2026-07-04 |", version_row + "| `1.11-source-recovery-figure-4-1` | 2026-07-04 |")
    path.write_text(text)


def rebuild_review_pdf() -> None:
    manifest_path = ROOT / "output/pdf/recreated_figures_review_scroll.manifest.json"
    manifest = json.loads(manifest_path.read_text())
    items = [item for item in manifest["items"] if item["figure_id"] != FIG_ID]
    item_path = "figures/10-2/plots/comparisons/figure_10_2_extended_comparison.png"
    im = Image.open(ROOT / item_path)
    items.append(
        {
            "figure_id": "10-2",
            "title": "Sustainability, 1955-2109",
            "status": "updated_equivalent",
            "path": item_path,
            "selected_image": Path(item_path).name,
            "notes": "xkcd source page/image and Google Ngram source data recovered. Exact xkcd future fitting method is unpublished; future anchors are transcript-derived and separately labeled. No Pinker plotted values were digitized.",
            "image_size": [im.width, im.height],
        }
    )
    def key(item: dict[str, str]) -> tuple[int, int]:
        a, b = item["figure_id"].split("-")
        return int(a), int(b)
    items = sorted(items, key=key)

    pdf_path = ROOT / "output/pdf/recreated_figures_review_scroll.pdf"
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(pdf_path), pagesize=letter)
    w, h = letter
    c.setFont("Helvetica-Bold", 16)
    c.drawString(40, h - 50, "Recreated Figures Review Scroll")
    c.setFont("Helvetica", 10)
    c.drawString(40, h - 70, f"Updated {TODAY}; {len(items)} figure comparison/source-recovery items.")
    y = h - 100
    for item in items:
        line = f"{item['figure_id']}  {item['status']}  {item['title']}"
        c.drawString(45, y, line[:105])
        y -= 14
        if y < 45:
            c.showPage()
            y = h - 45
    c.showPage()

    for item in items:
        c.setFont("Helvetica-Bold", 13)
        c.drawString(36, h - 36, f"{item['figure_id']}: {item['title']} [{item['status']}]")
        img_path = ROOT / item["path"]
        im = Image.open(img_path)
        max_w, max_h = w - 72, h - 170
        scale = min(max_w / im.width, max_h / im.height)
        draw_w, draw_h = im.width * scale, im.height * scale
        x, y = (w - draw_w) / 2, h - 58 - draw_h
        c.drawImage(ImageReader(str(img_path)), x, y, width=draw_w, height=draw_h, preserveAspectRatio=True, mask="auto")
        c.setFont("Helvetica", 8)
        note_y = 72
        for line in wrap(item["notes"], 120)[:4]:
            c.drawString(40, note_y, line)
            note_y -= 10
        c.showPage()
    c.save()

    manifest.update({"output": "output/pdf/recreated_figures_review_scroll.pdf", "count": len(items), "updated": TODAY, "items": items})
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")


def main() -> None:
    ensure_dirs()
    crop_reference()
    download_sources()
    book, anchors, current = clean_data()

    book_plot = BASE / "plots/book_period/figure_10_2_book_period_reconstruction.png"
    ext_plot = BASE / "plots/extended/figure_10_2_extended_reconstruction.png"
    plot_reconstruction(book, anchors, current, book_plot, extended=False)
    plot_reconstruction(book, anchors, current, ext_plot, extended=True)
    ref = BASE / "plots/comparisons/pdf_reference_figure_10_2.png"
    side_by_side(ref, book_plot, BASE / "plots/comparisons/figure_10_2_book_period_comparison.png", "Figure 10-2 Book-Period Comparison")
    side_by_side(ref, ext_plot, BASE / "plots/comparisons/figure_10_2_extended_comparison.png", "Figure 10-2 Extended Comparison")

    write_docs()
    update_registry()
    update_figure_metadata_csv()
    update_project_state()
    write_checksums()
    rebuild_review_pdf()


if __name__ == "__main__":
    main()
