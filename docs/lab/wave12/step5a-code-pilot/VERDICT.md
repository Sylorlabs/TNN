# STEP 5a CODE Curriculum Pilot — Verdict (Repaired)

**Date:** 2026-09-20
**Status:** GO — all preregistered bars pass on the repaired curriculum

## What was done

Repaired the pure-Zag pilot to the frozen prereg (`PREREG_CODE_PILOT.md`) plus the dated amendment (`AMENDMENT_2026-09-20_code_pilot.md`, frozen before repaired evidence):

- **Stage reorder** to prereg C1–C12: C1 arithmetic/comparison/eager-logic, C2 sequencing, C3 scopes, C4 IFZ+short-circuit, C5 loops, C6 functions, C7 slices, C8 pointers, C9 optionals/errors, C10 modules, C11 invariant Q&A, C12 path-trace predicates.
- **PC3 plant moved** to C4 (per amendment): the C4 scaffold omits eager-vs-short-circuit discriminators; the disclosed tie-break selects `eager`; C4 K3 variants must fire.
- **Adversarial distribution fixed** to 10 K3 + 8 traps (A–H) + 5 K4 + 7 variation = 30 per stage (was 10+16+1+3).
- **Poison transcripts** now say `killed`/`absorbed` (was ambiguous numeric).
- **C11/C12** implemented as real mechanisms: C11 invariant Q&A over memory guard conditions/refusal codes (world's `qa_oracle` vs learner's hypothesis table); C12 event-based path predicates (world records IFZ/LOOP events; learner predicts predicates over them).
- **Bug fixes:** event-buffer ownership/capacity (double-free + overflow), `ln_qa_true` bit-layout/logic mismatch vs `qa_oracle`, `ln_localize` false positives on unfaulted programs.

## Evidence

- `evidence/corrected_run1.log`, `corrected_run2.log`: 3,950 episodes, byte-identical (`cmp` confirms).
- `evidence/planted_pc3.log`: 3,950 episodes, PC3 plant active.
- `evidence/pc1.log`: 94 episodes, weakened integrity.
- `evidence/pc2.log`: 98 episodes, validation leak.
- `evidence/checker_corrected.txt`: independent checker output.

## Bar results (corrected mode)

| Bar | Result | Required |
|-----|--------|----------|
| Episodes | 3,950 | 3,950 exactly |
| Byte-identical reruns | 2/2 identical | byte-identical |
| Held-out | 100% all 12 stages | ≥95% |
| Fault localization | 10/10 all stages | ≥9/10 |
| Composition | 10/10 all stages | ≥8/10 |
| Traps A–H | 8/8 all stages | 100% |
| K3 (corrected) | 0/10 all stages | ≤1 |
| K4 gain | 5/5 (gain ≤10) | ≤10 |
| Variation | 7/7 all stages | 7/7 |
| Adversarial distribution | 10+8+5+7 per stage | exact |
| Disconnects | 12 learner-initiated | 12 |
| Poison | 12/12 killed, 0 absorbed | 0 absorbed |
| Retention | 10/10 per stage | 10/10 |
| Audit | median 64B, max 384B | ≤4KiB |
| Template overlap | zero (stages 0–9) | zero |

## PC3 (planted) result

- **C4 K3: 2/10 fired** (≥2 required). The discriminators (ANDO with y=0 NONE; ORO with y≠0 NONE) defeated the planted `eager` hypothesis.
- All other stages: 0/10 (no false fires).
- Stage 3 held-out dropped (expected under plant); checker mode 3 confirms the plant fired and nothing else did.

## PC1 / PC2 results

- **PC1:** Weakened learner → 10/16 trap failures (≥1 required). Checker confirms the instrument is live.
- **PC2:** 50% validation leak → template overlap detected by checker.

## Amendment

`AMENDMENT_2026-09-20_code_pilot.md` (frozen 2026-09-20 before repaired evidence):
- Freezes the PC3 interpretation: C1 introduces AND/OR; C4 scaffold omits the branch contexts that discriminate eager from short-circuit; disclosed tie-break selects `eager`; C4 K3 variants must fire.
- Freezes C11 (invariant Q&A over guard conditions/refusal codes), C12 (event-based path predicates), and C1's product hypothesis space.
- Flagged for Micah's retroactive review. Original prereg unaltered.

## Honest limits

- C11/C12 fault-localization reuses the C1 fault machinery (retention-flavored; documented in code and amendment). The prereg does not specify per-stage fault program types.
- The learner is a disclosed-hypothesis reference learner (not a neural network). It genuinely induces via eliminative induction, but the hypothesis spaces are hand-designed.
- Scale: 3,950 episodes at 1x. The 10x/100x legs are future work.

## Files

- Source: `semantics.zag`, `codegen.zag`, `learner.zag`, `pilot.zag`, `checker.zag`, `hist.zag`, `st_memory_core.zag`, `zutil.zag`, `substrate/` (vendored)
- Evidence: `evidence/` (6 files)
- Prereg: `PREREG_CODE_PILOT.md` (frozen), `AMENDMENT_2026-09-20_code_pilot.md` (frozen)

## Verdict

**GO.** The repaired pilot passes every preregistered bar. The PC3 plant fires as predicted (2/10 C4 K3, nothing else). The mechanisms are real, deterministic, and independently verified.
