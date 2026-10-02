# PREREG_F2V3: Autonomous Scientist with X-Rule Distinguishability on Fresh Sealed Worlds

Date: 2026-10-01. Status: FROZEN. This prereg is written before any
implementation file for this wave exists. No `.zag` for F2 v3 exists at
freeze time. The coordinator must commit this prereg alone before any
implementation file exists; the commit-order self-check (prereg commit
strictly precedes the implementation commit) applies. UNVERIFIABLE
ORDERING voids this prereg.

Lane: F2v3 (wave-20261001-2021pdt). Governance: pure Zag only (safebin;
Step 0 recorded in NAMECHECK.md). No em dashes in wave documentation.

## 1. Objective

Test the F2 autonomous-scientist loop (hypotheses from passive data,
disagreement-driven experiment construction from primitives, elimination,
model-based goal planning) augmented with ONE generic mechanism change
(section 3) against FRESH sealed worlds, with the harder sustained goal
carried over from v1/v2 AND a new frozen distinguishability bar. The v2
BUILD-FAIL was a convergence failure (K3-R4: nalive=4 X-rule equivalence
class in World C), not a goal failure (GOAL_REAL_C2=1) and not a loop
malfunction. v3 must keep the harder sustained goal and additionally
resolve X-rule variants by learner-discovered evidence.

## 2. Prior history and re-derived failure analysis (read first)

- F2 v1 (autosci, prereg 2a87efa77, result 4ebde580a, 2026-09-30):
  BUILD-FAIL on K-AS5b. The loop worked in both sealed worlds. World B's
  goal (transient Y=1 within 6 steps, ~5% random base rate) was a weak
  goal instance that the frozen random control hit 1/20 on seed 12345.
  Bar failure on a weak goal, not loop failure.
- F2 retry (autosci2, prereg b9ab0acb6, result 2026-09-30): harder World B
  goal B2 (three consecutive steps with Y=1 AND K=0; 0/160 random
  pre-freeze) achieved BUILD-PASS on all seven bars with no architectural
  changes. Memorization control and independent reproduction later closed.
- F2 v2 (prereg df0c7ed64, wave-20261001-1721pdt): the next harder step
  (two independent contextual laws, delays 2 and 3 simultaneously, two
  persistent context variables both actively verified, fresh sealed World
  C). Result: BUILD-FAIL on K3-R4 in World C; all other bars passed in
  both worlds. The goal succeeded for real (GOAL_REAL_C2=1, control
  0/20). The failure is re-derived below from the frozen logs, not cited
  from memory.

### 2.1 What the X-rule equivalence class is

World C sealed physics (v2, now retired as a test world): variables
X=0, Y1=1, Y2=2, J=3, K=4; controllable X, J, K; J, K persistent
(declared context variables, change only via SET/CLR); true laws
(X -> Y1, delay 2, J == 0) and (X -> Y2, delay 3, K == 1); X has no
governing law (X decays to 0 unless SET at the current step); passive
14 steps with environment X pulses at t = 2, 6, 10 and J = 0, K = 1
throughout.

Candidate generation (generic rule, unchanged): for each effect variable
e, each cause c != e, each delay 1..4, each world context: keep the rule
if sufficient on the passive trace and fired at least twice. Persistent
J, K are skipped as effects (disclosed physics). X remains a candidate
effect. Runtime counts: X: 6, Y1: 6, Y2: 6, hence 216 hypotheses.

The 6 X candidates were:
[Y1->X d2; Y1->X d2 ctx J=0; Y1->X d2 ctx K=1;
 Y2->X d1; Y2->X d1 ctx J=0; Y2->X d1 ctx K=1].
These are spurious correlations induced by the environment's X-pulse
schedule: X=1 at t = 2, 6, 10 coincides with Y1=1 at t = 4, 8, 12 and
Y2=1 at t = 5, 9, 13 on the passive trace, so reversed rules with the
right delays are sufficient there.

The standard experiment loop (iterative deepening depths 1..6,
disagreement-driven) ran 5 rounds and correctly pinned both true laws:
rounds 1-4 eliminated all spurious Y1/Y2 rules (nalive 216 -> 72 ->
36 -> 12 -> 6), leaving Y1 = (X,2,J=0) and Y2 = (X,3,K=1) (true_h=83
alive). Round 5 ([SX,W,W,W,W,OX], actual [0]) killed X rules (Y1,2,ALWAYS)
and (Y1,2,J=0) via X decay. Survivors [80, 81, 82, 83] share the TRUE
Y1/Y2 rules and differ ONLY in the X rule:
(Y1,2,K=1), (Y2,1,ALWAYS), (Y2,1,J=0), (Y2,1,K=1).

### 2.2 What nalive counts and why depth 6 could not distinguish the survivors

nalive = the number of live (not yet eliminated) hypotheses. K3-R4
required exactly one survivor equal to the true law pair; nalive = 4
violated it.

Round 6 ran the full depth-6 scan and found zero disagreeing sequences
among the four survivors, so the loop terminated by exhaustion. The
blindness is structural, verified by hand: distinguishing any survivor
pair requires arranging a cause (Y1 or Y2 equal to 1) at the right delay
before an X observation while holding the pair's differing context
(J/K) at the observation step. Concretely:
- (Y1,2,K=1) vs (Y2,1,J=0): [SX,W,W,W,W,SK,OX] (7 primitives; actual [0]
  kills (Y1,2,K=1), which predicts 1 from Y1=1 at t=2 with K=1 at t=6).
- (Y1,2,K=1) vs (Y2,1,ALWAYS): [SJ,SK,SX,W,W,W,W,OX] (8 primitives;
  actual [0] kills (Y2,1,ALWAYS), which predicts 1 from Y2=1 at t=3).
Every distinguishing sequence needs a J/K manipulation plus an X
observation positioned at least 4 steps after the arranged cause, hence
at least 7 primitives. The frozen depth-6 bound is provably blind to
this discrimination class; the exhaustion was not bad luck. The goal
phase then succeeded because the sustained goal depends only on Y1/Y2,
which were correct.

## 3. The v3 mechanism change: discrimination-phase pairwise deep search (DPDS)

### 3.1 Specification (frozen)

The standard experiment loop is unchanged (section 8). DPDS is a
continuation of the same select-execute-eliminate loop, fired only when
the standard depth 1..6 full-alphabet scan finds no disagreeing sequence
AND nalive > 1:

1. Enumerate all unordered pairs (i, j) of live hypotheses, ascending
   index order.
2. For each pair, compute D(i, j): the set of variables whose governing
   rule (cause, delay, context) differs between h_i and h_j. This is a
   generic structural diff over hypothesis rule-set data, computed at
   runtime. (On the v2 instance every survivor pair yields D = {X}; the
   source contains no such fact.)
3. Restricted alphabet: all manipulations (SET v, CLR v per controllable
   in w_ctrl order), WAIT, plus OBSERVE v for v in D(i, j) (ascending
   variable index). Nothing else.
4. Iterative deepening over depths 1..8 (revised bound D2 = 8, see 3.2)
   over the restricted alphabet. Sequences must contain exactly one
   OBSERVE. Select the first sequence (depths ascending, lexicographic
   within depth) where the pair's predicted observation vectors
   disagree.
5. Scan pairs in order; the first pair yielding a distinguishing
   sequence determines the executed experiment. Log the pair, the
   sequence, and both predicted vectors.
6. RESET; execute the selected sequence exactly once; record actual
   observations; eliminate EVERY live hypothesis whose prediction
   contradicts actual (not only the pair). Append to the discrimination
   ledger (section 4): (round, pair, sequence, pred_i, pred_j, actual,
   killed[]).
7. Repeat from the standard scan. Terminate when nalive == 1, or when a
   full pass over all live pairs finds no distinguishing sequence to
   depth 8 (exhaustion; log a D2 certificate per pair).

Completeness note (frozen justification for the restriction): any
sequence distinguishing h_i from h_j over the full alphabet must contain
a disagreeing observation; observations of variables outside D(i, j)
agree under both hypotheses (all other rules are shared); OBSERVE is
state-neutral, so dropping non-D observations preserves the
disagreement. The restriction therefore loses no distinguishing
sequence within the bound.

### 3.2 Depth bound revision and its justification

The standard bound stays 6 (efficiency: the full 12-symbol alphabet at
depth 8 is ~4.3e8 sequences per scan, infeasible). The discrimination
bound is revised to D2 = 8 because:
(a) section 2.2 proves the X-variant discrimination class needs at
least 7 primitives, so bound 6 is provably blind and bound 8 covers the
witnessed class with one spare depth;
(b) the pair-restricted alphabet (at most 8 symbols: 6 manipulations +
WAIT + OBS of differing variables) makes depth 8 feasible (worst case
~1.7e7 sequences per pair scan; first-hit selection stops far earlier in
practice);
(c) the revision is made once, from analysis, not per world or per
failure. If a live pair needs 9+ primitives, the D2 certificate honestly
reports indistinguishability and K4-R4 fails; the bar has teeth.

### 3.3 Why this is not a patch, a mode, a bridge, or a semantic case

No-patch-treadmill analysis (three structurally different hypotheses
were considered for the bottleneck "fixed depth-6 search is provably
blind to >=7-primitive discriminations"):
(a) raise the global bound to 8: rejected as computationally infeasible
(see 3.2);
(b) exclude X as a candidate effect by researcher filter: rejected, this
would be a hardcoded semantic case smuggled into candidate generation
and would make the distinguishability bar vacuous;
(c) DPDS: chosen. It addresses the shared architectural cause (search
bound blindness) with a general mechanism: the pair-diff is computed
from hypothesis data at runtime, the sequences are discovered by
enumeration, and the identical code path applies to World A and to any
future world. There is no per-world branch, no task-specific admission
gate, no new subsystem, and no X-specific, delay-specific, or
context-specific knowledge in source. It is a continuation of the one
existing loop, not a new mode.

## 4. Distinguishability requirement and learner-created evidence

Distinguishability requirement (frozen): at loop termination on World C',
no live pair may be distinguishable within bound D2 = 8; every
elimination in the discrimination phase must be backed by a logged
distinguishing experiment; every live pair at termination must carry a
logged D2 certificate. Together with the exact-count bar (K4-R4) this
forces the X-rule equivalence class to be resolved by evidence, never
exhausted as an indistinguishable class.

The exact distinguishing evidence the mechanism uses: for each survivor
pair, a distinguishing sequence discovered by the learner's own search
(manipulations + WAITs + exactly one OBSERVE of a differing variable),
e.g. on the v2 instance the mechanism would discover [SX,W,W,W,W,SK,OX]
and [SJ,SK,SX,W,W,W,W,OX]; the executed actual observation vector (e.g.
[0]); and the contradiction between the actual vector and the spurious
X-rule's predicted vector (e.g. [1]). The sequence lengths (7, 8), the
variable choices, and the pair order appear nowhere in source.

This evidence lives in learner-created persistent state: the
discrimination ledger is allocated and appended by the learner at
runtime, persists across search rounds within the run, and its entries
(which pairs, which sequences, which outcomes) depend entirely on the
sealed world's responses. The source contains only the generic pair-diff,
the restricted-alphabet enumeration, and the ledger-append operations.
No researcher-supplied semantic case is involved at any point.

## 5. Sealed worlds (frozen family specs; C' designed post-freeze)

### World A: confounded chain (RETAINED EXACTLY)

Replicated exactly from F2/AUTOSCI2/v2: variables X=0, Z=1, Y=2, D=3;
controllable X, D; no context variables; true laws (X -> Z, delay 2,
ALWAYS), (Z -> Y, delay 1, ALWAYS), (X -> D, delay 1, ALWAYS); passive 12
steps with X SET at t = 2, 8; goal: reach X = 1 AND Y = 1 AND D = 0;
planner depths 1..8 over {SET X, CLR X, SET D, CLR D, WAIT}; random
control 20 sequences, length plan_length + 2, seed 12345, bar 0/20.
Regression anchor. DPDS applies to World A through the identical generic
code path (its outcome there is not frozen; see K4-R4).

### World C': dual contextual delay (FRESH; post-freeze independent adversary)

The v2 World C is RETIRED as a test world: its sealed laws are published
in the v2 build record, so reuse would permit tuning to it. World C' is
designed post-freeze by an independent adversary (not the implementer;
no access to implementer source) within this frozen family spec:

- Variables: X=0 (controllable pulse variable), Y1=1, Y2=2 (effects),
  J=3, K=4 (declared persistent context variables, controllable).
- True laws (adversary-chosen, sealed): (X -> Y1, delay d1, J == j1) and
  (X -> Y2, delay d2, K == k1), with d1 != d2, d1,d2 in 1..4, j1,k1 in
  {0,1}. No law governs X (X decays).
- Passive schedule (adversary-chosen): at least 12 steps, at least 3
  environment X pulses, J and K constant throughout.
- Goal setup (disclosed schema): environment establishes J = 1 - j1 and
  K = 1 - k1 (both gating contexts WRONG), then RESET to t = 0. The
  learner must discover both gates and flip both.
- Interface: the v2 w_* interface plus w_ngoalvars(), w_goalvar(i),
  w_goalval(i) declaring the sustained predicate's variables and target
  values (generic; keeps the learner world-agnostic). The adversary also
  provides the sealed w_verify implementing the K4-R4 contract.
- The two worlds are not variants of each other: confounded chain vs
  dual contextual delay are different law families.

Adversary non-vacuity certificate (verified pre-delivery with a scratch
calibration program, delivered to the coordinator):
1. Candidate generation under the v3 generic rule yields at least 2
   candidates for X, at least 2 for Y1, at least 2 for Y2 (the X-rule
   distinguishability bar is non-vacuous).
2. The v2-frozen loop (standard depth-6 search only, no DPDS) terminates
   with nalive >= 2 (the X-variant failure mode reproduces).
3. The sustained goal is achievable with len(M) <= 9 (witness disclosed
   to the coordinator under seal, never to the implementer).
4. Random control 0/160 across 8 seeds (12345 plus 7 adversary-chosen)
   with the frozen LCG, 7-symbol alphabet, length len(M)+17, semantic
   trajectory predicate.
The coordinator runs the frozen learner binary against C' under seal;
the implementer never sees C' laws or schedule before the sealed run.

## 6. Harder sustained goal (carried over from v1/v2)

v1 BUILD-FAILed on a weak goal (transient, ~5% random base rate, control
hit 1/20). v2 met the harder sustained goal (three consecutive joint
steps, 0/160 random) but missed K3-R4. v3 keeps the same hardness class
on the fresh world AND must pass the distinguishability bar, so v3 is
strictly harder than v2.

Goal C2' (frozen schema): the learner executes its full plan (M +
SUFFIX) for real exactly once. GOAL_REAL = 1 iff the real trajectory
contains three consecutive steps s, s+1, s+2 such that at each step every
goalvar equals its goal value (for the v2 instance: Y1 = 1, J = 0,
Y2 = 1, K = 1). Rationale (unchanged): the learner must discover both
gating contexts, flip both, manage two different delays simultaneously by
re-asserting X at the correct cadence, and hold both contexts across
three steps; a lucky transient firing cannot satisfy three consecutive
joint observations.

Goal planner (C2'): iterative deepening over {SET X, CLR X, SET J, CLR J,
SET K, CLR K, WAIT} (7 symbols; derived generically from the
controllable set), depths 1..9, lexicographic order (symbol order as
listed; depths ascending). For each M, simulate M followed by 3 WAITs
under the first surviving hypothesis (pure simulation, zero world
calls); the 3 WAITs are trajectory-equivalent to the SUFFIX observation
rounds because OBSERVE is state-neutral (disclosed here). Select the
first M (shortest depth, lexicographic) whose simulated trajectory
contains three consecutive predicate-satisfying steps. The full executed
plan is M + SUFFIX.

SUFFIX (fixed measurement protocol, disclosed, constructed
programmatically, no literal): [OBS v for v in goalvars ascending, WAIT]
repeated 3 times (for the v2 instance this is exactly [OBS Y1, OBS J,
OBS Y2, OBS K, WAIT] x 3). Contains no manipulations.

Random control (C2'): 20 sequences from the fixed-seed LCG
(deterministic, a priori seed 12345, multiplier 1103515245, mod 2^31,
disclosed), each of length len(M) + 17 over the 7-symbol manipulation
alphabet. Executed for real with RESET and goal setup. Count sequences
whose real trajectory contains three consecutive predicate-satisfying
steps (semantic predicate: cause, not observe; the most generous fair
reading). Bar: 0/20.

## 7. Learner architecture (v2 loop + DPDS delta; all else unchanged)

1. Passive phase: record the passive trace (world-declared length).
2. Candidate generation: generic rule (for each effect variable e, each
   cause c != e, each delay 1..4, each world context; sufficiency on the
   passive trace and at least two firings; declared persistent variables
   skipped as effects per disclosed physics). No other filter.
3. Hypotheses: cross product of one candidate rule per variable that has
   at least one candidate; variables with none are exogenous. Hypotheses
   are data (rule sets). No per-hypothesis code.
4. Experiment loop (per round):
   a. Standard scan: iterative deepening depths 1..6 over the full
      primitive alphabet (SET/CLR per controllable, WAIT, OBSERVE per
      variable); skip sequences with no OBSERVE; simulate under every
      live hypothesis (zero world calls); select the first lexicographic
      sequence with disagreeing predicted observation vectors.
   b. If found: log predictions, check budget, RESET, execute once,
      eliminate contradicting hypotheses. If zero remain: FAIL. If one
      remains: stop.
   c. If not found and nalive > 1: DPDS pass per section 3 (pairs
      ascending, restricted alphabet, depths 1..8, exactly one
      OBSERVE); execute the first distinguishing sequence found;
      eliminate; append to the discrimination ledger.
   d. If not found and (nalive == 1, or DPDS pass finds nothing):
      stop (exhaustion; log D2 certificates per live pair).
5. Goal phase: World A as in v2; World C' per section 6.
6. Random-action control per section 6 (World C') and section 5
   (World A).

## 8. Kill bars (numbered; frozen)

- K4-R1 (passive ambiguity): after the passive phase, at least 2
  hypotheses fully consistent with the passive trace, in EACH world.
  Fewer: FAIL.
- K4-R2 (construction, not enumeration): the source contains no finite
  list of complete experiments, distinguishing sequences, or goal plans
  (verified by source audit; construction is exclusively
  iterative-deepening composition over primitives, standard and
  pair-restricted; SUFFIX is the preregistered programmatically
  constructed measurement protocol). The executed experiments AND goal
  plans differ across the two worlds in composition. A complete
  experiment, distinguishing sequence, or goal plan found as a literal
  in source (other than programmatic SUFFIX construction): FAIL.
- K4-R3 (disagreement-driven): every executed experiment is logged with
  predicted observation vectors showing disagreement (per-hypothesis for
  standard rounds, per-pair for discrimination rounds), and the
  world-action counter proves zero real-world actions during search
  (only RESET plus the single selected execution per round). The
  discrimination ledger is complete: every elimination is backed by a
  logged experiment. An executed experiment without logged prior
  disagreement, any world action during search, or a ledger gap: FAIL.
- K4-R4 (convergence; restated K3-R4 class): World A: the true
  hypothesis {Z<-(X,2), Y<-(Z,1), D<-(X,1)} survives AND the loop
  terminates by exhaustion (no live pair distinguishable to D2).
  World C': the loop terminates with exactly one survivor, and the
  sealed w_verify confirms its Y1 rule equals (X, d1, J == j1) and its
  Y2 rule equals (X, d2, K == k1). (No frozen nalive count for World A:
  DPDS may legitimately resolve its pair; freezing the v2 count would
  punish the mechanism for working.) Otherwise: FAIL.
- K4-R4b (pairwise distinguishability): (i) every hypothesis eliminated
  in the discrimination phase contradicted the actual observation vector
  of a logged distinguishing sequence; (ii) at termination, every live
  pair carries a logged D2 certificate (full pair-restricted scan to
  depth 8 found no disagreeing sequence). On World C' this bar plus
  K4-R4 means the X-rule equivalence class was resolved by
  learner-discovered evidence, not exhausted as an indistinguishable
  class. Otherwise: FAIL.
- K4-R5 (model to goal): World A: the planned sequence achieves Goal A
  for real, verified by OBSERVE; AND the random-action control achieves
  Goal A 0/20. World C': the full plan (M + SUFFIX) achieves the
  sustained triple predicate for real; AND the random-action control
  (7-symbol alphabet, length len(M) + 17, a priori seed 12345) achieves
  the predicate 0/20. Otherwise: FAIL.
- K4-R6 (observation economy): total active-phase OBSERVE actions across
  BOTH worlds is at most 32 (v2 used 23; each discrimination experiment
  costs exactly 1 by the frozen exactly-one-OBSERVE rule; the headroom
  covers the C' discrimination rounds). Passive observations are free
  given data. More: FAIL.
- K4-R7 (determinism and purity): 3/3 runs byte-identical per world;
  pure Zag (no Python at any stage, including analysis and artifact
  handling; safebin toolchain guard in NAMECHECK.md Step 0); no em
  dashes in wave documentation. Otherwise: FAIL.

BUILD-PASS requires all eight bars in both worlds. Any FAIL is
BUILD-FAIL. No promotion claims (promotion pipeline steps 4-11 remain
for the parent to schedule).

## 9. Negative controls (frozen)

- NC1 (random-action control): identical to K4-R5's control (kill bar).
- NC2 (memorization control; reported, not kill): a baseline planner
  that stores the passive trace and all executed experiment trajectories
  and acts by longest-suffix replay of memorized goalvar observation
  histories (WAIT on no match); no causal model, no simulation under
  hypotheses. Expected: fails the sustained predicate (0/1). Reported
  honestly. Rationale: separates storing traces (L0) from learning laws
  (L2); if replay succeeded, the goal would not evidence structural
  learning.
- NC3 (mechanism ablation; reported, not kill): the v2-frozen loop
  (standard depth-6 search only, no DPDS) executed against World C'.
  Expected: terminates with nalive >= 2 (X-variant equivalence class
  intact), reproducing the v2 failure mode. Reported honestly. Rationale:
  attributes any C' resolution to the DPDS mechanism rather than to the
  fresh world being easier. If the ablation also reaches nalive = 1, the
  control is reported as uninformative and the distinguishability claim
  is weakened accordingly.

## 10. Determinism standard

3/3 byte-identical reruns per world (sha256 recorded). Zero randomness
in decision paths: no RNG in the learner; the only stochastic element
is the random-action control, which uses the frozen fixed-seed LCG and
does not feed back into any decision. Pair order, alphabet orders, and
first-hit selection are frozen above, so the discrimination phase is
fully deterministic.

## 11. Design calculations (pre-freeze; analysis only, not implementation)

On the retired v2 World C instance, hand-verified distinguishing
witnesses (these sequences must NOT appear as literals in source;
K4-R2 audit covers this):
- [SX,W,W,W,W,SK,OX] (7 primitives): distinguishes (Y1,2,K=1) from
  (Y2,1,J=0); actual [0] kills the former.
- [SJ,SK,SX,W,W,W,W,OX] (8 primitives): distinguishes (Y1,2,K=1) from
  (Y2,1,ALWAYS); actual [0] kills the latter.
These witnesses justify D2 = 8 (section 3.2). The adversary's World C'
will differ in the sealed specifics; the witnesses are not reused.

## 12. Honest boundaries (what BUILD-PASS would and would not establish)

A BUILD-PASS would establish: the F2 loop with the generic DPDS
discrimination mechanism achieves sustained dual contextual control on a
fresh sealed world it never saw, and resolves X-rule variants by
learner-discovered distinguishing evidence with a complete elimination
trail. That is bounded L2 structural learning.

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

## 13. Governance

Pure Zag only. No Python anywhere in this wave (implementation, build,
execution, analysis, artifact handling). This prereg is frozen before
any implementation file exists; the coordinator commits it alone first
(commit-order self-check: prereg commit strictly precedes the
implementation commit). Commits local on tnn-native-lab; nothing is
pushed. The builder reports BUILD-PASS or BUILD-FAIL only, with the
exact frozen bars named; no SURVIVES claim. Implementation files may be
written only after the coordinator authorizes the build phase.

## 14. Architecture accounting (prereg step)

- Cognition source lines added: 0 (writing-only step; no
  implementation). Builder target: DPDS confined to the experiment
  loop (pair-diff, restricted-alphabet search, discrimination ledger),
  fewer than 120 added learner lines; builder reports the exact count.
- New hardcoded semantic cases: 0.
- New modes / bridges / routers: 0 (section 3.3).
- New task-specific handlers: 0.
- New learner-state structures: 1 planned (discrimination ledger;
  learner-created persistent state, section 4).
- The sealed worlds are authored test substrate, not cognition.
  Persistence of context variables and the goalvar interface are generic
  properties of the declared world interface, not per-world special
  cases.
