# VERIFY — T2-JOKE (independent re-verification)

**Re-verifier:** replacement coordinator (Wave-2 crossref), 2026-09-23 PDT.
**Frozen authority:** commit `7b2100d09911c5c10252c5756c7def288e70bd1f`, `docs/lab/crossref/PREREG_TIER2.md`, section T2-JOKE (extracted programmatically).
**Tier-2 crew verdict under test:** REPRODUCED (frozen PARTIAL).

## Pins
- Trial freeze (pre-run): `8f33adac1a43249d4d5f2cebdc1cf4a24e3fed0d`
- Trial evidence (post-run): `d7e59016792c1596d1f4fb27a9c213221c18e0c5`
- Sources fetched via API with blob-SHA verification from `docs/lab/senses/web-search/joke-lie-trial/src/`
- Toolchain: pinned znc. Zero RNG.

## Frozen PARTIAL reproduction
- `j_trial.zag` rebuilt: `wrote native binary j_trial_bin (127978 bytes main)`.
- 5 runs solo + 5 runs helper, all byte-identical:
  - solo: SHA256 `14aa6774baf577b217b72dc4784070255b40e0793a93586cd45978d55fa8ce6d` — EXACT match to committed.
  - helper: SHA256 `3cfd88c0ae9130d7f9c4ae597d4d1c1621271cf1923689899f7dd0109163d771` — EXACT match to committed.
- Bar figures (independent parse):
  - solo: joke catch 1/6 = 0.167 (K1 TRIPPED) ✓; non-sincere installed 1/30 = 0.033 (c3 tree-octopus) ✓
  - helper: joke catch 4/6 = 0.667 ✓; non-sincere installed 3/30 = 0.10 (b1 glue pizza, c1 Apple Wave, c5 Damascus) ✓
  - Glue-on-pizza: SOLO intent=2 (JOKING), install=2 (WITHHOLD) ✓; HELPER intent=1 (SINCERE), install=1 (INSTALL) ✓

## Red-team (fresh harder items, per frozen method)
9 fresh items through the frozen `j_classify`:
- Harder deadpan jokes: rt1 (4D vision) → SINCERE/INSTALL; rt2 (tabs) → SINCERE/INSTALL; rt3 (sourdough) → UNCERTAIN/withhold.
- Glue variants: rt4 (paraphrase) → UNCERTAIN/withhold; rt5 (warning) → JOKING/withhold.
- Fresh hoaxes: rt6 (bleach) → JOKING/withhold; rt7 (moon hologram) → SINCERE/INSTALL.
- Sincere truths: rt8 (Eiffel), rt9 (water boil) → UNCERTAIN/withhold (should install).

**Finding:** 2/3 harder deadpan jokes installed as sincere; 1/2 fresh hoaxes installed; 2/2 sincere truths withheld. The classifier is brittle on fresh harder items. This does NOT flip any frozen disposition (the 30 frozen items reproduce byte-identically), so per the frozen rule it is not RV-BROKE, but it is a material qualification.

## Verdict: REPRODUCED (frozen PARTIAL)
All frozen bars match including the solo K1 trip and glue-on-pizza split. Red-team reveals brittleness on fresh harder items (documented above, not hidden).
