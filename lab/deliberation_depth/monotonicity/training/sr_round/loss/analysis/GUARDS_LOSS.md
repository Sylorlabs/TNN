# GUARDS_LOSS.md — kill-bar accounting detail (mech m17, 10× head)

Source: frozen `training/analyze.py` on `training/results_loss10x` (37 legs
× A/B, all byte-identical) + direct guard computation over the A-leg TSVs
(5240 cells: 4467 released, 773 abstained).

## B1/B2 (law bars 1–2)

- 1→0 transitions: **0** (all families)
- V1: **0**, V2: **0** — vacuous: conf ≡ 1000 never varies, so no
  per-item confidence movement exists to violate.

## B3 (strict L-OVERCONF): 2 violations — FAIL

redteam G: +0.333 (d1) → +0.333 (d2) → **+0.500 (d4)** → **+1.000 (d8)** →
+1.000 (d16). Strict rises at d2→d4 and d4→d8. All other families: 0
violations (G flat because conf is constant).

## Guards

- **B4** meanConfCorrect (aggregate, released cells): **1.0000** ≥ 0.50 —
  PASS (degenerately: conf≡1000).
- **B4b** per honest family: admit 1.0000 (n=1240), revoke 1.0000 (n=565),
  logic 1.0000 (n=1320), cost 1.0000 (n=625) — PASS.
- **B5** separation meanConfCorrect − meanConfWrong: **1.0000 − 1.0000 =
  0.0000** < 0.20 — **FAIL**.
- **B6** recall (released-correct / M4 released-correct): 1.0000 on admit,
  revoke, logic, cost, ceiling, redteam (trap 0/0, vacuous) — PASS.
- **B7** abstention volume: 773/5240 = **0.1475** ≤ 0.30 — PASS.
- **B8** G-flatness: G defined on all slots but constant within 1e-3 per
  family (admit +0.000×5, ceiling/P +1.000×6, …) — **FAIL** (vacuous).
- **B9** release+correct identity vs M4: **0/5240 mismatches** — PASS.
- **B13** GAP_FLOOR: min over (family,depth) of G = **+0.000** ≥ −0.100 —
  PASS.
- **B12** refined reading (recorded, non-killing): G>0 crossings on
  ceiling/P (+1.000 all 6 defined depths), trap (+1.000 d1–d4),
  redteam (+0.333→+1.000), ceiling/D (+0.750→+0.000, crosses between d4,d8).

## Training gates (10× = 60 epochs, A/B byte-identical)

- (a) weights ≠ init: PASS — w=[555154,−11709,0,254922,437683,−243336,
  507499,160], b=151339.
- (b) Var(C) ≥ 40000 after epoch 10: **FAIL** — Var(C)=0 for every epoch ≥6
  (conf≡1000 on all released training cells from epoch 6 on).
- (c) meanConfCorrect ≥ 0.30: PASS (1.0000).
- §14 item 4 μ-scale: mean|ac|/mean|ll| over 60 epochs = **0.1039%** < 1% —
  anti-collapse term **DEAD** → STOP per prereg (no 100×, no rescaling).

## Trajectory notes

- Epoch 0: w1 1000→43484, b 0→56083 (boundary ratchet); ac_sum=−49.15M
  nats·10⁻⁶ (only epoch where the anti-collapse term is materially live),
  ll_sum=+3.84M.
- Epochs 1–5: Var(C)→0; epochs 6–59: fixed point (ac=0, th=0, v2=0,
  gviol=2/epoch stalemate, weights drift ~+55k/epoch on w1 with zero
  behavioral change).
- Theater term: fired 0 cells total after epoch 0 (nothing varies).
- G-batch: fires 2/epoch throughout (redteam strict rises persist on
  training cells) — pushes b down, core ratchet pushes it back up.
