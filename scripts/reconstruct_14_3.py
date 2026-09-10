"""Dated Wikipedia chronology, independently separated Amnesty continuation.

https://en.wikipedia.org/w/index.php?oldid=734519509#Abolition_chronology
Annual source URLs and raw hashes: figures/14-3/source_logs/downloads.json.
Source table errors are recorded, not repaired by guessing or plot digitization.
"""
import json
import re
from pathlib import Path

from bs4 import BeautifulSoup
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures/14-3"


def chronology(path):
    payload = json.loads(path.read_text())
    soup = BeautifulSoup(payload["parse"]["text"]["*"], "html.parser")
    table = soup.find(id="Abolition_chronology").find_next("table")
    rows = []
    for row in table.find_all("tr"):
        cells = row.find_all("td", recursive=False)
        if len(cells) != 4:
            continue
        countries = [el["data-sort-value"] for el in cells[1].select("[data-sort-value]")]
        rows.append({"year": int(cells[0].get_text(strip=True)),
                     "countries": " | ".join(countries), "countries_listed": len(countries),
                     "source_increment": int(cells[2].get_text(strip=True)),
                     "value": int(cells[3].get_text(strip=True)),
                     "source_revision": payload["parse"]["revid"]})
    result = pd.DataFrame(rows)
    result["count_discrepancy"] = result.source_increment - result.countries_listed
    result["cumulative_listed"] = result.countries_listed.cumsum()
    result["unit"] = "Countries abolishing capital punishment for all crimes"
    return result


def amnesty_count(path, year):
    soup = BeautifulSoup(path.read_text(), "html.parser")
    paragraphs = [" ".join(el.get_text(" ", strip=True).split()) for el in soup.select("p,li")]
    candidates = [t for t in paragraphs if f"At the end of {year}," in t]
    if year == 2016:
        candidates = [t for t in paragraphs if "In total," in t and "all crimes" in t and "In 2016" in t]
    pattern = (r"In total, (\d+) countries" if year == 2016 else
               r"(\d+) countries[^.]*?(?:all crimes|fully abolitionist)")
    matches = [re.search(pattern, t) for t in candidates]
    values = {int(m.group(1)) for m in matches if m}
    if len(values) != 1:
        raise ValueError(f"Ambiguous/missing all-crimes total for {year}: {values}")
    return values.pop()


def load_data():
    book = chronology(FIG / "data/raw/wikipedia_734519509.json")
    if book.year.max() != 2016 or book.value.iloc[-1] != 105:
        raise ValueError("Wrong historical revision")
    urls = {Path(r["path"]).name: r["url"] for r in json.loads((FIG / "source_logs/downloads.json").read_text())}
    later = []
    for year in range(2016, 2026):
        path = FIG / f"data/raw/amnesty_{year}.html"
        later.append({"year": year, "value": amnesty_count(path, year),
                      "source_url": urls[path.name], "source_file": str(path.relative_to(ROOT)),
                      "unit": "Countries abolitionist for all crimes, Amnesty year-end",
                      "source_version": f"Annual reporting year{year}; downloaded2026-09-10"})
    return book, pd.DataFrame(later)


def main():
    book, successor = load_data()
    clean = FIG / "data/clean"
    clean.mkdir(parents=True, exist_ok=True)
    book.to_csv(clean / "figure_14_3_book_period.csv", index=False)
    successor.to_csv(clean / "figure_14_3_successor.csv", index=False)
    book[book.count_discrepancy.ne(0)].to_csv(clean / "figure_14_3_source_anomalies.csv", index=False)
    for mode in ["book_period", "extended"]:
        extended = mode == "extended"
        fig = plt.figure(figsize=(9, 8.5 if extended else 6.8), dpi=200)
        ax = fig.add_axes([.14, .49 if extended else .27, .84, .48 if extended else .70])
        ax.plot(book.year, book.value, color="#252525", lw=2.7)
        ax.set(xlim=(1860, 2020), ylim=(0, 110), ylabel="Number of countries that have\nabolished capital punishment")
        ax.set_xticks(range(1860, 2021, 10))
        ax.set_yticks(range(0, 111, 10))
        ax.tick_params(axis="x", rotation=45)
        ax.spines[["top", "right"]].set_visible(False)
        ax.annotate("", xy=(2008, 89), xytext=(2008, 76), arrowprops={"arrowstyle": "->", "color": "#cccccc", "lw": 1.5})
        if extended:
            extra = fig.add_axes([.14, .195, .84, .19])
            overlap = book[book.year.ge(2008)]
            extra.plot(overlap.year, overlap.value, color="#252525", marker=".", label="Cited2016 chronology")
            extra.plot(successor.year, successor.value, color="#197f7c", ls="--", marker=".", label="Amnesty year-end totals")
            extra.set(xlim=(2008, 2026), ylim=(88, 116), ylabel="Countries", title="Separate institutional continuation; no forced join")
            extra.set_xticks([2008, 2012, 2016, 2020, 2025])
            extra.spines[["top", "right"]].set_visible(False)
            extra.legend(frameon=False, fontsize=8, loc="lower right")
        fig.text(.025, .11 if extended else .15, "Figure 14-3: Death penalty abolitions, 1863-2016", fontsize=12)
        fig.text(.025, .025, "Source: cited Wikipedia revision734519509 (August14,2016); numerical chronology, not digitized values.\n"
                 "Source running totals retained, including country-count inconsistencies in2009/2012; legal dates need audit.\n"
                 + ("Amnesty2016-2025 is an independently classified series (104vs105 in2016), not an unchanged-source extension."
                    if extended else "Territorial abolition-date adjustments in the book remain unresolved. Arrow marks2008."), fontsize=8)
        path = FIG / f"plots/{mode}/figure_14_3_{mode}.png"
        path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(path, facecolor="white")
        plt.close(fig)
    fig, ax = plt.subplots(figsize=(9, 4), dpi=180)
    ax.plot(book.year, book.value, color="black", label="Published running total")
    ax.plot(book.year, book.cumulative_listed, color="#a33b7d", ls="--", label="Count of explicitly listed countries")
    ax.set(xlim=(1985, 2017), ylim=(25, 110), title="Figure14-3: internal source-table inconsistencies", ylabel="Countries", xlabel="Year")
    ax.legend(frameon=False)
    fig.tight_layout()
    path = FIG / "plots/diagnostics/source_counts.png"
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    main()
