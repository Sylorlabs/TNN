# PREREG_AMENDMENT1.md: Q_COMB A_SEARCH hand-derivation correction (280 -> 260)

Status: PRE-VERDICT amendment. Pure arithmetic/hand-trace
correction only. No algorithmic counting change. No code
change. Committed before the verdict.

## The error

PREREG.md section 4, ARM-FULL Q_COMB, hand-derived
`(mB0,b=1)` as 70 = 50 (AGG-head) + 20 (partner-tail).
That is wrong. The frozen mr_combine (PREREG section 2,
implemented as specified) attempts the partner-tail ONLY
when the AGG-head succeeds:

```
let hp:i32=mr_agg_seg(...);   // b=1 head
let w1:i32=0;
if(hp!=0){
  ... partner-tail ...
}
if(w1==0){
  ex_p("MR-BIND b=1 FAIL\n");
  // b=2 ...
}
```

For Q_COMB from s=90, the AGG-head mr_agg_seg(90, k=3,
final=0) FAILS SHAPE: the entry (90,7,91) is found, but
the foldwalk from 91 discovers s1=7, s2=17 and then needs
rel 7 from 80, which does not exist (20-tick failing
scan). So hp==0, the tail is never attempted, and
(mB0,b=1) = 50 (head only), not 70.

The sibling combine lane's prereg derived this correctly
((mB0,b=1) = head only, 48); this lane's hand-derivation
mistakenly added a tail that the frozen algorithm never
runs.

## Corrected derivation

Q_COMB A_SEARCH = 2 (AGG search) + 3 (partner collection)
+ 50 (mD,b=1: failed head only)
+ 20 (mD,b=2)
+ 50 (mB0,b=1: failed head only)
+ 135 (mB0,b=2: verified)
= 260.

A_EXEC = 2 (verify + deliver), unchanged.

## What changes

- F-COUNT bar for QC-AS: 280 -> 260.
- PREREG section 4 Q_COMB: A_SEARCH=260 (was 280);
  the "(mB0,b=1)" line is corrected to 50 (head only,
  no tail attempted).
- The composition "2+3+50+20+50+135 = 260" replaces
  "2+3+50+20+70+135 = 280".

## What does NOT change

- Frozen counting rules (section 3): untouched.
- Frozen learner machinery (section 2): untouched.
- All other hand-derived counts (Q_SUB 214/2, Q_TRUNC
  203/2): untouched; Q_SUB and Q_TRUNC have SUCCEEDING
  b=1 heads (midpoints reaching 43/42), so their tails
  ARE attempted and their derivations were already
  correct.
- Kill bars K1-K8, falsifiers, K7 audit: untouched
  (F-COUNT now checks the corrected value).

## Verification

The built binary (no source change) reports
`ARM-FULL-END as=260/214/203 ae=2/2/2`, i.e. QC-AS=260
exactly, confirming the corrected hand-derivation
against the frozen algorithm.
