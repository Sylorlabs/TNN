# SEG3-ADV RESULT: H-SEG3 Red Team

**Verdict: H-SEG3 SURVIVES. All four preregistered attacks fail.**
**Date:** 2026-09-29
**Prereg:** PREREG_SEG3_ADV.md (commit c3aaac6b3, frozen before any attack code)
**Harness:** seg3_adv.zag (this directory)
**Raw evidence:** SEG3_ADV_RAW.txt (md5 66db4c69adb63fd4a7c7690d82312c7e, 3/3 runs byte-identical)
**Toolchain:** znc 2026.07.0-dev (edition 2026)
**Purity:** Pure Zag. No Python at any stage.

## Method

seg3_adv.zag is a byte-copy of seg3_learn.zag (commit 522acf3a4) with
ONLY three documented changes, verified by diff:
1. Corpus fixture block extended with G1/H1 corpora (ids 4,5) and
   dispatch (fixtures, not learning logic).
2. Appended independent audit functions: cover_bf (brute-force
   coverage written directly from the prereg spec text, no q-window
   optimization), audit_uncovered, ch_find, verify_cand, xrun_verify.
3. Replaced main(): frozen regression suite first, then attacks.

The learning path (chunk induction, occ_covered, compute_uncovered,
ch_uscore, mv_add, relax, build_best, enum_bwd, dump_lexicon,
run_exp) is byte-identical to seg3_learn.zag. The only removed lines
in the diff are the corpus dispatch fallthrough (extended, not
removed), header/footer emits, and one comment.

## Regression control: PASS

The harness re-runs the exact frozen H-SEG3 suite (EXP-A/B/C/D,
ADV1-T1/T2, ADV2-T2, ADV3). Output is byte-identical to
SEG3_RAW_OUTPUT.txt (diffed after stripping header/footer lines).

## X-SG3-1 (genuine morpheme discounted): ATTACK FAILS

Fixture G1: corpus "xbcde" x2, "ybcde" x2, "zbcde" x2. Lexicon
confirms "bcde" count 6, uncovered 0, score 0; "xbcde"/"ybcde"/
"zbcde" score 50; all shorter substrings score 0.

- G1-T1 "xbcde": SEGMENTED "xbcde", score 50, NOPT 1. As predicted.
- G1-T2 "bcde": AMBIGUOUS, candidates "bcde" and "bc|de", score 0,
  NOPT 2. As predicted. The fully discounted word is recovered as a
  candidate, not shattered.
- G1-T3 "xbcdeybcde": SEGMENTED "xbcde|ybcde", 100, NOPT 1.
- G1-T4 "qbcde" (novel prefix): AMBIGUOUS, candidates "q|bcde" and
  "q|bc|de", score -20. The discounted chunk is recovered, not
  shattered into chars.

No confidently-wrong segmentation on any G1 test. The discount-to-zero
is verdict-safe: a zero-score chunk always beats fallback chars
(0 > -20/len), so it is used whenever no positive-score alternative
covers the span; the only "losses" are honest ties (AMBIGUOUS) or
losses to corpus-supported positive chunks (defensible). The
documented boundary (honest failure mode #1) is, if anything,
less severe than stated.

## X-SG3-2 (heavy ties): ATTACK FAILS, boundary confirmed as documented

Fixture H1: corpus "xab" x2, "yab" x2, "zabab" x2, "wabab" x2; test
"ab" x 30 (60 chars). "ab" count 8 fully covered -> 0; "abab"
count 4 fully covered -> 0; no positive chunk matches the test.
True number of optimal tilings: ways(2k) = ways(2k-2) + ways(2k-4),
ways(60) = Fib(31) = 1346269.

- Exit 0, no hang, no crash.
- SCORE 0, NOPT 999 (cap saturation; true count 1346269),
  VERDICT AMBIGUOUS-TIED, NCAND 5.
- All 5 enumerated candidates independently re-scored (string
  parsing path: chunk uscore summation, -20 per single char) to
  exactly the best score 0: VERIFY-ALL-OK.

No corrupt enumeration, no hidden ties, no crash. The NOPT 999
saturation is exactly the documented cap (prereg honest mode #3);
confirming it is an informational boundary confirmation, not a
downgrade. Note: the 8-move cap in mv_add is dead code in practice
(at most 5 distinct (j,l) moves can reach any position: 1 fallback
+ 4 chunk lengths), so it cannot bind.

## X-SG3-3 (independent coverage audit): ATTACK FAILS

Brute-force checker (no window optimization) cross-checked against
the mechanism's dumped uncovered values for every chunk:

- AUD-A (corpus A, 108 chunks): bad=0
- AUD-B (corpus B, 22 chunks): bad=0
- AUD-ADV1 (18 chunks): bad=0
- AUD-ADV2 (22 chunks): bad=0
- AUD-G1 (18 chunks): bad=0
- AUD-H1 (17 chunks): bad=0

Implementation matches spec exactly on all 205 chunks.

## X-SG3-4 (source audit): PASS

- (a) Harness mechanism region byte-identical to seg3_learn.zag
  except documented fixture/audit/main changes (diff-verified).
- (b) seg3_learn.zag vs seg2_learn.zag: only additive changes.
  ch_score removed, ch_uscore added (old scorer fully replaced, no
  remaining references); occ_covered/compute_uncovered new;
  dump_lexicon/run_exp take unc; stacks (n+1); buf 2*n+8; stride
  2*n+16.
- (c) No expected-output literals in the learning path (grep for
  "small|green|ball", "xabcd|yabcd", "ab|cde": no hits).
- (d) Sizing verified by reading: build_best stacks (n+1) entries;
  enum_bwd caller stacks (n+1); single-best buffer 2*n+8 bytes;
  candidate row stride 2*n+16 bytes. A path has at most n moves
  (each advances >= 1); printed segmentation needs at most 2n-1
  bytes. No overflow possible.
- (e) Prereg compliance: score(C) = uncovered(C)*len(C)^2
  (ch_uscore); MINC >= 2 gate on the RAW count (run_exp checks
  ch_cnt, not uncovered); FBPEN=20 used only as the fallback
  single-char cost (one site).

## Informational probe P-SENT (not a kill criterion)

60000-char digit string on the corpus-A table: SCORE -1000000,
NOPT 0, VERDICT AMBIGUOUS, NCAND 0. No crash. This is the
pre-existing DP sentinel boundary (sentinel -1000000, fallback
-20/char: positions >= 50000 unreachable by construction; identical
in H-SEG2, unchanged by H-SEG3). Degenerate-but-no-crash output is
a boundary confirmation for a future hypothesis, not a downgrade:
the frozen robustness claim was the 120-char stack overflow, which
is fixed.

## Classification

H-SEG3 stands as bounded L2 structural learning repair, not L3
(unchanged). The coverage discount is data-derived but the
containment family, MAXL=5, MINC=2, and len^2 shape remain authored.

## Commits (branch tnn-native-lab, local only)

- c3aaac6b3: PREREG H-SEG3-ADV FROZEN (before any attack code)
- (this commit): seg3_adv.zag, SEG3_ADV_RAW.txt, SEG3_ADV_RESULT.md

## Files

- docs/lab/research-lead/overnight-20260928/PREREG_SEG3_ADV.md
- docs/lab/research-lead/overnight-20260928/seg3_adv.zag
- docs/lab/research-lead/overnight-20260928/SEG3_ADV_RAW.txt
- docs/lab/research-lead/overnight-20260928/SEG3_ADV_RESULT.md

## Governance

Pure Zag throughout; no Python at any stage. No em dashes in
adversary-authored content (the harness header comment is a
byte-verbatim copy of the target's). Only adversary-owned files
staged and committed; concurrent agents' files untouched. No
binaries committed (build ran in /tmp). Determinism: 3/3 runs
byte-identical (md5 66db4c69adb63fd4a7c7690d82312c7e).
