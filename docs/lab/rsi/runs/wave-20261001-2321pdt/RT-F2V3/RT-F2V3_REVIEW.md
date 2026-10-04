# RT-F2V3 RED-TEAM REVIEW: F2 v4 (depth-9 candidate), wave-20261001-2321pdt

Reviewer: RT-F2V3 lane (independent second opinion on the F2V3 lane's
BUILD-PASS verdict for F2 v4). Pure Zag throughout; toolchain guard
Step 0 recorded in this lane's NAMECHECK.md (`which python3` printed
nothing). Working copy ~/workspace/tnn-rsi, branch tnn-native-lab.
READ-ONLY toward the F2V3 lane dir: every lane source below was
extracted with `git show` from the recorded commits (prereg
5e4e56a5f, implementation b5fcf9ae3, sealed eval 30a1ff7e0, judge
brief d0846df90). No em dashes in this document (checked with
check_no_dash.sh before commit).

## Verdict: EVIDENCE-HOLDS (clean pass)

I attacked the BUILD-PASS verdict along all seven assigned axes,
rebuilding both binaries from committed sources and re-running the
key experiments independently. Every claim I could test reproduced
exactly. One axis (depth-9 minimality) I tested more strongly than
the lane did, and it held. No bar moved, no ordering violation, no
hidden mechanism change, no vacuously easy world. Details below.

## Axis 1. Weakened bars: no bar moved after freezing

I compared each bar as reported in SEALED_EVAL.md (commit 30a1ff7e0)
against the frozen PREREG_F2V4.md (commit 5e4e56a5f), K4-R1 through
K4-R7 plus the D2=9 restatement:

- K4-R1: prereg demands >= 2 passive-consistent hypotheses in EACH
  world. Eval reports NHYP 4 (A-prime) and NHYP 216 (C2-prime). My
  independent runs print the same NHYP values. Match.
- K4-R2: prereg demands no complete experiment, distinguishing
  sequence, or goal plan as a source literal, and requires the
  executed experiments and goal plans to differ across the two worlds
  in composition. Eval cites the IMPLEMENTATION.md source audit. I
  audited L_dpds_pair, L_find, and L_plan myself: all three construct
  sequences exclusively by iterative-deepening base-A/P counting over
  primitives; no sequence literal exists in source. My runs show
  A-prime PLAN [SX,W,W,W,W,W,SX] with zero discrimination rounds vs
  C2-prime PLAN_C2 M=[SX,SJ,SK,W,SX,W,SX,W,SX] with four
  discrimination rounds. Composition differs. Match.
- K4-R3: prereg demands every executed experiment be logged with
  prior disagreement and zero world actions during search, with a
  complete discrimination ledger. Eval reports world_calls=0 on all
  rounds and a complete 4-round ledger. My runs print
  `SEARCH round=N world_calls=0` and `DPDS round=N world_calls=0`
  for every round on both worlds, and the DISC_LEDGER lines match
  the eval verbatim. Match.
- K4-R4: prereg demands on A-prime that the true hypothesis
  {Z<-(X,3), Y<-(Z,2), D<-(X,1)} survives with no live pair
  distinguishable to D2=9, and on C2-prime exactly one survivor
  with w_verify confirming Y1=(X,3,J==1), Y2=(X,2,K==1). My runs:
  A-prime SURVIVORS [0] (nalive=1, true hypothesis), C2-prime
  SURVIVORS [82] with `K4-R4 PASS` (ty1=1 ty2=2). Match. (With
  nalive=1 there are no live pairs, so the A-prime exhaustion
  clause is vacuously satisfied; this is the prereg's own
  formulation, not a reinterpretation.)
- K4-R4b: prereg clause (i) requires every discrimination-phase
  elimination to contradict the actual observation vector of a
  logged distinguishing sequence; clause (ii) requires a logged D2
  certificate for every live pair at termination. The eval reports
  (i) via ledger rounds 6-9 and (ii) as "no D2 certificate is owed
  (nalive=1)". This is a faithful reading, not a weakening: the
  prereg's own parenthetical for this bar states that on C2-prime
  the bar is meant to establish the class "was resolved by
  learner-discovered evidence, not exhausted as an indistinguishable
  class", which is exactly what nalive=1 via four logged
  distinguishing sequences establishes. Match.
- K4-R5: A-prime GOAL_REAL 1 + RANDOM 0/20; C2-prime GOAL_REAL_C2 1
  (twelve SUFFIX observations all 1) + RANDOM_BASELINE_C2 0/20 with
  the frozen seed 12345, 7-symbol alphabet, length 26. My runs print
  identical lines. Match.
- K4-R6: budget 32 total active OBSERVEs. My runs: 6 (A-prime) +
  21 (C2-prime) = 27 <= 32. Match.
- K4-R7: 3/3 byte-identical reruns per world, pure Zag, no em
  dashes. Independently verified below (axis 5). Match.

BUILD-PASS required all eight bars in both worlds; the eval names
the exact frozen bars. No bar text changed between the freeze and
the verdict.

## Axis 2. Commit-order self-check: ordering verifies

- 5e4e56a5f (prereg freeze): 2026-10-02 06:38:18 UTC. Contains ONLY
  PREREG_F2V4.md (1 file, 316 lines).
- b5fcf9ae3 (implementation): 2026-10-02 06:42:42 UTC. Adds build.sh
  and f2v4_learner.zag. Strictly after the freeze.
- 30a1ff7e0 (sealed eval): 2026-10-02 07:20:36 UTC.
- d0846df90 (judge brief): 2026-10-02 07:20:56 UTC.
- `git log --diff-filter=A -- '*f2v4_learner.zag'` shows the file
  was added only in b5fcf9ae3 and in the restore commit 30a1ff7e0.
  No F2 v4 implementation file existed anywhere in history before
  the prereg freeze.
- `git merge-base --is-ancestor` confirms both 5e4e56a5f and
  b5fcf9ae3 are ancestors of HEAD.
- The unrelated worker commit f461e812d (2026-10-02 07:19:22 UTC)
  deleted lane files from the tree; 30a1ff7e0 restored them. I
  verified the restoration is byte-identical: sha256 of
  PREREG_F2V4.md is ece67fb7... at both 5e4e56a5f and 30a1ff7e0;
  sha256 of f2v4_learner.zag is 0f51707d... at both b5fcf9ae3 and
  30a1ff7e0. The judge brief's account of this incident is
  accurate, and the commit-order self-check still verifies because
  the original commits remain ancestors of HEAD.

No UNVERIFIABLE ORDERING. The prereg was frozen alone before any
implementation file existed.

## Axis 3. The "one constant" claim: diff verifies exactly

`diff` of f2v3_learner.zag (from the 2021pdt wave record, commit
a272a8f6a) against f2v4_learner.zag (commit b5fcf9ae3) contains
exactly these changes, nothing else:

1. Header comment block rewritten (wave/prereg references).
2. `L_D2()`: `return 8` -> `return 9`. The single mechanism change.
3. Two comment lines updated (bound references).
4. Discrimination ledger record: copy loop `while(i<8)` ->
   `while(i<9)`; offsets reshifted (seq kinds base+16, seq vars
   base+25, predi/predj/actual/nkilled at base+34/38/42/46,
   killed flags at base+50); reclen 48+nhyp -> 50+nhyp.
5. Discrimination sequence buffers dsk/dsv: `z_alloc(8)` ->
   `z_alloc(10)`.

(IMPLEMENTATION.md says "8 hunks"; normal diff shows 9 hunk groups.
Trivial counting difference; the scope claim verifies exactly.)

No change to L_pairdiff, the restricted alphabet, the
exactly-one-OBSERVE rule, first-hit selection order, the standard
depth-6 scan, candidate generation, the goal planner, the random
control, or any world interface. No new modes, bridges, routers,
handlers, or semantic cases. `L_D2()` has exactly two use sites
besides its definition: the DPDS iterative-deepening bound
(`while(d<=L_D2())`) and the D2CERT log message. The bound change
cannot leak into any other mechanism.

## Axis 4. Non-vacuity: the fresh world is a genuine depth-9 test

I rebuilt the v3-frozen binary from committed sources
(f2v3_learner.zag at a272a8f6a + sealed C2-prime world at
30a1ff7e0) with the pinned znc via safebin. Result:

- Rebuilt binary sha256:
  44f800c7542cb9d0e930063b0786f072f89e26c734cdbfd42aa0594344c2d3e9,
  which EXACTLY matches the calibration binary hash recorded in
  PREREG_F2V4.md section 4. The committed sources reproduce the
  pre-prereg calibration binary byte-for-byte.
- Running it on the sealed C2-prime world reproduces the
  calibration: NHYP 216; standard phase reduces to nalive=6;
  `D2CERT pair=(78,79) no distinguishing sequence to depth 8`;
  `D2CERT pair=(80,82) no distinguishing sequence to depth 8`;
  `SURVIVORS [80,82] exhausted=1`; final `PROGRAM_FAIL mask=31`
  (K4-R4 FAIL, as the prereg's NC3-prime calibration reported).
- Sealed world file hashes match the prereg verbatim:
  A-prime fe909a1c..., C2-prime 6454ff33... (sha256 of the
  committed blobs).
- The goal achievability and random-control legs of the
  non-vacuity certificate are corroborated by my v4 runs
  (GOAL_REAL_C2 1 with len(M)=9; RANDOM 0/20).

C2-prime is not tuned for the v4 binary: the v3-frozen binary
fails on it in exactly the preregistered way. The depth-9 gap is
real.

## Axis 5. Determinism: 3/3 byte-identical, independently verified

I rebuilt both v4 binaries from committed sources (f2v4_learner.zag
at b5fcf9ae3 + worlds at 30a1ff7e0):

- /tmp/rt/v4_a sha256
  9c1d44b85eeeae7be26b3b1777e26c09bdca4dc2307180be476fd3991a9cdfe7:
  EXACT match to IMPLEMENTATION.md.
- /tmp/rt/v4_c2 sha256
  bdb8f9fc5e6ddad2c2cf9f98ca911debaffe654e70296925d5019ca9b70a7783:
  EXACT match to IMPLEMENTATION.md.

Then 3 runs per world, stdout captured, compared with `cmp`:

- A-prime: 3/3 byte-identical. PROGRAM_ALL_BARS_PASS on all three.
- C2-prime: 3/3 byte-identical (sha256
  b31017ef0f2500d666609fb42a7ac9e6c5f5afb4f7a9bed0aeb04c1c47021ccc
  on all three logs). PROGRAM_ALL_BARS_PASS (mask 63) on all
  three.

Reproducible builds from committed sources plus independent 3/3
reruns. K4-R7 holds on evidence I generated myself, not on the
lane's /tmp logs.

## Axis 6. Depth-9 minimality: holds over the FULL alphabet

The lane's minimality evidence is (a) a hand proof (prereg 2.1)
that any distinguishing sequence for the crossed pair needs >= 9
primitives, and (b) the v3 scan's exhaustive depth-8 search logging
a D2 certificate. I probed both:

(a) Scan exhaustiveness audit. I read L_dpds_pair in full. For each
depth d in 1..D2 it enumerates all A^d sequences by base-A
counting (A = 2*nctrl+1+nd), filters to exactly-one-OBSERVE, and
simulates both hypotheses. The exactly-one-OBSERVE filter is
completeness-preserving: OBSERVE is state-neutral in both L_sim
and w_act, so any distinguishing sequence has a distinguishing
prefix ending at its first distinguishing OBSERVE, which the
enumeration covers. The enumeration itself is complete (standard
positional decoding, lexicographic). No pruning bug found.

(b) Independent brute-force minimality check (pure Zag program,
/tmp scratch, not committed). I reimplemented the exact law
semantics (L_advance: context evaluated at cause time s=t-d,
persistent J/K, decay of unruled vars; L_sim: SET/CLR at current
t, WAIT advances t, OBSERVE records) and enumerated ALL sequences
to depth 8 over the FULL 12-symbol alphabet (SET/CLR X,J,K; WAIT;
OBSERVE of X,Y1,Y2,J,K), simulating both crossed hypotheses
(Y1->X,d2,K==1) vs (Y2->X,d3,J==1) with shared true Y1/Y2 rules
from the zero initial state, checking all five observables. This
is strictly stronger than the lane's restricted-alphabet scan.
Result: 0 distinguishing sequences at depth <= 8
("MINIMALITY-HOLDS"). Sanity check: the learner-discovered
9-primitive witness [SX,SJ,W,SK,W,W,W,W,OX] distinguishes in my
simulator too (A=1, B=0), confirming my semantics match the
learner's.

The "provably could not distinguish" claim therefore holds not
just within the scan's restricted alphabet but over the full
action alphabet. No depth-8 distinguishing sequence exists for
the v3 scan to have missed.

## Axis 7. Knowledge-vs-architecture: bound raise only

- The v4 binary's C2-prime resolution is fully explained by the
  bound raise: my v4 run's ledger shows round 9 resolving pair
  (80,82) with the 9-primitive sequence, which the D2=8 scan
  provably could not express (axis 6) and the D2=8 binary
  provably could not find (axis 4).
- The buffer resize (8->10) is capacity only: dsk/dsv are filled
  by L_dpds up to found length and consumed by index < dlen;
  enumeration order is by (depth, lexicographic index) and does
  not depend on buffer size. The 10th slot is never addressed by
  a 9-length sequence.
- The ledger changes (reclen, 9-slot copy loop, reshifted offsets)
  are record-layout only; the ledger is append-only logging
  consumed by the K4-R3 completeness check, not by search
  decisions.
- Nothing in the diff alters search order, candidate generation,
  the goal planner, or world interfaces.

The success depends on nothing beyond the bound raise plus the
capacity the bound requires, exactly as the lane claims.

## Process observations (not qualifications)

1. The sealed world files were committed at 30a1ff7e0, after the
   sealed runs; during the runs they lived in the working tree.
   The seal mechanism that matters (hashes frozen in the prereg
   before any v4 run) is intact: the committed blobs hash exactly
   to the prereg-recorded values, and committed sources rebuild
   the recorded binaries byte-for-byte. Provenance chain closed.
2. IMPLEMENTATION.md says "8 hunks"; normal diff shows 9 hunk
   groups. Wording only; the scope claim ("all within the
   bound/buffer/ledger scope") verifies exactly.
3. NC2 (memorization-replay baseline) is reported-not-kill; I
   reviewed its documented design and result but did not
   independently re-run it, since no kill bar depends on it.

## Bottom line

The F2V3 lane's BUILD-PASS for F2 v4 stands. The prereg froze
alone before any implementation file; the implementation is
exactly the one-constant change claimed; the fresh sealed world
is a genuine depth-9 test (the v3 binary fails it in the
preregistered way, reproduced from committed sources); the v4
binary passes all eight frozen bars in both worlds with
independently verified 3/3 byte-identical determinism; and the
depth-9 minimality claim survives an independent full-alphabet
brute-force check. No frozen bar or process rule was violated.
