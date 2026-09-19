# R38 fresh factor-recombination challenge preregistration

This challenge is frozen before R38 development results are aggregated.

Fresh seeds: 36401, 36407, 36413, 36419.

Fresh schedules are generated from independently reusable success and cost factors:

- success_cycle: success A/B/C/A while cost A is stable;
- cost_cycle: cost A/B/C/A while success A is stable;
- unseen_recombine: previously observed factors return in pairings not previously experienced as whole contexts;
- cross_return: success and cost factors return on different schedules before jointly returning to A/A;
- factor_noise: stationary A/A with separate unlabelled outcome-noise and cost-noise bursts.

The learner receives no schedule, factor identity, change flag, regime label, or evaluator state.

After development, only the single preregistered R38 selection may be exposed once to this family. Retained R36 and V2 are evaluated as controls.

Fresh admission gates:

1. selected mean return regret <= 0.95 * retained R36;
2. selected worst-world return-regret ratio vs matched V2 < retained R36's worst-world ratio;
3. selected unseen_recombine mean return regret <= 0.90 * retained R36 unseen_recombine return regret;
4. selected overall mean regret <= 1.03 * retained R36;
5. selected post-change regret <= 1.05 * retained R36;
6. selected factor_noise mean regret <= 1.05 * retained R36;
7. max success factors <= 5 and max cost factors <= 5;
8. diagnostic action fraction <= 0.20.

Failure is preserved. No fresh-specific retuning is allowed.
