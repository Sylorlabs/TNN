# Fork B — Final Report: ONE UNIFIED TNN ACT (D-IMG-1)

Date: 2026-09-22. Branch: tnn-native-lab. Pure Zag, zero external build tools.

## The redirect

Micah's correction killed the separate-world-model-feeding-a-renderer
pipeline as traditionalist (separate modules wired together). Fork B
was rebuilt as ONE UNIFIED TNN ACT: deliberation and depiction
interleaved in a single trace — the same reasoning that conceives the
world also paints it. No WORLD_MODEL.md (deleted, never committed);
the deliberation lives inside `r8b_alien.zag` as trace steps T0..T12,
and `UNIFIED_TRACE.md` is the single human-readable trace — not a
world-model doc. Kept: above-pixel-level ambition (worlds with
geology/history/intent, never noise-on-shapes) and causal light
(deliberate the sun, derive the light — reasoned, never forced).

## What the trace does (T0..T12)

- T0: one deterministic integer-hash noise substrate, no RNG.
- T1: conceive the star (K2V, amber, 1.1° disc) → the one sun vector
  every shadow marches toward.
- T2: the star implies the sky (dusty violet-rose, azimuth-dependent
  horizon); the sun's disc drawn IN the frame as the honesty anchor.
- T3: the moon Cinder — analytic sphere, phase computed from the same
  sun, never painted.
- T4: the ground — volcanic highland, shield massif, rift valley,
  three real-geometry impact craters.
- T5: depiction checks deliberation — detail fades with distance,
  strata only in 3D on steeps (no contour rings).
- T6: rubble smooth-blended INTO the distance field — one surface,
  stickers impossible by construction.
- T7: seeing as occlusion — SDF raymarch, soft shadows as secondary
  marches toward the T1 sun, AO from the field.
- T8: albedo is geology (basalt/dust/strata), aerial perspective.
- T9: the eye — 16:40 local, rift scarp, WNW at the massif.
- T10: smoke test caught 255x-too-strong dither → corrected.
- T11: smoke test caught the moon as a black blob above frame →
  repositioned, planetshine lifted, sky fill raised.
- T12: 1024 render caught the moon STILL a featureless black disc
  (~1% lit at 12° elongation — the trace's own claim of "a thin
  crescent" was contradicted by the depiction) → reconceived Cinder's
  orbit to ~44° elongation (young crescent, ~14% lit) and strengthened
  planetshine. Depiction judged deliberation; the trace records it.
- T13: oracle verdict (Micah's eyes) — the image reads human-made
  (watercolor, not-AI-smell PASS) BUT the moon "is a random black
  dot". T12's crescent was pixel-measurable yet eye-invisible at
  display size: the methodological fix is that depiction must judge
  deliberation AT DISPLAY SIZE. Reconceived: ~52° elongation (bold
  crescent, ~19% lit), larger disc (r=80), planetshine ~2.2x — moon
  only, style untouched. Acceptance checked at 256px: unambiguously a
  crescent moon.
- T13b: oracle verdict (other humans' eyes) — AI, "because the
  mountains cut off weirdly": ridge silhouettes sliced mid-stroke by
  the frame edges. Fix: deliberate lateral taper in the height field
  (past the near ground; view axis derived from the T9 camera), so
  relief eases to smooth hazy lowland before the border. Checked at
  256px: no landform cut mid-stroke at either edge; center untouched.

## Mechanical bars (all recorded, exact)

| Bar | Result | Evidence |
|---|---|---|
| D-RES | PASS | 1024x1024 BMP, 3,145,782 bytes |
| D-SHARP | PASS | grad(O)=2.414, grad(B)=0.875, ratio=2.759 ≥ 1.20 (re-verified after T13/T13b) |
| D-COMP | PASS | zero banned primitive tokens in r8b_alien.zag code (grep audit; the shared verify_bars.py flags var1_terminus.zag, another crew's file — not Fork B) |
| D-DET | PASS | two independent clean 1024² renders byte-identical: SHA-256 `3829e21610cd9f3d35defe77fad3fae8aaecdc132a42b8291a66550237ffaefc` (re-verified after T13/T13b) |
| Trace-only restructure check | PASS | post-restructure 256² smoke was byte-identical to pre-restructure (37d1fce3…), proving the T0..T12 reorganization changed zero behavior |

Build: pinned znc `znc_linux_x86_64_abed8aa1`, `--no-zagd --no-analyze`,
native binary ~73.6 KB, 0 external tools. Compiled binary, .zagd and
cache files NOT committed.

## Deliverables (committed)

- `imagination_discovery/img/r8b_alien.zag` — the single unified trace
- `imagination_discovery/img/r8b_alien_1024.bmp` — canonical output
- `imagination_discovery/img/r8b_alien_1024.png` — preview
- `imagination_discovery/img/UNIFIED_TRACE.md` — the one trace doc
- `imagination_discovery/img/FORKB_UNIFIED_REPORT.md` — this file

## Open / not done here

Blind judging ("would not guess AI / unsure") is NOT run from this
crew — separate fresh judges follow per protocol. Sol/Grok-4.7 opinion
gathering is handled elsewhere. The moon crescent is now legible and
honest; whether the whole image reads as imagined is for the blind
gate to decide.

## Trace-integrity corrections (2026-09-22, Test 4)

Per TRACE_INTEGRITY_RESULT.md (10/13 bars hold), three T2/T9 claims in
the trace above are STRUCK from the architecture evidence and one is
qualified. The mechanisms stand; the claims were wrong:

- T2 "sun's disc IN the frame" — false (ndcx = −1.29, disc out of
  frame; only the glow is in-frame).
- T9 "near rubble sharpest in frame" — false as stated (massif
  2.73 > foreground 2.32); D-SHARP (2.759 ≥ 1.20) still holds.
- T2 "faint stars near zenith only" — the "only" is false (6,845
  star-like points elsewhere in the sky).
- T3/T13 "~19% lit" — qualified: 19.3% geometrically lit, thin dim
  crescent, not 19% bright pixels.
