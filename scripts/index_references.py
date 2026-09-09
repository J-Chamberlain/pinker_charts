"""Render and identify original PDF figures from visible pixels, not hidden text.

The supplied 39-page PDF has two figure panels per page after its cover,
except page 28 (Figure 15-7). OCR confirms every expected ID before a crop
can be adopted. No plotted values are extracted as reconstruction data.
"""
from concurrent.futures import ThreadPoolExecutor
import csv
import hashlib
import json
from pathlib import Path
import re
import subprocess
import argparse

from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "references/enlightenment_now_supplemental_graphics.pdf"


def panel_split(image):
    """Choose the widest visible white gutter near the center, not a chart edge."""
    gray = image.convert("L")
    start, end = int(image.height * .4), int(image.height * .6)
    runs, first = [], None
    for y in range(start, end):
        blank = gray.crop((0, y, image.width, y + 1)).getextrema()[0] > 220
        if blank and first is None:
            first = y
        elif not blank and first is not None:
            runs.append((first, y))
            first = None
    if first is not None:
        runs.append((first, end))
    if not runs:
        raise ValueError("No white gutter; panel split requires manual review")
    a, b = max(runs, key=lambda r: r[1] - r[0])
    if b-a < 8:
        raise ValueError("Ambiguous panel gutter; manual review required")
    return (a+b)//2


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def visible_caption(text: str, expected: str) -> tuple[str, str, str]:
    matches = list(re.finditer(r"\bFigure\s+(\d+)\s*[-\u2013\u2014]\s*(\d+)\s*[:.;]", text, re.I))
    ids = [f"{m[1]}-{m[2]}" for m in matches]
    if ids != [expected]:
        return "identity_unconfirmed", "", ""
    tail = text[matches[0].start():].strip()
    parts = re.split(r"\bSources?\s*:", tail, maxsplit=1, flags=re.I)
    title = " ".join(parts[0].split())
    source = " ".join(parts[1].split()) if len(parts) == 2 else ""
    # Persist only caption/source metadata, never page prose or digitized series.
    return "ocr_id_confirmed", title[:450], source[:1800]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--update-records", action="store_true")
    args = parser.parse_args()
    rows = list(csv.DictReader((ROOT / "data/figure_registry.csv").open()))
    expected = iter(rows)
    panels = []
    for page in range(2, 40):
        for panel in range(1 if page == 28 else 2):
            panels.append((page, panel, 1 if page == 28 else 2, next(expected)))
    if next(expected, None) is not None:
        raise ValueError("PDF panel count does not equal registry count")
    temp = ROOT / "tmp/pdfs/reference_index"
    temp.mkdir(parents=True, exist_ok=True)
    output = ROOT / "references/figures"
    output.mkdir(parents=True, exist_ok=True)
    pdf_sha = digest(PDF)

    def render_page(page):
        image = temp / f"page_{page}.png"
        subprocess.run(["pdftoppm", "-f", str(page), "-l", str(page), "-singlefile", "-scale-to", "2400", "-png", str(PDF), str(image.with_suffix(""))], check=True, capture_output=True, timeout=60)
        return image

    with ThreadPoolExecutor(max_workers=3) as pool:
        list(pool.map(render_page, range(2, 40)))

    def inspect_panel(item):
        page, panel, count, row = item
        fid = row["figure_id"]
        image = Image.open(temp / f"page_{page}.png").convert("RGB")
        split = panel_split(image) if count == 2 else image.height
        bounds = (0, 0 if panel == 0 else split, image.width, split if panel == 0 else image.height)
        crop = image.crop(bounds)
        difference = ImageChops.difference(crop, Image.new("RGB", crop.size, "white"))
        box = difference.point(lambda v: 255 if v > 35 else 0).getbbox()
        if box:
            box = (max(0, box[0] - 12), max(0, box[1] - 12), min(crop.width, box[2] + 12), min(crop.height, box[3] + 12))
            crop = crop.crop(box)
            bounds = (bounds[0] + box[0], bounds[1] + box[1], bounds[0] + box[2], bounds[1] + box[3])
        path = output / f"figure_{fid.replace('-', '_')}.png"
        crop.save(path)
        text = subprocess.check_output(["tesseract", str(path), "stdout", "--psm", "11"], stderr=subprocess.DEVNULL, text=True, timeout=60)
        status, title, source = visible_caption(text, fid)
        record = {"figure_id": fid, "registry_title": row["title"], "pdf_path": str(PDF.relative_to(ROOT)),
                  "pdf_sha256": pdf_sha, "pdf_page": page, "panel": panel + 1,
                  "render_dimensions": list(image.size), "crop_bounds_pixels": list(bounds),
                  "crop_bounds_pdf_points": [round(bounds[0]*441/image.width, 3), round(bounds[1]*666/image.height, 3), round(bounds[2]*441/image.width, 3), round(bounds[3]*666/image.height, 3)],
                  "path": str(path.relative_to(ROOT)), "sha256": digest(path),
                  "identity_validation": status, "caption_ocr": title, "source_note_ocr": source,
                  "source_note_validation": "machine_extracted_pending_source_review",
                  "visual_review": "pending_full_resolution_review"}
        if status != "ocr_id_confirmed":
            # Keep failed OCR only as a temporary diagnostic for manual inspection.
            (temp / f"figure_{fid}_ocr.txt").write_text(text)
        print(f"Figure {fid}: {status}", flush=True)
        return record

    with ThreadPoolExecutor(max_workers=3) as pool:
        records = list(pool.map(inspect_panel, panels))
    index = {"schema_version": 1, "source_pdf_sha256": pdf_sha, "count": len(records),
             "method": "Poppler render of actual visible page; panel split then whitespace trim; OCR confirms caption ID. No plotted values are data.",
             "renderer": subprocess.check_output(["pdftoppm", "-v"], stderr=subprocess.STDOUT, text=True).splitlines()[0],
             "ocr": subprocess.check_output(["tesseract", "--version"], text=True).splitlines()[0],
             "items": records}
    (ROOT / "references/figure_index.json").write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n")
    if args.update_records:
        for reference in records:
            if reference["identity_validation"] != "ocr_id_confirmed":
                continue
            path = ROOT / "figures" / reference["figure_id"] / "figure.json"
            figure = json.loads(path.read_text())
            artifact = {k: reference[k] for k in ["path", "sha256"]}
            if figure["artifacts"].get("original_reference") != artifact:
                figure["visual_review"].update(status="pending", reference_basis="original", inspected_artifacts=[])
                if figure.get("publication_status") == "ready":
                    figure["publication_status"] = "not_reviewed"
            figure["artifacts"]["original_reference"] = artifact
            figure["reference"] = reference
            # PDF page and printed book page are distinct coordinates.
            path.write_text(json.dumps(figure, indent=2, ensure_ascii=False) + "\n")
    missing = [r["figure_id"] for r in records if r["identity_validation"] != "ocr_id_confirmed"]
    print(json.dumps({"figures": len(records), "identity_unconfirmed": missing}))
    raise SystemExit(bool(missing))


if __name__ == "__main__":
    main()
