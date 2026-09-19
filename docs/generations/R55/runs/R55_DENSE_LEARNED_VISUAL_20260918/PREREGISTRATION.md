# R55 dense learned visual representation — preregistration

Date: 2026-09-18  
Status: **FROZEN BEFORE FRESH EXECUTION**

R50–R54 preserve a sequence of failures from hand-designed visual summaries. The capability master plan explicitly permits dense learned components when they materially expand capability. R55 therefore tests a small fully learned visual classifier.

Architecture: 13×13 raw binary/noisy pixels → 64-unit ReLU hidden layer → four category logits. No category-specific feature extractor is supplied. Training examples vary translation, pixel noise, and single-pixel occlusion. Category display labels are evaluator-randomized after source freeze.

The model is trained only on generated training examples, then frozen. Fresh evaluation uses disjoint seeds and measures clean, occluded, noise-heavy, and active-reinspection panels. Active reinspection may request one additional lower-noise view only below a frozen confidence threshold.

Frozen gates: clean >= 0.95, occluded >= 0.85, noise-heavy >= 0.85, active >= 0.93, second-view fraction < 0.60, randomized label literals absent from source.

This is bounded synthetic perception evidence only. It is not natural-video competence. `learn_authority=0`; canonical R27 unchanged.

