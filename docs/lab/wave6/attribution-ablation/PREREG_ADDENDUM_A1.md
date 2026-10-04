# PREREG addendum A1 — independent-streak recomputation keyed on genuine signal

**Date:** 2026-09-20. **Status:** pre-trial (written before the first ablation
binary compiled; the trial later confirmed the intact anchor unmoved).

## The change

In `run_arm`, the driver's independent verification-streak recomputation
(`dstreak`, the bar family C is judged against) was changed from keying on
the **delivered** signal (`del==1`) to keying on the **genuine** signal
(`gen==1`):

- Old (integ-1 inherited): `verified=1` required `del==1`.
- New: `verified=1` requires `gen==1`. (`elim_now` still keys on `del==-1`,
  exactly as in integ-1.)

## Why

The driver's recompute is the independent instrument that measures whether
the learner's release rested on genuine evidence. On the R-ladder the two
definitions coincide during P0 (there `del==gen`), so the intact anchor is
untouched. On the F-ladder (full-run flattery), `del==1` is identically true:
the old definition would count delivered flattery as verification, inflating
`rstreak_at_fire` for the NOHS arms and **masking the very failure family C
exists to catch** (flattery-driven release). Keying on `gen` makes the
instrument strict in exactly the direction the hypothesis under test needs:
an evidence-free release must show a low independent streak.

## What it does not do

- It does not touch the learner, its streak counter, its audit vocabulary,
  or any decision path. It is a change to the driver's measuring instrument
  only.
- It does not move the intact baseline: on the R-ladder, P0 is uncorrupted
  (`del==gen`), so the recomputed streak for INT_R and the checker-ablation
  arms is byte-identical to the integ-1 definition. Empirically confirmed in
  the trial: `INT_R_rstreak_at_fire,8,8`; twin `e_twin_div,0`.
- It does not change which episodes count as elimination resets (`elim_now`
  still uses `del==-1`, preserving the integ-1 semantics where a corrupted
  `-1` delivery is an elimination event).

## Trial confirmation of the intended effect

- NOHS: learner streak at fire 8 (counts flattery +1s), independent genuine
  streak 1 → `c_sig1` fires, judge H1'=1.
- INT_R/NOIL/NOPROV/NOIL_NOPROV: independent streak 8 = learner streak 8 →
  no C-signature, HOLD.

## Prereg status

This addendum is the only change to the preregistered plan. All expected
values in §4 were written against this definition (e.g. NOHS
`rstreak_at_fire=1`).
