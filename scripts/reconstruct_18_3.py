"""Recover country components from official numeric tables, never chart pixels.

HSSO: https://hsso.ch/en/2012/d/50a and /b/42
CDC: https://www.cdc.gov/nchs/nvss/mortality/hist290.htm
CDC successor: https://www.cdc.gov/nchs/products/databriefs/db541.htm
"""
from pathlib import Path
import re
import subprocess
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
try:
    from reconstruct_18_4 import compare
except ImportError:
    from scripts.reconstruct_18_4 import compare

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "figures/18-3"
RAW = BASE / "data/raw"
CLEAN = BASE / "data/clean"


def pdf_text(name):
    return subprocess.check_output(["pdftotext", "-layout", str(RAW/name), "-"], text=True)


def swiss():
    deaths = pd.read_excel(RAW/"hsso_D50a_2012.xlsx", header=None)
    population = pd.read_excel(RAW/"hsso_B42_2012.xlsx", header=None)
    assert deaths.iloc[2,29] == "CH" and population.iloc[6,1] == "Total"
    d = deaths[[0,29]].apply(pd.to_numeric, errors="coerce").dropna()
    p = population[[0,1]].apply(pd.to_numeric, errors="coerce").dropna()
    d.columns = ["year", "deaths"]
    p.columns = ["year", "population_thousands"]
    result = d.merge(p, on="year", validate="one_to_one")
    result["year"] = result.year.astype(int)
    assert result.year.tolist() == list(range(1876,1996))
    result["rate"] = result.deaths / (1000 * result.population_thousands) * 100000
    result["country"] = "Switzerland"
    result["definition"] = "crude; annual deaths / year-end permanent residents"
    result["source_url"] = "https://hsso.ch/get/D.50a.xlsx; https://hsso.ch/get/B.42.xlsx"
    return result


def us_historical():
    files = [("cdc_hist290_0039.pdf",1900,1939), ("cdc_mx194049.pdf",1940,1949),
             ("cdc_mx1950_59.pdf",1950,1959), ("cdc_mx196067.pdf",1960,1967),
             ("cdc_mx196878.pdf",1968,1978), ("cdc_gm290_98.pdf",1979,1998)]
    rows=[]
    for name,start,end in files:
        pages=pdf_text(name).split("\f")
        candidates=[(i+1,p) for i,p in enumerate(pages) if "suicide" in p.lower()]
        page, text=candidates[0]
        # First block is total/all races, both sexes. Never consume male rows.
        block=text.split("BOTH SEXES",1)[1]
        block=re.split(r"\bMALE\b",block)[0]
        matches=re.findall(r"^\s*(19\d{2})[. ]+\s*(\d+\.\d+)\s",block,re.M)
        assert len(matches)==end-start+1, (name,len(matches))
        for year,rate in matches:
            rows.append(dict(year=int(year),rate=float(rate),country="United States",
                             definition="crude; death-registration states before 1933, US thereafter",
                             source_file=name,source_pdf_page=page,
                             source_url="https://www.cdc.gov/nchs/nvss/mortality/hist290.htm"))
    data=pd.DataFrame(rows).sort_values("year")
    assert data.year.tolist()==list(range(1900,1999))
    return data


def us_recent(name, start, end):
    text=pdf_text(name)
    if name == "cdc_db541_2025.pdf":
        text=text.split("Data table for Figure 1.",1)[1].split("Data table for Figure 2.",1)[0]
    else:
        text=text.split("\f")[0]
    matches=re.findall(r"^\s*((?:19|20)\d{2})[. ]+\s*([\d,]+)\s+(.*)$",text,re.M)
    rows=[]
    for year,number,rest in matches:
        fields=rest.split()
        rate=float(fields[0] if name=="cdc_db541_2025.pdf" else fields[2])
        rows.append(dict(year=int(year),deaths=int(number.replace(",","")),rate=rate,
                         country="United States",definition="age-adjusted; US2000 standard population",
                         source_file=name,source_url="https://www.cdc.gov/nchs/products/databriefs/"+
                         ("db541.htm" if name=="cdc_db541_2025.pdf" else "db241.htm")))
    data=pd.DataFrame(rows).sort_values("year")
    assert data.year.tolist()==list(range(start,end+1))
    return data


def plot(ch,us,recent,later,extended,path):
    fig,ax=plt.subplots(figsize=(10,7),dpi=180)
    ax.plot(ch.year,ch.rate,color="#c4c4c4",lw=2,label="Switzerland (alternative crude series)")
    ax.plot(us.year,us.rate,color="#222222",lw=2.5)
    ax.plot(recent.year,recent.rate,color="#222222",lw=2.5)
    if extended:
        s=later[later.year>=2014]
        ax.plot(s.year,s.rate,color="#222222",lw=2.2,ls="--")
    ax.set(xlim=(1860,2025 if extended else 2020),ylim=(0,30),
           ylabel="Suicides per 100,000 people")
    ax.set_xticks(list(range(1860,2021,20)))
    ax.set_yticks(range(0,31,5))
    ax.spines[["top","right"]].set_visible(False)
    ax.text(1945,27.5,"Switzerland",fontsize=15,color="#888888")
    ax.text(1979,15.6,"United States",fontsize=14)
    ax.text(1890,5,"England/Wales: author series not recovered",fontsize=11,color="#666666")
    ax.set_title("Figure 18-3: Suicide | partial country reconstruction" + (" + US successor" if extended else ""),loc="left",fontsize=12)
    fig.text(.12,.065,"Sources: HSSO D.50a/B.42; CDC HIST290, DB241 (2016), DB541 (2025).\n"
             "Swiss alternative ends 1995; English series missing. US: crude to 1998, age-adjusted from 1999 (not joined).\n"
             "Dashed = US successor after 2014; exact book dataset/definitions not fully established.",fontsize=8)
    fig.subplots_adjust(left=.12,right=.98,top=.9,bottom=.21)
    path.parent.mkdir(parents=True,exist_ok=True)
    fig.savefig(path,facecolor="white")
    plt.close(fig)


def main():
    CLEAN.mkdir(parents=True,exist_ok=True)
    ch,us=swiss(),us_historical()
    recent=us_recent("cdc_db241_table_2016.pdf",1999,2014)
    later=us_recent("cdc_db541_2025.pdf",2003,2023)
    for name,data in [("swiss_alternative",ch),("us_historical",us),("us_1999_2014",recent),("us_successor",later)]:
        data.to_csv(CLEAN/f"figure_18_3_{name}.csv",index=False)
    audit=recent.merge(later,on="year",suffixes=("_2016","_2025"))
    audit["rate_difference"]=audit.rate_2025-audit.rate_2016
    audit["deaths_difference"]=audit.deaths_2025-audit.deaths_2016
    audit.to_csv(CLEAN/"figure_18_3_us_revision_diagnostic.csv",index=False)
    for kind,ext in [("book_period",False),("extended",True)]:
        path=BASE/f"plots/{kind}/figure_18_3_{kind}.png"
        plot(ch,us,recent,later,ext,path)
        compare(ROOT/"references/figures/figure_18_3.png",path,
                BASE/f"plots/comparisons/figure_18_3_{kind}_review.png",
                f"Figure 18-3 {kind.replace('_',' ')} | partial: England missing; Swiss alternative")


if __name__=="__main__":
    main()
