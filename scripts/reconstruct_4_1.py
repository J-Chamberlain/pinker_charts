#!/usr/bin/env python3
"""Source-recovery artifact builder for Figure 4-1.

This figure is intentionally not reconstructed from the printed line chart.
The accepted outcome of this pass is a documented source blocker plus visual
reference artifacts.
"""

from __future__ import annotations

import base64
import csv
import hashlib
import json
import shutil
import subprocess
import textwrap
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures" / "4-1"
TODAY = date(2026, 7, 4).isoformat()

TITLE = "Tone of the news, 1945-2010"
STATUS = "manual_review_needed"
LIFECYCLE = "source_recovery_blocked_reference_captured"
CONFIDENCE = 0.30

PDF_REF = FIG / "plots" / "comparisons" / "pdf_reference_figure_4_1.png"
BOOK_PANEL = FIG / "plots" / "book_period" / "figure_4_1_book_period_reconstruction.png"
EXT_PANEL = FIG / "plots" / "extended" / "figure_4_1_extended_reconstruction.png"
BOOK_COMP = FIG / "plots" / "comparisons" / "figure_4_1_book_period_comparison.png"
EXT_COMP = FIG / "plots" / "comparisons" / "figure_4_1_extended_comparison.png"

LEETARU_ARTICLE = "https://firstmonday.org/ojs/index.php/fm/article/view/3663/3040"
GDELT_FIGURES = "https://blog.gdeltproject.org/culturomics-2-0-high-resolution-figures/"
NYT_PNG = "http://data.gdeltproject.org/blog/2011-culturomics-20/figure10.png"
SWB_PNG = "http://data.gdeltproject.org/blog/2011-culturomics-20/figure11.png"


def ensure_dirs() -> None:
    for rel in [
        "metadata",
        "provenance",
        "source_logs",
        "anomaly_reviews",
        "captions",
        "plots/comparisons",
        "plots/book_period",
        "plots/extended",
        "data/raw",
        "data/candidates",
        "search_iterations",
        "checksums",
        "lineage",
        "discrepancy_logs",
    ]:
        (FIG / rel).mkdir(parents=True, exist_ok=True)


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, cwd=ROOT, check=True)


def png_size(path: Path) -> tuple[int, int]:
    with path.open("rb") as f:
        sig = f.read(24)
    if sig[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"{path} is not a PNG")
    return int.from_bytes(sig[16:20], "big"), int.from_bytes(sig[20:24], "big")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def xml_escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def svg_text_lines(text: str, x: int, y: int, width: int, size: int, leading: int) -> str:
    lines: list[str] = []
    for para in text.split("\n"):
        wrapped = textwrap.wrap(para, max(24, width // (size // 2)), break_long_words=False)
        lines.extend(wrapped or [""])
    out = []
    yy = y
    for line in lines:
        out.append(f'<text x="{x}" y="{yy}" class="body">{xml_escape(line)}</text>')
        yy += leading
    return "\n".join(out)


def write_svg(path: Path, title: str, body: str, *, width: int = 1517, height: int = 917) -> None:
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" fill="#ffffff"/>
  <style>
    .title {{ font-family: Helvetica, Arial, sans-serif; font-size: 52px; font-weight: 700; fill: #222; }}
    .kicker {{ font-family: Helvetica, Arial, sans-serif; font-size: 24px; font-weight: 700; fill: #777; letter-spacing: 1px; }}
    .body {{ font-family: Helvetica, Arial, sans-serif; font-size: 30px; fill: #2a2a2a; }}
    .small {{ font-family: Helvetica, Arial, sans-serif; font-size: 24px; fill: #555; }}
  </style>
  <text x="80" y="120" class="kicker">FIGURE 4-1 SOURCE RECOVERY</text>
  <text x="80" y="190" class="title">{xml_escape(title)}</text>
  <line x1="80" y1="230" x2="{width - 80}" y2="230" stroke="#d0d0d0" stroke-width="3"/>
  {svg_text_lines(body, 80, 300, width - 160, 30, 45)}
  <text x="80" y="{height - 90}" class="small">Generated {TODAY}. This is a blocker/status artifact, not a data reconstruction.</text>
</svg>
"""
    path.write_text(svg, encoding="utf-8")


def svg_to_png(svg_path: Path, png_path: Path, size: int) -> None:
    del size
    tmp_jpg = png_path.with_suffix(".render.jpg")
    run(["sips", "-s", "format", "jpeg", str(svg_path), "--out", str(tmp_jpg)])
    run(["sips", "-s", "format", "png", str(tmp_jpg), "--out", str(png_path)])
    tmp_jpg.unlink(missing_ok=True)


def write_comparison_svg(path: Path, title: str, right_png: Path) -> None:
    ref_w, ref_h = png_size(PDF_REF)
    right_w, right_h = png_size(right_png)
    ref_b64 = base64.b64encode(PDF_REF.read_bytes()).decode("ascii")
    right_b64 = base64.b64encode(right_png.read_bytes()).decode("ascii")
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="2095" height="861" viewBox="0 0 2095 861">
  <rect width="100%" height="100%" fill="#ffffff"/>
  <style>
    .head {{ font-family: Helvetica, Arial, sans-serif; font-size: 32px; font-weight: 700; fill: #222; }}
    .label {{ font-family: Helvetica, Arial, sans-serif; font-size: 23px; font-weight: 700; fill: #555; }}
  </style>
  <text x="45" y="50" class="head">{xml_escape(title)}</text>
  <text x="55" y="95" class="label">Supplemental Graphics PDF reference</text>
  <text x="1085" y="95" class="label">Repository status artifact</text>
  <rect x="45" y="120" width="970" height="710" fill="#fafafa" stroke="#dddddd"/>
  <image href="data:image/png;base64,{ref_b64}" x="85" y="150" width="890" height="{int(890 * ref_h / ref_w)}"/>
  <rect x="1065" y="120" width="985" height="710" fill="#fafafa" stroke="#dddddd"/>
  <image href="data:image/png;base64,{right_b64}" x="1115" y="155" width="885" height="{int(885 * right_h / right_w)}"/>
</svg>
"""
    path.write_text(svg, encoding="utf-8")


def make_visuals() -> None:
    body = (
        "No reconstructed line chart was generated.\n"
        "The Supplemental Graphics PDF cites Leetaru 2011 and says the series are plotted by month. "
        "The First Monday article and GDELT mirror identify the two source visuals: New York Times "
        "monthly tone, 1945-2005, and Summary of World Broadcasts monthly tone, January 1979-July 2010.\n"
        "The underlying monthly numeric data file was not located in this pass. The mirrored Leetaru PNGs "
        "are retained as visual evidence only. The project rule forbids digitizing Pinker's plotted values "
        "or Leetaru's plotted PNGs as source data."
    )
    book_svg = BOOK_PANEL.with_suffix(".svg")
    ext_svg = EXT_PANEL.with_suffix(".svg")
    write_svg(book_svg, "Source data not recovered", body)
    write_svg(ext_svg, "No valid extension", body + "\nNo book-period dataset means no defensible post-2010 extension.")
    svg_to_png(book_svg, BOOK_PANEL, 1517)
    svg_to_png(ext_svg, EXT_PANEL, 1517)

    book_comp_svg = BOOK_COMP.with_suffix(".svg")
    ext_comp_svg = EXT_COMP.with_suffix(".svg")
    write_comparison_svg(book_comp_svg, "Figure 4-1 book-period comparison", BOOK_PANEL)
    write_comparison_svg(ext_comp_svg, "Figure 4-1 extended comparison", EXT_PANEL)
    svg_to_png(book_comp_svg, BOOK_COMP, 2095)
    svg_to_png(ext_comp_svg, EXT_COMP, 2095)


def write_docs() -> None:
    (FIG / "README.md").write_text(
        f"""# Figure 4-1: {TITLE}

Status: `{STATUS}`

This directory records a source-recovery pass completed on {TODAY}. The Supplemental
Graphics PDF reference and source line were captured, and Leetaru 2011/GDELT visual
evidence was saved, but the underlying monthly numeric tone data were not recovered.
No reconstruction was made from plotted values.
""",
        encoding="utf-8",
    )
    (FIG / "captions" / "caption.txt").write_text(
        "Figure 4-1: Tone of the news, 1945-2010. Supplemental Graphics PDF source line: "
        "Leetaru 2011; plotted by month, beginning in January. No recreated data series is "
        "plotted because the original monthly tone values for the New York Times and Summary "
        "of World Broadcasts were not recovered as inspectable data. The Leetaru/GDELT PNGs "
        "are retained only as visual source evidence, and no plotted values were digitized.\n",
        encoding="utf-8",
    )
    (FIG / "provenance" / "provenance.md").write_text(
        f"""# Figure 4-1 Provenance

## Evidence

- Title: {TITLE}
- Primary reference: Supplemental Graphics PDF page 2.
- Source line: Leetaru 2011. Plotted by month, beginning in January.
- Book visual: two monthly tone series, New York Times and Summary of World Broadcasts, in standard deviations.
- Source article: Leetaru 2011, *Culturomics 2.0: Forecasting large-scale human behavior using global news media tone in time and space*, First Monday.

## Source Recovery Result

The underlying monthly numeric tone series were not recovered as inspectable files.
The First Monday article documents the source corpora and method, and the GDELT
mirror provides high-resolution original PNGs for the two component figures, but
those PNGs are not source data.

## Reconstruction

No reconstruction data file was accepted. The generated comparison images include
the Supplemental Graphics PDF reference and a source-recovery/status panel only.
This is intentional: project rules forbid digitizing Pinker's plotted values, and
the same caution applies to Leetaru's plotted figure PNGs.

## Next Action

Recover an original Leetaru monthly-tone table, code output, or author/institutional
archive for:

- New York Times average monthly tone, January 1945-December 2005.
- Summary of World Broadcasts average monthly tone, January 1979-July 2010.

Useful evidence URLs:

- {LEETARU_ARTICLE}
- {GDELT_FIGURES}
- {NYT_PNG}
- {SWB_PNG}
""",
        encoding="utf-8",
    )
    (FIG / "source_logs" / "source_log.md").write_text(
        f"""# Figure 4-1 Source Log

Date: {TODAY}

## Accepted Sources

- Supplemental Graphics PDF page 2, accepted as the primary reference image and source-line authority.
- Leetaru 2011 First Monday article, accepted for method/source-corpus context.
- GDELT 2019 high-resolution figure mirror, accepted as visual evidence for Leetaru figures 10 and 11 only.

## Rejected Or Unresolved

- No underlying monthly numeric table was located.
- Pinker's plotted values were not digitized.
- Leetaru/GDELT plotted PNG values were not digitized.
- The Internet Archive CDX probe for the GDELT 2011 figure directory did not expose a companion CSV/table.

## Search Notes

- Searched web for Leetaru 2011 tone of news coverage standard deviations, Culturomics 2.0 data files, New York Times tone, and Summary of World Broadcasts tone.
- Downloaded the First Monday HTML article to `data/candidates/leetaru_2011_culturomics20_first_monday.html`.
- Downloaded Leetaru figure PNGs 10 and 11 to `data/candidates/` as visual evidence.

## Targeted Recovery

Search author, ICHASS/NCSA, GDELT, First Monday, and web archive holdings for a CSV,
spreadsheet, or code-output table containing the monthly z-scores behind figures 10
and 11 of Leetaru 2011.
""",
        encoding="utf-8",
    )
    (FIG / "anomaly_reviews" / "anomaly_review.md").write_text(
        f"""# Figure 4-1 Anomaly Review

## Visible Differences

- The left panel shows the Supplemental Graphics PDF reference.
- The right panel is a source-recovery/status panel, not a recreated chart.
- No extended line is shown because no accepted book-period numeric data exist.

## Reviewer Challenge

- Pinker would likely ask for the Leetaru monthly tone values. They were not recovered as an inspectable source file.
- A data journalist would ask whether the chart was digitized. It was not.
- A peer reviewer would require original monthly values or reproducible text-mining output before accepting a reconstruction.
- A reader will immediately notice the missing recreated line; the panel and caption explicitly explain the blocker.

## Editorial Review Summary

- Critical issues found: missing underlying numeric source data, which blocks reconstruction.
- Major issues found: no book-period or extended comparison can be accepted as a data reconstruction.
- Minor issues found: status-panel typography is utilitarian.
- Issues automatically corrected: captured the Supplemental Graphics PDF page-2 reference and saved Leetaru/GDELT visual evidence with source notes.
- Issues remaining: original monthly tone data still need recovery.
- Publication calibration: acceptable only as a documented source-recovery artifact; not accepted as a recreated figure.

## Confidence

- Overall confidence: low/source-blocked.
- Book reconstruction: not attempted without accepted data.
- Extension: not available.
- Recommended next action: recover original Leetaru monthly-tone data or code output.
""",
        encoding="utf-8",
    )
    (FIG / "discrepancy_logs" / "discrepancy_log.md").write_text(
        "# Figure 4-1 Discrepancy Log\n\nNo data discrepancies were measured because no reconstruction was attempted.\n",
        encoding="utf-8",
    )
    (FIG / "search_iterations" / "search_iterations.md").write_text(
        f"""# Figure 4-1 Search Iterations

Date: {TODAY}

1. Confirmed Supplemental Graphics PDF page 2 source line.
2. Located Leetaru 2011 First Monday article and method/source-corpus discussion.
3. Located GDELT high-resolution mirror for Leetaru figures 10 and 11.
4. Downloaded figure PNGs as visual evidence only.
5. Probed Internet Archive CDX for the GDELT 2011 figure directory; no companion numeric data were found in this pass.

Blocked next step: find original monthly z-score tables or author code output.
""",
        encoding="utf-8",
    )
    lineage = [
        {"stage": "Book Figure", "value": "Figure 4-1: Tone of the news, 1945-2010", "status": "confirmed"},
        {"stage": "Book Citation", "value": "Leetaru 2011", "status": "confirmed"},
        {"stage": "Original Article", "value": LEETARU_ARTICLE, "status": "located"},
        {"stage": "Original Visuals", "value": f"{NYT_PNG}; {SWB_PNG}", "status": "located_visual_only"},
        {"stage": "Original Dataset", "value": "Monthly tone z-scores", "status": "not_located"},
        {"stage": "Generated Plot", "value": str(BOOK_PANEL.relative_to(ROOT)), "status": "status_panel_only"},
    ]
    with (FIG / "lineage" / "figure_lineage.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["figure_id", "stage", "value", "status"])
        w.writeheader()
        for row in lineage:
            w.writerow({"figure_id": "4-1", **row})
    (FIG / "lineage" / "figure_lineage.json").write_text(json.dumps(lineage, indent=2) + "\n", encoding="utf-8")


def write_metadata() -> None:
    meta = {
        "figure_id": "4-1",
        "title": TITLE,
        "chapter": "4",
        "book_page": "Supplemental Graphics PDF page 2",
        "year_range": "1945-2010",
        "claim_summary": "Pinker uses Leetaru's monthly tone series to argue that news became increasingly negative even as objective human welfare improved.",
        "book_citation": "Leetaru 2011. Plotted by month, beginning in January.",
        "original_dataset": "Leetaru 2011 monthly tone z-scores for New York Times and Summary of World Broadcasts were not recovered as inspectable data files.",
        "dataset_url": "",
        "archive_url": "",
        "download_date": TODAY,
        "reproduction_status": STATUS,
        "confidence_score": CONFIDENCE,
        "visual_validation": "blocked",
        "notes": "Reference and source chain captured; no digitized values used; recover original Leetaru monthly tables before reconstruction.",
        "canonical_artifacts": {
            "pdf_reference": str(PDF_REF.relative_to(ROOT)),
            "book_period_comparison": str(BOOK_COMP.relative_to(ROOT)),
            "extended_comparison": str(EXT_COMP.relative_to(ROOT)),
            "book_period_status_panel": str(BOOK_PANEL.relative_to(ROOT)),
            "extended_status_panel": str(EXT_PANEL.relative_to(ROOT)),
        },
    }
    (FIG / "metadata" / "metadata.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")


def upsert_csv(path: Path, key: str, row: dict[str, object]) -> None:
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)
    for k in row:
        if k not in fieldnames:
            fieldnames.append(k)
    values = {k: "" for k in fieldnames}
    values.update({k: str(v) for k, v in row.items()})
    replaced = False
    for i, existing in enumerate(rows):
        if existing.get(key) == row[key]:
            merged = {k: existing.get(k, "") for k in fieldnames}
            merged.update(values)
            rows[i] = merged
            replaced = True
            break
    if not replaced:
        rows.append(values)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def update_registries() -> None:
    registry_row = {
        "figure_id": "4-1",
        "book": "Enlightenment Now",
        "chapter": "4",
        "title": TITLE,
        "page": "",
        "year_range": "1945-2010",
        "current_status": STATUS,
        "lifecycle_stage": LIFECYCLE,
        "source_type_guess": "media_text_analysis_dataset",
        "priority": "active_high",
        "current_owner": "Codex",
        "next_action": "Recover original Leetaru 2011 monthly tone tables/code output for NYT and SWB; do not digitize plotted values.",
        "notes": "Processed 2026-07-04: Supplemental PDF reference and Leetaru/GDELT visual source evidence captured; numeric monthly data not recovered.",
    }
    upsert_csv(ROOT / "data" / "figure_registry.csv", "figure_id", registry_row)
    data = json.loads((ROOT / "data" / "figure_registry.json").read_text(encoding="utf-8"))
    for i, item in enumerate(data):
        if item.get("figure_id") == "4-1":
            data[i] = registry_row
            break
    else:
        data.append(registry_row)
    (ROOT / "data" / "figure_registry.json").write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    metadata_row = {
        "figure_id": "4-1",
        "chapter": "4",
        "title": TITLE,
        "book_page": "Supplemental PDF page 2",
        "claim_summary": "Leetaru's news-tone series show increasingly negative news tone across NYT and SWB coverage.",
        "book_citation": "Leetaru 2011. Plotted by month, beginning in January.",
        "original_dataset": "Leetaru monthly tone z-scores not recovered as inspectable data.",
        "dataset_url": "",
        "archive_url": "",
        "download_date": TODAY,
        "reproduction_status": STATUS,
        "confidence_score": CONFIDENCE,
        "visual_validation": "blocked",
        "notes": "Source-recovery blocker documented; no digitized plotted values used.",
    }
    upsert_csv(ROOT / "data" / "metadata" / "figure_metadata.csv", "figure_id", metadata_row)


def update_project_state() -> None:
    path = ROOT / "PROJECT_STATE.md"
    text = path.read_text(encoding="utf-8")
    text = text.replace("Last update: 2026-07-01 America/Los_Angeles", f"Last update: {TODAY} America/Los_Angeles")
    text = text.replace("Project version: `1.10-production-loop-figure-10-1`", "Project version: `1.11-figure-4-1-source-recovery`")
    row = "| 4-1 | Tone of the news, 1945-2010 | Source recovery blocked; PDF reference captured | `manual_review_needed` | Low | Supplemental Graphics PDF page 2 and Leetaru 2011/GDELT visual evidence were captured, but original monthly NYT/SWB tone values were not recovered; no digitized reconstruction was made. |\n"
    marker = "| 5-1 | Life expectancy, 1771-2015 |"
    if "| 4-1 | Tone of the news" not in text:
        text = text.replace(marker, row + marker)
    unresolved = "- Figure 4-1: Supplemental PDF reference and Leetaru 2011 source chain are captured, but original monthly NYT/SWB tone values were not recovered; no digitized reconstruction was made.\n"
    if unresolved not in text:
        text = text.replace("## Attempted But Not Expanded\n", unresolved + "\n## Attempted But Not Expanded\n")
    text = text.replace(
        "Figures 5-1, 5-2, 5-3, 5-4, 6-1, 7-1, 7-2, 8-4, 10-5, 10-6, 10-7, 10-8, and 19-1 have been carried",
        "Figures 4-1, 5-1, 5-2, 5-3, 5-4, 6-1, 7-1, 7-2, 8-4, 10-5, 10-6, 10-7, 10-8, and 19-1 have been carried",
    )
    section = f"""### Figure 4-1 - Tone of the news, 1945-2010

Status: `manual_review_needed`

Canonical visual artifacts:

- Original reference: `figures/4-1/plots/comparisons/pdf_reference_figure_4_1.png`
- Book-period status panel: `figures/4-1/plots/book_period/figure_4_1_book_period_reconstruction.png`
- Extended status panel: `figures/4-1/plots/extended/figure_4_1_extended_reconstruction.png`
- Book-period comparison: `figures/4-1/plots/comparisons/figure_4_1_book_period_comparison.png`
- Extended comparison: `figures/4-1/plots/comparisons/figure_4_1_extended_comparison.png`

Canonical documentation:

- Caption: `figures/4-1/captions/caption.txt`
- Provenance: `figures/4-1/provenance/provenance.md`
- Anomaly review: `figures/4-1/anomaly_reviews/anomaly_review.md`
- Metadata: `figures/4-1/metadata/metadata.json`
- Review checklist: `figures/4-1/review_checklist.md`

"""
    if "### Figure 4-1 - Tone of the news" not in text:
        text = text.replace("### Figure 5-1 - Life expectancy, 1771-2015\n", section + "### Figure 5-1 - Life expectancy, 1771-2015\n")
    changelog = f"| `1.11-figure-4-1-source-recovery` | {TODAY} | Processed Figure 4-1 as a documented source-recovery blocker: Supplemental PDF reference and Leetaru/GDELT visual evidence captured, but no monthly numeric tone data recovered and no digitized reconstruction made. |\n"
    if "`1.11-figure-4-1-source-recovery`" not in text:
        text = text.replace("| `1.6-supplemental-graphics-reference`", changelog + "| `1.6-supplemental-graphics-reference`")
    path.write_text(text, encoding="utf-8")


def write_review_checklist() -> None:
    (FIG / "review_checklist.md").write_text(
        f"""# Figure Acceptance Checklist

## Figure

- Figure ID: 4-1
- Title: {TITLE}
- Reviewer: Codex
- Review date: {TODAY}
- Current status: {STATUS}

## Phase 1 - Evidence Review

- [x] Supplemental Graphics PDF figure inspected.
- [x] Title extracted.
- [x] Caption/source note extracted.
- [x] Surrounding page reviewed.
- [x] Bibliography/source mapping documented or unresolved.

## Phase 2 - Source Review

- [x] Original/successor publication located.
- [ ] Dataset provenance documented.
- [x] Archive/search notes documented.
- [ ] Successor datasets evaluated.
- [x] Substitution or source blocker explained.

## Phase 3 - Reconstruction Review

- [ ] Reconstruction uses legitimate data.
- [x] No digitized figure values used as reconstruction data.
- [ ] Transformation code is reproducible.
- [x] Book-period comparison/status artifact generated.
- [x] Remaining book-period discrepancies explained.

## Phase 4 - Extension Review

- [x] Later data searched and documented at source-family level.
- [x] Extension absence explained.
- [x] Extended comparison/status artifact generated.

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
- [x] Registry updated.
- [x] Review PDF and manifest updated.

## Final Decision

- [ ] Accepted as `updated_equivalent`.
- [x] Classified as `manual_review_needed`.
""",
        encoding="utf-8",
    )


def write_checksums() -> None:
    files = sorted(p for p in FIG.rglob("*") if p.is_file() and "checksums/sha256sums.txt" not in str(p))
    lines = [f"{sha256(p)}  {p.relative_to(FIG)}" for p in files]
    (FIG / "checksums" / "sha256sums.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_review_pdf() -> None:
    manifest_path = ROOT / "output" / "pdf" / "recreated_figures_review_scroll.manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    item = {
        "figure_id": "4-1",
        "title": TITLE,
        "status": STATUS,
        "path": str(EXT_COMP.relative_to(ROOT)),
        "selected_image": EXT_COMP.name,
        "notes": "Source-recovery-only artifact: Supplemental PDF reference captured; original Leetaru monthly tone values not recovered; no digitized reconstruction.",
        "image_size": list(png_size(EXT_COMP)),
    }
    items = [x for x in manifest["items"] if x.get("figure_id") != "4-1"]
    items.insert(0, item)
    manifest["items"] = items
    manifest["count"] = len(items)
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    pdf_tmp = ROOT / "output" / "pdf" / "_pages"
    shutil.rmtree(pdf_tmp, ignore_errors=True)
    pdf_tmp.mkdir(parents=True, exist_ok=True)
    pdfs: list[Path] = []
    for idx, entry in enumerate(items, start=1):
        img = ROOT / entry["path"]
        pdf = pdf_tmp / f"{idx:03d}_{entry['figure_id'].replace('-', '_')}.pdf"
        run(["sips", "-s", "format", "pdf", str(img), "--out", str(pdf)])
        pdfs.append(pdf)
    out_pdf = ROOT / "output" / "pdf" / "recreated_figures_review_scroll.pdf"
    run(["pdfunite", *map(str, pdfs), str(out_pdf)])
    shutil.rmtree(pdf_tmp, ignore_errors=True)


def main() -> None:
    ensure_dirs()
    if not PDF_REF.exists():
        run([
            "pdftoppm",
            "-png",
            "-r",
            "180",
            "-f",
            "2",
            "-l",
            "2",
            "-singlefile",
            "-x",
            "80",
            "-y",
            "130",
            "-W",
            "860",
            "-H",
            "650",
            "references/enlightenment_now_supplemental_graphics.pdf",
            str(PDF_REF.with_suffix("")),
        ])
    make_visuals()
    write_docs()
    write_metadata()
    write_review_checklist()
    update_registries()
    update_project_state()
    update_review_pdf()
    write_checksums()


if __name__ == "__main__":
    main()
