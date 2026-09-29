# SEG3 RESULT: H-SEG3 SURVIVES (9/9)

**Date:** 2026-09-29
**Prereg:** PREREG_SEG3.md (commit 31b718fa2, frozen before implementation)
**Implementation:** seg3_learn.zag (this directory)
**Raw evidence:** SEG3_RAW_OUTPUT.txt (md5 b9c585fa426222b02e8011e19c8a8277, 3/3 byte-identical)
**Toolchain:** znc 2026.07.0-dev (edition 2026)
**Purity:** Pure Zag. No Python anywhere.

## Verdict: H-SEG3 SURVIVES (9/9)

All three H-SEG2 red-team failure classes are repaired. The
frequency-fragile constant penalty is replaced by a data-derived
coverage discount; the 64-entry move stacks are sized by input length.

## What was built

`seg3_learn.zag` = `seg2_learn.zag` plus:

**Repair 1 (X-SG2-1/X-SG2-2): coverage-discounted chunk scoring.**
New Phase 1b: for each chunk C, uncovered(C) counts occurrences NOT
strictly contained in an occurrence of a longer recurring chunk
(count >= 2). DP score(C) = uncovered(C) * len(C)^2. The MINC >= 2
gate stays on the raw count. Rationale (frozen): a lexicon entry's
value is its unexplained occurrences; a chunk explained everywhere by
a longer recurring chunk is redundant and scores ~0 for ANY raw
count. No new constant. The containment family, MAXL=5, MINC=2, the
len^2 shape, and FBPEN=20 remain authored. FBPEN is now a residual
unexplained-material cost, not the load-bearing repair.

**Repair 2 (X-SG2-3): input-sized stacks and buffers.** build_best and
enum_bwd move stacks: (n+1) entries (a path has at most n moves, each
advancing >= 1, so overflow is impossible). Single-best output buffer:
2*n+8 bytes. Ambiguity-candidate rows: stride 2*n+16 (enum_bwd takes
the stride as a parameter). The 8-move cap per position and nopt cap
999 are unchanged (documented boundary, no demonstrated failure).

## Frozen bar results

- **K-SG3-1 PASS (3/3):** ADV1-T1 "xabcd" -> SEGMENTED "xabcd",
  score 50, NOPT 1 (was "x|abcd" under H-SEG2). ADV1-T2 "xabcdyabcd"
  -> SEGMENTED "xabcd|yabcd", score 100, NOPT 1. ADV2-T2 ->
  SEGMENTED "xabcd|yabcd", score 100, NOPT 1. The spurious "abcd"
  (count 6/8) is fully covered by "xabcd"/"yabcd"/"zabcd"/"wabcd"
  (uncovered 0, score 0), so the failure recurs at no frequency.
- **K-SG3-2 PASS (1/1):** ADV3 120-char digit string -> exit 0,
  SCORE -2400, NOPT 1, VERDICT SEGMENTED. No crash, no hang.
- **K-SG3-3 PASS (4/4):** EXP-A SEGMENTED "small|green|ball", 132,
  NOPT 1. EXP-B AMBIGUOUS, candidates "ab|cde" and "abc|de",
  NOPT 2. EXP-C SEGMENTED "small|red|cube", 100, NOPT 1. EXP-D
  SEGMENTED "big|b|l|u|e|cube", -30, NOPT 1. All identical to H-SEG2
  verdicts.
- **K-SG3-4 PASS (1/1):** 3 consecutive runs byte-identical
  (cmp-verified), md5 b9c585fa426222b02e8011e19c8a8277.

## Correction to the prereg's design-analysis note

PREREG_SEG3.md predicted EXP-B candidates would tie at 26/26. The
actual tie is 22/22: the implementation correctly discounts two
chunks the hand analysis missed ("ab" is covered once by the
recurring "zab", uncovered 1 -> 4; "de" is covered once by the
recurring "dez", uncovered 1 -> 4). The frozen bar constrains verdict
and candidate identities only, so K-SG3-3 still passes; the mechanism
is behaving as specified, and the hand analysis was wrong, not the
code. "all" in EXP-A discounts to exactly 0 as predicted
(count 4 -> uncovered 0).

## Source audit (self)

- No expected-output literals in the learning path; corpora are
  disclosed fixtures; verdict strings are generic.
- Coverage check is structural (length comparisons and byte matches).
- FBPEN/DPSENT/MAXL/MINC unchanged from H-SEG2.

## Classification

Bounded L2 structural learning repair, not L3. The discount rule is
data-derived (no new constant) but the containment family is
researcher-chosen. Value: the shared-substring failure class is
closed in general (spurious chunk score -> 0 at any count), not in a
tuned frequency band, and the mechanism no longer crashes on long
inputs.

## Honest limits (carried from prereg)

1. A genuine morpheme occurring only inside a longer recurring chunk
   would be discounted to ~0. Not tested; known boundary.
2. 8-move cap per position and nopt cap 999 remain.
3. MAXL=5: words longer than 5 chars cannot be single chunks.
4. Slot assignment, compositional semantics, novel referents remain
   open per RESULT_SYNLANG.md.

## Commits (branch tnn-native-lab, local only)

- 31b718fa2 -- PREREG H-SEG3 FROZEN (before any implementation)
- (this commit) -- seg3_learn.zag, SEG3_RAW_OUTPUT.txt,
  SEG3_RESULT.md
- Commit order: prereg strictly precedes implementation (verified via
  merge-base --is-ancestor before pushing this report upstream).

## Files

- docs/lab/research-lead/overnight-20260928/PREREG_SEG3.md
- docs/lab/research-lead/overnight-20260928/seg3_learn.zag
- docs/lab/research-lead/overnight-20260928/SEG3_RESULT.md
- docs/lab/research-lead/overnight-20260928/SEG3_RAW_OUTPUT.txt

## Governance

Pure Zag throughout; no Python at any stage. No em dashes. Only
H-SEG3-owned files staged and committed; concurrent agents' files
untouched. No binaries committed (build ran in /tmp).
