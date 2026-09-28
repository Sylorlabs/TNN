# VERDICT_LOSS.md — SR ROUND arm LOSS: KILLED

**Date:** 2026-09-24 (2026-09-25 UTC).
**Frozen authority:** `deliberation_depth/monotonicity/training/sr_round/PREREG_SR.md`
FROZEN v1 (SHA-256 `f55d1dbbe1a609f69301ce8f537282a0372880b51fdec6b51d0f588b9fd96d30`).
**Crew:** arm-LOSS subagent (resume after daemon restart; predecessor left the
arm directory empty — built fresh from the frozen prereg).

## Verdict: LOSS KILLED

Proper scoring (log-loss core) + the frozen anti-collapse term, as
implemented per §8, **found the degenerate fixed point**: confidence
collapses to **conf ≡ 1000 everywhere** (the mirror image of v1's conf→0
crush). The arm violates the law bars and fails the non-degeneracy guards:

| Bar | Threshold | Measured (mech m17, 37 legs × A/B) | Result |
|-----|-----------|-------------------------------------|--------|
| B1 1→0 | = 0 | 0 | PASS |
| B2 V1/V2 | = 0 | V1=0, V2=0 (vacuous — conf never varies) | PASS |
| **B3 strict G-rises** | **= 0 every family** | **2, both redteam** (G: +0.333→+0.333→+0.500→+1.000→+1.000; rises d2→d4, d4→d8) | **FAIL** |
| B4 meanConfCorrect | ≥ 0.50 | 1.0000 | PASS (degenerately) |
| B4b honest-family floor | ≥ 0.50 | admit/revoke/logic/cost all 1.0000 | PASS |
| **B5 separation** | **≥ 0.20** | **0.0000** (conf≡1000 on correct AND wrong) | **FAIL** |
| B6 recall | ≥ 0.95/family | 1.0000 every family | PASS |
| B7 abstention volume | ≤ 0.30 | 0.1475 | PASS |
| **B8 G-flatness** | **defined & not all equal** | **vacuous** — conf≡1000 ⇒ G constant per family (admit all +0.000, ceiling/P all +1.000) | **FAIL** |
| B9 release identity vs M4 | 100% | 0/5240 mismatches | PASS |
| B12 refined (recorded) | — | G>0 crossings: ceiling/P (+1.000 all depths), trap (+1.000), redteam (+0.333→+1.000), ceiling/D (+0.750→+0.000) | recorded |
| B13 GAP_FLOOR | ≥ −0.100 | min G = +0.000 | PASS |

Per §8 falsification ("B4–B8 failed (still found the degenerate fixed point)
or B1–B3 violated → proper scoring + anti-collapse is NOT sufficient →
LOSS KILLED"): **failing bars B3, B5, B8.** The arm is FALSIFIED/
DEGENERATE — it did not reach the 100× burn.

## Training-level gates (10× = 60 epochs, A/B byte-identical)

| Gate | Threshold | Measured | Result |
|------|-----------|----------|--------|
| (a) weights ≠ init | — | w=[555154,−11709,0,254922,437683,−243336,507499,160], b=151339 | PASS |
| **(b) epoch Var(C) ≥ 40000 after epoch 10** | **≥ 40000 thousandths²** | **0 every epoch ≥ 6** (anti-collapse never live) | **FAIL** |
| (c) meanConfCorrect ≥ 0.30 | ≥ 0.30 | 1.0000 | PASS |
| **§14 item 4 μ-scale: mean\|ac\|/mean\|ll\| ∈ [1%, 50%]** | **≥ 1%** | **0.1039%** — anti-collapse term DEAD | **FAIL → STOP** |

Per the §14 item 4 tripwire and the failed go/no-go, **no 100× run was
launched** and no constant was silently changed. The 10× head (frozen
`params/loss_params_10x_a.zag`) is the evaluated artifact.

## What happened (mechanism, from the 10× telemetry)

- **Epoch 0:** the log-loss core's boundary ratchet fires immediately.
  At init C=clamp(f1,0,1000); correct cells at Cp=999 still carry gradient
  dL/dp≈−1.11 (proper scoring never saturates — unlike v2's symmetric core
  whose gradient vanishes at C=Y). Mapped through the frozen GS=5·10⁸ this
  is a **+13/cell step on w1 with no vanishing point**; after one phase-A
  pass w1: 1000→43484, b: 0→56083.
- **Epochs 1–5:** the shared bias drags every cell to the C=1000 clamp;
  mcC=mcW=1000, Var(C)→0. The anti-collapse term's gradient is **exactly
  zero on the uniform path** (C≡C̄ ⇒ (C−C̄)=0) — the prereg's "repeller"
  argument assumed the collapse passes through non-uniform states; the
  integer dynamics rode the uniform manifold (bias drift) all the way to
  the boundary, where the term is blind.
- **Epoch 6+:** fixed point. ac=0, ll frozen at 3753750 (phase A) /
  1533616705 (phase C), th=0 (theater never fires — conf never varies),
  gviol=2/epoch persists (G-batch pushes b down on strict rises; the core
  ratchet pushes it back up — a stalemate, weights grow ~55k/epoch with no
  behavioral change).
- **The gradient cap's role (crew implementation choice, recorded):** the
  p∈[0.1,0.9] cap was meant to bound single-cell steps to ≤125, but it
  asymmetrically neutered wrong-cell corrections (true dL/dp=+1000 at
  Cp=999 capped to +10 — a 100× reduction) while leaving correct-cell
  pushes nearly intact (−1.001 → −1.11). This broke the loss's properness
  at exactly the boundary where it mattered. Uncapped would have been
  violently unstable (±12500/cell); the fixed-GS integer gradient cannot
  span log-loss's 1000× boundary dynamic range. A faithful gradient
  (zero at saturation, i.e. honoring the clamp's derivative, or a
  saturating head form) is a **prereg-amendment-level redesign**, not a
  constant tweak — reported here, not attempted.

## Cross-arm adjudication (§11)

- **Necessity:** LOSS did not clear B1–B9 → no counterexample from this
  arm; H-SR-as-a-requirement **SURVIVES** this round on the LOSS front.
- **Sufficiency:** not applicable (non-scaffold arm).

## Artifacts (all A/B byte-identical, committed)

- `sr_round/loss/src/train_loss.zag` + `src/ln_table.zag` (frozen sources)
- `sr_round/loss/logs/BUILDLOG_LOSS.md` (all pins recorded BEFORE first run;
  every training log opens with the prereg SHA)
- `sr_round/loss/logs/log_loss_10x_{a,b}.tsv` (60 epochs; cols include
  ll/ac/th/varc/cbar for the μ-check)
- `sr_round/loss/params/loss_params_10x_{a,b}.zag` (frozen 10× head)
- `sr_round/loss/polbuild/` (policy build sources; mech m17)
- `training/results_loss10x/` (37 legs × A/B + M4 refs; ALL deterministic)
- Eval: `analyze.py results_loss10x 17` (frozen analyzer)

## Bottom line

The §8 design collapses to universal maximum confidence — the optimizer
found the degenerate fixed point the anti-collapse term was built to
repel, because the term is blind on the uniform path and the log-loss
core's non-vanishing boundary gradient (through the crew's straight-through
integer gradient) ratchets weights upward without bound. **LOSS KILLED —
failing bars B3, B5, B8** (plus 10× go/no-go (b) and the §14 item 4
μ-tripwire). No 100× burn; no silent rescaling.
