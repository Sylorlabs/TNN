# R39 wave 3 preregistration — stability-weighted online factors

Wave 2 showed that `balanced_blend25` passes six of seven unchanged development gates. Its remaining failure is stationary-noise robustness: the online factor bank reacts well to recurrence/recombination, while the retained R36 posterior is more stable during transient noise.

The frozen R39 fresh family remains unopened.

Wave 3 tests only the stability mechanism implied by that result:

- `balanced_blend30`: 70% wave-1 `expert_balanced` factor predictions + 30% retained R36 predictions.
- `balanced_blend35`: 65% factor predictions + 35% retained R36 predictions.
- `confidence_blend`: factor weight is learner-owned and changes only with factor-bank posterior concentration. The factor weight is `clip(0.35 + 0.55 * min(success_posterior_max, cost_posterior_max), 0.55, 0.90)`; the remainder is retained R36. No evaluator state enters the weight.

No confirmation-window variants are continued because wave 2 showed that delayed confirmation harmed recurrence/recombination enough to fail multiple unchanged gates.

Development worlds, controls, and all seven R39 admission gates remain exactly unchanged. Selection remains lowest worst-world return ratio, then lowest mean return regret. If no candidate passes every gate, R39 closes without opening the fresh family. If a candidate passes every gate, freeze its source and selection before the single fresh exposure.
