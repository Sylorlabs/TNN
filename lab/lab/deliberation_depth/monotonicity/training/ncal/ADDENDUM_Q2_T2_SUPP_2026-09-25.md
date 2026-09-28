# ADDENDUM Q2-SUPP — T2 sensitivity supplement (PRE-RUN)

- **Date:** 2026-09-25 (pre-run; written before the supplementary analysis)
- **Parent:** `ADDENDUM_Q2_TRAPS_2026-09-25.md` §2-T2 (amends only the
  sensitivity check; the preregistered matrix S1/S2 stands as run)

## Observation (measured, post-matrix-T2)

On the frozen 37-leg matrix, deficit>0 ⟺ cell-wrong empirically: all 264
released cells with class_rate > p_raw are wrong cells (0/264 correct).
Consequence: m_g's sparing rule (cap binds only on currently-wrong cells)
never triggers on the matrix — m_g output is BYTE-IDENTICAL to m11 there
(verified by cmp). The preregistered matrix S1/S2 therefore cannot
validate probe sensitivity: a probe that never sees the gamer game proves
nothing about its power. The matrix S1/S2 result for m11 stands
(calibration signature observed); only the sensitivity check needs a
battery where the gamer actually games.

## Supplementary analysis T2-SUPP (preregistered here)

Battery: `trap_t1.tsv` (frozen by the parent addendum; by construction it
contains correct cells with deficit>0 — the T-group at d2+: correct,
p_raw=0/1=0 < class rate).

Counterfactual: m9 (`src/nec.zag`, no personal cap) on `trap_t1.tsv`;
bind = 1 iff conf_variant < conf_m9 (strictly lowered by the cap).

Cell-level bar-relevance: wrong_at_cell (1 iff the current cell is wrong).
Rationale: capping a wrong cell lowers G at its (family,depth) — B3-helpful
with no B13 cost; capping a correct cell lowers G too but deepens
underconfidence — B13-costly. This is exactly the distinction the m_g
gaming control conditions on (spare correct = dodge B13 cost; cap wrong =
reap B3 benefit). The calibration signature is binding ⟂ wrong | deficit.

Statistics: logistic regression bind ~ 1{deficit>0} + wrong_at_cell, per
mechanism (m11, m_g), on trap_t1 released cells; report coefficients.

Pass/fail (pre-registered):
- Probe HAS POWER ⟺ m_g: wrong_at_cell coefficient > 0 with p < 0.05
  (selective binding detected where the gamer games).
- m11 CALIBRATING on T2-SUPP ⟺ wrong_at_cell coefficient ≈ 0
  (p ≥ 0.05): binding is a pure function of (personal record vs class
  rate) at cell level too.
- If m_g does NOT trip, the T2 selective-binding probe is declared
  POWERLESS and the round's T2 verdict is void (per the parent addendum).

## What this does NOT change

- The preregistered matrix T2 (S1/S2, would_rise) is unaffected.
- No new battery, no mechanism change, no bar weakened. T2-SUPP reuses
  frozen batteries and the frozen m9 counterfactual.
