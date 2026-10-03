# REPORT.md -- IVWC-PERBUCKET: per-bucket worth-K bars

## Verdict: BUILD-PASS (K1 through K10 all pass)

Two learner-computable per-bucket worth-K bars were built and
tested against the fixed-K control and a fenced per-bucket
exact bound. The preregistered verdict is a clean NULL on the
task's key questions:

1. **Do per-bucket bars beat fixed-K? NO (K4/K9).** UCB x V_PBK
   totals 248 and UCB x V_PBOPT totals 243, both < UCB x V_WK's
   258. Going below batch level does not fix the fundamental
   problem: the bars move on train's bucket miscalibration, and
   the shift moves the sealed bucket miscalibration differently.
2. **Do they approach the per-bucket exact bound? NO (K10).**
   The learner's best per-bucket total (248) trails the exact
   bound V_PBX (283) by 35. The bound is matched exactly at @30
   (138 = 138) but missed at @15 (70 vs 90) and @45 (40 vs 55)
   -- both misses come from train->sealed per-bucket gap
   sign/magnitude shifts.
3. **Is the below-batch information usable? NO as a verdict
   input.** Every learner-computable per-bucket bar tested
   fails to beat fixed-K, while the exact per-bucket signal
   gains 25 over it (283 > 258). The information is real but
   not extractable from {train, bucket identity, K} on these
   shifts. Both bars keep probe-proofness structurally
   (K1-A10): neither reads a sealed bias-adjusted score.

## Headline numbers (profit at K=15; GO/NO-GO, no labels)

| arm | @15 | @30 | @45 | total |
|---|---|---|---|---|
| UCB x V_WK (control) | 75 (6) | 128 (8) | 55 (3) | 258 |
| UCB x V_PBK (KEY-1) | 70 (8) | 138 (9) | 40 (4) | 248 |
| UCB x V_PBOPT (KEY-2) | 60 (7) | 128 (8) | 55 (3) | 243 |
| V_PBX (fenced exact) | 90 (8) | 138 (9) | 55 (3) | 283 |
| execute-all (ref) | 43 | 113 | -80 | 76 |

(Parentheses: GO counts.) Every number was preregistered exactly
from the committed tables; all confirm. Per-bucket bars: V_PBK
= K + mcalib = (15,4,3,12); V_PBOPT (train-profit-optimal, ties
toward K) = (15,16,5,15). V_PBX exact bars: @15 (15,8,28,4),
@30 (15,8,13,14), @45 (15,32,13,28).

## What was built

`src/ivwc_perbucket.zag` (pure Zag, single file, pinned znc),
`bin/ivwc_perbucket` (build artifact; excluded from the commit
per Micah's 2026-10-03 guidance). World/belief/composer/stepper/
seeds/biases/bars verbatim from the IVWC lineage (24/24 train
TAUDIT lines byte-identical to the committed table; K3
re-verifies bars). New:

- **V_PBK:** bar_b = K + mcalib[b] per bucket. The
  miscalibration-adjusted score is adj - mcalib[b]; GO iff
  adj_s > K + mcalib[bkt_s]. The direct below-batch-level
  analog of V_BAMK: instead of averaging bucket
  miscalibrations into one batch bar, each bucket keeps its
  own. Reads only bkt_s (sealed, bias-free), mcalib
  (train-fixed), K. Never reads a sealed bias-adjusted score;
  probe-proof by structure (K1-A10).
- **V_PBOPT:** per-bucket train-profit-optimal bars. bar*_b
  maximizes sum over train cases in bucket b with adj > bar of
  (eff - K) on train consequences (learner-visible); ties
  broken toward K (then the larger bar). Integer candidate
  search over [min_adj-1, max(max_adj, K)]; the K-closest
  optimal bar provably lies in this range (prereg derivation).
  No researcher constants, no sealed data; probe-proof by
  structure (K1-A10). Computed bars: (15,16,5,15).
- **V_PBX:** fenced per-bucket exact diagnostic. bar_b(sh) = K
  + G(sh,b) with the exact sealed per-bucket gap G(sh,b) =
  mean over sealed cases in bucket b of (adjucb - eff),
  computed fenced after REFERENCE. Bounds the per-bucket
  estimand. Zero world calls (pure arithmetic). Named `pbx` in
  source (the token "oracle" appears nowhere).
- The V_HA/V_HKC verdict arms and the D1b/D2b +40 probe arms
  were not re-run this wave (their bars are still computed and
  printed for the K3 verbatim-machinery check; probe-proofness
  for the per-bucket bars holds by the same bkt-driven
  structure and is audited as K1-A10).
- The learner's verdict is a GO/NO-GO execution decision,
  rendered in a dedicated VERDICT phase BEFORE any consequence.
  The learner never sees `eff`.
- Scoring is pure consequence: the world charges EXCOST=15 per
  GO; profit = sum over GO cases of (eff - 15). No `ge`, no
  threshold on truth -- K1-A9 audits zero `Tpred` tokens.
- `world_execute(` appears exactly 4 times (1 def + 3 call sites:
  train CONSEQ, the shared `conseq_arm` helper, REFERENCE).
  WC-FINAL = 116 (24 train + 56 GO + 36 reference; PBX uses zero
  world calls).
- In-program kill flags K3-K10 all 1; K1STRUCT=1.

Build: pinned znc `$HOME/safebin/znc`
`src/ivwc_perbucket.zag -o bin/ivwc_perbucket` under the
safebin PATH (`which python3` and `which python` return nothing).
Analyzer: the standard zagd-unavailable informational notice
only.

## Kill-bar results

- K1 (diet / commit order / no-exact-signal / probe-proofness):
  PASS. A1: phase order
  447<454<462<474<480<639<707<711<719<737<780<805<814<829
  (train SETUP < COMMIT < PREFF < CONSEQ < LEARN < BAR < sealed
  SHIFT < SETUP < COMMIT < BARS < VERDICT < CONSEQUENCE <
  REFERENCE < FENCED-PBX). A2: 0 `world_buf`/`world_off` in
  learner fns. A3: 0 `expected|answer|key|target`. A4: 0
  `correct|reference_plan|gold`. A5: `world_execute(` x4. A6:
  WC-FINAL=116. A7: 0 `learner_`/`belief_` after the
  CONSEQUENCE marker. A8: 0 `oracle`. A9: 0 `Tpred`. A10: the
  V_PBK bar is computed without reading any sealed
  bias-adjusted score (dataflow: bkt_s -> mcalib[bkt_s] -> K +
  mcalib[bkt_s]); the V_PBOPT bars are computed from train
  (adj, eff) only and likewise selected by bkt_s; the lineage
  probes touch adjusted scores only, never bkt, so they cannot
  move either per-bucket bar. The PBX diagnostic is fenced (not
  a learner bar) and reads sealed eff only after REFERENCE.
- K2 (determinism): PASS. 3/3 byte-identical, sha256
  `96db827a77e6e591597f8859fdb5a743dff41ff899bd4445f381d8b186c3822f`.
- K3 (verbatim machinery + new): PASS. BARS ThyA=13/20/6,
  ThyB=13/20/13; TFIXED=12; CVAL=15; ThyHKC=15/20/15;
  mcalib=(0,-11,-12,-3); V_PBK bars=(15,4,3,12); V_PBOPT
  bars=(15,16,5,15); UCB x V_WK=(75,128,55)=258;
  V_PBX=(90,138,55)=283; execute-all=(43,113,-80)
  (in-program K3=1, via shallow sub-flags).
- K4 (PRIMARY, preregistered NULL): PASS. UCB x V_PBK total 248
  < 258 AND UCB x V_PBOPT total 243 < 258 (in-program K4=1).
  No learner-computable per-bucket bar beats the fixed stakes
  bar.
- K5: PASS. Execute-all = (43, 113, -80) (in-program K5=1).
- K6: PASS. UCB x V_PBK total = 248 (in-program K6=1),
  coinciding with the V_BAMK lineage total.
- K7: PASS. UCB x V_PBOPT total = 243 < 248 = V_PBK total
  (in-program K7=1). Train-profit-optimal per-bucket bars
  overfit train.
- K8: PASS. WC-FINAL=116 (in-program K8=1).
- K9 (divergence): PASS. UCB x V_PBK total 248 < UCB x V_WK
  total 258 (in-program K9=1).
- K10 (divergence): PASS. V_PBX total 283 > UCB x V_PBK total
  248 (in-program K10=1).

## Mechanism detail (white box)

### Why V_PBK coincides exactly with V_BAMK (K6)

V_PBK's bars (15,4,3,12) differ from V_BAMK's batch bars
(8,8,11), yet the GO sets coincide on all three batches. The
reason is distributional, not structural: the differential
bands contain no sealed cases. At @15: no b0 case with adj in
(8,15] (s1, s8 have adj 0), no b1 case with adj in (4,8]
(all are 9+), no b2 case with adj in (3,8] (s0 has adj 13),
no b3 case with adj in (8,12] (s5 has 24; s6, s11 have <=6).
Same emptiness at @30 and @45. So per-bucket gap-adjustment
and batch-mix gap-adjustment make identical commitments here
-- the bucket refinement buys nothing on these batches, and
both inherit the same failures (s0's -15 at @15 via the b2
bar 3; s5's -15 at @45 via the b3 bar 12).

### Why V_PBOPT does worse than V_PBK (K7)

The train-optimal bars overfit train noise. The b1 bar 16 is
optimal on train because it exploits the single train case
(17,0): taking it loses 15 on train, so the optimum sits just
below 17. On sealed batches, two cases sit at adj=9 in b1
(s10 at @15 and @30, eff=25, +10 each): the gap-adjusted bar
4 takes both (+20 total); the train-optimal bar 16 misses
both. The b3 bar 15 does avoid s5's -15 at @45 (hence PBOPT
@45 = 55 > PBK @45 = 40), but -20 + 15 = -5 net vs PBK.
Parametric gap-adjustment generalizes better than empirical
threshold-picking with 3-7 cases per bucket -- but neither
beats fixed-K.

### Why the exact per-bucket signal wins and the learner cannot follow (K10)

The exact sealed per-bucket gaps vs the train gaps the learner
must use:

| bucket | train gap | @15 exact | @30 exact | @45 exact |
|---|---|---|---|---|
| b0 | 0 | 0 | 0 | 0 |
| b1 | -11 | -7 | -7 | +17 |
| b2 | -12 | +13 | -2 | -2 |
| b3 | -3 | -11 | -1 | +13 |

The shift moves bucket-level miscalibration in ways bucket
identity cannot predict: b2 flips sign at @15 (-12 -> +13),
b1 flips sign at @45 (-11 -> +17), b3 flips sign at @45
(-3 -> +13) and triples in magnitude at @15 (-3 -> -11).
The exact bound's 35-point edge over the learner decomposes
exactly: @15, the exact b2 bar 28 avoids s0's -15 and the
exact b3 bar 4 takes s6's +5 (20); @30, 0 -- the learner
already matches the bound (138 = 138), because train's
bucket gaps happen to be decision-equivalent there; @45, the
exact b3 bar 28 avoids s5's -15 (15).

The @30 match is the informative detail: per-bucket
information is not uniformly unusable -- when the shift
preserves the bucket gaps' decision-relevant structure, the
train-derived bars are optimal. The failure is in
transferability, not in the per-bucket form. Bucket identity
is a proxy for the bias mechanism (UCB spread by gather
count), and the wall-density shift changes how that mechanism
miscalibrates per bucket. Nothing in {train, bkt, K} observes
the shift's per-bucket effect before commitment.

### Probe-proofness is preserved (K1-A10)

Structural, not claimed. The PBK dataflow is bkt_s (sealed,
from belief composition, bias-free) -> mcalib[bkt_s]
(train-fixed) -> K + mcalib[bkt_s]. The PBOPT dataflow is
train (adj, eff) -> bar*_b, selected by bkt_s. No sealed
bias-adjusted score (adjucb/d1adj/d2adj) enters either bar
computation. The lineage's fenced +40 probes move adjusted
scores only; bkt is untouched, so both per-bucket bars are
identical under probes. The PBX diagnostic is explicitly
fenced and does not feed any verdict.

## Answers to the task's key questions

1. **Do per-bucket bars beat fixed-K?** No -- K4/K9
   (248 and 243 < 258). Two learner-computable designs, the
   parametric gap-adjustment and the nonparametric
   train-optimal bars, both lose to the fixed stakes bar.
   Below-batch resolution does not repair the core defect:
   the bars still move on train's miscalibration while the
   shift moves sealed miscalibration elsewhere.
2. **Do they approach the per-bucket exact bound (283)?** No
   -- K10 (248 vs 283, a 35 gap). The bound is matched at @30
   but missed at @15 and @45, entirely through
   train->sealed per-bucket gap shifts.
3. **Is the information actually usable (not just exact)?**
   No, as a verdict input on these shifts: every
   learner-computable per-bucket bar tested fails to beat
   fixed-K, while the exact per-bucket signal gains 25 over
   it. The below-batch-level information is real but not
   extractable from {train, bucket identity, K}. Named next
   steps: marginal (decision-boundary-local) per-bucket
   miscalibration, learner-owned K, the K-sensitivity curve.

## Honest caveats

1. One wall-density law-change axis; item law, belief noise, and
   energy budget fixed (inherited from the IVWC lineage).
2. K=15 is a preregistered world cost, chosen near the bar
   center (inherited); the profit ranking is K-sensitive. The
   K4/K9/K10 divergences are specific to K=15; the
   K-sensitivity curve is a preregistered follow-up.
3. The execute-all reference is counterfactual (fenced); the
   primary metric uses only real GO commitments.
4. The V_PBX diagnostic is fenced (reads sealed eff) and is not
   a candidate mechanism; its value is in bounding the
   per-bucket estimand, not as a proposal.
5. Both learner bars inherit train's bucket gaps; neither can
   adapt to sign flips under shift. This is a property of the
   signals, reported as a finding.
6. The D1b/D2b probe arms were not re-run; probe-proofness for
   the per-bucket bars is established structurally (K1-A10),
   not behaviorally, this wave.
7. Mechanism application, not a composition-novelty or L3 claim.
   The composer is fixed.

## Process notes and disclosures

- **No toolchain incident.** This lane is clean: zero
  python3/python invocations at any step. Safebin PATH
  throughout (`which python3` and `which python` return
  nothing). Pure Zag, pinned znc. See NAMECHECK.md Step 0.
- **Token audit fix, pre-build:** the source initially contained
  "miscalibration-corrected" (matches K1-A4's `correct`); it
  was reworded to "miscalibration-adjusted" before the build.
  The audits now read 0/0.
- **Unused lineage buffer:** `gout2` is still allocated but no
  longer read (the nphantom block was dropped with the probe
  arms); `gather_cells` remains as a verbatim learner fn for
  the A2 audit. No behavioral effect.
- No post-prereg probe of any kind. All predictions were
  arithmetic on the committed tables. Every frozen prediction --
  all arm profits, all GO counts, WC-FINAL=116, all bar values,
  mcalib, PBX gaps/bars -- confirmed exactly.

## Reproduction

```
cd docs/lab/research-lead/overnight-20260928/ivwc_perbucket
$HOME/safebin/znc src/ivwc_perbucket.zag -o bin/ivwc_perbucket  # safebin PATH, pinned znc
./bin/ivwc_perbucket | sha256sum  # expect 96db827a77e6e591597f8859fdb5a743dff41ff899bd4445f381d8b186c3822f
```

Frozen audits (PREREG K1): A1 phase order
447<454<462<474<480<639<707<711<719<737<780<805<814<829; A2 0;
A3 0; A4 0; A5 `world_execute(` x4 (1 def + 3 call sites);
A6 WC-FINAL=116; A7 0 `learner_`/`belief_` after CONSEQUENCE;
A8 0; A9 0 `Tpred`; A10 PBK/PBOPT bars read no sealed adjusted
score (bkt -> train-fixed quantities -> bar); PBX fenced, not a
learner bar. K2: sha256 equality across
runs/ivwc_perbucket-run{1,2,3}.txt. Train TAUDIT 24/24
byte-identical to the committed lineage table.

## Branch note

Work committed on `tnn-native-lab` in the `~/workspace/tnn-rsi`
worktree (prereg commit `c31059ce5` strictly precedes the
implementation). All commits use explicit pathspecs (via
separate GIT_INDEX_FILE plumbing, leaving the shared index
untouched) confined to `ivwc_perbucket/`. `bin/` (reproducible
via the pinned znc) is deliberately excluded from the commit per
Micah's 2026-10-03 guidance. This is a non-ledger task. Pushing
to origin is AUTHORIZED per Micah's 2026-10-03 authorization;
this lane is clean (zero python3/python invocations).
