# SEG4 RESULT: H-SEG4 SURVIVES (13/13)

**Date:** 2026-09-29
**Prereg:** PREREG_SEG4.md (commit d7afeff5a, frozen before implementation)
**Implementation:** seg4_learn.zag (this directory)
**Raw evidence:** SEG4_RAW_OUTPUT.txt (md5 cd551d3bb7613b5bcd725bbff159c427, 3/3 byte-identical)
**Toolchain:** znc 2026.07.0-dev (edition 2026)
**Purity:** Pure Zag. No Python anywhere.

## Verdict: H-SEG4 SURVIVES (13/13)

Both red-team-documented H-SEG3 boundaries are closed: the P-SENT DP
sentinel degeneracy is repaired structurally with a per-run sentinel
derived from the input instance (no new constant, no arbitrary length
cap), and the nopt 999 cap now prints honestly as "999+" exactly when
the true count strictly exceeds 999.

## What was built

`seg4_learn.zag` = `seg3_learn.zag` plus the frozen SEG-LEX-D changes
(diff-verified; learning path otherwise byte-identical):

**Repair 1 (P-SENT): growable DP sentinel.** `run_exp` computes
`sent = 0 - FBPEN()*n - 1` from the test input length n, initializes
the dp array to `sent`, and uses `dpi > sent` as the reachability
guard. Proof of exactness (frozen in the prereg): every DP move
scores >= -FBPEN (single-char fallback) or >= 0 (chunk scores are
uncovered*len^2, both non-negative), so any path ending at position
i scores >= -FBPEN*i >= -FBPEN*n > sent; a cell holding `sent` is
genuinely unreached, for every n. The fixed DPSENT() = -1000000 is
removed (its only two uses were the dp init and the guard). No new
constant is introduced; the bound is derived from the instance.

**Repair 2 (honest cap label).** `relax` takes a per-run saturation
flag set when the 999 clamp fires. `run_exp` prints "NOPT 999+" iff
the final count is 999 and the flag is set, else the plain count.
Proof of exact honesty (frozen in the prereg): the clamp fires only
when a true subtotal exceeds 999, and nopt only grows by adding
positive integers, so (999 and flag set) implies the true count
strictly exceeds 999, while (999 and flag clear) implies it is
exactly 999.

**New fixtures (test-only; no learning-logic change):** corpus id 4 =
H1 (the red-team X-SG3-2 fixture, byte-identical strings); SENT60
("0123456789" x 6000 on the corpus-A table, pure fallback); LONG60
("xabcd" x 12000 on the ADV-1 table, chunk matches at 60000-char
scale).

## Frozen bar results

- **K-SG4-1 PASS (1/1):** SENT60 -> exit 0, SCORE -1200000, NOPT 1,
  VERDICT SEGMENTED. The per-run sentinel (-1200001) keeps every
  fallback position reachable; the P-SENT degeneracy (SCORE
  -1000000, NOPT 0, degenerate AMBIGUOUS) is gone.
- **K-SG4-2 PASS (1/1):** LONG60 -> exit 0, SCORE 600000, NOPT 1,
  VERDICT SEGMENTED ("xabcd" repeated). Chunk moves propagate
  correctly at 60000-char scale; each 5-char block is uniquely
  optimal at 50 (no cross-boundary chunk matches exist in the ADV-1
  lexicon), exactly as the frozen hand analysis predicted.
- **K-SG4-3 PASS (1/1):** H1-T -> exit 0, SCORE 0, NOPT printed as
  "999+", VERDICT AMBIGUOUS, NCAND 5. The saturation is now labeled
  honestly instead of printing a bare "999".
- **K-SG4-4 PASS (9/9):** all nine H-SEG3 frozen checks pass with
  byte-identical output lines (verified per-tag by cmp against
  SEG3_RAW_OUTPUT.txt): ADV1-T1 (50, "xabcd", NOPT 1), ADV1-T2 (100,
  "xabcd|yabcd", NOPT 1), ADV2-T2 (100, NOPT 1), ADV3 (120-char:
  -2400, NOPT 1, SEGMENTED), EXP-A (132, "small|green|ball", NOPT 1),
  EXP-B (22, AMBIGUOUS, NOPT 2), EXP-C (100, "small|red|cube",
  NOPT 1), EXP-D (-30, NOPT 1).
- **K-SG4-5 PASS (1/1):** 3 consecutive runs byte-identical
  (cmp-verified), md5 cd551d3bb7613b5bcd725bbff159c427, including
  the two 60000-char tests (total runtime about 1.2 s per run).

## Source audit (self)

- The seg4 vs seg3 diff contains only: DPSENT() removal, corpus_h1
  plus cid-4 dispatch, the sat parameter in relax, the per-run
  sentinel in run_exp, the 999+ label, and the three new fixture
  blocks in main(). No learning-logic change.
- No expected-output literals in the learning path; corpora are
  disclosed fixtures; verdict strings are generic.
- The 8-move cap per position and the nopt cap of 999 are unchanged
  (documented boundaries).

## Classification

Bounded L2 structural learning repair, not L3. The sentinel is
derived from the instance rather than learned, and the containment
family, MAXL=5, MINC=2, the len^2 shape remain authored. Value: the
documented P-SENT degeneracy is closed in general (exact
reachability at any input length, no new arbitrary bound), and the
saturation cap is now exactly honest.

## Honest limits (carried from prereg)

1. DP time is O(n * nch) and memory is O(n); practical input size is
   allocation-bound (engineering bound, not a correctness boundary).
2. enum_bwd recursion depth is bounded by the number of moves (<= n);
   on heavily-tied very long inputs the host call stack is the
   bound. Not exercised by the frozen fixtures (H1-T depth <= 60;
   SENT60/LONG60 have NOPT 1 so enum_bwd is not called).
3. The 999+ label is exactly honest but the count above the cap
   remains unrecoverable.
4. A genuine morpheme occurring only inside a longer recurring chunk
   is still discounted to ~0 (H-SEG3 boundary, unchanged).

## Commits (branch tnn-native-lab, local only)

- d7afeff5a -- PREREG H-SEG4 FROZEN (before any implementation)
- (this commit) -- seg4_learn.zag, SEG4_RAW_OUTPUT.txt,
  SEG4_RESULT.md
- Commit order: prereg strictly precedes implementation (verified via
  merge-base --is-ancestor).

## Files

- docs/lab/research-lead/overnight-20260928/PREREG_SEG4.md
- docs/lab/research-lead/overnight-20260928/seg4_learn.zag
- docs/lab/research-lead/overnight-20260928/SEG4_RESULT.md
- docs/lab/research-lead/overnight-20260928/SEG4_RAW_OUTPUT.txt

## Governance

Pure Zag throughout; no Python at any stage. No em dashes. Only
H-SEG4-owned files staged and committed; concurrent agents' files
untouched. No binaries committed (build ran in /tmp/seg4).
