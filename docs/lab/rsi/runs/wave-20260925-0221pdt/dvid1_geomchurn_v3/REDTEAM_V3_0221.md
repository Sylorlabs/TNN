# REDTEAM V3 0221: D-VID-1 V3 geometry-churn independent red-team review

Wave: wave-20260925-0221pdt. Reviewer: Worker 1b (independent red-team / VKB6 eye review).
Working copy: ~/workspace/tnn-rsi, branch tnn-native-lab. Implementation under review:
docs/lab/rsi/runs/wave-20260925-0221pdt/dvid1_geomchurn_v3/ocean_dvid1_v3.zag.
Prereg: commit 0ba679b11 (PREREG_DVID1_V3_2321.md), certified before implementation.
This review was done from the committed-source files, not from Worker 1's claims.
Worker 1's files were awaited (run dir appeared during the session); nothing here
is taken on trust. Zero Python was used at any step of this review (shell
coreutils, git, ffmpeg, od/awk only). The voided 2321pdt bytes were never opened
or cited, per the quarantine rule.

## Provenance probe (quoted verbatim)

"What is the provenance of the artifacts under judgment, and what exactly is new
versus inherited?"

Answer from the committed record. The artifacts under judgment are the 48
variant frames rendered from ocean_dvid1_v3.zag, RENDER_SHA
c654ebe4ba3a96361324fdcf362324da30ef857feed4a60202d07d4e00d3827c
(sha256 of the source file, independently re-hashed and matching), wave
wave-20260925-0221pdt, manifest MANIFEST_V3_SHA256.txt. Component lineage, from
the frozen prereg: D-VID-1 V1 (flow-advected foam breakup): DEAD [NEW],
wave-20260923-2321pdt, killed on the frozen T1 bar (variant 606 vs baseline 580
per-mille, ratio 1.045 against bar <= 0.700). D-VID-1 V2 (co-rotating foam
breakup): DEAD [VOID], wave-20260924-0521pdt, analytic no-op proof (bfade = 0 in
the disc kills every retargeted term), wave evidence VOID on a mid-wave python3
heredoc. Whirlpool SCOOP: DISCARDED. Whirlpool surface-planform:
READY-FOR-JUDGE, QUEUED-UNJUDGED. NEW in V3, verified by direct diff against the
baseline ocean.zag (exactly three hunks, nothing else): (1) file header comment
(lines 3-15), (2) the o_sin_bh / o_sin1000 helpers (lines 235-245), (3) the
frozen churn block in o_shade_water (lines 523-592). INHERITED, byte-identical
to the 2026-09-22 D-VID-1 baseline: scene, camera, frame count (48),
resolution (1024x1024), breakup sampling coordinates and seeds (bup 51, abup 52,
sbup 54), the bfade fade law, capth, streak ridge scale 36 seed 53, ring scale,
normal perturbation, base color, specular, fog, dither. The file header states
this is a fresh implementation from the frozen prereg text only, written after
the 2321pdt implementation was voided on a Python breach; the review below does
not rely on that statement.

## G-LIVE re-verification (from the source, per sub-gate)

G1 (the V2 failure cannot recur): PASS. Line 479:
`let bfade:i64 = o_clamp01k((200 - wz) * 1000 / 140);` is 0 for all wz >= 200.
o_mix is the identity at t = 0 (line 75: `return a + (b - a) * t / 1000;`), so
line 481 gives bupm = o_mix(1000, X, 0) = 1000. Line 576
(`foam_d = foam_d * bupm / 1000;`) is the identity, and line 585 (the streak
breakup factor `o_mix(1000, o_ss((sbup - 430) * 1000 / 270), bfade) / 1000`)
equals 1. The displaced geometry terms reach foam_d through max() comparisons
(lines 574, 575, 578, 586, 588) with no bfade-gated zero factor anywhere in the
block.

G2 (dataflow): PASS. foam_d = max(crestf2, steepf2, armf2, streakf2, ringf2):
seeded at line 574 (crestf2), maxed with steepf2 at line 575, scaled by the
identity bupm at line 576, maxed with armf2 at line 578, with streakf2 at line
586, with ringf2 at line 588, clamped at line 589. Each term is a pure function
of the displaced position (mwx, mwz): crestf2 from h2 computed by o_height at
(mwx, mwz) (line 557); steepf2 from central differences of o_height at displaced
offsets (lines 561-571); armf2 from arm2 returned by the same displaced o_height
call; streakf2 from o_ridge2(mbx * 36, mbz * 36, 2, 53) where (mbx, mbz) derive
from the displaced (mwx, mwz) (lines 579-584); ringf2 from sprox2 from the
displaced o_height call (line 587). Line 591:
`foam = o_mix(foam, foam_d, churn_gate);`. churn_gate (line 533:
`o_clamp01k((190 - gr) * 1000 / 40)`) equals 1000 for gr <= 150 world units, so
the gate is fully open over the metric region core.

G3 (displacement is non-degenerate): PASS. Amplitudes A1..A4 = 22, 14, 20, 12
(lines 552-553), all strictly positive. The four sine phases (lines 537-540)
use (P, Q) pairs (9, 35), (14, 55), (11, 45), (17, 28) per-mille per world unit
and per frame. Temporal periods are 1000/35 = 28.57, 1000/55 = 18.18,
1000/45 = 22.22, 1000/28 = 35.71 frames; every pairwise beat period exceeds the
48-frame clip (for example 200/7 vs 200/11 frames beat at 200 frames), so no two
components resynchronize inside the clip and no standing-wave cancellation
occurs. Dx = 0 requires 22*s1 + 14*s2 = 0 (a one-dimensional level set per
frame) and Dz = 0 requires 20*s3 + 12*s4 = 0 (an independent one-dimensional
level set); their intersection is sparse, so (mwx, mwz) != (wx, wz) on a dense
set of disc pixels at every frame. Displacement magnitude: |Dx| <= 36,
|Dz| <= 32 world units (|D| <= 49), matching the frozen "about 61 px at disc
depth" scale note in order of magnitude.

Honest limitation (frozen): VERIFIED. ringf2 is dead in the disc because
sprox2 = 0 there. sprox is nonzero only within 120 world units of a spire base
(lines 310-327); spires stand at wz 2500..3900 (o_spire); disc pixels sit at wz
560..880 and the displacement moves them at most 49 world units, so the nearest
approach to any spire stays above 1500 world units. Line 587 therefore yields
ringf2 = 0 throughout the disc. Liveness rests on crestf2, steepf2, armf2,
streakf2, as the prereg states.

G-LIVE overall: PASS (G1 PASS, G2 PASS, G3 PASS, honest limitation verified).

## Novelty vs V1/V2: genuinely NEW mechanism, verified

The diff of ocean_dvid1_v3.zag against the baseline ocean.zag contains exactly
three hunks and no other changes: the header comment, the sine helpers, and the
churn block. In particular: no coordinate-retargeting of breakup sampling (bup
line 480, abup line 508, sbup line 517 keep the exact baseline formulas and
seeds 51/52/54; only line numbers shifted). No bfade law change (line 479 is
the baseline formula). No "inverse" or "retarget" tokens anywhere in the V3
source. The frozen "what does NOT change" list holds in the source: bfade2
block (lines 430-432), capth, streak ridge scale 36 seed 53 (line 583), ring
scale 750/1000, base color, specular, fog, dither, 48 frames, 1024x1024,
scene, camera. Outside the disc (churn_gate = 0) the variant is bit-identical
to the baseline by construction (the block is skipped; o_mix(foam, foam, 0) =
foam), and this was verified empirically on frames f10, f24, f40 (zero differing
pixels outside a y 380..420 exclusion band). The displacement block is written
fresh: it introduces the Bhaskara sine helpers (absent from the baseline) and a
displacement-field resampling of foam geometry, sharing no code with the voided
V2 approach (no breakup-sampling retargeting, no inverse transform; the prereg
lineage was read, void/ was not opened). Novelty verdict: PASS, genuinely new
relative to V1 and V2.

## VKB6 eye review (core of this review)

Method: all 48 baseline BMPs and all 48 variant BMPs (render r1) converted to
PNG with ffmpeg; full frames viewed; the churn footprint localized with
difference bounding boxes at f0/f12/f24/f36/f47; temporal strips built
(time-vertical, 48 frames) through the churn band at four heights for both
sequences; magnified band crops viewed base-vs-variant; Worker 1's foam_dbg
dumps (dbg=6 foam channel, f00/f10/f23/f47, base and v3) reviewed.

Concrete observations:

1. Footprint. The variant differs from the baseline only inside a thin sliver:
x ~419..1016 (drifting horizontally as the vortex center wanders via o_scene),
y 395..408 (11 to 13 px tall), at every frame f0..f47. This matches the analytic
projection: the disc (r <= 190 world units around (vwx, vwz ~= 720)) foreshortens
to about 13 px vertically at that distance (projected disc depth extent sy
398..411 by direct evaluation of o_sy). The churn is live, but its screen
footprint is a ~13 px sliver near the horizon.

2. Saturation. In the sliver the foam channel is saturated: base mean 253.9/255
(foam ~= 996/1000), v3 mean 254.7/255, over a 478x10 sample at f10; only 30 of
4780 sampled foam-channel pixels differ between base and v3. The rendered
frames show only sparse single-pixel differences there (a 24x-amplified
difference at f10 shows roughly 20 isolated pixel ticks). The displacement
resamples foam that is already ~= 1000, so foam_d ~= foam.

3. Temporal character. Time-vertical strips through the band show the variant's
texture breaking up slightly more frame-to-frame than the baseline's rigid
sweep, but at full-frame scale the effect is sub-perceptual. The foam in the
sliver reads as static white foam in both sequences.

4. Artifact screen. No new strobing, no banding, no texture swimming outside
the disc (bit-identical there, verified), no frozen-overlay regression (T2
lower bound satisfied), spire foam rings intact in the far field where
churn_gate = 0 (zoomed views show the spires unchanged), no CG-plastic look
introduced. The dbg foam channel shows no detached rings and no block
structure.

VKB6 verdict: PASS on the artifact screen (no new artifact class of any kind).
Caveat, stated plainly: the displacement does not read as churning water at any
normal viewing scale; it is visually negligible because the disc foreshortens
to a 13 px sliver and the foam there is saturated. The eye review therefore
cannot credit the lever with a realism gain, but it also finds nothing wrong
with the frames. The verdict does not hinge on VKB6.

## Metric-gaming assessment

T1-GC moves by construction only if the displacement changes the foam mask
inside the metric region. Here it does not: the foam in the disc is saturated
(mask = 1 in both sequences), and the 204 px-radius metric region is dominated
by non-churned pixels (sky above, near water below, both bit-identical).
Worker 1's verifier reports T1GC_baseline_pm = 572 and T1GC_variant_pm = 572,
identical on all 47 pairs, and D1_f10_region_diff_pm = 0. The T1-GC validation
gate passes (572 within 580 +- 25), and T3 validates (baseline f0/f47 =
1608/1543 against frozen 1607/1543), so the verifier itself is sane; the zero
is an honest measurement, not a gamed one. The D1 diagnostic correctly flagged
the problem (FAIL at 0 < 5 percent). No metric gaming detected. The failure is
substantive: foreshortening plus foam saturation, not procedure.

## Spot checks

VKB1 (byte-identity): RENDER_SHA c654ebe4ba3a96361324fdcf362324da30ef857feed4a60202d07d4e00d3827c
matches the independently computed sha256 of ocean_dvid1_v3.zag. 7 of 7 sampled
frames match MANIFEST_V3_SHA256.txt via system sha256sum (r1: f00, f17, f33,
f47; r2: f05, f29, f44). The full three-render claim is Worker 1's; the spot
check passes.

Outside-disc identity: 0 differing pixels outside the churn band on f10, f24,
f40 samples (independent check; the verifier reports
OUTSIDE_DISC_DIFF_PIXELS = 0). PASS.

VKB2 (metric bars): T1-GC 572 vs 572, bar requires T1v_pm * 1000 >= T1b_pm *
1300 (572000 >= 743600): FAIL. T2 range [859, 1075] inside [50, 1500] on all 47
pairs: PASS. T3 within 5 percent on f0 and f47 with validation gate passing:
PASS. VKB2 overall: FAIL on the T1-GC bar.

VKB3 (tell list): no tell worse on any of the five items (see the artifact
screen above; VRES_variant_ok = 48 in the verify log). PASS.

VKB4 (cost): all three 48-frame renders completed rc = 0 inside the wave
budget (baseline 48 frames in ~94 s; variant renders finished by 09:59). The
per-frame <= 2x ratio was not independently timed; no red flags.

VKB5 (clean build): no .py files anywhere in the run dir; no "python" token in
build/render/verify logs or hashes (the only mentions are historical, in
JUDGE_BRIEF.md, which was not read beyond a token grep for this check); no
rand/random/srand/time/clock tokens in ocean_dvid1_v3.zag, v3_verify.zag, or
v3_sha.zag; zero Python contact with any new wave artifact. PASS on all
checkable components. The pinned compiler hash is as frozen in the prereg and
was not independently re-verified.

## Confounds and notes

1. Design confound for any future disc-foam lever: the vortex sits at wz ~= 720
and foreshortens to ~13 px vertically, while the foam there is saturated. A
screen-space foam-boil metric cannot resolve churn in that geometry; the metric
region (204 px radius) is dominated by pixels the lever cannot touch. Any
revival of this lever family needs a nearer vortex, an unsaturated foam
regime, or a metric that operates in world space.

2. Worker 1's foam_dbg dumps cover only f00, f10, f23, f47 (4 of 48 frames).
Adequate for the channel check performed here.

3. During this session the newest run-dir files intermittently disappeared
across exec invocations (readdir showed them, immediate open failed); every
read used here was performed inside a single invocation and cross-checked with
hashes. No evidence of tampering; treated as a sandbox filesystem quirk and
noted for the record.

4. JUDGE_BRIEF.md exists in the run dir; per instructions it was not read
(beyond the single token grep for the VKB5 Python check). No sealed mapping
was touched. No sealed pair should be prepared: the verdict mapping below does
not reach READY-FOR-JUDGE.

## Independent recommendation

DEAD [NEW], with the killing evidence logged, per the frozen verdict mapping
(G-LIVE passes and VKB2 fails).

Killing evidence: T1GC_variant_pm = 572 against T1GC_baseline_pm = 572 (ratio
1.000, frozen bar >= 1.300); D1 diagnostic 0 percent (needs >= 5 percent);
foam saturated in the churned sliver (foam-channel mean 253.9/255 baseline,
254.7/255 variant; 30 of 4780 sampled pixels differ); churn screen footprint
only ~13 px tall (x ~419..1016, y 395..408) from foreshortening at wz ~= 720.
The mechanism is genuinely new and correctly implemented, the evidence is
clean (no Python contact, byte-identical determinism spot-checked, outside-disc
identity holds), and the eye finds no new artifacts: this is an honest lever
that fails on its own frozen bar, not a compromised wave. UNVERIFIABLE does not
apply (G-LIVE passes, validation gates pass, evidence uncompromised).
READY-FOR-JUDGE is not reached; no sealed pair is prepared.
