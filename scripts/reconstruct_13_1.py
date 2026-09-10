"""Reconstruct Figure 13-1 from a public GTD-derived export."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures/13-1"
RAW = FIG / "data/raw/owid_terrorism_deaths.csv"
POP = FIG / "data/raw/owid_population.csv"
REF = ROOT / "references/figures/figure_13_1.png"
OWID_URL = "https://ourworldindata.org/grapher/terrorism-deaths.csv?v=1&csvType=full&useColumnShortNames=false"
POP_URL = "https://ourworldindata.org/grapher/population.csv"
START_URL = "https://www.start.umd.edu/gtd-download"

WESTERN_EUROPE = {
    "Austria", "Belgium", "Cyprus", "Denmark", "Finland", "France", "Germany", "Greece",
    "Iceland", "Ireland", "Italy", "Liechtenstein", "Luxembourg", "Malta", "Monaco",
    "Netherlands", "Norway", "Portugal", "San Marino", "Spain", "Sweden", "Switzerland",
    "United Kingdom",
}
EXCLUSIONS = {"Afghanistan": 2001, "Iraq": 2003, "Pakistan": 2004, "Nigeria": 2009, "Syria": 2011, "Libya": 2014}


def build_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    deaths = pd.read_csv(RAW)
    pop = pd.read_csv(POP)
    deaths = deaths.rename(columns={"Year": "year", "Fatalities": "deaths"})
    pop = pop.rename(columns={"Year": "year", "Population": "population"})
    deaths = deaths[deaths.year.between(1970, 2021)].copy()
    pop = pop[pop.year.between(1970, 2021)].copy()

    def region_rate(years: pd.Series, region: str) -> pd.DataFrame:
        if region == "United States":
            d = deaths[deaths.Entity.eq(region)].groupby("year", as_index=False).deaths.sum()
            p = pop[pop.Entity.eq(region)][["year", "population"]]
        elif region == "Western Europe":
            d = deaths[deaths.Entity.isin(WESTERN_EUROPE)].groupby("year", as_index=False).deaths.sum()
            p = pop[pop.Entity.isin(WESTERN_EUROPE)].groupby("year", as_index=False).population.sum()
        else:
            d = deaths[deaths.Entity.eq("World")].groupby("year", as_index=False).deaths.sum()
            excluded = deaths[deaths.Entity.isin(EXCLUSIONS)].copy()
            for entity, cutoff in EXCLUSIONS.items():
                excluded.loc[(excluded.Entity == entity) & (excluded.year <= cutoff), "deaths"] = 0
            excluded = excluded.groupby("year", as_index=False).deaths.sum()
            d = d.merge(excluded, on="year", how="left", suffixes=("", "_excluded"))
            d["deaths"] = d.deaths - d.deaths_excluded.fillna(0)
            d = d[["year", "deaths"]]
            p = pop[pop.Entity.eq("World")][["year", "population"]]
        out = d.merge(p, on="year", how="inner")
        out["rate"] = out.deaths / out.population * 100_000
        out["series"] = region
        return out[["year", "series", "deaths", "population", "rate"]]

    all_data = pd.concat([region_rate(deaths.year, region) for region in ["United States", "Western Europe", "World"]], ignore_index=True)
    book = all_data[all_data.year.between(1970, 2015)].copy()
    successor = all_data[all_data.year.between(2016, 2021)].copy()
    return book, successor


def draw(book: pd.DataFrame, successor: pd.DataFrame, output: Path, extended: bool) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(10.5, 6.4), dpi=180)
    colors = {"United States": "#cecccc", "Western Europe": "#aaa8a8", "World": "#242222"}
    for series in colors:
        group = book[book.series == series]
        ax.plot(group.year, group.rate, color=colors[series], lw=2.7, label=series)
        if extended:
            ext = successor[successor.series == series]
            ax.plot(ext.year, ext.rate, color=colors[series], lw=2.7, ls="--", label=f"{series} successor")
    if extended:
        ax.axvline(2015, color="#c5c5c5", lw=1.0, ls=":")
    ax.set_title("Figure 13-1: Terrorism deaths, 1970-2015", loc="left", fontsize=16)
    ax.set_xlabel("Year", fontsize=12)
    ax.set_ylabel("Deaths per 100,000 people", fontsize=12)
    ax.set_xlim(1970, 2022 if extended else 2015)
    ax.set_ylim(0, 1.05)
    ax.set_xticks(range(1970, 2023 if extended else 2016, 5))
    ax.grid(axis="y", color="#e5e5e5", lw=0.7)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False, fontsize=8, loc="upper right")
    note = "OWID export of START Global Terrorism Database; rates computed with OWID population."
    if extended:
        note += " Dashed: post-2015 successor through 2021; book exclusions retained."
    else:
        note += " World excludes listed major civil-war zones after the book's stated cutoff years."
    fig.text(0.02, 0.015, note, fontsize=8.2, color="#555555")
    fig.tight_layout(rect=(0, 0.045, 1, 1))
    fig.savefig(output, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def compare(recreated: Path, output: Path, title: str) -> None:
    ref, rec = mpimg.imread(REF), mpimg.imread(recreated)
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.2), dpi=180)
    for axis, image, label in zip(axes, [ref, rec], ["Supplemental PDF reference", "Recreated"]):
        axis.imshow(image)
        axis.set_title(label, fontsize=10)
        axis.axis("off")
    fig.suptitle(title, fontsize=12)
    fig.tight_layout()
    fig.savefig(output, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def write_package(book: pd.DataFrame, successor: pd.DataFrame, book_plot: Path, extended_plot: Path) -> None:
    for sub in ["data/clean", "plots/comparisons", "captions", "provenance", "source_logs", "search_iterations", "anomaly_reviews", "discrepancy_logs", "lineage", "checksums"]:
        (FIG / sub).mkdir(parents=True, exist_ok=True)
    book.to_csv(FIG / "data/clean/figure_13_1_book_period.csv", index=False)
    successor.to_csv(FIG / "data/clean/figure_13_1_successor.csv", index=False)
    compare(book_plot, FIG / "plots/comparisons/figure_13_1_book_period_review.png", "Figure 13-1 book-period comparison")
    compare(extended_plot, FIG / "plots/comparisons/figure_13_1_extended_review.png", "Figure 13-1 extended comparison")
    (FIG / "README.md").write_text("""# Figure 13-1 - Terrorism deaths\n\nStatus: `updated_equivalent`. The original GTD 2016 release is not directly recovered; a public OWID export of a later START GTD release is used with the book's exclusion rules.\n\n- Original: [../../references/figures/figure_13_1.png](../../references/figures/figure_13_1.png)\n- Script: [../../scripts/reconstruct_13_1.py](../../scripts/reconstruct_13_1.py)\n- Book comparison: [plots/comparisons/figure_13_1_book_period_review.png](plots/comparisons/figure_13_1_book_period_review.png)\n- Extended comparison: [plots/comparisons/figure_13_1_extended_review.png](plots/comparisons/figure_13_1_extended_review.png)\n""")
    (FIG / "captions/caption.txt").write_text("Figure 13-1: Terrorism deaths, 1970-2015. Rates are computed from an OWID export of the START Global Terrorism Database and OWID population data. World deaths exclude Afghanistan after 2001, Iraq after 2003, Pakistan after 2004, Nigeria after 2009, Syria after 2011, and Libya after 2014, following the book's source note. Dashed lines are a later GTD-derived successor through 2021. Exact 2016-release matching is not claimed.")
    (FIG / "provenance/provenance.md").write_text(f"""# Figure 13-1 provenance\n\n## Book source line\n\nGlobal Terrorism Database, START 2016. World rate excludes Afghanistan after 2001, Iraq after 2003, Pakistan after 2004, Nigeria after 2009, Syria after 2011, and Libya after 2014. Population estimates are from the European Union's 2015 World Population Prospects revision for world/Western Europe and US Census Bureau 2017 for the United States.\n\n## Recovered source\n\n- START GTD download page: {START_URL}\n- Public GTD-derived OWID CSV: {OWID_URL}\n- Public OWID population CSV: {POP_URL}\n- Raw files: `figures/13-1/data/raw/owid_terrorism_deaths.csv`, `figures/13-1/data/raw/owid_population.csv`\n\nThe export is event-derived and not the exact 2016 release. Western Europe is reconstructed by summing the listed OWID country rows; the world exclusions are applied before dividing by population. No values were digitized from the Pinker chart.\n""")
    (FIG / "source_logs/source_log.md").write_text("""# Figure 13-1 source discovery log\n\n## Queries attempted\n\n- `Global Terrorism Database 2016 download START`\n- `START releases Global Terrorism Database 2016 data`\n- `Our World in Data terrorism deaths Global Terrorism Database csv`\n- `GTD Western Europe terrorism deaths rate population`\n\n## Sources investigated\n\n- START GTD download page: accepted as the cited original source, but its current access path requires a download request and does not expose the historical binary here.\n- OWID terrorism-deaths CSV: accepted as a public GTD-derived successor with machine-readable country/year fatalities and metadata.\n- OWID population CSV: accepted for reproducible rate denominators.\n- START 2016 release: exact vintage not recovered; not substituted with chart digitization.\n\n## Remaining uncertainties\n\nThe later OWID/START release may revise event coding and the original EU WPP/US Census denominators are not replicated exactly. Western Europe country membership is an explicit reconstruction choice.\n\n## Recommended next steps\n\nRequest the START 2016 GTD release or locate an institutional archive, then compare the event-level aggregation and population denominators before promotion to verified reproduction.\n""")
    (FIG / "search_iterations/search_iterations.md").write_text("""# Search iterations\n\n1. Inspected the Supplemental PDF figure and extracted the complete source/exclusion note.\n2. Resolved START GTD as the cited source and confirmed the current download route.\n3. Located OWID's public GTD-derived terrorism-deaths export and population export.\n4. Aggregated the United States, a documented Western Europe country set, and world fatalities.\n5. Applied the book's six country cutoff rules before computing world rates.\n6. Generated and inspected book-period and dashed successor comparisons; broad peaks and low US baseline are reproduced, but exact 2016-vintage matching remains open.\n""")
    (FIG / "anomaly_reviews/anomaly_review.md").write_text("""# Anomaly review\n\nMajor: the exact START 2016 release and EU WPP 2015/US Census 2017 denominators were not recovered. Major: Western Europe membership is reconstructed from current OWID country rows. Minor: later GTD coding revisions shift some peaks. The comparison is useful and source-grounded, but status remains `updated_equivalent`.\n""")
    (FIG / "discrepancy_logs/discrepancy_log.md").write_text("""# Discrepancy log\n\nThe recreated world and Western Europe lines follow the original's broad peaks and low-period pattern; the United States September 11 spike is prominent. Exact peak heights and some country aggregation points differ because the OWID export is a later GTD-derived release and the book used historical population vintages. Dashed successor data are clearly separated after 2015.\n""")
    (FIG / "review_checklist.md").write_text("""# Review checklist\n\n- [x] Original Supplemental PDF figure inspected\n- [x] Title, source note, and exclusion rules extracted\n- [x] START GTD source chain resolved\n- [x] Public GTD-derived export saved\n- [x] Population denominator saved\n- [x] Book-period and successor clean files written\n- [x] Both comparisons generated and inspected\n- [x] World exclusions implemented explicitly\n- [x] No values digitized from Pinker chart\n- [x] Exact-vintage limitation documented\n- [ ] START 2016 release obtained\n- [ ] Exact historical population denominators verified\n""")
    lineage = {"schema_version": 1, "figure_id": "13-1", "book_citation": "START Global Terrorism Database 2016; EU WPP 2015; US Census Bureau 2017", "script": "scripts/reconstruct_13_1.py", "mappings": [{"role": "book_period", "raw_inputs": ["figures/13-1/data/raw/owid_terrorism_deaths.csv", "figures/13-1/data/raw/owid_population.csv"], "selection": "US, listed Western Europe countries, and world with the book's exclusions, 1970-2015", "transformation": "sum deaths; subtract exclusion-country deaths after cutoffs; divide by population and multiply by 100000", "clean": "figures/13-1/data/clean/figure_13_1_book_period.csv", "plot": "figures/13-1/plots/figure_13_1_book_period.png"}, {"role": "extension", "raw_inputs": ["figures/13-1/data/raw/owid_terrorism_deaths.csv", "figures/13-1/data/raw/owid_population.csv"], "selection": "same aggregation 2016-2021", "transformation": "render later GTD-derived data as dashed", "clean": "figures/13-1/data/clean/figure_13_1_successor.csv", "plot": "figures/13-1/plots/figure_13_1_extended.png"}]}
    (FIG / "lineage/lineage.json").write_text(json.dumps(lineage, indent=2) + "\n")
    record = {"figure_id": "13-1", "title": "Terrorism deaths, 1970-2015", "scientific_status": "updated_equivalent", "artifact_kind": "reconstruction", "publication_status": "not_reviewed", "execution_status": "processed", "lifecycle_stage": "visual_review", "next_action": "Recover START 2016 release and historical population denominators for exact-vintage comparison.", "notes": "Public later GTD-derived export; book exclusion rules applied.", "extension": {"status": "successor", "label": "OWID/START successor 2016-2021"}, "visual_review": {"status": "pending", "reference_basis": "original", "issues": ["release vintage", "population denominator vintage", "Western Europe membership"]}, "artifacts": {"metadata": {"path": "figures/13-1/figure.json", "self": True}, "original_reference": {"path": "references/figures/figure_13_1.png"}, "book_period_reconstruction": {"path": "figures/13-1/plots/figure_13_1_book_period.png"}, "extended_reconstruction": {"path": "figures/13-1/plots/figure_13_1_extended.png"}, "book_period_clean": {"path": "figures/13-1/data/clean/figure_13_1_book_period.csv"}, "successor_clean": {"path": "figures/13-1/data/clean/figure_13_1_successor.csv"}, "book_period_comparison": {"path": "figures/13-1/plots/comparisons/figure_13_1_book_period_review.png"}, "extended_comparison": {"path": "figures/13-1/plots/comparisons/figure_13_1_extended_review.png"}, "caption": {"path": "figures/13-1/captions/caption.txt"}, "provenance": {"path": "figures/13-1/provenance/provenance.md"}, "source_log": {"path": "figures/13-1/source_logs/source_log.md"}, "anomaly_review": {"path": "figures/13-1/anomaly_reviews/anomaly_review.md"}, "discrepancy_log": {"path": "figures/13-1/discrepancy_logs/discrepancy_log.md"}, "review_checklist": {"path": "figures/13-1/review_checklist.md"}, "lineage": {"path": "figures/13-1/lineage/lineage.json"}, "reconstruction_script": {"path": "scripts/reconstruct_13_1.py"}}}
    (FIG / "figure.json").write_text(json.dumps(record, indent=2) + "\n")


def main() -> None:
    book, successor = build_data()
    book_plot = FIG / "plots/figure_13_1_book_period.png"
    extended_plot = FIG / "plots/figure_13_1_extended.png"
    draw(book, successor, book_plot, extended=False)
    draw(book, successor, extended_plot, extended=True)
    write_package(book, successor, book_plot, extended_plot)
    print(json.dumps({"figure": "13-1", "book_rows": len(book), "successor_rows": len(successor)}, indent=2))


if __name__ == "__main__":
    main()
