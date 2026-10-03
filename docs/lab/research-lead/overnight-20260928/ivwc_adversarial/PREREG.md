# PREREG.md -- IVWC-ADVERSARIAL: sealed adversarial worlds testing the fragility signal

## Wave

Follow-up from IVWC-LEARNEREVAL (BUILD-PASS K1-K8). LEARNEREVAL showed a
learner can evaluate itself without an expected-answer oracle, and that a
knife-edge fragility penalty (PEN = sum of |tnet| over train cases with
|tadj - bar| <= 1; self-error flag iff 2*PEN > P) detects the known
overfit on the one committed world (93 < 211, 93 < 238; flag exactly on
V_LOKB). The report's honest caveat: the fragility rule was
researcher-designed with the committed tables in hand (one world, one
wall-density law-change axis). It demonstrates an oracle-free fragility
signal CAN detect the known overfit; it does not establish the rule
generalizes. The named next frontier: "a learner-owned fragility notion
that is not researcher-designed, or sealed adversarial worlds that test
this one."

This wave builds the sealed adversarial worlds. Non-ledger task. Lane
`ivwc_adversarial/`. Pure Zag, safebin, 3/3 byte-identical. Commits local
on `tnn-native-lab` via explicit pathspecs. Push note: do NOT push via
`gh_push_api.py` (known HTTP 403); document the blockage for the parent.

## The frozen rule under test

Verbatim from IVWC-LEARNEREVAL, frozen, not to be tuned to the new
worlds. Any tuning would require a fresh preregistration.

- SEST_NAIVE[v] = P(bar_v) = sum of train tnet over train cases with
  tadj > bar_v (per-bucket sum for V_LOKB).
- PEN(bar) = sum of |tnet| over train cases with |tadj - bar| <= 1
  (per-bucket for V_LOKB).
- SEST_PEN[v] = P(bar_v) - PEN(bar_v).
- FLAG[v] = 1 iff 2*PEN(bar_v) > P(bar_v) and P(bar_v) > 0.
- GO rule on sealed: GO = 1 iff sadj > bar (per-bucket bars for V_LOKB).
- Harness profit = sum of sealed snet over the verdict's GO set.
- SE_RETRO[v] = sum of experienced sealed nets (snet) over the verdict's
  GO set (consequence interface; structural identity with harness profit).

## Adversarial design (post-freeze, independent-adversary mindset)

The adversary's job is to break the frozen rule. Four worlds, each a
committed train table plus a committed sealed table with a stated
law-change story. The seal is methodological: every table and every
prediction below is committed here before the implementation is written,
and the diet audit (K1-A10) proves the learner-side self-evaluation
functions never read sealed quantities. The object under test is the
fragility signal, not world generation, so worlds are committed tables;
there is no world stepper and no world_execute calls (WC-FINAL = 0,
preregistered).

Verdict characters mirror the lineage: V_WK (given conservative global
bar), V_LOK (learned global bar), V_LOKB (learned per-bucket bars, the
overfit candidate).

### ADV-A: "sparse-boundary overfit" -- false negative via adj shift

Story: the per-bucket learner fit its bars to the richest train cells;
every bar sits in a sparse train region (PEN = 0). The sealed law change
shifts the adj distribution: the rich high-adj cells the overfitter
targeted collapse to losses, while mid-adj cells (where the global bars
earn) survive. Train density near the boundary says "robust"; the sealed
regime change says otherwise.

Train (16 cases; bkt, adj, net):

- b0 (4): (0,-15) x2, (50,40) x2
- b1 (4): (34,35) x2, (17,18), (17,-15)
- b2 (4): (23,10), (15,27), (6,18), (6,-15)
- b3 (4): (5,-10), (7,1), (9,-4), (60,50)

Bars: V_WK 15; V_LOK 14; V_LOKB (45,30,20,55).

Frozen derivations:

- SEST_NAIVE. V_WK (adj>15): b0 40x2=80; b1 35x2=70; b2 10 (adj 23;
  adj 15 excluded); b3 50. Total 210. V_LOK (adj>14): b0 80; b1 70;
  b2 10+27=37; b3 50. Total 237. V_LOKB: b0 adj>45: 80; b1 adj>30: 70;
  b2 adj>20: 10; b3 adj>55: 50. Total 210.
- PEN. V_WK (15): adj in {14,15,16}: b2 (15,27) -> 27. V_LOK (14): adj
  in {13,14,15}: b2 (15,27) -> 27. V_LOKB: b0 bar 45: {44,45,46}: none;
  b1 bar 30: {29,30,31}: none; b2 bar 20: {19,20,21}: none; b3 bar 55:
  {54,55,56}: none. PEN = 0.
- SEST_PEN: V_WK 210-27=183; V_LOK 237-27=210; V_LOKB 210-0=210.
- FLAG (2*PEN > P): V_WK 54>210 no -> 0; V_LOK 54>237 no -> 0;
  V_LOKB 0>210 no -> 0.

Sealed (16 cases):

- b0 (4): (52,-20) x2, (20,25), (25,30)
- b1 (4): (36,-25) x2, (20,30), (25,35)
- b2 (4): (25,-12), (16,20), (18,22), (6,18)
- b3 (4): (62,-30), (20,35), (25,40), (7,1)

Harness profits (GO iff sadj > bar):

- V_WK (15): b0 -20-20+25+30=15; b1 -25-25+30+35=15; b2 -12+20+22=30;
  b3 -30+35+40=45. Total 105.
- V_LOK (14): identical GO sets (no sealed adj in {15}... all GO adjs
  >= 16). Total 105.
- V_LOKB (45,30,20,55): b0 52,52 -> -40; b1 36,36 -> -50; b2 25 -> -12;
  b3 62 -> -30. Total -132.

SE_RETRO: (105, 105, -132), identical by construction.

Falsification F1 (preregistered): harness LOKB (-132) is strictly below
both globals (105, 105), yet FLAG_LOKB = 0 and SEST_PEN_LOKB (210) is
tied-best with SEST_PEN_LOK (210) and above SEST_PEN_WK (183). The
frozen rule misses a catastrophic failure completely: no flag, and the
failing verdict ranks tied-first prospectively.

### ADV-B: "dense but sound" -- false positive

Story: the learned global bar sits inside a dense train cluster (high
PEN), but the sealed law is unchanged there. The verdict is the best
sealed performer; the rule flags it as fragile anyway.

Train (16 cases):

- b0 (4): (14,20) x2, (15,-5), (30,40)
- b1 (4): (14,25) x2, (15,-8), (30,45)
- b2 (4): (14,18) x2, (15,-6), (30,38)
- b3 (4): (14,22) x2, (15,-7), (30,42)

Bars: V_WK 20; V_LOK 14; V_LOKB (20,20,20,20).

Frozen derivations:

- SEST_NAIVE. V_WK (adj>20): 40+45+38+42=165. V_LOK (adj>14):
  b0 -5+40=35; b1 -8+45=37; b2 -6+38=32; b3 -7+42=35. Total 139.
  V_LOKB (adj>20 per bucket): 165.
- PEN. V_WK (20): {19,20,21}: none -> 0. V_LOK (14): {13,14,15}:
  b0 20+20+5=45; b1 25+25+8=58; b2 18+18+6=42; b3 22+22+7=51.
  Total 196. V_LOKB: {19,20,21}: none -> 0.
- SEST_PEN: V_WK 165; V_LOK 139-196=-57; V_LOKB 165.
- FLAG: V_WK 0>165 no -> 0; V_LOK 2*196=392>139 yes -> 1;
  V_LOKB 0 -> 0.

Sealed (12 cases; same distribution as train, fresh draws):

- b0 (3): (14,20), (15,-5), (30,40)
- b1 (3): (14,25), (15,-8), (30,45)
- b2 (3): (14,18), (15,-6), (30,38)
- b3 (3): (14,22), (15,-7), (30,42)

Harness profits:

- V_WK (20): 165. V_LOK (14): b0 20-5+40=55; b1 25-8+45=62;
  b2 18-6+38=50; b3 22-7+42=57. Total 224. V_LOKB (20): 165.

SE_RETRO: (165, 224, 165).

Falsification F2 (preregistered): FLAG_LOK = 1 while harness LOK (224)
is the strictly best verdict (224 > 165 = 165). The frozen rule
false-flags the best performer and ranks it worst prospectively (-57).

### ADV-C: "payoff shift" -- structural blind spot (PEN = 0)

Story: the per-bucket overfitter concentrates GO on the single richest
train cell per bucket; its bars sit in completely empty regions
(PEN = 0 exactly, maximally "robust" by the rule). The sealed law change
alters payoffs, not positions: the same adjs, but the rich cells' nets
flip sign. Train density near the boundary is zero, so the rule is
maximally confident while the verdict loses everything.

Train (12 cases):

- b0..b3 (3 each): (10,30), (40,60), (70,80)

Bars: V_WK 5; V_LOK 35; V_LOKB (65,65,65,65).

Frozen derivations:

- SEST_NAIVE. V_WK (adj>5): 4*(30+60+80)=680. V_LOK (adj>35):
  4*(60+80)=560. V_LOKB (adj>65 per bucket): 4*80=320.
- PEN. V_WK (5): {4,5,6}: none -> 0. V_LOK (35): {34,35,36}: none -> 0.
  V_LOKB (65): {64,65,66}: none -> 0.
- SEST_PEN: (680, 560, 320). FLAG: (0,0,0).

Sealed (12 cases; identical adjs, flipped rich-cell payoffs):

- b0..b3 (3 each): (10,30), (40,60), (70,-50)

Harness profits:

- V_WK (5): 4*(30+60-50)=160. V_LOK (35): 4*(60-50)=40.
  V_LOKB (65): 4*(-50)=-200.

SE_RETRO: (160, 40, -200).

Falsification F3 (preregistered): PEN_LOKB = 0 exactly, FLAG_LOKB = 0,
yet harness LOKB = -200 < 0. The knife-edge density notion is
structurally blind to payoff-shift failure: it measures where train
cases sit relative to the boundary, not whether sealed payoffs in the
GO region resemble train payoffs.

### ADV-D: "clean world" -- specificity control

Story: no law change; sealed is a fresh draw from the train
distribution. The per-bucket learner converged to the global bars (no
overfit). Tests whether the frozen rule stays quiet and ranks sanely
when nothing is wrong.

Train (12 cases):

- b0..b3 (3 each): (20,25), (30,35), (40,-10)

Bars: V_WK 15; V_LOK 25; V_LOKB (25,25,25,25).

Frozen derivations:

- SEST_NAIVE. V_WK (adj>15): 4*(25+35-10)=200. V_LOK (adj>25):
  4*(35-10)=100. V_LOKB: 100.
- PEN: all zero (no train adj in {14,15,16} or {24,25,26}).
- SEST_PEN: (200, 100, 100). FLAG: (0,0,0).

Sealed (12 cases):

- b0..b3 (3 each): (20,22), (30,38), (40,-12)

Harness profits: V_WK 4*(22+38-12)=192; V_LOK 4*(38-12)=104;
V_LOKB 104.

SE_RETRO: (192, 104, 104).

Control F4 (preregistered): all flags 0, and the SEST_PEN ranking
(200 > 100 = 100) matches the harness ranking (192 > 104 = 104). The
rule is well-behaved when nothing is wrong; its failures are about
scope, not total invalidity.

## Secondary: alternative fragility notion (contested profit)

To test whether the fragility IDEA transfers across researcher designs
(even though the specific knife-edge rule does not), the wave also
implements a second, differently-designed fragility signal, computed
learner-side from train experience alone with no sealed reads:

- CPF_W[v] = sum of max(0, tnet) over the verdict's train GO set;
  CPF_L[v] = sum of max(0, -tnet) over the verdict's train GO set.
  (Outcome heterogeneity inside the accepted set: how much of the GO
  profit came with accompanying losses. No distance window, no boundary
  density, no perturbation.)
- CPF_FLAG1[v] = 1 iff CPF_W[v] > 0 and 2*CPF_L[v] > CPF_W[v]
  (relative rule; no magnitude constant, no world parameter).

Frozen derivations:

- ADV-A: V_WK (W210,L0)->0; V_LOK (W237,L0)->0; V_LOKB (W210,L0)->0.
  The train GO sets contain no losers; contested profit is quiet.
- ADV-B: V_WK (W165,L0)->0; V_LOK: W=40+45+38+42=165, L=5+8+6+7=26;
  2*26=52>165? No -> 0; V_LOKB (W165,L0)->0. Quiet where the
  knife-edge rule false-flags.
- ADV-C: (W680,L0)->0; (W560,L0)->0; (W320,L0)->0. Quiet.
- ADV-D: V_WK: W=4*60=240, L=4*10=40; 80>240? No -> 0. V_LOK:
  W=4*35=140, L=40; 80>140? No -> 0. V_LOKB: same -> 0. Quiet.

Transfer predictions (preregistered): the contested-profit signal avoids
ADV-B's false positive (S-K2) but shares the blind spot on ADV-A and
ADV-C (S-K1, S-K3): both researcher-designed fragility notions miss
sealed-regime-change failures. Neither generalizes; they trade blind
spots. This is reported as a finding, not a failure of the wave.

## Frozen kill bars

- **ADV-K1 (diet / commit order / no-oracle / self-eval ownership): PASS
  required.** A1: phase order per world train SELFEVAL < sealed
  CONSEQUENCE < SELFREPORT, by source line order (strict increase is the
  frozen property; actual line numbers recorded in the report). A2: zero
  `world_buf`/`world_off` tokens in learner fns (se_p, se_pen, se_ppb,
  se_ppenb, se_cpfw, se_cpfl, se_retro); there is no world stepper in
  this wave. A3: zero `expected|answer|key|target` (case-insensitive).
  A4: zero `correct|reference_plan|gold`. A5: `world_execute(` zero
  occurrences (worlds are committed tables; the seal is the prereg
  commitment plus A10). A6: WC-FINAL = 0. A7: zero `learner_`/`belief_`
  calls after the SELFREPORT marker line. A8: zero `oracle`
  (case-insensitive). A9: zero `Tpred`. A10 (self-eval ownership): the
  prospective self-eval functions read only train buffers (tadj, tnet,
  tbkt) and the bars: zero `teff` tokens in their bodies, zero
  `sealed_adj`/`sealed_net`/`sadj`/`snet` tokens in their bodies; the
  retrospective function (se_retro) reads only `snet` (experienced
  sealed nets) and `go`. The snet buffers are filled harness-side inside
  CONSEQUENCE from the committed sealed tables (the consequence
  interface); the learner never reads a sealed table directly.
- **ADV-K2 (determinism): PASS required.** 3/3 runs byte-identical
  stdout.
- **ADV-K3 (frozen predictions): PASS required.** Every number in the
  Frozen derivations sections is reproduced exactly in-program
  (in-program exact-equality flags per world: k3a..k3d).
- **ADV-K4 (retrospective identity): PASS required.** SE_RETRO == harness
  profit for all 12 (world, verdict) pairs (in-program).
- **ADV-K5 (F1, PRIMARY): PASS required.** ADV-A: (h_lokb < h_wk) AND
  (h_lokb < h_lok) AND (flag_lokb == 0) AND (pp_lokb >= pp_wk), i.e.
  -132 < 105, -132 < 105, flag 0, 210 >= 183 (in-program). The frozen
  rule misses the catastrophic failure: no flag, failing verdict ranked
  tied-best prospectively.
- **ADV-K6 (F2): PASS required.** ADV-B: (flag_lok == 1) AND
  (h_lok > h_wk) AND (h_lok > h_lokb), i.e. flag 1 with 224 > 165, 165
  (in-program). The frozen rule false-flags the best verdict.
- **ADV-K7 (F3): PASS required.** ADV-C: (pen_lokb == 0) AND
  (h_lokb < 0) AND (flag_lokb == 0), i.e. 0, -200 < 0, flag 0
  (in-program). The density notion is structurally blind to payoff
  shift.
- **ADV-K8 (F4, control): PASS required.** ADV-D: all knife-edge flags
  0 AND (pp_wk > pp_lok) AND (pp_lok == pp_lokb) AND (h_wk > h_lok) AND
  (h_lok == h_lokb), i.e. ranking agreement 200>100=100 vs 192>104=104
  (in-program).
- **S-K1: PASS required.** Contested-profit flags on ADV-A are (0,0,0)
  (in-program): the alternative notion shares the blind spot.
- **S-K2: PASS required.** Contested-profit flags on ADV-B are (0,0,0)
  while knife-edge FLAG_LOK = 1 (in-program): the notions disagree
  exactly as preregistered; the alternative avoids the false positive.
- **S-K3: PASS required.** Contested-profit flags on ADV-C and ADV-D are
  (0,0,0) (in-program).

**BUILD-PASS requires ADV-K1 through ADV-K8 and S-K1 through S-K3.**

## Preregistered answers to the task's key questions

1. **Does the researcher-designed fragility rule generalize?** Predicted:
   NO. It misses catastrophic failures caused by sealed regime change
   (ADV-A adj shift, ADV-C payoff shift) and false-flags a sound verdict
   whose bar sits in a dense train region (ADV-B). It is well-behaved
   only on the clean control (ADV-D) and on the single world/axis it was
   designed against.
2. **Can fragility be learner-owned?** Predicted: not demonstrated here.
   The contested-profit signal is an alternative researcher-designed
   FORM whose values are learner-filled (L1 with L2 flavor, same as
   LEARNEREVAL's own assessment). A truly learner-owned fragility notion
   (learner invents the form from experience) remains the open frontier.
   The viable path this battery suggests: prospective fragility from
   train alone is structurally blind to sealed regime change, so the
   robust Priority #4 channel is retrospective consequence plus
   learner-updated calibration across worlds (cross-world learned
   discount), to be preregistered as a separate wave.
3. **What would falsify the fragility approach?** This battery IS the
   falsification test, preregistered: ADV-K5/K6/K7 PASS means the
   specific knife-edge rule is falsified as a general fragility notion
   (it fails exactly as predicted on three of four adversarial worlds).
   What would falsify the broader approach (oracle-free self-evaluation
   itself): ADV-K4 failing (retrospective identity breaking), or the
   control ADV-K8 failing (rule misbehaving with no law change).

## L2 vs L3 assessment (preregistered)

This wave is mechanism-testing, not a capability claim: it adversarially
evaluates an L1 mechanism (the knife-edge rule) and an alternative L1
form (contested profit). No L2/L3 claim is made. The battery's value is
negative information: it maps the exact boundary where train-only
prospective fragility stops working, which is what the next mechanism
must survive.

## Determinism and honesty rules

- Integer arithmetic only. The knife-edge window (+/-1) and both flag
  rules are frozen structural rules, never tuned to fit.
- The adversarial worlds were designed AFTER the LEARNEREVAL freeze with
  the explicit goal of breaking the frozen rule. The implementer and the
  adversary are the same worker; mitigation: the rule is frozen verbatim
  (no tuning), all tables and predictions are committed here before any
  implementation, and the report discusses the dual-role limitation and
  what a truly independent adversary would add.
- No post-prereg probing of any kind. Predictions are arithmetic on the
  committed tables above.
- 3/3 byte-identical runs required; stdout bytes verified against the
  hand computations above beyond the in-program flags, per the toolchain
  lesson on trusting binary output.
