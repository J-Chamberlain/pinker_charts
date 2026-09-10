# Figure14-3 provenance

Original: supplied Supplemental Graphics PDF p24 upper, inspected directly.
Title: Death penalty abolitions,1863-2016. Citation: "Capital Punishment by
Country: Abolition Chronology," Wikipedia, retrieved August15,2016. The book
specifies the last abolition in any jurisdiction/territory; arrow marks2008.

## Original data
MediaWiki revision query ending2016-08-15T23:59:59Z returns revision734519509,
dated2016-08-14T21:58:02Z. Retrieved parsed historical article:
https://en.wikipedia.org/w/index.php?oldid=734519509#Abolition_chronology.
Raw JSON retains revision id and complete source HTML. Modern templates can
render current country labels (e.g. North Macedonia); numerical chronology is
from this pinned article revision. Nearby Internet Archive capture resolves
to2016-10-12, later than citation: retained as candidate, NOT plot input.

`scripts/reconstruct_14_3.py` extracts the chronology HTML table using BeautifulSoup.
It retains year, country labels, stated increment, running total and independently
counted listed countries. Source totals rise to105; listed countries sum to102.
2009 lists4 but adds5;2012 lists2 but adds4. These are source errors, not parsing
errors: the stored table cells were inspected. Published running totals are
preserved to reconstruct the cited source, NOT presented as validated legal data.
The book's territorial-date corrections and some early levels remain unresolved.
Lines connect supplied event-year totals as in the book; no annual values invented.

## Extension and rejected candidates
Current Wikipedia revision1374111817 is retained only as a candidate. It revises
dates and contains internal listed-count inconsistencies. It is NOT used to
extend or silently repair the2016series. DPIC's current chronology also conflicts
with Amnesty categories (e.g. Burkina Faso all-crimes versus ordinary-crimes),
so it is contextual only, not a numerical input.

Ten annual Amnesty publications2016-2025 supply independently classified year-end
all-crimes totals. Each original HTML file is saved with URL/date/hash. A
paragraph-specific parser extracts one unambiguous all-crimes number; ordinary-
crimes/practice totals are excluded. Source URLs are preserved per clean row and
in downloads.json.2016Amnesty104 differs from the cited Wikipedia105; no forced
join.2025total113 independently agrees with report AnnexII p39:
https://www.amnesty.org/en/wp-content/uploads/2026/05/ACT5007782026ENGLISH.pdf.
Current reporting pages can be revised; these frozen downloads are evidence of
what was retrieved, not a claim of original first-publication snapshots.

Wikipedia text is CC-BY-SA with revision attribution retained. Amnesty numerical
facts and source pages are credited; obtain any additional permissions needed
before redistributing full reports in a publication. No proprietary API used.
Reproduce offline: `.venv/bin/python scripts/reconstruct_14_3.py`.
Refresh: retain each new annual reporting page under a new year/version filename,
add an explicit year mapping, validate the all-crimes category and legal timing.
Never overwrite history or infer adoption date from an aggregate change.

Status partial_match: close overall visual trajectory but source legal/date and
counting problems preclude a verified scientific reconstruction. Surrounding
Pinker discussion beyond supplied graphics and independent approval pending.
