# PREREG: H-PROCLANG1 simple-baseline comparison (step 5 of 11)

Status: FROZEN. Committed alone before any baseline implementation, build, or run.
Worker: simple-baseline comparison worker (subagent), H-PROCLANG1 pipeline step 5.
Date: 2026-09-30.

## 1. Question

H-PROCLANG1 reports BUILD-PASS with hidden scores 2001/2001 on four tasks
(T1 y=|x|, T4 y=|x-3|, T2 y=step(x), T3 y=|1-u|) via an invented COND operator
family, versus 1001/2001 for the affine-only ablation and 41/2001 for the
memorization control. This step asks: do simple, non-inventing baselines
achieve the same hidden scores? If yes, the hidden-accuracy headline does not
by itself distinguish operator invention from generic fitting; the invention
claim must then rest on persistence, reuse, revision, transfer, and the
white-box creation trace.

## 2. Frozen tasks (worlds are environment code; baselines see only pairs)

T1: y = |x|. Train x in [-20, 20] (41 points). Hidden x in [-1000, 1000]
  (2001 points). COND reference score: 2001/2001.
T4: y = |x-3|. Train x in [-20, 20] (41 points). Hidden x in [-1000, 1000]
  (2001 points). COND reference score: 2001/2001.
T2: y = step(x) = 1 if x >= 0 else -1. Train x in [-20, 20] (41 points).
  Hidden x in [-1000, 1000] (2001 points). COND reference score: 2001/2001.
T3: y = |1-u|. Train u in [-19, 21] (41 points). Hidden u in [-999, 1001]
  (2001 points). COND reference score: 2001/2001.

All baselines are fit on TRAINING pairs only, then scored by exact-match
count on the hidden points. No baseline may see hidden data during fitting
(except B1b, which is an explicit cheating oracle upper bound).

## 3. Frozen baselines

B1a. Exhaustive D0 search, train-selected (mirrors learner Phase A).
  Enumerate all 2955 D0 programs (program length 0, then 1, 2, 3; op index
  ascending where 0..6 = ADD (idx-3), 7..13 = MUL (idx-10); strict
  improvement on training mismatches, ties keep the earlier program).
  Score the selected program on hidden by exact matches.
  Expected: T1 = 1001/2001 (independent check of the builder ablation
  number); every task < 2001/2001.

B1b. Exhaustive D0 search, hidden-selected oracle (cheating upper bound).
  Same enumeration; select the program maximizing exact matches on the
  HIDDEN points themselves. This bounds what ANY affine search could ever
  achieve on each task, even with full knowledge of the test set.
  Expected: all tasks < 2001/2001 (T1/T2/T3 = 1001, T4 = 1004).

B2. Generic 2-piece least-squares regression (no COND machinery, no
  operator, no persistence, no reuse, no revision, no transfer; a fresh
  statistical fit per task).
  For each integer threshold t in [xmin-1, xmax+1] (ascending, same range
  the learner scans; disclosed, not hidden):
    L = {training points with x < t}, R = {training points with x >= t}.
    Fit an ordinary least-squares line on each side using exact integer
    arithmetic (i64 accumulators): with sums Sx, Sy, Sxx, Sxy, Syy over n
    points, denom = n*Sxx - Sx*Sx; if denom == 0 the side is constant and
    the line is y = round(Sy/n); else the line is y = (P*x + Q)/D with
    P = n*Sxy - Sx*Sy, Q = Sxx*Sy - Sx*Sxy, D = denom.
    Empty side contributes zero error.
    total_SSE(t) = sum over both sides of (1/D_side^2) * sum((D_side*y -
    P_side*x - Q_side)^2), compared across thresholds by exact integer
    cross-multiplication (no floating point anywhere).
  Pick t minimizing total_SSE(t); ties keep the smaller t.
  Predict each hidden x as round((P*x+Q)/D) to the nearest integer, half
  away from zero, on the side its x falls into; count exact matches.
  Expected: 2001/2001 on all four tasks, because the worlds are exactly
  2-piece affine and noise-free, and the least-squares fit recovers the
  true pieces exactly.

B3. 1-nearest-neighbor on training data.
  For each hidden x, predict the y of the training point minimizing
  |x - xt| (ties broken toward the smaller training index; no ties occur
  on these integer grids). Count exact matches on hidden.
  Expected: T1 41/2001, T4 41/2001, T2 2001/2001 (step is constant outside
  the training range, so endpoint neighbors are exactly right), T3 41/2001.

## 4. Frozen verdict rules

Per baseline per task, compare against the COND reference 2001/2001:
  COND-BEATS: baseline score strictly below 2001.
  BASELINE-MATCHES: baseline score equals 2001.
  BASELINE-BEATS: baseline score strictly above 2001 (not expected;
    would indicate a scoring bug, since 2001 is the maximum).

Overall labels reported per baseline:
  B1: expected COND-BEATS on all tasks (affine search provably cannot fit).
  B2: if 2001/2001 on all four tasks, report BASELINE-MATCHES with the
    interpretation that generic piecewise least-squares fitting reaches
    the same hidden score, so the invention claim cannot rest on hidden
    accuracy alone.
  B3: expected COND-BEATS on T1/T4/T3 and BASELINE-MATCHES on T2.

The central question "is the task trivially solvable by generic piecewise
fitting" is answered YES iff B2 reaches 2001/2001 on all four tasks.

## 5. Frozen determinism and governance

D1: 3/3 runs byte-identical (cmp), exit code 0, zero stderr.
D2: Pure Zag only: implementation, builds, runs, analysis
  (grep, cmp, md5sum). No Python anywhere. Disclosure does not cure.
D3: No em dashes in any documentation (byte-checked before commit).
D4: Commit only owned paths under
  docs/lab/research-lead/overnight-20260928/proclang_baseline/.
D5: Commits stay local. Nothing is pushed without the user authorization.
D6: The world functions are environment code; baselines observe only
  (x, y) pairs (B1b excepted as a declared oracle).

## 6. Frozen honesty notes

N1. B2 deliberately uses the same threshold scan range as the learner.
  The difference under test is not the scan range; it is that B2 is a
  per-task statistical fit with no invented operator, no persistent
  library, no reuse, no revision, and no white-box creation trace.
N2. B2 matching COND on hidden score would NOT refute invention; it would
  bound what the hidden score alone proves. Persistence, reuse (T2),
  transfer (T3), revision after contradiction (T4), and the creation
  trace remain invention-specific evidence for later pipeline steps.
N3. B3 matching COND on T2 is expected and honest: a step function is
  constant outside the training range, so nearest-neighbor extrapolation
  is exact there. This is a property of T2, not of the learner.
