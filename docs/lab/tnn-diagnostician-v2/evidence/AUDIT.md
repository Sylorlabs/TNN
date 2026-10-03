# Generation-vs-Drawing Audit — TNN construction lines

**Order:** Micah 2026-09-26 ~15:04 PDT. Standing law adopted: **TNN must GENERATE, not DRAW.**
**Trigger:** the pig-front "realistic renderer" was caught drawing — `pf_fur_ellipse` /
`pf_fur_rect` stamp crew-designed feathered ellipses with radial+vertical shading and
hash grain. A current AI image generator built on drawings would look horrible; TNN's
construction must come from its own understanding, not procedural primitives.
**Scope:** audit the other lines' construction paths at the code level. No rebuilds —
investigation with measured findings.

## The test

For each line: trace every output byte back to its source. If bytes come from a
crew-designed primitive (ellipse rasterizer, Bresenham chord, cosine oscillator,
bicubic kernel), that portion is DRAWING. If bytes are measured from observation and
re-emitted through a learned decomposition, that portion is RECONSTRUCTION. If bytes
are produced from the model's learned knowledge of the world (never observed in this
input), that portion is GENERATION. Collage (rearranging observed bytes) is neither.

## Per-line verdicts

| Line | Verdict | Drawing primitives found | What's missing for generation | Smallest honest next step |
|---|---|---|---|---|
| Image upscale (`azupscale.zag`, f67e9893) | MIXED — measured vocabulary, crew-designed render ops | `tl_chord_paint`/`tl_bres_list` (azlayers.zag:1034,1064): Bresenham-rasterized chords for LINES; `bicubic2x` (azupscale.zag:453) for NO-FIT; 50/50 nearest/bilinear blend (azupscale.zag:294) | No pixel is ever synthesized from world-knowledge: every output byte is a deterministic function of observed bytes (re-sampled atoms, re-arranged). Outpaint (azoutpaint.zag:189) just repeats the edge column's mean+atom — no model of what lies beyond the frame | Replace the LINES chord rasterizer with atom-based rendering (thin measured atoms); then teach the SHAPES vocabulary from a multi-image corpus and test 2x prediction on a held-out image — the first true generation-from-learned-knowledge test |
| Image production (`docs/lab/image_production/`, adaptive layers) | RECONSTRUCTION — not drawing, not generating | One drawing-ish element: LINES segments re-rasterized via Bresenham (`tl_lines_render`, azlayers.zag:1219). Everything else: SMOOTH CART leaf means (`tl_smooth_render`, azlayers.zag:968) + SHAPES mean+measured-atom (`tl_shapes_render`, azlayers.zag:1581), atoms built by farthest-point exemplars from the image itself (`tl_vocab_from_rects`, azlayers.zag:1473) | This line was never an imagination line — its contract is understanding + exact closure (residual channel carries the true bytes). It has no pixel synthesis at all and its atoms are per-image, so it cannot emit anything it hasn't seen | Nothing needed for its stated job. For generation: a shared cross-image atom vocabulary experiment — render a novel image's regions from the shared vocabulary with no residual, measure the gap |
| Audio planner/vocabulary (`planner_vocab/src/plan_main.zag`) | DRAW — with oscillators | `render_plan` (plan_main.zag:330): single cosine carrier `s = 0.25*cosr(phase - pi/2)` — ONE partial, no harmonics; FM vibrato LFOs, per-period jitter via `fmix32` hash, exponential envelope, 10ms fades. Vocabulary atoms are oscillator presets (`VOCAB.md`: "vib1 single sine FM", "contour 16-pt"). Sibling `render_act.zag:124` (`render_ep`) is the same family | The entire waveform family is sine-derived — oscillators + FM + envelopes are all on Micah's synth ban list. The phase-3 semantic model (harmonic hum with per-period amplitude + textured body + transient events) exists in the understanding line, but the planner cannot render through it — its "grown vocabulary" grows oscillator presets, not timbres | Port the phase-3 decomposition into the planner's render path: atoms become (harmonic stack, per-period amplitude, texture, transients) measured from real audio, replacing the cosine. Then the growth loop grows timbres instead of presets — the bridge from drawing-with-oscillators to generating-with-learned-sound |
| Video (`forkb.zag` render path; `composer.zag` imagination) | COLLAGE — neither drawing nor generating | No procedural pixel primitives found. `render_round` (forkb.zag:1560): copy recipient frame → `warp_graft` (forkb.zag:688, affine warp of observed donor pixels) → `composite` (forkb.zag:775, paste with feather). `execute_plan` (composer.zag:1049): `rect_copy` paste, `scale_nn` paste, split-screen, alternate frames, crossfade — every output pixel is an observed pixel, only rearranged | Not a single pixel is synthesized from understanding. The deliberation (which arrangement) is intelligent; the render is dumb rearrangement. There is no frame synthesizer — no imagined water, fur, motion, or texture | One synthesis primitive with white-box provenance: motion-compensated frame interpolation where intermediate pixels are generated from measured motion (not blended), judged by TNN's own perception for continuity. Smallest "novel pixels from understanding" step |

## Mechanism-level notes

**Upscale atoms are genuinely measured, not primitives.** `tl_vocab_from_rects`
(azlayers.zag:1473) builds each scale's vocabulary "ONLY from the full s×s blocks
inside the regions that actually reach that scale (farthest-point exemplars… no
vocabulary is invented without evidence)". The render (`tl_shapes_render`,
azlayers.zag:1581; `shapes_render2x`, azupscale.zag:294) stamps
`pixel = region_mean + atom_deviation`. This is the honest substrate: a learned
decomposition. The drawing lives in the *operators* (Bresenham chords, bicubic,
blend), not the vocabulary.

**Production pipeline pixels trace to measurement + residual.** The knowmap
(`TNNKTLM3`, 17-byte region records: x,y,w,h + scale + atom + mean) is a pure
decomposition of the observed image; `azemit` re-renders with the same functions
(Path A == Path B byte-identical); the 2.7% residual channel carries exact original
bytes. Nothing is invented, nothing is drawn from primitives — but nothing is
generated either.

**Audio is the furthest from the law.** The planner's whole world is one cosine.
Its hearing measures f0/env/CV of sine-derived tones; its vocabulary grows sine
presets; its renders are sine presets. Under the no-synth law this entire line's
*render* side must be replaced — the planning/deliberation machinery is sound, but
it plans in oscillator-land.

**Video has no drawing to remove — and no generation to keep.** Both examined
render paths are pixel-rearrangement of observed frames. The imagination lies
entirely in the deliberation (which donor, which geometry, which family). The gap
is a synthesizer, not a de-drawer.

## Out of scope (separate tracks)

- The 22px head-placement investigation (fable + crew): why taught knowledge only
  moved pig-front error 52px→22px, and what else is missing. Tracked separately
  per Micah's order.
- Whether the production image pipeline *should* become a generation line: its
  contract is understanding + exact closure. The generation law binds imagination
  lines; applying it here is a program decision, not an audit finding.
