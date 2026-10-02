# PREREG_F2V4: Depth-9 discrimination bound on fresh sealed worlds

Date: 2026-10-01. Status: FROZEN. This prereg is written before any
implementation file for this wave exists. No `.zag` for F2 v4 exists at
freeze time. The coordinator must commit this prereg alone before any
implementation file exists; the commit-order self-check (prereg commit
strictly precedes the implementation commit) applies. UNVERIFIABLE
ORDERING voids this prereg.

Lane: F2V3 (wave-20261001-2321pdt). Candidate name: F2 v4 (depth-9
candidate). Governance: pure Zag only (safebin; Step 0 recorded in
NAMECHECK.md). No em dashes in wave documentation.

## 1. Objective

Test the F2 autonomous-scientist loop with DPDS (frozen v3 mechanism)
against FRESH sealed worlds with the ONE generic change in section 3:
the discrimination depth bound D2 raised from 8 to 9. The v3 BUILD-FAIL
was a depth-bound coverage gap (K4-R4: nalive=2; the final X-rule pair
provably needs depth-9 distinguishing sequences, D2=8 insufficient),
not a loop malfunction and not a goal failure. v4 must resolve the
depth-9 pair by learner-discovered evidence while passing every other
bar with no regressions.

## 2. Prior history (read first)

- F2 v1 (2026-09-30): BUILD-FAIL on K-AS5b (weak goal instance).
- F2 retry (2026-09-30): BUILD-PASS on the harder B2 goal.
- F2 v2 (wave-20261001-1721pdt): BUILD-FAIL on K3-R4 (nalive=4 X-rule
  equivalence class; depth-6 bound provably blind to >=7-primitive
  discriminations).
- F2 v3 (wave-20261001-2021pdt): DPDS mechanism (pairwise deep search to
  D2=8). Sealed evaluation: K4-R1/R2/R3/R5/R6/R7 PASS, K4-R4b PASS,
  K4-R4 FAIL. The sealed World C-prime run terminated by exhaustion
  with SURVIVORS [80,82] (nalive=2): the crossed-context X-rule pair
  (Y1->X, d3, K==1) vs (Y2->X, d2, J==1), with a logged D2 certificate
  (no distinguishing sequence to depth 8). DPDS resolved 4 of 6
  X-variants by discovered evidence; the residual pair needs depth 9.
  DPDS is bounded-effective, not complete, at D2=8. The 2021pdt
  BUILD-FAIL stands as history; this is a new candidate with its own
  prereg, not a bar change.

### 2.1 The depth-9 proof (carried over, re-verified on the fresh world)

For a crossed-context X-rule pair (Ya,da,Kb==1) vs (Yb,db,Ja==1) with
true laws (X->Ya, dta, Ja==1), (X->Yb, dtb, Kb==1), da+dta = db+dtb = 5,
|da-db| = 1, experimental initial state J=K=0: any distinguishing
sequence must (i) SET X at t-5 (the unique cause time arranging both
effects), (ii) SET the cause-enabling context at t-5, (iii) SET the
discriminating context at a strictly later step (t-4..t-3) so it holds
at the later context-evaluation time but not at the earlier cause
time, (iv) WAIT 5 steps total, (v) OBSERVE X at t. That is at least 3
manipulations at 2 distinct steps + 5 WAITs + 1 OBSERVE = 9 primitives;
every alternative construction (context flip instead of
cause-blocking, arranging the other cause) uses 9 or more. The fresh
C2-prime (section 5) instantiates this structure with (d1,d2) = (3,2)
and spurious X delays (2,3); the v3-frozen binary's exhaustive
depth-8 scan certifies no shorter sequence exists (D2CERT logged in
calibration, section 5).

## 3. The v4 mechanism change: D2 = 9 (bound only)

The DPDS mechanism is UNCHANGED (prereg v3 sections 3.1-3.3, carried
over verbatim except the bound). The single change:

- `L_D2()` returns 9 instead of 8.
- Buffer capacities resized to fit depth-9 sequences (discrimination
  sequence buffers 8 -> 10 slots; discrimination ledger record
  reclen 48+nhyp -> 50+nhyp with 9 sequence slots). These are capacity
  consequences of the bound, not mechanism changes.
- No change to the pair-diff, the restricted alphabet, the
  exactly-one-OBSERVE rule, first-hit selection order, the standard
  depth-6 scan, candidate generation, the goal planner, the random
  control, or any world interface.

Why a constant bound, not adaptive depth: the task permits either; the
constant keeps the change minimal and auditable ("the mechanism stays
generic, only the depth bound changes"). A D2 certificate at depth 9
retains the bar's teeth: if a live pair needs 10+ primitives, K4-R4
fails honestly.

Why this is not a patch, a mode, a bridge, or a semantic case: the
v3 section 3.3 analysis carries over unchanged. The bound is set once,
from the depth-9 proof, not per world or per failure. No per-world
branch, no task-specific gate, no X-specific or delay-specific
knowledge in source.

## 4. Sealed worlds (frozen; hashes recorded before any v4 run)

### World A-prime: confounded chain (FRESH)

Fresh parameters (2021pdt World A retired as a test world, kept for
regression only): variables X=0, Z=1, Y=2, D=3; controllable X, D; no
context variables; true laws (X -> Z, delay 3), (Z -> Y, delay 2),
(X -> D, delay 1); passive 14 steps (t = 0..13) with X SET at t = 2, 7,
13 (unequal spacing, so no reversed rule reaches two firings: X has no
candidates and stays exogenous, keeping the true hypothesis unique);
goal: reach X = 1 AND Y = 1 AND D = 0; planner depths 1..8 over
{SET X, CLR X, SET D, CLR D, WAIT}; random control 20 sequences, length
plan_length + 2, a priori seed 12345, bar 0/20. Regression anchor.
File: f2v4_world_aprime.zag,
sha256 fe909a1cf633238c2ebf30e1ba75acfc2486b2c4fad5863779a7d932423a824a.

### World C2-prime: dual contextual delay (FRESH, sealed)

Fresh sealed world (2021pdt World C-prime retired as a test world, kept
for regression only). Family spec (v3 prereg section 5): variables X=0
(controllable pulse), Y1=1, Y2=2 (effects), J=3, K=4 (declared
persistent context variables, controllable); true laws (X -> Y1, delay
d1, J == j1) and (X -> Y2, delay d2, K == k1) with d1 != d2, d1,d2 in
1..4, j1,k1 in {0,1}; no law governs X (decays); passive at least 12
steps with at least 3 X pulses and constant J,K; goal setup J = 1 - j1,
K = 1 - k1 (both wrong); goalvar interface [Y1,Y2,J,K] with target
values [1,1,j1,k1]; sealed w_verify implementing the K4-R4 contract.
Fresh sealed specifics: (d1,d2) = (3,2), (j1,k1) = (1,1), npass = 18
(t = 0..17), X pulses at t = 3, 8, 13, J = 1 and K = 1 throughout
passive, setup J = 0, K = 0, goalvals [1,1,1,1]. The two worlds are not
variants of each other: confounded chain vs dual contextual delay are
different law families. File: sealed/f2v4_world_c2prime.zag,
sha256 6454ff33815f31d3509f258b4633de0ab007f0c66dd72cfe292e088fcbfd3d5f.

### Design provenance and seal discipline

The fresh worlds were designed by this worker from the frozen family
specs before this prereg was written; their hashes are recorded above
before any v4-learner run. The v4 learner is the v3 learner with only
the section-3 change, so it carries no world-specific content. The
anti-tuning evidence is: (i) the prereg (with hashes) is committed
before any v4 run; (ii) the v3-frozen (D2=8) binary was calibrated on
both fresh worlds BEFORE this prereg (non-vacuity certificate below);
it fails K4-R4 on C2-prime exactly as required, so C2-prime is a
genuine depth-9 test, not a world tuned for the new binary; (iii) the
v4 binary is verified on the retired 2021pdt worlds (regression only)
before the sealed runs, and its first run on C2-prime is the sealed
evaluation.

### Non-vacuity certificate (v3-frozen binary calibration, pre-prereg)

C2-prime (binary 44f800c7542cb9d0e930063b0786f072f89e26c734cdbfd42aa0594344c2d3e9):
1. Candidate generation under the generic rule yields X:6 [Y1->X d2
   (+ctx J=1,K=1); Y2->X d3 (+ctx J=1,K=1)], Y1:6, Y2:6 (each >= 2).
   NHYP = 216. The X-rule distinguishability bar is non-vacuous.
2. The v3-frozen loop terminates by exhaustion with SURVIVORS [80,82]
   (nalive = 2 >= 2): X-rules (Y1->X, d2, K==1) and (Y2->X, d3, J==1)
   sharing the true Y1/Y2 rules; D2CERT logged for the pair (full
   pair-restricted scan to depth 8, no disagreeing sequence). The v3
   failure mode reproduces: DPDS resolves 4 of 6 X-variants, the
   crossed-context pair needs depth 9 (section 2.1).
3. The sustained goal is achievable with len(M) = 9 <= 9:
   PLAN_C2 M=[SX,SJ,SK,W,SX,W,SX,W,SX], PLAN_AGREEMENT 1,
   GOAL_REAL_C2 1 (all twelve SUFFIX observations 1).
4. Random control 0/20 (a priori seed 12345, 7-symbol alphabet,
   length len(M)+17 = 26, semantic trajectory predicate).

A-prime (binary dbf81c9d7675a9b9c56782593cb6b3357c2a69d15dd8e414b43cdbff5253d190):
NHYP = 4 (X:0, Z:2, Y:2, D:1) >= 2; the v3 binary passes all bars
(PROGRAM_ALL_BARS_PASS, mask 63): true hypothesis survives, nalive=1;
PLAN [SX,W,W,W,W,W,SX], GOAL_REAL 1; RANDOM 0/20; OBS_USED 6. The
regression anchor is well-formed. (An earlier A-prime draft with X
pulses {2,7,12} gave X 2 spurious candidates whose surviving rule
corrupted the goal plan (GOAL_REAL 0); it was discarded and replaced
by the {2,7,13} schedule above. This is calibration, not tuning: the
anchor must be solvable.)

## 5. Harder sustained goal (carried over)

Unchanged from v3 prereg section 6 (C2' schema): the learner executes
its full plan (M + SUFFIX) for real exactly once; GOAL_REAL = 1 iff
the real trajectory contains three consecutive steps with every
goalvar at its goal value. Goal planner: iterative deepening over
{SET X, CLR X, SET J, CLR J, SET K, CLR K, WAIT}, depths 1..9,
lexicographic. SUFFIX: [OBS v for v in goalvars ascending, WAIT] x 3
(programmatically constructed). Random control: 20 sequences, frozen
LCG, a priori seed 12345, length len(M) + 17, 7-symbol alphabet,
semantic trajectory predicate, bar 0/20. World A-prime: final-state
goal X=1 AND Y=1 AND D=0 as in v3 section 5.

## 6. Learner architecture (v3 loop + D2=9; all else unchanged)

Identical to v3 prereg section 7 with D2 = 9 in step 4c/4d (DPDS
discrimination bound and D2 certificates). No other change.

## 7. Kill bars (numbered; frozen)

- K4-R1 (passive ambiguity): after the passive phase, at least 2
  hypotheses fully consistent with the passive trace, in EACH world.
  Fewer: FAIL.
- K4-R2 (construction, not enumeration): the source contains no finite
  list of complete experiments, distinguishing sequences, or goal plans
  (verified by source audit; construction is exclusively
  iterative-deepening composition over primitives, standard and
  pair-restricted, to the frozen bounds; SUFFIX is the preregistered
  programmatically constructed measurement protocol). The executed
  experiments AND goal plans differ across the two worlds in
  composition. A complete experiment, distinguishing sequence, or goal
  plan found as a literal in source (other than programmatic SUFFIX
  construction): FAIL.
- K4-R3 (disagreement-driven): every executed experiment is logged with
  predicted observation vectors showing disagreement (per-hypothesis for
  standard rounds, per-pair for discrimination rounds), and the
  world-action counter proves zero real-world actions during search
  (only RESET plus the single selected execution per round). The
  discrimination ledger is complete: every elimination is backed by a
  logged experiment. An executed experiment without logged prior
  disagreement, any world action during search, or a ledger gap: FAIL.
- K4-R4 (convergence): World A-prime: the true hypothesis
  {Z<-(X,3), Y<-(Z,2), D<-(X,1)} survives AND the loop terminates by
  exhaustion (no live pair distinguishable to D2=9). World C2-prime:
  the loop terminates with exactly one survivor, and the sealed
  w_verify confirms its Y1 rule equals (X, 3, J == 1) and its Y2 rule
  equals (X, 2, K == 1). (On A-prime DPDS may legitimately resolve a
  pair; freezing a nalive count would punish the mechanism for
  working.) Otherwise: FAIL.
- K4-R4b (pairwise distinguishability): (i) every hypothesis eliminated
  in the discrimination phase contradicted the actual observation vector
  of a logged distinguishing sequence; (ii) at termination, every live
  pair carries a logged D2 certificate (full pair-restricted scan to
  depth 9 found no disagreeing sequence). On C2-prime this bar plus
  K4-R4 means the X-rule equivalence class was resolved by
  learner-discovered evidence, not exhausted as an indistinguishable
  class. Otherwise: FAIL.
- K4-R5 (model to goal): World A-prime: the planned sequence achieves
  the goal for real, verified by OBSERVE; AND the random-action control
  achieves the goal 0/20. World C2-prime: the full plan (M + SUFFIX)
  achieves the sustained triple predicate for real; AND the
  random-action control (7-symbol alphabet, length len(M) + 17, a priori
  seed 12345) achieves the predicate 0/20. Otherwise: FAIL.
- K4-R6 (observation economy): total active-phase OBSERVE actions across
  BOTH worlds is at most 32 (v3 used 25; each discrimination experiment
  costs exactly 1 by the frozen exactly-one-OBSERVE rule; the headroom
  covers the C2-prime discrimination rounds at the deeper bound).
  Passive observations are free given data. More: FAIL.
- K4-R7 (determinism and purity): 3/3 runs byte-identical per world;
  pure Zag (no Python at any stage, including analysis and artifact
  handling; safebin toolchain guard in NAMECHECK.md Step 0); no em
  dashes in wave documentation. Otherwise: FAIL.

BUILD-PASS requires all eight bars in both worlds. Any FAIL is
BUILD-FAIL. No promotion claims (promotion pipeline steps 4-11 remain
for the parent to schedule).

## 8. Negative controls (frozen)

- NC1 (random-action control): identical to K4-R5's control (kill bar).
- NC2 (memorization control; reported, not kill): as v3 prereg section
  9 (longest-suffix replay baseline, no causal model). Expected: fails
  the sustained predicate. Rationale: separates storing traces (L0)
  from learning laws (L2).
- NC3-prime (mechanism ablation; reported, not kill): the v3-frozen
  loop (D2=8) executed against C2-prime. Already run in calibration
  (section 4): terminates with nalive=2 (SURVIVORS [80,82]),
  reproducing the v3 failure mode. Rationale: attributes any C2-prime
  resolution to the depth-bound change rather than to the fresh world
  being easier. If the v4 run also stalls above nalive=1, the
  comparison is reported as uninformative about the bound.

## 9. Determinism standard

3/3 byte-identical reruns per world (cmp-verified; the v3 wave's
sha256sum EOF quirk is noted and cmp is the definitive check). Zero
randomness in decision paths: no RNG in the learner; the only
stochastic element is the random-action control (frozen fixed-seed
LCG, no feedback into decisions). Pair order, alphabet orders, and
first-hit selection are frozen, so the discrimination phase is fully
deterministic.

## 10. Honest boundaries (what BUILD-PASS would and would not establish)

A BUILD-PASS would establish: the F2 loop with DPDS at D2=9 achieves
sustained dual contextual control on a fresh sealed world it never
saw, and resolves the full X-rule equivalence class including the
depth-9 crossed-context pair by learner-discovered distinguishing
evidence with a complete elimination trail. That is bounded L2
structural learning. DPDS remains bounded-effective, not complete:
the bound is 9, not infinity, and a future pair needing 10+
primitives would fail K4-R4 honestly.

It would NOT establish, and no claim to the contrary may be made:

- L3 representational invention. Against Criterion 0: (C0-A) FAILS, the
  rule semantics (cause/effect/delay/context) are researcher-authored
  and the learner fills in edges, delays, and contexts; (C0-B) FAILS,
  the solution space (rule sets over a researcher-fixed alphabet) is
  researcher-enumerated and the loop is enumerate-then-select;
  (C0-C) is NOT TESTED (two worlds, one law family each, mechanism
  frozen throughout); (C0-D) is only partially met (the learned model
  is reused for goal planning within the wave).
- Generality beyond the tested worlds. Even a full pass is a targeted
  result on two sealed worlds, not a broad capability claim (the same
  discipline as the FW1-FW9 regression-battery ruling).
- Escape from the enumerate-then-select family. DDES remains the lane
  that escapes it; F2 does not.

## 11. Governance

Pure Zag only. No Python anywhere in this wave (implementation, build,
execution, analysis, artifact handling). This prereg is frozen before
any implementation file exists; the coordinator commits it alone first
(commit-order self-check: prereg commit strictly precedes the
implementation commit). Commits local on tnn-native-lab; nothing is
pushed. The builder reports BUILD-PASS or BUILD-FAIL only, with the
exact frozen bars named; no SURVIVES claim. Implementation files may be
written only after the coordinator authorizes the build phase.

## 12. Architecture accounting (prereg step)

- Cognition source lines added: 0 (writing-only step; no
  implementation). Builder target: the section-3 change only
  (L_D2 constant 8 -> 9 plus buffer-capacity resizes); builder reports
  the exact diff line count.
- New hardcoded semantic cases: 0.
- New modes / bridges / routers: 0.
- New task-specific handlers: 0.
- New learner-state structures: 0 (the discrimination ledger is
  carried over from v3; only its record capacity changes).
- The sealed worlds are authored test substrate, not cognition.
