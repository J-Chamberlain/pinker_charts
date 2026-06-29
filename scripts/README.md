# Scripts

These scripts were imported from the local proof-of-concept project.

Current role:

- Preserve the transformation and plotting logic used during the two-figure
  proof of concept.
- Provide a starting point for repository-relative regeneration.

Known limitation:

- Some scripts still contain historical local paths or write to the old
  `outputs/` layout. Before using them as production commands, update them to
  read from `figures/<id>/data/` and write back into the corresponding figure
  directory.

Do not use these scripts to expand to new figures until the path and output
contracts are cleaned up.
