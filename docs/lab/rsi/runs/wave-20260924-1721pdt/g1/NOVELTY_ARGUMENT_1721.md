# NOVELTY_ARGUMENT_1721.md - G1 v3 mechanism novelty, wave-20260924-1721pdt

Claim: the v3 mechanism frozen in PREREG_G1_SHAFTS_1721.md is genuinely new
relative to the 1121pdt and 1421pdt mechanisms, and it cannot fail in the
specific way 1421pdt failed. If this argument does not hold up under
red-team review, the recommendation is STAND-DOWN, not a re-freeze.

## What the three mechanisms are, precisely

1121pdt (G1 v1): field T(P) = mean over a 12-step screen-space march from
pixel P toward the sun S of (1024 - D(q)). One sightline per pixel, no
angular structure. Selection: global threshold T(P) > 400, hardcoded,
about 2.75 sigma below the field mean. Result: 97.14 percent of sky pixels
lifted (broad wash, mean dL +33.07), and the verifier point set was
geometrically defective, so the shaft bars were unevaluable. Discarded.

1421pdt (G1 v2): the SAME field T(P) and the SAME single-sightline march,
sun moved to a validated (110,300). Selection: global threshold
T(P) > 707, where 707 = measured mean_T + 1.5 std_T (569 + 1.5*92) under a
normality assumption. Result: 1.1 percent of sky lifted in one faint blob
(2238 px, max dL 9) at x 888..1023, y 254..305, about 870 px from the sun;
0 of 39 validated wedge points lifted; KB2 = 1.0000, KB3 = 0.00.
Discarded as a mechanism miss: the march-mean rewards long line-of-sight
alignments through low-density corridors far from the sun, not fan-shaped
shafts radiating from it; and the 1.5-sigma rule promised about 7 percent
but the field's thin upper tail delivered 1.1 percent.

1721pdt (G1 v3): a DIFFERENT field and a DIFFERENT predicate. The field is
per-ray integrated density I_m(P) = sum of D over 12 march samples, over a
fan of K = 7 sightlines per pixel anchored on the sunward ray (lateral
spread plus or minus 144 px around the sun at the far end). The predicate
is a conjunction: (a) the sunward sightline's integrated density is a
strict local angular minimum, delta(P) = min_{m != 3}(I_m - I_3) > 0
(the gap is flanked by occluders); (b) the radially normalized clarity
score s(P) = (bandmean_T[b] - T(P))*1024/bandstd_T[b] meets a measured
quantile gate, s(P) >= 1088 = the measured 90th percentile of s. The lift
scales with the angular contrast: L = 90*delta/(delta+1024).

## The differences, point by point

1. Field: v1/v2 select on a single march-mean per pixel. v3 computes seven
   integrated densities per pixel and selects on their angular profile.
   The single-sightline quantity T(P) appears in v3 only inside the
   normalized clarity score, never as the selection field.
2. Selection predicate: v1/v2 ask "is this pixel's sightline to the sun
   clear in absolute terms" (a global threshold). v3 asks "is the sunward
   sightline the locally clearest direction from this pixel, and is it
   clear relative to its radial band" (an angular comparison plus a
   normalized quantile gate). Absolute global thresholding exists nowhere
   in v3.
3. Gate basis: v1 hardcoded 400; v2 derived mean + 1.5 sigma assuming
   normality. v3 uses SGATE = 1088, the measured 90th percentile of the
   measured s distribution. No distributional assumption.
4. Geometry coupling: v1/v2 gate the raw field, whose band means run
   447 near the sun to 654 far away (measured this wave), so a global gate
   systematically excludes near-sun pixels. v3 gates the band-normalized
   score, decoupling clarity from radial position.

## Why the 1421pdt failure mode cannot recur

The 1421pdt failure, precisely stated: the selector (global threshold on
march-mean transmittance) lifted high-clearance pixels with no angular
relationship to the sun (a far-field corridor blob, max dL 9, zero wedge
lift), and the gate's normality assumption mispredicted the lift fraction
by a factor of six.

This failure is unrepresentable in v3, for three independent reasons:

(a) The old selector does not exist in v3. A far-field corridor pixel of
    the 1421pdt kind can lift in v3 only if its sunward sightline is
    strictly clearer than all six flank sightlines AND clearer than about
    90 percent of its radial band. A pixel that was lifted in v2 purely
    for absolute clearance, with no angular contrast to the sun, fails
    the delta(P) > 0 predicate by definition. The v2 failure set and the
    v3 lift set are defined by disjoint predicates; the v2 failure cannot
    be reproduced because its selecting condition was deleted.

(b) The gate cannot mispredict the way v2's did. SGATE is the measured
    90th percentile of the measured s distribution on the byte-identical
    baseline, so the clarity gate passes about 10 percent of gated sky
    pixels by construction, not by a normality assumption. The "1.1
    percent versus 7 percent promised" attribution failure has no
    mechanism left to occur.

(c) The radial exclusion cannot recur. The measured 207-step band-mean
    gradient that let a global gate systematically exclude near-sun
    pixels is normalized away per band before the gate is applied.

## Honest caveats (what novelty does not promise)

- v3 can still fail KB2/KB3: if no wedge sightline is a strict angular
  local minimum, or if the D field near the sun has no gap structure at
  the frozen fan scale, the wedge points get zero lift and v3 discards
  exactly like v2. The bars remain genuinely at risk; novelty is a claim
  about the mechanism being structurally different, not about success.
- The D field is shaft machinery only, never rendered as visible cloud,
  so v3's shafts will not align with the rendered clouds. Whether
  sun-anchored bright streaks read as crepuscular shafts is a judgment
  for Micah's eyes on a sealed pair, not something this argument claims.
- The v3 lift concentrates on pixels satisfying a strict inequality over
  integer sums; ties (delta = 0) do not lift. This is frozen as stated.

## Verdict

The v3 mechanism differs from v1 in the field, the predicate, and the
gate; it differs from v2 (which shared v1's field and single-sightline
structure) in the field, the predicate, the gate basis, and the
geometry decoupling. The 1421pdt failure mode depended on the exact
components v3 removed: the global march-mean threshold and the
normality-assumed sigma gate. The novelty claim is rigorous.

Recommendation: PROCEED to implementation under the frozen prereg,
pending red-team certification of this argument. If the red team finds
the argument unconvincing, STAND-DOWN: do not re-freeze, do not
implement.
