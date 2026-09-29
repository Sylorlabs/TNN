# PREREG H-SEG4: Growable Sentinel and Honest Cap Label

**Status:** FROZEN. This prereg strictly precedes implementation.
**Date:** 2026-09-29
**Author:** H-SEG4 Frontier Researcher (subagent)
**Parent result:** H-SEG3 SURVIVES (9/9); red team (SEG3-ADV) all four
attacks fail. Clean survival. See SEG3_ADV_RESULT.md.

## Background

The H-SEG3 red team confirmed two remaining boundaries, both
documented as informational:

1. **P-SENT (DP sentinel degeneracy).** The DP uses a fixed
   unreachable sentinel DPSENT = -1000000. The single-char fallback
   scores -FBPEN = -20 per character, so an all-fallback path of
   length n scores -20n. For n >= 50000 the fallback path reaches the
   sentinel value exactly, the reachability guard `dpi > DPSENT()`
   stops propagating, and a 60000-char input yields the degenerate
   output SCORE -1000000, NOPT 0, VERDICT AMBIGUOUS, NCAND 0.
   Degenerate-but-no-crash; pre-existing in H-SEG2, unchanged by
   H-SEG3.
2. **NOPT 999 cap honesty.** On heavy-tie inputs the optimal-path
   count saturates at 999 and prints as a plain "NOPT 999",
   indistinguishable from a genuine count of exactly 999. The
   red-team H1 fixture ("ab" x 30, true count Fib(31) = 1346269)
   saturates it.

## Hypothesis H-SEG4

A per-run sentinel derived from the input instance closes the P-SENT
degeneracy structurally (no new constant, no arbitrary length cap),
and a saturation flag makes the 999 cap print honestly, while all
nine frozen H-SEG3 checks are preserved byte-for-byte.

## Algorithm SEG-LEX-D (frozen)

Identical to SEG-LEX-C (PREREG_SEG3.md) except:

1. **Growable DP sentinel (P-SENT repair).** In `run_exp`, with test
   input length n, compute `sent = 0 - FBPEN()*n - 1`. Initialize the
   dp array to `sent` and use `dpi > sent` as the reachability guard.
   Rationale (frozen): every DP move scores >= -FBPEN (fallback) or
   >= 0 (chunk scores are uncovered*len^2, both non-negative), so any
   path ending at position i scores >= -FBPEN*i >= -FBPEN*n > sent.
   The value `sent` is therefore strictly below every reachable
   score and every array cell still holding `sent` is genuinely
   unreached, for every n. Reachability becomes exact at any input
   length. No new constant is introduced; the bound is derived from
   the instance (FBPEN and n). The fixed DPSENT() function is removed
   (its only two uses were the dp init and the guard in run_exp).
   Frozen hand prediction: 60000-char digit string on the corpus-A
   table is pure fallback, score -20*60000 = -1200000 > sent
   (-1200001) at every position, so every position propagates:
   SCORE -1200000, NOPT 1, VERDICT SEGMENTED, exit 0.

2. **Honest nopt cap label.** `relax` takes a per-run saturation flag
   (a 4-byte zeroed buffer). When the 999 clamp fires (`v > 999`),
   the flag is set. `run_exp` prints "NOPT 999+" iff the final count
   is 999 and the flag is set, else the plain count. Rationale
   (frozen): the clamp fires only when a true subtotal exceeds 999,
   and nopt values only grow by adding positive integers, so
   (final == 999 and flag set) implies the true count strictly
   exceeds 999, while (final == 999 and flag clear) implies the true
   count is exactly 999. The label is exactly honest. No frozen test
   saturates the cap, so no frozen output line changes.

3. **New fixtures (test-only; no learning-logic change).**
   - Corpus id 4 = H1 (the red-team X-SG3-2 fixture, byte-identical
     strings): "xab"x2, "yab"x2, "zabab"x2, "wabab"x2 (8 strings).
     Test H1-T = "ab" x 30 (60 chars).
   - SENT60: corpus-A table, test = "0123456789" x 6000
     (60000 chars, zero chunk matches, pure fallback).
   - LONG60: ADV-1 table, test = "xabcd" x 12000 (60000 chars).
     Frozen hand prediction: the only positive chunks in the ADV-1
     lexicon are xabcd/yabcd/zabcd (score 50 each); every len 2..4
     chunk is fully covered by a longer recurring chunk (score 0).
     No corpus substring spans a block boundary (no corpus string
     contains "dx", so no chunk matches text crossing from one
     "xabcd" block to the next). Each 5-char block is therefore
     uniquely optimal as "xabcd" (50 beats "x|abcd" = -20): SCORE
     12000*50 = 600000, NOPT 1, VERDICT SEGMENTED.

All else unchanged: MAXL=5, MINC=2, FBPEN=20, coverage discounting,
input-sized stacks/buffers, 8-move cap per position, nopt cap 999,
AMBIGUOUS on ties, NCAND cap 5.

## Experiments

### SENT60 (K-SG4-1)

Corpus-A table; test = "0123456789" x 6000 (60000 chars).
**Expected:** exit 0, SCORE -1200000, NOPT 1, VERDICT SEGMENTED.
No crash, no hang (60 s timeout per run), no corrupted output.

### LONG60 (K-SG4-2)

ADV-1 table; test = "xabcd" x 12000 (60000 chars).
**Expected:** exit 0, SCORE 600000, NOPT 1, VERDICT SEGMENTED
("xabcd" repeated with "|" separators).

### H1-T (K-SG4-3)

Corpus id 4 (H1); test = "ab" x 30 (60 chars).
**Expected:** exit 0, VERDICT AMBIGUOUS, the NOPT field prints
exactly "999+" (saturation label), NCAND 5. Per SEG3-ADV the true
count is Fib(31) = 1346269 and all 5 enumerated candidates re-score
to the best score 0.

### Regression: all H-SEG3 frozen checks (K-SG4-4)

ADV1-T1, ADV1-T2, ADV2-T2, ADV3 (120-char), EXP-A, EXP-B, EXP-C,
EXP-D, in the same order as seg3_learn.zag main(). **Expected:** the
corresponding output lines are byte-identical to SEG3_RAW_OUTPUT.txt
(the mechanism path is unchanged for non-saturating short inputs;
the sentinel and cap-label changes provably do not alter them).
Header/footer lines change to the H-SEG4 banner.

### Determinism (K-SG4-5)

Three consecutive runs byte-identical (cmp-verified), including the
60000-char tests.

## Kill bars (frozen)

- K-SG4-1 (sentinel repair, 1/1): SENT60 produces exactly SCORE
  -1200000, NOPT 1, VERDICT SEGMENTED, exit 0.
- K-SG4-2 (long input with chunk matches, 1/1): LONG60 produces
  exactly SCORE 600000, NOPT 1, VERDICT SEGMENTED, exit 0.
- K-SG4-3 (honest cap, 1/1): H1-T produces VERDICT AMBIGUOUS with
  the NOPT field printing exactly "999+", exit 0.
- K-SG4-4 (no regression, 9/9): all nine H-SEG3 frozen checks pass
  with byte-identical output lines (K-SG3-1 3/3, K-SG3-2 1/1,
  K-SG3-3 4/4).
- K-SG4-5 (determinism, 1/1): three runs byte-identical.

## What kills H-SEG4

- Any of K-SG4-1, K-SG4-2, K-SG4-3 failing on the exact expected
  outputs: H-SEG4 KILLED, actual output documented.
- Any K-SG4-4 regression: H-SEG4 KILLED.
- Non-deterministic output: K-SG4-5 FAILS, H-SEG4 KILLED.

## Honest failure modes (documented, not hidden)

1. The per-run sentinel makes reachability exact, but DP time is
   O(n * nch) and memory is O(n); practical input size is
   allocation-bound. This is an engineering bound, not a correctness
   boundary.
2. enum_bwd recursion depth is bounded by the number of moves (<= n);
   on heavily-tied very long inputs the host call stack is the
   bound. Not exercised by the frozen fixtures (H1-T depth <= 60;
   SENT60/LONG60 have NOPT 1 so enum_bwd is not called).
3. The 999+ label reports saturation honestly but the exact count
   above the cap remains unrecoverable (unchanged).
4. MAXL=5, the containment family, the len^2 shape, MINC=2 remain
   authored (unchanged). A pass is at most bounded L2 structural
   learning, not L3.

## Scope

Bounded to raw-sequence word segmentation: growable DP sentinel plus
honest cap label, two 60000-char stress fixtures, one saturation
fixture. Five kill bars, thirteen checks. Pure Zag. No Python.

## Prereg commit ordering

This file is committed before any implementation or result. The
implementation (seg4_learn.zag) and result (SEG4_RESULT.md) come in
later commits.
