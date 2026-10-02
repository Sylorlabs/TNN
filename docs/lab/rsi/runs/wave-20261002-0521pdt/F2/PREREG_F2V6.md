# PREREG_F2V6: Evidence-driven revision loop under two progressive hidden law changes

Date: 2026-10-02. Status: FROZEN. This prereg is written before any
v6 implementation run on the sealed worlds exists. It is committed ALONE
first (no implementation in that commit): the prereg's first commit must
strictly precede the implementation's; the commit-order self-check
applies. UNVERIFIABLE ORDERING voids this prereg.

Lane: F2 (wave-20261002-0521pdt). Candidate name: F2 v6 (harder sustained
goal candidate). Governance: pure Zag only (safebin; Step 0 recorded in
NAMECHECK.md). No em dashes in wave documentation (check_no_dash.sh
before every commit).

## 1. Objective

Test the F2 autonomous-scientist loop against FRESH sealed worlds in
which TWO hidden laws change progressively mid-stream (double regime
shift), requiring sustained multi-wave experiment construction: the
learner must converge under Regime 1, detect from a failed plan
execution that the world contradicted its model, revise (fresh passive +
full re-discrimination in Regime 2), detect a SECOND contradiction from
the second failed execution, revise AGAIN, re-converge under Regime 3,
re-plan, and achieve the sustained goal. The v5 mechanism has a fixed
one-revision cap and provably fails this world (NC3 calibration,
section 9).

## 2. Prior history (read first)

- F2 v1 (2026-09-30): BUILD-FAIL on K-AS5b (weak goal instance).
- F2 retry (2026-09-30): BUILD-PASS on the harder B2 goal.
- F2 v2 (wave-20261001-1721pdt): BUILD-FAIL on K3-R4 (nalive=4 X-rule
  equivalence class; depth-6 bound provably blind).
- F2 v3 (wave-20261001-2021pdt): DPDS mechanism (pairwise deep search to
  D2=8). BUILD-FAIL on K4-R4 (nalive=2; crossed X-rule pair needs
  depth 9, D2=8 insufficient).
- F2 v4 (wave-20261001-2321pdt): D2=9. BUILD-PASS, RT-F2V3
  EVIDENCE-HOLDS (all seven attack axes clean). v4 achieves sustained
  dual contextual control on fresh sealed worlds by one convergence and
  one plan. It never re-validates its model against real observations
  after convergence, so any mid-stream law change defeats it.
- F2 v5 (wave-20261002-0221pdt): regime-shift revision design (one
  revision edge, planner tightening, L_wave refactor). INTERRUPTED
  MID-FLIGHT: prereg written but never frozen, implementation written
  but never committed, sealed shift world never written, no sealed
  runs, no verdict. The v5 files exist only as uncommitted working-copy
  files in docs/lab/rsi/runs/wave-20261002-0221pdt/F2/. This v6 prereg
  supersedes v5; v5's core claim (single-shift revision) is still
  evaluated via NC4 below.
- Queued next: "Active experiment construction F2 retry with a harder
  sustained goal (v1 BUILD-FAIL on a weak goal)". v5 was that retry's
  first attempt (interrupted); this v6 prereg is the harder-goal retry.

## 3. The v6 mechanism change (one structural change from v5)

The v5 design capped revision at EXACTLY ONE wave (a researcher-set
constant). The v6 change replaces the fixed cap with an
evidence-driven revision loop in L_run:

- After each wave, if the wave's executed plan was correct under the
  converged model but the world's real verification observations
  contradict the model's predictions (plan found, goal NOT met for
  real, predicted != actual, exactly one survivor), the learner runs
  another revision wave (fresh passive trace, full re-discrimination,
  re-verification, re-plan, re-execution).
- The loop stops when (a) a wave's plan verifies for real (goal met),
  or (b) a wave re-converges to a law set ALREADY SEEN in this run
  (fixed point: the converged rule bytes for every effect var match a
  previous wave's; further waves would repeat identically, so the
  learner stops honestly with FAIL, no infinite regress), or (c) a
  wave ends without a prediction-vs-observation contradiction (the
  planner lied or no plan; honest FAIL).
- There is NO researcher-set revision count. The stopping conditions
  are learner-verifiable (observed contradiction, observed law-set
  repetition). A wave-safety cap (6) exists as pure engineering hygiene
  against pathological infinite-regime worlds; the fixed-point stop is
  the principled terminator and the cap is never hit in eval.

Why this is not a mode, bridge, router, handler, or patch-treadmill
retry: it is the SAME single back-edge as v5 (prediction-vs-observation
contradiction drives revision), with the researcher-set constant REMOVED
rather than incremented. "One more retry" would be a patch; removing the
count entirely is architectural compression (fewer researcher-set
parameters, stopping condition derived from evidence). It fixes one
shift, two shifts, and N shifts by the same principle; it does not add
a per-failure handler.

Supporting changes (frozen, generic, no per-world content):
- L_wave exports a convergence signature per wave (res buffer extended:
  +52 nalive, +56 ne, +60 ne*5 rule bytes of the survivor; res grown
  64 -> 128 bytes) for the fixed-point comparison in L_run.
- Return encoding (v6): bits 0-5 final wave's v4-style mask; bits 8-10
  number of revision waves triggered; bit 11 fixed-point stop hit.
  A single-wave run (no revision) returns the v4-style mask unchanged,
  so frozen v4 world mains (which check m==63) keep working.
- D2 stays 9. L_DMAX stays 4. Candidate generation, L_find, DPDS, the
  ledger, the planners, the random controls, and all world interfaces
  are unchanged.

Implementation provenance (honest record): the v6 learner is adapted
from the uncommitted v5 working-copy implementation
(docs/lab/rsi/runs/wave-20261002-0221pdt/F2/f2v5_learner.zag), which was
NEVER executed against any sealed world (its sealed world was never
written). The v6 delta (loop + signature export + return encoding) is
applied AFTER this prereg's freeze commit. The base was compile-checked
and run once on the v4 C2-prime world pre-freeze (base validation:
PROGRAM_ALL_BARS_PASS, mask 63, identical ledger to the v4 sealed run);
no v6 sealed-world run exists before the freeze.

## 4. Why this goal is materially harder than v5's (anti-cosmetics)

The skeptic's attack is: "v6 is v5 with the cap removed; harder is
goalpost cosmetics." Four answers, each empirically checkable:

(a) v5 provably fails the v6 world. The v5-frozen mechanism (exactly
one revision) is calibrated on the sealed SHIFT2 world pre-eval (NC3,
section 9): it converges under Regime 1, its Regime-1 plan fails in
Regime 2, it revises once, its Regime-2 plan fails in Regime 3, and it
has no second revision path, so it reports PROGRAM_FAIL. The world
defeats v5 structurally (revision budget), not by a depth gap.

(b) No bound raise fixes it. D2=9, 10, or 100 all converge correctly
per-regime (the passive and discrimination evidence is genuinely each
regime's); the failure is revision budget, not depth. The "just raise
the bound" attack is provably wrong here, as in v5.

(c) The sustained structure is real and load-bearing. The goal
requires THREE outcome-linked experiment waves, where waves 2 and 3
are each CAUSED by the previous wave's failed execution (each
REVISION_TRIGGER cites the exact predicted-vs-actual mismatch). Each
wave's experiments are chosen sequentially with each choice justified
by prior outcomes (K6-R3). This is sustained multi-wave experiment
construction over a horizon, not a single distinguishing probe.

(d) The loop is not a blind retry and it terminates. Revisions fire
only on prediction-vs-observation contradiction under a converged
single survivor (not on any failure); each revision re-runs the FULL
discrimination machinery (not a plan tweak); the fixed-point stop
prevents infinite regress (tested by NC5); NC4 proves the loop does
NOT spuriously revise when one revision suffices.

## 5. Sealed worlds (fresh, sealed)

### 5.1 SHIFT2 (the v6 test world)

File: sealed/f2v6_world_shift2.zag.
sha256: 05e26e0854427b07fa3b0971f46d22cdec368f9d84bad1b6a057d05f730ca054
(recorded here at prereg freeze, before any v6-learner run).

Family: dual contextual delay (C2-prime family). Variables X=0
(controllable pulse), Y1=1, Y2=2 (effects), J=3, K=4 (declared
persistent context variables, controllable).

- Regime 1: (X -> Y1, delay 2, J == 1), (X -> Y2, delay 2, K == 1).
- Regime 2: (X -> Y1, delay 2, J == 1), (X -> Y2, delay 3, K == 1).
  (shift 1: Y2 delay 2 -> 3)
- Regime 3: (X -> Y1, delay 2, J == 1), (X -> Y2, delay 4, K == 1).
  (shift 2: Y2 delay 3 -> 4)
- Each shift lengthens Y2's delay by exactly one step past the previous
  regime's max delay, which provably breaks the previous regime's goal
  plan (the 3-step verification window loses its earliest step; the
  model's predicted SUFFIX observations then mismatch reality).
- The latches: the FIRST w_goal_setup call advances Regime 1 -> Regime 2
  (one-way); the 23rd w_goal_setup call (first goal setup of wave 2;
  each wave issues exactly 22 setup calls under the frozen learner
  protocol: 2 goal-phase + 20 random-control) advances Regime 2 ->
  Regime 3 (one-way); later calls are regime no-ops. Rationale: the
  goal-setup procedure reconfigures the apparatus mid-stream. The
  learner is never told; the latches are hidden world-side state
  (packed with the clock in the ws t-cell; w_reset preserves them).
- Passive: 18 steps (t = 0..17), X pulses at t = 3, 8, 13, J = 1 and
  K = 1 throughout. Regime-independent (all latches fire in goal
  phases, strictly after the passive).
- Goal setup (disclosed schema): J = 0, K = 0 (both WRONG).
- Goalvar interface: [Y1, Y2, J, K] with values [1, 1, 1, 1].
  Unchanged across regimes (the goal does not move; the laws do).
- w_plan_maxd = 12 (disclosed; the Regime-3 goal needs a length-11
  plan, the longest in the eval).
- w_verify returns the regime number (1, 2, 3) whose laws the survivor
  matches, 0 otherwise; it logs which. Signature unchanged from v4 so
  the frozen v4/v5 learners link unmodified.
- The world's main expects: final mask 63, exactly 2 revisions, no
  fixed-point stop (PROGRAM_ALL_BARS_PASS).

### 5.2 SHIFT1 (NC4 world: single shift)

File: sealed/f2v6_world_shift1.zag.
sha256: c0986c12fd3ad22366b37eb943927c1df7ba482557b18a75ccbae5f075dc6f5c

Identical to SHIFT2 except only the first latch exists (Regime 1 ->
Regime 2 on setup call #1; no second latch). Regimes: R1 (Y1 d2, Y2 d2),
R2 (Y1 d2, Y2 d3). The v6 binary must handle this with EXACTLY ONE
revision (mask 63, nrev=1): proves the loop stops when one revision
suffices (no spurious second revision).

### 5.3 OSC (NC5 world: oscillating regimes; DEV, not sealed)

File: sealed/f2v6_world_osc.zag.
sha256: 31c18f1598e58a35c86acf8c68f623ac1c3f89512d6a6532e939890cd20c2584

The latch alternates regimes (odd latch indices -> Regime 2, even ->
Regime 1) on setup calls #1, #23, #45, #67. The world never sits still.
Expected: wave 1 (R1 model, exec R2) contradicts and revises; wave 2
(R2 model, exec R1) contradicts and revises; wave 3 re-converges to
Regime-1 laws (already seen in wave 1) while its plan again contradicts
-> FIXED_POINT stop (bit 11), nrev=2, honest FAIL, no infinite regress.
The goal is unachievable in principle here; PASS would be wrong.

### Design provenance and seal discipline

The worlds were designed by this worker from the frozen C2 family spec;
their hashes are recorded above at prereg freeze, before any v6 run.
The v6 learner carries no shift-specific content (the loop is
regime-agnostic; verified by source audit). Anti-tuning evidence:
(i) this prereg (with hashes) is committed before any v6 run;
(ii) the v5-frozen mechanism is calibrated on SHIFT2 (NC3): it fails
exactly as required (one revision, then stuck), so the world is a
genuine double-shift test, not tuned for v6; (iii) the v6 binary is
verified on the v4 sealed suite (regression) and on SHIFT1 (NC4).

## 6. Sustained goal (frozen)

The learner must achieve the v4-style sustained predicate (three
consecutive steps with every goalvar at its goal value, verified by the
programmatic SUFFIX protocol) IN REGIME 3, after TWO hidden law changes.
Concretely: wave 1 converges under Regime 1 (w_verify=1); its plan
fails for real with a logged predicted-vs-actual contradiction; a first
revision wave runs (fresh passive + full re-discrimination in Regime 2,
w_verify=2); its plan fails for real with a logged contradiction; a
second revision wave runs (fresh passive + full re-discrimination in
Regime 3, w_verify=3); the re-planned sequence achieves the sustained
triple predicate for real; the random-action control achieves it 0/20.

## 7. Learner architecture (v5 loop + evidence-driven revision)

Identical to v5 (PREREG_F2V5 sections 3, 7) with the section-3 change
(evidence-driven loop replacing the one-revision cap, signature export,
v6 return encoding). D2=9, L_DMAX=4, standard depth 6, exactly-one-
OBSERVE DPDS, discrimination ledger, goal planners, random controls:
all unchanged.

## 8. Kill bars (numbered; frozen)

- K6-R1 (passive ambiguity): after the passive phase, at least 2
  hypotheses fully consistent with the passive trace, in EACH of the
  three waves. Fewer: FAIL.
- K6-R2 (construction, not enumeration): the source contains no finite
  list of complete experiments, distinguishing sequences, or goal plans
  (verified by source audit; construction is exclusively
  iterative-deepening composition over primitives, standard and
  pair-restricted, to the frozen bounds; SUFFIX is the preregistered
  programmatic protocol). The executed experiments differ in
  composition across the three waves. A complete experiment,
  distinguishing sequence, or goal plan found as a literal in source
  (other than programmatic SUFFIX construction): FAIL.
- K6-R3 (sequential justification): every executed experiment is
  logged with predicted observation vectors showing disagreement
  (per-hypothesis for standard rounds, per-pair for discrimination
  rounds), and the world-action counter proves zero real-world actions
  during search (only RESET plus the single selected execution per
  round). The discrimination ledger is complete in EACH wave. Each
  revision wave's experiments are justified by the previous wave's
  failure: each REVISION_TRIGGER log cites the specific
  predicted-vs-actual mismatch that caused it. An executed experiment
  without logged prior disagreement, any world action during search, a
  ledger gap, or a revision without a logged contradiction: FAIL.
- K6-R4 (convergence + two revisions): wave 1 terminates with exactly
  one survivor and w_verify returns 1 (Regime-1 laws); the wave-1 goal
  plan FAILS for real with a logged predicted-vs-actual contradiction;
  EXACTLY TWO revision waves run (no more, no fewer); wave 2 terminates
  with exactly one survivor and w_verify returns 2 (Regime-2 laws);
  the wave-2 goal plan FAILS for real with a logged contradiction;
  wave 3 terminates with exactly one survivor and w_verify returns 3
  (Regime-3 laws). Any deviation: FAIL.
- K6-R5 (model to goal): the wave-3 full plan (M + SUFFIX) achieves the
  sustained triple predicate for real (GOAL_REAL_C2 = 1, all twelve
  SUFFIX observations at goal values); AND the random-action control
  (7-symbol alphabet, length len(M) + 17, a priori seed 12345) achieves
  the predicate 0/20. Otherwise: FAIL.
- K6-R6 (observation economy): total active-phase OBSERVE actions on
  the SHIFT2 world is at most 110 (three waves; v5 allowed 70 for two);
  total across all eval worlds at most 300. More: FAIL.
- K6-R7 (determinism and purity): 3/3 runs byte-identical per world
  (cmp-verified); pure Zag (no Python at any stage; safebin toolchain
  guard in NAMECHECK.md Step 0); no em dashes in wave documentation.
  Otherwise: FAIL.
- K6-R8 (no regression): the v6 binary on v4's sealed suite (A-prime,
  C2-prime) passes all v4 bars (PROGRAM_ALL_BARS_PASS, mask 63) with
  zero revisions triggered. Otherwise: FAIL.

BUILD-PASS requires all eight bars. Any FAIL is BUILD-FAIL. No
promotion claims (promotion pipeline steps 4-11 remain for the parent
to schedule).

## 9. Negative controls (frozen)

- NC1 (random-action control): identical to K6-R5's control (kill bar).
- NC2 (memorization control; reported, not kill): passive-replay
  baseline (f2v6_nc2.zag, pure Zag): stores the passive trace, replays
  the memorized X-pulse cadence after one goal setup (latch fires, so
  the attempt runs in Regime 2 on Regime-1-memorized cadence), checks
  the sustained triple predicate on its real trajectory. Expected:
  NC2_RESULT 0. Rationale: separates storing traces (L0) from revising
  laws (L2); replay cannot construct the dense pulse burst the goal
  needs and cannot adapt to the shift.
- NC3 (mechanism ablation; VOID CONDITION): the pristine v5-base binary
  (one-revision cap; docs/lab/rsi/runs/wave-20261002-0221pdt/F2/
  f2v5_learner.zag, never modified) against the sealed SHIFT2 world.
  Expected: PROGRAM_FAIL (survives shift 1 via its one revision, then
  its Regime-2 plan fails in Regime 3 with no second revision path).
  If the v5-base binary PASSES SHIFT2, the world is not a genuine
  double-shift test and any v6 BUILD-PASS is VOID.
- NC4 (loop specificity): the v6 binary on SHIFT1 (single shift).
  Expected: PROGRAM_ALL_BARS_PASS with EXACTLY ONE revision (mask 63,
  nrev=1, no fixed-point stop). A second revision here would prove the
  loop over-revises.
- NC5 (terminator honesty): the v6 binary on OSC (alternating
  regimes). Expected: FIXED_POINT stop (bit 11 set, nrev=2), honest
  FAIL, no infinite regress. The goal is unachievable here; the test
  is that the loop terminates on evidence instead of looping forever.

## 10. Determinism standard

3/3 byte-identical reruns per world (cmp-verified). Zero randomness in
decision paths: no RNG in the learner; the only stochastic element is
the random-action control (frozen fixed-seed LCG, no feedback into
decisions). Revision triggers and the fixed-point comparison are
deterministic functions of the logged observations. Pair order,
alphabet orders, and first-hit selection are frozen.

## 11. Honest boundaries (what BUILD-PASS would and would not establish)

A BUILD-PASS would establish: the F2 loop with the evidence-driven
revision loop detects TWO hidden progressive mid-stream law changes,
each from a failed plan execution, re-discriminates on fresh evidence
each time, re-converges under each new regime, terminates its revisions
on evidence (goal met), and achieves the sustained goal under the final
regime, on a fresh sealed world; and it does not over-revise (NC4) and
terminates honestly when the world never settles (NC5). That is bounded
L2 structural learning with counterexample-driven revision.

It would NOT establish, and no claim to the contrary may be made:

- L3 representational invention. Against Criterion 0: (C0-A) FAILS
  (rule semantics researcher-authored); (C0-B) FAILS (solution space
  researcher-enumerated); (C0-C) NOT TESTED; (C0-D) partially met
  (models reused for planning within and across waves).
- Generality beyond the tested worlds. A targeted result, not a broad
  capability claim.
- That the loop handles arbitrary shifts. Tested: two specific
  progressive delay lengthenings (Y2 2->3->4) via goal-setup latches.
  Other shift types (gate flips, structural changes, gradual drift,
  shifts during discrimination) are not tested.
- That the loop is computationally cheap. The Regime-3 plan needs an
  11-action exhaustive search; wall-clock cost is reported, not hidden.

## 12. Governance

Pure Zag only. No Python anywhere in this wave. This prereg is frozen
before any v6 implementation run on the sealed worlds exists; the
coordinator commits it alone first (commit-order self-check: prereg
commit strictly precedes the implementation commit). Commits local on
tnn-native-lab; nothing is pushed. The builder reports BUILD-PASS or
BUILD-FAIL only, with the exact frozen bars named; no SURVIVES claim.

## 13. Architecture accounting (prereg step)

- Cognition source lines added: 0 (writing-only step).
- New hardcoded semantic cases: 0.
- New modes / bridges / routers: 0.
- New task-specific handlers: 0.
- New learner-state structures: 0 (the loop reuses the wave-local
  ledger and result buffer; the convergence signature is a wave-local
  export compared in L_run, no new persistent structure).
- The sealed worlds and NC substrates are authored test substrate, not
  cognition.
- Builder target: evidence-driven L_run loop + signature export +
  return encoding (section 3); builder reports the exact diff line
  count. No other mechanism changes.
