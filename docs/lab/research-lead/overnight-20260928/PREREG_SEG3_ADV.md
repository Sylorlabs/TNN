# PREREG H-SEG3-ADV: H-SEG3 Red Team (frozen)

**Status:** FROZEN. This prereg strictly precedes any attack implementation
or execution.
**Date:** 2026-09-29
**Author:** H-SEG3 Red Team (subagent, independent of H-SEG3 builder)
**Target:** H-SEG3 SURVIVES (9/9), SEG3_RESULT.md, seg3_learn.zag
(commit 522acf3a4). Prereg of target: PREREG_SEG3.md (31b718fa2).

## Mission

Assume the H-SEG3 claim is false. Attack the two repairs:
(R1) coverage-discounted chunk scoring closes the shared-substring
failure class for any frequency; (R2) input-sized stacks remove the
long-input crash. Four preregistered attacks below. Pure Zag. No Python.

## Attack X-SG3-1: genuine morpheme discounted to ~0

The target's own honest failure mode #1: "A genuine morpheme occurring
only inside a longer recurring chunk would be discounted to ~0."
Construct the fixture and test whether the discount is verdict-harmful.

Fixture G1 (mirrors ADV-1 structure): corpus "xbcde" x2, "ybcde" x2,
"zbcde" x2. Expected lexicon: "xbcde"/"ybcde"/"zbcde" len 5 count 2
score 50; "bcde" count 6 fully covered -> score 0; all shorter
substrings score 0.

- G1-T1: "xbcde" -> expect SEGMENTED "xbcde", score 50, NOPT 1.
  (Sanity: genuine words still segment.)
- G1-T2: "bcde" (the fully discounted substring, never standalone in
  corpus). Predicted tilings: "bcde" = 0; "bc|de" = 0 + 0 = 0;
  "bcd|e" = -20; "b|cde" = -20; all-chars = -80.
  Predicted: AMBIGUOUS with candidates "bcde" and "bc|de".
- G1-T3: "xbcdeybcde" -> expect SEGMENTED "xbcde|ybcde", 100, NOPT 1.
- G1-T4: "qbcde" (novel prefix + discounted chunk). Predicted:
  "q|bcde" = -20 and "q|bc|de" = -20 tie -> AMBIGUOUS; the discounted
  chunk must be recovered, not shattered into chars.

Kill/downgrade criteria (frozen):
- DOWNGRADE iff any G1 test yields a confidently WRONG segmentation
  (SEGMENTED with NOPT 1 and a segmentation that shatters or drops
  the discounted word, e.g. "b|c|d|e"), or any crash/hang/corrupt
  output. AMBIGUOUS that includes the discounted word as a candidate
  is honest, not a failure: the corpus never shows "bcde" standalone.
- If all four behave as predicted (or honest-AMBIGUOUS), X-SG3-1 FAILS
  (attack fails, mechanism holds on this fixture).

## Attack X-SG3-2: heavy ties against the remaining caps

Prereg honest mode #3: "The 8-move cap per position and nopt cap 999
remain; heavy-tie inputs could still corrupt AMBIGUOUS enumeration."
Demonstrate the boundary and test whether enumeration corrupts.

Fixture H1: corpus "xab" x2, "yab" x2, "zabab" x2, "wabab" x2.
Expected lexicon: "xab"/"yab" len 3 count 2 score 18; "zabab"/"wabab"
len 5 count 2 score 50; "ab" count 8 fully covered -> 0; "abab"
count 4 fully covered -> 0; all other substrings 0.
Test: "ab" repeated 30 times (60 chars). Every even position admits
"ab" (0) and every position 0..56 step 2 admits "abab" (0); no
positive chunk matches. Best score 0. True number of optimal tilings:
f(0)=1, f(2k)=f(2k-1... positions step 2: ways(2k)=ways(2k-2)+
ways(2k-4) -> ways(60) = Fib(31) = 1346269.

Frozen expectations:
- Exit 0, no hang (30 s timeout), no crash.
- VERDICT AMBIGUOUS, NOPT == 999 (cap saturation; true count
  1346269), NCAND == 5 (enumeration cap).
- Every enumerated candidate re-scores (by independent summation of
  chunk scores over "|" separated pieces, fallback -20/char) to
  exactly the printed best SCORE (0).

Kill/downgrade criteria (frozen):
- KILL iff crash, hang, or corrupt output.
- DOWNGRADE iff verdict is not AMBIGUOUS despite massive ties, or
  any enumerated candidate does not re-score to the best score
  (corrupt enumeration), or NOPT == 1 (ties hidden).
- NOPT == 999 while the true count is 1346269 is the DOCUMENTED cap;
  confirming it is an informational boundary confirmation, not a
  downgrade.

## Attack X-SG3-3: independent coverage audit

Write an independent brute-force coverage checker directly from the
prereg spec text (no q-window optimization): occurrence of C at (s,p)
is covered iff there exists chunk D with count(D) >= MINC,
len(D) > len(C), whose bytes match s at some q with q <= p and
p + len(C) <= q + len(D). Cross-check its uncovered counts against
the mechanism's dumped uncovered values for every chunk on corpora:
frozen A, frozen B, ADV-1, ADV-2, G1, H1.

Kill/downgrade criteria (frozen):
- DOWNGRADE iff any chunk's brute-force uncovered count differs from
  the mechanism's dumped uncovered value (implementation does not
  match spec). KILL iff the mismatch changes a frozen verdict
  (re-run of frozen suite is included in the harness; see below).

## Attack X-SG3-4: source audit

- (a) The adversary harness's mechanism region is byte-identical to
  seg3_learn.zag except for the documented fixture/main changes
  (verified by diff).
- (b) diff seg3_learn.zag vs seg2_learn.zag shows only additive
  changes: Phase 1b coverage discounting, input-sized stacks/buffers,
  main() fixtures. No other learning-path changes.
- (c) No expected-output literals in the learning path: grep the
  mechanism region for "small|green|ball", "xabcd|yabcd",
  "SEGMENTED", "AMBIGUOUS" outside of emit/verdict-print code.
- (d) Stack/buffer sizing claims verified by reading: build_best
  stacks (n+1), enum_bwd caller stacks (n+1), single-best buffer
  2*n+8, candidate row stride 2*n+16.
- (e) Prereg compliance: score(C) = uncovered(C)*len(C)^2;
  MINC >= 2 gate on the RAW count; FBPEN retained as residual
  fallback cost only.

Kill/downgrade criteria (frozen):
- DOWNGRADE iff any check fails (hardcoding, wrong sizing with a
  demonstrable overflow, or spec non-compliance).

## Regression control

The harness first re-runs the exact frozen H-SEG3 suite
(EXP-A/B/C/D, ADV1-T1/T2, ADV2-T2, ADV3) and the raw output is
diffed against SEG3_RAW_OUTPUT.txt. Any divergence KILLS the
adversary harness as invalid (not the target); a divergence caused
by the target's nondeterminism would KILL the target.

## Informational probe P-SENT (not a kill criterion)

60000-char digit string on the corpus-A table. The DP sentinel is
-1000000 and fallback is -20/char, so positions >= 50000 are
unreachable by construction (pre-existing in H-SEG2, unchanged).
Record behavior: predicted degenerate-but-no-crash
(SCORE -1000000, NOPT 0, VERDICT AMBIGUOUS, NCAND 0). A crash here
would be a DOWNGRADE (robustness). Degenerate output is a
boundary confirmation for a future hypothesis.

## What kills vs downgrades H-SEG3

- KILL: crash/hang/corrupt output on any attack fixture; any frozen
  bar failing in the regression control due to target behavior;
  confidently-wrong SEGMENTED verdict on G1.
- DOWNGRADE: corrupt AMBIGUOUS enumeration (X-SG3-2); coverage
  implementation not matching spec (X-SG3-3); source audit failure
  (X-SG3-4).
- Informational: nopt 999 saturation; P-SENT sentinel degeneracy;
  X-SG3-1 failing (mechanism handles the documented boundary
  gracefully).

## Execution plan (frozen)

1. Commit this prereg before writing any attack code.
2. Build seg3_adv.zag: byte-copy of seg3_learn.zag with ONLY the
   corpus fixture extensions (G1/H1 corpora + dispatch), appended
   independent audit functions, and a replaced main(). Diff-verify
   the learning path is untouched.
3. Compile with znc to /tmp (no binaries committed). Run 3x;
   md5 the raw output; runs must be byte-identical.
4. Analyze raw output against the frozen criteria above.
5. Write SEG3_ADV_RESULT.md + SEG3_ADV_RAW.txt; commit only
   adversary-owned files.

## Governance

Pure Zag. No Python at any stage. No em dashes. Only stage and
commit adversary-owned files; leave concurrent agents' files alone.
