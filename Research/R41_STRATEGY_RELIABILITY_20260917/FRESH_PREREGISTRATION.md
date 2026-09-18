# R41 fresh strategy-reliability challenge

Frozen before R41 development aggregation.

Seeds: 36701, 36707, 36713, 36719.

Scenarios:
- `subset_cost_return`: only a subset of strategies changes cost factor and later returns;
- `subset_success_return`: only a subset changes success factor and later returns;
- `split_async`: different strategy subsets change success/cost on offset boundaries;
- `partial_recombine`: strategy-wise factors recombine into an unseen action-space composition;
- `selective_noise`: outcome/cost noise targets different strategy subsets before a true recurrence.

Single selected candidate may be exposed once with V2/R36/R39 controls.

Fresh gates against retained R39:
1. subset-cost return <= 0.95 * R39;
2. subset-success return <= 0.95 * R39;
3. worst return ratio vs V2 < R39;
4. mean return <= R39;
5. overall mean <= 1.02 * R39;
6. post-change <= 1.02 * R39;
7. partial-recombine return <= 1.02 * R39;
8. selective-noise mean <= 1.03 * R39;
9. expert banks <=5.

No fresh-specific retuning.
