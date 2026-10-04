# PREREG AMENDMENT 1: arm A phase-2 creation mechanism; K-H2 check precision

Frozen 2026-10-02, pre-result-adoption. Arm A never passed; no
result has been adopted. This amendment is committed alone before
any implementation change.

## A1: arm A phase-2 must create Xt by direct call

Design bug found at first build (observed: ADAPT-CREATED n=0,
xt=-1, ph2=34 via trial, A-NONPREFIX-STALE=FAIL on p2/p3/p5/p6).

Cause: the arm A phase-2 query is ev_query_tt(32,72,34), but the
fresh-adaptation fallback satisfies each source MAP from the query
s. cc_satisfy(Z,32) fails because Z = [1,2,1] from 31: its first
link needs a live (32,1,*) fact, which does not exist. So neither
adapt_truncate nor adapt_nonprefix can fire from s=32, and the
head-drop Xt = [2,1] is never created through the fallback.

Correction: after the gap facts and before the phase-2 query, the
driver calls adapt_nonprefix(W,31,0) directly (s=31 is Z root, so
cc_satisfy succeeds). The call must return nk=1 (exactly one
head-drop created; only Z is eligible). The phase-2 query
(32,72,34) then answers 34 via the frozen rebind path over the
created Xt (t2_gather finds the [32,33,34] path; pc_try_one
verifies against expected), promoting a rebound MAP with a
type-14 edge to Xt. The rebound MAP carries no type-16 edge, so
it is invisible to the adapted-MAP finders and to the type-16
edge counts.

K-A1 is unchanged in its observable content (ph2=34, Xt relseq
[2,1], recorded kind 2, type-16 Xt->Z) and is strengthened: p1
now also requires nk=1, so Xt creation is deterministic and not
fallback-order dependent. No kill bar is weakened.

The remaining arm A steps are unchanged: world change
teach (32,5,40) then kill (32,2,33), withdraw (32,72,34),
ph4 = ev_query_tt(32,73,99) expecting -2.

## A2: K-H2 source check precision

The K-H2 grep `mode|bridge|handler` also matches the substring in
"promote"/"adapt_promote" (frozen function names), so a raw count
can never be 0. The check is refined to whole-word matches:
`grep -ciw -e mode -e bridge -e handler` on tt_patch.zag and
tt_driver.zag must return 0. The tt_patch.zag header comment is
reworded to avoid the words entirely ("No new subsystems,
dispatchers, semantic cases, opcodes, or MAP/edge types").
No kill bar is weakened; the architecture accounting is unchanged.
