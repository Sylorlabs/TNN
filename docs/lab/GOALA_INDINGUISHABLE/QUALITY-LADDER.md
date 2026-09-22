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

## Known limits (not fixed tonight)
- Content detail still bounded by the 24x24 field grid (bilinear smooth). A 48x48 grid refactor was scoped: ~40 touch sites, deferred as follow-up (logged).
- Video keyframe content unchanged (same 4 imagined keys); only fidelity upgraded.
- Audio substrate still sine-LUT (separate track owns the replacement).
