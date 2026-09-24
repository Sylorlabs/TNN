# PREREG — H5 Training Hypothesis, v2 (FROZEN v1)

- **Status:** FROZEN v1 — no training or measurement under this prereg yet.
  Any change requires coordinator sign-off + version bump + retrain + re-measure.
- **Date:** 2026-09-24
- **Crew:** H5 training crew, round 2 (subagent 16dcd8c0)
- **Authority:** Micah's hypothesis (2026-09-24): overconfidence with depth is a
  TRAINING/LEARNING property, not a mechanism flaw. Round 1 (PREREG_TRAINING.md
  v1, commit 2e93311b) FALSIFIED AT TRAINING LEVEL: the v1 curriculum was a
  one-way confidence ratchet (VERDICT.md) — an implementation bug (train.zag
  read feats from field 8+k, training on f2..f8) compounded by a STRUCTURAL
  flaw (upward calibration arithmetically impossible: every correct-cell
  gradient numerator had |num| < DIV=4000000 and truncated to 0; every
  surviving term pushed confidence down only). v1 could only suppress, never
  calibrate. This v2 prereg is a NEW design that fixes both root causes; it is
  not a rerun of v1.

## §1 The claim under test

**H (Micah's hypothesis, unchanged):** A deterministically trained policy can
satisfy the L-OVERCONF law — G(d+1) ≤ G(d) on every battery/family AND zero
per-item V1/V2 violations — while passing the §1 accuracy bar (zero 1→0
transitions), where hand-designed mechanism gates (M1–M7) all failed.

**Scope delimiter (unchanged from v1):** the trainable locus is the
CONFIDENCE head, not the release rule. The P/O mirror theorem
(PREREG_MONOTONICITY §3) characterizes the entire bar-safe release set for
index-state functions — learned or not; a trained release rule can at best
rediscover M4/M5's skeleton. The release skeleton is therefore FIXED to
M4-ABSTAIN (provably bar-safe). The trained artifact is the calibration
function conf(s) mapping index-level deliberation state to released
confidence. The calibration function is exactly what L-OVERCONF measures,
and its weights come only from the drills.

**What v2 changes vs v1:** the loss. v1's loss had no representable upward
gradient; v2's loss is symmetric-calibration-first (fixed point = calibration,
not suppression), with the law's teeth (theater penalty, G-batch) as
guardrails rather than the whole signal.

## §2 Admissibility of the frozen trained policy

The frozen policy is evaluated as a mechanism under PREREG_MONOTONICITY §2:
1. Pure Zag, deterministic: training run twice → byte-identical params;
   every (battery, policy, depth) leg run twice (A/B), byte-identical.
2. No GT at decision time. GT is revealed to the trainer only AFTER the
   release+confidence are emitted (delayed revelation — the drill structure).
   The frozen policy never reads GT.
3. Index-level state only: the 8 features of §4. No hypothesis IDs, no text,
   no family labels, no battery labels. (Family is used only to GROUP
   measurements and the G-batch training term — never as a policy input.)
4. Within-item at decision time: the frozen weights are constants baked
   into the binary (like learned synaptic weights); no cross-item state,
   no learning during evaluation.
5. Audited abstention: inherited from M4 (reason `leader-changed`).

## §3 Falsification conditions (preregistered BEFORE any v2 training)

Let MT2-CONF be the frozen v2 policy (M4 skeleton + v2-trained confidence
head) after the full 100× curriculum (§5), evaluated on the SAME matrix as
M0–M7 (admit/revoke/logic/trap/cost + ceiling P/O/D + redteam, same depths,
A/B byte-identical), metrics computed by the frozen analyzer
(training/analyze.py), mech ids 13 (10×) / 14 (100×).

- **H SUPPORTED:** 0 transitions (inherited from M4's proof; asserted by the
  release-identity check §8), AND zero V1/V2 violations, AND zero
  G(d+1)>G(d) on every battery/family (strict reading; refined reading
  recorded too), AND the non-degeneracy bar (§3a) clears, AND the
  learned-pin criterion (§3b) holds — i.e., MT2-CONF passes BOTH bars where
  M4 passed only one, non-degenerately.
- **H FALSIFIED (design):** ≥1 V1 or V2 violation, or ≥1 G(d+1)>G(d), on the
  eval matrix at 100×. The v2 upward signal did not produce law-satisfying
  depth. Plainly reported with the numbers; no rescue.
- **H FALSIFIED AT TRAINING LEVEL** (reported even before eval): if the
  training loss plateaus (§5) with V2>0 or G-violations persisting on the
  TRAINING cells at 100×, the curriculum failed to teach the property.
- **DEGENERATE:** the v1 failure mode recurring under a new loss. If mean
  released confidence on CORRECT eval cells < 0.50, or
  (meanCorrect − meanWrong) < 0.20, the head is degenerate and H cannot be
  supported — regardless of the bars.
- **PARTIAL (frontier moved, H neither supported nor falsified):**
  violations eliminated on Phase-A/B families but persisting on adversarial
  families (trap/O/redteam), or violation counts strictly reduced vs M4 with
  the residual pattern characterized. Partial progress is data, not failure;
  H stays ALIVE but narrowed.
- **PIN-IGNORED / PIN-INFLATED:** if w7(100×) == 0 exactly, the pin feature
  was ignored by learning (report PIN-IGNORED — not learned handling). If on
  eval released f7=1000 cells mean conf > empirical accuracy + 0.10, the pin
  inflates confidence beyond calibration (report PIN-INFLATED — handling
  failed). Either blocks H SUPPORTED via §3b.

**Burial vs survival of Micah's hypothesis (preregistered):**
- H is **BURIED FOR GOOD** iff v2 returns FALSIFIED or DEGENERATE at 100×
  AND the v2 machinery audit passes: (i) feature indexing byte-correct
  (field-index probe, §8); (ii) upward steps representable AND observed
  (weights moved from init; mean correct-conf rose during training);
  (iii) the theater term fired >0 epochs (the anti-theater signal was live);
  (iv) autopsy finds no implementation bug. Two independent curricula, both
  with a working upward signal, failed → the confidence-head locus is not
  where training beats mechanisms.
- H stays **ALIVE** iff SUPPORTED (vindicated — training did what mechanisms
  couldn't) or PARTIAL with characterized residual (narrowed, not dead).
- If autopsy finds an implementation bug behind a v2 failure, H remains
  **OPEN** (a v3 question) — a bug burial is not a hypothesis burial.

### §3a Non-degeneracy guard (teeth from the start, not post-hoc)

v1's §3 guard caught degeneracy only after the fact. v2 logs, EVERY epoch,
over released training cells with epoch-end weights: meanConfCorrect,
meanConfWrong, meanConfAll. The guard is part of the frozen verdict:
DEGENERATE iff at 100× eval (a) mean released conf on correct cells < 0.50,
or (b) meanCorrect − meanWrong < 0.20. A head that will not be confident when
right (v1: 0.000), or that cannot separate right from wrong, is degenerate.

### §3b Learned pin handling (the sole-survivor conf=1000 pin)

The harness hardcodes `if(nalive<=1){st.conf=1000;}` — confidence by code,
independent of truth (instrumentation: 100/100 truth-kill rounds pinned 1000
while wrong). v1 "gated" this by universal suppression (conf=0 everywhere) —
that does not count. v2's head never reads harness conf; the pin reaches it
only as features f7 (pin flag) and f1 (margin, saturated on sole-survivor).
**PIN-LEARNED** iff: (a) w7(100×) ≠ 0 (the pin feature was learned, not
ignored); (b) on eval released cells with f7=1000, mean conf ≤ empirical
accuracy + 0.10 (no systematic pin inflation beyond what calibration
warrants); (c) per-cell confs on wrong f7 cells reported individually. The
§3a guard jointly rules out "handling by universal suppression": the head
must stay confident where confidence is earned (meanCorrect ≥ 0.50) while
not inflating the pin.

## §4 Policy architecture (frozen)

Release (fixed M4 skeleton): release L_t iff L_t == L_1, else
ABSTAIN:`leader-changed`. (Provably: releases only the constant judgment
L_1 → no 1→0 → V1 impossible by construction.)

Confidence head (TRAINED): for released cells only,
  C(s) = clamp( (Σ_{i=1..8} w_i·f_i)/1000 + b, 0, 1000 )
Features (all index-level, from the frozen harness DSt at t=min(depth,rounds);
byte-identical feat.zag as v1 — the extractor was correct, only the trainer's
field parser was wrong):
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

## §5 Training v2 (deterministic guided learning — the fixed curriculum)

No RNG anywhere: fixed file order, fixed init, integer arithmetic,
deterministic update rules. GT is revealed per cell AFTER release+confidence
(the delayed-revelation drill). One "cell" = (item, depth) with M4 released.

**The v2 loss (frozen).** Per released training cell:
  Y = 1000 if correct else 0; C = C(s) with current weights.
  V2rise = 1 iff same item has an earlier M4-released depth d'<d with
           y_prev=0, y=0, and C > C_prev (C_prev recomputed with CURRENT
           weights — the theater penalty). rise = C − C_prev.
  L = (C−Y)² + 4·[V2rise]·(C−C_prev)²
      (symmetric calibration core + theater penalty; the ×2 confident-wrong
      asymmetry of v1 is REMOVED — the prescription is symmetry: reward
      well-calibrated high confidence on correct answers as strongly as
      confident-wrong is punished. The anti-overconfidence teeth that remain
      are targeted: the theater term fires exactly on the V2 pathology, and
      the one-sided G-batch fires exactly on law violations.)
  Fixed point: E[2(C−Y)f_i] = 0 ∀i (modulo the targeted guardrails) — i.e.,
  the least-squares / calibration fixed point C ≈ E[Y|s], NOT suppression.
  The theater term's fixed point on wrong→wrong chains (C = 0.8·C_prev,
  decaying toward 0) agrees in direction with calibration (C→0); it shapes
  the trajectory, it does not relocate the fixed point.

**Representable updates (the v1 structural fix, frozen).**
  w_i ← w_i − tdiv( 2(C−Y)f_i + 8·rise·f_i, DIV2 )
  b   ← b   − tdiv( 2(C−Y)·1000 + 8·rise·1000, DIV2 )
  DIV2 = 40000 (frozen). Rationale: v1's DIV=4000000 made even the LARGEST
  correct-cell gradient (2·10⁶) vanish. With DIV2, any cell miscalibrated by
  |C−Y|·f_i ≥ 20000 moves its weight (bias moves on any |C−Y| ≥ 20), while the
  largest single-cell step (theater: 8·10⁶/40000 = 200) stays two orders of
  magnitude below the weight clamp. Upward steps are representable across the
  full gradient range — verified by probe before the 100× run (§8).
  tdiv = truncation toward zero (matches Zag native `/` on negatives per the
  v1 division probe).
  Anti-saturation guard (frozen): after each epoch, clamp w_i to
  [−2000000, 2000000]; binding events counted in the log. The calibration
  fixed point has weights O(1000); the clamp binds only on divergence paths.

**G-batch term (the law as a training signal, unchanged in form):** after
each epoch, per training family F and adjacent depth pair, with G in
thousandths over M4-released training cells (all phases): if G_F(d+1) >
G_F(d): b ← b − tdiv(G_F(d+1) − G_F(d), 4). One-sided per the law (the law
forbids rises, not falls). v1's pathology — the batch firing forever after
conf hit the floor with nothing able to push back — is structurally gone:
the symmetric per-cell term pushes confidence back UP on correct cells.

**Non-degeneracy telemetry (frozen):** every epoch logs, over released
training cells with epoch-end weights: meanConfCorrect, meanConfWrong,
meanConfAll, plus clamp bindings. The §3a guard is evaluated at 100× eval.

**Field-index fix (v1 Layer-1 bug):** train.zag read feats[k] from TSV field
(8+k) — training on (f2..f8, atoi("")=0). v2 reads field (7+k): feats[k] from
`line[tabs[6+k]+1 .. tabs[7+k]]` = f1..f8. Verified by a byte-level probe
with known feature values before training (§8).

**Curriculum phases** (developmental: basics → deep → adversarial; within
each pass, Phase A cells first, then B, then C — fixed order; unchanged):
- **Phase A (basics, shallow calibration):** admit/revoke/logic/cost,
  depths 1,2,4,8,16.
- **Phase B (deep items):** ceiling P/D families, EVEN replicates only,
  depths 1,2,4,8,16,32,64.
- **Phase C (adversarial traps):** trap battery (1,2,4,8,16), ceiling O
  family even replicates (all 7 depths), redteam battery (1,2,4,8,16).
- **HELD-OUT (never trained, generalization check):** ceiling P/O/D ODD
  replicates (01,03,05,07,09). Reported separately at eval.

**Scale (frozen):** 1× = 6 epochs (2 per phase in A→B→C order).
**10× = 60 epochs → MT2-CONF-10x checkpoint. 100× = 600 epochs →
MT2-CONF-100x.** Training log records loss, V2 count, G-violations,
clamp bindings, w1..w8, b, and meanConfCorrect/meanConfWrong/meanConfAll
per epoch; plateau = loss decrease <1% over 10 epochs (reported, not a stop
rule — the epoch budget is fixed).

**10× go/no-go (frozen):** proceed to 100× iff (a) final weights ≠ init,
(b) theater term fired >0 epochs, (c) meanConfCorrect on training cells at
10× ≥ 0.30 (lenient early trajectory bar toward calibration), (d) phase-A
loss decreased pass 1 vs pass 0. Otherwise stop and diagnose — do not burn
100× on a broken design.

## §6 Secondary experiment (CONDITIONAL — preregistered)

The v1 §6 (trained abstention gate → MT-FULL) was never built; its premise
is a functional confidence head. v2 re-preregisters it as CONDITIONAL: it
runs ONLY if MT2-CONF-100x is non-degenerate per §3a (meanCorrect ≥ 0.50).
If the primary head is degenerate, §6 stays blocked (same premise failure
as v1) and is reported as such, not silently dropped.
If unblocked: train gate g(s) = (Σ v_i·f_i)/1000 + c ≥ 0 (init v_i=0,
c=1000 → always release = M4) with release iff (L_t==L_1) AND (g(s)≥0),
hinge loss per M4-released cell: [y=1]·max(0,200−g) + [y=0]·max(0,200+g),
subgradient steps v_i ← v_i ± tdiv(f_i,4), c ← c ± 250. Schedule: 60 epochs
gate-only (conf head frozen), then 60 epochs joint polish at halved step
(DIV2-equivalent 80000). Freeze MT2-FULL, evaluate on the same matrix.
Secondary claim: training the gate moves the SHIP-(v) frontier without
breaking §1 or L-OVERCONF. Falsified if MT2-FULL shows any 1→0, V1/V2, or G
violation.

## §7 Mirror-theorem confrontation (preregistered prediction)

The §3 P/O mirror binds the release DECISION as a function of index state —
training does not change the function's domain. MT2-CONF's release decisions
are M4's by construction (asserted by the release-identity check: 100% cell
agreement), so correctness patterns on P/O same-flip pairs still mirror
(c^O = 1−c^P wherever both release). The theorem's accuracy-bar corollary is
therefore UNTOUCHED by training; the prereg predicts it still holds exactly.
What training CAN challenge is the §3 headline PREDICTION ("no admissible
mechanism meets all SHIP gates") — made when confidence came only from the
harness. Precise scope note: even a fully law-satisfying confidence head
cannot break the headline prediction outright, because MT2-CONF inherits
M4's SHIP-(v) failure on trap/redteam released-accuracy (the conf head does
not change release decisions). The break, if it comes, is localized: the
prediction's L-OVERCONF content is satisfiable by a trained confidence head,
which the theorem never modeled. If MT2-CONF instead fails, the report
states exactly which gate blocks it and whether the violation counts moved
vs M4. Note: full SHIP is not expected even on success — the §6 gate
experiment tests whether training moves THAT frontier.

## §8 Determinism & evaluation gates

1. Frozen input: training/features/features.tsv (5240 cells) adopted
   byte-identical from v1 (SHA256
   4682190cfd504cb692df122a6b054d8fad65ef860707e6a92abfdf04e65a897d);
   v1's §8 gate 1 (extraction ×2 byte-identical) already passed on it.
   The v2 trainer parses it with corrected field indexing — verified by a
   synthetic probe (known f1..f8 values → recovered exactly) before training.
2. Upward-representability probe: synthetic correct cell (Y=1000, C<Y) →
   weights move UP by the exact tdiv amount; synthetic wrong→wrong rising
   chain → theater term fires and pushes DOWN. Both asserted before 100×.
3. Training run twice → byte-identical mt2_params_*.zag + logs.
4. Policy binary built twice → byte-identical.
5. Every (battery, policy, depth) leg run twice (A/B) → byte-identical TSV.
   Mech ids 13 (MT2-CONF-10x), 14 (MT2-CONF-100x) — no collision with 0–12.
6. Release-identity: MT2-CONF release+correct agree with M4 on 100% of
   cells. Any disagreement = implementation bug: stop, fix, re-run.
7. Baselines M0–M7 re-analyzed with the same analyzer for the comparison
   table (their TSVs are frozen evidence; not re-run).
8. 10× go/no-go per §5 before the 100× burn.

## §9 Deliverables

(a) this prereg (frozen v1); (b) pure-Zag trainer (train2.zag) + unchanged
frozen policy driver (policy.zag) and feature extractor (feat.zag) in
training/v2/src/ (harness modules copied byte-identical, SHA256-verified);
(c) frozen params (mt2_params_10x.zag, mt2_params_100x.zag) + training logs
with per-epoch non-degeneracy telemetry; (d) per-leg records for
MT2-CONF-10x/MT2-CONF-100x + analysis tables; (e) verdict on H per §3
(SUPPORTED / FALSIFIED / FALSIFIED AT TRAINING LEVEL / DEGENERATE / PARTIAL /
PIN-*) with numbers, both L-OVERCONF readings, and the burial-vs-alive
statement; (f) mirror-confrontation statement per §7; (g) commit of the full
v2 tree to tnn-native-lab under deliberation_depth/monotonicity/training/v2/
(parent-ordered).

---
*End of PREREG_TRAINING_V2.md v1 — H5 training crew round 2, 2026-09-24.
Frozen before any training or measurement under it. The v1 design could only
suppress; v2 is built to calibrate — symmetric loss, representable upward
steps, and a non-degeneracy guard with teeth from epoch 0.*
