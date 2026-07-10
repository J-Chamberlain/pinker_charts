from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import textwrap
from datetime import date
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
FIG_ID = "9-3"
FIG_SLUG = FIG_ID.replace("-", "_")
BASE = ROOT / "figures" / FIG_ID
TODAY = date.today().isoformat()

SUPPLEMENTAL_PDF = ROOT / "references/enlightenment_now_supplemental_graphics.pdf"
PDF_PAGE = 10
PAGE_IMAGE = BASE / "data/raw/supplemental_pdf_page_10.png"
REFERENCE_CROP = BASE / "plots/comparisons/supplemental_pdf_reference_figure_9_3.png"

TITLE = "Inequality, UK and US, 1688-2013"
SOURCE_LINE = "Milanovic 2016, fig. 2.1, disposable income per capita."
BOOK_PAGE = "Supplemental Graphics PDF page 10"
WORKBOOK_CANDIDATE = "US_and_uk.xls / uk_and_usa.xls"
PIIE_URL = "https://www.piie.com/sites/default/files/documents/milanovic20160509ppt.pdf"
LIS_URL = "https://www.lisdatacenter.org/wp-content/uploads/Milanovic-slides.pdf"


def ensure_dirs() -> None:
    for rel in [
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
        "data/candidates",
        "checksums",
    ]:
        (BASE / rel).mkdir(parents=True, exist_ok=True)


def download(url: str, dest: Path) -> str:
    if dest.exists() and dest.stat().st_size > 0:
        return "already_present"
    req = Request(url, headers={"User-Agent": "Mozilla/5.0 source-recovery-audit"})
    try:
        with urlopen(req, timeout=45) as response:
            dest.write_bytes(response.read())
        return "downloaded"
    except (HTTPError, URLError, TimeoutError) as exc:
        return f"failed: {exc}"


def run(cmd: list[str]) -> str:
    return subprocess.run(cmd, check=True, text=True, capture_output=True).stdout


def render_supplemental_page() -> None:
    # Poppler numbers output files from the requested first page.
    out_prefix = BASE / "data/raw/supplemental_pdf_page"
    generated = BASE / "data/raw/supplemental_pdf_page-10.png"
    if not PAGE_IMAGE.exists():
        run(
            [
                "pdftoppm",
                "-f",
                str(PDF_PAGE),
                "-l",
                str(PDF_PAGE),
                "-png",
                "-r",
                "200",
                str(SUPPLEMENTAL_PDF),
                str(out_prefix),
            ]
        )
        generated.rename(PAGE_IMAGE)


def crop_reference() -> None:
    render_supplemental_page()
    # Coordinates are for the 200 dpi rendering above. The crop includes the
    # Figure 9-3 chart, title, and source note, but avoids adjacent Figure 9-2.
    Image.open(PAGE_IMAGE).convert("RGB").crop((115, 1125, 1115, 1815)).save(REFERENCE_CROP)


def wrap(text: str, width: int = 88) -> str:
    return "\n".join(textwrap.wrap(text, width=width))


def make_status_panel(output: Path, extended: bool) -> None:
    body = (
        "The source workbook used for Milanovic 2016 Figure 2.1 is identified in "
        "Milanovic slide evidence as US_and_uk.xls / uk_and_usa.xls, but the workbook "
        "was not recovered as an inspectable file in live CUNY/Stone Center/LIS paths "
        "or Internet Archive CDX filename probes. The component-source trail is "
        "documented, but it does not expose Pinker's book-period UK/US series as a "
        "single auditable table."
    )
    image = Image.new("RGB", (1512, 936), "white")
    draw = ImageDraw.Draw(image)
    title_font, heading_font, body_font, small_font = fonts()
    y = 58
    draw.text((55, y), f"Figure {FIG_ID}: {TITLE}", fill="black", font=title_font)
    y += 82
    draw.text((55, y), "Source recovery blocked - no reconstruction plotted", fill="black", font=heading_font)
    y += 82
    y = draw_multiline(draw, (55, y), wrap(body, 78), body_font, line_spacing=10)
    y += 40
    y = draw_multiline(
        draw,
        (55, y),
        wrap("No digitized values from Pinker's chart or from slide images were used. Data fidelity cannot be tested until the workbook or an equivalent table is recovered.", 82),
        body_font,
        line_spacing=10,
    )
    y += 55
    draw.text((55, y), f"Book source line: {SOURCE_LINE}", fill="black", font=small_font)
    y += 50
    extension = (
        "not added; no comparable successor series was established"
        if extended
        else "not applicable to blocked book-period reconstruction"
    )
    draw.text((55, y), f"Extension status: {extension}", fill="black", font=small_font)
    image.save(output)


def fonts() -> tuple[ImageFont.ImageFont, ImageFont.ImageFont, ImageFont.ImageFont, ImageFont.ImageFont]:
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    font_path = next((p for p in candidates if Path(p).exists()), None)
    if font_path:
        return (
            ImageFont.truetype(font_path, 38),
            ImageFont.truetype(font_path, 31),
            ImageFont.truetype(font_path, 25),
            ImageFont.truetype(font_path, 22),
        )
    default = ImageFont.load_default()
    return default, default, default, default


def draw_multiline(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, font: ImageFont.ImageFont, line_spacing: int) -> int:
    x, y = xy
    for line in text.splitlines():
        draw.text((x, y), line, fill="black", font=font)
        bbox = draw.textbbox((x, y), line or " ", font=font)
        y += bbox[3] - bbox[1] + line_spacing
    return y


def trim_image(path: Path) -> Image.Image:
    image = Image.open(path).convert("RGB")
    diff = ImageChops.difference(image, Image.new("RGB", image.size, "white"))
    bbox = diff.getbbox()
    return image.crop(bbox) if bbox else image


def save_side_by_side(reference: Path, recreated: Path, output: Path, title: str) -> None:
    ref = trim_image(reference)
    rec = trim_image(recreated)
    panel_w, panel_h = 980, 700
    margin, gap, title_h, label_h = 44, 44, 58, 48
    canvas = Image.new("RGB", (margin * 2 + panel_w * 2 + gap, title_h + label_h + panel_h + margin), "white")
    draw = ImageDraw.Draw(canvas)
    title_font, label_font, _, _ = fonts()

    def paste_fit(im: Image.Image, x: int, y: int) -> None:
        fitted = ImageOps.contain(im, (panel_w, panel_h), method=Image.Resampling.LANCZOS)
        canvas.paste(fitted, (x + (panel_w - fitted.width) // 2, y + (panel_h - fitted.height) // 2))
        draw.rectangle([x, y, x + panel_w, y + panel_h], outline=(225, 225, 225), width=1)

    draw.text((canvas.width // 2, 18), title, fill="black", anchor="ma", font=title_font)
    left_x = margin
    right_x = margin + panel_w + gap
    draw.text((left_x + panel_w // 2, title_h + 7), "Supplemental PDF reference", fill="black", anchor="ma", font=label_font)
    draw.text((right_x + panel_w // 2, title_h + 7), "Source-recovery status", fill="black", anchor="ma", font=label_font)
    paste_fit(ref, left_x, title_h + label_h)
    paste_fit(rec, right_x, title_h + label_h)
    canvas.save(output)


def write_candidate_audit() -> None:
    rows = [
        {
            "candidate": "Milanovic 2016 Figure 2.1 workbook",
            "url_or_identifier": "US_and_uk.xls / uk_and_usa.xls",
            "evidence": "PIIE 2016 slide deck labels the UK and US Kuznets frames with US_and_uk.xls; LIS 2014 slide deck labels the combined long-run chart with uk_and_usa.xls.",
            "result": "identified_by_name_not_recovered",
            "accepted_for_reconstruction": "no",
        },
        {
            "candidate": "PIIE May 9 2016 slide deck",
            "url_or_identifier": PIIE_URL,
            "evidence": "Downloaded PDF text exposes the workbook label and component source notes for UK and US.",
            "result": "downloaded_as_provenance_evidence",
            "accepted_for_reconstruction": "no",
        },
        {
            "candidate": "LIS Milanovic slides",
            "url_or_identifier": LIS_URL,
            "evidence": "Downloaded PDF text shows the combined long-run England/UK and USA chart with 'From uk_and_usa.xls'.",
            "result": "downloaded_as_provenance_evidence",
            "accepted_for_reconstruction": "no",
        },
        {
            "candidate": "Live CUNY/Stone Center/LIS guessed workbook paths",
            "url_or_identifier": "stonecenter.gc.cuny.edu/files/uk_and_usa.xls; gc.cuny.edu/.../brankoData/...; lisdatacenter.org/wp-content/uploads/uk_and_usa.xls",
            "evidence": "HEAD/curl probes returned 404 or redirect-to-404 for guessed live paths.",
            "result": "not_recovered",
            "accepted_for_reconstruction": "no",
        },
        {
            "candidate": "Internet Archive CDX filename probes",
            "url_or_identifier": "*uk_and_usa.xls*; *us_and_uk.xls*; *milanovic*/*uk*usa*.xls*; *brankomilanovic.com*.xls*",
            "evidence": "CDX probes returned empty JSON results or transient 503/504 for broad CUNY media searches; no 200 capture of the workbook was found.",
            "result": "not_recovered",
            "accepted_for_reconstruction": "no",
        },
    ]
    path = BASE / "data/candidates/source_recovery_audit.csv"
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_docs() -> None:
    raw_piie = BASE / "data/raw/milanovic_piie_20160509ppt.pdf"
    raw_lis = BASE / "data/raw/milanovic_lis_slides.pdf"
    download(PIIE_URL, raw_piie)
    download(LIS_URL, raw_lis)
    write_candidate_audit()

    source_log = f"""# Figure 9-3 Source Log

Date: {TODAY}

## Supplemental PDF Evidence

- Inspected `references/enlightenment_now_supplemental_graphics.pdf`, page 10.
- Title: `{TITLE}`.
- Source note: `{SOURCE_LINE}`
- Visible series: `England/UK` and `US`, plotted as Gini index from 1688 through 2013.
- Surrounding text says both countries followed a Kuznets-arc pattern: inequality rose during industrialization, fell in the late nineteenth and mid-twentieth centuries, then rose again after about 1980.

## Bibliography Resolution

- The book source line resolves to Branko Milanovic, *Global Inequality: A New Approach for the Age of Globalization* (Harvard University Press, 2016), Figure 2.1.
- The repository bibliography tables do not currently contain a canonical `Milanovic 2016` record, so this per-figure record treats the entry as resolved from the figure source line and corroborating Milanovic slide evidence rather than from an existing central bibliography row.

## Source Recovery Result

- The likely original workbook is identified by name as `{WORKBOOK_CANDIDATE}`.
- PIIE slide evidence (`{PIIE_URL}`) labels the UK and US Kuznets-frame charts with `US_and_uk.xls` and exposes the component source notes.
- LIS slide evidence (`{LIS_URL}`) labels the combined long-run England/UK and USA chart with `From uk_and_usa.xls`.
- The workbook was not recovered as an inspectable data file from live guessed CUNY/Stone Center/LIS paths or Internet Archive CDX filename probes.
- No plotted values from Pinker's chart, the Supplemental PDF, or Milanovic slide images were digitized or used as data.

## Component Source Trail From Milanovic Slide Evidence

- UK/England early values: social tables for 1688, 1759, 1801, and 1867 as reported in Milanovic, Lindert, and Williamson; 1880 and 1913 from Lindert and Williamson (1983), Table 2.
- UK/England modern values: 1961 to 2010 official UK disposable-income-per-capita data calculated by Jonathan Cribb, Institute for Fiscal Studies.
- US early values: 1774 and 1860 from social tables created by Lindert and Williamson (2013).
- US interwar values: 1929 from Radner and Hinricks (1974); 1931 and 1933 from Smolensky and Plotnick (1992).
- US 1935-1950 and later values: Goldsmith et al. (1954), US Census Bureau income reports, with gross income data adjusted to disposable income.
- GDP-per-capita context in the slide-deck Kuznets-frame charts comes from the Maddison Project 2014 version; Pinker Figure 9-3 itself plots only Gini over time.

## Blocker

The original workbook/table behind Milanovic 2016 Figure 2.1 has been identified by filename but not recovered. The component-source trail is too stitched and partly personal-communication/adjustment based to recreate the plotted series without silently substituting or inventing values. A verified reconstruction requires the workbook or an equivalent author/publisher table.
"""
    (BASE / "source_logs/source_log.md").write_text(source_log)

    provenance = f"""# Figure 9-3 Provenance

## Evidence

- Title: {TITLE}
- Book page: {BOOK_PAGE}
- Source line: {SOURCE_LINE}
- Claim summary: Long-run UK and US Gini series rose, fell in the mid-twentieth century, and rose again in recent decades.

## Provenance Trail

Supplemental Graphics PDF page 10 -> Milanovic 2016 Figure 2.1 -> Milanovic slide-deck evidence naming `{WORKBOOK_CANDIDATE}` -> source-recovery audit in `figures/9-3/data/candidates/source_recovery_audit.csv` -> source-recovery-blocked status panels.

## Source Recovery Result

The likely original data workbook is identified but not recovered. The recovered evidence names the workbook and documents the component-source families, but no inspectable source table exposes the UK/England and US disposable-income-per-capita Gini series used in Pinker's 1688-2013 chart.

## Reconstruction

No reconstruction data file was accepted. The generated comparison images are source-recovery/status panels only, not reconstructed charts. This is intentional: the project rule forbids using digitized values from the book chart or slide images as reconstruction data.

## Extension

No extension is plotted. Current World Bank, ONS, LIS/SWIID, or WID-style Gini series are not a verifiably comparable continuation of Milanovic's stitched disposable-income-per-capita workbook series across the full UK/US book period.

## Next Action

Recover `US_and_uk.xls` / `uk_and_usa.xls` from Milanovic, a publisher supplement, archived CUNY/LIS storage, or an equivalent author-supplied table.
"""
    (BASE / "provenance/provenance.md").write_text(provenance)

    search_iterations = f"""# Figure 9-3 Search Iterations

Date: {TODAY}

- Inspected the Supplemental Graphics PDF page 10 figure, source note, and surrounding explanatory text.
- Resolved the figure source to Milanovic 2016, Figure 2.1, and downloaded the PIIE May 9, 2016 slide deck.
- Extracted slide text showing `US_and_uk.xls` and component source notes for UK/England and US.
- Downloaded the LIS Milanovic slide deck and extracted the combined long-run chart label `From uk_and_usa.xls`.
- Probed live guessed workbook paths under Stone Center/CUNY/LIS upload locations; no workbook was recovered.
- Probed Internet Archive CDX for `*uk_and_usa.xls*`, `*us_and_uk.xls*`, `*milanovic*/*uk*usa*.xls*`, and `*brankomilanovic.com*.xls*`; no 200 capture of the workbook was found.
- Evaluated current World Bank/ONS/LIS/SWIID/WID-style successor families conceptually and rejected them for extension because they do not verify comparability with the stitched Milanovic workbook series.
"""
    (BASE / "search_iterations/search_iterations.md").write_text(search_iterations)

    discrepancy = f"""# Figure 9-3 Discrepancy Log

- Critical source blocker: the likely workbook (`{WORKBOOK_CANDIDATE}`) is identified by name but was not recovered as an inspectable file.
- No recreated book-period line chart is produced, so axes, scale, year range, and series fidelity cannot be verified against source data.
- Comparison images show the Supplemental PDF reference beside a source-recovery status panel only.
- No chart-image digitization was used. This avoids silently substituting approximate visual readings for the original data.
- No extension segment is shown because no genuinely comparable successor series was established.
"""
    (BASE / "discrepancy_logs/discrepancy_log.md").write_text(discrepancy)

    anomaly = f"""# Figure 9-3 Editorial Review

## Decision

Status remains `manual_review_needed` / source recovery blocked. The run improved provenance by identifying the likely source workbook names and component sources, but it did not recover the data table needed for reconstruction.

## Reviewer Challenge

- Could this be reconstructed from the Supplemental PDF or Milanovic slide images? No. That would be chart digitization rather than source recovery.
- Could modern Gini datasets extend the figure? Not as a verified extension. They use different institutions, income definitions, equivalization, survey coverage, and revision vintages.
- Is the source completely unknown? No. The source family is now better specified: Milanovic 2016 Figure 2.1, likely `US_and_uk.xls` / `uk_and_usa.xls`, with component-source notes captured from Milanovic's own slides.

## Remaining Risk

The exact workbook may exist in private author files or an uncrawled publisher/academic directory. Recovery should continue there before any reconstruction is attempted.
"""
    (BASE / "anomaly_reviews/anomaly_review.md").write_text(anomaly)

    caption = (
        f"Figure 9-3: {TITLE}. Source line inspected from the Supplemental Graphics PDF: "
        f"{SOURCE_LINE} Milanovic slide evidence identifies the likely underlying workbook as "
        "`US_and_uk.xls` / `uk_and_usa.xls`, but this run did not recover it as an inspectable "
        "data file. No recreated data series is plotted, no chart values were digitized, and no "
        "successor extension is added."
    )
    (BASE / "captions/caption.txt").write_text(caption + "\n")

    metadata = {
        "figure_id": FIG_ID,
        "title": TITLE,
        "chapter": "9",
        "book_page": BOOK_PAGE,
        "year_range": "1688-2013",
        "claim_summary": "Long-run UK and US Gini series rose, fell in the mid-twentieth century, and rose again in recent decades.",
        "book_citation": SOURCE_LINE,
        "bibliography_resolution": "Branko Milanovic, Global Inequality: A New Approach for the Age of Globalization, Harvard University Press, 2016, Figure 2.1.",
        "original_dataset": "Likely workbook identified as US_and_uk.xls / uk_and_usa.xls, but not recovered as an inspectable data file.",
        "dataset_url": "",
        "archive_url": "",
        "download_date": TODAY,
        "reproduction_status": "manual_review_needed",
        "confidence_score": 0.42,
        "visual_validation": "blocked_source_workbook_not_recovered",
        "notes": "Source recovery improved but reconstruction remains blocked. Component-source notes were captured from Milanovic slide evidence; no values were digitized or substituted.",
        "canonical_artifacts": {
            "supplemental_pdf_reference": "figures/9-3/plots/comparisons/supplemental_pdf_reference_figure_9_3.png",
            "book_period_comparison": "figures/9-3/plots/comparisons/figure_9_3_book_period_comparison.png",
            "extended_comparison": "figures/9-3/plots/comparisons/figure_9_3_extended_comparison.png",
            "book_period_status_panel": "figures/9-3/plots/book_period/figure_9_3_book_period_reconstruction.png",
            "extended_status_panel": "figures/9-3/plots/extended/figure_9_3_extended_reconstruction.png",
            "source_recovery_audit": "figures/9-3/data/candidates/source_recovery_audit.csv",
        },
    }
    (BASE / "metadata/metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")

    checklist = f"""# Figure Acceptance Checklist

## Figure

- Figure ID: {FIG_ID}
- Title: {TITLE}
- Reviewer: Codex
- Review date: {TODAY}
- Current status: manual_review_needed

## Phase 1 - Evidence Review

- [x] Supplemental Graphics PDF figure inspected.
- [x] Title extracted.
- [x] Caption/source note extracted.
- [x] Surrounding discussion reviewed at the figure page level.
- [x] Bibliography/source mapping resolved to Milanovic 2016 Figure 2.1.

## Phase 2 - Source Review

- [x] Source publication family located.
- [x] Likely source workbook filename identified.
- [x] Dataset provenance trail documented.
- [x] Archive/search notes documented.
- [x] Successor datasets evaluated at source-family level.
- [x] Substitution or source blocker explained.

## Phase 3 - Reconstruction Review

- [ ] Reconstruction uses legitimate data.
- [x] No digitized figure values used as reconstruction data.
- [x] Transformation/status code is reproducible.
- [x] Book-period status comparison generated.
- [x] Remaining book-period discrepancies explained.

## Phase 4 - Extension Review

- [x] Later data families considered.
- [x] Extension absence explained.
- [N/A] Extended data comparison generated; status comparison only.

## Phase 5 - Reviewer Challenge

- [x] Reviewer questions answered in anomaly review.

## Final Gate - Editorial Review

- [x] Comparison image opened and visually scanned.
- [x] Ten-second-obvious issues corrected or explicitly explained.
- [x] No unexplained Critical/Major issues remain; source blocker is explicit.

## Repository Updates

- [x] Caption written.
- [x] Anomaly review written.
- [x] Provenance/source/discrepancy/search logs updated.
- [x] Metadata updated.
- [x] Registry left untouched for orchestrator review.

## Final Decision

- [ ] Accepted as `updated_equivalent`.
- [x] Classified as `manual_review_needed`.
"""
    (BASE / "review_checklist.md").write_text(checklist)

    lineage_csv = BASE / "lineage/figure_lineage.csv"
    with lineage_csv.open("w", newline="") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow(["figure_id", "artifact_type", "description", "status"])
        writer.writerow([FIG_ID, "book_reference", "Supplemental Graphics PDF page 10 crop", "reference"])
        writer.writerow([FIG_ID, "source_evidence", "Milanovic slide evidence naming source workbook", "source_family_identified"])
        writer.writerow([FIG_ID, "source_recovery_audit", "Live and archive workbook probes", "workbook_not_recovered"])
        writer.writerow([FIG_ID, "status_panel", "No accepted reconstruction data", "manual_review_needed"])
    (BASE / "lineage/figure_lineage.json").write_text(
        json.dumps(
            [
                {"figure_id": FIG_ID, "artifact_type": "book_reference", "description": "Supplemental Graphics PDF page 10 crop", "status": "reference"},
                {"figure_id": FIG_ID, "artifact_type": "source_evidence", "description": "Milanovic slide evidence naming source workbook", "status": "source_family_identified"},
                {"figure_id": FIG_ID, "artifact_type": "source_recovery_audit", "description": "Live and archive workbook probes", "status": "workbook_not_recovered"},
                {"figure_id": FIG_ID, "artifact_type": "status_panel", "description": "No accepted reconstruction data", "status": "manual_review_needed"},
            ],
            indent=2,
        )
        + "\n"
    )


def write_checksums() -> None:
    files = sorted(
        p
        for p in BASE.rglob("*")
        if p.is_file() and "checksums" not in p.parts and p.suffix.lower() not in {".pyc"}
    )
    lines = []
    for path in files:
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        lines.append(f"{digest}  {path.relative_to(ROOT)}")
    (BASE / "checksums/sha256sums.txt").write_text("\n".join(lines) + "\n")


def main() -> None:
    ensure_dirs()
    crop_reference()
    book_status = BASE / f"plots/book_period/figure_{FIG_SLUG}_book_period_reconstruction.png"
    extended_status = BASE / f"plots/extended/figure_{FIG_SLUG}_extended_reconstruction.png"
    make_status_panel(book_status, extended=False)
    make_status_panel(extended_status, extended=True)
    save_side_by_side(
        REFERENCE_CROP,
        book_status,
        BASE / f"plots/comparisons/figure_{FIG_SLUG}_book_period_comparison.png",
        f"Figure {FIG_ID}: Book-period source recovery status",
    )
    save_side_by_side(
        REFERENCE_CROP,
        extended_status,
        BASE / f"plots/comparisons/figure_{FIG_SLUG}_extended_comparison.png",
        f"Figure {FIG_ID}: Extension status",
    )
    write_docs()
    write_checksums()


if __name__ == "__main__":
    main()
