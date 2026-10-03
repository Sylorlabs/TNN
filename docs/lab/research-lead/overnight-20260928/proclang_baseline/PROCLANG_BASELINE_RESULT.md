# H-PROCLANG1 BASELINE COMPARISON RESULT (pipeline step 5 of 11)

Worker: simple-baseline comparison worker (subagent).
Date: 2026-09-30.
Prereg: `PREREG_PROCLANG_BASELINE.md` (frozen; committed in `ddd90d06b`).
Implementation: `baseline.zag` (this commit; strict prereg-before-implementation
ancestry: the prereg commit contains only prereg markdown, and `baseline.zag`
first appears in this result commit).
Raw evidence: `BASELINE_RAW_1.txt`, `BASELINE_RAW_2.txt`, `BASELINE_RAW_3.txt`
(md5 `944099a8ce8ff802a075759f39895105`, 3/3 byte-identical via cmp,
exit code 0, zero stderr on all three runs).
Toolchain: `znc 2026.07.0-dev (edition 2026)`.
Pure Zag throughout: implementation, builds, runs, analysis
(grep/cmp/md5sum only). No Python anywhere.

## 1. Frozen scores (all from the raw output, n=2001 hidden points per task)

COND reference (builder, H-PROCLANG1): 2001/2001 on T1, T4, T2, T3.

T1 (y=|x|):
  B1A train_mm=20 prog=ID hidden_correct=1001
  B1B prog=ID hidden_correct=1001
  B2 t=0 hidden_correct=2001
  B3 hidden_correct=41

T4 (y=|x-3|):
  B1A train_mm=17 prog=ADD -3;MUL -1 hidden_correct=1004
  B1B prog=ADD -3;MUL -1 hidden_correct=1004
  B2 t=3 hidden_correct=2001
  B3 hidden_correct=41

T2 (y=step(x)):
  B1A train_mm=20 prog=MUL 0;ADD 1 hidden_correct=1001
  B1B prog=MUL 0;ADD 1 hidden_correct=1001
  B2 t=0 hidden_correct=2001
  B3 hidden_correct=2001

T3 (y=|1-u|):
  B1A train_mm=20 prog=ADD -1 hidden_correct=1001
  B1B prog=ADD -1 hidden_correct=1001
  B2 t=1 hidden_correct=2001
  B3 hidden_correct=41

## 2. Per-baseline verdicts (frozen rules)

B1a (exhaustive D0 search, train-selected): COND-BEATS on all four tasks
  (1001, 1004, 1001, 1001 vs 2001). The T1 score 1001/2001 independently
  reproduces the builder ablation number from K-P1-4.

B1b (exhaustive D0 search, hidden-selected cheating oracle): COND-BEATS on
  all four tasks (1001, 1004, 1001, 1001 vs 2001). Even with full knowledge
  of the hidden set, no affine program solves any task.

B2 (generic 2-piece least-squares, no COND machinery): BASELINE-MATCHES on
  all four tasks (2001/2001 each, thresholds t = 0, 3, 0, 1).

B3 (1-nearest-neighbor): COND-BEATS on T1, T4, T3 (41/2001 each);
  BASELINE-MATCHES on T2 (2001/2001).

## 3. Central question

"Is the task trivially solvable by generic piecewise fitting?"
Answer: YES. B2, a per-task statistical fit with no invented operator, no
persistent library, no reuse, no revision, and no white-box trace, reaches
2001/2001 on all four tasks. The hidden-accuracy headline therefore does
not by itself distinguish operator invention from generic piecewise
fitting. This confirms the builder's frozen honesty caveat (a): the
threshold-scan machinery supplies the "1-level decision stump" solution
family, and a generic statistician equipped with the same 2-piece
inductive bias matches the learner's static score.

## 4. What B2 does NOT refute

Per prereg note N2, BASELINE-MATCHES on hidden score bounds what the score
alone proves; it does not refute invention. The invention-specific evidence
stands or falls on the operator-level properties, which B2 does not have:
persistence of invented operators across tasks, reuse of the COND family
(T2), transfer with re-learned threshold in new coordinates (T3), revision
after full contradiction (T4), and the white-box creation trace. Those are
for the later pipeline steps (independent adversary, which already has the
machinery-vs-content caveat referred to it).

B3 matching COND on T2 is expected and honest (prereg N3): a step function
is constant outside the training range, so endpoint nearest neighbors are
exactly right. This is a property of T2, not of the learner.

## 5. Independent cross-validation notes

a) B1a's train-selected programs reproduce the builder's Phase-A selections
   exactly from the raw builder output: ID with 20 mismatches (T1),
   ADD -3;MUL -1 with 17 mismatches (T4), MUL 0;ADD 1 with 20 mismatches
   (T2), ADD -1 with 20 mismatches (T3). This independently validates the
   D0 enumeration fidelity of both implementations.
b) B2's chosen thresholds (0, 3, 0, 1) match the analytically derived
   SSE minima: T1 zero-SSE at t=0,1 (tie broken to 0); T4 zero-SSE at
   t=3,4 (tie broken to 3); T2 zero-SSE uniquely at t=0; T3 zero-SSE at
   t=1,2 (tie broken to 1). The exact 2001/2001 hidden scores further
   prove the refit lines are exactly the true pieces: any wrong threshold
   or wrong line would break exactness on the wide hidden range.
c) B2's least-squares fits use exact integer arithmetic (i64) with an
   exact quotient-remainder rational comparison for SSE minimization.
   No floating point exists anywhere in the implementation.

## 6. Determinism and governance

D1 PASS: 3/3 runs byte-identical (cmp), md5
  944099a8ce8ff802a075759f39895105, exit code 0, zero stderr.
D2 PASS: pure Zag only (znc build, native runs, grep/cmp/md5sum analysis).
  No Python anywhere.
D3 PASS: no em dashes in any documentation (byte-checked before commit).
D4: only owned paths under
  docs/lab/research-lead/overnight-20260928/proclang_baseline/ committed.
D5: commits stay local; nothing pushed.
D6 PASS: baselines observe only (x, y) pairs; B1b is the declared oracle
  exception.
