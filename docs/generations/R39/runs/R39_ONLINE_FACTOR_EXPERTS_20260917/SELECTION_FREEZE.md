# R39 selection freeze — before fresh exposure

Wave 3 completed all 60 preregistered development jobs with zero harness errors.

Selected candidate: `balanced_blend30`.

Selection rule was frozen before results: among candidates passing all seven unchanged R39 development gates, choose lowest worst-world return ratio vs V2, then lowest mean return regret.

`balanced_blend30` development metrics:
- mean regret: 0.0319215694425855
- post-change regret: 0.044084946304708716
- mean return regret: 0.02565649578137607
- worst-world return ratio vs V2: 1.2534520436526426
- cost_cycle return regret: 0.020373663209549645
- unseen_recombine return regret: 0.026316966571513924
- factor_noise mean regret: 0.024712584957839387
- max success experts: 5
- max cost experts: 5

All seven unchanged development gates passed.

The already-frozen fresh family in `FRESH_PREREGISTRATION.md` and `SOURCE_FREEZE_FRESH.sha256` may now be opened once. No fresh-specific tuning is allowed.
