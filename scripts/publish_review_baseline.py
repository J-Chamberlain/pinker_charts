"""Package hash-verified comparison pages into a local gallery and review PDF."""
import html
import json
import argparse
import subprocess
from pathlib import Path

from PIL import Image
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.utils import ImageReader

from project_state import ROOT, dumps, safe_path, sha, read_records


def collect_existing(root=ROOT):
    """Refresh the gallery without regenerating already inspected comparisons."""
    entries, excluded = [], []
    for record in read_records(root):
        if record["artifact_kind"] != "reconstruction":
            excluded.append({"figure_id": record["figure_id"], "reason": record["artifact_kind"]})
            continue
        artifacts = record["artifacts"]
        comparisons = []
        for mode in ["book_period", "extended"]:
            comparison = artifacts.get(mode + "_comparison")
            reconstruction = artifacts.get(mode + "_reconstruction")
            if not comparison or not reconstruction:
                continue
            reference = artifacts["original_reference"]
            for artifact in [comparison, reconstruction, reference]:
                if sha(safe_path(root, artifact["path"])) != artifact["sha256"]:
                    raise ValueError(f"Unreviewed artifact change: {artifact['path']}")
            comparisons.append({"mode": mode, **comparison, "reference": reference,
                                "reconstruction": reconstruction,
                                "display_viewport": record.get("comparison_viewports", {}).get(mode)})
        if comparisons:
            entries.append({"figure_id": record["figure_id"],
                            "scientific_status": record["scientific_status"], "comparisons": comparisons})
    return {"schema_version": 1,
            "baseline_commit": subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip(),
            "notice": "Existing hash-verified comparisons; not publication approval. Missing extensions omitted, not fabricated.",
            "figure_count": len(entries), "comparison_count": sum(len(e["comparisons"]) for e in entries),
            "figures": entries, "excluded": excluded}


def main(refresh_manifest=False):
    source = ROOT / "reports/review_baseline/manifest.json"
    if refresh_manifest:
        source.write_text(dumps(collect_existing()))
    manifest = json.loads(source.read_text())
    output = ROOT / "output/pdf"
    output.mkdir(parents=True, exist_ok=True)
    pdf_path = output / "recreated_figures_review_scroll.pdf"
    canvas = Canvas(str(pdf_path), pageCompression=1, invariant=1)
    canvas.setTitle("Pinker Charts: consolidated audit baseline (not publication approval)")
    pages, sections = [], []
    for entry in manifest["figures"]:
        fid = entry["figure_id"]
        section = [f'<section id="figure-{fid}"><h2>Figure {fid}</h2><p>{html.escape(entry["scientific_status"])}</p>']
        for comparison in entry["comparisons"]:
            path = safe_path(ROOT, comparison["path"])
            if sha(path) != comparison["sha256"]:
                raise ValueError(f"Comparison hash mismatch: {path}")
            with Image.open(path) as image:
                width, height = image.size
            scale = 1080 / width
            page_h = height * scale + 30
            canvas.setPageSize((1080, page_h))
            canvas.drawImage(ImageReader(str(path)), 0, 30, width=1080, height=height*scale)
            canvas.setFont("Helvetica", 8)
            canvas.drawString(18, 12, f"Audit baseline | Figure {fid} | {comparison['mode']} | page {len(pages)+1}")
            canvas.showPage()
            pages.append({"page": len(pages)+1, "figure_id": fid, **comparison})
            link = "../../" + comparison["path"]
            section.append(f'<h3>{comparison["mode"].replace("_", " ").title()}</h3><a href="{html.escape(link)}"><img src="{html.escape(link)}" alt="Figure {fid} {comparison["mode"]} original and recreation" loading="lazy"></a>')
        sections.append("\n".join(section) + "</section>")
    canvas.save()
    pdf_manifest = {**manifest, "pdf_path": str(pdf_path.relative_to(ROOT)), "pdf_sha256": sha(pdf_path), "page_count": len(pages), "pages": pages}
    (output / "recreated_figures_review_scroll.manifest.json").write_text(dumps(pdf_manifest))
    nav = " | ".join(f'<a href="#figure-{e["figure_id"]}">{e["figure_id"]}</a>' for e in manifest["figures"])
    document = '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Pinker Charts audit baseline</title><style>body{font:16px system-ui;margin:24px;color:#222;background:#fff}h1{font-size:28px}h2{font-size:24px}h3{font-size:18px}nav{line-height:2}section{border-top:1px solid #ccc;margin-top:36px;padding-top:12px}img{width:100%;height:auto;display:block}a{color:#096663}p{max-width:85ch}</style><h1>Pinker Charts: consolidated visual audit</h1><p>Actual supplied PDF references beside preserved reconstructions. This is an unaccepted audit baseline, not publication approval. Source-only, diagnostic, and untouched packages are excluded. Extension candidates still require methodological review. Reference material is for research review; no redistribution clearance is asserted.</p><nav>' + nav + '</nav>' + "\n".join(sections) + '</html>'
    (ROOT / "reports/review_baseline/index.html").write_text(document)
    print(dumps({"figures": len(manifest["figures"]), "pages": len(pages), "pdf": str(pdf_path)}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh-manifest", action="store_true",
                        help="Use current canonical comparison paths/hashes; do not regenerate images")
    main(parser.parse_args().refresh_manifest)
