# JUDGE_BRIEF.md - F1-BUFFER trigger-time buffer predictiveness test

Provenance:
- RENDER_SHA: 451823613 (sealed evaluation commit; prereg b5ff3ab17
  committed alone before any fresh fixture; calibration cd59426d5;
  fixtures ff7623aa5; all on branch tnn-native-lab, local only)
- FIRST_RENDERED_WAVE: wave-20261001-2321pdt
- COMPONENT_LINEAGE: F1 BUILD-FAIL, F1-FOLLOWUP Part 2 NOT-FOUND with
  the buffer hypothesis
- NEW_KNOWLEDGE_CLAIM: The constructor's greedy overfit is not
  predictable from trigger-time buffer mass: the best-calibrated
  buffer rule (T>=12 predicts OVERFIT) misclassifies 7 of 24 fresh
  sealed sum2 worlds, and identical first-trigger buffers produce
  opposite outcomes because later-trigger repair dynamics, not the
  first buffer, decide the final structure.

## Verdict: BUFFER-NOT-PREDICTIVE

Governing bar (frozen in PREREG_BUFFER.md section 6, committed alone
at b5ff3ab17 before any fresh fixture was generated; binary under
test is F1's frozen impl/f1_learn, used read-only):

- Bar: the frozen rule (predict OVERFIT iff first-trigger buffer
  mass T(B) >= 12) must misclassify at most 2 of 24 fresh sealed
  sum2 worlds (8100-series, manifest committed at ff7623aa5 before
  any sealed run; 3/3 byte-identical reruns per world, cmp-verified).
- Result: 7 misclassified (seeds 4, 9, 12, 15, 17, 22 predicted
  CORRECT but OVERFIT; seed 18 predicted OVERFIT but CORRECT).
  Contingency (ovf_ge/cor_ge/ovf_lt/cor_lt): 2/1/6/15.
- Overfit rate on fresh worlds: 8/24 = 33 percent, cleanly bimodal
  (0 to 10 percent vs 100 percent), matching the 5100-series
  signature (6/24 = 25 percent).

## Why this matters (one paragraph)

F1-FOLLOWUP's post-hoc story located the greedy failure in the
first-trigger buffer. This lane tested that story as a frozen
prediction and it failed out of sample, and the training
calibration explains why: two seed pairs share every buffer
feature yet diverge, because the first-trigger buffer fixes the
greedy second construct but later triggers over the unfolding
episode sequence decide whether the degenerate structure is
repaired or locked in. A trigger-time policy over buffer mass
cannot fix this failure mode; the repair dynamics or the greedy
depth-1 trial itself are the next targets. No L3 claim follows;
this is a constructor limitation being mapped, not a capability.

## Evidence

- PREREG_BUFFER.md (frozen rule, bar, reference outcome)
- SEALED_EVAL_BUFFER.md (full per-seed tables, contingency)
- dev/CALIBRATION_5100.md (training calibration, collision proof)
- sealed3/ (fixtures, manifest), runs3/ (3x run outputs,
  determinism hashes, fresh_table.txt, fresh_scores.txt)

No em-dashes are used in this document.
