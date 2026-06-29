# Kindle Figure-Source Extraction Test: Enlightenment Now

## What Was Captured

- Extracted 75 visible List of Figures entries from two Kindle screens.
- The list appeared to end after `20-1`; paging forward went to the Preface rather than more figure-list entries.
- Page/location references were not shown in the List of Figures view, so untested rows use the visible list screen as their location note.

## Figures Tested

### Figure 10-5: Oil spills, 1970-2016

- Navigation: clicked from the List of Figures after dismissing a one-time Kindle "Preview Links" popup.
- Kindle display location: Page 131 of 556, 20%, Chapter 10.
- Citation/source found: yes.
- Captured citation snippet: `Source: Our World in Data, Roser 2016r, based on data (updated) from the International Tanker Owners Pollution Federation.`
- Note: the visible source line continued with a URL and short data definitions.

### Figure 10-6: Protected areas, 1990-2014

- Navigation: manual page-forward from the Figure 10-5 page.
- Kindle display location: Page 133 of 556, 21%, Chapter 10.
- Citation/source found: yes.
- Captured citation snippet: `Source: World Bank 2016h and 2017, based on data from the United Nations Environment Programme and the World Conservation Monitoring Centre.`
- Note: the visible source line continued with a compilation credit.

## Reliability Assessment

Kindle plus Computer Use is viable for a chapter-by-chapter metadata workflow, but it is only moderately reliable without an OCR/text-selection assist. The figure links are useful, but Kindle introduced a one-time link-preview popup and the first coordinate click did not land where expected. Once on a figure page, nearby figures were easy to reach by manual paging, and source lines were readable when the figure and caption were visible on screen.

Recommended next-batch changes:

- Work chapter-by-chapter rather than from the entire List of Figures whenever possible.
- After each navigation action, capture and inspect the screen before recording data.
- Prefer list hyperlinks for the first figure in a chapter, then page manually through adjacent figures.
- Keep a `navigation_notes` habit in the CSV notes field for popups, overlay interference, and OCR uncertainty.
- Use a larger Kindle font or a narrower window only if captions remain fully visible; otherwise preserve the current two-page layout because it exposes figure and source together.

## Validation Notes

- Figure IDs use a consistent `chapter-number` format such as `10-5`.
- Every row has a non-empty figure title.
- The two tested rows, `10-5` and `10-6`, have `citation_text` populated.
- Unchecked rows are explicitly marked `not_checked`.
