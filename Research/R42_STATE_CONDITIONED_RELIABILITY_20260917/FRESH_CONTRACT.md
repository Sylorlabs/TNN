# R42 inherited fresh contract

Frozen before R42 development execution by binding the already-unopened R41 fresh family.

Source family: `../R41_STRATEGY_RELIABILITY_20260917/r41_fresh_challenge.py`
Original preregistration: `../R41_STRATEGY_RELIABILITY_20260917/FRESH_PREREGISTRATION.md`
Seeds: 36701, 36707, 36713, 36719.
Scenarios: subset_cost_return, subset_success_return, split_async, partial_recombine, selective_noise.

A single development-selected state-conditioned candidate may be exposed once, with V2/R36/R39 controls. No fresh-specific retuning.

Fresh gates against retained R39:
1. subset-cost return <= 0.95 * R39;
2. subset-success return <= 0.95 * R39;
3. worst return ratio vs V2 < R39;
4. mean return <= R39;
5. overall mean <= 1.02 * R39;
6. post-change <= 1.02 * R39;
7. partial-recombine return <= 1.02 * R39;
8. selective-noise mean <= 1.03 * R39;
9. success/cost expert banks <=5 and state correction exercised.
