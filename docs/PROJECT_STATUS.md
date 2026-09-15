# Project Status

**Current stage:** Phase 0 — target identity / reproducibility baseline

Initial setup is complete. Metadata-only target inventory tooling and CI are active.

## Progress
- [x] Establish repository baseline and ROM/key exclusion rules
- [x] Add deterministic target inventory tooling
- [x] Add machine-readable version inventory and CI
- [ ] Inventory the first verified Ultra Sun target
- [ ] Record region/language/revision/update/hash metadata
- [ ] Document NCCH/ExeFS/RomFS and executable layout
- [ ] Map code modules/CROs, symbols, functions, and major subsystems
- [ ] Document game-data formats and resource containers
- [ ] Begin bounded source reconstruction
- [ ] Add reconstruction matching verification

Machine-readable inventory: `manifests/version-inventory.json`

## Immediate next milestone
Run `tools/inventory_target.py` on the first local Ultra Sun target or extracted tree, register exact identity, then begin NCCH/ExeFS/RomFS structural mapping. Retail bytes and keys remain local.
