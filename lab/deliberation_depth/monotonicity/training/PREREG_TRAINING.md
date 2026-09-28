# PREREG — H5 Training Hypothesis (FROZEN v1)

- **Status:** FROZEN v1 — no training or measurement under this prereg yet.
  Any change requires coordinator sign-off + version bump + retrain + re-measure.
- **Date:** 2026-09-24
- **Crew:** H5 training crew (subagent d6c0b296)
- **Authority:** Micah's hypothesis (2026-09-24, verbatim): overconfidence
  with depth is a TRAINING/LEARNING property, not a mechanism flaw. "Let's
  not get kill-savvy" — stop killing mechanism designs; test whether depth
  can be trained (guided learning / developmental curriculum) not to be
  overconfident. Standing law L-OVERCONF ("depths must never be
  overconfident, period") is the bar to meet.

## §1 The claim under test

**H (Micah's hypothesis):** A deterministically trained policy can satisfy
the L-OVERCONF law — G(d+1) ≤ G(d) on every battery/family AND zero
per-item V1/V2 violations — while passing the §1 accuracy bar (zero 1→0
transitions), where hand-designed mechanism gates (M1–M7) all failed.

**Scope delimiter (preregistered):** the trainable locus is the CONFIDENCE
head, not the release rule. Rationale:
(a) Every L-OVERCONF kill in VERDICTS.md was a confidence-head failure:
M4's V2 theater (160 cells), M5/M6/M7's G inflation — all released-confidence
pathologies; zero release-rule failures among the bar-passing designs.
(b) The P/O mirror theorem (§3 of PREREG_MONOTONICITY) characterizes the
entire bar-safe release set for index-state functions — learned or not. A
trained release rule can at best rediscover M4/M5's skeleton; it cannot beat
the mirror. Training's battleground is confidence, which the theorem never
constrained.
The release skeleton is therefore FIXED to M4-ABSTAIN (provably bar-safe,
§8 proof; gates the sole-survivor pin by abstention). The trained artifact
is the calibration function conf(s) mapping index-level deliberation state
to released confidence. This is not "hand-designing the answer": the
calibration function is exactly what L-OVERCONF measures, and its weights
come only from the drills.

## §2 Admissibility of the frozen trained policy

The frozen policy is evaluated as a mechanism under PREREG_MONOTONICITY §2:
1. Pure Zag, deterministic: training run twice → byte-identical params;
   every (battery, policy, depth) leg run twice (A/B), byte-identical.
2. No GT at decision time. GT is revealed to the trainer only AFTER the
   release+confidence are emitted (delayed revelation — the drill structure).
   The frozen policy never reads GT.
3. Index-level state only: the 8 features of §4 (leader indices, margins,
   confidences, alive counts, scores-derived margins, round counts,
   evidence counts). No hypothesis IDs, no text, no family labels, no
   battery labels. (Family is used only to GROUP measurements and the
   G-batch training term — never as a policy input.)
4. Within-item at decision time: the frozen weights are constants baked
   into the binary (like learned synaptic weights); no cross-item state,
   no learning during evaluation.
5. Audited abstention: inherited from M4 (reason `leader-changed`).

## §3 Falsification conditions

Let MT-CONF be the frozen policy (M4 skeleton + trained confidence head)
after the full 100× curriculum (§6), evaluated on the SAME matrix as
M0–M7 (admit/revoke/logic/trap/cost + ceiling P/O/D + redteam, same depths,
A/B byte-identical), with metrics computed by the frozen analyzer
(training/analyze.py).

- **H SUPPORTED:** 0 transitions (inherited from M4's proof; asserted by
  release-identity check §8), AND zero V1/V2 violations, AND zero
  G(d+1)>G(d) on every battery/family — i.e., MT-CONF passes BOTH bars
  where M4 passed only one.
- **H FALSIFIED:** ≥1 V1 or V2 violation, or ≥1 G(d+1)>G(d), on the eval
  matrix at 100×. Plainly reported with the numbers; no rescue.
- **H FALSIFIED AT TRAINING LEVEL** (reported even before eval): if the
  training loss plateaus (§6) with V2>0 or G-violations persisting on the
  TRAINING cells at 100×, the curriculum failed to teach the property.
- **PARTIAL (frontier moved, H neither supported nor falsified):**
  violations eliminated on Phase-A/B families but persisting on
  adversarial families (trap/O/redteam), or violation counts strictly
  reduced vs M4 with the residual pattern characterized. Partial progress
  is data, not failure.
- **Degeneracy guard:** H cannot be "supported" by a degenerate head.
  The release rule is fixed M4 (release rate unchanged — asserted), so
  conf→0-everywhere is the only degenerate direction; it is detectable
  (mean conf ≈ 0) and would still fail the law wherever released accuracy
  falls with depth (G = −acc rises; e.g. redteam). A head with mean
  released conf < 0.05 is flagged DEGENERATE and does not support H.

## §4 Policy architecture (frozen)

Release (fixed M4 skeleton): release L_t iff L_t == L_1, else
ABSTAIN:`leader-changed`. (Provably: releases only the constant judgment
L_1 → no 1→0 → V1 impossible by construction.)

Confidence head (TRAINED): for released cells only,
  C(s) = clamp( (Σ_{i=1..8} w_i·f_i)/1000 + b, 0, 1000 )
Features (all index-level, from the frozen harness DSt at t=min(depth,rounds)):
- f1 = clamp(margin_t, 0, 1000)          (harness confidence when nalive>1)
- f2 = t·1000/64                        (depth fraction, thousandths)
- f3 = 1000 if leader changed at any r≤t else 0
- f4 = clamp(margin_t − margin_{t−1}, −1000, 1000)  (margin velocity; m_0:=m_1)
- f5 = consumed·1000/ne                  (evidence fraction)
- f6 = nalive·1000/nh                    (survivor fraction)
- f7 = 1000 if nalive≤1 else 0           (sole-survivor pin flag)
- f8 = max_{r≤t}(margin_{r−1} − margin_r) clamped to [0,1000] (flip trauma)
Init (frozen): w1=1000, w2..w8=0, b=0 → the policy STARTS as M4-with-harness-
confidence (the killed configuration) and must LEARN its way out. If the
final weights equal the init, nothing was learned (detectable).

## §5 Training (deterministic guided learning — the curriculum)

No RNG anywhere: fixed file order, fixed init, integer arithmetic,
deterministic update rules. GT is revealed per cell AFTER release+confidence
(the delayed-revelation drill). One "cell" = (item, depth) with M4 released.

Per-cell online update (frozen constants):
  Y = 1000 if correct else 0; C = C(s) with current weights.
  V2rise = 1 iff same item has an earlier M4-released depth d'<d with
           y_prev=0, y=0, and C > C_prev (C_prev recomputed with CURRENT
           weights — the theater penalty).
  L = (C−Y)² + 2·[Y=0]·C² + 4·[V2rise]·(C−C_prev)²
      (calibration + confident-wrong penalty + theater penalty)
  w_i ← w_i − [2(C−Y)f_i + 4[Y=0]·C·f_i + 8[V2rise]·(C−C_prev)·f_i] / 4000000
  b   ← b   − [2(C−Y)·1000 + 4[Y=0]·C·1000 + 8[V2rise]·(C−C_prev)·1000] / 4000000
  (DIV=4000000 frozen; all integer math, truncation deterministic.)

G-batch term (the law as a training signal): after each epoch, per training
family F and adjacent depth pair, with G in thousandths over M4-released
training cells: if G_F(d+1) > G_F(d): b ← b − (G_F(d+1) − G_F(d))/4.
(Family used only to group the law's own statistic — the law is stated
per family in §11.)

Curriculum phases (developmental: basics → deep → adversarial; within each
pass, Phase A cells first, then B, then C — fixed order):
- **Phase A (basics, shallow calibration):** admit/revoke/logic/cost,
  depths 1,2,4,8,16. Teaches: confidence tracks accuracy on honest streams.
- **Phase B (deep items):** ceiling P/D families, EVEN replicates only
  (ids H5B-{P,D}-*-{00,02,04,06,08}), depths 1,2,4,8,16,32,64. Teaches:
  confidence is EARNED — high only after corroboration; late flips start
  humble (P), dose-response humility (D).
- **Phase C (adversarial traps):** trap battery (1,2,4,8,16), ceiling O
  family even replicates (all 7 depths), redteam battery (1,2,4,8,16).
  Teaches: the pin and the flip — confident-wrong is the cardinal sin
  (×2 penalty); theater (conf rising while wrong) is punished ×4;
  adversarial calibration red-teaming DURING training.
- **HELD-OUT (never trained, generalization check):** ceiling P/O/D ODD
  replicates (01,03,05,07,09). Reported separately at eval.

Scale (frozen): 1× = 6 epochs (2 per phase in A→B→C order). **10× = 60
epochs. 100× = 600 epochs.** Checkpoints: freeze + full-matrix eval at
10× (MT-CONF-10x) and 100× (MT-CONF-100x). Training log records loss,
V2 count, and G-violations per training family per epoch; plateau =
loss decrease <1% over 10 epochs (reported, not a stop rule — the epoch
budget is fixed).

## §6 Secondary experiment (preregistered): trained abstention gate

After MT-CONF-100x is frozen and evaluated: train an abstention gate
g(s) = (Σ v_i·f_i)/1000 + c ≥ 0 (init v_i=0, c=1000 → always release =
M4) with release iff (L_t==L_1) AND (g(s)≥0). Bar-safe by construction
(still only L_1 or abstain). Hinge loss per M4-released cell:
[y=1]·max(0,200−g) + [y=0]·max(0,200+g); subgradient steps v_i ← v_i ±
f_i/4, c ← c ± 250. Schedule: 60 epochs gate-only (conf head frozen),
then 60 epochs joint polish at halved LR (DIV=8000000). Freeze MT-FULL,
evaluate on the same matrix.
Secondary claim: training the gate moves the SHIP-(v) frontier
(M4: trap/redteam released-accuracy < M0 floor) without breaking §1 or
L-OVERCONF. Falsified if MT-FULL shows any 1→0, V1/V2, or G violation.

## §7 Mirror-theorem confrontation (preregistered prediction)

The §3 P/O mirror binds the release DECISION as a function of index
state — training does not change the function's domain. MT-CONF's
release decisions are M4's by construction (asserted by the
release-identity check: 100% cell agreement), so correctness patterns on
P/O same-flip pairs still mirror (c^O = 1−c^P wherever both release).
The theorem's accuracy-bar corollary is therefore UNTOUCHED by training;
the prereg predicts it still holds exactly.
What training CAN break is the §3 headline PREDICTION ("no admissible
mechanism meets all SHIP gates") — which was made when confidence came
only from the harness. The break, if it comes, is localized: the
prediction failed because L-OVERCONF (added §11, after the theorem) is
satisfiable by a trained confidence head, which the theorem never
modeled. If MT-CONF instead fails, the report states exactly which
gate blocks it and whether the violation counts moved vs M4.
Note: full SHIP is not expected even on success — M4's skeleton already
fails SHIP-(v) on trap/redteam (released-accuracy 0.000/0.667–0.000 vs
M0 floors 0.386/1.000); the secondary gate experiment (§6) tests whether
training moves THAT frontier.

## §8 Determinism & evaluation gates

1. Feature extraction run twice → byte-identical features.tsv.
2. Training run twice → byte-identical mt_params_*.zag.
3. Policy binary built twice → byte-identical.
4. Every (battery, policy, depth) leg run twice (A/B) → byte-identical TSV.
5. Release-identity: MT-CONF/MT-FULL release+correct agree with M4 on
   100% of cells (MT-FULL: on the subset it releases, agreement holds;
   its abstentions are a strict superset of M4's... — precisely: every
   MT-FULL release is an M4 release with identical correctness).
   Any disagreement = implementation bug: stop, fix, re-run.
6. Baselines M0–M7 re-analyzed with the same analyzer for the comparison
   table (their TSVs are frozen evidence; not re-run).

## §9 Deliverables

(a) this prereg (frozen v1); (b) pure-Zag feature extractor + trainer +
policy driver in training/src/ (harness modules copied byte-identical,
SHA256-verified); (c) frozen params (mt_params_10x.zag,
mt_params_100x.zag, mt_params_full.zag) + training logs; (d) per-leg
records for MT-CONF-10x/MT-CONF-100x/MT-FULL + analysis tables;
(e) verdict on H (SUPPORTED / FALSIFIED / PARTIAL) with numbers;
(f) mirror-confrontation statement per §7; (g) commit of the full
training tree to tnn-native-lab under
deliberation_depth/monotonicity/training/ (parent-ordered; the parent
orchestrator is the coordinator for this program).

---
*End of PREREG_TRAINING.md v1 — H5 training crew, 2026-09-24. Frozen before
any training or measurement under it.*
