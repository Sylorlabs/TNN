# R53 occlusion-marginal visual prototype — preregistration

Date: 2026-09-18  
Status: **FROZEN BEFORE FRESH EXECUTION**

R52 passed clean and active-view floors but failed the single-view occlusion floor. R53 preserves the local cluster/translation normalization and changes only category scoring.

For each evaluator-randomized category, the learner estimates a Bernoulli occupancy prototype over the normalized local patch from training examples. At inference, missing expected evidence receives a generic occlusion likelihood while unexpected extra evidence receives the ordinary noise likelihood. The same likelihood rule is used for every category and contains no shape identity.

Frozen gates: clean >= 0.90, occluded >= 0.75, active >= 0.88, second-view fraction < 0.80, randomized labels absent from source.

`learn_authority=0`; canonical R27 unchanged.

