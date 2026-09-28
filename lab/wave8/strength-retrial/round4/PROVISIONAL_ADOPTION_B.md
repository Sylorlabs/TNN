# PROVISIONAL adoption of Arm B — strength trial round 4

**Date:** 2026-09-25. **Authority:** Micah Cooley's order 2026-09-25 ~16:26 PDT
("adopt the best arm for now"). **Status: PROVISIONAL — not full law.**
The trial continues; this adoption is revisited, not ratified.

## What is adopted

Arm B (uniform strength, LR_ARM_B=1) is adopted PROVISIONALLY as the
best arm of the strength trial, on the strength-trial evidence as
re-verified 2026-09-25 (commit dfa38c3a) and round-4 hardened-checker
re-validation (this directory):

- Sole survivor at S1/S10/S100 with no 100× degradation.
- 100/100 evidence logs byte-identical on rebuild; pure Zag, zero RNG.
- Round-4 hardened checker (effort-before-overwrite): 54/54 S1 cells
  ST_INVALID 0, 27/27 run-pairs byte-identical, 54/54 logs byte-identical
  to the frozen 2026-09-20 evidence — the hardening changes nothing on
  honest B trails and flags the R4 discount attack (2 failures on the
  position-(a) trail, 0 on (b)/(c)).

## What is NOT claimed

- B is capacity-bound at **~21% against the 95% graded-arm bar**. The
  capacity gap is the thing to beat, and it is the explicit target of the
  round-4 capacity-iteration workstream. B is the best arm *for now*
  because it alone survives without degradation — not because its
  capacity is sufficient.
- B's freeze (protection with no cost, no expiry, no audit trail) remains
  the contested structural point from the trial. The round-4 red team vs B
  is tasked with falsifying the freeze or proving the concern empty.
  This adoption does not settle that question.
- Settled rulings carried, not relitigated: R2 (B is the no-free-lunch
  survivor), R3 (shifted implant schedule per Micah's amendment), R4
  (fused effort-paid overwrite per his amendment).
- Still open and NOT decided here: (a) R1 amendment sign-off (30% vs 20%
  wrong-rate deviation — needs Micah's signature); (b) P2+P3 vs the
  standing P3+P2+P1 package.

## Revisit conditions

This provisional adoption is revisited (not automatically renewed) when:
1. The capacity-iteration workstream produces a challenger that beats B
   on capacity while holding every bar (displacement is Micah's call);
2. Any red team falsifies a claimed B property;
3. The R1 or P2+P3/P1 open questions resolve in a way that changes the
   bar B is judged against.

*Recorded by the round-4 coordinator under Micah's explicit order.
Nothing here overclaims: B is the survivor, not the finished law.*
