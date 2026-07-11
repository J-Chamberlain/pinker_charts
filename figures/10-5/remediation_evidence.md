# Figure 10-5 Remediation Evidence

Validation date: 2026-07-10 (America/Los_Angeles)

Status remains `partial_match` at lifecycle stage
`source_recovery_and_discrepancy_analysis`. The exact annual 1970-2016 gray
oil-shipped-by-sea line remains unresolved; none of this evidence upgrades the
figure to a verified reproduction.

## Registry consistency

The canonical registry row is:

```csv
10-5,Enlightenment Now,10,"Oil spills, 1970-2016",,1970-2016,partial_match,source_recovery_and_discrepancy_analysis,environment_institutional_dataset,active_high,repository,Target exact Roser 2016r/ITOPF/UNCTADStat oil-shipped-by-sea source or archival equivalent; do not expand until status language remains explicit.,Current repository state: oil-spill line supported; exact annual oil-shipping gray-line source unresolved. See figures/10-5/.
```

Its status and lifecycle stage agree with `PROJECT_STATE.md` and
`figures/10-5/metadata/metadata.json`. The operating rule assigns registry
updates to the orchestrator, so this remediation did not edit the registry.
The SHA-256 before and after remediation is identical:
`2d3c99831e5327da3e2a5b88a5650fec4bd11c67261c2220fe352399c38f1885`.

## RMT diagnostic artifacts

Both documented RMT artifacts are tracked, non-empty repository files:

| Artifact | Size | SHA-256 |
| --- | ---: | --- |
| `figures/10-5/data/candidates/unctad_rmt2020_tanker_trade_selected_years.csv` | 3,583 bytes; 20 lines including header | `55e464b8ae02bb271bc7cfb18461db97a0653e2a7ea9d1bf8db1ed7aec4f7197` |
| `figures/10-5/plots/diagnostics/figure_10_5_rmt_tanker_trade_selected_years_diagnostic.png` | 143,093 bytes | `ded4236b2bd7be1e8af16843bc686062fb45703d513b926a409299fa750b2819` |

The CSV spans selected years 1970-2019. It identifies UNCTAD *Review of
Maritime Transport 2020*, Table 1.1 as the source and states that tanker trade
includes crude oil, refined petroleum products, gas, and chemicals. It is
diagnostic evidence only, not an annual substitute for the unresolved gray
line.

## Regeneration

The canonical portable command, run from the repository root after installing
the script dependencies, is:

```sh
python3 scripts/reconstruct_10_5_source_recovery.py
```

For this validation, the same repository-relative script was run in an
isolated dependency-resolved environment:

```sh
UV_CACHE_DIR=.uv-cache uv run --no-project --with matplotlib --with pandas --with pillow scripts/reconstruct_10_5_source_recovery.py
```

The command exited 0. The temporary `.uv-cache` was removed afterward. The
regenerated artifacts retained their recorded hashes, demonstrating
deterministic output:

| Artifact | SHA-256 |
| --- | --- |
| `figures/10-5/plots/book_period/figure_10_5_book_period_reconstruction.png` | `8810707eda9741f3085f6225a3a65913be607437ef2d26b12836761dee5734e4` |
| `figures/10-5/plots/extended/figure_10_5_extended_reconstruction.png` | `c8c54ac325f104b7dcf916509c8a1f3e77855a57e0ff86a3d92481ef04710549` |
| `figures/10-5/plots/comparisons/figure_10_5_book_style_comparison_captioned.png` | `5bd4e0341f5c75b69ebccd13ca4f78b85d79a2a684caf156106fa41afc658c2c` |
| `figures/10-5/plots/comparisons/figure_10_5_extended_comparison_captioned.png` | `a7ecd8defd98acccca802c2d864e1b48d2a74b9396546da5f8cce1b2ea1f88e9` |

## Visual comparison review

The regenerated captioned book-period and extended comparisons were opened at
full resolution. Both place the book reference beside the repository output.
The book-period output shows the supported spill-count line and explicitly
labels the unrecovered oil-shipping line. The extended output distinguishes
the 2017-2025 spill-count continuation with a dotted line and explicitly says
that no oil-shipping extension is plotted. The RMT diagnostic plot was also
opened and confirms that RMT points are selected-year evidence while the live
UNCTADStat candidate is visually distinguished. These outputs support the
calibrated `partial_match` conclusion rather than an exact visual match.
