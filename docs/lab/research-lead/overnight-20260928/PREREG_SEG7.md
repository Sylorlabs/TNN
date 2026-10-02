# PREREG H-SEG7 FROZEN

**Date:** 2026-09-29
**Researcher:** H-SEG7 Frontier Researcher (subagent)
**Parent:** H-SEG6 SURVIVES (3/3); H-SEG6 red team SURVIVES all 4 attacks.
**Status:** FROZEN. This document is committed alone before any
implementation edit, build, or test run. No Python at any stage.
No em dashes in loop documentation.

## Targeted residual

H-SEG6 honest limit #1 (SEG6_RESULT.md): "Big-integer has 32
base-1e9 digits (T_n < 1e288). Beyond this, the count would overflow
the digit array (carry dropped)."

The H-SEG6 red team (X-SG6-3) confirmed the failure mode precisely:
beyond budget, M == R mod 10^288, no crash, lower digits uncorrupted.
But the failure mode is SILENT: the mechanism prints a wrong value
with no signal that the budget was exceeded. The red team's
recommended follow-up #1: "a budget-exceeded signal would be the
principled next repair if the frontier ever needs it."

H-SEG7 does both halves of the principled repair:
1. Widen the digit budget 32 -> 64 (T_n < 1e576), so the
   characterized SEG6 failure case ("ab" x 958, T = 2^957, 289
   digits) becomes exactly representable.
2. Add an explicit, loud budget-exceeded signal: if any
   accumulation drops a carry out of the top digit, the label
   marks the printed value as a modular residue instead of
   printing it silently as if exact.

## Repair (frozen, exact)

seg7_learn.zag = seg6_learn.zag copied verbatim plus exactly these
edits:

**R1: NDIGITS() 32 -> 64.** One-line change. New budget:
T_n < 1e576. Allocation `(n+1)*NDIGITS()*4` scales automatically.

**R2: Carry-out reporting add.** New function, placed directly after
`bigint_add`:
```
// bigint_add_of: like bigint_add but returns the final carry out of
// the top digit (0 or 1). A return of 1 means the true sum met or
// exceeded the nd-digit budget and the stored result is truncated
// to the sum mod 1e9^nd.
fn bigint_add_of(d:[]u8, doff:i32, s:[]u8, soff:i32, nd:i32)i32 {
  let carry:i32=0;
  let i:i32=0;
  while(i<nd){
    let v:i32=get32(d,(doff+i)*4)+get32(s,(soff+i)*4)+carry;
    if(v>=1000000000){ set32(d,(doff+i)*4,v-1000000000); carry=1; }
    else { set32(d,(doff+i)*4,v); carry=0; }
    i=i+1;
  }
  return carry;
}
```
`bigint_add` itself is untouched.

**R3: Overflow flag in the accumulation block.** Declare
`let ovf:i32=0;` next to `let bc:[]u8="";` before the
`if(get32(sat,n*4)==1)` block. Replace the two `bigint_add(...)`
call sites inside the block with:
```
if(bigint_add_of(bc,bnp*NDIGITS(),bc,bi*NDIGITS(),NDIGITS())==1){ ovf=1; }
```
(and the bnp2 analogue). Once set, ovf stays 1.

**R4: Loud label on overflow.** In the NOPT label, replace
```
if(get32(sat,n*4)==1){ bigint_print(bc,n*NDIGITS(),NDIGITS()); }
```
with
```
if(get32(sat,n*4)==1){
  bigint_print(bc,n*NDIGITS(),NDIGITS());
  if(ovf==1){ emit(" TRUNCATED-BUDGET-EXCEEDED"); }
}
```
and after the `emit("\n");` that ends the NOPT line, add:
```
if(ovf==1){ emit(tag); emit(" SAT-BUDGET-OVERFLOW: exact-count accumulation exceeded 64 base-1e9 digits; printed NOPT is T_n mod 1e576 (lower 576 digits exact)\n"); }
```
The ovf declaration (R3) is outside the sat==1 block so the label
can read it; ovf is 0 whenever sat[n]==0 (block never ran).

**R5: New fixtures in main()** (reusing the trained H1 corpus
cth1/unh1/nh1, exactly like H1-T):
- SG7-ADD-UNIT: inline unit checks of bigint_add_of before the
  experiments: U1: d = 64 max digits + s = [1,0..] -> carry-out 1,
  d all zero. U2: d = zero + s = [5,0..] -> carry-out 0, d[0]=5.
  U3: bigint_add (void) on the same U1 inputs -> d all zero
  (keeps the original function exercised). Each emits
  `SG7 ADD-UNIT-Uk PASS` or `FAIL`.
- SG7-BIG: "ab" x 958 (n=1916) on the H1 corpus. True count
  T = 2^957 (289 decimal digits; 957*log10(2) = 288.09). Under
  SEG6 this printed the silent truncation; under SEG7 it must
  print exactly with ovf==0 (no marker lines).
- SG7-OVF: "ab" x 1915 (n=3830) on the H1 corpus. True count
  T = 2^1914 (577 decimal digits; 1914*log10(2) = 576.17, so
  T >= 1e576). The 64-digit budget MUST overflow: ovf==1, the
  `TRUNCATED-BUDGET-EXCEEDED` marker and the `SAT-BUDGET-OVERFLOW`
  line must appear, and the printed number must equal
  2^1914 mod 10^576.

**R6: Banners and header.** "H-SEG6 SEG-LEX-F" -> "H-SEG7 SEG-LEX-G";
"H-SEG6 COMPLETE" -> "H-SEG7 COMPLETE". Header comment first line
and algorithm line updated to H-SEG7; the honest-limit comment
updated (see below). Nothing else changes. seg6_learn.zag untouched.

## Correctness argument (frozen)

- R1 is a pure parameter widening; the R correctness proof from
  PREREG_SEG6.md is unchanged.
- R2/R3: each stored add now computes (x+y) mod 1e9^64, dropping
  the top carry exactly as before; the only new behavior is
  reporting the dropped carry. By induction over the accumulation
  order (same order as SEG6), bc[i] = T_i mod 1e9^64 for all i,
  and ovf==1 iff some add dropped a nonzero top carry.
- Provable label semantics:
  - ovf==0 implies no add ever dropped a carry, hence every
    stored bc[i] equals the true T_i, hence the printed value
    equals T_n exactly.
  - ovf==1 implies the printed value equals T_n mod 1e576, and
    the label says so loudly (marker + dedicated line). The
    failure mode is no longer silent.
- R5 fixtures use the "ab" x k family where T = 2^k exactly (same
  move structure as the red-team-validated H1 family: at each
  position the fallback pair and the "ab" chunk are the two
  optimal moves). 2^957 < 1e576 < 2^1914 is arithmetic, verified
  by the independent doubling script (see kill bars).

## Frozen kill bars

- **K-SG7-1 (budget widening):** SG7-BIG prints the exact 2^957
  (289 digits), byte-equal to the independent doubling script's
  output for 2^957, with NO `TRUNCATED-BUDGET-EXCEEDED` marker
  and NO `SAT-BUDGET-OVERFLOW` line anywhere in the SG7-BIG
  section. Verified by grep + cmp against the script output.
- **K-SG7-2 (loud overflow):** SG7-OVF section contains exactly
  one `TRUNCATED-BUDGET-EXCEEDED` marker on its NOPT line and
  exactly one `SAT-BUDGET-OVERFLOW` line; the printed number
  (NOPT field before the marker) is byte-equal to the doubling
  script's lower-576-digit rendering of 2^1914; the script's full
  exact rendering of 2^1914 has 577 digits (confirming the true
  count genuinely exceeds the budget, so the flag is not a false
  alarm on this fixture).
- **K-SG7-3 (unit + regression):** U1/U2/U3 all print PASS, zero
  FAIL. All K-SG6-1..K-SG6-3 bars still PASS with exactly these
  preregistered output differences vs SEG6_RAW_OUTPUT.txt: the
  two banner lines, the SG7 ADD-UNIT lines, and the SG7-BIG /
  SG7-OVF sections (including their VERDICT/NCAND/CAND lines).
  Every other line byte-identical (verified by diff).
- **K-SG7-4 (determinism):** 3 consecutive full runs byte-identical
  (cmp), md5 recorded, exit 0.

The independent doubling script (pure Zag, /tmp scratch, never
committed): repeated-doubling big-int with 128 base-1e9 digits
(single loop, no DP, no move enumeration - a different code path
from the mechanism). Prints exact 2^957; prints exact 2^1914 and
its lower 576 digits. Compared against mechanism output with cmp.

**Verdict rule:** H-SEG7 SURVIVES iff all four bars PASS.
Classification: bounded L2 structural-learning repair (budget
widening + honest overflow signaling). Not L3.

## Honest limits (frozen)

1. The big-integer now has 64 base-1e9 digits (T_n < 1e576). Beyond
   this, the count is reported as T_n mod 1e576 WITH an explicit
   loud overflow signal (no longer silent). A future wave could
   widen further; the signal makes the boundary self-describing.
2. ovf==0 is an exactness certificate; ovf==1 is conservative: the
   printed residue is always exactly T_n mod 1e576, and the flag
   fires iff a top carry was dropped during accumulation.
3. The big-integer DP remains on-demand (sat[n]==1 only). Worst-case
   added memory is (n+1)*64*4 bytes for the saturated run.
4. All other H-SEG6 honest limits unchanged.

## Governance (frozen)

- Prereg committed alone before any implementation edit, build, or run.
- Pure Zag: fixtures, builds, runs, greps, md5, cmp. No Python anywhere.
- Only H-SEG7-owned files staged. No binaries committed (builds in /tmp).
- seg6_learn.zag and all prior evidence untouched.
- No em dashes in loop documentation.
