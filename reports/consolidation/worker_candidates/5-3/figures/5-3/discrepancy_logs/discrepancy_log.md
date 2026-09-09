# Discrepancy Log: Figure 5-3

- Side-by-side comparisons regenerated with `scripts/reconstruct_5_3.py`.
- The visible book axes are now matched more closely: 1750-2020 x-range with 1750-2010 ticks and 0-1.5 percent y-range.
- Sweden, United States, and Malaysia now use recovered Gapminder GD010 values wherever available. This fixes the prior major discrepancy where Malaysia appeared only near 2000.
- Ethiopia remains a source-vintage discrepancy: the recovered Gapminder workbook does not include Ethiopia, and the exact book-era OWID/World Bank 2015 supplement was not recovered. The plotted Ethiopia segment uses current OWID successor data and is labeled as such in the clean CSV.
- Short post-Gapminder tails for Sweden, United States, and Malaysia also use current OWID successor fill because the exact book-era OWID tail values were not recovered.
- Current status remains `partial_match`; do not promote to `verified_reproduction`.
