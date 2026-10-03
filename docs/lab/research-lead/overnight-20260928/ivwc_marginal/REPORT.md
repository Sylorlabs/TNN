# REPORT.md -- IVWC-MARGINAL: decision-boundary-local per-bucket miscalibration

## Verdict: BUILD-PASS (K1 through K10 all pass)

Two learner-computable marginal miscalibration bars were built
and tested against the fixed-K control, the bucket-mean approach
(V_PBK), and fenced marginal exact bounds. The preregistered
verdict is a clean NULL on the task's key questions:

1. **Is marginal miscalibration more predictive than
   bucket-mean? NO (K4/K6/K7).** UCB x V_PMW totals 228 and
   UCB x V_PMN totals 248, vs UCB x V_PBK's 248. The
   fixed-window version is strictly worse; the N-nearest
   version makes identical GO commitments to the bucket mean
   (not better).
2. **Does it beat fixed-K? NO (K4/K9).** 228 and 248 < 258.
   Locality does not repair the transfer defect.
3. **Can we capture the decision-relevant information? NO as a
   verdict input (K10).** The exact marginal bounds (V_PMWX
   288, V_PMNX 318) beat the learner marginal bars (228, 248)
   by 60/70. The marginal information is real -- PMNX gains 30
   over the per-bucket exact bound at @45 -- but the
   train->sealed marginal gap shifts are not predictable from
   {train, bucket identity, K}.
4. **What is the right definition of "marginal"?** Of the two
   tested, the data-driven half-nearest rule (V_PMN) generalizes
   no worse than the bucket mean (identical commitments), while
   the fixed window W=10 (V_PMW) generalizes worse: with only 2
   marginal train cases in b1, the local estimate is dominated
   by the single (17,0) train case that also made PBOPT
   overfit. Neither beats fixed-K.

## Headline numbers (profit at K=15; GO/NO-GO, no labels)

| arm | @15 | @30 | @45 | total |
|---|---|---|---|---|
| UCB x V_WK (control) | 75 (6) | 128 (8) | 55 (3) | 258 |
| UCB x V_PBK (bucket-mean) | 70 (8) | 138 (9) | 40 (4) | 248 |
| UCB x V_PMW (KEY-1) | 60 (7) | 128 (8) | 40 (4) | 228 |
| UCB x V_PMN (KEY-2) | 70 (8) | 138 (9) | 40 (4) | 248 |
| V_PMWX (fenced marginal exact) | 90 (8) | 143 (10) | 55 (3) | 288 |
| V_PMNX (fenced marginal exact) | 90 (8) | 143 (10) | 85 (1) | 318 |
| V_PBX (fenced per-bucket exact) | 90 (8) | 138 (9) | 55 (3) | 283 |
| execute-all (ref) | 43 | 113 | -80 | 76 |

(Parentheses: GO counts.) Every number was preregistered exactly
from the committed tables; all confirm. Marginal bars: V_PMW =
K + mwmcalib = (15,15,3,12) with mwmcalib = (0,0,-12,-3);
V_PMN = K + mncalib = (15,8,3,10) with mncalib =
(0,-7,-12,-5). Exact marginal gaps: PMWX @15 (0,-16,13,-11),
@30 (0,-16,-2,-12), @45 (0,17,-2,13); PMNX @15 (0,-16,13,-11),
@30 (0,-16,-2,-12), @45 (0,34,-2,13).

## What was built

`src/ivwc_marginal.zag` (pure Zag, single file, pinned znc),
`bin/ivwc_marginal` (build artifact; excluded from the commit
per Micah's 2026-10-03 guidance). World/belief/composer/stepper/
seeds/biases/bars verbatim from the IVWC lineage (24/24 train
TAUDIT lines byte-identical to the committed table; K3
re-verifies bars). New:

- **V_PMW:** bar_b = K + mwmcalib[b] per bucket. The marginal
  train set per bucket is {t : |adj_t - K| <= 10} (MWIN = 10
  frozen); the local miscalibration is the trunc mean of
  (adj - eff) over that set, falling back to the full-bucket
  train mcalib when the set is empty (b0). GO iff adjucb_s >
  K + mwmcalib[bkt_s]. Reads only bkt_s (sealed, bias-free),
  train-fixed local quantities, K, and the frozen structural
  window rule. Never reads a sealed bias-adjusted score;
  probe-proof by structure (K1-A10).
- **V_PMN:** bar_b = K + mncalib[b] per bucket. The marginal
  train set per bucket is the N_b = ceil(n_b/2) cases with
  smallest |adj_t - K|, ties by lowest train index (N_b is
  data-driven; no magnitude constant). The local
  miscalibration is the trunc mean of (adj - eff) over those
  N_b cases. No researcher constants, no sealed data;
  probe-proof by structure (K1-A10). Computed bars:
  (15,8,3,10).
- **V_PMWX / V_PMNX:** fenced marginal exact diagnostics.
  bar_b(sh) = K + exact sealed marginal gap under the same two
  marginality rules, computed fenced AFTER the REFERENCE
  phase. They bound the marginal estimand: the best any
  decision-boundary-local signal could do. Zero world calls
  (pure arithmetic). Named `pmmwx` / `pmmnx` in source (the
  token "oracle" appears nowhere).
- Comparators re-run verbatim in the same binary: UCB x V_WK
  (bar = K, the fixed-K control) and UCB x V_PBK (bars
  (15,4,3,12), the bucket-mean approach). Fenced: V_PBX
  per-bucket exact diagnostic (recomputed verbatim, 283) and
  execute-all.
- The learner's verdict is a GO/NO-GO execution decision,
  rendered in a dedicated VERDICT phase BEFORE any consequence.
  The learner never sees `eff`.
- Scoring is pure consequence: the world charges EXCOST=15 per
  GO; profit = sum over GO cases of (eff - 15). No `ge`, no
  threshold on truth -- K1-A9 audits zero `Tpred` tokens.
- `world_execute(` appears exactly 4 times (1 def + 3 call sites:
  train CONSEQ, the shared `conseq_arm` helper, REFERENCE).
  WC-FINAL = 138 (24 train + 78 GO + 36 reference; PMWX/PMNX/PBX
  use zero world calls).
- In-program kill flags K3-K10 all 1; K1STRUCT=1.

Build: pinned znc `$HOME/safebin/znc`
`src/ivwc_marginal.zag -o bin/ivwc_marginal` under the
safebin PATH (`which python3` and `which python` return nothing).
Analyzer: the standard zagd-unavailable informational notice
only.

## Kill-bar results

- K1 (diet / commit order / no-exact-signal / probe-proofness):
  PASS. A1: phase order
  480<487<495<507<513<763<867<875<893<936<966<977<992<1067<1145
  (train SETUP < COMMIT < PREFF < CONSEQ < LEARN < BAR < sealed
  SETUP < COMMIT < BARS < VERDICT < CONSEQUENCE < REFERENCE <
  FENCED-PBX < FENCED-PMWX < FENCED-PMNX). A2: 0
  `world_buf`/`world_off` in learner fns. A3: 0
  `expected|answer|key|target`. A4: 0
  `correct|reference_plan|gold`. A5: `world_execute(` x4. A6:
  WC-FINAL=138. A7: 0 `learner_`/`belief_` after the
  CONSEQUENCE marker. A8: 0 `oracle`. A9: 0 `Tpred`. A10: the
  V_PMW bar is computed without reading any sealed
  bias-adjusted score (dataflow: bkt_s -> train-fixed local
  mwmcalib[bkt_s] under the frozen W=10 rule -> K +
  mwmcalib[bkt_s]); the V_PMN bar likewise (bkt_s ->
  train-fixed mncalib under the frozen N_b = ceil(n_b/2) rule
  -> K + mncalib[bkt_s]); the lineage probes touch adjusted
  scores only, never bkt, so they cannot move either marginal
  bar. The PMWX/PMNX diagnostics are fenced (not learner bars)
  and read sealed eff only after REFERENCE.
- K2 (determinism): PASS. 3/3 byte-identical, sha256
  `5aad447e116406088993c1ae6449fa359e3608a4814c194078d20243d730a60f`.
- K3 (verbatim machinery + new): PASS. BARS ThyA=13/20/6,
  ThyB=13/20/13; TFIXED=12; CVAL=15; ThyHKC=15/20/15;
  mcalib=(0,-11,-12,-3); pbkbar=(15,4,3,12);
  pboptbar=(15,16,5,15); UCB x V_WK=(75,128,55)=258;
  UCB x V_PBK=(70,138,40)=248; V_PBX=(90,138,55)=283;
  execute-all=(43,113,-80). New: mwmcalib=(0,0,-12,-3);
  pmwbar=(15,15,3,12); mncalib=(0,-7,-12,-5);
  pmnbar=(15,8,3,10) (in-program K3=1, via shallow sub-flags
  k3a-k3f).
- K4 (PRIMARY, preregistered NULL): PASS. UCB x V_PMW total
  228 < 258 AND UCB x V_PMN total 248 < 258 (in-program K4=1).
  No learner-computable marginal bar beats the fixed stakes
  bar.
- K5: PASS. Execute-all = (43, 113, -80) (in-program K5=1).
- K6: PASS. UCB x V_PMN total = 248 = UCB x V_PBK total
  (in-program K6=1), with identical GO sets on all three
  batches.
- K7: PASS. UCB x V_PMW total = 228 < 248 = UCB x V_PMN total
  (in-program K7=1). The fixed-window marginal estimate is
  noisier, not more decision-relevant.
- K8: PASS. WC-FINAL=138 (in-program K8=1).
- K9 (divergence): PASS. UCB x V_PMN total 248 < UCB x V_WK
  total 258 (in-program K9=1).
- K10 (divergence): PASS. V_PMWX total 288 > UCB x V_PMW total
  228 AND V_PMNX total 318 > UCB x V_PMN total 248
  (in-program K10=1).

## Mechanism detail (white box)

### Why V_PMN coincides exactly with V_PBK (K6)

V_PMN's bars (15,8,3,10) differ from V_PBK's (15,4,3,12), yet
the GO sets coincide on all three batches. The reason is
distributional, not structural: the differential bands contain
no sealed cases. b1 band (4,8]: sealed b1 adjs are 17/34/9 --
s10's adj=9 sits just above the band, GO under both bars.
b3 band (10,12]: sealed b3 adjs are 24/6/2, 30/20/5, 13 --
none in (10,12]. b2 and b0 bars are identical (3, 15). So the
half-nearest marginal estimate buys nothing over the bucket
mean here, and both inherit the same failures (s0's -15 at @15
via the b2 bar 3; s5's -15 at @45 via the b3 bars 10/12).

### Why V_PMW does worse than V_PMN (K7)

The W=10 window keeps only 2 marginal train cases in b1: t5
(17,33) with gap -16 and t17 (17,0) with gap +17. The local
estimate is (1)/2 = 0 -- the single (17,0) train case exactly
cancels the (17,33) case, the same (17,0) case that made
PBOPT's b1 bar overfit in PERBUCKET. So the b1 bar stays at 15
and misses s10's +10 at @15 and @30 (-20 vs V_PMN). The
N-nearest rule keeps 4 cases (adding two (34,50) cases with
gap -16), giving -7 and bar 8, which takes s10. Fewer cases
make the marginal estimate dominated by train noise: locality
amplifies overfitting rather than removing it.

### Why the exact marginal bounds win and the learner cannot follow (K10)

The exact sealed marginal gaps vs the train marginal gaps the
learner must use (W=10 rule):

| bucket | train marginal | @15 exact | @30 exact | @45 exact |
|---|---|---|---|---|
| b0 | 0 (fallback) | 0 (fb) | 0 (fb) | 0 (fb) |
| b1 | 0 | -16 | -16 | 17 (fb) |
| b2 | -12 | +13 | -2 | -2 (fb) |
| b3 | -3 | -11 | -12 | +13 |

The shift moves marginal miscalibration in ways bucket
identity cannot predict, just as it did for the bucket means:
b2 flips sign at @15 (-12 -> +13), b3 flips sign at @45
(-3 -> +13), b1 shifts level (-16 sealed vs 0 train). Locality
does not fix transferability -- it cannot, because nothing in
{train, bkt, K} observes the shift's local effect before
commitment.

The exact bounds' edge decomposes exactly. V_PMWX (288) vs
V_PMW (228): @15, the exact b1 bar -1 takes s10's +10 and the
exact b2 bar 28 avoids s0's -15 (20), plus the exact b3 bar 4
takes s6's +5 (10); @30, the exact b3 bar 3 takes s11's +5
(5); @45, 0. V_PMNX (318) vs V_PMN (248): the same 35, plus
@45 the exact b1 bar 49 avoids s0/s4's -15s (30) -- because
the two marginal sealed b1 cases at @45 are both (34,0) with
local gap +34, while the far-from-margin case (84,100) has gap
-16 and drags the full-bucket mean down to 17. That is the
"mean driven by far-from-margin cases" phenomenon made
exact: at the margin, the miscalibration is +34, not +17.
V_PMNX (318) beats even the per-bucket exact bound V_PBX
(283) by 35 -- but it is a bound on a finer estimand, using
sealed data at finer locality. The learner cannot touch it.

### Is the marginal signal more stable across train->sealed shifts? No.

Train vs sealed marginal gaps (W=10): b1: 0 -> (-16, -16);
b2: -12 -> (+13, -2); b3: -3 -> (-11, -12, +13). Compare the
full-bucket gaps: b1: -11 -> (-7, -7, +17); b2: -12 ->
(+13, -2, -2); b3: -3 -> (-11, -1, +13). The sign flips (b2
@15, b3 @45) and level shifts (b1) persist at the margin; the
marginal estimates are additionally noisier (2-4 cases vs 7).
Locality neither stabilizes the signal nor makes the shifts
predictable.

### Probe-proofness is preserved (K1-A10)

Structural, not claimed. The PMW dataflow is bkt_s (sealed,
from belief composition, bias-free) -> mwmcalib[bkt_s]
(train-fixed under the frozen W=10 rule) -> K +
mwmcalib[bkt_s]. The PMN dataflow is bkt_s -> mncalib[bkt_s]
(train-fixed under the frozen N_b rule) -> K +
mncalib[bkt_s]. No sealed bias-adjusted score (adjucb)
enters either bar computation. The lineage's fenced probes
touch adjusted scores only, never bkt, so both marginal bars
are identical under probes. The PMWX/PMNX diagnostics are
explicitly fenced and do not feed any verdict.

## Answers to the task's key questions

1. **Is marginal miscalibration more predictive than
   bucket-mean?** No -- K4/K6/K7 (228 < 248 = 248). The
   fixed-window version is strictly worse; the N-nearest
   version makes identical commitments to the bucket mean,
   not better ones. Measuring miscalibration only on
   marginal cases does not improve on the bucket mean from
   train alone.
2. **Can we capture the decision-relevant information?** No,
   as a verdict input -- K10 (288/318 vs 228/248, gaps of
   60/70). The exact marginal bounds show the information is
   real (PMNX avoids s0/s4's -15s at @45 through the exact
   local gap +34; PMWX takes s11's +5 at @30 through the
   exact local gap -12), but train->sealed marginal gap
   shifts (sign flips in b2 @15 and b3 @45, level shift in b1)
   are not predictable from {train, bucket identity, K}.
   Locality does not fix the transfer problem.
3. **What is the right definition of "marginal"?** Of the two
   tested: the data-driven half-nearest rule (V_PMN)
   generalizes no worse than the bucket mean (identical GO
   sets, 248 = 248), while the fixed window W=10 (V_PMW)
   generalizes worse (228 < 248) -- with 2 marginal train
   cases in b1, the local estimate is dominated by the
   single (17,0) train case that also drove PBOPT's
   overfitting. Neither beats fixed-K (258). Named follow-up
   not tested this wave: a two-stage definition (marginality
   relative to the stage-1 bar K + mcalib rather than K).

## Honest caveats

1. One wall-density law-change axis; item law, belief noise, and
   energy budget fixed (inherited from the IVWC lineage).
2. K=15 is a preregistered world cost, chosen near the bar
   center (inherited); the profit ranking is K-sensitive. The
   K4/K9/K10 divergences are specific to K=15; the
   K-sensitivity curve remains a named follow-up.
3. The execute-all reference is counterfactual (fenced); the
   primary metric uses only real GO commitments.
4. The V_PMWX/V_PMNX diagnostics are fenced (read sealed eff)
   and are not candidate mechanisms; their value is in
   bounding the marginal estimand, not as proposals. V_PMNX is
   a bound on a finer estimand than V_PBX (finer locality),
   so 318 > 283 is not a contradiction.
5. Both learner marginal bars inherit train's marginal gaps;
   neither can adapt to sign flips under shift. This is a
   property of the signals, reported as a finding.
6. The D1b/D2b probe arms were not re-run; probe-proofness for
   the marginal bars is established structurally (K1-A10),
   not behaviorally, this wave.
7. W=10 is a frozen structural mechanism parameter
   (preregistered, never tuned); N_b = ceil(n_b/2) is
   data-driven with no magnitude constant. The two-stage
   marginality definition (relative to K + mcalib) was named
   but not tested.
8. Mechanism application, not a composition-novelty or L3 claim.
   The composer is fixed.

## Process notes and disclosures

- **No toolchain incident.** This lane is clean: zero
  python3/python invocations at any step. Safebin PATH
  throughout (`which python3` and `which python` return
  nothing). Pure Zag, pinned znc. See NAMECHECK.md Step 0.
- **Token audits pre-build:** A3/A4/A8/A9 all read 0 before the
  build; the source avoids "miscalibration-adjusted"
  phrasing only where the audit tokens would match (the
  perbucket "miscalibration-corrected" lesson was applied:
  "adjusted" used throughout).
- No post-prereg probe of any kind. All predictions were
  arithmetic on the committed tables. Every frozen prediction --
  all arm profits, all GO counts, WC-FINAL=138, all bar values,
  mwmcalib, mncalib, PMWX/PMNX gaps/bars -- confirmed exactly.

## Reproduction

```
cd docs/lab/research-lead/overnight-20260928/ivwc_marginal
$HOME/safebin/znc src/ivwc_marginal.zag -o bin/ivwc_marginal  # safebin PATH, pinned znc
./bin/ivwc_marginal | sha256sum  # expect 5aad447e116406088993c1ae6449fa359e3608a4814c194078d20243d730a60f
```

Frozen audits (PREREG K1): A1 phase order
480<487<495<507<513<763<867<875<893<936<966<977<992<1067<1145;
A2 0; A3 0; A4 0; A5 `world_execute(` x4 (1 def + 3 call sites);
A6 WC-FINAL=138; A7 0 `learner_`/`belief_` after CONSEQUENCE;
A8 0; A9 0 `Tpred`; A10 PMW/PMN bars read no sealed adjusted
score (bkt -> train-fixed local quantities under the frozen
marginality rules -> bar); PMWX/PMNX fenced, not learner bars.
K2: sha256 equality across
runs/ivwc_marginal-run{1,2,3}.txt. Train TAUDIT 24/24
byte-identical to the committed lineage table.

## Branch note

Work committed on `tnn-native-lab` in the `~/workspace/tnn-rsi`
worktree (prereg commit `d7008d7ee` strictly precedes the
implementation). All commits use explicit pathspecs (via
separate GIT_INDEX_FILE plumbing, leaving the shared index
untouched) confined to `ivwc_marginal/`. `bin/` (reproducible
via the pinned znc) is deliberately excluded from the commit per
Micah's 2026-10-03 guidance. This is a non-ledger task. Pushing
to origin is AUTHORIZED per Micah's 2026-10-03 authorization;
this lane is clean (zero python3/python invocations).
