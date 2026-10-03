# PREREG_B_AMEND1: transparent re-freeze correcting B-S3's predicted count

Status: PREREG-FROZEN (design only; no implementation in this commit).
Wave: wave-20261002-1121pdt. Lane: CONTLEARN (queue item 9, exercise b).
Date: 2026-10-02. This amendment is committed before any implementation
file for exercise (b) exists; it forms part of the frozen prereg family
with PREREG_B.md. Reason: PREREG_B.md section 5, bar B-S3, predicted the
costume core's fire-time unccount in schedule A as 3. The correct
prediction is 4: in schedule A the episode query sits at ev 6, and under
the costume core (which fires at evidx 12, not evidx 5) that query finds
no proposal, misses, and reifies a fourth UNCERT before the evidx-12
firing. The bar's logic is unchanged: the costume fires at the identical
position (evidx 12) under different learner state, proving
state-blindness. Only the predicted count is corrected.

Note: this document uses hyphens only; no em or en dashes appear.

## B-S3 (corrected)

sc_costume_a and sc_costume_b both print SCHED_FIRE with evidx=12;
fire-time unccount is 4 in schedule A and 0 in schedule B. The costume
fires identically with and without the triggering state, proving
state-blindness. (Schedule B is unaffected: its episode query at ev 84
sits after the treat core's evidx-83 firing, and the costume's evidx-12
firing precedes all three of schedule B's misses.)

## Unchanged

All other bars (B-S0, B-S1, B-S2, B-S4, K0-K3), the decision rule, the
claim bound, and sections 1-4 and 6-8 of PREREG_B.md stand unaltered.
