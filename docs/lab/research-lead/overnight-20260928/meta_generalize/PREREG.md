# PREREG: META-GENERALIZE -- Does the LM2 meta-learning transfer to a new task distribution?

Committed BEFORE any implementation. Fresh experiment (not an amendment):
new prereg, new seeds, new distribution. Frozen kill bars; no weakening after
results. Commit order: this prereg (+ NAMECHECK.md Step 0) strictly precedes
all implementation files.

## 0. Relation to LM2 (C411 META-LEARNING DEMONSTRATED)

LM2 froze the verdict META-LEARNING DEMONSTRATED on typical episodes
(B5a ADV_C=672>=350, all 13 bars PASS). Its preregistered honest boundary:
"One frozen task distribution, one frozen seed triple. Generalization to
other distributions untested."

This experiment tests that boundary with the LEARNER FROZEN: the learner
functions (`etc_ep`, `run_cond`) are copied byte-for-byte from the frozen
`lm2.zag`; ONLY the task distribution changes (Option A: different typical
cluster location). If the cluster-advantage effect survives at a new
location, the LM2 effect is not tied to the specific 80-location geometry.
If it fails, the LM2 meta-learning may be distribution-specific.

## 1. Question

Constitution: "Learning to learn: examples-to-criterion must decrease with
experience; causal ablation required." Is the persistent shrinkage
learner's speedup GENERAL across task distributions (a genuine
distribution-learning mechanism), or did LM2 merely overfit to one
frozen distribution (cluster near 80)? The primary claim is tested on the
NEW distribution's typical episodes only; atypical episodes get the same
separate negative-transfer signature bar as LM2.

## 2. New problem family (frozen)

Same biased-coin bias-learning family as LM2, NEW distribution. Each
episode: hidden bias p* (hundredths, integer). Examples: a stream of
N = 1200 binary flips, flip = 1 iff PRNG draw < p*.

Episode generation (frozen deterministic procedure; LCG
s <- (s*1103515245 + 12345) mod 2^31):

- Seed SEED_B = 20261007: 9 "typical" episodes use 9 DISTINCT biases, a PRNG
  Fisher-Yates permutation of {16,17,18,19,20,21,22,23,24} (mean 20),
  placed on all episodes except 4, 8, 12 (1-indexed).
- Same seed stream: 3 "atypical" episodes (4, 8, 12) use 3 DISTINCT biases,
  a PRNG permutation of {40,47,54} (UNCHANGED from LM2).
- All 12 biases are pairwise distinct. The task distribution has a learnable
  regularity (biases cluster near 20); the learner is never told this.
- Flips: INDEPENDENT streams per condition (LM2's fix retained). After
  reseeding to SEED_T = 20261008, 12x1200 flips for the treatment episodes
  (draw < p*); after reseeding to SEED_C = 20261009, 12x1200 flips for the
  control episodes. Both conditions see the SAME episode biases; their flip
  trajectories are independent.
- The three seeds are consecutive, frozen here, and disjoint from LM2's
  triple (20261004/05/06) and from every calibration seed. Consecutive LCG
  seeds diverge immediately (first draws differ by 1103515245 mod 2^31);
  stream independence is audited by B5e.
- genfail flag on PRNG/logic fault (none expected); genfail = 1 -> VOID.

DESIGN RATIONALE (why this distribution): the naive-vs-informed gap is held
CONSTANT (|50-20| = 30, identical to LM2's |80-50| = 30); only the typical
cluster LOCATION changes (80 -> 20). The atypical set is unchanged. This
isolates cluster location as the single causal variable: a PASS means the
mechanism is location-invariant, not that it survives a smaller gap. The
p(1-p) noise is symmetric about 50, so the mechanism's sampling
distribution should be near-identical; the calibration (Section 5)
confirms this rather than assuming it.

Novelty: every episode has a distinct bias; all 24 flip vectors (12 per
condition) are pairwise distinct (in-Zag check, B4/B5e).

## 3. Learner (FROZEN from LM2; byte-identical)

Shrinkage estimator with a learned prior mean. After n flips with h heads,
with prior mean m (hundredths) and frozen pseudo-count w = 20:

  est = (w*m + 100*h) / (w + n)          (hundredths; integer arithmetic)

- Treatment: m = mean of all PAST episodes' true biases (integer floor;
  m = 50 before the first episode). Persistent state is (sum, count).
  After each episode the truth p* is revealed (supervised episode boundary,
  not a within-episode signal) and folded into (sum, count).
- Control: IDENTICAL estimator, identical code path, but m = 50 at every
  episode start (reset ablation: no accumulation). Control sees its OWN
  independent flip stream.

The update takes ONLY the revealed bias as input -- never the episode
index, never problem identity (B6 audit). No within-episode feedback.

FREEZE GUARANTEE: `etc_ep` and `run_cond` in `mg1.zag` are byte-identical
to the frozen `lm2.zag` (verified by diff before the implementation
commit). The only permitted source differences between `mg1.zag` and
`lm2.zag` are: (a) `gen()` typical-bias literals 76+i -> 16+i; (b) seed
literals 20261004/05/06 -> 20261007/08/09; (c) MARG bound literals for the
new expected marginal (Section 7, B5e); (d) the B5a threshold literal
(recalibrated, Section 5); (e) header/output label strings (neutral
identifiers retained). Any other diff -> implementation rejected.

## 4. Metric: examples-to-criterion (etc)

Identical to LM2: etc = smallest n in {1..1200} with |est_n - p*| < 5,
exact integer arithmetic |num - p**den| < 5*den. If never reached,
etc = 1201 (B5f apparatus bar then fails -> VOID; calibration Section 5
bounds this risk: zero cap hits in 24,000 episode-runs).

Predicted shape (mechanism, calibrated by Monte Carlo Section 5):
- Naive (m=50) on typical (p*~20): drift-crossing from 50 down to ~20,
  distance 30, mirror of LM2's 80 case; MC mean T1 = 99 (LM2: 104).
- Informed (m~=20) on typical: |m - p*| <= 4, prior does the work;
  MC late-typical mean ~= 7/episode (LM2: 18/episode total 54/3).
- Per-typical-episode advantage ~= 86; 9 episodes ~= 772 (MC mean).
- Atypical: treatment m~=20..24 vs p* in {40,47,54} -> slow; control
  m=50 is within <=10 -> fast. Negative transfer preserved (MC mean -219).

## 5. Threshold calibration (design-phase Monte Carlo, pure Zag)

A /tmp Zag program (`cal_mg.zag`) replicated the EXACT frozen mechanism
(verbatim `etc_ep`/`run_cond`; w=20, tol=5, N=1200, typical {16..24},
atypical {40,47,54} on episodes 4/8/12, independent streams, same LCG)
over R=1000 replications with fresh non-overlapping seeds
(31,000,000+7*rep+{1,2,3}; disjoint from the frozen 20261007/08/09).
Power analysis, not seed selection: no frozen-seed outcome was observed
or selected. Results (means, sd, min, max):

- ADV_C (typical advantage, 9 eps): mean=772, sd=262, min=-492, max=1985
- ADV_O (atypical advantage, 3 eps): mean=-219, sd=175, min=-1576, max=398
- T1: mean=99, sd=81, min=15, max=902
- TLATE (T9+T10+T11): mean=21, sd=37
- TMID (T5+T6+T7): mean=25, sd=35
- DEC = 3*T1-TLATE: mean=275, sd=248, min=-238
- STAB = TLATE-TMID: mean=-3, sd=50
- MAXET: max 1026 over 24,000 episode-runs; cap-hit rate 0/24,000

Threshold derivations (frozen):
- B5a = 370: 0.48x the calibrated mean (772), 1.53 sd below it; nominal
  power ~94%. Substantively: >=41 examples saved per typical episode
  (~42% of the naive ~99). Same 0.48x principle as LM2's 350.
- B5g = 0 (sign): calibrated mean -219, sd 175; P(<=0) ~= 0.89. Tests the
  predicted negative-transfer SIGN on atypical episodes, separated from B5a.
- B5b = 75: same substantive bar as LM2 (>=25/episode improvement over the
  learner's own naive start); calibrated E[DEC]=275.
- B5c = 150: coarse no-catastrophe bound as in LM2 (calibrated mean -3,
  sd 50; nominal P(pass) > 0.99).
- B5d = 25: unchanged floor-validity bar (calibrated T1 mean 99, min 15).
- B5f cap 1200: calibrated cap-hit 0/24,000 runs; accepted, stated.

## 6. Frozen predictions

- P1: T_1 >= 25 (naive learner does real statistical work; MC mean 99).
- P2: ADV_C = SUM_{k in typical}(EC_k - ET_k) >= 370 (MC mean 772).
- P3: ADV_O = SUM_{k in atypical}(EC_k - ET_k) <= 0 (MC mean -219).
- P4: 3*T_1 - (T_9+T_10+T_11) >= 75 (MC mean 275).
- P5: (T_9+T_10+T_11) - (T_5+T_6+T_7) <= 150 (MC mean -3).
- P6: 3/3 runs byte-identical; 12 biases distinct; 24 flip vectors distinct;
  pstar identical across conditions; streams cross-disjoint.

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
- B4 NOVELTY: PASS iff the binary prints DISTINCTB=1 (12 biases pairwise
  distinct) and DISTINCTF=1 (24 flip vectors pairwise distinct). Else VOID.
- B5a TYPICAL-ADVANTAGE (PRIMARY): PASS iff ADV_C >= 370.
- B5b DECREASE: PASS iff 3*T_1 - TLATE >= 75.
- B5c STABILITY: PASS iff TLATE - TMID <= 150.
- B5d FLOOR-VALIDITY: PASS iff T_1 >= 25. If T_1 < 25 the verdict is
  UNDECIDED (task too easy; redesign), never a pass.
- B5e STREAM-VALIDITY: PASS iff BIASID=1 (per-episode bias identical across
  conditions) AND XDISJ=1 (every treatment flip vector differs byte-wise
  from its same-episode control vector) AND MARG=1 (per-condition ones
  count within [2880, 5040] of 14400 flips; gross PRNG fault check).
  Bounds changed from LM2's [6480,12240] because the new distribution's
  expected marginal is 3852 (vs 10332): typical mean 20, atypical
  {40,47,54} -> expected ones = 12*(180+141) = 3852; sd ~= 53; bounds are
  ~18/22 sd wide, a gross-fault check as before. Else VOID.
- B5f APPARATUS: PASS iff every etc_k <= 1200 and genfail = 0. Else VOID.
- B5g NEGATIVE-TRANSFER (signature, secondary): PASS iff ADV_O <= 0.
- B6 NO-RESEARCHER-META-RULE: PASS iff (a) the cross-episode update's only
  input is the revealed bias, (b) grep for episode-index/counter references
  inside learner code returns empty, (c) the driver never modifies
  (sum, count) except via the learner's update (treatment) or
  re-initialization to m=50 (control), AND (d) `etc_ep` and `run_cond`
  are byte-identical to the frozen `lm2.zag` (diff-verified). The estimator
  form, w = 20, and initial m = 50 are disclosed researcher-supplied
  mechanism; the learned quantity is m itself.
- B7 OPAQUE-IDS: PASS iff episode labels are exactly E01..E12, biases and
  flips are bare integers, and a grep audit for the frozen semantic word
  list (coin, bias, heads, tails, shrink, prior, learn, meta, cluster,
  outlier, typical, atypical, general) in sources returns empty.

## 8. Verdict mapping (frozen)

- B1 fail: VOID. B2 fail: PROCESS-FAIL. B3 fail: UNDECIDED (name the
  decisive rerun). B4, B5e, or B5f fail: VOID. B5d fail: UNDECIDED.
- B5a PASS (+ B5d PASS): TRANSFER DEMONSTRATED -- the frozen learner
  acquires the new distribution's typical bias in its own state and
  converts it into fewer examples per new typical problem; the LM2
  meta-learning effect is NOT tied to the 80-location. The reset ablation
  attributes the speedup to persistence, as in LM2.
- B5a FAIL: NO TRANSFER (on this distribution). Report the numbers. The
  LM2 effect may be location-specific; the meta-learning claim does not
  generalize even to a gap-matched new location.
- B5b / B5c: secondary consistency bars; reported with numbers.
- B5g FAIL: SIGNATURE MISMATCH (negative transfer absent on atypical
  episodes); reported prominently; does not overturn a B5a PASS.

## 9. How this tests LM2's honest boundary

LM2's verdict rested on one frozen distribution (typical near 80) and one
frozen seed triple. The only credible rival explanation for the
cluster-advantage effect that LM2's design could not exclude is
distribution-specificity: the mechanism might depend on the particular
80-vs-50 geometry rather than implementing a general
distribution-typical-value learner. This experiment holds the learner,
the gap, the atypical set, the apparatus, and the analysis all fixed and
moves ONLY the typical cluster location. A B5a PASS therefore excludes
the location-specificity rival; a B5a FAIL confirms it (at least for this
new location).

## 10. Honest boundaries (pre-declared)

- This is ONE new distribution: a PASS shows the effect is not tied to the
  80-location, NOT full generality across all distributions. Options B
  (different task family) and C (distractor-then-original) remain untested
  and are recorded as follow-ups.
- What is learned is the PRIOR MEAN over biases: empirical-Bayes base-rate
  learning (L1/L2-ish), same as LM2. Not strategy invention, not L3. The
  estimator form, w=20, initial m=50 are researcher-supplied mechanism;
  the learned quantity is m.
- The truth-reveal at episode end is supervised; within-episode learning is
  unsupervised (zero feedback).
- The new seed triple (20261007/08/09) was fixed here before any
  implementation ran; no seed was selected on outcomes.
- The MARG bound change is an apparatus adjustment for the new
  distribution's expected marginal (3852 vs 10332), preregistered here;
  the check remains a ~18sd gross-fault check, not a fitted one.
- The harness's tolerance check is measurement scaffolding, not a learning
  signal: the learner never observes it.
- The calibration Monte Carlo used the same PRNG family with disjoint
  seeds; it estimated the mechanism's sampling distribution under the new
  distribution (power analysis). The frozen seed triple was fixed here
  before any implementation ran; no seed was selected on outcomes.
