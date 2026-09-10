"""Reconstruct Figure 11-2 from PRIO/UCDP battle-death datasets.

The book uses PRIO for 1946-1988 and UCDP version 5.0 for 1989-2015. The
current UCDP release is retained as a separate continuation. World population
is an explicitly labelled current OWID denominator because the cited Census
series was not recovered as a downloadable historical table in this pass.
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
FIG = ROOT / "figures/11-2"
PRIO = FIG / "data/raw/PRIO_Battle_Deaths_Dataset_31.xls"
UCDP_BOOK = FIG / "data/raw/ucdp_brd_conf_50_2016.csv"
UCDP_CURRENT = FIG / "data/raw/ucdp_brd_conf_261.csv"
POP = FIG / "data/raw/owid_world_population.csv"
PRIO_URL = "https://cdn.cloud.prio.org/files/d21ef702-a546-45a8-b3c9-5b520dcc1239/PRIO%20Battle%20Deaths%20Dataset%2031.xls?inline=true"
UCDP_BOOK_URL = "https://ucdp.uu.se/downloads/brd/ucdp-brd-conf-50-2016.csv"
UCDP_CURRENT_URL = "https://ucdp.uu.se/downloads/brd/ucdp-brd-conf-261-csv.zip"
POP_URL = "https://ourworldindata.org/grapher/population.csv"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_series():
    prio = pd.read_excel(PRIO)
    prio["bdeadbes"] = pd.to_numeric(prio["bdeadbes"], errors="coerce").where(lambda x: x >= 0)
    prio = prio[prio["year"].between(1946, 1988)]
    historical = prio.groupby("year", as_index=False).agg(
        deaths=("bdeadbes", "sum"), conflict_rows=("id", "size"), missing_estimates=("bdeadbes", lambda x: int(x.isna().sum()))
    )
    historical["source_series"] = "PRIO Battle Deaths Dataset 3.1"
    historical["source_version"] = "PRIO 3.1; cited Lacina & Gleditsch 2005 family"

    old = pd.read_csv(UCDP_BOOK)
    recent = old[old["Year"].between(1989, 2015)].groupby("Year", as_index=False).agg(
        deaths=("BdBest", "sum"), conflict_rows=("ConflictID", "size")
    ).rename(columns={"Year": "year"})
    recent["missing_estimates"] = 0
    recent["source_series"] = "UCDP Battle-Related Deaths Dataset v5.0"
    recent["source_version"] = "UCDP v5.0-2016 release"
    book_deaths = pd.concat([historical, recent], ignore_index=True).sort_values("year")

    current = pd.read_csv(UCDP_CURRENT)
    successor = current[current["year"].between(2016, 2023)].groupby("year", as_index=False).agg(
        deaths=("bd_best", "sum"), conflict_rows=("conflict_id", "size")
    )
    successor["missing_estimates"] = 0
    successor["source_series"] = "UCDP Battle-Related Deaths Dataset v26.1"
    successor["source_version"] = "UCDP v26.1 current successor"

    pop = pd.read_csv(POP)
    pop = pop[pop["Entity"].eq("World")][["Year", "Population"]].rename(columns={"Year": "year", "Population": "population"})
    book = book_deaths.merge(pop, on="year", how="left", validate="one_to_one")
    extension = successor.merge(pop, on="year", how="left", validate="one_to_one")
    for frame in [book, extension]:
        if frame["population"].isna().any():
            raise ValueError("Missing world population denominator")
        frame["rate_per_100k"] = frame["deaths"] / frame["population"] * 100000
        frame["unit"] = "battle deaths per 100,000 people per year"
    if len(book) != 70 or book.year.min() != 1946 or book.year.max() != 2015:
        raise ValueError("Book period is not 1946-2015")
    return book, extension


def plot(book, extension, mode):
    extended = mode == "extended"
    fig, ax = plt.subplots(figsize=(10.5, 6.6 if not extended else 7.25), dpi=220)
    ax.plot(book.year, book.rate_per_100k, color="#252525", lw=3.0, solid_capstyle="round", label="Cited book-period sources")
    if extended:
        overlap = book[book.year.ge(2008)]
        ax.plot(overlap.year, overlap.rate_per_100k, color="#252525", lw=2.3, linestyle=":", label="Book-period overlap")
        ax.plot(extension.year, extension.rate_per_100k, color="#888888", lw=2.3, linestyle="--", label="UCDP v26.1 successor")
        ax.axvline(2015, color="#bbbbbb", lw=1, linestyle=":")
        inset = ax.inset_axes([0.63, 0.08, 0.30, 0.25])
        inset.plot(overlap.year, overlap.rate_per_100k, color="#252525", lw=1.8, linestyle=":")
        inset.plot(extension.year, extension.rate_per_100k, color="#888888", lw=1.8, linestyle="--")
        inset.set(xlim=(1998, 2024), ylim=(0, 5), title="Recent years")
        inset.set_xticks([2000, 2008, 2015, 2023])
        inset.set_yticks([0, 2, 4])
        inset.tick_params(labelsize=7)
        inset.spines[["top", "right"]].set_visible(False)
        ax.set_xlim(1945, 2025)
    else:
        ax.set_xlim(1945, 2016)
    ax.set_ylim(0, 25)
    ax.set_xticks(range(1945, 2016, 5))
    ax.set_yticks([0, 5, 10, 15, 20, 25])
    ax.tick_params(axis="x", rotation=45)
    ax.set_xlabel("Year")
    ax.set_ylabel("Battle deaths per 100,000 people per year")
    ax.set_title("Figure 11-2: Battle deaths, 1946-2016", loc="left", fontsize=14, pad=12)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color="#eeeeee", linewidth=0.7)
    if extended:
        ax.legend(frameon=False, fontsize=8, loc="upper right")
    note = (
        "Sources: PRIO Battle Deaths Dataset 3.1 (1946-1988); UCDP v5.0-2016 (1989-2015). "
        "Denominator: current OWID world population series; cited Census vintage not recovered."
        if not extended else
        "Solid: cited book-period sources. Dotted: book-period overlap. Dashed: UCDP v26.1 successor; definitions and source vintage may differ."
    )
    fig.text(0.02, 0.015, note, fontsize=8, color="#444444")
    fig.tight_layout(rect=(0, 0.055, 1, 1))
    out = FIG / f"plots/{mode}/figure_11_2_{mode}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, facecolor="white")
    plt.close(fig)
    return out


def write_docs(book, extension):
    for sub in ["captions", "provenance", "source_logs", "search_iterations", "anomaly_reviews", "discrepancy_logs", "lineage", "data/clean"]:
        (FIG / sub).mkdir(parents=True, exist_ok=True)
    book.to_csv(FIG / "data/clean/figure_11_2_book_period.csv", index=False)
    extension.to_csv(FIG / "data/clean/figure_11_2_successor.csv", index=False)
    (FIG / "captions/caption.txt").write_text(
        "Figure 11-2: Battle deaths, 1946-2016. The book-period reconstruction "
        "uses PRIO best estimates for 1946-1988 and the cited UCDP v5.0 release "
        "for 1989-2015, divided by a retained world-population series. The "
        "extended view uses UCDP v26.1 from 2016-2023 as a dashed successor. "
        "The Census population vintage named in the book was not recovered, so "
        "the denominator is explicitly marked as a modern substitute and the "
        "status remains partial_match."
    )
    (FIG / "provenance/provenance.md").write_text(
        "# Figure 11-2 provenance\n\n"
        "The original PDF crop was inspected directly. Its source note identifies "
        "the Human Security Report Project 2007; PRIO Battle Deaths Dataset for "
        "1946-1988; UCDP Battle-Related Deaths Dataset v5.0 for 1989-2015; and "
        "US Census/McEvedy & Jones population figures.\n\n"
        "The retained PRIO 3.1 workbook is an institutionally hosted successor in "
        "the cited dataset family and is aggregated by year from its `bdeadbes` "
        "conflict-year field. The archived UCDP v5.0-2016 conflict CSV is summed "
        "by year from `BdBest`. The current UCDP v26.1 conflict CSV is a separate "
        "continuation through 2023.\n\n"
        "The book's exact Census denominator was not recovered. The plot therefore "
        "uses a current OWID world population file, retained as raw input and "
        "identified in every clean row. No values were digitized from the book image."
    )
    (FIG / "source_logs/source_log.md").write_text(
        "# Figure 11-2 source discovery log\n\n"
        "- Figure: 11-2\n- Title: Battle deaths, 1946-2016\n"
        "- Original citation: Human Security Report Project 2007; PRIO/UCDP; Census and McEvedy & Jones.\n\n"
        "## Queries and investigations\n\n"
        "- `Battle deaths 1946-2016 Pinker UCDP data`\n"
        "- `Battle-related deaths 1946-1988 Lacina Gleditsch CSV`\n"
        "- `Human Security Report Project 2007 battle deaths download`\n"
        "- UCDP historical download center and version-history pages.\n"
        "- PRIO Battle Deaths dataset and its versioned secondary downloads.\n"
        "- Library of Congress Battle Deaths Dataset record and current OWID/UCDP pages.\n\n"
        "## Sources investigated\n\n"
        f"1. PRIO Battle Deaths Dataset 3.1: {PRIO_URL}. Accepted for the 1946-1988 numeric series; its `bdeadbes` field is the best estimate and is aggregated by year.\n"
        f"2. UCDP v5.0-2016 conflict CSV: {UCDP_BOOK_URL}. Accepted for 1989-2015, exactly matching the book's source vintage family.\n"
        f"3. UCDP v26.1 current conflict ZIP: {UCDP_CURRENT_URL}. Accepted only as a dashed successor from 2016-2023.\n"
        f"4. OWID population series: {POP_URL}. Accepted as denominator substitute; rejected as proof of the cited Census vintage.\n"
        "5. PRIO 2.0 yearly aggregate ZIP. Retained candidate for historical comparison, but not used because PRIO 3.1 is the later institutional release in the cited family and exposes the underlying conflict rows.\n"
        "6. Human Security Report and McEvedy/Jones publications. Context confirmed, but a machine-readable exact population denominator was not recovered.\n\n"
        "## Uncertainties and next steps\n\n"
        "The denominator vintage and the exact HSRP transformation/adjustments remain unresolved. Compare the clean rates against a recovered Census IDB table or HSRP workbook before considering verification. Preserve PRIO/UCDP source seams; do not silently splice current UCDP into the historical source."
    )
    (FIG / "source_logs/downloads.json").write_text(json.dumps([
        {"path": str(PRIO.relative_to(ROOT)), "url": PRIO_URL, "retrieved": str(date.today()), "sha256": sha256(PRIO), "accepted_for": "1946-1988 deaths"},
        {"path": str(UCDP_BOOK.relative_to(ROOT)), "url": UCDP_BOOK_URL, "retrieved": str(date.today()), "sha256": sha256(UCDP_BOOK), "accepted_for": "1989-2015 deaths"},
        {"path": str(UCDP_CURRENT.relative_to(ROOT)), "url": UCDP_CURRENT_URL, "retrieved": str(date.today()), "sha256": sha256(UCDP_CURRENT), "accepted_for": "2016-2023 successor"},
        {"path": str(POP.relative_to(ROOT)), "url": POP_URL, "retrieved": str(date.today()), "sha256": sha256(POP), "accepted_for": "denominator substitute", "limitation": "not the cited Census vintage"},
    ], indent=2) + "\n")
    (FIG / "search_iterations/search_iterations.md").write_text(
        "# Figure 11-2 search iterations\n\n"
        "1. Confirmed the original title, annual scale, source split, and arrow from the supplied PDF crop.\n"
        "2. Recovered PRIO 3.1 and independently checked its aggregate shape against the original postwar peak and 1970s bump.\n"
        "3. Recovered UCDP v5.0-2016 for the cited 1989-2015 segment and current UCDP v26.1 for a separate extension.\n"
        "4. Used a retained modern OWID population file because the exact cited Census table was not found; downgraded status and documented the gap.\n"
        "5. Inspected both side-by-side comparisons; the main curve is close in shape, while denominator vintage, exact HSRP adjustments, and recent-series seam remain unresolved."
    )
    (FIG / "anomaly_reviews/anomaly_review.md").write_text(
        "# Figure 11-2 anomaly review\n\n"
        "PRIO and UCDP are related but distinct source vintages. The script keeps their source labels and does not average or backcast between them. Unknown PRIO best estimates are excluded from annual sums rather than silently set to zero. The modern UCDP extension is dashed and uses the same rate concept but a revised source release. The population denominator is a modern substitute, not the cited Census vintage."
    )
    (FIG / "discrepancy_logs/discrepancy_log.md").write_text(
        "# Figure 11-2 discrepancy log\n\n"
        "- The overall postwar trajectory and major peaks align with the original.\n"
        "- Small level differences remain because the exact Census denominator and HSRP adjustments were not recovered.\n"
        "- UCDP v5.0 and current v26.1 have different source vintages and coding revisions; the seam is visible and documented.\n"
        "- The original arrow and surrounding discussion are not numerical inputs.\n"
        "- Classification: partial_match; exact denominator recovery is a reasonable next research step."
    )
    (FIG / "review_checklist.md").write_text(
        "# Figure 11-2 review checklist\n\n"
        "- [x] Original PDF figure inspected\n- [x] Title and source note extracted\n"
        "- [x] PRIO and UCDP source chain documented\n- [x] Raw versioned downloads retained\n"
        "- [x] No digitized plotted values used\n- [x] Book-period reconstruction generated\n"
        "- [x] Extended successor view generated\n- [x] Caption written\n"
        "- [x] Anomaly and discrepancy reviews written\n- [x] Side-by-side comparisons inspected\n"
        "- [ ] Exact Census/McEvedy denominator recovered\n- [ ] HSRP adjustments independently reproduced\n- [ ] Independent publication review complete\n\n"
        "Overall confidence: medium. Book reconstruction: medium for trajectory, lower for exact levels. Extension: medium for source continuity, low for historical comparability. Source provenance: medium-high. Outstanding risks: denominator vintage and HSRP adjustment details. Recommended next action: recover the exact population table and HSRP transformation notes."
    )


def main():
    book, extension = load_series()
    clean = FIG / "data/clean"
    clean.mkdir(parents=True, exist_ok=True)
    book.to_csv(clean / "figure_11_2_book_period.csv", index=False)
    extension.to_csv(clean / "figure_11_2_successor.csv", index=False)
    book_plot = plot(book, extension, "book_period")
    extended_plot = plot(book, extension, "extended")
    write_docs(book, extension)
    (FIG / "README.md").write_text(
        "<!-- canonical-state:start -->\n# Figure 11-2: Battle deaths, 1946-2016\n\n"
        "Scientific status: `partial_match`. Execution: `processed`. Publication: `incomplete`.\n\n"
        "PRIO and UCDP numeric sources recover the main annual trajectory. The exact cited population denominator and HSRP adjustments remain unresolved, so this package is not a verified reproduction.\n\n"
        "- Metadata: [figure.json](figure.json)\n- Original reference: [../../references/figures/figure_11_2.png](../../references/figures/figure_11_2.png)\n"
        "- Book-period comparison: [plots/comparisons/figure_11_2_book_period_review.png](plots/comparisons/figure_11_2_book_period_review.png)\n"
        "- Extended comparison: [plots/comparisons/figure_11_2_extended_review.png](plots/comparisons/figure_11_2_extended_review.png)\n"
        "<!-- canonical-state:end -->\n"
    )
    lineage = {
        "schema_version": 1, "figure_id": "11-2",
        "book_citation": "Human Security Report Project 2007; PRIO Battle Deaths Dataset; UCDP Battle-Related Deaths Dataset v5.0",
        "script": "scripts/reconstruct_11_2.py", "mappings": [
            {"role": "book_period", "raw_inputs": [str(PRIO.relative_to(ROOT)), str(UCDP_BOOK.relative_to(ROOT)), str(POP.relative_to(ROOT))], "selection": "PRIO 1946-1988; UCDP v5.0 1989-2015; World population", "transformation": "sum best estimates by year; divide by population and multiply by 100000", "clean": "figures/11-2/data/clean/figure_11_2_book_period.csv", "plot": "figures/11-2/plots/book_period/figure_11_2_book_period.png"},
            {"role": "successor", "raw_inputs": [str(UCDP_CURRENT.relative_to(ROOT)), str(POP.relative_to(ROOT))], "selection": "UCDP v26.1 2016-2023", "transformation": "sum current best estimates by year; same rate formula; dashed source seam", "clean": "figures/11-2/data/clean/figure_11_2_successor.csv", "plot": "figures/11-2/plots/extended/figure_11_2_extended.png"},
        ]
    }
    (FIG / "lineage/lineage.json").write_text(json.dumps(lineage, indent=2) + "\n")
    with (FIG / "lineage/lineage.csv").open("w", newline="") as handle:
        fields = ["figure_id", "book_citation", "role", "raw", "script", "selection", "transformation", "clean", "plot"]
        writer = csv.DictWriter(handle, fieldnames=fields); writer.writeheader()
        for item in lineage["mappings"]:
            writer.writerow({"figure_id": "11-2", "book_citation": lineage["book_citation"], "role": item["role"], "raw": " | ".join(item["raw_inputs"]), "script": lineage["script"], "selection": item["selection"], "transformation": item["transformation"], "clean": item["clean"], "plot": item["plot"]})
    ref_path = "references/figures/figure_11_2.png"
    paths = {
        "metadata": "figures/11-2/figure.json", "original_reference": ref_path,
        "provenance": "figures/11-2/provenance/provenance.md", "caption": "figures/11-2/captions/caption.txt",
        "source_log": "figures/11-2/source_logs/source_log.md", "download_log": "figures/11-2/source_logs/downloads.json",
        "search_log": "figures/11-2/search_iterations/search_iterations.md", "anomaly_review": "figures/11-2/anomaly_reviews/anomaly_review.md",
        "discrepancy_log": "figures/11-2/discrepancy_logs/discrepancy_log.md", "review_checklist": "figures/11-2/review_checklist.md",
        "book_period_reconstruction": str(book_plot.relative_to(ROOT)), "extended_reconstruction": str(extended_plot.relative_to(ROOT)),
        "book_period_clean": "figures/11-2/data/clean/figure_11_2_book_period.csv", "successor_clean": "figures/11-2/data/clean/figure_11_2_successor.csv",
        "lineage": "figures/11-2/lineage/lineage.json", "lineage_csv": "figures/11-2/lineage/lineage.csv", "reconstruction_script": "scripts/reconstruct_11_2.py",
    }
    artifacts = {}
    for role, rel in paths.items():
        item = {"path": rel, "sha256": sha256(ROOT / rel)}
        if role == "metadata": item["self"] = True
        artifacts[role] = item
    record = {
        "schema_version": 1, "figure_id": "11-2", "book": "Enlightenment Now", "chapter": "11", "title": "Battle deaths, 1946-2016", "page": "", "year_range": "1946-2016", "source_type_guess": "health_demographic_dataset", "priority": "backlog", "current_owner": "codex_direct", "scientific_status": "partial_match", "execution_status": "processed", "publication_status": "incomplete", "lifecycle_stage": "visual_review", "next_action": "Recover the exact Census/McEvedy population denominator and HSRP adjustment procedure.", "notes": "PRIO/UCDP sources recover the main curve; current OWID population denominator is a documented substitute.", "artifact_kind": "reconstruction", "book_citation": lineage["book_citation"], "status_evidence": {"basis": "Strong source-family recovery and close trajectory, but denominator and HSRP adjustments remain unresolved."}, "visual_review": {"status": "pending", "reference_basis": "original", "inspected_artifacts": [], "issues": ["Denominator vintage not exact", "HSRP adjustments not independently reproduced", "Source-version seam in extension"]}, "extension": {"status": "comparable_successor", "label": "UCDP v26.1 successor, 2016-2023", "notes": "Dashed successor from current institutional release; revised coding may differ."}, "artifacts": artifacts, "research": {"book_page": "", "claim_summary": "Battle deaths per 100,000 people per year fell after the postwar peaks, with smaller later increases.", "original_dataset": "PRIO Battle Deaths Dataset 3.1 and UCDP v5.0-2016", "dataset_url": UCDP_BOOK_URL, "archive_url": "https://ucdp.uu.se/downloads/olddw.html", "download_date": str(date.today()), "confidence_score": "0.70"}, "reference": {"figure_id": "11-2", "pdf_path": "references/enlightenment_now_supplemental_graphics.pdf", "path": ref_path, "sha256": sha256(ROOT / ref_path), "identity_validation": "ocr_id_confirmed", "caption_ocr": "Figure 11-2: Battle deaths, 1946-2016", "source_note_ocr": "Adapted from Human Security Report Project 2007. For 1946-1988: Peace Research Institute of Oslo Battle Deaths Dataset 1946-2008, Lacina & Gleditsch 2005. For 1989-2015: UCDP Battle-Related Deaths Dataset version 5.0, Uppsala Conflict Data Program 2017, Melander, Pettersson, & Themnér 2016, updated with information from Therese Pettersson and Sam Taub of UCDP. World population figures: 1950-2016, US Census Bureau; 1946-1949, McEvedy & Jones 1978, with adjustments. The arrow points to 2008, the last year plotted in fig. 6-2 of Pinker 2011.", "visual_review": "pending_full_resolution_review"}
    }
    (FIG / "figure.json").write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps({"figure": "11-2", "book_rows": len(book), "successor_rows": len(extension), "book_plot": str(book_plot), "extended_plot": str(extended_plot)}))


if __name__ == "__main__":
    main()
