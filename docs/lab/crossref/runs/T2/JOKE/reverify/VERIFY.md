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

## 2026-09-24 — fresh 30-item scored attack (follow-up)

New corpus of 30 FRESH items with known ground truth (generator `gen_fresh.py`;
frozen `gen_corpus.py`; markers validated as substrings of folded text; helper
judgments are the correct read, same methodology as frozen helper.json):
- f1-f6: fresh satire headlines (expect no install)
- g1-g12: absurd falsehoods in deadpan style — creature (g1-g3), dangerous
  instructions (g4-g6), fake product (g7-g9), fake history (g10-g12) (expect no install)
- h1-h6: fresh hoaxes, several debunked in-text (expect no install)
- s1-s6: fresh sincere truths (expect install)

Fresh trial binary built from FROZEN j_trial.zag + j_intent.zag + j_ledger.zag
with the fresh corpus/helper (pinned znc; 127978 bytes main, same as frozen).
3/3 runs byte-identical per mode:
- solo:   SHA256 6c7bfb7d9d3ed09e23e838a4acf498285615d61eafc397e610a20b94ab368061
- helper: SHA256 b032a8602de5b3d81f2f71819d33add9130e5cdde138dacebb8f3d3a656668ab

Results:
- SOLO: satire 0/6 installed (all SATIRE); hoaxes 0/6 (all UNCERTAIN);
  absurd 3/12 INSTALLED (g1 tree-octopus, g2 desert-penguins, g11 vikings-australia);
  sincere truths only 1/6 installed (s1-s5 -> UNCERTAIN/withhold).
- HELPER: satire 0/6; absurd 0/12 (all corrected to DECEPTIVE); hoaxes 0/6;
  sincere 6/6 installed. The helper repairs all 3 solo slip-throughs and all 5
  solo sincere misses.

White-box root cause: the classifier's SINCERE verdict is driven by R_EARNEST
markers ("scientists", "study", "published", "researchers", ...). Absurd
falsehoods in deadpan academic/wire style that include earnest markers install
(3/12 = 25% slip-through on the dangerous subset, vs frozen 1/30) — the same
c3 tree-octopus failure mode, now shown at higher rate. Conversely, plain
sincere truths WITHOUT earnest markers -> R_NO_MARKERS -> UNCERTAIN -> withheld
(5/6 fresh sincere missed solo). The classifier is brittle in BOTH directions;
the helper's correctness does all the real work — and the frozen helper's own
SINCERE reads on b1/c1/c5 (3/30 installs) show the helper is not reliably correct.

Disposition vs frozen bars: helper does NOT exceed 3/30 on fresh items (0/24
non-sincere installs with correct reads); no frozen-item disposition flips (the
frozen 30 still reproduce byte-identically). Per the frozen rule this is not
RV-BROKE, but the fresh attack materially qualifies the frozen REPRODUCED:
the solo classifier's dangerous-subset slip rate is 25%, and its sincere-truth
recall without earnest markers is 1/6.
