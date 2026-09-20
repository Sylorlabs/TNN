# R52 local visual geometry correction — preregistration

Date: 2026-09-18  
Status: **FROZEN BEFORE FRESH EXECUTION**

R51 established the tool-policy correction but failed visual transfer because pairwise features included every noisy pixel in the frame. R52 changes only visual representation.

The representation is generic: find the densest local window, rank candidate pixels by local neighborhood support, retain a bounded cluster, translate that cluster to a local origin, and compute occupancy/moment/pairwise-offset features. Category labels remain evaluator-randomized; no shape-specific classifier rule is encoded.

Training includes translation, noise, and partial occlusion. Fresh evaluation uses unseen placements and corruption. A second view may be requested only when learned-distance margin is below a calibration threshold fixed before the final panel.

Frozen gates: clean >= 0.90, occluded >= 0.75, active >= 0.85 and >= occluded + 0.05, second-view fraction < 0.80, randomized labels absent from source.

`learn_authority=0`; canonical R27 unchanged.

