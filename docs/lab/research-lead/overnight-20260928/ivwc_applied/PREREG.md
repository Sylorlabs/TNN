# PREREG.md -- IVWC-APPLIED: the hybrid verdict on a real internal-verification problem (no oracle)

## Wave

Follow-up from IVWC-HYBRID-VERDICT (BUILD-PASS K1-K10) and
IVWC-HYBRID-CLEAN (clean reproduction, PROCESS-FAIL lifted). Those
waves established the hybrid verdict as a *mechanism*: a bar that is
batch-responsive yet correction-independent (V_HA: ThyA(sh) =
mean_sealed(preff) - C; V_HB: ThyB(sh) =
mean_sealed(preff - bucb_frozen[bkt])). But they scored the verdict
against transductive labels ge = (eff >= Tpred) -- an
expected-answer oracle, explicitly listed as inherited limit (b):
"no verdict in this family tracks label shifts that preff doesn't
reflect."

This wave applies the hybrid verdict to a REAL internal
verification problem with NO expected-answer oracle anywhere --
not for the learner, not even for scoring.

Non-ledger task. Lane `ivwc_applied/`. Pure Zag, safebin, 3/3
byte-identical. Commits local on `tnn-native-lab`. Pushing to
origin is AUTHORIZED per Micah's 2026-10-03 authorization (fresh
GitHub PAT; exclude reproducible cache/build artifacts).

## The real problem: selective execution (GO / NO-GO)

The learner composes a plan per sealed case (verbatim composer),
forms its bias-free internal prediction `preff` (from belief) and
its bias-adjusted estimate `adjV = preff - bias` (its own learned
UCB bias, the REAL case). It must then VERIFY its own work: GO
(commit resources, execute the plan) or NO-GO (abstain). There is
no oracle: the learner never sees the true outcome `eff` before
deciding, and -- unlike every prior IVWC wave -- the EXPERIMENT
never computes a label either. No `ge`, no `Tpred`, no accuracy.
The score is CONSEQUENCE: the world charges a fixed execution cost
K per GO, and profit per case = (eff - K) if GO else 0. Total
profit per batch per arm is the oracle-free measure of
verification quality. This is learner commitment -> world
consequence -> measured outcome, with no expected answer at any
point.

The experimental variable is the verdict (the trust rule):
V_T (bar = mean sealed adjV; reads its own corrected scores),
V_N (bar = T_fixed, train-frozen), V_HA (hybrid-A, preff-scoped),
V_HB (hybrid-B, frozen-baseline-scoped). Biases: B0 = UCB (the
learner's genuinely learned per-bucket bias -- the REAL
self-verification case), B1 = D1b / B2 = D2b (fenced harness
diagnostics with researcher-set +40, retained verbatim as
red-team stress tests on the verdict structure; honest about
being fenced, as in the verdict wave).

Arms (10): A1=B0xV_T, A2=B0xV_N, A7a=B0xV_HA, A7b=B0xV_HB
(learner-side: the learner's own bias verified by each bar),
A3=B1xV_T, A4=B1xV_N, A8a=B1xV_HA, A8b=B1xV_HB,
A9a=B2xV_HA, A9b=B2xV_HB (fenced diagnostics).
Reference: execute-all profit per batch (fenced, counterfactual;
answers "is verification better than none?").

## Execution cost K

K = 15 efficiency units per execution, fixed across all batches
and arms, preregistered here. K is a WORLD parameter (the cost of
committing resources), not a label and not a threshold on truth.
Justification, stated before any profit was examined: K sits near
the center of the learner's committed bar range (ThyA/ThyB/Tfixed
span 6-20 in the committed tables), so the learner's GO/NO-GO
trust rule is approximately cost-calibrated rather than
systematically over- or under-executing; and it is nontrivial
because sealed effs (0-100) have mass on both sides of 15 in every
batch. The learner's verdict does NOT take K as input -- this wave
applies the hybrid verdict as-is (cost-blind); how a cost-blind
trust rule fares under a costly world is part of what is being
measured (see the preregistered limits).

## Background facts (from committed tables, not probed)

World/belief/composer/stepper/seeds/biases/bars are verbatim from
IVWC-HYBRID-VERDICT (K3 checks: BARS ThyA=13/20/6, ThyB=13/20/13,
TFIXED=12, CVAL=15). Committed per-case sealed eff (from
`ivwc_hybrid_verdict/runs/ivwc_hybrid_verdict-run1.txt`, V lines):

- sh=0 (@15): eff = [0,0,33,0,33,33,20,33,0,33,25,13]
- sh=1 (@30): eff = [10,0,33,50,50,30,0,25,50,0,25,20]
- sh=2 (@45): eff = [0,0,0,0,0,0,0,0,0,0,0,100]

Committed GO sets (verdict = 1 from the same V lines; a1,a2,a7a,
a7b,a8a,a8b,a3,a4,a9a,a9b):

- sh=0: a1{2,3,4,5,7,9} a2{0,2,3,4,5,7,9} a7a{2,3,4,5,7,9}
  a7b{2,3,4,5,7,9} a8a{2,4,7,9} a8b{2,4,7,9}
  a3{1,2,4,7,8,9,10} a4{2,4,7,9} a9a{2,3,7,9} a9b{2,3,7,9}
- sh=1: a1{0,3,4,6,7,8} a2{0,2,3,4,5,6,7,8} a7a{0,3,4,6,7,8}
  a7b{0,3,4,6,7,8} a8a{3,4,8} a8b{3,4,8} a3{2,3,4,8,10}
  a4{2,3,4,8} a9a{3,6,7,8} a9b{3,6,7,8}
- sh=2: a1{0,4,11} a2{0,4,5,11} a7a{0,4,5,11} a7b{0,4,11}
  a8a{11} a8b{11} a3{11} a4{11} a9a{0,4,11} a9b{0,4,11}

GO counts per batch: 52 / 49 / 24 (sum 125). Train executions 24;
fenced execute-all reference 36. WC-FINAL = 24 + 125 + 36 = 185.

## Frozen profit predictions (K=15; profit = sum over GO of (eff-15))

sh=0: a1=75 a2=60 a7a=75 a7b=75 a8a=72 a8b=72 a3=52 a4=72
       a9a=39 a9b=39 all=43
sh=1: a1=95 a2=128 a7a=95 a7b=95 a8a=105 a8b=105 a3=133 a4=123
       a9a=65 a9b=65 all=113
sh=2: a1=55 a2=40 a7a=40 a7b=55 a8a=85 a8b=85 a3=85 a4=85
       a9a=55 a9b=55 all=-80

Totals: a1=225 a2=228 a7a=210 a7b=225 a8a=262 a8b=262 a3=270
        a4=280 a9a=159 a9b=159 all=76

All predictions are arithmetic on the committed tables above. No
new data was generated or read before this prereg. If any profit
differs in either direction, the report states the exact
mechanism; no number moves after seeing results.

## Frozen kill bars

- **K1 (diet / commit order / no-oracle): PASS required.**
  A1: phase order train COMMIT < train PREFF < train CONSEQ <
  train LEARN < train BAR < sealed COMMIT < sealed BARS < sealed
  VERDICT (GO) < CONSEQUENCE (world_execute on GO) < REFERENCE,
  by source line order (exact numbers recorded post-build; strict
  increase is the frozen property). A2: zero `world_buf`/
  `world_off` tokens in learner fns. A3: zero
  `expected|answer|key|target` (case-insensitive). A4: zero
  `correct|reference_plan|gold`. A5: `world_execute(` exactly 4
  occurrences (1 def + 3 call sites: train CONSEQ, CONSEQUENCE,
  REFERENCE). A6: WC-FINAL = 185. A7: zero `learner_`/`belief_`
  calls after the CONSEQUENCE marker. A8: the token "oracle"
  (case-insensitive) appears zero times. A9 (the no-oracle bar):
  the token `Tpred` appears zero times -- no transductive label
  threshold is computed anywhere, not even fenced.
- **K2 (determinism): PASS required.** 3/3 runs byte-identical
  stdout.
- **K3 (verbatim machinery): PASS required.** BARS lines:
  ThyA = 13/20/6, ThyB = 13/20/13 @15/30/45; TFIXED = 12;
  CVAL = 15 (in-program exact checks).
- **K4 (PRIMARY): PASS required.** UCB x V_HA per-batch profit =
  (75, 95, 40), total 210; and 210 > execute-all total 76. The
  learner verifies its own learned-bias work with the hybrid bar,
  zero oracle anywhere, and beats no-verification by 134.
- **K5: PASS required.** Execute-all per-batch profit =
  (43, 113, -80).
- **K6: PASS required.** UCB x V_HA @45 = 40 < UCB x V_HB @45 =
  55. The preregistered @45 bias-mix limit (K10 of the verdict
  wave) reproduces in consequence terms: HA's s=5 false GO
  (adjV=13 clears ThyA=6; eff=0) costs exactly 15 profit.
- **K7: PASS required.** D1b x V_HA @15 = 72 > D1b x V_T @15 =
  52. The un-blocking has consequence value: V_T's chase-down
  executes s=1, s=8 (eff=0; -15 each) while HA's unmoved bar
  holds.
- **K8: PASS required.** WC-FINAL = 185 (in-program).
- **K9: PASS required.** Totals: D1b x V_HA = 262,
  D1b x V_T = 270, D1b x V_N = 280.
- **K10: PASS required.** D2b x V_HA total = 159,
  D2b x V_HB total = 159.

**BUILD-PASS requires K1..K10.**

## Preregistered answers to the task's key questions

1. **Can the learner verify without an oracle?** Predicted YES:
   K4 -- the learner's self-verification (own UCB bias, own
   hybrid bar, no label or threshold anywhere in the experiment)
   yields profit 210 vs 76 for executing everything. The
   verification is real: GO/NO-GO decisions with a real cost,
   judged by consequences.
2. **Does the hybrid verdict help?** Predicted MIXED, and the mix
   is the finding. On the learner's own bias the four verdicts
   bunch (210-228): HA does not dominate, because its @45
   bias-mix limit (K6) is a real 15-profit loss. Where the
   correction-independence bites (@15 D1b, K7), HA beats V_T by
   20. The hybrid verdict helps exactly where its structural
   property matters and hurts exactly where its preregistered
   limit lives.
3. **What are the limits?** (a) K6: the @45 limit is now a
   profit loss, not just an accuracy gap. (b) Preregistered from
   K9: D1b x V_N totals 280 > D1b x V_HA 262 -- while the verdict
   wave's committed accuracy table has A8a (35/36) ABOVE A4
   (34/36). Accuracy-optimal and profit-optimal DIVERGE: the
   hybrid bar answers a relative-trust question ("above the
   batch's level?"), not a consequence question ("worth K?").
   VN's lower frozen bar executes more, and at K=15 more
   executions pay. This divergence is the next-frontier pointer:
   a consequence-aware verdict (a bar that knows K) is not in
   this family. (c) The verdict remains cost-blind by
   construction; K-sensitivity of the ranking is expected and
   will be reported as measured.

## Determinism and honesty rules

- Integer arithmetic only. No researcher-set constants in any
  learner path (K=15 lives in the world/consequence phase as the
  execution cost; the D1b/D2b +40 lives only in the fenced
  diagnostic, as in prior waves).
- No post-prereg probe of any kind. All predictions above are
  arithmetic on the committed verdict-wave per-case tables.
- The words `Tpred`, `oracle`, `expected`, `answer`, `key`,
  `target`, `correct`, `reference_plan`, `gold`, `label` do not
  appear in the implementation source (K1 A3/A4/A8/A9).
- If any arm differs from prediction in either direction, report
  the exact mechanism. No bar moves after seeing results.
