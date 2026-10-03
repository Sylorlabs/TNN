# PREREG: LIFETIME-META-2 -- Does examples-to-criterion decrease with experience?

Committed BEFORE any implementation. Fresh experiment (not an amendment):
new prereg, new seed, new design. Frozen kill bars; no weakening after results.
Commit order: this prereg (+ NAMECHECK.md Step 0) strictly precedes all
implementation files.

## 0. Relation to LM1 (C405)

LM1 (frozen verdict: NO META-LEARNING on the net-advantage claim) produced a
split finding: B5b (within-learner decrease) PASSED decisively (226 >= 75)
while B5a (net paired advantage) FAILED (-39 < 150). Post-hoc mechanism
analysis (LM1 REPORT.md) diagnosed three issues:

1. **Outlier conflation:** B5a summed cluster speedup (+141/9 episodes) with
   outlier negative transfer (-180/3 episodes). The bar mixed two phenomena.
2. **Overshoot coupling (unpredicted, confirmed):** under shared flip streams,
   a head-heavy start makes control converge early while treatment overshoots
   above p*+5 and decays slowly (LM1 E02: control n=13, treatment n=51). This
   anti-correlation inflates var(C-T) under common random numbers.
3. **Threshold miscalibration:** B5a's bar (150) exceeded the mechanism's true
   expectation (~125) for LM1's design; the bar was set from a flawed
   hand-analysis that missed the overshoot coupling.

LM2 is a FRESH test of the split finding (real learning on cluster episodes)
with all three issues addressed by design (Section 9), plus the effect-size
enlargement LM1's report recommended considering (cluster mean moved from
~70 to ~80, widening the naive-vs-informed gap; learner mechanism unchanged).

## 1. Question

Constitution: "Learning to learn: examples-to-criterion must decrease with
experience; causal ablation required." Does the persistent shrinkage learner
get FASTER at new problems as experience accumulates, compared against a
reset control (causal ablation isolating persistence)? The primary claim is
tested on CLUSTER (typical) episodes only; outlier episodes get a separate
negative-transfer signature bar.

## 2. Problem family (frozen)

Biased-coin bias learning, 12 episodes. Each episode: hidden bias p*
(hundredths, integer). Examples: a stream of N = 1200 binary flips,
flip = 1 iff PRNG draw < p*. The learner must estimate p*.

Episode generation (frozen deterministic procedure; LCG
s <- (s*1103515245 + 12345) mod 2^31):

- Seed SEED_B = 20261004: 9 "cluster" episodes use 9 DISTINCT biases, a PRNG
  Fisher-Yates permutation of {76,77,78,79,80,81,82,83,84} (mean 80),
  placed on all episodes except 4, 8, 12 (1-indexed).
- Same seed stream: 3 "outlier" episodes (4, 8, 12) use 3 DISTINCT biases,
  a PRNG permutation of {40,47,54}.
- All 12 biases are pairwise distinct. The task distribution has a learnable
  regularity (biases cluster near 80); the learner is never told this.
- Flips: INDEPENDENT streams per condition (this is the LM1b fix for the
  overshoot anti-correlation). After reseeding to SEED_T = 20261005, 12x1200
  flips for the treatment episodes (draw < p*); after reseeding to
  SEED_C = 20261006, 12x1200 flips for the control episodes. Both conditions
  see the SAME episode biases; their flip trajectories are independent.
- The three seeds are arbitrary, consecutive, and frozen here. Consecutive
  LCG seeds diverge immediately (first draws differ by 1103515245 mod 2^31);
  stream independence is audited by B5e (cross-condition disjointness).
- genfail flag on PRNG/logic fault (none expected); genfail = 1 -> VOID.

Novelty: every episode has a distinct bias; all 24 flip vectors (12 per
condition) are pairwise distinct (in-Zag check, B4/B5e).

## 3. Learner (frozen, generic; identical to LM1)

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

## 4. Metric: examples-to-criterion (etc)

For an episode, etc = smallest n in {1..1200} with |est_n - p*| < 5,
exact integer arithmetic |num - p**den| < 5*den. If never reached,
etc = 1201 (B5f apparatus bar then fails -> VOID; calibration Section 5
bounds this risk at ~0.1%).

Predicted shape (mechanism, calibrated by Monte Carlo Section 5):
- Naive (m=50) on cluster (p*~80): drift-crossing median ~4*(p*-55) ~= 100;
  MC mean T1 = 104.
- Informed (m~=80) on cluster: |m - p*| <= 4, prior does the work;
  MC late-cluster mean ~= 18/episode.
- Per-cluster-episode advantage ~= 80; 9 episodes ~= 724 (MC mean).
- Outliers: treatment m~=73..80 vs p* in {40,47,54} -> slow (MC mean
  ~-275/3 episodes); control m=50 is close -> fast. Negative transfer
  is the honest signature.

## 5. Threshold calibration (design-phase Monte Carlo, pure Zag)

A /tmp Zag program replicated the EXACT frozen mechanism (w=20, tol=5,
N=1200, cluster {76..84}, outliers {40,47,54} on episodes 4/8/12,
independent streams, same LCG) over R=1000 replications with fresh
non-overlapping seeds (1,000,000+7*rep+13 etc.; disjoint from the frozen
20261004/05/06). This is power analysis, not seed selection: no frozen-seed
outcome was observed or selected. Results (means, sd, min, max):

- ADV_C (cluster advantage, 9 eps): mean=724, sd=271, min=-122, max=1833
- ADV_O (outlier advantage, 3 eps): mean=-275, sd=194, min=-1293, max=335
- T1: mean=104, sd=81, min=15, max=689
- TLATE (T9+T10+T11): mean=54, sd=64
- TMID (T5+T6+T7): mean=35, sd=44
- DEC = 3*T1-TLATE: mean=259, sd=252, min=-323
- STAB = TLATE-TMID: mean=18, sd=77
- MAXET=956, MAXEC=1201 over 24,000 episode-runs (cap-hit rate ~0.004%/ep)

Threshold derivations (frozen):
- B5a = 350: 0.48x the calibrated mean (724), 1.38 sd below it; nominal
  power ~92%. Substantively: >=39 examples saved per cluster episode
  (~37% of the naive ~104). LM1's miscalibrated 150 is replaced by a
  mechanism-quantified bar.
- B5g = 0 (sign): calibrated mean -275, sd 194; P(<=0) ~= 0.92. Tests the
  predicted negative-transfer SIGN on outliers, separated from B5a.
- B5b = 75: same substantive bar as LM1 (>=25/episode improvement over the
  learner's own naive start); calibrated E[DEC]=259.
- B5c = 150: LM1's 24 was unachievable under the noise (calibrated sd=77)
  and outlier-pollution of the prior (calibrated mean +18); loosened to a
  coarse no-catastrophe bound (nominal P(pass) ~= 0.96).
- B5d = 25: unchanged floor-validity bar (calibrated T1 mean 104).
- B5f cap 1200: calibrated cap-hit ~0.1% per full run; accepted, stated.

## 6. Frozen predictions

- P1: T_1 >= 25 (naive learner does real statistical work; MC mean 104).
- P2: ADV_C = SUM_{k in cluster}(EC_k - ET_k) >= 350 (MC mean 724).
- P3: ADV_O = SUM_{k in outliers}(EC_k - ET_k) <= 0 (MC mean -275).
- P4: 3*T_1 - (T_9+T_10+T_11) >= 75 (MC mean 259).
- P5: (T_9+T_10+T_11) - (T_5+T_6+T_7) <= 150 (MC mean 18).
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
- B5a CLUSTER-ADVANTAGE (PRIMARY): PASS iff ADV_C >= 350.
- B5b DECREASE: PASS iff 3*T_1 - TLATE >= 75.
- B5c STABILITY: PASS iff TLATE - TMID <= 150.
- B5d FLOOR-VALIDITY: PASS iff T_1 >= 25. If T_1 < 25 the verdict is
  UNDECIDED (task too easy; redesign), never a pass.
- B5e STREAM-VALIDITY (replaces LM1's B5e MECHANISM-IDENTITY, which required
  T_1 == C_1 under shared streams): PASS iff BIASID=1 (per-episode bias
  identical across conditions) AND XDISJ=1 (every treatment flip vector
  differs byte-wise from its same-episode control vector) AND MARG=1
  (per-condition fraction of 1s within [0.45, 0.85] of flips; gross PRNG
  fault check). Else VOID.
- B5f APPARATUS: PASS iff every etc_k <= 1200 and genfail = 0. Else VOID.
- B5g NEGATIVE-TRANSFER (signature, secondary): PASS iff ADV_O <= 0.
- B6 NO-RESEARCHER-META-RULE: PASS iff (a) the cross-episode update's only
  input is the revealed bias, (b) grep for episode-index/counter references
  inside learner code returns empty, (c) the driver never modifies
  (sum, count) except via the learner's update (treatment) or
  re-initialization to m=50 (control). The estimator form, w = 20, and
  initial m = 50 are disclosed researcher-supplied mechanism; the learned
  quantity is m itself.
- B7 OPAQUE-IDS: PASS iff episode labels are exactly E01..E12, biases and
  flips are bare integers, and a grep audit for the frozen semantic word
  list (coin, bias, heads, tails, shrink, prior, learn, meta, cluster,
  outlier) in sources returns empty.

## 8. Verdict mapping (frozen)

- B1 fail: VOID. B2 fail: PROCESS-FAIL. B3 fail: UNDECIDED (name the
  decisive rerun). B4, B5e, or B5f fail: VOID. B5d fail: UNDECIDED.
- B5a PASS (+ B5d PASS): META-LEARNING DEMONSTRATED on cluster episodes --
  the persistent learner acquires the task distribution's typical bias in
  its own state and converts it into fewer examples per new typical
  problem; the reset ablation attributes the speedup to persistence.
- B5a FAIL: NO META-LEARNING (cluster-advantage claim). Report the numbers.
- B5b / B5c: secondary consistency bars; reported with numbers.
- B5g FAIL: SIGNATURE MISMATCH (negative transfer absent on outliers);
  reported prominently; does not overturn a B5a PASS.

## 9. How LM2 addresses LM1's three diagnosed issues

1. Outlier separation: the primary bar (B5a) sums ONLY the 9 cluster
   episodes. Outliers are measured by their own bar (B5g) with the
   predicted negative sign. No phenomenon is hidden inside another bar.
2. Overshoot anti-correlation: treatment and control draw INDEPENDENT flip
   streams (SEED_T / SEED_C). A head-heavy trajectory can no longer make
   control lucky AND treatment overshoot on the same flips; E[ADV_C] is
   unchanged by independence (linearity of expectation) while the
   anti-correlation variance inflation is removed. B5e (T_1 == C_1) is
   replaced by the stream-validity audit (bias identity + cross-condition
   disjointness + marginal sanity).
3. Threshold calibration: every numeric bar is set from a 1000-rep
   mechanism Monte Carlo (Section 5), not from hand analysis. The primary
   bar sits at 0.48x the calibrated mean with ~92% nominal power; the
   stability bar was loosened from LM1's noise-impossible 24 to 150.

## 10. Honest boundaries (pre-declared)

- What is learned is the PRIOR MEAN over biases: empirical-Bayes base-rate
  learning (L1/L2-ish). Not strategy invention, not L3. The estimator form,
  w = 20, initial m = 50 are researcher-supplied mechanism; the learned
  quantity is m.
- The truth-reveal at episode end is supervised; within-episode learning is
  unsupervised (zero feedback).
- One frozen task distribution (12 episodes), one frozen seed triple.
  Generalization to other distributions untested.
- The cluster mean (80) was placed far from the naive prior (50) to enlarge
  the naive-vs-informed gap per LM1's recommendation; this is a disclosed
  design choice, not a fitted one (frozen before implementation).
- The harness's tolerance check is measurement scaffolding, not a learning
  signal: the learner never observes it.
- The calibration Monte Carlo used the same PRNG family with disjoint seeds;
  it estimated the mechanism's sampling distribution (power analysis). The
  frozen seed triple was fixed here before any implementation ran; no seed
  was selected on outcomes.
