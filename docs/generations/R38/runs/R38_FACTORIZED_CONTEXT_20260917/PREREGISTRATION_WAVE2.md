# R38 development wave 2 preregistration

Wave 1 factorization improved recombination but revealed a stability tradeoff. No wave-1 candidate passed every gate, and the already-frozen fresh family remains unopened.

Wave 2 tests one new architectural principle: a bounded mixture of a stable whole-context posterior and an independently factorized posterior. Both components receive the same learner-visible delayed experience. Neither receives evaluator context.

Candidates:
- hybrid25: 25% factorized prediction, 75% monolithic prediction;
- hybrid50: 50% / 50%;
- hybrid75: 75% factorized;
- hybrid_adaptive: factor weight rises only when the factorized success/cost posteriors are jointly more concentrated than the monolithic context posterior.

The development worlds, baselines, and admission gates are unchanged from R38 wave 1. The fresh generator/source hashes remain frozen and unseen.

No candidate may proceed to fresh challenge unless every original R38 development gate passes.
