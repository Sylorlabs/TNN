# PREREG_G1_SHAFTS_1721_ADDENDUM_SIGN.md - sign correction to the v3 clarity gate

Dated 2026-09-24, pre-implementation. This addendum is committed strictly
before any G1 v3 implementation file exists (commit-order discipline: the
frozen prereg commit acf7cedce strictly first, this addendum second,
implementation only after).

## What was found

The frozen prereg PREREG_G1_SHAFTS_1721.md contains an internal
inconsistency, caught by red-team novelty review before implementation.
The clarity-gate formula and its prose describe opposite gates selecting
disjoint pixel sets:

- Formula as frozen: s(P) = (BMEAN_T[b] - T(P))*1024/max(BSTD_T[b],1),
  gate s(P) >= 1088. Since high T means a clear sightline, this s(P) is
  large when T is LOW (dense sightline): the formula gate selects the
  densest decile per radial band.
- Prose as frozen: "clarity score," "light reaches the pixel through a
  gap," "clearer than about 90 percent of its radial band": the prose
  gate selects the clearest decile per radial band.

These two gates select disjoint pixel sets. Both cannot be intended.

## Coordinator decision (quoted verbatim)

COORDINATOR DECISION (dated 2026-09-24, pre-implementation): the frozen
prereg's clarity-gate formula and its prose describe opposite gates
selecting disjoint pixel sets. I adopt the PROSE-INTENDED reading,
because the entire design narrative ("clarity score," "light reaches the
pixel through a gap," "clearer than about 90 percent of its radial band")
is consistent only with it. Concretely: freeze s'(P) =
(T(P) - BMEAN_T[b])*1024/BSTD_T[b] and SGATE = 1152 (the measured p10 of
the flipped score, derived from your committed T-distribution measurement
with no renders involved; it passes ~10% by construction, same design
intent as the frozen 1088). This is a sign-correction addendum under the
S10 internal-consistency rule, not a bar weakening: the gate remains a
measured quantile, frozen before any v3 render.

## Operative frozen change

1. The clarity score is s'(P) = (T(P) - BMEAN_T[b])*1024/BSTD_T[b],
   x1024 units, positive means clearer than the pixel's radial band
   typical. The clarity gate is s'(P) >= SGATE with SGATE = 1152 frozen.
2. 1152 is the negated measured s p10 (-(-1152)) from the committed
   phase-1 T-distribution measurement
   (g1/measure/T_DISTRIBUTION_1721.md): the flipped score's 90th
   percentile, so the gate passes about 10 percent of gated sky pixels
   by construction on the byte-identical baseline. No render was
   involved in deriving it; no normality was assumed.
3. Implementation note (behavior-identical on frozen constants): the
   implementation evaluates (T(P) - BMEAN_T[b])*1024/max(BSTD_T[b],1).
   Every frozen BSTD_T[b] is at least 27, so the guard never fires and
   the evaluated formula equals the frozen s'(P) exactly.

## What is unchanged

Everything else in PREREG_G1_SHAFTS_1721.md stands as frozen: the fan
geometry (K=7, plus or minus 144 px lateral, N=12), the delta(P) > 0
angular predicate, the lift formula, the band constants, the V1-V6
validator, KB1-KB8 and their thresholds, the verdict mapping, and the
purity discipline. This addendum corrects the sign of the clarity gate
only, under the S10 internal-consistency rule. It is not a bar
weakening: the gate remains a measured quantile, frozen before any v3
render, passing about 10 percent by construction exactly as the prereg
intended.
