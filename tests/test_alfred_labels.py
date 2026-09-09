import json

import pytest

from scripts.alfred_labels import read_labels, vintage_values


def test_retained_numeric_labels_require_units_unique_years_and_coverage(tmp_path):
    path = tmp_path / "labels.json"
    data = {"url": "https://alfred.stlouisfed.org/series?seid=TEST", "retrieved_date": "2026-09-09",
            "observations": [{"label": "1929, 1,234.50 Billions of Dollars",
                              "series": "Test Vintage: 2016-07-29 series with 1 points"}]}
    path.write_text(json.dumps(data))
    assert vintage_values(path, "2016-07-29", 1929, 1929).iloc[0] == 1234.5
    assert read_labels(path).value_text.iloc[0] == "1,234.50"
    with pytest.raises(ValueError, match="expected"):
        vintage_values(path, "2016-07-29", 1929, 1930)
    data["observations"] *= 2
    path.write_text(json.dumps(data))
    with pytest.raises(ValueError, match="duplicate"):
        read_labels(path)
    data["observations"] = data["observations"][:1]
    data["observations"][0]["label"] = "1929, 10 Percent"
    path.write_text(json.dumps(data))
    with pytest.raises(ValueError, match="units"):
        read_labels(path)
