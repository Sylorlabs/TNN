# REPORT: LIFETIME-META-1 -- Does examples-to-criterion decrease with experience?

## Frozen verdict: NO META-LEARNING (net-advantage claim)

Per the frozen verdict mapping, B5a failed (ADV = -39 < 150), so the
preregistered headline verdict is NO META-LEARNING. This report gives
the full picture: B5b (within-learner decrease) PASSED decisively, the
control ablation held, and post-hoc analysis identifies exactly why B5a
failed -- including a prereg calibration error on my part and one
unpredicted real phenomenon (overshoot coupling). Nothing in the
frozen bars was weakened or reinterpreted.

## What was built (pure Zag, safebin-only)

- `lm.zag` (6798 bytes): 12 episodes of biased-coin bias learning.
  Hidden bias p* per episode (hundredths); 300 PRNG flips per episode
  (LCG, seed 20261003); 9 distinct cluster biases = permutation of
  {66..74} on episodes {1,2,3,5,6,7,9,10,11}; 3 distinct outlier biases
  = permutation of {40,47,54} on episodes {4,8,12}. Estimator:
  est_n = (20*m + 100*h)/(20+n); treatment m = mean of past revealed
  biases, control m = 50 always. Criterion |est_n - p*| < 5, smallest n.
  Both conditions share the identical flip matrix (common random numbers).
- Commit order honored: prereg v1 (174f6d0) then prereg v2 amendment
  (80d1edb), both before any implementation file. This commit adds the
  implementation + report only.
- Toolchain: PATH="$HOME/safebin" throughout; python3/python/perl/ruby/
  node all unresolvable; zero forbidden invocations. One znc analyzer
  warning (A0101 off-by-one heuristic on `G[56+e*300+n-1]` with
  `n<=300`): false positive, max index is 56+e*300+299, in bounds;
  build succeeded.
- Determinism: 3/3 runs byte-identical,
  sha256 `17eedbd39d72d0ee111de6a9da18148d5eb80f34247aba7f57770140e5b4480b`.

## Results (frozen binary output, 3/3 identical)

```
E01 P=74 ET=84 EC=84
E02 P=68 ET=51 EC=13
E03 P=67 ET=11 EC=9
E04 P=47 ET=15 EC=1
E05 P=66 ET=1  EC=11
E06 P=71 ET=37 EC=57
E07 P=72 ET=5  EC=71
E08 P=40 ET=114 EC=5
E09 P=70 ET=13 EC=32
E10 P=69 ET=1  EC=11
E11 P=73 ET=12 EC=68
E12 P=54 ET=58 EC=1
ADV=-39 T1=84 C1=84 TLATE=26 TMID=43
B5A=0 B5B=1 B5C=1 B5D=1 B5E=1 B5F=1 DISTINCTB=1 DISTINCTF=1 GENFAIL=0
```

Bar scorecard:
- B1 COMMIT-ORDER: PASS (v1 174f6d0, v2 80d1edb, both implementation-free).
- B2 TOOLCHAIN: PASS (safebin-only, Step 0 recorded).
- B3 DETERMINISM: PASS (3/3 identical, digest above).
- B4 NOVELTY: PASS (12 distinct biases, 12 distinct flip vectors).
- B5a ADVANTAGE: FAIL (-39 < 150). Decisive.
- B5b DECREASE: PASS (3*84-26 = 226 >= 75). Decisive.
- B5c STABILITY: PASS (26-43 = -17 <= 24).
- B5d FLOOR-VALIDITY: PASS (84 >= 25).
- B5e MECHANISM-IDENTITY: PASS (84 == 84).
- B5f APPARATUS: PASS (max etc 114 <= 300, genfail 0).
- B6 NO-RESEARCHER-META-RULE: PASS (update's only input is the revealed
  p*; no episode-conditioned logic in learner fns; driver never touches
  (sum,count) except via the update).
- B7 OPAQUE-IDS: PASS (labels E01..E12; frozen word-list grep empty).

## The split finding

The persistent learner DID get faster with experience: its own
examples-to-criterion fell from 84 (naive) to a late-cluster mean of
8.7 (B5b: 226 >= 75), with no degradation (B5c). The reset control
showed no decrease (early-half mean 29.2 vs late-half 31.3). The
speedup is causally attributable to accumulation: the only
treatment/control difference is the persistent (sum,count).

But the NET paired advantage failed (-39): on the 9 cluster episodes
persistence saved +141 flips (avg 15.7/episode); on the 3 outlier
episodes it cost -180 (avg -60/episode). The learned prior helps on
typical problems and hurts on atypical ones -- net negative on this
75/25 mixture.

## Diagnosis of the B5a shortfall (post-hoc, clearly labeled)

1. Outlier negative transfer (predicted in direction, underestimated in
   size): prereg expected ~-38/episode on outliers; observed ~-60.
   Cause: control's fixed m=50 is CLOSE to outlier biases {40,47,54},
   while treatment's learned m~=64 is FAR -- the prior actively hurts.
2. Overshoot coupling (UNPREDICTED, real, empirically confirmed): with
   shared flips, a head-heavy start makes control converge fast while
   treatment -- whose prior is already high -- OVERSHOOTS above p*+5
   and needs many flips to decay back. Verified on E02's exact flip
   trajectory: at n=13, h=11, control est=63.6 (converged, EC=13) while
   treatment est=78.2 (overshoot, converged only at n=51, ET=51).
   This anti-correlation inflates var(C-T) under common random numbers.
3. Prereg calibration error (mine): B5a's threshold (150) exceeded the
   mechanism's true expectation (~+125 even without bad luck). The bar
   was set from a flawed hand-analysis that missed the overshoot
   coupling. This is a design error, not a learner failure.

PRNG audit (independent /tmp Zag program, not part of the frozen
binary): marginal P(d<50) = 49951/100000; serial P(d2<50|d1<50) =
0.5027, P(d2<50|d1>=50) = 0.4986. The flip stream is sound; the
outcome is mechanism + seed luck, not apparatus bias.

## Honest boundaries

- What was learned is the prior MEAN over biases: empirical-Bayes
  base-rate learning (L1/L2-ish). Not strategy invention, not L3.
  The estimator form, w=20, initial m=50 are researcher-supplied
  mechanism; the learned quantity is m.
- The truth-reveal per episode is supervised; within-episode learning
  has zero feedback.
- One frozen task distribution, one frozen seed. The overshoot
  coupling is seed-dependent; the negative-transfer direction is not.
- The B5a bar conflated two phenomena (cluster speedup, outlier
  interference). A cleaner primary bar would test them separately.

## Recommended follow-up (LM1b, needs fresh prereg)

1. Primary bar = paired advantage on CLUSTER episodes only (the
   "faster with experience" question); outliers get their own
   negative-transfer bar (expected sign: negative).
2. Recalibrate thresholds from the mechanism analysis in this report
   (overshoot coupling included), with margin.
3. Consider independent flip streams per condition (kills the
   overshoot anti-correlation; B5e then needs replacing with a
   distributional identity check).
4. Consider a wider cluster / narrower tolerance to enlarge the
   naive-vs-informed gap if a bigger effect size is wanted.

## Artifacts in this commit

- `lm.zag`: frozen implementation (B6/B7 audited).
- `lm_bin`: frozen compiled binary.
- `run1.txt`, `run2.txt`, `run3.txt`: 3/3 byte-identical outputs
  (sha256 `17eedbd3...e5b4480b`).
- `REPORT.md`: this file.
- `NAMECHECK.md`: build record updated.
