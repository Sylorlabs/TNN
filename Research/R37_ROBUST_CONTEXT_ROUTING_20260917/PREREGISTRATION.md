# R37 robust context routing preregistration

R37 addresses the per-world regressions exposed by the already-frozen R36 fresh challenge. Those R36 fresh worlds are now development data and cannot be reused as R37 qualification evidence.

Mechanism family: retain R36's bounded reusable self-context archive and sparse EIG diagnostic routing, but replace the fixed posterior leak with a learner-owned adaptive hazard driven by pre-update predictive surprise. Surprise is accumulated with a leaky evidence state so isolated bad outcomes do not immediately reset context belief. No regime id, switch flag, evaluator context, oracle competence, or hidden change time enters the learner.

Development candidates: retained R36 `eig_012`, plus hazard scales 0.05, 0.15, 0.30 and a robust 0.15 variant with likelihood clipping. Development uses the exposed R36 fresh seeds/scenarios only.

Selection objective, in order:
1. reduce the maximum return-regret ratio versus V2 across development worlds;
2. reduce mean return regret;
3. keep overall regret <= 1.03x retained R36;
4. keep false-context / diagnostic action rate bounded by the R36 model cap and <= 0.20 probe fraction.

Fresh challenge will be generated from new seeds 36301, 36307, 36313, 36319 and new schedules `irregular_return`, `double_return`, `partial_mix`, `noisy_stationary`, `novel_then_return`. Source and thresholds are frozen before fresh execution. No fresh-specific retuning is allowed.

Phase 6 remains closed and learn authority remains zero regardless of R37 reference results; native persistence and behavioral reproduction remain required.
