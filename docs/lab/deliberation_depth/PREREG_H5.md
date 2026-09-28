# H5 — Deliberation Depth vs Accuracy: FROZEN MASTER PREREG (v1)

- **Status:** FROZEN — no measurement runs under this prereg yet. Any change requires H5 coordinator sign-off + version bump + re-measurement of affected legs.
- **Date:** 2026-09-23
- **Program:** H5 — "deliberation adapts to state, no fixed think-count" is law but unmeasured. Measure the curve, find the knee.
- **Hypothesis:** deeper deliberation improves judgment quality; the accuracy-vs-depth curve has a knee (diminishing returns), and a state-adaptive stopping rule matches fixed-deep accuracy at lower cost.

## §1 Frozen inputs (Phase 1 commits, verified on branch tnn-native-lab)

| Artifact | Commit | Path |
|---|---|---|
| Depth definition (DEPTH_DEF.md v1) | `248392f20ac52f9b4d51841a8da450ae8b4919ea` | `docs/lab/deliberation_depth/DEPTH_DEF.md` |
| Harness (pure Zag, determinism proven on smoke) | `e45b5f536d9d7c31798d856bbd7ef277057d4f6a`, `f57760b3267c73df9d14989be6f87feaed42d2b7` | `docs/lab/deliberation_depth/harness/` |
| Batteries (625 items, program-verified GT) | `50a62d38c8353eff2169e5a676c45b046f81729f` | `docs/lab/deliberation_depth/batteries/` |
| Red-team batteries (252 items) + plan | `ba05b096f12ee7dd7404838c95845330d2a7da5a` | `docs/lab/deliberation_depth/redteam/` |

Depth config values (from DEPTH_DEF.md §5, frozen): `rounds_shallow=2`,
`rounds_deep=16`, `rounds_baseline=1`, `sweep_rounds=1,2,4,8,16`,
`adaptive_epsilon=0.02`, `adaptive_k=3`, `adaptive_cap_rounds=16`
(= rounds_deep, enforced), `round_min_work=1`. Adaptive rule (§6): after
round r, stop iff r ≥ k and |c_i − c_{i−1}| < ε for the last k rounds;
cap → stop with `cap_hit=true`. Confidence = deterministic function of
deliberation state (harness-frozen margin formula), [0,1] fixed-point.

Batteries: admit 248 (PAM gate dispositions), revoke 113 (FL2 red-team
verdicts), logic 264 (hell-hole verifier verdicts). Red-team: trap 127
(shallow answer always wrong), cost 125 (each with `optimal_stopping_depth`
d* ∈ {1,2,3} and `gain_vanishes_proof`).

## §2 Measurement matrix (frozen)

Every battery item × every sweep point {1,2,4,8,16} × ADAPTIVE, run through
the frozen harness at the frozen commits above. Per-run record per
DEPTH_DEF.md §7: `item_id | level | rounds_used | evidence_items |
hyp_considered | hyp_eliminated | audit_steps | conf_final | judgment |
correct | cap_hit | config_sha`.

Gates (all must pass or the run is invalid):
1. **Determinism gate:** every (item, level) run twice; records byte-identical. Any mismatch = harness bug: stop, fix, re-run.
2. **Config freeze:** `config_sha` identical across all runs; any deviation = re-run.
3. **Trap validation (pre-analysis):** the depth-1 baseline must select `shallow_answer` on ≥90% of trap items per family; a family it doesn't fall for is a weak trap — report it, do not silently drop it.

## §3 Decision rules (frozen — these settle the hypothesis)

**Primary — the knee** (DEPTH_DEF.md §8.3): accuracy vs rounds, x-axis log2,
pooled over batteries and per battery. `d(p) = acc(p) − acc(p/2)` in
percentage points, p ∈ {2,4,8,16}. Knee = smallest p with d(p) < 1 AND all
later d(q) < 1. No such p → verdict KNEE-BEYOND-RANGE (report, do not
extrapolate). Secondary: max-curvature point. Tertiary: accuracy vs mean
audit_steps. All three reported; the knee rule governs the headline.

**Adaptive vs fixed** (the law's test): ADAPTIVE-WINS iff
|acc_adaptive − acc_deep| ≤ 1pt AND mean(audit_steps_adaptive) <
mean(audit_steps_deep) AND censoring check passes (< 1/3 cap hits).
ADAPTIVE-TIES-DEEP iff accuracy within 1pt but cost not lower.
ADAPTIVE-LOSES otherwise. Censoring ≥ 1/3 cap hits → verdict CENSORED:
adaptive leg invalid, §12 amendment required, no knee read off it.

**Trap/cost batteries:** report accuracy-vs-depth curves separately.
Expectations (not kill bars): SHALLOW accuracy on traps ≪ DEEP
(validates headroom); DEEP mean rounds_used on cost attacks ≫ d*
(validates the cost axis); ADAPTIVE rounds_used should track d*.

**Cost analysis:** mean audit_steps per level per battery; accuracy per
audit-step (efficiency frontier); the knee restated in cost space.

## §4 Analysis deliverables

`RESULTS_H5.md`: per-battery curves + pooled curve (tables, accuracy at
each sweep point with n), knee verdict per rule, adaptive-vs-fixed verdict,
censoring fractions, cost tables, trap/cost battery results, every
held/broken expectation, honest limitations (incl. harness's pre-encoded
evidence scope note; Sol second-opinion deferred). All evidence committed:
per-run records, ledgers, analysis scripts, byte-identical rerun proofs.

## §5 Standing constraints

Pure Zag for the judge/harness; zero RNG in any decision path;
byte-identical reruns; commit via `~/workspace/commit_racefree.py` with
lab-relative paths (`deliberation_depth/...`), `TMPDIR=~/workspace/tmp_commit`;
no binaries, no `.zagd`. ε/k tuning post-data is inadmissible without
amendment + re-measurement.

## §6 Amendments

Coordinator sign-off + version bump + re-measurement of affected legs.
The deferred Sol second-opinion pass on DEPTH_DEF.md enters here if it
surfaces a defect.
