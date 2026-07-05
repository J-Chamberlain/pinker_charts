#!/usr/bin/env python3
"""Figure 4-1 source-recovery package.

This intentionally creates a blocked/status artifact instead of a reconstructed
series. The accepted source trail currently contains Leetaru/GDELT plot images
and bibliographic evidence, but not the underlying monthly tone data.
"""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from datetime import date
from pathlib import Path

import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
FIG_ID = "4-1"
FIG_KEY = "4_1"
TODAY = date.today().isoformat()
BASE = ROOT / "figures" / FIG_ID
SOURCE_LINE = "Leetaru 2011. Plotted by month, beginning in January."
TITLE = "Tone of the news, 1945-2010"
STATUS = "manual_review_needed"
LIFECYCLE = "source_recovery_blocked_no_reconstruction"


def ensure_dirs() -> None:
    for rel in [
        "metadata",
        "provenance",
        "source_logs",
        "search_iterations",
        "discrepancy_logs",
        "anomaly_reviews",
        "captions",
        "checksums",
        "lineage",
        "plots/book_period",
        "plots/extended",
        "plots/comparisons",
        "plots/diagnostics",
        "data/raw",
        "data/candidates",
        "data/clean",
        "review",
    ]:
        (BASE / rel).mkdir(parents=True, exist_ok=True)


def render_pdf_reference() -> None:
    page = BASE / "data/raw/supplemental_page_02-02.png"
    if not page.exists():
        subprocess.run(
            [
                "pdftoppm",
                "-f",
                "2",
                "-l",
                "2",
                "-png",
                "-r",
                "220",
                str(ROOT / "references/enlightenment_now_supplemental_graphics.pdf"),
                str(BASE / "data/raw/supplemental_page_02"),
            ],
            check=True,
        )

    img = Image.open(page).convert("RGB")
    crop = img.crop((135, 205, 1225, 1010))
    crop.save(BASE / f"plots/comparisons/kindle_reference_figure_{FIG_KEY}.png")


def draw_status_panel(out: Path, extended: bool) -> None:
    fig, ax = plt.subplots(figsize=(10.6, 5.8))
    ax.axis("off")
    ax.text(0.03, 0.88, f"Figure {FIG_ID}: {TITLE}", fontsize=18, weight="bold")
    ax.text(0.03, 0.76, "Source recovery blocked", fontsize=15, weight="bold", color="#9b1c1c")
    body = [
        "No accepted underlying monthly data table was recovered.",
        "Leetaru/GDELT high-resolution PNGs were preserved as source-chain evidence only.",
        "The book/supplemental chart and Leetaru plot images were not digitized as data.",
        "Required next step: recover the original monthly NYT and SWB tone series,",
        "or a reproducible extraction from the original text corpora and sentiment method.",
    ]
    if extended:
        body.append("No extension is plotted until the book-period source is recovered.")
    ax.text(0.03, 0.60, "\n".join(body), fontsize=12.5, linespacing=1.55, va="top")
    ax.text(
        0.03,
        0.08,
        "Status: manual_review_needed | Visual artifact is a status panel, not a reconstruction.",
        fontsize=10,
        color="#555555",
    )
    fig.savefig(out, dpi=170, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def make_comparison(reference: Path, status_panel: Path, out: Path, label: str) -> None:
    ref = Image.open(reference).convert("RGB")
    stat = Image.open(status_panel).convert("RGB")
    target_h = 760
    ref = ref.resize((int(ref.width * target_h / ref.height), target_h), Image.Resampling.LANCZOS)
    stat = stat.resize((int(stat.width * target_h / stat.height), target_h), Image.Resampling.LANCZOS)
    margin = 55
    header_h = 90
    w = ref.width + stat.width + margin * 3
    h = target_h + header_h + margin
    canvas_img = Image.new("RGB", (w, h), "white")
    draw = ImageDraw.Draw(canvas_img)
    font = ImageFont.load_default()
    draw.text((margin, 24), f"Figure {FIG_ID}: {TITLE} - {label}", fill=(25, 25, 25), font=font)
    draw.text((margin, 58), "Supplemental PDF reference", fill=(80, 80, 80), font=font)
    draw.text((margin * 2 + ref.width, 58), "Source-recovery status", fill=(80, 80, 80), font=font)
    canvas_img.paste(ref, (margin, header_h))
    canvas_img.paste(stat, (margin * 2 + ref.width, header_h))
    canvas_img.save(out)


def write_text_files() -> None:
    (BASE / "captions/caption.txt").write_text(
        f"Figure {FIG_ID}: {TITLE}. Source line from the Supplemental Graphics PDF: {SOURCE_LINE} "
        "No recreated data series is plotted because the original monthly Leetaru data table was not recovered. "
        "Leetaru/GDELT high-resolution PNGs were preserved only as source-chain evidence; no plotted values from "
        "Pinker or Leetaru were digitized as reconstruction data.\n",
        encoding="utf-8",
    )

    (BASE / "provenance/provenance.md").write_text(
        f"""# Figure {FIG_ID} Provenance

## Evidence

- Title: {TITLE}
- Primary visual/source reference: Supplemental Graphics PDF page 2.
- Source line: {SOURCE_LINE}
- Visible series: New York Times, 1945-2005, and Summary of World Broadcasts, 1979-2010, plotted monthly in standard deviations.
- Kindle-specific confirmation: not performed in this executor session; the Supplemental Graphics PDF is the canonical project reference.

## Source Recovery Result

The cited publication is Kalev Leetaru's 2011 First Monday paper, "Culturomics 2.0: Forecasting large-scale human behavior using global news media tone in time and space." The GDELT blog mirrors the original high-resolution Figure 10 and Figure 11 images for the New York Times and Summary of World Broadcasts monthly tone charts. Those files are plot images, not the underlying monthly data.

No inspectable monthly data table for the two series was recovered in this pass. No Pinker or Leetaru plotted values were digitized.

## Reconstruction

No reconstruction data file was accepted. The generated comparison images include a Supplemental PDF reference crop and a source-recovery status panel only.

## Next Action

Recover the underlying monthly Leetaru 2011 tone data for New York Times and Summary of World Broadcasts, or a reproducible corpus/sentiment extraction matching Leetaru's method. If available, confirm the same source line in Kindle during a separate audit.
""",
        encoding="utf-8",
    )

    (BASE / "source_logs/source_log.md").write_text(
        f"""# Figure {FIG_ID} Source Log

Date: {TODAY}

## Accepted For Reconstruction

- None.

## Accepted As Evidence Only

- Supplemental Graphics PDF page 2, figure/source crop.
- Leetaru 2011 First Monday article: https://firstmonday.org/ojs/index.php/fm/article/view/3663/3040
- GDELT high-resolution figure mirror: https://blog.gdeltproject.org/culturomics-2-0-high-resolution-figures/
- Candidate visual files stored locally:
  - `figures/4-1/data/candidates/leetaru_2011_figure10_nyt_tone.png`
  - `figures/4-1/data/candidates/leetaru_2011_figure11_swb_tone.png`

## Rejected Or Unresolved

- Pinker's plotted values: not digitized and not used.
- Leetaru/GDELT PNG plots: rejected as reconstruction data because they are plotted images, not original monthly data.
- Underlying monthly NYT/SWB tone series: not recovered as an inspectable table.
- Corpus-level reproduction: not attempted because the original licensed/proprietary corpora and exact sentiment-processing pipeline were not recovered.

## Targeted Recovery

Search for Leetaru supplementary data, archived original figure-host data directories, author-shared monthly values, or a reproducible GDELT/NYT/SWB extraction that can regenerate the two monthly tone series without digitizing plots.
""",
        encoding="utf-8",
    )

    (BASE / "search_iterations/search_iterations.md").write_text(
        f"""# Figure {FIG_ID} Search Iterations

Date: {TODAY}

1. Inspected Supplemental Graphics PDF page 2 and extracted the title/source line.
2. Searched public web for `Leetaru 2011 tone of news coverage standard deviations 1945 2010 data`.
3. Located Leetaru 2011 First Monday article.
4. Located GDELT 2019 mirror of the original high-resolution Culturomics 2.0 figure images.
5. Downloaded Leetaru/GDELT Figure 10 and Figure 11 PNGs as candidate evidence only.
6. Searched for CSV/monthly data mirrors on `data.gdeltproject.org`, GDELT, and query snippets; no data table was found in this pass.
""",
        encoding="utf-8",
    )

    (BASE / "discrepancy_logs/discrepancy_log.md").write_text(
        f"""# Figure {FIG_ID} Discrepancy Log

- Critical source blocker: no accepted underlying monthly data table was recovered.
- Comparison images show a source-recovery status panel instead of a recreated chart.
- No book-period or extended numerical comparison can be generated without violating the no-digitization rule.
- The Leetaru/GDELT PNGs are visually relevant but cannot be treated as data.
""",
        encoding="utf-8",
    )

    (BASE / "anomaly_reviews/anomaly_review.md").write_text(
        f"""# Figure {FIG_ID} Anomaly Review

## Visible Differences

- The left side of the comparison is the Supplemental PDF reference crop.
- The right side is a source-recovery status panel, not a chart.
- This is intentional because the original monthly data were not recovered.

## Reviewer Challenge

- Pinker would likely ask why the Leetaru monthly values are not plotted. They were not recovered as data.
- A data journalist would ask whether the published chart was digitized. It was not.
- A peer reviewer would require either Leetaru's monthly table or a reproducible corpus extraction before accepting any reconstruction.
- A skeptical reader would immediately notice the missing recreated line; the status panel and caption explain the blocker.

## Editorial Review Gate

- Critical issues found: missing accepted reconstruction data.
- Major issues found: no book-period or extended reconstruction.
- Minor issues found: none beyond the status-panel nature of the artifact.
- Issues automatically corrected: the figure now has a reference crop, status panels, metadata, source log, provenance, caption, and checksums.
- Issues remaining: source recovery is still required before reconstruction.
- Publication decision: acceptable only as a documented source-recovery-blocked artifact, not as a completed figure.

## Confidence

- Overall confidence: low/source-blocked
- Book reconstruction: not attempted without accepted data
- Extension: not available
- Source provenance: citation and candidate visual source-chain evidence recovered; original monthly data unresolved
- Recommended next action: recover Leetaru's monthly NYT/SWB tone data or a reproducible corpus extraction.
""",
        encoding="utf-8",
    )

    (BASE / "review_checklist.md").write_text(
        f"""# Figure Acceptance Checklist

## Figure

- Figure ID: {FIG_ID}
- Title: {TITLE}
- Reviewer: Codex
- Review date: {TODAY}
- Current status: {STATUS}

## Phase 1 - Evidence Review

- [x] Supplemental Graphics PDF figure inspected.
- [x] Title extracted.
- [x] Source note extracted.
- [x] Surrounding page context reviewed.
- [x] Bibliography/source mapping documented.
- [ ] Kindle source line confirmed in this session.

## Phase 2 - Source Review

- [x] Original publication located.
- [x] Source chain partially reconstructed.
- [ ] Dataset provenance documented.
- [x] Archive/search notes documented.
- [ ] Successor datasets evaluated.
- [x] Source blocker explained.
- [x] Download URLs recorded for evidence-only candidate PNGs.
- [x] Checksums recorded for stored files.

## Phase 3 - Reconstruction Review

- [ ] Reconstruction uses legitimate data.
- [x] No digitized figure values used as reconstruction data.
- [ ] Transformation code is reproducible.
- [ ] Scales and labels are correct.
- [ ] Styling reasonably matches the book.
- [ ] Book-period reconstruction completed.
- [x] Book-period status comparison generated.
- [x] Remaining book-period discrepancies explained.

## Phase 4 - Extension Review

- [x] Later/source successor data searched at a preliminary level.
- [x] Absence of extension explained.
- [N/A] Extension clearly distinguished from book-period reconstruction.
- [N/A] Extended side-by-side comparison generated where available.

## Phase 5 - Reviewer Challenge

- [x] Answered: What would Steven Pinker likely question?
- [x] Answered: What would a data journalist question?
- [x] Answered: What would a peer reviewer question?
- [x] Answered: What would a skeptical reader notice immediately?
- [x] Each reviewer issue marked documented or new research task.

## Final Gate - Editorial Review

- [x] Book-period comparison/status image opened and visually scanned.
- [x] Extended comparison/status image opened and visually scanned.
- [x] Completeness checked; reconstruction absence is explicit.
- [x] Layout checked.
- [x] Visual similarity checked; no reconstruction claimed.
- [x] Extension clarity checked; no extension plotted.
- [x] Caption checked.
- [x] Every ten-second-obvious issue corrected or explicitly explained.
- [x] Issues classified as `Critical`, `Major`, or `Minor`.
- [ ] No `Critical` issues remain.
- [x] No unexplained `Major` issues remain.
- [x] Cross-figure review completed; single-figure batch.
- [x] Editorial Review Summary written.

## Repository Updates

- [x] Caption written or updated.
- [x] Anomaly review written or updated.
- [x] Provenance file updated.
- [x] Source log updated.
- [x] Search iteration log updated.
- [x] Discrepancy log updated.
- [x] Metadata updated.
- [x] Registry CSV updated.
- [x] Registry JSON updated.
- [x] `PROJECT_STATE.md` updated.
- [x] Review PDF/manifest updated.

## Reviewer Confidence

- Overall confidence: low/source-blocked
- Book reconstruction: not attempted
- Extension: unavailable
- Source provenance: partial citation/source-chain evidence only
- Outstanding risks: original monthly data may exist in an unrecovered author/archive location.
- Recommended next action: recover Leetaru monthly data or reproducible source extraction.

## Final Decision

- [x] Classified as `manual_review_needed`.
- [x] Returned to Source Recovery.
""",
        encoding="utf-8",
    )

    (BASE / "README.md").write_text(
        f"""# Figure {FIG_ID}: {TITLE}

Status: `{STATUS}`

This package documents a source-recovery blocker. The Supplemental PDF source
line and Leetaru/GDELT visual source chain were recovered, but the underlying
monthly New York Times and Summary of World Broadcasts tone data were not.
""",
        encoding="utf-8",
    )


def write_metadata_and_lineage() -> None:
    metadata = {
        "figure_id": FIG_ID,
        "title": TITLE,
        "chapter": "4",
        "book_page": "Supplemental PDF page 2; Kindle not inspected in this executor session",
        "year_range": "1945-2010",
        "claim_summary": "News coverage tone became more negative across the New York Times and Summary of World Broadcasts monthly series.",
        "book_citation": SOURCE_LINE,
        "original_dataset": "Leetaru 2011 monthly NYT/SWB tone data not recovered as an inspectable table.",
        "dataset_url": "",
        "archive_url": "",
        "download_date": TODAY,
        "reproduction_status": STATUS,
        "confidence_score": 0.35,
        "visual_validation": "blocked",
        "notes": "Source line and candidate visual source-chain evidence recovered; no reconstruction because original monthly data remain unresolved.",
        "canonical_artifacts": {
            "supplemental_reference": f"figures/{FIG_ID}/plots/comparisons/kindle_reference_figure_{FIG_KEY}.png",
            "book_period_status_panel": f"figures/{FIG_ID}/plots/book_period/figure_{FIG_KEY}_book_period_reconstruction.png",
            "extended_status_panel": f"figures/{FIG_ID}/plots/extended/figure_{FIG_KEY}_extended_reconstruction.png",
            "book_period_comparison": f"figures/{FIG_ID}/plots/comparisons/figure_{FIG_KEY}_book_period_comparison.png",
            "extended_comparison": f"figures/{FIG_ID}/plots/comparisons/figure_{FIG_KEY}_extended_comparison.png",
        },
    }
    (BASE / "metadata/metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")

    rows = [
        {
            "figure_id": FIG_ID,
            "artifact": "supplemental_reference",
            "source": "references/enlightenment_now_supplemental_graphics.pdf page 2",
            "status": "reference_only",
        },
        {
            "figure_id": FIG_ID,
            "artifact": "candidate_visual_source",
            "source": "GDELT mirror of Leetaru 2011 Figure 10 and Figure 11 PNGs",
            "status": "evidence_only_not_data",
        },
        {
            "figure_id": FIG_ID,
            "artifact": "status_panel",
            "source": "no accepted reconstruction data",
            "status": STATUS,
        },
    ]
    with (BASE / "lineage/figure_lineage.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["figure_id", "artifact", "source", "status"], lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    (BASE / "lineage/figure_lineage.json").write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")


def update_registry() -> None:
    path = ROOT / "data/figure_registry.csv"
    rows = list(csv.DictReader(path.open(encoding="utf-8")))
    for row in rows:
        if row["figure_id"] == FIG_ID:
            row["current_status"] = STATUS
            row["lifecycle_stage"] = LIFECYCLE
            row["priority"] = "active_high"
            row["current_owner"] = "Codex"
            row["next_action"] = "Recover Leetaru 2011 monthly NYT/SWB tone data or reproducible source extraction; optionally audit Kindle source line."
            row["notes"] = "Processed 2026-07-05: Supplemental PDF source line and Leetaru/GDELT candidate visual sources recovered; no original monthly data table found; no plotted values digitized."
            break
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys(), lineterminator="\r\n")
        writer.writeheader()
        writer.writerows(rows)
    (ROOT / "data/figure_registry.json").write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")


def update_metadata_csv() -> None:
    path = ROOT / "data/metadata/figure_metadata.csv"
    rows = list(csv.DictReader(path.open(encoding="utf-8")))
    fieldnames = list(rows[0].keys())
    existing = {row["figure_id"]: row for row in rows}
    row = existing.get(FIG_ID, {k: "" for k in fieldnames})
    row.update(
        {
            "figure_id": FIG_ID,
            "chapter": "4",
            "title": TITLE,
            "book_page": "Supplemental PDF page 2; Kindle not inspected in this executor session",
            "claim_summary": "News coverage tone became more negative across the New York Times and Summary of World Broadcasts monthly series.",
            "book_citation": SOURCE_LINE,
            "original_dataset": "Leetaru 2011 monthly NYT/SWB tone data not recovered as an inspectable table.",
            "dataset_url": "",
            "archive_url": "",
            "download_date": TODAY,
            "reproduction_status": STATUS,
            "confidence_score": "0.35",
            "visual_validation": "blocked",
            "notes": "Source line and candidate visual source-chain evidence recovered; no reconstruction because original monthly data remain unresolved.",
        }
    )
    if FIG_ID not in existing:
        rows.insert(0, row)
    else:
        rows = [row if r["figure_id"] == FIG_ID else r for r in rows]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\r\n")
        writer.writeheader()
        writer.writerows(rows)


def update_project_state() -> None:
    path = ROOT / "PROJECT_STATE.md"
    text = path.read_text(encoding="utf-8")
    text = text.replace("Last update: 2026-07-01 America/Los_Angeles", f"Last update: {TODAY} America/Los_Angeles")
    text = text.replace("Project version: `1.10-production-loop-figure-10-1`", "Project version: `1.11-source-recovery-figure-4-1`")
    row = f"| {FIG_ID} | {TITLE} | Source recovery blocked; Supplemental PDF reference captured | `{STATUS}` | Low | Source line and Leetaru/GDELT candidate visual source-chain evidence recovered, but underlying monthly NYT/SWB tone data were not found; no digitized reconstruction was made. |\n"
    if f"| {FIG_ID} | {TITLE} |" not in text:
        marker = "| 5-1 | Life expectancy"
        text = text.replace(marker, row + marker)
    section = f"""
### Figure {FIG_ID} - {TITLE}

Status: `{STATUS}`

Canonical visual artifacts:

- Supplemental reference: `figures/{FIG_ID}/plots/comparisons/kindle_reference_figure_{FIG_KEY}.png`
- Book-period status panel: `figures/{FIG_ID}/plots/book_period/figure_{FIG_KEY}_book_period_reconstruction.png`
- Extended status panel: `figures/{FIG_ID}/plots/extended/figure_{FIG_KEY}_extended_reconstruction.png`
- Book-period comparison/status: `figures/{FIG_ID}/plots/comparisons/figure_{FIG_KEY}_book_period_comparison.png`
- Extended comparison/status: `figures/{FIG_ID}/plots/comparisons/figure_{FIG_KEY}_extended_comparison.png`

Source status: Supplemental Graphics PDF source line captured; Leetaru 2011 article and GDELT high-resolution figure mirror located as source-chain evidence only. Original monthly data remain unrecovered, and no plotted values were digitized.
"""
    if f"### Figure {FIG_ID} - {TITLE}" not in text:
        marker = "## Completed Figures"
        text = text.replace(marker, section + "\n" + marker)
    changelog = f"| `1.11-source-recovery-figure-4-1` | {TODAY} | Processed Figure 4-1 as a documented source-recovery-blocked artifact; recovered Supplemental PDF source line and Leetaru/GDELT candidate visual evidence, but no underlying monthly data table. |\n"
    wrong_active_row = changelog
    active_header = "| Figure | Title | Lifecycle stage | Status | Confidence | Current disposition |\n| --- | --- | --- | --- | --- | --- |\n"
    text = text.replace(active_header + wrong_active_row, active_header)
    history_header = "## Repository Version History\n\n| Version | Date | Summary |\n| --- | --- | --- |\n"
    if "| `1.11-source-recovery-figure-4-1` |" not in text:
        text = text.replace(history_header, history_header + changelog, 1)
    path.write_text(text, encoding="utf-8")


def update_review_pdf() -> None:
    manifest_path = ROOT / "output/pdf/recreated_figures_review_scroll.manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    items = [item for item in manifest["items"] if item["figure_id"] != FIG_ID]
    img_path = f"figures/{FIG_ID}/plots/comparisons/figure_{FIG_KEY}_extended_comparison.png"
    with Image.open(ROOT / img_path) as img:
        size = list(img.size)
    items.insert(
        0,
        {
            "figure_id": FIG_ID,
            "title": TITLE,
            "status": STATUS,
            "path": img_path,
            "selected_image": Path(img_path).name,
            "notes": "Source-recovery-blocked status panel; original monthly Leetaru data not recovered and no plotted values digitized.",
            "image_size": size,
        },
    )
    manifest["count"] = len(items)
    manifest["items"] = items
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    pdf_path = ROOT / "output/pdf/recreated_figures_review_scroll.pdf"
    c = canvas.Canvas(str(pdf_path), pagesize=letter)
    page_w, page_h = letter
    c.setFont("Helvetica-Bold", 16)
    c.drawString(42, page_h - 54, "Recreated Figures Review Scroll")
    c.setFont("Helvetica", 10)
    c.drawString(42, page_h - 76, f"Generated {TODAY}; {len(items)} comparison/status items.")
    c.showPage()
    for item in items:
        p = ROOT / item["path"]
        if not p.exists():
            continue
        img = Image.open(p)
        max_w, max_h = page_w - 70, page_h - 135
        scale = min(max_w / img.width, max_h / img.height)
        draw_w, draw_h = img.width * scale, img.height * scale
        x, y = (page_w - draw_w) / 2, page_h - 82 - draw_h
        c.setFont("Helvetica-Bold", 12)
        c.drawString(35, page_h - 40, f"{item['figure_id']}: {item['title']} [{item['status']}]")
        c.setFont("Helvetica", 8)
        c.drawString(35, page_h - 56, item["notes"][:130])
        c.drawImage(ImageReader(img), x, y, width=draw_w, height=draw_h)
        c.showPage()
    c.save()


def write_checksums() -> None:
    paths = [
        BASE / f"plots/comparisons/kindle_reference_figure_{FIG_KEY}.png",
        BASE / f"plots/book_period/figure_{FIG_KEY}_book_period_reconstruction.png",
        BASE / f"plots/extended/figure_{FIG_KEY}_extended_reconstruction.png",
        BASE / f"plots/comparisons/figure_{FIG_KEY}_book_period_comparison.png",
        BASE / f"plots/comparisons/figure_{FIG_KEY}_extended_comparison.png",
        BASE / "data/candidates/leetaru_2011_figure10_nyt_tone.png",
        BASE / "data/candidates/leetaru_2011_figure11_swb_tone.png",
        ROOT / "output/pdf/recreated_figures_review_scroll.pdf",
        ROOT / "output/pdf/recreated_figures_review_scroll.manifest.json",
    ]
    lines = []
    for path in paths:
        if path.exists():
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            lines.append(f"{digest}  {path.relative_to(ROOT)}")
    (BASE / "checksums/sha256sums.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    ensure_dirs()
    render_pdf_reference()
    reference = BASE / f"plots/comparisons/kindle_reference_figure_{FIG_KEY}.png"
    book_panel = BASE / f"plots/book_period/figure_{FIG_KEY}_book_period_reconstruction.png"
    extended_panel = BASE / f"plots/extended/figure_{FIG_KEY}_extended_reconstruction.png"
    draw_status_panel(book_panel, extended=False)
    draw_status_panel(extended_panel, extended=True)
    make_comparison(reference, book_panel, BASE / f"plots/comparisons/figure_{FIG_KEY}_book_period_comparison.png", "book-period status")
    make_comparison(reference, extended_panel, BASE / f"plots/comparisons/figure_{FIG_KEY}_extended_comparison.png", "extended status")
    write_text_files()
    write_metadata_and_lineage()
    update_registry()
    update_metadata_csv()
    update_project_state()
    update_review_pdf()
    write_checksums()


if __name__ == "__main__":
    main()
