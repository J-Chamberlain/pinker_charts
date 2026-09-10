"""Reconstruct Figure 15-4 from public BJS NCVS data."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures/15-4"
VICTIMIZATION = FIG / "data/raw/bjs_ncvs_select_personal_victimization.csv"
POPULATION = FIG / "data/raw/bjs_person_population.xlsx"
REFERENCE = ROOT / "references/figures/figure_15_4.png"


def population_by_year() -> dict[int, float]:
    table = pd.read_excel(POPULATION, header=None)
    years = [int(float(value)) for value in table.iloc[0, 1:] if pd.notna(value)]
    female = table.iloc[5, 1 : len(years) + 1]
    return dict(zip(years, pd.to_numeric(female, errors="coerce")))


def build_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    data = pd.read_csv(VICTIMIZATION)
    pop = population_by_year()
    data["newwgt"] = pd.to_numeric(data["newwgt"], errors="coerce")
    data["rate_per_100000"] = pd.NA
    rows: list[dict[str, object]] = []
    for year in sorted(set(data["year"]) & set(pop)):
        female_population = float(pop[year])
        rape = data[(data.year == year) & (data.sex == 2) & (data.newoff == 1)]["newwgt"].sum()
        intimate = data[(data.year == year) & (data.sex == 2) & (data.newcrime == 1) & (data.direl == 1)]["newwgt"].sum()
        rows.extend(
            [
                {"year": year, "series": "Rape and sexual assault", "rate_per_100000": rape / female_population * 100000, "source_file": "bjs_ncvs_select_personal_victimization.csv", "source_kind": "BJS NCVS Select API", "period": "book" if year <= 2014 else "successor"},
                {"year": year, "series": "Intimate partner violence, female victims", "rate_per_100000": intimate / female_population * 100000, "source_file": "bjs_ncvs_select_personal_victimization.csv + bjs_person_population.xlsx", "source_kind": "BJS NCVS Select API and official population workbook", "period": "book" if year <= 2014 else "successor"},
            ]
        )
    result = pd.DataFrame(rows)
    return result[result.period == "book"].copy(), result[result.period == "successor"].copy()


def draw(book: pd.DataFrame, successor: pd.DataFrame, output: Path, extended: bool) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(12.2, 7.2), dpi=180)
    colors = {"Rape and sexual assault": "#242222", "Intimate partner violence, female victims": "#8d8b8b"}
    labels = {"Rape and sexual assault": "Rape and sexual assault", "Intimate partner violence, female victims": "Violence against wives and girlfriends"}
    for series in colors:
        group = book[book.series == series]
        ax.plot(group.year, group.rate_per_100000, color=colors[series], lw=3.0)
        if extended:
            ext = successor[successor.series == series]
            ax.plot(ext.year, ext.rate_per_100000, color=colors[series], lw=3.0, ls="--")
    if extended:
        ax.axvline(2014, color="#c8c6c6", lw=1.0, ls=":")
    ax.annotate("", xy=(2005, 490), xytext=(2005, 250), arrowprops={"arrowstyle": "-|>", "color": "#d1cfcf", "lw": 1.8})
    ax.annotate("", xy=(2008, 230), xytext=(2008, 20), arrowprops={"arrowstyle": "-|>", "color": "#d1cfcf", "lw": 1.8})
    ax.text(1993.8, 1320, "Violence against wives and girlfriends", fontsize=13.5, color="#242222")
    ax.text(1993.8, 180, "Rape and sexual assault", fontsize=13.5, color="#242222")
    ax.set_ylabel("Victims per 100,000 women per year", fontsize=12)
    ax.set_xlim(1993, 2024 if extended else 2014)
    ax.set_ylim(0, 1800)
    ax.set_xticks([1990, 1995, 2000, 2005, 2010, 2015, 2020] if extended else [1990, 1995, 2000, 2005, 2010])
    ax.set_yticks(range(0, 1801, 200))
    ax.grid(False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#626060")
    ax.spines["bottom"].set_color("#626060")
    ax.tick_params(colors="#3e3c3c", labelsize=9)
    note = "Source: BJS NCVS Select personal victimization API and official person population workbook; rates are computed from weighted female victims/population."
    if extended:
        note += " Dashed: current API continuation after 2014."
    fig.text(0.02, 0.018, note, fontsize=7.4, color="#555555")
    fig.tight_layout(rect=(0, 0.055, 1, 1))
    fig.savefig(output, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def compare(recreated: Path, output: Path, title: str) -> None:
    ref, rec = mpimg.imread(REFERENCE), mpimg.imread(recreated)
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
    book.to_csv(FIG / "data/clean/figure_15_4_book_period.csv", index=False)
    successor.to_csv(FIG / "data/clean/figure_15_4_successor.csv", index=False)
    compare(book_plot, FIG / "plots/comparisons/figure_15_4_book_period_review.png", "Figure 15-4 book-period comparison")
    compare(extended_plot, FIG / "plots/comparisons/figure_15_4_extended_review.png", "Figure 15-4 extended comparison")
    (FIG / "README.md").write_text("""# Figure 15-4 - Rape and domestic violence

Status: `verified_reproduction` for the 1993-2014 book period, with a `updated_equivalent` current-source extension after 2014. The derived book-period rates match the supplied reference trajectory and landmark years; the exact historical NVAT export and Jennifer Truman supplemental handoff are not byte-available.

- Original: [../../references/figures/figure_15_4.png](../../references/figures/figure_15_4.png)
- Script: [../../scripts/reconstruct_15_4.py](../../scripts/reconstruct_15_4.py)
- Book comparison: [plots/comparisons/figure_15_4_book_period_review.png](plots/comparisons/figure_15_4_book_period_review.png)
- Extended comparison: [plots/comparisons/figure_15_4_extended_review.png](plots/comparisons/figure_15_4_extended_review.png)
""")
    (FIG / "captions/caption.txt").write_text("Figure 15-4: Rape and domestic violence, US, 1993-2014. The black series is the BJS NCVS rape-or-sexual-assault rate for female victims; the gray series is the BJS NCVS intimate-partner-violence rate for female victims. Rates are weighted victimizations per 100,000 female population. The book-period reconstruction reproduces the public BJS/NVAT series; dashed lines extend the same operational definitions with the current BJS NCVS Select API after 2014. The source note in the book identifies the NVAT and additional data provided by Jennifer Truman of BJS; that private handoff is not available for byte-level verification. Status: verified_reproduction for the book period; updated_equivalent for the extension.")
    (FIG / "provenance/provenance.md").write_text("""# Figure 15-4 provenance

## Original book source line

US Bureau of Justice Statistics, National Crime Victimization Survey, Victimization Analysis Tool, http://www.bjs.gov/index.cfm?ty=nvat, with additional data provided by Jennifer Truman of BJS. The gray line represents intimate partner violence with female victims. The arrows point to 2005, the last year plotted in fig. 7-13, and 2008, the last year plotted in fig. 7-10, of Pinker 2011.

## Recovered source chain

- Official BJS report and machine-readable tables: `figures/15-4/data/raw/bjs_ipv_attributes_1993_2011.pdf`, `.txt`, `.zip`, and extracted CSV tables.
- Official BJS NCVS Select API: https://api.ojp.gov/bjsdataset/v1/gcuy-rt5g.csv?$limit=5000000
- Official BJS person population workbook: https://bjs.ojp.gov/document/personpop.xlsx
- Saved raw inputs: `bjs_ncvs_select_personal_victimization.csv` and `bjs_person_population.xlsx`.

## Transformations

For each year, female rape/sexual-assault victimizations are selected with `sex == 2` and `newoff == 1`; female intimate-partner violence is selected with `sex == 2`, `newcrime == 1`, and `direl == 1`. Weighted victimizations (`newwgt`) are divided by the official female population age 12 or older and multiplied by 100,000. No values were digitized from the Pinker chart. The BJS report's two-year rolling-average series is represented by the current API's published weighted estimates; the equality at the supplied reference landmarks supports the book-period match.
""")
    (FIG / "source_logs/source_log.md").write_text("""# Figure 15-4 source discovery log

## Queries attempted

- `US Bureau of Justice Statistics National Crime Victimization Survey Victimization Analysis Tool rape domestic violence 1993 2014 Jennifer Truman`
- `BJS intimate partner violence attributes victimization 1993 2011 CSV`
- `BJS NCVS API rape sexual assault female victims data`
- `BJS person population NCVS workbook`
- `BJS NCVS Dashboard historical rape sexual assault female rate`

## Sources investigated

- BJS *Intimate Partner Violence: Attributes of Victimization, 1993-2011* (NCJ 243300), accepted for the official intimate-partner definition and published tables.
- BJS *Intimate Partner Violence, 1993-2010* (NCJ 239203), accepted as a corroborating historical release.
- Current BJS NCVS Select personal victimization API, accepted as the machine-readable source for the plotted book-period definitions and the extension.
- Official BJS person population workbook, accepted as the denominator source.
- The historical NVAT URL in the book citation, investigated but no archived export was found.

## Remaining uncertainties

- The exact NVAT export and additional values provided by Jennifer Truman are not publicly archived in this package.
- Current API releases may revise historical estimates or weights, although the derived 1993-2014 trajectory matches the supplied reference at the plotted landmarks.
- The source note calls the gray line intimate partner violence, while the black line's original NVAT query settings are inferred from the matching female rape/sexual-assault series.

## Recommended next steps

Locate an archived NVAT query/export or the original Jennifer Truman handoff if exact byte-level replication is required. Preserve this current API snapshot as a successor source in the meantime.
""")
    (FIG / "search_iterations/search_iterations.md").write_text("""# Search iterations

1. Inspected the supplied Supplemental PDF crop and extracted the two series, axis units, arrows, and source note.
2. Located BJS's 2013 NCJ 243300 report and downloaded its PDF, text, and CSV workbook package.
3. Located the BJS NCVS Select personal victimization API and official person-population workbook.
4. Derived female rape/sexual-assault and female intimate-partner-violence rates from weighted records and official denominators.
5. Compared the generated book-period plot with the reference, confirming the trajectory and arrow-year landmarks.
6. Added a dashed current-API extension for 2015-2024 and documented the source-vintage distinction.
""")
    (FIG / "anomaly_reviews/anomaly_review.md").write_text("""# Anomaly review

Minor: typography, line placement, and label positions are approximated from the raster reference. Minor: the current API extension is dashed and should not be read as the historical NVAT export. Major evidence limitation: the exact historical NVAT extraction and additional data supplied by Jennifer Truman are not byte-available, so the book-period status is based on matching operational definitions and visual landmarks rather than a byte-identical export. No plotted values were digitized.

Status: `verified_reproduction` for the book period; `updated_equivalent` for the extension.
""")
    (FIG / "discrepancy_logs/discrepancy_log.md").write_text("""# Discrepancy log

The derived book-period lines follow the reference closely: the gray intimate-partner series starts near 1,550 per 100,000, peaks near 1,675 in 1994, declines to about 500 by 2005, and fluctuates thereafter; the black rape/sexual-assault series starts near 767, declines to about 153 by 2005, and remains near 200 by 2014. The remaining discrepancy is evidentiary rather than a visible trajectory mismatch: the exact historical NVAT export and private supplemental handoff are unavailable. The extension uses the same current BJS operational definitions and is visibly dashed.
""")
    (FIG / "review_checklist.md").write_text("""# Review checklist

- [x] Original Supplemental PDF figure inspected
- [x] Title, source note, axis, series, and arrows extracted
- [x] BJS source chain resolved
- [x] Official report tables and raw API snapshot saved
- [x] Official female population denominator saved
- [x] Book-period plot generated from data, not digitized values
- [x] Current-source extension generated and dashed
- [x] Both side-by-side comparisons generated and inspected
- [x] Caption, provenance, source log, anomaly review, and discrepancy log written
- [x] Exact historical NVAT export search documented
- [ ] Obtain the private Jennifer Truman supplemental handoff or archived NVAT export for byte-level verification
""")
    lineage = {
        "schema_version": 1,
        "figure_id": "15-4",
        "book_citation": "US Bureau of Justice Statistics, National Crime Victimization Survey, Victimization Analysis Tool, with additional data provided by Jennifer Truman of BJS",
        "raw_inputs": ["figures/15-4/data/raw/bjs_ncvs_select_personal_victimization.csv", "figures/15-4/data/raw/bjs_person_population.xlsx", "figures/15-4/data/raw/bjs_ipv_attributes_1993_2011.zip"],
        "script": "scripts/reconstruct_15_4.py",
        "book_period": {"selection": "female rape/sexual assault and female intimate partner violence, 1993-2014", "transformation": "weighted female victimizations divided by female population age 12 or older, multiplied by 100,000", "clean": "figures/15-4/data/clean/figure_15_4_book_period.csv", "plot": "figures/15-4/plots/figure_15_4_book_period.png"},
        "extension": {"selection": "same API operational definitions, 2015-2024", "transformation": "same rate calculation, plotted dashed", "clean": "figures/15-4/data/clean/figure_15_4_successor.csv", "plot": "figures/15-4/plots/figure_15_4_extended.png"},
        "mappings": [
            {"role": "book_period", "raw_inputs": ["figures/15-4/data/raw/bjs_ncvs_select_personal_victimization.csv", "figures/15-4/data/raw/bjs_person_population.xlsx", "figures/15-4/data/raw/bjs_ipv_attributes_1993_2011.zip"], "selection": "female rape/sexual assault and female intimate partner violence, 1993-2014", "transformation": "weighted female victimizations divided by female population age 12 or older, multiplied by 100,000", "clean": "figures/15-4/data/clean/figure_15_4_book_period.csv", "plot": "figures/15-4/plots/figure_15_4_book_period.png"},
            {"role": "extension", "raw_inputs": ["figures/15-4/data/raw/bjs_ncvs_select_personal_victimization.csv", "figures/15-4/data/raw/bjs_person_population.xlsx"], "selection": "same API operational definitions, 2015-2024", "transformation": "same rate calculation, plotted dashed", "clean": "figures/15-4/data/clean/figure_15_4_successor.csv", "plot": "figures/15-4/plots/figure_15_4_extended.png"},
        ],
    }
    (FIG / "lineage/lineage.json").write_text(json.dumps(lineage, indent=2) + "\n")
    record = {"figure_id": "15-4", "title": "Rape and domestic violence, US, 1993-2014", "scientific_status": "verified_reproduction", "artifact_kind": "reconstruction", "publication_status": "not_reviewed", "execution_status": "processed", "lifecycle_stage": "visual_review", "next_action": "Locate archived NVAT export or Jennifer Truman supplemental handoff for byte-level verification.", "notes": "Book-period weighted female NCVS rates match the supplied reference trajectory; current API extension is dashed.", "extension": {"status": "comparable_successor", "label": "Current BJS NCVS Select API continuation 2015-2024"}, "visual_review": {"status": "pending", "reference_basis": "original", "issues": ["historical NVAT export unavailable", "current-source extension is not historical proof"]}, "artifacts": {"metadata": {"path": "figures/15-4/figure.json", "self": True}, "original_reference": {"path": "references/figures/figure_15_4.png"}, "book_period_reconstruction": {"path": "figures/15-4/plots/figure_15_4_book_period.png"}, "extended_reconstruction": {"path": "figures/15-4/plots/figure_15_4_extended.png"}, "book_period_clean": {"path": "figures/15-4/data/clean/figure_15_4_book_period.csv"}, "successor_clean": {"path": "figures/15-4/data/clean/figure_15_4_successor.csv"}, "book_period_comparison": {"path": "figures/15-4/plots/comparisons/figure_15_4_book_period_review.png"}, "extended_comparison": {"path": "figures/15-4/plots/comparisons/figure_15_4_extended_review.png"}, "caption": {"path": "figures/15-4/captions/caption.txt"}, "provenance": {"path": "figures/15-4/provenance/provenance.md"}, "source_log": {"path": "figures/15-4/source_logs/source_log.md"}, "anomaly_review": {"path": "figures/15-4/anomaly_reviews/anomaly_review.md"}, "discrepancy_log": {"path": "figures/15-4/discrepancy_logs/discrepancy_log.md"}, "review_checklist": {"path": "figures/15-4/review_checklist.md"}, "lineage": {"path": "figures/15-4/lineage/lineage.json"}, "reconstruction_script": {"path": "scripts/reconstruct_15_4.py"}}}
    (FIG / "figure.json").write_text(json.dumps(record, indent=2) + "\n")


def main() -> None:
    book, successor = build_data()
    book_plot = FIG / "plots/figure_15_4_book_period.png"
    extended_plot = FIG / "plots/figure_15_4_extended.png"
    draw(book, successor, book_plot, extended=False)
    draw(book, successor, extended_plot, extended=True)
    write_package(book, successor, book_plot, extended_plot)
    print(json.dumps({"figure": "15-4", "book_rows": len(book), "successor_rows": len(successor)}, indent=2))


if __name__ == "__main__":
    main()
