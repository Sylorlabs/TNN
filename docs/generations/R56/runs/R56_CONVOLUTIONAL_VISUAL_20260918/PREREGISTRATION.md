# R56 convolutional visual representation — preregistration

Date: 2026-09-18  
Status: **FROZEN BEFORE FRESH EXECUTION**

R55 demonstrated that a learned dense representation nearly closes clean visual transfer but remains fragile to occlusion and noise. R56 changes the representation to a learned local convolutional bank with global max/mean pooling, providing translation structure without category-specific features.

Architecture: raw 13×13 pixels → 16 learned 3×3 filters → ReLU → global max + mean pooling → learned category logits. Training includes the same task family with stronger generic noise/occlusion augmentation. Display labels are evaluator-randomized after source freeze.

R56 preserves the R55 gates unchanged: clean >= 0.95, occluded >= 0.85, noise-heavy >= 0.85, active >= 0.93, second-view fraction < 0.60, randomized labels absent from source.

Bounded synthetic perception only. `learn_authority=0`; canonical R27 unchanged.

