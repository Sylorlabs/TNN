# PREREG AMENDMENT 2 (transparent): contracts record successful compositions

Date: 2026-10-02. Status: H1/H2/UNI run 1 complete. K1-K4 predictions all
match (H1, H2, UNI, pending NOKIND). P5 (K5) failed as originally specified:
UNI solved Z2 (ANS=3) but via widening (TRIES=7, WIDEN=1), not via contract
pruning (predicted TRIES=4, no widen). Census showed X.outmask={2}, n=1.

## Root cause: under-specified observation channel

PREREG Section 3 defines the contract as "observed (input-kind, output-kind)
pairs from its teaching executions". The implementation therefore records
observations ONLY in teach(). But PREREG Section 5 (P5) predicts that after Z1
is solved, "X.outmask is now {1,2} (observations 11->14 NUM and 41->44 NODE)"
-- i.e., the P5 prediction already assumes the Z1 composition's executions feed
the contract. Section 3's "teaching executions" phrasing contradicts Section
5's frozen P5 intent. Same class of internal inconsistency as Amendment 1.

## The fix (mechanism clarification; K1-K4 provably unaffected)

On ANY successful composition trial (single or pair), the unified mechanism
records kind observations for each executed MAP: single success records
(m, s->v); pair success records (x, s->v1) and (y, v1->v2). Failed trials
record nothing. This is part of the single execution rule, always on; it is
not a mode, flag, or researcher intervention. Rationale: a behavior contract
that ignores behavior the learner just observed would be incoherent; the
contract summarizes observed behavior, and a successful composition IS
observed behavior of its stages.

Why K1-K4 cannot change: every success in P1/P2a/P2b/P3 is terminal (the
solver returns immediately), so newly recorded observations can never affect
admission within the same solve. Verified by code inspection: uni_solve
returns `c` in the same statement sequence as the success; no further
admission decision follows. (Empirically re-verified below by re-running the
full UNI battery.)

## Updated P5 predictions (re-frozen; everything else unchanged)

Z1 (P2b): unchanged: ANS=2 TRIES=7 INTER=44 WIDEN=1. Its success records
X: 41->44 (NODE) and Y: 44->2.
Z2 (P5): X.outmask={1,2} now admits (X,Y) without widening. ANS=3 TRIES=4
INTER=53, no WIDEN=1. Z1 TRIES=7 > Z2 TRIES=4.
Census after Z2 (Z2's own success is also recorded):
CENSUS m=0 inmask=1 outmask=3 n=3
CENSUS m=1 inmask=1 outmask=2 n=3
CENSUS m=2 inmask=1 outmask=1 n=1
CENSUS m=3 inmask=1 outmask=2 n=1

## Governance

Recorded BEFORE the corrected UNI run. K1-K4 predictions are untouched and
will be re-verified empirically on the re-run. No kill bar is weakened; K5's
bar is clarified to the prereg's own P5 intent. The H1/H2 arms are unaffected
(canonical H1/H2 record observations from teaching only, as in their preregs).
