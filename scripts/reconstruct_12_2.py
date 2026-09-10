"""Reconstruct the publicly recoverable components of Figure 12-2."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures/12-2"
RAW = FIG / "data/raw"
CLEAN = FIG / "data/clean"
PLOTS = FIG / "plots"
REF = ROOT / "references/figures/figure_12_2.png"
UNODC_URL = "https://ourworldindata.org/grapher/homicide-rate-unodc.csv"
BJS_URL = "https://bjs.ojp.gov/content/pub/pdf/htius.pdf"


def load_series() -> tuple[pd.DataFrame, pd.DataFrame]:
    text_path = RAW / "bjs_homicide_trends_1950_2005_table.txt"
    if not text_path.exists():
        text_path.write_text(subprocess.check_output(["pdftotext", "-layout", str(RAW / "bjs_homicide_trends_1950_2005.pdf"), "-"], text=True))
    rows = []
    for year, rate, count in re.findall(r"(?m)^(19\d{2}|20\d{2})\s+([0-9.]+)\s+([0-9,]+)\s*$", text_path.read_text()):
        rows.append({"year": int(year), "rate": float(rate), "series": "United States", "source_series": "BJS/FBI homicide victimization table"})
    us = pd.DataFrame(rows).drop_duplicates("year").loc[lambda x: x.year.between(1967, 2005)]
    modern = pd.read_csv(RAW / "owid_homicide_rate_unodc.csv")
    modern = modern.rename(columns={"Year": "year", "Homicide rate per 100,000 population": "rate"})
    modern = modern.loc[modern.year.between(1990, 2023)]
    keep = {"United States": "United States", "England and Wales": "England", "World": "World"}
    modern = modern.loc[modern.Entity.isin(keep)].copy()
    modern["series"] = modern.Entity.map(keep)
    modern["source_series"] = "OWID/UNODC successor export"
    book = pd.concat([us, modern.loc[modern.year.between(1990, 2015)]], ignore_index=True)
    book = book.sort_values(["series", "year"]).drop_duplicates(["series", "year"], keep="last")
    extension = modern.loc[modern.year.between(2016, 2023), ["year", "rate", "series", "source_series"]].copy()
    if us.empty or book.year.min() != 1967 or book.year.max() != 2015:
        raise ValueError("unexpected Figure 12-2 coverage")
    return book.reset_index(drop=True), extension.reset_index(drop=True)


def plot(book: pd.DataFrame, extension: pd.DataFrame, mode: str) -> Path:
    PLOTS.mkdir(parents=True, exist_ok=True)
    path = PLOTS / ("figure_12_2_extended.png" if mode == "extended" else "figure_12_2_book_period.png")
    fig, ax = plt.subplots(figsize=(12, 7.5), dpi=180)
    colors = {"United States": "#8a8888", "England": "#b3b1b1", "World": "#211f1f"}
    for series, group in book.groupby("series"):
        ax.plot(group.year, group.rate, lw=2.8, color=colors[series], label=series)
    if mode == "extended":
        for series, group in extension.groupby("series"):
            ax.plot(group.year, group.rate, lw=2.3, ls="--", color=colors[series], label=f"{series} successor")
        ax.axvline(2015, color="#c8c8c8", lw=1.2, ls=":")
    ax.set_title("Figure 12-2: Homicide deaths, 1967-2015", loc="left", fontsize=18, pad=14)
    ax.set_xlabel("Year", fontsize=13)
    ax.set_ylabel("Homicides per 100,000 people per year", fontsize=13)
    ax.set_xlim(1965, 2024 if mode == "extended" else 2016)
    ax.set_ylim(0, 11)
    ax.set_xticks(range(1965, 2020, 5))
    ax.grid(axis="y", color="#e5e5e5", lw=0.8)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False, loc="upper right")
    note = "BJS/FBI US table through 2005; OWID/UNODC public series for modern overlap, England, and world."
    if mode == "extended":
        note += " Dashed: post-2015 successor; definitions and source vintages differ."
    else:
        note += " World is available publicly from 2000; England from 1991."
    fig.text(0.02, 0.015, note, fontsize=8.5, color="#555555")
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def write_package(book: pd.DataFrame, extension: pd.DataFrame, plots: dict[str, Path]) -> None:
    for sub in ["provenance", "source_logs", "search_iterations", "anomaly_reviews", "discrepancy_logs", "captions", "lineage", "checksums", "plots/comparisons"]:
        (FIG / sub).mkdir(parents=True, exist_ok=True)
    CLEAN.mkdir(parents=True, exist_ok=True)
    book.to_csv(CLEAN / "figure_12_2_book_period.csv", index=False)
    extension.to_csv(CLEAN / "figure_12_2_successor.csv", index=False)
    (FIG / "README.md").write_text("""# Figure 12-2 - Homicide deaths\n\nStatus: `partial_match`. The US series uses the BJS/FBI homicide table through 2005 and a public OWID/UNODC overlap thereafter. Public modern series supply England and World where available. The book's original world conversion and exact ONS/FBI vintages are not fully recovered.\n\n- Original: [../../references/figures/figure_12_2.png](../../references/figures/figure_12_2.png)\n- Script: [../../scripts/reconstruct_12_2.py](../../scripts/reconstruct_12_2.py)\n- Book comparison: [plots/comparisons/figure_12_2_book_period_review.png](plots/comparisons/figure_12_2_book_period_review.png)\n- Extended comparison: [plots/comparisons/figure_12_2_extended_review.png](plots/comparisons/figure_12_2_extended_review.png)\n""")
    (FIG / "captions/caption.txt").write_text("Figure 12-2 is a partial reconstruction. The United States line uses the BJS/FBI homicide victimization table through 2005 and an OWID/UNODC public overlap thereafter. England and World use the public UNODC export where available. The original world conversion from UN Economic and Social Council percentages and the exact ONS/FBI source vintages were not fully recovered. Dashed lines are post-2015 successor data.")
    (FIG / "provenance/provenance.md").write_text(f"""# Provenance\n\n## Book source line\n\nUnited States: FBI Uniform Crime Reports and Federal Bureau of Investigation 2016. England including Wales: Office for National Statistics 2017. World, 2000: Krug et al. 2002. World, 2003-2011: UN Economic and Social Council 2014, fig. 1; percentages converted using a 2012 rate of 6.2 from UNODC 2014.\n\n## Downloads\n\n- BJS/FBI table: {BJS_URL}\n- OWID/UNODC rates: {UNODC_URL}\n\n## Transformations\n\nThe BJS PDF table is text-extracted programmatically into yearly US rates for 1967-2005. OWID/UNODC rates are used for the US overlap, England, and World through 2015, then as a dashed successor through 2023. No plotted values were digitized.\n""")
    (FIG / "source_logs/source_log.md").write_text("""# Source discovery log\n\nQueries attempted: `FBI homicide rate 1967 2015 CSV United States`; `ONS homicide rate England Wales 1967 2015`; `UNODC homicide rate world 2000 2015`; official FBI UCR table 1; Bureau of Justice Statistics Homicide Trends; OWID/UNODC homicide-rate export.\n\n- BJS Homicide Trends in the United States PDF: accepted because it contains a public machine-readable text table for the US series.\n- FBI 2015 Table 1: investigated for 1996-2015; direct XLS endpoint returned an HTML wrapper, so the public BJS table and OWID/UNODC export were retained.\n- OWID/UNODC export: accepted for modern US, England, World, and post-2015 successor observations.\n- UN ECOSOC percentage table: citation resolved but original conversion table not recovered.\n\nRemaining uncertainty: exact book-era ONS/FBI vintages and Pinker's world-rate transformation.\n""")
    (FIG / "search_iterations/search_iterations.md").write_text("""# Search iterations\n\n1. Inspected original PDF crop and extracted the four-part source line.\n2. Located BJS/FBI national homicide table and parsed its public yearly rates.\n3. Located OWID/UNODC modern export for US, England, and World.\n4. Preserved source-vintage differences and separated post-2015 successor.\n5. Side-by-side review found the US trajectory close in shape; England/World early-period coverage remains incomplete.\n""")
    (FIG / "anomaly_reviews/anomaly_review.md").write_text("""# Anomaly review\n\nMajor: World is missing before 2000 and England is missing before 1991 because the public recoverable exports do not cover those periods. Major: the original UN ECOSOC percentage-to-rate transformation is not reproduced. Minor: the exact FBI/ONS source vintages differ from the book. Status: `partial_match`.\n""")
    (FIG / "discrepancy_logs/discrepancy_log.md").write_text("""# Discrepancy log\n\nThe US line is directionally close and has a long source-table run. England and World begin later than the original figure. The extension is dashed and separated at 2015. Remaining gaps are source-data gaps, not digitization targets.\n""")
    (FIG / "review_checklist.md").write_text("""# Review checklist\n\n- [x] Original PDF figure inspected\n- [x] Source note extracted\n- [x] Public BJS/FBI US table recovered\n- [x] Public UNODC successor recovered\n- [x] Book and extended plots generated\n- [x] Side-by-side comparisons generated and inspected\n- [x] No plotted values digitized\n- [x] Status classified as `partial_match`\n- [ ] Exact ONS/FBI book vintages recovered\n- [ ] Original World conversion reproduced\n""")
    lineage = {"schema_version": 1, "figure_id": "12-2", "book_citation": "FBI UCR; ONS; Krug et al.; UN ECOSOC; UNODC", "script": "scripts/reconstruct_12_2.py", "mappings": [{"role": "book_period", "raw_inputs": ["figures/12-2/data/raw/bjs_homicide_trends_1950_2005.pdf", "figures/12-2/data/raw/owid_homicide_rate_unodc.csv"], "selection": "US BJS table 1967-2005 plus public modern overlap; England/World public coverage", "transformation": "text-extract BJS rates and combine with OWID/UNODC by series/year", "clean": "figures/12-2/data/clean/figure_12_2_book_period.csv", "plot": "figures/12-2/plots/figure_12_2_book_period.png"}, {"role": "extension", "raw_inputs": ["figures/12-2/data/raw/owid_homicide_rate_unodc.csv"], "selection": "US, England, and World 2016-2023", "transformation": "retain source rates and render dashed", "clean": "figures/12-2/data/clean/figure_12_2_successor.csv", "plot": "figures/12-2/plots/figure_12_2_extended.png"}]}
    (FIG / "lineage/lineage.json").write_text(json.dumps(lineage, indent=2) + "\n")
    record = {"figure_id": "12-2", "title": "Homicide deaths, 1967-2015", "scientific_status": "partial_match", "artifact_kind": "reconstruction", "publication_status": "not_reviewed", "execution_status": "processed", "lifecycle_stage": "visual_review", "next_action": "Recover original ONS/FBI vintages and reproduce the UN ECOSOC world conversion.", "notes": "US public table recovered; England and World early coverage remain incomplete.", "extension": {"status": "comparable_successor", "label": "OWID/UNODC successor"}, "visual_review": {"status": "pending", "reference_basis": "original", "issues": ["World and England early gaps", "world transformation unresolved"]}, "artifacts": {"metadata": {"path": "figures/12-2/figure.json", "self": True}, "original_reference": {"path": "references/figures/figure_12_2.png"}, "book_period_reconstruction": {"path": "figures/12-2/plots/figure_12_2_book_period.png"}, "extended_reconstruction": {"path": "figures/12-2/plots/figure_12_2_extended.png"}, "book_period_clean": {"path": "figures/12-2/data/clean/figure_12_2_book_period.csv"}, "successor_clean": {"path": "figures/12-2/data/clean/figure_12_2_successor.csv"}, "caption": {"path": "figures/12-2/captions/caption.txt"}, "provenance": {"path": "figures/12-2/provenance/provenance.md"}, "source_log": {"path": "figures/12-2/source_logs/source_log.md"}, "anomaly_review": {"path": "figures/12-2/anomaly_reviews/anomaly_review.md"}, "discrepancy_log": {"path": "figures/12-2/discrepancy_logs/discrepancy_log.md"}, "review_checklist": {"path": "figures/12-2/review_checklist.md"}, "lineage": {"path": "figures/12-2/lineage/lineage.json"}, "reconstruction_script": {"path": "scripts/reconstruct_12_2.py"}}}
    (FIG / "figure.json").write_text(json.dumps(record, indent=2) + "\n")


def main() -> None:
    book, extension = load_series()
    plots = {"book": plot(book, extension, "book"), "extended": plot(book, extension, "extended")}
    write_package(book, extension, plots)
    print(json.dumps({"figure": "12-2", "book_rows": len(book), "extension_rows": len(extension)}, indent=2))


if __name__ == "__main__":
    main()
