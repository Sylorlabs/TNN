# VERDICT — image intake fidelity (input verdict, 2026-09-26)

**Question:** how faithfully does TNN take in real still images — what bytes go
in vs what TNN's intake holds? And: does the circle→pentagon faceting Micah
observed in the zoom fork enter at INTAKE (held pixels already faceted) or
downstream?

**Verdict: intake is BIT-EXACT. Faceting is 100% downstream — a machinery
ceiling, not a knowledge gap.**

## 1. Intake machinery found

TNN's image intake is a single idiom shared byte-identically by all 6 files in
the image program (verified by grep over `origin/tnn-native-lab`):

| File | Intake |
|---|---|
| `docs/lab/image-repro/repro.zag` (r12) | `pix[p] = fbuf[q+2]` idiom |
| `docs/lab/image_exact_work/v0..v3/ingest.zag` | same idiom, verbatim |
| `docs/lab/image_zoom_fork/ingest.zag` | same idiom, verbatim |

Mechanics (`v3/ingest.zag`, authoritative): raw file bytes via
`nio_read_exact` → parse BMP header (magic `BM`, `bpp==24`, `comp==0`
uncompressed enforced, `off/w/h` read LE) → stride `(w*3+3)/4*4` → copy pixels
BGR bottom-up → **RGB top-down** into the `pix` buffer:

```
pix[p]   = fbuf[q+2];   // R
pix[p+1] = fbuf[q+1];   // G
pix[p+2] = fbuf[q];     // B
```

What intake does **not** do: no color-space conversion (RGB stays RGB, never
YUV/YCbCr), no scaling, no quantization, no gamma, no dithering, no JPEG-style
DCT. It is a pure byte reorder + orientation flip. `pix` is the observation
every downstream layer deliberates over (structure, edges, texture/zoom,
residual all read `pix`).

Boundary: intake only speaks **uncompressed 24-bit BMP**. Anything else
(JPEG/PNG) must be converted before TNN sees it — quantization from such a
conversion would live in the *converter*, outside TNN's intake.

## 2. Fidelity measurements (real stills)

Probe: `intake_probe.zag` (this dir) — runs the intake block VERBATIM from
`v3/ingest.zag`, writes the held `pix` back out via `bmp_write`, prints
dimensions + FNV-1a of the held buffer. Pure Zag, zero RNG. Toolchain
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.

| Test | Input | Result |
|---|---|---|
| Albi fixture (sealed real photo, 512×187) | `original_512.bmp`, SHA `4ee3414b…b00` | round-trip **SHA-identical to input**, 2 runs byte-identical; held-buffer FNV-1a equal across runs |
| Synthetic circles (ring r=60, filled discs r=40/28, concentric rings, 512×187) | `circles.bmp` | **287,232/287,232 pixel bytes identical, 0 differing bytes** |
| Odd geometry (511×199, stride padding, deterministic pattern + ring) | `odd.bmp` | round-trip **SHA-identical** (stride-padding path clean) |

Per-pixel deltas intake vs held: **exactly 0 on all channels, all tests.**
Channel handling: R/G/B copied to R/G/B (BGR file order → RGB held order only).
The intake holds the photograph bit-for-bit.

## 3. Circle-faceting verdict: NOT at intake — downstream

The intake-held pixels of the circles image are the circles, bit-exact
(ring pixels: radius 60.02 ± 0.41 px — the ±0.41 is 512×187 rasterization, not
faceting). The pentagon-with-sides Micah saw enters in the knowledge layers
**after** intake. White-box attribution, each mechanism curvature-blind by
construction:

| Layer | Mechanism (file:fn) | What it does to curves |
|---|---|---|
| L0 structure | `common.zag:deliberate_structure` — axis-aligned quadtree rectangles, mean + axis-planar gradient fit | curves tiled into **rectangular staircase** (visible in `render_struct.bmp`: Albi arch = stack of rectangles) |
| L1 edges | `common.zag:deliberate_edges` — Sobel → direction quantized to **4 codes** → greedy tracing walks `(dx,dy) ∈ {(0,1),(1,0),(1,-1),(1,1)}` → `edge_draw_*` rasterizes **straight Bresenham chords** | curved boundaries stored as chains of straight 4-direction chords → **polygons** |
| L2 texture/zoom | `zoom.zag` — 16×16 / 8×8 / 4×4 square motif blocks stamped | boundaries **block-quantized** to the grid |

Empirical (synthetic circles through the real pipeline):
- v0 structure-only render: 1 quadtree leaf (threshold 2000 tuned for natural
  photos; `vmax=7.09e12 < 1.83e13` → no split, correct behavior) — circles
  absorbed into a single planar gradient, interior detail gone.
- v1 structure+edges render: **368 straight segments**; the filled red disc
  (5,025 px) survives only as a **polygonal outline** (316 px at r=39.83±0.54);
  interiors erased.
- Zoom fork on the circles image: 94 L0 + 4 L1 + 1 L2 motifs; ring preserved
  via edge segments, residual carries 74.4% of pixels.

On the real Albi image: the understanding render's bridge arches are visibly
chord-segmented vs the smooth intake-exact original (arch-apex crop in the
gallery). The **residual layer** (v3 / zoom+residual) then closes the final
render to byte-exact — so the delivered render is exact, but the *understanding*
(the knowledge TNN holds pre-residual) facets curves.

## 4. Knowledge gap or machinery ceiling?

**Machinery ceiling.** No knowledge, deliberation, or motif count within this
vocabulary can represent curvature: the quadtree can only subdivide into
axis-aligned rectangles, the edge tracer can only chain 4-direction straight
segments, motifs are square blocks. More data or more motifs shrinks the error
(the residual proves it) but never produces a curved primitive. The fix is a
vocabulary change — curved primitives (arc/circular segments, radial gradients)
— not more training. This is the same class of finding as the zoom fork's own
boundary note: the deliberation is real, the primitive set is the ceiling.

## Evidence

- `intake_probe.zag` + `build.sh` — rebuilds the probe from the committed
  `common.zag` / `R33_NATIVE_IO_V1.zag` in this dir.
- `evidence/measure.log` — probe outputs + SHAs (Albi ×2, circles, odd-size).
- `SHASUMS.txt` — SHAs of probe, sources, and reference fixture.
- Gallery: `~/workspace/your_files/input_verdict_NEW/image_section.html`
  (self-contained, data URIs) — input vs TNN-held side-by-sides, arch crops,
  circle test.

## Boundary notes

- Intake was measured on uncompressed 24-bit BMP only — the only container the
  intake speaks. A JPEG/PNG intake does not exist in the image program.
- The synthetic-circle v0 run produced 1 leaf: correct per the approved
  threshold-2000 rule (proven by recomputation), which is tuned for natural
  photos, not sparse synthetics.
- The zoom fork's final render (post-residual) is byte-exact; faceting is a
  property of the *understanding* render, which is what Micah's eyes judged.
