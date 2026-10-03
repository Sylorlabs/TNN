# PREREG: META-DISTRACTOR -- Does a distractor distribution interfere with subsequent learning on the original distribution?

Committed BEFORE any implementation. Fresh experiment (not an amendment):
new prereg, new seeds, new episode sequence. Frozen kill bars; no weakening
after results. Commit order: this prereg (+ NAMECHECK.md Step 0) strictly
precedes all implementation files.

## 0. Relation to META-GENERALIZE (C415) and META-FAMILY-B (C419)

META-GENERALIZE froze TRANSFER DEMONSTRATED across cluster location
(B5a ADV_C=679>=370, all bars PASS). META-FAMILY-B (Bernoulli->Poisson)
froze UNDECIDED: the floor-validity luck tripwire fired (T1=14<25 at
calibrated P~=0.31) and the primary bar was unmet on an underpowered draw
(ADV_C=267<343, 22nd percentile); the run licenses neither a transfer nor
a family-specificity claim. The remaining untested option from
META-GENERALIZE's honest boundary is Option C (distractor-then-original).

This experiment tests Option C with the LEARNER FROZEN: the learner
mechanism (`etc_ep` byte-identical to the frozen `lm2.zag`; `run_cond`
identical except the episode-count loop bound, Section 3) is held fixed;
ONLY the episode sequence changes (a distractor distribution first, then
the original LM2 distribution). Key question: does the distractor
interfere with (or help) subsequent learning on the original? This tests
robustness of the meta-learning to distribution shift.

## 1. Question

Constitution: "Learning to learn: examples-to-criterion must decrease with
experience; causal ablation required." LM2/MG showed the persistent
shrinkage learner acquires a task distribution's typical parameter value
and converts it into fewer examples per new typical problem. Is that
acquired "meta-knowledge" robust when the distribution shifts -- here,
when the learner first faces a competing distribution (distractor) and
then returns to the original? The primary claim is tested on the ORIGINAL
distribution's typical episodes only; the distractor phase serves as the
manipulation (with its own check), and atypical episodes get separate
signature bars as in LM2/MG/FB.

## 2. Problem sequence (frozen)

Bernoulli bias-learning family (LM2's original family; the family question
was Option B's and is not re-litigated here). 24 episodes. Each episode:
hidden bias p* (hundredths, integer). Examples: a stream of N = 1200
binary flips, flip = 1 iff PRNG draw < p*.

Episode generation (frozen deterministic procedure; LCG
s <- (s*1103515245 + 12345) mod 2^31):

- Seed SEED_B = 20261013: episodes 1-12 ("D", the distractor): 9 episodes
  use 9 DISTINCT biases, a PRNG Fisher-Yates permutation of
  {16,17,18,19,20,21,22,23,24} (mean 20; MG's validated distribution),
  placed on all episodes except 4, 8, 12 (1-indexed). The 3 remaining
  episodes (4, 8, 12) use 3 DISTINCT biases, a PRNG permutation of
  {40,47,54} (unchanged from LM2/MG/FB).
- Same seed stream: episodes 13-24 ("R", the original distribution): 9
  episodes use 9 DISTINCT biases, a PRNG Fisher-Yates permutation of
  {76,77,78,79,80,81,82,83,84} (mean 80; LM2's original distribution),
  placed on episodes 13,14,15,17,18,19,21,22,23 (1-indexed). The 3
  remaining episodes (16, 20, 24) use 3 DISTINCT biases, a PRNG
  permutation of {40,47,54}.
- Within each 12-episode block the 12 biases are pairwise distinct. The
  atypical set {40,47,54} repeats across blocks BY DESIGN (both blocks use
  their historically validated distributions); this is disclosed, not a
  novelty violation (B4 is defined per-block).
- Flips: INDEPENDENT streams per condition. After reseeding to
  SEED_T = 20261014, 24x1200 flips for the treatment episodes; after
  reseeding to SEED_C = 20261015, 24x1200 for the control episodes. Both
  conditions see the SAME episode biases; their flip trajectories are
  independent.
- The three seeds are consecutive, frozen here, and disjoint from LM2's
  triple (20261004/05/06), MG's triple (20261007/08/09), FB's triple
  (20261010/11/12), and every calibration seed. Consecutive LCG seeds
  diverge immediately; stream independence is audited by B5e.
- genfail flag on PRNG/logic fault (none expected); genfail = 1 -> VOID.

DESIGN RATIONALE (why this distractor): the 20-location is MG's validated
distribution, so block D is a replication-with-new-seeds (manipulation
check), and 20 sits on the opposite side of the naive 50 from 80,
maximizing the shift's stringency: the distractor prior (~26) ends up
FARTHER from the original typicals (80) than even the naive prior (50).
The family is held at Bernoulli (LM2's) so that ONLY the sequence
changes; the family change was Option B's variable.

Novelty: within each block the 12 biases are pairwise distinct; all 48
flip vectors (24 per condition) are pairwise distinct (in-Zag check,
B4/B5e).

## 3. Learner (FROZEN from LM2; mechanism identical)

Shrinkage estimator with a learned prior mean. After n flips with h heads,
with prior mean m (hundredths) and frozen pseudo-count w = 20:

  est = (w*m + 100*h) / (w + n)          (hundredths; integer arithmetic)

- Treatment: m = mean of all PAST episodes' true biases (integer floor;
  m = 50 before the first episode). Persistent state is (sum, count),
  carried across ALL 24 episodes including the block boundary. After each
  episode the truth p* is revealed (supervised episode boundary, not a
  within-episode signal) and folded into (sum, count).
- Control: IDENTICAL estimator, identical code path, but m = 50 at every
  episode start (reset ablation: no accumulation). Control sees its OWN
  independent flip stream.

The update takes ONLY the revealed bias as input -- never the episode
index, never problem identity (B6 audit). No within-episode feedback.

FREEZE GUARANTEE: `etc_ep` in `md1.zag` is byte-identical to the frozen
`lm2.zag` (verified by diff before the implementation commit). `run_cond`
is identical except the episode-count loop-bound literal 12 -> 24
(harness change for the 24-episode sequence; the estimator and update
statements are byte-identical). The only other permitted source
differences between `md1.zag` and `lm2.zag` are: (a) `gen()` two-block
parameter assignment (block-D literals 16+i / block-R literals 76+i,
atypical literals unchanged) and 24-episode loops; (b) seed literals
20261004/05/06 -> 20261013/14/15; (c) arena offsets/sizes for 24 episodes
(28800 flips per condition) and the added tmp regions; (d) the threshold
literals (recalibrated, Section 5); (e) header/output label strings
(neutral identifiers retained); (f) malloc 32768 -> 65536; (g) a `med9`
helper (bubble-sort median of 9 i32 values) implementing the preregistered
luck-robust B5d floor; the helper is used only for the B5d median
computation and touches no learner code. Any other diff -> implementation
rejected. In particular the estimator form, w = 20, initial m = 50, and
the cross-episode update rule are unchanged: the experiment varies ONLY
the episode sequence.

AMENDMENT NOTE (v1.1, pre-implementation): class (g) was added by this
amendment because the v1 permitted list omitted the helper required by the
already-preregistered B5d median bar. No bar, threshold, prediction, or
verdict mapping is changed by this amendment; it only names the apparatus
implementing a frozen bar. Amended and re-frozen BEFORE any implementation
file was committed or run.

## 4. Metric: examples-to-criterion (etc)

Identical to LM2: etc = smallest n in {1..1200} with |est_n - p*| < 5,
exact integer arithmetic |num - p**den| < 5*den. If never reached,
etc = 1201 (B5f apparatus bar then fails -> VOID; calibration Section 5
bounds this risk: max etc 1201 observed once in 1000x48 episode-runs).

Predicted shape (mechanism, calibrated by Monte Carlo Section 5):
- Block D replicates MG: naive (m=50) on D-typicals (p*~20) drifts down
  from 50 (MC mean T1 = 101); informed (m~=20) is fast; MC ADV_D mean 765.
- Treatment enters block R with m = floor(321/12) = 26 DETERMINISTICALLY
  (9x20 + 40+47+54 = 321 regardless of permutation order). Control m=50.
- Block-R typicals (p*~80): treatment drifts from ~26 (distance ~54),
  control from 50 (distance 30) -> treatment slower: MC ADV_R mean -406
  (INTERFERENCE). MC mean T13 (first block-R treatment typical) = 201.
- As block-R reveals (~80s) accumulate, m climbs 26 -> ~49: treatment's
  own etc decreases across block R (RECOVERY, MC DEC_R mean 183),
  approaching but not beating control within 12 episodes (full return
  to ~80 needs ~100+ reveals: m_k = (321+80k)/(12+k) >= 75 only at
  k >= 116).
- Block-R atypicals: NO systematic effect predicted (MC ADV_O2 mean -8,
  sd 99): which atypical value lands on the early block-R episodes is
  permuted, so the distractor prior is sometimes closer, sometimes
  farther, averaging to ~0. (An early design hypothesis of a positive
  "reversal" was corrected by the calibration; Section 5.)

## 5. Threshold calibration (design-phase Monte Carlo, pure Zag)

A /tmp Zag program (`cal_md.zag`) replicated the EXACT frozen mechanism
(verbatim `etc_ep`; `run_cond` with the 24-episode loop bound; w=20,
tol=5, N=1200, block D {16..24}/{40,47,54} on episodes 4,8,12, block R
{76..84}/{40,47,54} on episodes 16,20,24, independent streams, same LCG)
over R=1000 replications with fresh non-overlapping seeds
(51,000,000+7*rep+{0,1,2}; disjoint from the frozen 20261013/14/15).
Power analysis, not seed selection: no frozen-seed outcome was observed
or selected. Results (means, sd, min, max):

- ADV_D (block-D typical advantage, 9 eps): mean=765, sd=258, min=-23, max=1793
- ADV_R (block-R typical advantage, 9 eps): mean=-406, sd=377, min=-1628, max=995
- ADV_OD (block-D atypical advantage, 3 eps): mean=-218, sd=180, min=-1415, max=472
- ADV_O2 (block-R atypical advantage, 3 eps): mean=-8, sd=99, min=-818, max=604
- T1: mean=101, sd=81, min=15, max=562
- MEDCD (median of 9 control block-D typicals): mean=83, sd=24, min=35, max=210
- MEDCR (median of 9 control block-R typicals): mean=84, sd=23, min=38, max=177
- DEC_R = (T13+T14+T15)-(T21+T22+T23): mean=183, sd=247, min=-626, max=1598
- STAB_R = (T21+T22+T23)-(T17+T18+T19): mean=-49, sd=228, min=-1143, max=672
- MAXET (max etc over 48 runs): mean=408, sd=138, min=166, max=1201
- T13: mean=201, sd=118, min=38, max=959
- MGT/MGC (per-condition total ones): mean=14183/14182, sd=72/73 (expected 14184)

Threshold derivations (frozen):
- B5a = 0 (sign): the predicted effect is INTERFERENCE (negative). Calibrated
  mean -406, sd 377; P(ADV_R <= 0) ~= 0.86. A magnitude bar at the 0.48x
  level (-195) would have only ~71% nominal power (sd 377), below the
  adequacy line C419's lesson demands; the directional prediction is the
  preregistered claim, so the sign bar is primary. The 0.48x magnitude
  level (-195) is reported as a secondary consistency check (B5h).
- B5d2 = 365 (manipulation): 0.48x the calibrated ADV_D mean (765),
  same principle as LM2's 350 / MG's 370; nominal power ~94%.
  If the distractor was not learned, the interference test is invalid.
- B5g = 0 (sign): calibrated ADV_OD mean -218, sd 180; P(<=0) ~= 0.89.
  Tests the predicted negative-transfer sign on block-D atypicals,
  separated from B5a. ADV_O2 is report-only (predicted ~= 0).
- B5b = 75: same substantive bar as LM2/MG (>=25/episode improvement over
  the learner's own early-block-R start); calibrated E[DEC_R]=183, sd=247,
  nominal P(pass) ~= 0.67. Secondary consistency bar; reported with numbers.
- B5c = 150: coarse no-catastrophe bound as in LM2/MG (calibrated mean -49,
  sd 228; nominal P(pass) ~= 0.81). Secondary; reported with numbers.
- B5d = 25: luck-robust floor (C419's lesson): MEDIAN over the 9 naive
  control typicals per block, not T1 alone (which tripped C419's tripwire
  at calibrated P ~= 0.31). Calibrated medians 83/84 with sd 24/23;
  P(fire) < 0.001. If either median < 25 the verdict is UNDECIDED (task
  too easy by luck of the draw), never a pass.
- B5e MARG bounds [12700,15700]: expected per-condition ones 14184,
  sd ~72; bounds are ~20sd, a gross-fault check as in LM2/MG/FB.
- B5f cap 1200: calibrated max etc 1201 in 1000x48 episode-runs;
  small per-run VOID risk, accepted and stated.

## 6. Frozen predictions

- P1: MEDCD >= 25 and MEDCR >= 25 (naive control does real statistical
  work in both blocks; MC means 83/84).
- P2: ADV_D = SUM_{block-D typical}(EC-ET) >= 365 (manipulation: the
  distractor distribution is learned; MC mean 765).
- P3: ADV_R = SUM_{block-R typical}(EC-ET) <= 0 (INTERFERENCE; MC mean -406).
- P4: ADV_OD = SUM_{block-D atypical}(EC-ET) <= 0 (MC mean -218).
- P5: ADV_O2 ~= 0, no systematic sign (MC mean -8, sd 99); report-only.
- P6: DEC_R = (T13+T14+T15)-(T21+T22+T23) >= 75 (recovery; MC mean 183).
- P7: STAB_R = (T21+T22+T23)-(T17+T18+T19) <= 150 (MC mean -49).
- P8: 3/3 runs byte-identical; 12 block-D biases distinct; 12 block-R
  biases distinct; 48 flip vectors distinct; pstar identical across
  conditions; streams cross-disjoint.

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
- B4 NOVELTY: PASS iff the binary prints DISTINCTBD=1 (12 block-D biases
  pairwise distinct) and DISTINCTBR=1 (12 block-R biases pairwise
  distinct) and DISTINCTF=1 (48 flip vectors pairwise distinct). The
  cross-block repeat of the atypical set {40,47,54} is by design
  (Section 2), not a novelty violation. Else VOID.
- B5a INTERFERENCE (PRIMARY): PASS iff ADV_R <= 0.
- B5b RECOVERY: PASS iff DEC_R >= 75.
- B5c STABILITY: PASS iff STAB_R <= 150.
- B5d FLOOR-VALIDITY (luck-robust): PASS iff MEDCD >= 25 AND MEDCR >= 25.
  If either fails the verdict is UNDECIDED (task too easy; redesign),
  never a pass.
- B5d2 MANIPULATION: PASS iff ADV_D >= 365. If FAIL the verdict is
  UNDECIDED (distractor not learned; the interference test is invalid),
  never "no interference".
- B5e STREAM-VALIDITY: PASS iff PARID=1 (per-episode bias identical across
  conditions) AND XDISJ=1 (every treatment flip vector differs byte-wise
  from its same-episode control vector) AND MARG=1 (per-condition ones
  count within [12700,15700]; gross PRNG fault check). Else VOID.
- B5f APPARATUS: PASS iff every etc_k <= 1200 and genfail = 0. Else VOID.
- B5g NEGATIVE-TRANSFER (signature, secondary): PASS iff ADV_OD <= 0.
  ADV_O2 reported with numbers (no bar).
- B5h MAGNITUDE (secondary): report ADV_R against the 0.48x level -195;
  no bar.
- B6 NO-RESEARCHER-META-RULE: PASS iff (a) the cross-episode update's only
  input is the revealed bias, (b) grep for episode-index/counter references
  inside learner code returns empty, (c) the driver never modifies
  (sum, count) except via the learner's update (treatment) or
  re-initialization to m=50 (control), AND (d) `etc_ep` is byte-identical
  to the frozen `lm2.zag` and `run_cond` differs from it ONLY in the
  episode-count loop-bound literal 12 -> 24 (diff-verified), with only the
  six permitted change classes of Section 3. The estimator form, w = 20,
  and initial m = 50 are disclosed researcher-supplied mechanism; the
  learned quantity is m itself.
- B7 OPAQUE-IDS: PASS iff episode labels are exactly E01..E24, biases and
  flips are bare integers, and a grep audit for the frozen semantic word
  list (coin, bias, heads, tails, shrink, prior, learn, meta, cluster,
  outlier, typical, atypical, general, poisson, rate, lambda, gauss, count,
  event, slot, family, distractor, shift, phase, regime, original,
  interference, recover) in sources returns empty.

## 8. Verdict mapping (frozen)

- B1 fail: VOID. B2 fail: PROCESS-FAIL. B3 fail: UNDECIDED (name the
  decisive rerun). B4, B5e, or B5f fail: VOID. B5d fail: UNDECIDED.
  B5d2 (manipulation) fail: UNDECIDED.
- B5a PASS (+ B5d PASS + B5d2 PASS): INTERFERENCE DEMONSTRATED -- the
  distractor distribution's learned prior interferes with subsequent
  learning on the original distribution; the LM2 meta-learning is NOT
  robust to distribution shift (single-regime prior commitment). The
  reset ablation attributes the slowdown to the persistent distractor
  history, as the only treatment/control difference is (sum, count).
- B5a FAIL with ADV_R > 0: NO INTERFERENCE -- the distractor did not
  interfere with original-distribution learning (unexpected robustness);
  report the numbers. This would be the surprising outcome.
- B5b / B5c / B5g / B5h: secondary consistency bars; reported with numbers.
- B5g FAIL: SIGNATURE MISMATCH on block-D atypicals; reported prominently;
  does not overturn a B5a PASS.

## 9. How this tests the boundary

LM2/MG established that the frozen learner acquires a task distribution's
typical parameter value and speeds up on new typical problems (transfer
across location). The rival explanation this design excludes is
shift-robustness: that the acquired prior is a general "learning to learn"
improvement rather than a single-regime commitment. The design holds the
learner, the family, the gap, the atypical set, the apparatus, and the
analysis fixed and varies ONLY the episode sequence (distractor block
then original block). A B5a PASS shows the distractor prior actively hurts
on the original distribution -- the meta-knowledge is regime-specific and
overwrites, the meta-learning analogue of catastrophic interference. A
B5a FAIL with ADV_R > 0 would show unexpected robustness. Either way, with
the manipulation check gating interpretation, the run discriminates.

## 10. Honest boundaries (pre-declared)

- This is ONE shift scenario (20 -> 80, Bernoulli family): a PASS shows
  interference under this shift, NOT that all shifts interfere. The
  magnitude and recovery speed are specific to the 12-episode blocks and
  the w=20 inertia.
- What is learned is the PRIOR MEAN over biases: empirical-Bayes base-rate
  learning (L1/L2-ish), same as LM2/MG/FB. Not strategy invention, not L3.
  The estimator form, w=20, initial m=50 are researcher-supplied mechanism;
  the learned quantity is m.
- The truth-reveal per episode is supervised; within-episode learning is
  unsupervised (zero feedback).
- The new seed triple (20261013/14/15) was fixed here before any
  implementation ran; no seed was selected on outcomes.
- The calibration Monte Carlo used the same PRNG family with disjoint
  seeds; it estimated the mechanism's sampling distribution under the new
  sequence (power analysis). The frozen seed triple was fixed here before
  any implementation ran; no seed was selected on outcomes.
- The primary bar is a sign bar (not the family's usual 0.48x magnitude
  bar) because the calibrated sd (377) makes the magnitude bar
  underpowered (~71%); the directional interference prediction carries
  ~86% nominal power. The 0.48x level (-195) is reported as B5h. This
  choice is stated, not hidden.
- The harness's tolerance check is measurement scaffolding, not a learning
  signal: the learner never observes it.
- C419 (Option B) remains UNDECIDED and is not re-litigated here; a PASS
  here does not imply cross-family generality.
