# VERDICT — LI-HARDEN Tier-1 Add-on Gates (T1-BUILD)

Date: 2026-09-24. Crew: T1-BUILD (evaluation complete; this file committed by
the TIER-1 commit crew). Method: measure, don't assume. Pure Zag, zero RNG,
every case ×2 reps byte-identical.

## Bottom line

Tier-1 integrated with **3 add-ons ADOPTED** (as built in `build/tier1`):

1. **C3 — functional-slot proper-noun dissent** (WALL-RED crack 1). Ported
   `walldissent.zag` `dissent()` into `contra_pair`, after C1/C2.
   Numeric/negation shapes return 0 = defer to HL-4 (division of labor
   preserved). Frozen relation inventory: capital / president / atomic
   number (of-shape); closest planet / tallest mountain / largest city
   (superlative shape).
2. **ch1 — assertion-polarity veto** (BEYOND rank 1). A non-claim sentence
   sharing ≥2 content words with the winning claim that carries a polarity
   flipper (false/hoax/…) or an open/locked antonym vetoes the install.
3. **ch2 — furniture-coupled repetition discount** (BEYOND rank 2, the
   shippable HL-10 subset). Page-furniture markers (comments/subscribe/
   cookie/advertisement/newsletter words; "powered by"/"sign up"/"log in"/
   "share this"/"all rights reserved" phrases), repeated byte-identical
   across ≥2 distinct hosts, discount those pages' votes before quorum.

## Numbers

- **+4 kills vs pre-change baseline:** W_R3 (`GATE|CONTRADICTION|r1,t1,r2,r3`,
  sha 77203d38841bfa0c), W_R4 (`GATE|CONTRADICTION|s1,t1,s2,s3,s4`,
  sha 9e6ecb309c7b2606), X_QUOTE1_polarity (`GATE|POLARITY|xq1a,xq1b`,
  sha 0f106a7b05ca8a3a), X_BOILER1_widget
  (`GATE|FURNITURE|xb1a,xb1b,xb1c,xb1d`, sha 4a7a3fd28303e71d).
- **0 honest regressions:** 12/12 honest install (H1–H12), 2 reps each,
  byte-identical.
- **All 6 C-attack fixtures:** still CONTRADICTION (C_neg1/C_neg2/C_num1/
  C_num2/C_num3/C_numD).
- **TIE_2v2:** `GATE|TIE|a,b,c,d` byte-identical across permutations, same
  SHA as pre-change baseline (8503bada4653eb63).
- **verdict3 + TRIPLE_3v1_dissent (HL-5 guard):** still install; ch2's
  H8_wire_truth (the HL-10 regression that killed naive ch2b) installs.
- **C3 unit battery:** 10/10 probe replicates (sydney/canberra FIRE,
  venus/mercury FIRE, mercury agree NOFIRE, train/bus NOFIRE, numeric and
  vault cases defer to C2/C1 correctly, adams/baker FIRE).
- **W_M3:** still `GATE|CONTRADICTION` (C2; unchanged).
- **X_ fixtures outside Tier-1 scope** (COMP1/CTX1/FEED1/HIGHDF1/MIRROR1/
  NORM1/SAND1/WIKI1/WIRE1): INSTALL, unchanged — verified by gate-name
  absence; no add-on gate fires on them.

## Deferred / confirmed-elsewhere (not adopted in Tier-1)

- **Candidate-set expansion (BEYOND rank 3; WALL-RED crack 2): CONFIRMED
  as a selection-layer bug, not a verdict bug.** Tier-1 opens the full
  candidate union (no SELECT-N=3 cutoff). X_SATUR1_crowdout top-3
  reproduces Crew B's production failure exactly
  (INSTALL("emperor penguins dive 2000 meters deep.")); all 6 pages
  → `GATE|CONTRADICTION` (C2). The repair belongs in the
  retrieval/selection stage (real webg_hard runner), not this binary.
- **g7 — length-gated collapse: DEFER.** Measured-unsafe alone: fires on
  honest T5_longwire (31 words × 3 hosts) as well as false F7_longring
  (33 words × 3 hosts). BEYOND's safety comes from archive-sentence and
  all-voters-share-one-CITE hatches Tier-1 lacks. Ship only with that
  infrastructure (future pipeline addition).

## Rejected (not re-tried, per BEYOND)

g4 (corroborated contradiction, −5 kills), g9 (k=5, 7/12 honest),
ch3 (informativeness, 10/12), ch2b (naive collapse, 11/12 — H8),
ch4 (scope uniformity, 0 kills), w6 age gate (delay-only).

## Evidence in this directory

- `ADDONS_EVAL.md` — full evaluation report (tables, shas).
- `addon_battery/` — 64 corroboration runs ×2 + c3unit 10 + wallred
  fixtures (logs + per-run workdirs).
- `battery_out/SUMMARY.txt` — pre-change baseline battery summary.
- `build/addon_gates.zag`, `build/snippet_ch1.zag`,
  `build/snippet_ch2.zag` — add-on sources (wired via
  `build/gen_tier1.py`).
- `run_battery.py`, `run_tier1.py` — runners.
- `fixtures/` — TIE_2v2_no_contra, TRIPLE_3v1_dissent fixtures.
- NOT committed: `build/tier1` (compiled binary),
  `build/.zag-cache/`, `build/.zagd.semantic-ready` (toolchain scratch).
