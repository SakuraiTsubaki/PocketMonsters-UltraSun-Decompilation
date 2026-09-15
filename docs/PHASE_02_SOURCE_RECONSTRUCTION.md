# Phase 02 — Source Reconstruction Bootstrap

## Objective

Establish the first verified source-reconstruction map for **Pokémon Ultra Sun** from local extracted metadata while keeping original game binaries out of Git.

## Required local inputs

- extracted `exheader.bin`
- extracted ExeFS `.code`
- decompressed `.code` when required by the exheader flag
- extracted RomFS directory

## Generated metadata

1. `inventory_extracted_tree.py` — path/size/SHA-256 inventory
2. `inspect_3ds_exheader.py` — executable memory map
3. `map_3ds_code_layout.py` — virtual-address ↔ `.code` file-offset map
4. `classify_romfs.py` — structural RomFS clustering

Recommended outputs:

- `analysis/executable/exheader.json`
- `analysis/executable/code_layout.json`
- `analysis/romfs/classification.json`

## Reconstruction queues

After the target and section map are verified, classify code/data into startup/runtime, resource loading, event/script, field/map, battle, Pokémon data, UI/text, save, communication, and graphics/audio queues. Unknown regions stay unknown until supported by evidence.

## Ultra Sun ↔ Ultra Moon comparison

Use `Sakurai/tools/compare_gen7_inventories.py` after both full inventories exist. Separate identical content, same-path modifications, version-only resources, and content moved to different paths.

Sun/Moon findings may be used as comparative evidence, but Ultra Sun/Ultra Moon are separate targets and must not inherit addresses or labels without verification.

## Exit criteria

- exact target revision recorded
- `.code` layout verified
- full RomFS inventory reproducible
- first executable/resource families evidence-backed
- Ultra Sun/Ultra Moon machine-generated difference baseline produced
