# PREREG H-SEG4-ADV: Red Team Against H-SEG4

**Status:** FROZEN. This prereg strictly precedes any attack code,
execution, or analysis.
**Date:** 2026-09-29
**Author:** H-SEG4 Red Team (subagent)
**Target:** H-SEG4 SURVIVES (13/13), commits d7afeff5a (prereg),
9618ffeb4 (implementation + evidence).

## Target claims under attack

H-SEG4 makes two repair claims beyond H-SEG3:

1. **Growable DP sentinel.** `run_exp` computes
   `sent = 0 - FBPEN()*n - 1` from the test input length n. Claim:
   every DP move scores >= -FBPEN (fallback) or >= 0 (chunk scores
   are uncovered*len^2), so any path ending at position i scores
   >= -FBPEN*i >= -FBPEN*n > sent; a cell holding `sent` is
   genuinely unreached, for every n. Reachability exact at any input
   length; no new constant; the fixed -1000000 sentinel (P-SENT
   degeneracy at n >= 50000) is removed.
2. **Honest nopt cap label.** `relax` sets a per-run saturation flag
   (`sat`, a 4-byte buffer) when the 999 clamp fires
   (`if(v>999){v=999; set32(sat,0,1);}`). `run_exp` prints "NOPT
   999+" iff final count is 999 and the flag is set, else the plain
   count. Claim (PREREG_SEG4.md): "(final == 999 and flag set)
   implies the true count strictly exceeds 999, while (final == 999
   and flag clear) implies the true count is exactly 999. The label
   is exactly honest."

## Adversary stance

Assume both claims are false. Four preregistered attacks.

## Attack X-SG4-1: sentinel reachability sweep

**Method.** Copy `seg4_learn.zag` mechanism verbatim (all functions
except `main()`); in the adversary `main()`, call the real
`run_exp` on the corpus-A table with pure-fallback digit strings
("0123456789" repeated; the frozen SENT60 evidence establishes zero
chunk matches on corpus A) at lengths n in
{1, 2, 3, 10, 100, 1000, 10000, 49999, 50000, 50001, 60000,
100000}. n = 50000 is the exact length where the old fixed
sentinel (-1000000 = -20*50000) degenerated.

**Expected under the claim.** Every n: exit 0, SCORE exactly
-20*n, NOPT 1, VERDICT SEGMENTED. No crash, no hang (120 s
timeout per run).

**Kill criterion.** X-SG4-1 SUCCEEDS if any tested n yields SCORE
!= -20*n, NOPT != 1, a degenerate AMBIGUOUS with NOPT 0 (the old
P-SENT signature), a crash, or a hang. Success KILLS H-SEG4 (the
sentinel repair is broken).

## Attack X-SG4-2: cap-label exact honesty

**Theory of the attack.** The honesty proof argues the clamp fires
only when a true subtotal exceeds 999. That lemma is correct for
the position where the clamp fires. But the `sat` flag is
PER-RUN (one buffer per `run_exp` call), set if the clamp fires at
ANY position. A clamp firing at a position OFF the optimal route
to n does not imply the true optimal count at n exceeds 999. The
label logic prints "999+" whenever (no == 999 and flag set).
Hence a possible false positive: an off-route clamp (flag = 1)
combined with a genuine final count of exactly 999 prints "999+"
for a true-999 count, contradicting "exactly honest".

Two sub-attacks:

**(a) Allocation-zeroing check.** The proof assumes the 4-byte
`sat` buffer starts zeroed (`z_alloc(4)` with no explicit zeroing
in `run_exp`; contrast `nopt`/`mvc`, which are explicitly zeroed
in the init loop). Empirically test: allocate a 4-byte buffer and
read it; dirty the allocator with 0xFF fills, allocate again,
read again. If any read is nonzero, the flag's initial value is
unreliable and the "exactly honest" proof's assumption fails.

**Kill criterion (a).** X-SG4-2a SUCCEEDS if any fresh
`z_alloc(4)` reads nonzero. Success DOWNGRAADES H-SEG4 (the cap
label is not provably honest; observed outputs may still be
correct by luck).

**(b) Mislabel search.** Build a clamped DP (the mechanism's
`relax` with the sat flag, copied verbatim) and an unclamped
reference DP (identical loop, counts capped at 2000000000, no sat
writes; anything reaching the cap is recorded as HUGE > 999).
Calibrate the reference on the frozen H1-T fixture: it must
reproduce the red-team-established true count Fib(31) =
1346269. Then sweep a deterministic generated space (fixed LCG
seed, no randomness in the verdict):
- Corpus families (fixed string sets over small alphabets,
  designed for ambiguity): C1 {"xab","xab","yab","yab"}, C2
  {"aab","aab","abb","abb"}, C3 {"aaab","aaab","aabb","aabb",
  "abbb","abbb"}, C4 {"abcab","abcab","bcabc","bcabc"}, C5 the
  frozen H1 corpus (cid 4).
- Tests per corpus: "ab" x k for k = 1..40, "a" x k + "b" x k
  for k = 1..20, and LCG-generated strings over {a,b} (lengths
  6..48), at least 200 tests per corpus.
For each (corpus, test): train with the real `train_corpus` /
`compute_uncovered`, run clamped DP (record no, sat) and
reference DP (record T_n). Flag MISLABEL-FP if the printed label
would be "999+" (no == 999 and sat == 1) while T_n <= 999.
Flag MISLABEL-FN if the label would be "999" (no == 999 and sat
== 0) while T_n > 999 (expected impossible; included for
completeness).

**Kill criterion (b).** X-SG4-2b SUCCEEDS if any MISLABEL-FP or
MISLABEL-FN is found, with the full fixture (corpus, test,
clamped trace, reference count) documented and reproducible.
Success DOWNGRAADES H-SEG4: the "exactly honest" cap-label claim
is narrowed (the 13/13 frozen bars stand; the sentinel repair is
unaffected; H-SEG3 printed a bare "999" so no regression versus
the parent either way).

## Attack X-SG4-3: regression

**Method.** Copy `seg4_learn.zag` to /tmp unmodified, compile
with the repo `znc 2026.07.0-dev`, run three times, md5 the
outputs. Compare against the committed `SEG4_RAW_OUTPUT.txt`
(md5 cd551d3bb7613b5bcd725bbff159c427). Extract the nine frozen
check lines (ADV1-T1, ADV1-T2, ADV2-T2, ADV3, EXP-A/B/C/D) and
byte-compare against `SEG3_RAW_OUTPUT.txt`.

**Kill criterion.** X-SG4-3 SUCCEEDS if the recompiled output md5
differs from the committed md5, the three runs are not
byte-identical, or any of the nine frozen lines differs from
H-SEG3's. Success KILLS H-SEG4 per its own prereg kill bars
(K-SG4-4, K-SG4-5).

## Attack X-SG4-4: source audit

**Method.** (i) Verify the seg3 -> seg4 diff contains only the
preregistered change set (DPSENT removal, corpus_h1 + cid-4
dispatch, sat parameter in relax, per-run sentinel in run_exp,
999+ label, three new fixture blocks, banner strings). (ii) Grep
the mechanism region for test-answer literals (expected scores,
segmentations, "999+"). (iii) Verify the sentinel formula and
the sat-flag logic match the prereg text exactly.
(iv) Confirm the z_alloc-zeroing assumption against (a).

**Kill criterion.** X-SG4-4 SUCCEEDS if the implementation
deviates from the prereg, contains test-answer literals in the
learning path, or hardcodes fixture-specific branches. Severity
decides DOWNGRADE vs KILL.

## What does NOT count

- Arguing the authored constants (MAXL=5, MINC=2, len^2,
  FBPEN=20) are arbitrary: out of scope, unchanged from H-SEG3.
- The documented honest limits (O(n*nch) time, enum_bwd stack
  bound, unrecoverable count above cap, morpheme discount):
  already disclosed, not kills.
- Performance timing differences between runs.

## Deliverables

- This prereg (committed alone, before any attack code).
- `seg4_adv.zag`: adversary harness (mechanism region
  byte-identical to `seg4_learn.zag` except `main()` replaced;
  verified by diff/cmp), built in /tmp only.
- `SEG4_ADV_RAW.txt`: raw evidence, 3/3 byte-identical runs.
- `SEG4_ADV_RESULT.md`: full adversary report with verdict.
- All committed to `tnn-native-lab`. Pure Zag. No Python.

## Verdict mapping (frozen)

- X-SG4-1 success -> H-SEG4 KILLED.
- X-SG4-2a success -> H-SEG4 DOWNGRADED (label honesty
  unproven).
- X-SG4-2b success -> H-SEG4 DOWNGRADED (label honesty
  narrowed; give the mislabeling fixture).
- X-SG4-3 success -> H-SEG4 KILLED.
- X-SG4-4 success -> DOWNGRADE or KILL by severity.
- All fail -> H-SEG4 SURVIVES this red team.
