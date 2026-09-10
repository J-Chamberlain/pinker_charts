"""Recover Figure14-1 public data without redistributing full restricted datasets.

Source terms: https://www.systemicpeace.org/inscrdata.html
Full numerical releases stay in .private_sources/ (ignored by Git).
Repository exports contain only global aggregates and release references.
"""
import argparse
import hashlib
import json
from pathlib import Path

import pandas as pd

try:
    from scripts.source_cache import fetch
except ModuleNotFoundError:
    from source_cache import fetch

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures/14-1"
CACHE = ROOT / ".private_sources/14-1"
SOURCES = {
    "hp_2016.html": ("https://web.archive.org/web/20160812092952id_/http://humanprogress.org/f1/2560", "7493f888d738a662d75dd5f6bc90f61ff59bee816bc21eb9744146a532884c86"),
    "hp_f1_archive.html": ("https://web.archive.org/web/20170427220920id_/http://humanprogress.org/f1/2560", "cbe92c448087722dad036ee2b07661830febce4bce2a8d8fc21ab4736a560a4f"),
    "p4v2015.xls": ("https://www.systemicpeace.org/inscr/p4v2015.xls", "3539f76feb80160d78abb7c583da767bde59d19398c50f2fd134ae8ca64b18c5"),
    "p4v2018.xls": ("https://www.systemicpeace.org/inscr/p4v2018.xls", "944f6f366c59ab25890d8d317a45caf24106fd3a9255d05439e7ef0ee4c14472"),
    "p5v2018.xls": ("https://www.systemicpeace.org/inscr/p5v2018.xls", "f81248561cb4fd884b0a439c7c0af298bc7f81b993bcd42e006988cb6d37a71c"),
}


def aggregate_polity(path):
    frame = pd.read_excel(path)
    if frame.duplicated(["ccode", "year"]).any():
        raise ValueError("Duplicate country-year")
    frame["valid_polity"] = frame.polity.where(frame.polity.between(-10, 10))
    return frame.groupby("year").agg(
        polity_valid_mean=("valid_polity", "mean"), polity2_mean=("polity2", "mean"),
        n_valid=("valid_polity", "count"), n_polity2=("polity2", "count"),
        n_rows=("polity", "size")).reset_index()


def main(download=False):
    manifest = []
    for name, (url, expected) in SOURCES.items():
        path = CACHE / name
        if download:
            fetch(url, path, FIG / "source_logs/downloads.json")
        if not path.exists():
            raise FileNotFoundError(f"Missing local source {path}; run with --download")
        sha = hashlib.sha256(path.read_bytes()).hexdigest()
        if sha != expected:
            raise ValueError(f"Source version changed: {name}; inspect before refreshing")
        manifest.append({"filename": name, "url": url, "sha256": sha,
                         "local_cache_path": path.relative_to(ROOT).as_posix(),
                         "redistribution": "full source retained locally, excluded from Git pending permission"})
    html = (CACHE / "hp_f1_archive.html").read_text()
    decoder = json.JSONDecoder()
    metadata = decoder.raw_decode(html.split("gon.dataset=", 1)[1])[0]["data"]
    frame = pd.DataFrame(decoder.raw_decode(html.split("gon.countries=", 1)[1])[0]["data"])
    if metadata["_id"] != 2560 or metadata["calculation_type"] != "Average":
        raise ValueError("Unexpected HumanProgress dataset")
    world = frame[frame.country.eq("World")][["year", "value", "generated"]].sort_values("year")
    if world.year.tolist() != list(range(1800, 2016)):
        raise ValueError("Incomplete World trajectory")
    earlier = (CACHE / "hp_2016.html").read_text()
    earlier_frame = pd.DataFrame(decoder.raw_decode(earlier.split("gon.countries=", 1)[1])[0]["data"])
    earlier_world = earlier_frame[earlier_frame.country.eq("World")][["year", "value"]]
    audit = world.merge(earlier_world, on="year", suffixes=("_2017_capture", "_2016_capture"), validate="one_to_one")
    audit["capture_difference"] = audit.value_2017_capture - audit.value_2016_capture
    if len(audit) != 216 or audit.capture_difference.abs().max() > 1e-12:
        raise ValueError("Archived World data changed; inspect release differences")
    out = FIG / "data/raw"
    out.mkdir(parents=True, exist_ok=True)
    world.to_csv(out / "hp_world_2016.csv", index=False)
    audit.to_csv(out / "hp_archive_agreement.csv", index=False)
    (out / "hp_metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    (out / "source_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    for version in ["p4v2015", "p4v2018", "p5v2018"]:
        aggregate_polity(CACHE / f"{version}.xls").to_csv(out / f"{version}_world_aggregates.csv", index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--download", action="store_true")
    main(parser.parse_args().download)
