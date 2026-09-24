# VERDICT W4 — self-training PAM (third generation)

Evidence commit: `0b3f1b621dec409532de4395775d9d98af4d8f98`
(prereg `wild/prereg/PREREG_W4.md`, frozen; comparator bar frozen by AMEND1.)

## Observed numbers (instrument + independent mirror agree exactly)

- Final CT: **841** (= offline optimum CT*, independently verified)
- Converged: yes, epoch 2 (epoch 1 ended at 841)
- Correct admits: **433/1102 = 39.29%**
- Wrong admits: **0** (12 W + 9 P pairs all rejected)
- Misses/revisions: 9/9, strictly alternating C-miss/P-false-admit
- Cap hits: 1 (first revision 700->764, +64 bound)
- Revision trace: 700->764->775->789->799->800->801->807->833->841
- D-W4-1 margin-inflation diagnostic:
  - W4 bar (841): admits W = 0/12, P pairs = 0/9
  - M1 bar (705): admits W = 12/12, P pairs = 0/9
- Instruments: kb_w4_t=0, kb_w4_mono=0, kb_w4_conv=0
- Battery: 2x byte-identical,
  SHA-256 `8928815c5d6fa2e9b57e4ec640d3950294a9e001a619ee299a7b901e47d21860`

## Bar evaluation

- K1 (no false admits): PASS (0 wrong admits).
- K2 (2x determinism): PASS (byte-identical).
- K3 (>=60% throughput): raw number 39.29% FAILS the number, but the frozen
  conditional applies: K3 is SURVIVE-with-documented-tradeoff iff D-W4-1
  demonstrates the compensating safety gain. It does: the learned bar
  rejects 12/12 W (which the M1 bar admits 12/12) while holding 0 wrong
  admits. -> **SURVIVE-with-documented-tradeoff**.
- K4 (O(1) decisions): PASS (21 decisions/epoch max).
- K5 (termination): PASS (epoch cap 3; terminated).

## Status: SURVIVE-with-documented-tradeoff

The preregistered conditional is met exactly as written. The throughput loss
(82.58% -> 39.29%) is the documented price of the demonstrated safety gain
(zero wrong admits, 12/12 W rejected that the frozen M1 bar lets through).
Redesign direction (frozen): hybrid arms.

## Numeric-cap classification (standing law: no arbitrary hard limits)

- Per-miss bound (existence): LOAD-BEARING (K5 termination argument needs a
  bounded step; without it a single miss could jump CT arbitrarily).
- Per-miss bound value (+64): ARBITRARY calibration -> FLAGGED for removal /
  generalization (derive from observed margins, not a constant).
- Epoch cap (3): value ARBITRARY as design law (termination itself is
  load-bearing; the number 3 is not) -> FLAGGED for removal / generalization
  (converge on fixpoint, not a count).
