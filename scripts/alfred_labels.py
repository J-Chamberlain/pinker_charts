"""Parse retained ALFRED numeric accessibility observations, never image coordinates.

Source: https://alfred.stlouisfed.org/ ; each retained export carries its series URL.
The exported labels have display precision, not necessarily download precision.
"""
import json
import re
from pathlib import Path

import pandas as pd


def read_labels(path: Path) -> pd.DataFrame:
    payload = json.loads(path.read_text())
    rows = []
    for observation in payload["observations"]:
        value = re.fullmatch(r"(\d{4}), ([\d,.]+) Billions of Dollars", observation["label"])
        vintage = re.search(r" Vintage: (\d{4}-\d{2}-\d{2}) series with (\d+) points$", observation["series"])
        if not value or not vintage:
            raise ValueError(f"Unexpected ALFRED units or label: {observation}")
        rows.append({"year": int(value[1]), "value": float(value[2].replace(",", "")),
                     "value_text": value[2], "vintage": vintage[1],
                     "unit": "billion current USD", "series": observation["series"].split(" Vintage:")[0],
                     "url": payload["url"], "retrieved_date": payload["retrieved_date"],
                     "expected_count": int(vintage[2])})
    frame = pd.DataFrame(rows)
    if frame.empty or frame.duplicated(["year", "vintage"]).any():
        raise ValueError("Empty or duplicate ALFRED observations")
    for _, group in frame.groupby("vintage"):
        years = sorted(group.year.tolist())
        if len(group) != group.expected_count.iloc[0] or years != list(range(min(years), max(years) + 1)):
            raise ValueError("Incomplete or nonannual ALFRED export")
    return frame.drop(columns="expected_count")


def vintage_values(path: Path, vintage: str, start: int, end: int) -> pd.Series:
    frame = read_labels(path)
    group = frame[frame.vintage.eq(vintage)].set_index("year").sort_index()
    if group.index.tolist() != list(range(start, end + 1)):
        raise ValueError(f"{path}: expected {vintage}, {start}-{end}")
    return group.value
