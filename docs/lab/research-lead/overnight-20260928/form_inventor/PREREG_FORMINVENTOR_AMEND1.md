# AMENDMENT 1 to PREREG_FORMINVENTOR.md

Worker: Form Inventor Builder.
Date: 2026-09-30 UTC.
Status: FROZEN before any implementation. This file must be committed
before `inventor.zag` exists. Strict descendant of 45d3d6875.

## What changes

One cell of the frozen predictions table (K2), RETAINED G2 cost:
6 -> 20. All other cells unchanged.

## Why

Re-derivation of the RETAINED G2 run, step by step, from the
frozen design:

1. After RETAINED H, live=3 (the 2-exception tree), uses3=3,
   strikes3=1, live_sig=SIG3.
2. On G2, phase 1 (refit) fills R=4 examples: subjects
   7000..7003, objects 0,5,5,5. Cost so far: 4.
3. Re-diagnosis on the 4-buffer fires SIG1 (two contiguous
   clusters {0},{5,5,5}), which does not match live_sig=SIG3.
   Strike recorded (strikes3=2), live=-1, discovery resumes with
   the 4 refuting examples kept (n=4, ei=4).
4. Discovery adds subjects 7004 (n=5) and 7005 (n=6). At n=6 the
   menu is tried: F2 fits via the nodd==n-1 branch. Cost: 4+2=6.
5. V=verify_need with uses2=0 gives V=14. Fourteen verify
   examples (subjects 7006..7019). Total cost: 6+14=20.
6. adopted=2.

The original "6" counted only steps 2..4 and omitted the
14-example verification phase. The mechanism note is unchanged:
refit sig mismatch (strike inv), menu F2 wins at n=6, inventor
silent. The tie-break demonstration is unaffected: the menu
still wins because it fits first; only the cost accounting was
wrong.

## Corrected K2 row

| G2 | 2 | 20 | refit sig mismatch (strike inv), menu F2 at n=6 |

K2 passes iff all fourteen adopted/cost pairs match exactly with
this correction, AND the log shows the predicted INV trace lines
(DIAG sig per inventor run, PROMOTE on FRESH G/H/K and RETAINED
G/Gp/H, HONESTFAIL on FRESH J, REFIT sig_match on RETAINED Gp,
STRIKE on RETAINED H and RETAINED G2, and no INV lines at all on
FRESH G2).

## Governance

- This amendment is committed before `inventor.zag` exists.
- `git merge-base --is-ancestor 45d3d6875 HEAD` must pass at the
  result commit, and the amendment commit must be a strict
  descendant of 45d3d6875.
- No other change to the frozen design. The operator vocabulary,
  signatures, and protocols are untouched.
