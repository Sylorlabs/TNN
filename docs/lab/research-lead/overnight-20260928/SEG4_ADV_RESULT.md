# SEG4-ADV RESULT: H-SEG4 Red Team Report

**Date:** 2026-09-29
**Author:** H-SEG4 Red Team (subagent)
**Prereg:** PREREG_SEG4_ADV.md (commit 0fa95b3c9, frozen before any
attack code or execution)
**Target:** H-SEG4 SURVIVES (13/13), implementation commit 9618ffeb4
**Harness:** seg4_adv.zag (mechanism region byte-identical to
seg4_learn.zag lines 1-415; only main() replaced; verified by cmp)
**Raw evidence:** SEG4_ADV_RAW.txt (md5
94006076321d97b44631404c61efd609, 3/3 byte-identical)
**Toolchain:** znc 2026.07.0-dev (edition 2026)
**Purity:** Pure Zag. No Python anywhere.

## Verdict: H-SEG4 SURVIVES this red team

All four preregistered attacks fail. The growable sentinel holds at
every tested length including the exact length where the old fixed
sentinel degenerated. The 999+ cap label is exactly honest on all
800 searched cases; no mislabeling fixture was found. The
regression reproduces byte-for-byte. The source audit is clean.

One significant documentation correction (not a mechanism failure):
the true optimal-path count for the H1-T fixture is 2^29 =
536870912, not Fib(31) = 1346269 as stated in SEG3_ADV_RESULT.md,
PREREG_SEG4.md, and SEG4_RESULT.md. The X-SG3-2 analysis missed
three zero-score chunks ("aba", "ba", "bab") that match the test
and participate in optimal tilings. The "999+" label remains
correct (536870912 > 999), so no frozen bar is affected.

## Attack X-SG4-1 (sentinel reachability sweep): FAILS

**Method.** Called the real, unmodified `run_exp` (from the
byte-identical mechanism region) on the corpus-A table with
pure-fallback digit strings ("0123456789" repeated; the frozen
SENT60 evidence establishes zero chunk matches on corpus A) at
lengths n = 1, 2, 3, 10, 100, 1000, 10000, 49999, 50000, 50001,
60000, 100000. n = 50000 is the exact length where the old fixed
sentinel (-1000000 = -20*50000) degenerated into SCORE -1000000,
NOPT 0, AMBIGUOUS.

**Frozen kill criterion.** Any n with SCORE != -20*n, NOPT != 1,
degenerate AMBIGUOUS, crash, or hang.

**Result.** All 12 lengths: SCORE exactly -20*n, NOPT 1, VERDICT
SEGMENTED, exit 0. At n = 50000: SCORE -1000000, NOPT 1,
SEGMENTED (the old sentinel produced NOPT 0 / degenerate
AMBIGUOUS here; the per-run sentinel sent = -1000001 keeps every
fallback position reachable). No crash, no hang.

X-SG4-1 FAILS. The sentinel repair holds.

## Attack X-SG4-2a (z_alloc zeroing): FAILS

**Method.** The honesty proof assumes the 4-byte `sat` buffer
starts zeroed (`z_alloc(4)` with no explicit zeroing in
`run_exp`). Empirical test: allocated a 4-byte buffer and read
it; dirtied the allocator with 256 bytes of 0xFF; allocated again
and read again.

**Frozen kill criterion.** Any fresh `z_alloc(4)` reading nonzero.

**Result.** ZALLOC-INIT 0. ZALLOC-AFTER-DIRTY 0. The allocator
zeroes.

X-SG4-2a FAILS. The proof's assumption holds.

## Attack X-SG4-2b (cap-label mislabel search): FAILS

**Theory of the attack.** The honesty proof's lemma (the clamp
fires only when a true subtotal exceeds 999) is correct for the
position where the clamp fires. But the `sat` flag is per-run,
set if the clamp fires at ANY position. A clamp firing at a
position off the optimal route to n would not imply the true
count at n exceeds 999, so (no == 999 and flag set) with a
genuine final count of exactly 999 would print a false "999+".

**Method.** Built two DPs sharing the real lexicon training
(`train_corpus` / `compute_uncovered` for frozen corpora;
mirrored `train_adv` / `compute_uncovered_adv` for custom
corpora, reusing the real `train_seq`, `ch_match`,
`occ_covered`, `ch_uscore`):
- Clamped DP: the mechanism's real `relax` (with sat flag),
  copied DP loop, recording (no, sat).
- Reference DP: identical loop with an unclamped relax
  (`relax_ref`; counts capped at 1000000000, reported as HUGE;
  the cap preserves the =999 / >999 / <999 distinction).
Searched 800 deterministic cases (fixed LCG seed 12345): 5
corpus families x (40 structured repetition tests + 120
LCG-random tests over the corpus alphabet, lengths 6..48).
Corpus families: C1 {"xab","xab","yab","yab"}, C2
{"aab","aab","abb","abb"}, C3 {"aaab","aaab","aabb","aabb",
"abbb","abbb"}, C4 {"abcab","abcab","bcabc","bcabc"}, C5 the
frozen H1 corpus.
Flagged MISLABEL-FP if the label would be "999+" (no == 999,
sat == 1) while true T_n <= 999; MISLABEL-FN if the label would
be "999" (no == 999, sat == 0) while T_n > 999.

**Reference validation.** On all 770 cases where the clamp never
fired (sat == 0), the clamped DP and the reference DP agree
exactly (0 mismatches). The reference is faithful.

**Frozen kill criterion.** Any MISLABEL-FP or MISLABEL-FN with a
reproducible fixture.

**Result.** 0 MISLABEL-FP. 0 MISLABEL-FN. Of the 800 cases: 770
with sat == 0 (all exact agreement); 30 with sat == 1, all with
no == 999 and true T_n > 999 (powers of two from 2048 to
536870912), i.e. all 30 "999+" labels are correct. Zero cases
with sat == 1 and no < 999 (no off-route clamp observed in the
searched space).

X-SG4-2b FAILS. The "exactly honest" claim holds on all 800
cases. Residual (theoretical, unobserved): a clamp firing at a
position off every optimal route to n, combined with a genuine
final count of exactly 999, would mislabel as "999+"; the search
did not produce such a fixture.

## Attack X-SG4-3 (regression): FAILS

**Method.** Copied seg4_learn.zag to /tmp unmodified, compiled
with znc 2026.07.0-dev, ran three times.

**Frozen kill criterion.** Recompiled md5 differs from committed
cd551d3bb7613b5bcd725bbff159c427, runs not byte-identical, or
any of the nine frozen check lines differs from H-SEG3's.

**Result.** All three runs md5 cd551d3bb7613b5bcd725bbff159c427,
matching the committed SEG4_RAW_OUTPUT.txt; 3/3 byte-identical.
All eight frozen tag groups (ADV1-T1, ADV1-T2, ADV2-T2, ADV3,
EXP-A, EXP-B, EXP-C, EXP-D) byte-identical to SEG3_RAW_OUTPUT.txt
(TEST, SCORE, VERDICT lines).

X-SG4-3 FAILS. No regression.

## Attack X-SG4-4 (source audit): FAILS (no finding)

**Method.** (i) Diffed seg3_learn.zag -> seg4_learn.zag: the only
changes are DPSENT() removal, corpus_h1 + cid-4 dispatch, the
sat parameter in relax, the per-run sentinel in run_exp, the
999+ label, the three new fixture blocks in main(), and banner
strings. This matches the preregistered change set exactly.
(ii) Grepped the mechanism region for test-answer literals: none
(the only "999+" is the emit string; no expected scores or
segmentations; corpora are disclosed fixtures). (iii) Verified
the sentinel formula `let sent:i32=0-FBPEN()*n-1` and the
reachability guard `if(dpi>sent)`, and the sat logic
`if(v>999){v=999; set32(sat,0,1);}` plus the label branch, all
match the prereg text. (iv) DPSENT is fully removed (only
comment mentions remain).

**Frozen kill criterion.** Implementation deviates from prereg,
test-answer literals, or hardcoded fixture branches.

**Result.** No deviation found.

X-SG4-4 FAILS (clean).

## Correction: H1-T true count is 2^29, not Fib(31)

**Finding.** The X-SG4-2b reference DP (validated: 770/770 exact
agreement with the clamped DP wherever the clamp never fires)
gives the true optimal-path count for H1-T ("ab" x 30 on the H1
corpus) as 536870912 = 2^29, not Fib(31) = 1346269.

**Evidence.**
1. The H1 lexicon (committed SEG4_RAW_OUTPUT.txt, H1-T CHUNK
   lines) contains five zero-score chunks matching the test,
   not two: "ab" (len 2), "aba" (len 3), "abab" (len 4), "ba"
   (len 2), "bab" (len 3), all with uncovered=0, score=0. The
   X-SG3-2 analysis counted only "ab" and "abab".
2. The committed H1-T candidates themselves use the missed
   chunks (e.g. CAND "ab|aba|bab|abab|...", CAND
   "aba|ba|bab|abab|..."), proving they participate in optimal
   tilings.
3. The reference DP yields exactly T = 2^(k-1) for "ab" x k at
   k = 1..30 (lengths 2..60: 1, 2, 4, ..., 536870912),
   confirmed at all 30 lengths, then HUGE past the 1e9
   reference cap. The powers-of-two pattern is exact, not
   approximate.
4. Hand trace for "abababab" (len 8): nopt accumulates
   1,2,4,8 at even positions via the five zero-score moves,
   matching the reference output T=8.

**Impact on H-SEG4.** None on the verdict. The frozen K-SG4-3
bar requires only VERDICT AMBIGUOUS with NOPT printing "999+";
since 536870912 > 999, the label is correct. The error is in
the supporting analysis (SEG3_ADV_RESULT.md X-SG3-2,
PREREG_SEG4.md, SEG4_RESULT.md), which should be corrected to
2^29 = 536870912. The saturation conclusion of X-SG3-2 stands
(the cap genuinely saturates), only the cited true count was
wrong.

## Boundaries and honest limits (unchanged)

1. The sentinel proof covers reachability; DP time O(n*nch)
   and memory O(n) remain allocation-bound (engineering bound).
2. The off-route-clamp mislabeling scenario is theoretically
   possible but unobserved in 800 cases; the label is exactly
   honest on everything tested.
3. The count above the 999 cap remains unrecoverable (the
   reference DP here is an adversary instrument, not part of
   the mechanism).
4. MAXL=5, MINC=2, the containment family, the len^2 shape,
   FBPEN=20 remain authored. Bounded L2 at most, not L3.

## Governance

- Prereg PREREG_SEG4_ADV.md committed alone (0fa95b3c9) before
  any attack code was written or executed.
- Pure Zag throughout: harness, reference DP, search, and
  analysis all in Zag; no Python at any stage.
- Only H-SEG4-ADV-owned files staged and committed; concurrent
  agents' files untouched.
- No binaries committed (builds ran in /tmp/sg4adv).
- No em dashes in loop documentation.

## Files

- docs/lab/research-lead/overnight-20260928/PREREG_SEG4_ADV.md
  (commit 0fa95b3c9)
- docs/lab/research-lead/overnight-20260928/seg4_adv.zag
- docs/lab/research-lead/overnight-20260928/SEG4_ADV_RAW.txt
  (md5 94006076321d97b44631404c61efd609, 3/3 byte-identical)
- docs/lab/research-lead/overnight-20260928/SEG4_ADV_RESULT.md
  (this file)

## Recommended follow-ups (for the parent, not this red team)

1. Correct the H1-T true count (2^29 = 536870912, not
   Fib(31) = 1346269) in SEG3_ADV_RESULT.md, PREREG_SEG4.md,
   and SEG4_RESULT.md; mark the old number SUPERSEDED with
   lineage to this report.
2. Consider a targeted fixture for the theoretical
   off-route-clamp scenario if the "exactly honest" claim is
   to be promoted to a proof; until then it stands as
   "exactly honest on all 800 tested cases".
