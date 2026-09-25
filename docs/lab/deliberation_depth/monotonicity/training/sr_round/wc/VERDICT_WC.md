# VERDICT_WC.md — SR Round Arm WC (worst-case OPTIMIZER): FALSIFIED

Date: 2026-09-24. Prereg: PREREG_SR.md FROZEN v1 (SHA-256
`f55d1dbbe1a609f69301ce8f537282a0372880b51fdec6b51d0f588b9fd96d30`).
Arm spec: §6. Kill bars: §10 table (hash
`c4f5dfd8723efc3c46cb57f6c9a147449bc89ce4414ff7a146745304375be1d0`).

## Verdict: FALSIFIED

The claim — "a non-greedy optimizer (batch updates + per-epoch trust
region) with a finite-λ worst-case loss finds the non-degenerate
calibration fixed point that T-05's greedy online optimizer crushed" —
fails. The batch+trust-region optimizer found the crush anyway: logic
correct-cell mean confidence collapses 1000 → 124 (B4b), D/O families
sit at conf≡0 on correct cells (G = −1.000), and the strict law is
violated on 6 adjacent-depth pairs. Per §6, "B1–B3 violated or B4–B8
failed → the optimizer hypothesis for this class is KILLED". Both fired.

## Kill-bar accounting (frozen analyzer, 37-leg matrix, A/B byte-identical)

| Bar | Result | Number |
|---|---|---|
| B1 1→0 transitions = 0 | PASS | 0 |
| B2 theater V1=0, V2=0 | PASS | V1=0, V2=0 |
| B3 strict G-violations = 0 | **FAIL** | 6 (admit 2, cost 1, logic 1, redteam 1, revoke 1) |
| B4 meanConfCorrect ≥ 0.50 | **FAIL** | 0.4880 |
| B4b honest-family floor ≥ 0.50 | **FAIL** | logic 0.1242 (n=1320), revoke 0.4814 (n=565); admit 0.8177, cost 0.7894 pass |
| B5 separation ≥ 0.20 | PASS | 0.4783 |
| B6 recall ≥ 0.95/family | PASS | 1.0000 all 7 families |
| B7 abstention ≤ 0.30 | PASS | 0.1475 |
| B8 G-flatness | **FAIL** | trap: G defined (≥10 rel. cells) on 2/5 slots (d1=127, d2=85, d4=5, d8=0, d16=0) |
| B9 answer channel frozen | PASS | 5240/5240 release+correct identity vs M4 |
| B12 refined (recorded) | 4 crossings | ceiling/D d1 +0.016, ceiling/P d1 +0.028, redteam d8/d16 +0.234 |
| B13 G ≥ −0.100 | **FAIL** | worst −1.0000 (ceiling/D d8, nrel=10; also O/logic families) |

## What happened (mechanism)

1. **Crushed (same class as T-05, different optimizer).** The finite-λ
   worst-case term (λ=2 on released P/O cells) still dragged the shared
   feature direction into a degenerate fixed point: logic d1
   released-correct cells get conf = 0.0 exactly (n=264, min=max=0);
   ceiling/D d8 released-correct conf = 0.0 (n=10); ceiling/O conf≡0
   wherever accuracy = 1. The batch optimizer did not protect the
   f5-separation fixed point — final w4 (f5) = −4459, w1 = −27558,
   b = +17073: the weights marched steadily for 600 epochs without
   converging.
2. **Still violated.** B3: 6 strict G-rises — all are underconfidence
   shrinking with depth (admit −0.718→−0.097→−0.032; logic/cost/revoke
   −1.000→−0.845/−0.398 rises at d1→d2), i.e. the arm is maximally
   underconfident at d1 and "recovers" upward — the strict bar counts
   every rise. B12 (refined): 4 G>0 crossings, including redteam d8/d16
   at +0.234 — genuine overconfidence on the adversarial family, so the
   arm fails under both L-OVERCONF readings.
3. **Guard-failed.** B4 0.4880 < 0.50; B4b logic 0.1242 / revoke 0.4814;
   B13 −1.0000 (conf≡0 with acc=1.0 is exactly the degenerate
   suppression T-05's D-guards were built to catch).
4. **B8 note (battery-driven, flagged):** trap d8/d16 have 0 released
   cells and d4 has 5 under the frozen M4 skeleton; B9 = 100% identity
   means NO compliant arm can change release counts, so B8-trap is
   unpassable by construction on this battery. Reported literally as
   FAIL per §10, but it does not discriminate arms — the kill rests on
   B3/B4/B4b/B13 regardless.

## Training telemetry (for the record)

- 10× go/no-go: PASS — weights≠init; meanConfCorrect=0.498 ≥ 0.30;
  trust-region bound hit 22/60 epochs (36.7% < 50%).
- 100× (600 epochs): trust-region bound hit 360/600 epochs (60%) —
  per the prereg note, at 100× "the region, not the optimizer, is the
  story" for the dynamics, but it does not change the verdict: the
  bound was doing exactly its job (capping swings at ±1000/±5000) and
  the crush still won.
- Phase oscillation persisted all 600 epochs (phase A → saturation
  toward conf=1000; phases B/C → crush toward conf=0) — the batch
  optimizer turned T-05's per-cell drag into a per-epoch tug-of-war and
  lost it.
- Determinism: trainer build A/B byte-identical; 10× and 100×
  params+logs A/B byte-identical (two full runs each, cmp); policy
  binaries A/B byte-identical; 37/37 eval legs A/B byte-identical.

## Consequences

- **Optimizer hypothesis for this class: KILLED.** Non-greedy
  (batch) + trust region + finite λ=2 still found the degenerate crush
  and still violated the law. The binding constraint is not the
  optimizer's greediness — batching the updates did not save the
  separating fixed point.
- **H-SR necessity (§11): SURVIVES this round on the WC front** — no
  non-scaffold counterexample from this arm. (ARCH/LOSS adjudicate
  separately.)
- **Grok's independent prediction (P=0.38, highest-ranked arm):
  FALSIFIED** — recorded for scoring. The highest-probability
  intervention failed; the crush class is more robust than predicted.
- For Micah's hypothesis (depth-overconfidence is trainable away):
  second clean negative data point alongside T-05 — the "right" loss
  with a non-greedy optimizer still failed non-degenerately. The
  failure mode is now characterized in two flavors: T-05's greedy
  per-cell crush (logic 1000→67) and WC's batch phase-oscillation crush
  (logic 1000→124, D/O conf≡0).

## Artifacts

- src/train_wc.zag (trainer), src/policy.zag + src/mt_gate.zag +
  frozen dlb_*.zag (verified byte-identical copies)
- params/wc_params_10x.zag, params/wc_params_100x.zag (frozen weights)
- logs/BUILDLOG_WC.md (pins, inherited state, design decisions),
  logs/log_wc_10x.tsv, logs/log_wc_100x.tsv (per-epoch telemetry)
- results/ (74 WC TSVs, A/B per leg) + frozen M4 reference TSVs
- analysis/analyze_wc.py (imports frozen training/analyze.py; strips
  its module-level main()), analysis/killbars_wc.txt (this table)
- run_eval_wc.sh (37-leg runner adapted from frozen run_eval.sh)
- Commits: de27c282 (build+training) + this verdict commit; no
  binaries/.zagd committed.

*End of VERDICT_WC.md — 2026-09-24. The optimizer hypothesis for this
class is dead; the crush is robust to batching + trust regions.*
