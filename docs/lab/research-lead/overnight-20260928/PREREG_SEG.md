# PREREG H-SEG: Segmentation Learning Test

**Status:** FROZEN. This prereg strictly precedes implementation.
**Date:** 2026-09-29
**Author:** Segmentation Frontier Researcher (subagent)

## Background

H-SYNLANG was KILLED (RESULT_SYNLANG.md). The kill revealed a fundamental
architectural gap: no TNN mechanism learns segmentation from raw sequences.
The procedure learner is a string transducer (positional index functions,
requires character overlap). The causal learner uses fixed 3-variable
states. FDCR uses pre-segmented triples. The step "raw sequence -> word
boundaries" is entirely researcher-supplied in every existing test.

This prereg designs the FIRST test of whether segmentation can be learned
from statistical regularities in raw sequences. It does not claim the
learner invents segmentation; the algorithm is authored. The question is
whether statistical regularities SUFFICE for a learner to discover word
boundaries, as an existence proof that the gap is bridgeable.

## Hypothesis H-SEG

A statistical chunk-lexicon learner using only recurring substring
statistics can segment novel raw sequences into words, and honestly
withholds (reports AMBIGUOUS) when the statistics support two
segmentations equally.

## Algorithm SEG-LEX (frozen)

Input: a training corpus = list of raw byte strings (concatenated words,
no boundaries marked). The corpus is the environment; the learner sees
only the raw strings.

**Phase 1: Lexicon induction.**
1. Extract every substring of length 2..MAXL from every corpus string.
2. Count occurrences per distinct substring (overlapping occurrences
   count; counts accumulate across the whole corpus).
3. Lexicon L = { substring s : count(s) >= MINC }, each with
   score(s) = count(s) * len(s)^2.
   Rationale (authored heuristic, honestly labeled): prefer units that
   are both frequent and long. This is a frequency-weighted bias toward
   longer recurring units, not a derived principle.

**Phase 2: Segmentation by dynamic programming.**
For a test string T of length n:
1. dp[0] = 0; dp[i] = max over lexicon chunks c with len(c) <= i and
   T[i-len(c)..i] == c of dp[i-len(c)] + score(c). A single-character
   fallback (score 0) is always available, so dp is fully defined.
2. nopt[i] = number of distinct predecessor choices achieving dp[i]
   (capped at 999; deterministic tie handling by fixed chunk order).
3. Reconstruct the best segmentation. If nopt[n] > 1, enumerate the
   tied optimal segmentations (up to 5 listed).

**Output:**
- If nopt[n] == 1: emit SEGMENTED with the boundary-marked string.
- If nopt[n] > 1: emit AMBIGUOUS with the ranked tied candidates.
  The learner does not silently guess.

**Frozen parameters:** MAXL = 5, MINC = 2.

## Experiment A: novel sequence segmentation (K-SEG1)

**Vocabulary (fresh, chosen for distinctive boundary letters):**
sizes {big, small}, colors {red, green}, shapes {cube, ball}.
Grammar: [size] [color] [shape], shape required.

**Training corpus (4 raw strings, pairs unique by construction):**
1. "bigredcube"     (pairs: big-red, red-cube)
2. "biggreenball"   (pairs: big-green, green-ball)
3. "smallredball"   (pairs: small-red, red-ball)
4. "smallgreencube" (pairs: small-green, green-cube)

Each word appears exactly twice (count = MINC). Each ordered word pair
appears at most once, so cross-boundary chunks cannot reach MINC via a
single pair. (A few cross-boundary fragments such as "gre" reach count 2
via shared letters across different pairs; the design analysis shows
they are dominated by full-word tilings. The implementation is the
arbiter.)

**Test:** "smallgreenball" (novel: not in the training corpus).
**Expected:** SEGMENTED "small|green|ball" with nopt == 1.
Design analysis: intended score = 50 + 50 + 32 = 132
(small: 2*25, green: 2*25, ball: 2*16). The strongest hand-checked
competitor is "small|green|ba|ll" = 50 + 50 + 8 + 16 = 124 < 132.
Every proper fragment tiling of each word scores strictly below the
whole word (big 18 > 8, small 50 > 34, red 18 > 8, green 50 > 32,
cube 32 > 18, ball 32 > 24), so any misplaced boundary degrades the
total. If the implementation finds a different optimum, K-SEG1 FAILS
and the actual optimum is documented.

## Experiment B: ambiguous boundaries (K-SEG2)

**Training corpus (8 raw strings, symmetric by construction):**
"zab", "abz", "zcde", "cdez", "zabc", "abcz", "zde", "dez"
("z" is a frequent context character, as a common word would be.)

**Test:** "abcde".
**Expected:** AMBIGUOUS with exactly the tied candidates "ab|cde"
and "abc|de" (either order).
Design analysis: substring counts give ab:4 (16), de:4 (16),
abc:2 (18), cde:2 (18). "ab|cde" = 16 + 18 = 34.
"abc|de" = 18 + 16 = 34. Exact tie by symmetric construction.
The next-best ("ab|cd|e" = 16 + 8 + 0 = 24) is strictly worse.
If the implementation does not produce AMBIGUOUS with both
candidates, K-SEG2 FAILS and the actual output is documented.

## Kill bars (frozen)

- K-SEG1 (novel segmentation, 1/1): EXP-A test "smallgreenball" outputs
  SEGMENTED with segmentation exactly "small|green|ball" and nopt == 1.
- K-SEG2 (ambiguity, 1/1): EXP-B test "abcde" outputs AMBIGUOUS and the
  candidate list contains both "ab|cde" and "abc|de".
- K-SEG3 (determinism): three consecutive runs produce byte-identical
  stdout (cmp-verified).

## What kills H-SEG

- EXP-A segments "smallgreenball" as anything other than
  "small|green|ball", or with nopt != 1: K-SEG1 FAILS, H-SEG KILLED.
- EXP-B does not output AMBIGUOUS, or omits either tied candidate:
  K-SEG2 FAILS, H-SEG KILLED.
- Non-deterministic output: K-SEG3 FAILS, H-SEG KILLED.

## Honest failure modes (documented, not hidden)

1. If K-SEG1 fails because a fragment tiling outscores the intended
   words, the actual optimum is documented. This would show the
   count*len^2 heuristic is insufficient and a stronger principle
   (e.g., MDL lexicon prior, Bayesian unigram model) is needed. That
   is a finding about the SCORING, not about whether statistics can
   in principle support segmentation.

2. If K-SEG2 fails because the tie does not materialize (one candidate
   wins), the actual scores are documented. This would reveal a flaw
   in the symmetric fixture design.

3. Classification ceiling: the SEG-LEX algorithm is fully authored.
   A pass is at most bounded L2 structural learning (the learner
   constructs the chunk lexicon and segmentations from experience via
   generic counting/DP mechanisms), not L3. No representational
   invention is claimed. The value of a pass is an existence proof
   that statistical regularities suffice for segmentation in the
   minimal case, mapping the boundary of the H-SYNLANG gap.

4. This test does not address slot assignment (words -> semantic roles),
   compositional semantics from sequences, or novel referents. Those
   remain open per RESULT_SYNLANG.md.

## Scope

Bounded to raw-sequence word segmentation from recurring substring
statistics. Two experiments, three kill bars. Pure Zag. No Python.

## Prereg commit ordering

This file is committed before any implementation or result. The
implementation (seg_learn.zag) and result (SEG_RESULT.md) come in
later commits.
