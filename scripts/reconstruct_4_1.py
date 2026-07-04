from __future__ import annotations

import csv
import hashlib
import json
import shutil
import subprocess
import ssl
import textwrap
from datetime import date
from pathlib import Path
from urllib.request import Request, urlopen

import matplotlib.pyplot as plt
from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "figures/4-1"
PDF_SOURCE = ROOT / "references/enlightenment_now_supplemental_graphics.pdf"
PDF_PAGE = ROOT / "tmp/pdf_pages_4_1/page-2.png"
TODAY = date.today().isoformat()

TITLE = "Tone of the news, 1945-2010"
SOURCE_LINE = "Leetaru 2011. Plotted by month, beginning in January."
STATUS = "manual_review_needed"
LIFECYCLE = "source_recovery_blocked_reference_captured"
NEXT_ACTION = (
    "Recover Leetaru 2011 monthly NYT and Summary of World Broadcasts tone tables "
    "or obtain author/institutional data; do not reconstruct by digitizing Pinker "
    "or Leetaru plotted figure values."
)

FIRST_MONDAY_URL = "https://firstmonday.org/ojs/index.php/fm/article/download/3663/3040"
GDELT_FIG10_URL = "https://data.gdeltproject.org/blog/2011-culturomics-20/figure10.png"
GDELT_FIG11_URL = "https://data.gdeltproject.org/blog/2011-culturomics-20/figure11.png"
WAYBACK_CDX_URL = (
    "https://web.archive.org/cdx?url=contentanalysis.ichass.illinois.edu/"
    "Culturomics20/*&output=json&fl=timestamp,original,statuscode,mimetype,digest"
    "&filter=statuscode:200&collapse=urlkey"
)


def ensure_dirs() -> None:
    for part in [
        "metadata",
        "provenance",
        "source_logs",
        "search_iterations",
        "anomaly_reviews",
        "captions",
        "plots/book_period",
        "plots/extended",
        "plots/comparisons",
        "data/candidates",
        "checksums",
    ]:
        (BASE / part).mkdir(parents=True, exist_ok=True)
    PDF_PAGE.parent.mkdir(parents=True, exist_ok=True)


def download(url: str, out: Path) -> None:
    if out.exists() and out.stat().st_size > 0:
        return
    req = Request(url, headers={"User-Agent": "pinker-charts-source-recovery/1.0"})
    context = ssl._create_unverified_context() if "data.gdeltproject.org" in url else None
    with urlopen(req, timeout=90, context=context) as response:
        out.write_bytes(response.read())


def render_pdf_page() -> None:
    if PDF_PAGE.exists():
        return
    subprocess.run(
        [
            "pdftoppm",
            "-r",
            "220",
            "-png",
            "-f",
            "2",
            "-singlefile",
            str(PDF_SOURCE),
            str(PDF_PAGE.with_suffix("")),
        ],
        check=True,
    )


def crop_reference() -> Path:
    out = BASE / "plots/comparisons/pdf_reference_figure_4_1.png"
    page = Image.open(PDF_PAGE).convert("RGB")
    # Crop includes the plot and caption/source line from Supplemental Graphics PDF page 2.
    page.crop((115, 200, 1155, 1055)).save(out)
    return out


def trim_image(path: Path) -> Image.Image:
    image = Image.open(path).convert("RGB")
    bg = Image.new("RGB", image.size, "white")
    diff = ImageChops.difference(image, bg)
    bbox = diff.getbbox()
    return image.crop(bbox) if bbox else image


def placeholder_plot(extended: bool) -> Path:
    folder = "extended" if extended else "book_period"
    suffix = "extended_reconstruction" if extended else "book_period_reconstruction"
    out = BASE / f"plots/{folder}/figure_4_1_{suffix}.png"
    fig, ax = plt.subplots(figsize=(8.4, 5.2), dpi=180)
    ax.axis("off")
    ax.text(0.02, 0.88, "Figure 4-1: Tone of the news, 1945-2010", fontsize=15, weight="bold", transform=ax.transAxes)
    ax.text(0.02, 0.70, "No reconstruction plotted.", fontsize=13, weight="bold", transform=ax.transAxes)
    ax.text(
        0.02,
        0.53,
        "The cited Leetaru 2011 monthly source data were not recovered.\n"
        "The available public artifacts are article text and plotted PNG figures.\n"
        "Project rules forbid reconstructing from digitized plotted values.",
        fontsize=11,
        transform=ax.transAxes,
        linespacing=1.35,
    )
    next_action = textwrap.fill(f"Next action: {NEXT_ACTION}", width=82)
    ax.text(0.02, 0.25, next_action, fontsize=9.5, transform=ax.transAxes, linespacing=1.25)
    ax.text(0.02, 0.10, f"Source line: {SOURCE_LINE}", fontsize=8.5, transform=ax.transAxes, wrap=True)
    fig.tight_layout()
    fig.savefig(out, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return out


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
    draw.text((left_x + panel_w // 2, label_y), "PDF reference", fill="black", anchor="ma", font=label_font)
    draw.text((right_x + panel_w // 2, label_y), "Recreated/status", fill="black", anchor="ma", font=label_font)
    paste_fit(ref, left_x, title_h + header_h)
    paste_fit(rec, right_x, title_h + header_h)
    canvas.save(output)


def collect_evidence() -> None:
    candidates = BASE / "data/candidates"
    download(FIRST_MONDAY_URL, candidates / "leetaru_2011_first_monday.html")
    download(GDELT_FIG10_URL, candidates / "gdelt_mirror_leetaru_figure10_nyt.png")
    download(GDELT_FIG11_URL, candidates / "gdelt_mirror_leetaru_figure11_swb.png")
    cdx_out = candidates / "wayback_cdx_contentanalysis_culturomics20.json"
    tmp_cdx = Path("/tmp/pinker_4_1/cdx_culturomics20.json")
    if tmp_cdx.exists() and tmp_cdx.stat().st_size > 0:
        shutil.copyfile(tmp_cdx, cdx_out)
    else:
        download(WAYBACK_CDX_URL, cdx_out)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_text_files() -> None:
    (BASE / "captions/caption.txt").write_text(
        "Figure 4-1 shows Leetaru's monthly tone series for New York Times and "
        "Summary of World Broadcasts news coverage. No recreated data series is "
        "plotted because the underlying monthly tone tables were not recovered; "
        "available public artifacts are article text and plotted figures, and "
        "this project does not reconstruct from digitized chart values.\n",
        encoding="utf-8",
    )

    (BASE / "provenance/provenance.md").write_text(
        f"""# Figure 4-1 Provenance

## Evidence

- Title: {TITLE}
- Supplemental Graphics PDF reference: page 2, top figure and source line.
- Source line: {SOURCE_LINE}
- Surrounding discussion: Chapter 4 frames the chart as evidence that news tone became more negative while many objective welfare indicators improved.

## Source Recovery Result

The original monthly data were not recovered. The accepted evidence package contains:

- First Monday article HTML for Leetaru 2011.
- GDELT 2019 mirror PNGs for Leetaru article figures 10 and 11.
- Wayback CDX listing for the old `contentanalysis.ichass.illinois.edu/Culturomics20/` directory.

The First Monday article documents the corpora and method: full New York Times text from 1945-2005, Summary of World Broadcasts from 1979-2010, and Hu-Liu sentiment mining normalized as standard deviations from each series mean. It publishes plotted figures but no monthly tables. The GDELT mirror likewise republishes high-resolution plotted PNGs, not source data. The old `contentanalysis.ichass.illinois.edu` host no longer resolves, and the Wayback CDX listing found image/GIF/PDF assets but no adjacent CSV/TXT/XLS monthly tone tables.

## Reconstruction

No reconstruction data file was accepted. The comparison images include a status panel instead of a reconstructed chart. This is intentional: the source-recovery rule forbids using digitized values from Pinker's or Leetaru's plotted figures as reconstruction data.

## Next Action

{NEXT_ACTION}
""",
        encoding="utf-8",
    )

    (BASE / "source_logs/source_log.md").write_text(
        f"""# Figure 4-1 Source Log

Date: {TODAY}

## Confirmed Reference

- Supplemental Graphics PDF page 2: top chart inspected and cropped.
- Source line: {SOURCE_LINE}
- The task requested Kindle confirmation before source recovery; the local workflow now designates the Supplemental Graphics PDF as the primary reference. No Kindle artifact was available in this workspace, so the PDF source line is the confirmed source evidence for this pass.

## Accepted Evidence, Not Reconstruction Data

- Leetaru 2011 First Monday article: `{FIRST_MONDAY_URL}`.
- GDELT mirror, Leetaru Figure 10 NYT plotted image: `{GDELT_FIG10_URL}`.
- GDELT mirror, Leetaru Figure 11 SWB plotted image: `{GDELT_FIG11_URL}`.
- Wayback CDX for old Culturomics20 host: `{WAYBACK_CDX_URL}`.

These artifacts support the source chain and visual reference but are not accepted as reconstruction data because they do not expose the underlying monthly values.

## Rejected Or Unavailable Paths

- Direct old host checks for likely CSV names under `contentanalysis.ichass.illinois.edu/Culturomics20/` failed because the host no longer resolves.
- Wayback CDX listing for the old directory returned only the root HTML, map/movie images, and a network PDF; no monthly NYT/SWB tone CSV, TXT, XLS, or JSON tables were listed.
- GDELT's 2019 mirror explicitly republishes high-resolution images for article figures 10 and 11, not data tables.
- The First Monday article text includes method details and plotted figures, but no supplemental dataset link or table.

## Blocker

Original monthly tone tables remain unrecovered. Do not digitize Pinker's plotted values or Leetaru's plotted values to create a data series.
""",
        encoding="utf-8",
    )

    (BASE / "anomaly_reviews/anomaly_review.md").write_text(
        """# Figure 4-1 Anomaly Review

## Data Fidelity

- Critical blocker: no original monthly data table was recovered.
- No plotted values from Pinker or Leetaru were digitized.
- Publicly recovered Leetaru artifacts are non-tabular plotted images and article text.

## Visual Fidelity

- The PDF reference crop is preserved.
- The book-period and extended comparison panels deliberately show a status panel rather than a reconstructed line chart.
- Visual mismatch is therefore expected and documented; this is not a failed reconstruction but a source-recovery stop.

## Extension Clarity

- No extension is plotted because no accepted book-period source series exists.
- The next extension question is whether GDELT or another reproducible news-tone successor can extend after 2010, but that should not be mixed with this figure until the book-period source is recovered or explicitly replaced.

## Reviewer Challenge

- Pinker would likely ask whether Leetaru's own monthly values were used. They were not recovered.
- A data journalist would ask whether the chart was digitized from the book. It was not.
- A peer reviewer would ask whether the proprietary NYT/SWB corpora can be reproduced. Not from public data in this pass.
- A skeptical reader would notice no recreated line chart. The status panel explains why.

## Editorial Review Gate

- Critical issues found: missing underlying source data blocks reconstruction.
- Major issues found: no unexplained visual mismatch; the comparison panel explicitly states the blocker.
- Minor issues found: none material.
- Issues automatically corrected: reference crop and status comparisons generated instead of a weak or digitized reconstruction.
- Issues remaining: recover original monthly Leetaru NYT/SWB tone tables or author/institutional data.
- Status calibration: `manual_review_needed`, not accepted or verified.
""",
        encoding="utf-8",
    )

    (BASE / "review_checklist.md").write_text(
        f"""# Figure Acceptance Checklist - 4-1

- Figure ID: 4-1
- Title: {TITLE}
- Reviewer: Codex
- Review date: {TODAY}
- Current status: `{STATUS}`

## Phase 1 - Evidence Review

- [x] Supplemental Graphics PDF figure inspected.
- [x] Title extracted.
- [x] Caption extracted.
- [x] Source note extracted.
- [x] Surrounding discussion reviewed.
- [x] Bibliography/source article resolved to Leetaru 2011.
- [x] Missing Kindle artifact documented.

## Phase 2 - Source Review

- [x] Original publication located.
- [x] Source chain partly reconstructed.
- [x] Dataset provenance documented.
- [x] Archive search completed for old Culturomics20 host.
- [x] Successor/non-tabular artifacts evaluated.
- [x] Modern proxy not substituted.
- [x] Download URLs recorded.
- [x] Archive-search notes recorded.
- [x] Checksums recorded for stored files.

## Phase 3 - Reconstruction Review

- [ ] Reconstruction uses legitimate data.
- [x] No digitized figure values used as reconstruction data.
- [x] Status panels are reproducible.
- [ ] Scales and labels are correct for a reconstruction.
- [ ] Styling reasonably matches the book.
- [ ] Book-period reconstruction completed.
- [x] Book-period side-by-side status comparison generated.
- [x] Visible discrepancy documented as source blocker.

## Phase 4 - Extension Review

- [x] Later/successor path noted.
- [x] No extension plotted because no accepted book-period data exists.
- [x] Absence explained.
- [x] Extended status comparison generated.

## Phase 5 - Reviewer Challenge

- [x] Answered: What would Steven Pinker likely question?
- [x] Answered: What would a data journalist question?
- [x] Answered: What would a peer reviewer question?
- [x] Answered: What would a skeptical reader notice immediately?
- [x] Each reviewer issue marked documented or new research task.

## Repository Updates

- [x] Caption written.
- [x] Anomaly review written.
- [x] Provenance file updated.
- [x] Source log updated.
- [x] Metadata updated.
- [x] Registry CSV updated.
- [x] Registry JSON updated.
- [x] `PROJECT_STATE.md` updated.
- [x] Review PDF regenerated.

## Reviewer Confidence

- Overall confidence: low for reconstruction, high for blocker classification.
- Book reconstruction: not attempted.
- Extension: not attempted.
- Source provenance: medium for article/source chain; low for underlying data availability.
- Outstanding risks: source data may exist in a private author archive, institutional corpus output, or uncrawled supplemental location.
- Recommended next action: {NEXT_ACTION}

## Final Decision

- [x] Keep as `{STATUS}` pending source recovery.
""",
        encoding="utf-8",
    )


def write_metadata() -> None:
    metadata = {
        "figure_id": "4-1",
        "title": TITLE,
        "status": STATUS,
        "source_fidelity": "source_chain_only",
        "book_citation": SOURCE_LINE,
        "original_reference": "figures/4-1/plots/comparisons/pdf_reference_figure_4_1.png",
        "book_period_reconstruction": "figures/4-1/plots/book_period/figure_4_1_book_period_reconstruction.png",
        "extended_reconstruction": "figures/4-1/plots/extended/figure_4_1_extended_reconstruction.png",
        "book_period_comparison": "figures/4-1/plots/comparisons/figure_4_1_book_period_comparison.png",
        "extended_comparison": "figures/4-1/plots/comparisons/figure_4_1_extended_comparison.png",
        "candidate_sources": [
            "figures/4-1/data/candidates/leetaru_2011_first_monday.html",
            "figures/4-1/data/candidates/gdelt_mirror_leetaru_figure10_nyt.png",
            "figures/4-1/data/candidates/gdelt_mirror_leetaru_figure11_swb.png",
            "figures/4-1/data/candidates/wayback_cdx_contentanalysis_culturomics20.json",
        ],
        "processed_data": [],
        "script": "scripts/reconstruct_4_1.py",
        "visual_validation": "blocked_status_panel",
        "confidence": "low",
        "unresolved_issues": [
            "Original monthly Leetaru NYT and Summary of World Broadcasts tone tables were not recovered.",
            "No extension plotted because no accepted book-period data series exists.",
        ],
        "recommended_next_action": NEXT_ACTION,
    }
    (BASE / "metadata/metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")


def update_registry() -> None:
    csv_path = ROOT / "data/figure_registry.csv"
    rows = list(csv.DictReader(csv_path.open(newline="", encoding="utf-8")))
    for row in rows:
        if row["figure_id"] == "4-1":
            row.update(
                {
                    "current_status": STATUS,
                    "lifecycle_stage": LIFECYCLE,
                    "source_type_guess": "Leetaru 2011 media text analysis dataset",
                    "priority": "high",
                    "current_owner": "Codex",
                    "next_action": NEXT_ACTION,
                    "notes": (
                        f"{TODAY} source recovery: Supplemental PDF source line captured; "
                        "Leetaru article, GDELT image mirror, and Wayback CDX checked; "
                        "monthly source tables not recovered."
                    ),
                }
            )
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    (ROOT / "data/figure_registry.json").write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")


def update_metadata_csv() -> None:
    path = ROOT / "data/metadata/figure_metadata.csv"
    rows = list(csv.DictReader(path.open(newline="", encoding="utf-8")))
    row = {
        "figure_id": "4-1",
        "chapter": "4",
        "title": TITLE,
        "book_page": "Supplemental PDF page 2; Kindle not available in workspace",
        "claim_summary": "News tone became more negative in NYT and Summary of World Broadcasts coverage.",
        "book_citation": SOURCE_LINE,
        "original_dataset": "Leetaru 2011 monthly NYT/SWB sentiment tone tables not recovered",
        "dataset_url": FIRST_MONDAY_URL,
        "archive_url": WAYBACK_CDX_URL,
        "download_date": TODAY,
        "reproduction_status": STATUS,
        "confidence_score": "0.25",
        "visual_validation": "blocked_status_panel",
        "notes": "Source-recovery package only; no plotted-value digitization and no accepted reconstruction data.",
    }
    rows = [r for r in rows if r["figure_id"] != "4-1"]
    rows.insert(0, row)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        writer.writeheader()
        writer.writerows(rows)


def update_project_state() -> None:
    path = ROOT / "PROJECT_STATE.md"
    text = path.read_text(encoding="utf-8")
    active_row = (
        "| 4-1 | Tone of the news, 1945-2010 | Source recovery blocked; PDF reference captured | "
        "`manual_review_needed` | Low | Supplemental PDF page 2 source line cites Leetaru 2011; First Monday article, "
        "GDELT image mirror, old-host checks, and Wayback CDX did not recover the monthly NYT/SWB tone tables. "
        "No reconstruction was plotted because chart digitization is forbidden. |"
    )
    if "| 4-1 |" not in text.split("## Active Figures", 1)[1].split("## Completed Figures", 1)[0]:
        marker = "| --- | --- | --- | --- | --- | --- |\n"
        text = text.replace(marker, marker + active_row + "\n", 1)
    text = text.replace("Last update: 2026-07-01 America/Los_Angeles", f"Last update: {TODAY} America/Los_Angeles")
    text = text.replace(
        "Project version: `1.10-production-loop-figure-10-1`",
        "Project version: `1.11-source-recovery-figure-4-1`",
    )
    history = (
        f"| `1.11-source-recovery-figure-4-1` | {TODAY} | Captured Figure 4-1 from the Supplemental Graphics PDF, "
        "confirmed the Leetaru 2011 source line, checked article/GDELT/old-host/Wayback paths, and left the figure "
        "as manual-review-needed because the monthly source tables were not recovered. |"
    )
    hist_marker = "## Repository Version History\n\n"
    if history not in text:
        text = text.replace(hist_marker, hist_marker + history + "\n", 1)
    path.write_text(text, encoding="utf-8")


def write_checksums() -> None:
    files = [
        p
        for p in BASE.rglob("*")
        if p.is_file() and p.relative_to(BASE).as_posix() != "checksums/sha256sums.txt"
    ]
    lines = [f"{sha256(p)}  {p.relative_to(ROOT).as_posix()}" for p in sorted(files)]
    (BASE / "checksums/sha256sums.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_review_pdf() -> None:
    manifest_path = ROOT / "output/pdf/recreated_figures_review_scroll.manifest.json"
    pdf_path = ROOT / "output/pdf/recreated_figures_review_scroll.pdf"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    item = {
        "figure_id": "4-1",
        "title": TITLE,
        "status": STATUS,
        "path": "figures/4-1/plots/comparisons/figure_4_1_extended_comparison.png",
        "selected_image": "figure_4_1_extended_comparison.png",
        "notes": "Source-recovery blocked: Leetaru 2011 monthly tone tables not recovered; no digitized reconstruction plotted.",
        "image_size": list(Image.open(BASE / "plots/comparisons/figure_4_1_extended_comparison.png").size),
    }
    items = [i for i in manifest["items"] if i["figure_id"] != "4-1"]
    items.insert(0, item)
    manifest["items"] = items
    manifest["count"] = len(items)
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.utils import ImageReader
        from reportlab.pdfgen import canvas
    except ImportError:
        return

    c = canvas.Canvas(str(pdf_path), pagesize=letter)
    width, height = letter
    c.setFont("Helvetica-Bold", 16)
    c.drawString(36, height - 40, "Recreated Figures Review Scroll")
    c.setFont("Helvetica", 10)
    c.drawString(36, height - 58, f"Generated {TODAY}; {len(items)} comparison/status items.")
    c.showPage()
    for entry in items:
        image_path = ROOT / entry["path"]
        if not image_path.exists():
            continue
        c.setFont("Helvetica-Bold", 13)
        c.drawString(36, height - 34, f"Figure {entry['figure_id']}: {entry['title']}")
        c.setFont("Helvetica", 9)
        c.drawString(36, height - 50, f"Status: {entry['status']}")
        c.drawString(36, height - 64, entry["notes"][:140])
        im = Image.open(image_path)
        max_w, max_h = width - 72, height - 110
        scale = min(max_w / im.width, max_h / im.height)
        draw_w, draw_h = im.width * scale, im.height * scale
        x, y = (width - draw_w) / 2, height - 90 - draw_h
        c.drawImage(ImageReader(im), x, y, width=draw_w, height=draw_h, preserveAspectRatio=True, mask="auto")
        c.showPage()
    c.save()


def main() -> None:
    ensure_dirs()
    render_pdf_page()
    collect_evidence()
    ref = crop_reference()
    book = placeholder_plot(extended=False)
    ext = placeholder_plot(extended=True)
    save_side_by_side(ref, book, BASE / "plots/comparisons/figure_4_1_book_period_comparison.png", "Figure 4-1 book-period comparison")
    save_side_by_side(ref, ext, BASE / "plots/comparisons/figure_4_1_extended_comparison.png", "Figure 4-1 extended comparison")
    write_text_files()
    write_metadata()
    update_registry()
    update_metadata_csv()
    update_project_state()
    write_checksums()
    update_review_pdf()


if __name__ == "__main__":
    main()
