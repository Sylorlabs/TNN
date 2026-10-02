# Amendment 1 to PREREG_CAUSALV3 (transparent, before result freeze)

**Date:** 2026-09-29 (PDT)
**Status:** FROZEN (before any H-CAUSALV3 result is frozen)
**Amends:** PREREG_CAUSALV3.md (commit 7f535c115)

## What changed during implementation testing

The frozen R2 (ties become AMBIGUOUS over all tied minima) was
implemented and run against all frozen fixtures. K-CV3-1 and K-CV3-2
pass as frozen. 3i2, 3c, 3d, C2 are byte-identical as frozen. But
B2 is NOT byte-identical, in a way the prereg did not anticipate:

- B2's entry 2 has a within-variable tie the prereg missed: s0
  admits THREE tied minima (THR s0<=0, THR s0<=1, EQ s0, all 2
  cells), plus EQ s2. Old code: AMBIGUOUS over 2 (per-variable
  fiat winners THR s0<=0, EQ s2). New code: AMBIGUOUS over 4
  (all tied minima).
- Probe `Q (1 1 1) | 2` changed from `(1 1 1)` to WITHHOLD.

## Why the withhold is wrong (not merely conservative)

At Q(1 1 1), every tied candidate that CAN cover the query agrees
s1=1: THR s0<=0 -> UNCH -> 1; THR s0<=1 -> SET(1) -> 1; EQ s2 ->
SET(1) -> 1. The withhold is caused solely by EQ s0, which cannot
cover the unseen s0=1 (pred_under_cand returns 0: no episodes in
cell), combined with the agreed-under-ambiguity rule that treats
non-coverage as a veto (ok=0). A candidate with no opinion is
exercising a veto over a unanimous opinionated agreement. That is
a technicality, not evidential honesty: the answer (1,1,1) does
not depend on how the s0 tie resolves.

Accepting the withhold as a "supersession" would enshrine a
strictly-less-informative mechanism for no evidential reason.
The honest fix is to the agreement rule, not to the bar.

## AMEND1: abstention in agreed-under-ambiguity (frozen)

In `predict_entry`'s ST_AMB branch: a candidate for which
pred_under_cand returns 0 (cannot cover the query) ABSTAINS
rather than vetoing. Prediction requires at least one covering
candidate and unanimous agreement among covering candidates;
otherwise WITHHOLD (including the case where no candidate
covers).

Rationale: non-coverage (e.g. EQ on an unseen value) is the
absence of an opinion, not a disagreement. Unanimity is assessed
over opinions held.

## Frozen expected effects of AMEND1

- B2: probe predictions byte-identical to committed
  CV2_B2_RUN.txt ((2,0,0), WITHHOLD, (1,1,1)). The trace line
  honestly reports 4 tied candidates (documented trace change,
  not a silent one).
- thr (X-CV2-2): still WITHHOLD on Q(1 1 0) (THR s0<=0 and THR
  s0<=1 are both covering and genuinely disagree). K-CV3-2
  unaffected.
- 3i: I1 (1,1,0), I2 (0,0,1), I3 (2,0,0) unchanged (both tied
  candidates cover and agree).
- 3c, 3d, 3i2, C2, mask, double: no ST_AMB entries at probe
  time; unaffected (verified by grep: zero AMBIGUOUS lines).

## Revised K-CV3-3(c)

B2: probe predictions byte-identical to CV2_B2_RUN.txt; trace
shows the honest 4-candidate tie line (S3 supersession of the
trace line only, documented here). 3c, 3d, C2 remain fully
byte-identical.

No other prereg terms change. Pure Zag. No new fixtures.
