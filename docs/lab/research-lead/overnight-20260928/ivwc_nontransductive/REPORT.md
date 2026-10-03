# REPORT.md -- IVWC-NONTRANSDUCTIVE: non-transductive verdicts

## Verdict: BUILD-PASS (K1 through K10 all pass)

The bar was the bottleneck. A non-transductive verdict -- the same mean
statistic, train scope instead of batch scope -- lets the perfect phantom
signal (D1) reach 11/12 @15, exactly its theoretical ceiling under any
threshold verdict, versus 8/12 under the transductive mean bar. Every
frozen mechanism prediction was confirmed exactly, including all nine
preregistered error sets.

Headline numbers (arms: A1=UCBxV_T, A2=UCBxV_N, A3=D1bxV_T, A4=D1bxV_N,
A5=D2bxV_T, A6=D2bxV_N; V_T = transductive mean bar, V_N =
non-transductive fixed train bar):

| arm | @15 (wp=15) | @30 (wp=30) | @45 (wp=45) |
|---|---|---|---|
| A1 UCB x V_T (anchor) | 11 {s=3} | 9 | 10 {s=0,s=4} |
| A2 UCB x V_N | 10 {s=0,s=3} | 7 {s=0,s=2,s=5,s=6,s=7} | 9 {s=0,s=4,s=5} |
| A3 D1b x V_T (anchor) | 8 {s=1,s=5,s=8,s=10} | 10 | 12 |
| A4 D1b x V_N (KEY) | **11 {s=5}** | **11 {s=2}** | **12** |
| A5 D2b x V_T (anchor) | 6 | 8 | 10 |
| A6 D2b x V_N | 8 {s=0,s=3,s=4,s=5} | 8 {s=2,s=4,s=6,s=7} | 10 {s=0,s=4} |
| anchors OF / X3 / HYB / MG | 10 / 9 / 9 / 10 | 8 / 9 / 8 / 8 | 8 / 10 / 9 / 10 |

The 2x2 interaction is the result: switching V_T -> V_N helps D1b
(+3 @15, +1 @30, +0 @45) and hurts-or-holds UCB (-1 @15, -2 @30, -1
@45). The non-transductive verdict is not "a better bar" in general; it
is specifically the verdict structure that stops punishing large
corrections.

## What was built

`src/ivwc_nontransductive.zag` (pure Zag, single file, pinned znc),
`bin/ivwc_nontransductive` (frozen binary). World/belief/composer/
stepper/verifier/seeds copied verbatim from IVWC-CASEBIAS-RETRY (sealed
(bucket, eff) pairs bit-identical; K3/K4 anchors confirm). The SENS
machinery was removed; the experimental variable is the verdict:

- Train (learner): COMMIT, PREFF, CONSEQ (harness), LEARN (UCB bucket
  bias recomputed: (0,16,27,20)), then BAR: T_fixed = mean over the 24
  train cases of (preff_tr - bucb[bkt_tr]). Program-derived: TFIXED=12
  (train adjV sums to 306; 306/24 = 12). No sealed data, no
  researcher-set constant anywhere in the bar.
- Sealed loop (wp=15/30/45, seeds verbatim): COMMIT (learner; preff,
  adjV_ucb), then learner verdicts A1 = (adjV_ucb > TV_ucb) with TV_ucb
  = mean sealed adjV_ucb (transductive) and A2 = (adjV_ucb > T_fixed)
  (non-transductive); anchors OF/X3/HYB/MG re-scored in-program.
- SCORING (harness, fenced): one world_execute per case (WC-FINAL=60),
  labels ge = (eff >= Tpred), nphantom counts from the true world, then
  D1b/D2b biases (bucb[bkt] + 40 iff nphantom>0, resp. rotated-by-7)
  with verdicts A3 = (d1adj > TV_d1b), A4 = (d1adj > T_fixed), A5 =
  (d2adj > TV_d2b), A6 = (d2adj > T_fixed).

The ONLY difference between V_T and V_N arms is the scope of the mean
bar (sealed batch vs train). Bias content is identical within each row,
so the 2x2 isolates the verdict structure.

Build: pinned znc `src/tools/toolchain/znc_linux_x86_64_abed8aa1
src/ivwc_nontransductive.zag -o bin/ivwc_nontransductive` under the
safebin PATH (`which python3` returns nothing; Step 0 attested in
NAMECHECK.md; no interpreter invoked at any step). Analyzer: the
standard zagd-unavailable informational notice only.

## Kill-bar results

- K1 (diet / commit order): PASS. Phase order 630<637<650<667<673<735
  <771<779<806<855. A2: 0 world_buf/world_off in learner decision fns
  (lc_*, learner_compose*, belief_execute, gather_cells,
  verifier_*). A3: 0. A4: 0. A5: `world_execute(` x3 (1 def + 2 call
  sites). A6: WC-FINAL=60 (24 train + 36 sealed). A7: 0 learner_/belief_
  calls after the SCORING marker. A8: 0 "oracle" tokens. In-program
  K1T/K1P/K1S STRUCT-PASS (0 world calls after train COMMIT, train
  PREFF, sealed COMMIT at all three shifts).
- K2 (determinism): PASS. 3/3 byte-identical, sha256
  `55fd7edfd6b7ef736e4c9b3c21908bbc6e323c96902de248898ab33cc6c6a8f4`.
- K3 (anchor @15): PASS. acc_of=10, acc_x3=9.
- K4 (anchor @45): PASS. acc_of=8, acc_x3=10.
- K5 (PRIMARY): PASS. A4 @15 = 11/12, error set exactly {s=5}
  (K5e=1, K5s=5). The three bar-chase errors (s=1, s=8, s=10) vanish;
  s=3 is fixed; s=5 remains.
- K6: PASS. A3 @15 = 8/12 (reproduces the bar-destroys-signal anchor;
  the signal is unchanged).
- K7: PASS. A2 @15 = 10/12 <= 10, errors {s=0, s=3}. The fixed bar
  alone is not a general improvement.
- K8: PASS. A6 @15 = 8 < A4 @15 = 11 (K8lt=1). The A4 gain is
  phantom-signal content, not a bar artifact.
- K9: PASS. A4 @45 = 12/12. The phantom correction generalizes under
  the wp=15->45 law change with a fixed bar.
- K10: PASS. A4 @30 = 11 > A3 @30 = 10 (K10gt=1).

## Mechanism detail (white box)

### Why V_N fixes D1b @15 (K5)

D1b adjV @15: s=3 (phantom, the case UCB misses) is pushed to -6, below
the unmoved bar T_fixed=12 -> correct FAIL. The +40 corrections on
s=0,3,5,6,11 no longer move the bar, so the untouched true-negatives
s=1, s=8 (adjV=0) and s=10 (adjV=9) stay below it -> correct FAIL.
Under V_T, those same corrections dragged TV below 0 and below 9,
flipping all three to wrong PASS. The verdict structure, not the
signal, was the difference between 8/12 and 11/12.

### Why s=5 remains (the ceiling proof)

s=5 @15 is a TRUE-POSITIVE phantom: nph=1 (one planned gather at a
cell with no true item) yet eff=33 >= Tpred=28 (ge=1). The binary +40
crushes it to adjV=-16. No single-threshold verdict on D1b adjV can
score 12/12 @15: s=5 at -16 must PASS while s=3 at -6 must FAIL, and
-16 < -6 is inverted, so every threshold errs on at least one of the
two. 11/12 is the THEORETICAL CEILING of the (D1b x threshold-verdict)
family. V_N attains the ceiling; V_T scores 3 below it. The remaining
error is bias crudeness (the binary +40 cannot distinguish 1-phantom
of 1 gather from 1-phantom of 4), not verdict structure. Fixing s=5
needs a better bias, which the retry explicitly closed as a research
line ("do not fund further bias-estimator variants").

### Why V_N hurts UCB (K7, and the @30/@45 pattern)

s=0 @15 (bkt=2, preff=40, eff=0): UCB adjV=13. Under V_T the bar sat at
exactly TV=13 and the strict margin flipped it to correct FAIL (the
scorebias report's load-bearing tie). Under V_N, 13 > T_fixed=12 ->
wrong PASS. The fixed bar loses UCB's tie-break: -1 @15. Under law
change the fixed bar cannot track the shifting adjV distribution at
all: A2 @30 = 7/12 (five false passes as the batch's adjV shifts up
while T_fixed stays at 12), A2 @45 = 9/12. The transductive bar's
virtue is batch adaptation; its vice is chase-down. V_N keeps only
what the corrections need: a bar they cannot move.

### Why D1b still reaches 12/12 @45 under V_N (K9)

@45 the D1b correction is decisive: every phantom case is crushed to
adjV <= 0, the single true positive (s=11) sits at 84. Any bar in
(0, 84] separates them; T_fixed=12 does. The correction generalizes
across the law change; the bar just has to stay out of the way.

### The @30 middle case (K10)

@30, V_T's chase-down costs D1b one case (10/12); V_N recovers it
(11/12, sole error s=2: adjV=17 > 12 PASS but ge=0, because the
batch-relative label threshold Tpred@30=35 exceeds eff=33 -- a
label/bar-scope mismatch no train-fixed bar can track, the same
adaptation limit as K7).

## Answers to the task's key questions

1. **Can a non-transductive verdict achieve 12/12 @15 with perfect
   phantom information (D1)?** No: 11/12, and that is the ceiling, not
   a shortfall. The bar was the bottleneck for 3 of D1's 4 @15 errors
   (confirmed); the 4th (s=5) is the binary bias crushing a
   true-positive phantom, unfixable by any threshold verdict (proved).
   The task's "something else is wrong" branch, with the something-else
   precisely diagnosed and proved out of the verdict's reach.
2. **What is the right non-transductive verdict structure?** The
   train-scoped mean bar: the same statistic as the transductive bar,
   computed over train instead of the sealed batch. Each case is judged
   independently against a bar its own correction cannot move. No
   researcher-set constant; fully learner-computable.
3. **Does it generalize, or overfit to the phantom signal?** It does
   not overfit: the shuffled-signal control gains nothing from V_N
   (K8: 8 < 11). But it does not adapt to law change either: V_N
   degrades UCB @30/@45 relative to V_T (K7, A2 @30 = 7/12). The
   honest summary: the transductive bar adapts but punishes
   corrections; the non-transductive bar permits corrections but
   cannot adapt. @45 the D1b correction is strong enough that the
   fixed bar holds 12/12 anyway (K9).

## What this closes and what it opens

Closed: the preregistered hypothesis #1 from IVWC-CASEBIAS-RETRY.
Non-transductive verdicts are now measured: they un-block exactly the
corrections the mean bar punished (D1b: 8 -> 11 @15, 10 -> 11 @30,
12 -> 12 @45), at the cost of batch adaptation (UCB: 11 -> 10 @15,
9 -> 7 @30, 10 -> 9 @45). The (D1b x threshold-verdict) family is at
its theoretical ceiling.

Open, in evidence order: (1) the synthesis the results point at but
this wave did not test: a bar that is batch-responsive yet
correction-independent (e.g. scoped to preff, which the bias cannot
move) -- predicted to keep V_N's un-blocking while recovering V_T's
adaptation; (2) belief representations annotating uncertainty (retry
recommendation #2, untouched); (3) whether a learner-computable
phantom signal exists at all remains closed four ways -- this wave
used the fenced perfect signal only to isolate the verdict.

## Honest caveats

1. One wall-density law-change axis; item law, belief noise, and energy
   budget fixed (inherited).
2. The label ge = (eff >= Tpred) remains transductive (batch-relative);
   the verdict is non-transductive but it is scored against a
   transductive label. The @15 in-distribution alignment is what makes
   the test meaningful; @30/@45 the label/bar-scope mismatch is visible
   (s=2 @30, A2's degradation).
3. The 12-case test makes every bar a one-case margin (s=0's 13 vs 12
   decides K7).
4. D1b/D2b remain fenced harness diagnostics with a researcher-set +40
   probe magnitude; they test the verdict structure, not a learnable
   bias. No claim is made that the learner can compute phantom-ness.
5. Mechanism test, not a composition-novelty or L3 claim. The composer
   is fixed.

## Reproduction

```
cd docs/lab/research-lead/overnight-20260928/ivwc_nontransductive
~/workspace/tnn-rsi-gpi3/src/tools/toolchain/znc_linux_x86_64_abed8aa1 src/ivwc_nontransductive.zag -o bin/ivwc_nontransductive   # safebin PATH, pinned znc
./bin/ivwc_nontransductive | sha256sum   # expect 55fd7edfd6b7ef736e4c9b3c21908bbc6e323c96902de248898ab33cc6c6a8f4
```

Frozen audits (PREREG K1): A1 phase order
630<637<650<667<673<735<771<779<806<855; A2 0 (learner decision fns);
A3 0; A4 0; A5 `world_execute(` x3; A6 WC-FINAL=60; A7 0 learner/belief
calls after SCORING; A8 0 "oracle" tokens. K2: sha256 equality across
runs/ivwc_nontransductive-run{1,2,3}.txt.

## Branch note

Work committed on `tnn-native-lab` in the sibling worktree
~/workspace/tnn-rsi-gpi3 (this worker was spawned on a checkout parked
at lane-l2hetero-20261003 with tnn-native-lab checked out in the gpi3
worktree). All commits use explicit pathspecs confined to
`ivwc_nontransductive/`. Local only, never pushed. Git writes via
/usr/bin/git directly (safebin git symlink known-broken for writes).
Prereg commit strictly precedes the implementation commit. This is a
non-ledger task.
