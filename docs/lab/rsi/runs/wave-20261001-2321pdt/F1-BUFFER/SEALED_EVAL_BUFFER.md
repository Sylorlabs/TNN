# SEALED_EVAL_BUFFER.md - F1-BUFFER sealed test results

Lane F1-BUFFER, wave wave-20261001-2321pdt. Sealed runs executed
2026-10-02 ~00:10 PDT against the frozen F1 binary
`../F1/impl/f1_learn` (sha256
6f2b155b233a95ad1a8323e8565b9a798dc822db6eff57e065b71b5be8882847,
verified before running; match confirmed). 24 fresh sealed sum2
worlds (frozen 8100-series seeds, manifest sealed3/FIXTURE_SHA256.txt,
all hashes verified before runs). Frozen rule from PREREG_BUFFER.md
(committed alone at b5ff3ab17 before any fresh fixture was generated;
fixture manifest committed at ff7623aa5 before any sealed run):
predict OVERFIT iff T(B) >= 12, where T(B) = S0(B)+S1(B) over the
first-trigger buffer.

No em-dashes are used in this document.

## 1. Determinism evidence

Each of the 48 sealed invocations (24 seeds x train/hidden) was
executed 3 times (runs3/1, runs3/2, runs3/3). All corresponding
outputs are byte-identical across the three repetitions
(cmp-verified, zero diffs). SHA-256 of all runs3/1 outputs is
recorded in runs3/DETERMINISM_SHA256.txt. The 24-seed set with 3/3
determinism per seed is complete (24/24). Zero NOTRIG worlds.

## 2. Overfit rate on fresh worlds (frozen classification)

OVERFIT = hidden accuracy below 80 percent (f1_score acc on the
30-probe masked set, frozen pure-Zag scorer). CORRECT = at least 80
percent. The split is cleanly bimodal; no seed is near the boundary.

| seed | hidden | class |
|---|---|---|
| 3 | 3/30 = 10% | OVERFIT |
| 4 | 0/30 = 0% | OVERFIT |
| 9 | 0/30 = 0% | OVERFIT |
| 10 | 0/30 = 0% | OVERFIT |
| 12 | 0/30 = 0% | OVERFIT |
| 15 | 0/30 = 0% | OVERFIT |
| 17 | 0/30 = 0% | OVERFIT |
| 22 | 1/30 = 3% | OVERFIT |
| 0,1,2,5,6,7,8,11,13,14,16,18,19,20,21,23 | 30/30 = 100% | CORRECT |

Overfit rate: 8/24 = 33 percent, same catastrophic signature as the
5100-series (6/24 = 25 percent): every overfit seed scores 0 to 10
percent.

## 3. Frozen rule application (pure-Zag bufapply)

Rule: predict OVERFIT iff T(B) >= 12, else CORRECT. Per-seed
predictions vs frozen labels (T = S0+S1 from dev/bufx):

| seed | T(B) | predicted | truth | hit |
|---|---|---|---|---|
| 0 | 9 | CORRECT | CORRECT | yes |
| 1 | 11 | CORRECT | CORRECT | yes |
| 2 | 9 | CORRECT | CORRECT | yes |
| 3 | 13 | OVERFIT | OVERFIT | yes |
| 4 | 10 | CORRECT | OVERFIT | MISS |
| 5 | 9 | CORRECT | CORRECT | yes |
| 6 | 11 | CORRECT | CORRECT | yes |
| 7 | 2 | CORRECT | CORRECT | yes |
| 8 | 9 | CORRECT | CORRECT | yes |
| 9 | 8 | CORRECT | OVERFIT | MISS |
| 10 | 12 | OVERFIT | OVERFIT | yes |
| 11 | 9 | CORRECT | CORRECT | yes |
| 12 | 7 | CORRECT | OVERFIT | MISS |
| 13 | 5 | CORRECT | CORRECT | yes |
| 14 | 4 | CORRECT | CORRECT | yes |
| 15 | 7 | CORRECT | OVERFIT | MISS |
| 16 | 5 | CORRECT | CORRECT | yes |
| 17 | 8 | CORRECT | OVERFIT | MISS |
| 18 | 12 | OVERFIT | CORRECT | MISS |
| 19 | 9 | CORRECT | CORRECT | yes |
| 20 | 4 | CORRECT | CORRECT | yes |
| 21 | 6 | CORRECT | CORRECT | yes |
| 22 | 4 | CORRECT | OVERFIT | MISS |
| 23 | 7 | CORRECT | CORRECT | yes |

Contingency (ovf_ge / cor_ge / ovf_lt / cor_lt): 2 / 1 / 6 / 15.
Misclassified seeds: 7 (seeds 4, 9, 12, 15, 17, 22 predicted
CORRECT but OVERFIT; seed 18 predicted OVERFIT but CORRECT).

## 4. Verdict: BUFFER-NOT-PREDICTIVE (per the frozen bar)

PREREG_BUFFER.md section 6(c) requires at most 2 misclassified
seeds. The frozen rule misclassifies 7 of 24 fresh seeds. The
verdict is therefore BUFFER-NOT-PREDICTIVE, with the full tables
above. This is the informative reference outcome named in the
prereg, reported fully, not hidden.

## 5. Interpretation (post-hoc, explanatory only)

The negative generalizes: on the training series the best buffer
rule already missed 5/24, and two seed pairs (6/18, 11/17) proved
no single buffer-feature rule can beat misc = 2 there. The fresh
series confirms the rule has no predictive power out of sample
(misc 7/24, worse than training).

The refined mechanistic picture, consistent with both series: the
first-trigger buffer fully determines the greedy burst's second
construct (verified: the 5100-series seeds 6 and 18 share the exact
first-trigger buffer multiset and take identical first two
constructs, including the degenerate re-add), but the final
OVERFIT vs CORRECT outcome is decided by later-trigger repair
dynamics over the subsequent episode sequence (seed 6 is repaired
by a later full-buffer trigger; seed 18 stalls). The F1-FOLLOWUP
hypothesis is therefore refined, not confirmed: trigger-time
buffer mass predicts the greedy second step, not the final
overfit. A trigger-time policy that only sees buffer mass cannot
fix the failure; any fix must address the later repair dynamics
or the greedy depth-1 trial itself.

Evidence paths (all under
docs/lab/rsi/runs/wave-20261001-2321pdt/F1-BUFFER/):
- PREREG_BUFFER.md (frozen rule, bar, reference outcome)
- dev/CALIBRATION_5100.md, dev/calib_5100.txt (training calibration)
- dev/bufx.zag, dev/bufsep.zag, dev/bufapply.zag (pure-Zag tools)
- sealed3/ (24 fresh fixtures, gen3.sh, run_buffer.sh,
  FIXTURE_SHA256.txt)
- runs3/ (1, 2, 3 repetitions; DETERMINISM_SHA256.txt;
  fresh_table.txt; fresh_scores.txt; run_buffer.log)
