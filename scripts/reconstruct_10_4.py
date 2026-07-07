from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from datetime import date
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
FIG_ID = "10-4"
BASE = ROOT / "figures" / FIG_ID
TODAY = date.today().isoformat()

SUPPLEMENTAL_PDF = ROOT / "references" / "enlightenment_now_supplemental_graphics.pdf"
FAO_SOFO_2012_URL = "https://www.fao.org/4/i3010e/i3010e.pdf"
FAO_CHAPTER2_URL = "https://www.fao.org/4/i3010e/i3010e02.pdf"
FRA_2010_MAIN_URL = "https://www.fao.org/4/i1757e/i1757e.pdf"
FRA_2010_PAGE_URL = "https://www.fao.org/forest-resources-assessment/past-assessments/fra-2010/en"
FRA_2010_GLOBAL_TABLES_URL = "https://openknowledge.fao.org/bitstreams/d010c16c-632e-4c29-885f-72ee2d11ac30/download"
OWID_2013_IMAGE_URL = "https://ourworldindata.org/uploads/2013/11/estimated-deforestation-by-type-of-forest-and-time-period-pre-1700-2000-fao-20120-645x422.png"
STATUS = "manual_review_needed"


WILLIAMS_ROWS = [
    ("1700-1849", 109, 180, -289, 1.94),
    ("1850-1919", 70, 135, -205, 2.97),
    ("1920-1949", 235, 99, -334, 11.52),
    ("1950-1979", 318, 18, -336, 11.57),
    ("1980-1995", 220, 6, -226, 15.10),
]

FRA_REGION_ROWS = [
    ("Africa", 749238, 708564, 691468, 674419, -4067, -3419, -3410),
    ("Asia", 576110, 570164, 584048, 592512, -595, 2777, 1693),
    ("Europe", 989471, 998239, 1001150, 1005001, 877, 582, 770),
    ("North and Central America", 708383, 705497, 705296, 705393, -289, -40, 19),
    ("Oceania", 198744, 198381, 196745, 191384, -36, -327, -1072),
    ("South America", 946454, 904322, 882258, 864351, -4213, -4413, -3581),
    ("World", 4168399, 4085168, 4060964, 4033060, -8323, -4841, -5581),
]


def ensure_dirs() -> None:
    for part in [
        "metadata",
        "provenance",
        "source_logs",
        "search_iterations",
        "discrepancy_logs",
        "anomaly_reviews",
        "captions",
        "plots/book_period",
        "plots/extended",
        "plots/comparisons",
        "data/raw",
        "data/clean",
        "data/candidates",
        "checksums",
    ]:
        (BASE / part).mkdir(parents=True, exist_ok=True)


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def download_sources() -> None:
    downloads = [
        (FAO_SOFO_2012_URL, BASE / "data/raw/fao_state_of_worlds_forests_2012.pdf"),
        (FAO_CHAPTER2_URL, BASE / "data/raw/fao_state_of_worlds_forests_2012_chapter2.pdf"),
        (FRA_2010_MAIN_URL, BASE / "data/candidates/fao_fra_2010_main_report_i1757e.pdf"),
        (FRA_2010_GLOBAL_TABLES_URL, BASE / "data/candidates/fra2010_global_tables.xls"),
        (OWID_2013_IMAGE_URL, BASE / "data/candidates/owid_uploaded_fao_deforestation_2013.png"),
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


def write_recovered_tables() -> None:
    clean = BASE / "data/clean"
    with (clean / "figure_10_4_williams_recovered_1700_1995.csv").open("w", newline="") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow(["period", "tropical_mha", "temperate_mha", "total_net_change_mha", "annual_rate_mha_per_year", "source_status"])
        for row in WILLIAMS_ROWS:
            writer.writerow([*row, "recovered_from_Williams_table_12_2_via_accessible_snippet"])
        writer.writerow(["1996-2010", "", "", "", "", "unrecovered_FAO_2010b_period_split"])
    with (clean / "figure_10_4_fra2010_region_summary.csv").open("w", newline="") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow([
            "region",
            "forest_area_1990_1000ha",
            "forest_area_2000_1000ha",
            "forest_area_2005_1000ha",
            "forest_area_2010_1000ha",
            "annual_change_1990_2000_1000ha_per_year",
            "annual_change_2000_2005_1000ha_per_year",
            "annual_change_2005_2010_1000ha_per_year",
        ])
        writer.writerows(FRA_REGION_ROWS)


def make_partial_recovery_panel(out: Path) -> None:
    img = Image.new("RGB", (1400, 850), "white")
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, 1400, 92), fill=(42, 42, 42))
    draw.text((42, 25), "Figure 10-4: recovered source table, partial", fill="white", font=font(34, True))
    draw.text((60, 126), "Williams Table 12.2 values recovered for 1700-1995; FAO-added 1996-2010 split remains unrecovered.", fill=(35, 35, 35), font=font(22))

    left = 110
    top = 690
    chart_w = 1080
    chart_h = 470
    max_v = 360
    bar_w = 62
    gap = 88
    colors = {"Tropical": (62, 130, 92), "Temperate": (127, 102, 157)}
    draw.line((left, top - chart_h, left, top), fill=(80, 80, 80), width=2)
    draw.line((left, top, left + chart_w, top), fill=(80, 80, 80), width=2)
    for yv in [0, 100, 200, 300]:
        y = top - int(yv / max_v * chart_h)
        draw.line((left - 8, y, left + chart_w, y), fill=(225, 225, 225), width=1)
        draw.text((45, y - 10), str(yv), fill=(80, 80, 80), font=font(18))
    draw.text((35, 205), "Million hectares", fill=(80, 80, 80), font=font(18))
    x = left + 45
    for period, tropical, temperate, *_ in WILLIAMS_ROWS:
        for label, value, dx in [("Tropical", tropical, 0), ("Temperate", temperate, bar_w + 8)]:
            h = int(value / max_v * chart_h)
            draw.rectangle((x + dx, top - h, x + dx + bar_w, top), fill=colors[label])
            draw.text((x + dx + 10, top - h - 24), str(value), fill=(50, 50, 50), font=font(16, True))
        draw.text((x - 6, top + 18), period.replace("-", "-\n"), fill=(45, 45, 45), font=font(16))
        x += gap + 2 * bar_w
    draw.rectangle((x + 18, top - 28, x + 18 + 2 * bar_w + 8, top), outline=(150, 150, 150), width=2)
    draw.text((x - 8, top - 78), "1996-2010", fill=(45, 45, 45), font=font(16, True))
    draw.text((x - 20, top - 50), "unrecovered", fill=(90, 90, 90), font=font(16))

    draw.rectangle((1030, 145, 1055, 170), fill=colors["Tropical"])
    draw.text((1065, 145), "Tropical", fill=(45, 45, 45), font=font(18))
    draw.rectangle((1030, 180, 1055, 205), fill=colors["Temperate"])
    draw.text((1065, 180), "Temperate", fill=(45, 45, 45), font=font(18))
    draw.text((60, 770), "Do not read this as Pinker's continuous-line chart. It is the recovered Williams period table plus an explicit FAO 2010b blocker.", fill=(70, 70, 70), font=font(20))
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
    book_panel = BASE / "plots/book_period/figure_10_4_book_period_reconstruction.png"
    ext_panel = BASE / "plots/extended/figure_10_4_extended_source_recovery_status.png"
    make_partial_recovery_panel(book_panel)
    make_status_panel(
        ext_panel,
        "Figure 10-4: extension/status",
        "Recovered source table: Williams Table 12.2 supplies period estimates for tropical and temperate net forest change, 1700-1995.\n"
        "Unrecovered source component: FAO SOFO 2012 adds a 1996-2010 bar attributed to FAO 2010b, but the tropical/temperate split and production calculation were not found in the SOFO PDF, FRA 2010 main report, FRA global tables, FAO static assets, OWID assets, or archived pages checked here.\n"
        "No post-2010 extension is plotted. Modern FAO/GFW forest-loss series are not methodologically equivalent to the Williams period estimates or Pinker's restyled continuous lines.",
    )
    side_by_side(supp_crop, book_panel, BASE / "plots/comparisons/figure_10_4_book_period_comparison.png", "Figure 10-4: Deforestation, 1700-2010")
    side_by_side(supp_crop, ext_panel, BASE / "plots/comparisons/figure_10_4_extended_comparison.png", "Figure 10-4: Deforestation, 1700-2010")
    # Backward-compatible aliases used by earlier review packets.
    (BASE / "plots/comparisons/figure_10_4_book_period_status_comparison.png").write_bytes((BASE / "plots/comparisons/figure_10_4_book_period_comparison.png").read_bytes())
    (BASE / "plots/comparisons/figure_10_4_extended_status_comparison.png").write_bytes((BASE / "plots/comparisons/figure_10_4_extended_comparison.png").read_bytes())

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
        "original_dataset": "Partially recovered. Williams Table 12.2 recovers 1700-1995 tropical/temperate period estimates; FAO 2010b/FRA 2010 1996-2010 split remains unrecovered.",
        "dataset_url": "",
        "source_publication_url": FAO_SOFO_2012_URL,
        "source_data_url": "Not recovered; see source log for FAO FRA 2010 global tables and blocked FAO/Williams production-data search.",
        "archive_url": "Wayback CDX and OWID asset probes retained in data/candidates; no production data file recovered.",
        "download_date": TODAY,
        "reproduction_status": STATUS,
        "confidence_score": 0.55,
        "visual_validation": "partial_source_table_recovered_1996_2010_blocked",
        "notes": "Williams period values for 1700-1995 were recovered from an accessible book/snippet source; the FAO 2010b/FRA 2010 1996-2010 tropical/temperate split behind SOFO 2012 Figure 2 remains unrecovered. Pinker's plotted values were not digitized.",
        "canonical_artifacts": {
            "original_reference": "figures/10-4/plots/comparisons/supplemental_pdf_reference_figure_10_4.png",
            "source_reference": "figures/10-4/plots/comparisons/fao_sofo_2012_source_figure_2.png",
            "book_period_reconstruction": "figures/10-4/plots/book_period/figure_10_4_book_period_reconstruction.png",
            "extended_status": "figures/10-4/plots/extended/figure_10_4_extended_source_recovery_status.png",
            "book_period_comparison": "figures/10-4/plots/comparisons/figure_10_4_book_period_comparison.png",
            "extended_comparison": "figures/10-4/plots/comparisons/figure_10_4_extended_comparison.png",
            "recovered_table": "figures/10-4/data/clean/figure_10_4_williams_recovered_1700_1995.csv",
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
- Exact FAO 2010b citation identified in SOFO 2012 references: FAO. 2010b. *Global Forest Resources Assessment 2010 - main report*. FAO Forestry Paper No. 163. Rome. `{FRA_2010_MAIN_URL}`.
- Downloaded the FRA 2010 main report and official FRA 2010 Global Tables from the current FAO FRA 2010 page `{FRA_2010_PAGE_URL}`. The global tables expose 1990, 2000, 2005, and 2010 forest-area and annual net-change values by country/region, but not the SOFO Figure 2 tropical/temperate 1996-2010 production split.
- Recovered Williams Table 12.2 values for 1700-1995 from accessible book/snippet text and corroborating reuse: `figures/10-4/data/clean/figure_10_4_williams_recovered_1700_1995.csv`.
- Downloaded the OWID-hosted 2013 FAO image asset from `{OWID_2013_IMAGE_URL}`. It is a reused image, not a table.

## Blocker
The Williams component is recovered through 1995, but the FAO 2010b/FRA 2010 calculation that turns FRA data into the 1996-2010 tropical/temperate Figure 2 bar was not recovered. The live and archived FAO materials checked do not provide a production spreadsheet or a table matching SOFO Figure 2. Reconstructing from Pinker's plotted values remains prohibited. Digitizing the FAO source graphic, not Pinker's chart, would be an explicitly approximate secondary reconstruction only; it is not treated here as recovered original data.

## Search and Access Attempts
- Query: `"Estimated deforestation, by type of forest and time period" data`; URL checked: FAO SOFO PDF and search results; access date: {TODAY}; result: source graphic/PDF only, non-tabular.
- Query: `"State of the World's Forests 2012" "Figure 2" "Estimated deforestation"`; URL checked: `{FAO_SOFO_2012_URL}` and `{FAO_CHAPTER2_URL}`; access date: {TODAY}; result: source figure recovered, no values table.
- Query: `"FAO 2010b" "Global Forest Resources Assessment 2010" "main report"`; URL checked: `{FRA_2010_MAIN_URL}` and `{FRA_2010_PAGE_URL}`; access date: {TODAY}; result: exact citation and official global tables recovered, but only FRA 1990-2010 forest-area/net-change tables.
- Query: `"Deforesting the Earth" "Table 12.2"`; URLs checked: University of Chicago Press page, WorldCat, Google/search snippets, `https://dokumen.pub/deforesting-the-earth-from-prehistory-to-global-crisis-an-abridgment-9780226899053.html`; access date: {TODAY}; result: publisher/library pages non-tabular, accessible snippet/table recovers Williams 1700-1995 values; not a FAO 1996-2010 table.
- Query: `"Deforesting the Earth" "temperate forest" "tropical forest" "1700" "1849"`; URLs checked: Google/search snippets, Stop Fossil Fuels reuse page, ResearchGate dissertation snippet; access date: {TODAY}; result: corroborates Williams table/reuse, but secondary/reused or snippet access.
- Query: `site:ourworldindata.org/uploads "estimated-deforestation-by-type-of-forest-and-time-period"`; URL checked: `{OWID_2013_IMAGE_URL}`; access date: {TODAY}; result: image asset only, no data file.
- Query: `site:fao.org/forestry "Estimated deforestation" "xls"` and Wayback CDX probes for `foris.fao.org/static/data/fra2010/*`; access date: {TODAY}; result: FRA global tables and maps/reports found, no SOFO Figure 2 production asset or spreadsheet.

## Next Recovery Targets
- Inspect a full authorized copy of Williams, M. 2002, *Deforesting the Earth: From Prehistory to Global Crisis*, to confirm the Table 12.2 values against the original edition rather than accessible snippets/reuses.
- Inspect additional FAO FRA 2010b annexes, FORIS exports, or staff production files for the 1996-2010 components used in Figure 2.
- Search FAO production files, chart source assets, and archived SOFO 2012 supporting files for Figure 2 data.
- If no table exists, document whether digitizing the FAO source graphic, not Pinker's chart, is acceptable for a future approximate reconstruction.
"""
    )

    (BASE / "provenance/provenance.md").write_text(
        f"""# Provenance: Figure 10-4

## Status
`{STATUS}`. Source publication and graphic recovered; Williams 1700-1995 table values recovered; FAO 2010b/FRA 2010 1996-2010 tropical/temperate split not recovered.

## Inputs Retained
- `figures/10-4/data/raw/fao_state_of_worlds_forests_2012.pdf`
- `figures/10-4/data/raw/fao_state_of_worlds_forests_2012_chapter2.pdf`
- `figures/10-4/data/candidates/fao_fra_2010_main_report_i1757e.pdf`
- `figures/10-4/data/candidates/fra2010_global_tables.xls`
- `figures/10-4/data/candidates/owid_uploaded_fao_deforestation_2013.png`
- `figures/10-4/data/clean/figure_10_4_williams_recovered_1700_1995.csv`
- Rendered page images in `figures/10-4/data/raw/`

## Source Chain
Pinker cites United Nations Food and Agriculture Organization 2012, p. 9. That resolves to FAO, *State of the World's Forests 2012*, printed page 9, Figure 2. FAO identifies the estimates as based on Williams 2002 and FAO 2010b. The SOFO bibliography identifies FAO 2010b as *Global Forest Resources Assessment 2010 - main report*, FAO Forestry Paper No. 163.

## Reconstruction Decision
A partial book-period source reconstruction is generated from Williams Table 12.2 for 1700-1995. No 1996-2010 value or post-2010 extension is plotted as recovered data because the FAO 2010b split remains unresolved.
"""
    )

    (BASE / "anomaly_reviews/anomaly_review.md").write_text(
        """# Anomaly Review: Figure 10-4

## Data Fidelity
- No Pinker plotted values were digitized.
- Williams 1700-1995 period values are recovered and written as a clean table.
- The FAO source graphic is recovered, but the FAO 2010b 1996-2010 tropical/temperate split is unresolved.

## Visual Fidelity
- The Supplemental PDF reference crop is captured.
- The comparison panels explicitly distinguish the partial Williams-source reconstruction from the unresolved FAO 2010b final-period split.
- The FAO source graphic shows period bars, while Pinker restyles the source into two continuous lines; the interpolation/smoothing implied by Pinker's rendering is not documented in SOFO 2012.

## Extension Clarity
- No extension is plotted.
- Current forest datasets are not treated as commensurable extensions of the historical temperate/tropical deforestation estimates.

## Reviewer Challenge
- Steven Pinker might ask why the visible FAO chart was not simply digitized. The blocker is that the task requires original data recovery first, and Pinker's plotted values cannot be used.
- A data journalist would ask for the final 1996-2010 period values and uncertainty; those remain unrecovered.
- A peer reviewer would ask how Williams 2002 and FAO 2010b were combined. That transformation is not documented in the recovered PDF.
- A skeptical reader would notice that the panels are not line charts; captions and labels state that the figure is source-recovery blocked.

## Editorial Review Gate
- Critical issues: no false reconstruction is presented.
- Major issues: original data unrecovered; documented and reflected in status.
- Minor issues: status panels are less visually satisfying than a reconstruction, but they are clear and non-misleading.
"""
    )

    (BASE / "discrepancy_logs/discrepancy_log.md").write_text(
        f"""# Discrepancy Log: Figure 10-4

## Rendering Mismatch
Pinker renders `Deforestation, 1700-2010` as two continuous lines for temperate and tropical forest. The cited FAO source, SOFO 2012 Figure 2, is a period-bar graphic with uneven bins: pre-1700, 1700-1849, 1850-1919, 1920-1949, 1950-1979, 1980-1995, and 1996-2010.

## Data Mismatch
Williams Table 12.2 directly supports the 1700-1995 period values for tropical and temperate net forest change. It does not provide a 1996-2010 value. FAO 2010b/FRA 2010 provides 1990, 2000, 2005, and 2010 forest-area/net-change tables, but the reviewed materials do not disclose the tropical/temperate split or gross/net transformation used for SOFO Figure 2's final bar.

## Remediation Decision
The standard comparison image shows recovered Williams period bars plus an explicit 1996-2010 blocker. It intentionally does not imitate Pinker's continuous-line rendering, because doing so would require undocumented interpolation and/or digitization of Pinker's plotted values.
"""
    )

    (BASE / "search_iterations/search_iterations.md").write_text(
        f"""# Search Iterations: Figure 10-4

Access date for this remediation pass: {TODAY}.

| Query / route | URL(s) checked | Result |
|---|---|---|
| `"Estimated deforestation, by type of forest and time period" data` | `{FAO_SOFO_2012_URL}`; `{FAO_CHAPTER2_URL}` | FAO source graphic recovered; no numerical table. |
| SOFO references for `FAO, 2010b` | `{FAO_SOFO_2012_URL}` | Exact citation identified as FRA 2010 main report, FAO Forestry Paper No. 163. |
| FRA 2010 official page and Global Tables | `{FRA_2010_PAGE_URL}`; `{FRA_2010_GLOBAL_TABLES_URL}` | Official XLS recovered; contains 1990/2000/2005/2010 country-region forest area and net annual change, not SOFO Figure 2 production values. |
| `"Deforesting the Earth" "Table 12.2"` | University of Chicago Press, WorldCat, Google/search snippets, Dokumen preview | Williams 1700-1995 values recovered from accessible snippet/preview; publisher/library pages are descriptive or require purchase/library access. |
| Internet Archive / Wayback FAO static data | `foris.fao.org/static/data/fra2010/*`; `www.fao.org/forestry/fra/2560/en/*` | FRA global tables/maps/reports found; no SOFO 2012 Figure 2 data asset. |
| OWID asset search | `{OWID_2013_IMAGE_URL}`; Wayback CDX for matching OWID filenames | Image asset recovered; no CSV/grapher data found. |
| Reuse/citation searches | Stop Fossil Fuels, ResearchGate, WEF, Mongabay/worldrainforests | Mostly image reuse or secondary snippets; useful corroboration, not original FAO production data. |
"""
    )

    (BASE / "captions/caption.txt").write_text(
        "Figure 10-4 source recovery status. Williams Table 12.2 values for 1700-1995 were recovered, but the FAO 2010b/FRA 2010 1996-2010 tropical/temperate split behind SOFO 2012 Figure 2 remains unrecovered. No Pinker plotted values were digitized.\n"
    )

    (BASE / "review_checklist.md").write_text(
        """# Review Checklist: Figure 10-4

- [x] Supplemental Graphics PDF figure inspected.
- [x] Source note extracted from Supplemental PDF.
- [x] Surrounding text reviewed in Supplemental PDF text extraction.
- [x] FAO 2012 source publication located.
- [x] FAO source graphic located and captured.
- [x] Williams 1700-1995 numerical table recovered.
- [ ] FAO 2010b/FRA 2010 1996-2010 tropical/temperate split recovered.
- [x] No Pinker plotted values digitized.
- [x] Book-period status comparison generated.
- [x] Extension absence documented.
- [x] Pinker line vs FAO period-bar discrepancy logged.
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
                    "lifecycle_stage": "partial_source_recovery_final_period_blocked",
                    "priority": "active_high",
                    "current_owner": "Codex",
                    "next_action": "Recover FAO 2010b/FRA 2010 production calculation for the 1996-2010 tropical/temperate split behind SOFO 2012 Figure 2; do not digitize Pinker values.",
                    "notes": f"Source recovery {TODAY}: Williams Table 12.2 values recovered for 1700-1995; FAO SOFO 2012 p. 9 Figure 2 and FRA 2010 sources captured; 1996-2010 split remains unresolved.",
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
        "original_dataset": "Partially recovered: Williams Table 12.2 values for 1700-1995 recovered; FAO 2010b/FRA 2010 1996-2010 split unresolved.",
        "dataset_url": "",
        "archive_url": "No original production data archive recovered; FAO/Wayback/OWID probes documented in source log.",
        "download_date": TODAY,
        "reproduction_status": STATUS,
        "confidence_score": "0.55",
        "visual_validation": "partial_source_table_recovered_1996_2010_blocked",
        "notes": "Williams source table recovered for 1700-1995; FAO 2010b final-period split and Pinker's line conversion remain unresolved.",
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
    table_row = "| 10-4 | Deforestation, 1700-2010 | Partial source recovery: Williams 1700-1995 recovered; FAO 2010b final split blocked | `manual_review_needed` | Medium-low | Supplemental PDF cites FAO 2012 p. 9; FAO SOFO 2012 Figure 2 recovered; Williams Table 12.2 values recovered for 1700-1995; FAO 2010b/FRA 2010 1996-2010 tropical/temperate split and Pinker's line conversion remain unresolved. |"
    lines = text.splitlines()
    replaced = False
    for i, line in enumerate(lines):
        if line.startswith("| 10-4 |"):
            lines[i] = table_row
            replaced = True
            break
    text = "\n".join(lines) + "\n"
    if not replaced:
        marker = "| 10-3 | Pollution, energy, and growth, US, 1970-2015 | Verified EPA 2016 book-period chart-data reconstruction with successor extension | `verified_reproduction` | High | EPA Our Nation's Air 2016 embedded GrowthAndEmissions chart values recovered; EPA 2025 successor extension added; PDF five-pollutant label conflicts with EPA six-pollutant source label and is documented. |"
        text = text.replace(marker, marker + "\n" + table_row)
    section = f"""
### Figure 10-4 - Deforestation, 1700-2010

Status: `manual_review_needed`

Canonical visual artifacts:

- Supplemental PDF reference: `figures/10-4/plots/comparisons/supplemental_pdf_reference_figure_10_4.png`
- FAO source reference: `figures/10-4/plots/comparisons/fao_sofo_2012_source_figure_2.png`
- Book-period comparison: `figures/10-4/plots/comparisons/figure_10_4_book_period_comparison.png`
- Extended/status comparison: `figures/10-4/plots/comparisons/figure_10_4_extended_comparison.png`
- Recovered Williams table: `figures/10-4/data/clean/figure_10_4_williams_recovered_1700_1995.csv`

Source status: Supplemental Graphics PDF source line captured; it cites United Nations Food and Agriculture Organization 2012, p. 9. The cited source resolves to FAO *State of the World's Forests 2012*, Figure 2, with estimates based on Williams 2002 and FAO 2010b. Williams Table 12.2 values for 1700-1995 were recovered. The FAO 2010b citation resolves to *Global Forest Resources Assessment 2010 - main report*, but the FRA main report/global tables do not expose the 1996-2010 tropical/temperate split used in SOFO Figure 2. No Pinker plotted values were digitized.
"""
    marker = "\n### Figure 10-3 - Pollution, energy, and growth, US, 1970-2015\n"
    start = text.find("### Figure 10-4 - Deforestation, 1700-2010")
    if start != -1:
        next_section = text.find("\n### Figure ", start + 1)
        if next_section != -1:
            text = text[:start] + section.strip() + "\n" + text[next_section:]
        else:
            text = text[:start] + section.strip() + "\n"
    else:
        text = text.replace(marker, section + marker)
    path.write_text(text)


def update_checksums() -> None:
    paths = sorted(
        p for p in BASE.rglob("*") if p.is_file() and "checksums/sha256sums.txt" not in str(p)
    )
    lines = [f"{sha256(p)}  {p.relative_to(ROOT)}" for p in paths]
    (BASE / "checksums/sha256sums.txt").write_text("\n".join(lines) + "\n")


def update_review_packet() -> None:
    manifest_path = ROOT / "output/pdf/recreated_figures_review_scroll.manifest.json"
    if not manifest_path.exists():
        return
    manifest = json.loads(manifest_path.read_text())
    items = [item for item in manifest["items"] if item["figure_id"] != FIG_ID]
    img_path = "figures/10-4/plots/comparisons/figure_10_4_extended_comparison.png"
    items.append(
        {
            "figure_id": FIG_ID,
            "title": "Deforestation, 1700-2010",
            "status": STATUS,
            "root": "base_track_d_current",
            "path": img_path,
            "selected_image": Path(img_path).name,
            "notes": "Williams Table 12.2 recovered for 1700-1995; FAO 2010b/FRA 2010 1996-2010 tropical/temperate split remains blocked; no Pinker plotted values digitized.",
            "image_size": list(Image.open(ROOT / img_path).size),
        }
    )
    items.sort(key=lambda x: [int(part) for part in x["figure_id"].split("-")])
    manifest["count"] = len(items)
    manifest["items"] = items
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")

    pdf_path = ROOT / "output/pdf/recreated_figures_review_scroll.pdf"
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(pdf_path), pagesize=letter)
    width, height = letter
    c.setFont("Helvetica-Bold", 14)
    c.drawString(36, height - 36, "Pinker Charts Review Packet")
    c.setFont("Helvetica", 9)
    c.drawString(36, height - 52, f"Generated {TODAY}; manifest count: {len(items)}")
    for item in items:
        p = ROOT / item["path"]
        if not p.exists():
            continue
        c.showPage()
        c.setFont("Helvetica-Bold", 12)
        c.drawString(36, height - 36, f"{item['figure_id']} - {item['title']} [{item['status']}]")
        img = Image.open(p).convert("RGB")
        iw, ih = img.size
        max_w = width - 72
        max_h = height - 104
        scale = min(max_w / iw, max_h / ih)
        draw_w = iw * scale
        draw_h = ih * scale
        c.drawImage(ImageReader(img), 36, height - 64 - draw_h, width=draw_w, height=draw_h)
    c.save()


def main() -> None:
    ensure_dirs()
    download_sources()
    write_recovered_tables()
    supp_crop, fao_crop, _ = crop_reference_images()
    make_visuals(supp_crop, fao_crop)
    write_docs()
    update_registries()
    update_project_state()
    update_review_packet()
    update_checksums()


if __name__ == "__main__":
    main()
