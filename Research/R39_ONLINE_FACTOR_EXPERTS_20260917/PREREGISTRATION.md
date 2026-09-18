# R39 online latent factor experts preregistration

R38 showed that independently stored success/cost factors are useful but frozen snapshot routing can still reactivate the wrong factor on recurrence. R39 changes the learning substrate: success and cost are represented as separate bounded banks of online experts. Delayed learner-visible evidence is assigned by posterior responsibility, and persistent prediction failure can create a new factor without evaluator labels.

## Development family

The now-exposed R38 fresh worlds only:
- seeds 36401, 36407, 36413, 36419
- success_cycle
- cost_cycle
- unseen_recombine
- cross_return
- factor_noise

## Controls

- v2 retained single model
- r36 retained monolithic posterior
- r38 retained `hybrid_adaptive`

## R39 candidates

- expert_strict: winner-weighted online factor experts, conservative factor creation
- expert_balanced: winner-weighted online factor experts, medium novelty threshold
- expert_fast: faster factor creation

Each success and cost bank is independently bounded to five experts. New factors are created only from learner-visible predictive surprise and posterior ambiguity. Experts are updated only from delayed outcomes/costs assigned by their posterior responsibility.

## Development admission gate

A candidate passes only if:
1. worst return-regret ratio vs V2 < retained R38;
2. cost_cycle mean return regret <= 0.90 * retained R38;
3. unseen_recombine mean return regret <= 0.95 * retained R38;
4. overall mean regret <= 1.03 * retained R38;
5. post-change regret <= 1.05 * retained R38;
6. factor_noise mean regret <= 1.05 * retained R38;
7. max success experts <=5 and max cost experts <=5.

Selection is lowest worst-world return ratio, then lowest mean return regret.
