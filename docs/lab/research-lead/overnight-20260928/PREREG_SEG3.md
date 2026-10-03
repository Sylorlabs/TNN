# PREREG H-SEG3: Coverage-Discounted Segmentation Repair

**Status:** FROZEN. This prereg strictly precedes implementation.
**Date:** 2026-09-29
**Author:** H-SEG3 Repair Researcher (subagent)
**Parent result:** H-SEG2 DOWNGRADED by red team (SEG2-ADV). See
SEG2_ADV_RESULT.md. Frozen 5/5 bars stand; generality claim fell.

## Background

H-SEG2 repaired H-SEG's shared-substring kill with a constant
fragmentation penalty FBPEN=20 per fallback character. The red team
demonstrated (X-SG2-1, X-SG2-2) that the repair is frequency-fragile:
chunk scores scale as count*len^2 while the penalty is constant, so a
frequent shared chunk ("abcd", count 6, score 96) beats its true words
("xabcd", count 2, score 50) via the tiling "x|abcd" (76 > 50). The
mechanism fragmented even seen training words. The red team also
demonstrated (X-SG2-3) a crash on 120-char input: build_best's 64-entry
move stacks overflow (slice index out of bounds, exit 1).

## Hypothesis H-SEG3

A data-derived coverage discount on chunk scores closes the
shared-substring failure class for any chunk frequency (not just the
frozen fixture's band), and move stacks sized by input length remove
the crash, while all frozen H-SEG2 verdicts are preserved.

## Algorithm SEG-LEX-C (frozen)

Identical to SEG-LEX-P (PREREG_SEG2.md) except:

1. **Coverage discounting (Phase 1b, new).** After chunk induction, for
   each chunk C compute uncovered(C): the number of occurrences of C
   in the training corpus that are NOT strictly contained in an
   occurrence of a longer recurring chunk. Formally, an occurrence of
   C at (string s, position p) is covered iff there exists a chunk D
   with count(D) >= MINC, len(D) > len(C), matching s at q, with
   q <= p and p + len(C) <= q + len(D). (With len(D) > len(C) this
   implies strict containment.) The DP score becomes
   score(C) = uncovered(C) * len(C)^2. The MINC >= 2 recurrence gate
   stays on the raw count; only the score is discounted.
   Rationale (frozen): a lexicon entry's value is its unexplained
   occurrences. A chunk whose every occurrence is already explained by
   a longer recurring chunk is redundant; its score collapses to ~0
   for ANY raw count, which removes the frequency-band dependence that
   killed H-SEG2's generality claim. No new constant is introduced;
   the discount is computed from the data. The containment family
   itself, MAXL=5, MINC=2, the len^2 shape, and FBPEN=20 remain
   authored (honest labeling). FBPEN is retained as a residual
   unexplained-material cost; it is no longer the load-bearing repair.

2. **Robustness: stacks and buffers sized by n (input length).**
   build_best's move stacks: (n+1) entries instead of 64. enum_bwd's
   recursion stacks: (n+1) entries instead of 64. Single-best output
   buffer: 2*n+8 bytes instead of 256. Ambiguity-candidate result rows:
   stride 2*n+16 bytes instead of 80 (enum_bwd takes the stride as a
   parameter). Rationale: a segmentation path has at most n moves
   (each move advances >= 1), so (n+1) entries can never overflow;
   a printed segmentation needs at most 2*n-1 bytes (n chars plus
   n-1 separators). The 8-move cap per position in mv_add and the
   nopt cap of 999 are UNCHANGED and documented as remaining
   boundaries (informational in the X-SG2-4 audit, no demonstrated
   failure).

All else unchanged: MAXL=5, MINC=2, FBPEN=20, DPSENT=-1000000,
nopt tie counting, AMBIGUOUS on ties.

## Frozen design analysis (predictions)

ADV-1 corpus ("xabcd"x2, "yabcd"x2, "zabcd"x2): "abcd" count 6, every
occurrence inside "xabcd"/"yabcd"/"zabcd" (count 2, len 5) ->
uncovered 0 -> score 0. "xabcd"/"yabcd"/"zabcd" uncovered 2 ->
score 50 each. T1 "xabcd": best tiling "xabcd" = 50 (competitor
"x|abcd" = -20 + 0 = -20). T2 "xabcdyabcd": "xabcd|yabcd" = 100
(competitor "x|abcd|y|abcd" = -40). ADV-2 adds "wabcd"x2 (score 50);
"abcd" count 8 still fully covered -> 0; T2 unchanged at 100.

Frozen EXP-A: "all" count 4, all occurrences inside "small"/"ball"
-> score 0. "small|green|ball" = 50 + 50 + 32 = 132; strongest
fragment competitor "small|green|b|all" = 80. EXP-B: "ab" uncovered 2
-> 8; "abc" -> 18; "bc" covered by "abc" -> 0; "cde" -> 18; "de"
uncovered 2 -> 8; "cd" covered by "cde" -> 0. Test "abcde": tie
"ab|cde" = 26 vs "abc|de" = 26 -> AMBIGUOUS, same candidates.
EXP-C "smallredcube": "small|red|cube" = 100. EXP-D "bigbluecube":
"big|b|l|u|e|cube" = -30 (no chunk matches "blue" material).

ADV-3: 120-char digit string, zero chunk matches, pure fallback:
SCORE -2400, NOPT 1, completes with exit 0 (120 <= n+1 stack).

## Experiments

### ADV-1-T1 / ADV-1-T2 / ADV-2-T2 (K-SG3-1)

Corpora and tests exactly as frozen in PREREG_SEG2_ADV.md (ADV-1:
6 strings; ADV-2: 8 strings; T1 "xabcd"; T2 "xabcdyabcd").
**Expected:** T1 SEGMENTED "xabcd", NOPT 1. T2 (both corpora)
SEGMENTED "xabcd|yabcd", NOPT 1.

### ADV-3 (K-SG3-2)

Frozen EXP-A corpus table; test = "0123456789" x 12 (120 chars).
**Expected:** exit 0, SCORE -2400, NOPT 1, VERDICT SEGMENTED.
No crash, no hang (20 s timeout per run), no corrupted output.

### EXP-A / EXP-B / EXP-C / EXP-D (K-SG3-3)

Same corpora and tests as H-SEG2 frozen bars.
**Expected (identical to H-SEG2):** EXP-A SEGMENTED "small|green|ball",
score 132, NOPT 1. EXP-B AMBIGUOUS with candidates "ab|cde" and
"abc|de". EXP-C SEGMENTED "small|red|cube", score 100, NOPT 1.
EXP-D SEGMENTED "big|b|l|u|e|cube", score -30, NOPT 1.
(Note: EXP-B candidate scores become 26/26 under discounting; the bar
is on verdict and candidate identities, not the score value.)

### Determinism (K-SG3-4)

Three consecutive runs byte-identical (cmp-verified), including ADV-3.

## Kill bars (frozen)

- K-SG3-1 (generality repair, 3/3): ADV-1-T1, ADV-1-T2, ADV-2-T2
  produce exactly the expected segmentations with NOPT == 1.
- K-SG3-2 (robustness, 1/1): ADV-3 completes, exit 0, SCORE -2400,
  NOPT 1, VERDICT SEGMENTED.
- K-SG3-3 (no regression, 4/4): EXP-A/B/C/D verdicts identical to
  H-SEG2 (per expected values above).
- K-SG3-4 (determinism, 1/1): three runs byte-identical.

## What kills H-SEG3

- Any of K-SG3-1, K-SG3-2, K-SG3-3 failing on the exact expected
  outputs: H-SEG3 KILLED, actual output documented.
- Non-deterministic output: K-SG3-4 FAILS, H-SEG3 KILLED.

## Honest failure modes (documented, not hidden)

1. Coverage discounting is structural and data-derived, but the
   containment family is researcher-chosen; it is not a learned
   representation. A pass is at most bounded L2 structural learning,
   not L3.
2. A genuine morpheme that only ever occurs inside a longer recurring
   chunk would be discounted to ~0. The frozen fixtures do not test
   this; it is a known boundary of the rule.
3. The 8-move cap per position and nopt cap 999 remain (unchanged from
   H-SEG2); heavy-tie inputs could still corrupt AMBIGUOUS
   enumeration. No demonstrated failure; documented boundary.
4. MAXL=5: words longer than 5 characters cannot be single chunks
   (pre-existing boundary, unchanged).
5. This test does not address slot assignment, compositional semantics,
   or novel referents (open per RESULT_SYNLANG.md).

## Scope

Bounded to raw-sequence word segmentation with coverage-discounted
scoring plus input-sized stacks/buffers. Eight experiments, nine
checks. Pure Zag. No Python.

## Prereg commit ordering

This file is committed before any implementation or result. The
implementation (seg3_learn.zag) and result (SEG3_RESULT.md) come in
later commits.
