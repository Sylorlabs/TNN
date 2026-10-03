# REPORT.md -- IVWC-SCOREBIAS: score-side bias-estimator improvements

## Verdict: BUILD-FAIL (K5, K7 fail; K1, K2, K3, K4, K6, K8, K9, K10 pass)

Better bias does NOT achieve strict dominance. But the wave is
decisive, not inconclusive: every frozen mechanism prediction was
confirmed exactly (all four variant accuracies on both regimes,
all four variant bars), V-UCB is the first strict in-distribution
improvement in the IVWC line (11/12 > OF's 10/12), and the
strict-dominance failure is now characterized as two structural
ceilings, not a bar artifact and not estimator noise.

Headline numbers (variant order: UCB, MAX, SHR0, SHRG):

- wp=15: UCB 11, MAX 5, SHR0 10, SHRG 10 vs OF 10, X3 9, HYB 9, MG 10
- wp=30: UCB 9, MAX 8, SHR0 8, SHRG 8 vs OF 8, X3 9, HYB 8, MG 8 (finding)
- wp=45: UCB 10, MAX 9, SHR0 9, SHRG 9 vs OF 8, X3 10, HYB 9, MG 10

V-UCB is never worse than the per-regime winner and strictly
better in-distribution: weak dominance, but not the preregistered
strict dominance (K5 needs strict on BOTH regimes; UCB ties X3
@45, 10 = 10).

## What was built

`src/ivwc_scorebias.zag` (pure Zag, single file, pinned znc),
`bin/ivwc_scorebias` (frozen binary). World/belief/composer/
stepper/verifier/seeds copied verbatim from IVWC-HYBRID; sealed
(bucket, eff) pairs bit-identical (K3/K4 anchors confirm).
New machinery, all in MAIN, all computed from the 24 train cases
only (no sealed data, no researcher-set constant except the
declared 1/2 shrinkage factor):

- Per-bucket train overconfidence d_t = preff_tr - teff; the
  original mean bias m_b = (0,4,15,16), gbias = 7.
- V-UCB (vv=0): m_b + isqrt(S_b/(n_b-1)), S_b = sum (d-m_b)^2.
  Trained: (0,16,27,20).
- V-MAX (vv=1): max train d per bucket. Trained: (0,33,33,20).
- V-SHR0 (vv=2): m_b/2. Trained: (0,2,7,8).
- V-SHRG (vv=3): (m_b+gbias)/2. Trained: (3,5,11,11).
- Shuffled-bias ablations vv=4..7 (same rotate-by-7 consequence
  shuffle as the hybrid).
- Each variant: adjV = P - BV[bkt], verdict adjV > TV (strict
  margin inherited from MG; TV = mean adjV over sealed batch).
- Anchors re-scored in-program: OF, X3, HYB (>=), MG (>).

Build: pinned znc `src/tools/toolchain/znc_linux_x86_64_abed8aa1
src/ivwc_scorebias.zag -o bin/ivwc_scorebias` under the safebin
PATH (python3/python unresolvable; Step 0 attested in
NAMECHECK.md). Analyzer: the standard zagd-unavailable
informational notice only; all constant-folding warnings
eliminated. No post-prereg probe of any kind; the hybrid's
committed per-case sealed outputs were not read (predictions
were derived from the published REPORT.md per-case details plus
the learner-visible train T-lines).

## Kill-bar results

- K1 (commit before signal / diet): PASS. K1T/K1P STRUCT-PASS,
  K1S STRUCT-PASS at sh=0/1/2. A1: train COMMIT (643) / PREFF
  (658) precede train CONSEQ world_execute (677); sealed COMMIT
  (874/876) precedes SCORING world_execute (978). A2: 0. A3: 0.
  A4: 0. A6: `world_execute(` x3 (def + 2 call sites);
  WC-FINAL=60 (24 train + 36 sealed). A7: 0 learner/belief
  calls in the SCORING section.
- K2 (determinism): PASS. 3/3 byte-identical, sha256
  ef8df60992ecc037d1f4bf60e034f4c5c09dcd491223db177fc591f122db7831.
- K3 (replication anchor, wp=15): PASS. acc_of=10, acc_x3=9.
- K4 (replication anchor, wp=45): PASS. acc_of=8, acc_x3=10.
- K5 (strict dominance): FAIL. No variant clears both regimes:
  UCB 11>10 @15 but 10=10 @45; the rest trail on at least one.
- K6 (@15 gain): PASS. UCB 11/12 > 10, the only strict
  in-distribution gain in the IVWC line to date.
- K7 (@45 gain): FAIL. Best variant ties X3 at 10/12.
- K8 (consequence-content): PASS. VSTAR=0 (UCB, argmax @15);
  shuffled UCB 3/12 < 11/12 @15 strictly. The bias CONTENT
  drives the gain, not the procedure.
- K9 (non-degenerate, wp=15): PASS. 11 > maj 7.
- K10 (MAX self-defeat): PASS. MAX 5/12 < OF 10/12 @15,
  exactly the predicted overcorrection collapse.

## Mechanism detail (white box)

### Why UCB wins @15 and what it fixes

Trained UCB biases (0,16,27,20) vs mean (0,4,15,16). The
action is bucket 2: bias_2 = 27 (mean 15 + sd 12; train
bucket-2 overconfidence is {12,25,17,0,0,33,18}, heavy-tailed).
Sealed s=0 @15 sits alone in bucket 2 with P=40: adj drops
40-27=13, exactly the variant bar (TV=13), and the strict
margin flips it to FAIL (true label FAIL). Every other @15
verdict holds: the four genuine bucket-1 positives keep a
margin of 4 above the bar (adj=17 > 13), s=10 stays FAIL,
bucket 3 behaves. UCB errors @15: {s=3} only.

The s=0 fix needs bias_2 >= 20; the mean (15) misses it, UCB
(27) clears it. The margin is load-bearing here: with >= the
13==13 tie would verdict PASS (wrong). Score-side and bar-side
compose; neither alone suffices.

### Ceiling 1 (@15): s=3 is unfixable by any per-bucket bias

s=3 (phantom items, P=50) shares bucket 1 with four genuine
positives (P=33). Raising bias_1 by D drops every bucket-1
case D relative to a bar that itself drops D/2, so s=3 flips
only at D > 50 while the positives flip at D > 16. No
per-bucket bias fixes s=3 without breaking four correct
verdicts first. 11/12 is the ceiling for the whole
bucket-bias + global-bar family @15, and UCB attains it.
The remaining error is bucket coarseness, not miscalibration:
fixing it needs case-level (not bucket-level) bias, which is
new machinery, not a better estimator.

### Ceiling 2 (@45): the train tail does not reach the law-change shift

s=0/s=4 @45 (P=50, bucket 1, true FAIL) need bias_1 > 44 to
flip while keeping the genuine bucket-1 positive (P=98)
above the dropping bar. The train bucket-1 tail caps at 33
(the single 33-point train miss); UCB reaches 16, MAX reaches
33, neither clears 44. UCB errors @45: {s=0, s=4} = X3's set,
10/12. No estimator computed from wp=15 train data can
anticipate the magnitude of the wp=15 -> 45 overconfidence
shift; the failure is train-tail coverage under law change.

### Why MAX self-destructs (K10 mechanism, confirmed)

V-MAX @15 errors {s=0,s=2,s=3,s=4,s=6,s=7,s=9} -> 5/12. The
max bias (33/33/20) overcorrects: the four genuine bucket-1
positives flip to FAIL, the transductive bar chases the
correction down to TV=4, and the phantom s=3 (adj=17, largest
P) still sits above it. Worst-case bias is self-defeating
under a mean bar: it inverts the ranking it was meant to
calibrate. @45 MAX adds s=5 (adj=13 > TV=8) -> 9/12.

### Why shrinkage is neutral (predicted)

SHR0/SHRG @15 = 10/12 = OF; @45 = 9/12. The textbook
bias-variance trade moves the wrong way here: the residual
errors are confident optimism (adj too HIGH), and shrinkage
reduces correction. Both variants preserve the structural
FPs exactly. Shrinkage is the right answer to sampling noise;
the hybrid's problem is tail risk, not noise.

### Ablation anomaly @45 (honest reporting)

The fixed rotate-by-7 shuffle happens to produce large
bucket-1/2 shuffled biases (UCBsh b1=55, MAXsh b1=50),
exceeding the @45 flip threshold (44), so UCBsh scores 12/12
and MAXsh 11/12 @45. This is shuffle luck, not a legitimate
estimator: the rotation is arbitrary, and under the @45
label skew (11/12 FAIL) any huge-bias rule looks good. It is
mechanism-confirming luck, though: it proves the @45 errors
are fixable by bias_1 > 44, i.e. the binding constraint is
the train tail's coverage (max 33), not the verdict
structure. K8 (@15) is unaffected: there the shuffle
destroys performance (3/12 < 11/12), confirming consequence
content drives the real gain.

## Scoreboard

wp=15: UCB 11, SHR0 10, SHRG 10, MAX 5 vs OF 10, X3 9, HYB 9, MG 10
wp=30: UCB 9, SHR0 8, SHRG 8, MAX 8 vs OF 8, X3 9, HYB 8, MG 8
wp=45: UCB 10, SHR0 9, SHRG 9, MAX 9 vs OF 8, X3 10, HYB 9, MG 10

Variant bars (TV): @15: 13, 4, 24, 21; @45: 13, 8, 19, 16 --
all four exactly as preregistered.

## Honest caveats

1. One wall-density law-change axis; item law, belief noise,
   and energy budget fixed (inherited from the hybrid setup).
2. Tpred/TV are computed over the sealed batch (transductive),
   but from predictions + learned biases only; no world data
   enters any bar.
3. The 12-case test makes every bar a one-case margin; the
   UCB @15 gain rests on the s=0 tie at TV=13 flipped by the
   strict margin, verified per-case.
4. The consequence-training diet (24 true train outcomes at
   wp=15) is declared in PREREG section 7, not hidden; sealed
   verdicts never observe sealed truth (K1).
5. Mechanism test, not a composition-novelty or L3 claim (per
   PREREG section 7). The composer is fixed; the claims concern
   bias estimators for the hybrid verdict loop.
6. K5's "exists variant" form tests four preregistered
   estimators, not a blind search; the per-variant mechanism
   predictions (section 5 of the prereg) named UCB as the
   predicted gainer before implementation.
7. The @45 shuffled-ablation fluke (12/12) is reported above
   and does not alter K8, which is @15-scoped by the prereg.

## What this closes and what it opens

Closed: the score-side follow-up recommended by IVWC-PERBUCKET.
Better bias was tested in four principled forms; UCB gives the
first strict in-distribution gain, but strict dominance is
unattainable for train-computable per-bucket biases on these
regimes, for two structural reasons (bucket coarseness @15,
train-tail coverage @45). Further estimator tuning within the
per-bucket family cannot beat 11/12 @15 or 10/12 @45.

Open, in priority order: (1) case-level (not bucket-level)
bias signals for phantom-type errors like s=3 -- the bias
must see what the bucket cannot; (2) law-change-robust bias
that extrapolates beyond the train tail, e.g. bias with a
structural model of how overconfidence scales with wp rather
than a statistic of the wp=15 tail; (3) retiring the
transductive mean bar, whose chase-down behavior both enables
(shuffled @45) and punishes (MAX @15) large corrections.

## Reproduction

```
cd docs/lab/research-lead/overnight-20260928/ivwc_scorebias
~/workspace/tnn-rsi-gpi3/src/tools/toolchain/znc_linux_x86_64_abed8aa1 src/ivwc_scorebias.zag -o bin/ivwc_scorebias   # safebin PATH, pinned znc
./bin/ivwc_scorebias | sha256sum   # expect ef8df60992ecc037d1f4bf60e034f4c5c09dcd491223db177fc591f122db7831
```

Frozen audits (PREREG section 8): A1 ordering 643/658 < 677 and
874/876 < 978; A2 count 0; A3 count 0; A4 count 0; A5 sha256
equality across runs/ivwc_scorebias-run{1,2,3}.txt; A6
`world_execute(` count 3, WC-FINAL=60; A7 count 0.

## Branch note

Work committed on `tnn-native-lab`. Prereg commit ec3d8561c
strictly precedes the implementation commit. All commits use
explicit pathspecs confined to `ivwc_scorebias/`. Local only,
never pushed. Git writes via /usr/bin/git directly (safebin git
symlink is known-broken for writes). Note: this worker was
spawned on a checkout parked at lane-ma4b-20261003 with
tnn-native-lab checked out in the sibling worktree
~/workspace/tnn-rsi-gpi3 (active workers there, in other lane
dirs); all work and commits were done in the gpi3 worktree on
tnn-native-lab per the task constraint.
