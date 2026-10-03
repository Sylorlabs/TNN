# PREREG.md -- IVWC-CONSEQUENCE: consequence-aware hybrid verdict

## Wave

Follow-up from IVWC-APPLIED (BUILD-PASS K1-K10). APPLIED applied
the hybrid verdict (V_HA/V_HB) to selective execution with no
oracle and found the central divergence: D1b x V_HA has better
accuracy than D1b x V_N (35/36 vs 34/36, committed verdict-wave
table) but worse profit (262 vs 280). The hybrid bar answers a
relative-trust question ("above the batch's level?"), not a
consequence question ("worth K?"). It is cost-blind by
construction: K never enters the bar.

This wave builds the specified next frontier: a
**consequence-aware hybrid verdict** that keeps
correction-independence (the bar never reads the learner's sealed
corrected scores) while incorporating the stakes K (a world
parameter, not a label).

Non-ledger task. Lane `ivwc_consequence/`. Pure Zag, safebin, 3/3
byte-identical. Commits local on `tnn-native-lab` via explicit
pathspec plumbing. Pushing to origin is AUTHORIZED per Micah's
2026-10-03 authorization (fresh GitHub PAT; exclude reproducible
cache/build artifacts).

## Design

Two new verdicts, same selective-execution setup as APPLIED
(verbatim world/belief/composer/stepper/seeds/biases; K3
re-verifies bars; scoring is pure consequence, profit = sum over
GO of (eff - K), no labels anywhere).

**V_HKC (consequence-aware hybrid, KEY).** bar_HKC(sh) =
max(ThyA(sh), K), with K = EXCOST = 15. The learner renders GO
iff its corrected score clears BOTH the hybrid bar and the
stakes: above the batch's level AND worth K. Correction-
independence is preserved structurally: the bar reads only
preff (sealed, bias-free), C (train-fixed), and K (world
constant). It never reads the learner's sealed corrected scores
(adjucb / d1adj / d2adj), so the fenced +40 probes cannot move
it -- the same structural guarantee as V_HA, now with stakes.
When the batch level undershoots the stakes (@45: ThyA=6 < 15),
K binds and blocks losing executions. When the batch level
covers the stakes (@15/@30), the hybrid governs.

**V_WK (worth-K control).** bar = K = 15, a constant. The pure
consequence question ("worth K?") with no batch-relative
component. This arm tests the task's key question directly: is
"worth K?" the right question, and does the hybrid's
relative-trust level carry any profit-relevant information once
stakes are incorporated? The K bar is trivially
correction-independent (it reads nothing at all).

Arms (9 + reference): UCB x V_HA (baseline), UCB x V_HKC (KEY),
UCB x V_WK (control); D1b x V_HA, D1b x V_HKC, D1b x V_WK;
D2b x V_HA, D2b x V_HKC, D2b x V_WK (fenced diagnostics, +40
never learner-visible); fenced execute-all reference.

## Stakes K

K = 15 efficiency units per execution, fixed across all batches
and arms, preregistered here and inherited from APPLIED. K is a
WORLD parameter (the cost of committing resources), not a label
and not a threshold on truth. Unlike APPLIED (where the
learner's verdict did not take K as input -- cost-blind by
design), this wave gives the verdict K as an explicit world
parameter: the bar may read K, but K is a constant of the world,
fixed before any sealed case is seen, so no oracle is
introduced and correction-independence is preserved.

## Background facts (from committed tables, not probed)

World/belief/composer/stepper/seeds/biases/bars verbatim from
IVWC-HYBRID-VERDICT (K3 checks: BARS ThyA=13/20/6,
ThyB=13/20/13, TFIXED=12, CVAL=15). Committed per-case sealed
eff (from `ivwc_hybrid_verdict/runs/ivwc_hybrid_verdict-run1.txt`,
V lines):

- sh=0 (@15): eff = [0,0,33,0,33,33,20,33,0,33,25,13]
- sh=1 (@30): eff = [10,0,33,50,50,30,0,25,50,0,25,20]
- sh=2 (@45): eff = [0,0,0,0,0,0,0,0,0,0,100]

Per-case scores reconstructed from the committed V lines
(preff, bkt, nph per case) with bucb=(0,16,27,20) (from the
committed train TAUDIT: adj = preff - bucb[bkt] verified on all
24 train cases): adjucb = preff - bucb[bkt];
d1adj = adjucb - (40 iff nph>0); d2adj = adjucb - (40 iff
nph[(s+7)%12]>0). Reconstructed (adjucb, d1adj, d2adj, eff):

- sh=0: s0:(13,-27,13,0) s1:(0,0,0,0) s2:(17,17,17,33)
  s3:(34,-6,34,0) s4:(17,17,-23,33) s5:(24,-16,-16,33)
  s6:(6,-34,6,20) s7:(17,17,17,33) s8:(0,0,-40,0)
  s9:(17,17,17,33) s10:(9,9,-31,25) s11:(2,-38,-38,13)
- sh=1: s0:(30,-10,-10,10) s1:(0,0,0,0) s2:(17,17,17,33)
  s3:(34,34,34,50) s4:(34,34,-6,50) s5:(20,-20,-20,30)
  s6:(34,-6,34,0) s7:(23,-17,23,25) s8:(34,34,34,50)
  s9:(0,0,0,0) s10:(9,9,-31,25) s11:(5,-35,-35,20)
- sh=2: s0:(34,-6,34,0) s1:(0,0,0,0) s2:(0,0,0,0)
  s3:(-2,-42,-2,0) s4:(34,-6,34,0) s5:(13,-27,-27,0)
  s6:(0,0,0,0) s7:(0,0,0,0) s8:(0,0,-40,0) s9:(0,0,-40,0)
  s10:(0,0,-40,0) s11:(84,84,84,100)

Bars: ThyA=(13,20,6) [committed]; ThyHKC=max(ThyA,15)=(15,20,15);
WK bar=15. GO = 1 iff score > bar (strict, as in the lineage).

Derived GO sets (new arms; baselines are the committed V-line
verdict bits a7a/a8a/a9a):

- UCB-HA: sh0 {2,3,4,5,7,9} sh1 {0,3,4,6,7,8} sh2 {0,4,5,11}
- UCB-HKC: sh0 {2,3,4,5,7,9} sh1 {0,3,4,6,7,8} sh2 {0,4,11}
- UCB-WK: sh0 {2,3,4,5,7,9} sh1 {0,2,3,4,5,6,7,8} sh2 {0,4,11}
- D1b-HA: sh0 {2,4,7,9} sh1 {3,4,8} sh2 {11}
- D1b-HKC: sh0 {2,4,7,9} sh1 {3,4,8} sh2 {11}
- D1b-WK: sh0 {2,4,7,9} sh1 {2,3,4,8} sh2 {11}
- D2b-HA: sh0 {2,3,7,9} sh1 {3,6,7,8} sh2 {0,4,11}
- D2b-HKC: sh0 {2,3,7,9} sh1 {3,6,7,8} sh2 {0,4,11}
- D2b-WK: sh0 {2,3,7,9} sh1 {2,3,6,7,8} sh2 {0,4,11}

GO counts per batch: (48, 34, 25) summed over the 9 arms = 107.
Train executions 24; fenced execute-all reference 36.
WC-FINAL = 24 + 107 + 36 = 167.

## Frozen profit predictions (K=15; profit = sum over GO of (eff-15))

sh=0: ucb_ha=75 ucb_hkc=75 ucb_wk=75 d1b_ha=72 d1b_hkc=72
       d1b_wk=72 d2b_ha=39 d2b_hkc=39 d2b_wk=39 all=43
sh=1: ucb_ha=95 ucb_hkc=95 ucb_wk=128 d1b_ha=105 d1b_hkc=105
       d1b_wk=123 d2b_ha=65 d2b_hkc=65 d2b_wk=83 all=113
sh=2: ucb_ha=40 ucb_hkc=55 ucb_wk=55 d1b_ha=85 d1b_hkc=85
       d1b_wk=85 d2b_ha=55 d2b_hkc=55 d2b_wk=55 all=-80

Totals: ucb_ha=210 ucb_hkc=225 ucb_wk=258 d1b_ha=262
        d1b_hkc=262 d1b_wk=280 d2b_ha=159 d2b_hkc=159
        d2b_wk=177 all=76

All predictions are arithmetic on the committed tables above. No
new data was generated or read before this prereg. If any profit
differs in either direction, the report states the exact
mechanism; no number moves after seeing results.

## Frozen kill bars

- **K1 (diet / commit order / no-oracle / correction-independence):
  PASS required.** A1: phase order train COMMIT < train PREFF <
  train CONSEQ < train LEARN < train BAR < sealed COMMIT < sealed
  BARS < sealed VERDICT (GO) < CONSEQUENCE (world_execute on GO)
  < FENCED-DIAG < REFERENCE, by source line order (exact numbers
  recorded post-build; strict increase is the frozen property).
  A2: zero `world_buf`/`world_off` tokens in learner fns
  (lc_blocked, lc_leg, learner_compose, gather_cells). A3: zero
  `expected|answer|key|target` (case-insensitive). A4: zero
  `correct|reference_plan|gold`. A5: `world_execute(` exactly 4
  occurrences (1 def + 3 call sites: train CONSEQ, the shared
  conseq_arm helper, REFERENCE). A6: WC-FINAL = 167. A7: zero
  `learner_`/`belief_` calls after the CONSEQUENCE marker. A8:
  the token "oracle" (case-insensitive) appears zero times. A9
  (the no-oracle bar): the token `Tpred` appears zero times --
  no transductive label threshold is computed anywhere, not even
  fenced. A10 (correction-independence): the BARS section
  contains zero reads of adjucb/d1adj/d2adj -- both new bars are
  computed from preff, C, bucb_frozen-aggregates, and K only
  (audited by source inspection of the BARS block).
- **K2 (determinism): PASS required.** 3/3 runs byte-identical
  stdout.
- **K3 (verbatim machinery): PASS required.** BARS lines:
  ThyA = 13/20/6, ThyB = 13/20/13 @15/30/45; TFIXED = 12;
  CVAL = 15; ThyHKC = 15/20/15 (in-program exact checks).
- **K4 (PRIMARY): PASS required.** UCB x V_HKC per-batch profit
  = (75, 95, 55), total 225; and 225 > UCB x V_HA total 210.
  Incorporating the stakes improves profit on the real learner
  case while keeping correction-independence: the
  consequence-aware hybrid beats the cost-blind hybrid.
- **K5: PASS required.** Execute-all per-batch profit =
  (43, 113, -80).
- **K6: PASS required.** UCB x V_HKC @45 = 55 > UCB x V_HA @45 =
  40. Mechanism: the K-floor binds (@45: max(6,15)=15) and blocks
  s=5's false GO (adjucb=13 < 15; eff=0; -15 avoided), recovering
  the @45 loss priced in APPLIED's K6 (and matching V_HB's
  committed 55 via stakes, not via the frozen baseline).
- **K7: PASS required.** D1b x V_HKC @15 = 72. The K-floor does
  not destroy the @15 un-blocking: max(13,15)=15 leaves the
  D1b-HA GO set {2,4,7,9} unchanged, profit 72 = HA's 72.
- **K8: PASS required.** WC-FINAL = 167 (in-program).
- **K9 (preregistered divergence): PASS required.** D1b totals:
  V_HKC = 262 < V_WK = 280. The pure worth-K bar beats the
  consequence-aware hybrid on the diagnostic: under the @30
  shift the hybrid's batch-tracking (bar 20) skips s=2
  (d1adj=17, eff=33, +18) while the stakes bar (15) takes it.
  The hybrid's relative-trust component is profit-harmful here.
- **K10 (preregistered divergence): PASS required.** UCB totals:
  V_HKC = 225 < V_WK = 258. Same finding on the learner's own
  arms: "worth K?" is not only the right question, it is
  sufficient -- the batch-relative level carries no
  profit-relevant information beyond the stakes on this problem.

**BUILD-PASS requires K1..K10.**

## Preregistered answers to the task's key questions

1. **Can we incorporate stakes without breaking
   correction-independence?** Predicted YES: K4+K6 (profit
   improves via the K-floor) with K1-A10 (the bars never read a
   sealed corrected score). K is a world parameter -- a constant
   of the consequence phase -- so it introduces no oracle and no
   transduction. Correction-independence is a structural property
   of what the bar reads, not of whether the bar knows the
   stakes.
2. **Is "worth K?" the right question?** Predicted YES, and more:
   K9/K10 preregister that the pure worth-K bar (V_WK) BEATS the
   consequence-aware hybrid (V_HKC) on both UCB (258>225) and
   D1b (280>262). The hybrid's batch-responsiveness -- the
   property that made it good for accuracy -- is actively harmful
   for profit when the batch level and the stakes disagree. The
   consequence-aware hybrid is a strict improvement over the
   cost-blind hybrid (K4), but the experiment is designed to
   falsify the hybrid's profit-relevance, not to protect it.
3. **What's the next frontier for Priority #4?** Whatever K9/K10
   confirm, the follow-up is a batch-aware worth-K: a bar that
   tracks the batch's *miscalibration* (how far the learner's
   corrected scores deviate from realized consequences under
   shift), not the batch's *level*. The hybrid tracked the wrong
   estimand for profit. Other candidates preregistered as
   follow-ups, not claims: (i) learner-owned K (stakes inferred
   from train consequences rather than given); (ii) the
   K-sensitivity curve (for which K do relative-trust and
   consequence-optimality align vs diverge?); (iii) per-bucket
   worth-K bars (the train bias is per-bucket; the stakes bar
   could be too).

## Determinism and honesty rules

- Integer arithmetic only. No researcher-set constants in any
  learner path (K=15 lives in the world/consequence phase as the
  execution cost and as the V_WK/V_HKC bar parameter; the
  D1b/D2b +40 lives only in the fenced diagnostic, as in prior
  waves).
- No post-prereg probe of any kind. All predictions above are
  arithmetic on the committed verdict-wave per-case tables.
- The tokens `Tpred`, `oracle`, `expected`, `answer`, `key`,
  `target`, `correct`, `reference_plan`, `gold` do not appear in
  the implementation source (K1 A3/A4/A8/A9). The BARS block
  reads no sealed corrected score (K1 A10).
- If any arm differs from prediction in either direction, report
  the exact mechanism. No bar moves after seeing results.
