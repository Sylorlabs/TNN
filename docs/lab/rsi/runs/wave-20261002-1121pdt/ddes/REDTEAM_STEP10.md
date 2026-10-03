# STEP-10 RED TEAM: independent adversarial attack on the DDES t*=0 repair

Wave: wave-20261002-1121pdt. Lane: DDES. Queue item 5(a).
Prereg: PREREG_DDES_RT10.md, frozen alone at dd5d92f63 before any
implementation existed. Implementation: ddes_rt.zag (this directory),
written after the prereg commit; its mechanism functions
(compute_arrivals, compute_frontier, eff_waits, synthesize_plan,
emit_plan, predict, world_step, ddes_world) are byte-identical to the
frozen repair ddesr2.zag at b42b10db5 (verified by diff: first 353
lines identical, zero differences). Only world tables and the driver
are new. The red-team worker did not author the repair.

Target: the t*=0 soundness repair R2 (eff_waits clamp max(t*,1) in
synthesis and prediction; TSTAR-ZERO-BOUNDARY flag). Frozen repair
bars K-R2.1..K-R2.6 (d31e901b0) passed on World F plus A-E
regression (b42b10db5).

Red-team question: does the repair GENUINELY close the t*=0
silent-wrong-convergence hole (adversary finding e40bdfc9b, sealed
World F), or does it paper over it?

Binding caveats (restated; they bind every citation): (1) "a menu of
size 2 reproduces the sealed phase-2 outputs"; (2) "World G is
signature-identical to F by prereg design"; (3) "the
derivation-to-record binding is enforced by offline reviewer checks
only". Ceiling: bounded L2 guided generation, NOT L3. DDES-ALT H1/H3
already established the repair's decision substance is the clamp
alone (FLAG unconsumed); not re-litigated here.

## Attack battery (all worlds designed post-repair)

RT1 (multi-hop all-zero chain at t*=0; F had a single 0-delay rule):
H0=[(X,Z,0),(Z,Y,0)] vs H1=[(X,Z,0),(Z,Y,9)]. Frontier V*=Y t*=0.
RT2 (t*=0 negative control; both hypotheses predict 1 under the clamp
floor): H0=[(X,Z,0),(Z,Y,0)] vs H1=[(X,Z,0),(Z,Y,1)]. Predicted
LOUD-FAIL both configs.
RT3 (t*=0 with a decoy 0-delay rule Z to Y that never fires):
H0=[(X,Y,0),(Z,Y,0)] vs H1=[(X,Z,7),(Z,Y,0)]. Frontier V*=Y t*=0.
RT4 (t*=1 leading-zero-delay chain; BOUND probe, one tick outside the
clamp): H0=[(X,Z,0),(Z,Y,1)] vs H1=[(X,Z,0),(Z,Y,6)]. Predicted
SILENT-WRONG on cfg0, CORRECT on cfg1. At t*=1 the repaired mechanism
is line-identical to the unrepaired lineage (eff_waits(1)=1, flag
condition false), so RT4 probes a pre-existing lineage property.

## Build and determinism

- znc ddes_rt.zag -o ddes_rt_bin: exit 0, 93-byte stderr (the
  unconditional zagd-availability warning only), binary 46195 bytes.
- 3/3 runs byte-identical, exit 0, zero stderr bytes every run.
  Transcript sha256 (run_rt_1/2/3.txt):
  a8b1ce04009698b0f6c698937c6a502cc5f47ed6b16d814050430f451ce2a780
- 16 plans built (8 worlds x 2 configs). Zero randomness anywhere.

## Measured results vs frozen predictions

- RT1: TARGET V*=2 t*=0, FLAG, PLAN [S,W,OY] both configs; cfg0
  real=1 PRED 1/0 SURVIVE h0 CONVERGE-OK; cfg1 real=0 PRED 1/0
  ELIM h0 SURVIVE h1 CONVERGE-OK. Matches frozen rows exactly.
- RT2: TARGET V*=2 t*=0, FLAG, PLAN [S,W,OY]; PRED h0=1 h1=1 both;
  cfg0 real=1 SURVIVE/SURVIVE CONVERGE-FAIL; cfg1 real=0
  ELIM/ELIM CONVERGE-FAIL. Matches frozen rows exactly: the
  boundary degrades LOUDLY, never silently.
- RT3: TARGET V*=2 t*=0, FLAG, PLAN [S,W,OY]; cfg0 real=1 PRED 1/0
  SURVIVE h0 CONVERGE-OK; cfg1 real=0 ELIM h0 SURVIVE h1
  CONVERGE-OK. Matches frozen rows exactly.
- RT4: TARGET V*=2 t*=1, NO flag, PLAN [S,W,OY]; PRED h0=1 h1=0;
  cfg0 real=0 ELIM h0 (TRUE) SURVIVE h1 CONVERGE-OK claimed on the
  false hypothesis: SILENT-WRONG as predicted; cfg1 real=0 ELIM h0
  SURVIVE h1 CONVERGE-OK (correct). Matches frozen rows exactly.

Kill-bar check: RT-K1 (RT1+RT3 exact row match) HOLD. RT-K2 (RT2
loud both configs, no silent convergence) HOLD. RT-K3 (zero
silent-wrong cells across RT1/RT2/RT3) HOLD. RT-K5 (3/3
byte-identical, exit 0, zero stderr) HOLD. RT-K6 (pure Zag, dash
scan clean) HOLD.

## The paper-over question, answered

The red team could not construct any t*=0 silent-wrong. Stronger:
at t*=0 the repaired mechanism PROVABLY cannot be silently wrong
on this harness. Sketch: at t*=0 the frontier variable V* has
min arrival 0, so one hypothesis (wlog h0) has an all-zero-delay
path X to V*, which the execution model fully propagates within
the single clamped tick (0-delay cascade; chain depth at most 2
under n_vars=3, within the 3-pass budget), giving real=1, matching
p0=(0<=1)=1. The other hypothesis has arrival e>=1: if e>=2 its
prediction is 0 and real is 0 (tick-arrival >= analytic arrival by
induction on the firing rules, so no spurious activation within
one tick); if e=1 both predictions are 1 and the cell fails loud
(p0==p1). In every case the true hypothesis's prediction matches
real, or the cell fails loudly. The clamp plus the aligned
predictor genuinely close the t*=0 hole; the flag marks it. This
is not a paper-over of World F: three structurally novel t*=0
worlds (multi-hop chain, decoy, loud-fail control) all behave
exactly as the soundness argument predicts.

## BOUND: RT4 (recorded, does not affect the verdict)

RT4 cfg0 is SILENT-WRONG in the repaired binary, exactly as
frozen-predicted. Root cause: the analytic predictor's
delay-additive arrival model vs the execution model's tick
semantics. A 0-delay hop followed by a positive-delay hop needs
one more tick than the analytic arrival counts (Z activates at
tick 1 via the 0-delay rule; Z to Y with delay 1 needs tick 2;
analytic arrival[Y]=1 <= eff_waits(1)=1 predicts 1). This gap is
PRE-EXISTING in the lineage: the repair is the identity at t*>=1
(eff_waits(1)=1, no flag), so the unrepaired 56db8d606 lineage has
the identical RT4 decision lines. The repair never claimed to fix
predictor/execution alignment in general; its frozen bars scope to
World F plus A-E regression, which RT4 does not violate. Killing
the repair for RT4 would be moving the kill bar after the fact.
Disposition: BOUND on the repair's scope; queued as the next lane
hypothesis (predictor/execution tick-semantics alignment).

## Red-team verdict: SURVIVES

The t*=0 repair genuinely closes the t*=0 silent-wrong hole on
adversarial post-repair worlds, with the boundary failing loudly
(RT2) rather than silently wherever the clamp floor erases
discrimination. Zero regressions on the mechanism (diff-empty vs
b42b10db5). The RT4 bound is documented above and queued, not
counted against the repair. DDES remains bounded L2; no L3 claim;
no new modes, bridges, handlers, or semantic cases (harness only,
0 cognition lines).

## Architecture accounting (ONE-SYSTEM rule)

- New hardcoded semantic cases: 0. New modes: 0. New bridges: 0.
  New handlers: 0. Cognition lines added: 0 (test harness only).
