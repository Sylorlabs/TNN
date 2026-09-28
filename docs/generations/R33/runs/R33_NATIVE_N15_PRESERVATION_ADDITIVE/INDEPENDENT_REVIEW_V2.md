# R33-N15 independent pre-run review V2

Terminal disposition: **REQUEST_CHANGES**

The exact V2 read-only review found one remaining preregistration blocker: `n15_run_dev()` can emit `N15_DEV_SELECTION,-1,0` if every non-frozen arm has aggregate `new_gain <= 0`, but the holdout/stage-binding path did not define how that sentinel is handled.

The reviewer confirmed that the three V1 blockers were otherwise closed. No execution authorization was granted.

The correction is protocol-only: `selected=-1` is now explicitly a terminal development negative. No validation or confirmation may execute for that campaign outcome. No learner mechanism, development selector, holdout threshold, seed, or binary behavior is changed.
