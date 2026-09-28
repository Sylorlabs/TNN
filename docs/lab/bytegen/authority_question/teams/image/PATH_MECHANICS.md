# PATH_MECHANICS — how image natively generates

Team Image, 2026-09-23. All citations verified by direct read of the sources
below. Zero RNG anywhere in any path (deterministic coordinate hashes only).

## Three native image paths

### Path A — field.zag stroke → field → raster → BMP
(`~/workspace/tnn-lab/imagination/src/field.zag`)

**Core loop.** Two phases, both plan-driven:

1. **Stroke application** (`f3_fill` :154, `f3_vgrad` :169, `f3_hgrad` :187,
   `f3_blotch` :205, `f3_band` :234, `f3_rect` :277, `f3_dither` :322).
   Each stroke function does two things in order: **records** the stroke
   via `f3_stroke(ar, op, p1..p8)` (`f3_stroke` :107 — writes op + 8 params
   into the arena's stroke log, words 3..3+n·9, max 64 strokes) and
   **eagerly applies** it into the 24×24×4 field cells (`f3_vcellput` :~123).
   Header law, :12–13: "Rasterization is eager, integer, deterministic.
   No RNG anywhere: texture comes from a deterministic coordinate hash."

2. **Rasterization** (`f3_raster_visual` :1233 — integer bilinear 24×24 →
   W×H×3; `f3_raster_spec` :1282 — audio-energy heat map; `f3_raster_relief`
   :1303 — hillshaded heightfield; `f3_raster_g` :2257 — G-series with
   V3 grain model). Each output pixel is a pure function of the field
   cells plus deterministic coordinate hashes (`f3_hash2` :315). Emitters
   `f3_emit_bmp` :1363 and `f3_emit_bmp_g` :2408 pack rows bottom-up into
   BMP. No normalization, no auto-levels, no global gain — verified by
   read: the pixel emitters copy rows, nothing else.

**What state is carried.** The field cells themselves (24×24×4 visual,
48×48 audio, 24×24 structural). Strokes accumulate into them. Within a
single stroke, `f3_blotch`/`f3_band`/`f3_rect` read a cell back and apply
`f3_blend(old, new, a)` (`f3_blend` :148 — `old + (new-old)*a/1000`,
a∈0..1000): local compositing, an arithmetic operand only (see d_blend
settlement below; the same logic applies).

**What the "plan" is.** The stroke log: op + 8 params per stroke, ≤64
(`f3_stroke` :107, `f3_sop`/`f3_spar` accessors). Because every stroke
records before/with application, the full plan survives generation —
plan-pure replay (re-run the recorded strokes into a fresh arena,
re-rasterize) is always available. Scene generators (`f3_gen_g1`…`g6`
:2398+; briefs :706) are plan authors, not feedback sources.

**Grain subtlety (checked).** `f3_raster_g` :2257 computes a shadow-growing
grain term `gr = (gp+gt)·(384−luma)/256` where `luma` is derived from the
*plan's freshly computed cell values in the same call* — not from the
output pixel buffer. Adaptive, but plan-pure: a function of the plan, not
a measurement of the output. Re-rasterization reproduces it exactly.

### Path B — design canvas painting → BMP
(`~/workspace/tnn-lab/imagination/design/render.zag` → `toolkit.zag`)

**Core loop.** `r_one` (:34) allocates a `W·H·3` canvas (`d_new`, toolkit
:36), dispatches to a screen builder (`scr_library` etc. in screens.zag),
which calls components (`c_card`, `c_button`, …) that call draw ops:
`d_px` :40, `d_fill` :49, `d_rect` :58, `d_blend` :69, `d_rrect` :78,
`d_rrect_blend` :103, `d_shadow` :136, `d_circle` :139, `d_line` :167, `d_text` :228,
then `d_emit_bmp` packs rows bottom-up. Ordered imperative layer painting
onto one carried canvas. No normalization.

**What state is carried.** The canvas pixels — every layer paints over the
accumulated result of earlier layers.

**What the "plan" is.** The ordered op sequence (the screen function's
call tree with literal args). Unlike Path A's stroke log it is not
recorded to a data structure, but it is a fixed, deterministic program —
re-running the screen function over a fresh canvas (or over a sub-region,
replaying all layers in order) reproduces the image bit-exactly.

### Path C — imagination_discovery/img generative fields → BMP
(`~/workspace/tnn-lab/imagination_discovery/img/disc.zag`)

**Core loop.** `d_render_alien` :767 / `d_render_arch` :940: nested y/x
loops, but each pixel is computed by a closed-form evaluator
(`d_alien_px` :753 — sky/planes/fog/planet dispatch; arch: mitered
beam geometry) from **(x, y, w, h, seed) only**, plus a ±3 LSB
deterministic hash dither (`d_h01(x,y,seed+999)` — `d_hash` :101).
Header comment (:17–33): "Composition is GENUINE GENERATIVE: every pixel
is evaluated from continuous fields… Deterministic: integer hash noise,
fixed seeds, no RNG anywhere." This is the **only true-PARALLEL native
image path** (bytegen survey classification): zero carried state —
`pixel = F(plan, x, y)` in the strict sense.

**What state is carried.** None.

**What the "plan" is.** (scene selector, seed, W, H) — passed to main
(:1229). Anyone, in any order, can recompute any pixel.

### Video frames (image-relevant)
`f3_emit_avi_g` :1848 (G-series AVI): per-frame `f3_vidsubject_g(v,fr,NF,far)`
(:1841 — morphs the background field arena, draws subject) →
`f3_raster_g` :2257 → BGR chunk. All plan-pure (fr is an explicit plan
input; grain seed is frozen constant per scene, :1996–2000). **Exception:**
the audio track in this writer is peak-normalized from the *rendered*
mix (`peak` measured, every sample ×24000/peak — read at :1863–1881).
The same output-derived global gain appears in `f3_emit_wav` :1025–1039
(peak→28000), `f3_emit_wav_hifi` :1166–1184 (peak→24000), and the legacy
video writer `f3_emit_avi` :1496–1512 (peak→28000). **No pixel
path does this** — the disease lives in audio emitters, and it is the
gamma.zag lesson in the flesh (see FAULT_ANALYSIS §F3).

---

## d_blend: settled — it is NOT generative feedback

`d_blend` (toolkit.zag :69–77):
```zag
let er:i64 = px[at] as i64; ... // reads the existing pixel
px[at] = ((er*(256-a) + r*a)/256 as i64 & 255) as u8; // pure function of (old,new,a)
```
It is the only native site where generated output bytes are read during
generation (survey FINDINGS.md already flags it). Settlement, five points:

1. **No semantic input.** The bytegen AR criterion requires output bytes
   read as *semantic input* — used to decide later content. `d_blend`
   reads the old pixel only as an arithmetic operand of a fixed formula.
   It never selects which op runs next, never changes a color, alpha,
   coordinate, or layer order, never gates anything.

2. **No measurement, no threshold.** The value participates in no
   predicate. There is no detection, no comparison, no band. Nothing is
   "noticed" about the rendered pixels; alpha `a` is a plan argument.

3. **No carried variable updated from output.** Compare audio Attack 4's
   involution: a servo gain `g ↦ clamp(T/(g·S))` *updated from measured
   output* created 2-cycles and rail pins. `d_blend` has no update step —
   there is no variable that the read-back feeds. The operator is
   pointwise, bounded to [0,255] by clamp, and has no memory across pixels
   (beyond the compositing semantics the plan intends).

4. **The data-flow / control-flow crux.** Authority is about **control
   flow over measured output**: measured bytes choosing content. `d_blend`
   is **data flow**: the old pixel flows into an arithmetic expression
   whose operator and parameters are plan-fixed. Data flow with a
   plan-fixed operator is rendering; control flow over measured output is
   feedback authority. `d_blend` is entirely the former.

5. **Corroboration: `d_get` is dead code.** `d_get` (toolkit.zag :45), the
   pixel-read accessor, is *defined but never called anywhere* in the
   design path (verified by grep over the design tree — only the
   definition site matches). Nothing in the entire canvas pipeline branches
   on a rendered pixel's value. The field path is the same: `f3_vcell`
   reads inside strokes feed only `f3_blend` arithmetic (:148) and
   `f3_dither` addition (:322–341) — never a branch. There is no latent
   feedback controller waiting to be "extended"; there is nothing to
   extend.

**Verdict:** `d_blend` is bounded alpha compositing — a rendering operator
belonging to Piece 1 (plan path), provably not generative feedback, and
not a precedent for feedback authority. Granting it "authority" status
would be a category error: it would license a rendering operator to
masquerade as a controller.
