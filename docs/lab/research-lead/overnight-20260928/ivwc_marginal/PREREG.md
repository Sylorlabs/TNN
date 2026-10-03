# PREREG.md -- IVWC-MARGINAL: decision-boundary-local per-bucket miscalibration

## Wave

Follow-up from IVWC-PERBUCKET (BUILD-PASS K1-K10). PERBUCKET
established: (1) preregistered NULL on all three key questions --
per-bucket bars V_PBK (248) and V_PBOPT (243) do NOT beat fixed-K
(258, K4/K9), and do NOT approach the exact bound (283, K10,
trail by 35); (2) the below-batch-level information is real but
not learner-usable from train alone; (3) root cause: the batch
mean gap is not decision-relevant because the mean is driven by
far-from-margin cases, and profit asks which side of the bar the
marginal cases are on. PERBUCKET's named next frontier:
"marginal (decision-boundary-local) per-bucket miscalibration,
learner-owned K, and the K-sensitivity curve -- since this wave
closed the 'per-bucket bars with train-level signals' branch with
a clean NULL."

This wave builds the specified next frontier: **marginal
(decision-boundary-local) per-bucket miscalibration**. Instead
of measuring miscalibration over the whole bucket (driven by
far-from-margin cases), measure it only on the train cases near
the worth-K bar -- where the marginal cases live -- and set each
bucket's bar from that local estimate. Two marginality rules are
tested (fixed window vs data-driven nearest count), against the
fixed-K control, the bucket-mean approach (V_PBK), and fenced
marginal exact bounds.

Non-ledger task. Lane `ivwc_marginal/`. Pure Zag, safebin, 3/3
byte-identical. Commits local on `tnn-native-lab` via explicit
pathspec plumbing. Pushing to origin is AUTHORIZED per Micah's
2026-10-03 authorization (fresh GitHub PAT; exclude reproducible
cache/build artifacts).

## Design

**V_PMW (marginal window, KEY-1).** Per bucket b, the marginal
train set is M_b = {t : tbkt[t] = b and |adj_t - K| <= W}, with
K = EXCOST = 15 and the half-width W = 10 frozen (a structural
mechanism parameter, preregistered, never tuned; the learner
still computes everything else from train data). adj_t =
preff_tr[t] - bucb[b] (learner-visible on train). The local
miscalibration is mwmcalib[b] = trunc mean over t in M_b of
(adj_t - teff[t]). If M_b is empty, fall back to the full-bucket
train mcalib[b] (documented; occurs for b0). bar_b = K +
mwmcalib[b]. Sealed verdict: GO iff adjucb_s > pmwbar[sbkt_s].
Reads only bkt_s (sealed, bias-free), train-fixed local
quantities, K, and the frozen window rule. Never reads a sealed
bias-adjusted score; probe-proof by structure (K1-A10).

**V_PMN (marginal N-nearest, KEY-2).** Per bucket b, let n_b be
the train case count in bucket b and N_b = ceil(n_b/2) =
(n_b+1)/2 (integer; data-driven, no magnitude constant). The
marginal train set is the N_b cases t with tbkt[t] = b
minimizing |adj_t - K|, ties broken by lowest train index t.
The local miscalibration is mncalib[b] = trunc mean over those
N_b cases of (adj_t - teff[t]). (All buckets are nonempty on
train, so no empty-set fallback is needed.) bar_b = K +
mncalib[b]. Sealed verdict: GO iff adjucb_s > pmnbar[sbkt_s].
Learner-computable, no sealed data, probe-proof by structure
(K1-A10).

**V_PMWX / V_PMNX (fenced marginal exact diagnostics, NOT
learner verdicts).** The exact sealed marginal gaps under the
same two marginality rules, computed fenced AFTER the REFERENCE
phase (which fills eff for all cases in cseal). V_PMWX: per
batch sh and bucket b, the marginal sealed set is {s :
sbkt[s] = b and |adjucb_s - K| <= 10}; the gap is the trunc
mean of (adjucb_s - eff_s) over that set, falling back to the
full-bucket exact gap when the set is empty; bar = K + gap.
V_PMNX: per batch sh and bucket b, n = sealed count in bucket
b, N = (n+1)/2; the gap is the trunc mean of (adjucb_s - eff_s)
over the N sealed cases minimizing |adjucb_s - K|, ties by
lowest sealed index; bar = K + gap. These bound the marginal
estimand: the best any decision-boundary-local signal could do.
They read sealed eff, so they are explicitly NOT probe-proof and
NOT candidate mechanisms; they are diagnostics. Zero
world_execute calls (pure arithmetic on the REFERENCE-filled
buffer and stored adjucb). In the source they are named `pmmwx`
/ `pmmnx` (the token "oracle" appears nowhere, per K1-A8).

Arms (4 + 3 fenced diagnostics + reference): UCB x V_WK
(verbatim lineage control; pure worth-K, bar = K); UCB x V_PBK
(verbatim bucket-mean comparator, bars (15,4,3,12)); UCB x V_PMW
(KEY-1); UCB x V_PMN (KEY-2); V_PMWX and V_PMNX (fenced marginal
exact diagnostics); V_PBX (fenced per-bucket exact diagnostic,
recomputed verbatim); fenced execute-all reference. The V_HA /
V_HKC verdict arms and the D1b/D2b +40 probe arms are not
re-run (their bars are still computed and printed for the K3
verbatim-machinery check; probe-proofness for the marginal bars
holds by the same bkt-driven structure and is audited as
K1-A10). The V_PBOPT verdict arm is not re-run (its bars are
still computed and printed for the K3 check); the key
comparisons this wave are marginal vs bucket-mean (V_PBK) vs
fixed-K (V_WK).

## Stakes K

K = 15, preregistered, inherited from the IVWC lineage. World
parameter (execution cost), not a label.

## Background facts (from committed tables, not probed)

World/belief/composer/stepper/seeds/biases/bars verbatim from
the IVWC lineage (K3 re-verifies: ThyA = 13/20/6, ThyB =
13/20/13, TFIXED = 12, CVAL = 15, ThyHKC = 15/20/15).
bucb = (0,16,27,20). Committed sealed (bkt, adjucb, eff) from
PERBUCKET PREREG.md (12-tuple eff for sh=2 read from the
per-case listing):

- sh=0 (@15): bkt = [2,0,1,1,1,3,3,1,0,1,1,3]
  (adj,eff): s0:(13,0) s1:(0,0) s2:(17,33) s3:(34,0) s4:(17,33)
  s5:(24,33) s6:(6,20) s7:(17,33) s8:(0,0) s9:(17,33)
  s10:(9,25) s11:(2,13)
- sh=1 (@30): bkt = [3,0,1,1,1,3,1,2,1,0,1,3]
  (adj,eff): s0:(30,10) s1:(0,0) s2:(17,33) s3:(34,50)
  s4:(34,50) s5:(20,30) s6:(34,0) s7:(23,25) s8:(34,50)
  s9:(0,0) s10:(9,25) s11:(5,20)
- sh=2 (@45): bkt = [1,0,0,2,1,3,0,0,0,0,0,1]
  (adj,eff): s0:(34,0) s1:(0,0) s2:(0,0) s3:(-2,0) s4:(34,0)
  s5:(13,0) s6:(0,0) s7:(0,0) s8:(0,0) s9:(0,0) s10:(0,0)
  s11:(84,100)

Train (t, bkt, adj, eff, gap = adj - eff) from the committed
train TAUDIT (`ivwc_perbucket/runs/ivwc_perbucket-run1.txt`,
24/24 lines):

- b0 (7): t1,t2,t12,t14,t15,t22,t23: (0,0) x7, gaps 0.
- b1 (7): t3:(34,50,-16) t5:(17,33,-16) t6:(84,100,-16)
  t9:(34,50,-16) t10:(34,50,-16) t13:(34,50,-16)
  t17:(17,0,+17). mcalib = -79/7 = -11.
- b2 (7): t4:(-9,6,-15) t11:(23,25,-2) t16:(-10,0,-10)
  t18:(6,33,-27) t19:(15,42,-27) t20:(6,0,+6) t21:(0,9,-9).
  mcalib = -84/7 = -12.
- b3 (3): t0:(5,5,0) t7:(7,16,-9) t8:(9,11,-2).
  mcalib = -11/3 = -3.

V_PMW local miscalibration (|adj - 15| <= 10; integer division,
trunc toward zero):

- b0: no train case within the window (all adj=0, d=15) ->
  fallback to full-bucket mcalib: **0**, bar **15**.
- b1: t5 (d2, gap -16), t17 (d2, gap +17) -> (1)/2 = **0**,
  bar **15**.
- b2: t11 (d8, -2), t18 (d9, -27), t19 (d0, -27), t20 (d9, +6)
  -> (-50)/4 = **-12**, bar **3**.
- b3: t0 (d10, 0), t7 (d8, -9), t8 (d6, -2) -> (-11)/3 =
  **-3**, bar **12**.

So mwmcalib = **(0,0,-12,-3)** and the V_PMW bars are
**(15,15,3,12)**.

V_PMN local miscalibration (N_b = ceil(n_b/2) nearest to K=15,
ties by lowest train index):

- b0: n=7, N=4: t1,t2,t12,t14 (all d=15, gaps 0) -> **0**,
  bar **15**.
- b1: n=7, N=4: t5 (d2,-16), t17 (d2,+17), t3 (d19,-16),
  t9 (d19,-16) -> (-31)/4 = **-7**, bar **8**.
- b2: n=7, N=4: t19 (d0,-27), t11 (d8,-2), t18 (d9,-27),
  t20 (d9,+6) -> (-50)/4 = **-12**, bar **3**.
- b3: n=3, N=2: t8 (d6,-2), t7 (d8,-9) -> (-11)/2 = **-5**,
  bar **10**.

So mncalib = **(0,-7,-12,-5)** and the V_PMN bars are
**(15,8,3,10)**.

Exact sealed marginal gaps (fenced; integer division, trunc
toward zero). V_PMWX (|adjucb - 15| <= 10, fallback to the
full-bucket exact gap when the marginal set is empty):

- sh=0: b0: {} -> fallback 0, bar 15. b1: {s2,s4,s7,s9,s10}
  gaps all -16 -> -16, bar -1. b2: {s0} gap +13 -> bar 28.
  b3: {s5,s6} gaps (-9,-14) -> -11, bar 4.
  PMWX bars sh=0: **(15,-1,28,4)**.
- sh=1: b0: {} -> fallback 0, bar 15. b1: {s2,s10} gaps
  (-16,-16) -> -16, bar -1. b2: {s7} gap -2 -> bar 13.
  b3: {s5,s11} gaps (-10,-15) -> -12, bar 3.
  PMWX bars sh=1: **(15,-1,13,3)**.
- sh=2: b0: {} -> fallback 0, bar 15. b1: {} -> fallback
  full-bucket exact gap 17 (gaps 34,34,-16 -> 52/3), bar 32.
  b2: {} -> fallback gap -2, bar 13. b3: {s5} gap +13 ->
  bar 28. PMWX bars sh=2: **(15,32,13,28)**.

V_PMNX (N = ceil(n/2) sealed cases nearest K=15, ties by lowest
sealed index):

- sh=0: b0: n=2,N=1: s1 (d15, gap 0) -> 0, bar 15.
  b1: n=6,N=3: s2,s4,s7 (d2, gaps -16) -> -16, bar -1.
  b2: n=1,N=1: s0 -> +13, bar 28.
  b3: n=3,N=2: s5,s6 (d9, gaps -9,-14) -> -11, bar 4.
  PMNX bars sh=0: **(15,-1,28,4)**.
- sh=1: b0: n=2,N=1: s1 -> 0, bar 15.
  b1: n=6,N=3: s2 (d2,-16), s10 (d6,-16), s3 (d19,-16) ->
  -16, bar -1. b2: n=1,N=1: s7 -> -2, bar 13.
  b3: n=3,N=2: s5 (d5,-10), s11 (d10,-15) -> -12, bar 3.
  PMNX bars sh=1: **(15,-1,13,3)**.
- sh=2: b0: n=7,N=4: s1,s2,s6,s7 (all gap 0) -> 0, bar 15.
  b1: n=3,N=2: s0,s4 (d19, gaps 34,34) -> 34, bar 49.
  b2: n=1,N=1: s3 -> -2, bar 13.
  b3: n=1,N=1: s5 -> +13, bar 28.
  PMNX bars sh=2: **(15,49,13,28)**.

## Frozen profit predictions (K=15; profit = sum over GO of (eff-15); GO iff score > bar, strict)

UCB x V_WK (bar 15; verbatim lineage control):

- sh=0: GO {2,3,4,5,7,9} (6). profit 75.
- sh=1: GO {0,2,3,4,5,6,7,8} (8). profit 128.
- sh=2: GO {0,4,11} (3). profit 55.
- Total: **258** (17 GO).

UCB x V_PBK (bars (15,4,3,12); verbatim bucket-mean comparator):

- sh=0: GO {0,2,3,4,5,7,9,10} (8). profit 70.
- sh=1: GO {0,2,3,4,5,6,7,8,10} (9). profit 138.
- sh=2: GO {0,4,5,11} (4). profit 40.
- Total: **248** (21 GO).

UCB x V_PMW (bars (15,15,3,12); KEY-1):

- sh=0: s0 b2 13>3 GO eff0 -15; s1 b0 0 no; s2 b1 17>15 GO
  eff33 +18; s3 b1 34>15 GO eff0 -15; s4 b1 17>15 GO eff33
  +18; s5 b3 24>12 GO eff33 +18; s6 b3 6 no; s7 b1 17>15 GO
  eff33 +18; s8 b0 0 no; s9 b1 17>15 GO eff33 +18; s10 b1 9
  no; s11 b3 2 no.
  GO {0,2,3,4,5,7,9} (7).
  profit = -15+18-15+18+18+18+18 = **60**.
- sh=1: s0 b3 30>12 GO eff10 -5; s1 b0 0 no; s2 b1 17>15 GO
  eff33 +18; s3 b1 34>15 GO eff50 +35; s4 b1 34>15 GO eff50
  +35; s5 b3 20>12 GO eff30 +15; s6 b1 34>15 GO eff0 -15;
  s7 b2 23>3 GO eff25 +10; s8 b1 34>15 GO eff50 +35; s9 b0 0
  no; s10 b1 9 no; s11 b3 5 no.
  GO {0,2,3,4,5,6,7,8} (8).
  profit = -5+18+35+35+15-15+10+35 = **128**.
- sh=2: s0 b1 34>15 GO eff0 -15; s1 b0 0 no; s2 b0 0 no;
  s3 b2 -2 no; s4 b1 34>15 GO eff0 -15; s5 b3 13>12 GO eff0
  -15; s6..s10 b0 0 no; s11 b1 84>15 GO eff100 +85.
  GO {0,4,5,11} (4).
  profit = -15-15-15+85 = **40**.
- Total: **228** (19 GO).

UCB x V_PMN (bars (15,8,3,10); KEY-2):

- sh=0: s0 b2 13>3 GO eff0 -15; s1 b0 0 no; s2 b1 17>8 GO
  eff33 +18; s3 b1 34>8 GO eff0 -15; s4 b1 17>8 GO eff33
  +18; s5 b3 24>10 GO eff33 +18; s6 b3 6 no; s7 b1 17>8 GO
  eff33 +18; s8 b0 0 no; s9 b1 17>8 GO eff33 +18; s10 b1
  9>8 GO eff25 +10; s11 b3 2 no.
  GO {0,2,3,4,5,7,9,10} (8).
  profit = -15+18-15+18+18+18+18+10 = **70**.
- sh=1: s0 b3 30>10 GO eff10 -5; s1 b0 0 no; s2 b1 17>8 GO
  eff33 +18; s3 b1 34>8 GO eff50 +35; s4 b1 34>8 GO eff50
  +35; s5 b3 20>10 GO eff30 +15; s6 b1 34>8 GO eff0 -15;
  s7 b2 23>3 GO eff25 +10; s8 b1 34>8 GO eff50 +35; s9 b0 0
  no; s10 b1 9>8 GO eff25 +10; s11 b3 5 no.
  GO {0,2,3,4,5,6,7,8,10} (9).
  profit = -5+18+35+35+15-15+10+35+10 = **138**.
- sh=2: s0 b1 34>8 GO eff0 -15; s1 b0 0 no; s2 b0 0 no;
  s3 b2 -2 no; s4 b1 34>8 GO eff0 -15; s5 b3 13>10 GO eff0
  -15; s6..s10 b0 0 no; s11 b1 84>8 GO eff100 +85.
  GO {0,4,5,11} (4).
  profit = -15-15-15+85 = **40**.
- Total: **248** (21 GO).

V_PMWX fenced diagnostic (bars above; arithmetic only):

- sh=0 (bars (15,-1,28,4)): s0 13>28 no; s1 0 no; s2 17>-1
  GO eff33 +18; s3 34>-1 GO eff0 -15; s4 17>-1 GO eff33
  +18; s5 24>4 GO eff33 +18; s6 6>4 GO eff20 +5; s7 17>-1 GO
  eff33 +18; s8 0 no; s9 17>-1 GO eff33 +18; s10 9>-1 GO
  eff25 +10; s11 2>4 no.
  GO {2,3,4,5,6,7,9,10} (8).
  profit = 18-15+18+18+5+18+18+10 = **90**.
- sh=1 (bars (15,-1,13,3)): s0 30>3 GO eff10 -5; s1 0 no;
  s2 17>-1 GO eff33 +18; s3 34>-1 GO eff50 +35; s4 34>-1 GO
  eff50 +35; s5 20>3 GO eff30 +15; s6 34>-1 GO eff0 -15;
  s7 23>13 GO eff25 +10; s8 34>-1 GO eff50 +35; s9 0 no;
  s10 9>-1 GO eff25 +10; s11 5>3 GO eff20 +5.
  GO {0,2,3,4,5,6,7,8,10,11} (10).
  profit = -5+18+35+35+15-15+10+35+10+5 = **143**.
- sh=2 (bars (15,32,13,28)): s0 34>32 GO eff0 -15; s4 34>32
  GO eff0 -15; s5 13>28 no; s11 84>32 GO eff100 +85; rest 0
  no.
  GO {0,4,11} (3).
  profit = -15-15+85 = **55**.
- Total: **288** (21 GO).

V_PMNX fenced diagnostic (bars above; arithmetic only):

- sh=0 (bars (15,-1,28,4)): identical to V_PMWX sh=0.
  GO {2,3,4,5,6,7,9,10} (8). profit **90**.
- sh=1 (bars (15,-1,13,3)): identical to V_PMWX sh=1.
  GO {0,2,3,4,5,6,7,8,10,11} (10). profit **143**.
- sh=2 (bars (15,49,13,28)): s0 34>49 no; s4 34>49 no;
  s5 13>28 no; s11 84>49 GO eff100 +85; rest 0 no.
  GO {11} (1). profit **85**.
- Total: **318** (19 GO).

Lineage reference:

- V_PBX (fenced per-bucket exact, recomputed verbatim):
  (90, 138, 55) = 283, GO (8,9,3).
- execute-all: (43, 113, -80) = 76.

WC-FINAL: 24 train + 78 GO (17 + 21 + 19 + 21; PMWX/PMNX/PBX
use zero world calls) + 36 reference = **138**.

## Frozen kill bars

- **K1 (diet / commit order / no-exact-signal / probe-proofness):
  PASS required.** A1: phase order train SETUP < train COMMIT <
  train PREFF < train CONSEQ < train LEARN < train BAR < sealed
  SETUP < sealed COMMIT < sealed BARS < sealed VERDICT (GO) <
  CONSEQUENCE (world_execute on GO) < REFERENCE < FENCED-PBX <
  FENCED-PMWX < FENCED-PMNX, by source line order (strict
  increase is the frozen property; the actual line numbers are
  recorded in the report). A2: zero `world_buf`/`world_off`
  tokens in learner fns (lc_blocked, lc_leg, learner_compose,
  gather_cells). A3: zero `expected|answer|key|target`
  (case-insensitive). A4: zero
  `correct|reference_plan|gold`. A5: `world_execute(` exactly 4
  occurrences (1 def + 3 call sites: train CONSEQ, the shared
  `conseq_arm` helper, REFERENCE). The PMWX/PMNX/PBX diagnostics
  use zero world_execute calls (pure arithmetic on the
  REFERENCE-filled buffer and stored adjucb). A6: WC-FINAL =
  138. A7: zero `learner_`/`belief_` calls after the
  CONSEQUENCE marker. A8: the token "oracle" (case-insensitive)
  appears zero times. A9 (the no-exact-signal bar): the token
  `Tpred` appears zero times. A10 (probe-proofness): the V_PMW
  and V_PMN bars are computed without reading any sealed
  bias-adjusted score -- bar_b = K + local_mcalib[b], with the
  local miscalibration train-fixed under the frozen structural
  marginality rules (W=10 window; N_b = ceil(n_b/2) nearest),
  and the bar selected by bkt_s (sealed, bias-free). The
  fenced probes of the lineage touch adjusted scores only,
  never bkt, so they cannot move either marginal bar. The
  PMWX/PMNX/PBX diagnostics are fenced (not learner bars) and
  read sealed eff only after REFERENCE; they do not affect any
  verdict.
- **K2 (determinism): PASS required.** 3/3 runs byte-identical
  stdout.
- **K3 (verbatim machinery + new quantities): PASS required.**
  BARS lines: ThyA = 13/20/6, ThyB = 13/20/13 @15/30/45; TFIXED
  = 12; CVAL = 15; ThyHKC = 15/20/15; mcalib = (0,-11,-12,-3);
  pbkbar = (15,4,3,12); pboptbar = (15,16,5,15). New:
  mwmcalib = (0,0,-12,-3); pmwbar = (15,15,3,12); mncalib =
  (0,-7,-12,-5); pmnbar = (15,8,3,10); UCB x V_WK =
  (75,128,55) = 258; UCB x V_PBK = (70,138,40) = 248;
  V_PBX = (90,138,55) = 283; execute-all = (43,113,-80)
  (in-program exact checks).
- **K4 (PRIMARY, preregistered NULL): PASS required.** UCB x
  V_PMW total = 228 < 258 AND UCB x V_PMN total = 248 < 258. No
  learner-computable marginal bar beats the fixed stakes bar.
  Locality does not repair the transfer defect: the
  train->sealed marginal gap shifts (b1 marginal: 0 train vs
  -16 sealed; b2 marginal: -12 train vs +13 sealed @15; b3
  marginal: -3 train vs +13 sealed @45) are not predictable
  from bucket identity plus train.
- **K5: PASS required.** Execute-all per-batch profit =
  (43, 113, -80).
- **K6: PASS required.** UCB x V_PMN total = 248 = UCB x V_PBK
  total. Mechanism: the differential bands between the marginal
  bars (15,8,3,10) and the bucket-mean bars (15,4,3,12) -- b1:
  (4,8], b3: (10,12] -- contain no sealed cases on these
  batches (b1: sealed adjs are 17/34/9, none in (4,8]; b3:
  sealed adjs are 24/6/2, 30/20/5, 13, none in (10,12]), so
  the GO sets coincide exactly.
- **K7: PASS required.** UCB x V_PMW total = 228 < 248 = UCB x
  V_PMN total. The W=10 window keeps only 2 train cases in b1
  (gaps -16 and +17), so the local estimate is 0 and the b1
  bar stays at 15, missing s10's +10 at @15 and @30 (-20). The
  N-nearest rule keeps 4 cases (adding two (34,50) cases with
  gap -16), giving -7 and bar 8, which takes s10. Fewer cases
  make the marginal estimate noisier, not more
  decision-relevant.
- **K8: PASS required.** WC-FINAL = 138 (in-program).
- **K9 (divergence): PASS required.** UCB x V_PMN total = 248 <
  UCB x V_WK total = 258. Marginal worth-K does NOT beat pure
  worth-K: the @15 loss (takes s0's -15 via the b2 bar 3) and
  the @45 loss (takes s5's -15 via the b3 bar 10) mirror the
  bucket-mean signal's failures, now at marginal resolution.
- **K10 (divergence): PASS required.** V_PMWX total = 288 > UCB
  x V_PMW total = 228 AND V_PMNX total = 318 > UCB x V_PMN
  total = 248. The exact marginal signal beats the learner
  marginal signal by 60/70, decomposed as: @15, the exact b1
  bar -1 takes s10's +10 and the exact b2 bar 28 avoids s0's
  -15 (30); @30, the exact b3 bar 3 takes s11's +5 (5);
  @45, the exact b1 bar 49 avoids s0/s4's -15s (30, PMNX).
  The marginal information is real -- the exact marginal
  bounds gain 30/60 over fixed-K -- but it lives below what
  train alone can supply.

**BUILD-PASS requires K1..K10.**

## Preregistered answers to the task's key questions

1. **Is marginal miscalibration more predictive than
   bucket-mean?** Predicted NO (K4/K6/K7): V_PMW totals 228 <
   248 = V_PBK, and V_PMN totals 248 = V_PBK with identical GO
   commitments (not better). Measuring miscalibration only on
   marginal cases does not improve on the bucket mean from
   train alone; the fixed-window version is strictly worse.
2. **Can we capture the decision-relevant information?**
   Predicted NO as a verdict input (K10): the exact marginal
   bounds (288/318) beat the learner marginal bars (228/248)
   by 60/70. The marginal information is real -- PMNX at @45
   avoids s0/s4's -15s through the exact local gap +34, and
   PMWX at @30 takes s11's +5 through the exact local gap -12
   -- but train->sealed marginal gap shifts (sign flips in b2
   @15 and b3 @45, level shift in b1) are not predictable from
   {train, bucket identity, K}. Locality does not fix the
   transfer problem.
3. **What is the right definition of "marginal"?** Predicted:
   of the two tested, the data-driven half-nearest rule (V_PMN)
   generalizes no worse than the bucket mean (identical
   commitments), while the fixed window W=10 (V_PMW)
   generalizes worse (228 < 248): with only 2 marginal train
   cases in b1, the local estimate is dominated by the single
   (17,0) train case that also made PBOPT overfit. Neither
   beats fixed-K (258). A two-stage definition (marginality
   relative to the stage-1 bar K + mcalib rather than K) is a
   named follow-up, not tested this wave.

## Determinism and honesty rules

- Integer arithmetic only. W=10 is a frozen structural
  mechanism parameter (like PLANMAX/EBUD), preregistered and
  never tuned; N_b = ceil(n_b/2) is data-driven with no
  magnitude constant. The learner computes all miscalibration
  quantities from train data.
- No post-prereg probe of any kind. All predictions above are
  arithmetic on the committed tables.
- The tokens `Tpred`, `oracle`, `expected`, `answer`, `key`,
  `target`, `correct`, `reference_plan`, `gold` do not appear in
  the implementation source (K1 A3/A4/A8/A9).
- If any arm differs from prediction in either direction, report
  the exact mechanism. No bar moves after seeing results.
