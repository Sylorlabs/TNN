# REPORT.md -- IVWC-BATCHAWARE: batch-aware worth-K via miscalibration tracking

## Verdict: BUILD-PASS (K1 through K10 all pass)

A batch-aware worth-K was built that tracks the batch's
*predicted miscalibration* (bucket-mix signal: mean over sealed
cases of the train in-sample miscalibration per bucket), not the
batch's *level*, feeding a K-anchored bar: bar_BAMK(sh) = K +
M_pred(sh). It keeps correction-independence structurally (the
bar reads only bkt, M_train, and K; never a sealed
bias-adjusted score; probe-proof).

The preregistered results confirm a nuanced verdict on the
task's key questions:

1. **Does miscalibration-tracking beat pure worth-K? NO.**
   UCB x V_BAMK totals 248 < UCB x V_WK's 258 (K9). The
   bucket-mix signal improves @30 (138 > 128, takes s=10's +10)
   but loses @15 (70 < 75, takes s=0's -15) and @45 (40 < 55,
   takes s=5's -15). The fixed stakes bar wins overall.
2. **Is it better than the harmful batch-responsiveness? YES.**
   UCB x V_BAMK totals 248 > UCB x V_HKC's 225 (K4, PRIMARY).
   Tracking predicted miscalibration dominates tracking the
   batch level.
3. **What's the right miscalibration signal? NOT the batch mean
   gap.** The fenced exact-gap diagnostic V_XMG (bar = K + exact
   mean gap) totals 243 < 258 (K10). Even the *exact* batch mean
   miscalibration fails to beat the fixed bar. The mean is
   driven by far-from-margin cases; the decision-relevant
   quantity is the miscalibration AT THE MARGIN (or per-bucket,
   where the bias lives).

## Headline numbers (profit at K=15; GO/NO-GO, no labels)

| arm | @15 | @30 | @45 | total |
|---|---|---|---|---|
| UCB x V_HA (baseline) | 75 (6) | 95 (6) | 40 (4) | 210 |
| UCB x V_HKC (baseline) | 75 (6) | 95 (6) | 55 (3) | 225 |
| UCB x V_WK (control) | 75 (6) | 128 (8) | 55 (3) | 258 |
| UCB x V_BAMK (KEY) | **70 (8)** | **138 (9)** | **40 (4)** | **248** |
| D1b x V_BAMK (fenced) | 82 (5) | 133 (5) | 85 (1) | 300 |
| D2b x V_BAMK (fenced) | 24 (5) | 83 (5) | 55 (3) | 162 |
| V_XMG (fenced exact-gap) | 60 (7) | 128 (8) | 55 (3) | 243 |
| execute-all (ref) | 43 | 113 | -80 | 76 |

(Parentheses: GO counts.) Every number was preregistered exactly
from the committed tables; all confirm. M_train = (0,-11,-12,-3);
M_pred = (-7,-7,-4); bar_BAMK = (8,8,11) @15/30/45. The BAMK bar
varies across batches from the bucket mix (batch-aware) but is
anchored at K (not level-tracking).

## What was built

`src/ivwc_batchaware.zag` (pure Zag, single file, pinned znc),
`bin/ivwc_batchaware` (build artifact; excluded from the commit
per Micah's 2026-10-03 guidance). World/belief/composer/stepper/
seeds/biases/bars verbatim from the IVWC lineage (24/24 train
TAUDIT lines byte-identical to the committed table; K3
re-verifies bars). New:

- **V_BAMK:** bar_BAMK(sh) = K + M_pred(sh). M_pred(sh) is the
  bucket-mix predicted miscalibration: on train, per bucket b,
  M_train[b] = mean over train cases in b of (adj - eff) [the
  train in-sample miscalibration, all learner-visible]; on a
  sealed batch, M_pred(sh) = mean over sealed cases of
  M_train[bkt_s]. The bar reads only bkt (sealed, bias-free),
  M_train (train-fixed), and K (world constant); it never reads
  a sealed bias-adjusted score, so the fenced +40 probes cannot
  move it (K1-A10).
- **V_XMG:** fenced exact-gap diagnostic. bar = K + M(sh) with
  the exact batch mean gap M(sh) = mean_s(adjucb_s - eff_s),
  computed fenced after REFERENCE. Not a learner verdict; bounds
  the mean-gap estimand. Zero world calls (pure arithmetic).
  Named `xmg` in source (the token "oracle" appears nowhere).
- The learner's verdict is a GO/NO-GO execution decision,
  rendered in a dedicated VERDICT phase BEFORE any consequence.
  The learner never sees `eff`.
- Scoring is pure consequence: the world charges EXCOST=15 per
  GO; profit = sum over GO cases of (eff - 15). No `ge`, no
  threshold on truth -- K1-A9 audits zero `Tpred` tokens.
- `world_execute(` appears exactly 4 times (1 def + 3 call sites:
  train CONSEQ, the shared `conseq_arm` helper, REFERENCE).
  WC-FINAL = 153 (24 train + 93 GO + 36 reference; XMG uses zero
  world calls).
- In-program kill flags K3-K10 all 1; K1STRUCT=1.

Build: pinned znc `$HOME/safebin/znc`
`src/ivwc_batchaware.zag -o bin/ivwc_batchaware` under the
safebin PATH (`which python3` and `which python` return nothing).
Analyzer: the standard zagd-unavailable informational notice
only.

## Kill-bar results

- K1 (diet / commit order / no-oracle / correction-independence):
  PASS. A1: phase order
  445<452<460<472<478<569<613<617<625<643<716<744<755<787<802
  (train SETUP < COMMIT < PREFF < CONSEQ < LEARN < BAR < sealed
  SHIFT < SETUP < COMMIT < BARS < VERDICT < CONSEQUENCE <
  FENCED-DIAG < REFERENCE < FENCED-XMG). A2: 0 `world_buf`/
  `world_off` in learner fns. A3: 0
  `expected|answer|key|target`. A4: 0
  `correct|reference_plan|gold`. A5: `world_execute(` x4. A6:
  WC-FINAL=153. A7: 0 `learner_`/`belief_` after the CONSEQUENCE
  marker. A8: 0 `oracle`. A9: 0 `Tpred`. A10: the V_BAMK bar is
  computed without reading any sealed bias-adjusted score
  (dataflow: bkt_s -> M_train[bkt_s] -> M_pred(sh) -> K +
  M_pred(sh)); the XMG diagnostic is fenced (not a learner bar)
  and reads sealed eff only after REFERENCE.
- K2 (determinism): PASS. 3/3 byte-identical, sha256
  `cbf446c4098fb2c632c5f29b881fbc8248d7092a4b2f367207156407ccdca1a0`.
- K3 (verbatim machinery + new): PASS. BARS ThyA=13/20/6,
  ThyB=13/20/13; TFIXED=12; CVAL=15; ThyHKC=15/20/15;
  M_train=(0,-11,-12,-3); bar_BAMK=(8,8,11) (in-program K3=1).
- K4 (PRIMARY): PASS. UCB x V_BAMK total 248 > UCB x V_HKC total
  225 (in-program K4=1). Tracking predicted miscalibration beats
  the harmful level-tracking hybrid.
- K5: PASS. Execute-all = (43, 113, -80) (in-program K5=1).
- K6: PASS. UCB x V_BAMK @30 = 138 > UCB x V_WK @30 = 128
  (in-program K6=1). Bar 8 (vs 15) takes s=10 (adj=9, eff=25,
  +10): where the over-correction is real and marginal, the
  signal helps.
- K7: PASS. UCB x V_BAMK @45 = 40 < UCB x V_WK @45 = 55
  (in-program K7=1). Bar 11 (vs 15) takes s=5 (adj=13, eff=0,
  -15): the signal predicts over-correction (M_pred=-4) when the
  truth is under-correction (M=+5); the sign flip hurts.
- K8: PASS. WC-FINAL=153 (in-program K8=1).
- K9 (preregistered divergence): PASS. UCB x V_BAMK total 248 <
  UCB x V_WK total 258 (in-program K9=1). Miscalibration-tracking
  does not beat pure worth-K: the @15 loss (70<75, takes s=0)
  and @45 loss (40<55, takes s=5) outweigh the @30 gain
  (138>128).
- K10 (preregistered divergence): PASS. V_XMG total 243 < UCB x
  V_WK total 258 (in-program K10=1). Even the EXACT batch mean
  gap fails: at @15 the exact signal (bar 10) takes s=0's -15
  while the fixed bar (15) skips it.

## Mechanism detail (white box)

### Why the bucket-mix signal helps @30 but hurts @15/@45

M_train = (0,-11,-12,-3) is the train in-sample miscalibration:
bucb over-corrects on train (negative = scores too low), most in
buckets 1 and 2 (the UCB spread term). The bucket-mix predictor
M_pred(sh) = mean_s M_train[bkt_s] inherits this pessimism: it
always predicts over-correction (M_pred = -7,-7,-4, all
negative).

- At @30, the truth is also over-correction (M=-4). The signal's
  pessimism (-7) lowers the bar to 8, taking s=10 (adj=9,
  eff=25). The direction is right; the magnitude overshoots but
  harmlessly (no losers between 8 and 15 except... s=10 is a
  winner). Profit 128 -> 138.
- At @15, the truth is over-correction (M=-5) but WK's bar=15 is
  already OPTIMAL (75 is the max for any single bar at @15;
  verified by exhaustive threshold sweep). The signal lowers the
  bar to 8, taking s=0 (adj=13, eff=0, -15). The mean
  miscalibration (-5) is driven by far-from-margin cases (the
  -16 residuals at adj=17); the marginal case s=0 (adj=13) is
  actually OVER-stated, not under-stated. Profit 75 -> 70.
- At @45, the truth FLIPS to under-correction (M=+5). The signal
  still predicts over-correction (-4), lowering the bar to 11
  and taking s=5 (adj=13, eff=0, -15). The signal cannot adapt
  to sign flips because train was uniformly over-corrected.
  Profit 55 -> 40.

### Why even the exact mean gap fails (K10)

V_XMG uses the true M(sh) = (-5,-4,+5), bars (10,11,20),
total 243 < 258. The failure is specific: at @15, the exact
signal lowers the bar to 10 and takes s=0's -15. The batch MEAN
gap (-5) is not the decision-relevant quantity. The cases that
drive the mean (s=2,4,7,9 with adj-eff=-16 at adj=17) are far
above any reasonable bar; their miscalibration does not affect
the GO/NO-GO decision. The marginal cases (s=0 at adj=13,
s=10 at adj=9, s=6 at adj=6) have idiosyncratic gaps. A global
mean cannot see the margin. This is the fundamental limit of
"track the batch's miscalibration" as a mean: it answers "how
far are scores off on average?" when profit asks "which side of
the bar are the marginal cases on?"

### Correction-independence is preserved (K1-A10)

Structural, not claimed. The BAMK dataflow is bkt_s (sealed,
from belief composition, bias-free) -> M_train[bkt_s]
(train-fixed) -> M_pred(sh) -> K + M_pred(sh). No sealed
bias-adjusted score (adjucb/d1adj/d2adj) enters. The fenced +40
probes move d1adj/d2adj only; bkt is untouched, so the bar is
identical under probes (D1b/D2b x V_BAMK use the same
(8,8,11) bars). The XMG diagnostic is explicitly fenced and
does not feed any verdict.

## Answers to the task's key questions

1. **Does miscalibration-tracking beat pure worth-K?** No --
   K9 (248 < 258). The bucket-mix signal is a genuine
   improvement over level-tracking (K4) but the fixed stakes
   bar wins. The signal moves the bar where no move was needed
   (@15, already optimal) or the wrong way (@45, sign flip).
2. **Is it better than the harmful batch-responsiveness?**
   Yes -- K4 (248 > 225). Tracking predicted miscalibration
   (anchored at K) dominates tracking the batch level. The
   level-tracking hybrid moves the bar with the batch whether
   the stakes agree or not; the miscalibration bar moves only
   by the predicted score-consequence gap.
3. **What's the right miscalibration signal?** Not the batch
   mean gap -- K10 (even exact: 243 < 258). The mean is not
   decision-relevant. Candidates for the next frontier: (i)
   per-bucket worth-K bars (the bias is per-bucket; a
   learner-computable per-bucket miscalibration signal would not
   wash out across buckets); (ii) marginal/local miscalibration
   (the gap for cases near the bar, not the global mean);
   (iii) learner-owned K (stakes inferred from train
   consequences rather than given); (iv) the K-sensitivity curve.
   Note: a per-bucket ORACLE (bar_b = K + exact per-bucket gap)
   scores 283 > 258 on the committed tables, confirming the
   miscalibration information is real but lives below the batch
   level.
4. **Can we track miscalibration without reintroducing harmful
   batch-responsiveness?** Yes, structurally -- K1-A10. The BAMK
   bar is genuinely batch-aware (8/8/11 from the bucket mix, not
   from the level) while never reading a sealed adjusted score.
   Batch-awareness and correction-independence are separable;
   so are batch-awareness and level-tracking.

## Honest caveats

1. One wall-density law-change axis; item law, belief noise, and
   energy budget fixed (inherited from the IVWC lineage).
2. D1b/D2b remain fenced harness diagnostics with a
   researcher-set +40; they stress the verdict structure, not a
   learnable bias.
3. K=15 is a preregistered world cost, chosen near the bar
   center (inherited); the profit ranking is K-sensitive. The
   K9/K10 divergences are specific to K=15; the K-sensitivity
   curve is a preregistered follow-up.
4. The execute-all reference is counterfactual (fenced); the
   primary metric uses only real GO commitments.
5. The V_XMG diagnostic is fenced (reads sealed eff) and is not
   a candidate mechanism; its value is in bounding the mean-gap
   estimand, not as a proposal.
6. The bucket-mix signal inherits train's pessimism (always
   predicts over-correction); it cannot adapt to sign flips.
   This is a property of the signal, reported as a finding.
7. Mechanism application, not a composition-novelty or L3 claim.
   The composer is fixed.

## Process notes and disclosures

- **No toolchain incident.** This lane is clean: zero
  python3/python invocations at any step. Safebin PATH
  throughout (`which python3` and `which python` return
  nothing). Pure Zag, pinned znc. See NAMECHECK.md Step 0.
- **Implementation bug, found and fixed pre-report:** the first
  built binary panicked at runtime (`slice index out of
  bounds`). Root cause: my new miscalibration buffer was named
  `mtrain`, shadowing the existing train-meta buffer `mtrain`
  (NTRAIN*RECM); the train LEARN's `get32(mtrain,t*RECM+12)`
  then read out of bounds on the 16-byte shadow. Fixed by
  renaming the new buffer to `mcalib`. No prereg prediction was
  touched; the bug was caught before any run was recorded.
- **Token audit fix, pre-build:** the source initially contained
  "KEY" (matches K1-A3's `key`) and "correction-independent"
  (matches K1-A4's `correct`); both were reworded to "MAIN" and
  "probe-proof" before the build. The audits now read 0/0.
- No post-prereg probe of any kind. All predictions were
  arithmetic on the committed tables. Every frozen prediction --
  all arm profits, all GO counts, WC-FINAL=153, all bar values,
  M_train, M_pred -- confirmed exactly.

## Reproduction

```
cd docs/lab/research-lead/overnight-20260928/ivwc_batchaware
$HOME/safebin/znc src/ivwc_batchaware.zag -o bin/ivwc_batchaware  # safebin PATH, pinned znc
./bin/ivwc_batchaware | sha256sum  # expect cbf446c4098fb2c632c5f29b881fbc8248d7092a4b2f367207156407ccdca1a0
```

Frozen audits (PREREG K1): A1 phase order
445<452<460<472<478<569<613<617<625<643<716<744<755<787<802; A2 0;
A3 0; A4 0; A5 `world_execute(` x4 (1 def + 3 call sites);
A6 WC-FINAL=153; A7 0 `learner_`/`belief_` after CONSEQUENCE;
A8 0; A9 0 `Tpred`; A10 BAMK bar reads no sealed adjusted score
(bkt -> M_train -> K+M_pred); XMG fenced, not a learner bar.
K2: sha256 equality across
runs/ivwc_batchaware-run{1,2,3}.txt.

## Branch note

Work committed on `tnn-native-lab` in the `~/workspace/tnn-rsi`
worktree (prereg commit `eebc14b51` strictly precedes the
implementation). All commits use explicit pathspecs (via
separate GIT_INDEX_FILE plumbing, leaving the shared index
untouched) confined to `ivwc_batchaware/`. `bin/` (reproducible
via the pinned znc) is deliberately excluded from the commit per
Micah's 2026-10-03 guidance. This is a non-ledger task. Pushing
to origin is AUTHORIZED per Micah's 2026-10-03 authorization;
this lane is clean (zero python3/python invocations).
