# PREREG: META-RECOVERY -- Recovery timescale after distractor interference

Committed BEFORE any implementation. Fresh experiment (not an amendment):
new prereg, new seeds, new episode sequence. Frozen kill bars; no weakening
after results. Commit order: this prereg (+ NAMECHECK.md Step 0) strictly
precedes all implementation files.

## 0. Relation to META-DISTRACTOR (C426)

C426 froze INTERFERENCE DEMONSTRATED: after a 12-episode distractor block
(mean-20 distribution), the persistent learner entered the original block
with the distractor prior m=26 and paid 680 examples over 9 typical
episodes (~76/episode) against the reset control (ADV_R=-680). C426's
report named the suggested next question, analytic only: the recovery
timescale under a longer original block, with the mechanism-derived
estimate that full return of the prior to ~80 needs ~100+ reveals
(m_k = (321+80k)/(12+k) >= 75 only at k >= 116). This lane executes that
question with the LEARNER FROZEN; only the block length changes (plus one
disclosed harness addition, Section 3).

## 1. Question

Constitution: "Learning to learn: examples-to-criterion must decrease with
experience; causal ablation required." C426 showed the LM2 meta-knowledge
is a single-regime prior commitment that overwrites under shift. Three
questions remain, all about the cost of that interference:

1. How many episodes until the prior fully recovers (m -> 80)?
2. Is recovery faster than naive learning (meta-meta-learning), or does
   the prior merely re-converge to the no-distractor trajectory?
3. Does the distractor permanently impair, or does the drag decay to zero?

The honest mechanism-derived prediction (Section 4): the update rule is a
plain running mean with no regime memory, so T can at best ASYMPTOTICALLY
RE-CONVERGE to the fresh trajectory -- full recovery with a quantified
example cost, no meta-meta speedup, no permanent impairment. This
experiment tests whether the mechanism behaves as predicted or deviates;
a deviation either way is the surprise.

## 2. Problem sequence (frozen)

Bernoulli bias-learning family (LM2's family throughout). 732 episodes.
Each episode: hidden parameter p* (hundredths, integer). Examples: a
stream of N = 1200 binary outcomes, outcome = 1 iff PRNG draw < p*.

Episode generation (frozen deterministic procedure; LCG
s <- (s*1103515245 + 12345) mod 2^31):

- Seed SEED_B = 20261016: block D (distractor), episodes 1-12
  (0-based idx 0-11): 9 episodes use 9 DISTINCT parameters, a PRNG
  Fisher-Yates permutation of {16,17,18,19,20,21,22,23,24} (mean 20),
  placed on all idx except 3, 7, 11. The 3 remaining episodes (idx 3, 7,
  11) use 3 DISTINCT parameters, a PRNG permutation of {40,47,54}.
  Structure identical to C426's block D.
- Same seed stream: block R (long original block), episodes 13-732
  (0-based idx 12-731): 720 episodes = 80 cycles of 9; EACH cycle is a
  fresh PRNG Fisher-Yates permutation of {76,77,78,79,80,81,82,83,84}
  (mean exactly 80 per cycle; ALL typical -- no atypicals in block R, so
  the long-run mean of reveals is exactly 80 and the prior's return to
  80 is well-defined).
- Outcomes: INDEPENDENT streams per arm. After reseeding to
  SEED_T = 20261017, 732x1200 outcomes for the T arm; SEED_F = 20261018
  for the F arm; SEED_C = 20261019 for the C arm. All three arms see the
  SAME episode parameters; their outcome trajectories are independent.
- The four seeds are consecutive, frozen here, and disjoint from LM2's
  triple (20261004/05/06), MG's triple (20261007/08/09), FB's triple
  (20261010/11/12), C426's triple (20261013/14/15), every calibration
  seed, and the /tmp calibration seeds (61000000+). Stream independence
  is audited by B5f.
- genfail flag on PRNG/logic fault (none expected); genfail = 1 -> VOID.

DESIGN RATIONALE: block D replicates C426's manipulation (the treatment
must demonstrably learn the distractor first, B5c). Block R is long
enough (720) to span all three analytic milestones (K75 ~= 117,
K78 ~= 309, K79 ~= 627, Section 4) with margin, and its per-cycle mean
of exactly 80 makes the prior trajectory deterministic given the
sequence. Three arms separate the questions: T-vs-C measures return to
better-than-naive (recovery); T-vs-F measures convergence to the
no-distractor trajectory (permanent impairment or not).

Novelty: 12 block-D parameters pairwise distinct; each block-R 9-cycle
internally distinct; all 2196 arm-episode outcome vectors pairwise
distinct (hash check with byte-compare fallback, B4).

## 3. Learner (FROZEN from LM2/MG/C426; mechanism identical)

Shrinkage estimator with a learned prior mean. After n outcomes with h
ones, with prior mean m (hundredths) and frozen pseudo-count w = 20:

  est = (w*m + 100*h) / (w + n)          (hundredths; integer arithmetic)

- T arm: m = mean of all PAST episodes' revealed parameters (integer
  floor; m = 50 before the first episode). Persistent state is
  (sum, count), carried across ALL 732 episodes including the block
  boundary. Enters block R with m = floor(321/12) = 26 DETERMINISTICALLY
  (9x20 + 40+47+54 = 321 regardless of permutation order).
- F arm (fresh accumulator): reset mode (m = 50, no accumulation) during
  block D; from block-R episode 1 it accumulates with sum = cnt = 0.
  Harness-level re-initialization at the block boundary -- the same class
  of harness change as C426's reset control; the estimator, w = 20,
  initial m = 50, and update rule are untouched. Within-experiment
  "what if the distractor had never happened" reference.
- C arm (control): IDENTICAL estimator, identical code path, but m = 50
  at every episode start (reset ablation: no accumulation). Naive
  baseline. Sees its OWN independent outcome stream.

The update takes ONLY the revealed parameter as input -- never the
episode index, never problem identity (B6 audit). No within-episode
feedback. After each episode the truth p* is revealed (supervised episode
boundary, not a within-episode signal) and folded into (sum, count) when
the arm accumulates.

FREEZE GUARANTEE: `etc_ep` in `mr1.zag` is byte-identical to the frozen
`md1.zag`/`lm2.zag` (verified by diff before the implementation commit).
`run_cond`'s estimator call and update statements are byte-identical;
it differs ONLY in: (a) the episode-count loop-bound literal 24 -> 732
(harness change for the 732-episode sequence); (b) the `accum` flag
generalized to `acc_from` (accumulate from episode index acc_from;
acc_from = 0 reproduces md1's accum = 1 statement-for-statement,
acc_from >= 732 reproduces accum = 0; T uses 0, F uses 12, C uses 9999);
(c) recording m entering each block-R episode into a trajectory array
(harness instrumentation; touches no learner state). The only other
permitted source differences between `mr1.zag` and `md1.zag` are:
(d) `gen()` block-R cycle generation (80x9 permutations) and 732-episode
loops; (e) seed literals 20261013/14/15 -> 20261016/17/18/19 (fourth seed
for the F arm); (f) arena offsets/sizes for 732 episodes x 3 arms
(2,635,200 outcome bytes; malloc 4194304); (g) the threshold literals
(recalibrated, Section 5); (h) header/output label strings (neutral
identifiers retained); (i) a median-of-720 helper (bubble-sort median)
and an FNV-1a outcome-vector hash helper, both implementing
preregistered apparatus bars and touching no learner code. Any other
diff -> implementation rejected. In particular the estimator form,
w = 20, initial m = 50, and the cross-episode update rule are unchanged.

## 4. Predicted recovery curve (mechanism-derived, frozen)

Let S_k be the sum of the first k block-R reveals (S_k = 80k at cycle
boundaries, since each 9-cycle sums to exactly 720). Entering block-R
episode k (1-based):

  m_T(k) = floor((321 + S_k) / (12 + k))      (distractor anchor 321)
  m_F(k) = floor(S_k / k)                      (fresh; ~= 80 from k = 1)

Milestones (first k with m_T(k) >= level; deterministic given the
frozen sequence):
- K75 ~= 117  (prior within 5 of the typical mean 80)
- K78 ~= 309  (within 2)
- K79 ~= 627  (within 1)
The distractor anchor's drag decays as (m_F - m_T) ~= 639/(12+k):
at k = 720, m_T ~= 79.0 vs m_F = 80.

Behavioral predictions: late in block R (k = 631..720) m_T ~= 79 vs
m_C = 50, so T beats naive C by nearly the full learned advantage
(calibrated ADV_LATE mean 9040 over 90 episodes, Section 5); T-vs-F
converges (calibrated late ratio ~= 0.0003). Total price of the
distractor prior: COST_TF = sum_{k=1..720}(ET_k - EF_k), calibrated
mean 4779.

## 5. Threshold calibration (design-phase Monte Carlo, pure Zag)

A /tmp Zag program (`cal_mr.zag`) replicated the EXACT frozen mechanism
(verbatim `etc_ep`; `run_cond` with the 732-episode bound and `acc_from`;
w=20, tol=5, N=1200; block D as C426; block R 80x9-cycles; 3 arms;
independent streams; same LCG) over R=150 replications with fresh
non-overlapping seeds (61000000+10*rep+{0,1,2,3}; disjoint from the
frozen 20261016-19). Power analysis, not seed selection: no frozen-seed
outcome was observed or selected. Results (means, sd, min, max):

- ADV_LATE = sum_{k=631..720}(EC-ET): mean=9040, sd=834, min=7322, max=12088
- STF_LATE = sum_{k=631..720}(ET-EF): mean=3, sd=112, min=-661, max=367
- SCF_LATE = sum_{k=631..720}(EC-EF): mean=9044, sd=843, min=7304, max=12064
- ADV_D (block-D typicals, 9 eps): mean=766, sd=215, min=238, max=1436
- ADV_R9 = sum_{k=1..9}(EC-ET): mean=-388, sd=369, min=-1652, max=478
- MEDCR (median of 720 control block-R etc): mean=79, sd=5, min=73, max=85
- Per-arm ones: mean~=695051, sd~=900, min=694028, max=696263
  (expected 695052 = 12x321 + 12x80x720)
- MAXETC: mean=673, sd=133, min=477, max=1201 (1201 hit in 2/150 reps)
- K75: mean=117, min=116, max=118
- K78: mean=308, min=304, max=313
- K79: mean=627, min=618, max=631
- COST_TF: mean=4779, sd=659, min=3027, max=6755

Threshold derivations (frozen):
- B5a = 6000 (primary): 0.66x the calibrated ADV_LATE mean (9040);
  z = -3.67, nominal power ~99.99%; min observed 7322 clears it. A
  strongly substantive bar: requires ~2/3 of the full re-learned
  advantage over the last 90 episodes (~67/episode).
- B5b = 0.10 (one-sided): CONV = STF_LATE / SCF_LATE <= 0.10, with the
  guard SCF_LATE > 3000 (calibrated min 7304; denominator collapse would
  void the ratio). Calibrated ratio ~= 0.0003 (sd of numerator 112
  against denominator ~9044); nominal power ~100%. One-sided on purpose:
  a large NEGATIVE ratio (T beating F late) would be the surprise
  meta-meta-speedup finding and is reported, not barred.
- B5c = 365 (manipulation): same 0.48x bar as C426's B5d2 (calibrated
  ADV_D mean 766, sd 215; nominal P(pass) ~= 97%). If the distractor was
  not learned, the recovery test is invalid -> UNDECIDED.
- B5d = 0 (sign, secondary): calibrated ADV_R9 mean -388, sd 369;
  P(<=0) ~= 0.85. Replicates C426's interference onset on fresh seeds.
- B5e = 25 (luck-robust floor): median over all 720 naive control
  block-R etc values (C419's lesson: median, not a single early
  episode). Calibrated 79 +- 5, min 73; P(fire) ~= 0. Fail -> UNDECIDED.
- B5f MARG bounds [677000, 713000]: expected per-arm ones 695052,
  sd ~900; bounds are ~20sd, a gross-fault check as in LM2/MG/FB/C426.
- B5g apparatus: genfail = 0 -> VOID otherwise. The etc=1201 cap event
  hit in 2/150 calibration reps (heavy right tail at 2196 episode-runs
  per run); it is a legitimate measurement (contributes 1201 to sums,
  reported via MAXETC), NOT an apparatus fault, so it does not void.
  This disclosed deviation from the family template avoids ~4%
  gratuitous VOID risk over 3 runs.

## 6. Frozen predictions

- P1: MEDCR >= 25 (naive control does real statistical work across the
  long block; MC mean 79).
- P2: ADV_D >= 365 (manipulation: the distractor distribution is learned;
  MC mean 766).
- P3: ADV_R9 <= 0 (interference onset replicates on fresh seeds;
  MC mean -388).
- P4: ADV_LATE >= 6000 (functional recovery: treatment beats naive by
  ~2/3+ of the full re-learned advantage over the last 90 episodes;
  MC mean 9040).
- P5: CONV = STF_LATE / SCF_LATE <= 0.10 with SCF_LATE > 3000
  (convergence to the no-distractor trajectory; MC ratio ~= 0.0003).
- P6: K75 ~= 117; report the exact deterministic value.
- P7: K78 ~= 309 and K79 ~= 627; report exact deterministic values.
- P8: COST_TF ~= 4800 (report-only; MC mean 4779, sd 659): the total
  example-price of the distractor prior vs the fresh accumulator.
- P9: 3/3 runs byte-identical; 12 block-D parameters distinct; all 80
  block-R cycles internally distinct; 2196 outcome vectors pairwise
  distinct; parameters identical across arms.

## 7. Frozen kill bars

- B1 COMMIT-ORDER: PASS iff this prereg (+ NAMECHECK.md Step 0) is
  committed before any implementation file, and every implementation
  commit strictly postdates the prereg commit.
- B2 TOOLCHAIN: PASS iff PATH is safebin-only for all work,
  `which python3`, `which python`, `which perl`, `which ruby`,
  `which node` all return empty, all scientific computation is
  znc-compiled Zag, and zero forbidden executables are invoked.
- B3 DETERMINISM: PASS iff 3/3 runs of the frozen binary are pairwise
  byte-identical (cmp); sha256 digests recorded.
- B4 NOVELTY: PASS iff the binary prints DISTINCTBD=1 (12 block-D
  parameters pairwise distinct), CYCDIST=1 (all 80 block-R 9-cycles
  internally distinct), DISTINCTF=1 (all 2196 arm-episode outcome vectors
  pairwise distinct via FNV-1a hash with byte-compare fallback), and
  PARID=1 (parameters identical across the three arms). Else VOID.
- B5a RECOVERY (PRIMARY): PASS iff ADV_LATE >= 6000.
- B5b CONVERGENCE: PASS iff SCF_LATE > 3000 AND
  STF_LATE / SCF_LATE <= 0.10 (integer division toward zero; the ratio
  is computed as (STF_LATE <= SCF_LATE/10) to stay in integer
  arithmetic -- see note below).
- B5c MANIPULATION: PASS iff ADV_D >= 365. If FAIL the verdict is
  UNDECIDED (distractor not learned; the recovery test is invalid),
  never "no recovery".
- B5d ONSET (secondary): PASS iff ADV_R9 <= 0. Reported with numbers.
- B5e FLOOR-VALIDITY (luck-robust): PASS iff MEDCR >= 25. If FAIL the
  verdict is UNDECIDED (task too easy; redesign), never a pass.
- B5f STREAM-VALIDITY: PASS iff PARID=1 AND DISTINCTF=1 AND MARG=1
  (per-arm ones within [677000,713000]; gross PRNG fault check).
  Else VOID.
- B5g APPARATUS: PASS iff genfail = 0. Report MAXETC. An etc value of
  1201 is a legitimate heavy-tail measurement, not a fault. Else VOID.
- B6 NO-RESEARCHER-META-RULE: PASS iff (a) the cross-episode update's
  only input is the revealed parameter, (b) the estimator (`etc_ep`)
  and the update statements reference no episode index or counter
  (grep audit on the learner code), (c) the driver never modifies
  (sum, count) except via the learner's update (T from episode 0, F
  from episode 12) or non-accumulation (C always; F during block D),
  AND (d) `etc_ep` is byte-identical to the frozen `md1.zag`/`lm2.zag`
  and `run_cond` differs from it ONLY in the three documented ways
  (loop bound 24 -> 732; `accum` -> `acc_from` with behavioral identity
  at 0 / >= 732; m-trajectory recording), with only the nine permitted
  change classes of Section 3. The estimator form, w = 20, and initial
  m = 50 are disclosed researcher-supplied mechanism; the learned
  quantity is m itself.
- B7 OPAQUE-IDS: PASS iff episode labels are exactly E001..E732,
  parameters and outcomes are bare integers, and a grep audit for the
  frozen semantic word list (coin, bias, heads, tails, shrink, prior,
  learn, meta, cluster, outlier, typical, atypical, general, poisson,
  rate, lambda, gauss, count, event, slot, family, distractor, shift,
  phase, regime, original, interference, recover) in sources returns
  empty.

Note on B5b integer arithmetic: the binary checks
`10*STF_LATE <= SCF_LATE` (all i64; both sums' signs as observed).
With SCF_LATE > 3000 > 0 this is exactly STF/SCF <= 0.10. If
STF_LATE <= 0 the check passes trivially (T at least as fast as F).

## 8. Verdict mapping (frozen)

- B1 fail: VOID. B2 fail: PROCESS-FAIL. B3 fail: UNDECIDED (name the
  decisive rerun). B4, B5f, or B5g fail: VOID. B5e fail: UNDECIDED.
  B5c (manipulation) fail: UNDECIDED.
- B5a PASS (+ B5e PASS + B5c PASS): RECOVERY DEMONSTRATED -- after the
  distractor interference, the prior returns to the original
  distribution over the long block and beats the naive baseline by at
  least 6000 examples over the last 90 episodes. The reset ablation
  attributes the trajectory to the persistent history: the only
  T/C difference is (sum, count).
- B5a FAIL with ADV_LATE < 6000: NO RECOVERY (within 720 episodes) --
  report the numbers; the distractor prior still costs against naive
  after 720 original-distribution episodes.
- B5b PASS: CONVERGED -- the treatment trajectory re-converges to the
  fresh-accumulator trajectory (residual drag <= 10% of the naive
  disadvantage): no permanent impairment, and no faster-than-fresh
  speedup (the running-mean rule admits none).
- B5b FAIL with CONV > 0.10: LASTING DRAG -- after 720 episodes the
  distractor history still costs more than 10% of the naive
  disadvantage; report the numbers prominently.
- B5b with large negative CONV (T beating F late): surprise finding,
  reported as a candidate meta-meta-speedup and attacked, not barred.
- B5d: secondary consistency bar; reported with numbers.
- K75/K78/K79/COST_TF: report-only with preregistered predictions.

## 9. How this tests the boundary

C426 established that the acquired meta-knowledge is a single-regime
prior commitment that overwrites under shift (interference). The rival
explanations this design excludes: (a) that the interference is
permanent -- B5b tests convergence to the no-distractor trajectory on
the same draws; (b) that recovery never reaches better-than-naive --
B5a tests the restored advantage against the naive baseline;
(c) that re-learning is somehow faster than fresh learning
(meta-meta-learning) -- the design can only confirm or break the
mechanism's prediction of asymptotic re-convergence, and a break in
either direction is preregistered as a finding. The F arm is the
critical apparatus: without it, "permanent impairment" has no clean
within-experiment comparator. The deterministic prior milestones pin
the timescale analytically; the behavioral bars pin it empirically.

## 10. Honest boundaries (pre-declared)

- This is ONE shift scenario (20 -> 80, Bernoulli family, 12-episode
  distractor block, w=20 inertia, 720-episode original block): the
  recovery timescale and cost are specific to this design. The analytic
  milestones scale as ~639/(12+k) drag decay; other shifts differ.
- What is learned is the PRIOR MEAN over parameters: empirical-Bayes
  base-rate learning (L1/L2-ish), same as LM2/MG/FB/C426. Not strategy
  invention, not L3. The estimator form, w=20, initial m=50 are
  researcher-supplied mechanism; the learned quantity is m.
- The truth-reveal per episode is supervised; within-episode learning
  has zero feedback.
- One frozen sequence, one frozen seed quadruple (20261016/17/18/19),
  fixed before implementation; no seed selected on outcomes.
- The F arm's block-D episodes run in reset mode; their etc values are
  report-only (the F arm's science starts at block-R episode 1).
- The calibration Monte Carlo used the same PRNG family with disjoint
  seeds; it estimated the mechanism's sampling distribution under the
  new sequence (power analysis). The frozen seed quadruple was fixed
  here before any implementation ran; no seed was selected on outcomes.
- The harness's tolerance check is measurement scaffolding, not a
  learning signal: the learner never observes it.
- C419 (Option B, cross-family) remains UNDECIDED and is not
  re-litigated here.
- The B5g deviation (etc=1201 not voiding) is preregistered with its
  calibration justification (2/150 reps hit the cap): at 2196
  episode-runs per run the heavy tail is expected measurement, not
  apparatus fault.
