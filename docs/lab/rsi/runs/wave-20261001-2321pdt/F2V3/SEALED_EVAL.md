# SEALED EVALUATION: F2 v4 (depth-9 candidate)

Date: 2026-10-01/02. Lane: F2V3 (wave-20261001-2321pdt).
Frozen prereg: PREREG_F2V4.md (commit 5e4e56a5f).
Implementation: f2v4_learner.zag (commit b5fcf9ae3).
Sealed binaries: /tmp/f2v4_a
(sha256 9c1d44b85eeeae7be26b3b1777e26c09bdca4dc2307180be476fd3991a9cdfe7),
/tmp/f2v4_c2
(sha256 bdb8f9fc5e6ddad2c2cf9f98ca911debaffe654e70296925d5019ca9b70a7783).
Pure Zag throughout (Step 0 in NAMECHECK.md).

## Verdict: BUILD-PASS

All eight kill bars PASS in both fresh sealed worlds, 3/3 byte-identical
reruns per world (cmp-verified).

## World A-prime (fresh confounded chain): all bars PASS, 3/3 identical

- K4-R1 PASS: NHYP 4 >= 2 (X:0, Z:2, Y:2, D:1).
- K4-R2: source audit (IMPLEMENTATION.md); no complete experiment,
  distinguishing sequence, or goal plan as a literal; the executed
  discrimination experiments and goal plans differ across the two
  worlds in composition.
- K4-R3 PASS: zero world calls in search; ledger complete (no
  discrimination rounds needed; nalive=1 by the standard phase).
- K4-R4 PASS: true hypothesis {Z<-(X,3), Y<-(Z,2), D<-(X,1)} survives,
  nalive=1.
- K4-R4b: vacuous (no discrimination phase); standard-phase
  eliminations all contradicted actual observations.
- K4-R5 PASS: PLAN [SX,W,W,W,W,W,SX]; GOAL_REAL 1; RANDOM 0/20.
- K4-R6 PASS: OBS_USED 6.
- K4-R7 PASS: 3/3 byte-identical (cmp); pure Zag; no em dashes.
- PROGRAM_ALL_BARS_PASS (mask 63) on all three runs.

## World C2-prime (fresh sealed dual contextual delay): all bars PASS, 3/3 identical

- K4-R1 PASS: NHYP 216 >= 2 (X:6, Y1:6, Y2:6).
- K4-R2: as above.
- K4-R3 PASS: zero world calls in search. Every executed experiment
  logged with predicted observation vectors showing disagreement
  (per-hypothesis for the 5 standard rounds, per-pair for the 4
  discrimination rounds); the discrimination ledger is complete.
- K4-R4 PASS: the loop terminates with exactly one survivor
  (SURVIVORS [82], exhausted=0), and the sealed w_verify confirms its
  Y1 rule equals (X, 3, J == 1) and its Y2 rule equals (X, 2, K == 1).
  The full X-rule equivalence class (6 variants) is resolved by
  learner-discovered evidence.
- K4-R4b PASS: (i) every eliminated hypothesis contradicted the actual
  observation vector of a logged distinguishing sequence (ledger
  rounds 6-9, see below); (ii) at termination no live pair remains, so
  no D2 certificate is owed (nalive=1).
- K4-R5 PASS: PLAN_C2 M=[SX,SJ,SK,W,SX,W,SX,W,SX] full_len=24,
  PLAN_AGREEMENT 1; GOAL_REAL_C2 1 (all twelve SUFFIX observations 1);
  RANDOM_BASELINE_C2 0/20 (a priori seed 12345, 7-symbol alphabet,
  length len(M)+17=26).
- K4-R6 PASS: OBS_USED 21 on C2-prime; total across both worlds
  6 + 21 = 27 <= 32.
- K4-R7 PASS: 3/3 byte-identical (cmp); pure Zag; no em dashes.
- PROGRAM_ALL_BARS_PASS (mask 63) on all three runs.

### The killing evidence: the depth-9 crossed-context pair resolves

The sealed run's discrimination ledger (identical on all three runs):

- round 6, pair (78,79): 9-primitive [SX,SJ,W,CJ,W,W,W,W,OX],
  pred_i=[1] pred_j=[0] actual=[0], killed [78];
- round 7, pair (79,80): 8-primitive [SX,SJ,W,W,W,W,W,OX],
  pred_i=[1] pred_j=[0] actual=[0], killed [79];
- round 8, pair (80,81): 8-primitive [SX,SK,W,W,W,W,W,OX],
  pred_i=[0] pred_j=[1] actual=[0], killed [81,83];
- round 9, pair (80,82): 9-primitive [SX,SJ,W,SK,W,W,W,W,OX],
  pred_i=[1] pred_j=[0] actual=[0], killed [80].

SURVIVORS [82]: X rule (Y2->X, d3, J==1) [the true X has no law; this
is the surviving spurious X rule, which is outside the K4-R4 contract],
Y1 rule (X,3,J=1), Y2 rule (X,2,K=1), both true.

The pair (80,82) is the crossed-context pair (Y1->X, d2, K==1) vs
(Y2->X, d3, J==1): the exact structure the v3 prereg's depth-9 proof
covers and the v3 binary provably could not distinguish (D2CERT at
depth 8, nalive=2, K4-R4 FAIL in calibration). The v4 learner
discovered [SX,SJ,W,SK,W,W,W,W,OX]: SET X and SET J at t-5 (cause
arrangement), SET K at t-3 (the discriminating context, strictly
later), five WAITs, one OBSERVE X. This matches the hand-derived
minimal witness form from the prereg (section 2.1). The v3 buffer
could not even record a 9-primitive sequence; the resize was
load-bearing, not cosmetic.

### Non-regression

The v4 binary on the retired 2021pdt worlds (regression only):
- 2021pdt World A: PROGRAM_ALL_BARS_PASS (mask 63), GOAL_REAL 1,
  RANDOM 0/20. No regression.
- 2021pdt World C-prime (the v3 killing instance): the v4 binary
  resolves the (80,82) crossed pair with 9-primitive
  [SX,SJ,W,SK,W,W,W,W,OX], SURVIVORS [82] (true hypothesis),
  w_verify ty1=1 ty2=2, K4-R4 PASS, GOAL_REAL_C2 1, RANDOM 0/20,
  PROGRAM_ALL_BARS_PASS. Positive control: the bound change (and only
  the bound change) accounts for the resolution.

## Negative controls

- NC1 (random-action control; kill via K4-R5): 0/20 on both worlds.
  PASS.
- NC2 (memorization-replay baseline; reported, not kill): standalone
  pure-Zag program (f2v4_nc2.zag) storing the passive trace (18 steps)
  and all 4 executed discrimination experiment trajectories (34
  steps), acting by longest-suffix replay of goalvar observation
  histories (WAIT on no match), budget 30 steps. Replay produced
  [SX,SJ,W,CJ,W,W,W,W,OX,SJ,W,CJ,W,W,SJ,W,CJ,W,W,SJ,W,CJ,W,W,SJ,W,CJ,W,W,SJ]:
  it replays the first experiment and discovers the J gate flip from
  memory, but falls into a J-manipulation loop, never sets K, and
  cannot sustain the X cadence. NC2_RESULT 0: the sustained predicate
  is not achieved. Memorization (L0) does not explain the learner's
  goal success. Reported honestly as expected.
- NC3-prime (mechanism ablation; reported, not kill): the v3-frozen
  loop (D2=8) on C2-prime, run in pre-prereg calibration: terminates
  by exhaustion with SURVIVORS [80,82] (nalive=2), D2CERT logged for
  the crossed pair, K4-R4 FAIL (mask 31). The control is informative:
  the ONLY difference between the failing and passing binaries is the
  depth bound (8 vs 9) plus the buffer capacity it requires. The
  resolution is attributed to the bound change, not to the fresh
  world being easier.

## What BUILD-PASS establishes (and does not)

Establishes: the F2 loop with DPDS at D2=9 achieves sustained dual
contextual control on a fresh sealed world it never saw, and resolves
the full X-rule equivalence class including the depth-9
crossed-context pair by learner-discovered distinguishing evidence
with a complete elimination trail. That is bounded L2 structural
learning. DPDS remains bounded-effective, not complete: the bound is
9, and a future pair needing 10+ primitives would fail K4-R4 honestly.

Does NOT establish: L3 representational invention (Criterion 0 fails
as documented in the prereg section 10); generality beyond the tested
worlds; escape from the enumerate-then-select family. No L3 claim is
made. No promotion claim is made (promotion pipeline steps 4-11
remain for the parent to schedule).

## Provenance

- Prereg: PREREG_F2V4.md, frozen alone at commit 5e4e56a5f (before
  any implementation file existed; commit-order self-check in
  IMPLEMENTATION.md).
- Implementation: f2v4_learner.zag, commit b5fcf9ae3 (diff: 8 hunks,
  bound 8->9 plus buffer capacities).
- Sealed worlds: f2v4_world_aprime.zag (sha256
  fe909a1cf633238c2ebf30e1ba75acfc2486b2c4fad5863779a7d932423a824a),
  sealed/f2v4_world_c2prime.zag (sha256
  6454ff33815f31d3509f258b4633de0ab007f0c66dd72cfe292e088fcbfd3d5f);
  hashes recorded in the prereg before any v4 run.
- Sealed logs: /tmp/seal_a{1,2,3}.log, /tmp/seal_c{1,2,3}.log
  (ephemeral; 3/3 cmp-identical per world).
- Calibration logs (v3-frozen binary): /tmp/cal_a2.log (A-prime PASS),
  /tmp/cal_c2.log (C2-prime K4-R4 FAIL, nalive=2).
- Regression logs (v4 binary, 2021pdt worlds): /tmp/reg_a.log (PASS),
  /tmp/reg_c.log (killing instance resolved, PASS).
- NC2: /tmp/f2v4_nc2 binary; source f2v4_nc2.zag.
