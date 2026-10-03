# PREREG: LIFETIME-META-1 -- Does examples-to-criterion decrease with experience?

Committed BEFORE any implementation. Frozen kill bars; no weakening after results.
Commit order: this prereg (+ NAMECHECK.md Step 0) strictly precedes all implementation.

## 0. Amendment history (transparent)

- v1 (commit 174f6d0): problem family = hidden 2-step register programs,
  learner = persistent form-pair inventory with move-to-front.
- v2 (this file): problem family REPLACED by biased-coin bias learning
  with a learned shrinkage prior. Reason (design analysis, NO
  implementation run, NO data seen): for the program family, every
  accepted dominant-form episode is identified by the naive learner in
  exactly 2 examples -- the five canonically-earlier wrong forms are
  provably dead by example 2 (two die at example 1 outright; the linear
  ones force slope 1 by example 2, and slope-1 survivors are rejected by
  the uniqueness check), so T_1 = 2 always and B5d (T_1 >= 3) could never
  pass: zero headroom for any decrease. Additionally, (ADD,MUL) is
  functionally identical to (MUL,ADD) by distributivity, which would
  have forced the uniqueness filter to reject most dominant episodes.
  The flaw is structural (identification is too easy in small exact
  symbolic spaces), not tunable. The coin family below has a large,
  mechanism-proven naive-vs-informed gap because statistical
  identification under noise needs many examples while a learned prior
  cuts through it. All bars below are new and frozen.

## 1. Question

Constitution: "Learning to learn: examples-to-criterion must decrease with
experience; causal ablation required." The H-CONTLIFE series showed a
persistent learner across episodes. This experiment tests whether the
persistent learner gets FASTER at new learning problems as experience
accumulates (meta-learning), with a reset control as the causal ablation.

## 2. Problem family (frozen)

Biased-coin bias learning. Each episode: a hidden bias p* (hundredths,
integer 10..90). Examples: a stream of N = 300 binary flips,
flip = 1 iff PRNG draw < p*. The learner must estimate p*.

Episode generation (frozen deterministic procedure; LCG
s <- (s*1103515245 + 12345) mod 2^31, seed 20261003):

- 9 "cluster" episodes use 9 DISTINCT biases, a PRNG permutation of
  {66,67,68,69,70,71,72,73,74} (mean 70), placed on all episodes except
  4, 8, 12 (1-indexed).
- 3 "outlier" episodes (4, 8, 12) use 3 DISTINCT biases, a PRNG
  permutation of {40,47,54}.
- All 12 biases are pairwise distinct. The task distribution has a
  learnable regularity (biases cluster near 70); the learner is never
  told this.
- Flips: for each episode, 300 flips from the PRNG (draw < p*). The
  12 x 300 flip matrix is generated ONCE and shared by both conditions
  (common random numbers): the reset control sees the identical example
  streams, so any treatment/control difference is caused only by
  persistence.
- genfail flag on PRNG/logic fault (none expected); genfail = 1 -> VOID.

Novelty: every episode has a distinct bias AND a distinct flip vector
(in-Zag pairwise check, B5e). The flip sequences are never repeated.

## 3. Learner (frozen, generic)

Shrinkage estimator with a learned prior mean. After n flips with h
heads, with prior mean m (hundredths) and frozen pseudo-count w = 20:

  est = (w*m + 100*h) / (w + n)          (hundredths; integer arithmetic)

- Treatment: m = mean of all PAST episodes' true biases (integer floor;
  m = 50 before the first episode). The accumulated state is (sum, count)
  -- the learner's own persistent structure. After each episode the truth
  p* is revealed (supervised episode boundary, not a within-episode
  signal) and folded into (sum, count).
- Control: IDENTICAL estimator, identical code path, identical flips,
  but m is re-initialized to 50 at every episode start (reset ablation:
  no accumulation).

The update takes ONLY the revealed bias as input -- never the episode
index, never problem identity (B6 audit). No within-episode feedback:
the learner never sees whether its current estimate is good.

## 4. Metric: examples-to-criterion (etc)

For an episode, etc = the smallest n in {1..300} with
|est_n - p*| < 5 (i.e., within 0.05), evaluated by the harness with exact
integer arithmetic |num - p**den| < 5*den. If never reached, etc = 301
(B5e apparatus bar then fails -> VOID; the frozen parameters make this
measure-zero: worst case needs ~200 flips).

Predicted shape (mechanism-proven, not fitted):
- etc^T_1 = etc^C_1 EXACTLY (both naive: m = 50, same flips, same code;
  internal validity check). Naive needs n >~ 4*|50 - p*| - 20 flips
  (prior 20 points off, w = 20): ~60 for cluster episodes.
- After episode 1, treatment m ~= p*_1 (~70); on later cluster episodes
  |m - p*| <= ~10, so etc drops to ~1-16 (the prior does the work).
  Control stays ~30-80. The advantage appears as a STEP after the first
  experience and persists (m converges to ~64, still far better than 50
  for cluster episodes).
- Outlier episodes show transient NEGATIVE transfer (m ~= 64 is worse
  than 50 for p* in {40,47,54}): honest, tolerated by the sum bars.

## 5. Frozen predictions

- P1: T_1 == C_1 exactly, and T_1 >= 25 (naive learner does real
  statistical work; a floor start would leave no room to improve).
- P2: SUM_{k=2..12}(C_k - T_k) >= 150 -- persistence saves at least 150
  flips over the 11 post-first episodes (~13.6/episode; expected ~300
  from the mechanism: ~52/episode on 8 cluster episodes minus ~38/episode
  negative transfer on 3 outliers).
- P3: 3*T_1 - (T_9 + T_10 + T_11) >= 75 -- the learner's late-cluster
  etc is at least 25 flips below its own naive start (within-learner
  decrease; expected ~52).
- P4: (T_9 + T_10 + T_11) - (T_5 + T_6 + T_7) <= 24 -- no degradation
  with further experience (stability; both blocks are pure cluster
  episodes, expected difference ~0).
- P5: 3/3 runs byte-identical; all 12 biases distinct; all 12 flip
  vectors distinct.

## 6. Frozen kill bars

- B1 COMMIT-ORDER: PASS iff the prereg (v1 + this v2 amendment, each
  with NAMECHECK.md Step 0) is committed before any implementation
  file, and every implementation commit strictly postdates the v2
  commit.
- B2 TOOLCHAIN: PASS iff PATH is safebin-only for all work,
  `which python3`, `which python`, `which perl`, `which ruby`,
  `which node` all return empty, all scientific computation is
  znc-compiled Zag, and zero forbidden executables are invoked.
- B3 DETERMINISM: PASS iff 3/3 runs of the frozen binary are pairwise
  byte-identical (cmp); sha256 digests recorded.
- B4 NOVELTY: PASS iff the binary prints DISTINCTB=1 (12 biases pairwise
  distinct) and DISTINCTF=1 (12 flip vectors pairwise distinct).
  Else VOID.
- B5a ADVANTAGE: PASS iff SUM_{k=2..12}(C_k - T_k) >= 150.
- B5b DECREASE: PASS iff 3*T_1 - (T_9+T_10+T_11) >= 75.
- B5c STABILITY: PASS iff (T_9+T_10+T_11) - (T_5+T_6+T_7) <= 24.
- B5d FLOOR-VALIDITY: PASS iff T_1 >= 25. If T_1 < 25 the verdict is
  UNDECIDED (task too easy; redesign), never a pass.
- B5e MECHANISM-IDENTITY: PASS iff T_1 == C_1 exactly. Else VOID
  (implementation bug: common random numbers + identical naive state
  must give identical first episodes).
- B5f APPARATUS: PASS iff every etc_k <= 300 and genfail = 0. Else VOID.
- B6 NO-RESEARCHER-META-RULE: PASS iff (a) the cross-episode update's
  only input is the revealed bias, (b) grep for episode-index/counter
  references inside learner code returns empty, (c) the driver never
  modifies (sum, count) except via the learner's update (treatment) or
  re-initialization to (0,0)/m=50 (control). The estimator form, w = 20,
  and initial m = 50 are disclosed researcher-supplied mechanism; the
  learned quantity is m itself.
- B7 OPAQUE-IDS: PASS iff episode labels are exactly E01..E12, biases
  and flips are bare integers, and a grep audit for the frozen semantic
  word list (coin, bias, heads, tails, shrink, prior, learn, meta,
  cluster, outlier) in sources returns empty.

## 7. Verdict mapping (frozen)

- B1-B7 all PASS: META-LEARNING DEMONSTRATED (distribution-level: the
  learner acquires the task distribution's typical bias in its own
  persistent state and converts it into fewer examples per new problem;
  negative transfer on outliers is part of the signature).
- B5a or B5b FAIL: NO META-LEARNING. Report the numbers.
- B5c FAIL: DEGRADATION WITH EXPERIENCE. Report the numbers.
- B5d FAIL: UNDECIDED (floor; redesign and re-preregister, do not
  salvage).
- B4, B5e, or B5f FAIL: VOID. B1 FAIL: VOID. B2 FAIL: PROCESS-FAIL.
  B3 FAIL: UNDECIDED (name the decisive rerun).

## 8. Honest boundaries (pre-declared)

- What is learned is the PRIOR MEAN over biases: base-rate learning,
  L1/L2-ish, not L3 representational invention and not strategy
  invention. The estimator form, w = 20, and initial m = 50 are
  researcher-supplied mechanism; the speedup emerges from the
  accumulation of (sum, count), which the ablation isolates.
- The truth-reveal at episode end is supervised; within-episode learning
  is unsupervised (zero feedback). A fully autonomous version in which
  the learner itself decides when its estimate is good enough is future
  work.
- One frozen task distribution (12 episodes); generalization to other
  distributions untested. The outlier episodes are expected to show
  negative transfer; the claim is net advantage, not uniform dominance.
- The harness's tolerance check is measurement scaffolding, not a
  learning signal: the learner never observes it.
