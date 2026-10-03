# REPORT: META-GENERALIZE -- Does the LM2 meta-learning transfer to a new task distribution?

## Frozen verdict: TRANSFER DEMONSTRATED (new distribution)

Per the frozen verdict mapping, B5a (primary, typical-only advantage on the
NEW distribution) PASSED (679 >= 370) with B5d (floor) PASS, so the
preregistered headline verdict is TRANSFER DEMONSTRATED: the frozen LM2
learner acquires the new distribution's typical bias (near 20) in its own
state and converts it into fewer examples per new typical problem. Every
bar passed; nothing was weakened or reinterpreted. The LM2 meta-learning
effect is NOT tied to the 80-location geometry.

## What was built (pure Zag, safebin-only)

- `mg1.zag`: the LM2 experiment with ONLY the task distribution changed.
  12 episodes of bias learning with hidden integer parameter p per episode;
  9 episodes (idx 0,1,2,4,5,6,8,9,10) use p = PRNG permutation of
  {16..24} (mean 20); 3 episodes (idx 3,7,11) use p = permutation of
  {40,47,54} (unchanged from LM2). N=1200 flips per episode per condition
  from INDEPENDENT streams (SEED_T=20261008 treatment, SEED_C=20261009
  control; SEED_B=20261007 for the shared bias permutation). Learner:
  est_n = (20*m + 100*h)/(20+n); treatment m = floor(mean of past revealed
  p), control m = 50 always. Criterion |est_n - p| < 5, smallest n in
  1..1200, else 1201.
- Learner freeze verified: full diff of `mg1.zag` vs frozen `lm2.zag`
  shows ONLY the five prereg-permitted change classes (typical-bias
  literals 76+i -> 16+i; seeds 20261004/05/06 -> 20261007/08/09; MARG
  bounds [6480,12240] -> [2880,5040]; B5a literal 350 -> 370;
  header/output label strings). `etc_ep` and `run_cond` are byte-identical
  (no diff hunks in their ranges).
- Commit order honored: prereg v1 (86d015d, PREREG.md + NAMECHECK.md only)
  strictly before any implementation file. This commit adds the
  implementation + report only.
- Toolchain: PATH="$HOME/safebin" throughout; python3/python/perl/ruby/node
  all unresolvable; zero forbidden invocations. One znc analyzer warning
  (A0101 on `G[fbase+e*1200+n-1]` with `n<=1200`): false positive, max
  index is fbase+e*1200+1199, in bounds; build succeeded. Same warning
  class as LM2's build (learner code unchanged).
- Determinism: 3/3 runs byte-identical,
  sha256 `23132878677f5f93c3f8953544e3d56b4b93645929e77f448b3213f9c94ce112`.

## Results (frozen binary output, 3/3 identical)

```
E01 P=20 ET=37  EC=105
E02 P=22 ET=1   EC=47
E03 P=18 ET=1   EC=67
E04 P=40 ET=108 EC=3
E05 P=24 ET=1   EC=36
E06 P=23 ET=1   EC=45
E07 P=17 ET=2   EC=244
E08 P=47 ET=26  EC=2
E09 P=21 ET=1   EC=50
E10 P=19 ET=1   EC=68
E11 P=16 ET=23  EC=85
E12 P=54 ET=38  EC=1
ADV_C=679 ADV_O=-166 T1=37 C1=105 TLATE=25 TMID=4
B5A=1 B5B=1 B5C=1 B5D=1 B5E=1 B5F=1 B5G=1
DISTINCTB=1 DISTINCTF=1 PARID=1 XDISJ=1 MARG=1 GENFAIL=0
```

Bar scorecard:
- B1 COMMIT-ORDER: PASS (prereg 86d015d implementation-free, predates all
  implementation commits).
- B2 TOOLCHAIN: PASS (safebin-only, Step 0 recorded, zero incidents).
- B3 DETERMINISM: PASS (3/3 identical, digest above).
- B4 NOVELTY: PASS (12 distinct biases; 24 flip vectors pairwise distinct).
- B5a TYPICAL-ADVANTAGE (PRIMARY): PASS (679 >= 370; 1.84x the bar).
- B5b DECREASE: PASS (3*37-25 = 86 >= 75).
- B5c STABILITY: PASS (25-4 = 21 <= 150).
- B5d FLOOR-VALIDITY: PASS (37 >= 25).
- B5e STREAM-VALIDITY: PASS (PARID=1: per-episode bias identical across
  conditions; XDISJ=1: every treatment flip vector differs from its
  same-episode control vector; MARG=1: per-condition ones counts within
  the preregistered [2880,5040] bounds).
- B5f APPARATUS: PASS (max etc 244 <= 1200, genfail 0).
- B5g NEGATIVE-TRANSFER: PASS (-166 <= 0; sign as predicted).
- B6 NO-RESEARCHER-META-RULE: PASS (learner fns byte-identical to frozen
  LM2; update's only input is the revealed p; no episode-conditioned logic
  in learner fns; sum/cnt are run_cond locals touched only by the update).
- B7 OPAQUE-IDS: PASS (labels E01..E12; case-insensitive grep for the
  frozen word list, including typical/atypical/general, returns empty).

## Reading of the result

The frozen learner saved 679 examples over 9 typical episodes of the NEW
distribution (~75/episode, ~42% of the naive ~99/episode calibration
mean): its examples-to-criterion fell from 37 (naive) to a late-typical
mean of 8.3 (TLATE=25), because the accumulated prior (m -> ~20) does the
work. The reset control, identical except for accumulation, shows no such
decrease. Observed ADV_C=679 lands within 0.35 sd of the design-phase
calibration mean (772), confirming the mechanism's sampling distribution
is location-invariant as the symmetry argument predicted.

The negative-transfer signature transferred too: on all three atypical
episodes the treatment (prior ~20) was slower than the control (prior 50)
-- E04 108v3, E08 26v2, E12 38v1 -- for ADV_O=-166, sign as predicted.
The learned prior helps on typical problems and hurts on atypical ones,
at the new location, exactly as the mechanism predicts.

What this rules out: the rival explanation that LM2's cluster advantage
depended on the specific 80-vs-50 geometry. Gap, learner, atypical set,
apparatus, and analysis were all held fixed; only the typical cluster
location moved (80 -> 20). The effect survived at essentially identical
magnitude (679 vs LM2's 672; calibration means 772 vs 724).

## Honest boundaries

- This is ONE new distribution: the verdict is "not tied to the
  80-location," NOT full generality across all distributions. Options B
  (different task family) and C (distractor-then-original) remain untested.
- What was learned is the prior MEAN over biases: empirical-Bayes base-rate
  learning (L1/L2-ish), same as LM2. Not strategy invention, not L3. The
  estimator form, w=20, initial m=50 are researcher-supplied mechanism;
  the learned quantity is m.
- The truth-reveal per episode is supervised; within-episode learning has
  zero feedback.
- B5b passed at 86 >= 75, nearer its boundary than LM2's 179 -- expected
  under the calibrated sampling distribution (sd=248), not a concern, and
  the bar was frozen before the run.
- T1 (37) and C1 (105) differ because the streams are independent; both are
  naive (m=50) draws, and no identity is claimed (same design as LM2).

## Artifacts in this commit

- `mg1.zag`: frozen implementation (learner byte-identical to `lm2.zag`;
  B6/B7 audited).
- `mg1_bin`: frozen compiled binary.
- `run1.txt`, `run2.txt`, `run3.txt`: 3/3 byte-identical outputs
  (sha256 `23132878677f5f93c3f8953544e3d56b4b93645929e77f448b3213f9c94ce112`).
- `REPORT.md`: this file.
- `NAMECHECK.md`: build record updated.
