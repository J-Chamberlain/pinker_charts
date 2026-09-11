"""Recover original numerical sersets from authors' 2008 Stata graph archive.

Not pixel digitization: serialized data in their original units, before rendering.
Source: https://users.nber.org/~jwolfers/data/EasterlinParadox.zip
Stata documents data-bearing GPH: https://www.stata.com/manuals15/g-4conceptgphfiles.pdf
The narrow parser below supports only this known v2 little-endian cache layout.
It rejects unknown layouts and validates values against independent text metadata.
"""
from pathlib import Path
import hashlib
import json
import re
import struct
import zipfile
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
try:
    from reconstruct_18_4 import compare
except ImportError:
    from scripts.reconstruct_18_4 import compare

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"figures/18-1"
RAW=BASE/"data/raw"


def decode_serset(section):
    metadata, blob = section.split(b"<BeginSersetData>\r\n",1)
    blob=blob.split(b"\r\n<EndSersetData>",1)[0]
    if blob[:18] != b"sersetreadwrite\x00\x02\x02":
        raise ValueError("Unsupported serset version/byte order")
    ncols,nrows=struct.unpack_from("<II",blob,18)
    if ncols not in [2,7] or nrows != 132:
        raise ValueError("Unexpected original figure dimensions")
    types=blob[26:26+ncols]
    if any(t != 254 and not 1 <= t <= 244 for t in types):
        raise ValueError("Unsupported data type")
    pos=26+ncols
    names=[blob[pos+i*54:pos+(i+1)*54].split(b"\0",1)[0].decode("ascii") for i in range(ncols)]
    text_names=re.findall(rb'\.name = `"([^"\r\n]+)"',metadata)
    if names != [x.decode("ascii") for x in text_names]:
        raise ValueError("Binary/text name mismatch")
    pos += ncols * (54+49)  # fixed name slots and format slots
    extrema=np.frombuffer(blob[pos:pos+16*ncols],dtype="<f8").reshape(2,ncols)
    pos += 16*ncols
    fmt="<"+"".join("f" if t==254 else f"{t}s" for t in types)
    width=struct.calcsize(fmt)
    if len(blob)!=pos+nrows*width:
        raise ValueError("Unexpected record length or trailing data")
    rows=list(struct.iter_unpack(fmt,blob[pos:]))
    result=pd.DataFrame(rows,columns=names)
    series_meta=re.findall(rb"<BeginSeries>\r\n(.*?)<EndSeries>",metadata,re.S)
    for i,(name,t) in enumerate(zip(names,types)):
        if t != 254:
            result[name]=result[name].str.decode("ascii").str.rstrip("\0")
            continue
        # Stata float missing is 0x7f000000 and higher, not IEEE NaN.
        result.loc[result[name]>=2**127,name]=np.nan
        limits=[float(re.search(rb"\."+key+rb" =\s+([^\r\n]+)",series_meta[i])[1]) for key in [b"min",b"max"]]
        observed=[result[name].min(),result[name].max()]
        if not np.allclose(observed,limits,rtol=1e-7,atol=1e-7) or not np.allclose(observed,extrema[:,i]):
            raise ValueError(f"Extrema validation failed for {name}")
    return result


def recover(path):
    data=path.read_bytes()
    sections=re.findall(rb"<BeginSerset>\r\n(.*?)<EndSerset>\r\n",data,re.S)
    if len(sections)!=2:
        raise ValueError("Expected two numerical sersets")
    fit,points=map(decode_serset,sections)
    if points.cty.duplicated().any() or not points.cty.str.fullmatch("[A-Z]{3}").all():
        raise ValueError("Invalid country identifiers")
    arrows=points.dropna(subset=["satlow","sathigh","ylow","yhigh","sat_current_hat"])
    assert np.allclose((arrows.satlow+arrows.sathigh)/2,arrows.sat_current_hat,atol=2e-7)
    assert np.allclose(np.log(arrows.yhigh/arrows.ylow),.5,atol=2e-7)
    return fit,points


def main():
    gph=RAW/"original_fig11.gph"
    archive=RAW/"EasterlinParadox.zip"
    if not gph.exists():
        with zipfile.ZipFile(archive) as z:
            gph.write_bytes(z.read("Figures/fig11.gph"))
            manifest=[{"member":x.filename,"bytes":x.file_size,"crc32":f"{x.CRC:08x}"} for x in z.infolist()]
            (RAW/"archive_inventory.json").write_text(json.dumps({"url":"https://users.nber.org/~jwolfers/data/EasterlinParadox.zip",
                "sha256":hashlib.sha256(archive.read_bytes()).hexdigest(),"members":manifest},indent=2)+"\n")
    fit,points=recover(gph)
    clean=BASE/"data/clean"
    clean.mkdir(parents=True,exist_ok=True)
    fit.to_csv(clean/"figure_18_1_original_fit.csv",index=False)
    points.to_csv(clean/"figure_18_1_original_country_inputs.csv",index=False)
    fit_valid=fit.dropna()
    slope,intercept=np.polyfit(np.log(fit_valid.gdp),fit_valid.sat_current_fit,1)
    residual=np.max(np.abs(fit_valid.sat_current_fit-(slope*np.log(fit_valid.gdp)+intercept)))
    audit={"country_rows":len(points),"visible_country_points":len(points.dropna(subset=["sat_current_hat","gdp"])),
           "complete_arrows":len(points.dropna(subset=["satlow","ylow","sathigh","yhigh"])),
           "cached_fit_log_slope":float(slope),"cached_fit_intercept":float(intercept),
           "maximum_fit_residual":float(residual),"validation":"binary lengths/types/names + text and binary extrema + arrow midpoint/log-width identities",
           "source_gph_sha256":hashlib.sha256(gph.read_bytes()).hexdigest()}
    (clean/"extraction_validation.json").write_text(json.dumps(audit,indent=2)+"\n")
    fig,ax=plt.subplots(figsize=(10,8.4),dpi=180)
    ax.set_xscale("log")
    ax.set(xlim=(400,54000),ylim=(-1.58,1.58),ylabel="Life satisfaction",
           xlabel="Real GDP per capita (thousands of dollars, log scale)")
    ax.set_xticks([500,1000,2000,4000,8000,16000,32000],[".5","1","2","4","8","16","32"])
    ax.minorticks_off()
    ax.set_yticks(np.arange(-1.5,1.6,.5))
    ax.tick_params(labelsize=15)
    ax.xaxis.label.set_size(14)
    ax.yaxis.label.set_size(14)
    # Extend the archived fitted equation to the displayed axis limits only.
    # This is a fit, not added country observations.
    x=np.geomspace(400,54000,100)
    ax.plot(x,slope*np.log(x)+intercept,color="#999999",ls="--",lw=3)
    valid=points.dropna(subset=["gdp","sat_current_hat"])
    ax.scatter(valid.gdp,valid.sat_current_hat,s=55,color="#484848")
    for r in valid.itertuples():
        ax.annotate(r.cty,(r.gdp,r.sat_current_hat),xytext=(0,-14),textcoords="offset points",ha="center",fontsize=12,color="#444444")
    for r in points.dropna(subset=["satlow","ylow","sathigh","yhigh"]).itertuples():
        ax.annotate("",xy=(r.yhigh,r.sathigh),xytext=(r.ylow,r.satlow),
                    arrowprops=dict(arrowstyle="->",color="#292929",lw=1.8,mutation_scale=13,shrinkA=0,shrinkB=0))
    ax.set_title("Figure 18-1: Life satisfaction and income, 2006",loc="left",fontsize=12,pad=15)
    fig.text(.12,.06,"Source: Stevenson & Wolfers (2008), original Figure 11 numerical cache, Gallup 2006.\n"
             "Direct data extraction, not pixel digitization. Microdata analysis not re-executed; reuse terms unresolved.",fontsize=8)
    fig.subplots_adjust(left=.12,right=.98,top=.92,bottom=.18)
    out=BASE/"plots/book_period/figure_18_1_book_period.png"
    out.parent.mkdir(parents=True,exist_ok=True)
    fig.savefig(out,facecolor="white")
    plt.close(fig)
    compare(ROOT/"references/figures/figure_18_1.png",out,
            BASE/"plots/comparisons/figure_18_1_book_period_review.png",
            "Figure 18-1 | original author numerical inputs recovered")
    print(json.dumps(audit,indent=2))


if __name__=="__main__":
    main()
