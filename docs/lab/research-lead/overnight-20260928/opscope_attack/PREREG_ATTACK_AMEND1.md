# AMENDMENT 1 to PREREG_ATTACK.md: arithmetic correction (bit7 = 128, not 64)

## Status
FROZEN. Committed before the corrected re-run. This amendment corrects an
objective arithmetic error in the prereg; it does not change the hypotheses
(H0 vs H1 vs H2 vs H3), the probe constructions, or the verdict rule's logic.

## The error
PREREG_ATTACK.md states cub (word 7) maps to bit7, which is correct, but then
computes T values using 64 for bit7. In fact 1<<7 = 128, not 64. (Bit6 = 64;
cub is word 7, not word 6.) The sealed controls confirm: "tak cub" has
tgt=129 = 128+1.

This error was discovered after the first attack run, when the program's
world_T outputs (129, 128, 129, 33) disagreed with the prereg's documented
expectations (65, 64, 65, 33). The world_T outputs are correct; the prereg's
hand arithmetic was wrong. No probe construction, scene, or utterance changes.
The attacker's Zag code called the frozen world_T and did not hardcode targets
except in the falsifier-flag comparisons, which are also corrected below.

## Corrected expectations (replace the corresponding lines in PREREG_ATTACK.md)

### ATK1
- world_T: tak->bit0, not->0, bal->0 (shape!=0), cub->bit7 (=128). T = 129
  (was: 65).
- H0 (word-scoped deletion) predicts 129 ({tak, cub}) (was: 65).
- H1 (suffix suppression) predicts 1 ({tak}) (unchanged).
- Mechanism analysis predicts the learner outputs 1 (unchanged).

### ATK2
- world_T: cub->bit7 (=128), not->0, bal->0. T = 128 (was: 64).
- Genuine prefix computation predicts recmask(cub) = {bit0, bit7} = 129
  (was: 65). Bit0 is in every word prototype because "tak" appears in every
  training utterance and always satisfies; bit7 is cub's feature.
- Decision: predict==1 confirms H2. predict==129 refutes H2 (the 129 vs 128
  gap to world_T is the ubiquitous-tak prototype artifact, documented here,
  not a negation failure).

### ATK3
- world_T: tak->bit0, cub->bit7 (=128), not->0, bal->0. T = 129 (was: 65).
- Lexical trigger with positional split predicts 129 (was: 65).
- Mechanism analysis predicts the learner outputs 129 (was: 65).

### ATK4
- Unchanged. T = 33. Learner predicted 33.

## Corrected verdict rule (replaces the numeric conditions; logic unchanged)
Apply in order:
1. If ATK1 predicts 1 (and world_T=129, round-trip holds): H1 CONFIRMED, H0
   REFUTED. Verdict: OPSCOPE-ATTACK-KILLS. (Was: world_T=65.)
2. Else if ATK1 predicts 129: H0 survives ATK1. Then:
   a. If ATK2 predicts 1: OPSCOPE-ATTACK-KILLS (H2 confirmed).
   b. Else if ATK3 != 129 or ATK4 != 33: OPSCOPE-ATTACK-KILLS (was: ATK3 != 65).
   c. Else: OPSCOPE-ATTACK-SURVIVES.
3. Round-trip / training-reproduction guard unchanged.

## Corrected falsifier labels
- FA-SUFFIX: fires iff ATK1 predicts 1 while world_T=129 (was: 65).
- FA-CONST: fires iff ATK2 predicts 1 (unchanged).
- FA-POS: fires iff ATK3 != 129 (was: 65).
- FA-PREFIX: fires iff ATK4 != 33 (unchanged).

## Why this amendment is legitimate
The amendment fixes a factual arithmetic error (1<<7=128) before the corrected
re-run. It does not alter which hypothesis each probe discriminates, the probe
definitions, or the logic of the verdict rule. The first run's substantive
finding (ATK1 pred=1, confirming H1) is preserved under the corrected
constants; the corrected program flags will now agree with the verdict.
The original prereg commit is retained unmodified for audit.
