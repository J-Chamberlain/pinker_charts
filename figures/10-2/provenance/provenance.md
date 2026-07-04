# Provenance: Figure 10-2

- Primary visual reference: `references/enlightenment_now_supplemental_graphics.pdf`, page 13.
- Original source visual: xkcd 1007, `Sustainable`, downloaded from xkcd's image URL.
- Underlying observed data: Google Books Ngram API query for `sustainable`, US English 2012 corpus, years 1950-2008, smoothing 3.
- Successor extension data: Google Books Ngram API query for `sustainable`, US English 2019 corpus, years 1950-2022, smoothing 3; only nonzero 2009-2019 extension observations are plotted.
- Transformation: `scripts/reconstruct_10_2.py` parses the API JSON, converts shares to percentages, keeps xkcd future anchors as a separate role, and plots side-by-side comparisons.

## Limitations

xkcd did not publish the exact extrapolation/fitting method. The reconstruction therefore preserves data roles rather than forcing a false exact match: observed Ngram values are source data; future points are xkcd transcript annotations; the connecting future line is an interpolation through those annotations.
