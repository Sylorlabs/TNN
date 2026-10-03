# PREREG (FROZEN): DDES steps 7 (OOD test) and 8 (ablation)

Wave: wave-20261002-0521pdt. Lane: DDES.
Status: FROZEN before any step-7/8 implementation is written.
Committed alone before any .zag file for this lane exists.
This prereg covers promotion-pipeline steps 7 and 8 only.
No SURVIVES claim. Ceiling stays bounded L2 with persistence.
NOT L3.

## Binding context (frozen facts, not re-argued here)

- DDES V2 BUILD-PASS stands FROZEN for steps 1-5; DDES-ALT step 6
  BUILD-PASS with verdicts: H1 ATTACK-SUCCEEDS (clamp is the whole
  decision substance of the repair; the FLAG marker is unconsumed),
  H2 EVIDENCE-HOLDS (guidance builds menu-exceeding plans where the
  frozen baseline loud-fails), H3 ATTACK-SUCCEEDS (RT2 loud failure
  is a harness coincidence alarm x clamp interaction).
- The three binding citation caveats from the frozen DDES line:
  (1) "a menu of size 2 reproduces the sealed phase-2 outputs"
  (2) "World G is signature-identical to F by prereg design"
  (3) "the derivation-to-record binding is enforced by offline
  reviewer checks only"
- The DDES-ALT H1(b) rule binds this lane: ablation equivalence
  and difference are judged on DECISION lines only
  (TARGET, PLAN, EXEC, PRED, ELIM/SURVIVE, CONVERGE, CELLSUM).
  FLAG/print-only lines are excluded from both equivalence and
  difference claims.

## Frozen semantics (shared by every cell)

- Variables: X=0, Z=1, Y=2. S stimulates X at t=0 and fires no
  rules. W advances one tick; a rule (src,dst,delay) fires at the
  first W tick t with t - ts[src] >= delay while src is active
  (multi-pass per tick, so chains propagate within one tick).
- Arrival computation: Bellman-style relaxation over n_vars
  passes from the stimulated schema; frontier = earliest
  min(a0,a1) over variables with a0 != a1.
- Plan synthesis: [S] + w waits + O(V*), where w is the wait
  policy under test and O(V*) is OX/OY/OZ for V*=0/2/1.
- Predictor: variable v is predicted active iff
  arrival(v) <= w under the same wait policy.
- Convergence: CONVERGE-OK iff predictions differ (p0 != p1) and
  exactly one matches the executed real observation; else
  CONVERGE-FAIL (loud). CELLSUM VERDICT=CORRECT iff both configs
  converge with the true hypothesis surviving; SILENT-WRONG iff
  both converge but the true hypothesis was eliminated in some
  config; LOUD-FAIL otherwise.
- Zero randomness anywhere in the decision path. No baseline in
  this lane (step 5 / DDES-ALT H2 already cover it).

## Step 7: OOD sealed worlds (all fresh, none from F/A/H/K/RT1/RT2,
## P/Q/W1/W2/W4/W5/W5p/RT2a-d)

Structurally different from the training/repair families:
two-hop chains, longer t* horizons, decoy rules, competing
frontiers, fan-in convergence, one chain-shaped boundary world
as a negative control. Partial observability in this lane means
the discriminating difference propagates through an intermediate
variable whose arrival times are identical across hypotheses, so
a one-hop observer of the intermediate sees no difference.

- O1 (two-hop chain, indirect discrimination):
  H0=[(X,Y,2),(Y,Z,3)] H1=[(X,Y,2),(Y,Z,5)].
  Arrivals: Z: 5 vs 7; Y: 2 vs 2 (no difference).
  Frontier V*=Z=1, t*=5, schema=1. No FLAG.
- O2 (long horizon, t*=12):
  H0=[(X,Y,12)] H1=[(X,Y,16)].
  Frontier V*=Y=2, t*=12, schema=1. No FLAG.
- O3 (competing frontiers):
  H0=[(X,Y,0),(X,Z,6)] H1=[(X,Y,3),(X,Z,2)].
  Frontier Y: min(0,3)=0; frontier Z: min(6,2)=2.
  Earliest V*=Y=2, t*=0, schema=1. FLAG expected.
- O4 (two-hop chain plus decoy direct rule):
  H0=[(X,Y,1),(Y,Z,2),(X,Z,9)] H1=[(X,Y,1),(Y,Z,4),(X,Z,9)].
  Arrivals: Y: 1 vs 1 (no difference); Z: 3 vs 5
  (the (X,Z,9) decoy is dominated in both hypotheses).
  Frontier V*=Z=1, t*=3, schema=1. No FLAG.
- O5 (fan-in convergence):
  H0=[(X,Y,1),(X,Z,1),(Y,Z,1)] H1=[(X,Y,1),(X,Z,3),(Y,Z,1)].
  Arrivals: Y: 1 vs 1 (no difference); Z: 1 vs 2.
  Frontier V*=Z=1, t*=1, schema=1. No FLAG.
- O6 (chain-shaped boundary world, negative control):
  H0=[(X,Y,0),(Y,Z,0)] H1=[(X,Y,0),(Y,Z,1)].
  Arrivals: Z: 0 vs 1. Frontier V*=Z=1, t*=0, schema=1.
  FLAG expected. This is the RT2-shaped outcome on a chain
  world: the clamp floor of 1 wait makes both predictions
  coincide (p0=p1=1), so loud failure is the predicted honest
  outcome, NOT silent-wrong.

## Step 7 prediction table (variant V_full, decision lines)

- O1: TARGET V*=1 t*=5 schema=1. PLAN [S,W,W,W,W,W,OZ].
  cfg0: EXEC real=1, PRED h0=1 h1=0, SURVIVE h0, ELIM h1,
  CONVERGE-OK. cfg1: EXEC real=0, PRED h0=1 h1=0, ELIM h0,
  SURVIVE h1, CONVERGE-OK. CELLSUM VERDICT=CORRECT.
- O2: TARGET V*=2 t*=12 schema=1. PLAN [S,12xW,OY].
  cfg0: real=1, PRED 1/0, SURVIVE/ELIM, CONVERGE-OK.
  cfg1: real=0, PRED 1/0, ELIM/SURVIVE, CONVERGE-OK.
  CELLSUM VERDICT=CORRECT.
- O3: TARGET V*=2 t*=0 schema=1. FLAG TSTAR-ZERO-BOUNDARY
  floor=1. PLAN [S,W,OY].
  cfg0: real=1, PRED 1/0, SURVIVE/ELIM, CONVERGE-OK.
  cfg1: real=0, PRED 1/0, ELIM/SURVIVE, CONVERGE-OK.
  CELLSUM VERDICT=CORRECT.
- O4: TARGET V*=1 t*=3 schema=1. PLAN [S,W,W,W,OZ].
  cfg0: real=1, PRED 1/0, SURVIVE/ELIM, CONVERGE-OK.
  cfg1: real=0, PRED 1/0, ELIM/SURVIVE, CONVERGE-OK.
  CELLSUM VERDICT=CORRECT.
- O5: TARGET V*=1 t*=1 schema=1. PLAN [S,W,OZ].
  cfg0: real=1, PRED 1/0, SURVIVE/ELIM, CONVERGE-OK.
  cfg1: real=0, PRED 1/0, ELIM/SURVIVE, CONVERGE-OK.
  CELLSUM VERDICT=CORRECT.
- O6: TARGET V*=1 t*=0 schema=1. FLAG TSTAR-ZERO-BOUNDARY
  floor=1. PLAN [S,W,OZ].
  cfg0: real=1, PRED h0=1 h1=1, SURVIVE h0, SURVIVE h1,
  CONVERGE-FAIL. cfg1: real=0, PRED h0=1 h1=1, ELIM h0,
  ELIM h1, CONVERGE-FAIL. CELLSUM VERDICT=LOUD-FAIL.

### Step 7 kill bars (frozen)

- BUILD-PASS iff ALL of: (7a) 3/3 runs byte-identical
  (sha256 recorded), exit 0 every run, zero stderr bytes every
  run; (7b) every world's decision-line sequence matches its
  prereg prediction row exactly (TARGET, FLAG presence, PLAN,
  EXEC, PRED, ELIM/SURVIVE, CONVERGE, CELLSUM); (7c) zero
  SILENT-WRONG CELLSUMs across the 6 worlds x 2 configs.
- PARTIAL iff (7a) and (7c) hold but at least one world fails
  to match its predicted decision-line row. The divergence is
  reported as the finding; per the no-patch-treadmill rule it is
  clustered by shared architectural cause, never patched with a
  benchmark-specific case.
- BUILD-FAIL iff any SILENT-WRONG occurs, or runs are not
  byte-identical, or any crash/nonzero exit.

## Step 8: ablation design

Guidance components under test (the three named by the wave
task; the FLAG marker stays out of scope per DDES-ALT H1(b),
already settled as unconsumed):

- C1 (clamp): eff_waits = max(t*,1) in synthesis and prediction.
  Removed: identity waits (t*).
- C2 (t*-derived wait counts): wait count derived from the
  arrival analysis. Removed: fixed wait count w=2 in synthesis
  and prediction (w=2 is inside the frozen baseline menu and is
  distinct from the clamp floor of 1, so the removal is
  distinguishable from C1 removal on t*=0 worlds).
- C3 (earliest-frontier V* selection): the discriminating
  variable with the minimal min-arrival. Removed: anti-frontier
  selection (maximal min-arrival; strict-greater tie-break).

Controlled variants (derivation code otherwise unchanged):

- V_full: C1 + C2 + C3 (the frozen guided derivation).
- V_noclamp: C1 removed (identity waits), C2 + C3 kept.
- V_nowaitderiv: C2 removed (fixed w=2), C1 + C3 kept.
- V_nofrontier: C3 removed (anti-frontier), C1 + C2 kept.
- V_none: C1 + C2 + C3 all removed (fixed w=2, anti-frontier).

The FLAG marker is still emitted when best_t == 0 in all
variants (print-only; excluded from all comparisons per the
H1(b) rule).

## Step 8 prediction table (decision lines, vs V_full)

- V_noclamp: identical decision lines to V_full on O1, O2, O4,
  O5 (t* >= 1 makes the clamp the identity there). On O3:
  plan [S,OY], cfg0 EXEC real=0, PRED 1/0, ELIM h0 with h0
  true, CONVERGE-OK claimed on h1: SILENT-WRONG. On O6:
  plan [S,OZ], cfg0 EXEC real=0, PRED 1/0, ELIM h0 true,
  SILENT-WRONG (flips the predicted LOUD-FAIL).
  Predicted component verdict: LOAD-BEARING.
- V_nowaitderiv: on O1, O2, O4, O5 the fixed w=2 horizon
  cannot reach the derived t* (5, 12, 3, 4): PRED h0=0 h1=0,
  p0==p1, CONVERGE-FAIL: LOUD-FAIL on all four (verdict flip
  from CORRECT). On O3: plan [S,W,W,OY], PRED 1/0, CORRECT
  both configs (same verdict, longer plan). On O6:
  plan [S,W,W,OZ], PRED 1/1, LOUD-FAIL (same verdict).
  Predicted component verdict: LOAD-BEARING.
- V_nofrontier: identical to V_full on O1, O2, O4, O5, O6
  (single discriminating frontier each). On O3 the anti-frontier
  picks Z at t*=2: plan [S,W,W,OZ], PRED h0=0 h1=1, CORRECT
  both configs (different experiment, same verdict).
  Predicted component verdict: PARTIALLY-LOAD-BEARING.
- V_none: O1, O2, O4, O5 LOUD-FAIL (fixed w=2 cannot reach
  t*); O3 CORRECT with plan [S,W,W,OZ]; O6 LOUD-FAIL.
  Predicted: no better than the worst single removal (4 verdict
  flips, matching V_nowaitderiv; no positive interaction).

### Step 8 mechanical component-verdict rule (frozen)

Applied per component on the 6 sealed OOD worlds, V_x vs
V_full on decision lines only (FLAG lines and variant labels
excluded from the comparison):

- LOAD-BEARING: removing it alone changes at least one world's
  CELLSUM verdict relative to V_full on the same world.
- DECORATIVE: decision lines byte-identical to V_full on all
  6 worlds.
- PARTIALLY-LOAD-BEARING: neither (decision lines change on
  at least one world but no CELLSUM verdict flips).

### Step 8 kill bars (frozen)

- BUILD-PASS iff ALL of: (8a) every variant x every world x
  3 runs byte-identical within cell, exit 0, zero stderr;
  (8b) every component receives a verdict by the mechanical
  rule above, computed from the measured transcripts;
  (8c) the recorded verdict table is faithful: every claimed
  verdict flip is backed by a decision-line diff, and every
  decision-line diff carrying a verdict flip is recorded;
  (8d) V_none performs no better than the worst single removal
  (its flip count <= max single-removal flip count).
- PARTIAL iff (8a) holds but a predicted flip fails to
  materialize, while (8b)-(8d) still resolve mechanically.
  The miss is reported as the finding.
- BUILD-FAIL iff non-determinism anywhere, or an uncounted
  SILENT-WRONG, or the table is unfaithful.

## Execution and determinism (frozen)

- One binary from ddes_78.zag via plain znc (no
  instrumentation). Build stderr expected: exactly the 93-byte
  unconditional zagd-availability warning. Exit 0.
- Every variant x world cell run 3/3; transcripts
  byte-identical across the three runs (sha256 recorded in
  SEALED_EVAL.md). Run stderr: 0 bytes every run.
  Exit 0 every run.
- Main runs the full matrix: 5 variants x 6 worlds x 2 configs
  in one deterministic transcript. Step 7 reads the V_full
  rows; step 8 reads all rows.

## Governance (frozen)

- Pure Zag at every stage; safebin PATH in every shell; zero
  em-dash and zero en-dash bytes in all lane files (byte-checked
  with check_no_dash.sh before each commit).
- Commits only under
  docs/lab/rsi/runs/wave-20261002-0521pdt/DDES/ with an explicit
  pathspec; no push; no promotion claims; verdicts name the exact
  frozen bars that governed them.
- New hardcoded semantic cases: 0 expected. New modes: 0.
  New bridges: 0. New handlers: 0. (ONE-SYSTEM accounting; the
  variants are controlled single-policy ablations of the frozen
  derivation machinery, not new machinery.)
- If step 7 fails on any world, the no-patch-treadmill rule
  applies: cluster by shared architectural cause; do not add
  benchmark-specific cases, opcodes, modes, or bridges.
- This prereg is committed ALONE. The implementation
  (ddes_78.zag) is written only after the prereg commit lands.
