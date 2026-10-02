# H-SEG8 RESULT: SURVIVES (4/4)

**Date:** 2026-09-29 (PDT)
**Researcher:** H-SEG8 Frontier Researcher (independent subagent)
**Target:** H-SEG7 SURVIVES (4/4). Prereg `44cee8122`, result this doc.
H-SEG7 red team SURVIVES all 4 attacks (X-SG7-1..X-SG7-4).
**Verdict:** SURVIVES. All four frozen kill bars PASS. Classification:
bounded L2 structural-learning repair (adaptive exactness; the
truncation failure mode is eliminated, not just signaled). Not L3:
the counting is mechanical; no representational invention.

## Lineage

- Prereg `PREREG_SEG8.md` committed alone as `44cee8122` BEFORE any
  implementation edit, build, or run. No amendments.
- `seg8_learn.zag` = `seg7_learn.zag` copied verbatim (cmp-verified)
  plus exactly the frozen R1-R4 changes. `seg7_learn.zag` untouched.
- Prereg is a verified strict ancestor of the result commit
  (merge-base --is-ancestor, checked at commit time).
- Pure Zag throughout: fixtures, implementation, builds, runs, greps,
  md5, cmp, diff. Zero Python at any stage. (One mechanical
  `sed -i` rename of SG7 to SG8 in ADD-UNIT emit strings; no logic
  touched.)

## Repairs implemented (exactly per frozen prereg)

**R1: Adaptive accumulation loop.** In run_exp, the fixed 64-digit
accumulation is replaced by a loop: nd starts at NDIGITS() (64);
if any bigint_add_of drops a carry out of the top digit (ovf==1),
nd doubles and the accumulation re-runs from scratch on a fresh
bc. The loop exits only with ovf==0. All NDIGITS() references
inside the accumulation become the local nd. dp, sat, and the
chunk table are read-only during accumulation, so re-runs are
deterministic.

**R2: Overflow signal retired.** The NOPT label now prints
bigint_print(bc,n*nd,nd) unconditionally when sat[n]==1; the
TRUNCATED-BUDGET-EXCEEDED marker and SAT-BUDGET-OVERFLOW line are
removed as unreachable (ovf cannot be 1 at print time).

**R3: New fixtures.** SG8 ADD-UNIT (U1/U2/U3, same carry checks),
SG8-BIG ("ab" x 958, single iteration), SG8-HUGE ("ab" x 1915,
one doubling to 128 digits), SG8-XL ("ab" x 4000, two doublings
to 256 digits).

**R4: Banners.** "H-SEG7 SEG-LEX-G" -> "H-SEG8 SEG-LEX-H";
"H-SEG7 COMPLETE" -> "H-SEG8 COMPLETE". Header comment updated.

Source diff seg7 -> seg8 contains only the pre-declared categories:
header, NDIGITS comment, adaptive loop (comment + while wrapper +
nd substitution), label block, overflow line removal, main banner,
ADD-UNIT renames, SG8-BIG/SG8-HUGE/SG8-XL fixtures, COMPLETE banner.

## Frozen kill-bar evidence

Toolchain: znc 2026.07.0-dev (edition 2026). Builds in /tmp/sg8
only; no binaries committed. Raw: `SEG8_RAW_OUTPUT.txt`
(md5 `44a071f08ea8594c66413a32d52817a5`), program output only
(direct binary run, exit 0, zero stderr).

Independent reference (pure Zag, /tmp scratch, never committed):
repeated-doubling big-int with 256 base-1e9 digits - a different
code path from the mechanism (no DP, no move enumeration, no chunk
table). Prints exact 2^957, 2^1914, 2^3999.

- **K-SG8-1 PASS (single-iteration exactness):** SG8-BIG prints the
  exact 2^957 (289 digits), byte-equal (cmp) to the reference.
  Zero TRUNCATED-BUDGET-EXCEEDED markers and zero
  SAT-BUDGET-OVERFLOW lines in the entire program output.
- **K-SG8-2 PASS (boundary inversion):** SG8-HUGE prints the FULL
  exact 2^1914 (577 digits), byte-equal (cmp) to the reference
  full rendering. Zero markers and zero overflow lines anywhere.
  Under SEG7 this input printed the 576-digit residue with the
  loud signal; the count is now exact. The 10^576 boundary is
  gone.
- **K-SG8-3 PASS (double doubling):** SG8-XL prints the FULL exact
  2^3999 (1204 digits), byte-equal (cmp) to the reference full
  rendering. Zero markers and zero overflow lines anywhere. The
  adaptive loop doubled twice (64 -> 128 -> 256) and terminated
  exact.
- **K-SG8-4 PASS (unit + regression + determinism):** U1/U2/U3 all
  print PASS, zero FAIL lines in the full output. Regression: all
  326 shared fixture lines (everything except banners, ADD-UNIT
  renames, and the SG7-BIG/SG7-OVF vs SG8-BIG/SG8-HUGE/SG8-XL
  sections) byte-identical between SEG7_RAW_OUTPUT.txt and
  SEG8_RAW_OUTPUT.txt (verified by filtered diff). 3 consecutive
  full runs byte-identical (cmp); md5
  `44a071f08ea8594c66413a32d52817a5` x3; exit 0.

Final tally: **4/4. H-SEG8 SURVIVES.**

## Exactness guarantee (new, frozen)

- The adaptive loop exits iff an iteration ends with ovf==0.
- Per the SEG7 induction, ovf==0 at end of iteration implies
  bc[i] == T_i exactly for all i (no carry dropped anywhere).
- Hence at loop exit bc[n] == T_n exactly, and the printed NOPT
  is the exact count for every input. The ovf==0 exit condition
  is the exactness certificate.
- Termination: T_n is finite (number of optimal segmentations of
  a length-n input). Some finite nd suffices (crude bound:
  T_n <= 513^n); the doubling sequence reaches it.

## Honest limits (updated)

1. The exact count is now unconditional: for every input, the
   printed NOPT equals T_n exactly. There is no budget boundary
   and no truncation mode. The SEG7 honest limit #1 is closed.
2. Memory for the saturated run is (n+1)*nd_final*4 bytes where
   nd_final <= 2x the base-1e9 digits of the true count. Each
   doubling costs at most one extra full accumulation pass.
3. The big-integer DP remains on-demand (sat[n]==1 only).
4. All other H-SEG7 honest limits unchanged.

## Governance disclosures

1. Prereg committed alone before any implementation; ordering
   verified by merge-base --is-ancestor.
2. Pure Zag throughout. Zero Python at any stage.
3. No binaries committed (builds in /tmp/sg8 only).
4. Only the four owned files staged/committed
   (PREREG_SEG8.md, seg8_learn.zag, SEG8_RAW_OUTPUT.txt,
   SEG8_RESULT.md). No other worker's files touched.
   Pathspec-restricted staging used throughout.
5. No em dashes in loop documentation (byte-checked).
6. seg7_learn.zag and all prior evidence files untouched.

## Suggested follow-ups for parent

1. Independent red team on H-SEG8 (natural attacks: X-SG8-1
   adversarial counts forcing many doublings; X-SG8-2 the
   discarded-bc safety on ovf iterations; X-SG8-3 termination on
   pathological inputs; X-SG8-4 regression).
2. The segmentation arc (H-SEG through H-SEG8) has now closed every
   residual the red teams found: fragmentation (H-SEG3), the
   per-run flag hole (H-SEG5), silent truncation above 999
   (H-SEG6), the 288-digit ceiling and silent overflow (H-SEG7),
   and now the 576-digit boundary itself (H-SEG8: unconditional
   exactness). Candidate for transfer/integration into the
   continuing learner per the mandate (survivor -> replication ->
   transfer -> integration).
