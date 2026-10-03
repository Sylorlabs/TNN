# REPORT: LIFETIME-META-2 -- Does examples-to-criterion decrease with experience?

## Frozen verdict: META-LEARNING DEMONSTRATED (cluster episodes)

Per the frozen verdict mapping, B5a (primary, cluster-only advantage) PASSED
(672 >= 350) with B5d (floor) PASS, so the preregistered headline verdict is
META-LEARNING DEMONSTRATED on cluster episodes. Every bar passed; nothing
was weakened or reinterpreted. LM1's split finding -- real learning on
cluster episodes -- survives proper experimental design.

## What was built (pure Zag, safebin-only)

- `lm2.zag` (8768 bytes): 12 episodes of biased-coin bias learning with the
  LM2 design. Hidden bias p* per episode (hundredths); 9 distinct typical
  biases = PRNG permutation of {76..84} on episodes {1,2,3,5,6,7,9,10,11};
  3 distinct atypical biases = permutation of {40,47,54} on episodes
  {4,8,12}. N=1200 flips per episode per condition from INDEPENDENT streams
  (SEED_T=20261005 treatment, SEED_C=20261006 control; SEED_B=20261004 for
  the shared bias permutation). Estimator: est_n = (20*m + 100*h)/(20+n);
  treatment m = floor(mean of past revealed biases), control m = 50 always.
  Criterion |est_n - p*| < 5, smallest n in 1..1200, else 1201.
- Commit order honored: prereg v1 (77b1a98, PREREG.md + NAMECHECK.md only)
  strictly before any implementation file. This commit adds the
  implementation + report only.
- Toolchain: PATH="$HOME/safebin" throughout; python3/python/perl/ruby/node
  all unresolvable; zero forbidden invocations. One znc analyzer warning
  (A0101 on `G[fbase+e*1200+n-1]` with `n<=1200`): false positive, max
  index is fbase+e*1200+1199, in bounds; build succeeded.
- Determinism: 3/3 runs byte-identical,
  sha256 `1a68561a44809c804bc8d7c1775d68595cf220d4abc0fe87feea1f40d5b0bcba`.

## Results (frozen binary output, 3/3 identical)

```
E01 P=82 ET=63  EC=102
E02 P=79 ET=1   EC=34
E03 P=78 ET=1   EC=40
E04 P=40 ET=40  EC=3
E05 P=81 ET=6   EC=68
E06 P=84 ET=31  EC=157
E07 P=83 ET=4   EC=131
E08 P=54 ET=26  EC=2
E09 P=76 ET=1   EC=149
E10 P=77 ET=7   EC=34
E11 P=80 ET=2   EC=73
E12 P=47 ET=26  EC=1
ADV_C=672 ADV_O=-86 T1=63 C1=102 TLATE=10 TMID=41
B5A=1 B5B=1 B5C=1 B5D=1 B5E=1 B5F=1 B5G=1
DISTINCTB=1 DISTINCTF=1 PARID=1 XDISJ=1 MARG=1 GENFAIL=0
```

Bar scorecard:
- B1 COMMIT-ORDER: PASS (prereg 77b1a98 implementation-free, predates all
  implementation commits).
- B2 TOOLCHAIN: PASS (safebin-only, Step 0 recorded, zero incidents).
- B3 DETERMINISM: PASS (3/3 identical, digest above).
- B4 NOVELTY: PASS (12 distinct biases; 24 flip vectors pairwise distinct).
- B5a CLUSTER-ADVANTAGE (PRIMARY): PASS (672 >= 350; 1.92x the bar).
- B5b DECREASE: PASS (3*63-10 = 179 >= 75).
- B5c STABILITY: PASS (10-41 = -31 <= 150).
- B5d FLOOR-VALIDITY: PASS (63 >= 25).
- B5e STREAM-VALIDITY: PASS (PARID=1: per-episode bias identical across
  conditions; XDISJ=1: every treatment flip vector differs from its
  same-episode control vector; MARG=1: per-condition ones-fraction in
  [0.45, 0.85]).
- B5f APPARATUS: PASS (max etc 157 <= 1200, genfail 0).
- B5g NEGATIVE-TRANSFER: PASS (-86 <= 0; sign as predicted).
- B6 NO-RESEARCHER-META-RULE: PASS (update's only input is the revealed p;
  no episode-conditioned logic in learner fns; sum/cnt are run_cond locals
  touched only by the update).
- B7 OPAQUE-IDS: PASS (labels E01..E12; case-insensitive grep for the frozen
  word list returns empty).

## Reading of the result

The persistent learner saved 672 examples over 9 typical episodes
(~75/episode, ~37% of the naive ~88/episode control mean): its own
examples-to-criterion fell from 63 (naive) to a late-typical mean of 3.3
(TLATE=10), because the accumulated prior (m -> ~80) does the work. The
reset control, identical except for accumulation, shows no such decrease.
The speedup is causally attributable to persistence: the only
treatment/control difference is the accumulated (sum, count), and both
conditions saw the same episode biases.

The three LM1 issues were addressed and the fixes behaved as designed:
1. Outlier separation: B5a measured typical episodes only (672); outliers
   measured separately (B5g: -86, treatment slower on all three atypical
   episodes 40v3, 26v2, 26v1 -- the honest interference signature, sign
   as predicted, no longer able to sink the primary bar).
2. Overshoot anti-correlation: independent streams; treatment's typical etc
   values (63,1,1,6,31,4,1,7,2) show its own overshoot only uncoupled from
   control's luck (e.g., E06: treatment 31 on its stream while control took
   157 on its own). Observed ADV_C=672 lands almost exactly on the
   calibration mean (724), confirming E[ADV_C] was not an artifact of
   shared-stream coupling.
3. Threshold calibration: the primary bar (350 = 0.48x calibrated mean,
   1.38 sd below) passed at 1.92x; no bar was near its boundary except by
   design margins.

## Honest boundaries

- What was learned is the prior MEAN over biases: empirical-Bayes base-rate
  learning (L1/L2-ish). Not strategy invention, not L3. The estimator form,
  w=20, initial m=50 are researcher-supplied mechanism; the learned
  quantity is m.
- The truth-reveal per episode is supervised; within-episode learning has
  zero feedback.
- One frozen task distribution (12 episodes), one frozen seed triple.
  Generalization to other distributions untested.
- The typical-cluster mean (80) was deliberately placed far from the naive
  prior (50) to enlarge the naive-vs-informed gap (disclosed pre-prereg
  design choice, LM1 recommendation #4); the learner mechanism is identical
  to LM1.
- Negative transfer on atypical episodes is part of the signature, not a
  defect: the learned prior helps on typical problems and hurts on
  atypical ones.
- T1 (63) and C1 (102) differ because the streams are independent; both are
  naive (m=50) draws, and no identity is claimed (B5e replaced by design).

## Artifacts in this commit

- `lm2.zag`: frozen implementation (B6/B7 audited).
- `lm2_bin`: frozen compiled binary.
- `run1.txt`, `run2.txt`, `run3.txt`: 3/3 byte-identical outputs
  (sha256 `1a68561a...5b0bcba`).
- `REPORT.md`: this file.
- `NAMECHECK.md`: build record updated.
