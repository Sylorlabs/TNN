# VERDICT — F28 DEB (Differential Evidence Budget), mech 28

Date: 2026-09-24. Frozen authority: PREREG_FORKROUND.md §3 (F28) +
ideas/fable_forks.md Mechanism A. Full 37-leg battery. Adjudication per §10.

## Verdict: KILLED — failure-mode (1) clamp attractors

Kill trigger (b) FIRES: the per-item budget pins at 1000 on 100% of cells
in ALL 37 legs (threshold: >50% in any leg). The mechanism as frozen is a
pure clamp attractor: confidence = 1000 on 4467/4467 released cells.

## Why (structural, measured not asserted)

The frozen head:
- budget_0 = 1000
- budget_t = clamp(budget_{t-1} + margin_t*(1000/nh) − t*1000/64, 0, 1000)
- C = clamp(min(budget_t, clamp(margin_t*1000/nh, 0, 1000)), 0, 1000)

Frozen-feature margin scale (f1): means 562–938 across families, max 1000,
zero zeros. Per-round replenishment = margin_t*(1000/nh): ≥111 (admit,
nh=9) up to 500,000 (trap/cost/ceiling, nh=2). Per-round charge =
t*1000/64 ≤ 1000. Replenishment exceeds charge by 2–3 orders of magnitude
at every round, so the budget can never deplete: budget_t ≡ 1000 for every
item at every depth, on every leg (probe-measured, 5240/5240 cells).

The head therefore reduces exactly to C = clamp(margin_t*1000/nh, 0, 1000),
verified conf == margin_score on 4467/4467 released cells — the budget never
binds. Since observed margins satisfy margin_t ≥ nh essentially everywhere,
C saturates: conf = 1000 on 100% of released cells. The "differential"
budget is vacuous; F28 is a constant-1000 head wearing a budget costume.
This is failure-mode (1), not a training or tuning problem: no fittable
parameter exists that could change it (the charge coefficients are
structural constants, and any α_div ≥ 1 still over-replenishes at real
margin scales — the formula's fixed-point scaling is off by ~1000×).

## Kill-bar table (frozen analyzer semantics; B8 amended §4b)

| Bar | Result |
|---|---|
| B1 1→0 | 0 → PASS |
| B2 theater | V1=0 V2=0 → PASS (vacuous: constant conf cannot rise) |
| B3 strict | 2 violations (redteam d2→d4, d4→d8; tiny-n, n=3,2,1) → FAIL |
| B4 non-degenerate | meanConfCorrect = 1.0000 → PASS |
| B4b honest floor | 1.0000 on all honest families → PASS |
| B5 separation | 1.0000 − 1.0000 = 0.0000 → FAIL |
| B6 recall | 1.00 every family (2 vacuous) → PASS |
| B7 abstention | 773/5240 = 0.1475 → PASS |
| B8 amended | admit/cost/logic/revoke PASS (perfect-cal); ceiling D/O PASS; ceiling P FAIL (VACUOUS: G≡+1.000); redteam/trap VOID |
| B9 frozen channel | 5240/5240 release+correct identity vs M4 → PASS |
| B13 | 0 (F,d) with G < −0.100 → PASS |
| B12 (recorded) | G>0 crossings: D:3, P:6, redteam:5, trap:3, else 0 |
| B3pi (recorded) | 0 rising / 3467 adjacent released pairs |

## F28 falsification triggers
- (a) strict B3 no better than NEC m9: F28 Gviol=2 vs NEC m9 Gviol=6 → CLEAR
  (better than NEC, but still fails strict B3).
- (b) clamp attractor: budget pinned at 1000 on 100% of cells, 37/37 legs → KILL.
- (c) B4 < 0.50 honest: 0 hits → CLEAR.

## Q2 prediction vs per-family split (F28 Gviol vs NEC m9 Gviol)
admit 0/0, revoke 0/0, logic 0/0, trap 0/0, cost 0/0, redteam 2/2,
ceiling D 0/0, ceiling O 0/4, ceiling P 0/0.
Q2 predicted beats-NEC on logic/admit deep and loses on redteam/trap: NOT
borne out — the only delta is ceiling/O (0 vs 4), everywhere else tied.
With conf ≡ 1000, G(d) = 1 − acc(d), so F28's G-violations are just
accuracy drops across adjacent depths; its "win" over NEC is an artifact
of constant confidence, not of budget dynamics.

## §10 adjudication
KILLED (kill trigger (b) fired + B3/B5/B8 failures; failure-mode (1)
clamp attractors). Not DEGENERATE-classified: it fails the law bars
outright. Not VOID/STILLBORN: the mechanism built and ran cleanly —
37/37 legs A/B byte-identical, B9 100%. The death is in the frozen
formula's fixed-point scaling, confirmed by exact integer re-simulation
in the probe (shares deb.zag with the eval binary).

No long-horizon leg per §6 (short-battery kill).
No new failure mode: FM1 covers it.
