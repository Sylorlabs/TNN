# PREREG.md -- IVWC-LEARNEREVAL: learner-owned evaluation

## Wave

Follow-up from IVWC-KSENSITIVITY (BUILD-PASS KS1-KS7). The worth-K arc is
complete: fixed-K (258) is the robust optimum; no learner-computable
adjustment beats it. Every wave so far evaluated the learner the same way:
the harness scored GO/NO-GO commitments against `eff` (expected answers)
and reported profit. The learner never evaluated itself. This wave builds
**learner-owned evaluation**, the first mechanism for Micah's Priority #4
(internal verification: reduce dependence on harness expected answers;
prefer learner commitment, world consequence, learner-owned evaluation).

Non-ledger task. Lane `ivwc_learnereval/`. Pure Zag, safebin, 3/3
byte-identical. Commits local on `tnn-native-lab` via explicit pathspec
plumbing. Push note: do NOT push via `gh_push_api.py` (known HTTP 403);
document the blockage for the parent.

## Operational definition of "learner-owned evaluation"

Evaluation is currently a harness operation: compare the learner's GO sets
against the world's `eff` table (expected answers) and report profit. A
learner-owned evaluation must satisfy three constraints:

1. **No expected-answer oracle.** The evaluation computation never reads
   `eff`/`teff`, never compares against a label, never touches a sealed
   bias-adjusted score before commitment. (K1 A3/A4/A8/A9/A10.)
2. **Commitment + consequence.** The learner commits to a self-assessment
   *before* acting (prospective: a prediction of its own performance,
   formed from train experience alone), then acts, then experiences
   consequences. The retrospective self-assessment is a function of its
   *experienced* sealed nets only (the consequence interface: reward minus
   charge as one number per executed case, exactly as train `tnet` was
   experienced in IVWC-LEARNERK). The harness never hands it "answers";
   its own experienced outcomes ARE the evaluation.
3. **Falsifiable calibration.** The self-assessment must be checkable
   against harness evaluation (correlation test) and must be capable of
   detecting the learner's own errors (self-error flag) -- both
   preregistered as kill bars, including a preregistered NULL.

## Design

World / belief / composer / stepper / seeds / biases / UCB tables /
verdict bars / consequence machinery are verbatim from IVWC-LEARNERK
(K3 re-verifies). Three verdicts: UCB x V_WK (bar 15, given), UCB x V_LOK
(bar 14, owned), UCB x V_LOKB (bars (0,16,5,9), owned per bucket).
New mechanism, all learner-side:

**SE1 -- Prospective self-evaluation (learner, train-only).** Before any
sealed case, the learner commits to a self-estimate of each verdict's
sealed profit, computed from train experience alone (tnet, tadj, tbkt):

- Naive: `SEST_NAIVE[v] = P(bar_v)` = sum of train `tnet` over train cases
  with `tadj > bar_v` (per-bucket sum for V_LOKB). The "would-have-earned"
  train profit: the learner's best honest estimate of sealed performance
  from experience alone.
- Fragility-penalized: `SEST_PEN[v] = P(bar_v) - PEN(bar_v)`, where
  `PEN(bar)` = sum of `|tnet|` over train cases with `|tadj - bar| <= 1`
  (knife-edge profit-at-risk: the experienced profit sitting within one
  unit of the decision boundary). Integer arithmetic, no division.
- Self-error flag: `FLAG[v] = 1` iff `2*PEN(bar_v) > P(bar_v)` and
  `P(bar_v) > 0` (relative rule: the knife-edge profit-at-risk exceeds
  half the estimated profit; no magnitude constant, no world parameter).

**SE2 -- Retrospective self-evaluation (learner, post-consequence).** After
each batch's consequences, the harness reports experienced sealed nets
per executed case (`snet[s] = se - EXCOST` for GO cases, 0 otherwise --
the consequence interface, filled harness-side from the already-executed
world calls, zero new world calls). The learner's retrospective module
sums its experienced nets per arm: `SE_RETRO[v]`. This reads no `eff`,
no label, no expected answer: it is the learner totaling what it lived
through. Structural identity with harness profit is the test (K4).

**SE3 -- Correlation test (harness-printed, learner-committed).** The
program prints the learner's prospective estimates, flags, and
retrospective self-evaluations alongside the harness profits. Kill bars
test: (a) whether the retrospective self-evaluation matches harness
profit exactly (K4); (b) whether the naive prospective estimate is
calibrated (K5, preregistered NULL: it is not); (c) whether the
fragility-penalized estimate discriminates the known overfit (K6);
(d) whether the self-error flag fires exactly on the failing verdict
(K7).

The D1b/D2b probe arms are not re-run (unchanged from LEARNERK). The
execute-all fenced reference is re-run (K3/K5 lineage anchor).

## Background facts (from committed tables, not probed)

Train (t, bkt, adj, net=eff-15), from the IVWC-LEARNERK PREREG
(24/24 TAUDIT lines re-verified byte-identical by K3):

- b0 (7): adj 0 x7, nets -15 x7.
- b1 (7): (adj,net): (34,35)x4, (17,18), (17,-15), (84,85).
- b2 (7): (-9,-9), (23,10), (-10,-15), (6,18), (15,27), (6,-15), (0,-6).
- b3 (3): (5,-10), (7,1), (9,-4).

Sealed harness profits (verbatim lineage, K3): UCB x V_WK = (75,128,55)
= 258; UCB x V_LOK = (75,128,55) = 258; UCB x V_LOKB = (60,128,40) =
228; execute-all = (43,113,-80) = 76.

## Frozen derivations (arithmetic on the committed tables)

**Naive prospective self-estimates** (train P at each verdict's bar):

- V_WK (bar 15): adj>15: b1: 35*4+18-15+85 = 228; b2: 10 (adj 23);
  b3: 0. **SEST_NAIVE = 238.**
- V_LOK (bar 14): adj>14: b1: 228; b2: 27 (adj 15) + 10 (adj 23) = 37.
  **SEST_NAIVE = 265.**
- V_LOKB (bars (0,16,5,9)): b0: adj>0: none -> 0; b1: adj>16:
  18-15+140+85 = 228; b2: adj>5: 18-15+27+10 = 40; b3: adj>9: none
  -> 0. **SEST_NAIVE = 268.**

Naive ranking: V_LOKB (268) > V_LOK (265) > V_WK (238). Harness sealed
ranking: V_WK = V_LOK (258) > V_LOKB (228). The naive self-estimate is
*inverted*: the overfitter looks best to itself. This is the preregistered
NULL (K5): train-fit self-evaluation misleads, which is exactly why
harness evaluation seemed necessary.

**Knife-edge penalties** (sum of |tnet| over train cases with
|tadj - bar| <= 1):

- V_WK (15): adj in {14,15,16}: b2 adj 15 (net 27) -> **PEN = 27**.
- V_LOK (14): adj in {13,14,15}: b2 adj 15 (net 27) -> **PEN = 27**.
- V_LOKB: b0 bar 0: adj in {-1,0,1}: 7 x adj 0 (nets -15) -> 105;
  b1 bar 16: adj in {15,16,17}: 2 x adj 17 (nets 18,-15) -> 33;
  b2 bar 5: adj in {4,5,6}: 2 x adj 6 (nets 18,-15) -> 33;
  b3 bar 9: adj in {8,9,10}: 1 x adj 9 (net -4) -> 4.
  **PEN = 175.**

**Penalized self-estimates** (P - PEN):

- V_WK: 238 - 27 = **211**. V_LOK: 265 - 27 = **238**.
  V_LOKB: 268 - 175 = **93.**

Penalized ranking: V_LOK (238) > V_WK (211) > V_LOKB (93). The overfitter
is strictly below both global verdicts, matching the harness ordering's
essential discrimination (global bars above per-bucket), up to the
V_LOK/V_WK tie which the estimate resolves as strict (238 > 211) while
the harness ties (258 = 258). Self-evaluation is a coarse instrument:
it detects the failure but does not resolve near-ties (reported, not
hidden).

**Self-error flags** (1 iff 2*PEN > P and P > 0):

- V_WK: 2*27 = 54 > 238? No -> **0**.
- V_LOK: 54 > 265? No -> **0**.
- V_LOKB: 2*175 = 350 > 268? Yes -> **1.**

The flag fires exactly on the verdict that seals worst, from train data
alone, with no oracle.

**Retrospective self-evaluations** (experienced sealed nets per arm):
identical by construction to harness profits: V_WK = 258, V_LOK = 258,
V_LOKB = 228 (per-batch: (75,128,55), (75,128,55), (60,128,40)).

WC-FINAL: 24 train + 53 GO (17 + 17 + 19; snet recording adds zero world
calls) + 36 reference = **113**.

## Frozen kill bars

- **K1 (diet / commit order / no-oracle / self-eval ownership): PASS
  required.** A1: phase order train SETUP < train COMMIT < train PREFF <
  train CONSEQ < train LEARN < train TNET < train LOKBARS < train
  SELFEVAL < sealed SETUP < sealed COMMIT < sealed BARS < sealed VERDICT
  < CONSEQUENCE < SELFREPORT < REFERENCE, by source line order (strict
  increase is the frozen property; actual line numbers recorded in the
  report). A2: zero `world_buf`/`world_off` tokens in learner fns
  (lc_blocked, lc_leg, learner_compose, gather_cells, lok_global,
  lok_bucket, se_p, se_pen, se_ppb, se_ppenb, se_retro). A3: zero
  `expected|answer|key|target` (case-insensitive). A4: zero
  `correct|reference_plan|gold`. A5: `world_execute(` exactly 4
  occurrences (1 def + 3 call sites: train CONSEQ, conseq_arm,
  REFERENCE). A6: WC-FINAL = 113. A7: zero `learner_`/`belief_` calls
  after the SELFREPORT marker line (only fenced REFERENCE world calls
  remain). A8: the token "oracle" (case-insensitive) appears zero times.
  A9: the token `Tpred` appears zero times. A10 (self-eval ownership):
  the prospective self-eval functions (se_p, se_pen, se_ppb, se_ppenb)
  read only train buffers (tadj, tnet, tbkt) and the bars -- zero
  `teff` tokens in their bodies, zero reads of any sealed quantity;
  the retrospective function (se_retro) reads only `snet` (experienced
  sealed nets) and `go` -- zero `eff`/`teff` in its body. The snet
  buffers are filled harness-side inside CONSEQUENCE from the
  already-executed world calls (the consequence interface).
- **K2 (determinism): PASS required.** 3/3 runs byte-identical stdout.
- **K3 (verbatim machinery + new): PASS required.** BARS lines: ThyA =
  13/20/6, ThyB = 13/20/13 @15/30/45; TFIXED = 12; CVAL = 15; ThyHKC =
  15/20/15; bucb = (0,16,27,20); mcalib = (0,-11,-12,-3); pbkbar =
  (15,4,3,12); pboptbar = (15,16,5,15); lokbar = 14; lokbbar =
  (0,16,5,9); UCB x V_WK = (75,128,55) = 258; UCB x V_LOK =
  (75,128,55) = 258; UCB x V_LOKB = (60,128,40) = 228; execute-all =
  (43,113,-80). New (in-program exact checks): SEST_NAIVE =
  (238,265,268); SEST_PEN = (211,238,93); FLAG = (0,0,1);
  SE_RETRO totals = (258,258,228).
- **K4 (PRIMARY): PASS required.** Retrospective self-evaluation equals
  harness profit per arm exactly: se_wk_tot == tot_uwk (258),
  se_lok_tot == tot_ulok (258), se_lokb_tot == tot_ulokb (228)
  (in-program equality). The learner evaluates itself from experience
  with no expected-answer oracle.
- **K5 (PRIMARY, preregistered NULL): PASS required.** Naive prospective
  self-evaluation is anti-calibrated: (sest_lokb > sest_lok) AND
  (sest_lok > sest_wk) AND (tot_ulokb < tot_ulok) -- i.e. 268 > 265 >
  238 while 228 < 258 (in-program). Train-fit self-evaluation ranks the
  overfitter first.
- **K6: PASS required.** Fragility-penalized self-evaluation
  discriminates the overfit: (sest_pen_lokb < sest_pen_wk) AND
  (sest_pen_lokb < sest_pen_lok) -- i.e. 93 < 211 and 93 < 238
  (in-program). The penalized estimate puts the failing verdict
  strictly below both global verdicts, matching the harness ordering's
  global-above-per-bucket discrimination.
- **K7: PASS required.** The self-error flag fires exactly on the
  failing verdict: flag_wk == 0 AND flag_lok == 0 AND flag_lokb == 1
  (in-program).
- **K8: PASS required.** WC-FINAL = 113 (in-program).

**BUILD-PASS requires K1..K8.**

## Preregistered answers to the task's key questions

1. **What does "learner-owned evaluation" mean operationally?**
   Commitment + consequence: the learner commits to a self-assessment
   (prospective estimates and an error flag) from train experience alone
   before acting, then evaluates itself retrospectively from its
   experienced sealed nets. No expected-answer comparison anywhere in
   the learner's computation (K1-A10).
2. **Can the learner evaluate itself accurately?** Predicted: YES
   retrospectively (K4: experienced nets = profit exactly, no oracle),
   NO naively-prospectively (K5 NULL: train-fit self-estimates invert the
   true ranking), YES for error detection (K7: the fragility flag fires
   exactly on the failing verdict from train alone).
3. **Does self-evaluation correlate with harness evaluation?**
   Predicted: retrospective -- perfect (identity); naive prospective --
   anti-correlated (inverted ranking); penalized prospective --
   discriminates the failure (overfitter strictly below both globals)
   but resolves the V_LOK/V_WK tie as strict where the harness ties.
4. **Is this the right next step for Priority #4?** Predicted: partially.
   It replaces expected-answer comparison with commitment + consequence
   + fragility self-assessment, and the retrospective channel is exact.
   But the fragility rule (knife-edge +/-1, flag at 2*PEN > P) was
   designed with the committed tables in hand: one world, one axis. It
   demonstrates that an oracle-free fragility signal CAN detect the
   known overfit; it does not establish the rule generalizes.

## L2 vs L3 assessment (preregistered)

Learner-owned evaluation as built here is **L1 (parameter learning) with
an L2 flavor**, not L3. The self-evaluation *forms* (train-profit
estimate, knife-edge penalty, relative flag rule, experienced-net
retrospection) are researcher-given; the learner fills the *values*
from its experience (L1). The L2 flavor: evaluation itself -- previously
a harness operation comparing against expected answers -- becomes a
learner-executed computation over its own commitments and experienced
consequences. Not L3 by a wide margin: no new representation,
abstraction, or procedure is invented; the evaluation forms are
researcher-enumerated; Criterion 0 fails (the source holds the complete
evaluation machinery).

## Determinism and honesty rules

- Integer arithmetic only. The knife-edge window (+/-1) and the flag
  rule (2*PEN > P, P > 0) are preregistered structural rules, never
  tuned; their load-bearing nature (designed with the tables in hand)
  is disclosed above as a caveat, not a generalization claim.
- No post-prereg probe of any kind. All predictions above are arithmetic
  on the committed tables.
- The tokens `Tpred`, `oracle`, `expected`, `answer`, `key`, `target`,
  `correct`, `reference_plan`, `gold` do not appear in the implementation
  source (K1 A3/A4/A8/A9). The prospective self-eval functions
  additionally avoid `teff`; se_retro avoids `eff`/`teff` (K1 A10).
- If any arm differs from prediction in either direction, report the
  exact mechanism. No bar moves after seeing results.
