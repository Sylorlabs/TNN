# R47 frozen fresh challenge

Frozen before R47 development execution.

Seeds: `47013, 47029, 47047, 47063`.

Scenarios: `triple_return`, `cost_success_decouple`, `short_corruptions`, `alternating_recombine`, `slow_drift`, `stationary_noise_bursts`.

Each life has 5,900 steps. The learner sees observations and delayed feedback only; evaluator scenario/state identities remain hidden.

If and only if development selects a candidate, fresh executes once with that candidate and frozen V2/R36/R39 controls. Gates: mean regret `<=0.99×R39`; mean return regret `<=0.97×R39`; post-change no worse than R39; `cost_success_decouple` return `<=0.97×R39`; stationary noise-burst mean `<=1.02×R39`; worst paired return ratio vs V2 better than R39; expert bounds hold; residual mechanism remains exercised.

`learn_authority=0`; Phase 6 remains closed.
