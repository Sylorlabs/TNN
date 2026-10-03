# PREREG: META-FAMILY-B -- Does the LM2 meta-learning transfer to a different task family?

Committed BEFORE any implementation. Fresh experiment (not an amendment):
new prereg, new seeds, new task family. Frozen kill bars; no weakening after
results. Commit order: this prereg (+ NAMECHECK.md Step 0) strictly precedes
all implementation files.

## 0. Relation to META-GENERALIZE (C415 TRANSFER DEMONSTRATED)

META-GENERALIZE froze the verdict TRANSFER DEMONSTRATED on a new
distribution (B5a ADV_C=679>=370, all bars PASS): the LM2 meta-learning
effect is not tied to the 80-location. Its preregistered honest boundary:
"Options B (different task family) and C (distractor-then-original) remain
untested and are recorded as follow-ups."

This experiment tests Option B with the LEARNER FROZEN: the learner
functions (`etc_ep`, `run_cond`) are copied byte-for-byte from the frozen
`lm2.zag`; ONLY the task family changes (Option B: Bernoulli bias learning
-> Poisson rate learning). If the typical-advantage effect survives in the
new family, the LM2 mechanism is a family-general distribution-typical-value
learner, not a Bernoulli-specific one. If it fails, the meta-learning is
family-specific even with the learner held fixed.

## 1. Question

Constitution: "Learning to learn: examples-to-criterion must decrease with
experience; causal ablation required." Is the persistent shrinkage
learner's speedup GENERAL across task families (a genuine
distribution-typical-value learning mechanism), or is it specific to the
Bernoulli bias-learning family? The primary claim is tested on the new
family's typical episodes only; atypical episodes get the same separate
negative-transfer signature bar as LM2/MG.

## 2. New problem family (frozen)

Poisson rate learning, 12 episodes. Each episode: hidden rate parameter r*
(hundredths, integer; e.g. r* = 80 means 0.80 events per position).
Examples: a stream of N = 1200 positions; the position observation is a
nonnegative integer k drawn from Poisson(r*/100).

Episode generation (frozen deterministic procedure; LCG
s <- (s*1103515245 + 12345) mod 2^31):

- Seed SEED_B = 20261010: 9 "typical" episodes use 9 DISTINCT parameters,
  a PRNG Fisher-Yates permutation of {76,77,78,79,80,81,82,83,84}
  (mean 80), placed on all episodes except 4, 8, 12 (1-indexed).
- Same seed stream: 3 "atypical" episodes (4, 8, 12) use 3 DISTINCT
  parameters, a PRNG permutation of {40,47,54} (UNCHANGED from LM2/MG).
- All 12 parameters are pairwise distinct. The task distribution has a
  learnable regularity (parameters cluster near 80); the learner is never
  told this.
- Observations: INDEPENDENT streams per condition. After reseeding to
  SEED_T = 20261011, 12x1200 observations for the treatment episodes;
  after reseeding to SEED_C = 20261012, 12x1200 for the control episodes.
  Both conditions see the SAME episode parameters; their observation
  trajectories are independent.
- Per position, one 31-bit LCG draw u in [0, 2^31). The observation is the
  smallest j in 0..15 with u < t[j], where t[j] = round(2^31 * P(X <= j))
  for X ~ Poisson(r*/100), computed per episode in integer fixed point
  (scale 10^9: e^-x by alternating series to |term| < 3 units; pmf by
  recurrence pmf[k+1] = pmf[k]*r/(100*(k+1)); t[15] forced to 2^31).
  Self-checks: the raw computed t[15] must be within 100000 of 2^31 and
  the thresholds nondecreasing, else genfail = 1.
- The three seeds are consecutive, frozen here, and disjoint from LM2's
  triple (20261004/05/06), MG's triple (20261007/08/09), and every
  calibration seed. Consecutive LCG seeds diverge immediately (first draws
  differ by 1103515245 mod 2^31); stream independence is audited by B5e.
- genfail flag on PRNG/logic fault (none expected); genfail = 1 -> VOID.

DESIGN RATIONALE (why this family): the frozen learner is a shrinkage
estimator of a running mean in hundredths, est = (20*m + 100*h)/(20+n),
where h accumulates the observations. The task family is the
(parameter, observation model, noise) triple. LM2/MG: parameter = Bernoulli
bias (a probability), observations = binary flips, noise = Bernoulli
(var = p(1-p)). New family: parameter = Poisson rate (NOT a probability;
unbounded in principle), observations = per-position counts 0,1,2,...,
noise = Poisson (var = mean). The estimator form is LITERALLY unchanged
(h now accumulates counts; the code is byte-identical), so the family
change is isolated as the single causal variable. The typical location is
held at LM2's 80 (gap 30 from the naive 50) because META-GENERALIZE
already isolated location; moving both at once would confound. A Gaussian
mean family was considered and rejected: with observations in hundredths
it would require est = (20*m + h)/(20+n), i.e. a learner change,
violating the frozen-learner constraint. A categorical-mode family was
rejected: the estimand is not a mean, so the shrinkage form does not apply.

Novelty: every episode has a distinct parameter; all 24 observation
vectors (12 per condition) are pairwise distinct (in-Zag check, B4/B5e).

## 3. Learner (FROZEN from LM2; byte-identical)

Shrinkage estimator with a learned prior mean. After n positions with
accumulated observations h, with prior mean m (hundredths) and frozen
pseudo-count w = 20:

  est = (w*m + 100*h) / (w + n)          (hundredths; integer arithmetic)

- Treatment: m = mean of all PAST episodes' true parameters (integer
  floor; m = 50 before the first episode). Persistent state is
  (sum, count). After each episode the truth r* is revealed (supervised
  episode boundary, not a within-episode signal) and folded into
  (sum, count).
- Control: IDENTICAL estimator, identical code path, but m = 50 at every
  episode start (reset ablation: no accumulation). Control sees its OWN
  independent observation stream.

The update takes ONLY the revealed parameter as input -- never the
episode index, never problem identity (B6 audit). No within-episode
feedback.

FREEZE GUARANTEE: `etc_ep` and `run_cond` in `fb1.zag` are byte-identical
to the frozen `lm2.zag` (verified by diff before the implementation
commit). The only permitted source differences between `fb1.zag` and
`lm2.zag` are: (a) `gen()` observation generation (binary-flip loop ->
Poisson CDF-inversion tables + per-position scan; typical-parameter
literals UNCHANGED at 76+i); (b) seed literals 20261004/05/06 ->
20261010/11/12; (c) MARG accumulation (same code shape; now sums counts,
bounds unchanged, Section 7 B5e); (d) the B5a threshold literal
(recalibrated, Section 5); (e) header/output label strings (neutral
identifiers retained); (f) arena layout comment (+128 bytes threshold
scratch). Any other diff -> implementation rejected.

## 4. Metric: examples-to-criterion (etc)

Identical to LM2: etc = smallest n in {1..1200} with |est_n - r*| < 5,
exact integer arithmetic |num - r**den| < 5*den. If never reached,
etc = 1201 (B5f apparatus bar then fails -> VOID; calibration Section 5
bounds this risk: 46 cap hits in 24,000 episode-runs, ~0.19%/run).

Predicted shape (mechanism, calibrated by Monte Carlo Section 5):
- Naive (m=50) on typical (r*~80): drift-crossing from 50 up toward ~80,
  distance 30, same mean path as LM2 but noisier (Poisson var = mean =
  0.8/position vs Bernoulli 0.16); MC mean T1 = 112 (LM2: 104).
- Informed (m~=73..80, polluted by atypical reveals) on typical:
  prior does most of the work; MC late-typical mean ~= 29/episode.
- Per-typical-episode advantage ~= 79; 9 episodes ~= 715 (MC mean).
- Atypical: treatment m~=73..80 vs r* in {40,47,54} -> slow; control
  m=50 is close -> fast. Negative transfer preserved (MC mean -261).

## 5. Threshold calibration (design-phase Monte Carlo, pure Zag)

A /tmp Zag program (`cal_fb.zag`) replicated the EXACT frozen mechanism
(verbatim `etc_ep`/`run_cond`; w=20, tol=5, N=1200, typical {76..84},
atypical {40,47,54} on episodes 4/8/12, independent streams, same LCG;
Poisson observations via integer CDF-inversion tables with fixed-point
e^-x series and genfail self-checks) over R=1000 replications with fresh
non-overlapping seeds (41,000,000+7*rep+{0,1,2}; disjoint from the frozen
20261010/11/12). Power analysis, not seed selection: no frozen-seed
outcome was observed or selected. The generator was independently
sanity-checked (`check_pois.zag`: 200,000 draws at r=80 give mean 0.7995,
variance 0.801, histogram matching Poisson(0.8) within sampling noise).
Results (means, sd, min, max):

- ADV_C (typical advantage, 9 eps): mean=715, sd=591, min=-1100, max=2975
- ADV_O (atypical advantage, 3 eps): mean=-261, sd=241, min=-1436, max=1028
- T1: mean=112, sd=175, min=1, max=1201
- TLATE (T9+T10+T11): mean=86, sd=142, min=3, max=1212
- TMID (T5+T6+T7): mean=60, sd=117, min=3, max=1326
- DEC = 3*T1-TLATE: mean=250, sd=551, min=-1086
- STAB = TLATE-TMID: mean=25, sd=178, min=-1319
- MAXET: mean=501, sd=291, min=86, max=1201
- cap hits: 46/24,000 episode-runs (0.19%/run); genfail: 0/1000 reps

Threshold derivations (frozen):
- B5a = 343: 0.48x the calibrated mean (715), 0.63 sd below it; nominal
  power ~74% (lower than LM2/MG's ~92-94%: the honest cost of the noisier
  Poisson family). Substantively: >=38 examples saved per typical episode
  (~34% of the naive ~112). Same 0.48x principle as LM2's 350 and MG's 370.
- B5g = 0 (sign): calibrated mean -261, sd 241; P(<=0) ~= 0.86. Tests the
  predicted negative-transfer SIGN on atypical episodes, separated from B5a.
- B5b = 75: same substantive bar as LM2/MG (>=25/episode improvement over
  the learner's own naive start); calibrated E[DEC]=250, sd=551, nominal
  P(pass) ~= 0.62. Secondary consistency bar; reported with numbers.
- B5c = 150: coarse no-catastrophe bound as in LM2/MG (calibrated mean 25,
  sd 178; nominal P(pass) ~= 0.76). Secondary; reported with numbers.
- B5d = 25: unchanged floor-validity bar (calibrated T1 mean 112, nominal
  P(pass) ~= 0.69). If T1 < 25 the verdict is UNDECIDED (task too easy by
  luck of the draw), never a pass.
- B5f cap 1200: calibrated cap-hit 0.19%/episode-run -> ~4.5% per-run VOID
  risk; accepted, stated.

## 6. Frozen predictions

- P1: T_1 >= 25 (naive learner does real statistical work; MC mean 112).
- P2: ADV_C = SUM_{k in typical}(EC_k - ET_k) >= 343 (MC mean 715).
- P3: ADV_O = SUM_{k in atypical}(EC_k - ET_k) <= 0 (MC mean -261).
- P4: 3*T_1 - (T_9+T_10+T_11) >= 75 (MC mean 250).
- P5: (T_9+T_10+T_11) - (T_5+T_6+T_7) <= 150 (MC mean 25).
- P6: 3/3 runs byte-identical; 12 parameters distinct; 24 observation
  vectors distinct; pstar identical across conditions; streams
  cross-disjoint.

## 7. Frozen kill bars

- B1 COMMIT-ORDER: PASS iff this prereg (+ NAMECHECK.md Step 0) is committed
  before any implementation file, and every implementation commit strictly
  postdates the prereg commit.
- B2 TOOLCHAIN: PASS iff PATH is safebin-only for all work,
  `which python3`, `which python`, `which perl`, `which ruby`,
  `which node` all return empty, all scientific computation is
  znc-compiled Zag, and zero forbidden executables are invoked.
- B3 DETERMINISM: PASS iff 3/3 runs of the frozen binary are pairwise
  byte-identical (cmp); sha256 digests recorded.
- B4 NOVELTY: PASS iff the binary prints DISTINCTB=1 (12 parameters
  pairwise distinct) and DISTINCTF=1 (24 observation vectors pairwise
  distinct). Else VOID.
- B5a TYPICAL-ADVANTAGE (PRIMARY): PASS iff ADV_C >= 343.
- B5b DECREASE: PASS iff 3*T_1 - TLATE >= 75.
- B5c STABILITY: PASS iff TLATE - TMID <= 150.
- B5d FLOOR-VALIDITY: PASS iff T_1 >= 25. If T_1 < 25 the verdict is
  UNDECIDED (task too easy; redesign), never a pass.
- B5e STREAM-VALIDITY: PASS iff BIASID=1 (per-episode parameter identical
  across conditions) AND XDISJ=1 (every treatment observation vector
  differs byte-wise from its same-episode control vector) AND MARG=1
  (per-condition TOTAL observation counts within [6480, 12240] of the
  14400 positions; gross PRNG fault check). Expected total 10332
  (1200 * (9*0.80 + 1.41)), sd ~102; bounds are ~19/38 sd wide, a
  gross-fault check as in LM2/MG (same numerals, new meaning: counts,
  not ones). Else VOID.
- B5f APPARATUS: PASS iff every etc_k <= 1200 and genfail = 0. Else VOID.
- B5g NEGATIVE-TRANSFER (signature, secondary): PASS iff ADV_O <= 0.
- B6 NO-RESEARCHER-META-RULE: PASS iff (a) the cross-episode update's only
  input is the revealed parameter, (b) grep for episode-index/counter
  references inside learner code returns empty, (c) the driver never
  modifies (sum, count) except via the learner's update (treatment) or
  re-initialization to m=50 (control), AND (d) `etc_ep` and `run_cond`
  are byte-identical to the frozen `lm2.zag` (diff-verified), with only
  the six permitted change classes of Section 3. The estimator form,
  w = 20, and initial m = 50 are disclosed researcher-supplied mechanism;
  the learned quantity is m itself.
- B7 OPAQUE-IDS: PASS iff episode labels are exactly E01..E12, parameters
  and observations are bare integers, and a grep audit for the frozen
  semantic word list (coin, bias, heads, tails, shrink, prior, learn,
  meta, cluster, outlier, typical, atypical, general, poisson, rate,
  lambda, gauss, count, event, slot, family) in sources returns empty.

## 8. Verdict mapping (frozen)

- B1 fail: VOID. B2 fail: PROCESS-FAIL. B3 fail: UNDECIDED (name the
  decisive rerun). B4, B5e, or B5f fail: VOID. B5d fail: UNDECIDED.
- B5a PASS (+ B5d PASS): TRANSFER-ACROSS-FAMILIES DEMONSTRATED -- the
  frozen learner acquires the new family's typical parameter value in its
  own state and converts it into fewer examples per new typical problem;
  the LM2 meta-learning effect is NOT specific to the Bernoulli family.
  The reset ablation attributes the speedup to persistence, as in LM2/MG.
- B5a FAIL: NO TRANSFER (family-specific). Report the numbers. The LM2
  effect does not survive the Bernoulli -> Poisson family change even
  with the learner held fixed; the meta-learning claim is family-bound.
- B5b / B5c: secondary consistency bars; reported with numbers.
- B5g FAIL: SIGNATURE MISMATCH (negative transfer absent on atypical
  episodes); reported prominently; does not overturn a B5a PASS.

## 9. How this tests the boundary

META-GENERALIZE's verdict rested on the Bernoulli bias-learning family at
two locations. The remaining rival explanation this design can exclude is
family-specificity: the mechanism might depend on the Bernoulli
observation model (binary flips, p(1-p) noise, probability parameter)
rather than implementing a general distribution-typical-value learner.
This experiment holds the learner (byte-identical), the typical location
(80), the gap (30), the atypical set, the apparatus (N=1200, w=20,
tol=5), and the analysis all fixed and changes ONLY the task family
(Bernoulli -> Poisson). A B5a PASS therefore excludes the
family-specificity rival for this pair; a B5a FAIL confirms it. Option C
(distractor-then-original) remains untested either way.

## 10. Honest boundaries (pre-declared)

- This is ONE new family: a PASS shows the effect is not Bernoulli-bound,
  NOT full generality across all families. Option C remains untested.
- What is learned is the PRIOR MEAN over parameters: empirical-Bayes
  base-rate learning (L1/L2-ish), same as LM2/MG. Not strategy invention,
  not L3. The estimator form, w=20, initial m=50 are researcher-supplied
  mechanism; the learned quantity is m.
- The truth-reveal per episode is supervised; within-episode learning is
  unsupervised (zero feedback).
- The new seed triple (20261010/11/12) was fixed here before any
  implementation ran; no seed was selected on outcomes.
- The MARG check keeps LM2/MG's numerals with the new meaning
  (per-condition total observation counts, expected 10332, sd ~102);
  preregistered here; the check remains a gross-fault check, not a fitted
  one.
- The harness's tolerance check is measurement scaffolding, not a learning
  signal: the learner never observes it.
- The calibration Monte Carlo used the same PRNG family with disjoint
  seeds; it estimated the mechanism's sampling distribution under the new
  family (power analysis). The frozen seed triple was fixed here before
  any implementation ran; no seed was selected on outcomes.
- Nominal power on the primary bar is ~74% (vs ~92-94% for LM2/MG): the
  Poisson family is noisier per observation, so the same 0.48x-mean bar
  principle buys less power. This is stated, not hidden; the bar was not
  moved to chase power.
