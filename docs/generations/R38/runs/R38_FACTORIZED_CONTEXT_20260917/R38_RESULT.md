# R38 factorized self-context — final result

Status: **FRESH CHALLENGE FAIL / PRESERVED**

Wave 1 established that pure factorization improves partial recombination but trades off stability. Wave 2 selected `hybrid_adaptive` under the unchanged development gate before the fresh challenge was opened.

## Fresh result

Retained R36 return regret: 0.03418861
R38 return regret: 0.03345616
Retained R36 worst return ratio vs V2: 1.6471x
R38 worst return ratio vs V2: 1.8535x
R36 unseen-recombine return regret: 0.03623828
R38 unseen-recombine return regret: 0.03680002
R38 overall regret: 0.03677859
R38 post-change regret: 0.05279095
R38 factor-noise regret: 0.02399743

Passed gates: 5/8. Failed the return, worst-world, and unseen-recombination gates.

Worst fresh miss: seed 36407 / `cost_cycle` with R38/V2 return ratio 1.8535x.

## Research conclusion

Separating success and cost factors is useful, but prediction blending is still too passive: the learner can store reusable factors yet fail to reactivate the right cost factor on return. The next architecture should maintain online latent factor experts and assign delayed evidence directly to those factors, rather than depending on frozen snapshots plus a single adapting active model.

No fresh-specific retuning was performed. `learn_authority = 0`; Phase 6 remains closed.
