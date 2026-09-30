# H-SEG7 RESULT: SURVIVES (4/4)

**Date:** 2026-09-29
**Researcher:** H-SEG7 Frontier Researcher (independent subagent)
**Target:** H-SEG6 SURVIVES (3/3). Prereg `5e5f0b9bb`, result this doc.
Red team SURVIVES all 4 attacks (X-SG6-1..X-SG6-4).
**Verdict:** SURVIVES. All four frozen kill bars PASS. Classification:
bounded L2 structural-learning repair (budget widening + honest
overflow signaling). Not L3: the counting is mechanical; no
representational invention.

## Lineage

- Prereg `PREREG_SEG7.md` committed alone as `5e5f0b9bb` BEFORE any
  implementation edit, build, or run. No amendments.
- `seg7_learn.zag` = `seg6_learn.zag` copied verbatim (cmp-verified)
  plus exactly the frozen R1-R6 changes. `seg6_learn.zag` untouched.
- Prereg is a verified strict ancestor of the result commit
  (merge-base --is-ancestor, checked at commit time).
- Pure Zag throughout: fixtures, implementation, builds, runs, greps,
  md5, cmp, diff. Zero Python at any stage.

## Repairs implemented (exactly per frozen prereg)

**R1: NDIGITS() 32 -> 64.** One-line change. Budget T_n < 1e576
(was T_n < 1e288). Allocation `(n+1)*NDIGITS()*4` scales
automatically.

**R2: `bigint_add_of` (new function).** Same digit loop as
`bigint_add`, but returns the final carry out of the top digit
(0 or 1). `bigint_add` itself untouched.

**R3: Overflow flag.** `let ovf:i32=0;` declared before the
sat==1 block; the two accumulation call sites now use
`bigint_add_of` and set `ovf=1` on carry-out. Once set, ovf stays 1.

**R4: Loud label.** On sat[n]==1 with ovf==1, the NOPT number is
followed by ` TRUNCATED-BUDGET-EXCEEDED`, and a dedicated line is
emitted:
`SAT-BUDGET-OVERFLOW: exact-count accumulation exceeded 64
base-1e9 digits; printed NOPT is T_n mod 1e576 (lower 576 digits
exact)`.

**R5: New fixtures.** SG7 ADD-UNIT (U1/U2/U3 carry-out unit checks),
SG7-BIG ("ab" x 958, n=1916), SG7-OVF ("ab" x 1915, n=3830), all on
the trained H1 corpus.

**R6: Banners.** "H-SEG6 SEG-LEX-F" -> "H-SEG7 SEG-LEX-G";
"H-SEG6 COMPLETE" -> "H-SEG7 COMPLETE". Header comment updated.

Source diff seg6 -> seg7 contains only the pre-declared categories:
header, NDIGITS, utility comment, bigint_add_of, ovf declaration,
two call sites, label block, overflow line, main banner, ADD-UNIT
block, SG7-BIG/SG7-OVF fixtures, COMPLETE banner.

## Frozen kill-bar evidence

Toolchain: znc 2026.07.0-dev (edition 2026). Builds in /tmp/sg7
only; no binaries committed. Raw: `SEG7_RAW_OUTPUT.txt`
(md5 `adfa444130bd93a56f000d66817452f7`), program output only
(direct binary run).

Independent reference (pure Zag, /tmp scratch, never committed):
repeated-doubling big-int with 128 base-1e9 digits - a different
code path from the mechanism (no DP, no move enumeration).
Confirms 2^957 has 289 digits; 2^1914 uses 65 base-1e9 digits
(577 decimal digits), genuinely exceeding the 64-digit budget.

- **K-SG7-1 PASS (budget widening):** SG7-BIG prints the exact
  2^957 = 121816425142499988504417279848439853885952835719937594
  085848830715161858634580326280820188323525128240316311452892608
  352293239623315038675582224841203908167744140971249455912873384
  870693625670604409994918490229735921069974067435936821829545193
  3620701603467350388034693385228573748989263872 (289 digits),
  byte-equal (cmp) to the independent doubling reference. Zero
  `TRUNCATED-BUDGET-EXCEEDED` markers and zero
  `SAT-BUDGET-OVERFLOW` lines in the SG7-BIG section. Under SEG6
  this input printed the silent mod-1e288 truncation (red team
  X-SG6-3); it is now exact.
- **K-SG7-2 PASS (loud overflow):** SG7-OVF section contains exactly
  one `TRUNCATED-BUDGET-EXCEEDED` marker (on the NOPT line) and
  exactly one `SAT-BUDGET-OVERFLOW` line. The printed number
  (576 digits) is byte-equal (cmp) to the reference's lower-576-digit
  rendering of 2^1914, i.e. exactly 2^1914 mod 10^576. The
  reference's full exact rendering has 577 digits, confirming the
  true count genuinely exceeds the budget (flag is not a false
  alarm on this fixture).
- **K-SG7-3 PASS (unit + regression):** U1/U2/U3 all print PASS,
  zero FAIL lines in the full output. Regression: pristine SEG6
  rebuild from `git show HEAD:` produces md5
  `8a90adf4d437f8d040ccb9729fb9ccee`, matching the md5 recorded in
  SEG6_RESULT.md and confirmed by the red team. Diff of SEG6
  pristine output vs SEG7 output: exactly 2 removed lines (the two
  banner lines) and 60 added lines, all in preregistered
  categories (28 SG7-OVF, 27 SG7-BIG, 3 SG7 ADD-UNIT, 2 H-SEG7
  banner). Every other line byte-identical, including H1-T
  `NOPT 536870912`.
- **K-SG7-4 PASS (determinism):** 3 consecutive full runs
  byte-identical (cmp); md5 `adfa444130bd93a56f000d66817452f7` x3;
  exit 0.

Final tally: **4/4. H-SEG7 SURVIVES.**

## Provable label semantics (new, frozen)

- ovf==0 implies no accumulation ever dropped a top carry, hence
  every stored bc[i] equals the true T_i, hence the printed value
  equals T_n exactly. ovf==0 is an exactness certificate.
- ovf==1 implies the printed value equals T_n mod 1e576, and the
  label says so loudly (marker + dedicated line). The SEG6 silent
  failure mode is closed: it is now impossible to print a
  truncated count without the explicit signal.

## Honest limits (updated)

1. The big-integer has 64 base-1e9 digits (T_n < 1e576). Beyond
   this, the count is reported as T_n mod 1e576 WITH the loud
   overflow signal (no longer silent). The boundary is now
   self-describing in the output.
2. ovf==1 is conservative by construction: the printed residue is
   always exactly T_n mod 1e576, and the flag fires iff a top
   carry was dropped during accumulation.
3. The big-integer DP remains on-demand (sat[n]==1 only).
   Worst-case added memory is (n+1)*64*4 bytes on the saturated
   run (SG7-OVF: ~0.98 MB).
4. All other H-SEG6 honest limits unchanged.

## Governance disclosures

1. Prereg committed alone before any implementation; ordering
   verified by merge-base --is-ancestor.
2. Pure Zag throughout. Zero Python at any stage.
3. No binaries committed (builds in /tmp/sg7 only).
4. Only the four owned files staged/committed
   (PREREG_SEG7.md, seg7_learn.zag, SEG7_RAW_OUTPUT.txt,
   SEG7_RESULT.md). No other worker's files touched.
   Pathspec-restricted staging used throughout.
5. No em dashes in loop documentation (byte-checked).
6. seg6_learn.zag and all prior evidence files untouched.

## Suggested follow-ups for parent

1. Independent red team on H-SEG7 (natural attacks: X-SG7-1 forged
   near-boundary counts, X-SG7-2 overflow-flag spoofing / false
   negatives, X-SG7-3 the conservative-flag edge, X-SG7-4
   regression).
2. The segmentation arc (H-SEG through H-SEG7) has now closed every
   residual the red teams found: fragmentation (H-SEG3), the
   per-run flag hole (H-SEG5), silent truncation above 999
   (H-SEG6), the 288-digit ceiling and silent overflow (H-SEG7).
   Candidate for transfer/integration into the continuing learner
   per the mandate (survivor -> replication -> transfer ->
   integration).
