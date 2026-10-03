# PREREG: H-CAUSALEXP1 Simple-Baseline Comparison (step 5 of 11-step pipeline)

Date: 2026-09-30. Pure Zag only. No Python at any stage.
Status: FROZEN. Committed alone before any baseline implementation, build, or run.

## Mission

H-CAUSALEXP1 (builder result `ce8f1eddb`, repro `bc9c63be8`) reports
BUILD-PASS (7/7) for an active causal discovery loop with max-split
discriminating-experiment selection. Step 5 of the frontier promotion
pipeline requires comparison against simple baselines to check whether the
intervention loop is trivially matched by memorization or dumb search.

Builders report BUILD-PASS / BUILD-FAIL only. This comparison reports
BASELINE-BEATS / BASELINE-MATCHES / H-CAUSALEXP1-WINS. It does NOT promote
to SURVIVES.

## Frozen reference numbers (H-CAUSALEXP1, from committed builder + repro)

Worlds: W1 true mask = bit0 (X2Y), W2 true mask = bit1 (Y2X).
Variables x, y in {0,1}. Actions: 0 idle, 1 trigger, 2 do(x:=0),
3 do(x:=1), 4 do(y:=0), 5 do(y:=1).
Hypotheses: id=0 X2Y (mask bit0), id=1 Y2X (mask bit1), id=2 NONE (mask 0).
Passive phase: start (0,0), fixed script [0,1,0,1,1,0]; all three hypotheses
6/6 LIVE in both worlds; passive logs byte-identical across worlds.

H-CAUSALEXP1 frozen outcomes:
  W1: 1 intervention (seq=[2]), CONVERGED id=0 X2Y (correct), PLAN seq=[2],
      PLAN-OK.
  W2: 2 interventions (seq=[2], seq=[5]), CONVERGED id=1 Y2X (correct),
      PLAN seq=[4], PLAN-OK.
Total interventions across both worlds: 3.
Plans: W1 [2], W2 [4]; both execute in the true world reaching (0,0).

## Frozen baseline definitions

All baselines share the frozen causal mechanics (predict, sim_seq,
intervention semantics, trigger/root semantics), the frozen passive phase,
the frozen hypothesis store, the frozen elimination rule (eliminate exactly
the hypotheses whose predicted final state mismatches the observed state),
and the frozen planner (BFS over action sequences length 1..3 under the
converged mask from (1,1), shortest then lexicographic, goal (0,0)).
Only world_step takes wid (grep audit required). The ONLY difference from
H-CAUSALEXP1 is the experiment-selection policy (or its absence).

### BL-RANDOM: random experiment selection

Per round, select uniformly at random among the 42 candidate experiments
(a in 0..5, b in -1..5 where -1 = length 1) instead of max-split.
Deterministic PRNG: state = (state*1103515245 + 12345) & 0x7fffffff;
pick = draw % 42; candidate i: a = i/7, b = (i%7)-1.
Frozen seeds: 7, 42, 999 (one run-section per seed).
Round cap: 4 (same as H-CAUSALEXP1). Stop early when live==1.
Per world report: n_int (interventions executed), converged id or
NO-CONVERGE, correct (converged id == true id: W1->0, W2->1).
If converged correctly, run the frozen planner and execute the plan;
else emit PLAN-SKIP.

### BL-FIXORDER: fixed-script baseline

Fixed predetermined script, no adaptive selection: length-1 actions in
lexicographic order 0,1,2,3,4,5, cycled, one action per step, max 12 steps.
After each step, apply the frozen elimination rule. Stop when live==1.
If 12 steps exhaust with live>1, emit NO-CONVERGE.
Per world report: n_int, converged id or NO-CONVERGE, correct.
If converged correctly, run the frozen planner and execute the plan;
else emit PLAN-SKIP.

### BL-MEM: memorization / lookup-table check

Tests whether a lookup table mapping passive-log patterns to correct plans
achieves the same result WITHOUT the intervention loop.
Frozen key evidence (from prereg bd883d969 K-CX-1): the passive logs are
byte-identical across W1 and W2, so the table holds exactly one key.
Stored value: plan seq=[2] (do(x:=0)), the lexicographically smallest plan
achieving (0,0) under hypothesis id=0 (X2Y), the first-listed hypothesis.
Procedure: compute the passive-log hash, look up the single table entry,
execute seq=[2] in each true world from (1,1). Zero interventions.
Per world report: PLAN-OK or PLAN-FAIL.
A lookup table CANNOT condition on the hidden world: the input patterns
are identical, so the same plan must be returned for both worlds.

## Frozen determinism requirement

The baseline binary is run 3 consecutive times. All three outputs must be
byte-identical (md5 match), exit code 0, stderr empty.

## Frozen success criteria

K-BL-1 (build/run): cxbase.zag compiles with the frozen toolchain
(/home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc),
exit code 0, empty stderr.
K-BL-2 (determinism): 3 consecutive runs byte-identical.
K-BL-3 (complete report): for BL-RANDOM (seeds 7, 42, 999), BL-FIXORDER,
and BL-MEM, each world reports n_int, converged id or NO-CONVERGE,
correct (0/1), plan seq, and PLAN-OK / PLAN-FAIL / PLAN-SKIP.
K-BL-4 (verdict rule):
  BASELINE-BEATS: some baseline converges correctly in BOTH worlds with
    total n_int < 3 and both plans PLAN-OK; OR BL-MEM achieves PLAN-OK in
    both worlds with zero interventions.
  BASELINE-MATCHES: some baseline converges correctly in BOTH worlds with
    total n_int == 3 and both plans PLAN-OK.
  H-CAUSALEXP1-WINS: otherwise (no baseline beats or matches). Report
    exact per-baseline numbers.
K-BL-5 (purity): grep audit shows wid only as an argument to world_step
in baseline code; zero Python at every stage; zero em dashes (byte-checked
in source, prereg, raw output, and report).

## Honest scope (frozen)

Baselines deliberately reuse all authored machinery (hypothesis vocabulary,
experiment vocabulary, intervention semantics, elimination rule, planner).
The comparison isolates ONE question: does max-split discriminating
selection buy intervention efficiency over random selection, a fixed
script, or no intervention at all? A BASELINE-MATCHES or H-CAUSALEXP1-WINS
verdict does not claim L3 or representational invention; H-CAUSALEXP1 is
bounded L2 per the builder's honest scope.
