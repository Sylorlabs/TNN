# RESULT H-SEG2: Segmentation Repair SURVIVES (5/5)

**Prereg:** PREREG_SEG2.md (commit 28266d158, frozen before implementation)
**Implementation:** seg2_learn.zag (SEG-LEX-P algorithm, pure Zag)
**Date:** 2026-09-29
**Verdict:** H-SEG2 SURVIVES. All four kill bars PASS (5/5 checks).

## Summary

H-SEG was KILLED by the shared-substring limitation: frequency-weighted
chunking rewarded the cross-word fragment "all" (count 4) over the true
word "ball" (count 2) because the single-character fallback was free.
H-SEG2 freezes the repair into the algorithm: the fallback now costs
FBPEN = 20 per uncovered character (authored parameter, MDL intuition),
plus the required DP sentinel fix for negative reachable scores.

## Kill bar results

### K-SG2-1: PASS (repair)

EXP-A test "smallgreenball": SEGMENTED "small|green|ball", score 132,
NOPT 1. The H-SEG failure is repaired: "small|green|b|all" now scores
50 + 50 - 20 + 36 = 116 < 132. The penalty reverses the optimum exactly
as the prereg predicted.

### K-SG2-2: PASS (no regression)

EXP-B test "abcde": VERDICT AMBIGUOUS, score 34, NOPT 2, candidates
exactly "ab|cde" and "abc|de". Neither optimum uses fallback, so the
penalty is inert and the genuine tie is preserved. Ambiguity detection
survives the repair.

### K-SG2-3: PASS (determinism)

Three consecutive runs byte-identical (md5
cf600b114c8ac78da4bd4e4f7ab67cb5, cmp-verified).

### K-SG2-4: PASS (generality, 2/2)

- EXP-C "smallredcube" (novel pairing of seen words): SEGMENTED
  "small|red|cube", score 100 (50 + 18 + 32), NOPT 1. The penalty does
  not over-penalize valid novel combinations; with no fallback needed
  it is inert.
- EXP-D "bigbluecube" (unseen word "blue", no lexicon chunks cover it):
  SEGMENTED "big|b|l|u|e|cube", score -30 (18 - 80 + 32), NOPT 1.
  Fallback still works under the penalty: unseen material segments
  char by char, and the learner prefers maximal lexicon coverage
  ("big" and "cube" intact rather than further fragmented). A negative
  total score is expected and acceptable; boundary placement is what
  the bar checks.

## What changed versus SEG-LEX (mechanical diff)

1. `fn FBPEN()i32 { return 20; }` added; fallback relax call changed
   from score 0 to score 0 - FBPEN() per character.
2. DP unreachable sentinel changed from -1 to -1000000
   (`fn DPSENT()i32`), reachability guard from `dpi >= 0` to
   `dpi > DPSENT()`. Required because reachable scores can now be
   negative; without it, fallback-reached positions would read as
   unreachable. Disclosed in the prereg before implementation.
3. Two new test strings: "smallredcube" (EXP-C), "bigbluecube" (EXP-D).

No other logic touched. Lexicon induction, scoring (count * len^2),
tie counting, and ambiguity reporting are byte-identical to H-SEG.

## Classification

H-SEG2 SURVIVES as a bounded L2 structural learning repair: the learner
constructs the chunk lexicon and segmentations from experience via
generic counting/DP mechanisms, now with a fragmentation penalty that
repairs the diagnosed failure and generalizes to unseen words. Not L3:
the algorithm, the penalty value, and the corpora are authored. The
value of the pass: the precise limitation H-SEG mapped is closed by a
minimal, interpretable, honestly-labeled change.

## Open (not claimed)

- FBPEN = 20 is authored, not derived. A principled MDL lexicon prior
  or branching-factor cue remains future work.
- Slot assignment (words to semantic roles), compositional semantics
  from sequences, and novel referents remain open per RESULT_SYNLANG.md.

## Commits

- Prereg: 28266d158 (frozen before implementation; note: the commit
  also swept in a concurrent agent's ROUTER3 files, which I did not
  create or modify)
- Implementation + result + raw output: (this commit)

## Files

- docs/lab/research-lead/overnight-20260928/PREREG_SEG2.md
- docs/lab/research-lead/overnight-20260928/seg2_learn.zag
- docs/lab/research-lead/overnight-20260928/SEG2_RESULT.md
- docs/lab/research-lead/overnight-20260928/SEG2_RAW_OUTPUT.txt

## Governance

Pure Zag throughout. No Python used at any stage. Prereg 28266d158
strictly precedes implementation. Only H-SEG2-owned files staged and
committed; concurrent agents' untracked files left untouched. No em
dashes in documentation. No binaries committed.
