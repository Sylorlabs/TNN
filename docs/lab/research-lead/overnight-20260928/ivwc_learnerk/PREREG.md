# PREREG.md -- IVWC-LEARNERK: learner-owned K (revealed stakes)

## Wave

Follow-up from IVWC-MARGINAL (BUILD-PASS K1-K10). MARGINAL closed the
"marginal decision-boundary-local miscalibration" branch with a clean NULL:
V_PMW 228 and V_PMN 248 both lose to fixed-K V_WK 258, while the fenced
exact marginal bounds (288/318) confirm the information is real but not
learner-usable from train alone. The arc pattern is now eight waves deep:
every learner-computable adjustment to the worth-K bar loses to the fixed
stakes bar. The remaining named frontiers are **learner-owned K** and the
**K-sensitivity curve**. This wave builds the first: can the learner own K
-- determine the stakes itself from experience -- rather than having K=15
supplied as a world parameter?

Non-ledger task. Lane `ivwc_learnerk/`. Pure Zag, safebin, 3/3
byte-identical. Commits local on `tnn-native-lab` via explicit pathspec
plumbing. Pushing to origin is AUTHORIZED per Micah's 2026-10-03
authorization (fresh GitHub PAT; exclude reproducible cache/build
artifacts).

## Operational definition of "learner-owned K"

K=15 (EXCOST) is currently a `const` in the source: a world parameter the
bars read as a given. "Learner-owned K" is operationalized here as
**revealed stakes**: the learner sets its GO/NO-GO threshold to the bar
that maximized its *experienced* train net outcomes, where the world's
cost parameter never enters the learner's computation.

Concretely:

- On train, the harness reports per-case **net outcomes**
  `tnet[t] = teff[t] - EXCOST` (a new learner-visible train quantity,
  filled harness-side after train CONSEQ; zero world calls). The net is
  what the learner actually experienced: reward minus charge as a single
  number, the faithful "consequence" interface. (The current
  eff-visible-plus-K-given interface is the artificial one: in deployment
  you experience net outcomes, not a decomposed (effect, cost) pair plus a
  separately announced price.)
- The stakes-owning computation reads **only** `tnet`, the learner's own
  train scores `tadj[t] = preff_tr[t] - bucb[tbkt[t]]`, and bucket ids.
  It never reads `EXCOST` and never reads `teff` directly. This is enforced
  by a textual audit (K1-A10b): zero `EXCOST` tokens and zero `teff`
  tokens inside the two LOK functions.
- Note the learner *could* recover K=15 from (teff, tnet) -- it does not.
  The restriction is the point: the stakes are set from experienced
  outcomes, not from a world model plus an announced cost. The audit makes
  the restriction structural, not claimed.

This answers "what does learner-owned K mean operationally": the decision
threshold becomes a learner-determined variable (argmax over experienced
nets) instead of a world-supplied constant. It is *not* cost inference
(backing K=15 out of (eff, net) pairs, which would be trivial and teach
nothing), and it is *not* a researcher-set risk attitude.

## Design

**V_LOK (MAIN-1): global revealed stakes.** `lokbar` = argmax over integer
bars b of P(b) = sum over train cases t with `tadj[t] > b` of `tnet[t]`.
Candidate range [min_t tadj[t] - 1, max_t tadj[t]] (data-driven, no
magnitude constant; the bar must be decidable from the data). Ties broken
toward the **larger** bar (conservative: when train-indifferent, demand
higher stakes). Sealed verdict: GO iff `adjucb_s > lokbar`. Reads no
bucket, no sealed quantity except the score under test (as every verdict
does). The direct learner-owned analog of the V_WK fixed-K control.

**V_LOKB (MAIN-2): per-bucket revealed stakes (context-adaptive).**
Per bucket b, `lokbbar[b]` = argmax over integer bars c of
P_b(c) = sum over train cases t in bucket b with `tadj[t] > c` of
`tnet[t]`, candidate range [min/max train adj within bucket] (same
data-driven rule), ties toward the larger bar. Sealed verdict: GO iff
`adjucb_s > lokbbar[sbkt_s]`. This is the "adapt K based on context"
reading: stakes vary by bucket, all owned. (It is PBOPT's objective with
the K-given tie-break and K-referencing candidate range removed; see the
b3 difference below.)

**Controls / lineage.** UCB x V_WK (bar = EXCOST, verbatim lineage
control) is re-run; it is also the exact-stakes reference (no fenced exact
diagnostic is needed: V_WK *is* the true-stakes verdict). Fenced
execute-all reference is re-run (K5). The V_HA/V_HKC/V_BAMK/V_PBK/V_PMW/
V_PMN verdict arms and the D1b/D2b +40 probe arms are not re-run (their
bars remain computed and printed for the K3 verbatim-machinery check;
probe-proofness for the LOK bars holds structurally: the bars are
train-fixed and never read a sealed bias-adjusted score, K1-A10).

**Correction-independence.** The LOK bars are computed from train
(tnet, tadj, tbkt) only. The verdict compares the sealed score to the
train-fixed bar. No sealed bias-adjusted score enters any bar computation;
the fenced lineage probes touch adjusted scores only and cannot move the
LOK bars. Structural, audited as K1-A10/A10b.

## Stakes K

K = 15 remains the world's execution cost (EXCOST), charged in
`conseq_arm` and the REFERENCE. What changes is that the *learner's new
verdicts* do not read it. The world parameter is unchanged; the learner's
dependence on it is removed.

## Background facts (from committed tables, not probed)

World/belief/composer/stepper/seeds/biases/bars verbatim from the IVWC
lineage (K3 re-verifies: ThyA = 13/20/6, ThyB = 13/20/13, TFIXED = 12,
CVAL = 15, ThyHKC = 15/20/15, bucb = (0,16,27,20)).
Committed train (t, bkt, adj, eff) and sealed (s, bkt, adjucb, eff)
per-case tables from IVWC-MARGINAL PREREG.md (citing IVWC-PERBUCKET):

Train nets `net = eff - 15`:
- b0 (7): (0,-15) x7.
- b1 (7): (34,35) (17,18) (84,85) (34,35) (34,35) (34,35) (17,-15).
- b2 (7): (-9,-9) (23,10) (-10,-15) (6,18) (15,27) (6,-15) (0,-6).
- b3 (3): (5,-10) (7,1) (9,-4).

Sealed (bkt, adj, eff):
- sh=0 (@15): s0:(2,13,0) s1:(0,0,0) s2:(1,17,33) s3:(1,34,0)
  s4:(1,17,33) s5:(3,24,33) s6:(3,6,20) s7:(1,17,33) s8:(0,0,0)
  s9:(1,17,33) s10:(1,9,25) s11:(3,2,13).
- sh=1 (@30): s0:(3,30,10) s1:(0,0,0) s2:(1,17,33) s3:(1,34,50)
  s4:(1,34,50) s5:(3,20,30) s6:(1,34,0) s7:(2,23,25) s8:(1,34,50)
  s9:(0,0,0) s10:(1,9,25) s11:(3,5,20).
- sh=2 (@45): s0:(1,34,0) s1:(0,0,0) s2:(0,0,0) s3:(2,-2,0)
  s4:(1,34,0) s5:(3,13,0) s6:(0,0,0) s7:(0,0,0) s8:(0,0,0)
  s9:(0,0,0) s10:(0,0,0) s11:(1,84,100).

## Frozen derivations (arithmetic on the committed tables)

**Global revealed bar.** P(b) = sum of train nets over cases with adj >
b. Grouping by adj: (-10,-15) (-9,-9) (0,-111 over 8 cases) (5,-10)
(6,+3 over 2) (7,+1) (9,-4) (15,+27) (17,+3 over 2) (23,+10)
(34,+140 over 4) (84,+85). Cumulative from the top:
b>=84: 0; 34<=b<=83: 85; 23<=b<=33: 225; 17<=b<=22: 235;
15<=b<=16: 238; 9<=b<=14: 265; 7<=b<=8: 261; b=6: 262; b=5: 265;
0<=b<=4: 255; -9<=b<=-1: 144; b=-10: 135; b<=-11: 120.
Maximum 265, tied exactly at b in {5} U {9,10,11,12,13,14} (the
(6,+-15),(7,+1),(9,-4) nets cancel: 18-15+1-4 = 0, so b=5 ties the
9..14 plateau). Preregistered tie-break (larger / conservative):
**lokbar = 14**. Sensitivity (arithmetic, not run): the aggressive
tie-break (b=5) would give sealed (75,138,-40) = 173 -- the tie-break is
load-bearing and is disclosed here, not chosen post-hoc.

**Per-bucket revealed bars.**
- b0: adjs {0}x7, nets -15 x7. P(0) = 0 (adj>0: none); P(-1) = -105.
  Range [-1,0]. Unique max at **0**.
- b1: P(b): b>=84: 0; 34<=b<=83: 85; 17<=b<=33: 225; b<=16: 228.
  Range [16,84]. Unique max at **16**.
- b2: P(b): b>=23: 0; 15<=b<=22: 10; 6<=b<=14: 37; 0<=b<=5: 40;
  -9<=b<=-1: 34; b=-10: 25; b<=-10... b=-11: 10. Range [-11,23].
  Max 40 tied at {0..5}, larger -> **5**.
- b3: P(b): b>=9: 0; 7<=b<=8: -4; 5<=b<=6: -3; b<=4: -13.
  Range [4,9]. Unique max at **9**.
So **lokbbar = (0,16,5,9)**. Note vs PBOPT's (15,16,5,15): b0 and b3
differ *only* through the K-free candidate range and tie-break (PBOPT's
range reached up to max(max_adj, K) and its tie-break pulled toward K).
Behaviorally on sealed: b0 (all sealed b0 adjs are 0; 0>0 false under
both bars) is identical; b3 differs at sh=2 s5 (adj 13: 13>9 GO under
LOKB, 13>15 no-GO under PBOPT) -- a -15 swing, priced below.

## Frozen profit predictions (profit = sum over GO of (eff-15); GO iff score > bar, strict)

UCB x V_LOK (bar 14; MAIN-1):
- sh=0: GO {2,3,4,5,7,9} (6): 18-15+18+18+18+18 = 75. (s0 adj 13,
  not > 14; s10 adj 9, no.)
- sh=1: GO {0,2,3,4,5,6,7,8} (8): -5+18+35+35+15-15+10+35 = 128.
- sh=2: GO {0,4,11} (3): -15-15+85 = 55. (s5 adj 13, not > 14.)
- Total: **258** (17 GO). GO sets identical to V_WK on all batches
  (no sealed adj equals 15; 14 and 15 are decision-equivalent here).

UCB x V_LOKB (bars (0,16,5,9); MAIN-2):
- sh=0: s0 b2 13>5 GO -15; s2 b1 17>16 GO +18; s3 b1 34>16 GO -15;
  s4 b1 17>16 GO +18; s5 b3 24>9 GO +18; s7 b1 17>16 GO +18;
  s9 b1 17>16 GO +18. GO {0,2,3,4,5,7,9} (7).
  profit = -15+18-15+18+18+18+18 = **60**.
- sh=1: s0 b3 30>9 GO -5; s2 b1 17>16 GO +18; s3 b1 34>16 GO +35;
  s4 b1 34>16 GO +35; s5 b3 20>9 GO +15; s6 b1 34>16 GO -15;
  s7 b2 23>5 GO +10; s8 b1 34>16 GO +35. GO {0,2,3,4,5,6,7,8} (8).
  profit = -5+18+35+35+15-15+10+35 = **128**.
- sh=2: s0 b1 34>16 GO -15; s4 b1 34>16 GO -15; s5 b3 13>9 GO -15;
  s11 b1 84>16 GO +85. GO {0,4,5,11} (4).
  profit = -15-15-15+85 = **40**.
- Total: **228** (19 GO).

Lineage reference:
- UCB x V_WK (bar 15; verbatim control): (75,128,55) = **258**,
  GO (6,8,3).
- execute-all: (43,113,-80) = 76.

WC-FINAL: 24 train + 53 GO (17 + 17 + 19; no fenced diagnostics use
world calls) + 36 reference = **113**.

## Frozen kill bars

- **K1 (diet / commit order / no-exact-signal / probe-proofness /
  ownership): PASS required.** A1: phase order train SETUP < train
  COMMIT < train PREFF < train CONSEQ < train LEARN < train TNET <
  train BAR < sealed SETUP < sealed COMMIT < sealed BARS < sealed
  VERDICT (GO) < CONSEQUENCE (world_execute on GO) < REFERENCE, by
  source line order (strict increase is the frozen property; actual line
  numbers recorded in the report). A2: zero `world_buf`/`world_off`
  tokens in learner fns (lc_blocked, lc_leg, learner_compose,
  gather_cells, lok_global, lok_bucket). A3: zero
  `expected|answer|key|target` (case-insensitive). A4: zero
  `correct|reference_plan|gold`. A5: `world_execute(` exactly 4
  occurrences (1 def + 3 call sites: train CONSEQ, the shared
  `conseq_arm` helper, REFERENCE). A6: WC-FINAL = 113. A7: zero
  `learner_`/`belief_` calls after the CONSEQUENCE marker. A8: the
  token "oracle" (case-insensitive) appears zero times. A9: the token
  `Tpred` appears zero times. A10 (probe-proofness): the V_LOK/V_LOKB
  bars are computed from train (tnet, tadj, tbkt) only and never read a
  sealed bias-adjusted score; the fenced lineage probes touch adjusted
  scores only, never bkt, so they cannot move either LOK bar. A10b
  (ownership): zero `EXCOST` tokens and zero `teff` tokens inside the
  `lok_global` / `lok_bucket` function bodies (the stakes computation
  never sees the world's cost parameter nor the decomposed effect
  table; it sees only experienced nets, the learner's own train scores,
  and bucket ids).
- **K2 (determinism): PASS required.** 3/3 runs byte-identical stdout.
- **K3 (verbatim machinery + new): PASS required.** BARS lines: ThyA =
  13/20/6, ThyB = 13/20/13 @15/30/45; TFIXED = 12; CVAL = 15; ThyHKC =
  15/20/15; bucb = (0,16,27,20); mcalib = (0,-11,-12,-3); pbkbar =
  (15,4,3,12); pboptbar = (15,16,5,15); UCB x V_WK = (75,128,55) =
  258; execute-all = (43,113,-80). New: lokbar = 14; lokbbar =
  (0,16,5,9) (in-program exact checks).
- **K4 (PRIMARY, preregistered NULL): PASS required.** UCB x V_LOK
  total = 258, NOT > 258, AND UCB x V_LOKB total = 228 < 258.
  Learner-owned K does not beat fixed-K: the global revealed-stakes bar
  ties the given stakes exactly, and the per-bucket revealed stakes lose.
- **K5: PASS required.** Execute-all per-batch profit = (43,113,-80).
- **K6: PASS required.** UCB x V_LOK total = 258 with GO sets identical
  to UCB x V_WK on all three batches (in-program per-case GO equality
  check). Mechanism: lokbar 14 vs fixed 15; no sealed adj equals 15, so
  the bars are decision-equivalent on these batches.
- **K7: PASS required.** UCB x V_LOKB total = 228 < 258 = UCB x V_LOK
  total. Per-bucket revealed stakes overfit relative to the global
  revealed bar (the b3 bar 9 takes s5's -15 at @45; the b2 bar 5 takes
  s0's -15 at @15) -- the same below-batch overfitting lesson as
  PBOPT, now without K anywhere in the computation.
- **K8: PASS required.** WC-FINAL = 113 (in-program).
- **K9 (divergence): PASS required.** UCB x V_LOKB total 228 < UCB x
  V_WK total 258. Context-adaptive owned stakes do NOT beat pure
  worth-K.
- **K10: PASS required.** UCB x V_LOK total = 258 = UCB x V_WK total
  (in-program equality). Ownership without loss: the learner recovers
  decision-equivalent stakes from experienced net outcomes alone, with
  the world's cost parameter absent from its computation (K1-A10b).

**BUILD-PASS requires K1..K10.**

## Preregistered answers to the task's key questions

1. **Can the learner own K effectively?** Predicted YES for the global
   bar (K10: V_LOK 258 = V_WK 258 -- the learner recovers
   decision-equivalent stakes from train net outcomes alone; K6: the GO
   sets coincide exactly), NO for the per-bucket version (K7/K9: 228 <
   258 -- revealed per-bucket stakes overfit train, mirroring PBOPT's
   lesson with K removed from the computation entirely).
2. **Does learner-owned K beat fixed-K (15)?** Predicted NO (K4,
   preregistered NULL): 258 ties, 228 loses. Owning the stakes does not
   improve on being given them; at best (global) it matches.
3. **Is this the right direction for Priority #4?** Predicted: it closes
   the "can the learner determine stakes from experience" question
   (yes -- globally, without loss) but opens no new winning direction;
   the worth-K verdict is *robust* to removing K as a given rather than
   improved by owning it. The remaining frontier is the K-sensitivity
   curve (for which K do the rankings change?), explicitly not tested
   this wave.

## L2 vs L3 assessment (preregistered)

Learner-owned K as built here is **L1 (parameter learning) with an L2
flavor**, not L3. The bar *form* (single global threshold / per-bucket
thresholds) is researcher-given; the learner fills the *value* by
optimization over its experience (L1). The L2 flavor: the learner takes
ownership of a decision variable (its stakes) that was previously a
world-supplied constant, via a revealed-preference optimization it runs
itself. It is not L3 by a wide margin: no new representation,
abstraction, or procedure is invented; the final threshold form is
researcher-enumerated; Criterion 0 fails (the source holds the complete
threshold machinery, not generic machinery from which the learner builds
something unforeseen).

## Determinism and honesty rules

- Integer arithmetic only. The candidate ranges ([min_adj-1, max_adj],
  global and per-bucket) are data-driven with no magnitude constant; the
  larger-bar tie-break is a preregistered conservative structural rule,
  never tuned (its load-bearing sensitivity, b=5 -> 173, is disclosed
  above as arithmetic, not run).
- No post-prereg probe of any kind. All predictions above are arithmetic
  on the committed tables.
- The tokens `Tpred`, `oracle`, `expected`, `answer`, `key`, `target`,
  `correct`, `reference_plan`, `gold` do not appear in the implementation
  source (K1 A3/A4/A8/A9). The LOK functions additionally avoid `EXCOST`
  and `teff` (K1 A10b).
- If any arm differs from prediction in either direction, report the
  exact mechanism. No bar moves after seeing results.
