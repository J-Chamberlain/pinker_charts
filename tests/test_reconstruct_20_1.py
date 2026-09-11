from scripts.reconstruct_20_1 import recover, cohort


def test_saved_poll_tables_recovered():
    data = recover()
    assert len(data) == 10
    assert data[data.series.eq("Trump")].percent.tolist() == [52, 52, 41, 36]
    assert data[data.series.eq("Brexit")].percent.tolist() == [60, 57, 56, 48, 38, 27]
    assert data.source_url.notna().all()


def test_open_bin_not_given_invented_midpoint():
    x, method = cohort("65 & over")
    assert x == 1951
    assert "bound" in method
    assert cohort("18-29")[0] == 1992.5
