# Bug / Glitch Eradication Track — Pocket Monsters Ultra Sun

## Objective

Remove every reproducible bug, glitch, crash, softlock, incorrect battle rule, text/data error, visual/audio defect, overflow/underflow, invalid state transition, save-risk condition, and other unintended behavior that can be demonstrated in the selected Pocket Monsters Ultra Sun target.

This is a living evidence-backed inventory. New findings must be added instead of being silently omitted.

## Target state

- Repository target: Pocket Monsters Ultra Sun
- Platform: Nintendo 3DS
- Latest official game update baseline: Ver. 1.2
- Exact ROM/update/region/revision/hash in this repository: **not selected yet** (`config/target.json`)
- ROM binaries remain outside Git; hashes, extracted non-ROM data, patches, tests, logs, and reports belong in the repository.

## Required workflow

1. Fingerprint the exact base ROM and update layer.
2. Inventory ExeFS, RomFS, executable modules, scripts, tables, text, models, audio, and save-related structures.
3. Reproduce each applicable issue on the selected build.
4. Locate the exact code/data/resource cause.
5. Apply the smallest behavior-correct fix without deleting unrelated original content.
6. Add deterministic regression coverage.
7. Re-test adjacent battle, overworld, save, communication, and event paths.
8. Preserve evidence for fixed, not-applicable, cannot-reproduce, and research-needed cases.

## Officially fixed issues that must remain fixed

### Ver. 1.1

- Occasional freeze after choosing Litten in the opening sequence.
- Wide Guard interacting incorrectly with some Z-Moves.
- Ion Deluge failing to behave correctly.
- Move Tutor/BP learning overwriting or forgetting an existing move when the Pokémon had fewer than four moves.

### Ver. 1.2

- Additional gameplay fixes, including the Version 1.1 QR-event battle freeze class reported for String Shot, Forest's Curse, Power Trick, and non-Ghost Curse.

## Known latest-version candidates to investigate and eliminate

### Battle / mechanics

- Charge Beam additional-effect chance overflow with Serene Grace + pledge rainbow.
- Rollout stored-power state surviving interaction with Mimikyu Disguise.
- Shell Trap + Encore stale trap state.
- Toxic same-turn sure-hit state leakage.
- Trick Room effective-Speed overflow/rollover at extreme Speed values.

### Data / text / form logic

- Case-conversion failure for language-specific characters in text entry.
- Japanese/Chinese emoticon display mapping error.
- Giratina + Nectar invalid form/cry behavior.
- Therian Thundurus incorrectly blocked from learning Smart Strike.
- Partner Cap Pikachu shiny-lock check using the player's trainer data rather than the event Pokémon's intended data.
- Silvally Move Tutor offering only Grass Pledge despite data indicating all three pledge moves.
- French post-Mallow-trial dialogue using the feminine pronoun regardless of selected player character.

### Overworld / presentation

- Disguised Chef Ditto event pathing collision that leaves the chef running into the player before dialogue.
- Any remaining model, animation, camera, outline, audio, or script-state defects demonstrated on Ver. 1.2.

## Evidence status rules

- `CONFIRMED-ROM`: reproduced against the selected ROM/update hash.
- `CONFIRMED-DATA`: directly proven by extracted code/data but not yet reproduced in gameplay.
- `OFFICIAL-FIX`: documented by Nintendo / Pokémon official update notes.
- `PUBLIC-REPORT`: reproducible public report not yet confirmed against our target.
- `RESEARCH-NEEDED`: trigger/cause/version scope remains uncertain.
- `FIXED`: patch applied and regression verification passed.

## Primary references

- Nintendo Support — Pokémon Ultra Sun / Ultra Moon update history: https://en-americas-support.nintendo.com/app/answers/detail/a_id/28054/p/605/c/120
- Bulbapedia — Generation VII glitch index: https://bulbapedia.bulbagarden.net/wiki/List_of_glitches_in_Generation_VII
- Bulbapedia — Generation VII battle glitches: https://bulbapedia.bulbagarden.net/wiki/List_of_battle_glitches_in_Generation_VII
- Bulbapedia — Generation VII overworld glitches: https://bulbapedia.bulbagarden.net/wiki/List_of_overworld_glitches_in_Generation_VII

## Immediate blocker

No exact Ultra Sun ROM/update build is selected in `config/target.json`. Do not invent offsets, file names, symbols, functions, or patch bytes. Fingerprint the actual input first, then promote each candidate into a ROM-backed reproduction and regression case.
