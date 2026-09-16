# Target Profile: Pocket Monsters Ultra Sun

## Known repository scope

- Repository: `SakuraiTsubaki/PocketMonsters-UltraSun-Decompilation`
- Working target name: Pocket Monsters Ultra Sun
- Platform family: Nintendo 3DS
- Series generation: Generation VII
- Exact release, region, revision, and build: **not yet selected**

The repository name is a working label, not proof of a particular binary. No address, symbol, format, or behavior should be treated as target fact until the exact build is identified.

## Identity checklist

Record all available items before substantive reconstruction:

- official title and product identifier;
- platform and execution environment;
- region, language, revision, update, and distribution form;
- hashes for user-supplied images, executables, modules, or manifests;
- executable/container layout and relevant segment identifiers;
- analysis, extraction, compiler, linker, and SDK tool versions;
- legal provenance and distribution constraints for every input;
- differences from related versions that affect addresses, formats, or behavior.

Store machine-readable identifiers in `config/target.json`. Store restricted inputs outside Git.

## Initial research priorities

- Fingerprint the exact title/update and document the relevant container, ExeFS, RomFS, and executable modules.
- Map code/data segments, relocations, module boundaries, services, and compiler/SDK fingerprints.
- Document target-specific archives, compression, shaders, graphics, text, audio, maps, and scripts.
- Keep encrypted, decrypted, and extracted user inputs outside Git while recording hashes and tool versions.
- Build deterministic extraction and structural/behavior comparison tools for the selected build.

## First milestone

The foundation milestone is complete when the exact target build is recorded, the initial file/executable map is reproducible, at least one research record has been promoted to an analysis with stated confidence, and all commands needed to repeat that result are documented.
