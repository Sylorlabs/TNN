# PREREG — LIGHT-FIELD: scene illumination as a construction operator

Wave: wave-20260927-0221pdt (sensory headspace worker).
Written 2026-09-27 BEFORE any implementation or run. Frozen.
Post-result change to any frozen number, rule, or bar below voids the round.

## 1. Mechanism (one new sensory mechanism)

**LIGHT-FIELD**: a global per-channel scene illumination gradient,
estimated once per image from the observed input only, applied
structurally inside the 2x construction.

**Knowledge claim (one sentence):** Real scenes carry a large-scale
illumination gradient (light falls off across the frame); the current
construction renders every SHAPES region from a flat region mean plus
local texture, dropping the scene light, so constructed pixels are
photometrically wrong wherever the gradient is strong; LIGHT-FIELD
re-bases each region's mean onto the measured global light field.

**Why this is a big lever, not a micro-tweak:**
(a) No part of the pipeline models light today: R9 contact occlusion is
geometric, the operators are local (atom texture, local plane, flat
mean). Illumination is the dominant photometric structure of any real
scene, and it is entirely absent. (b) It changes the construction
equation for every SHAPES pixel on every image; it is a new knowledge
structure (a scene-level field), not a blend ratio, threshold, or veto.
(c) It is the photometric counterpart to the geometric occlusion work:
the pipeline learned where things occlude; it has never learned how
things are lit.

## 2. Host and baseline

Host: the r8c honest-upscale build, `docs/lab/image_upscale/src/`
(azupscale.zag + azlayers.zag + common_az.zag + R33_NATIVE_IO_V1.zag),
copied to `docs/lab/image_upscale/light_field/src/`; the variant is
`azupscale_light.zag` (copy plus Section 4 only). The pristine baseline
is rebuilt from the committed sources with the pinned toolchain and is
never modified.

Baseline validity (BAR 0): on the sealed fixture the rebuilt baseline
reproduces the published VERDICT.md numbers (TNN 25.96 dB, bicubic
25.89 dB, each within 0.05 dB) and two reruns are byte-identical
(SHA-256). If BAR 0 fails, the wave reports INCOMPLETE (build pipeline
broken) and scores nothing.

## 3. Frozen light-field estimator

Computed from the observed input image ONLY (w x h, RGB), immediately
after input load, BEFORE the held ground truth is opened (the GT load
sits near the end of main; the estimator call is placed at input load
and the ordering is enforced in code with a comment citing this
prereg). Per channel c in {R,G,B}:

1. Partition into 8x8 blocks (edge blocks may be partial, minimum 1 px).
2. Block median m_i of channel c by insertion sort (deterministic).
   For n values sorted ascending v[0..n-1]: n odd -> v[n/2];
   n even -> (v[n/2 - 1] + v[n/2] + 1) / 2 (round half up).
3. Left half: blocks with center_x < w/2; right half: center_x >= w/2.
   (center_x = x0 + bw/2, integer division.) Same split on y for
   top/bottom halves.
4. meanL_c = round_half_away(sum of left medians, count_left);
   meanR_c likewise. xLc = round_half_away(sum of left center_x,
   count_left); xRc likewise.
5. gx_num_c = meanR_c - meanL_c; gx_den_c = xRc - xLc.
   If count_left == 0 or count_right == 0 or gx_den_c <= 0:
   gx_num_c = 0, gx_den_c = 1. Same construction for gy on the
   top/bottom halves.
6. round_half_away(a, b): b > 0; (a >= 0 ? (2*a + b) / (2*b)
   : (2*a - b) / (2*b)).

The field is never materialized as an image. The six rationals
(gx_num, gx_den, gy_num, gy_den per channel) are written to
UPSCALE_TRACE.txt as a LIGHT_FIELD line. A flat image yields all-zero
gradients; then the variant is bit-identical to the baseline (honest
null, scored as decoration per BAR 1).

Rationale for half-means (recorded, not tuned): a global illumination
field must be coarse by design; it must not chase local structure
(that is the local operators' job). Half-means is O(n), overflow-proof
in i64, deterministic, and robust to texture via the medians.

## 4. Frozen construction change

In `shapes_render2x` only (SHAPES-atom regions). LINES, the NO-FIT
bicubic fallback, the INVENTED fallback, and boundary feathering are
byte-identical to baseline (their renders already follow local light,
or the delta is negligible on thin structures; frozen scope decision).

For region ri with input coords (x0, y0) and the render loop's clamped
dims (bwc, bhc), the output region center is xc = 2*x0 + bwc,
yc = 2*y0 + bhc. For each output pixel (OX, OY):
dx = OX - xc; dy = OY - yc.
delta_c = round_half_away(gx_num_c * dx, 2 * gx_den_c)
        + round_half_away(gy_num_c * dy, 2 * gy_den_c).
The accumulator write becomes acc[p+c] += m_c + e_c + delta_c
(replacing acc[p+c] += m_c + e_c). At the region center the delta is
zero, so fitted values are unchanged; away from the center the
construction rides the scene light instead of a flat mean.

Overflow: |gx_num| <= 255, |dx| <= 2048 -> |product| <= 522240,
denominator >= 2. Safe in i64.

Epistemic labeling is unchanged: the light term is a global measured
field, not a region operator; the trace records the field.

## 5. Frozen battery

Images (both fully supported by the committed binary; no buffer
changes, no JPEG decode, no Python anywhere):
- sealed: the canonical fixture. azprep (pure Zag, committed) builds
  gt_512x184.bmp + input_256x92.bmp from
  docs/lab/image_adaptivelayers/sealed/original_512.bmp
  (SHA-256 4ee3414bddd289ca7c9544a91ec39b8885f8dcde96fa0ffa0d56aebc38da1b00).
- skycrop: rows 0..255 of
  docs/lab/image_upscale/generation/run_sky_1/gt.bmp (a real photo),
  prepared by a new pure-Zag tool azcrop.zag (crop 512x256, then the
  documented 2x2 box downscale to input_256x128.bmp). The crop is
  frozen here because the committed binary's 400 KB GT buffer cannot
  hold the full 768x512 sky GT; the top crop is the gradient-dominant
  part of the frame, which is where the mechanism's claim applies.
  The crop rows are frozen before any run.

Note (provenance, verified 2026-09-27 by byte comparison):
generation/run_bridge_1/gt.bmp is byte-identical to the sealed crop,
so bridge is not a second image and is excluded from the battery.

Per image: baseline runs twice (fresh outdirs), variant runs twice;
SHA-256 of every output compared (all must be identical). Filenames
input_256x92.bmp / gt_512x184.bmp are aliased per indir (bytes
unchanged, verified by SHA-256; documented per run).

Scoring: new pure-Zag tool azdb.zag reads gt + upscale_tnn.bmp (+
labels_raw.bin for the tell metric) and prints integer-exact
per-channel SSE, PSNR per channel and mean (metrics.py convention:
mean of per-channel dB), and the checkerboard tell metric below.
SSIM is omitted (no Zag implementation; the perceptual tells and the
human judge cover the visual side; recorded, not hidden).

dB conversion (frozen): PSNR_c = 10 * log10(65025 * N / SSE_c),
N = pixel count. log10 in Zag by range reduction
(x = m * 2^k, m in [1,2)) plus the atanh series for ln(m)
(7 terms, y = (m-1)/(m+1) <= 1/3) divided by ln(10); log10(2) is the
frozen constant 0.30103. Self-test asserts compiled into azdb
(hand-computed values, no external oracle):
|log10(2) - 0.30103| < 2e-4; |log10(10) - 1| < 2e-4;
PSNR for SSE = N (MSE = 1) in [48.12, 48.14] dB.
If any assert fails the binary refuses to score.

## 6. Frozen bars

- BAR 0 (baseline validity): Section 2. Gate: fail -> INCOMPLETE.
- BAR 1 (no-regression plus earn-keep): over {sealed, skycrop},
  mean Delta-dB (variant minus baseline, full-frame PSNR) >= 0.00,
  AND min Delta-dB >= -0.15 on any single image,
  AND at least one image Delta-dB >= +0.10 (else LIGHT is decoration:
  tested-not-ready, reported as decoration, not shipped).
- BAR 2 (perceptual tells, all checkable in Zag):
  (a) checkerboard: for odd pixels labeled SHAPES (3), mean
  |v(OX,OY) - v(ex,ey)| where (ex,ey) is the even-parity horizontal
  neighbor (always an observed KNOWN pixel): variant <= baseline on
  each image (no new grid);
  (b) label-4 INVENTED count unchanged from baseline (baseline: 0);
  (c) UPSCALE_TRACE.txt carries the LIGHT_FIELD line with six
  rationals, byte-identical across reruns.
- BAR 3 (cost, free lunch): variant wall-clock <= 1.05x baseline per
  image (mean of the two runs; shell date +%s%N around the binary).
  The estimator is one O(n) pass; construction adds one multiply-add
  per SHAPES pixel.
- Determinism: every binary x every image x two runs byte-identical
  (SHA-256 of all outputs). Any mismatch voids that image's scores.

## 7. Void conditions

Any post-freeze change to Sections 3, 4, 5, or 6; any Python anywhere
(glue, analysis, verifiers, harnesses, scratch); GT bytes reaching the
construction (the estimator and construction run before the GT load);
any tuning after scores are seen. Violation -> the round is VOID,
reported as such.

## 8. Judge rule and provenance

Only if the variant is coded, tested, READY, passing BAR 0 through
BAR 3 plus red-team review: prepare a sealed blind A/B pair
(baseline vs variant, randomized, mapping sealed) with JUDGE_BRIEF.md
carrying the provenance header (RENDER_SHA, FIRST_RENDERED_WAVE,
COMPONENT_LINEAGE with prior IDs and JUDGED/QUEUED-UNJUDGED status,
NEW_KNOWLEDGE_CLAIM one sentence). Otherwise report killed or
tested-not-ready with kill evidence. No sealed pair is fabricated.

Provenance: FIRST_RENDERED_WAVE = wave-20260927-0221pdt. Baseline
lineage: r8c honest-upscale (docs/lab/image_upscale/src/). No sealed
blind pair components (R9, C1, C2v3, S11-IMG, C12, S11-AUD, S13, S14,
whirlpool-planform) are touched, re-presented, or decided. No
governance ruling is touched. No foreign lineage
(docs/lab/invention/survival/*.origin-wave.*) is used.

Toolchain: pinned znc at
src/tools/toolchain/znc_linux_x86_64_abed8aa1, SHA-256
498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef,
verified before use. Pure Zag only.
