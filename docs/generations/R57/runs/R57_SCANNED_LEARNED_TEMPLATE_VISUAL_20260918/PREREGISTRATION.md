# R57 scanned learned visual templates — preregistration

Date: 2026-09-18  
Status: **FROZEN BEFORE FRESH EXECUTION**

R56 shows a learned convolutional representation is strong on clean and active-view panels but still below the frozen single-view corruption floors. R57 tests a different generic mechanism: learn a local occupancy template per randomized category from examples, then scan the learned template over every spatial location at inference. This directly marginalizes translation and isolates local evidence from global noise.

No category-specific detector is written. The same learned-template estimator, scan, missing-evidence cost, and extra-evidence cost apply to all categories.

R57 preserves the R55/R56 gates unchanged: clean >= 0.95, occluded >= 0.85, noise-heavy >= 0.85, active >= 0.93, second-view fraction < 0.60, randomized labels absent from source.

Bounded synthetic perception only. `learn_authority=0`; canonical R27 unchanged.

