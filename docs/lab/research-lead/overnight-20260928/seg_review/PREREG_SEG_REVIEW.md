# PREREG: Segmentation Architecture Review

Frozen before review analysis begins. Review only; no implementation authorized.

## Review question

DEVANG2, DEVANG3, and DEVANG4 are three consecutive generations that repair
adjacent distributional edge cases (bigram DP, TP threshold plus
lexicon-reuse, merge pass plus negator-aware grounding) while retaining the
same representation: one-pass boundary decisions from corpus string
statistics, decoupled from consequence grounding. NEG novel is 0/3 in
DEVANG3 and DEVANG4. This review asks whether the representation itself is
wrong, and compares at least three structurally different
segmentation/grounding hypotheses before a DEVANG5 repair is authorized.

## Frozen evidence sources

- DEVANG2 prereg 402e53d32, result 153e2af8e: bigram DP, 13/20.
- DEVANG3 prereg b2ceb6b38, result e0d3a5e94: V3 TP plus lexicon-reuse,
  16/20, NEG novel 1/3 to 0/3.
- DEVANG4 prereg c73372286, result d9ebbfe6d: merge pass plus
  negator-aware grounding, 16/20, NEG novel still 0/3.
- SEGREDESIGN prereg fc82df44b, amend 5dfdc776d, result 8178531c8:
  REDESIGN-BLOCKED. V3 exploratory 6/10 vs 3/10 baseline.

Key failure facts used by the review (all from d9ebbfe6d, Analysis K1):

1. Test "taknotgrn" segments as ["tak","not","g","r","n"]; "grn" never
   forms as a lexicon entry.
2. "not" neg_tot=13, neg_viol=4, is_negator=0 (31 percent below the
   70 percent threshold).
3. "red" is mis-grounded: NEG episodes ground it to the wrong color,
   breaking ("not","red") pair statistics.
4. Grounding and negator statistics are interdependent: mis-grounded
   primaries break pair stats; polluted pairs block negator
   identification.
5. Fragment counts are high ("r"=55), so count filters cannot remove
   fragments; length filters remove true violations.

## Hypotheses to compare (frozen set, all four)

- H1: consequence-grounded segmentation. Boundary utility is measured by
  consequence-prediction improvement, not string statistics.
- H2: predictive boundary discovery. Boundaries at maxima of the
  learner's own online next-character prediction failure, computed
  causally from past observations only.
- H3: recurrence/compression-based units. Chunks promoted when they
  reduce total code length of the corpus-so-far; the lexicon is a
  compression codebook.
- H4: multi-level revisable chunks. Segments can split when fragments
  develop independent grounding and merge when adjacent segments share
  grounding; boundaries are revisable after the first pass.

DEVANG3/DEVANG4 (distributional TP plus lexicon repair) is the frozen
baseline control, not a fifth hypothesis.

## Kill bars (frozen)

- K1: all four hypotheses specified with concrete mechanisms,
  including the exact boundary decision rule and the learner state it
  reads and writes. PASS requires each mechanism to be implementable
  from the description without inventing new semantic cases.
- K2: failure analysis per hypothesis against the five frozen failure
  facts above: states what the hypothesis would fix, what it would
  still fail, and why. PASS requires at least one predicted residual
  failure per hypothesis.
- K3: discriminating test design: a frozen battery where the four
  hypotheses make divergent predictions, with the online constraint
  enforced. PASS requires at least three tests whose predictions differ
  across hypotheses.

## Verdict rules

- REVIEW-COMPLETE requires K1, K2, K3.
- The review recommends at most one hypothesis for implementation, with
  stated falsification conditions. It does not authorize DEVANG5; the
  implementer must preregister separately.
- If no hypothesis is predicted to pass the discriminating battery,
  the review reports that outcome instead of recommending one.

## Governance

- Design only. No implementation, no binaries, no run outputs.
- Pure shell tooling only. No Python anywhere, including diagnostics.
- No em dashes in any file. Byte check with grep before each commit.
- Commits local on tnn-native-lab, owned path seg_review/ only.
