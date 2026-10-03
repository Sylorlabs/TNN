# REPORT.md -- IVWC-HYBRID: internal prediction + consequence training

## Verdict: BUILD-FAIL (K5, K6, K7 fail; K1-K4, K8, K9 pass)

The hybrid was implemented exactly as preregistered and the
machinery works as designed -- the trained biases are informative
(0/4/15/16 per bucket), the consequence content drives the
verdicts (K8: shuffled 4/12 < 9/12), and the hybrid fixes one
pure-approach error on each regime (s=5@15, X3's false-FAIL;
s=3@45, OF's false-PASS). But it also breaks one correct verdict
on each regime at the bar boundary (s=10@15, adj=21 >= thyb=21;
s=5@45, adj=17 >= thyb=17), landing at 9/12 on both key regimes:
it matches X3 in-distribution (9=9, below OF's 10) and sits
between the two under law change (OF 8 < 9 < X3 10). The
"best of both" hypothesis fails in both weak form (K5/K6: the
hybrid does not match the per-regime winners) and strict form
(K7: no strict dominance anywhere). The hybrid is a compromise
that inherits weaknesses from both sides rather than strengths
from either: in-distribution the bucket-prior adjustment dilutes
the fine internal signal; under law change the stale trained
bias plus the internal deviation term adds optimistic noise the
coarser X3 rule avoids. Deterministic 3/3. No probe was run
pre-prereg; bar directions were theory-fixed.

## What was built

`src/ivwc_hybrid.zag` (pure Zag, single file, ~1000 lines, pinned
znc), `bin/ivwc_hybrid` (frozen binary). World/belief/composer/
stepper/verifier/seeds copied verbatim from IVWC-EXPAND3 and
IVWC-ORACLE-FREE. New machinery: a train phase (24 cases, wp=15)
with COMMIT (beliefs only), PREFF (`belief_execute` on train
plans, zero world cost), CONSEQ (the declared consequence-training
observations: 24 true train outcomes), and LEARN (expand3 bucket
table verbatim + per-bucket prediction-bias means bias_b =
mean(P_tr - E_tr), plus shuffled-eff variants for the ablation).
Sealed verdict: adjusted score C = P - bias_bkt, PASS iff
C >= T_hyb (mean C over sealed batch, learner-computed). Three
rules scored in-program against one shared label ge =
(eff >= T_pred): HYB, OF (P >= T_pred), X3 (frozen bucket table).

Build: `src/tools/toolchain/znc_linux_x86_64_abed8aa1
src/ivwc_hybrid.zag -o bin/ivwc_hybrid`. Analyzer: one
informational zagd-unavailable notice only, no warnings. One
post-prereg /tmp language check (i32 division on negative
operands; mechanism-independent) confirmed truncation-toward-zero
with no trap; it revealed nothing about outcomes.

## Kill-bar results

- K1 (commit before signal / diet): PASS. K1T/K1P STRUCT-PASS
  (wc unchanged across train COMMIT and train PREFF); K1S
  STRUCT-PASS at sh=0/1/2. A1: train COMMIT/PREFF call sites
  (622, 637) precede train CONSEQ world_execute (656); sealed
  COMMIT (779, 781) precedes SCORING world_execute (852). A2: 0.
  A3: 0. A4: 0. A6: `world_execute(` x3 (def + 2 call sites);
  WC-FINAL=60 (24 train + 36 sealed). A7: 0.
- K2 (determinism): PASS. 3/3 byte-identical, sha256
  f390310b6006631086366533c6ad3b3db415c2739fdb64cef0af332603734f0a.
- K3 (replication anchor, wp=15): PASS. In-program acc_of=10,
  acc_x3=9 -- exact match to the published dissociation numbers.
  The shared sealed setup and both pure rules are bit-identical
  to the expand3/oracle-free runs.
- K4 (replication anchor, wp=45): PASS. In-program acc_of=8,
  acc_x3=10 -- exact match under law change.
- K5 (best-of-both, wp=15): FAIL. acc_h=9 < acc_of=10 (=
  acc_x3=9). The hybrid does not match the in-distribution
  winner.
- K6 (best-of-both, wp=45): FAIL. acc_h=9 < acc_x3=10 (>
  acc_of=8). The hybrid does not match the law-change winner.
- K7 (strict dominance, both regimes): FAIL. No strict win on
  either regime.
- K8 (consequence-content ablation, wp=15): PASS. acc_hsh=4 <
  acc_h=9 (strict). Shuffling the consequence mapping collapses
  the hybrid: the trained-bias content (not the procedure alone)
  drives its verdicts. The internal-prediction component is
  identical under the shuffle, so the drop isolates the
  consequence-training contribution.
- K9 (non-degenerate, wp=15): PASS. 9/12 > maj 7/12.

## Mechanism detail (white box)

Trained quantities (train, wp=15): bucket table means 0/47/16/10
(cnt 7/7/7/3), T=20 -- bit-identical to expand3's table (second
independent replication). Learned biases: b0=0, b1=4, b2=15,
b3=16. The internal model is unbiased on empty plans, nearly
unbiased on single-gather plans, and systematically optimistic
(+15/+16) on dense multi-gather plans -- optimism grows with
plan density, consistent with phantom items and accumulating
belief error. Shuffled biases (-35/37/15/21) are unstructured,
as designed.

wp=15 (tpred=28, thyb=21; labels eff>=28):
HYB errors {s=0 FP, s=3 FP phantom, s=10 FP} -> 9/12.
OF errors {s=0, s=3} -> 10/12. X3 errors {s=3, s=5, s=10} -> 9/12.
The hybrid kept OF's fine win on s=5 (bkt=3, adj=28 >= 21 PASS;
X3's table said FAIL) but lost OF's fine win on s=10: the
bucket-1 bias (4) pulled adj to exactly 21, and 21 >= thyb=21
flipped it to PASS (OF: preff=25 < 28 FAIL, true eff=25).
s=0 (adj=25): the bucket-2 bias (15) damped the optimism
(40 -> 25) but not below the bar. s=3 (phantom, adj=46): still
FP -- the K8 limit from oracle-free is inherited, as predicted;
bucket-level consequence training cannot see case-level
phantoms either.

wp=45 (tpred=21, thyb=17; labels eff>=21):
HYB errors {s=0 FP, s=4 FP, s=5 FP} -> 9/12.
OF errors {s=0, s=3, s=4, s=5} -> 8/12. X3 errors {s=0, s=4} ->
10/12. The hybrid fixed OF's s=3 FP (bkt=2, adj=10 < 17 FAIL --
the trained bucket-2 optimism correction working as designed
under law change) but broke X3's s=5 TN: adj=17 >= thyb=17, an
exact bar-boundary flip to FP. s=0/s=4 (bkt=1, adj=46): the
bucket-1 bias (4) is far too small to dent confident optimism.

The symmetric trade is the finding: the hybrid repairs one
pure-approach error per regime and introduces one boundary
error per regime, net zero. Both misses are exact ties against
the learner-computed bar (adj == thyb) -- the mechanism sits
one notch away on each regime, but the bar is frozen and
learner-computed, so the result stands as measured. A follow-up
could test per-bucket bars or a bar margin; this wave does not.

Scoreboard (hybrid vs OF vs X3): wp=15: 9 vs 10 vs 9; wp=30:
8 vs 8 vs 9 (finding); wp=45: 9 vs 8 vs 10. The hybrid is never
strictly best and ties worst at wp=15. "Internal prediction as
prior, consequence training as likelihood" does not compose into
best-of-both here: the coarse trained prior washes out the fine
signal where it matters (s=10@15) and the stale bias under-
corrects where the world moved (s=5@45).

## Honest caveats

1. One wall-density law-change axis; item law, belief noise, and
   energy budget fixed. Other axes may break the mechanisms at
   different points.
2. T_pred/T_hyb are computed over the sealed batch
   (transductive), but from predictions + learned biases only --
   no world data enters any bar.
3. The 12-case test makes every bar a one-case margin: K5/K6
   fail by exactly one case each, both on bar-boundary ties.
   Reported as measured; the boundary pattern is a finding, not
   an adjustment.
4. The consequence-training diet (24 true train outcomes at
   wp=15) is declared in PREREG section 1, not hidden; sealed
   verdicts never observe sealed truth (K1).
5. Mechanism test, not a composition-novelty or L3 claim (per
   PREREG section 3). The composer is fixed; the claims concern
   the hybrid verdict loop and the dissociation regimes.

## Reproduction

```
cd docs/lab/research-lead/overnight-20260928/ivwc_hybrid
~/workspace/tnn-rsi-gpi3/src/tools/toolchain/znc_linux_x86_64_abed8aa1 src/ivwc_hybrid.zag -o bin/ivwc_hybrid
./bin/ivwc_hybrid | sha256sum   # expect f390310b6006631086366533c6ad3b3db415c2739fdb64cef0af332603734f0a
```

Frozen audits (PREREG section 4): A1 ordering 622/637 < 656 and
779/781 < 852; A2 count 0; A3 count 0; A4 count 0; A5 sha256
equality across runs/ivwc_hybrid-run{1,2,3}.txt; A6
`world_execute(` count 3, WC-FINAL=60; A7 count 0.

## Branch note

Work committed on `tnn-native-lab` (the shared checkout this
worker was spawned on). Prereg commit 9c32b1403 strictly precedes
the implementation commit. All commits use explicit pathspecs
confined to `ivwc_hybrid/`. Local only, never pushed. Git writes
via /usr/bin/git directly.
