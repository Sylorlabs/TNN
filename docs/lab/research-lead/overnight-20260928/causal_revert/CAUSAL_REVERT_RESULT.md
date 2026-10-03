# CAUSAL-REVERT-PASS: learner-constructed graphs survive law change-and-revert

Date: 2026-09-30 UTC
Worker: Causal-Lane Revert Worker
Verdict: CAUSAL-REVERT-PASS
Prereg: PREREG_CAUSAL_REVERT.md (commit c09afd95e) + Amendment 1
  (commit ab68dd121, transparent correction of R2 REBUILD hand-count)
Implementation: causal_revert.zag (pure Zag, zero Python)
Kill bars: K1 prereg precedence (c09afd95e strictly before implementation;
  verified via git log), K2 frozen predictions match (41/41 VERIFY.sh
  checks), K3 pure Zag + 3/3 byte-identical (md5
  56d8e00a3299b812b7a5dbc197dea469) + shell-only dash check clean.

## What was built

The DDES law-revert battery ported onto the H-CAUSALEXP causal lane.
The derivation core (arrival computation, n-candidate frontier, plan
synthesis [S]+t*[W]+[O(V)], analytic predictor, world stepper) is
copied verbatim from ddes_revert.zag at 00e9a766e. New: candidate
graphs are LEARNER-CONSTRUCTED by a generic enumerator (all 78 graphs
over the frozen vocabulary) filtered by passive evidence and quotiented
by behavioral signature, not researcher-supplied. Three modes:

- REVISE: the learned graph persists across phases; on new evidence it
  is revised via k-edit BFS (change-delay, add-rule, remove-rule;
  KMAX=3), keeping the same structure when consistent.
- REBUILD: fresh construction per phase (re-selection baseline; nothing
  persists).
- FROZEN: learn once, never revise (pathology baseline).

Cases: R1 change-then-revert [G0,G1,G0]; R2 permanent-change control
[G0,G2,G2].

## Results (all match frozen predictions, 41/41)

R1 REVISE (revert-resilience):
- P0: constructor finds 9 graphs in 2 classes; 1 intervention (Z,3)
  eliminates [(X->Y,1),(Y->Z,2)]; winner [(X->Y,1)].
- P1: W0 inconsistent with E1; k=1 empty; k=2 yields 2 classes;
  1 intervention (Z,1) eliminates [(X->Y,2),(X->Z,2)];
  winner [(X->Y,2),(X->Z,1)].
- P2: W1 inconsistent with E0; k=1 empty; k=2 yields 1 class;
  winner [(X->Y,1)] with 0 interventions.
- Trace: W0 ->k=2-> W1 ->k=2-> W2=W0. The learned graph survives the
  round trip structurally (W2==W0). rounds_total=2.

R1 REBUILD: identical winners, rounds_total=3 (fresh 78-graph
construction per phase; nothing persists).

R1 FROZEN: P1 winner [(X->Y,1)] WINNER-INCONSISTENT (failure to revise);
P2 recovers by luck of the revert.

R2 REVISE (permanent-change control):
- P1p: W0 inconsistent with E1p; k=1 yields 1 class;
  winner [(X->Y,2)], rounds=0.
- P2p: W1p consistent; KEEP; winner [(X->Y,2)], rounds=0.
- W2==W1, W2!=W0: revised once, then stable; NO SNAPBACK to the
  original graph. rounds_total=1.

R2 REBUILD (amended predictions): P1p/P2p each find 9 graphs in 3
classes, 2 interventions, winner [(X->Y,2)]; rounds_total=5.

R2 FROZEN: P1p/P2p WINNER-INCONSISTENT (pathology confirmed).

## L3-revision framing (honest evaluation)

REVISE vs REBUILD reach identical winners, but the white-box traces
differ in the way the prereg specified: REVISE shows the SAME learned
structure modified by edits (W0 ->k=2-> W1 ->k=2-> W2=W0), i.e. the
structure persists and is revised, not discarded and rebuilt. This is
evidence TOWARD the revision criterion (criterion 12 in the
procedure-invention list; the causal analogue).

What is still missing for L3 (disclosed in prereg section 7): the edit
vocabulary (change-delay, add-rule, remove-rule), the KMAX bound, the
consistency criterion, and the revision trigger are researcher-supplied;
the learner does not invent edit types. The learned graphs are
behavioral representatives (the chain [(X->Z,1),(Z->Y,1)] and
[(X->Y,2),(X->Z,1)] are indistinguishable under X-only interventions;
chain-form identification is NOT claimed).

Classification: bounded L2+. NOT L3. The generic causal-revision
interpretation stays KILLED (REVISE-REDTEAM-KILLS); this work tests
revision of a learner-constructed graph, not generic causal revision.

## Amendment transparency

During debugging, the implementation revealed the prereg's hand-count
for R2 REBUILD was wrong (E1p yields 3 classes, not 1; the manual count
missed [(X->Y,2),(Y->Z,1)] and [(X->Y,2),(Y->Z,2)]). Amendment 1
(ab68dd121) corrects the predictions transparently; the code was not
changed to fit. R2 REVISE was unaffected (k=1 neighborhood correctly
yields 1 class).

## Files

- causal_revert.zag (implementation)
- BUILD.sh, RUN.sh, VERIFY.sh (3/3 byte-identical, 41/41 checks)
- RUN1.txt (frozen output), PREREG_CAUSAL_REVERT.md,
  PREREG_AMENDMENT_1.md, NAMECHECK.md
