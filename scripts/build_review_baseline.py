"""Build original-pixel comparisons without modifying underlying data or plots.

Reference identities and hashes must match the PDF index. Source-only packages
are excluded. Generated pages are an audit baseline, never automatic acceptance.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import textwrap

from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageOps

from project_state import ROOT, dumps, file_record, read_records, safe_path, sha


def font(size):
    for name in ["DejaVuSans.ttf", "/System/Library/Fonts/Supplemental/Arial.ttf"]:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            pass
    return ImageFont.load_default(size=size)


def trimmed(path, viewport=None):
    with Image.open(path) as source:
        image = source.convert("RGB")
    if viewport is not None:
        x0, y0, x1, y1 = viewport
        if not (0 <= x0 < x1 <= image.width and 0 <= y0 < y1 <= image.height):
            raise ValueError(f"Invalid comparison viewport: {viewport}")
        image = image.crop(viewport)
    difference = ImageChops.difference(image, Image.new("RGB", image.size, "white"))
    box = difference.point(lambda v: 255 if v > 30 else 0).getbbox()
    if not box:
        raise ValueError(f"Blank image: {path}")
    return ImageOps.expand(image.crop(box), border=12, fill="white")


def render_comparison(reference, plot, output, title, right_label, notes, viewport=None):
    width, panel, margin, gap = 2440, 1160, 40, 40
    images = [trimmed(reference), trimmed(plot, viewport)]
    fitted = [ImageOps.contain(im, (panel, 1100), Image.Resampling.LANCZOS) for im in images]
    panel_height = max(im.height for im in fitted)
    note_lines = textwrap.wrap(notes, width=166)
    canvas = Image.new("RGB", (width, 130 + panel_height + 70 + len(note_lines) * 27), "white")
    draw = ImageDraw.Draw(canvas)
    draw.text((margin, 20), title, font=font(30), fill="black")
    for i, (im, label) in enumerate(zip(fitted, ["Original: supplied Supplemental Graphics PDF", right_label])):
        x = margin + i * (panel + gap)
        draw.text((x, 77), label, font=font(23), fill="#333333")
        canvas.paste(im, (x + (panel - im.width)//2, 125))
    draw.line((margin, 145 + panel_height, width-margin, 145 + panel_height), fill="#cccccc", width=2)
    for n, line in enumerate(note_lines):
        draw.text((margin, 164 + panel_height + n*27), line, font=font(21), fill="#333333")
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output)


def eligible(record):
    return record["artifact_kind"] == "reconstruction" and "book_period_reconstruction" in record["artifacts"]


def build(root=ROOT, figures=None, update=False):
    records = read_records(root)
    index = json.loads((root / "references/figure_index.json").read_text())
    refs = {r["figure_id"]: r for r in index["items"]}
    entries, excluded = [], []
    for record in records:
        fid = record["figure_id"]
        if figures and fid not in figures:
            continue
        if not eligible(record):
            excluded.append({"figure_id": fid, "reason": record["artifact_kind"]})
            continue
        ref = refs[fid]
        if ref["identity_validation"] != "ocr_id_confirmed":
            raise ValueError(f"Reference identity unconfirmed: {fid}")
        reference = safe_path(root, ref["path"])
        if sha(reference) != ref["sha256"]:
            raise ValueError(f"Changed reference: {fid}")
        comparisons = []
        changed = record["artifacts"].get("original_reference") != {k: ref[k] for k in ["path", "sha256"]}
        for mode in ["book_period", "extended"]:
            artifact = record["artifacts"].get(mode + "_reconstruction")
            if not artifact:
                continue
            plot = safe_path(root, artifact["path"])
            if sha(plot) != artifact["sha256"]:
                raise ValueError(f"Changed plot: {fid} {mode}; update its audited record first")
            label = "Book-period reconstruction" if mode == "book_period" else "Extension candidate: methodology review pending"
            extension = record.get("extension", {})
            if mode == "extended" and extension.get("status") in {"same_source", "comparable_successor"}:
                label = "Extension: " + extension.get("label", extension["status"].replace("_", " "))
            if mode == "extended" and extension.get("status") == "not_plotted":
                label = "No comparable extension plotted; book-period result shown"
            caption = record["artifacts"].get("caption")
            notes = safe_path(root, caption["path"]).read_text().strip() if caption else "Caption missing; publication review blocked."
            notes = f"Scientific status: {record['scientific_status']}. Audit baseline, not publication approval. " + notes
            path = f"figures/{fid}/plots/comparisons/figure_{fid.replace('-', '_')}_{mode}_review.png"
            viewport = record.get("comparison_viewports", {}).get(mode)
            render_comparison(reference, plot, root/path, f"Figure {fid}: {record['title']}", label, notes, viewport)
            generated = file_record(root, path)
            comparisons.append({"mode": mode, **generated, "reference": {"path": ref["path"], "sha256": ref["sha256"]}, "reconstruction": artifact, "display_viewport": viewport})
            if update:
                changed |= record["artifacts"].get(mode + "_comparison") != generated
                record["artifacts"][mode + "_comparison"] = generated
        entries.append({"figure_id": fid, "scientific_status": record["scientific_status"], "comparisons": comparisons})
        if update:
            if changed:
                record["visual_review"].update(status="pending", reference_basis="original", inspected_artifacts=[])
                if record.get("publication_status") == "ready":
                    record["publication_status"] = "not_reviewed"
            (root/f"figures/{fid}/figure.json").write_text(dumps(record))
    manifest = {"schema_version": 1, "baseline_commit": subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip(),
                "notice": "Unaccepted visual audit baseline; input/output hashes identify working-tree artifacts beyond baseline_commit.",
                "figure_count": len(entries), "comparison_count": sum(len(e["comparisons"]) for e in entries), "figures": entries, "excluded": excluded}
    output = root / "reports/review_baseline"
    output.mkdir(parents=True, exist_ok=True)
    name = "manifest.json" if not figures else "manifest_" + "_".join(figures) + ".json"
    (output / name).write_text(dumps(manifest))
    print(json.dumps({k: manifest[k] for k in ["figure_count", "comparison_count"]}))
    return manifest


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--figure", action="append")
    parser.add_argument("--update-records", action="store_true")
    args = parser.parse_args()
    build(figures=args.figure, update=args.update_records)
