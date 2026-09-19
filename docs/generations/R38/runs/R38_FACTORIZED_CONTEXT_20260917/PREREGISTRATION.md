# R38 factorized self-context preregistration

## Research question

Can learner-side self-context identification become robust to partial recombination by representing success/capability and cost/resource state as independently reusable latent factors?

R37 showed that a monolithic context posterior can improve average adaptation while still making severe return-routing errors when previously learned success and cost components recombine. R38 therefore changes the representation rather than retuning the R37 hazard.

## Learner-visible inputs only

The learner may use its feature vector, selected strategy, delayed binary outcome, experienced cost, its own predictive distributions, posterior uncertainty, and stored self-model state. It receives no regime ID, context label, switch flag, task label, evaluator state, hidden schedule, or oracle utility.

## Development data

R37's already-exposed fresh family is now development data:

- seeds 36301, 36307, 36313, 36319
- irregular_return
- double_return
- partial_mix
- noisy_stationary
- novel_then_return

## Candidates

- v2: retained single self-model baseline
- r36: retained monolithic posterior archive
- haz05: rejected R37 development winner, kept as a control
- factor_passive: independent bounded success/cost posterior archives, no diagnostic value bonus
- factor_eig: factorized archive + opportunity-cost-aware diagnostic action value
- factor_haz: factorized archive + independent mild surprise hazard + diagnostic value

All factor archives are bounded at four dormant + one active factor per channel.

## Development admission gate

A factorized candidate passes only if all are true:

1. worst return-regret ratio vs matched V2 is lower than retained R36 on the development family;
2. mean partial_mix return regret <= 0.90 * retained R36 partial_mix return regret;
3. overall mean regret <= 1.03 * retained R36;
4. post-change regret <= 1.05 * retained R36;
5. noisy_stationary mean regret <= 1.05 * retained R36;
6. success-factor count <= 5 and cost-factor count <= 5;
7. diagnostic action fraction <= 0.20.

Selection among passers is by lowest worst-world return ratio, then lowest mean return regret.

No development candidate receives access to the later fresh-family generator or seeds.
