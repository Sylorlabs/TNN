# PREREG_A_AMEND1: transparent re-freeze of K3 (no-regression bar)

Status: PREREG-FROZEN (design only; no implementation in this commit).
Wave: wave-20261002-1121pdt. Lane: CONTLEARN (queue item 9, exercise a).
Date: 2026-10-02. This amendment is committed before any implementation
file for exercise (a) exists; it forms part of the frozen prereg family
with PREREG_A.md. Reason: PREREG_A.md section 5 cited a frozen record
("46/46 per the 0521pdt RUN_LOG") for K3 that is not verifiable from the
records available in this worktree. The bar below replaces it with an
operational regression test. No other bar is altered.

Note: this document uses hyphens only; no em or en dashes appear.

## K3 (amended): no regression of the frozen core under the instrument derivation

Rationale: the instrument cores derive from the frozen base core. With
an empty contradiction ledger (own) and with relations other than 850
(hard), both instruments are return-value-identical to the base by
construction; any divergence in the frozen core's own test battery is a
regression introduced by the derivation.

Procedure (frozen):

- A k3 driver fixture (k3_driver.zag, 0 cognition functions, 0
  structural writes) whose main calls run_all() (the frozen core's own
  battery, which prints "TOTAL p/t" and returns 0 iff p==t).
- Three binaries, built once via the logged wrapper before any lane
  run: k3_base (frozen base core + k3 driver), k3_own (rj_core_own +
  k3 driver), k3_hard (rj_core_hard + k3 driver). One run each.
- Bar: the "TOTAL p/t" lines are identical across all three binaries
  (same p, same t), and rc==0 on all three runs.

Stdout is NOT required byte-identical across the three binaries: the
instruments add ENGAGE/MISS diagnostic prints that the base lacks. Only
the TOTAL line (p and t) and the return code are compared. This is
stated here so it cannot be misread later as a weakened bar; it is the
frozen form.

Kill: any TOTAL mismatch, or any rc!=0, is K3-FAIL and VOIDs the lane
(the derivation regressed the frozen core).

## Unchanged

All other bars (A-R0 through A-R4, K0, K1, K2), the decision rule, the
claim bound, and sections 1-4 and 6-8 of PREREG_A.md stand unaltered.
