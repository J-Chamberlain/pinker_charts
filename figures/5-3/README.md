# Figure 5-3: Maternal mortality, 1751-2013

Status: `verified_reproduction` for the book-period data and encoding.

The reconstruction uses the preserved Our World in Data dataset 522, which
combines Gapminder's 2010 historical compilation with World Bank 2015 values
without adjustment. The supplemental PDF was located through its indexed
College Sidekick record, but its original pixels could not be downloaded in
this run because the host returned a Cloudflare denial. The reference image in
this package is therefore explicitly labeled as an evidence-based facsimile,
not an original page capture.

Run with:

```sh
PYTHONPATH=tmp/pydeps python3 scripts/reconstruct_5_3.py
```

The script assumes `matplotlib` and `Pillow` are available. It never uses
digitized chart values.
