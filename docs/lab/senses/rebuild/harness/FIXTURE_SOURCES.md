# Fixture sources — senses rebuild harness (2026-09-21)

Generator: `harness/gen.py`. Deterministic: all draws from splitmix64 streams.
Master seed **20260921**; streams: photo pool=11, primary=100+10·task, noise=200+10·task,
adversarial=300+10·task, fixture index mixed into every draw. Noise is precomputed and
baked into fixture files — no randomness at scoring time.

Photo pool: 170 real photographs from picsum.photos (`seed=tnnsr<i>`, 160×120 JPEG),
cached in `fixtures/_photos/ph000.jpg … ph169.jpg`. Verified: all 170 decode as JPEG.

Per-task batches (primary / noise / adversarial):

| task | primary (n) | photographic vs procedural | adversarial (n) | notes |
|---|---|---|---|---|
| t1 colordisc | 60 | **Procedural, physically realistic.** Uniform sRGB patch pairs in 128×64 .img; distances controlled in CIELAB with full ΔE2000. Photos cannot carry exact graded ΔE distances, so controlled patches are the honest source. Truth boundary: SAME iff ΔE2000 < 2.3 (standard JND). 20 SAME (10 identical, 10 ΔE∈[0.4,1.6]), 40 DIFFERENT graded easy[10,28] / medium[4,10) / hard[2.4,4). | 30 | Pairs straddling the 2.3 boundary (ΔE∈[1.6,2.25] SAME ×15, [2.35,3.2] DIFFERENT ×15). |
| t2 colorconst | 40 | **Photographic + real color math.** 40 distinct photo crops; each rendered under 2 of 3 illuminants (D65 / warm-A / cool-F2) via von-Kries chromatic adaptation (Bradford CAT, sRGB↔XYZ↔LMS). 20 same-photo/different-illuminant → SAME_SURFACE; 20 different-photo → DIFFERENT. | 20 | Trick lighting: extreme blue/red illuminants + 0.55 exposure; 10 same-surface, 10 different. |
| t3 shapetrans | 90 | **Procedural real rasterization + photographic backgrounds.** Circle/triangle/square rasterized with 3×3 supersample anti-aliasing, random rotation, scale 30–44px, translation ±14px, on dimmed (0.45) photo backgrounds; 96×96. 30 per class. | 45 | Heavy transforms: small scale 16–26px, low-contrast gray shapes, full-strength clutter backgrounds, 1/3 with occlusion bar. |
| t4 pitchdisc | 60 | **Procedural harmonic synthesis.** 16kHz int16: two 0.4s tones (f0∈[220,660]Hz, fundamental+0.3·2nd+0.15·3rd, 20ms raised-cosine ramps) + 0.08s gap. 20 SAME, 20 HIGHER, 20 LOWER; differences 0.5%–25%. Truth boundary: SAME iff \|Δf\|/f < 0.5% (pitch JND). | 30 | Near-threshold pairs straddling 0.5% (0.1–0.45% SAME ×12, 0.55–0.9% up/down ×18). |
| t5 timbredisc | 60 | **Procedural harmonic synthesis.** Single 0.8s 440Hz tone; 4 classes by harmonic profile: PURE (sine), BRIGHT (1..8 partials, slow rolloff), DARK (fundamental + weak 2nd), RICH (1..6 moderate). 15 per class. | 30 | Distractor harmonics: BRIGHT with weak fundamental, DARK with extra 3rd, RICH pushed bright, near-PURE with faint 2nd — straddling class boundaries. |
| t6 motiondir | 60 | **Photographic motion.** 8-frame 64×64 clips: a photo window translated 2px/frame in one of 8 compass directions (wrap-around) or static. 4 STILL + 7 per direction. | 30 | Camouflaged: contrast flattened to 25%, 1px/frame displacement. |

Noise variants: same counts as primary (60/40/90/60/60/60). Images/video: per-byte
uniform ±8 from the fixture's noise stream; audio: per-sample ±300 int16. Truth
unchanged from the primary fixture.

Totals: 370 primary + 370 noise + 185 adversarial = **925 fixtures**, each with a
sibling `.truth` file (`truth=<value>` in the INTERFACE.md judgment vocabularies).

No synthetic toy is the primary fixture for any task: color uses real CIELAB/ΔE2000
and von-Kries optics math; shapes use real supersampled rasterization; audio uses
real harmonic synthesis with anti-click envelopes; motion moves real photograph pixels.
