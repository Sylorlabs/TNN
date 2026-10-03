# GOAL-A TELL-CLOSURE TABLE (2026-09-22, pre-dawn)

Synthesis of Worker 1 (TELLS.md), Worker 2 (HUMANLIKE.md), the sol red-team
critiques, and the G-series implementation. "Closed" = fix implemented in a
shipped artifact AND measured past the bar AND fresh blind re-attack run.

## Image tells

| # | Tell (source) | Status | Evidence / fix |
|---|---|---|---|
| I-T1 | Pervasive H-mirror symmetry, 10/14 legacy at 0.79–1.00 (W1) | CLOSED (G-series) | G v6+V4: raw < 0.60 on **6/6** (g5 V4 0.471, was 0.706); detrended < 0.30 on 6/6. Canonical script (proc_6f9a7672f775). |
| I-T2 | Geometric-primitive vocabulary: nested squares, LED rects, 5-bar visualizer (W1) | CLOSED (G-series) | sol re-critique drove recompositions: occlusion, overlap, width variation, broken alignment (G2/G4/G6 v3) |
| I-T3 | 100% 1px-sharp edges on geometric images (W1) | CLOSED (G-series) | bilinear 24→480 upscale + per-pixel grain; no hard vector edges remain in G set |
| I-T4 | Dead-center composition, 11/14 (W1) | CLOSED (G-series) | all six G briefs asymmetric by design; focal masses off-center |
| I-T5 | Color-count spread 2…42,620; 85–98% values divisible by 8 (W1) | CLOSED (G-series) | G v6: 3,500–16,768 unique colors; grain breaks quantization fingerprint |
| I-T6 | 240×240 icon canvas (W1, PREREG) | CLOSED (G-series) | 480×480 native BMP |
| I-T7 | "Enumerated" compositions — every element cleanly purposeful (sol critique) | CLOSED (G-series) | v3: overlapping/occluded/broken elements; desaturation; faded forms |
| I-T8 | Uniform white grain = post-process filter look (sol video critique, stills apply) | CLOSED (G-series) | V3 grain: monochromatic, luminance-dependent (1.5× shadows → 0.5× highlights) |
| I-T9 | Subject-less noise fields (W1) | OPEN | needs compositional briefs with subjects; G-series are abstract fields by brief |
| I-T10 | Saturation presets 0.0 vs ~0.99 (W1) | OPEN | partially covered by palette discipline; no dedicated fix |
| I-T11 | Focal hierarchy absent; motif development; pentimenti (W2 top-10) | OPEN | W2 first-wave features I-1/I-3/I-4 not yet implemented |

## Video tells

| # | Tell (source) | Status | Evidence / fix |
|---|---|---|---|
| V-T1 | Linear keyframe interpolation = crossfade/ghosting (sol, HIGH) | CLOSED (G-video) | f3_vidfield_g: per-cell ±2/8 deterministic lead/lag; endpoints exact |
| V-T2 | 8fps stepping (sol, HIGH) | CLOSED (G-video) | 12fps / 36 frames; 25.2MB < 33MB slice limit |
| V-T3 | Independent per-frame grain = digital shimmer (sol, HIGH) | CLOSED (G-video) | persistent + temporal grain components |
| V-T4 | No coherent subject — animated static (W1) | OPEN | W1 F10 (persistent silhouette + scene integration) not implemented |
| V-T5 | v2 near-static; unstructured pixel change, no motion path (W1) | OPEN | W1 F11/F12 (eased path, phase structure) not implemented |
| V-T6 | No shot structure / narrative beats (W1, W2 V-1) | OPEN | W2 V-1/V-2 (beat structure, varied easing) not implemented |
| V-T7 | Audio unrelated to visuals (sol, LOW) | OPEN | deferred: filter swell tied to visual transitions |

## Audio tells (tell-hunt only; synth rebuild is the audio track's job)

| # | Tell (source) | Status | Evidence / fix |
|---|---|---|---|
| A-T1 | Exact integer-grid timing, zero rubato (W1) | OPEN | W1 F6 (structured onset timing) specified, not implemented |
| A-T2 | Flat dynamics, CV 0.154 (W1) | OPEN | W1 F7 specified, not implemented |
| A-T3 | Sterile mono, dry, 19.8/31.1 dB separation (W1) | OPEN | W1 F8 specified, not implemented |
| A-T4 | Exact 12-TET, zero drift (W1) | OPEN | W1 F9 (±1.5 cents) specified, not implemented |
| A-T5 | Scale-exercise composition; round-number ±24000 limiter; invariant timbre (W1) | OPEN | compositional/synth-track items |
| A-T6 | No motivic development; no phrasing arcs (W2 top audio cues) | OPEN | W2 A-1/A-2 first-wave, not implemented |

## Blind re-attack status
- CORRECTION (2026-09-22 ~06:50 UTC): no valid external blind re-attack of the
  V3 artifacts completed. Three attempts, all dead:
  (a) the successful sol image critique used a V2-state prompt ("five scattered
  warm lights", "three uniform mullions", "two clean vertical reflections") —
  its FIX list is exactly what V3 implemented, i.e. it was the critique that
  DROVE V3, not a fresh attack on it (archived as
  `raw/sol-critiques/image-critique-v2.md`);
  (b) a proper V3-state blind image re-attack ("wide reflection interrupted by
  a dark water gap", "four scattered warm lights", "green bar overlapping the
  amber one") errored with `choices: null`;
  (c) the video re-attack errored the same way. A bounded retry loop for (b)
  was killed per the no-burn order.
- Native re-attack substituted per standing order (track owner as analyst).
  DOCUMENTED WEAKENING: the analyst knows the fixes and cannot be truly
  blind. Rule applied: a tell the native analyst still spots stays OPEN;
  nothing is closed on native review alone — closure still requires the
  measured bar AND (when providers recover) a fresh external blind.
- Micah blind batch G1 (6 images + 2 videos): preregistered (BLIND-G1.md, bar
  reconciled to the frozen 0%-"obviously AI" default), packet rewritten
  (`your_files/imagination_fields/blind_g1.html` — no authorship reveal,
  correct 36-frame video specs). Awaiting Micah's ratings.

## Native re-attack findings (2026-09-22 ~06:50 UTC, V3+V4 shipped pixels)

Per-image residual tells (adversarial pass by track owner; severities are the
analyst's honest judgment):

| Piece | Residual tell | Severity | Disposition |
|---|---|---|---|
| G1 ember coast | pale horizontal streak left of the fire connects to nothing — reads as artifact or UI remnant | MED | NEW → I-T12 OPEN |
| G1 | fire→reflection correspondence still legible despite V3 interruption | LOW-MED | I-T7 stays CLOSED (improved); note for next wave |
| G2 greenhouse | lamp glow is a perfect radial gradient — generic AI focal marker | MED | NEW → I-T13 OPEN |
| G2 | mullions still straight/geometric; sparse symbolic cues, no real space | MED | I-T2 stays CLOSED for the set; G2 composition noted for next wave |
| G3 paper storm | two bands still near-parallel — compositional formula | LOW-MED | strongest piece; note for next wave |
| G4 harbor lights | left light's long connected reflection still a clean correspondence; water band uniform full-width; top-right occluder blob ambiguous | MED-LOW | I-T7 stays CLOSED; notes for next wave |
| G5 clay field (V4) | asymmetric tonal mass reads as directional light/cloud shadow — clay-plausible; no longer empty-by-default | LOW | I-T1 CLOSED (raw 0.471) |
| G6 signal garden | enumerated bar set persists: bottom-aligned, evenly spaced, equal conceptual weight; V3 varied widths but concept unchanged | MED | I-T2/I-T7 CLOSED for geometry; compositional concept → next wave (W2: motif development) |

Native ranking, most→least human-plausible: **G3 > G5 > G1 > G4 > G2 > G6**.
(G6 remains the weakest — matches the external critique's ranking.)

Video (frames extracted from preview MP4s; motion measured):
- vid1: mean abs frame diff 28.33 — genuine large-scale morph (dark blue field
  → warm orange/pale blue split, wandering horizon). Organic, not static.
- vid2: mean abs frame diff 4.95 — very subtle; first second reads near-frozen
  as faint warm glows emerge from black. NEAR-STATIC OPENING → V-T5 note.
- Both: no subject, no motion path, no beats — pure field morphing. Reads as
  screensaver/wallpaper transition, not authored motion. V-T4, V-T5, V-T6 stay
  OPEN (confirmed, not closed). V-T1/V-T2/V-T3 fixes hold (organic timing,
  12fps, temporally-correlated grain as far as stills show).
- Audio-visual relationship not assessable from frames; V-T7 stays OPEN.

New tell rows:
| # | Tell (source) | Status | Evidence / fix |
|---|---|---|---|
| I-T12 | G1: disconnected pale horizontal streak left of fire (native re-attack) | CLOSED (V5b, 2026-09-22) | Test-both: V5a (remove → haze wisps) and V5b (connect: band broken into two segments with a gap at the fire glow, tapering toward it, asymmetric tilt/offset; fire drawn in front). Shipped V5b — preserves the brief's horizon cue. 6/6 images raw H-sym < 0.60 (g1 0.347), detrended < 0.30 (g1 0.073). Byte-identical 3/3 clean runs (sha256 4ac7de63…). |
| I-T13 | G2: perfect radial-gradient lamp glow = generic focal marker (native re-attack) | CLOSED (2026-09-22) | Two concentric centered blotches replaced: two overlapping offset glow lobes (non-circular) + offset secondary scatter + hot core kept + dark mullion bar drawn AFTER the glow (foreground occlusion; lamp sits behind the frame). Raw H-sym 0.293, detrended 0.034. Byte-identical 3/3 (sha256 5734b305…). |

## V4 subject-video closure (2026-09-22, Goal-A finish crew)

Pure-Zag subject system added to the G-video path (`f3_vidsubject_g` in
`imagination/src/field.zag`; legacy `f3_emit_avi` untouched; 480x480, 36f,
12fps, 44.1kHz; existing `f3_video_audio` kept — V-T7 deferred by design,
audio chunks bit-identical). Normal vision throughout.

| # | Tell | Status | Evidence |
|---|---|---|---|
| V-T4 | No coherent subject — animated static | CLOSED | v1: bird (flapping wings, 8-frame deterministic triangle), 36/36 frames, bbox 19.6–28.8%; v2: lit boat, 36/36 frames, bbox 17.3–47.5%. Integration: ridge/piling occlusion, dawn glow, following reflection, speed-coupled wake/lamp. Template-persistence self-attack: mean MAD 29.0 (v1) / 40.8 (v2) vs 0.00 rigid floor (sanity-checked). |
| V-T5 | v2 near-static; unstructured pixel change, no motion path | CLOSED | Eased velocity profile: hold 0–5, accelerate, cruise, decelerate, settle 32–35. Active mean abs frame diff 6.60 (v1) / 3.18 (v2) — both > 2.0 bar. Temporal raster-grain frozen (constant seed) so frame change is coherent motion, not shimmer (tested both; evidence chose frozen). Coherence: subject-dominated, inside/outside ratios 7.8x–45x (v2). Caveat: v1 has 3 isolated frozen frame pairs (0→1, 6→7, 31→32) from integer morph quantization — 1/12 s each, minor. |
| V-T6 | No shot structure / narrative beats | CLOSED | Establish → move → settle with continuous interpolation. Position-triggered events (not frame numbers): bird swoop + landing descent with wing-fold onto far ridge (s>900), tone ramp to silhouette; boat hesitation zone + piling occlusion. Byte-identical 2/2 renders (fe0d2fb3…, d7aa5f22…); reconciled source re-verified byte-identical by coordinator. |

## Micah redirect (2026-09-22 ~07:46 PDT)

Micah's verdict on the G-series: reads as blurry (480x480 + heavy grain =
fuzzy) and template-driven (placed f3_blotch/f3_band primitives). Orders:
(1) mechanical repairs in flight finished and reported (above); (2) NO
further blind-judging rounds on the old 480x480 series — superseded, judge
budget not spent; (3) high-res rebuild NOT started here — a dedicated
discovery wave is dispatched for the new program ("I discovered some
high-quality alien planet", judged by "would you have guessed AI"; high
resolution and SHARP; no template primitives as the creative ceiling; audio
gets zero forced instruments with full frequency freedom). The V5 image
renders and V4 videos above remain the byte-identical mechanical baseline,
not the new creative bar.

## Residual risks (from W1 blind re-attack, apply to next wave)
- Cross-image hash-residual fingerprint (shared f3_hash2 grain signature across the set).
- Bimodal edge populations; palette-band jitter as anti-quantization evidence.
- Metric-optimized distributions (symmetry/centroid avoiding old ranges = new fingerprint).
- W2 backfire law: uniform application of individually-good features = screensaver.
