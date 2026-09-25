# F28 DEB — params

F28 has NO fittable parameters and no training phase.

The frozen mechanism (PREREG_FORKROUND.md §3 + ideas/fable_forks.md
Mechanism A) is fully specified structurally:
- budget_0 = 1000 (constant)
- depth-charge coefficients t*1000/64 (structural constants — "never
  increase during learning"; there is no learning)
- α_div = 1000/nh with nh = per-item hypothesis count (data, not fitted)

Per prereg §5, non-training forks skip the training checkpoint; per §5b,
the v2 TRAIN-COORD repair applies to F24–F27 only. This directory is
intentionally empty of parameter files.
