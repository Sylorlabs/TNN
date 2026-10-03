# PREREG_SEGREDESIGN AMENDMENT 1: Exploratory V2

**Date:** 2026-09-30.
**Status:** This amendment does NOT alter the frozen V1 specification,
frozen kill bars, or verdict rule. It adds an exploratory variant.

## Frozen V1 result (for the record)

V1 as frozen (ilog TP, +26 Laplace, THETA=-15, forward only):
- V1 words discovered: 4/10 (tak, red, blu, cub)
- V0 baseline: 3/10 (tak, bal, cub)
- V1 > V0, but 4/10 < 5/10. Frozen K3 FAILS.

## Rationale for exploratory V2

Diagnosis of V1's limitation: the integer `ilog` quantization destroys
the transitional-probability distinction. Example: P(m|s)=0.43
("sm", within "smal", correct to merge) vs P(r|k)=0.30 ("kr",
tak|red boundary, correct to split). In ilog units both score -20,
indistinguishable. A raw integer ratio preserves the distinction:
342 vs 220.

Additionally, forward-only TP fails when the left character is very
frequent (e.g. 'b' starts bal/blu/big/biger; 'r' is in red/tri/grn/
biger). Taking max(forward, backward) TP uses the more informative
direction per pair.

## V2 specification (exploratory, NOT frozen)

For pair (x=utt[p], y=utt[p+1]):

    fwd = (c_xy + 1) * 1000 / (c_x + 26)
    bwd = (c_xy + 1) * 1000 / (c_y + 26)
    s(p) = max(fwd, bwd)

Boundary iff s(p) < THETA2. THETA2 explored at 250 and 300.
(At t=0: s(p) = 1000/26 = 38 < THETA2, so single characters;
cold-start fix preserved.)

V2 is exploratory. It does not replace V1 for K3. If V2 performs
well, it becomes the candidate for a future frozen wave.

## Governance

- This amendment committed before V2 implementation.
- V1 remains frozen as specified. K3 judged on V1 only.
- No em dashes.
