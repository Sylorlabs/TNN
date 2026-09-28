# R32 E51Q — Fresh Residual Margin Geometry Audit

Date frozen: 2026-08-30
Branch: `r32-agent-sequential-frontier`
Canonical status: R27 remains canonical.

## Causal basis

E51P's valid native 32-cell conditional-weight expert reached 4,200 / 4,200 known-state reachability but only 1,170 / 1,200 no-unique UNKNOWN reachability. Every expert arm hit its 12-sweep optimization ceiling. Before changing representation, adding feature interactions, increasing topology, or scaling cell count, E51Q asks what geometry remains under the frozen 32-cell model.

This is an evaluator-only diagnostic. It does not train a new cognitive mechanism and cannot promote R32.

## Frozen model reconstruction

Deterministically reconstruct the exact E51P 32-cell candidate using:

- stage-61 development worlds;
- the same first-1x absolute-utility terminal-ordering fit;
- the same full-4x global sign calibrator;
- the same E51O learner-grown routing tree;
- the same 32-cell local conditional expert;
- the same 12-sweep resource ceiling.

Require all E51P forward/reverse identity and strict-loss gates before the audit is valid.

## Fresh audit worlds

Use E51N's domain-separated evaluator infrastructure with stage 64:

- audit = 5,400 episodes / 91,800 sequential states.

Stage 64 is disjoint from E51P development, validation, and sealed confirmation worlds. It is used only for causal diagnosis; it is not a training or model-selection partition for a future candidate.

## Measures

For each known episode:

- inspect only states where the frozen terminal ordering selects a grounded-correct commit;
- record `best_correct_margin = max(calibrated_commit_score)` across those states.

For each no-unique episode:

- record `best_unknown_margin = min(calibrated_commit_score)` across all states;
- UNKNOWN is reachable iff this margin is < 0;
- record the routed cell at the minimum-margin state.

Compute the exact uniform-shift feasibility interval:

- preserving all known reachability requires `delta >= -min_known_best_correct_margin`;
- making UNKNOWN reachable on all no-unique episodes requires `delta < -max_no_unique_min_margin`.

If the lower bound is not strictly below the upper bound, no uniform score shift can solve the fresh audit without losing at least one known episode.

Also report:

- blocked no-unique count;
- minimum/maximum/mean blocked margins;
- known weakest margin;
- maximum blocked-cell concentration and number of distinct cells containing blocked minima;
- normalized learner-visible feature distance from each blocked minimum state to the nearest weakest-known correct state, with exact equality checked feature by feature if distance is zero;
- per-feature mean difference between blocked minima and weakest-known correct states for diagnostic trace only.

Evaluator labels used to form these diagnostic groups never enter learner state or parameter fitting.

## Frozen classifications

- `UNIFORM_MARGIN_RESCUE_EXISTS` — a single scalar interval exists on fresh audit worlds;
- `UNIFORM_MARGIN_RESCUE_IMPOSSIBLE_LOCAL_STRUCTURE_REMAINS` — no uniform interval exists and blocked states are learner-distinguishable;
- `RESIDUAL_EXACT_ALIASING_FOUND` — blocked and known-critical states include exact learner-feature aliases requiring different signs;
- `INVALID_RESIDUAL_AUDIT_INTEGRITY_FAILURE` — reconstruction/freshness/determinism fails.

Because E51P hit its optimizer sweep ceiling, even a no-uniform-rescue result does not immediately justify new architecture. The next training-first discriminator should first compare longer optimization dose on the same 32-cell conditional-weight architecture. Only after that plateaus should learner-owned interactions or temporary routed connections be tested.

No E51Q result promotes R32 or establishes AGI/consciousness.
