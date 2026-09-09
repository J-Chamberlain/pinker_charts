#!/usr/bin/env python3
"""Build the explicitly partial Figure 5-4 research artifact.

The book's exact combined-sex HMD vintage is unavailable without an HMD
account.  The post-1845 lines below therefore use the public ONS male
decennial table only as a visual/data diagnostic, never as a substitution.
"""
from pathlib import Path
import csv
import hashlib
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures/5-4"
RAW = FIG / "data/raw"
CLEAN = FIG / "data/clean"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    CLEAN.mkdir(parents=True, exist_ok=True)
    for p in [FIG / "plots/book_period", FIG / "plots/comparisons", FIG / "checksums"]:
        p.mkdir(parents=True, exist_ok=True)

    clio = pd.read_csv(RAW / "owid_clio_infra_life_expectancy_at_birth.csv")
    clio = clio[(clio.Entity == "United Kingdom") & clio.Year.between(1701, 1844)].copy()
    clio.columns = ["entity", "year", "expected_age_at_death"]
    clio["age_at_observation"] = 0
    clio["series_status"] = "cited_source_component"

    ons = pd.read_csv(RAW / "ons_expected_age_to_reach_males.csv", skiprows=1)
    years = [int(x) for x in ons.columns[1:] if str(x).isdigit()]
    rows = []
    for age in [0, 1, 30, 70]:
        source = ons[ons.iloc[:, 0].astype(str) == str(age)].iloc[0]
        for year in years:
            rows.append(["England and Wales (males)", year, float(source[str(year)]), age,
                         "diagnostic_proxy_not_book_data"])
    diagnostic = pd.DataFrame(rows, columns=clio.columns)
    clean = pd.concat([clio, diagnostic], ignore_index=True).sort_values(["age_at_observation", "year"])
    clean.to_csv(CLEAN / "figure_5_4_partial_source_recovery.csv", index=False)

    fig, ax = plt.subplots(figsize=(9, 5.4))
    ax.plot(clio.year, clio.expected_age_at_death, color="black", lw=1.8, label="At birth (cited Clio component)")
    styles = {0: "-", 1: "--", 30: "-.", 70: ":"}
    for age in [0, 1, 30, 70]:
        d = diagnostic[diagnostic.age_at_observation == age]
        ax.plot(d.year, d.expected_age_at_death, color="0.35", lw=1.5,
                linestyle=styles[age], label=f"Age {age} (ONS male diagnostic)")
    ax.set(xlim=(1701, 2013), ylim=(20, 100), xlabel="Year", ylabel="Expected age at death")
    ax.set_xticks([1701, 1750, 1800, 1850, 1900, 1950, 2013])
    ax.set_yticks(range(20, 101, 10))
    ax.grid(axis="y", color="0.88", lw=.7)
    ax.legend(frameon=False, fontsize=8, ncol=2, loc="lower right")
    ax.set_title("Life expectancy, UK, 1701-2013\nPARTIAL SOURCE-RECOVERY DIAGNOSTIC - not a book reconstruction", loc="left")
    fig.tight_layout()
    out = FIG / "plots/book_period/figure_5_4_partial_diagnostic.png"
    fig.savefig(out, dpi=200)
    plt.close(fig)

    files = [RAW / "owid_clio_infra_life_expectancy_at_birth.csv",
             RAW / "ons_expected_age_to_reach_males.csv",
             CLEAN / "figure_5_4_partial_source_recovery.csv", out]
    (FIG / "checksums/sha256sums.txt").write_text("".join(f"{sha(p)}  {p.relative_to(FIG)}\n" for p in files))


if __name__ == "__main__":
    main()
