"""Partial reconstruction of Figure 12-1 from public homicide-rate releases.

The historical European series are the current OWID import of Eisner/WHO data;
UNODC supplies a public modern series for Mexico and later overlap. Roth's New
England and Southwest US observations and the historical personal-communication
Mexico series are deliberately not invented.
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures/12-1"
RAW = FIG / "data/raw"
CLEAN = FIG / "data/clean"
PLOTS = FIG / "plots"
REF = ROOT / "references/figures/figure_12_1.png"

WESTERN_URL = "https://ourworldindata.org/grapher/homicide-rates-across-western-europe.csv"
UNODC_URL = "https://ourworldindata.org/grapher/homicide-rate-unodc.csv"


def load_series() -> tuple[pd.DataFrame, pd.DataFrame]:
    western = pd.read_csv(RAW / "owid_homicide_rates_western_europe.csv")
    value = western.columns[-1]
    western = western.rename(columns={value: "rate"})
    wanted = western.loc[western.Entity.isin(["England and Wales", "Italy", "Netherlands", "Belgium"]), ["Entity", "Year", "rate"]].copy()
    wanted["rate"] = pd.to_numeric(wanted["rate"], errors="coerce")
    england = wanted.loc[wanted.Entity.eq("England and Wales"), ["Year", "rate"]].rename(columns={"Year": "year"})
    england["series"] = "England"
    italy = wanted.loc[wanted.Entity.eq("Italy"), ["Year", "rate"]].rename(columns={"Year": "year"})
    italy["series"] = "Italy"
    benelux = wanted.loc[wanted.Entity.isin(["Netherlands", "Belgium"])].groupby("Year", as_index=False).rate.mean().rename(columns={"Year": "year"})
    benelux["series"] = "Netherlands & Belgium"

    modern = pd.read_csv(RAW / "owid_homicide_rate_unodc.csv")
    modern_value = "Homicide rate per 100,000 population"
    modern = modern.rename(columns={"Year": "year", modern_value: "rate"})
    mexico = modern.loc[modern.Entity.eq("Mexico"), ["year", "rate"]].copy()
    mexico["series"] = "Mexico"
    # Current UNODC/OWID overlap is used for the book-era Mexico line; the
    # pre-1990 personal-communication series remains unrecovered.
    book = pd.concat([england, italy, benelux, mexico], ignore_index=True)
    book = book.loc[book.year.between(1300, 2015)].sort_values(["series", "year"]).reset_index(drop=True)

    extension = modern.loc[modern.Entity.isin(["Mexico", "Italy", "Netherlands", "Belgium", "England and Wales"]), ["Entity", "year", "rate"]].copy()
    extension["series"] = extension["Entity"].replace({"England and Wales": "England", "Netherlands": "Netherlands & Belgium", "Belgium": "Netherlands & Belgium"})
    extension = extension.loc[extension.year.between(2016, 2023)].drop(columns="Entity")
    extension = extension.groupby(["series", "year"], as_index=False).rate.mean()
    return book, extension


def plot(book: pd.DataFrame, extension: pd.DataFrame, mode: str) -> Path:
    PLOTS.mkdir(parents=True, exist_ok=True)
    path = PLOTS / ("figure_12_1_extended.png" if mode == "extended" else "figure_12_1_book_period.png")
    fig, ax = plt.subplots(figsize=(12, 7.5), dpi=180)
    colors = {"England": "#d2d0d0", "Netherlands & Belgium": "#aaa8aa", "Italy": "#777777", "Mexico": "#171515"}
    for series, group in book.groupby("series"):
        ax.plot(group.year, group.rate, lw=2.8, color=colors[series], label=series)
    if mode == "extended" and not extension.empty:
        for series, group in extension.groupby("series"):
            ax.plot(group.year, group.rate, lw=2.3, ls="--", color=colors.get(series, "#555555"), label=f"{series} successor")
        ax.axvline(2015, color="#c8c8c8", lw=1.2, ls=":")
    ax.set_title("Figure 12-1: Homicide deaths, Western Europe, US, and Mexico, 1300-2015", loc="left", fontsize=15, pad=14)
    ax.set_xlabel("Year", fontsize=13)
    ax.set_ylabel("Homicides per 100,000 people per year", fontsize=13)
    ax.set_xlim(1300, 2024 if mode == "extended" else 2016)
    ax.set_ylim(0, 200)
    ax.set_xticks([1300, 1350, 1400, 1450, 1500, 1550, 1600, 1650, 1700, 1750, 1800, 1850, 1900, 1950, 2000])
    ax.grid(axis="y", color="#e5e5e5", lw=0.8)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False, loc="upper right")
    note = "Reproduced public components: OWID Eisner/WHO historical European rates; UNODC/OWID Mexico overlap."
    if mode == "extended":
        note += " Dashed: post-2015 UNODC successor; Roth US regional series remain unavailable."
    else:
        note += " Roth New England/Southwest US and pre-1990 Mexico components unavailable."
    fig.text(0.02, 0.015, note, fontsize=8.3, color="#555555")
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def write_package(book: pd.DataFrame, extension: pd.DataFrame, plots: dict[str, Path]) -> None:
    for sub in ["provenance", "source_logs", "search_iterations", "anomaly_reviews", "discrepancy_logs", "captions", "lineage", "checksums", "plots/comparisons"]:
        (FIG / sub).mkdir(parents=True, exist_ok=True)
    CLEAN.mkdir(parents=True, exist_ok=True)
    book.to_csv(CLEAN / "figure_12_1_book_period.csv", index=False)
    extension.to_csv(CLEAN / "figure_12_1_successor.csv", index=False)
    (FIG / "captions/caption.txt").write_text("Figure 12-1 is a partial reconstruction from publicly recoverable source components. The European historical lines use the current OWID import of Eisner and WHO data; Mexico uses UNODC data where available. Roth's New England and Southwest US series and the pre-1990 Mexico personal-communication series were not recovered and are not fabricated. Dashed lines in the extended view are post-2015 UNODC successors.")
    (FIG / "provenance/provenance.md").write_text(f"""# Provenance\n\n## Book source line\n\nEngland, Netherlands & Belgium, Italy, 1300-1994: Eisner 2003, plotted in fig. 3-3 of Pinker 2011. England, 2000-2014: UK Office for National Statistics. Italy and Netherlands, 2010-2012: United Nations Office on Drugs and Crime 2014. New England and Southwest US: Roth 2009, plotted in figs. 3-13 and 3-16 of Pinker 2011. Mexico: Carlos Vilalta, personal communication, originally from INEGI 2016 and Botello 2016.\n\n## Downloaded public data\n\n- OWID historical Europe import: {WESTERN_URL}\n- OWID/UNODC current rates: {UNODC_URL}\n\n## Transformation\n\nThe OWID Europe table is filtered to England and Wales, Italy, Netherlands, and Belgium. Netherlands and Belgium are averaged by year as a transparent approximation to the original combined line. Mexico is retained from the UNODC series from 1990 onward. Modern post-2015 data are separate dashed successor series. No values were digitized from Pinker's plot.\n""")
    (FIG / "source_logs/source_log.md").write_text("""# Source discovery log\n\nQueries attempted: `Eisner 2003 homicide rates England Netherlands Belgium Italy data`; `Pinker figure 12-1 homicide source data`; `Our World in Data homicide rates western Europe`; `UNODC homicide rate Mexico`; official ONS homicide tables; FBI Uniform Crime Reports; Roth 2009 homicide data.\n\n- OWID homicide-rates-across-western-europe.csv: accepted as a public modern import of Eisner historical rates plus WHO data.\n- OWID homicide-rate-unodc.csv: accepted for modern Mexico and post-2015 successor observations.\n- Eisner 2003 paper: accepted as the original publication context; its plotted local estimates are not treated as machine-readable values.\n- ONS, FBI, and UNODC original tables: investigated; current OWID/UNODC export was retained as the reproducible download for the recoverable modern overlap.\n- Roth 2009 New England and Southwest US series: source citation resolved, numeric data not recovered.\n- Vilalta/INEGI/Botello Mexico pre-1990 series: source citation resolved, numeric data not recovered.\n\nRemaining uncertainty: the original combined-region calculations and Roth series cannot be reproduced from the presently downloaded public files.\n""")
    (FIG / "search_iterations/search_iterations.md").write_text("""# Search iterations\n\n1. Inspected original PDF crop and transcribed its component source line.\n2. Located OWID's public Eisner/WHO historical Europe export.\n3. Located OWID's UNODC current export for Mexico and successors.\n4. Tested the cited ONS/FBI/Roth/Vilalta paths; retained unresolved components as explicit gaps.\n5. Side-by-side review confirms the recovered European decline is directionally consistent, but the missing US regional and pre-1990 Mexico curves make the result partial.\n""")
    (FIG / "anomaly_reviews/anomaly_review.md").write_text("""# Anomaly review\n\nMajor: New England and Southwest US curves are absent because Roth 2009 numeric data were not recovered. Major: Mexico is absent before 1990, and the original personal-communication series is unavailable. Minor: Netherlands and Belgium are averaged from separate OWID country rows; this is not proven identical to Pinker's combined historical line. Modern dashed extensions use successor definitions. Status: `partial_match`.\n""")
    (FIG / "discrepancy_logs/discrepancy_log.md").write_text("""# Discrepancy log\n\nThe original has five labelled components and recovered output has four. The recovered European trajectories occupy the expected historical range and decline, but cannot visually match missing US regional lines or the early Mexico segment. These discrepancies are data-availability gaps, not digitization targets.\n""")
    (FIG / "review_checklist.md").write_text("""# Review checklist\n\n- [x] Original PDF figure inspected\n- [x] Caption and source note extracted\n- [x] Public historical European data located\n- [x] Public UNODC/Mexico data located\n- [x] Source log and provenance written\n- [x] Book-period plot generated\n- [x] Extended plot generated\n- [x] Side-by-side comparisons generated\n- [x] Missing series documented\n- [x] No plotted values digitized\n- [x] Status classified as `partial_match`\n- [ ] Roth New England/Southwest US data recovered\n- [ ] Original Mexico pre-1990 series recovered\n""")
    lineage = {"schema_version": 1, "figure_id": "12-1", "book_citation": "Eisner 2003; ONS; UNODC; Roth 2009; Vilalta/INEGI/Botello", "script": "scripts/reconstruct_12_1.py", "mappings": [{"role": "book_period", "raw_inputs": ["figures/12-1/data/raw/owid_homicide_rates_western_europe.csv", "figures/12-1/data/raw/owid_homicide_rate_unodc.csv"], "selection": "European historical lines and Mexico 1990-2015 public overlap", "transformation": "filter series, average Netherlands/Belgium, retain rates", "clean": "figures/12-1/data/clean/figure_12_1_book_period.csv", "plot": "figures/12-1/plots/figure_12_1_book_period.png"}, {"role": "extension", "raw_inputs": ["figures/12-1/data/raw/owid_homicide_rate_unodc.csv"], "selection": "post-2015 UNODC successor through 2023", "transformation": "filter and average Netherlands/Belgium; dashed styling", "clean": "figures/12-1/data/clean/figure_12_1_successor.csv", "plot": "figures/12-1/plots/figure_12_1_extended.png"}]}
    (FIG / "lineage/lineage.json").write_text(json.dumps(lineage, indent=2) + "\n")
    (FIG / "figure.json").write_text(json.dumps({"figure_id": "12-1", "title": "Homicide deaths, Western Europe, US, and Mexico, 1300-2015", "scientific_status": "partial_match", "artifact_kind": "reconstruction", "publication_status": "not_reviewed", "execution_status": "processed", "lifecycle_stage": "visual_review", "next_action": "Recover Roth 2009 regional series and historical Mexico component.", "notes": "Public European and UNODC components reproduced; original US regional and early Mexico components remain missing.", "extension": {"status": "comparable_successor", "label": "UNODC successor"}, "visual_review": {"status": "pending", "reference_basis": "original", "issues": ["Missing Roth regional curves", "Missing pre-1990 Mexico"]}, "artifacts": {"metadata": {"path": "figures/12-1/figure.json", "self": True}, "original_reference": {"path": "references/figures/figure_12_1.png"}, "book_period_reconstruction": {"path": "figures/12-1/plots/figure_12_1_book_period.png"}, "extended_reconstruction": {"path": "figures/12-1/plots/figure_12_1_extended.png"}, "book_period_clean": {"path": "figures/12-1/data/clean/figure_12_1_book_period.csv"}, "successor_clean": {"path": "figures/12-1/data/clean/figure_12_1_successor.csv"}, "caption": {"path": "figures/12-1/captions/caption.txt"}, "provenance": {"path": "figures/12-1/provenance/provenance.md"}, "source_log": {"path": "figures/12-1/source_logs/source_log.md"}, "anomaly_review": {"path": "figures/12-1/anomaly_reviews/anomaly_review.md"}, "discrepancy_log": {"path": "figures/12-1/discrepancy_logs/discrepancy_log.md"}, "review_checklist": {"path": "figures/12-1/review_checklist.md"}, "lineage": {"path": "figures/12-1/lineage/lineage.json"}, "reconstruction_script": {"path": "scripts/reconstruct_12_1.py"}}}, indent=2) + "\n")


def main() -> None:
    book, extension = load_series()
    plots = {"book": plot(book, extension, "book"), "extended": plot(book, extension, "extended")}
    write_package(book, extension, plots)
    print(json.dumps({"figure": "12-1", "book_rows": len(book), "extension_rows": len(extension), "plots": {k: str(v) for k, v in plots.items()}}, indent=2))


if __name__ == "__main__":
    main()
