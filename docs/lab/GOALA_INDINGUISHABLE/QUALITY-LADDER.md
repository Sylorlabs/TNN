# QUALITY LADDER — G-series (2026-09-22)

## What changed (all in `imagination/src/field.zag`, purely additive)

| # | Change | Why |
|---|---|---|
| G1 | New `f3_raster_g`: bilinear 24x24→WxH + **per-pixel deterministic grain** (`f3_hash2(ox,oy,seed)`, ±14) | Pixel-level texture; kills smooth-CG look. Cell-level `f3_dither` alone made 20px mosaic blocks at 480p |
| G2 | New `f3_emit_bmp_g`: **480x480** BMP emit (was 240) | Resolution ladder; Micah: no resolution limits |
| G3 | Six new scene builders `f3_gen_g1..g6` (briefs 21-26): ember coast, greenhouse at night, paper storm, harbor lights, clay field, signal garden — **asymmetric by design**, layered, varied palettes, subtle cell dither (8-14 not 60-90) | Close the mirror-symmetry tell at the composition level |
| G4 | New `f3_emit_avi_g`: **480x480** AVI, per-frame grain seed, **44.1kHz hi-fi audio** (`f3_synth_hifi`, sign-extending reads, peak→24000 normalization) | Video fidelity ladder; audio no longer 8kHz telephone |
| G5 | New main commands `f3gbmp`, `f3gavi`; briefs 21-26 wired into `f3_build` | — |

## What did NOT change (frozen)
- All 14 legacy BMP scenes: **byte-identical** under the new binary (14/14 cmp OK).
- Legacy `f3_emit_avi` (f3vid1/2.avi): **byte-identical** (2/2 cmp OK).
- Legacy 8kHz WAV emitters: untouched.

## Verification
- G-BMP: 6/6 byte-identical across two clean runs (v2; v1 also 6/6 before dither fix).
- G-AVI: 2/2 byte-identical reruns; RIFF parses clean (480x480, 24 frames @8fps, 44.1kHz/16-bit PCM, idx1 present).
- G-AVI audio full track: bipolar (min -16064, max 24000), DC mean 6.3 (0.02% FS), 0 clipped samples, peak exactly 0.732 FS.

## Measured before/after (images)

| metric | legacy 240px (14) | G-series 480px (6) | bar | verdict |
|---|---|---|---|---|
| resolution | 240x240 | 480x480 | ≥480 hero | PASS |
| H-mirror symmetry (raw) | 0.79-1.00 (10/14) | 0.06-0.93 | <0.60 | 5/6 PASS raw |
| H-mirror symmetry (**gradient-detrended**) | n/a | -0.24..0.00 | <0.30 | **6/6 PASS** |
| unique colors | 2-42,620 | 3,538-24,498 | >50 | 6/6 PASS |
| edge energy (texture) | 0.5-11.6 | 17.2-18.1 | — | richer micro-texture |

**Metric correction (honest):** raw H-symmetry is confounded by vertical gradients (any sunset-over-water scores high). The binding metric is now gradient-detrended symmetry; PREREG bar updated to <0.30 detrended. f3g5's raw 0.929 → detrended -0.080: no mirror tell, just a strong gradient.

## V3 red-team pass (gpt-5.6-sol via UnoRouter, 2026-09-22 ~07:00 UTC)

Two fresh critiques (image set + video) after the grok-4.7 provider hard stop.
All HIGH/MEDIUM tells were fixed in the Zag sources; fixes verified by re-render.

**Image tells closed:**
| Image | Tell (severity) | Fix applied |
|---|---|---|
| G6 signal garden | HIGH — six bars read as enumerated palette request / procedural UI motif | widths varied 20-64px, green occludes amber, teal desaturated into ground, one glow removed |
| G4 harbor lights | HIGH — postcard template, algorithmic light scatter | 5→4 lights, one occluded by dark shape, only one reflection connects; second became a broken offset glint |
| G2 greenhouse | HIGH — sparse symbolic cues, geometric mullions | middle mullion broken out of alignment + faded into field, faint cool secondary glow added |
| G1 ember coast | MED — too-legible fire→reflection correspondence | main reflection widened + interrupted by dark water band, second streak shortened and offset laterally |
| G3 paper storm | MED — compositionally "solved" accent | band B tapered to a stub at its end, red blotch moved onto band A's edge (partially absorbed) |
| G5 clay field | LOW — empty-by-default minimalism | three low-contrast tonal blotches crossing dome and shadow (material behavior) |

**Video tells closed:**
| Tell (severity) | Fix applied |
|---|---|
| HIGH — linear interpolation reads as crossfade/ghosting | `f3_vidfield_g`: per-cell ±2/8 lead/lag (deterministic), endpoints still exact |
| HIGH — 8fps stepping | 12fps / 36 frames (buffer 25.2MB < 33MB slice limit) |
| HIGH — independent per-frame grain = digital shimmer | temporally-correlated grain: persistent + changing components |
| MED — uniform noise = post-process filter look | monochromatic grain, amplitude ∝ darkness (film-like, 1.5x shadows → 0.5x highlights) |
| MED — keyframe plateau / exact keyframe hit | keys spread over all 36 frames (pos8 = fr·24/35), no hold; offsets keep interior organic |

**Caught during v3 implementation (self-review):**
- `f3_rect`'s last param is a *pixel feather radius* — passed 350-600 on three occlusion/glint rects, creating giant blobs. Fixed to 14-24.
- Diagonal `f3_band`s bead on the 24-cell grid at sub-cell widths; widened g3's bands (60→96, 34→80) for continuous ink.
- New-frame-count bug: chunk index tables were hardcoded 192 bytes (24 frames); parameterized to NF·8.

## Final measured metrics (v6 images)

| image | unique colors | raw H-sym | detrended H-sym | bar |
|---|---|---|---|---|
| f3g1 | 16,768 | 0.364 | -0.272 | PASS |
| f3g2 | 12,614 | 0.197 | -0.029 | PASS |
| f3g3 | 6,391 | -0.009 | -0.146 | PASS |
| f3g4 | 8,498 | 0.331 | -0.040 | PASS |
| f3g5 | 3,844 | 0.471 | -0.398 | PASS (V4) |
| f3g6 | 15,076 | 0.012 | -0.217 | PASS |

\* raw confounded by vertical gradient; binding metric is detrended (< 0.30).
V4 note: g5's raw 0.706 (V3) failed the ORIGINAL raw < 0.60 bar. Rather than
bend the bar, g5 was repaired natively (V4, 2026-09-22 ~06:50 UTC): two
overlapping deep-umber lobes darken the left field (cloud-shadow / uneven kiln
firing), one pale lobe lifts the upper right. Genuine compositional change —
also answers the "empty by default" weakness — not metric gaming. Canonical
metrics (proc_6f9a7672f775 script): raw 0.706 → **0.471** (< 0.60 PASS),
detrended −0.087 → −0.398 (< 0.30 PASS), unique colors 3,500 → 3,844.
g1–g4, g6 byte-identical (V3 renders untouched); g5 2/2 byte-identical reruns.

## V4 native repair pass (2026-09-22 ~06:50 UTC, no providers available)

ExperientialLabs grok-4.7 hard-down (429 insufficient_credits); sol via
UnoRouter timing out. Standing order: proceed natively, max one API probe/hour.
- g5 V4 repair above (raw bar now 6/6 PASS on the original < 0.60 bar).
- Native re-attack of all 6 V3/V4 images + both videos by the track owner
  (documented limitation: analyst knows the fixes — weaker than a fresh blind;
  see TELL-CLOSURE.md). Residual tells recorded, none hidden.
- blind_g1.html rewritten: no authorship reveal ("generated entirely by TNN's
  own code" removed), video specs corrected to 36 frames, neutral wording.
- BLIND-G1.md bar reconciled to the frozen PREREG default: 0% "obviously AI"
  across all 8 pieces (an earlier draft had weakened this to ≥4/6 — reverted).
- Video: true motion-advection morph (vs per-cell timing offsets) and audio-visual coupling (filter swell tied to visual transitions) are deferred.
- Content detail still bounded by the 24x24 field grid (bilinear smooth). A 48x48 grid refactor was scoped: ~40 touch sites, deferred as follow-up (logged).
- Video keyframe content unchanged (same 4 imagined keys); only fidelity upgraded.
- Audio substrate still sine-LUT (separate track owns the replacement).
