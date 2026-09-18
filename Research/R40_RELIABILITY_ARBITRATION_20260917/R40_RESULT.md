# R40 channel-specific reliability arbitration — closeout

Status: **DEVELOPMENT NO-GO / FRESH UNOPENED**

R40 tested learner-owned independent reliability arbitration between the retained R36 stable posterior and the R39 online success/cost factor experts. Reliability was updated only from delayed learner-visible prediction error; no evaluator state or regime label was used.

All 120 preregistered development jobs completed with zero harness errors. The already-frozen R40 fresh family was not opened because no candidate cleared all eight development gates.

## Retained R39 control
- mean regret: 0.034513707514499996
- post-change regret: 0.04462921986452752
- return regret: 0.025529542910353566
- cost-recurrence return regret: 0.018535745090004763
- unseen-pairing return regret: 0.028734055062601793
- cross-noise mean regret: 0.02934619555283101
- worst return ratio vs V2: 1.066095788327457

## Best R40 observations
`arb_sharp` achieved the best cost recurrence of the R40 candidates (0.018921825996179007) and a worst return ratio of 1.047759256999323, but failed cost recurrence, mean return, and unseen-pairing gates.

`arb_mid` achieved the best worst-return ratio (0.9844902287498468) and good unseen pairing, but failed cost recurrence, mean return, and post-change gates.

The learned success/cost factor weights remained close to 0.5 across development, indicating global channel-level predictive-loss arbitration did not separate the substrates strongly enough.

## Research conclusion

Global success-vs-cost channel arbitration is too coarse. Factor/stable superiority varies within a channel across strategies and local operating state. The next architecture should learn reliability at a finer granularity (at least strategy-specific, potentially state-conditioned) from the same delayed learner-visible evidence.

`learn_authority = 0`. Phase 6 remains closed. R40 fresh remains unopened and must not be used for R40 tuning.
