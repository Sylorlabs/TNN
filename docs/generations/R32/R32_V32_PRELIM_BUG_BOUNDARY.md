# R32 V32 preliminary pass — rejected evaluator defect

Status: **REJECTED_BEFORE_INTERPRETATION**.

The first V32 predictive-dynamics pass was not scientifically interpreted. Two implementation defects were detected:

1. the learned shadow-cost column was appended after candidate-history features instead of before them, so the base feature matrix was a permutation of V30 and failed strict matched parity (`X_max_abs_delta=4.9113`);
2. expected-value metrics indexed numeric 0/1 labels as array positions rather than boolean masks, making reported positive/nonpositive and crossing rates invalid.

The advantage targets and episode splits did match, but strict causal qualification requires exact base-feature parity and correct metrics. The corrected rerun preserves this note and supersedes the preliminary outputs.
