# R37 robust context routing — final result

Status: **FRESH CHALLENGE FAIL / PRESERVED**

Development selected `haz05` under the preregistered worst-world criterion. The source and fresh challenge were frozen before execution.

## Fresh result

Retained R36:
- mean regret: 0.03444355
- post-change regret: 0.05398002
- return regret: 0.02927037
- worst return ratio vs V2: 1.4677x

R37 `haz05`:
- mean regret: 0.03369641
- post-change regret: 0.05299842
- return regret: 0.02937797
- worst return ratio vs V2: 1.6630x
- noisy-stationary mean regret: 0.02715617
- max contexts: 5
- max diagnostic-action fraction: 0.002917

Passed gates: 5/7.
Failed gates: mean return regret did not reach the frozen 5% improvement requirement; worst-world return routing regressed versus R36.

Worst exposed fresh miss: seed 36307 / `partial_mix`. V2 return regret 0.02972450; R36 0.04362565; R37 0.04943115; R37/V2 ratio 1.6630x.

## Research conclusion

A small adaptive hazard helps average adaptation and reduces some recurrence errors, but a monolithic self-context posterior still confuses partial recombinations of capability/cost state. The next architectural hypothesis should factor self-context into independently reusable latent factors rather than treating each whole context as one identity.

No fresh-specific retuning was performed. `learn_authority = 0`; Phase 6 remains closed.
