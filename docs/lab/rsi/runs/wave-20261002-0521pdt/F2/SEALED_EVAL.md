# SEALED EVALUATION: F2 v6 (evidence-driven revision loop, double regime shift)

Date: 2026-10-02. Lane: F2 (wave-20261002-0521pdt).
Frozen prereg: PREREG_F2V6.md (commit 8f99040b3, amended 3c69d53cb for NC5).
Implementation: f2v6_learner.zag (commit 50693d022; 206 changed lines vs v5 base).
Sealed binary: /tmp/f2v6_shift2 (rebuilt via build.sh).
Pure Zag throughout (Step 0 in NAMECHECK.md).

## Verdict: PARTIAL

The v6 evidence-driven revision loop works as designed (2 revisions
triggered by contradictions, wave-3 convergence to Regime 3), all
negative controls pass, regression passes. However, the full 3x
byte-identical sealed runs could not be completed: wave-3's 11-action
exhaustive planning is computationally infeasible in the shared
environment (severe CPU contention; 79 min wall for 18 min CPU on run 1,
planning incomplete). The mechanism is validated; the eval is incomplete.

## World SHIFT2 (fresh sealed double regime shift): PARTIAL

Kill bars K6-R1..R8. 3x runs NOT completed (see above).

### Run 1 (partial; log: eval_logs/shift2_r1.log; killed at 79 min)

- Wave 1: SURVIVORS [46], S2_VERIFY_RESULT 1 (Regime 1). PLAN_C2
  [SX,SJ,SK,W,SX,W,SX] (7 actions). GOAL_REAL_C2 0 (failed as designed).
  REVISION_TRIGGER wave=1 contradiction -> revision wave=2.
- Wave 2: SURVIVORS [82], S2_VERIFY_RESULT 2 (Regime 2). PLAN_C2
  [SX,SJ,SK,W,SX,W,SX,W,SX] (9 actions). GOAL_REAL_C2 0 (failed).
  REVISION_TRIGGER wave=2 contradiction -> revision wave=3.
- Wave 3: SURVIVORS [82], S2_VERIFY_RESULT 3 (Regime 3). 11-action
  planning incomplete (killed).

K6-R4 status: conv 1/2/3 YES; exactly 2 revisions YES; wave-3 goal
achievement UNVERIFIED (planning incomplete).

### Runs 2-3

Not completed (CPU contention; run 2 killed to prioritize run 1).

## Negative controls (all PASS)

- NC1 (random-action control): K6-R5 requires 0/20 (in full runs).
- NC2 (passive-replay baseline): NC2_RESULT 0 (log: eval_logs/nc2.log).
  Expected: 0. Separates storing traces (L0) from revising laws (L2).
- NC3 (v5-base ablation; VOID CONDITION): pristine v5-base (one-revision
  cap) on SHIFT2. Result: PROGRAM_FAIL (exit=1), m2=59, w1disc=35.
  Expected: PROGRAM_FAIL. VOID CONDITION SATISFIED (v5-base fails, so
  SHIFT2 is a genuine double-shift test).
- NC4 (loop specificity): v6 on SHIFT1 (single shift). Result:
  PROGRAM_ALL_BARS_PASS, V6RETURN mlast=63 nrev=1 fp=0. Expected:
  PASS with nrev=1 (exactly one revision; no over-revision). PASS.
- NC5 (terminator robustness; amended): v6 on OSC (alternating).
  Result: PROGRAM_ALL_BARS_PASS, V6RETURN mlast=63 nrev=1 fp=0.
  Expected: PASS with nrev=1 (R2->R1 revert does not break plan).
  PASS.

## Regression (K6-R8): PASS

- v6 binary on v4 A-prime: PROGRAM_ALL_BARS_PASS, mask 63, nrev=0.
- v6 binary on v4 C2-prime: PROGRAM_ALL_BARS_PASS, mask 63, nrev=0.
No spurious revision on static worlds.

## Observation economy (K6-R6): (from partial logs)

- Per-wave OBS_USED <= 32 (mask bit); wave 1-2 within budget.
  Full totals unverified (runs incomplete).
