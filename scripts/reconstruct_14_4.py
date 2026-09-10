"""Execution records / Census populations; no digitized figure values.

Archived records: https://web.archive.org/web/20160419133009id_/http://www.deathpenaltyinfo.org/documents/ESPYFile.xls
Current records: https://deathpenaltyinfo.org/query/executions.csv
Census versions and URLs: figures/14-4/source_logs/downloads.json.
"""
import re
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures/14-4"


def population_vintage(year):
    table = pd.read_csv(FIG / f"data/raw/census_nst{year}.csv", encoding="cp1252")
    us = table[table.SUMLEV.eq(10) & table.NAME.eq("United States")]
    if len(us) != 1:
        raise ValueError("Ambiguous national population")
    return {int(col[-4:]): int(us[col].iloc[0]) for col in us if re.fullmatch(r"POPESTIMATE\d{4}", col)}


def load_data():
    original = pd.read_excel(FIG / "data/raw/espy_archive.xls", header=1)
    original.columns = original.columns.str.strip()
    current_espy = pd.read_excel(FIG / "data/raw/espy_1608_2002.xls", header=1)
    current_espy.columns = current_espy.columns.str.strip()
    if not original.equals(current_espy):
        raise ValueError("Archived and current Espy tables differ; re-audit")
    original["source_row"] = np.arange(3, len(original)+3)
    original["identical_visible_fields"] = original.drop(columns="source_row").duplicated(keep=False)
    # Repeated unknown names can represent distinct people; do not deduplicate.
    original = original.rename(columns={"YEAR": "year", "STATE": "state"})
    history = original.groupby("year").size()
    old_modern = pd.read_csv(FIG / "data/raw/dpic_2017_export.xls")  # CSV despite .xls URL
    old_modern["year"] = pd.to_datetime(old_modern.Date, format="%m/%d/%Y").dt.year
    current = pd.read_csv(FIG / "data/raw/dpic_executions_current.csv")
    current["year"] = pd.to_datetime(current["Execution Date"], format="%m/%d/%Y").dt.year
    annual = current.groupby("year").size()
    overlap = pd.concat([old_modern.groupby("year").size().rename("archive"), annual.rename("current")], axis=1)
    overlap = overlap.loc[1977:2015].fillna(0).astype(int)
    overlap["difference"] = overlap.current - overlap.archive
    if overlap.difference.ne(0).any():
        raise ValueError("Modern counts no longer match the pre-book archive")
    counts = pd.concat([history.loc[:1976], annual.loc[1977:2025]]).reindex(range(1780, 2026), fill_value=0)
    census = pd.read_excel(FIG / "data/raw/census_12s0001.xls", header=None)
    year = census[0].astype(str).str.extract(r"^(\d{4}) \(")[0]
    selected = census[year.notna()].copy()
    values = selected[1].astype(str).str.replace(r"^\\\d+\s*", "", regex=True).str.replace(",", "", regex=False).astype(float)
    population = dict(zip(year.dropna().astype(int), values))
    text = PdfReader(FIG / "data/raw/census_colonial.pdf").pages[13].extract_text()
    match = re.search(r"\n1780\s+([\d.,]+)", text)
    if not match:
        raise ValueError("Missing colonial population table cell")
    population[1780] = int(re.sub(r"[.,]", "", match.group(1)))
    vintage2016, vintage2019, vintage2025 = [population_vintage(y) for y in [2016, 2019, 2025]]
    rows = []
    for start in range(1780, 2010, 10):
        total = int(counts.loc[start:start+9].sum())
        midpoint = (population[start] + population[start+10]) / 2
        rows.append({"year": start, "end_year": start+9, "executions": total,
                     "years_averaged": 10, "population": midpoint,
                     "value": total/10/midpoint*100000, "period_type": "decade_mean",
                     "population_version": "Census2011decennial endpoints;1780Census1960historical estimate"})
    for year in range(2010, 2017):
        rows.append({"year": year, "end_year": year, "executions": int(counts[year]),
                     "years_averaged": 1, "population": vintage2016[year],
                     "value": counts[year]/vintage2016[year]*100000, "period_type": "annual",
                     "population_version": "Census vintage2016"})
    book = pd.DataFrame(rows)
    book["unit"] = "Executions per100000 residents peryear"
    successor = []
    for year in range(2010, 2026):
        version, pop = (2019, vintage2019[year]) if year <= 2019 else (2025, vintage2025[year])
        successor.append({"year": year, "executions": int(counts[year]), "population": pop,
                          "population_version": f"Census vintage{version}",
                          "value": counts[year]/pop*100000, "unit": "Executions per100000 residents peryear"})
    diagnostic = book[book.period_type.eq("decade_mean")].copy()
    diagnostic["start_year_executions"] = diagnostic.year.map(counts)
    diagnostic["start_year_population"] = diagnostic.year.map(population)
    diagnostic["single_year_rate"] = diagnostic.start_year_executions/diagnostic.start_year_population*100000
    pop_table = pd.DataFrame([{"year": y, "population": v, "role": "historical_census_endpoint"} for y, v in sorted(population.items())])
    return book, pd.DataFrame(successor), diagnostic, original[["source_row", "year", "state", "identical_visible_fields"]], overlap.reset_index(), pop_table


def main():
    book, successor, diagnostic, records, overlap, population = load_data()
    clean = FIG / "data/clean"
    clean.mkdir(parents=True, exist_ok=True)
    for name, data in [("book_period", book), ("successor", successor), ("diagnostic", diagnostic),
                       ("historical_records", records), ("archive_agreement", overlap), ("population", population)]:
        data.to_csv(clean / f"figure_14_4_{name}.csv", index=False)
    for mode in ["book_period", "extended"]:
        extended = mode == "extended"
        fig = plt.figure(figsize=(9, 8.5 if extended else 6.8), dpi=200)
        ax = fig.add_axes([.11, .47 if extended else .27, .87, .50 if extended else .70])
        ax.plot(book.year, book.value, lw=2.7, color="#252525")
        if extended:
            tail = pd.concat([book[book.year.eq(2016)][["year", "value"]], successor[successor.year.gt(2016)][["year", "value"]]])
            ax.plot(tail.year, tail.value, ls="--", lw=2, color="#197f7c")
        ax.set(xlim=(1775, 2027 if extended else 2017), ylim=(0, .9), ylabel="Executions per 100,000 people")
        ax.set_xticks(list(range(1775, 2016, 15)) + ([2025] if extended else []))
        ax.set_yticks(np.arange(0, 1, .1))
        ax.tick_params(axis="x", rotation=45)
        ax.spines[["top", "right"]].set_visible(False)
        ax.annotate("", xy=(2010, .035), xytext=(2010, .13), arrowprops={"arrowstyle": "->", "color": "#cccccc", "lw": 1.5})
        if extended:
            extra = fig.add_axes([.11, .19, .87, .18])
            historic = book[book.year.ge(2010)]
            extra.plot(historic.year, historic.value, lw=2, color="#252525", label="Book-period annual counts")
            prior, later = successor[successor.year.le(2016)], successor[successor.year.ge(2016)]
            extra.plot(prior.year, prior.value, ls=":", color="#197f7c", lw=1.5, label="Revised population overlap")
            extra.plot(later.year, later.value, ls="--", color="#197f7c", lw=1.8, marker=".", label="2017-2025")
            extra.set(xlim=(2010, 2026), ylim=(0, .02), ylabel="Annual rate", title="Recent detail: same execution definition, revised Census population vintages")
            extra.title.set_fontsize(10)
            extra.set_xticks([2010, 2013, 2016, 2019, 2022, 2025])
            extra.spines[["top", "right"]].set_visible(False)
            extra.legend(frameon=False, fontsize=7, ncols=3, loc="upper center")
        fig.text(.025, .11 if extended else .15, "Figure 14-4: Executions, US, 1780-2016", fontsize=12)
        fig.text(.025, .025, "Sources: archived DPIC/Espy records; modern DPIC execution CSV; U.S. Census population tables.\n"
                 "1780-2009: decade-average executions / midpoint population; 2010 onward: annual rates.\n"
                 + ("Dashed extension ends 2025; incomplete 2026 excluded. Census vintages revised; no shift to match image."
                    if extended else "Historical averaging rule inferred, not confirmed from author code. Source record-count issues retained."), fontsize=8)
        path = FIG / f"plots/{mode}/figure_14_4_{mode}.png"
        path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(path, facecolor="white")
        plt.close(fig)
    fig, ax = plt.subplots(figsize=(9, 4), dpi=180)
    ax.plot(diagnostic.year, diagnostic.value, color="black", label="Decade mean / midpoint population")
    ax.plot(diagnostic.year, diagnostic.single_year_rate, color="#a33b7d", ls=":", label="Rejected: single census-year rate")
    ax.set(title="Figure14-4: temporal aggregation diagnostic", xlabel="Decade start", ylabel="Executions per100,000/year")
    ax.legend(frameon=False)
    fig.tight_layout()
    path = FIG / "plots/diagnostics/temporal_aggregation.png"
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    main()
