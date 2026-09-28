# R33-N15 closeout summary

R33-N15 is **closed and consumed** with terminal disposition `CONFIRM_CONSUMED_NEGATIVE_WITH_PROMISING_FRONTIER_SIGNAL`.

## What ran

- one native development invocation: 12 arms x 8 fresh populations = 96 arm-population exposures;
- one native exploratory validation invocation: controls 0/1/4/8 plus selected arm10 x 12 fresh populations = 60 exposures;
- zero confirmation invocations, because development gate0 forbade confirmation;
- total fresh scientific N15 exposures: **156**.

No stage was rerun. No threshold, source, arm, seed, control or resource bound was changed after exposure. Confirmation namespace710000 remains untouched.

## Native decisions

Development selected fallback arm10 with `N15_DEV_SELECTION,10,0`. Native development arm10 summary was `N15_DEV_ARM,10,49,1120,45,11,0`: total old_lost49, aggregate new_gain1120, minimum population new gain45, maximum final-old deficit11, eligibility0. The frozen <=4 deficit criterion failed.

Fresh exploratory validation returned `N15_HOLDOUT_ARM,N15_VAL,10,131,3,1844,44,21,21,7692,234,7458,10740,0,12` and gate `N15_HOLDOUT_GATE,N15_VAL,10,0,0`. Arm10 retained positive new gain in every validation population but still exceeded frozen preservation limits: max final-old deficit21, max pointwise old_lost21, total old_lost131.

## Scientific conclusion

Within this synthetic campaign, additive specialization plus preservation produced the strongest observed stability/plasticity compromise, but it did not satisfy the frozen preservation requirements. The especially useful clue is arm10 validation `anchor_loss=0` alongside material unseen old-probe loss: the current preservation anchors are being protected while protection fails to generalize across the broader old-behavior distribution. The current additive routing boundary reduces interference but does not isolate it tightly enough.

This is a negative qualification result, not a near-pass promotion claim. The next new scientific identity should improve old-support representation/protection or specialist-routing isolation and use wholly fresh populations. N15 thresholds and populations must not be reused as fresh evidence.

## Scope

N15 uses a synthetic parent and cannot establish why R27 itself is unbeaten, original-R27 continuity, full learner preservation, general cognition or promotion. R27 remains canonical at development step60,423 with zero newborn restarts. Original R27 source/digest/verifier/runtime closure remains unresolved. Canonical mutation=false, learner authority=false, promotion=false.

Full tables and evidence are in `Research/R33_NATIVE_N15_PRESERVATION_ADDITIVE/RESULT.md`. Final independent post-run disposition is recorded in `Research/R33_NATIVE_N15_PRESERVATION_ADDITIVE/POSTRUN_INDEPENDENT_REVIEW.md`.
