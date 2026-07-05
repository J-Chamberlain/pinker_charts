from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from datetime import date
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
FIG_ID = "10-4"
BASE = ROOT / "figures" / FIG_ID
TODAY = date.today().isoformat()

SUPPLEMENTAL_PDF = ROOT / "references" / "enlightenment_now_supplemental_graphics.pdf"
FAO_SOFO_2012_URL = "https://www.fao.org/4/i3010e/i3010e.pdf"
FAO_CHAPTER2_URL = "https://www.fao.org/4/i3010e/i3010e02.pdf"
STATUS = "manual_review_needed"


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
        "checksums",
    ]:
        (BASE / part).mkdir(parents=True, exist_ok=True)


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def download_sources() -> None:
    downloads = [
        (FAO_SOFO_2012_URL, BASE / "data/raw/fao_state_of_worlds_forests_2012.pdf"),
        (FAO_CHAPTER2_URL, BASE / "data/raw/fao_state_of_worlds_forests_2012_chapter2.pdf"),
    ]
    for url, out in downloads:
        if out.exists() and out.stat().st_size > 0:
            continue
        run(["curl", "-L", "--fail", "--silent", "--max-time", "45", url, "-o", str(out)])


def render_pdf_page(pdf: Path, page: int, out_prefix: Path, dpi: int = 180) -> Path:
    out_prefix.parent.mkdir(parents=True, exist_ok=True)
    run(["pdftoppm", "-png", "-r", str(dpi), "-f", str(page), "-l", str(page), str(pdf), str(out_prefix)])
    return out_prefix.with_name(f"{out_prefix.name}-{page}.png")


def crop_reference_images() -> tuple[Path, Path, Path]:
    supp_page = render_pdf_page(SUPPLEMENTAL_PDF, 14, BASE / "data/raw/supplemental_pdf_page", 180)
    fao_page = render_pdf_page(BASE / "data/raw/fao_state_of_worlds_forests_2012.pdf", 21, BASE / "data/raw/fao_sofo_2012_page", 220)

    supp_crop = BASE / "plots/comparisons/supplemental_pdf_reference_figure_10_4.png"
    fao_crop = BASE / "plots/comparisons/fao_sofo_2012_source_figure_2.png"
    fao_page_copy = BASE / "plots/comparisons/fao_sofo_2012_page_9_context.png"

    Image.open(supp_page).convert("RGB").crop((65, 35, 1045, 695)).save(supp_crop)
    Image.open(fao_page).convert("RGB").crop((1010, 1080, 1780, 1585)).save(fao_crop)
    Image.open(fao_page).convert("RGB").save(fao_page_copy)
    return supp_crop, fao_crop, fao_page_copy


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            continue
    return ImageFont.load_default()


def wrap_text(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.ImageFont, width: int) -> list[str]:
    lines: list[str] = []
    for para in text.split("\n"):
        if not para:
            lines.append("")
            continue
        current = ""
        for word in para.split():
            trial = word if not current else f"{current} {word}"
            if draw.textbbox((0, 0), trial, font=fnt)[2] <= width:
                current = trial
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
    return lines


def make_status_panel(out: Path, heading: str, body: str) -> None:
    img = Image.new("RGB", (1400, 850), "white")
    draw = ImageDraw.Draw(img)
    title_font = font(34, True)
    body_font = font(24)
    small_font = font(20)
    draw.rectangle((0, 0, 1400, 92), fill=(42, 42, 42))
    draw.text((42, 25), heading, fill="white", font=title_font)
    y = 140
    for line in wrap_text(draw, body, body_font, 1280):
        draw.text((60, y), line, fill=(35, 35, 35), font=body_font)
        y += 36 if line else 22
    draw.line((60, 690, 1340, 690), fill=(190, 190, 190), width=2)
    draw.text((60, 720), "No plotted values from Pinker's chart were digitized or used as source data.", fill=(70, 70, 70), font=small_font)
    draw.text((60, 752), "The next recovery target is the Williams 2002 / FAO 2010b estimate table behind FAO SOFO 2012 Figure 2.", fill=(70, 70, 70), font=small_font)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out)


def side_by_side(left: Path, right: Path, out: Path, title: str) -> None:
    left_img = Image.open(left).convert("RGB")
    right_img = Image.open(right).convert("RGB")
    h = 740
    left_img.thumbnail((900, h), Image.Resampling.LANCZOS)
    right_img.thumbnail((900, h), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (1900, 980), "white")
    draw = ImageDraw.Draw(canvas)
    draw.text((40, 30), title, fill=(25, 25, 25), font=font(30, True))
    draw.text((40, 82), "Supplemental Graphics PDF reference", fill=(75, 75, 75), font=font(22, True))
    draw.text((990, 82), "Reconstruction status", fill=(75, 75, 75), font=font(22, True))
    canvas.paste(ImageOps.expand(left_img, border=1, fill=(210, 210, 210)), (40, 125))
    canvas.paste(ImageOps.expand(right_img, border=1, fill=(210, 210, 210)), (990, 125))
    out.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out)


def make_visuals(supp_crop: Path, fao_crop: Path) -> None:
    book_panel = BASE / "plots/book_period/figure_10_4_book_period_source_recovery_status.png"
    ext_panel = BASE / "plots/extended/figure_10_4_extended_source_recovery_status.png"
    make_status_panel(
        book_panel,
        "Figure 10-4: source recovery blocked",
        "Recovered source line: United Nations Food and Agriculture Organization 2012, p. 9.\n"
        "Recovered source graphic: State of the World's Forests 2012, Figure 2, 'Estimated deforestation, by type of forest and time period.'\n"
        "The source graphic is based on Williams 2002 and FAO 2010b. The underlying numerical estimate table was not found in the FAO PDF text stream, FAO chapter PDF, likely OWID grapher slugs, or targeted web searches in this pass.\n"
        "Because the original estimate table remains unrecovered, this artifact is a source-recovery status panel rather than a data reconstruction.",
    )
    make_status_panel(
        ext_panel,
        "Figure 10-4: no comparable extension",
        "The book-period chart is already blocked on recovery of the Williams 2002 / FAO 2010b estimates used by FAO SOFO 2012 Figure 2.\n"
        "Current forest-loss datasets such as FAO FRA 2025, OWID forest-area successors, and Global Forest Watch tree-cover loss are not methodologically comparable to the 1700-2010 historical deforestation estimates by tropical/temperate forest type.\n"
        "No extension is plotted until the original source table is recovered or a clearly commensurable successor is identified.",
    )
    side_by_side(supp_crop, book_panel, BASE / "plots/comparisons/figure_10_4_book_period_status_comparison.png", "Figure 10-4: Deforestation, 1700-2010")
    side_by_side(supp_crop, ext_panel, BASE / "plots/comparisons/figure_10_4_extended_status_comparison.png", "Figure 10-4: Deforestation, 1700-2010")

    source_comp = Image.new("RGB", (1900, 760), "white")
    draw = ImageDraw.Draw(source_comp)
    draw.text((40, 30), "Figure 10-4 source comparison", fill=(25, 25, 25), font=font(30, True))
    draw.text((40, 82), "Pinker Supplemental PDF reference", fill=(75, 75, 75), font=font(22, True))
    draw.text((990, 82), "FAO SOFO 2012 Figure 2 source graphic", fill=(75, 75, 75), font=font(22, True))
    left_img = Image.open(supp_crop).convert("RGB")
    right_img = Image.open(fao_crop).convert("RGB")
    left_img.thumbnail((900, 580), Image.Resampling.LANCZOS)
    right_img.thumbnail((850, 580), Image.Resampling.LANCZOS)
    source_comp.paste(ImageOps.expand(left_img, border=1, fill=(210, 210, 210)), (40, 125))
    source_comp.paste(ImageOps.expand(right_img, border=1, fill=(210, 210, 210)), (990, 125))
    source_comp.save(BASE / "plots/comparisons/figure_10_4_source_reference_comparison.png")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_docs() -> None:
    metadata = {
        "figure_id": FIG_ID,
        "chapter": "10",
        "title": "Deforestation, 1700-2010",
        "book_page": "Supplemental PDF page 14",
        "claim_summary": "Temperate deforestation peaked earlier and then slowed/reversed, while tropical deforestation continued through the late twentieth century.",
        "book_citation": "United Nations Food and Agriculture Organization 2012, p. 9.",
        "original_dataset": "Not recovered. FAO SOFO 2012 Figure 2 is an estimated graphic based on Williams 2002 and FAO 2010b.",
        "dataset_url": FAO_SOFO_2012_URL,
        "archive_url": "Not found in this pass; live FAO PDF and chapter PDF retained as raw sources.",
        "download_date": TODAY,
        "reproduction_status": STATUS,
        "confidence_score": 0.35,
        "visual_validation": "source_reference_captured_no_reconstruction",
        "notes": "The Supplemental PDF source line and FAO source graphic were recovered. The underlying Williams 2002 / FAO 2010b estimate table was not recovered, so no plotted reconstruction or extension was generated. Pinker's plotted values were not digitized.",
        "canonical_artifacts": {
            "original_reference": "figures/10-4/plots/comparisons/supplemental_pdf_reference_figure_10_4.png",
            "source_reference": "figures/10-4/plots/comparisons/fao_sofo_2012_source_figure_2.png",
            "book_period_status": "figures/10-4/plots/book_period/figure_10_4_book_period_source_recovery_status.png",
            "extended_status": "figures/10-4/plots/extended/figure_10_4_extended_source_recovery_status.png",
            "book_period_comparison": "figures/10-4/plots/comparisons/figure_10_4_book_period_status_comparison.png",
            "extended_comparison": "figures/10-4/plots/comparisons/figure_10_4_extended_status_comparison.png",
        },
    }
    (BASE / "metadata/metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")

    (BASE / "source_logs/source_log.md").write_text(
        f"""# Source Log: Figure 10-4

## Supplemental PDF Evidence
- Inspected `references/enlightenment_now_supplemental_graphics.pdf`, page 14.
- Title: `Deforestation, 1700-2010`.
- Source note: `United Nations Food and Agriculture Organization 2012, p. 9.`
- Visible series: `Temperate forest` and `Tropical forest`, plotted in million hectares.
- Surrounding discussion links the figure to environmental rebound and the shift from temperate to tropical forest loss.

## Source Recovery
- Downloaded FAO, *State of the World's Forests 2012*, from `{FAO_SOFO_2012_URL}` on {TODAY}.
- Downloaded the FAO Chapter 2 PDF from `{FAO_CHAPTER2_URL}` on {TODAY}.
- Located printed page 9, Figure 2: `Estimated deforestation, by type of forest and time period`.
- FAO Figure 2 source note: `Estimates based on Williams, 2002; FAO, 2010b.`
- Extracted PDF text around Figure 2. The period labels and source note are exposed, but the bar heights are not exposed as a numerical table.
- Checked likely OWID grapher slugs for `estimated-deforestation-by-type-of-forest...`; all returned 404.
- Web search located mirrors/reuses of the FAO graphic, but no underlying table.

## Blocker
The underlying numerical estimates behind FAO SOFO 2012 Figure 2 were not recovered. The figure appears to be an estimated graphic derived from Williams 2002 and FAO 2010b rather than a published table in the FAO PDF. Reconstructing it from Pinker's plotted values would violate the project rule; digitizing the FAO graphic may be a possible future validation/recovery tactic, but it is not treated here as recovered original data.

## Next Recovery Targets
- Inspect Williams, M. 2002, *Deforesting the Earth: From Prehistory to Global Crisis*, for tabular period estimates.
- Inspect FAO FRA 2010b tables and annexes for the 1990-2010 components used in Figure 2.
- Search FAO production files, chart source assets, and archived SOFO 2012 supporting files for Figure 2 data.
- If no table exists, document whether digitizing the FAO source graphic, not Pinker's chart, is acceptable for a future approximate reconstruction.
"""
    )

    (BASE / "provenance/provenance.md").write_text(
        f"""# Provenance: Figure 10-4

## Status
`{STATUS}`. Source publication and source graphic recovered; original numerical estimate table not recovered.

## Inputs Retained
- `figures/10-4/data/raw/fao_state_of_worlds_forests_2012.pdf`
- `figures/10-4/data/raw/fao_state_of_worlds_forests_2012_chapter2.pdf`
- Rendered page images in `figures/10-4/data/raw/`

## Source Chain
Pinker cites United Nations Food and Agriculture Organization 2012, p. 9. That resolves to FAO, *State of the World's Forests 2012*, printed page 9, Figure 2. FAO identifies the estimates as based on Williams 2002 and FAO 2010b.

## Reconstruction Decision
No book-period or extended data reconstruction was generated because the numerical table remains unrecovered. Status panels and source/reference comparisons are provided so a future executor can continue from the documented source chain.
"""
    )

    (BASE / "anomaly_reviews/anomaly_review.md").write_text(
        """# Anomaly Review: Figure 10-4

## Data Fidelity
- No Pinker plotted values were digitized.
- No reconstructed data table is claimed.
- The FAO source graphic is recovered, but its underlying Williams 2002 / FAO 2010b estimate table is unresolved.

## Visual Fidelity
- The Supplemental PDF reference crop is captured.
- The comparison panels are explicitly status-only and do not pretend to be a reconstructed chart.
- The FAO source graphic shows period bars, while Pinker restyles the source into two continuous lines; this transformation cannot be reproduced without recovered data.

## Extension Clarity
- No extension is plotted.
- Current forest datasets are not treated as commensurable extensions of the historical temperate/tropical deforestation estimates.

## Reviewer Challenge
- Steven Pinker might ask why the visible FAO chart was not simply digitized. The blocker is that the task requires original data recovery first, and Pinker's plotted values cannot be used.
- A data journalist would ask for the actual period values and uncertainty; these remain unrecovered.
- A peer reviewer would ask how Williams 2002 and FAO 2010b were combined. That transformation is not documented in the recovered PDF.
- A skeptical reader would notice that the panels are not line charts; captions and labels state that the figure is source-recovery blocked.

## Editorial Review Gate
- Critical issues: no false reconstruction is presented.
- Major issues: original data unrecovered; documented and reflected in status.
- Minor issues: status panels are less visually satisfying than a reconstruction, but they are clear and non-misleading.
"""
    )

    (BASE / "captions/caption.txt").write_text(
        "Figure 10-4 source recovery status. The Supplemental Graphics PDF cites FAO, State of the World's Forests 2012, p. 9; the cited FAO source graphic was recovered, but the underlying Williams 2002 / FAO 2010b estimate table was not. No Pinker plotted values were digitized, and no reconstruction or extension is claimed.\n"
    )

    (BASE / "review_checklist.md").write_text(
        """# Review Checklist: Figure 10-4

- [x] Supplemental Graphics PDF figure inspected.
- [x] Source note extracted from Supplemental PDF.
- [x] Surrounding text reviewed in Supplemental PDF text extraction.
- [x] FAO 2012 source publication located.
- [x] FAO source graphic located and captured.
- [ ] Original numerical estimate table recovered.
- [x] No Pinker plotted values digitized.
- [x] Book-period status comparison generated.
- [x] Extension absence documented.
- [x] Data fidelity reviewed.
- [x] Visual fidelity reviewed against PDF reference.
- [x] Extension clarity reviewed.
- [x] Status calibrated.
- [x] Editorial Review Gate applied.
- [x] Registry, metadata, PROJECT_STATE, review PDF, manifest, and checksums updated.
"""
    )


def update_registries() -> None:
    registry_csv = ROOT / "data/figure_registry.csv"
    rows = list(csv.DictReader(registry_csv.open()))
    for row in rows:
        if row["figure_id"] == FIG_ID:
            row.update(
                {
                    "current_status": STATUS,
                    "lifecycle_stage": "source_recovery_blocked_no_reconstruction",
                    "priority": "active_high",
                    "current_owner": "Codex",
                    "next_action": "Recover Williams 2002 / FAO 2010b estimate table behind FAO SOFO 2012 Figure 2; do not digitize Pinker values.",
                    "notes": f"Source recovery {TODAY}: Supplemental PDF source line and FAO SOFO 2012 p. 9 Figure 2 captured; underlying numerical estimates not recovered; status-only artifacts generated.",
                }
            )
    with registry_csv.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys(), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    (ROOT / "data/figure_registry.json").write_text(json.dumps(rows, indent=2) + "\n")

    metadata_csv = ROOT / "data/metadata/figure_metadata.csv"
    meta_rows = list(csv.DictReader(metadata_csv.open()))
    fieldnames = list(meta_rows[0].keys())
    meta = {
        "figure_id": FIG_ID,
        "chapter": "10",
        "title": "Deforestation, 1700-2010",
        "book_page": "Supplemental PDF page 14; Kindle not inspected in this executor session",
        "claim_summary": "Temperate deforestation peaked earlier and then slowed/reversed, while tropical deforestation continued through the late twentieth century.",
        "book_citation": "United Nations Food and Agriculture Organization 2012, p. 9.",
        "original_dataset": "Not recovered; FAO SOFO 2012 Figure 2 estimates based on Williams 2002 and FAO 2010b.",
        "dataset_url": FAO_SOFO_2012_URL,
        "archive_url": "Not recovered in this pass.",
        "download_date": TODAY,
        "reproduction_status": STATUS,
        "confidence_score": "0.35",
        "visual_validation": "source_reference_captured_no_reconstruction",
        "notes": "Source publication and graphic recovered; no data reconstruction because underlying estimate table remains unresolved.",
    }
    found = False
    for i, row in enumerate(meta_rows):
        if row["figure_id"] == FIG_ID:
            meta_rows[i] = {k: meta.get(k, row.get(k, "")) for k in fieldnames}
            found = True
            break
    if not found:
        meta_rows.append({k: meta.get(k, "") for k in fieldnames})
    with metadata_csv.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(meta_rows)


def update_project_state() -> None:
    path = ROOT / "PROJECT_STATE.md"
    text = path.read_text()
    text = text.replace("Project version: `1.14-reconstruct-figure-10-3-epa-air-trends`", "Project version: `1.15-source-recovery-figure-10-4-deforestation`")
    table_row = "| 10-4 | Deforestation, 1700-2010 | Source recovery blocked; Supplemental PDF and FAO source captured | `manual_review_needed` | Low | Supplemental PDF cites FAO 2012 p. 9; FAO SOFO 2012 Figure 2 recovered, but the underlying Williams 2002 / FAO 2010b estimate table was not found; no Pinker plotted values were digitized and no reconstruction is claimed. |"
    if "| 10-4 |" not in text:
        marker = "| 10-3 | Pollution, energy, and growth, US, 1970-2015 | Verified EPA 2016 book-period chart-data reconstruction with successor extension | `verified_reproduction` | High | EPA Our Nation's Air 2016 embedded GrowthAndEmissions chart values recovered; EPA 2025 successor extension added; PDF five-pollutant label conflicts with EPA six-pollutant source label and is documented. |"
        text = text.replace(marker, marker + "\n" + table_row)
    section = f"""
### Figure 10-4 - Deforestation, 1700-2010

Status: `manual_review_needed`

Canonical visual artifacts:

- Supplemental PDF reference: `figures/10-4/plots/comparisons/supplemental_pdf_reference_figure_10_4.png`
- FAO source reference: `figures/10-4/plots/comparisons/fao_sofo_2012_source_figure_2.png`
- Book-period status comparison: `figures/10-4/plots/comparisons/figure_10_4_book_period_status_comparison.png`
- Extended status comparison: `figures/10-4/plots/comparisons/figure_10_4_extended_status_comparison.png`

Source status: Supplemental Graphics PDF source line captured; it cites United Nations Food and Agriculture Organization 2012, p. 9. The cited source resolves to FAO *State of the World's Forests 2012*, Figure 2, with estimates based on Williams 2002 and FAO 2010b. The underlying numerical estimate table was not recovered from the FAO PDF, chapter PDF, likely OWID grapher slugs, or targeted web searches. No Pinker plotted values were digitized; status panels are not reconstructions.
"""
    marker = "\n### Figure 10-3 - Pollution, energy, and growth, US, 1970-2015\n"
    if "### Figure 10-4 - Deforestation, 1700-2010" not in text:
        text = text.replace(marker, section + marker)
    path.write_text(text)


def update_checksums() -> None:
    paths = sorted(
        p for p in BASE.rglob("*") if p.is_file() and "checksums/sha256sums.txt" not in str(p)
    )
    lines = [f"{sha256(p)}  {p.relative_to(ROOT)}" for p in paths]
    (BASE / "checksums/sha256sums.txt").write_text("\n".join(lines) + "\n")


def main() -> None:
    ensure_dirs()
    download_sources()
    supp_crop, fao_crop, _ = crop_reference_images()
    make_visuals(supp_crop, fao_crop)
    write_docs()
    update_registries()
    update_project_state()
    update_checksums()


if __name__ == "__main__":
    main()
