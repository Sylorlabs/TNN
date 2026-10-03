# H-PROCLANG1 RESULT: BUILD-PASS (9/9 frozen kill bars)

Worker: procedure-language invention frontier researcher (subagent).
Date: 2026-09-29/30.
Prereg: `PREREG_PROCLANG1.md` (frozen; committed in `bd883d969`).
Implementation: `proclang1.zag` (this commit; strict prereg-before-implementation
ancestry verified: the prereg commit contains only prereg markdown, and
`proclang1.zag` first appears in this result commit).
Raw evidence: `PROCLANG1_RAW.txt` (md5 `e6b87d123bdb3497e94afb9be0cfc3ae`,
3/3 byte-identical runs, exit 0, zero stderr).
Toolchain: `znc 2026.07.0-dev (edition 2026)`.
Pure Zag throughout: implementation, builds, runs, analysis
(grep/cmp/md5sum only). No Python anywhere.

Verdict: **BUILD-PASS**. This is a builder verdict only. It is NOT a SURVIVES
claim. Promotion requires the full 11-step frontier pipeline (independent
reproduction, baseline attack, OOD, ablation, transfer, independent adversary,
governance audit).

## 1. What was built

Frozen DSL D0: one i32 register; ops ADD k / MUL k with k in {-3..3};
programs of length 0..3 (2955 total). No conditional, no loop, no comparison.
Frozen lemma L0: every D0 program computes an affine function f(x) = a*x + b.

Learner (one persistent instance across four tasks, append-only operator
library): Phase A exhaustively searches D0 (deterministic: lengths ascending,
op indices ascending, strict improvement). If the best D0 program still
mismatches training data, the language is declared INADEQUATE and Phase B
runs: scan integer thresholds t over the input coordinate, fit best D0
program on each side, and if some split reaches zero total mismatches,
REIFY a persistent operator COND(t, leftProg, rightProg) with a white-box
creation trace. Otherwise the task FAILS (no invention).

Worlds (environment only; learner observes only (x, y) pairs):
T1 y=|x|, T4 y=|x-3| (presented as continuation/counterexample to T1),
T2 y=step(x) (1 if x>=0 else -1), T3 y=|1-u| with u=-x+1 (re-coordinatized).
Frozen impossibility: each target violates the affine 3-point test
f(-1)+f(1)=2*f(0) (values (1,0,1), (1,0,1), (-1,1,1), (1,0,1) respectively),
so NO D0 program solves any of them, even on three points.

## 2. Kill-bar results (all from the frozen raw output)

K-P1-1 (impossibility, empirical): PASS.
  AFFINE_LEMMA checked=2955 ok=2955: every enumerated D0 program satisfies
  f(-1)+f(1)=2*f(0). Best D0 program on T1 training: ID with 20 mismatches
  (>= 1 required).

K-P1-2 (invention + hidden success): PASS.
  INVENT op=COND_T1 t=0 left=MUL -1 right=ID. HIDDEN n=2001 correct=2001
  on x in [-1000, 1000].

K-P1-3 (white-box trace): PASS. Raw contains for the T1 invention:
  trigger_residual=20, SPLIT_SCAN n_thresh=43, best_t=0, left=MUL -1,
  right=ID, train_before=20, train_after=0, op name COND_T1, lib_size=1.

K-P1-4 (ablation): PASS. Affine-only (best Phase-A program ID):
  n=2001 correct=1001 (< 2001 required). Removing the invented operator
  destroys the advantage.

K-P1-5 (reuse): PASS. T2: REVISE old=COND_T4 new=COND_T2 t=0
  left=MUL 0;ADD -1 right=MUL 0;ADD 1. HIDDEN n=2001 correct=2001.

K-P1-6 (transfer): PASS. T3 (reflected/shifted inputs): REVISE new=COND_T3
  t=1 left=ADD -1;MUL -1 right=ADD -1. HIDDEN n=2001 correct=2001, and the
  chosen threshold t=1 is re-learned in the new coordinates (the T1
  threshold t=0 would fail here: the operator family transfers, not a
  memorized constant).

K-P1-7 (revision after counterexample): PASS.
  CUR_OP_TRAIN_MISMATCHES op=COND_T1 n=41 on T4 training: the stored T1
  operator is fully contradicted (|x|=|x-3| has no integer solution, so all
  41 points mismatch). REVISE old=COND_T1 new=COND_T4 t=3
  left=ADD -3;MUL -1 (= 3-x) right=ADD -3 (= x-3). HIDDEN n=2001 correct=2001.
  The learner revised its stored operator rather than ignoring the
  counterexample.

K-P1-8 (determinism): PASS. 3/3 runs byte-identical (md5
  e6b87d123bdb3497e94afb9be0cfc3ae via cmp), exit code 0, zero stderr.

K-P1-9 (memorization control): PASS. Exact-match table baseline:
  n=2001 correct=41 (< 2001 required). The hidden ranges extend far beyond
  training, defeating pure memorization.

All nine bars pass. Verdict: BUILD-PASS.

## 3. Independent hand-verification of the headline numbers

The three current-operator mismatch counts were verified by hand from the
emitted operator definitions:
  T4 train vs COND_T1 (t=0, -x / x) on |x-3|: no integer x satisfies
    |x|=|x-3|, so 41/41 mismatch. Raw: 41. Match.
  T2 train vs COND_T4 (t=3, 3-x / x-3) on step(x): left side correct only
    at x=2, right side only at x=4: 39/41 mismatch. Raw: 39. Match.
  T3 train vs COND_T2 (t=0, -1 / +1) on |1-u|: left side never -1
    (abs is non-negative), right side correct only at u=0,2: 39/41
    mismatch. Raw: 39. Match.
Each invented operator was hand-checked against its world function
(e.g. COND_T4 left (x-3)*(-1)=3-x for x<3; right x-3 for x>=3).
The ablation count 1001/2001 is exactly the x>=0 half where ID matches |x|.
The table baseline 41/2001 is exactly the 41 training points contained in
the hidden range.

## 4. Self-assessment against the 12 L3 criteria (honest)

 1. Final procedure not in source: YES. COND(t,A,B) with A!=B computes a
    non-affine function; D0 = affine only (L0). Not expressible in D0.
 2. Not enumerated as one complete candidate: YES. The specific operators
    (threshold values 0, 3, 0, 1 and sub-programs) were found by data-driven
    search, never listed.
 3. Created after experience: YES. Invention events fire during the run,
    triggered by measured residual error.
 4. Present in persistent learner state: YES. Append-only library ends with
    4 operators (LIB_SIZE 4); all four remain stored.
 5. White-box trace explains creation: YES. TRACE lines give trigger
    residual, thresholds scanned, chosen t, sub-programs, before/after error.
 6. Hidden instances solved: YES. 2001/2001 on four disjoint wider ranges.
 7. Ablation destroys the advantage: YES. 2001 -> 1001 without COND.
 8. Reused later: YES (family-level). The COND operator family is reused
    for T4, T2, T3; each reuse persists as a new library operator. Note:
    per-task the current operator is replaced (REVISE), so reuse is of the
    invented operator FORM, not of one fixed operator instance.
 9. Transfers across changed surface representation: WEAK YES. T3 reflects
    and shifts the input coordinate; the family re-learns (t=1, pieces
    swapped). This is affine re-coordinatization of a 1-D input, not a
    radically new surface. Stronger transfer is deferred.
10. Beats simple memorization/search controls: YES. Table baseline 41/2001;
    affine search provably cannot fit (K-P1-1).
11. Survives independent red team: PENDING. Not done; required before any
    SURVIVES consideration.
12. Revisable after counterexample: YES. T4 contradicts COND_T1 (41/41
    mismatches); the learner emits REVISE and replaces it with COND_T4,
    which then scores 2001/2001.

Score: 10.5/12 with #11 pending and #9 weak. 7/12 is not "basically L3";
this report claims BUILD-PASS only, not L3.

## 5. Frozen honesty caveats (carried from the prereg)

a) Machinery vs content. The case-split MACHINERY (threshold scan over the
   input coordinate, reification into COND) is researcher-supplied generic
   machinery; the CONTENT (that a split is needed at all, each threshold
   value, each sub-program) is learner-created from data. An adversary may
   argue the machinery implicitly enumerates "1-level decision stumps" as a
   solution family. The builder's position: COND(t,A,B) with A!=B is
   provably not expressible in D0, so the operator extends the
   representational language per Criterion 0. This dispute is OUT OF SCOPE
   for BUILD-PASS/FAIL and is referred to the independent adversary.
b) The predicate family (single threshold on the input coordinate) is a
   researcher-chosen generic form; threshold VALUES are learned. For 1-D
   tasks this is the natural generic choice, but a critic may call it
   enumerating the solution shape. Disclosed for the adversary.
c) Transfer T3 is weak (see #9 above).
d) Prereg commit note: PREREG_PROCLANG1.md was committed in `bd883d969`
   together with another worker's PREREG_CAUSALEXP1.md (a concurrent commit
   swept the staged file). The commit contains only prereg markdown, no
   implementation; `proclang1.zag` first appears in this result commit.
   Strict prereg-before-implementation ancestry holds; the "alone" aspect
   is the disclosed deviation.
e) No Python was used anywhere. No em dashes in any documentation
   (byte-verified). Only owned paths under proclang_frontier/ were
   committed.

## 6. Suggested next steps (for the parent, not decided here)

- Independent adversary: attack the machinery-vs-content caveat (a-c above),
  try to break COND_T1..T4 with distributional shift, and probe whether the
  threshold-scan machinery smuggles the solution.
- Stronger transfer: change the surface representation non-affinely
  (e.g. 2-D inputs, permuted feature order) in H-PROCLANG2.
- Developmental integration: offer the COND operator family to the
  continuing-learner lane as a reusable invention primitive.
