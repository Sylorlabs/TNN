# R46 frozen fresh challenge

This family is frozen before R46 development results.

## Seeds

`46011, 46023, 46037, 46051`

## Scenarios

- `very_long_return`
- `cost_reversal_return`
- `corruption_then_return`
- `delayed_recombine`
- `gradual_dynamics`
- `stationary_spikes`

Each life is 5,600 steps with learner-visible observations and delayed feedback only. No scenario or latent-state identifier is provided to the learner.

## Fresh pass gates

The selected R46 development candidate passes fresh only if every criterion holds:

1. mean regret `<= 0.98 * R39`;
2. mean return regret `<= 0.95 * R39`;
3. post-change regret `<= R39`;
4. `cost_reversal_return` return regret `<= 0.95 * R39`;
5. `stationary_spikes` mean regret `<= 1.02 * R39`;
6. worst paired return-regret ratio vs V2 `< R39`;
7. success/cost expert banks remain `<=5`;
8. residual mechanism is exercised: every row has at least 100 delayed residual updates and aggregate mean absolute utility correction is `>=0.003`.

Fresh executes once for the selected development candidate together with frozen V2, R36 and R39 controls. No threshold, seed, scenario or candidate change may be made from its result.

`learn_authority = 0`; Phase 6 remains closed.

