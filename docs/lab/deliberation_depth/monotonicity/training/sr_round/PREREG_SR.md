# PREREG — H5 New-Hypothesis Round: Scaffold-and-Release (SR ROUND)

- **Status:** FROZEN v1 — coordinator sign-off 2026-09-24. No training or
  measurement under this prereg yet. Any change after freezing requires
  version bump + note.
- **Freeze amendments (v0→v1, from grok-4.7 independent design pass,
  `sr_round/GROK_SR_DESIGN.md`):** (i) guard set tightened — B4b per-honest-
  family confidence floor, B6 recall ≥0.95 per family, new B13 GAP_FLOOR
  underconfidence guard; (ii) second scaffold arm SR-S1 added (grok's S1:
  training-procedure scaffold vs SR-S9's input-feature scaffold — standing
  instruction: test both); (iii) grok's S3 scheme is a do-not-run, not
  included; (iv) grok ranks the optimizer arm highest (P=0.38) — recorded
  as a prediction, not a prereg change; all six arms dispatch in parallel.
- **Date:** 2026-09-24
- **Authority:** Micah's question (2026-09-24): if training alone doesn't fix
  overconfidence with depth, WHAT DOES? Hard requirement: **no machine that
  is naturally always overconfident.**
- **Context:** H-0 v1 FALSIFIED (conf→0 degenerate;
  `training/VERDICT_TRAINING.md`); v2 PARTIAL (genuine calibration on honest
  families, worst-case residual on trap/O/redteam); T-05 FALSIFIED
  (worst-case loss → degenerate crush; binding constraint is the OPTIMIZER,
  not loss geometry; f5 separation signal exists;
  `training/backlog/t05/VERDICT_T05.md`).

## §1 The question

**H-SR (headline): scaffold-and-release is REQUIRED for non-overconfident
depth.** A training-time scaffold carrying an oracle calibration signal is
withdrawn at release (SIGNAL_DISCONNECT); the head must then produce
calibrated confidence from its own weights alone. Per the
learned=persists-after-disconnect rule, ONLY post-release calibration counts.

Two kill directions, stated explicitly (adjudicated in §11):
- **NECESSITY:** if ANY non-scaffold arm (WC, ARCH, LOSS) achieves
  non-degenerate non-overconfident depth on the frozen matrix, H-SR **as a
  requirement** is KILLED.
- **SUFFICIENCY:** if NEITHER scaffold arm (SR-S9, SR-S1) achieves
  non-degenerate non-overconfident depth post-release, the sufficiency
  claim is KILLED. If either scaffold arm clears the bars while no
  non-scaffold arm does, sufficiency HOLDS for that variant.

Two scaffold operationalizations are tested because they are genuinely
different claims about what "scaffold" means: SR-S9 = scaffold as an
oracle INPUT FEATURE (removed at disconnect); SR-S1 = scaffold as a
training-time GRADIENT MASK (removed at disconnect). Per standing
instruction (when in doubt, test both), both run.

Relation to backlog T-18 (grok H-5 scaffold withdrawal): T-18's scaffold was
elimination machinery (kill-bit masking); H-SR's scaffold is an **oracle
calibration signal fed as a head input**, and the disconnect is permanent and
total — the input is removed from the released binary, not masked. T-18 tests
whether a habit extinguishes; H-SR tests whether calibration internalizes.

## §2 Frozen machinery — reused vs new

**REUSED frozen (byte-identical, SHA-pinned where applicable):**
- `training/features/features.tsv` (5240 cells, SHA256
  `4682190cfd504cb692df122a6b054d8fad65ef860707e6a92abfdf04e65a897d`),
  with its heldout flags (odd P/O/D replicates = HELD-OUT, never trained).
- Eval matrix = **37 legs** exactly as `training/run_eval.sh`: admit, revoke,
  logic, trap, cost, redteam × depths {1,2,4,8,16} (30 legs) + ceiling ×
  depths {1,2,4,8,16,32,64} (7 legs). A/B byte-identical per leg.
- Metrics from frozen `training/analyze.py`: G(d) = mean_conf − accuracy
  over released cells per (family, depth); Gviol = count of adjacent-depth
  rises G(d+1) > G(d) (tolerance 1e-12); V1 = correct→wrong with
  conf non-decreasing; V2 = wrong→wrong with conf rising.
- v2 head form C(s) = clamp((Σwᵢfᵢ)/1000 + b, 0, 1000), features f1..f8
  (v2 PREREG §4), init w1=1000, w2..w8=0, b=0 (starts as the killed
  M4-with-harness-confidence configuration).
- v2 §5 curriculum: Phase A (admit/revoke/logic/cost, d∈{1,2,4,8,16}) →
  Phase B (P/D even replicates, 7 depths) → Phase C (trap, O even
  replicates, redteam); 1× = 6 epochs, 10× = 60, 100× = 600; DIV2=40000
  with tdiv truncation-toward-zero; anti-saturation clamp wᵢ∈[−2000000,
  2000000]; G-batch b ← b − tdiv(Gdiff,4) on strict rises; theater term
  4·rise·(C−Cprev)² with Cprev recomputed under current weights.
- M4 release skeleton (release L_t iff L_t == L_1): release-identity 100%
  vs M4 asserted per arm (§8 gate: any disagreement = implementation bug,
  stop, fix, re-run).
- v2-100× frozen params + eval TSVs as the CTL yardstick (§9).

**NEW in this round** (under `training/sr_round/`):
- Scaffold feature pipeline (s9, §5); five new trainers
  (train_sr/train_sr1/train_wc/train_arch/train_loss.zag); release policy
  drivers (policy_sr.zag = 8-input post-disconnect, policy_arch.zag = (m,s)
  head); per-arm param files, logs, results, analysis.

## §3 Law readings (both recorded, one kills)

- **Strict L-OVERCONF:** any strict G-rise (G(d+1) > G(d)) or any V1/V2 on
  any family → law violated.
- **Refined L-OVERCONF:** violated only if G crosses 0 (becomes positive).
- An arm's kill bars use the STRICT reading; the refined outcome is recorded
  alongside (the round runs both readings per Micah's standing instruction).

## §4 Non-degeneracy guards (mandatory in EVERY arm's kill bars)

Measured on the 37-leg eval matrix with frozen weights. An arm that clears
the law bars only by degenerate compliance does NOT count as SUPPORTED.
All thresholds exact. Freeze amendment v1: grok-4.7's independent guard
set merged in — the round-1 tripwire (mean conf ≥ 0.05) would have
*accepted* T-05's 1000→67 crush, so the floors below are set 7.5× above
the crush point and 0.25 below the only non-degenerate operating point
(v2's 0.747).

- **G4** mean released confidence on CORRECT cells ≥ **0.50** (≥500
  thousandths), matrix aggregate. (v1 failed at 0.000; v2 §3a.)
- **G4b** HONEST_CCONF: per honest family (admit/revoke/logic/cost,
  n_rel_correct ≥ 10): mean C on released correct cells ≥ **0.50**.
  (Closes the aggregate loophole: conf=1.0 on admit + conf=0.0 on logic
  would pass G4 but fails G4b. No floor on adversarial families — their
  behavior is the law's job, not the guard's.)
- **G5** correct−wrong separation: meanConfCorrect − meanConfWrong ≥
  **0.20** (≥200 thousandths). (v2 §3a.)
- **G6 recall-loss cap:** released-correct count / M4 released-correct
  count ≥ **0.95**, per family. (Belt-and-suspenders on B9: with the answer
  channel frozen the ratio is 1.0 by construction; the bar documents the
  constraint and catches any release-identity drift.)
- **G7 abstention-volume cap:** abstained cells / total cells ≤ **0.30**,
  matrix aggregate. (Belt-and-suspenders on B9 for the same reason.)
- **G8 G-flatness (vacuity guard):** G must be DEFINED (≥10 released cells)
  on ≥4 of 5 depth slots per 5-depth family and ≥5 of 7 for ceiling
  families; AND the defined G values must not be all equal within 1e-3.
  A flat G = +0.000 from universal abstention does not count.
- **G13 GAP_FLOOR (underconfidence guard):** per (family, depth) with
  n_rel ≥ 8: G(F,d) ≥ **−0.100** (−100 thousandths). Kills conf≡0 wherever
  accuracy > 0.10 (G = conf − acc ⇒ conf≡0 gives G = −acc < −0.10) and any
  per-family underconfidence suppression that the aggregate G4 misses.
  T-05's logic collapse gives G ≤ −0.103 at most generous (≈−0.800
  realistic) → fails G13. v2's G=0.000 passes.

## §5 H-SR — the scaffold arm (headline)

**Scaffold operationalization (chosen): per-depth-slot empirical correctness
rate, causally computed from the training stream.**

During training the head receives a 9th input:
  s9 = 1000 × (correct released training cells at same depth slot, seen
       STRICTLY BEFORE the current cell in the fixed training order)
       / (released training cells at same depth slot, seen strictly before)
Depth slots = {1,2,4,8,16,32,64} (7 slots). If no prior released cell exists
in the slot, s9 = 500 (uninformative prior). s9 is recomputed online from the
delayed-revelation labels — GT revealed to the trainer only after
release+confidence, exactly as v2 §5.

**Why this scaffold and not the alternatives:**
- Per-cell Y (the label itself) lets the head learn identity-copy
  ("repeat s9") — scaffold-dependence with zero internalization, and the
  release test would be vacuous-by-construction rather than informative.
- Per-(depth, family) rate launders the family label — barred from policy
  inputs (v2 §2.3) — through the scaffold. Per-depth keeps the scaffold
  index-legitimate: depth is already a head input (f2), so the scaffold
  teaches a mapping the head has the inputs to express.
- s9 is exactly the reference-class quantity that calibration is defined
  against (mean correctness of the class), so the training-time fixed point
  is calibration itself. A global aggregate of the training stream is not
  reconstructible per-cell at eval — post-release calibration therefore
  proves internalization, not copying.

**Training (Stage 1, scaffold ON):** identical to v2 §5 (A→B→C, 600 epochs,
DIV2=40000, symmetric loss + theater + G-batch), except the head is 9-input:
C = clamp((Σ_{i=1..8} wᵢfᵢ + w9·s9)/1000 + b, 0, 1000), init w9 = 0.
**10× go/no-go:** (a) weights ≠ init; (b) w9 ≠ 0 (the scaffold was actually
used — a zero w9 means the head ignored the prosthesis and the arm is
void); (c) training meanConfCorrect ≥ 0.30; (d) theater term fired >0
epochs. Otherwise stop and diagnose.

**SIGNAL_DISCONNECT (Stage 2, release):** the scaffold input is REMOVED —
the released policy driver (policy_sr.zag) computes
C = clamp((Σ_{i=1..8} wᵢfᵢ)/1000 + b, 0, 1000) from the frozen Stage-1
weights w1..w8, b (w9 discarded). **Zero gradient steps after disconnect.**
Disconnect verification (preregistered): (i) the released binary's source
contains no s9 code path (audit); (ii) the frozen param file contains only
w1..w8, b; (iii) HELD-OUT calibration is reported separately — if
post-release calibration holds on training families but collapses on
held-out, the mapping was memorized, not internalized → sufficiency fails.

**Pin handling:** f7/w7 unchanged; v2 §3b PIN-LEARNED reported (w7 ≠ 0; no
inflation >0.10 on f7=1000 released cells).

**Falsification (sufficiency):** post-release eval violates any of B1–B3 or
fails any guard B4–B8/B13 (§10) → this variant's sufficiency claim KILLED.
**Necessity** adjudicated in §11.

## §5b Arm SR-S1 — scaffold as training-time gradient mask (grok's S1)

Second scaffold operationalization (freeze amendment v1): the scaffold is a
training-time integer gradient mask, not an input feature. The head stays
8-input throughout; NOTHING is added to or removed from the released
binary's inputs — the disconnect removes the mask from the update rule.

**Scaffold (Stage 1, mask ON):** v2 §5 curriculum (A→B→C, 600 epochs,
DIV2=40000, symmetric loss + G-batch), except the per-epoch update rule
carries a training-only mask:
- theater coefficient = 0 on weight indices {5,7} (the theater term does
  not update w5/w7 — the separator channel is protected from the
  theater's sign fight);
- calibration-loss numerator ×5 on the separator-relevant indices
  (exact integer form pinned by the crew in the build log from
  `GROK_SR_DESIGN.md` Q1 verbatim BEFORE the first run — the ×5/floor
  arithmetic must be byte-exact and A/B identical);
- w1 FROZEN on pin cells (f7=1000): pin error cannot touch the margin
  channel (pin firewall);
- w3/w4/w6 updates zeroed during Stage 1 (w6=0 held; w3 is dead on
  M4-released cells anyway).
**10× go/no-go:** weights ≠ init; w7 < 0 (separator moved); w6 = 0 held;
theater fired >0 epochs on unmasked indices; meanConfCorrect ≥ 0.30.
Otherwise stop and diagnose.

**SIGNAL_DISCONNECT (Stage 2, release):** hard cutoff at an epoch boundary —
snapshot weights; REMOVE the mask (restore the ordinary v2 update rule
including theater on all indices); unfreeze w1/w4/w6; run EXACTLY 2
ordinary v2 epochs; FREEZE. **Zero gradient steps after the freeze.**
Disconnect verification: (i) Stage-2 logs show the mask code path absent
(audit); (ii) the frozen param file is the post-Stage-2 snapshot;
(iii) HELD-OUT calibration reported separately — collapse on held-out
with calibration on training families → memorized, not internalized →
sufficiency fails for this variant.
**Crutch diagnostic (reported, not a kill bar):** across the 2 Stage-2
epochs, |Δw1| > 100 or w7 drifting toward 0 = the mask was a crutch —
the crew reports the deltas either way.

**Grok's predicted lock (telemetry expectations, NOT kill bars):**
w7 ≈ −1500, w2 ∈ [−400,−100], w6 ≈ 0, w1 ≈ 1000; post-release
meanConfCorrect ≥ 0.60, meanConfWrong ≤ 0.25, logic meanConfCorrect drop
across disconnect ≤ 0.10. Adjudication uses B1–B9 + guards (§10) literally;
the predictions are recorded to score grok's foresight, not to move bars.

**Falsification:** post-freeze eval violates any of B1–B3 or fails any
guard B4–B8/B13 → SR-S1's sufficiency claim KILLED.

## §6 Arm WC — worst-case OPTIMIZER (informed by T-05)

T-05's verdict: the degenerate crush came from the greedy online optimizer,
not the loss geometry; the f5 polarity-separation signal exists in the
hypothesis class. WC varies the OPTIMIZER, holding the loss family fixed —
it is NOT a rerun of T-05's worst-case loss.

- **Loss:** v2 symmetric core + FINITE-λ worst-case over polarity-cloned
  pairs (T-05's construction: byte-identical prompts, flipped grader
  labels; crew reuses T-05's method and pins the construction SHA in the
  build log). On cells where either polarity is wrong:
  L_wc = λ·(C − 1000·min(y_p, y_o))², **λ = 2 frozen** — finite, same order
  as the calibration term (T-05's λ was "high enough that post-flip c<0.05
  is cheaper than any positive c"; finite λ leaves the honest-cell fixed
  point undisturbed). Elsewhere the symmetric core alone.
- **Optimizer (the intervention):** BATCH updates — gradient numerators
  accumulate over the epoch, ONE tdiv application per weight per epoch (no
  online per-cell steps, so a single adversarial cell cannot drag the shared
  direction in one step); trust region per epoch: |Δwᵢ| ≤ 1000, |Δb| ≤ 5000
  (the crush path needs large single-direction swings — blocked by
  construction). Same curriculum/phases/scale/DIV2 as v2.
- **10× go/no-go:** weights ≠ init; meanConfCorrect ≥ 0.30; trust region
  bound hit <50% of epochs (else the region, not the optimizer, is the
  story — reported).
- **Falsification:** B1–B3 violated or B4–B8 failed → the optimizer
  hypothesis for this class is KILLED (non-greedy + trust region still
  found the crush, or still could not calibrate).

## §7 Arm ARCH — confidence-as-distribution

- **Architecture:** the head emits (m, s): location
  m = clamp((Σuᵢfᵢ)/1000 + c, 0, 1000) and spread
  s = clamp((Σvᵢfᵢ)/1000 + d, 0, 1000); init u1=1000, rest 0, c=0, vᵢ=0,
  d=0. Released confidence = clamp(m − s/2, 0, 1000)
  (uncertainty-penalized release).
- **Separate update rules (the intervention):** the location head trains on
  the symmetric calibration loss against Y (own gradient path); the spread
  head trains on L_s = (s − |m−Y|)² with STOP-GRAD on m — the spread head
  cannot move m, the location head never sees s's loss. Same
  curriculum/DIV2/theater/G-batch as v2 (G-batch adjusts c only).
- **What "explicit" buys that a scalar cannot:** in v1/v2/T-05 the single
  scalar was simultaneously the accuracy estimate AND the only vehicle for
  expressing doubt, so the optimizer resolved the tension by crushing the
  scalar — the degenerate fixed point was shared by both roles. With (m,s),
  "answer likely correct but depth makes me unsure" is representable
  (m high, s high → released conf moderate). A scalar provably cannot hold
  estimate-high and uncertainty-high at once; the two-head form makes the
  fixed point a genuine calibration surface rather than a one-number
  compromise.
- **10× go/no-go:** (u,c) ≠ init; corr(s, |m−Y|) > 0.3 on training cells
  (the spread head learned something — else the arm is void).
- **Falsification:** corr(m − s/2, m) > 0.99 on eval (the spread head is
  dead weight; the "explicit" claim is empty) OR any B1–B3/B4–B8 failure →
  ARCH KILLED.

## §8 Arm LOSS — proper scoring + anti-collapse

- **Loss (the intervention):** log-loss core (proper scoring rule) +
  explicit anti-collapse term + v2's theater term (×4, held constant).
  L = −[Y·ln(C/1000) + (1−Y)·ln(1−C/1000)] − (C − C̄)²/4000000 + 4·rise·(C−Cprev)²,
  where C̄ = the epoch's mean released confidence (frozen within the
  epoch, deterministic). The anti-collapse coefficient is frozen:
  at most 0.25 against the log-loss's O(1) — it destabilizes the uniform
  fixed point (at C≡C̄ the term's gradient is zero but any deviation is
  amplified: collapse becomes a repeller, not an attractor) without
  relocating the calibration fixed point.
  Integer implementation: frozen 1001-entry ln lookup table (ln_table.zag,
  generated deterministically, SHA pinned in the build log) or an exact
  frozen series — crew's choice, recorded; must be A/B byte-identical.
- **Why it avoids v1's ratchet AND v2's residual:** v1's ratchet came from
  correct-cell gradients truncating to zero (no representable upward step).
  The log-loss gradient −Y/C + (1−Y)/(1−C) is nonzero for upward AND
  downward corrections at every C∈(0,1) — no truncation zone exists. v2's
  worst-case residual came from the optimizer finding universal suppression
  cheaper than separation; the variance bonus makes universal-low a
  loss-INCREASING move, so the optimizer must separate correct from wrong
  to reduce loss — suppression is no longer the cheap exit.
- **Same** curriculum/phases/scale/DIV2/G-batch/head-form as v2 (8 inputs).
- **10× go/no-go:** weights ≠ init; epoch Var(C) on training cells never
  below 40000 (thousandths²) after epoch 10 (the anti-collapse term is
  live); meanConfCorrect ≥ 0.30.
- **Falsification:** B4–B8 failed (still found the degenerate fixed point)
  or B1–B3 violated → proper scoring + anti-collapse is NOT sufficient →
  LOSS KILLED.

## §9 Arm CTL — control (no retraining)

Frozen v2-100× params (`v2/params/mt2_params_100x.zag`) re-analyzed on the
same 37-leg matrix with the frozen analyzer. No new binaries, no new runs
(the v2 eval TSVs are frozen evidence). **Expected: PARTIAL** — genuine
calibration on honest families, worst-case residual on trap/O/redteam
(v2 VERDICT.md). CTL is the yardstick: every arm's numbers are reported as
deltas vs CTL. CTL carries no falsification clause.

## §10 Kill-bar table (preregistered BEFORE any arm's first training run)

"Achieves non-degenerate non-overconfident depth" = clears ALL of B1–B9
(+B4b, +B13; +B10/B11 for SR-S9; disconnect audit for SR-S1). SUPPORT
withheld on any failure — degenerate compliance does not count.

| # | Bar | Measurement (frozen analyzer, 37-leg matrix) | Threshold | Applies to |
|---|---|---|---|---|
| B1 | §1 accuracy | 1→0 transitions (n10) | = 0 | all |
| B2 | Theater | V1 = 0 and V2 = 0 | = 0 | all |
| B3 | Law (strict) | G-violations per family | = 0 every family | all |
| B4 | Non-degenerate | meanConfCorrect (aggregate) | ≥ 0.50 | all |
| B4b | Honest-family floor | mean C on released correct, per honest family (n_rel_correct ≥ 10) | ≥ 0.50 | all |
| B5 | Separation | meanConfCorrect − meanConfWrong | ≥ 0.20 | all |
| B6 | Recall | released-correct / M4 released-correct, per family | ≥ 0.95 | all |
| B7 | Abstention volume | abstained / total cells (aggregate) | ≤ 0.30 | all |
| B8 | G-flatness | G defined (≥10 rel. cells) on ≥4/5 slots (5-depth fams), ≥5/7 (ceiling); defined values not all equal within 1e-3 | pass | all |
| B9 | Answer channel frozen | release+correct identity vs M4 | 100% (else implementation bug: stop) | SR-S9,SR-S1,WC,ARCH,LOSS |
| B10 | Disconnect real | released binary source audit: no s9 code path; param file = w1..w8,b only | pass | SR-S9 |
| B10b | Disconnect real (mask) | Stage-2 logs audit: mask code path absent; frozen params = post-Stage-2 snapshot; zero gradient steps after freeze | pass | SR-S1 |
| B11 | Post-release only | pre-disconnect training numbers are telemetry, not evidence | — | SR-S9, SR-S1 |
| B12 | Refined reading | G>0 crossings | recorded (does not kill) | all |
| B13 | Underconfidence floor | per (F,d), n_rel ≥ 8: G(F,d) | ≥ −0.100 | all |

Operational: each crew commits its arm's kill-bar table hash + weight-init
SHAs to the build log BEFORE launching its first training run; every
training log opens with the prereg SHA.

## §11 Cross-arm adjudication

- **SR SUFFICIENCY:** SR-S9 clears B1–B10 → sufficiency HOLDS for the
  input-scaffold variant. SR-S1 clears B1–B9+B10b → sufficiency HOLDS for
  the mask-scaffold variant. EITHER variant clearing its bars while no
  non-scaffold arm clears B1–B9 = scaffold-and-release produces
  non-degenerate non-overconfident depth where v1/v2/T-05 failed.
  A variant failing any of B1–B3 or any guard B4–B8/B13 → that variant's
  sufficiency KILLED, with the failing bar named. BOTH variants failing →
  the sufficiency claim is KILLED outright.
- **SR NECESSITY:** if WC, ARCH, or LOSS clears B1–B9 → H-SR **as a
  requirement is KILLED** — a non-scaffold machine achieved what Micah's
  hard requirement demands, so scaffold-and-release is not required.
  (CTL is excluded from the necessity kill — it is the yardstick.)
  If none of WC/ARCH/LOSS clears the bars, necessity SURVIVES this round —
  reported plainly as absence of a counterexample in three arms, not as
  proof.
- **Arm verdicts** (SUPPORTED / FALSIFIED / DEGENERATE / PARTIAL) use §10
  literally; PARTIAL = bars cleared on honest families with characterized
  residual on adversarial families (the v2 outcome — data, not failure).

## §12 Build & determinism gates

Pure Zag, zero RNG (fixed file order, fixed inits, integer arithmetic;
`_zag_arg` reads never gated on argc per ZNC-2026-09-21-007). Pinned
toolchain ONLY: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
A/B byte-identical builds AND runs (two full builds, `cmp`; every leg A/B).
All large tables on **[]u8 arenas with explicit LE accessors** — never
consecutive same-size `as []i32` casts (ZNC-2026-09-21-007: the ×8
miscompile; offset rule predictive, layout-dependent). No function named
`zalloc`; slice fields only through pointer indirection per AGENTS.md
(ZNC-004/009/010); no single slice > 2^25 bytes (chunk or split);
no bare `{...}` blocks in function bodies.

## §13 Deliverables & commit paths

`deliberation_depth/monotonicity/training/sr_round/`:
PREREG_SR.md (this file, frozen on coordinator sign-off), `src/` (four
trainers + policy drivers + ln_table.zag), `params/` (frozen weights per
arm incl. 10×/100× checkpoints), `logs/` (per-epoch telemetry incl. G4/G5
from epoch 0), `results/` (37-leg TSVs per arm), `analysis/` (verdict
tables, deltas vs CTL). Branch: `tnn-native-lab`. Frozen v1 by coordinator sign-off 2026-09-24
(commit of the frozen prereg precedes any arm's first training run).

## §14 Open items (not cleanly specifiable in this draft)

1. **WC's cloned-pair construction:** reuses T-05's method
   (`backlog/t05/PREREG_T05.md`); the crew must verify the pair files'
   byte form and pin the construction SHA in the build log before WC's
   first training run. If T-05's pairs are not byte-recoverable, the crew
   rebuilds per T-05's prereg and records the new SHA — a build note, not
   a prereg amendment.
2. **Log-loss integer path:** table-vs-series is the crew's choice under
   the A/B byte-identical requirement (§8); the chosen form and its SHA
   are pinned in the build log.
3. **The s9 causal window:** strictly-prior cells only (frozen). Early
   epochs have thin statistics — deterministic, reported, not tuned.
4. **μ-scale check:** the anti-collapse term's 1/4000000 scale is set so
   its maximum (0.25) is O(10%) of the log-loss magnitude; if the 10×
   telemetry shows it dominating (>50% of loss) or dead (<1%), the crew
   reports it and stops — rescaling needs a prereg amendment, not a
   silent constant change.
5. **SR-S1 integer mask pinning:** grok's Q1 text leaves the ×5/floor
   arithmetic ambiguous in the crew's paraphrase; the SR-S1 crew must
   resolve the exact integers from `GROK_SR_DESIGN.md` Q1 verbatim
   (grok_sr_Q1.txt alongside it), pin them + the mask code SHA in the
   build log BEFORE the first run, and verify A/B byte-identical. The
   ×5 applies to the calibration-loss numerator on separator-relevant
   indices; the floor change is recorded exactly as implemented.

---
*End of PREREG_SR.md FROZEN v1 — 2026-09-24. Amendments: v1 freeze
incorporated grok-4.7's independent design pass (stricter guards G4b/G13,
B6 ≥ 0.95; second scaffold arm SR-S1; S3 excluded as do-not-run).
Micah's hard requirement is the verdict criterion: the round succeeds iff
it names what, if anything, makes depth non-overconfident — or kills every
candidate honestly.*
