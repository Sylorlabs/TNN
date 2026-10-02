# RESULT: F2 Out-of-Distribution Test

Date: 2026-09-30. Worker: F2 OOD Worker.
Prereg: `8e795c2b9` (committed alone before implementation).
Amendment: `aab551087` (transparent correction of passive semantics and
W2/W4 schedules, re-frozen before rebuild; verified strict descendant
of the prereg).

## Verdict: OOD-TESTED

All three kill bars pass. Four structurally OOD worlds, frozen learner
used verbatim (md5 de95a49350f42122da5fb0a8dd445eba, from 1eb66765d),
each 3/3 byte-identical, pure Zag, zero Python, zero em-dash bytes.

## Kill bars

- **K1 PASS.** All four worlds implemented per prereg + amendment.
  Structural axes, all distinct from training worlds A (confounded
  chain) and B (contextual single-cause) and from ablation adversaries
  ADV1 (conjunction) and ADV2 (silent cause):
  W1 temporal aggregation, W2 negation, W3 timescale beyond DMAX,
  W4 redundant sufficient causes.
- **K2 PASS.** Per-world measurements below. All four prereg
  predictions CONFIRMED (W2/W4 under the amended schedules; the
  original-schedule runs are disclosed, not hidden).
- **K3 PASS.** Pure Zag at every stage (znc, bash, grep, git only; zero
  Python invocations). Zero em/en-dash bytes (byte-checked). 3/3
  byte-identical per world (md5s below). All exits 0. Zero stderr
  bytes across all 12 runs. One harness panic in the pre-amendment W4
  w_verify is disclosed (it indexed hysel with ne=0); the learner was
  unaffected, and the amended w_verify returns REFUTED instead of
  panicking.

## Per-world results

| World | md5 (3/3) | NHYP | Survivor | Exps | GOAL_REAL | Witness | Prediction |
|---|---|---|---|---|---|---|---|
| W1 hysteresis | 94dff282b3532951414815f77ba2ad27 | 3 | (X->Y,d1) | 1 | 1 | 1 | CONFIRMED |
| W2 inhibition | caa7a0d577ea4c38bb181043d1641b35 | 1 | none (ne=0) | 0 | n/a (no plan) | 1 | CONFIRMED |
| W3 long delay | 78a568f894d70a649968e4b07f1f9eb6 | 1 | none (ne=0) | 0 | n/a (no plan) | 1 | CONFIRMED |
| W4 disjunction | c4d52a3866309716c8d631aaec2613be | 2 | Y-rule (X->Y,d1) | 1 | 1 | 1 | CONFIRMED |

### W1: confident but false (temporal aggregation)

Truth Y(t)=1 iff X in {t-1,t-2,t-3}. Three candidates (d1,d2,d3);
the single experiment [SX,W,OY] killed d2 and d3, leaving (X->Y,d1),
the SHORTEST delay, as the confident survivor (nalive=1,
PLAN_AGREEMENT trivially 1). Goal [SX,W] succeeded (GOAL_REAL=1).
But the post-hoc pulse [SX,W,CX,W,OY] (harness-side): survivor
predicts Y=0, truth gives Y=1. **F2 converged with full confidence on
a false law; the goal succeeded by luck.** First-disagreement search
order biases toward the shortest delay, which for memory dynamics is
the maximally wrong model of persistence. No honesty signal exists.

### W2: declares impossible what is achievable (negation)

Truth Y(t)=X(t-1)&!Z(t-1), with X,Z pulsed together twice (cnt=2).
Y got ZERO candidates: every positive rule is genuinely refuted by
the overlap (ok=0 with cnt=2, not a data shortage). ne=0, zero
experiments, PLAN none found. Oracle witness [SX,W] achieves Y=1.
**F2 cannot represent negation, and reports the goal impossible
though it is achievable.** There is no signal distinguishing
"unmodeled" from "impossible".

### W3: blind beyond DMAX (timescale)

Truth Y(t)=X(t-5), DMAX=4. Zero candidates at every delay (the two X
pulses are never followed by Y within 4 steps). ne=0, PLAN none found.
Oracle witness [SX,W,W,W,W,W] achieves Y(5)=X(0)=1. **F2 cannot
distinguish "no cause" from "cause beyond search depth".** This maps
the enumerate boundary exactly at the DMAX parameter: lengthening the
delay by one step moves a solvable world to an impossible verdict.

### W4: kills a true hypothesis (redundant causation)

Truth Y(t)=X(t-1)|Z(t-2). Both (X->Y,d1) and (Z->Y,d2) fit passive
with cnt=2, and BOTH ARE TRUE of the world. The experiment [SX,W,OY]
(hand-predicted, observed exactly) killed the hyp carrying (Z->Y,d2).
**F2's hypothesis space frames candidates as exclusive alternatives,
so it discarded a true sufficient cause with full confidence.**
Survivor's Y-rule (X->Y,d1) planned [SX,W], GOAL_REAL=1. This is the
mirror of ADV1: there the family was too poor for conjunctive truth
and the goal failed; here each single rule is true, the goal succeeds,
but the converged model denies a real causal link.

## Where the enumerate-then-select boundary hits

1. **Vocabulary, not data.** W2 (with cnt=2) and W3 show the boundary
   is the fixed primitive alphabet (no NOT, delay cap 4), not sample
   size. More passive data would not help either world.
2. **One-cause-per-effect framing.** W4 shows the combination rule
   (exactly one rule per effect variable) is itself a structural
   commitment that silently discards true causes.
3. **Confidence is uncalibrated.** W1 and W4 both end at nalive==1 with
   PLAN_AGREEMENT=1 while holding false or partial models. F2 has no
   "none of my hypotheses explains the data" verdict at plan time
   (consistent with the ablation finding).
4. **Goal success is luck-dependent.** W1/W4 goals succeeded; ADV1's
   failed. Nothing in F2's internal state distinguishes these cases
   before execution.
5. **Search order biases the survivor.** W1's first-disagreement
   experiment selected the shortest delay; a different passive
   schedule could have selected d3. The survivor depends on
   lexicographic search order, not on which candidate is closest to
   the truth.

## Honest scope

F2 remains strong within its family (BUILD-PASS, reproduced,
memorization-tested, disagreement targeting essential per ablation).
The OOD results do not kill F2; they bound it: F2 is a sound
disagreement-driven discriminator over a fixed single-cause
vocabulary, blind outside it, and its confidence signals
(convergence, agreement) do not track model truth.

## Files

All under `docs/lab/research-lead/overnight-20260928/f2_ood/`:
`PREREG_F2OOD.md`, `PREREG_F2OOD_AMEND1.md`, `RESULT_F2OOD.md` (this
file), `learner_frozen.zag` (md5 de95a49350f42122da5fb0a8dd445eba),
`world_ood1.zag` .. `world_ood4.zag`, `run_ood1.zag` ..
`run_ood4.zag`, `bin_ood1` .. `bin_ood4` (binaries), `build_ood*.err`,
`raw_ood1_1.txt` .. `raw_ood4_3.txt` (12 run logs),
`raw_ood*_*.err` (12 empty stderr logs).

## Promotion relevance

Promotion step 7 (OOD) complete. F2's enumerate-then-select boundary
is now empirically mapped on four new structural axes beyond the
ablation's ADV1/ADV2. Steps 8 (ablation, done at 1f3a9511c), 9
(transfer/reuse), 10 (independent red team), 11 (governance audit)
remain. No SURVIVES claim is made.
