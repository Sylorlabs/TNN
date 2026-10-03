# R41 strategy-specific reliability arbitration preregistration

R40 showed that global success/cost reliability weights stayed near 0.5 and failed to improve retained R39. R41 retains the same two substrates but learns factor-vs-stable predictive reliability separately for each strategy and separately for success and cost.

Only learner-visible delayed outcomes/costs update the reliability state for the strategy that produced them. No hidden context, regime identity, switch event, or evaluator state is available.

## Development family
The now-exposed R39 fresh worlds only: seeds 36501/36507/36513/36519 across staggered_return, cost_recurrence, unseen_pairing, double_recombine, cross_noise.

Controls: V2, retained R36, retained R39 `balanced_blend30`.

Candidates:
- `strat_slow`: per-strategy loss EWMA update 0.015, beta 8;
- `strat_mid`: update 0.035, beta 8;
- `strat_sharp`: update 0.025, beta 12.

Weights are bounded to [0.15, 0.90]. Success/cost expert banks remain bounded to five each.

## Development gates against retained R39
1. cost-recurrence return regret <= 0.95 * R39;
2. worst return ratio vs V2 < R39;
3. mean return regret <= R39;
4. overall mean regret <= 1.02 * R39;
5. post-change regret <= 1.02 * R39;
6. unseen-pairing return regret <= 1.02 * R39;
7. cross-noise mean regret <= 1.03 * R39;
8. success/cost experts <=5.

Selection: lowest cost-recurrence return, then lowest worst return ratio, then lowest mean return. No fresh exposure unless every gate passes.
