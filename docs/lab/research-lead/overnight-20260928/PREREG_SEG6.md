# PREREG H-SEG6 FROZEN

**Date:** 2026-09-29
**Researcher:** H-SEG6 Frontier Researcher (subagent)
**Parent:** H-SEG5 SURVIVES (5/5); H-SEG5 red team SURVIVES all 4 attacks.
**Status:** FROZEN. This document is committed alone before any
implementation edit, build, or test run. No Python at any stage.
No em dashes in loop documentation.

## Targeted residual

H-SEG5 honest limit #2 (SEG5_RESULT.md): "The count above 999 remains
unrecoverable by the mechanism (the REF DP is an adversary instrument,
not part of the learner)."

H-SEG5 proved the 999+ cap label exactly honest (sat[n]=1 iff T_n >
999, by induction). But when sat[n]=1, the mechanism reports "999+"
and discards the magnitude. The true count T_n (e.g., 536870912 for
H1-T) is known to the adversary's REF DP but not to the learner.

H-SEG6 closes the residual: when sat[n]=1, the mechanism recomputes
the exact optimal-path count T_n on demand with arbitrary-precision
integer arithmetic, and prints the exact count instead of "999+". The
label becomes not just honest but complete.

## Why on-demand (frozen rationale)

The H-SEG5 proof identifies exactly when the exact count is needed:
sat[n]=1 iff T_n > 999. The big-integer DP runs only in this case.
On non-saturating inputs (the common case; 1969/2130 in the K-SG5-5
battery), no extra work is done. The cost is bounded and the trigger
is proof-derived, not heuristic.

## Why not a wider fixed cap

Any fixed cap C (i32max, i64max) merely moves the saturation point;
counts can exceed it (T_n grows exponentially in n). Arbitrary
precision is the only principled way to report T_n exactly for all
inputs within the digit budget. The digit budget (32 base-1e9 digits,
T_n < 1e288) is documented as an honest limit, not hidden.

## Repair (frozen, exact)

**R1: On-demand big-integer optimal-path counting.** seg6_learn.zag =
seg5_learn.zag copied verbatim plus exactly these edits:

a. New big-integer utilities (base 1e9, little-endian i32 digits):
   - `bigint_add(d, doff, s, soff, nd)`: d[doff..doff+nd) +=
     s[soff..soff+nd), propagating carry. void.
   - `bigint_print(d, doff, nd)`: emit the decimal representation:
     most significant nonzero digit without padding, remaining
     digits zero-padded to 9. If all zero, emit "0". void.
   - NDIGITS() = 32 (constant function, like MAXL()).

b. In run_exp, after the main DP loop completes and before the NOPT
   label: if get32(sat,n*4)==1, compute the exact count:
   - Allocate `bc:[]u8 = z_alloc((n+1)*NDIGITS()*4)`, zeroed.
   - Set bc[0] = 1 (digit 0 of position 0 = 1, rest 0).
   - For i in 0..n-1:
     - Fallback move (len 1, score -FBPEN): np=i+1. If
       get32(dp,i*4)-FBPEN()==get32(dp,np*4), then
       bigint_add(bc, np*NDIGITS(), bc, i*NDIGITS(), NDIGITS()).
     - For each chunk k in 0..nch-1: if ch_match(cht,k,t,i)==1,
       let l=ch_len(cht,k), s=ch_uscore(cht,unc,k), np=i+l.
       If get32(dp,i*4)+s==get32(dp,np*4), then
       bigint_add(bc, np*NDIGITS(), bc, i*NDIGITS(), NDIGITS()).
   - The dp[] array from the main DP is reused; no recomputation
     of scores. The move enumeration mirrors the main DP's move
     set (fallback + all matching chunks).
   - Store a flag `exact:i32=1` and keep `bc` for the label.

c. Label change: replace `emit("999+")` with:
   - If exact==1: `bigint_print(bc, n*NDIGITS(), NDIGITS())`.
   - (exact==1 iff sat[n]==1; the flag is for clarity.)

d. Banner "H-SEG5 SEG-LEX-D" -> "H-SEG6 SEG-LEX-F"; final
   "H-SEG5 COMPLETE" -> "H-SEG6 COMPLETE". No fixture changes.

e. Nothing else changes. seg5_learn.zag untouched.

## Correctness argument (frozen, reviewer-checked)

The big-integer DP computes T_n exactly:
- Base: T_0 = 1 (one empty path). bc[0]=1 correct.
- Step: T_i = sum over optimal moves (p->i) of T_p. A move (p,l,s)
  is optimal iff dp[p]+s == dp[i]. The loop adds bc[p] to bc[i]
  exactly for optimal moves. By induction on i (moves advance >=1,
  so p < i and bc[p] is final), bc[i] = T_i.
- The move set enumerated (fallback + all matching chunks) is
  identical to the main DP's move set, so the optimal-move
  predicate matches.
- Big-integer addition is exact (base 1e9, carry propagated).
- Therefore the printed value equals T_n.

The H-SEG5 proof is unaffected (nopt/sat logic unchanged). The new
code only READS dp/nopt/sat; it does not modify them.

## Frozen kill bars

- **K-SG6-1:** H1-T prints "NOPT 536870912" (the exact count, not
  "999+"). Verified by grep on the output. The value 536870912 =
  2^29 is the REF-confirmed true count (SEG5_RESULT.md).
- **K-SG6-2:** All K-SG5-1..K-SG5-5 still PASS, with one preregistered
  output difference: H1-T's NOPT line now shows the exact count
  instead of "999+". Specifically:
  - K-SG5-1 (doc correction): unchanged, PASS.
  - K-SG5-3 (13 frozen checks): all pass; output byte-identical to
    SEG5_RAW_OUTPUT.txt EXCEPT the H1-T NOPT line ("999+" ->
    "536870912") and the v5->v6 banner lines. The H1-T VERDICT
    (AMBIGUOUS), SCORE, and NCAND are unchanged.
  - K-SG5-4 (determinism): 3/3 byte-identical, md5 recorded.
  - K-SG5-5 (differential battery): the harness is updated so the
    NEW mechanism's printed count (exact, when sat=1) must EQUAL
    the REF true count for all cases with T_n <= 1e9. This is
    STRICTER than H-SEG5 (which only checked the "999+" label).
    0 mismatches required.
- **K-SG6-3:** 3/3 runs byte-identical (cmp), md5 recorded.

**Verdict rule:** H-SEG6 SURVIVES iff all three bars PASS.
Classification: bounded L2 structural-learning repair (exact count
recovery). Not L3: the counting is mechanical; no representational
invention.

## Honest limits (frozen)

1. The big-integer has 32 base-1e9 digits (T_n < 1e288). Beyond this,
   the count would overflow the digit array (carry dropped). The
   frozen fixtures are far below this (max 5e8). Documented, not
   hidden.
2. The big-integer DP is O(n * nch * NDIGITS) time and
   O(n * NDIGITS) memory, but runs only when sat[n]=1 (rare).
3. The H-SEG3 coverage discount is unchanged. The genuine-morpheme
   boundary remains (deliberate tradeoff; see below).
4. The VERDICT logic (SEGMENTED iff nopt[n]==1) is unchanged. The
   exact count does not affect verdicts, only the reported NOPT.

## Why the genuine-morpheme boundary is NOT targeted (frozen)

The H-SEG3 coverage discount exists because the H-SEG2 red team
(X-SG2-1, X-SG2-2) proved that crediting shared substrings fragments
seen training words ("x|abcd" beats "xabcd", 76 > 50). The discount
is a deliberate, red-team-validated tradeoff: preserve whole seen
words at the cost of discounting their shared parts. Any "shared-core
credit" would reintroduce the X-SG2-1 failure. H-SEG6 does not touch
the discount.

## Governance (frozen)

- Prereg committed alone before any implementation edit, build, or run.
- Pure Zag: fixtures, builds, runs, greps, md5, cmp. No Python anywhere.
- Only H-SEG6-owned files staged. No binaries committed (builds in /tmp).
- seg5_learn.zag and all prior evidence untouched.
- No em dashes in loop documentation.
