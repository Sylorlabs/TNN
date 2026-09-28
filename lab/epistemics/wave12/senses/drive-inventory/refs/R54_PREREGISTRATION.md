# R54 learned local-template visual correction — preregistration

Date: 2026-09-18  
Status: **FROZEN BEFORE FRESH EXECUTION**

R52 and R53 show that hand-selected geometric summaries are the current visual bottleneck. R54 removes that summary layer. It isolates a generic dense local region and learns a 3×3 probabilistic occupancy template for each evaluator-randomized category directly from examples. Translation is handled by window search; category identity is learned only through labeled exposure.

Training includes noise and single-pixel dropout. Evaluation uses fresh translations/noise/occlusion. Active second-view use is margin-triggered from a calibration panel.

Frozen gates: clean >= 0.92, occluded >= 0.80, active >= 0.90, second-view fraction < 0.75, randomized labels absent from source.

`learn_authority=0`; canonical R27 unchanged.
