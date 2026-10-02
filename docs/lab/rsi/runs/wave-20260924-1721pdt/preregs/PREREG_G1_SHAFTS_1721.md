# PREREG_G1_SHAFTS_1721.md - G1 SUNSHAFTS v3, wave-20260924-1721pdt

Frozen before any G1 v3 code exists. This prereg does not repair the 1421pdt
mechanism; it replaces it. Two waves have been spent on G1 internals
(1121pdt: geometrically defective verifier plus a 400 gate that washed
97.14 percent of the sky; 1421pdt: defects repaired, gate recalibrated to
707, then discarded on a mechanism miss). The 1421pdt verdict ruled the
miss structural: the march-mean transmittance rewards long line-of-sight
alignments through low-density corridors far from the sun, not fan-shaped
shafts radiating from it, and the frozen 1.5-sigma gate assumed a normality
the T field lacks (1.1 percent lifted versus about 7 percent promised).
This prereg freezes a genuinely new mechanism, directional-contrast fan
selection, plus a gate set from measured quantiles on a radially normalized
field, decoupling the two unknowns the 1421pdt freeze coupled together.
No constant below may be tuned against renders.

## Substrate (frozen, inherited unchanged)

- Source: docs/lab/imagination_discovery/img/r8c_alien.zag (Fork C,
  mind's-eye elaboration, 1024x1024 BMP output).
- Vendored IO: g1/sub/R33_NATIVE_IO_V1.zag, byte-identical copy of the
  committed file, sha256
  e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8.
- Baseline: the variant is built on a byte copy of r8c_alien.zag with only
  the @import line repointed. Frozen gate: baseline BMP sha256 must equal
  e4f6555700ad6983e323177573ea66cb0a16c5d121a7b32a34fff5735afecb0d
  (the S14 record). A mismatch aborts the battery before any variant
  work is evaluated.
- Toolchain: src/tools/toolchain/znc_linux_x86_64_abed8aa1, sha256
  498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef,
  verified with sha256sum before use.

## Measured T distribution (frozen diagnostic evidence, phase 1)

Measured in pure Zag on the rebuilt byte-identical baseline with the
verbatim 1421pdt field machinery (N=12 march toward S=(110,300)); the run
reproduced the 1421pdt record exactly (n=325786, mean_T=569, std_T=92),
confirming the machinery. Full record:
g1/measure/T_DISTRIBUTION_1721.md (read-only). Summary frozen here:

- T over sky pixels: min 383, max 725, mean 569, std 92, skewness -0.376
  (left-skewed; median 592 above mean 569).
- Exact quantiles: p01 392, p05 409, p10 431, p25 490, p50 592,
  p75 640, p90 682, p95 689, p99 708.
- Fraction above the old 707 gate: 1.12 percent, versus 6.68 percent under
  the normal assumption the 1421pdt gate used. The upper tail is thin; no
  sigma-multiple gate is safe on this field.
- Radial gradient around the sun (128 px bands, sky pixels with r >= 24):
  band means run 447 (band 0, r < 128) to 654 (band 5), a 207-step spread
  against within-band stds of 27 to 55. A global gate on T systematically
  excludes near-sun pixels: gate and geometry were coupled.

## Mechanism: G1 v3 directional-contrast fan selection (frozen)

Screen-space crepuscular shafts, a new pass g1_pass_sunshafts_v3 running
after r8c_pass3 (light logic) and before r8c_pass4 (fixations). Pure Zag,
zero RNG, fully deterministic. The core idea: for each sky pixel, march a
fan of sightlines toward the sun region; lift the pixel only where the
sunward sightline's integrated density is a strict local angular minimum
(light reaches the pixel through a gap) while the flank sightlines show
higher integrated density (occluders flank the gap). The selected set is a
collection of sun-anchored sightlines by construction: fan-shaped shafts
radiating from the sun, which the march-mean transmittance could not
select.

Frozen constants:

- SUN S = (110, 300), inherited. Geometry re-validated by the carried-over
  V1-V6 validator below (76 px above the ridge, tier 0).
- Cloud-deck density field D(x,y) =
  r8c_fbm(x*256/520, y*256/180, 9131, 3), inherited unchanged. Shaft
  machinery only, never rendered as visible cloud.
- N = 12 march steps, inherited. Jitter
  r8c_h01(x,y,seed)/64-8 and r8c_h01(y,x,seed+1)/64-8, inherited
  anti-banding, deterministic.
- R_MIN = 24: sky pixels with r(P) < 24, where
  r(P) = isqrt((x-110)^2 + (y-300)^2), are skipped (the fan degenerates
  at the sun; this is the sun-glow region). 323997 of 325786 sky pixels
  remain per the phase-1 measurement.
- Fan: K = 7 sightlines. Ray m = 0..6 corresponds to lateral offset
  j = m - 3 in (-3..3). Ray m marches from P toward
  Q_m = (110 + j*48*px/1024, 300 + j*48*py/1024), where
  px = -(300-y)*1024/r(P) and py = (110-x)*1024/r(P) is the x1024
  perpendicular of the sunward direction. March samples:
  q_k = P + (Q_m - P)*t/1024 + jitter, t = k*1024/12, k = 0..11,
  clamped to [0,1023]. The sunward ray (m = 3, j = 0) uses the exact
  g1_transmittance jitter seeds (9132+k, 9133+k), so its march is
  identical to the frozen T(P) march; flank rays (m != 3) use seeds
  9132+k+64*m and 9133+k+64*m, distinct per ray, deterministic.
- Integrated density I_m(P) = sum over the 12 march samples of D(q_k).
  For the sunward ray, I_3(P) = 12*(1024 - T(P)) exactly. Integrated
  density (optical-depth proxy) is the frozen quantity rather than
  bottleneck min-D: light attenuation scales with integrated density, so
  it is the physically right measure of "light reaches the pixel through
  a gap". This is a frozen design decision, not a tunable.
- Angular contrast: delta(P) = min over m != 3 of (I_m(P) - I_3(P)).
  Lift requires delta(P) > 0: the sunward sightline is strictly clearer
  than every flank sightline.
- Radial-band clarity gate (the decoupling): b = min(r(P) >> 7, 7),
  eight 128 px bands. s(P) =
  (BMEAN_T[b] - T(P)) * 1024 / max(BSTD_T[b], 1), x1024 units, positive
  means clearer than the band typical. Frozen band constants from the
  phase-1 measurement:
  b=0: mean 447, std 41; b=1: mean 461, std 53; b=2: mean 542, std 55;
  b=3: mean 616, std 29; b=4: mean 650, std 27; b=5: mean 654, std 30;
  b=6: mean 652, std 41; b=7: mean 633, std 55.
  Lift requires s(P) >= SGATE with SGATE = 1088 frozen, the measured
  90th percentile of s over gated sky pixels (about 10 percent pass the
  clarity gate; the delta predicate restricts further). No normality
  assumption anywhere: the gate is a measured quantile of a measured
  distribution, and the band normalization removes the 207-step radial
  gradient that coupled the 1421pdt gate to geometry.
- Lift: L(P) = 90 * delta(P) / (delta(P) + 1024), applied in sun color
  (255,172,112), per-channel clamp at 255, sky pixels only (tier 0,
  r >= 24). Rationale frozen: lift scales with the angular contrast (how
  much clearer the gap is than its flanks), saturating at the inherited
  LMAX = 90; a shaft is bright where the gap is clean relative to its
  occluders, which is also what gives the frozen variance bar something
  genuine to measure. Terrain skipped by construction.
- The elaboration trace records G1.1..G1.8 decision lines as in 1421pdt,
  plus the fan constants and the counts passing each predicate
  (clarity gate, delta > 0).

## Fan-direction design decision (explicit, frozen)

The fan has no fixed global opening direction; it is anchored per-pixel to
the sunward ray. The seven sightlines converge at the pixel and spread
plus or minus 144 px laterally around the sun at the far end (j*48 px for
j = -3..3). Globally, the lifted set is therefore a collection of
sightlines radiating from the sun region: fan-shaped shafts by
construction. This is the structural difference from 1121pdt and 1421pdt,
which tested one sightline per pixel with no angular comparison and so
could not distinguish a sun-anchored shaft from any high-clearance
corridor anywhere in the frame. The plus or minus 144 px lateral spread
(at r = 300 px about plus or minus 25 degrees; at r = 900 px about plus
or minus 9 degrees) spans several correlation lengths of the
wind-stretched fbm deck (x*256/520 maps about 2 px per fbm unit, 3
octaves, features decorrelate over tens of px), so flank rays sample
independent deck structure while the center ray samples the sightline.
The sun geometry the fan assumes (S = (110,300), 76 px above the ridge,
tier 0) is re-validated on every run by the carried-over V1-V6 validator;
the WEDGE point set (6 rays from S, directions (r-1,-1)) measures exactly
the fan the mechanism targets.

## Geometric validator (frozen procedure, carried over unchanged)

The pure-Zag validator g1_validate.zag from 1421pdt is carried over
verbatim: same frozen point sets (WEDGE 48 candidates, OFFWEDGE 48,
TERRAIN 64, RADCUT 24), same keep rules, same pass criteria V1 through V6
(sun at least 40 px above the ridge; sun tier 0; every kept WEDGE,
OFFWEDGE, RADCUT point tier 0; keep counts at least 36/36/56/16), same
runner cross-check diffing validator and verifier kept counts. The runner
aborts the whole battery (verdict DISCARD, no sealed pair) if the
validator fails.

## Frozen kill bars (re-frozen unchanged; they were honest and at risk)

Luma L = (299R + 587G + 114B)/1000; dL = L_variant - L_baseline.
Thresholds are inherited unchanged from the 1421pdt freeze: KB2 and KB3
killed v2 outright, so these bars are genuinely at risk, and re-freezing
them unchanged is the honest choice (no tuning against the new
mechanism's unknown behavior).

- KB1 determinism: 3 reruns of the variant are byte-identical
  (shas recorded).
- KB2 shaft ratio: mean variant luma / mean baseline luma over kept
  WEDGE points >= 1.12.
- KB3 shaft variance: var(dL) over kept WEDGE points >= 60.0.
- KB4 terrain untouched: mean|dL| over kept TERRAIN points <= 1.0.
- KB5 no broad wash: mean|dL| over kept OFFWEDGE points <= 6.0.
- KB6 acutance: D19 acutance ratio (variant/baseline, 2px step) over
  the frozen SKY12 points <= 1.10. The E3 film-grain rejection is
  honored: KB6 guards acutance, and no grain is added.
- KB7 smoothness: max |second difference of dL| along the kept RADCUT
  in t order <= 25.
- KB8 cost: variant total wall time <= 3.0x baseline total wall time.
  (The v3 shaft work is about 1.6 marches per sky pixel versus 2.0 for
  v2, so 3.0x remains passable while still binding runaway cost.)

## Verdict mapping (frozen)

READY-FOR-JUDGE (sealed blind A/B pair plus JUDGE_BRIEF.md carrying the
machine-checkable provenance header) iff the baseline byte-identity gate
passes AND the geometric validator passes AND KB1 through KB8 all pass as
specified. Any gate failed, any validator check failed, any bar failed,
or any bar unevaluable maps to DISCARD: no sealed pair is prepared and
nothing enters the judge queue. No bar may be weakened, narrowed, or
re-interpreted to force a pass. The E3 film grain rejection is honored.

## Provenance header (required on JUDGE_BRIEF.md if the verdict is
READY-FOR-JUDGE)

- RENDER_SHA: sha256 of the adopted variant BMP.
- FIRST_RENDERED_WAVE: wave-20260924-1721pdt.
- COMPONENT_LINEAGE: r8c substrate inherited from
  docs/lab/imagination_discovery/img/r8c_alien.zag; variant BMPs are new
  renders of this wave; prior judge-queue items R9, C1, C2v3, S11-IMG,
  C12, S11-AUD, S13, S14, whirlpool-planform untouched and listed
  QUEUED-UNJUDGED.
- NEW_KNOWLEDGE_CLAIM: one sentence stating what this candidate teaches
  that no prior wave established (candidate: whether sun-anchored
  directional-contrast selection produces visible crepuscular shafts where
  march-mean transmittance produced only a far-field wash).

## Purity and discipline (frozen)

Pure Zag only: no Python anywhere, not glue, not analysis, not verifiers,
not harnesses, not /tmp scratch. Any Python contact voids the evidence:
self-disclose, void tainted results, redo clean. Static checks in the
runner grep for .py files, python tokens in .zag sources and the runner,
and rand/time/clock calls. Commits stay local on tnn-native-lab; nothing
is pushed to GitHub. Commit order: this prereg commit strictly first,
then implementation and evidence commits. Only the candidate's own paths
are added. No em-dashes in loop documentation.
