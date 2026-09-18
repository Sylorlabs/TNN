# R40 fresh reliability-arbitration challenge

Frozen before R40 development results are aggregated.

Fresh seeds: 36601, 36607, 36613, 36619.

Fresh scenarios:
- `long_cost_return`: stable success factor with two long cost changes and recurrence;
- `async_return`: success and cost factors change/return on offset boundaries;
- `novel_recombine`: separately learned success/cost factors appear in unseen pairings before original return;
- `gradual_cost_return`: cost dynamics drift gradually to another factor and later return while success remains stable;
- `noise_then_return`: stationary noise bursts precede a real independent-factor recurrence.

The single development-selected candidate may be exposed once with V2, R36, and retained R39 controls.

Fresh gates against retained R39:
1. cost-return family mean return regret <= 0.95 * R39;
2. worst return ratio vs V2 < R39;
3. overall mean return regret <= R39;
4. overall mean regret <= 1.02 * R39;
5. post-change regret <= 1.02 * R39;
6. novel-recombine return regret <= 1.02 * R39;
7. noise-then-return mean regret <= 1.03 * R39;
8. success/cost experts <=5.

No fresh-specific retuning.
