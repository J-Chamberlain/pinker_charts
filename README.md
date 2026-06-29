# Pinker Charts

Research repository for reconstructing selected figures from Steven Pinker's
*Enlightenment Now* from public data sources.

This repository is now the canonical project memory. Future work should begin
by reading [PROJECT_STATE.md](PROJECT_STATE.md), then the relevant figure
directory, before using chat history or doing new research.

## Current Scope

The repository contains the hardened proof of concept for two Chapter 10
figures:

- [Figure 10-5](figures/10-5/README.md): Oil spills, 1970-2016
- [Figure 10-6](figures/10-6/README.md): Protected areas, 1990-2014

No additional book figures have been reconstructed yet. The initial Kindle
List of Figures extraction is preserved at
[data/metadata/kindle_list_of_figures_test.csv](data/metadata/kindle_list_of_figures_test.csv).

## Repository Layout

- [PROJECT_STATE.md](PROJECT_STATE.md): canonical project status, blockers,
  and next tasks.
- [docs/](docs/): lifecycle, workflow, lessons learned, and source-adapter
  playbooks.
- [data/figure_registry.csv](data/figure_registry.csv): canonical queue and
  status table for all captured book figures.
- [figures/](figures/): independently reviewable figure packages.
- [data/](data/): cross-figure metadata, lineage, bibliography, checksums,
  and imported source data grouped by figure.
- [reports/](reports/): narrative reports from the proof of concept.
- [scripts/](scripts/): reproducible Python scripts used during the proof of
  concept and hardening pass.

## Status Vocabulary

- `verified_reproduction`: original dataset or exact archival copy located;
  recreated figure matches within reasonable visual tolerance.
- `updated_equivalent`: original dataset unavailable, but a modern continuation
  from the same institution/source was located.
- `partial_match`: plausible data located, but important variables, time
  periods, or transformations remain missing.
- `source_unavailable`: no usable public dataset found.
- `manual_review_needed`: multiple plausible sources or insufficient evidence.

## Reproduction Notes

The historical local project used absolute paths on one Mac Mini. Repository
docs and metadata have been normalized for review, but some older scripts may
still contain local path assumptions. Treat [PROJECT_STATE.md](PROJECT_STATE.md)
and the per-figure metadata files as the authoritative status layer.

Visual validation assets include cropped figure references and side-by-side
comparison images for research audit purposes. Review copyright and fair-use
constraints before publishing those images on a public website.
