# PREREG H-SEG8 FROZEN

**Date:** 2026-09-29 (PDT)
**Researcher:** H-SEG8 Frontier Researcher (subagent)
**Parent:** H-SEG7 SURVIVES (4/4). Builder result `617957e69`,
builder prereg `5e5f0b9bb`. H-SEG7 red team SURVIVES all 4 attacks
(X-SG7-1..X-SG7-4), result `3728e6464`, adversary prereg `7c56eb3b3`.
**Status:** FROZEN. This document is committed alone before any
implementation edit, build, or test run. No Python at any stage.
No em dashes in loop documentation.

## Targeted residual

H-SEG7 honest limit #1 (SEG7_RESULT.md): "The big-integer has 64
base-1e9 digits (T_n < 1e576). Beyond this, the count is reported
as T_n mod 1e576 WITH the loud overflow signal (no longer
silent). A future wave could widen further; the signal makes the
boundary self-describing."

H-SEG7 closed the SILENT failure mode but kept a boundary: above
10^576 the mechanism prints a residue, not the count. The red
team pinned the boundary exactly ("ab" x 1914 = 2^1913 is the
largest exact count in the H1 family; "ab" x 1915 = 2^1914 is the
smallest overflow) and noted the boundary is pinned by the
family, not swept continuously.

H-SEG8 eliminates the boundary entirely: the digit budget adapts
to the input. If any accumulation drops a carry out of the top
digit, the budget doubles and the accumulation re-runs from
scratch. The loop exits only when zero carries are dropped, at
which point the printed NOPT is the exact T_n for every input.
The SEG7 overflow signal (TRUNCATED-BUDGET-EXCEEDED /
SAT-BUDGET-OVERFLOW) becomes unreachable and is retired. There is
no longer any input on which the mechanism prints anything but
the exact count.

## Repair (frozen, exact)

seg8_learn.zag = seg7_learn.zag copied verbatim (cmp-verified)
plus exactly these edits:

**R1: Adaptive accumulation loop in run_exp.** Replace the
fixed-budget accumulation block:

```
  let bc:[]u8="";
  let ovf:i32=0;
  if(get32(sat,n*4)==1){
    bc=z_alloc((n+1)*NDIGITS()*4);
    ...
  }
```

with:

```
  // H-SEG8: adaptive exact-count budget. nd starts at NDIGITS()
  // (64). If any accumulation drops a top carry (ovf==1), double
  // nd and re-run from scratch. The loop exits with ovf==0, at
  // which point the SEG7 induction gives bc[i]==T_i exactly for
  // all i. Termination: T_n is finite, so some nd suffices; the
  // ovf==0 exit condition is the exactness certificate. The
  // printed NOPT is always the exact T_n.
  let bc:[]u8="";
  let nd:i32=0;
  if(get32(sat,n*4)==1){
    nd=NDIGITS();
    let ovf:i32=1;
    while(ovf==1){
      ovf=0;
      bc=z_alloc((n+1)*nd*4);
      set32(bc,0,1);
      let bi:i32=0;
      while(bi<n){
        let bdpi:i32=get32(dp,bi*4);
        if(bdpi>sent){
          let bnp:i32=bi+1;
          if(bdpi-FBPEN()==get32(dp,bnp*4)){
            if(bigint_add_of(bc,bnp*nd,bc,bi*nd,nd)==1){ ovf=1; }
          }
          let bk:i32=0;
          while(bk<nch){
            if(ch_cnt(cht,bk)>=MINC()){
              let bl:i32=ch_len(cht,bk);
              if(bi+bl<=n){
                if(ch_match(cht,bk,t,bi)==1){
                  let bnp2:i32=bi+bl;
                  if(bdpi+ch_uscore(cht,unc,bk)==get32(dp,bnp2*4)){
                    if(bigint_add_of(bc,bnp2*nd,bc,bi*nd,nd)==1){ ovf=1; }
                  }
                }
              }
            }
            bk=bk+1;
          }
        }
        bi=bi+1;
      }
      if(ovf==1){ nd=nd*2; }
    }
  }
```

All NDIGITS() references inside the accumulation become the
local nd. The dp/chunk/score logic is untouched. On ovf==1 the
corrupted bc is discarded (reallocated fresh next iteration);
dp and the chunk table are read-only, so the re-run is
deterministic and correct.

**R2: Retire the overflow signal.** In the NOPT label block,
replace:

```
  if(no==999){
    if(get32(sat,n*4)==1){
      bigint_print(bc,n*NDIGITS(),NDIGITS());
      if(ovf==1){ emit(" TRUNCATED-BUDGET-EXCEEDED"); }
    }
    else { emit(i32s(no)); }
  } else {
    emit(i32s(no));
  }
  emit("\n");
  if(ovf==1){ emit(tag); emit(" SAT-BUDGET-OVERFLOW: ...\n"); }
```

with:

```
  // H-SEG8: the adaptive loop guarantees ovf==0 at print time,
  // so the printed value is always the exact T_n. The SEG7
  // overflow signal is retired (unreachable).
  if(no==999){
    if(get32(sat,n*4)==1){
      bigint_print(bc,n*nd,nd);
    }
    else { emit(i32s(no)); }
  } else {
    emit(i32s(no));
  }
  emit("\n");
```

The ovf variable no longer exists outside the adaptive loop.
The header comment block (lines 1-18) is updated to describe
SEG-LEX-H.

**R3: New fixtures in main()** (same trained H1 corpus
cth1/unh1/nh1 as the SG7 fixtures):

- SG8-ADD-UNIT: identical U1/U2/U3 carry-out checks (banner text
  "SG8 ADD-UNIT-Uk", exercising bigint_add_of at NDIGITS()=64).
- SG8-BIG: "ab" x 958 (n=1916), T = 2^957 (289 digits). Must
  print exactly, zero markers/lines. Exercises the nd=64
  single-iteration path.
- SG8-HUGE: "ab" x 1915 (n=3830), T = 2^1914 (577 digits). Under
  SEG7 this fired the loud overflow signal; under SEG8 the nd=64
  iteration sets ovf and the nd=128 re-run prints the FULL exact
  577-digit count. Zero markers, zero overflow lines. This is the
  inversion of K-SG7-2.
- SG8-XL: "ab" x 4000 (n=8000), T = 2^3999 (1204 digits).
  Exercises two doublings (64 -> 128 -> 256) and prints the full
  exact 1204-digit count. Zero markers, zero overflow lines.

All pre-existing fixtures (EXP-A/C/D, ADV3, EXP-B, ADV1-T1/T2,
ADV2-T2, H1-T, SENT60, LONG60) are unchanged.

**R4: Banners and header.** "H-SEG7 SEG-LEX-G" -> "H-SEG8
SEG-LEX-H"; "H-SEG7 COMPLETE" -> "H-SEG8 COMPLETE". Header
comment first line and algorithm line updated to H-SEG8; the
honest-limit comment updated (see below). Nothing else changes.
seg7_learn.zag untouched.

## Correctness argument (frozen)

- The per-iteration accumulation is exactly the SEG7
  accumulation with nd in place of NDIGITS(). The SEG7
  correctness proof applies per iteration: if an iteration ends
  with ovf==0, then bc[i] == T_i (mod 10^(9*nd)) with no dropped
  carry, hence bc[i] == T_i exactly for all i.
- The loop exits iff an iteration ends with ovf==0. Therefore at
  loop exit, bc[n] == T_n exactly, and the printed NOPT is the
  exact count. The ovf==0 exit is the exactness certificate; no
  separate signal is needed.
- Termination: T_n is the number of optimal segmentations of a
  length-n input, hence finite. Let D be the number of base-1e9
  digits of max_i(bc[i]) over the exact (infinite-precision)
  accumulation; D is finite. When nd >= D, no add can produce a
  carry out of the top digit, so ovf==0 and the loop exits. The
  doubling sequence 64, 128, 256, ... reaches such an nd. (A
  crude closed-form bound also exists: T_n <= 513^n, so
  nd >= ceil(n*log10(513)/9)+1 always suffices; the loop needs
  no explicit cap.)
- Discarding bc on ovf==1 is safe: the re-run reallocates bc
  zeroed and sets bc[0]=1 before accumulating; dp, sat, and the
  chunk table are never written by the accumulation.
- R2 removes only unreachable output paths: ovf cannot be 1 at
  print time because the loop only exits with ovf==0.

## Frozen kill bars

Independent reference (pure Zag, /tmp scratch, never committed):
repeated-doubling big-int with 256 base-1e9 digits (a different
code path from the mechanism: no DP, no move enumeration, no
chunk table). Prints the exact 2^957, 2^1914, and 2^3999.

- **K-SG8-1 (single-iteration exactness):** SG8-BIG prints the
  exact 2^957 (289 digits), byte-equal (cmp) to the reference
  output for 2^957. Zero TRUNCATED-BUDGET-EXCEEDED markers and
  zero SAT-BUDGET-OVERFLOW lines in the entire program output.
- **K-SG8-2 (boundary inversion):** SG8-HUGE prints the FULL
  exact 2^1914 (577 digits), byte-equal (cmp) to the reference
  full rendering of 2^1914. Zero markers and zero overflow lines
  in the entire program output. (Under SEG7 this input printed
  the 576-digit residue with the loud signal; the count is now
  exact.)
- **K-SG8-3 (double doubling):** SG8-XL prints the FULL exact
  2^3999 (1204 digits), byte-equal (cmp) to the reference full
  rendering of 2^3999. Zero markers and zero overflow lines in
  the entire program output.
- **K-SG8-4 (unit + regression + determinism):** U1/U2/U3 all
  print PASS, zero FAIL lines in the full output. Regression:
  every line of SEG7_RAW_OUTPUT.txt except the two banner lines
  appears byte-identical in the SEG8 output (verified by diff;
  only additions are the SG8 ADD-UNIT lines and the
  SG8-BIG/SG8-HUGE/SG8-XL sections replacing SG7-BIG/SG7-OVF).
  3 consecutive full runs byte-identical (cmp), md5 recorded,
  exit 0.

**Verdict rule:** H-SEG8 SURVIVES iff all four bars PASS.
Classification: bounded L2 structural-learning repair (adaptive
exactness; the truncation failure mode is eliminated, not just
signaled). Not L3: the counting is mechanical; no
representational invention.

## Honest limits (frozen)

1. The exact count is now unconditional: for every input, the
   printed NOPT equals T_n exactly. There is no budget boundary
   and no truncation mode. Memory for the saturated run is
   (n+1)*nd_final*4 bytes where nd_final <= 2x the digits of the
   true count; worst-case work is at most 2x a single
   sufficient-budget run per doubling step.
2. The adaptive loop re-runs the accumulation on overflow; a
   pathological input with an enormous count pays one failed
   iteration per doubling. Termination is guaranteed (see
   correctness argument).
3. The big-integer DP remains on-demand (sat[n]==1 only).
4. All other H-SEG7 honest limits unchanged.

## Governance (frozen)

- Prereg committed alone before any implementation edit, build,
  or run.
- Pure Zag: fixtures, builds, runs, greps, md5, cmp, diff. No
  Python anywhere.
- Only H-SEG8-owned files staged. No binaries committed (builds
  in /tmp/sg8 only).
- seg7_learn.zag and all prior evidence untouched.
- No em dashes in loop documentation.
