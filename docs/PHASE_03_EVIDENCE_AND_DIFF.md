# Phase 3 — Evidence Extraction and Binary Diff

This phase begins after the exact target build and executable layout have been verified.

## Goals

- Build a reproducible evidence index from the decompressed ExeFS `.code` image.
- Narrow Ultra Sun/Ultra Moon code differences without embedding executable bytes in reports.
- Generate pointer candidates only inside verified mapped address ranges.
- Keep all labels provisional until a reference is confirmed by code/data behavior.

## Required inputs

- verified `exheader.json`
- verified `code_layout.json`
- locally extracted/decompressed ExeFS `.code`
- paired-version `.code` when performing Ultra Sun ↔ Ultra Moon comparison

## Tools

- `tools/extract_binary_evidence.py` — indexes string candidates; default reports omit literal text.
- `tools/compare_binary_blocks.py` — fixed-size hash-only binary comparison.
- `tools/scan_pointer_candidates.py` — aligned little-endian integer scan inside researcher-supplied verified address ranges.

## 3DS workflow

1. Run `inspect_3ds_exheader.py`.
2. Run `map_3ds_code_layout.py` on a decompressed `.code` image.
3. Use mapped `.text/.rodata/.data` ranges to select address intervals.
4. Generate binary evidence indexes.
5. Compare Ultra Sun ↔ Ultra Moon only when both exact target revisions are known.
6. Generate pointer candidates inside verified section ranges.
7. Create function/data labels only after direct evidence or reproducible cross-version correspondence.

## Evidence rules

- Do not copy function names or addresses between Ultra Sun/Ultra Moon merely because binaries are similar.
- Do not inherit Sun/Moon addresses without independent verification.
- Numeric values inside an address range are only candidate pointers.
- String candidates do not establish function purpose on their own.
- Changed 4 KiB blocks are localization targets, not function boundaries.
- Unknowns remain unknown until verified.

## Repository policy

Do not commit ROM/CXI images, encrypted title content, proprietary executable payloads, keys, or literal extracted text dumps. Commit tooling, hashes, metadata, reconstructed source, analysis tables, and verification records according to project policy.
