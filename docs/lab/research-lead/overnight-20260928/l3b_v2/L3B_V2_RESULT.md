# L3B constructor v2: result

Verdict: **L3B-V2-PASS**

The constructor-level redesign closes both crux exhibits from
L3B-C0C-BOUNDARY-EXPOSED (a40aac558) without widening any vocabulary:
growth now searches a generic 205-program space and revision recalls
archived versions instead of rebuilding them.

## Kill bars

- K1 PASS: prereg 05620eaa2 and addendum 197e2547a committed alone before
  any implementation file existed; `git merge-base --is-ancestor`
  verified at commit time (addendum fixed a 3/6 vs 2/6 arithmetic slip in
  P-B2c before implementation, transparently re-frozen).
- K2 PASS: every frozen prediction holds, 3/3 byte-identical runs
  (V2-DET PASS).
- K3 PASS: pure Zag, zero Python at every step; shell-only dash check
  clean on all lane files (V2-PURE PASS); u8-backed cells only.

## Family 1: square residual (adversary's A2, verbatim episode lists)

- P-A2a (V2-F1a) PASS: KX-SQ max = 1. The 512 canonical singles are
  provably inadequate on the square family.
- P-A2b (V2-F1b) PASS: TRACE-CREATE v=1 p1=V p2=(M,V,V), r1=205 r2=208.
  The CALLS log shows the generic assembly:
  CREATE(op=2)->205, CREATE(op=2)->206, CREATE(op=2)->207,
  CREATE(op=4)->208, CONNECT(208,0,206), CONNECT(208,1,207).
  MUL(VAR,VAR) was found by enumerative search (first exact program in
  canonical order) and assembled by CREATE/CONNECT, not retrieved and
  not fitted from a vocabulary entry. Growth searched program space.
- P-A2c (V2-F1c) PASS: HIDDEN-A2 = 3/3.
- P-A2d (V2-F1d) PASS: N2-INTERP = 25.
- P-A2e (V2-A2e) PASS: interpreter region sha256-identical to v1
  (aee8090b1429e6206d26d6822ecb6a50f79def7da8cdaf8ae23c2bd5632e480d);
  rel_of absent (the vocabulary analyzer was deleted, not extended);
  no family-specific token in the mechanism source.

## Family 2: alternating regimes (adversary's B2, verbatim episode lists)

- P-B2a (V2-F2a) PASS: creates = 2, dispatches = 2.
- P-B2b (V2-F2b) PASS: archive keys exactly v1 = ("V", "(A,V,V)"),
  v2 = ("V", "(A,V,C4)").
- P-B2c (V2-F2c) PASS: HIDDEN-B2 = 3/3, SWITCH = 2/6 (0/3 then 2/3),
  FINAL-B2 = 1/2. The first episode after each regime flip fails
  honestly (no observable pre-prediction cue; predicting it would need
  task labels), then the dispatch corrects from the observed
  contradiction. v1 scored 0/2 on FINAL-B2 with no recall at all.
- P-B2d (V2-F2d) PASS: both dispatches are recalls. SWITCH2 ep1:
  TRACE-DISPATCH from=2 to=1 on=2 r1=205 r2=208 (v1's exact
  construction-time node ids). FINAL-B2 ep1: TRACE-DISPATCH from=1
  to=2 on=5 r1=209 r2=212 (v2's exact node ids). Zero constructor
  calls across each dispatch (program-side log-delta check). Revision
  recalled; nothing rebuilt.

## v1 regression families (behavioral bars)

- P-R1 (V2-R1) PASS: inst1 hiddenA = 3/3, follow = 2/2. The grown
  programs differ representationally from v1's (rel,k) pairs
  (ADD(VAR,VAR) for 2n instead of MUL(VAR,CONST(2))), an expected honest
  consequence of generic search: both compute the same function.
- P-R2 (V2-R2) PASS: inst2 hiddenB = 3/3 (grown (ADD(VAR,CONST(2)), VAR)).
- P-R3 (V2-R3) PASS: ablation total = 0/6.

## Scope (honest)

Bounded L2 at most. No L3 claim is made or implied. v2 is a bounded-L2
grower of small programs (depth <= 2, 205-program space, constants
0..8) with per-regime recall over at most 8 archived versions. C0-C
beyond the two frozen families remains untested, and the dispatch
ceiling after a regime flip is (k-1)/k without an oracle.

## Recommendation

Independent adversary on v2 next, not integration yet. The v2 claims
most worth attacking: (1) whether the 205-program enumeration is
genuinely generic search or a bigger vocabulary in disguise (attack
with a sealed family whose true program is depth-3 or needs constants
outside 0..8, plus one whose true program is in-space but not
first-exact, to test the selection rule); (2) whether single-failure
dispatch can be fooled by an ambiguous observation matching the wrong
archived version (the frozen families were verified free of accidental
matches, but a hostile family could plant one); (3) whether the archive
recall evidence (node-id equality) survives a longer churn sequence
with evictions. Only after that red team should v2 be considered for
the continuing-learner integration lane.
