# PREREG: H-CAUSALEXP-CONSTRUCT Ablation Study (cxconstruct_ablation)

Date: 2026-09-30.
Status: FROZEN. Committed before any implementation, build, or run.
Lane: causal frontier, step 8 of 11-step promotion pipeline for
H-CAUSALEXP-CONSTRUCT (BUILD-PASS 7/7 at 48f2adc15, REPRODUCED step 4,
BASELINE-LOSES step 5 at 48e24c825, ALTEXP step 6: A1/A2 killed L3 claim,
bounded L2).

## 1. Objective

Quantify what the learner's disagreement filter contributes, and which
components are load-bearing for correctness vs efficiency. The A1/A2
attacks established: the learner enumerates a researcher-bounded finite
family (1364 sequences, lengths 1-5, 4 primitives, fixed lexicographic
order, MAXD=5) and applies a disagreement filter. Researcher owns:
primitive set, enumeration order, depth bound. Learner owns: filter only.

Key question: which components are load-bearing for correctness vs
efficiency?

## 2. Reference learner (from frozen builder source)

The full learner, reimplemented from the frozen prereg description:
- K-CX1: verify all 4 single primitives agree (16/16 across 4 configs).
- Iterative deepening d=1..5: enumerate all 4^d sequences in fixed
  lexicographic order (S=0 < W=1 < OY=2 < OZ=3 via base-4 counting).
- For each sequence with at least one observe: simulate under both
  hypotheses with the generic rule simulator. Select the FIRST where
  predictions disagree. Zero real-world actions during selection.
- Execute selected sequence exactly ONCE against sealed true world.
- Eliminate hypotheses whose simulated prediction != real observation.
- Converge = exactly the true hypothesis survives.

Worlds (from frozen builder):
- World A: H0=[(X,Z,2),(Z,Y,0)], H1=[(X,Y,1)]. Full learner selects
  [S,W,OY] (len 3, 3rd with-observe at depth 3).
- World B: H0=[(X,Z,3),(Z,Y,0)], H1=[(X,Y,2)]. Full learner selects
  [S,W,W,OY] (len 4, 15th with-observe at depth 4).
- 4 configs: (A,true=H0), (A,true=H1), (B,true=H0), (B,true=H1).
- Full learner: 4/4 converge, 1 real-world execution each.

Simulator semantics (from frozen description): state (X,Z,Y,t,tX,tZ,tY);
S sets X:=1,tX:=t; W does t:=t+1 then two rule-application passes;
OY/OZ observe. Rule (src,dst,delay) fires when src==1 and t-t_src >=
delay. Variables X=0,Z=1,Y=2. Actions S=0,W=1,OY=2,OZ=3.

## 3. Ablations (exact procedures)

### AB1: Remove the disagreement filter

Procedure: at each depth d=1..5, enumerate in fixed order, select the
FIRST sequence with at least one observe (no simulation, no disagreement
check). Execute it once. Eliminate via simulation vs real observation
(simulation retained ONLY for elimination, not selection).

Measure: correct convergence (exactly true hypothesis survives) across
4 configs.

- AB1-K1: AB1 selects without any disagreement check. Selection is
  simulation-free.
- AB1-K2: PASS (filter load-bearing for correctness) iff AB1 converges
  correctly on <=1/4 configs. If AB1 gets >=3/4, the filter is NOT
  load-bearing for correctness (unexpected, report as such).

Expected: 0/4. The first-with-observe at depth 1 is [OY]; both
hypotheses predict Y=0 at t=0; both survive; no convergence.

### AB2: Remove simulation for selection

Procedure: enumerate in fixed order across depths 1..5. For selection,
the learner has NO simulator. It executes each candidate sequence in the
real world (count every real-world action). An ORACLE (outside the
learner's decision loop, used only for measurement) computes whether
hypotheses would disagree; the learner stops at the first sequence
where the oracle says disagree. Count total real-world actions to find
it. Elimination is impossible without simulation (noted, not measured).

Measure: real-world actions to find discriminating sequence, World A
and World B separately.

- AB2-K1: Selection uses zero simulation. Every candidate costs
  real-world actions.
- AB2-K2: PASS (simulation load-bearing for efficiency) iff AB2
  requires >=10 real-world actions for World A. Full learner uses 1
  (selection) + len (execution). If AB2 uses <10, simulation is NOT
  load-bearing for efficiency (unexpected).

Expected: World A needs on order 10-20 real executions; World B needs
on order 50-100. (Baseline B3 measured 17/85 for a greedy variant.)

### AB3: Remove iterative deepening (depth 5 only)

Procedure: skip depths 1-4. Enumerate ONLY depth 5 in fixed order.
Apply the disagreement filter (simulation retained). Select first
discriminating at depth 5. Execute once. Eliminate.

Measure: convergence (4 configs) and checked count and selected length.

- AB3-K1: Only depth 5 is enumerated. Depths 1-4 are never tried.
- AB3-K2: PASS (deepening load-bearing for efficiency) iff AB3 checks
  >=100 sequences before selecting, OR selects a sequence longer than
  length 4. If AB3 checks <100 AND selects length <=4, deepening is NOT
  load-bearing (unexpected).

Expected: converges 4/4 but checks hundreds at depth 5 and selects a
length-5 sequence (less efficient than the full learner's len 3/4).

### AB4: Reverse enumeration order

Procedure: full learner but enumerate in REVERSE lexicographic order
(index total-1 down to 0) at each depth. Disagreement filter retained.
Simulation retained.

Measure: checked count to find discriminating, World A and World B.

- AB4-K1: Enumeration order is exactly reversed from the researcher's
  order. No other change.
- AB4-K2: Exploratory. Report checked counts. If AB4 checked counts
  differ from full learner (3 for A, 15 for B) by more than 2x, order
  is efficiency-relevant. No strict pass/fail.

Expected: still converges 4/4 (filter is order-independent for
correctness), but checked counts differ.

### AB5: Shrink MAXD to 3

Procedure: full learner with MAXD=3 (depths 1-3 only). All else
identical.

Measure: convergence across 4 configs.

- AB5-K1: MAXD=3. Depths 4-5 never tried.
- AB5-K2: PASS (bound load-bearing for correctness) iff exactly 2/4
  converge (the two World A configs) and 2/4 fail with
  NO-DISCRIMINATING-SEQUENCE (the two World B configs). If 4/4
  converge, the bound is NOT load-bearing (unexpected). If 0/4
  converge, something else is wrong (report).

Expected: 2/4. World B needs depth 4.

## 4. Validity bars

- P-AB1: Prereg committed alone before any .zag is written. Verified
  via git log ordering.
- P-AB2: All ablation code is pure Zag. Zero Python at any stage
  (including scratch, editing, verification). Zero .py files.
- P-AB3: Each ablation runs 3/3 byte-identical (md5 of raw output
  matches across runs), exit 0, zero stderr.
- P-AB4: The full (unablated) learner is reimplemented and reproduces
  the builder's selections ([S,W,OY] for A, [S,W,W,OY] for B) before
  ablations are measured. This anchors the ablation deltas.
- P-AB5: No em-dash bytes in any committed documentation.
- P-AB6: Commits local only, owned path only
  (docs/lab/research-lead/overnight-20260928/cxconstruct_ablation/).

## 5. Verdict criteria

ABLATION-COMPLETE iff: P-AB1 through P-AB6 all pass, all five ablations
run with exact numbers reported, and each K-bar is adjudicated
PASS/FAIL per its frozen criterion.

The report will contain a table: component | correctness impact |
efficiency impact | load-bearing?.

This prereg does not authorize any L3 claim. H-CAUSALEXP-CONSTRUCT is
bounded L2 per A1/A2. The ablation quantifies the L2 mechanism's
internal structure.
