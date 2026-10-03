# JUDGE BRIEF: F2 v4 (depth-9 candidate), wave-20261001-2321pdt, lane F2V3

## Provenance header

- RENDER_SHA: 30a1ff7e0
- FIRST_RENDERED_WAVE: wave-20261001-2321pdt
- COMPONENT_LINEAGE: F2 v1 BUILD-FAIL, F2 v3 BUILD-FAIL on K4-R4 depth
- NEW_KNOWLEDGE_CLAIM: Raising the DPDS discrimination bound from 8 to
  9 (one constant plus the buffer capacity it requires, no mechanism
  change) lets the frozen F2 loop resolve the full X-rule equivalence
  class including the crossed-context depth-9 pair on a fresh sealed
  world, achieving sustained dual contextual control with a complete
  learner-discovered elimination trail.

## Verdict: BUILD-PASS

All eight frozen kill bars (K4-R1 through K4-R7, as restated with D2=9
in PREREG_F2V4.md, commit 5e4e56a5f) PASS in both fresh sealed worlds.
3/3 byte-identical reruns per world (cmp-verified). No regressions on
the retired 2021pdt worlds.

## What was tested

F2 v3 failed in wave-20261001-2021pdt on K4-R4: its DPDS mechanism
(pairwise deep search to D2=8) provably could not distinguish the
final crossed-context X-rule pair, which needs depth-9 distinguishing
sequences (hand-verified minimal construction: 9 primitives; the v3
binary's exhaustive depth-8 scan logged a D2 certificate). F2 v4
changes exactly one thing: the bound D2 is 9 (plus discrimination
sequence buffers 8->10 slots and ledger record 48+nhyp->50+nhyp, the
capacity the bound requires). The pair-diff, restricted alphabet,
exactly-one-OBSERVE rule, first-hit order, standard depth-6 scan,
candidate generation, goal planner, and random control are unchanged.

Two FRESH sealed worlds (hashes frozen in the prereg before any v4
run; the 2021pdt worlds are regression only):
- A-prime: confounded chain (X->Z d3, Z->Y d2, X->D d1), X pulses at
  t=2,7,13 (unequal spacing keeps X exogenous).
- C2-prime: dual contextual delay (X->Y1 d3 J==1, X->Y2 d2 K==1),
  npass=18, X pulses at t=3,8,13, goal setup J=0,K=0, sustained
  predicate [Y1,Y2,J,K]=[1,1,1,1] for three consecutive steps.

## Killing evidence

1. Non-vacuity (v3-frozen binary, pre-prereg calibration): C2-prime
   yields X:6/Y1:6/Y2:6 candidates (NHYP 216); the v3 loop terminates
   by exhaustion with SURVIVORS [80,82] (nalive=2), D2CERT logged for
   the crossed pair (Y1->X,d2,K==1) vs (Y2->X,d3,J==1); the goal is
   achievable (GOAL_REAL_C2 1, len(M)=9); random 0/20. The fresh
   world is a genuine depth-9 test, not tuned for the new binary.
2. Sealed C2-prime (v4 binary, first run = sealed evaluation): the
   discrimination ledger shows four rounds, all with logged prior
   disagreement; round 9 resolves pair (80,82) with the
   learner-discovered 9-primitive sequence [SX,SJ,W,SK,W,W,W,W,OX]
   (pred_i=[1] pred_j=[0] actual=[0], killed [80]), matching the
   hand-derived minimal witness form from the prereg. SURVIVORS [82]
   (single); sealed w_verify confirms Y1=(X,3,J==1), Y2=(X,2,K==1);
   K4-R4 PASS. GOAL_REAL_C2 1; RANDOM 0/20; OBS total 27/32.
   PROGRAM_ALL_BARS_PASS (mask 63), 3/3 identical.
3. Sealed A-prime: PROGRAM_ALL_BARS_PASS (mask 63), 3/3 identical;
   true hypothesis survives (nalive=1); GOAL_REAL 1; RANDOM 0/20.
4. Positive control (v4 binary on retired 2021pdt C-prime, the v3
   killing instance): resolves (80,82) with 9-primitive
   [SX,SJ,W,SK,W,W,W,W,OX]; SURVIVORS [82] (true hypothesis);
   PROGRAM_ALL_BARS_PASS. The bound change (and only the bound
   change) accounts for the resolution.
5. NC3-prime ablation (v3 binary on C2-prime): nalive=2, K4-R4 FAIL.
   Informative: the ONLY binary difference is the bound.
6. NC2 (memorization-replay baseline, standalone pure Zag): stores
   the passive trace and all 4 experiment trajectories, acts by
   longest-suffix replay (WAIT on no match), 30-step budget.
   NC2_RESULT 0: it replays the first experiment and finds the J
   gate flip but loops on J-manipulation, never sets K, and cannot
   sustain the X cadence. L0 storage does not explain the goal.

## Honest boundaries

DPDS remains bounded-effective, not complete: the bound is 9, and a
future pair needing 10+ primitives would fail K4-R4 honestly. No L3
claim is made (Criterion 0 fails as documented in the prereg: the
rule semantics are researcher-authored, the solution space is
researcher-enumerated, and only two worlds were tested). No
generality claim beyond the tested worlds. No promotion claim
(promotion pipeline steps 4-11 remain for the parent to schedule).

## Reproduction

- Prereg: docs/lab/rsi/runs/wave-20261001-2321pdt/F2V3/PREREG_F2V4.md
  (commit 5e4e56a5f, frozen alone before any implementation file).
- Implementation: f2v4_learner.zag (commit b5fcf9ae3; diff 8 hunks).
- Build: build.sh (pinned znc via safebin; pure Zag).
- Sealed worlds: f2v4_world_aprime.zag, sealed/f2v4_world_c2prime.zag
  (hashes in prereg).
- Evidence: SEALED_EVAL.md, IMPLEMENTATION.md (commit 30a1ff7e0).
- Note: an unrelated worker commit (f461e812d) accidentally deleted
  this lane's files from the tree; they were restored from the intact
  working copy at 30a1ff7e0 (no reset, no rebase; the original
  commits 5e4e56a5f and b5fcf9ae3 remain ancestors of HEAD, so the
  commit-order self-check still verifies).
