# R58 support-channel convolutional vision — preregistration

Date: 2026-09-18  
Status: **FROZEN BEFORE FRESH EXECUTION**

R55–R57 show that translation is mostly solved but sparse pixel noise remains the dominant failure. R58 adds one generic observation channel: local occupied-neighbor density. The learner receives both raw pixels and this generic local-support map, then learns all category features through a convolutional bank and hidden layer.

No category-specific denoising or detector is supplied. The support map is identical for every category and is computed only from the current observation.

R58 preserves the R55–R57 gates unchanged: clean >= 0.95, occluded >= 0.85, noise-heavy >= 0.85, active >= 0.93, second-view fraction < 0.60, randomized labels absent from source.

Bounded synthetic perception only. `learn_authority=0`; canonical R27 unchanged.

