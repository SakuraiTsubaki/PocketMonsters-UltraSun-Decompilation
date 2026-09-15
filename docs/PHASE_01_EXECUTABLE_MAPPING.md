# Phase 01 — Executable Mapping

## Goal

Establish a reproducible executable baseline for the exact local Pokémon Ultra Sun target before function naming or source reconstruction begins.

## Inputs

Use only a locally owned/extracted target. Do not commit ROM/CXI/CCI/3DS images, encrypted title packages, keys, or extracted proprietary executable binaries.

Expected local inputs include an extracted game tree, `exheader.bin`, ExeFS `.code` / `code.bin`, and the RomFS tree.

## Step 1 — Inventory

```bash
python tools/inventory_extracted_tree.py /path/to/extracted-game \
  --project "Pokemon Ultra Sun" --platform "Nintendo 3DS" \
  -o manifests/local/inventory.json
```

## Step 2 — Map System Control Info

```bash
python tools/inspect_3ds_exheader.py /path/to/exheader.bin \
  -o manifests/local/exheader-map.json
```

Record application title, remaster version, ExeFS code compression flag, `.text`, `.rodata`, `.data`, BSS, stack size, and dependency program IDs.

## Step 3 — Establish code image

If the exheader reports compressed ExeFS code, decompress the local `.code` before instruction-level analysis. Do not commit the proprietary code image. Use target-derived addresses rather than guessed or cross-title values.

## Step 4 — First reconstruction outputs

Repository-safe outputs include function/symbol maps, section maps, call-graph metadata, data-structure notes, reconstructed source, scripts, tests, hashes, and verification manifests.

## Evidence status

Until a real local target has been inventoried, all game/revision-specific values remain **Unverified**.
