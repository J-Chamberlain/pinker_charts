"""Reconstruct Figure 15-5 from historical legal-status data."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures/15-5"
RAW = FIG / "data/raw/owid_same_sex_sexual_acts_legal_mignot.csv"
REFERENCE = ROOT / "references/figures/figure_15_5.png"


def build_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    source = pd.read_csv(RAW)
    source = source.sort_values(["Entity", "Year"])
    transitions: list[dict[str, int | str]] = []
    for country, group in source.groupby("Entity"):
        group = group.sort_values("Year")
        legal = group["Legal status of homosexuality"].eq("Legal")
        previously_illegal = group["Legal status of homosexuality"].eq("Illegal").shift(1, fill_value=False)
        transition = legal & previously_illegal
        for year in group.loc[transition, "Year"]:
            transitions.append({"country": country, "decriminalization_year": int(year)})
    events = pd.DataFrame(transitions)
    first = events.groupby("country", as_index=False).decriminalization_year.min()
    year_index = range(int(first.decriminalization_year.min()), int(first.decriminalization_year.max()) + 1)
    years = pd.DataFrame({"year": year_index})
    events_by_year = first.decriminalization_year.value_counts().sort_index()
    years["decriminalized_countries"] = events_by_year.reindex(year_index, fill_value=0).cumsum().to_numpy()
    years["source_file"] = "owid_same_sex_sexual_acts_legal_mignot.csv"
    years["source_kind"] = "Our World in Data current historical series"
    years["period"] = years.year.map(lambda value: "book" if value <= 2016 else "successor")
    return years[years.period == "book"].copy(), years[years.period == "successor"].copy()


def draw(book: pd.DataFrame, successor: pd.DataFrame, output: Path, extended: bool) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(12.2, 7.2), dpi=180)
    ax.plot(book.year, book.decriminalized_countries, color="#242222", lw=3.0, drawstyle="steps-post")
    if extended:
        joined = pd.concat([book.tail(1), successor], ignore_index=True)
        ax.plot(joined.year, joined.decriminalized_countries, color="#242222", lw=3.0, ls="--", drawstyle="steps-post")
        ax.axvline(2016, color="#c8c6c6", lw=1.0, ls=":")
    ax.annotate("", xy=(2009, 81), xytext=(2009, 96), arrowprops={"arrowstyle": "-|>", "color": "#d1cfcf", "lw": 1.8})
    ax.set_ylabel("Number of countries that have\ndecriminalized homosexuality", fontsize=12)
    ax.set_xlim(1791, 2025 if extended else 2016)
    ax.set_ylim(0, 100)
    ax.set_yticks(range(0, 101, 10))
    ax.set_xticks(list(range(1795, 2016, 20)) + ([2025] if extended else []))
    ax.tick_params(axis="x", labelrotation=45, colors="#3e3c3c", labelsize=9)
    ax.tick_params(axis="y", colors="#3e3c3c", labelsize=9)
    ax.grid(False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#626060")
    ax.spines["bottom"].set_color("#626060")
    note = "Source: Our World in Data historical same-sex legal-status series; cumulative first transitions from illegal to legal."
    if extended:
        note += " Dashed: current-source continuation after 2016."
    fig.text(0.02, 0.018, note, fontsize=7.8, color="#555555")
    fig.tight_layout(rect=(0, 0.06, 1, 1))
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
    book.to_csv(FIG / "data/clean/figure_15_5_book_period.csv", index=False)
    successor.to_csv(FIG / "data/clean/figure_15_5_successor.csv", index=False)
    compare(book_plot, FIG / "plots/comparisons/figure_15_5_book_period_review.png", "Figure 15-5 book-period comparison")
    compare(extended_plot, FIG / "plots/comparisons/figure_15_5_extended_review.png", "Figure 15-5 extended comparison")
    (FIG / "README.md").write_text("""# Figure 15-5 - Decriminalization of homosexuality

Status: `partial_match`. The supplied reference cites Ottosson/ILGA and a 2016 Wikipedia supplement. The reconstruction uses a public current historical legal-status series from Our World in Data/Mignot, counts each country's first observed illegal-to-legal transition, and extends it with the same current source after 2016. The staircase shape is broadly similar, but the source version and country universe are not proven identical and the mid-century level visibly diverges.

- Original: [../../references/figures/figure_15_5.png](../../references/figures/figure_15_5.png)
- Script: [../../scripts/reconstruct_15_5.py](../../scripts/reconstruct_15_5.py)
- Book comparison: [plots/comparisons/figure_15_5_book_period_review.png](plots/comparisons/figure_15_5_book_period_review.png)
- Extended comparison: [plots/comparisons/figure_15_5_extended_review.png](plots/comparisons/figure_15_5_extended_review.png)
""")
    (FIG / "captions/caption.txt").write_text("Figure 15-5: Decriminalization of homosexuality, 1791-2016. The black staircase counts countries at their first observed transition from illegal to legal status in the current Our World in Data/Mignot historical series. The book cites Ottosson 2006, 2009 and a Wikipedia supplement retrieved July 31, 2016; the current series is a documented successor rather than an exact historical copy. Dashed lines extend the same current source after 2016. Status: partial_match because the reconstructed mid-century staircase is materially above the reference and the historical country-date table remains unrecovered.")
    (FIG / "provenance/provenance.md").write_text("""# Figure 15-5 provenance

## Original book source line

Ottosson 2006, 2009. Dates for an additional sixteen countries were obtained from “LGBT Rights by Country or Territory,” Wikipedia, retrieved July 31, 2016. Dates for an additional thirty-six countries that currently allow homosexuality are not listed in either source. The arrow points to 2009, the last year plotted in fig. 7-23 of Pinker 2011.

## Recovered source chain

- Archived ILGA report: `figures/15-5/data/raw/ilga_state_sponsored_homophobia_2009.pdf`.
- Public current historical series: `figures/15-5/data/raw/owid_same_sex_sexual_acts_legal_mignot.csv`.
- Current series metadata: `owid_same_sex_sexual_acts_legal_mignot.metadata.json`.
- Archived OWID legal-year snapshot: `wikimedia_owid_4910_snapshot.json`.
- Data URL: https://ourworldindata.org/grapher/same-sex-sexual-acts-legal-mignot.csv

## Transformations

For each country, the first year in which the series changes from `Illegal` to `Legal` is retained. Counts of those transition years are cumulatively summed by year. The 1791-2016 interval is the book-period comparison; 2017 onward is plotted as a dashed current-source continuation. No values were digitized from the Pinker chart.
""")
    (FIG / "source_logs/source_log.md").write_text("""# Figure 15-5 source discovery log

## Queries attempted

- `Ottosson 2006 2009 decriminalization homosexuality dates countries dataset`
- `State Sponsored Homophobia 2009 csv decriminalization`
- `Our World in Data decriminalization homosexuality historical countries 1791 2016`
- `Kenny Patel 2017 Norms and Reform Figure 2 data countries years`
- `ILGA State Sponsored Homophobia older editions 2009`

## Sources investigated

- ILGA State-Sponsored Homophobia 2009 report - accepted as an archived source-family reference, but it is not a machine-readable country-year table.
- Current OWID/Mignot country-year legal-status CSV - accepted as a transparent successor because it exposes the full historical state and supports reproducible counting.
- Archived OWID/Kenny-Patel legal-year table via Wikimedia - investigated; the tabular snapshot is preserved but its old CSV resource is empty in the archived GitHub dataset.
- CGD Kenny & Patel 2017 paper - investigated as a related published analysis, but its updated country universe does not reproduce the Pinker endpoint exactly.

## Remaining uncertainties

- Ottosson's exact country list and treatment of territories/never-criminalized countries are not recovered as a machine-readable original dataset.
- The current Mignot series reaches 91 cumulative first transitions by 2016 versus approximately 92 in the supplied reference.
- Country-year legal status can reflect re-criminalization and changes in territorial boundaries; the first-transition rule is an explicit approximation to the plotted concept.

## Recommended next steps

Recover the original Ottosson 2006/2009 country/date tables or the July 31, 2016 Wikipedia revision, then compare event-by-event before any promotion to `verified_reproduction`.
""")
    (FIG / "search_iterations/search_iterations.md").write_text("""# Search iterations

1. Inspected the supplied Supplemental PDF and extracted the staircase measure, 1791-2016 range, 2009 arrow, and source note.
2. Downloaded the archived ILGA 2009 report and checked it as the cited source family.
3. Located the OWID/Mignot machine-readable historical legal-status CSV and metadata.
4. Derived first illegal-to-legal transitions and cumulative counts without using plotted values.
5. Generated and inspected book-period and dashed extended comparisons; the successor endpoint is close but not identical.
""")
    (FIG / "anomaly_reviews/anomaly_review.md").write_text("""# Anomaly review

Major evidence limitation: the exact Ottosson/Wikipedia 2016 country-date inputs are not recovered, so the book-period result is a `partial_match`, not a verified reproduction or equivalent. The current series reaches 91 at 2016 versus approximately 92 in the reference, but its mid-century cumulative level is materially higher. Minor: line styling, tick placement, and annotation are approximated. The dashed extension is clearly separated and uses the same current source.
""")
    (FIG / "discrepancy_logs/discrepancy_log.md").write_text("""# Discrepancy log

The current-source staircase resembles the reference in overall shape, but not at every interval: the current series is materially higher through the mid-century portion while ending within about one country of the reference at 2016. Individual event years may differ because Mignot uses a different country universe and legal-history rules than Ottosson plus the 2016 Wikipedia supplement. This is a source-version discrepancy, not a plotting failure; exact historical country-date inputs remain the next recovery target.
""")
    (FIG / "review_checklist.md").write_text("""# Review checklist

- [x] Original Supplemental PDF figure inspected
- [x] Title, measure, date range, arrow year, and source note extracted
- [x] Cited ILGA source family downloaded
- [x] Public machine-readable successor located and saved
- [x] Book-period plot generated from country-year data, not digitized values
- [x] Current-source extension generated and dashed
- [x] Both side-by-side comparisons generated and inspected
- [x] Source-version discrepancy and endpoint difference documented
- [ ] Recover exact Ottosson/Wikipedia 2016 country-date tables
""")
    lineage = {"schema_version": 1, "figure_id": "15-5", "book_citation": "Ottosson 2006, 2009; Wikipedia LGBT Rights by Country or Territory retrieved July 31, 2016", "script": "scripts/reconstruct_15_5.py", "mappings": [{"role": "book_period", "raw_inputs": ["figures/15-5/data/raw/owid_same_sex_sexual_acts_legal_mignot.csv", "figures/15-5/data/raw/ilga_state_sponsored_homophobia_2009.pdf", "figures/15-5/data/raw/wikimedia_owid_4910_snapshot.json"], "selection": "First illegal-to-legal transition per country, 1791-2016", "transformation": "cumulative count of transition years", "clean": "figures/15-5/data/clean/figure_15_5_book_period.csv", "plot": "figures/15-5/plots/figure_15_5_book_period.png"}, {"role": "extension", "raw_inputs": ["figures/15-5/data/raw/owid_same_sex_sexual_acts_legal_mignot.csv"], "selection": "Same first-transition rule, 2017-2025", "transformation": "cumulative count plotted dashed", "clean": "figures/15-5/data/clean/figure_15_5_successor.csv", "plot": "figures/15-5/plots/figure_15_5_extended.png"}]}
    (FIG / "lineage/lineage.json").write_text(json.dumps(lineage, indent=2) + "\n")
    record = {"figure_id": "15-5", "title": "Decriminalization of homosexuality, 1791-2016", "scientific_status": "updated_equivalent", "artifact_kind": "reconstruction", "publication_status": "not_reviewed", "execution_status": "processed", "lifecycle_stage": "visual_review", "next_action": "Recover the exact Ottosson/Wikipedia 2016 country-date table and compare event-by-event.", "notes": "Current OWID/Mignot historical successor; cumulative first illegal-to-legal transitions.", "extension": {"status": "comparable_successor", "label": "Current OWID/Mignot series after 2016"}, "visual_review": {"status": "pending", "reference_basis": "original", "issues": ["original country-date table unavailable", "endpoint differs by approximately one country"]}, "artifacts": {"metadata": {"path": "figures/15-5/figure.json", "self": True}, "original_reference": {"path": "references/figures/figure_15_5.png"}, "book_period_reconstruction": {"path": "figures/15-5/plots/figure_15_5_book_period.png"}, "extended_reconstruction": {"path": "figures/15-5/plots/figure_15_5_extended.png"}, "book_period_clean": {"path": "figures/15-5/data/clean/figure_15_5_book_period.csv"}, "successor_clean": {"path": "figures/15-5/data/clean/figure_15_5_successor.csv"}, "book_period_comparison": {"path": "figures/15-5/plots/comparisons/figure_15_5_book_period_review.png"}, "extended_comparison": {"path": "figures/15-5/plots/comparisons/figure_15_5_extended_review.png"}, "caption": {"path": "figures/15-5/captions/caption.txt"}, "provenance": {"path": "figures/15-5/provenance/provenance.md"}, "source_log": {"path": "figures/15-5/source_logs/source_log.md"}, "anomaly_review": {"path": "figures/15-5/anomaly_reviews/anomaly_review.md"}, "discrepancy_log": {"path": "figures/15-5/discrepancy_logs/discrepancy_log.md"}, "review_checklist": {"path": "figures/15-5/review_checklist.md"}, "lineage": {"path": "figures/15-5/lineage/lineage.json"}, "reconstruction_script": {"path": "scripts/reconstruct_15_5.py"}}}
    # Keep machine-readable status aligned with the visual review: the current
    # successor has a material mid-century divergence from the book staircase.
    record["scientific_status"] = "partial_match"
    record["next_action"] = "Recover the exact Ottosson/Wikipedia 2016 country-date table and compare event-by-event, prioritizing the mid-century divergence."
    record["notes"] = "Current OWID/Mignot historical successor; cumulative first illegal-to-legal transitions; material mid-century divergence from the book reference."
    record["visual_review"]["issues"] = ["original country-date table unavailable", "mid-century cumulative level materially diverges", "endpoint differs by approximately one country"]
    (FIG / "figure.json").write_text(json.dumps(record, indent=2) + "\n")


def main() -> None:
    book, successor = build_data()
    book_plot = FIG / "plots/figure_15_5_book_period.png"
    extended_plot = FIG / "plots/figure_15_5_extended.png"
    draw(book, successor, book_plot, extended=False)
    draw(book, successor, extended_plot, extended=True)
    write_package(book, successor, book_plot, extended_plot)
    print(json.dumps({"figure": "15-5", "book_rows": len(book), "successor_rows": len(successor)}, indent=2))


if __name__ == "__main__":
    main()
