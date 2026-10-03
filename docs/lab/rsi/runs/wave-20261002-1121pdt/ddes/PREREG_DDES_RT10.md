# PREREG: DDES step-10 independent red team + adversary OOD probe on the t*=0 repair

Frozen before any implementation. Lane worker DDES, wave-20261002-1121pdt,
queue item 5. This prereg commits the attack/OOD world tables, the frozen
prediction rows, and the kill bars. Any amendment must be committed
transparently and re-frozen before implementation; no bar may be altered
after seeing results. Pure Zag only; no Python at any stage (a prereg
pre-authorizing Python tooling is VOID ON SIGHT).

## Provenance

NEW prereg, written by the wave-20261002-1121pdt DDES lane worker. The
worker did not author the t*=0 repair (repair R2: prereg d31e901b0,
implementation b42b10db5, wave-20260930-1121pdt recovery worker). All
twelve worlds below (RT1-RT4, P1-P4) were designed post-repair, in this
wave, specifically to attack or probe the repaired mechanism. The
mechanism under test is ddesr2.zag at b42b10db5; the test harness will
reuse its mechanism functions (compute_arrivals, compute_frontier,
eff_waits, synthesize_plan, predict, world_step, ddes_world) VERBATIM
and change only the world data tables and the driver. A diff of the
mechanism functions against b42b10db5 must show zero differences.

## Target and the question

Target: the t*=0 soundness repair R2 (eff_waits clamp max(t*,1) in both
synthesis and prediction, plus the TSTAR-ZERO-BOUNDARY flag). Frozen
repair kill bars K-R2.1..K-R2.6 (prereg d31e901b0) all passed on World F
plus Worlds A-E regression (b42b10db5, 3/3 byte-identical).

Red-team question (step 10): does the repair GENUINELY close the t*=0
silent-wrong-convergence hole, or does it paper over it? Attack with
adversarial t*=0-adjacent worlds designed post-repair. A paper-over
would show as silent-wrong convergence on a t*=0 world the repair's
development set did not include.

OOD question: the repair's development worlds are Worlds A-E
(single-hop X to V, positive delays, t* in {1,2,3,4}) and World F
(single 0-delay rule X to Y). The probe worlds below are structurally
unlike all of them and are frozen before running.

Binding caveats (restated; they bind every citation): (1) "a menu of
size 2 reproduces the sealed phase-2 outputs"; (2) "World G is
signature-identical to F by prereg design"; (3) "the derivation-to-record
binding is enforced by offline reviewer checks only". Ceiling for every
claim here: bounded L2 guided generation, NOT L3. DDES-ALT H1/H3
established the repair's decision substance is the clamp alone (the
FLAG marker is unconsumed: no branch reads it); nothing here re-litigates
that.

## Battery A: step-10 red-team worlds (adversarial, t*=0-adjacent)

Variables: X=0, Z=1, Y=2. Rules are (src, dst, delay). Each world runs
both truth configs (cfg0: truth = H0; cfg1: truth = H1).

RT1: multi-hop all-zero chain at t*=0 (F had a single 0-delay rule).
  H0 = [(X,Z,0),(Z,Y,0)]. H1 = [(X,Z,0),(Z,Y,9)].
  Arrivals H0: X=0 Z=0 Y=0. Arrivals H1: X=0 Z=0 Y=9.
  Frontier: Z agrees; Y 0 vs 9. V*=Y(2), t*=0, schema=1.
  Frozen prediction, cfg0: TARGET V*=2 t*=0 schema=1; FLAG
  TSTAR-ZERO-BOUNDARY floor=1; PLAN [S,W,OY]; EXEC real=1
  (zero chain propagates within the single tick); PRED h0=1 h1=0;
  SURVIVE h0; ELIM h1; CONVERGE-OK.
  Frozen prediction, cfg1: same TARGET/FLAG/PLAN; EXEC real=0;
  PRED h0=1 h1=0; ELIM h0; SURVIVE h1; CONVERGE-OK.

RT2: t*=0 negative control. Both hypotheses predict 1 after the
  clamp floor, so the mechanism must fail LOUD, never silent.
  H0 = [(X,Z,0),(Z,Y,0)]. H1 = [(X,Z,0),(Z,Y,1)].
  Arrivals H0: Z=0 Y=0. Arrivals H1: Z=0 Y=1.
  Frontier: Y 0 vs 1. V*=Y(2), t*=0, schema=1.
  Frozen prediction, cfg0: TARGET V*=2 t*=0 schema=1; FLAG;
  PLAN [S,W,OY]; EXEC real=1; PRED h0=1 h1=1; SURVIVE h0;
  SURVIVE h1; CONVERGE-FAIL (p0==p1, loud).
  Frozen prediction, cfg1: same TARGET/FLAG/PLAN/PRED; EXEC real=0
  (Z to Y delay 1 does not fire in one tick); ELIM h0; ELIM h1;
  CONVERGE-FAIL (loud).

RT3: t*=0 with a decoy 0-delay rule that never fires (F had no decoy).
  H0 = [(X,Y,0),(Z,Y,0)] (Z never active). H1 = [(X,Z,7),(Z,Y,0)].
  Arrivals H0: X=0 Z=INF Y=0. Arrivals H1: X=0 Z=7 Y=7.
  Frontier: Z INF vs 7 gives t=7; Y 0 vs 7 gives t=0. V*=Y(2),
  t*=0, schema=1.
  Frozen prediction, cfg0: TARGET V*=2 t*=0 schema=1; FLAG;
  PLAN [S,W,OY]; EXEC real=1; PRED h0=1 h1=0; SURVIVE h0;
  ELIM h1; CONVERGE-OK.
  Frozen prediction, cfg1: same TARGET/FLAG/PLAN; EXEC real=0;
  PRED h0=1 h1=0; ELIM h0; SURVIVE h1; CONVERGE-OK.

RT4: t*=1 leading-zero-delay chain (one tick outside the clamp;
  probes whether the predictor/execution alignment the repair
  relies on holds adjacent to the boundary). This is a BOUND probe:
  its outcome is recorded and does not pass/fail the repair, whose
  frozen bars scope to World F plus A-E regression.
  H0 = [(X,Z,0),(Z,Y,1)]. H1 = [(X,Z,0),(Z,Y,6)].
  Arrivals H0: Z=0 Y=1. Arrivals H1: Z=0 Y=6.
  Frontier: Z agrees; Y 1 vs 6. V*=Y(2), t*=1, schema=1. NO FLAG.
  The repaired mechanism is line-identical to the unrepaired
  mechanism at t*=1 (eff_waits(1)=1; flag condition false), so this
  probes a pre-existing lineage property, not a repair regression.
  Frozen prediction, cfg0: TARGET V*=2 t*=1 schema=1; no FLAG;
  PLAN [S,W,OY]; EXEC real=0 (Z activates at tick 1, Z to Y
  needs one more tick); PRED h0=1 h1=0 (arrival 1 <= 1); ELIM h0
  with h0 TRUE; SURVIVE h1; CONVERGE-OK claimed on the false
  hypothesis: SILENT-WRONG recorded.
  Frozen prediction, cfg1: same TARGET/PLAN/PRED; EXEC real=0;
  ELIM h0; SURVIVE h1; CONVERGE-OK (correct).

## Battery B: adversary OOD probe (structurally unlike A-F)

P1: t*=0 discriminating on Z, not Y (all repair-family worlds
  discriminate on Y, or on Z only with positive delays).
  H0 = [(X,Z,0)]. H1 = [(X,Z,4)].
  Arrivals H0: Z=0. Arrivals H1: Z=4. Y=INF both.
  Frontier: V*=Z(1), t*=0, schema=1. PLAN [S,W,OZ].
  Frozen prediction, cfg0: TARGET V*=1 t*=0 schema=1; FLAG;
  PLAN [S,W,OZ]; EXEC real=1; PRED h0=1 h1=0; SURVIVE h0;
  ELIM h1; CONVERGE-OK.
  Frozen prediction, cfg1: same TARGET/FLAG/PLAN; EXEC real=0;
  PRED h0=1 h1=0; ELIM h0; SURVIVE h1; CONVERGE-OK.

P2: t*=0 with coexisting 0-delay and positive-delay rules from X
  (F had a single rule).
  H0 = [(X,Y,0),(X,Z,2)]. H1 = [(X,Y,5),(X,Z,2)].
  Arrivals H0: Y=0 Z=2. Arrivals H1: Y=5 Z=2.
  Frontier: Z agrees; Y 0 vs 5. V*=Y(2), t*=0, schema=1.
  Frozen prediction, cfg0: TARGET V*=2 t*=0 schema=1; FLAG;
  PLAN [S,W,OY]; EXEC real=1; PRED h0=1 h1=0; SURVIVE h0;
  ELIM h1; CONVERGE-OK.
  Frozen prediction, cfg1: same TARGET/FLAG/PLAN; EXEC real=0;
  PRED h0=1 h1=0; ELIM h0; SURVIVE h1; CONVERGE-OK.

P3: t*=0 with INF arrival on the observed variable under one
  hypothesis (frontier picks Z; Y agrees at 0).
  H0 = [(X,Y,0)]. H1 = [(X,Z,0),(Z,Y,0)].
  Arrivals H0: X=0 Z=INF Y=0. Arrivals H1: X=0 Z=0 Y=0.
  Frontier: Y agrees at 0; Z INF vs 0 gives t=0. V*=Z(1), t*=0,
  schema=1. PLAN [S,W,OZ].
  Frozen prediction, cfg0: TARGET V*=1 t*=0 schema=1; FLAG;
  PLAN [S,W,OZ]; EXEC real=0 (Z never active); PRED h0=0 h1=1;
  SURVIVE h0; ELIM h1; CONVERGE-OK.
  Frozen prediction, cfg1: same TARGET/FLAG/PLAN; EXEC real=1;
  PRED h0=0 h1=1; ELIM h0; SURVIVE h1; CONVERGE-OK.

P4: t*=0 competing frontiers (Z and Y both disagree at t*=0;
  tie-break picks the lowest variable id, Z).
  H0 = [(X,Z,0),(X,Y,3)]. H1 = [(X,Z,5),(X,Y,0)].
  Arrivals H0: Z=0 Y=3. Arrivals H1: Z=5 Y=0.
  Frontier: Z 0 vs 5 at t=0; Y 3 vs 0 at t=0; tie-break to Z.
  V*=Z(1), t*=0, schema=1. PLAN [S,W,OZ].
  Frozen prediction, cfg0: TARGET V*=1 t*=0 schema=1; FLAG;
  PLAN [S,W,OZ]; EXEC real=1; PRED h0=1 h1=0; SURVIVE h0;
  ELIM h1; CONVERGE-OK.
  Frozen prediction, cfg1: same TARGET/FLAG/PLAN; EXEC real=0;
  PRED h0=1 h1=0; ELIM h0; SURVIVE h1; CONVERGE-OK.

## Aggregate frozen prediction

16 cells (8 worlds x 2 configs), 16 plans built. SUMMARY
ok=14/16 plans_built=16 (the two RT2 cells return CONVERGE-FAIL,
counted 0). FLAG TSTAR-ZERO-BOUNDARY floor=1 appears on every
t*=0 cell (14 cells) and on no t*=1 cell (2 cells).

## Kill bars

- RT-K1 (repair holds on novel t*=0 structure): RT1 and RT3 match
  their frozen prediction rows exactly on both configs
  (decision lines: TARGET, FLAG, PLAN, EXEC, PRED, ELIM/SURVIVE,
  CONVERGE). Kill: any decision-line mismatch on any of the 4 cells.
- RT-K2 (boundary degrades loudly): RT2 matches its frozen rows on
  both configs: CONVERGE-FAIL with SURVIVE/SURVIVE (cfg0) and
  ELIM/ELIM (cfg1). Kill: any CONVERGE-OK on RT2, or any cell
  where the true hypothesis is eliminated while convergence is
  claimed.
- RT-K3 (no silent-wrong at t*=0): zero cells across RT1, RT2, RT3
  where the true hypothesis is eliminated AND CONVERGE-OK is
  printed. Kill: any such cell. This is the paper-over detector.
- RT-K4 (bound probe): RT4's frozen rows are recorded as a BOUND
  finding. The repair SURVIVES/KILLED verdict does not depend on
  RT4. Kill: n/a (informational).
- RT-K5 (determinism): 3/3 runs byte-identical (sha256 match),
  exit 0, zero stderr bytes every run. Kill: any divergence,
  nonzero exit, or any stderr byte.
- RT-K6 (purity): pure Zag only, zero Python at any stage; zero
  em-dash and zero en-dash bytes in all committed files
  (check_no_dash.sh). Kill: any Python use or forbidden byte.
- OOD-K1 (probe correctness): P1-P4 match their frozen prediction
  rows exactly on both configs (8 cells). Kill: any
  decision-line mismatch.
- OOD-K2 (boundary flagged on novel structure): the exact line
  FLAG TSTAR-ZERO-BOUNDARY floor=1 appears between TARGET and PLAN
  on all 8 P cells. Kill: absent on any P cell.

## Verdict rule (frozen)

The t*=0 repair SURVIVES iff RT-K1, RT-K2, RT-K3, OOD-K1, OOD-K2
hold with RT-K5 and RT-K6 clean. RT4 is reported as a BOUND on
the repair's scope regardless of outcome. If any of RT-K1..K3 or
OOD-K1/K2 fails, the verdict is KILLED with the failing cell
cited. Builders report BUILD-PASS/BUILD-FAIL only; the
SURVIVES/KILLED verdict is the red-team verdict.

## Commit order

This prereg is committed alone. The implementation commit must be
a strict descendant. Verified via git merge-base --is-ancestor
before any verdict is reported.
