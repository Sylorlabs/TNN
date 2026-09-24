# Fork D: SELF-PAM AS DISCIPLINE

## Identity
**DISCIPLINE**: Catches mechanically ungrounded speech and claims **no new evidence about the world**. Never call it corroboration.

## Design
Fork 1 + Fork 3 from `~/workspace/selfpam_r2/debate/museA_forks.md`.

## Mechanism
- **Atom**: `Q|S|POL|R|O`; store adds `|PROV` (EXT or GEN).
- **Kernel**: K1 exact EXT, K2 IS_A transitivity, K3 LOC_IN transitivity, K4 sibling symmetry, K5 ALL→SOME, K6 polarity contradiction, K7 mutex (LOC_ON/UNDER, alive/dead, PROP_NUM), K8 ONLY exact-match.
- **Depth cap**: 3; **Store max**: 128.
- **GEN excluded** from trusted proof; GEN-dependent support is diagnostic `GEN_ONLY`.
- **Deliberation**: PREMISES:, STEPS:, CONCLUSIONS: sections.
- **INSTALL iff**: every draft atom is store-ENTAILED and trace-EARNED, with no UNPARSED or revision.

## Corpora
- **C1**: 140 confabulations (flips F1-F6) → expect WITHHOLD. Bar: ≥70% withhold (M1).
- **C2**: 140 paraphrases (100 direct + 40 surprising) → expect INSTALL. Bar: ≥90% install (M2).
- **C3**: 65 pairs paraphrases (P1-P5, 13 each) → expect INSTALL. Bar: ≥95% install (M3).
- **C4**: 60 trace alibis → expect WITHHOLD. Bar: ≥70% withhold (M4).
- **C5**: 60 provenance (20 mixed EXT+GEN) → expect ?. Bar: ≥70% (M5).
- **C6**: 40 → expect INSTALL (false-withhold ≤5%). Bar: ≥95% install (M6).
- **C7**: Held-out (70/70/65 pairs/30/30/20), disjoint forest/water stock. Bar: all held-out bars pass (M7).

## Build
```bash
./build.sh
```

## Run Battery
```bash
./src/forkD battery corpora/c1/manifest.txt > corpora/c1/results.txt
python3 score.py corpora
```

## No RNG
Verified by grep: no `rand`, `rng`, `seed`, `clock`, `time(`, `getrandom` in `src/*.zag`.

## Provenance Caveat
EXT/GEN is a harness-pinned stand-in, not write-once provenance infrastructure. Any M5 pass carries this caveat.
