# PREREG H-SEG2: Segmentation Repair with Fragmentation Penalty

**Status:** FROZEN. This prereg strictly precedes implementation.
**Date:** 2026-09-29
**Author:** H-SEG2 Researcher (subagent)
**Parent result:** H-SEG KILLED (2/3). See SEG_RESULT.md.

## Background

H-SEG tested SEG-LEX, a statistical chunk-lexicon learner, on raw-sequence
word segmentation. K-SEG1 FAILED: "smallgreenball" segmented as
"small|green|b|all" (136) instead of "small|green|ball" (132). Root cause,
precisely diagnosed: the chunk "all" (count 4, twice inside "small" and
twice inside "ball", score 36) outscores the true word "ball" (count 2,
score 32), and the single-character fallback costs nothing (score 0), so
fragmentation is free. K-SEG2 PASSED (ambiguity detection works).
K-SEG3 PASSED (deterministic).

Exploratory analysis (in /tmp only, not part of the frozen H-SEG verdict)
showed that charging -20 per fallback character repairs EXP-A to
"small|green|ball" while preserving EXP-B's AMBIGUOUS verdict. H-SEG2
freezes that repair into the algorithm and tests it, plus new fixtures.

## Hypothesis H-SEG2

SEG-LEX with a fragmentation penalty on unexplained material segments
novel raw sequences correctly, preserves genuine ambiguity detection,
and generalizes to unseen words without breaking.

## Algorithm SEG-LEX-P (frozen)

Identical to SEG-LEX (PREREG_SEG.md) except:

1. **Fragmentation penalty.** The single-character fallback scores
   -FBPEN per character instead of 0. Frozen: FBPEN = 20.
   Honest labeling: FBPEN is an authored parameter, not a derived
   principle. Motivation (MDL intuition): unexplained material costs;
   a tiling that leaves characters uncovered must pay for them, so
   the learner prefers lexicon units over fragmentation. The value 20
   was validated in H-SEG exploratory analysis: it exceeds the
   spurious gain from the "all" phenomenon (36 - 32 = 4 per use, plus
   residue effects) while remaining small enough that genuine novel
   words still segment via fallback. A derived MDL lexicon prior
   remains future work.

2. **DP sentinel fix (required correctness change).** Because reachable
   DP scores can now be negative, the unreachable sentinel changes
   from -1 to -1000000, and the reachability guard changes from
   `dpi >= 0` to `dpi > -1000000`. Without this fix, positions reached
   only via fallback (negative dp) would be treated as unreachable and
   the DP would be wrong. This is a mechanical consequence of negative
   scores, disclosed here before implementation.

All else unchanged: MAXL = 5, MINC = 2, score = count * len^2,
nopt tie counting, AMBIGUOUS on ties.

## Experiments

### EXP-A: novel sequence segmentation (K-SG2-1)

Same corpus and test as H-SEG EXP-A. Corpus: "bigredcube",
"biggreenball", "smallredball", "smallgreencube". Test: "smallgreenball".
**Expected:** SEGMENTED "small|green|ball", score 132, NOPT 1.
Design analysis: "small|green|ball" = 50 + 50 + 32 = 132 (no fallback).
Strongest fragment competitor "small|green|b|all" = 50 + 50 - 20 + 36
= 116 < 132. The penalty reverses the H-SEG optimum.

### EXP-B: ambiguous boundaries (K-SG2-2)

Same corpus and test as H-SEG EXP-B. Corpus: "zab", "abz", "zcde",
"cdez", "zabc", "abcz", "zde", "dez". Test: "abcde".
**Expected:** AMBIGUOUS with candidates "ab|cde" and "abc|de"
(score 34 each, no fallback involved). The penalty must not destroy
the tie: neither optimum uses fallback, so both stay at 34.

### EXP-C: second novel combination (K-SG2-4a)

Corpus A (same four strings). Test: "smallredcube" (novel pairing of
seen words; no training string contains the pair small-red or red-cube
in this order... note "smallredball" contains small-red; the pair
red-cube appears in "bigredcube". The full triple is novel).
**Expected:** SEGMENTED "small|red|cube", score 100 (50 + 18 + 32),
NOPT 1. Tests that the penalty does not over-penalize valid novel
combinations: no fallback is needed, so the penalty is inert here.

### EXP-D: unseen word with fallback (K-SG2-4b)

Corpus A. Test: "bigbluecube". The word "blue" never appears in the
corpus; none of its characters form lexicon chunks ("bl", "lu", "ue"
have count 0; checked against corpus A substrings).
**Expected:** SEGMENTED "big|b|l|u|e|cube", score -30
(18 - 80 + 32), NOPT 1. Tests that the penalty does not break
fallback: unseen material still segments (char by char at -20 each),
and the learner still prefers maximal lexicon coverage ("big" and
"cube" intact rather than further fragmented). A negative total score
is expected and acceptable; what matters is the boundary placement.

## Kill bars (frozen)

- K-SG2-1 (repair, 1/1): EXP-A outputs SEGMENTED with segmentation
  exactly "small|green|ball" and NOPT == 1.
- K-SG2-2 (no regression, 1/1): EXP-B outputs AMBIGUOUS and the
  candidate list contains both "ab|cde" and "abc|de".
- K-SG2-3 (determinism, 1/1): three consecutive runs produce
  byte-identical stdout (cmp-verified).
- K-SG2-4 (generality, 2/2): EXP-C outputs SEGMENTED "small|red|cube"
  with NOPT == 1; EXP-D outputs SEGMENTED "big|b|l|u|e|cube" with
  NOPT == 1.

## What kills H-SEG2

- Any of K-SG2-1, K-SG2-2, K-SG2-4 failing on the exact expected
  outputs: H-SEG2 KILLED, actual output documented.
- Non-deterministic output: K-SG2-3 FAILS, H-SEG2 KILLED.

## Honest failure modes (documented, not hidden)

1. If K-SG2-1 fails, the penalty value or the penalty mechanism is
   insufficient, and the actual optimum is documented. The H-SEG
   diagnosis would need revision.
2. If K-SG2-2 fails (tie broken), the penalty interacts with ambiguity
   detection, which would be a real regression versus H-SEG.
3. If K-SG2-4 fails, the penalty is too aggressive (EXP-C) or fallback
   is broken (EXP-D); the boundary of the penalty approach is mapped.
4. Classification ceiling: SEG-LEX-P is fully authored (algorithm,
   penalty value, corpora). A pass is at most bounded L2 structural
   learning, not L3. The value of a pass: the shared-substring
   limitation identified by H-SEG is repaired by a minimal,
   interpretable change, and the repair generalizes to unseen words.
5. This test does not address slot assignment, compositional semantics,
   or novel referents. Those remain open per RESULT_SYNLANG.md.

## Scope

Bounded to raw-sequence word segmentation with a fragmentation penalty.
Four experiments, four kill bars (five checks). Pure Zag. No Python.

## Prereg commit ordering

This file is committed before any implementation or result. The
implementation (seg2_learn.zag) and result (SEG2_RESULT.md) come in
later commits.
