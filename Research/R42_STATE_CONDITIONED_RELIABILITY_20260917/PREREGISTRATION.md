# R42 state-conditioned reliability preregistration — 2026-09-17 branch

Freeze revision 2. Frozen before any R42 candidate result is aggregated or inspected. The first orchestration attempt was stopped solely because concurrent subprocesses were CPU-throttled; its partial rows were deleted unread. This revision changes execution reuse and RNG alignment, not the mechanism, candidates, worlds, or admission gates.

## Hypothesis

R40 showed that global channel-level reliability is too coarse, and R41 showed that strategy-specific scalar reliability is still too coarse. R42 preserves the retained R36 monolithic posterior and R39 online success/cost factor experts, initialized at R39's fixed 70% factor / 30% stable blend. It adds only a bounded state-conditioned correction to that blend.

The correction uses learner-visible information available at decision time: factor-vs-stable disagreement, fast/slow delayed relative-error state, recent feature/error trajectory similarity, factor-bank posterior/evidence, and stable-memory posterior concentration. Delayed outcomes/costs train the correction using the state and predictions cached at action time. No latent context ID, regime/switch label, evaluator state, future outcome, or oracle competence is available.

## Development family

Worlds are exactly the exposed R39 fresh worlds used by R40/R41:
- seeds: 36501, 36507, 36513, 36519
- scenarios: staggered_return, cost_recurrence, unseen_pairing, double_recombine, cross_noise
- 4,800 steps per life with the inherited delayed-feedback schedule

The R42 candidate runner uses the exact R41 decision RNG schedule (`seed * 13007 + scenario-code sum`). Therefore the already-completed immutable R41 V2/R36/R39 rows are paired controls and are reused rather than recomputed. Verified R40/R41 arbitration rows are retained as historical mechanism controls but do not enter R42 admission thresholds.

New candidate jobs: 60 total (3 candidates × 20 worlds):
- `state_cautious`: learning rate 0.012, correction gain 0.70, fast trace 0.06, slow trace 0.010
- `state_balanced`: learning rate 0.025, correction gain 1.00, fast trace 0.08, slow trace 0.012
- `state_fast`: learning rate 0.045, correction gain 1.20, fast trace 0.12, slow trace 0.018

All candidates start exactly at factor weight 0.70 and remain bounded to [0.15, 0.90]. Factor expert banks remain bounded to five success and five cost experts.

## Development admission gates

Against the paired retained R39 rows, a state-conditioned candidate must satisfy every gate:
1. cost-recurrence return regret <= 0.95 * R39;
2. worst return-regret ratio vs paired V2 < R39;
3. mean return regret <= R39;
4. overall mean regret <= 1.02 * R39;
5. post-change regret <= 1.02 * R39;
6. unseen-pairing return regret <= 1.02 * R39;
7. cross-noise mean regret <= 1.03 * R39;
8. success/cost expert banks <=5 and state correction behaviorally exercised (>=100 delayed arbitration updates in every row and mean absolute factor-weight deviation from 0.70 >=0.01).

Selection among passing candidates: lowest cost-recurrence return regret, then lowest worst-world return ratio, then lowest mean return regret.

If no candidate passes every gate, the inherited R41 fresh family remains unopened.

`learn_authority = 0`. Phase 6 remains closed.
