# R33-N16 broader-support / localized-routing diagnostic

R33-N16 is a native-Zag synthetic stability/plasticity diagnostic. It is a new identity with new populations. It does not continue, rerun, retune, or reuse N15 scientific evidence, and it does not load or emulate canonical R27.

N15's bounded result was specific: additive+preservation materially reduced interference while retaining useful learning, but `anchor_loss=0` coexisted with substantial unseen old-probe loss. N16 isolates two plausible causes without changing the parent task, learner update rule, training dose, probe sizes, or additive zero-initialization principle:

1. preservation support may have been too narrow;
2. the single old/new prototype gate may have routed too many old-distribution states into the specialist.

The arm matrix therefore crosses broader preservation support with more localized routing. Arm4 is the N15-like control shape. Arms5/6 expand preservation from a small legacy anchor set to the complete old parent-training set and then to a second disjoint old-support set used only by the preservation constraint. Arm7 keeps dual support but allows one protected-anchor loss. Arm8 isolates eight-cluster routing with no preservation. Arms9-11 combine eight-cluster routing with progressively broader preservation support. Arm12 uses the same eight-cluster/dual-support mechanism with tolerance2 to test whether a very small controlled support concession restores useful plasticity. Arms13-15 add a training-input occupancy veto. Arms16-20 add a generic mean-shift projection gate: the old/new training means define a direction vector, and specialist activation requires the input projection to cross a prospectively fixed fraction of the old-to-new mean separation. The 50%,75%,85% thresholds test routing locality without using task truth; arms18/19 add preservation to the75% route.

The second old-support set is a prospectively allocated training-side support resource, not a probe. It is generated from a dedicated seed offset and never contributes gradient/update fitting. Dual-support preservation arms2/6/7/11/12/19 evaluate synthetic old-target correctness on those support inputs and use the resulting protected-behavior loss only to accept or reject proposed updates. Dual-old-support occupancy arms14/15 additionally use unlabeled support-input occupancy counts in the fixed routing veto. The support set never contributes probe outcomes, task ids, or evaluator bits. Old/new probes remain evaluator-only and are generated from distinct seed offsets after training.

For additive arms, the specialist starts at exactly zero contribution. Routing is based only on input geometry from old/new training examples. Eight-cluster routing partitions by the signs of input coordinates8,9,10 and compares Manhattan distance to the nearest nonempty old and new cluster prototype. No task id, probe membership, success label, target truth, or evaluator bit enters routing.

N16 additionally reports old-probe and new-probe gate activations. These are evaluator-only routing-leakage diagnostics. They are never used to accept individual updates. Behavioral success/loss remains primary; routing counts explain mechanism behavior rather than replacing it.

Development is21 arms x10 fresh populations =210 arm-population exposures. Validation and confirmation each use16 disjoint populations with fixed controls0/1/3/4/6/8/14/17 plus the selected arm when distinct, for128 or144 exposures per stage. Maximum campaign exposure is498 arm-population runs.

Development qualification requires positive new gain in every population, max final-old deficit<=4, max pointwise old_lost<=6, total old_lost<=40 and total new_gain>=800. Holdout qualification is stricter and includes matched-frontier comparisons against shared rewrite and the N15-like arm4 control. For preserved eight-cluster arms9-12, it additionally compares against the single-prototype dual-support arm6 and the unpreserved eight-cluster arm8. Arm15 uses its matched unpreserved dual-support occupancy control arm14; arms18/19 use their matched unpreserved 75-percent projection control arm17.

If development emits `N16_DEV_SELECTION,-1,0`, the campaign is a terminal development negative and no holdout may run. If it selects a real arm with gate0, exactly one exploratory validation may run with upstream0; confirmation is forbidden. Confirmation requires native validation gate1.

All negative results, population reversals, pointwise old losses/rescues, accepted/rejected/skipped updates, preservation losses/check counts, and routing gate hits are retained. No N16 threshold or population may be recycled after exposure.
