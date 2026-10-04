# C9GEN_INSTRUMENT_NOTE.md: C9 instrument chain ready for governance

Wave: wave-20261002-0521pdt | Lane: ARENA | Date: 2026-10-02

## Status: candidate instrument, adoption is a governance decision

This wave leaves a complete, validated C9 instrument chain. It is
offered as a candidate for future governance; nothing here
replaces the frozen arena battery, and no adoption is asserted.

## The chain (all pure Zag, all in this lane)

1. Generator: world_gen_c9d5fix.zag -> bin/world_gen_c9d5fix
   (sha256
   7b50a9c138742b0c8ade1661bad7413a3790289f009a7adeae23fa80124ca381).
   GEN-PASS this wave (C9D5FIX_EVAL.md, prereg bc049ef67):
   deterministic 3/3 byte-identical; 68 items, 291 turns; noisy
   causal observations (CHECK 1 removed); 80/80 real do/do_out
   intervention turns; 3 discrim items with full-chain keys and
   seeded coin-flip candidate order honored in BOTH battery.json
   and turns.jsonl (D5 fixed); old format exploit 0/3.
2. Calibration check: c9fix_check.zag -> bin/c9fix_check. The
   honest two-stage interventional protocol recovers 3/3 chains
   reading only the turn stream (the world admits a genuine
   experiment-driven solution).
3. Scorer: arena_512.zag -> bin/arena_512. Frozen arena.zag logic
   with turn-indexed buffers widened 256 -> 512 (diff-verified as
   the only change); cross-validated byte-identical results.json
   against the frozen scorer on the 131-turn world.
4. Reference contestant: causal_contestant.zag ->
   bin/causal_contestant. CAUSAL-PASS this wave
   (SEALED_EVAL_C9.md, frozen prereg fdaa5c0a4): C9 3/3 via
   intervention statistics, zero regressions, ablation kills C9,
   order-swap invariant. A future C9 contestant must beat this
   reference by mechanism, not by format parsing.
5. Reference world: fixrun2/ (frozen seed 71503461337030).

## What governance would need to decide

- Whether the D5-fixed generator replaces the frozen C9 battery
  for future C9 evaluation (the frozen battery's C9 section is
  unpassable by genuine means; ARENA2 negative finding stands).
- Whether fixrun2 (or a fresh seed's world from the fixed
  generator) becomes the canonical C9 reference world.
- The frozen competitive_arena/ tree was not modified by this
  lane and stays byte-identical regardless.

## Known limits (do not overclaim)

- The instrument covers the 3-variable chain-permutation C9
  family only. It does not test causal discovery in general
  (confounding, cycles, continuous variables, interventions with
  cost, active intervention choice by the learner).
- The reference contestant uses a researcher-specified protocol
  (L1/L2); it is a capability baseline, not an invention result.
- FW1-FW9 remains a regression battery only; 9/9 establishes no
  generality or L3.
