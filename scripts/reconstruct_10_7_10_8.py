from pathlib import Path

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]


def ensure_dirs(fig):
    base = ROOT / "figures" / fig
    for part in [
        "data/clean",
        "plots/book_period",
        "plots/extended",
        "plots/comparisons",
    ]:
        (base / part).mkdir(parents=True, exist_ok=True)
    return base


def save_side_by_side(reference, recreated, output, title):
    ref = mpimg.imread(reference)
    rec = mpimg.imread(recreated)
    fig, axes = plt.subplots(1, 2, figsize=(14, 6), dpi=180)
    for ax, image, label in zip(axes, [ref, rec], ["Kindle reference", "Recreated"]):
        ax.imshow(image)
        ax.set_title(label, fontsize=11)
        ax.axis("off")
    fig.suptitle(title, fontsize=13)
    fig.tight_layout()
    fig.savefig(output, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def plot_10_7():
    base = ensure_dirs("10-7")
    book_csv = (
        base
        / "data/candidates/owid_datasets_carbon_intensity_bookera/"
        / "Carbon intensity (kgCO2!$) - Madisson, World Bank, CDIAC.csv"
    )
    current_csv = base / "data/raw/owid_co2_intensity.csv"
    value_col_book = "Carbon intensity (kgCO2/$) (CDIAC (2017))"
    value_col_current = "Annual CO₂ emissions per GDP (kg per international-$)"

    book = pd.read_csv(book_csv)
    book = book.rename(columns={value_col_book: "kg_co2_per_2011_int_dollar"})
    keep = ["World", "United States", "United Kingdom", "China", "India"]
    book = book[book["Entity"].isin(keep)].copy()
    book["period"] = "book_period_owid_2017"
    book.to_csv(base / "data/clean/figure_10_7_book_period_clean.csv", index=False)

    current = pd.read_csv(current_csv)
    current = current[current["Entity"].isin(keep)].copy()
    current = current.rename(columns={value_col_current: "kg_co2_per_2011_int_dollar"})
    current["period"] = "current_owid_successor"
    current.to_csv(base / "data/clean/figure_10_7_extended_clean.csv", index=False)

    styles = {
        "World": dict(color="black", linewidth=3.0, linestyle="-", zorder=5),
        "United States": dict(color="0.35", linewidth=2.2, linestyle="-"),
        "United Kingdom": dict(color="0.55", linewidth=2.0, linestyle=":"),
        "China": dict(color="0.82", linewidth=2.0, linestyle="-"),
        "India": dict(color="0.72", linewidth=2.0, linestyle="--"),
    }
    labels = {"United States": "US", "United Kingdom": "UK"}

    def draw(df, out, extended=False):
        fig, ax = plt.subplots(figsize=(8.5, 5.2), dpi=180)
        for ent in keep:
            sub = df[df["Entity"] == ent].sort_values("Year")
            if not len(sub):
                continue
            style = styles[ent].copy()
            ax.plot(sub["Year"], sub["kg_co2_per_2011_int_dollar"], **style)
            if extended:
                ext = current[(current["Entity"] == ent) & (current["Year"] > 2014)].sort_values("Year")
                if len(ext):
                    ext_style = style.copy()
                    ext_style["linestyle"] = "--"
                    ext_style["linewidth"] = max(1.5, ext_style["linewidth"] - 0.4)
                    ext_style["alpha"] = 0.8
                    ax.plot(ext["Year"], ext["kg_co2_per_2011_int_dollar"], **ext_style)
        ax.set_xlim(1820, 2025 if extended else 2020)
        ax.set_ylim(0, 2.0)
        ax.set_xticks(list(range(1820, 2021, 20)))
        ax.set_ylabel("CO2 emissions per dollar of GDP")
        ax.set_xlabel("")
        ax.set_title("Figure 10-7: Carbon intensity", loc="left", fontsize=12)
        ax.grid(False)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.text(1987, 1.55, "China", color="0.35", fontsize=10)
        ax.text(1946, 0.94, "US", color="0.25", fontsize=10)
        ax.text(1872, 0.86, "UK", color="0.35", fontsize=10)
        ax.text(1910, 0.49, "World", color="black", fontsize=10, weight="bold")
        ax.text(1999, 0.19, "India", color="0.35", fontsize=10)
        note = (
            "Book-period data: OWID 2017 dataset based on CDIAC, World Bank, and Maddison."
            if not extended
            else "Solid lines use OWID 2017 book-period data; dashed segments use current OWID successor data after 2014."
        )
        ax.text(0, -0.16, note, transform=ax.transAxes, fontsize=7.5, va="top")
        fig.tight_layout()
        fig.savefig(out, bbox_inches="tight", facecolor="white")
        plt.close(fig)

    book_plot = base / "plots/book_period/figure_10_7_book_period_reconstruction.png"
    ext_plot = base / "plots/extended/figure_10_7_extended_reconstruction.png"
    draw(book, book_plot, extended=False)
    draw(book, ext_plot, extended=True)
    save_side_by_side(
        base / "plots/comparisons/kindle_reference_figure_10_7.png",
        book_plot,
        base / "plots/comparisons/figure_10_7_book_period_comparison.png",
        "Figure 10-7 book-period comparison",
    )
    save_side_by_side(
        base / "plots/comparisons/kindle_reference_figure_10_7.png",
        ext_plot,
        base / "plots/comparisons/figure_10_7_extended_comparison.png",
        "Figure 10-7 extended comparison",
    )


def plot_10_8():
    base = ensure_dirs("10-8")
    book_csv = (
        base
        / "data/candidates/owid_datasets_co2_region_2017_local/"
        / "CO2 per year by region - CDIAC (2017).csv"
    )
    current_csv = base / "data/raw/owid_annual_co2_emissions_by_region.csv"
    value_col_book = "CO2 per year by region (CDIAC (2017))"
    value_col_current = "Annual CO₂ emissions"

    order_book = [
        "EU-28",
        "United States",
        "China",
        "India",
        "Europe (other)",
        "Americas (other)",
        "Middle East",
        "Asia and Pacific (other)",
        "Africa",
        "International aviation and maritime transport",
        "Statistical difference",
    ]

    book = pd.read_csv(book_csv).rename(columns={value_col_book: "billion_tonnes_co2"})
    book = book[(book["Year"].between(1960, 2015)) & (book["Entity"].isin(order_book))].copy()
    book.to_csv(base / "data/clean/figure_10_8_book_period_clean.csv", index=False)

    current = pd.read_csv(current_csv).rename(columns={value_col_current: "tonnes_co2"})
    current["billion_tonnes_co2"] = current["tonnes_co2"] / 1e9
    mapping = {
        "European Union (27)": "EU-27",
        "United States": "United States",
        "China": "China",
        "India": "India",
        "Europe (excl. EU-27)": "Europe (other)",
        "North America (excl. USA)": "Americas (other)",
        "South America": "Americas (other)",
        "Middle East (GCP)": "Middle East",
        "Asia (excl. China and India)": "Asia and Pacific (other)",
        "Oceania": "Asia and Pacific (other)",
        "Africa": "Africa",
        "International aviation": "Intl air and sea",
        "International shipping": "Intl air and sea",
    }
    current = current[current["Entity"].isin(mapping)].copy()
    current["mapped_entity"] = current["Entity"].map(mapping)
    current = (
        current.groupby(["mapped_entity", "Year"], as_index=False)["billion_tonnes_co2"]
        .sum()
        .rename(columns={"mapped_entity": "Entity"})
    )
    current = current[current["Year"].between(1960, 2024)]
    current.to_csv(base / "data/clean/figure_10_8_extended_clean.csv", index=False)

    colors = {
        "EU-28": "0.02",
        "EU-27": "0.02",
        "United States": "0.38",
        "China": "0.56",
        "India": "0.72",
        "Europe (other)": "0.0",
        "Americas (other)": "0.45",
        "Middle East": "0.30",
        "Asia and Pacific (other)": "0.62",
        "Africa": "0.12",
        "International aviation and maritime transport": "0.78",
        "Intl air and sea": "0.78",
        "Statistical difference": "0.88",
    }

    def draw(df, order, out, title, extended=False):
        pivot = df.pivot_table(
            index="Year", columns="Entity", values="billion_tonnes_co2", aggfunc="sum"
        ).fillna(0)
        pivot = pivot[[c for c in order if c in pivot.columns]]
        fig, ax = plt.subplots(figsize=(8.5, 5.1), dpi=180)
        ax.stackplot(
            pivot.index,
            [pivot[c].values for c in pivot.columns],
            colors=[colors.get(c, "0.5") for c in pivot.columns],
            linewidth=0,
        )
        if extended:
            ext_order = [
                "EU-27",
                "United States",
                "China",
                "India",
                "Europe (other)",
                "Americas (other)",
                "Middle East",
                "Asia and Pacific (other)",
                "Africa",
                "Intl air and sea",
            ]
            ext = current[current["Year"] > 2015]
            ext_pivot = ext.pivot_table(
                index="Year", columns="Entity", values="billion_tonnes_co2", aggfunc="sum"
            ).fillna(0)
            ext_pivot = ext_pivot[[c for c in ext_order if c in ext_pivot.columns]]
            cumulative = ext_pivot.cumsum(axis=1)
            previous = cumulative.shift(axis=1, fill_value=0)
            for col in ext_pivot.columns:
                ax.fill_between(
                    ext_pivot.index,
                    previous[col],
                    cumulative[col],
                    color=colors.get(col, "0.5"),
                    alpha=0.72,
                    linewidth=0,
                )
            ax.axvline(2015, color="0.45", linewidth=0.8, linestyle="--", alpha=0.7)
        ax.set_xlim(1960, 2024 if extended else 2015)
        ax.set_ylim(0, max(38, pivot.sum(axis=1).max() * 1.05))
        ax.set_ylabel("Annual CO2 emissions (billion tons)")
        ax.set_title(title, loc="left", fontsize=12)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.text(2014 if not extended else 2023, 1.2, order[0], color="white", fontsize=9, ha="right")
        ax.text(2014 if not extended else 2023, 7.0, "United States", color="white", fontsize=9, ha="right")
        ax.text(2014 if not extended else 2023, 13.4, "China", color="0.1", fontsize=9, ha="right")
        ax.text(2014 if not extended else 2023, 17.2, "India", color="0.1", fontsize=9, ha="right")
        ax.text(1978, 12.5, "Europe (other)", color="white", fontsize=9)
        ax.text(2002, 18.0, "Americas (other)", color="white", fontsize=8, rotation=28)
        ax.text(2007, 22.1, "Middle East", color="0.1", fontsize=8, rotation=34)
        ax.text(2004, 25.2, "Asia & Pacific (other)", color="0.1", fontsize=8, rotation=35)
        if not extended:
            ax.annotate("Intl air & sea", xy=(2004, 25.5), xytext=(1995, 28.5),
                        arrowprops=dict(arrowstyle="-", color="0.65"), color="0.2", fontsize=9)
            ax.text(2009, 34.0, "Africa", color="white", fontsize=9, rotation=14)
            ax.text(2011, 35.2, "Other", color="0.2", fontsize=9, ha="right")
        note = (
            "Book-period data: OWID 2017 regional CDIAC dataset."
            if not extended
            else "Solid area uses OWID 2017 data through 2015; post-2015 area uses current OWID/GCB successor categories."
        )
        ax.text(0, -0.16, note, transform=ax.transAxes, fontsize=7.5, va="top")
        fig.tight_layout()
        fig.savefig(out, bbox_inches="tight", facecolor="white")
        plt.close(fig)

    book_plot = base / "plots/book_period/figure_10_8_book_period_reconstruction.png"
    ext_plot = base / "plots/extended/figure_10_8_extended_reconstruction.png"
    draw(book, order_book, book_plot, "Figure 10-8: CO2 emissions", extended=False)
    draw(book, order_book, ext_plot, "Figure 10-8: CO2 emissions, extended", extended=True)
    save_side_by_side(
        base / "plots/comparisons/kindle_reference_figure_10_8.png",
        book_plot,
        base / "plots/comparisons/figure_10_8_book_period_comparison.png",
        "Figure 10-8 book-period comparison",
    )
    save_side_by_side(
        base / "plots/comparisons/kindle_reference_figure_10_8.png",
        ext_plot,
        base / "plots/comparisons/figure_10_8_extended_comparison.png",
        "Figure 10-8 extended comparison",
    )


if __name__ == "__main__":
    plot_10_7()
    plot_10_8()
