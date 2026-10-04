# RESULT H-SEG: Segmentation Learning Test KILLED (2/3)

**Prereg:** PREREG_SEG.md (commit 615935452, frozen before implementation)
**Implementation:** seg_learn.zag (SEG-LEX algorithm, pure Zag)
**Date:** 2026-09-29
**Verdict:** H-SEG KILLED. K-SEG1 FAILS. K-SEG2 and K-SEG3 PASS.

## Summary

The first test of whether word segmentation can be learned from raw
sequences via recurring substring statistics. The learner induces a
chunk lexicon (substrings len 2..5, count>=2, score=count*len^2) and
segments via DP. Results are mixed and informative:

- K-SEG1 (novel segmentation): FAIL. "smallgreenball" segments as
  "small|green|b|all", not the expected "small|green|ball".
- K-SEG2 (ambiguity): PASS. "abcde" yields AMBIGUOUS with exactly the
  two tied candidates "ab|cde" and "abc|de".
- K-SEG3 (determinism): PASS. Three runs byte-identical (cmp-verified).

The failure is not a bug. It is a precise, diagnosable limitation of
the frequency-weighted heuristic, and exploratory analysis identifies
the exact repair.

## Kill bar results

### K-SEG1: FAIL (0/1)

EXP-A training corpus (raw, no boundaries):
"bigredcube", "biggreenball", "smallredball", "smallgreencube".
Each word appears exactly twice. Each ordered word pair appears once.

Test: "smallgreenball" (novel, not in training).
Output: SEGMENTED "small|green|b|all", score 136, NOPT 1.
Expected: "small|green|ball".

The learner chose "b|all" over "ball" because the chunk "all"
(count 4: twice inside "small", twice inside "ball", score 4*9=36)
outscores the true word "ball" (count 2, score 2*16=32).
"small|green|b|all" = 50 + 50 + 0 + 36 = 136, beating
"small|green|ball" = 50 + 50 + 32 = 132.

This is the shared-substring problem: "all" is a frequent substring
that appears across different words ("small", "ball"). Pure
frequency-weighted chunking rewards it without charging for the
fragmentation it causes (the residue "b" is covered by the
zero-cost single-character fallback).

### K-SEG2: PASS (1/1)

EXP-B training corpus: "zab", "abz", "zcde", "cdez", "zabc", "abcz",
"zde", "dez" (symmetric by construction).

Test: "abcde".
Output: VERDICT AMBIGUOUS, SCORE 34, NOPT 2.
Candidates: "ab|cde" and "abc|de" (exactly the two preregistered
tied optima, 16+18=34 each).

The learner correctly detects the exact tie and withholds instead of
silently guessing. This is the first demonstration in the lab of a
segmentation mechanism that reports genuine ambiguity.

### K-SEG3: PASS

Three consecutive runs of the binary produce byte-identical stdout
(cmp-verified on /tmp/seg_run1.txt, /tmp/seg_run2.txt,
/tmp/seg_run3.txt).

## Analysis: the "all" phenomenon

The K-SEG1 failure reveals a specific limitation, not a general
impossibility:

1. The chunk "all" is genuinely more frequent (count 4) than the
   word "ball" (count 2), because "all" occurs inside two different
   words. Frequency alone cannot distinguish "a frequent substring"
   from "a word".

2. The scoring (count*len^2) does not penalize fragmentation. Using
   "all" as a unit forces the residues "sm" and "b" to be covered
   separately, but the single-character fallback has score 0 (no
   penalty), so fragmentation is free.

3. Real unsupervised segmentation systems handle this via:
   (a) a penalty/cost for unknown or fallback units,
   (b) MDL lexicon priors (the lexicon {"all","b","sm",...} costs
   more than {"ball","small",...} when total encoding length is
   counted),
   (c) branching-factor / transitional-probability cues.

## Exploratory: fallback penalty repairs EXP-A (not part of verdict)

To identify exactly what would be needed, an exploratory variant was
tested (in /tmp only, NOT the frozen implementation): the
single-character fallback score changed from 0 to -20 (a penalty
for uncovered material). All else identical.

Result: EXP-A outputs "small|green|ball" (score 132, NOPT 1);
EXP-B still outputs AMBIGUOUS with "ab|cde" and "abc|de".
Both experiments pass with the penalty.

This confirms the diagnosis: the count*len^2 heuristic is sufficient
for segmentation IF fragmentation is penalized. The frozen H-SEG
did not include the penalty, so K-SEG1 stands as FAIL.

This exploratory result motivates H-SEG2: a new prereg with the
fallback penalty (or a derived MDL principle) as part of the frozen
algorithm.

## Classification

H-SEG KILLED by the shared-substring limitation. The SEG-LEX
algorithm is fully authored, so a pass would have been at most
bounded L2 structural learning (learner constructs chunk lexicon
and segmentations from experience via generic counting/DP), not L3.

The value of this kill:
1. First empirical test of segmentation learning in the lab.
2. K-SEG2 proves a statistical learner CAN detect genuine
   segmentation ambiguity and withhold (novel capability).
3. K-SEG1 precisely maps the boundary: frequency-weighted chunking
   needs a fragmentation penalty (or MDL/branching-factor principle).
4. The exploratory fallback-penalty result gives H-SEG2 a concrete,
   tested starting point.

## What would be needed (for H-SEG2 and beyond)

1. **Fragmentation penalty** (tested exploratory): charge for
   fallback/uncovered characters. Minimal change, fixes EXP-A.
2. **MDL lexicon prior** (principled): minimize total description
   length (lexicon + encoded corpus), not just sum of chunk scores.
3. **Branching factor**: prefer boundaries where the set of possible
   neighbors is large (Harris 1955).
4. Beyond segmentation: slot assignment (words -> semantic roles),
   compositional semantics from sequences, novel referent handling.
   These remain open per RESULT_SYNLANG.md.

## Commits

- Prereg: 615935452 (frozen before implementation)
- Implementation + result + raw output: (this commit)

## Files

- docs/lab/research-lead/overnight-20260928/PREREG_SEG.md
- docs/lab/research-lead/overnight-20260928/seg_learn.zag
- docs/lab/research-lead/overnight-20260928/SEG_RESULT.md
- docs/lab/research-lead/overnight-20260928/SEG_RAW_OUTPUT.txt

## Governance

Pure Zag throughout. No Python used at any stage. Prereg 615935452
strictly precedes implementation. The exploratory fallback-penalty
variant was run in /tmp only and is not committed; it does not
affect the frozen verdict. No em dashes in documentation.
