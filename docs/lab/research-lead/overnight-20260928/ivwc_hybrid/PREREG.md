# PREREG.md -- IVWC-HYBRID: internal prediction + consequence training

Frozen: 2026-10-03. This document fixes the experimental design and
the kill bars K1..K9. It must be committed ALONE (with NAMECHECK.md,
no implementation) before any implementation work. The prereg commit
must strictly precede the implementation commit. Amending a bar after
results invalidates the verdict.

## 1. What this wave is

IVWC-EXPAND3 (consequence-trained bucket verifier) and
IVWC-ORACLE-FREE (zero-observation internal-model verifier) exhibit
a clean dissociation on the same sealed setups (bit-identical
sealed (bucket, eff) pairs):

- wp=15 (in-distribution): oracle-free 10/12 > expand3 9/12.
  The internal prediction (predicted eff from `belief_execute`)
  is a finer signal than the coarse bucket bins: e.g. s=5 bkt=3
  correctly PASSED at eff=33 where the trained table said FAIL,
  and s=10 bkt=1 correctly FAILED at eff=25 < T_pred=28 where the
  table said PASS.
- wp=45 (strong wall-density law change): expand3 10/12 >
  oracle-free 8/12. Under law change the internal model's
  fidelity collapses faster than the consequence-trained table's.

Hypothesis: a hybrid combining both signals gets the best of
both -- fine discrimination in-distribution (from internal
prediction) plus robustness under law change (from consequence
training). The alternative under test: the hybrid inherits the
weaknesses (e.g. the coarse bucket prior washes out the fine
internal signal in-distribution, or the stale trained correction
misleads under law change).

### The combination (frozen)

Bias-corrected internal prediction: "internal prediction as
prior, consequence training as likelihood correction."

- TRAIN (wp=15, 24 cases, seeds verbatim from expand3): compose
  plans from train beliefs (learner); step each train plan through
  its beliefs via `belief_execute` -> predicted eff P_tr (learner,
  zero world cost); execute train plans on the true world -> true
  eff E_tr (the consequence-training observations; the ONLY true
  outcomes the learner ever sees). Learn per-bucket bias
  bias_b = mean(P_tr - E_tr) over train cases in bucket b
  (integer arithmetic; empty bucket -> global mean bias fallback,
  learner-computed). Also train the expand3 bucket table
  (bucket means + T) verbatim, used only for the in-program
  expand3-rule comparison arm.
- Equivalent form: corrected score C = P - bias_bkt
  = mu_b + (P - Pbar_b), where mu_b is the trained bucket mean
  eff and Pbar_b the trained mean predicted eff in bucket b:
  trained bucket mean as prior, within-bucket internal-prediction
  deviation as the fine term.
- SEALED (wp=15/30/45, 12 cases/shift, setups verbatim from
  expand3/oracle-free): for each case, P from `belief_execute`,
  C = P - bias_bkt, hybrid verdict PASS iff C >= T_hyb where
  T_hyb = mean(C) over the sealed batch (learner-computed,
  transductive; from predictions + learned biases only, no world
  data). The sealed VERDICT COMMIT touches beliefs, plans, and
  trained tables/biases only; the true-world stepper is never
  called there (K1).
- In-program comparison arms (same sealed cases, ONE shared
  label): ge = (eff >= T_pred), T_pred = mean(P) over the sealed
  batch (the oracle-free transductive bar). Rule OF: PASS iff
  P >= T_pred. Rule X3: PASS iff verifier_check(vb, bucket) with
  the frozen trained table. Rule HYB: PASS iff C >= T_hyb.
  Sharing the label makes the three rules exactly comparable; the
  label choice reproduces the published dissociation numbers as
  replication anchors (K3/K4).
- Ablation (consequence-content): rotate ONLY the train eff array
  by 7 (expand3's C1 correction, verbatim), relearn shuffled
  biases bias^sh_b, recompute C_sh/PASS-vs-T_shyb verdicts on the
  sealed cases with the SAME labels. The internal-prediction
  component is identical under the shuffle, so any accuracy drop
  isolates the consequence-training contribution (mirrors
  expand3's K6).

Incorporated by reference (verbatim copies): world generator,
belief generator, step physics, true-world stepper,
NAV+GATHER composer, `belief_execute`, `verifier_train`,
`verifier_check`, all train/sealed seeds, the wp=15/30/45 dial --
from ivwc_expand3/src/ivwc_expand3.zag and
ivwc_oracle_free/src/ivwc_oraclefree.zag. Arm B (re-derivation)
is out of scope (oracle-free showed it near-vacuous; honest
negative already recorded).

## 2. Frozen kill bars

Notation per sealed shift: acc_h = #{verdict_HYB == ge}/12;
acc_of, acc_x3 likewise for the OF/X3 rules; acc_hsh = shuffled-
bias hybrid accuracy; maj = majority share of ge; np_h/nf_h,
sp_h/sf_h = hybrid PASS/FAIL counts and true-eff sums (finding).

- K1 (commit before signal / training-diet hygiene): PASS iff
  (a) the world-call counter is unchanged across the train
  COMMIT block, (b) unchanged across the train PREFF block
  (internal predictions on train), (c) unchanged across each
  shift's sealed VERDICT COMMIT block, AND (d) the section-4
  audits confirm code ordering, the LEARNER section contains no
  world-truth tokens, and `world_execute(` occurs exactly 3
  times in the source (1 definition + train CONSEQ call site +
  sealed SCORING call site). The train CONSEQ observations are
  the declared consequence-training diet, not a leak: they occur
  strictly before any sealed verdict, on train cases only.
- K2 (determinism): PASS iff 3 runs byte-identical (equal sha256).
- K3 (replication anchor, wp=15): PASS iff in-program acc_of15
  == 10 AND acc_x315 == 9. Guards bit-identity of the shared
  sealed setup and both pure rules against the published runs.
- K4 (replication anchor, wp=45): PASS iff in-program acc_of45
  == 8 AND acc_x345 == 10. Same guard under law change.
- K5 (best-of-both, wp=15): PASS iff acc_h15 >= acc_of15 AND
  acc_h15 >= acc_x315 (hybrid matches-or-beats the per-regime
  winners in-distribution).
- K6 (best-of-both, wp=45): PASS iff acc_h45 >= acc_of45 AND
  acc_h45 >= acc_x345 (hybrid matches-or-beats the per-regime
  winners under law change).
- K7 (strict dominance, both regimes): PASS iff acc_h15 >
  acc_of15 AND acc_h15 > acc_x315 AND acc_h45 > acc_of45 AND
  acc_h45 > acc_x345. The task's question in bar form: does the
  hybrid strictly beat both pure approaches on both regimes?
- K8 (consequence-content ablation, wp=15): PASS iff acc_hsh15
  < acc_h15 (strict). Shuffling the consequence mapping must
  strictly degrade the hybrid: the trained-bias content (not the
  procedure alone) drives the hybrid's verdicts.
- K9 (non-degenerate, wp=15): PASS iff acc_h15 > maj15 (strict).

Verdict: BUILD-PASS iff K1..K9 all PASS. Any FAIL yields
BUILD-FAIL naming the failed bar(s). Interpretation is fixed now:
K5/K6 PASS + K7 FAIL = "best-of-both without strict dominance";
K5 or K6 FAIL = "hybrid inherits a pure approach's weakness"
(the report names which regime and which weakness). VOID
conditions: any forbidden-interpreter invocation (PROCESS-FAIL),
or any amendment to this prereg after implementation begins.

## 3. What is NOT claimed

Mechanism test of hybrid verification, not a composition-novelty
or L3 claim. The composer is fixed; the claims concern whether
combining internal prediction with consequence training beats the
pure approaches on the two dissociation regimes, or inherits
their weaknesses. One wall-density law-change axis; item law,
belief noise, and energy budget fixed. The sealed scoring pass is
harness ground truth used ONLY for scoring, never observed by the
learner. The consequence-training diet (24 train true outcomes
at wp=15) is declared in section 1, not hidden.

## 4. Frozen audit commands (run at report time, shell only)

- A1 (phase ordering): in src/ivwc_hybrid.zag, the train COMMIT
  and train PREFF call sites (learner_compose / belief_execute,
  no world_execute) textually precede the train CONSEQ block's
  world_execute call site; within each sealed shift, the VERDICT
  COMMIT block (learner_compose / belief_execute, no
  world_execute) textually precedes the SCORING block's
  world_execute call site. Verified by reporting grep -n line
  numbers.
- A2: the LEARNER section (between the `// ===== LEARNER =====`
  and `// ===== MAIN =====` markers) contains zero occurrences of
  `world_buf` or `world_off`.
- A3: zero occurrences of `expected|answer|key|target` in the
  .zag (grep -c -E).
- A4: zero occurrences of `correct|reference_plan|gold` in the
  .zag (grep -c -E).
- A5: sha256 equality across runs/ivwc_hybrid-run{1,2,3}.txt.
- A6 (diet): `grep -o "world_execute(" src/ivwc_hybrid.zag |
  wc -l` == 3 (one definition, train CONSEQ call site, sealed
  SCORING call site); WC-FINAL printed == 60 (24 train + 36
  sealed).
- A7 (learner information diet): the LEARNER section contains
  zero occurrences of `world_` (grep -c).

## 5. Why the bars discriminate, and calibration note

- K3/K4 pin the experiment to the published dissociation: they
  fail if the shared setup or either pure rule drifted by even
  one case (exact equality, not a threshold). Hand-verified
  before freezing: with T_pred labels, OF's rule gives 10/12 @
  wp=15 (errors s=0,s=3) and 8/12 @ wp=45 (errors s=0,s=3,s=4,
  s=5); X3's bkt==1 rule gives 9/12 @ wp=15 (errors s=3,s=5,s=10)
  and 10/12 @ wp=45 (errors s=0,s=4) -- matching the published
  cross-wave numbers.
- K5/K6 operationalize "best of both": they fail if the hybrid
  falls below either pure approach on either regime (e.g. if the
  coarse bucket prior washes out the fine internal signal
  in-distribution, or the stale trained bias misleads under law
  change).
- K7 is the strict form of the task's question; it fails if the
  hybrid merely matches the per-regime winners.
- K8 fails if the hybrid's accuracy does not depend on the
  consequence CONTENT (then the "hybrid" would be the OF rule
  wearing a trained-bias costume).
- K9 fails on degenerate always-PASS/always-FAIL hybrids.

Calibration: bar DIRECTIONS are theory-motivated and were fixed
before any implementation. NO probe of any kind was run before
this prereg (no /tmp mechanism probe): K3/K4 are hand-verified
against published runs (section 5, first bullet), and K5-K9
directions follow from the hypothesis stated in section 1. The
frozen verdict is computed from the three post-prereg runs of
the committed source. A post-prereg /tmp language-semantics
check (i32 division on negative operands) is permitted ONLY as
implementation safety, not as mechanism evidence.
