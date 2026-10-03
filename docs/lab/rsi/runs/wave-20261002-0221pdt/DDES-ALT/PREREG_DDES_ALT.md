# PREREG (FROZEN): DDES-ALT alternative-explanation attack on the t*=0 repair

Wave: wave-20261002-0221pdt. Lane: DDES-ALT (promotion step 6).
Status: FROZEN before any attack implementation is written.
Committed alone before any .zag file for this lane exists.
This prereg covers pipeline step 6 (alternative-explanation
attack) only. No SURVIVES claim. A successful attack does not
retroactively void the steps 4+5 BUILD-PASS; that is coordinator
business. Builders report BUILD-PASS/BUILD-FAIL only for the
attack lane itself.

## The three BINDING citation caveats (restated verbatim)

(1) "a menu of size 2 reproduces the sealed phase-2 outputs"
(2) "World G is signature-identical to F by prereg design"
(3) "the derivation-to-record binding is enforced by offline reviewer checks only"

Omitting any caveat when citing the frozen DDES V2 BUILD-PASS
is misrepresentation. This attack neither removes nor weakens
them.

## Background (frozen facts, not re-argued here)

- DDES V2 BUILD-PASS stands FROZEN: t*=0 hole closed by the
  repair (eff_waits clamp = max(t*,1), load-bearing per the
  no-clamp ablation, plus the FLAG TSTAR-ZERO-BOUNDARY loud
  marker); RT2 fails loudly, not silently wrong; steps 4+5
  reproduced byte-identically with per-world baseline parity
  (4 correct + 2 loud-fail on both sides).
- Ceiling: strong L2 guided generation with persistence. NOT L3.
- The repair, as frozen, consists of exactly two parts: (i) the
  uniform clamp eff_waits(t*) = max(t*,1) applied identically in
  plan synthesis and in prediction, and (ii) the FLAG marker
  emitted when the derived target t* equals 0. No other code
  branches on t* == 0 anywhere in the frozen source; the marker
  value tstar_zero is written into the persisted record and
  printed, but no branch in the frozen source consumes it.

## Attack hypotheses (all three are tested; the attack may fail)

- H1 (clamp vacuous): the repair passes because the clamp makes
  the dangerous case unreachable, not because DDES reasons about
  t*=0. The FLAG marker is cosmetic: no downstream decision
  consumes it.
- H2 (guidance adds nothing): the baseline parity (identical
  per-world verdicts on all 6 sealed worlds) means the guided
  component adds nothing over unguided synthesis; test whether
  guidance changes WHICH experiments are built, not just the
  verdicts, on fresh sealed worlds.
- H3 (RT2 loud failure is harness, not DDES): RT2's loud
  CONVERGE-FAIL is fully explained by the clamp x delay-contract
  interaction; DDES has no indistinguishability detector of its
  own (the p0==p1 alarm is a generic coincidence alarm).

## Frozen design constraints (shared by all three attacks)

- Pure Zag. New file ddes_alt.zag written only after this prereg
  is committed. It re-implements the frozen DDES V2 derivation
  machinery (arrival computation, frontier scan, plan synthesis,
  predictor, world simulator) with the exact frozen semantics,
  plus controlled variants (see below) and the frozen baseline
  (xorshift32 seed 14500418, B=64, 9 shapes, first discriminating
  candidate, same simulator).
- All fresh worlds use single-hop rules from X only
  (src = X = 0). This keeps the baseline simulator and the DDES
  world stepper in exact agreement (both measure delay from the
  stimulus tick), so guided and baseline verdicts are comparable.
  No chains, no multi-hop rules in this lane.
- Variables: X=0, Z=1, Y=2. S stimulates X at t=0 and fires no
  rules. W advances one tick; a rule (src,dst,delay) fires at the
  first W tick t with t - ts[src] >= delay while src is active.
  OX/OY/OZ read X/Y/Z. Truth: cfg0 runs the H0 rule table,
  cfg1 runs the H1 rule table (same convention as the frozen lane).
- Sealed worlds: every world below is defined HERE, in this
  frozen prereg, before implementation. None is drawn from the
  frozen DDES evaluation set (F, A, H, K, RT1, RT2); RT2a below
  re-uses the frozen RT2 contract only as the H3 control.

## H1 design: clamp-vacuity attack

Fresh sealed worlds:

- P (clamp load-bearing, t*=0, structurally unlike F/H):
  H0 = [(X,Y,0),(X,Z,9)] (decoy second rule, delay 9, present in
  both hypotheses), H1 = [(X,Y,4),(X,Z,9)].
  Arrival analysis: H0: Y=0, Z=9. H1: Y=4, Z=9.
  Frontier: V*=Y=2, t*=min(0,4)=0. FLAG expected.
- Q (clamp provably irrelevant: t*=1, so max(t*,1) = t*):
  H0 = [(X,Y,1)], H1 = [(X,Y,3)].
  Arrival analysis: H0: Y=1. H1: Y=3.
  Frontier: V*=Y=2, t*=min(1,3)=1. No FLAG expected.

Controlled DDES variants (DDES derivation code otherwise
unchanged; exactly one part removed each):

- V_full: clamp max(t*,1) + FLAG emission (the frozen repair).
- V_nomarker: clamp kept, FLAG emission line removed.
- V_noclamp: FLAG kept, eff_waits replaced by the identity
  (waits = t*), in both synthesis and prediction.

H1 experiment matrix (each cell run on both configs):

1. V_noclamp on P: must show the hole re-opened on fresh P
   (plan [S,OY], ELIM h0 on cfg0 with h0 true, convergence
   claimed on h1 = SILENT-WRONG). This establishes P as a valid
   "clamp is the only thing preventing silent-wrong" world.
2. V_full on P: FLAG + plan [S,W,OY] + CONVERGE-OK both configs.
3. V_nomarker on P: transcript must be line-identical to cell 2
   after removing FLAG lines (mechanical diff, empty).
4. V_full on Q: no FLAG, plan [S,W,OY], CONVERGE-OK both configs;
   decision-line sequence must match P's modulo the FLAG line
   and the t* value (same plan shape, same convergence pattern).

Predictions (labeled, not kill bars): cell 1 SILENT-WRONG on
cfg0; cell 3 diff empty; cell 4 matches cell 2 modulo FLAG.

### H1 kill bars (frozen)

- ATTACK-SUCCEEDS iff ALL of: (a) V_noclamp on P yields
  SILENT-WRONG on cfg0 (plan [S,OY], predictor h0=1/h1=0, real
  0, ELIM h0 with h0 true, CONVERGE claimed on h1); AND
  (b) the mechanical diff of V_nomarker-on-P vs V_full-on-P,
  after removing FLAG lines, is EMPTY (every TARGET, PLAN,
  EXEC, PRED, ELIM/SURVIVE, CONVERGE line byte-identical, so
  the marker changes no decision, plan, prediction, or record);
  AND (c) V_full on Q yields no FLAG line, plan [S,W,OY], and
  CONVERGE-OK on both configs, with the decision-line sequence
  matching P's modulo the FLAG line and t* value.
- EVIDENCE-HOLDS iff any sealed world in this lane shows a
  t*=0-specific decision-relevant behavior not entailed by the
  uniform max(t*,1) clamp (a different V* selection, schema
  switch, plan shape, or prediction at t*=0), or V_nomarker
  changes any decision-relevant line on P.
- Interpretation if ATTACK-SUCCEEDS: the repair's decision
  substance is the clamp alone; DDES performs no reasoning
  about t*=0 beyond max(t*,1) plus an unconsumed print. This
  does not dispute that the clamp is load-bearing (cell 1
  re-confirms it on a fresh world); it kills any reading of
  the repair as DDES "reasoning about" the boundary.

## H2 design: experiment-selection divergence

Fresh sealed worlds (guided V_full vs frozen-spec baseline):

- W1: H0=[(X,Y,0)] H1=[(X,Y,2)].
  Predicted: frontier V*=2 t*=0, FLAG, guided [S,W,OY];
  baseline shapes with w=1,OY only discriminate ([S,W,OY]).
  Predicted: same shape, both CORRECT (parity point).
- W2: H0=[(X,Y,3)] H1=[(X,Y,5)].
  Predicted: frontier V*=2 t*=3, no FLAG, guided [S,W,W,W,OY]
  CORRECT; baseline menu caps at w=2, zero discriminating
  candidates in 64 draws, LOUD-FAIL (guidance-exclusive win:
  t*-derived wait count exceeds the fixed menu).
- W4: H0=[(X,Y,1),(X,Z,0)] H1=[(X,Y,2),(X,Z,3)].
  Predicted: frontier V*=Z=1 t*=0 (Z: 0 vs 3 beats Y: 1 vs 2),
  FLAG, guided [S,W,OZ] CORRECT; baseline discriminating shapes
  are [S,W,OZ], [S,W,OY], [S,W,W,OZ]; first in PRNG order wins.
  Predicted: selection divergence likely, both CORRECT.
- W5: H0=[(X,Z,4)] H1=[(X,Z,6)].
  Predicted: frontier V*=1 t*=4, guided [S,W,W,W,W,OZ] CORRECT;
  baseline LOUD-FAIL (menu cap again; guidance-exclusive win).
- W5p: H0=[(X,Y,2),(X,Z,0)] H1=[(X,Y,2),(X,Z,2)] (Y rules are
  decoys, identical across hypotheses).
  Predicted: frontier V*=1 t*=0, FLAG, guided [S,W,OZ];
  baseline only [S,W,OZ] discriminates. Predicted: same shape,
  both CORRECT (parity point with decoys present).

Baseline runs the frozen spec exactly: 9 shapes ([S] + w in
0..2 waits + OX/OY/OZ), xorshift32 seed 14500418 chained across
worlds in prereg order W1, W2, W4, W5, W5p, B=64 draws, first
discriminating candidate selected, else NO-DISCRIMINATING-PLAN.
Verdict per world from its own simulator (single-hop worlds:
identical to the DDES stepper).

Frozen metrics:

- divergence_rate = (worlds where both built a plan AND shapes
  differ) / (worlds where both built a plan).
- guidance_exclusive = worlds where guided is CORRECT and the
  baseline is not CORRECT.
- baseline_exclusive = worlds where the baseline is CORRECT and
  guided is not CORRECT.

Predictions (labeled): divergence_rate = 1/3 (W4 only; W1 and
W5p same shape); guidance_exclusive = 2 (W2, W5);
baseline_exclusive = 0.

### H2 kill bars (frozen)

- ATTACK-SUCCEEDS iff guidance_exclusive == 0 AND
  baseline_exclusive == 0 AND divergence_rate == 0: per-world
  verdicts AND selected experiment shapes identical on every
  fresh world, so the parity extends from verdicts to experiment
  selection and guidance adds nothing measurable.
- EVIDENCE-HOLDS iff guidance_exclusive >= 1 OR
  divergence_rate > 0 with guided selecting a strictly more
  efficient (fewer waits) or menu-exceeding CORRECT plan.
  (baseline_exclusive >= 1 is reported as-is; not predicted.)
- Honest reading if EVIDENCE-HOLDS: the measured guidance
  contribution is the t*-derived wait count (adapting experiment
  length to the derived target) plus V* selection under
  competing frontiers. This is narrow, bounded L2 machinery;
  it says nothing about L3.

## H3 design: RT2 loud-failure provenance

Control and contract variants (DDES code unchanged across
RT2a/RT2b/RT2c; only the delay tables change):

- RT2a (frozen contract, control): H0=[(X,Y,1)] H1=[(X,Y,0)]
  on V_full. Predicted: reproduces the frozen outcome: FLAG,
  plan [S,W,OY], PRED h0=1 h1=1 (p0==p1), CONVERGE-FAIL loud
  on both configs.
- RT2b (widen the gap): H0=[(X,Y,2)] H1=[(X,Y,0)] on V_full.
  Predicted: frontier V*=2 t*=0, FLAG, plan [S,W,OY],
  PRED h0=0 (2<=1 false) h1=1, real cfg0 0 / cfg1 1,
  CONVERGE-OK both configs. The loud failure vanishes with only
  delay values changed.
- RT2c (same gap of 1, shifted off the boundary):
  H0=[(X,Y,2)] H1=[(X,Y,1)] on V_full.
  Predicted: frontier V*=2 t*=1, no FLAG, plan [S,W,OY],
  PRED h0=0 h1=1, CONVERGE-OK both configs. Moving the
  distinguishing time off t*=0 restores discrimination.
- RT2d (clamp removed, frozen contract): H0=[(X,Y,1)]
  H1=[(X,Y,0)] on V_noclamp.
  Predicted: plan [S,OY], PRED h0=0 h1=1; cfg0 real 0:
  CONVERGE-OK (correct); cfg1 real 0: SURVIVE h0, ELIM h1 with
  h1 true, convergence claimed on h0 = SILENT-WRONG. The loud
  failure is replaced by silent-wrong when the clamp is gone,
  confirming no DDES-side indistinguishability detection: the
  p0==p1 alarm fires only as a generic consequence of the
  clamped predictions coinciding.

### H3 kill bars (frozen)

- ATTACK-SUCCEEDS iff RT2b AND RT2c both yield CONVERGE-OK on
  both configs with DDES code unchanged (only the delay tables
  altered), AND RT2d yields SILENT-WRONG on cfg1 (ELIM h1 with
  h1 true, convergence claimed on h0). Together: the loud
  failure appears and disappears purely with the
  contract x clamp combination; DDES takes no
  boundary-specific detection action beyond the generic p0==p1
  coincidence alarm.
- EVIDENCE-HOLDS iff RT2b or RT2c still fails loudly
  (contract-independent detection), or any variant exhibits a
  t*=0-specific detection action beyond the generic alarm.
- Interpretation if ATTACK-SUCCEEDS: RT2's loud failure is a
  property of the harness contract (delay values 1 vs 0, whose
  clamped predictions coincide) interacting with the clamp, not
  a DDES detection achievement. The repair's credit narrows to:
  the clamp converts would-be silent-wrong into loud failure at
  the boundary, mechanically.

## Execution and determinism (frozen)

- One binary from ddes_alt.zag via plain znc (no
  instrumentation). Build stderr expected: exactly the 93-byte
  unconditional zagd-availability warning. Exit 0.
- Every attack cell run 3/3; transcripts byte-identical across
  the three runs (sha256 recorded in ATTACK_RESULTS.md).
  Run stderr: 0 bytes every run. Exit 0 every run.
- Mechanical checks: the H1(b) diff (V_nomarker vs V_full on P
  minus FLAG lines) must be empty; H2 metrics computed from the
  transcripts and reported per world.

## Governance (frozen)

- Pure Zag at every stage; safebin PATH in every shell;
  zero em-dash and zero en-dash bytes in all lane files
  (byte-checked with check_no_dash.sh before each commit).
- Commits only under
  docs/lab/rsi/runs/wave-20261002-0221pdt/DDES-ALT/ with an
  explicit pathspec; no push; no promotion claims; verdicts name
  the exact frozen bars that governed them.
- New hardcoded semantic cases: 0 expected. New modes: 0.
  New bridges: 0. New handlers: 0. (Recorded per the
  ONE-SYSTEM accounting rule; the attack re-uses the frozen
  derivation machinery with controlled single-line variants.)
- This prereg is committed ALONE. The implementation
  (ddes_alt.zag) is written only after the prereg commit lands.
