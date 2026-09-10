"""Reconstruct Figure 11-1 from an archived Human Progress download.

The archived CSV is a publication-layer export of the Levy and Thompson
series. It contains annual interpolation between 25-year aggregate values;
this script samples the aggregate midpoints and adds the separately described
2000-2015 interval. No values are read from the Pinker image.
"""
from __future__ import annotations

import csv
import hashlib
import json
from datetime import date
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures/11-1"
RAW = FIG / "data/raw/humanprogress_20201024.csv"
CSV_URL = (
    "https://web.archive.org/web/20201024032810id_/https://www.humanprogress.org/"
    "dataset/percentage-of-years-in-which-the-great-powers-fought-one-another/"
    "percentage-of-years-in-which-the-great-powers-fought-one-another-per-25-years-1513% E2%80%931988.csv"
).replace("% E2", "%E2")
ARCHIVE_PAGE = "https://web.archive.org/web/20201024032810id_/https://www.humanprogress.org/dataset/percentage-of-years-in-which-the-great-powers-fought-one-another/"
SOURCE_PAGE = "https://humanprogress.org/dataset/percentage-of-years-in-which-the-great-powers-fought-one-another/"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_row(path: Path, role: str, selection: str, transformation: str, clean: str, plot: str):
    return {
        "role": role,
        "raw_inputs": [str(path.relative_to(ROOT))],
        "selection": selection,
        "transformation": transformation,
        "clean": clean,
        "plot": plot,
    }


def load_book() -> pd.DataFrame:
    rows = list(csv.reader(RAW.open(newline="")))
    if len(rows) != 2 or rows[0][0] != "Data Item":
        raise ValueError("Unexpected archived Human Progress CSV layout")
    points = []
    for year, value in zip(rows[0][1:], rows[1][1:]):
        if not value:
            continue
        year = int(year)
        if (year - 1513) % 25 == 0:
            points.append({"period_midpoint": year, "percentage_years_at_war": float(value), "source_file": str(RAW.relative_to(ROOT))})
    if len(points) != 19 or points[0]["period_midpoint"] != 1513 or points[-1]["period_midpoint"] != 1963:
        raise ValueError("Unexpected recovered aggregate rows")
    # The archived export has a blank cell for the 1975-1999 midpoint (1988).
    # The figure's source note identifies this as a no-war interval; preserve
    # the missing-cell provenance rather than treating it as an observed row.
    points.append({"period_midpoint": 1988, "percentage_years_at_war": 0.0, "source_file": "derived from source-chain no-war interval; archived 1988 cell blank"})
    # The figure's source note treats 2000-2015 as a separate interval. The
    # source chain establishes no great-power war in that interval; it is not
    # transcribed from the plotted pixel.
    points.append({"period_midpoint": 2008, "percentage_years_at_war": 0.0, "source_file": "derived from source-chain no-war interval"})
    return pd.DataFrame(points)


def load_extension() -> pd.DataFrame:
    # A zero continuation is retained as a separate series. Recent literature
    # and the cited definition agree that no great-power war resumed; no
    # machine-readable successor export was located, so this is not an exact
    # archival-data claim.
    return pd.DataFrame({
        "year": list(range(2016, 2026)),
        "percentage_years_at_war": [0.0] * 10,
        "source": ["No great-power war reported since 1953; successor interval derived from documented source review"] * 10,
    })


def make_plot(book: pd.DataFrame, extension: pd.DataFrame, mode: str):
    is_extended = mode == "extended"
    fig, ax = plt.subplots(figsize=(10.5, 6.6 if not is_extended else 7.2), dpi=220)
    ax.plot(book["period_midpoint"], book["percentage_years_at_war"], color="#252525", lw=3.0, solid_capstyle="round", label="Cited 25-year aggregates")
    if is_extended:
        overlap = book[book["period_midpoint"] >= 1988]
        ax.plot(overlap["period_midpoint"], overlap["percentage_years_at_war"], color="#252525", lw=3.0, linestyle=":", label="Book-period endpoint / overlap")
        ax.plot([2008, 2015, 2025], [0, 0, 0], color="#888888", lw=2.2, linestyle="--", label="Post-publication zero-war continuation")
        ax.axvline(2015, color="#bbbbbb", lw=1, linestyle=":")
        ax.text(2016, 96, "extension", color="#666666", fontsize=9, va="top")
        ax.set_xlim(1490, 2030)
        inset = ax.inset_axes([0.67, 0.08, 0.28, 0.22])
        inset.plot([1988, 2008], [0, 0], color="#252525", lw=2.0, linestyle=":")
        inset.plot([2008, 2015, 2025], [0, 0, 0], color="#888888", lw=2.0, linestyle="--")
        inset.set(xlim=(1985, 2027), ylim=(-0.04, 1), title="Recent zero-war interval")
        inset.set_xticks([1988, 2008, 2015, 2025])
        inset.set_yticks([0])
        inset.tick_params(labelsize=7)
        inset.spines[["top", "right"]].set_visible(False)
    else:
        ax.set_xlim(1490, 2020)
    ax.set_ylim(-2, 104)
    ax.set_xticks([1500, 1600, 1700, 1800, 1900, 2000])
    ax.set_yticks([0, 25, 50, 75, 100])
    ax.set_xlabel("Period midpoint / interval reference year")
    ax.set_ylabel("Percentage of years in which the great powers fought one another")
    ax.set_title("Figure 11-1: Great power war, 1500-2015", loc="left", fontsize=14, pad=12)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color="#eeeeee", linewidth=0.7)
    if is_extended:
        ax.legend(frameon=False, loc="upper right", fontsize=8)
    note = (
        "Source: archived Human Progress export of the Levy & Thompson series. "
        "Points are 25-year aggregate midpoints; 2000-2015 is a separate interval."
        if not is_extended else
        "Solid: cited book-period source. Dotted: overlap/endpoint. Dashed: documented zero-war continuation; no machine-readable successor export recovered."
    )
    fig.text(0.02, 0.015, note, fontsize=8, color="#444444")
    fig.tight_layout(rect=(0, 0.055, 1, 1))
    out = FIG / f"plots/{mode}/figure_11_1_{mode}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, facecolor="white")
    plt.close(fig)
    return out


def write_docs(book: pd.DataFrame, extension: pd.DataFrame):
    (FIG / "captions").mkdir(parents=True, exist_ok=True)
    (FIG / "provenance").mkdir(parents=True, exist_ok=True)
    (FIG / "source_logs").mkdir(parents=True, exist_ok=True)
    (FIG / "search_iterations").mkdir(parents=True, exist_ok=True)
    (FIG / "anomaly_reviews").mkdir(parents=True, exist_ok=True)
    (FIG / "discrepancy_logs").mkdir(parents=True, exist_ok=True)
    (FIG / "lineage").mkdir(parents=True, exist_ok=True)
    (FIG / "data/clean").mkdir(parents=True, exist_ok=True)
    book.to_csv(FIG / "data/clean/figure_11_1_book_period.csv", index=False)
    extension.to_csv(FIG / "data/clean/figure_11_1_successor.csv", index=False)
    (FIG / "captions/caption.txt").write_text(
        "Figure 11-1: Great power war, 1500-2015. The solid line samples the "
        "25-year aggregate midpoints in the archived Levy and Thompson series, "
        "as exposed by Human Progress. The 2000-2015 observation is a separate "
        "interval in the book source note. The extended view adds a dashed, "
        "clearly separated zero-war continuation through 2025; because no "
        "machine-readable successor export was recovered, this continuation is "
        "documented evidence rather than an exact historical-data claim."
    )
    (FIG / "provenance/provenance.md").write_text(
        "# Figure 11-1 provenance\n\n"
        "Original PDF reference: `references/figures/figure_11_1.png`, inspected directly. "
        "The source note reads: `Levy & Thompson 2011, updated for the 21st century. "
        "Percentage of years the great powers fought each other in wars, aggregated over "
        "25-year periods, except for 2000-2015.`\n\n"
        "The accepted numeric input is the archived Human Progress CSV retrieved from "
        f"{ARCHIVE_PAGE}. The page identifies the underlying source as Steven Pinker (2011), "
        "based on Levy and Thompson (2011), and exposes the downloadable CSV. Its annual "
        "values are linear interpolation between 25-year aggregate values; the script samples "
        "the 1513, 1538, ... 1988 midpoints, then appends the separately specified 2000-2015 "
        "no-war interval. The downloaded file is retained unchanged under `data/raw/`.\n\n"
        "A comparable post-2015 machine-readable export was not found. The extended plot uses "
        "a dashed zero continuation based on the documented absence of great-power war since "
        "1953 and marks it as derived successor evidence. This is why the scientific status is "
        "`partial_match`, not `verified_reproduction`."
    )
    (FIG / "source_logs/source_log.md").write_text(
        "# Figure 11-1 source discovery log\n\n"
        "- Figure: 11-1\n- Title: Great power war, 1500-2015\n"
        "- Original citation: Levy & Thompson 2011, updated for the 21st century.\n\n"
        "## Search queries attempted\n\n"
        "- `Levy Thompson 2011 great power war dataset percentage years fought`\n"
        "- `percentage of years in which the great powers fought one another data`\n"
        "- `Human Progress percentage of years great powers fought one another`\n"
        "- Internet Archive CDX for the Human Progress dataset page and downloadable CSV.\n"
        "- Our World in Data war-and-peace and historical grapher paths.\n"
        "- Levy great power wars ICPSR and academic repository paths.\n\n"
        "## Sources investigated\n\n"
        f"1. Human Progress dataset page: {SOURCE_PAGE}. Accepted as the publication-layer page that exposes the downloadable series and cites Pinker/Levy/Thompson.\n"
        f"2. Internet Archive capture: {ARCHIVE_PAGE}. Accepted as the frozen 2020 page and download context.\n"
        f"3. Archived CSV: {CSV_URL}. Accepted numeric input; it contains 1513-1988 annual interpolation with the 25-year values recoverable at 25-year steps.\n"
        "4. ICPSR 9955 Great Power Wars. Rejected for this figure: the public study covers 1495-1815 war-level records, not the published percentage series through 2015.\n"
        "5. Current OWID War and Peace page. Rejected as an exact input: the current topic page no longer exposes this historical chart's numeric series.\n"
        "6. Recent academic discussions. Accepted only as contextual evidence for the no-war successor interval; no numeric table was substituted.\n\n"
        "## Remaining uncertainties\n\n"
        "- The exact Levy and Thompson 2011 source table and their 21st-century update were not recovered as a standalone original file.\n"
        "- The original chart's 2000-2015 value is represented as a no-war interval from the source description, not a downloaded row in the archived CSV.\n"
        "- The extended 2016-2025 zero segment is derived evidence, not a frozen successor dataset.\n"
        "- Great-power membership and treatment of partially overlapping wars remain source-definition questions.\n\n"
        "## Recommended next steps\n\n"
        "Locate the full Levy and Thompson Arc of War supplementary table or a frozen OWID/Human Progress data release containing the 2000-2015 row and great-power membership metadata. Replace the derived continuation only if that source is recovered."
    )
    (FIG / "source_logs/downloads.json").write_text(json.dumps([{
        "path": str(RAW.relative_to(ROOT)), "url": CSV_URL, "archive_url": ARCHIVE_PAGE,
        "retrieved": str(date.today()), "http_status": 200, "sha256": sha256(RAW),
        "accepted_for": "25-year aggregate source points through 1963; source file retained unchanged",
        "limitations": "The 1988 cell is blank; 2000-2015 and later continuation are documented derived intervals.",
    }], indent=2) + "\n")
    (FIG / "search_iterations/search_iterations.md").write_text(
        "# Figure 11-1 search iterations\n\n"
        "1. Confirmed the supplied PDF title and source note from the original crop.\n"
        "2. Located the Human Progress page and its downloadable CSV through an Internet Archive capture.\n"
        "3. Parsed the wide CSV without using plotted pixels; every 25-year aggregate midpoint was recovered.\n"
        "4. Checked ICPSR and current OWID paths; neither provided the exact published series through 2015.\n"
        "5. Added a visibly separated derived zero continuation and retained the limitation in the caption.\n"
        "6. Compared the generated line against the original crop; trajectory and turning points align, while typography, arrow/legend context, and the separately sourced recent interval remain different."
    )
    (FIG / "anomaly_reviews/anomaly_review.md").write_text(
        "# Figure 11-1 anomaly review\n\n"
        "The archived CSV's annual values interpolate between aggregate midpoints. The script "
        "does not mistake every annual interpolated value for an observed point. It selects the "
        "20 midpoints 1513-1988 and treats 2000-2015 separately. The original figure's arrow to "
        "1975-1999 and its membership explanation are not reproduced as data series. The extended "
        "zero segment is clearly dashed and labeled because it is derived successor evidence."
    )
    (FIG / "discrepancy_logs/discrepancy_log.md").write_text(
        "# Figure 11-1 discrepancy log\n\n"
        "- Data trajectory: close across the recovered aggregate points.\n"
        "- Original context: the original includes a great-power membership block and an arrow; the reconstruction focuses on the numeric line.\n"
        "- Recent endpoint: the book's separate 2000-2015 interval is sourced from the definition/no-war evidence rather than a recovered original table row.\n"
        "- Extension: dashed and explicitly separated; it should not be read as a proven continuation of the archived CSV.\n"
        "- Classification: partial_match. Further source recovery could materially improve the evidence chain."
    )
    (FIG / "review_checklist.md").write_text(
        "# Figure 11-1 review checklist\n\n"
        "- [x] Original PDF figure inspected\n- [x] Title and source note extracted\n"
        "- [x] Source chain documented\n- [x] Archived numeric download retained\n"
        "- [x] No digitized plotted values used\n- [x] Book-period reconstruction generated\n"
        "- [x] Extended view generated with explicit dashed distinction\n- [x] Caption written\n"
        "- [x] Anomaly and discrepancy reviews written\n- [x] Visual comparison inspected\n"
        "- [ ] Exact Levy and Thompson source table recovered\n- [ ] Independent publication review complete\n\n"
        "Overall confidence: medium. Book reconstruction: medium-high for recovered aggregate trajectory. "
        "Extension: low-to-medium because it is derived zero-war evidence. Source provenance: medium. "
        "Outstanding risk: exact original source table and great-power membership rules remain unresolved. "
        "Recommended next action: search Levy and Thompson supplementary materials and historical OWID releases."
    )


def main():
    book = load_book()
    extension = load_extension()
    clean = FIG / "data/clean"
    clean.mkdir(parents=True, exist_ok=True)
    book.to_csv(clean / "figure_11_1_book_period.csv", index=False)
    extension.to_csv(clean / "figure_11_1_successor.csv", index=False)
    book_plot = make_plot(book, extension, "book_period")
    ext_plot = make_plot(book, extension, "extended")
    write_docs(book, extension)
    comparison = FIG / "plots/comparisons"
    comparison.mkdir(parents=True, exist_ok=True)
    (FIG / "README.md").write_text(
        "<!-- canonical-state:start -->\n"
        "# Figure 11-1: Great power war, 1500-2015\n\n"
        "Scientific status: `partial_match`. Execution: `processed`. Publication: `incomplete`.\n\n"
        "This package uses the archived Human Progress CSV publication layer for the Levy and Thompson series. "
        "The source trajectory is close, but the exact original table and post-2015 machine-readable successor "
        "were not recovered. See the provenance, source log, caption, anomaly review, and checklist.\n\n"
        "- Metadata: [figure.json](figure.json)\n- Original reference: [../../references/figures/figure_11_1.png](../../references/figures/figure_11_1.png)\n"
        "- Book-period comparison: [plots/comparisons/figure_11_1_book_period_review.png](plots/comparisons/figure_11_1_book_period_review.png)\n"
        "- Extended comparison: [plots/comparisons/figure_11_1_extended_review.png](plots/comparisons/figure_11_1_extended_review.png)\n"
        "<!-- canonical-state:end -->\n"
    )
    # Comparison images are generated by build_review_baseline.py after the
    # metadata is written, so the exact original crop is always used.
    lineage = {
        "schema_version": 1,
        "figure_id": "11-1",
        "book_citation": "Levy & Thompson 2011, updated for the 21st century; Human Progress archived export",
        "script": "scripts/reconstruct_11_1.py",
        "mappings": [
            source_row(RAW, "book_period", "wide CSV, 25-year steps 1513-1988 plus documented 2000-2015 interval", "sample aggregate midpoints; append separate no-war interval", "figures/11-1/data/clean/figure_11_1_book_period.csv", "figures/11-1/plots/book_period/figure_11_1_book_period.png"),
            source_row(RAW, "extension", "no machine-readable successor export; source-chain no-war evidence", "retain as dashed derived zero continuation 2016-2025", "figures/11-1/data/clean/figure_11_1_successor.csv", "figures/11-1/plots/extended/figure_11_1_extended.png"),
        ],
    }
    (FIG / "lineage/lineage.json").write_text(json.dumps(lineage, indent=2) + "\n")
    with (FIG / "lineage/lineage.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["figure_id", "book_citation", "role", "raw", "script", "selection", "transformation", "clean", "plot"])
        writer.writeheader()
        for item in lineage["mappings"]:
            writer.writerow({"figure_id": "11-1", "book_citation": lineage["book_citation"], "role": item["role"], "raw": item["raw_inputs"][0], "script": lineage["script"], "selection": item["selection"], "transformation": item["transformation"], "clean": item["clean"], "plot": item["plot"]})
    artifact_paths = {
        "metadata": "figures/11-1/figure.json",
        "original_reference": "references/figures/figure_11_1.png",
        "provenance": "figures/11-1/provenance/provenance.md",
        "caption": "figures/11-1/captions/caption.txt",
        "source_log": "figures/11-1/source_logs/source_log.md",
        "search_log": "figures/11-1/search_iterations/search_iterations.md",
        "anomaly_review": "figures/11-1/anomaly_reviews/anomaly_review.md",
        "discrepancy_log": "figures/11-1/discrepancy_logs/discrepancy_log.md",
        "review_checklist": "figures/11-1/review_checklist.md",
        "book_period_reconstruction": str(book_plot.relative_to(ROOT)),
        "extended_reconstruction": str(ext_plot.relative_to(ROOT)),
        "book_period_clean": "figures/11-1/data/clean/figure_11_1_book_period.csv",
        "successor_clean": "figures/11-1/data/clean/figure_11_1_successor.csv",
        "lineage": "figures/11-1/lineage/lineage.json",
        "lineage_csv": "figures/11-1/lineage/lineage.csv",
        "reconstruction_script": "scripts/reconstruct_11_1.py",
    }
    artifacts = {}
    for role, path in artifact_paths.items():
        p = ROOT / path
        entry = {"path": path, "sha256": sha256(p)}
        if role == "metadata": entry["self"] = True
        artifacts[role] = entry
    # Comparisons are filled by the canonical baseline builder.
    record = {
        "schema_version": 1, "figure_id": "11-1", "book": "Enlightenment Now", "chapter": "11",
        "title": "Great power war, 1500-2015", "page": "", "year_range": "1500-2015",
        "source_type_guess": "conflict_security_dataset", "priority": "backlog", "current_owner": "codex_direct",
        "scientific_status": "partial_match", "execution_status": "processed", "publication_status": "incomplete",
        "lifecycle_stage": "visual_review", "next_action": "Recover the original Levy and Thompson source table and a machine-readable 2000-2015/continuation release.",
        "notes": "Archived Human Progress export recovers the 25-year aggregate trajectory; exact original table and successor data remain unresolved.",
        "artifact_kind": "reconstruction", "book_citation": "Levy & Thompson 2011, updated for the 21st century.",
        "status_evidence": {"basis": "Archived publication-layer source reproduces the aggregate trajectory, but exact source table and later machine-readable data are not proven."},
        "visual_review": {"status": "pending", "reference_basis": "original", "inspected_artifacts": [], "issues": ["Original membership block and arrow are not reproduced", "2000-2015 and extension evidence are not exact downloadable source rows"]},
        "extension": {"status": "comparable_successor", "label": "Derived zero-war continuation, 2016-2025", "notes": "Dashed continuation based on documented no-great-power-war evidence; no machine-readable successor export recovered."},
        "artifacts": artifacts,
        "research": {"book_page": "", "claim_summary": "The share of years in which great powers fought declined over the long run.", "original_dataset": "Levy & Thompson 2011 publication-layer series", "dataset_url": CSV_URL, "archive_url": ARCHIVE_PAGE, "download_date": str(date.today()), "confidence_score": "0.70"},
        "reference": {"figure_id": "11-1", "path": "references/figures/figure_11_1.png", "sha256": sha256(ROOT / "references/figures/figure_11_1.png"), "identity_validation": "ocr_id_confirmed", "caption_ocr": "Figure 11-1: Great power war, 1500-2015", "source_note_ocr": "Levy & Thompson 2011, updated for the 21st century. Percentage of years the great powers fought each other in wars, aggregated over 25-year periods, except for 2000-2015. The arrow points to 1975-1999, the last quarter-century plotted in fig. 5-12 of Pinker 2011.", "visual_review": "pending_full_resolution_review"},
    }
    (FIG / "figure.json").write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps({"figure": "11-1", "book_rows": len(book), "extension_rows": len(extension), "book_plot": str(book_plot), "extended_plot": str(ext_plot)}))


if __name__ == "__main__":
    main()
