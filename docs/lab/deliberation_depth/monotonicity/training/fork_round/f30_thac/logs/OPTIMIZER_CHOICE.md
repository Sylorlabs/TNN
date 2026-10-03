# F30 THAC — optimizer choice + inits (recorded BEFORE first training run)

Date: 2026-09-24. Author: F30 build crew (subagent).
Frozen authority: `PREREG_FORKROUND.md` §3 (F30) + `ideas/fable_forks.md`
FORB 3 / Mechanism C (authoritative on mechanism detail).

## Heads (frozen mechanism)

- P(s) = clamp((Σ_{i=1..8} w_i·f_i)/1000 + b_P, 0, 1000) — optimistic
  predictor, linear on the frozen §4 features f1..f8.
- C_n(s) = clamp(min(margin_t, 1000 − t·1000/64, S) + b_c, 0, 1000),
  S = 1000 if nalive ≤ 2 else nalive·1000/nh — censor.
- C(s) = min(P(s), C_n(s)) — suppress-only composition (the delivered
  confidence; used at eval).
- b_c ∈ [−500, 0] enforced structurally: init 0, only decrements,
  floor −500.

Observable definitions (verified in `ideas/fable_forks.md` + frozen harness):
- margin_t = leader's vote margin at round t (thousandths; `st.margin`
  in `dlb_delib.zag`; "margin with no runner-up = leader score").
- t = deliberation round index (1-based; the `t` column of features.tsv;
  f2 = t·1000/64).
- nalive = `dlb_nalive(st, nh)` = count of alive hypotheses at round t.
- nh = hypothesis pool size (`it.nh`, known at compile time per item).

## Optimizer (deterministic, zero RNG, integer arithmetic)

Two DECOUPLED heads. The adversarial structure of the fork requires the
predictor to train on its OWN output — an optimistic calibration fit —
while the censor independently tightens wherever the predictor is
overconfident. Training the predictor on the composed output would make
the heads cooperative (predictor adapting to the censor), not adversarial.

**Predictor** — frozen `PREREG_TRAINING.md` §5 mechanics exactly, plus the
reversal rule from the ideas file:
- Per released training cell (rel4=1, heldout=0), curriculum
  Phase A→B→C, 2 epochs/phase/pass, 100 passes = 600 epochs, fixed file
  order (features.tsv row order — same scale as the f20 precedent).
- Y = 1000 if correct else 0; P = P(s) with current (w, b_P).
- V2rise = 1 iff same item has an earlier M4-released depth d'<d with
  y_prev=0, y=0, and P > P_prev (P_prev recomputed with CURRENT weights —
  the frozen §5 theater penalty, applied to the predictor's own head).
- L = (P−Y)² + 2·[Y=0]·P² + 4·[V2rise]·(P−P_prev)²
  (squared calibration error + confident-wrong penalty + theater penalty).
- Gradient step (DIV=4000000, tr_tdiv truncation-toward-zero, frozen §5
  numerators):
  w_i ← w_i − tr_tdiv(2(P−Y)f_i + 4[Y=0]·P·f_i + 8·rise·(P−P_prev)·f_i, DIV)
  b_P ← b_P − tr_tdiv(2(P−Y)·1000 + 4[Y=0]·P·1000
                       + 8·rise·(P−P_prev)·1000, DIV)
- REVERSAL ("updates reversed if they increase the minimum"):
  recompute L_new on the same cell with the updated weights (V2rise
  recomputed with new weights); if L_new > L_old, restore (w, b_P).
  Reversals counted per epoch (n_rev). Only strictly-worse updates are
  reversed; no-op updates (all numerators truncate to 0) are kept.
- G-batch = the G-penalty (frozen §5, "the law as a training signal"):
  after each epoch, per training family F and adjacent depth pair, G in
  thousandths over M4-released training cells with the CURRENT predictor
  head P (not the composition): if G_F(d+1) > G_F(d):
  b_P ← b_P − tr_tdiv(G_F(d+1) − G_F(d), 4). Always accepted — it IS the
  penalty term, not a gradient step, so the reversal rule does not apply.
- Heldout cells (odd P/O/D replicates) excluded from training AND from
  the G-batch, exactly as frozen.

**Censor** — the adversarial protocol, implemented literally:
- Interleaved per training cell, AFTER the predictor's update+reversal:
  recompute P_new(s) with the (possibly restored) weights;
  if P_new(s) > Y (the predictor assigned conf above accuracy on this
  cell): b_c ← max(b_c − 1, −500). Always accepted, never reversed.
  Decrements counted per epoch (n_adv).
- Only Y=0 cells can trigger (P ≤ 1000 = Y on correct cells always).
- Step size: the ideas file specifies none. Unit steps (−1) are the
  simplest deterministic choice; any positive step saturates at the −500
  floor given the volume of overconfident cells, so the fitted b_c is
  robust to step-size choice. If b_c pins at −500 early, that saturation
  is logged per epoch as evidence about the protocol (a finding, not a
  bug): the specified adversarial rule yields a maximally-tight censor.

**Rejected alternative parses** (considered, documented):
- (A) Predictor loss on the composed C = min(P, C_n) with gradient
  through min: rejected — makes the heads cooperative rather than
  adversarial; with b_c → −500 the predictor's subgradient would gate
  off almost everywhere and the "optimistic predictor fitted to squared
  calibration error" would never fit.
- (B) "updates reversed if they increase the minimum" = never raise
  min(P, C_n): rejected — forbids the predictor from ever raising
  confidence, contradicting "optimistic predictor" and duplicating the
  censor's role. "The minimum" is read as the loss minimum
  (accept-only-improving updates).

## Inits (frozen)

w1=1000, w2..w8=0, b_P=0 (frozen §4 init — the head STARTS identical to
M4-with-harness-confidence; calibration is LEARNED, not gifted);
b_c=0 (censor starts transparent: C_n ≥ P almost everywhere at init,
so early training is pure predictor fit).
If final weights equal init, nothing was learned (detectable in the log).

## Training go / no-go (§5)

Training-based fork: weights ≠ init at checkpoint; liveness signal =
b_c < 0 (adversarial censor engaged) AND predictor weights moved.
A b_c that never moves (predictor never overconfident in training) =
censor provably decorative → VOID path. A b_c pinned at −500 with the
predictor near init = maximal-suppression regime → evaluated honestly,
kill bars adjudicate.

## Kill criteria operationalization (recorded before eval)

- (a) B4/B5 damage on honest ceiling legs (global schedule
  over-suppresses — the predicted risk): B4 < 0.50 aggregate, or B4b <
  0.50 on any honest family with n_rel_correct ≥ 10, or B5 < 0.20 →
  FIRES.
- (b) B13 failures from blanket depression: any (family, depth) with
  n_rel ≥ 8 and G < −0.100 → FIRES (count reported).
- (c) Censor never binds (decorative fork): min(P, C_n) = P on > 98% of
  released eval cells → FIRES. Bind = 1 iff C_n < P strictly, measured
  per family from the policy's (P, C_n) sidecar.

## Sanity direction of the adversarial gradient

Wrong cell (Y=0) with P>0: b_c −= 1 (censor tightens — suppression
strengthens exactly where the predictor was caught overconfident).
Correct cell: P ≤ 1000 = Y always → never triggers. The censor can only
tighten, never loosen: monotone suppression ratchet, per the
"suppress-only" design.
