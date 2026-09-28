# AMENDMENT PROPOSAL — Composition Battery (PROPOSED 2026-09-27, NOT ENACTED)

**Status:** PROPOSED. These change frozen bars/design → require Micah's
re-approval per standing law before the full battery builds. Nothing here is
enacted; the pilot repairs (scoring decoupling, P4 fixes) are implementation
repairs already landed in `pilot.zag`, not amendments.

Source: independent red-team report (`pilot/REDTEAM_REPORT.md`), all findings
demonstrated, none voiding the pilot.

## A1. K1 kill bar — chance must include wrong-order (PROPOSED)

- **Finding:** a wrong-order agent (masters parts, retrieves correctly,
  composes backwards — a genuine composition failure) scores 10/48 = 20.8% >
  frozen K1 kill line (chance+0.10 = 14.2%). K1 would not kill it.
- **Root cause:** pairs (1,3)/(3,1) commute on all inputs (8 free items) +
  2 length-2 coincidences.
- **Proposed:** chance = max{identity, single-rule, wrong-order} = 10/48;
  K1 bar → 30.8%. Ship `wrongord` as a permanent reference mode.

## A2. Generator — per-phase token salt (PROPOSED)

- **Finding:** all tokens are exact Caesar shifts of training tokens
  (same-mod-4 ⇒ shift, verified 70×70 exhaustive). A shift-memorizer scores
  24/24 on P0 without learning any rule → full-battery P2 failures would
  misclassify as (c) instead of (a); K2's void protection would never fire.
- **Proposed:** per-phase salt in the k-DEPENDENT token coefficients (an
  additive constant is still a Caesar shift); re-run the red team's
  shift-exhaustion test to verify.

## A3. Protocol — freeze P1/P2 presentation and chaining (PROPOSED)

- **Finding:** prereg §3 never specifies whether P1 names parts (cuing
  retrieval), whether P2 presents the pair or the agent's own P1 answer
  (decides whether (b) is measured or harness artifact), or distractor
  interleaving (8 blocked distractors are position-cued).
- **Proposed:** P1 must not name parts (index-based, semantically scored,
  format-tolerant); specify P1→P2 chaining; interleave P3 distractors;
  interleave item order (fix the 4,5,2,3 per-pair length pattern and
  contiguous pair blocking).

## A4. K6 scope — 10/12 pairs (PROPOSED)

- **Finding:** 36/48 P2 inputs share no bigram with training strings, so K6
  is operable — but pairs (1,0) and (3,1) have zero bigram-clean inputs.
- **Proposed:** scope K6 to the 10 covered pairs, or restate.

## A5. Documented limitations (PROPOSED, no bar change)

- Commuting pairs (1,3)/(3,1): 8/48 items order-insensitive by construction;
  verify P5/P6 (full battery) don't commute.
- 4 length-2 soft items are freebies to multiple dumb strategies; note as
  limitation.
- P4's 0.25/0.75 asymmetry criterion is blind to input-conditional
  interference (demonstrated 3/4 vs 4/4 staying (c)); either narrow (d)'s
  definition to pair-systematic asymmetry or add per-condition breakdown.

## A6. Align pilot P0 with prereg (PROPOSED)

- Pilot implements 6 probes at ≥5/6 (tok 6–11); prereg specifies 8 at ≥7/8
  (tok 6–13). Full battery implements the prereg's numbers.

## A7. D2 instrument spec (PROPOSED, required before build)

- The frozen prereg specifies no D2 instrument (no generator, scoring rule,
  or chance arms for action sequences). D2 is unbuildable-from-prereg; write
  the spec to the same bar before building.

## Already LANDED (implementation repairs, not amendments)

- Scoring decoupled from classification (`elig=X/Y` in SUMMARY).
- P4 reclassifies only actual C items; D-gate requires pair retrieval-correct.
- PILOT_REPORT 2/48 mechanism note corrected (length-2→1-char intermediates).
