# R32 R31-matched V4 calibration diagnostic

Status: **REFERENCE_ONLY / DECISION_CALIBRATION_FAILED**.

The evaluator anchor is valid: an exact replay of R31 seed 9700 matched the persisted result with zero delta. On V4 development seed 9710 (90 examples per condition), route A retained 0.992593 core-hard correctness and 0.533333 genuine-ambiguity abstention. However B/C/D replaced the R31 stopping calibration with generic delayed-consensus classifiers and became over-conservative: B core-hard 0.109259 with 1.0 ambiguity abstention; C 0.159259 with 1.0; D 0.538889 with 0.722222.

Causal classification: **decision calibration / causal-ablation confound**, not hypothesis architecture. B/C changed both representation and stopping logic at once, invalidating them as clean ablations. The next harness keeps the exact R31 stopping policy for A/B/C, changes only representation in B/C, and trains D as a conservative extension from R31-final decision states using delayed grounded regret/EIG.
