# PREREG H-PROCLANG1: Conditional-operator invention beyond a frozen affine DSL

Status: FROZEN. Committed alone before any implementation, build, or run.
Task: Procedure-Language Invention Frontier (parent directive 2026-09-29).
Worker: proclang frontier researcher (subagent).
Date: 2026-09-29.

## 1. Hypothesis

H-PROCLANG1: A learner equipped with
  (a) exhaustive search over a frozen straight-line DSL D0, and
  (b) generic inadequacy-triggered threshold case-split with operator reification,
will invent a conditional-dispatch operator family COND(t, A, B) that is NOT
expressible in D0, and will use it to solve task families that are PROVABLY
unsolvable by any D0 program. The invented operators persist in a learner-owned
library, are reused across tasks, transfer to a re-coordinatized input
representation, and are revised (not merely supplemented) when contradicted.

This is a frontier BUILD-PASS/BUILD-FAIL probe, not a SURVIVES claim.
Builders may not self-promote. Promotion requires the full pipeline
(reproduction, baseline attack, OOD, ablation, transfer, independent adversary).

## 2. Frozen DSL D0

State: one i32 register r, initialized to the input x.
Ops (k in K = {-3,-2,-1,0,1,2,3}):
  ADD k : r := r + k
  MUL k : r := r * k
Program: sequence of 0 to 3 ops. Length 0 = identity.
D0 contains NO conditional, NO loop, NO comparison, NO case split.

Lemma L0 (affine closure, frozen proof): Every D0 program computes an affine
function f(x) = a*x + b with integer a, b.
Proof: ADD k and MUL k are affine in r. The identity is affine (a=1, b=0).
Composition of affine functions is affine: if g(x) = a1*x + b1 and
h(y) = a2*y + b2, then h(g(x)) = (a2*a1)*x + (a2*b1 + b2). By induction over
program length, every D0 program is affine. QED.

Corollary C0 (3-point test): For every D0 program f,
f(-1) + f(1) = 2 * f(0).
The frozen run machine-checks C0 over the full enumerated space
(1 + 14 + 196 + 2744 = 2955 programs). This is K-P1-1 part A.

## 3. Task families and frozen impossibility proofs

World generates training pairs (x, y). The learner sees ONLY the pairs,
never the world function. Hidden evaluation uses disjoint, wider ranges.

T1 (invention): y = |x|. Train x in [-20, 20] (41 points).
  Hidden: x in [-1000, 1000] (2001 points).
  Impossibility: |.| at (-1, 0, 1) gives (1, 0, 1). By C0 any D0 program
  satisfies f(-1)+f(1) = 2*f(0), i.e. 1 + 1 = 2*0, false. So NO D0 program
  solves T1 exactly, even on just three points. Frozen.

T4 (revision / counterexample): y = |x - 3|. Train x in [-20, 20].
  Hidden: x in [-1000, 1000].
  Impossibility: at (2, 3, 4) gives (1, 0, 1); same C0 violation. Frozen.
  T4 is presented as a CONTINUATION of the absolute-value concept learned in
  T1. The T1 operator COND(t=0, NEG, ID) is contradicted by T4 training
  points x in [0, 3). The learner must REVISE its stored operator
  (threshold 0 -> 3, pieces updated), satisfying L3 criterion 12.

T2 (reuse): y = step(x) = 1 if x >= 0 else -1. Train x in [-20, 20].
  Hidden: x in [-1000, 1000].
  Impossibility: at (-1, 0, 1) gives (-1, 1, 1): -1 + 1 = 2*1 is false.
  Frozen. T2 reuses the invented COND operator FAMILY (new persistent
  operator COND2 in the library).

T3 (transfer, changed surface representation): world presents u = -x + 1
  (reflection plus shift; the learner is told nothing of this), target
  y = |1 - u|. Train u in [-19, 21] (41 points).
  Hidden: u in [-999, 1001] (2001 points).
  Impossibility: at (0, 1, 2) gives (1, 0, 1); C0 violated. Frozen.
  The COND family must be re-learned in the new coordinates (threshold 1,
  pieces swapped relative to T1). A memorized T1 threshold (t=0) FAILS here,
  so success demonstrates family transfer, not constant copying.

Execution order in the frozen run: T1, T4, T2, T3.

## 4. Frozen learner algorithm

The learner is ONE persistent instance across T1, T4, T2, T3. It owns an
append-only operator library (persistent state) and a "current operator"
pointer. All search is exhaustive and deterministic (fixed enumeration
order, strict-improvement replacement).

Phase A (DSL search): enumerate all 2955 D0 programs (length 0, then 1,
then 2, then 3; op index ascending where op index 0..6 = ADD (idx-3),
7..13 = MUL (idx-10)). Score = mismatches on training pairs. Keep the
best under strict improvement (ties keep the earlier = shorter, then
lexicographically smaller program). Deterministic.

Inadequacy trigger: if best Phase-A mismatches > 0, the current
representational language is declared INADEQUATE for this data and Phase B
runs. If best Phase-A mismatches == 0, predict with it (no invention).

Phase B (generic case-split + reification):
  For each integer threshold t in [xmin-1, xmax+1] (ascending):
    L = {training points with x < t}, R = {x >= t}.
    Fit best D0 program on L and on R separately (Phase-A routine;
    empty side fits vacuously with 0 mismatches, program ID).
    total(t) = mismatches(L) + mismatches(R).
  Pick t minimizing total(t); ties keep the smaller t (ascending scan,
  strict improvement).
  If min total == 0: REIFY a new persistent operator
    COND(name, t, progL, progR) with semantics
    predict(x) = progL(x) if x < t else progR(x).
    Append to the library with a white-box creation trace:
      trigger residual (Phase-A mismatches), thresholds scanned,
      chosen t, left/right program encodings, train error before and after.
    Emit INVENT on first creation, REVISE on later tasks (old -> new).
  Else: halt this task with FAILURE (no operator invented).

Per-task procedure: evaluate the current operator (if any) on the new
training data. If 0 mismatches, emit REUSE and predict with it. Else run
Phase A; if inadequate run Phase B; on success emit INVENT (library empty)
or REVISE (library non-empty, old operator contradicted).

Prediction on hidden data uses the current operator (or Phase-A program
if no invention occurred).

Required sub-programs are all within D0 length <= 3:
  T1: left NEG = [MUL -1], right ID = [] (expected t = 0).
  T4: left [MUL -1, ADD 3] (= 3 - x), right [ADD -3] (= x - 3) (expected t = 3).
  T2: left [MUL 0, ADD -1], right [MUL 0, ADD 1] (expected t = 0).
  T3: left [MUL -1, ADD 1] (= 1 - u), right [ADD -1] (= u - 1) (expected t = 1).

Baselines (frozen):
  Ablation: best Phase-A program alone (COND disabled) on T1 hidden.
  Memorization control: exact-match table on T1 training; unseen x -> 0.

## 5. Frozen kill bars

K-P1-1 (impossibility, empirical): (a) C0 machine-checked: 2955/2955
  enumerated programs satisfy f(-1)+f(1) = 2*f(0); (b) best D0 program on
  T1 training has >= 1 mismatch. Both required.
K-P1-2 (invention + hidden success): raw output contains an INVENT event
  for T1; current operator scores 2001/2001 exact on T1 hidden.
K-P1-3 (white-box trace): raw output contains, for the T1 invention:
  trigger residual value, number of thresholds scanned, chosen t,
  left and right program encodings, train mismatches before and after,
  operator name, library size after append. All required.
K-P1-4 (ablation): affine-only predictor scores < 2001/2001 on T1 hidden
  (expected 1001/2001 for the identity program).
K-P1-5 (reuse): T2 ends with a library operator scoring 2001/2001 on T2
  hidden; raw shows INVENT or REVISE for T2.
K-P1-6 (transfer): T3 hidden 2001/2001 AND chosen threshold t = 1
  (re-learned in new coordinates; t = 0 would fail).
K-P1-7 (revision): T4 training contradicts the T1 operator (raw shows
  current-operator training mismatches > 0 before re-invention); raw shows
  a REVISE event naming the old and new operator; new operator scores
  2001/2001 on T4 hidden with chosen t = 3.
K-P1-8 (determinism): 3/3 runs byte-identical (cmp), exit code 0.
K-P1-9 (memorization control): table baseline scores < 2001/2001 on T1
  hidden (expected 1/2001).

Verdict rule: BUILD-PASS iff K-P1-1 through K-P1-9 ALL pass.
Otherwise BUILD-FAIL, with the failed bars named.
The builder reports BUILD-PASS or BUILD-FAIL ONLY. No SURVIVES promotion.

## 6. Governance and honesty caveats (frozen)

- Pure Zag only: implementation, builds, runs, and all analysis
  (grep, awk, cmp, md5sum, diff). No Python anywhere. Disclosure does not cure.
- No em dashes in any documentation (byte-checked before commit).
- Commit only owned paths under
  docs/lab/research-lead/overnight-20260928/proclang_frontier/.
- The world functions (|x|, step, |1-u|, |x-3|) are environment code; the
  learner observes only (x, y) pairs. The harness never passes world
  internals to the learner.
- Central L3-interpretation caveat (frozen, for the future adversary):
  the case-split MACHINERY (threshold scan over the input coordinate,
  reification into COND) is researcher-supplied generic machinery; the
  CONTENT (that a split is needed at all, the threshold value, the
  sub-programs) is learner-created from data. An adversary may argue the
  machinery implicitly enumerates "1-level decision stumps" as a solution
  family. The builder's position: COND(t, A, B) with A != B is provably not
  expressible in D0 (it computes a non-affine function; D0 = affine only),
  so the operator extends the representational language per Criterion 0.
  This dispute is OUT OF SCOPE for BUILD-PASS/FAIL and is referred to the
  independent adversary.
- Transfer T3 is WEAK transfer (affine re-coordinatization of a 1-D input,
  not a radically new surface representation). Stronger surface-change
  transfer is deferred to a follow-up.
- L3 criterion 11 (independent red team) is PENDING by construction;
  criterion 9 (transfer) is claimed weakly; all others are tested above.
- /tmp may be wiped by the VM; all evidence is committed to the repo
  before any verdict is reported.
