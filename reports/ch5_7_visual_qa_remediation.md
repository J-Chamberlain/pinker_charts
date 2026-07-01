# Chapter 5-7 Visual QA Remediation

Date: 2026-06-30

Branch: `track-a-health-nutrition`

## Scope

Reviewed existing side-by-side comparisons for Figures 5-1, 5-2, 5-3, 5-4,
6-1, 7-1, and 7-2. The review focused on whether the recreated panel visibly
matches the PDF/book reference panel in chart type, units, scale, coverage,
and layout.

## Fixes Applied

- Figures 5-1 and 5-2 now use the supplied supplemental PDF chart references
  instead of dark Kindle screenshot crops.
- Figure 5-1 PDF crop was widened after visual inspection showed that the
  y-axis label was clipped.
- Figure 5-2 proxy series were trimmed to the coverage windows visible in the
  book reference, improving the side-by-side match without digitizing book
  values.
- Figure 6-1 no longer displays a misleading grouped bar-chart proxy. The
  comparison now shows the PDF line-chart reference beside a reconstruction
  blocked panel with the same axis context.

## Figure-by-Figure Visual Review

### Figure 5-1

Visual status: close.

The recreated regional line chart matches the original chart form, axis range,
and broad regional ordering. Remaining differences are mainly typography and
label placement. The extended panel remains explicitly marked as no comparable
extension plotted.

### Figure 5-2

Visual status: partial.

The recreated line chart now uses the same PDF reference and more comparable
country coverage windows. Remaining mismatches are visible in country line
shape, source vintage, and endpoint label crowding. The figure should remain
`partial_match`.

### Figure 5-3

Visual status: partial but usable for review.

The recreated chart uses the correct line-chart form and percent unit. The
overall shape is close for Sweden and the later declining series, but exact
source-vintage differences remain visible, especially for labels and some
country trajectories.

### Figure 5-4

Visual status: not visually adequate.

The recreated chart is missing most of the age-specific series visible in the
book reference. This cannot be fixed by styling; it requires targeted recovery
of the exact age-specific HMD/OWID source series.

### Figure 6-1

Visual status: blocked.

The book reference is a five-line annual time series in thousands of under-5
deaths. The previous recreation was a grouped bar chart in percent shares,
which was the wrong chart type, unit, and endpoint. That misleading proxy has
been removed. The current side-by-side marks reconstruction as blocked until
the cited CHERG/WHO Liu et al. 2014 supplementary appendix annual data, or a
verified equivalent, are recovered.

### Figure 7-1

Visual status: partial.

The recreated chart uses the correct line-chart form and calorie units. The
major visual differences appear to be source-vintage and series construction
differences, particularly in France and later developing-country trajectories.

### Figure 7-2

Visual status: partial.

The recreated chart uses the correct line-chart form and stunting percentage
unit. The Bangladesh and Kenya trajectories are plausible, but the exact
OWID/Roser 2016j WHO NLIS vintage remains unrecovered and visible differences
remain.

## Editorial Outcome

No figure was promoted to verified status in this remediation pass.

The main corrected workflow lesson is that generating a side-by-side image is
not sufficient. Codex must inspect it visually and continue iterating when the
chart type, unit, coverage, or visual encoding is plainly wrong.
