# PREREGISTRATION: Causal-Lane Revert (learner-constructed graphs)

Status: FROZEN PREREG. Committed alone before any implementation file
exists in the owned path. Any change requires a dated amendment
committed alone before the changed code runs.

Date: 2026-09-30 UTC
Worker: Causal-Lane Revert Worker
Owned path: docs/lab/research-lead/overnight-20260928/causal_revert/
Builds on: REVERT-ADAPT-PASS (prereg bb319407a, implementation
00e9a766e). The derivation core (arrival computation, n-candidate
frontier, plan synthesis, analytic predictor, world stepper) is copied
verbatim from ddes_revert.zag at 00e9a766e (which copies verbatim from
the frozen DDES sources). The intervention machinery is the
H-CAUSALEXP-CONSTRUCT experiment-construction mechanism (BUILD-PASS
7/7, SURVIVES-AS-L2, L3 KILLED; governance 45db44fab): primitive set
authored, discriminating sequences composed by predicted disagreement,
executed once against the sealed world. New in this work: the candidate
graphs are LEARNER-CONSTRUCTED (generic enumerator plus passive-evidence
filter plus behavioral-equivalence quotient), not researcher-supplied;
and the REVISE operator (edit-neighborhood revision of the persistent
learned graph) with REBUILD (fresh construction) and FROZEN (never
revise, pathology baseline) as comparison modes.

## 1. Problem

REVERT-ADAPT-PASS showed an adaptive planner tracking a law through
change-and-revert, but its candidate graphs were researcher-supplied;
the learner only selected and re-selected. The L3 revision criterion
asks whether a LEARNED structure survives a law change: does the learner
revise its own constructed graph, or merely re-select among supplied
candidates? This work ports the revert battery so the candidate set is
constructed by the learner from passive evidence in earlier episodes,
and the learned graph persists across episodes through an edit-based
revision operator.

## 2. Vocabulary and semantics (researcher-supplied, disclosed)

Variables X=0, Y=1, Z=2. Rules are (src,dst,delay) with src!=dst and
delay in {1,2}. Graphs hold 1 or 2 rules. Arrival semantics are schema-1
(verbatim compute_arrivals): X arr=0, others = min over rules of
(src_arr+delay), INF if unreachable. Prediction for (V,t) is 1 iff
arr[V] <= t. Interventions use primitives {S=set X:=1, W=wait,
OY=observe Y, OZ=observe Z}; plans are [S] + t* copies of [W] +
[O(V*)], synthesized verbatim by synthesize_plan_gen.

True laws (frozen):
- G0 = [(X->Y,1)]. Behavior: Y arr 1, Z INF.
- G1 = [(X->Z,1),(Z->Y,1)]. Behavior: Y arr 2, Z arr 1.
- G2 = [(X->Y,2)]. Behavior: Y arr 2, Z INF.

Passive evidence protocol (frozen, 3 observations per phase):
- E0 (under G0): (Y,1)=1, (Y,2)=1, (Z,2)=0.
- E1 (under G1): (Y,1)=0, (Y,2)=1, (Z,2)=1.
- E1p (under G2): (Y,1)=0, (Y,2)=1, (Z,2)=0.

## 3. Learner-side machinery (generic, no graph is researcher-supplied)

CONSTRUCTOR (phase 0 and REBUILD mode): enumerate all 78 graphs (12
one-rule + 66 two-rule), keep those consistent with the phase passive
evidence, quotient by behavioral signature (the (arr[Y],arr[Z]) vector;
with X-only interventions behaviorally identical graphs are one
hypothesis), keep one canonical representative per class (fewest rules,
then lexicographic on sorted (src,dst,delay)). The representative set
is the candidate set; the standard filter plus intervene loop
(frontier_surv, ADAPT-style chaining) selects the winner.

REVISE operator (REVISE mode, phases 1+): let W be the current learned
graph and E the new passive evidence. If W is consistent with E, keep W
(no revision). Else generate the k-edit neighborhood of W for k=1,2,3
(KMAX=3): single edits are change-one-delay (flip 1<->2), add-one-rule
(only if nr<2), remove-one-rule; higher k by iteration with dedupe via
canonical rule sorting. Filter each neighborhood by E, quotient by
behavioral signature, take the first k with a non-empty result as the
candidate set; then the standard intervene loop selects the winner. The
trace logs the edit depth k used. If no k<=KMAX yields a candidate,
emit DECLARE-REVISION-FAILED (honest; not reached in frozen cases).

FROZEN mode (pathology baseline): learn W0 in phase 0 via the
constructor; never revise afterwards regardless of evidence. This is
the failure-to-revise baseline.

REBUILD mode (re-selection baseline): run the constructor fresh from
each phase passive evidence; the learned graph does not persist.

## 4. Frozen cases

R1 change-then-revert: true phases [G0,G1,G0], evidence [E0,E1,E0].
R2 permanent-change control: true phases [G0,G2,G2], evidence
[E0,E1p,E1p].

## 5. Frozen predictions

Graph notation: [(s,d,w),...] with X=0,Y=1,Z=2.

R1 REVISE:
- P0: constructor from E0 yields 9 graphs in 2 behavioral classes
  {(Y:1,Z:INF),(Y:1,Z:3)}; reps [(X->Y,1)] and [(X->Y,1),(Y->Z,2)].
  Frontier (V*=2,t*=3). Plan [S,W,W,W,O(2)]. EXEC real=0 (G0 Z INF).
  Predictions 0 vs 1. ELIM (Y:1,Z:3). Winner [(X->Y,1)]. rounds=1.
- P1: W0 inconsistent with E1. k=1 empty (13 neighbors, none
  E1-consistent). k=2 yields 2 classes {(Y:2,Z:1),(Y:2,Z:2)}; reps
  [(X->Y,2),(X->Z,1)] and [(X->Y,2),(X->Z,2)]. Frontier (V*=2,t*=1).
  Plan [S,W,O(2)]. EXEC real=1 (G1 Z arr 1). Predictions 1 vs 0.
  ELIM (Y:2,Z:2). Winner [(X->Y,2),(X->Z,1)]. rounds=1.
- P2: W1 inconsistent with E0. k=1 empty (4 neighbors). k=2 yields
  1 class {(Y:1,Z:INF)}; rep [(X->Y,1)]. No intervention.
  Winner [(X->Y,1)]. rounds=0.
- Winners [[(X->Y,1)],[(X->Y,2),(X->Z,1)],[(X->Y,1)]]. W2==W0
  structurally: the learned graph survives the round trip.
  rounds_total=2.

R1 REBUILD:
- P0: winner [(X->Y,1)], rounds=1 (same as REVISE P0).
- P1: fresh from E1: 2 classes, frontier (V*=2,t*=1), real=1,
  winner [(X->Y,2),(X->Z,1)], rounds=1.
- P2: fresh from E0: 2 classes, frontier (V*=2,t*=3), real=0,
  winner [(X->Y,1)], rounds=1.
- Winners identical to REVISE. rounds_total=3. Trace shows fresh
  78-graph construction per phase (no persistence).

R1 FROZEN:
- P0: winner [(X->Y,1)], rounds=1. P1: winner [(X->Y,1)]
  INCONSISTENT with E1 (failure to revise). P2: winner [(X->Y,1)].

R2 REVISE:
- P0: winner [(X->Y,1)], rounds=1.
- P1p: W0 inconsistent with E1p. k=1 yields 1 class {(Y:2,Z:INF)};
  rep [(X->Y,2)]. No intervention. Winner [(X->Y,2)]. rounds=0.
- P2p: W1p consistent with E1p. No revision. Winner [(X->Y,2)].
  rounds=0.
- Winners [[(X->Y,1)],[(X->Y,2)],[(X->Y,2)]]. W2p != W0 and W2p is
  G2-consistent: no snapback. rounds_total=1.

R2 REBUILD:
- P0: winner [(X->Y,1)], rounds=1. P1p: fresh from E1p: 1 class
  {(Y:2,Z:INF)}, rep [(X->Y,2)], rounds=0. P2p: winner [(X->Y,2)],
  rounds=0.

R2 FROZEN:
- P0: winner [(X->Y,1)], rounds=1. P1p: winner [(X->Y,1)]
  INCONSISTENT. P2p: winner [(X->Y,1)] INCONSISTENT.

Frozen SUMMARY expectations (ok = phases completing the protocol;
winner_correct = winner behaviorally consistent with the phase true
law on the evidence):
- R1 REVISE: ok=3/3, rounds_total=2, W2==W0 true.
- R1 REBUILD: ok=3/3, rounds_total=3, W2==W0 true.
- R1 FROZEN: ok=3/3, P1 winner_correct=false.
- R2 REVISE: ok=3/3, rounds_total=1, W2p==W1p true, W2p!=W0 true.
- R2 REBUILD: ok=3/3, rounds_total=1.
- R2 FROZEN: ok=3/3, P1p/P2p winner_correct=false.

## 6. Kill bars

K1: this prereg commit strictly precedes the implementation commit
(verified with git merge-base --is-ancestor).
K2: R1 revert-resilience run (W2==W0 via REVISE edit trace, k=2/k=2)
and R2 permanent-change control (no snapback, W2p==W1p) both match
frozen predictions; FROZEN baseline shows the failure-to-revise
pathology; the L3-revision framing is evaluated honestly on the
trace (section 7).
K3: pure Zag, zero Python at every step, 3/3 byte-identical runs,
no em/en dash bytes (shell-only check_no_dash.sh).

## 7. L3-revision framing (frozen)

Mere L2 re-selection is REBUILD: the graph is discarded each phase
and rebuilt from scratch; nothing persists. Evidence TOWARD the
revision criterion is REVISE: the white-box trace shows the SAME
learned structure modified by edits (W0 ->k=2-> W1 ->k=2-> W2=W0),
i.e. the structure persists and is revised, not rebuilt. What is
still missing for L3: the edit vocabulary (change-delay, add-rule,
remove-rule), the KMAX bound, the consistency criterion, and the
revision trigger are researcher-supplied; the learner does not invent
edit types. Classification ceiling for this work: bounded L2+.
A REVISE outcome matching predictions is revision evidence, not an
L3 claim. If REVISE fails where REBUILD succeeds, the bound (not the
mechanism) is the finding.

## 8. Honesty notes (frozen)

- Researcher still owns: variable set, rule/delay vocabulary,
  arrival semantics, passive evidence sets, true laws, edit
  vocabulary, KMAX, intervention primitives, derivation core.
  The learner authors: the candidate graphs (constructed, not
  listed), the edit chains, per-round targets conditioned on
  observed outcomes, and resolutions.
- Learned graphs are behavioral representatives: with X-only
  interventions the chain [(X->Z,1),(Z->Y,1)] and
  [(X->Y,2),(X->Z,1)] are indistinguishable; the learner correctly
  treats them as one hypothesis. Chain-form identification is NOT
  claimed.
- Bounded L2+. NOT L3. The generic causal-revision interpretation
  stays KILLED (REVISE-REDTEAM-KILLS); this work tests revision of a
  learner-constructed graph, not generic causal revision.
- Do not spawn H-CAUSALV7. H-CAUSALEXP is the lane direction.

## 9. Deliverables

causal_revert.zag, BUILD.sh, RUN.sh (3 identical runs), VERIFY.sh
(checking every frozen line in section 5), CAUSAL_REVERT_RESULT.md.
Committed with owned pathspec only.
