# VERDICT — video intake fidelity (2026-09-26)

**Question:** how faithfully does TNN take in real video frames before any
imagination or reasoning? Part of Micah's "how good is input" verdict.

**Verdict: INTAKE IS BIT-EXACT.** Every tested path holds frames byte-for-byte.
Zero lossy points at intake. The only lossy stage in the frame pipeline is the
motif "understanding" render (downstream, honest, residual kept separate).

## 1. Intake machinery found (all in-repo, pure Zag, zero RNG)

| Line | Intake code | Format read |
|---|---|---|
| video-composer step2/3/nobridges | `imagination/video-composer-step2/src/composer.zag` → `read_ppm_gen` (also in `video-fusion-step3/src/composer_base.zag`, `video-composer-nobridges/src/composer_base_head.zag` — all three function bodies **byte-identical**, SHA `304ee68f7508e0f1…`) | raw PPM P6, maxval 255, video `ingest` = fixed 24×320×240, `stillingest` = any W/H ≤ 640×480 |
| image zoom fork | `~/workspace/image_zoom_fork/ingest.zag` (committed as `docs/lab/image_zoom_fork/ingest.zag`, commit `2384090e54cf`) — first ~100 lines | raw 24bpp uncompressed BMP `original_512.bmp`, ≤400k px |

Reader semantics (`read_ppm_gen`): validates magic `P6`, parses W/H/maxval with
exact-integer loops, **requires maxval==255**, skips exactly one whitespace byte
before the raster, requires **exact file size** (`n != p+need` → rc=-32, fails
loud, no silent truncation), then a plain `while (i < need) px[i] = buf[p+i]`
verbatim byte copy into the frame store with provenance (frame,row,episode) +
label. **No quantization, no chroma conversion, no resampling, no scaling**
anywhere in the path. Integrity gates: 1MB whole-file buffer with the
640×480 cap is load-bearing (921,615 bytes max < 1,048,576, so no truncation
possible within the caps); oversized/undersized/malformed PPMs fail with a
negative rc instead of ingesting garbage.

PNG is NOT native: PNGs enter via ffmpeg→PPM pre-conversion (outside Zag,
documented in DESIGN.md). The Zag inflate decoder is explicitly out of scope.
This is an honesty boundary, not a fidelity loss — the PPM that enters is the
measured frame.

## 2. Measurements — real frames, intake path only

Fixture: Big Buck Bunny (Blender Foundation, CC-BY 3.0) reference frames,
`~/workspace/video-repro/source/frames/frame_00..23.ppm`, 24 frames, 320×240,
8 fps, P6 raw. Build: pinned toolchain
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`,
`composer.zag` (mirror-layout build, source unmodified), `ingest bunny` ×2,
`recall` ×2.

| Metric | Result |
|---|---|
| Frames ingested | 24/24, 0 dropped, 0 malformed |
| Frames byte-identical after ingest→store→recall | **24/24** (0 differing bytes, max\|Δ\|=0 per frame, incl. PPM headers) |
| Per-frame PSNR / SSIM | **∞ / 1.0** (byte identity ⇒ vacuous) |
| All-frames SHA-256 (source) | `54436d1c31448f3c7163e71d2a38b2a403d096a67f38164130f778508578c384` |
| All-frames SHA-256 (TNN-held) | `54436d1c…578c384` — **identical** |
| Determinism ×2 | store.bin run1 == run2 (`658b3b91…c00a1c` both); recalls byte-identical |
| Pipeline's own hash chain | H_I (ingest trace) == FNV-1a-64(source raster) == H_R (recall stdout) = `11ea04e02cda202d`, verified independently in Python |

Still path (`stillingest`, 512×187 circle PPM): ingest→recall **byte-identical**,
deterministic ×2.

Image zoom-fork intake (raw BMP): independent run on own circle test image →
`renderA.bmp` (the held frame) **byte-identical** to input
(`652924dea7…4ae544842` both). Corroborated by a separate same-day probe with
different circle geometry (`2da0c6c7…`, also byte-identical).

## 3. Lossy points: none at intake

Every intake path measured holds pixels byte-for-byte. The **only** lossy stage
is the motif "understanding" render — which is downstream of intake, explicitly
the pre-residual understanding curve, and closes to byte-exact through the
honestly-labeled residual channel (19,051 delta pixels / 19.9% on the Albi
fixture; 76.4% on the circle test image, i.e. the render is honestly far from
the input there).

## 4. Circle→pentagon verdict: DOWNSTREAM (motif fitting) owns it. INTAKE EXONERATED.

**Test:** own 512×187 image with smooth anti-aliased circles (white outline
r=48, red filled r=28, blue filled r=18, green outline r=36 on gray) run through
the zoom fork's full intake→understanding pipeline.

- **Held frame (renderA.bmp): byte-identical to input.** TNN's held circles are
  the input's circles, smooth. SHA match, 0 differing bytes.
- **Understanding render:** blue filled circle → **octagon**; white/green
  outlines → visible **chord segments**. Same faceting as observed.

**White-box mechanism (machinery, not knowledge):** `zoom.zag` fits each 16×16
block of (`original − structure`) with the nearest exemplar from its
greedily-fit motif vocabulary (farthest-point, null seed, lowest-index ties;
78 coarse motifs converged on this image). A curve arc crossing a 16×16 block
at an arbitrary phase rarely matches a motif; the winner is a straight-edge or
corner motif, so arcs render as chords — polygon sides. The deliberative
zoom-in to 8×8 only fires where a block's residual energy exceeds 8192; on the
circle test **0 of 0 blocks zoomed**, so the coarse chords stand. This is a
property of the motif-fitting stage (coarse granularity + straight-edge-biased
converged vocabulary + zoom-in gate), not of intake and not a knowledge gap.

## 5. Reproduction

- `intake_measure.py` (this dir): rebuilds `composer.zag` with the pinned
  toolchain (mirror layout; committed source untouched), runs ingest×2 +
  recall×2 on the BBB reference frames, byte-compares all 24 frames, verifies
  the FNV hash chain, prints the table above. Expects `~/workspace/video-repro/source/frames/` present.
- `circle_test.py` (this dir): generates the circle PPM, runs `stillingest`/
  `stillrecall` ×2, byte-compares; and drives the zoom-fork `ingest_bin` on the
  BMP conversion, byte-compares `renderA` to input.

No binaries, no `.zagd`/`.zag-cache`, no stores committed — code + docs +
verdict evidence only, per repo standard.

## Caveats

1. The 24-frame 320×240 fixture is the sealed BBB reference; larger/different
   fixtures would exercise the same `read_ppm_gen` byte-copy loop, but only
   ≤640×480 stills and 320×240 video frames were measured.
2. ffmpeg→PPM pre-conversion (Lanczos downscale, H.264 decode) is outside
   TNN's intake and outside this verdict — measured intake starts at the PPM.
3. The circle test images are synthetic (PIL-drawn), chosen to isolate the
   faceting question; the intake claim on them is byte-identity, not realism.
