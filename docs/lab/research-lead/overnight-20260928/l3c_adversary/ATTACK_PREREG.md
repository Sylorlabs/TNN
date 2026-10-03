# L3C-ADVERSARY Phase 2: Attack Prereg (FROZEN before any attack run)

Date: 2026-09-30. Target: L3C-FORM-PASS (e663864f5), protocol UNMODIFIED.
Method: l3c_attack.zag = verbatim protocol functions from the committed
source (lines 1-311 of l3c_form.zag, proven byte-identical by diff) with
ONLY fn main() replaced by fresh contradiction families. No source change
to disc(), construct(), interp(), observe(), or any op_* is permitted.

## Attack hypothesis

The fixed construct() always emits the identical shape: one DISP node,
two TERM nodes, one unlabeled default edge to the old value, one labeled
(fi==fv) edge to the new value; interp() implements exactly the matching
fixed semantics. The conditional FORM is therefore researcher-supplied;
only the (feature, value) parameters are data-driven. These families test
whether that fixed template can be broken without a protocol change.

## Families and frozen predictions

All runs mode=1. Counters: events=cnt(2), built=cnt(3), unresolved=cnt(4).

### Family A (sig 501): two-feature conjunction needed
Train: (f1=0,f2=1)->2, (f1=1,f2=0)->2. Clash: (f1=0,f2=0)->0 twice.
No single-feature equality separates (f1=0 in train, f2=0 in train).
True separator: (f1==0 AND f2==0).
PREDICT: events=2, built=0, unresolved=2, eval=2/4 (train pass, clash fail).
Reading: HONEST FAIL (disc returns -1). Protocol change forced for a fix:
conjunctive edge labels (op_label_edge schema + interp matching) or
nested DISP emission in construct().

### Family B (sig 502): inequality/threshold needed
Train: (f1=5)->2, (f1=6)->2. Clash: (f1=9)->0, (f1=10)->0.
No single (f1==v) separates (9 and 10 each fail the all-clash check).
True law: f1>=9.
PREDICT: events=2, built=0, unresolved=2, eval=2/4.
Reading: HONEST FAIL. Protocol change forced: comparison operators in
edge labels.

### Family C (sig 503): nested dispatch (contradiction inside a branch)
Train: (f2=0)->2 twice. Clash1: (f2=1)->0 twice -> dispatch (f2==1)
built. Clash2: (f2=1,f3=9)->7 twice (contradiction under the labeled branch).
observe() on a DISP node takes the interp path: on mismatch it increments
events and returns 2 with NO construct() call and NO stash of the vector.
PREDICT: events=4, built=1, unresolved=0, clash2 observe() return codes
2 and 2, eval=4/6 (clash2 fails permanently).
Reading: SILENT DEAD END. The contradiction is counted but can never
resolve and is never flagged unresolved. Protocol change forced: stash on
the DISP branch + recursive construction re-pointing an edge target
(construct() currently only re-points the rule slot).

### Family D (sig 504): spurious separator / first-hit luck
Train: (f1=0,f3=5)->2, (f1=0,f3=6)->2. Clash: (f1=1,f3=9)->0 twice.
Two separators are consistent with all observed data: (f1==1) and
(f3==9). disc() scans f0..f3 in order and returns the first hit: (1,1).
True law (attack-side ground truth): out=0 iff f3==9.
PREDICT: events=2, built=1, unresolved=0, rep=(1,1). Held-out: (f1=1,f3=5)
true 2 -> protocol gives 0 (MISRESOLVE); (f1=0,f3=9) true 0 -> protocol
gives 2 (MISRESOLVE); the two on-distribution held-outs correct.
Held-out 2/4 with 2 silent misresolutions.
Reading: SILENT MISRESOLUTION. "Discovery" is first-consistent-hit in
scan order; the protocol cannot represent or detect underdetermination.

### Family E (sig 505, bonus): stash-window forgetting
Train: (f1=0,f2=0)->2, (f1=0,f2=1)->2, (f1=1,f2=0)->2 (third vector is
NOT stashed: stash keeps 2 per class). Clash: (f1=1,f2=1)->0 twice.
disc() sees only the first two train vectors, finds (f1==1), and builds
a dispatch contradicted by actually-observed training data.
PREDICT: events=2, built=1, unresolved=0, rep=(1,1). Eval over all 5
observed vectors: 4/5 (the forgotten train vector (f1=1,f2=0)->2
silently misresolves to 0).
Reading: SILENT MISRESOLUTION of observed data. The discriminator reasons
over a 2-vector window, not the history.

## Global frozen predictions

Total events=12, built=3, unresolved=4.

## Verdict mapping (frozen)

- If families A and B fail honestly as predicted AND family C dead-ends
  as predicted AND families D and E silently misresolve as predicted,
  the verdict is PROTOCOL-SMUGGLING-PROVEN: the conditional form is a
  fixed researcher template (single-level, single-feature-equality
  dispatch) with data-fitted parameters; each breaking family names the
  exact protocol change it forces.
- If any family resolves correctly against prediction, the verdict is
  re-examined per family (partial survival with a boundary map).
