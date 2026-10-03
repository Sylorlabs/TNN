# SPEC-FLIP-THRESHOLD: REPORT

**Lane:** docs/lab/research-lead/overnight-20260928/spec_flip_threshold/
**Date:** 2026-10-03
**Status:** Non-ledger (claim minting paused). Local commits only, never pushed.
**Verdict: BUILD-PASS (K1-K10 all pass)**

## Summary

This lane answered the well-posed redesign question from SPEC-FLIP-LATENCY:
should the flip threshold scale with L? 84 episodes (4 inherited regime
cells x 21 arms: fixed lazy, fixed eager, adapt L in {1,3,7,10},
guard L in {3,7,10}, fix2 / qmean / adaptd L in {1,3,7,10}), one binary,
pure Zag, safebin-built, 3/3 byte-identical (sha256
99d52d2b3aac843ad8ddc2225c742c95bf6cc977d9ee6570af8970defaf957a8).

The three new arms are the lane's experimental deltas on the parent's
policy layer, everything else inherited unchanged: pol 7 "fix2" replaces
the flip-path lazy bar (L+1)*qhi < dlo with the fixed 2*qhi < dlo;
pol 8 "qmean" keeps L-scaling but uses the point estimate,
(L+1)*qh < dlo; pol 9 "adaptd" uses M*qhi < dlo with M relaxing from
L+1 by 1 per fruitless post-shift checkpoint, floored at 2. The commit
rule (including the quirk), the eager-decisive direction, the EWMA, the
grid, and the arrival mechanics are the parent's, byte-identical on the
overlapping sweep (K5a: 20 adapt/guard lines byte-identical to the
parent's frozen run; K5d: fix2 L = 1 identical to adapt L = 1 modulo
the P= field on all four cells).

**Headline:** the threshold should NOT scale with L. The fixed bar
flips at tf1 = 144 for every L in {1,3,7,10} on the harm cell (K6e:
L-independent rescue timing), improves J at every L > 1 (62 < 74,
102 < 142, 132 < 134), and restores a positive rescue value at L = 10
(J = 132 < 133 = J_eager) where the L-scaled bar never flips at all.
J_fix2(7) = 102 exactly matches the frozen prediction and equals
fastewma's J = 102: the fixed threshold achieves by bar redesign what
doubling the estimator speed achieved by faster tracking. The point-
estimate variant (qmean) matches fix2 at L <= 7 but is trigger-happy:
it fired the only pre-shift flip in all 84 episodes (R = 21, L = 1,
stationary cell) and fails to beat eager at L = 10 (J = 137). The
adaptive-relaxation variant (adaptd) is the weakest redesign: it
improves on adapt at L = 7 (126 < 142) but at L = 10 it flips at
tf1 = 240 for J = 151, worse than never flipping (134). Patience
restores the flip, not the value. The quirk exoneration is preserved
(K8a: guard tick-identical to adapt), and the tf1 spread across the
four threshold arms at L = 7 (240/144/144/224) with identical quirk
fields confirms the latency is a flip-rule property (K8b).

## Answers to the four questions

1. **Does L-scaling improve J? No: un-scaling it improves J.**
   On R = 60, J_fix2 = 42/62/102/132 at L = 1/3/7/10 vs
   J_adapt = 42/74/142/134. The fixed bar is strictly better at every
   L > 1 (K7a: 102 < 142 at L = 7; the exact 102 was the frozen
   prediction, calibrated from the parent's adapt L = 1 line:
   rs = 22, od = 10, J = 22 + 10*(L+1)). Rescue value V(L) =
   J_eager - J_arm: fix2 gives 91/71/31/1 vs adapt's 91/59/-9/-1.
   The L multiplier buys nothing on this cell: it only delays the
   rescue (larger L needs deeper query-gap troughs) or kills it
   (L = 10 never-flip). qmean matches fix2 at L <= 7 (J = 42/62/102)
   but not at L = 10 (137 > 133); adaptd gives 42/74/126/151,
   beating adapt only at L = 7 and losing badly at L = 10.

2. **Does the redesign reduce tf1? Yes, for all three variants, in
   exactly the bar-ease order predicted.** On R = 60 (K6a-d, all
   theorems): tf1_fix2 <= tf1_adaptd <= tf1_adapt and
   tf1_qmean <= tf1_adapt at every L. Measured at L = 7:
   adapt 240, fix2 144, qmean 144, adaptd 224. fix2's rescue timing
   is L-independent (K6e: tf1/flips/fdir = 144/1/-1 at all four L,
   equal to adapt L = 1). adaptd's relaxation schedule is visible in
   its tf1 column (144/160/224/240): each step down the M ladder
   catches a later trough. No re-flips anywhere (tf2 = 0 on all 84
   lines): every rescue is a single clean flip, as in the parent.

3. **Is the quirk exoneration preserved? Yes.** K8a replicates the
   parent's K7 exactly: guard tf1/flips/fdir identical to adapt at
   L = 3/7/10 on R = 60, including the never-flip at L = 10. K8b: at
   L = 7 the four threshold arms show three distinct tf1 values
   (240/144/144/224) while their quirk fields are identical
   (tc = 32, cm = 2, Dc = 0 on all four): the tf1 spread is a
   flip-rule property by construction, since the commit path is
   untouched in every variant.

4. **Does the aggressive fixed bar flip where it should not? Almost
   never, and never harmfully here.** K9a (mechanism integrity) holds
   on all four cells. Findings: on R = 21 (stationary) and R = 82
   (query-dense shift), fix2 and adaptd never flip at any L; qmean
   fired one pre-shift flip (R = 21, L = 1, flips = 1 with pflips = 0,
   the only pre-shift flip in 84 episodes). Its J impact was benign
   (J = 9 vs adapt's 13, approaching the lazy-optimal 8), but it is a
   genuine false positive by design intent: the point-estimate bar
   fires on transients where the interval bar waits. On R = 120 (same
   regime as R = 60, D32 = 1), all three variants flip wherever adapt
   flips and earlier: fix2 L = 7/10 at tf1 = 160/160 (J = 78/93 vs
   adapt's 94/125), qmean at 160/176, adaptd at 176/176. No spurious
   post-shift flips on any control cell.

## Kill-bar adjudication

| Bar | Status | Detail |
|-----|--------|--------|
| K1 prereg order | PASS | prereg a65c4a189 -> implementation 0fa7c8e2a; no implementation file in prereg commit |
| K2 toolchain | PASS | safebin PATH, no python3/python, znc sha256 verified in-script |
| K3 determinism | PASS | build clean, exit 0, stderr empty, 3/3 byte-identical (99d52d2b...), 84 CELL lines |
| K4 anchoring | PASS | cross-arm (D,Q) identical (21 arms x 4 cells); fixed-arm identities; splits show the shift; structural accounting on all 76 adaptive lines; lc = 0 everywhere |
| K5a replication | PASS | 20 adapt/guard lines byte-identical to parent frozen run (delta is surgical) |
| K5b quirk in new arms | PASS | fix2/qmean/adaptd tc = 32, cm = 2, Dc = 0 on all D32 = 0 cells at L = 1/3/7/10 |
| K5c monotone latency | PASS | flips(Lb)>=1 => flips(La)>=1 and tf1(La)<=tf1(Lb) for every consecutive L pair in every adaptive arm, R = 60 |
| K5d L=1 identity | PASS | fix2 L = 1 line equals adapt L = 1 modulo P= on all 4 cells |
| K6a-d bar-ease | PASS | tf1_fix2 <= tf1_adaptd <= tf1_adapt, tf1_qmean <= tf1_adapt at L = 1/3/7/10, R = 60 |
| K6e L-independence | PASS | fix2 tf1/flips/fdir = 144/1/-1 at all L, equal to adapt L = 1 |
| K7a J at L=7 | PASS | J_fix2(7) = 102 < 142 = J_adapt(7) (exact frozen prediction) |
| K7b J at L=10 | PASS | J_fix2(10) = 132 < 133 = J_eager (positive rescue where L-scaled never flips) |
| K8a exoneration | PASS | guard/adapt tick-identical at L = 3/7/10 on R = 60 |
| K8b flip-rule property | PASS | 3 distinct tf1 values across threshold arms at L = 7 with identical quirk fields |
| K9a control integrity | PASS | bar-ease flips implication holds on all 4 cells |
| K10 hygiene | PASS | ASCII-only, no world literals, one fn main, reused sources unmodified, da_learn.zag untouched, parent lane unedited, local commits with explicit pathspecs, never pushed |

**K6 adjudication note (sentinel decoding, not a bar change).** The
frozen K6 bars compare first-flip ticks; the data encodes "never
flipped" as tf1 = 0 with flips = 0 (K4c). The check reads ticks in
extended reals (+infinity for never-flip): the tick inequality is
adjudicated only when the harder arm flipped, and the flips
implication is the operative clause otherwise. This is the unique
decoding under which the frozen bars are jointly satisfiable: K7b
*requires* fix2 to flip at L = 10 (J = 132 < 133 is impossible without
a flip, by the parent's K6b theorem giving J >= 134 for the never-flip
case), while adapt never flips there. Reading tf1 = 0 as tick zero
would make K6a demand that fix2 also never flip, contradicting K7b.
The easier-bar theorem ("fires whenever the harder bar fires") is
exactly the conditional form.

## Tested findings

1. **The L-scaling of the flip threshold is pure cost on the harm
   cell.** fix2 dominates adapt at every L > 1 in both tf1 and J, and
   the margin grows with L (V: 71 vs 59 at L = 3, 31 vs -9 at L = 7,
   1 vs -1 at L = 10). The (L+1) multiplier's only effect is to demand
   deeper query-gap troughs; nothing in the rescue benefits from it.
2. **The fixed bar matches the best estimator-speed lever.** J_fix2(7)
   = 102 = J_fastewma(7) from the parent lane: bar redesign and
   estimator speedup converge on the same rescue (tf1 = 144, rs = 22,
   od = 10). Two independent levers, one rescue value.
3. **Point estimates are trigger-happy.** qmean equals fix2 at L <= 7
   (tf1 = 144, J = 42/62/102) but fires a pre-shift flip on the
   stationary cell and cannot beat eager at L = 10 (J = 137 > 133).
   Dropping the interval removes the trough-gating *and* the
   conservatism that prevents transient firing. The interval upper
   bound is load-bearing for flip discipline even though it gates the
   rescue.
4. **Adaptive patience restores the flip but not the value.**
   adaptd L = 10 flips at tf1 = 240 (the relaxed bar eventually
   fires) for J = 151, worse than adapt's never-flip 134 (V = -18).
   At L = 7 it helps modestly (126 < 142, V = 7). Relaxing the bar
   with patience cannot fix a rescue that arrives after the eager
   stint has already cost more than the flip saves.
5. **No re-flips under any threshold.** tf2 = 0 on all 84 lines: the
   redesigned bars produce single clean rescues, never oscillation.
6. **Control-cell behavior is clean except the one qmean transient.**
   fix2/adaptd: zero flips on R = 21/82 at all L. R = 120 confirms
   the harm-cell pattern under D32 = 1: every variant flips no later
   than adapt and improves J (fix2: 78/93 vs 94/125 at L = 7/10).

## Honest scope limits

- One seed per cell (inherited); the trough realizations determine the
  exact tf1 values, though the bar-ease orderings are theorems, not
  realizations.
- One shift per episode at tick 128 (inherited); multiple shifts and
  gradual drift remain untested.
- The variants were compared at L in {1,3,7,10} only; the parent's
  L = 15/20/30 tail was not re-swept (the never-flip boundary at
  L = 10 already discriminates).
- L is caller-stated, not measured (inherited); none of the variants
  estimate the true cost ratio.
- The stale-data facet of the degenerate interval remains untested
  (inherited non-goal).
- Whether the fixed bar's aggressiveness hurts on cells where eager
  is truly optimal was probed only by R = 21/82/120; a broader
  adversarial sweep is future work.

## Recommendations

1. **Adopt the fixed threshold as the working flip bar.**
   (L+1)*qhi < dlo should become 2*qhi < dlo: on the tested cells the
   L-scaling is pure cost with no benefit, and the fixed bar is no
   worse on any control cell. If a future lane finds a cell where
   L-scaling helps, that cell's mechanism should be understood before
   re-complicating the bar.
2. **Keep the interval, not the point estimate.** qmean's pre-shift
   false positive shows the qhi upper bound does real work as flip
   discipline. Future qhi-estimation work should preserve
   conservatism under query bursts (e.g. asymmetric intervals), not
   drop it.
3. **Do not pursue patience-relaxation.** adaptd's L = 10 outcome
   (flip restored, value destroyed) shows the failure mode: a late
   rescue is worse than none. Latency reduction must come from the
   bar level (fix2) or the estimator (fastewma), not from waiting
   longer for a weaker bar.
4. **The next question is whether L should enter at all.** The fixed
   bar still takes L as an argument (for J accounting and the
   unchanged eager direction). A follow-up could test whether the
   eager-decisive direction or the cost model needs the caller-stated
   L, or whether the whole discipline can run L-free.

## Process notes

- Pure Zag throughout; safebin mandatory (`which python3` /
  `which python` empty, recorded in NAMECHECK.md Step 0);
  pinned znc znc_linux_x86_64_abed8aa1 (sha256-verified
  in-script: 498abcb5...); no Python invoked at any point.
  Output analysis via grep/cmp/awk/sed/shell only. ft_posthoc.sh
  is labeled post-hoc analysis, not a bar re-adjudication: it prints
  finding tables on the frozen data and must not move any frozen bar.
  (Posthoc display note: its fixed-lazy J row prints from the L = -1
  lazy line; the bars never use that path.)
- No new seed probe: cells inherited from SPEC-FLIP-LATENCY's frozen
  data; D32 = 0 re-confirmed by K5b (tc = 32, Dc = 0 in all three new
  arms on R = 21/60/82).
- One check-script correction during implementation (before the
  implementation commit): the K6 bar-ease check initially compared
  tf1 sentinels literally (144 <= 0), failing at L = 10 where K7b
  requires fix2 to flip while adapt never does. Corrected to the
  extended-reals reading documented above, which is the unique
  decoding under which the frozen K6 and K7b bars are jointly
  satisfiable. The frozen bar text was not changed; the decoding is
  recorded here for audit.
- Git: `/usr/bin/git` directly (safebin git symlink breaks writes per
  AGENTS.md); explicit pathspecs; commits local, never pushed. Commit
  order on the lane dir: a65c4a189 (PREREG + NAMECHECK) ->
  0fa7c8e2a (implementation). No amendments; no post-implementation
  bar changes.
- `da_learn.zag` not modified (separate lane only, per task).
- ft_spec.zag is a minimal documented delta on the parent's
  fl_spec.zag ([FT-DELTA] markers: nr_decide_ft with hoisted
  lzq/lzmult flags for pol 7/8/9, pol-9 nchk counter at CS+120;
  [FT-RENAME] fl_ -> ft_; nr_decide, the commit rule, the
  eager-decisive direction, the EWMA, the grid, and pol-3 code are
  the parent's, unchanged; pol 3 dormant, not swept). The parent's
  fl_spec.zag / fl_main.zag are byte-unmodified in their own lane
  (K10). For pol in {0,1,2,4} the tick dynamics are unchanged,
  verified by K5a byte-identity.
- Repro: `./ft_build.sh` assembles the binary, builds with the
  pinned znc, runs 3x (byte-identity + kill-bar adjudication);
  `./ft_posthoc.sh` prints the finding tables on the frozen data.
  All sources and logs are in this lane directory.
