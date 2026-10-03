# PREREG_AMEND1: Correction to the frozen K2 prediction (UNI-D Q1)

Committed BEFORE the corrected runs. Transparent amendment per the collapse
battery precedent (AMEND1/AMEND2): the error is reported, not hidden; the
earlier exploratory runs are discarded; the 3x3 official runs below are
governed by the amended prediction. No implementation change: the
implementation follows the frozen design; the error was in the prereg's
hand-derivation.

## The error

PREREG Section 5 (K2 derivation) assumed the ADD2 MAP's 1-input contract
fields (field 3 inmask, field 4 outmask) were EMPTY, i.e. "1-input path
untaught", hence "compatible with all". That assumption is false under the
frozen Section 7 allowlist: observe2 (allowlist item 2) writes inmask1 into
field 3 and outmask into field 4. After the frozen Q1 teaching
(teach2(m3,3,2,5); teach2(m3,2,1,3)), G's 1-input contract is inmask={2}
outmask={2}, not empty.

## Corrected derivation (Q1: s=202, kin=1, kout=2, expected=5)

Contracts: m0=X in{1} out{1}; m1=Y in{1} out{2}; m2=W in{1} out{2};
m3=G in{2} out{2} (1-input view).

Singles: X rejected (out{1} not compat kout=2); Y admitted, Y(202)=-2;
W admitted, W(202)=-2; G rejected (in{2} not compat kin=1). 2 tries.

Pairs (x,y), x!=y, in id order; admitted iff kin~x.in, x.out INTERSECTS
y.in, kout~y.out:
- (X,Y): admit. v1=X(202)=211, INTER=211; v2=Y(211)=3 != 5.
- (X,W): admit. INTER=211; v2=W(211)=2 != 5.
- (X,G): reject (out{1} INTER in{2} empty).
- (Y,X): reject (kout vs X.out{1}). (Y,W): reject (out{2} INTER in{1}
  empty). (Y,G): admit (out{2} INTER in{2}). v1=Y(202)=-2, INTER=-2.
- (W,X): reject. (W,Y): reject. (W,G): admit. v1=W(202)=-2, INTER=-2.
- (G,X),(G,Y),(G,W): reject (G.in{2} not compat kin=1).
4 admitted pairs, 4 INTER lines: 211, 211, -2, -2. 6 tries so far.

WIDEN=1 (exhaustive admitted failure). Rejected pairs in id order:
(X,G): v1=211, INTER=211, v2=exec_map(G,211)=-2 (class-4 1-input
arity-mismatch, allowlist item 1); (Y,X),(Y,W),(W,X),(W,Y): v1=-2;
(G,X),(G,Y),(G,W): v1=exec_map(G,202)=-2. 8 tries, 8 INTER lines.

Total TRIES=14, ANS=-2.

## Corrected K2 prediction (replaces the Section 5 Q1 block)

```
INTER=211
INTER=211
INTER=-2
INTER=-2
WIDEN=1
INTER=211
INTER=-2
INTER=-2
INTER=-2
INTER=-2
INTER=-2
INTER=-2
INTER=-2
ARM=UNI-D PROB=Q1 ANS=-2 TRIES=14
```

## What is unchanged

- The bar's substance: U exhausts its entire trial space (admitted singles,
  admitted pairs, widened rejected pairs), fires WIDEN=1, and returns
  ANS=-2. The INFORMATIVE-FAIL verdict condition is identical.
- No implementation change was made or is needed; d6_base.zag/d6_uni.zag
  implement the frozen design, and the observed output matches the
  corrected derivation exactly.
- K1, K3, K4, K5, K6 predictions are unaffected: K1's arenas contain no
  class-4 MAP; GEN never applies 1-input admission to G (garity=2 routes
  it to gen_m2, which reads the same field-3 value the original
  prediction used).
- The discarded exploratory runs (which surfaced this derivation error)
  are reported here, not hidden, and are not used for any kill bar.
