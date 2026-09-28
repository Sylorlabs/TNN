# ADDENDUM Q3 — B13-at-scale: diagnosis plan, fixture designs, principles, target

- **Date:** 2026-09-25 (pre-FIX-run; diagnosis D1/D2/D3 measured before FIX batteries)
- **Crew:** Q3 (B13 degradation with scale)
- **Parent:** `PREREG_NCAL_V3_FOLLOWUP_FROZEN.md` (frozen `3edb49e87b91`) §3 — the amendment governs.
- **Mechanism under test:** m11 frozen (`src/nec_scale.zag`, mech 10 for scale legs).
  FIX-* are INPUT/curriculum variations; the m11 binary is byte-identical across all FIX runs.
- **Pipeline (validated):** `replicate.py` (deterministic N× sequential passes,
  IDs `#s10rNN`/`#s100rNNN`) → pinned `znc` build of `nec_scale.zag` →
  `convert.py` → frozen `training/analyze.py` + `bars13.py`.
  Validation: rebuilt s10/s100 outputs are byte-identical to v1
  `results_scale_10x/` and `results_scale_100x/` on all 37 legs.

## §1 Diagnosis plan (D1/D2/D3) — measured before FIX runs

**D1 prior washout.** Method: bit-exact Python replica of m11 (`replica.py`);
dump per-class raw ledger rate `(c·10⁶+1.9·10⁶)/(t+2)` vs t at s10;
per-pass d1 conf for honest families; per-class (c,t) at s1/s10/s100.
CONFIRMED ⟺ raw rate declines from the p0=0.95 prior toward each bin's
pooled empirical rate as t grows, AND honest families' d1 conf tracks the
pooled rate of their bins downward with scale.
Refined hypothesis (from pre-measurement): bins are shared across families
(no family labels); wrong items (trap/P/K12/D-wrongs) pollute honest bins;
s1's cold ledger + honest-first order gives clean d1 conf (ceiling locks
d2+), while the warm ledger at scale serves the pooled rate to every new
item's d1. The O-class 0.55 clause is expected to explain the s1 baseline
(6), NOT the degradation — O is processed last (always warm).

**D2 fixture shift.** Method: first pass of the s100 input (5240 rows,
`#s100r001`) through the s1 pipeline; count B13. FIXTURE problem ⟺
subsample B13 ≠ s1 B13 (6).

**D3 pessimistic drift (cap ablation).** Method: `nec_scale_m9.zag` =
`nec_scale.zag` with ONLY the personal-cap block deleted (personal ledger
still updated but never read ⇒ behavior == v0 m9 exactly); run at s10/s100;
count B13. Cap contributes ⟺ m9 violations < m11 violations; report the
exact per-(F,d) split.

## §2 Why fixtures can move B13 (binding-constraint analysis)

For honest families at scale: d1 conf comes ONLY from the class ledger
(no personal history at d1, no family/depth features); §2.3 ceiling locks
d2+ ≤ d1 conf. Hence G(F,d) ≥ −0.100 for acc≈1.0 families REQUIRES the
honest bins' pooled rate ≥ ~0.90 at scale. No d2+ mechanism (floors,
personal dominance) can help — the ceiling blocks it (v1's floor
experiment already proved this). The only levers: (a) change what the
ledger converges to (fixtures: anchors/thinning; mechanism: prior), or
(b) accept the residual. O's 6 violations are irreducible without
fixtures (v1 joint-constraint note); the target therefore requires
eliminating ALL non-O violations at s10/s100 while holding O at ≤6.

## §3 FIX designs (all labeled FIX-*, m11 frozen)

Shared: anchors/calibration items are correct (release=1, correct=1),
unique deterministic IDs, (f1,f5) copied from CORRECT cells in the target
class (correct=1 needs no family label), interleaved uniformly through the
battery (every N/A rows) so the online ledger sees them throughout;
skipped by `convert.py` (not scored; bars measured on the 37-leg matrix).
Anchor counts are DERIVED from stated principles, never tuned to B13.

**FIX-A — prior-anchoring (prior-curriculum consistency).**
For each class containing honest-correct cells with pooled rate < 0.95,
add correct anchors until the class's empirical rate = 0.95.
Principle: the Laplace prior p0=0.95 is a substantive claim that 95% of
each reference class is correct in the deployment population; a curriculum
that contradicts its prior teaches the ledger the curriculum's
adversarial mix, not the deployment population. Anchors restore
prior-curriculum consistency. Count = (0.95·t − c)/0.05, derived from the
frozen prior — not bar-tuned. (~32.7k anchors at s10, ~327k at s100.)

**FIX-B — scale-graded calibration (balanced honest replication).**
Replicate every honest correct released cell 1:1 (new IDs), interleaved
uniformly; replication mass scales with the battery (constant 1:1 ratio at
all scales — a fixed-size calibration set would wash out, the disease
itself). Principle: deployment balance — the red-team battery oversamples
adversarial items; a deployment curriculum represents the honest
population at parity. 1:1 is the balanced-curriculum principle, not tuned.
Predicted weaker than FIX-A (e.g. cls 15 → 0.874 < 0.90); the miss, if it
misses, maps the dose-response honestly.

**FIX-C — underconfidence traps (adversarial honesty).**
Correct items with (f1,f5) MATCHED to wrong items' features (low margin,
same bins), 1:1 matched to released wrongs in the 7 polluted classes —
honest traps indistinguishable by allowed features from the wrong items
that drive pessimism. Principle: the strongest counter to pessimistic
drift is positive evidence in exactly the bins where pessimism is worst;
matched traps force the ledger to weight honesty where it is most
pessimistic. 1:1 matching is the adversarial-honesty principle, not tuned.
Predicted weaker than FIX-A (cls 15 → ~0.82).

**FIX-D — deployment-mix thinning (crew-designed).**
Deterministically thin RELEASED wrong cells to the prior's 5% rate (keep
every 20th released-wrong cell in input order; all else untouched).
Principle: deployment representativeness — the battery's adversarial
oversampling is a test artifact contradicting the prior's deployment
claim; thinning restores the deployment mix WITHOUT synthetic items
(lean alternative to FIX-A's anchors). "Every 20th" derives from p0=0.95.
Risk disclosed: thins red-team content; B2/B3 measured on the thinned
battery and reported.

**PRIOR-WASHOUT mechanism candidate (for the decision rule's sub-case).**
Fixed-shrinkage prior: conf = (empirical + p0)/2 (α=1, very strong
shrinkage to the frozen prior). Principle attempted: structural population
knowledge should not wash out. Predicted to MISS (convex combo bounded by
max(empirical, prior); cls 15 → 0.863 < 0.90) — the miss, if measured,
proves no convex-combo prior can hit the target, bounding the
mechanism sub-case.

## §4 Gaming probes (FIX-A must pass; run on all FIX-* that hit the target)

**GP-1 held-out honesty:** hold out 10% of honest-correct cells (deterministic:
every 10th) from anchor-(f1,f5)-sourcing AND from the battery; run FIX-A;
measure |conf − 1.0| on held-out honest items. PASS ⟺ mean |conf−1.0| ≤ 0.10
(conf tracks honesty, not the bar).
**GP-2 wrong-item overconfidence:** on the FIX-A battery, measure mean conf
of released WRONG cells (trap/P/K12). PASS ⟺ mean conf(wrong) ≤ 0.50 (anchors
do not inflate wrong items' confidence; no bar-ward optimism).
**GP-3 cap integrity:** K12 conf at d2+ = 0.000 under FIX-A (personal cap
still binds; anchors don't rescue adversarial items).

## §5 Exact target and decision rule (amendment §3 verbatim)

Target: B13 violations nonincreasing with scale (viol_s100 ≤ viol_s10 ≤
viol_s1), B3 ≤ 3 (not worsened vs m11), B2 = 0 held, no other bar broken,
gaming probes passed.
Decision: MECHANISM ⟺ D1/D3 confirmed and no FIX-* hits target with bars
held. FIXTURE ⟺ D2 confirmed or a FIX-* hits target. PRIOR-WASHOUT ⟺ D1
confirmed and a principled scale-invariant prior hits target.
No story without numbers.

## §6 Commit discipline

This addendum committed BEFORE any FIX battery runs. Then: FIX inputs,
drivers, result TSVs, SHA logs, RUNLOG. Then VERDICT_Q3.md. No binaries,
no `.zagd` in commits.
