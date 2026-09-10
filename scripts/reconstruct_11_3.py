"""Reconstruct Figure 11-3 from PITF and UCDP source files.

The PITF workbook stores an ordinal death-magnitude category, not a death
count. The bounded categories are decoded to arithmetic midpoints and the
open-ended 5.0 category is retained at its documented lower bound. This is a
reproducible lower-bound reconstruction, not a claim to recover Pinker's
case-specific estimates.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures/11-3"
RAW = FIG / "data/raw"
CLEAN = FIG / "data/clean"
PLOTS = FIG / "plots"
REF = ROOT / "references/figures/figure_11_3.png"

PITF_URL = "https://www.systemicpeace.org/inscr/PITF%20GenoPoliticide%202018.xls"
PITF_CODEBOOK_URL = "https://www.systemicpeace.org/inscr/PITFProbSetCodebook2018.pdf"
UCDP_BOOK_URL = "https://ucdp.uu.se/downloads/nsos/ucdp-onesided-171.xlsx"
UCDP_CURRENT_URL = "https://ucdp.uu.se/downloads/nsos/ucdp-onesided-261-csv.zip"
POP_URL = "https://ourworldindata.org/grapher/population.csv"

# Arithmetic midpoints for the bounded PITF DEATHMAG intervals.  5.0 is open
# ended; using its lower bound avoids inventing an upper bound.
PITF_DEATHMAG_TO_COUNT = {
    0.0: 0,
    0.5: 650,
    1.0: 1_500,
    1.5: 3_000,
    2.0: 6_000,
    2.5: 12_000,
    3.0: 24_000,
    3.5: 48_000,
    4.0: 96_000,
    4.5: 192_000,
    5.0: 256_000,
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def load_population() -> pd.DataFrame:
    path = ROOT / "figures/11-2/data/raw/owid_world_population.csv"
    pop = pd.read_csv(path)
    return pop.loc[pop["Entity"].eq("World"), ["Year", "Population"]].rename(
        columns={"Year": "year", "Population": "population"}
    )


def load_series() -> tuple[pd.DataFrame, pd.DataFrame]:
    pitf = pd.read_excel(RAW / "PITF_GenoPoliticide_2018.xls")
    pitf["DEATHMAG"] = pd.to_numeric(pitf["DEATHMAG"], errors="coerce")
    pitf["estimated_deaths_lower_bound"] = pitf["DEATHMAG"].map(
        PITF_DEATHMAG_TO_COUNT
    )
    pitf_book = (
        pitf.loc[pitf["YEAR"].between(1956, 1988)]
        .groupby("YEAR", as_index=False)
        .agg(
            deaths=("estimated_deaths_lower_bound", "sum"),
            active_pitf_rows=("COUNTRY", "size"),
            deathmag_sum=("DEATHMAG", "sum"),
        )
        .rename(columns={"YEAR": "year"})
    )
    pitf_book["source_series"] = "PITF 2018 workbook, decoded lower-bound estimate"

    old = pd.read_excel(RAW / "ucdp_onesided_171.xlsx")
    old_book = (
        old.loc[old["Year"].between(1989, 2016)]
        .groupby("Year", as_index=False)
        .agg(
            deaths=("HighFatalityEstimate", "sum"),
            active_ucdp_rows=("ActorId", "size"),
        )
        .rename(columns={"Year": "year"})
    )
    old_book["source_series"] = "UCDP v17.1 high fatality estimate"

    current = pd.read_csv(RAW / "OneSided_v26_1.csv")
    current_book = (
        current.loc[current["year"].between(2017, 2025)]
        .groupby("year", as_index=False)
        .agg(
            deaths=("high_fatality_estimate", "sum"),
            active_ucdp_rows=("actor_id", "size"),
        )
    )
    current_book["source_series"] = "UCDP v26.1 successor high fatality estimate"

    pop = load_population()
    old_book = old_book.merge(pop, on="year", how="left")
    current_book = current_book.merge(pop, on="year", how="left")
    pitf_book = pitf_book.merge(pop, on="year", how="left")
    for frame in (pitf_book, old_book, current_book):
        frame["rate_per_100k"] = frame["deaths"] / frame["population"] * 100_000

    book = pd.concat([pitf_book, old_book], ignore_index=True).sort_values("year")
    book = book.loc[book["year"].between(1956, 2016)].reset_index(drop=True)
    extension = current_book.loc[current_book["year"].between(2017, 2023)].copy()
    if len(book) != 61 or book["year"].min() != 1956 or book["year"].max() != 2016:
        raise ValueError("unexpected Figure 11-3 book-period coverage")
    return book, extension


def plot(series: pd.DataFrame, extension: pd.DataFrame, mode: str) -> Path:
    PLOTS.mkdir(parents=True, exist_ok=True)
    path = PLOTS / ("figure_11_3_extended.png" if mode == "extended" else "figure_11_3_book_period.png")
    fig, ax = plt.subplots(figsize=(12, 7.5), dpi=180)
    pitf = series.loc[series["source_series"].str.startswith("PITF")]
    ucdp = series.loc[series["source_series"].str.startswith("UCDP")]
    ax.plot(pitf["year"], pitf["rate_per_100k"], color="#aaa8aa", lw=3, label="PITF")
    ax.plot(ucdp["year"], ucdp["rate_per_100k"], color="#171515", lw=3, label="UCDP")
    if mode == "extended" and not extension.empty:
        ax.axvline(2008, color="#c8c8c8", lw=1.5, ls=":")
        ax.plot(extension["year"], extension["rate_per_100k"], color="#777777", lw=2.5, ls="--", label="UCDP v26.1 successor")
        ax.annotate("", xy=(2008, 3), xytext=(2008, 8), arrowprops={"arrowstyle": "->", "color": "#c8c8c8", "lw": 2})
    ax.set_title("Figure 11-3: Genocide deaths, 1956-2016", loc="left", fontsize=18, pad=14)
    ax.set_xlabel("Year", fontsize=13)
    ax.set_ylabel("Genocide deaths per 100,000 people per year", fontsize=13)
    ax.set_xlim(1955, 2018 if mode == "extended" else 2017)
    ax.set_ylim(0, 50)
    ax.set_xticks(range(1955, 2020, 5))
    ax.grid(axis="y", color="#e5e5e5", lw=0.8)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False, loc="upper right")
    note = "PITF bounded-category lower-bound decode; UCDP high-fatality estimates; OWID population denominator."
    if mode == "extended":
        note += " Dashed: current UCDP successor, not the book series."
    fig.text(0.02, 0.015, note, fontsize=8.5, color="#555555")
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def write_docs(book: pd.DataFrame, extension: pd.DataFrame, plots: dict[str, Path]) -> None:
    for sub in ["provenance", "source_logs", "search_iterations", "anomaly_reviews", "discrepancy_logs", "captions", "lineage", "checksums", "plots/comparisons"]:
        (FIG / sub).mkdir(parents=True, exist_ok=True)
    (CLEAN / "figure_11_3_book_period.csv").parent.mkdir(parents=True, exist_ok=True)
    book.to_csv(CLEAN / "figure_11_3_book_period.csv", index=False)
    extension.to_csv(CLEAN / "figure_11_3_successor.csv", index=False)
    (FIG / "README.md").write_text("""# Figure 11-3 - Genocide deaths\n\nStatus: `partial_match`. The PITF source is an ordinal death-magnitude workbook. The primary reconstruction decodes bounded categories to arithmetic midpoints and the open-ended 5.0 category to its lower bound; this is not a recovery of Pinker's case-specific estimates. UCDP uses high-fatality estimates, with a separate v26.1 successor extension.\n\n- Original reference: [../../references/figures/figure_11_3.png](../../references/figures/figure_11_3.png)\n- Script: [../../scripts/reconstruct_11_3.py](../../scripts/reconstruct_11_3.py)\n- Book-period comparison: [plots/comparisons/figure_11_3_book_period_review.png](plots/comparisons/figure_11_3_book_period_review.png)\n- Extended comparison: [plots/comparisons/figure_11_3_extended_review.png](plots/comparisons/figure_11_3_extended_review.png)\n""")
    (FIG / "captions/caption.txt").write_text("Figure 11-3 is a partial reconstruction. The PITF workbook records ordinal annual death-magnitude categories rather than exact counts, so bounded categories were decoded to arithmetic midpoints and the open-ended 5.0 category was retained at its lower bound. UCDP high-fatality estimates are shown separately from the PITF series. The dashed continuation uses current UCDP v26.1 data and an OWID population denominator; it is not an exact historical continuation of the book's source vintage.")
    (FIG / "provenance/provenance.md").write_text(f"""# Provenance\n\n## Book citation\n\nPITF, 1955-2008: Political Instability Task Force State Failure Problem Set, 1955-2008, Marshall, Gurr, & Harff 2009; Center for Systemic Peace 2015; calculations described in Pinker 2011, p. 338. UCDP, 1989-2016: UCDP One-Sided Violence Dataset v. 2.5-2016 (the historical download center exposes the one-sided release as v1.4-2016), Melander, Pettersson, & Themnér 2016; Uppsala Conflict Data Program 2017.\n\n## Downloaded sources\n\n- PITF workbook: {PITF_URL}\n- PITF codebook: {PITF_CODEBOOK_URL}\n- Historical UCDP one-sided CSV: {UCDP_BOOK_URL}\n- Current UCDP one-sided CSV archive: {UCDP_CURRENT_URL}\n- Population denominator: {POP_URL}\n\n## Transformations\n\nPITF DEATHMAG categories use the codebook's bounded intervals. The script uses arithmetic midpoints for 0.5 through 4.5 and 256,000, the lower bound, for open-ended 5.0. Values are summed by year and divided by the World population series. UCDP uses the high fatality estimate, summed by year, with the same denominator.\n\nThe exact Census Bureau/McEvedy denominator and Pinker's case-specific death estimates were not recovered.\n""")
    (FIG / "source_logs/source_log.md").write_text(f"""# Source discovery log\n\n- Figure: 11-3, Genocide deaths, 1956-2016.\n- Queries attempted: `Pinker genocide deaths 1956 2016 data PITF UCDP`; `Political Instability Task Force State Failure Problem Set 1955 2008 genocide deaths`; `UCDP One-Sided Violence Dataset 2016`; official UCDP historical downloads; official Center for Systemic Peace data page; OWID historical PITF mirror.\n\n## Investigated\n\n- Center for Systemic Peace PITF GenoPoliticide 2018 workbook: accepted as the maintained official workbook and preserved raw. It contains the ordinal DEATHMAG scale, not exact counts.\n- UCDP historical one-sided v1.4-2016 CSV: accepted as the downloadable historical one-sided source; the book's v2.5 label conflicts with the historical download center label and remains an uncertainty.\n- UCDP v26.1 CSV archive: accepted only for a clearly labelled successor extension.\n- OWID PITF mirror: rejected as primary data because the available table exposes an indicator rather than the plotted death counts.\n- Pinker 2017 PDF: used as corroborating publication context only; no plotted values were transcribed.\n\n## Remaining uncertainties\n\nPinker appears to have used case-specific estimates and the cited Census/McEvedy denominator; the workbook's ordinal categories cannot reproduce those estimates exactly. The UCDP version label in the book differs from the historical download label.\n\n## Next steps\n\nRecover the 2015 Center for Systemic Peace workbook or Pinker's calculation table if publicly released; otherwise retain this as partial_match.\n""")
    (FIG / "search_iterations/search_iterations.md").write_text("""# Search iterations\n\n1. Resolved the supplemental-PDF source note and confirmed the PITF/UCDP split.\n2. Located and downloaded official PITF and historical UCDP files.\n3. Located current UCDP successor data and separated it from the book period.\n4. Tested OWID as a mirror; rejected its indicator-only table for the primary reconstruction.\n5. Full-resolution side-by-side inspection found the lower-bound PITF decode materially under-represents the book's large late-1960s/1970s peaks; status remains partial_match.\n""")
    (FIG / "anomaly_reviews/anomaly_review.md").write_text("""# Anomaly review\n\nMajor: the PITF lower-bound decode does not reproduce the book's 1971 peak or several late-1960s values. This is a source-information limitation, not a plotting omission. Major: the book's Census/McEvedy denominator is unavailable in the repository. Minor: line weights and annotations are approximations. The UCDP 1994 high-fatality spike is directionally consistent, but its historical version label is unresolved.\n\nClassification: `partial_match`; not verified.\n""")
    (FIG / "discrepancy_logs/discrepancy_log.md").write_text("""# Discrepancy log\n\n- Original reference was inspected at full resolution.\n- The reconstructed PITF line has the same broad episodes but materially lower peaks because the source exposes categories, not Pinker's case-specific estimates.\n- The UCDP 1994 spike is close in timing and order of magnitude when using high-fatality estimates.\n- The extension is dashed and explicitly separated; it is a successor series, not a historical match.\n""")
    (FIG / "review_checklist.md").write_text("""# Review checklist\n\n- [x] Supplemental PDF reference inspected\n- [x] Caption and source note extracted\n- [x] Official PITF workbook downloaded\n- [x] Historical UCDP file downloaded\n- [x] Current successor searched and separated\n- [x] Legitimate source data used; no plotted values digitized\n- [x] Book-period plot generated\n- [x] Extended plot generated\n- [x] Side-by-side comparisons generated\n- [x] Visual discrepancies investigated\n- [x] Remaining discrepancies documented\n- [x] Status calibrated as `partial_match`\n- [ ] Exact Pinker PITF death estimates recovered\n- [ ] Exact cited population denominator recovered\n""")
    lineage = {"figure_id": "11-3", "status": "partial_match", "book_citation": "PITF 1955-2008 and UCDP 1989-2016", "original_dataset": "PITF_GenoPoliticide_2018.xls plus ucdp_onesided_14_2016.csv", "modern_dataset": "OneSided_v26_1.csv", "transformation_script": "scripts/reconstruct_11_3.py", "generated_plots": [str(p.relative_to(ROOT)) for p in plots.values()], "limitations": ["PITF DEATHMAG is ordinal", "Census/McEvedy denominator unrecovered", "historical UCDP version label differs"]}
    (FIG / "lineage/lineage.json").write_text(json.dumps(lineage, indent=2) + "\n")
    pd.DataFrame([{"stage": k, "artifact": v} for k, v in {"book_reference": "references/figures/figure_11_3.png", "pitf_raw": "figures/11-3/data/raw/PITF_GenoPoliticide_2018.xls", "ucdp_raw": "figures/11-3/data/raw/ucdp_onesided_14_2016.csv", "clean_book": "figures/11-3/data/clean/figure_11_3_book_period.csv", "clean_successor": "figures/11-3/data/clean/figure_11_3_successor.csv", "script": "scripts/reconstruct_11_3.py", "book_plot": "figures/11-3/plots/figure_11_3_book_period.png", "extended_plot": "figures/11-3/plots/figure_11_3_extended.png"}.items()]).to_csv(FIG / "lineage/lineage.csv", index=False)
    for doc in [FIG / "provenance/provenance.md", FIG / "source_logs/source_log.md", FIG / "lineage/lineage.csv"]:
        text = doc.read_text()
        text = text.replace("Historical UCDP one-sided CSV", "Historical UCDP one-sided workbook")
        text = text.replace("ucdp_onesided_14_2016.csv", "ucdp_onesided_171.xlsx")
        text = text.replace("v1.4-2016 CSV", "v17.1 workbook")
        text = text.replace("historical download center label", "historical download center labels")
        doc.write_text(text)
    lineage = {
        "schema_version": 1,
        "figure_id": "11-3",
        "book_citation": "PITF 1955-2008 and UCDP 1989-2016",
        "script": "scripts/reconstruct_11_3.py",
        "mappings": [
            {
                "role": "book_period",
                "raw_inputs": [
                    "figures/11-3/data/raw/PITF_GenoPoliticide_2018.xls",
                    "figures/11-3/data/raw/ucdp_onesided_171.xlsx",
                ],
                "selection": "PITF 1956-1988, then UCDP 1989-2016 high fatality estimates",
                "transformation": "decode PITF categories using documented arithmetic midpoints/lower bound; sum by year and divide by OWID World population",
                "clean": "figures/11-3/data/clean/figure_11_3_book_period.csv",
                "plot": "figures/11-3/plots/figure_11_3_book_period.png",
            },
            {
                "role": "extension",
                "raw_inputs": ["figures/11-3/data/raw/OneSided_v26_1.csv"],
                "selection": "UCDP v26.1 high fatality estimates, 2017-2023",
                "transformation": "sum by year and divide by OWID World population; render as dashed successor",
                "clean": "figures/11-3/data/clean/figure_11_3_successor.csv",
                "plot": "figures/11-3/plots/figure_11_3_extended.png",
            },
        ],
    }
    (FIG / "lineage/lineage.json").write_text(json.dumps(lineage, indent=2) + "\n")

    artifacts = {"metadata": {"path": "figures/11-3/figure.json", "self": True}, "original_reference": {"path": str(REF.relative_to(ROOT)), "sha256": sha256(REF)}, "book_period_reconstruction": {"path": str(plots["book"].relative_to(ROOT)), "sha256": sha256(plots["book"])}, "extended_reconstruction": {"path": str(plots["extended"].relative_to(ROOT)), "sha256": sha256(plots["extended"])}, "book_period_clean": {"path": "figures/11-3/data/clean/figure_11_3_book_period.csv", "sha256": sha256(CLEAN / "figure_11_3_book_period.csv")}, "successor_clean": {"path": "figures/11-3/data/clean/figure_11_3_successor.csv", "sha256": sha256(CLEAN / "figure_11_3_successor.csv")}}
    for role, path in {
        "caption": "figures/11-3/captions/caption.txt",
        "provenance": "figures/11-3/provenance/provenance.md",
        "source_log": "figures/11-3/source_logs/source_log.md",
        "anomaly_review": "figures/11-3/anomaly_reviews/anomaly_review.md",
        "discrepancy_log": "figures/11-3/discrepancy_logs/discrepancy_log.md",
        "review_checklist": "figures/11-3/review_checklist.md",
        "lineage": "figures/11-3/lineage/lineage.json",
        "lineage_csv": "figures/11-3/lineage/lineage.csv",
        "reconstruction_script": "scripts/reconstruct_11_3.py",
    }.items():
        artifacts[role] = {"path": path, "sha256": sha256(ROOT / path)}
    record = {"figure_id": "11-3", "title": "Genocide deaths, 1956-2016", "scientific_status": "partial_match", "source_status": "ordinal_PITF_data_and_historical_UCDP_recovered", "artifact_kind": "reconstruction", "publication_status": "not_reviewed", "execution_status": "processed", "lifecycle_stage": "visual_review", "next_action": "Recover Pinker's case-specific PITF estimates and cited population denominator.", "notes": "Official PITF and UCDP source-family data recovered; PITF is ordinal and cannot reproduce the published peaks exactly.", "extension": {"status": "comparable_successor", "label": "UCDP v26.1 successor"}, "visual_review": {"status": "pending", "reference_basis": "original", "issues": ["PITF category decode under-represents major peaks", "denominator vintage unresolved"]}, "artifacts": artifacts}
    (FIG / "figure.json").write_text(json.dumps(record, indent=2) + "\n")


def main() -> None:
    book, extension = load_series()
    plots = {"book": plot(book, extension, "book"), "extended": plot(book, extension, "extended")}
    write_docs(book, extension, plots)
    print(json.dumps({"figure": "11-3", "book_rows": len(book), "extension_rows": len(extension), "plots": {k: str(v) for k, v in plots.items()}}, indent=2))


if __name__ == "__main__":
    main()
