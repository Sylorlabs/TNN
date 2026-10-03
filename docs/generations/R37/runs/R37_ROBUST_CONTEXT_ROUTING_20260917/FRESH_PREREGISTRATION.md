# R37 fresh challenge preregistration

Selected from exposed development only: `haz05`.

Fresh seeds: 36301, 36307, 36313, 36319.
Fresh schedules:
- irregular_return: unequal A/B/A/C/A dwell times;
- double_return: repeated A/B recurrence with unequal final dwell;
- partial_mix: success and cost factors change independently and recombine;
- noisy_stationary: no true context change, with two unlabelled adverse feedback bursts;
- novel_then_return: A/B/D/A with a long novel interval before return.

The learner never receives these schedule names or boundaries.

Qualification compares `haz05` against retained R36 (`eig_012`) and V2.
All gates are frozen before execution:
1. mean return regret <= 0.95 * retained R36;
2. worst-world return-regret ratio vs V2 < retained R36's worst-world ratio vs V2;
3. overall mean regret <= 1.03 * retained R36;
4. post-change regret <= 1.05 * retained R36;
5. noisy-stationary mean regret <= 1.05 * retained R36;
6. max contexts <= 5;
7. diagnostic action fraction <= 0.20.

A failure is preserved. No fresh-specific retuning is allowed.
