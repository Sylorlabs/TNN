# SEG6 ADVERSARY RESULT: H-SEG6 Independent Red-Team Report

**Date:** 2026-09-29
**Researcher:** H-SEG6 Independent Red-Team Adversary (subagent)
**Target:** `seg6_learn.zag` (committed; verified unmodified via cmp
against `git show HEAD:...` before any attack work)
**Prereg:** PREREG_SEG6.md (commit afa0d2e75); attack plan is the four
preregistered attacks X-SG6-1..X-SG6-4 from the tasking (no separate
adversary prereg was written; attacks were designed before any build
or run, per the task list)
**Toolchain:** znc 2026.07.0-dev (edition 2026), binary at
`docs/lab/rsi/runs/wave-20260929-0821pdt/evidence/build_host/znc`
**Purity:** Pure Zag. No Python at any stage (builds, harnesses,
analysis via znc, sh, sed, awk, grep, diff, cmp, md5sum only).
**Harness:** /tmp/sg6adv (never committed; raw outputs
adv_out3.txt, pristine1/2/3.txt retained there)

## Verdict: H-SEG6 SURVIVES this red team

All four preregistered attacks failed to meet their kill criteria.
No reproducible counterexample, no move-set mismatch, no trigger
flaw, no carry bug within the documented digit budget, no
regression. The exact-count recovery claim stands as bounded
(T_n < 1e288, the documented honest limit).

## X-SG6-1: Differential attack on the big-int exact count -- FAILED (no break)

**Method.** Three-way differential per test case, all in one Zag
harness (/tmp/sg6adv/adv.zag):

- **M (mechanism):** the main-DP section (seg6 lines 385-419) plus
  the big-int block (lines 421-454) extracted byte-verbatim
  (verified with diff: VERBATIM_IDENTICAL), run on the case, with
  dp/nopt/sat/big-int digits captured instead of printed.
- **R (independent reference):** independently written backward
  big-integer DP with 64 base-1e9 digits: rb[n]=1,
  rb[i] = sum of rb[j] over optimal moves i->j, optimal-move
  predicate re-derived from the dp definition
  (dp[i]+s == dp[j]), move set enumerated independently
  (fallback + all matching recurring chunks). Different direction,
  different accumulation, wider digits than M. Result rb[0].
- **B (brute force, n <= 12):** fully independent reference that
  enumerates EVERY segmentation path recursively (no DP, no
  optimality predicate), tracking max score and exact optimal-path
  count with i64 arithmetic.

**Arithmetic layer (M and R share bigint_add):** tested separately
with i64-verified expectations: U1 999999999+1 carry, U2 5-digit
carry chain, U3/U4 400 randomized one- and two-digit adds with
carry-in (0 failures), U5 print formatting checked against an
independent repeated-divmod-10 formatter (3/3 match, including the
all-zero "0" case).

**Battery and results:**

- H1 family "ab" x k, k=1..20: all match (M == R digits; brute
  force cross-checks R for k<=6). Saturation boundary confirmed:
  k=10 -> NOPT 512 unsaturated, k=11 -> NOPT 1024 saturated,
  printed exactly. H1-T equivalent (k=30 class) prints 536870912.
- 4 reset-after-saturation fixtures ("ab"x12 + sep + "ab"x12,
  sep in {"zabab","xab","wabab","qq"}): each separator takes a
  unique optimal parse (T_sep=1, a strict-improvement reset on the
  saturated path), total T = 2^22. M == R on all 4.
- Random differential fuzz, 1200 cases (3 corpus families over
  {a,b} and {a,b,c}, test lengths 10-70, brute force on n<=12):
  0 mismatches of any kind.
- FAM4: 300 random {a,b} tests (length 30-70) on the H1 corpus,
  chosen for tie-rich diverse saturation (non-uniform branching,
  fallback gaps, varied chunk mixes): **300/300 saturated, M == R
  on every one**, trigger semantics exact (see X-SG6-2).
- Unsaturated cross-check: on all 1185 unsaturated cases,
  R == nopt[n] exactly (re-validates the untouched main DP), and
  brute force agrees with R wherever run.

**Totals: 1500 cases, 315 saturated, 0 count mismatches, 0 brute
force disagreements.** The optimal-move predicate, the move-set
enumeration, the forward accumulation order, and the digit printing
are all exactly right within the documented budget.

## X-SG6-2: Trigger attacks -- FAILED (no break)

Two sub-attacks on the `sat[n]==1` big-int trigger:

- **X-SG6-2a (structural):** the big-int block runs iff
  `get32(sat,n*4)==1`; the label prints the big-int result in
  exactly the same condition (`no==999` and `sat[n]==1`, and
  sat[n]==1 implies no==999 by the H-SEG5 capping invariant).
  Verified in code and in-harness on all 1500 cases: no case ran
  the big-int without saturation, none saturated without running
  it, and `bc` is never read uninitialized (allocated exactly when
  sat[n]==1).
- **X-SG6-2b (semantic):** `sat[n]==1` iff true T_n > 999, with R
  as truth, on all 1500 cases: 0 mismatches. The trigger fires
  exactly on the proof-derived condition, never on a
  non-saturated input, and is never suppressed on a saturated one.

## X-SG6-3: Carry / overflow attacks -- FAILED (no break within budget)

- **Within budget:** "ab" x 31 -> T = 2^30 = 1073741824 (2
  base-1e9 digits, cross-digit carry): exact. "ab" x 61 ->
  T = 2^60 = 1152921504606846976 (3 digits): exact.
  "ab" x 957 -> T = 2^956 (288 decimal digits, the largest power
  of two below 1e288): M prints all 288 digits, M == R exactly.
- **Beyond budget (documented honest limit #1):** "ab" x 958
  (T = 2^957, 289 digits) and "ab" x 960: the mechanism prints a
  wrong value, but the failure mode is precisely the documented
  one: M == R mod 10^288 (lower 32 digits identical, R has nonzero
  higher digits), i.e. the final carry out of digit 31 is dropped.
  No crash, no hang, no corruption of lower digits. The honest
  limit is real, exactly as documented, and the claim is bounded
  by it. This is a confirmation of the documented limit, not a
  break of any claim.

## X-SG6-4: Regression and silent-change audit -- PASSED (defense holds)

- seg5_learn.zag and seg6_learn.zag both byte-identical to
  `git show HEAD:...` (cmp). Nothing committed was touched.
- Source diff seg5 -> seg6 contains exactly the preregistered
  edits: header comment, NDIGITS(), the three big-int utilities,
  the big-int DP block in run_exp, the label change
  (`emit("999+")` -> `bigint_print(...)`), and the two banner
  lines. No change to relax, nopt/sat logic, the main DP loop, or
  any fixture. The new code only reads dp/nopt/sat.
- Pristine rebuild of committed seg6_learn.zag: 3/3 runs
  byte-identical (cmp), md5 8a90adf4d437f8d040ccb9729fb9ccee,
  matching the md5 recorded in SEG6_RESULT.md.
- Output vs committed SEG5_RAW_OUTPUT.txt differs in exactly the
  3 preregistered lines (banner, H1-T NOPT 999+ -> 536870912,
  COMPLETE banner). All H-SEG5 behavior otherwise byte-identical.

## Minor deviations noted (not breaks)

1. PREREG_SEG6.md R1(b) says "Store a flag `exact:i32=1`"; the
   implementation has no `exact` variable and re-checks
   `get32(sat,n*4)==1` in the label. sat[n] is not modified
   between the two reads, so this is functionally identical.
   Cosmetic prereg/implementation wording drift only.
2. K-SG6-2's bar text ("the harness is updated so the NEW
   mechanism's printed count must EQUAL the REF true count for
   all cases with T_n <= 1e9") was evidenced by the builder with
   H1-T, H1-K11, unit tests, and the frozen proof, not a full
   battery re-run. This red team closes that gap: 315 saturated
   cases differentially validated M == independent-exact R
   (see X-SG6-1). The bar is now more strongly evidenced than as
   committed. No contradiction with the recorded verdict.

## Recommended follow-ups (for the parent, not this lane)

1. The 32-digit budget is a hard ceiling on the "exact for all
   inputs" reading of claim 1; any future claim extension past
   T_n >= 1e288 needs a wider digit array (the failure mode is
   characterized and silent, so a budget-exceeded signal would be
   the principled next repair if the frontier ever needs it).
2. The K-SG6-2 evidence gap noted above is now closed by this
   red team's differential battery; no parent action required.

## Files

- This report:
  docs/lab/research-lead/overnight-20260928/seg6_adversary/SEG6_ADV_RESULT.md
- Raw evidence (uncommitted, /tmp/sg6adv): adv.zag (harness),
  adv_out3.txt (full battery output), pristine1/2/3.txt,
  seg6pristine binary build log.

## Governance disclosures

- Attack plan was the four task-specified attacks, designed
  before any build or run; no separate adversary prereg written.
- Target verified unmodified (cmp against git show) before and
  after attack work.
- All harnesses in /tmp/sg6adv only; never committed.
- Pure Zag throughout (znc builds; sh/sed/awk/grep/diff/cmp/
  md5sum for assembly and analysis). No Python.
- Only this adversary-owned result file staged for commit.
- No em dashes in this document (verified by grep).
