# JUDGE ADDENDUM: 11:21 M4 (DDES R2) provisional status LIFTED

Parent-agent inline, 2026-09-30. This addendum executes the conditional
ruling in JUDGE_1121_RECOVERY.md M4: "ADOPTED AS PROVISIONAL pending
independent re-verification of K-R2.1..K-R2.6."

## The independent re-verification

Wave 20260930-2021pdt staffed lane ddes_r2_verify, a different worker
from the recovery coordinator that implemented DDES R2. The lane
(LANE_RESULT.md, committed with the 20:21 wave record):

- Recompiled ddesr2.zag from committed source with the pinned znc in
  safebin (pure Zag toolchain, NAMECHECK Step 0 records python3 and
  python both unresolvable in PATH).
- Ran the rebuilt binary 3x. All three runs byte-identical to the
  committed evidence (sha256 50a990d33f5074b05d0bb6c56a0f54fb6f581
  75f7266011e4a95f57f2fd33ae4 across vrun1/2/3.txt and the committed
  run1.txt). Exit 0, zero stderr bytes, all runs.
- Confirmed K-R2.1 (flag present on both World F configs, absent on
  A-E), K-R2.2 (no silent wrong convergence; surviving hypothesis
  matches truth on both configs; 10/10 CONVERGE-OK), K-R2.3 (A-E
  block byte-identical to DDES_RAW.txt prefix; SUMMARY ok=11/11
  plans_built=10), K-R2.4 (determinism), K-R2.5 (purity, safebin
  only), K-R2.6 (diff shows exactly the prereg-specified changes,
  no new enumeration, no new dedicated semantic case).

## Parent-agent spot verification

Before lifting, the parent independently checked the three
load-bearing claims: (1) prereg d31e901b0 is a strict ancestor of
implementation b42b10db5 (git merge-base --is-ancestor: OK); (2) the
four run files share one sha256 (sort -u over vrun1/2/3.txt and
committed run1.txt yields a single hash); (3) the
FLAG TSTAR-ZERO-BOUNDARY line occurs exactly twice in vrun1.txt
(the two World F configs). All confirmed.

## Ruling

The PROVISIONAL status is LIFTED. DDES R2 is CONFIRMED as
REPAIR-PASS on all six frozen bars, independently verified. The t*=0
soundness hole is closed. Classification stands: strong L2 repair to
a bounded mechanism; no L3 claim attaches. DDES remains strong L2
guided generation, with its promotion blocker removed.
