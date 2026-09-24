# WILD-C Addendum Corrigendum (pre-evidence)

**Date:** 2026-09-24. **Track:** WILD-C. **Status:** PRE-EVIDENCE CORRECTION.
Parent: `pam/round4/wild/tape/TAPE_WILDC_ADDENDUM.md` (frozen).

This corrigendum corrects two wording errors in the frozen addendum. It does
not alter any frozen value, fixture, or mechanism.

## 1. Build import (§5)

The addendum §5 states "`wildc.zag` (imports `common.zag`, both compiled from
the build directory)".

**Correction:** The WILD-C battery (`wildc.zag`) imports the IO substrate
`R33_NATIVE_IO_V1.zag` directly. There is no `common.zag` in the WILD-C
build. The pipeline described in §5 (parse → canonicalize → producer lookup
→ feature word → C3 bit → design rule → OUT) is implemented directly in
`wildc.zag` using the substrate's native IO primitives.

## 2. W18 SeedGaps disjointness (§6)

The addendum §6 states: "G1 (domain=FNV("tape"), pred=1, evidence={EXT},
OPEN); G2 (domain=FNV("probe"), pred=1, evidence={EXT}, OPEN). Disjoint from
all frozen fixtures (synthetic domains)."

**Correction:** G1's domain `FNV("tape")` intentionally matches the honest C
rows' subject (`tape`). G1 is NOT disjoint from the honest C family; it
exercises the gap-fill machinery on honest C traffic (first C row fills G1;
subsequent C rows with the same object are not vetoed). G1 IS disjoint from
the attack (A/LAU/FRK/FRG), W, P, and B families. G2's domain `FNV("probe")`
is synthetic and disjoint from all frozen fixtures.

The "disjoint from all frozen fixtures" clause is corrected to: "G1 exercises
C and is disjoint from attack/W/P/B families; G2 is fully synthetic."

## 3. No mechanism change

Both corrections are documentation-only. The compiled receptors, feature
inventory, producer table, and all design mechanisms are unchanged from the
frozen preregs.
