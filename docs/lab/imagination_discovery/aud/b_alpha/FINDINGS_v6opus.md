# V6 "opus's version" — render notes and measurements

**Status:** rendered 2026-09-23, committed (see commit id in parent report).
**Clip:** `imagination_discovery/aud/b_alpha/clips/b_alpha_kids_1e_f_v6opus.wav`
(NEW — first and only v6 render; do not confuse with the v5 a–e set.)
**Source:** `src/render_v6opus.zag` (pure Zag; Python used only for measurement glue).
**Binary:** `src/render_v6opus` (build artifact, not committed).
**Oracle:** `v6_opus_swarm/DIAGNOSIS.md` — every fix below traces to a
measured mechanism there. opus-5.5 itself was unreachable (ExperientialLabs
credits empty), so this is the coordinator's implementation of opus's
verified fix spec.

## What was built

1. **Bed — no more DJ.** Three layered loops of the only 3 qualified
   textures (tx0 2.00 s / tx1 1.32 s / tx2 2.00 s; rms<600, crest<7.0),
   each looping seamlessly onto itself with a short equal-power loop
   crossfade, at incommensurate effective periods (77175/47187/70560
   samples), each under a slow independent LFO (17.3/23.9/11.7 s,
   0.70±0.30 gain — control-rate Taylor sine, inaudible modulation only).
   No chunk rotation, no crossfade-everywhere, no 3 dB boundary dips.
   Two-pass render measures the composite bed RMS and scales it to
   **−37 dBFS** (~20 dB below foreground; v5 was −48.4 dBFS / 31 dB).
2. **Events — no more digital-zero gaps.** The bed runs continuously under
   everything; atom release is 500 ms (decays into the bed / into each
   other); peak-normalization replaced by class-median reference
   (cls0 13108 / cls1 3836 / cls2 9182 — natural intra-class dynamics).
   The score composes through 30 s: v2's reserved 4th footstep (~27.1 s),
   27.0 s laugh, and 28.6 s call are PLACED; grammar fill runs to 29.2 s;
   two composed tail breaths (28.2 s, 29.0 s) end it. Event selection
   for 0–26.4 s is hash-identical to v5's clip (c) — clean A/B.
3. **Mastering — limiter only on clipping.** The always-on
   `x/(1+0.35|x|)` waveshaper (3.6% THD at peaks) is replaced by a soft
   knee that engages only above 0.95 FS. Below that the path is
   transparent. DC removal, FIXPEAK normalization, 30 ms raised ends kept.

## Verification (all measured on the committed WAV, reproducible)

- **Determinism:** two independent runs → SHA256 identical
  (`22f5f8d8d99a236443daaeab40d3745731146f2f771882e31d2ba4846b8e5314`).
- **Silence structure:** 0 gaps ≥50 ms (v5 clip b: 20); 0.00 s dead head,
  0.01 s dead tail (v5: 0.60 s / 3.40 s); 6.8% of samples below −60 dBFS
  are scattered texture dips, never clustered (v5: 23.7% incl. the tail).
- **Bed continuity:** mean bed RMS −37 dBFS (two-pass measurement);
  quiet windows −39.6…−43.1 dBFS (LFO swing, no pumping rhythm). The only
  large 50 ms-window jumps (20–26 dB) coincide exactly with composed
  event attacks (5.15/7.6/16.15/16.4/20.45/26.95 s) — genuine transients,
  not bed artifacts.
- **Mastering:** `limited_samples=0` — the limiter never engaged, so the
  render carries **zero added THD** by construction. Peak −9.1 dBFS,
  crest 20.4 dB, DC residual −0.04 LSB.
- **Contrast:** foreground (tumble 16–18 s) −23.6 dBFS RMS vs bed −37
  dBFS — inside the 10–20 dB band the v5 crew recommended.

## Not claimed

Whether it sounds good. Micah's ears are the judge; this render awaits
his verdict. If he hears residual looping/DJ-ness, the next knob is the
texture set itself (only 3 of 13 textures qualified — the material is
the binding constraint, not the machinery).
