# R39 fresh online-factor challenge preregistration

Frozen before R39 development results are aggregated.

Fresh seeds: 36501, 36507, 36513, 36519.

Fresh scenarios:
- staggered_return: success and cost factors change and return on different boundaries;
- cost_recurrence: long cost-factor recurrence with stable success factor;
- unseen_pairing: learned factors are recombined into a whole-context pairing not previously experienced;
- double_recombine: several independent success/cost returns before the original pair returns;
- cross_noise: stationary base factors with separated outcome-noise and cost-noise bursts.

Only the single development-selected R39 candidate may be exposed once, with V2, R36, and retained R38 as controls.

Fresh gates:
1. worst-world return ratio vs V2 < retained R38;
2. mean return regret <= 0.95 * retained R38;
3. cost_recurrence return regret <= 0.90 * retained R38;
4. unseen_pairing return regret <= 0.95 * retained R38;
5. overall mean regret <= 1.03 * retained R38;
6. post-change regret <= 1.05 * retained R38;
7. cross_noise mean regret <= 1.05 * retained R38;
8. success experts <=5 and cost experts <=5.

Failure is preserved; no fresh-specific retuning.
