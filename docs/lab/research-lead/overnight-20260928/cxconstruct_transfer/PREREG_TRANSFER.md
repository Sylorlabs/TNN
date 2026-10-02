# PREREG: H-CAUSALEXP-CONSTRUCT Transfer/Reuse (cxconstruct_transfer)

Date: 2026-09-30.
Status: FROZEN. Committed before any implementation, build, or run.
Lane: causal frontier, step 9 of 11-step promotion pipeline.

## 1. Objective

H-CAUSALEXP-CONSTRUCT is BUILD-PASS (7/7), REPRODUCED, BASELINE-LOSES
(step 5). A1/A2 attacks killed the L3 construction claim: the learner
is bounded L2, enumerating a researcher-bounded finite family (1364
sequences) and applying a disagreement filter. Researcher owns:
primitive set, enumeration order, depth bound. Learner owns:
disagreement filter only.

Step 9 asks: is there any reusable cognitive structure here, or is it
a one-trick pony? Specifically, does the disagreement-filter principle
(enumerate candidates, simulate under competing hypotheses, select by
predicted disagreement) transfer to new settings, or is it tied to the
specific delay-rule setup?

This prereg defines four transfer tests and freezes the verdict
criteria.

## 2. Transfer tests (frozen)

### T1: New primitive set (6 primitives, base-6 enumeration)

The original uses 4 primitives (S,W,OY,OZ) with base-4 enumeration.
T1 adds two primitives:
- R: reset X:=0 (records t_X := -1, clears X).
- OX: observe X (returns 0/1; changes nothing).

The enumeration must become base-6. Total sequences depths 1-5:
6+36+216+1296+7776 = 9330.

Test world W-T1:
- H-T1a: [(X,Z,2),(Z,Y,0)] with X-persistence: once X=1, it stays 1.
- H-T1b: [(X,Z,2),(Z,Y,0)] with X-decay: X returns to 0 after 1 tick
  unless re-set. (Implemented as: on W, if t - t_X >= 1 then X:=0.)

Discriminating sequence: [S,W,OX]. H-T1a predicts X=1 (persists).
H-T1b predicts X=0 (decayed). DISAGREE.

With only the original 4 primitives, no sequence can observe X
directly, so the learner MUST use OX. This tests whether the
enumeration machinery is parameterized by primitive count or hardcoded
to base-4.

Success: learner constructs [S,W,OX] (or another OX-containing
discriminating sequence) with 1 real-world execution, survivor is true
hypothesis.

### T2: New hypothesis form (threshold rules, not delay rules)

The original uses delay rules: (src,dst,delay). T2 uses threshold
rules: (src1,src2,dst,threshold) meaning dst:=1 iff src1+src2 >=
threshold, evaluated on W.

Primitives for T2:
- S: set X:=1.
- T: set Z:=1.
- W: evaluate all threshold rules once.
- OY: observe Y.

Test world W-T2:
- H-T2a: [(X,Z,Y,2)] (Y=1 iff X+Z >= 2; AND).
- H-T2b: [(X,Z,Y,1)] (Y=1 iff X+Z >= 1; OR).

Discriminating sequence: [S,W,OY]. Set X=1, Z=0. H-T2a: 1+0=1 < 2,
predicts 0. H-T2b: 1+0=1 >= 1, predicts 1. DISAGREE.

The simulator must handle threshold semantics, not delay semantics.
The enumerate-filter-select loop is unchanged. This tests whether the
principle transfers to different rule semantics.

Success: learner constructs [S,W,OY] (or another discriminating
sequence) with 1 real-world execution, survivor is true hypothesis.

### T3: New domain (concept learning, not causal experiments)

The original is sequential causal experiments. T3 is static concept
learning. This tests the abstract principle in a non-sequential,
non-causal domain.

Objects: 2 colors {red,blue} x 2 shapes {round,square} = 4 objects.
Encoded as (color,shape) with color: 0=red,1=blue; shape: 0=round,1=square.

Hypotheses:
- H-T3a: "red things are heavy": heavy=1 iff color=0.
- H-T3b: "round things are heavy": heavy=1 iff shape=0.

Candidates: the 4 objects, enumerated in fixed order:
(red,round), (red,square), (blue,round), (blue,square).

Simulation: for each object, predict heavy? under each hypothesis.
- (red,round): H-T3a=1, H-T3b=1. Agree.
- (red,square): H-T3a=1, H-T3b=0. DISAGREE.
- (blue,round): H-T3a=0, H-T3b=1. DISAGREE.
- (blue,square): H-T3a=0, H-T3b=0. Agree.

Selection: first object with disagreeing predictions: (red,square).

This is NOT a sequence. There is no temporal order, no simulation
steps. The "enumerate candidates, predict under hypotheses, select by
disagreement" principle is applied to a static set.

Success: learner selects (red,square) (first disagreeing in order),
with 1 real-world test (weigh the object), survivor is true hypothesis.

### T4: Composition (reuse of partial solutions)

The original learner enumerates from scratch for each world. T4 tests
whether it can reuse a previously found solution as a building block.

Setup:
- Phase 1: Solve World A (as in original): constructs [S,W,OY].
- Phase 2: Present World A2, which is World A with an additional
  requirement: the discriminating sequence must end with OZ (not OY),
  and the hypotheses differ on Z (not Y).
  - H-A2a: [(X,Z,2)] (Z follows X with delay 2; Y never changes).
  - H-A2b: [(X,Z,5)] (Z follows X with delay 5; Y never changes).
  - Discriminating: [S,W,W,OZ]. H-A2a: t=2, 2>=2, Z=1. H-A2b: t=2,
    2<5, Z=0. DISAGREE.

The compositional opportunity: [S,W] is a useful prefix (sets up X
and advances time). A compositional learner would reuse [S,W] and only
search for the suffix. The original learner enumerates all sequences
from scratch.

We test TWO variants:
- T4a (from-scratch): Learner enumerates all sequences depths 1-5,
  finds [S,W,W,OZ]. This should work (same as original).
- T4b (compositional): Learner is given [S,W] as a macro primitive M
  (in addition to S,W,OY,OZ). It should find [M,W,OZ] at depth 3
  instead of [S,W,W,OZ] at depth 4. This tests if the machinery can
  exploit a provided abstraction.

Success for T4a: finds [S,W,W,OZ], 1 execution, correct survivor.
Success for T4b: finds [M,W,OZ] (or [S,W,W,OZ]), 1 execution, correct
survivor. The key measure is whether T4b is faster (fewer checked
sequences) than T4a, demonstrating reuse has value.

## 3. What counts as "transfer" (frozen definitions)

- DATA CHANGE: New primitive definitions, new rule sets, new object
  encodings, new hypothesis pairs. The core enumerate-simulate-filter
  loop is unchanged.
- ALGORITHM CHANGE: Modifying the enumeration logic, the selection
  criterion, or the core loop structure.

- T1: Requires DATA CHANGE only (add R,OX to primitive list; the
  base should parameterize automatically). If the code has base-4
  hardcoded and must be edited to base-6, that is an ALGORITHM CHANGE
  and T1 is PARTIAL, not PASS.
- T2: Requires a new simulator (threshold vs delay). The
  enumerate-filter-select loop is unchanged. This is a DATA CHANGE
  for the loop, ALGORITHM CHANGE for the simulator. T2 PASS if the
  loop transfers without modification.
- T3: Requires a new "simulator" (concept evaluator). The loop is
  unchanged. Same as T2: PASS if loop transfers.
- T4a: Should work identically to original. PASS if it does.
- T4b: Tests if providing a macro helps. PASS if [M,W,OZ] found with
  fewer checked sequences than T4a.

## 4. Kill bars (numbered; all must pass for TRANSFER-PASS)

- K-TR1 (T1 primitive parameterization): The learner, given 6
  primitives, constructs an OX-containing discriminating sequence for
  W-T1. Verified from raw output: SELECT line contains OX, EXEC
  executes once, survivor is true hypothesis in both configs.
  Additionally, the source must NOT have base-4 hardcoded; the base
  must derive from the primitive count. (Checked by code inspection:
  if `total=total*4` appears literally, T1 is PARTIAL.)
- K-TR2 (T2 threshold transfer): The learner, given threshold rules
  and the T2 primitives, constructs a discriminating sequence for
  W-T2. SELECT, EXEC once, correct survivor. The enumerate-filter
  loop must be byte-identical to the original (modulo simulator).
- K-TR3 (T3 concept transfer): The learner selects (red,square),
  tests once, correct survivor. The selection logic must be the same
  first-disagreement filter.
- K-TR4 (T4 composition): T4a finds [S,W,W,OZ]. T4b finds [M,W,OZ]
  with strictly fewer checked sequences than T4a (demonstrating
  reuse value).
- K-TR5 (determinism): 3 runs, byte-identical (cmp), exit 0.
- K-TR6 (purity): pure Zag; no Python anywhere; no em dash bytes.

Verdict:
- TRANSFER-PASS iff K-TR1 through K-TR6 all pass.
- TRANSFER-PARTIAL iff 2-3 of K-TR1..K-TR4 pass (with K-TR5,K-TR6
  passing).
- TRANSFER-FAIL iff 0-1 of K-TR1..K-TR4 pass.

## 5. Honest limitations (frozen)

- T2 and T3 require new simulators. This is not "free" transfer; it
  tests whether the enumerate-filter-select PRINCIPLE is general, not
  whether the delay-rule simulator is general.
- T1 tests implementation parameterization, not conceptual transfer.
- T4b provides the macro; it does not test macro invention.
- All worlds are synthetic and tiny.
- This is step 9 of the promotion pipeline. Steps 10 (red team, done
  by A1) and 11 (governance) remain.

## 6. Amendments

None.
