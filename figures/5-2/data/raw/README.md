# Figure 5-2 raw and candidate data

- `owid_gapminder_child_mortality_2013.csv`: previously tested proxy, rejected
  as the canonical source because it draws early country lines absent from the
  book.
- `owid_current_child_mortality.csv`: closest live OWID successor proxy, stored
  in percent units. It is not the recovered Roser 2016a source.
- `owid_current_child_mortality.metadata.json`: live OWID metadata retrieved
  2026-07-10 local time (endpoint reports 2026-07-11 UTC); it identifies
  changed Gapminder (2015)/UN IGME (2025) sources.
- `../candidates/owid_cme_info_2016.csv` and its datapackage: immutable archival
  OWID dataset 161 from commit `b6746f923dd64ca0fad7de1b1f2f78bebe25205f`.
  OWID metadata records retrieval from CME Info on 2016-01-29. It is a
  contemporaneous source component, but covers only 1970–2015.
