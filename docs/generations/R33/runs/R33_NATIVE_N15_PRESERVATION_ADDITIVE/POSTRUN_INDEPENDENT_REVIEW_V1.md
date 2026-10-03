# R33-N15 independent post-run review V1

Terminal disposition: **REQUEST_CORRECTION**

The reviewer verified all 22 entries in the first post-run evidence manifest and confirmed the execution/evidence accounting:

- exact frozen BUILD_09/source/admission identities were preserved;
- development executed exactly96 arm-population exposures and native selection was `N15_DEV_SELECTION,10,0`;
- raw development arm10 rows reconcile to old_lost49, new_gain1120, minimum new gain45, maximum final-old deficit11, eligible0;
- validation was correctly admitted as exploratory `validate 10 0`, exactly60 arm-population exposures;
- raw validation arm10 rows reconcile to old_lost131, rescued3, new_gain1844, minimum gain44, maximum deficit21, maximum loss21, proposals7692, accepted234, rejected7458, skipped10740, anchor_loss0;
- native validation gate is `N15_HOLDOUT_GATE,N15_VAL,10,0,0`;
- total exposure is156, confirmation executions are0 and the confirmation run directory is absent as required;
- observed maximum RSS 5,799,936 / 3,981,312 bytes remained below the frozen 67,108,864-byte ceiling;
- no evidence of rerun, retune, reselection, threshold change, or confirmation exposure was found.

The sole requested correction was interpretive scope. The first `RESULT.md` version said the synthetic N15 result explained a major part of why recent candidates had not beaten R27. The reviewer correctly judged that broader causal/R27 claim unsupported by this synthetic campaign. The sentence was replaced with bounded N15-only stability/plasticity language.

The reviewer stated that with this scope correction the evidence supports terminal disposition `CONFIRM_CONSUMED_NEGATIVE_WITH_PROMISING_FRONTIER_SIGNAL`. No additional N15 execution was authorized.
