# IMPLEMENTATION.md - F2 v3 (wave-20261001-2021pdt, lane F2v3)

Date: 2026-10-01. Frozen prereg: PREREG_F2V3.md, committed alone at
13206c15b. Builder: research worker (depth 2/2), lane F2v3-IMPL.
Pure Zag; safebin toolchain guard recorded in NAMECHECK.md Steps 0 and
0b (`which python3` / `which python` return nothing; no forbidden
executable invoked at any stage, including build, execution, and log
handling). No em dashes in this documentation (verified by grep).

Commit-order self-check: 13206c15b is an ancestor of HEAD
(`git merge-base --is-ancestor` verified); zero commits touched this
lane dir between 13206c15b and the implementation writes; all
implementation files below are new untracked files first appearing
after the prereg commit. Ordering verifiable; prereg not voided.
No commits by this worker; coordinator commits.

## Status: IMPLEMENTATION COMPLETE

DPDS implemented exactly per prereg section 3. Development and control
testing done on World A (retained) and two implementer-designed
development C-prime analogs (Cdev1, Cdev2). Negative controls NC1
(random 0/20, seed 12345, part of K4-R5b on all worlds) and NC3 (v2-loop
ablation) run. NC2 (memorization-replay baseline) is preregistered as
reported-not-kill and is left for the sealed-evaluation phase; it was
not run this turn.

## What was built

Five Zag sources under this lane dir (concatenated at build time;
build.sh):

- f2v3_learner.zag (1133 lines): v2 learner plus the ONE generic
  mechanism change. New: L_pairdiff (runtime structural diff over
  hypothesis rule-set data; no variable-specific knowledge in source),
  L_dpds_pair (restricted-alphabet iterative deepening to D2 = 8:
  SET/CLR per controllable in w_ctrl order, WAIT, OBSERVE of differing
  variables only in ascending index order, exactly one OBSERVE per
  sequence; first hit in depth-ascending lexicographic order),
  L_dpds (ascending live-pair scan; first distinguishing pair wins;
  per-pair D2 certificates on exhaustion), L_ledger_append /
  L_ledger_emit (discrimination ledger: learner-created persistent
  state, fixed records of round, pair, sequence, both predicted
  vectors, actual vector, killed indices; allocated once, appended
  across search rounds). The experiment loop is the v2 loop with the
  DPDS continuation: standard scan miss with nalive > 1 fires DPDS;
  after each discrimination experiment the loop repeats from the
  standard scan; termination at nalive == 1 or full-pair D2 exhaustion.
  Also generalized: the C2 goal planner, SUFFIX builder, agreement
  check, and random control are now generic over the
  w_ngoalvars/w_goalvar/w_goalval interface (prereg section 5), so the
  learner is world-agnostic. World A path replicated exactly from v2.
  Observation budget raised to 32 (K4-R6).
- f2v3_world_a.zag: World A replicated exactly (same physics, goal,
  planner, control). w_verify implements K4-R4: true hypothesis
  {Z<-(X,2), Y<-(Z,1), D<-(X,1)} survives AND termination by exhaustion
  (no live pair distinguishable to D2); the v2 nalive count is not
  frozen (DPDS may legitimately resolve the pair; with nalive == 1 the
  no-distinguishable-pair condition holds vacuously). Goalvar
  interface stubs added (unused in goal mode 0).
- f2v3_world_cdev1.zag: DEVELOPMENT dual-contextual world (not
  sealed). Implementer-designed C-prime analog: X->Y1 delay 3 iff
  J==1; X->Y2 delay 2 iff K==0; X decays; J,K persistent; passive 13
  steps with X pulses at t = 1, 5, 9 and J=1, K=0 throughout; goal
  setup J=0, K=1 (both gates wrong); goalvars [Y1,Y2,J,K] = [1,1,1,0].
  w_verify implements the K4-R4 C-prime contract: exactly one
  survivor whose Y1 rule is (X,3,J==1) and Y2 rule is (X,2,K==0).
- f2v3_world_cdev2.zag: second DEVELOPMENT analog (mirrored):
  X->Y1 delay 2 iff J==1; X->Y2 delay 3 iff K==0; same passive shape;
  same goal setup and interface.
- build.sh: concatenation + pinned znc compile. Binaries in /tmp
  (ephemeral); logs in this lane dir.

Binaries (sha256):
- /tmp/f2v3_a: 62ee648f5d31d67b0877e77f1fe7dfe3e40740d39001015caaa71beb47d8dc40
- /tmp/f2v3_cdev1: f967ddcf5db8a0cb4f997e7f63515c580ec14813c26831942529b67b8f3efbf9
- /tmp/f2v3_cdev2: 961890b42e91a22e51e4d2184af3ab7aedb9588fe2443a01e0de43dba4209547
- /tmp/f2v3_nc3 (NC3 ablation, frozen v2 learner + Cdev1): 514fcdb0a9bdf56a331efaed19de7ccc2ce2e694a75c0e14c96b0363e6022731

## Development results

### World A (regression anchor)

3/3 runs byte-identical, sha256
d264bfb78bcb1a3877c4aea2a8811fa437be7e8a8d3c37b245e92be05b99a23d.
Program verdict: F2V3_A PROGRAM_ALL_BARS_PASS (MASK 63).

| Bar | Result | Numbers |
|-----|--------|---------|
| K4-R1 | PASS | NHYP 6 >= 2 (X:0, Z:2, Y:3, D:1) |
| K4-R2 | PASS | source audit below; experiments composed by enumeration; plans differ across worlds |
| K4-R3 | PASS | 2 standard rounds + 1 DPDS pass, world_calls=0 in every search |
| K4-R4 | PASS | true_h=2 alive=1, nalive=2, exhausted=1 |
| K4-R5a | PASS | PLAN [SX,W,W,W,SX], PLAN_AGREEMENT 1, GOAL_REAL 1 |
| K4-R5b | PASS | RANDOM_BASELINE 0/20 (seed 12345) |
| K4-R6 | PASS | OBS_USED 6 <= 32 |
| K4-R7 | PASS | 3/3 byte-identical; pure Zag; no em dashes |

DPDS behavior on A: after the standard scan exhausted with nalive=2,
DPDS fired on the single live pair (0,2), computed D={Y} at runtime,
scanned the pair-restricted alphabet to depth 8, found no
distinguishing sequence, and logged the D2 certificate:
`D2CERT pair=(0,2) no distinguishing sequence to depth 8`.
Termination by honest exhaustion; ledger_n=0 (no discrimination
experiments, correctly).

### Development world Cdev1 (implementer-designed analog)

3/3 runs byte-identical, sha256
2ef223ba27f60a6c7088bff9256290a2446e1f66985541794c1acaabc6ae3634.
Program verdict: F2V3_CDEV1 PROGRAM_ALL_BARS_PASS (MASK 63).

| Bar | Result | Numbers |
|-----|--------|---------|
| K4-R1 | PASS | NHYP 216 >= 2 (X:6, Y1:6, Y2:6; 6x6x6) |
| K4-R2 | PASS | source audit below |
| K4-R3 | PASS | 7 rounds (5 standard + 2 DPDS), world_calls=0 in every search; every executed experiment logged with disagreement |
| K4-R4 | PASS | nalive=1; survivor hyp79 with Y1rule=(X,3,J==1) and Y2rule=(X,2,K==0) = true laws |
| K4-R4b | PASS | (i) all 3 discrimination eliminations backed by logged distinguishing experiments; (ii) nalive=1 so no live pairs remain (certificates vacuous) |
| K4-R5a | PASS | PLAN_C2 M=[SX,SJ,CK,W,SX,W,SX,W,SX] (9 primitives), PLAN_AGREEMENT 1, GOAL_REAL_C2 1, obs=[1,1,1,0]x3 |
| K4-R5b | PASS | RANDOM_BASELINE_C2 0/20 (7-symbol alphabet, len 26, seed 12345, semantic trajectory predicate) |
| K4-R6 | PASS | OBS_USED 19 <= 32 |
| K4-R7 | PASS | 3/3 byte-identical; pure Zag; no em dashes |

Discrimination phase detail (the mechanism working as specified):
- Standard rounds 1-5 pinned Y1/Y2 to truth (216 -> 72 -> 36 -> 12 ->
  6 -> 4), leaving the X-rule equivalence class [78,79,80,82].
- Round 6: standard scan miss; DPDS pair (78,79), D={X} computed at
  runtime; restricted-alphabet search found [SX,SJ,W,CJ,W,W,W,OX]
  (8 primitives; discovered by enumeration, not a source literal);
  pred_i=[1] vs pred_j=[0]; actual [0]; eliminated EVERY
  contradictor [78,80]; nalive=2. Ledger entry appended.
- Round 7: standard scan miss; DPDS pair (79,82), D={X}; found
  [SX,W,SJ,W,W,W,OX] (7 primitives); pred_i=[0] vs pred_j=[1];
  actual [0]; killed [82]; nalive=1. Ledger entry appended.
- Survivor hyp79 carries the true Y1/Y2 laws (its X rule,
  (Y1,1,J==1), is spurious but harmless; the K4-R4 contract checks
  only Y1/Y2, per prereg).
- Cross-world observation total: A(6) + Cdev1(19) = 25 <= 32.

### Development world Cdev2 (second implementer-designed analog)

3/3 runs byte-identical, sha256
b863f168eb03c8d2100f185fce087671516f4bda85a3373bf02a669e3fab1127.
Program verdict: F2V3_CDEV2 PROGRAM_ALL_BARS_PASS (MASK 63).
Same bar table as Cdev1 (NHYP 216; 7 rounds; same DPDS pair order and
same discovered sequences, an artifact of the isomorphic X-variant
structure; survivor hyp79 with Y1rule=(X,2,J==1), Y2rule=(X,3,K==0);
M=[SX,SJ,CK,W,SX,W,SX,W,SX]; GOAL_REAL_C2 1; RANDOM 0/20;
OBS_USED 19). The true laws differ from Cdev1 (delays 2,3 vs 3,2),
so this is an independent mechanism check, not a copy.

## Negative controls

- NC1 (random-action control; kill bar via K4-R5b): 0/20 on World A,
  0/20 on Cdev1, 0/20 on Cdev2 (all with a priori seed 12345).
  On the dual-contextual worlds the control uses the 7-symbol
  manipulation alphabet, length len(M)+17, and the semantic
  trajectory predicate (three consecutive joint steps).
- NC3 (mechanism ablation; reported, not kill): the frozen v2 learner
  (standard depth-6 search only, no DPDS) against Cdev1 terminates
  with nalive=4 (SURVIVORS [78,79,80,82], EXHAUSTION, PROGRAM_FAIL
  mask=19); against Cdev2 likewise nalive=4. This reproduces the v2
  failure mode exactly (X-variant equivalence class intact at the
  depth-6 bound) and attributes the Cdev1/Cdev2 resolutions to the
  DPDS mechanism rather than to the dev worlds being easier. The
  control is informative (not uninformative): the ablation fails
  K4-R4 on both dev worlds while the DPDS learner passes.
- NC2 (memorization-replay baseline): not run this turn; scheduled
  for the sealed-evaluation phase per the lane task.

## Discrimination ledger samples (Cdev1 run 1; complete ledger, 2 entries)

```
DISC_LEDGER round=6 pair=(78,79) seq=[SX,SJ,W,CJ,W,W,W,OX] pred_i=[1] pred_j=[0] actual=[0] killed=[78,80]
DISC_LEDGER round=7 pair=(79,82) seq=[SX,W,SJ,W,W,W,OX] pred_i=[0] pred_j=[1] actual=[0] killed=[82]
```

Both sequences were discovered by restricted-alphabet enumeration
(depths ascending, lexicographic); neither appears in source. Each
elimination is backed by its logged experiment (K4-R4b(i)). The
ledger is learner-created persistent state: allocated once in L_run,
appended once per discrimination experiment, entries determined
entirely by world responses. Binary records (round, pair, seqlen,
8+8 seq bytes, pred_i, pred_j, actual, nkilled, killed[nhyp]) are
held in memory across rounds; the log lines above are the audit
trail.

## K4-R2 source-audit self-check

- grep for the prereg's illustrative witness literals
  ([SX,W,W,W,W,SK,OX], [SJ,SK,SX,W,W,W,W,OX] patterns): no matches
  in f2v3_learner.zag.
- grep for hardcoded sequence/array literals or printed primitive
  sequences: none. The only bracket emit is L_emit_seq's generic
  delimiter; all sequences are printed from discovered buffers.
- Experiments are produced exclusively by L_find (standard,
  iterative deepening depths 1..6 over the full primitive alphabet)
  and L_dpds_pair (discrimination, depths 1..8 over the
  pair-restricted alphabet). No per-world branch, no task-specific
  gate, no variable-specific knowledge in the DPDS code path
  (L_pairdiff compares rule bytes generically).
- Goal plans are produced exclusively by L_plan (World A) and
  L_plan_c2 (dual-contextual worlds, generic over the goalvar
  interface). SUFFIX is built by L_build_suffix (counted loop over
  goalvars; the preregistered fixed measurement protocol; no
  manipulations; no literal).
- Executed experiments and goal plans differ across worlds in
  composition (A: [SD,W,OZ], [SD,W,W,OY], plan [SX,W,W,W,SX];
  Cdev1: five standard experiments plus two DPDS sequences above,
  plan [SX,SJ,CK,W,SX,W,SX,W,SX]).
- World files contain the worlds' own true laws (sealed test
  substrate, disclosed to the harness only); the learner never reads
  them (interface-only access).

K4-R2: PASS on all worlds.

## Architecture accounting

- Cognition source lines: learner 1133 lines total (v2: 840).
  DPDS block (L_pairdiff, L_dpds_pair, L_dpds, L_ledger_append,
  L_ledger_emit, lines 301-476): 176 lines including comments
  (over the prereg's 120-line builder target; the overrun is ledger
  append/emit plus section documentation). Remainder of the delta is
  the goalvar-interface generalization of the C2 planner/control
  and the loop restructuring.
- New hardcoded semantic cases: 0.
- New modes / bridges / routers: 0. DPDS is a continuation of the
  one existing select-execute-eliminate loop (prereg 3.3 analysis
  holds: identical code path for all worlds).
- New task-specific handlers: 0.
- New learner-state structures: 1 (discrimination ledger,
  learner-created persistent state, prereg section 4).
- The dev worlds are authored test substrate, not cognition.

## Honest boundaries

- Bounded L2 only. Criterion 0 fails as preregistered (C0-A: rule
  semantics researcher-authored; C0-B: solution space
  researcher-enumerated; C0-C not tested; C0-D partially met via
  goal planning). No L3 claim. No generality claim beyond the
  tested worlds (same discipline as the FW1-FW9 regression-battery
  ruling).
- The sealed World C-prime comes from the independent adversary
  post-freeze; the implementer never saw it. Cdev1/Cdev2 are
  implementer-designed analogs for development and controls only
  and must not be mistaken for sealed evaluation.

## Deviations

1. First Cdev1 build used npass=14, which produced zero X candidates
   (trace edge effects excluded the spurious X correlations), so
   DPDS never fired. Corrected to npass=13 (still >= 12 per the
   family spec) with X pulses at t = 1, 5, 9, which yields the
   intended 6 X candidates and the X-variant equivalence class.
   The npass=14 binary was discarded; all reported numbers are from
   the npass=13 build.
2. DPDS block is 176 lines vs the 120-line builder target (reported
   honestly above; not a kill bar).

## Verdict and readiness

IMPLEMENTATION COMPLETE. All development bars pass on World A,
Cdev1, and Cdev2 (MASK 63 each); NC1 kills at 0/20 on all three;
NC3 reproduces the v2 failure mode (nalive=4) on both dev analogs,
confirming the DPDS mechanism accounts for the resolution; R2
source audit passes; 3/3 byte-identical determinism on all worlds;
pure Zag throughout; no em dashes.

READY FOR SEALED EVALUATION, with one scheduling note: the sealed
run needs the adversary's World C-prime (laws, passive schedule,
goal setup, w_verify) plus the non-vacuity certificate, delivered
to the coordinator under seal. The frozen learner binary
(/tmp/f2v3_a-equivalent built from f2v3_learner.zag + sealed world)
must be built by the coordinator; the implementer must not see the
sealed world. NC2 (memorization-replay baseline) remains to be run
in the sealed phase.

## Files (all under docs/lab/rsi/runs/wave-20261001-2021pdt/F2v3/)

- NAMECHECK.md (Steps 0, 0b toolchain guard + build authorization)
- PREREG_F2V3.md (frozen prereg; committed alone at 13206c15b)
- f2v3_learner.zag, f2v3_world_a.zag, f2v3_world_cdev1.zag,
  f2v3_world_cdev2.zag, build.sh
- world_a_run1/2/3.log, world_cdev1_run1/2/3.log,
  world_cdev2_run1/2/3.log (3/3 byte-identical each)
- world_cdev1_nc3.log, world_cdev2_nc3.log (NC3 ablation logs)
- IMPLEMENTATION.md (this file)
