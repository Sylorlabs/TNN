# RED-TEAM REVIEW: G1 SUNSHAFTS v3 DISCARD (wave-20260924-1721pdt)

Reviewer: independent red-team agent (finish-up phase), read-only review,
2026-09-25. No repo modifications made by the reviewer.

## Executive verdict: AGREE with DISCARD. No reclassification.

I attacked the verdict on all five assigned fronts: bar integrity, the
addendum, evidence honesty, purity, and confounds, plus implementation
fidelity against the amended prereg. Every attack failed on the evidence.
The DISCARD is sound, the "mechanism miss, not freeze defect"
classification is correct, and the kill bars were not weakened, narrowed,
or re-interpreted. Findings ordered by severity below, with file/commit
evidence for each.

---

## Finding 1 (SEVERE, investigated): The sector-agnostic / upward-detector
tension is real but does not void the verdict

The prereg genuinely contains both statements:

- Sector-agnostic: "The fan has no fixed global opening direction; it is
  anchored per-pixel to the sunward ray" (PREREG_G1_SHAFTS_1721.md,
  Fan-direction design decision).
- Detector-bound: "the WEDGE point set (6 rays from S, directions (r-1,-1))
  measures exactly the fan the mechanism targets" (same file).

I verified the WEDGE geometry in the frozen detector: v_wedge_x(r,t) =
110 + t*(r-1)*36, v_wedge_y(r,t) = 300 - t*36, r=0..5, t=1..8
(g1_validate.zag lines 105-106, 133-149). Since t starts at 1, every
wedge point has y <= 264 < 300: an upward fan, exactly as the prereg
describes, and structurally disjoint from the realized lift band (probe
bbox y 308..458). The verdict's "every wedge point has y < 300" is
verified, not asserted.

Why the verdict's "mechanism miss" ruling still stands: three independent
locks.

(a) The frozen verdict mapping resolves the ambiguity: "No bar may be
weakened, narrowed, or re-interpreted to force a pass." Reading the WEDGE
set as "mis-specified for a sector-agnostic fan" and discounting KB2/KB3
would be precisely the forbidden post-hoc re-interpretation.

(b) The novelty argument's honest caveat pre-registered this exact branch:
"v3 can still fail KB2/KB3: if no wedge sightline is a strict angular
local minimum... the wedge points get zero lift and v3 discards exactly
like v2" (NOVELTY_ARGUMENT_1721.md). You cannot pre-register "this
failure mode maps to DISCARD" and then reclassify it as a freeze defect
when it happens.

(c) The prereg's own authorial claim binds intent: the prereg asserts the
WEDGE "measures exactly the fan the mechanism targets." The author
believed the mechanism targeted the upward fan; the mechanism missed that
target because its predicate has no sector prior and the D field's
near-sun angular minima lie below the sun. That is a property of the
mechanism-field interaction: a mechanism miss. The visual concept
(crepuscular shafts fan upward from a sun 76 px above the ridge) is
unchanged; the mechanism failed to produce it.

Fault assignment: mechanism. Not the detector (it measures exactly what
was frozen: the generation functions in g1_verify_v3.zag lines 107-108
are the same functions as the validator's, and the prereg's (r-1,-1)
description matches exactly). Not a voidable freeze defect (the bars are
fully evaluable and measured what they specify).

## Finding 2 (HIGH, investigated): The sign-correction addendum is a
legitimate freeze-defect repair, not post-hoc tuning

The prereg's clarity gate contained a genuine internal contradiction,
which I verified arithmetically: frozen formula
s(P) = (BMEAN_T[b] - T(P))*1024/max(BSTD_T[b],1) with gate s >= 1088,
where high T means a clear sightline. s is large when T is LOW, so the
formula gate selects the densest decile per band. The prose ("clarity
score," "clearer than about 90 percent of its radial band," "light
reaches the pixel through a gap") selects the clearest decile. Disjoint
pixel sets; both cannot be intended.

Legitimacy evidence:

- Commit order verified by git ancestry: acf7cedce (prereg) is an
  ancestor of 1da140387 (addendum), which is an ancestor of 39707e077
  (implementation). git show 1da140387 --stat confirms the addendum
  commit contains only the addendum .md file; g1_sunshafts_v3.zag first
  appears in 39707e077. No implementation existed when the gate was
  corrected.
- SGATE=1152 is independently derivable from the committed diagnostic:
  T_DISTRIBUTION_1721.md records s quantiles p10 = -1152 for the
  unflipped score; the flipped score s' = -s therefore has p90 = 1152.
  No renders involved. The addendum correctly used the flipped score's
  own 90th percentile rather than blindly negating 1088 (the
  distribution is slightly asymmetric: p10=-1152 vs p90=1088), which is
  the careful move.
- Design intent preserved and confirmed on the byte-identical baseline:
  tripwire measured 28476/323997 = 87.9 per mille, inside the frozen
  50..150 band: "about 10 percent by construction" holds.
- Precedent: the S10 internal-consistency addendum is an established
  loop convention, used in the 0521pdt wave (PREREG_SECONDPATH_PARTE_0521.md
  references the S10 addendum commit fb307a1b7 for a pre-implementation
  bound dispute). Not invented ad hoc for this wave.
- Not a bar weakening: KB1..KB8 thresholds are untouched; the clarity
  gate is a mechanism predicate, not a kill bar. Adopting the formula
  reading instead would have made the mechanism lift the densest
  sightlines, contradicting the entire design narrative: the prose
  reading was forced, not chosen.
- Implementation matches the amended freeze exactly: fn g1v3_sgate()
  i64 { return 1152; } (g1_sunshafts_v3.zag:1086), gate evaluates
  (T - bandmean)*1024/std >= 1152 (line 1149), center-ray jitter seeds
  9132+k/9133+k (lines 1038-1039), flank seeds +64*m (lines 1095-1096),
  lateral spread j*48 (lines 1161-1162), perpendicular
  (dys*1024/r, -dxs*1024/r) matching the prereg's formula, strict
  delta > 0, L = 90*delta/(delta+1024) in sun color (255,172,112) via
  L*255/90 etc., sky-only, frozen short-circuit evaluation order. The
  verdict's "predicate worked as specified" is verified, not assumed.

## Finding 3 (MEDIUM, verified): Load-bearing numbers are honest: every
one traces to committed evidence

- Probe output (evidence_probe_lift.txt) reads verbatim: lift_n=2609,
  bbox_x=125..1023, bbox_y=308..458, centroid=301,349,
  max_abs_dL=35, near_sun_r200=2003. The verdict quotes all six exactly.
  2003/2609 = 76.78 percent, so "77 percent" is fair rounding. The probe
  defines near-sun as isqrt(dx^2+dy^2) < 200 (probe_lift_v3.zag),
  matching "within 200 px."
- Trace (evidence_v3_run1.txt): "gated_px=323997 clarity_pass=28476
  delta_pass=2805 lifted_px=2805": matches the verdict and the tripwire
  record (evidence_tripwire.txt: per_mille=87).
- Quantization reconciliation is correct: 2805 - 2609 = 196, and
  L = 90*delta/(delta+1024) < 1 iff 89*delta < 1024 iff delta <= 11,
  i.e. delta < 12 gives integer L = 0. The verdict's parenthetical is
  exact.
- Verifier (evidence_verify_v3.txt): INFO_KB2_RATIO_X10000=10000 gives
  1.0000; INFO_KB3_VAR_X100=0 gives 0.00; KB4/KB5 x100 = 0; KB6 472/472
  gives 1.0000; KB7 = 0. All match the per-bar table. Kept counts
  39/48/64/24 are identical in evidence_validator.txt and
  evidence_verify_v3.txt.
- Thresholds in the verifier match the frozen prereg: KB2
  sumLv*100 >= sumLb*112 (g1_verify_v3.zag:350) = ratio >= 1.12; KB3
  (sumD2*wn - sumD*sumD)*100 >= 6000*wn*wn (line 351) = var(dL) >= 60.0.
  No drift.
- Determinism sha 96f3a899... matches across evidence_v3_sha.txt and
  the verdict; walltime 1964/934 = 2.10x <= 3x (evidence_walltime.txt).
- Effective marches: 1 + 6*(28476/323997) = 1.53 per gated pixel: the
  verdict's "about 1.5" checks out.

Minor nits (immaterial): "8.7 percent" is actually 8.79 percent; "2609
sky pixels": the probe counts all nonzero-dL pixels without a tier
filter, but sky-only follows from the mechanism's tier-0 construction
plus KB4 = 0.00. Neither affects any bar.

## Finding 4 (LOW, verified): Purity holds under independent check

With // comments stripped (the Zag comment convention; the runner's own
check uses the same), grepped all .zag sources in g1/, g1/sub/,
g1/measure/ plus run_g1v3.sh: zero python tokens, zero .py files, zero
python invocations in the runner (the only matches are the runner's own
self-check grep patterns and comments reading "No Python"), zero
rand/time/clock calls (only comments). The verdict's purity section is
accurate. Pure Zag throughout, pinned toolchain as recorded.

## Finding 5 (MEDIUM, investigated): KB2/KB3 failure is geometric, not a
validator/verifier confound

- The verifier's point-set generation functions are the same functions
  as the validator's (byte-comparable definitions), and kept counts are
  identical (39/48/64/24 on both): no tier-filtering divergence between
  validator and verifier.
- dL = 0 at all 39 wedge points because the lifted band (y 308..458,
  probe-measured) is structurally disjoint from the wedge fan
  (y <= 264). The probe characterizes the lift geometry independently of
  the verifier's point sets, and the two agree.
- KB4 = KB5 = 0.00 corroborate: the lift landed neither on terrain nor
  on off-wedge sky: exactly what the probe's below-sun band says.
- Integer quantization (Finding 3) explains the 2805 to 2609
  reconciliation and is disclosed; it is not the driver of the kill (the
  driver is location, not magnitude).

## On the verdict's "mechanism miss, not freeze defect" ruling

Agree. The mechanism's predicate, as frozen and as implemented, selects
strict angular local minima of integrated density wherever the D field
puts them, with no sector prior. The deck's clearest near-sun angular
minima lie below the sun; the upward fan the concept and detector
require got zero lift. The verdict's structural observation: the
predicate needs a sector prior, or the D field needs correspondence
with the visible cloud: is the correct lesson, and it is correctly
deferred to a new prereg rather than patched. The novelty claim's core
(v2's far-field corridor blob is gone; the selector was deleted) held,
and a new failure mode (sector-agnostic selection) appeared in its
place: exactly the honest terminal state the verdict reports.

## Recommended ruling for the debate group

DISCARD stands. No reclassification. No bar may be revisited. The wave
spent is a clean negative result: sun-anchored directional-contrast
selection confirmed working as frozen (87.9 per mille clarity pass,
delta predicate firing on 2805 px, max dL 35, 77 percent within 200 px
of the sun), but sector-agnostic selection misses the upward fan KB2/KB3
require. Any future shaft work needs a sector prior and is a new prereg,
not a repair. Per the verdict's staffing note and the standing mandate,
the frontier remains PAMs v2 and b_alpha v9.

Also verified: no G1 sealed A/B pair or JUDGE_BRIEF.md was prepared (the
sealed/ files in the wave dir belong to CV-1's scoring, a separate
candidate), and nothing was pushed to GitHub.
