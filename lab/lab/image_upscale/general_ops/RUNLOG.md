# RUNLOG — Crew C: TNN General Image Operator (azops)

Date: 2026-09-27. Preregistration: `OPS_PREREG.md` (frozen before any official run).
Driver: `src/azops.zag` + modules `src/opgen.zag` (UPSCALE-2X unit) +
`src/opfill.zag` (EDIT-FILL unit). All pure Zag, zero RNG.

## Build

- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
  (`znc 2026.07.0-dev (edition 2026)`), built from `src/` (cwd-relative imports).
- Binary: `/tmp/azops_ops`, SHA-256
  `a422fcf95031119a1e80627ab3a2eed653300b5f61fa23bcbf75560e5de812e3`
  (461,039 bytes; deleted after the gallery was built, per repo rules).
- Build warnings only (15 analyzer notes): 3 false-positive A0101 off-by-one
  lints (index math verified bounded) + 12 A0102 ignored-return-value notes.
  No errors.
- Fidelity proof: the ported matcher reproduces azgen's own sky run
  byte-for-byte in behavior — on `generation/run_sky_1/input.bmp` (384×256)
  this driver records `SHAPES: G=8594117 N=294912 takes=24 nofits=84` /
  `LINES: G=2565616 N=13260 takes=1105`, exactly azgen's `out_sky_3` figures.

## Fixture preparation (scratch only, deterministic)

- `indir/vocab.bin`: copy of `generation/teach_out/vocab.bin` (1,958,448 bytes).
- `indir/sky_768x512.bmp`: copy of `generation/run_sky_1/gt.bmp` (held-out real photo).
- `indir/sky_crop96x64.bmp`: PIL crop of GT at (192,128)+384×256, then two
  PIL BOX 2× downscales → 96×64. (Downscale is fixture prep, not generation.)
- `indir/sky_crop_gt_384x256.bmp`: the 384×256 GT crop, for scoring only.

## Official runs (each run twice; all outputs SHA-compared)

| Case | Input | Goal | TNN choice | Reason (trace) | Outputs SHA-256 |
|---|---|---|---|---|---|
| A | sky_crop96x64.bmp (96×64) | "upscale it four times" | **UPSCALE-4X** | upscale-hits 2 > edit-hits 0, four/4x factor word | trace `d8a4de43…`, 4x `a01f64a4…`, stage1 `427bb3c3…`, labels `2a45376f…` |
| B | sky_768x512.bmp (768×512) | "remove the cloud at top left" | **EDIT-FILL**, mask (0,0) 256×256 | edit-hits 1 > upscale-hits 0, position words → zone rect | trace `4ea3a573…`, fill `fb55752f…`, masked `74ecf784…`, labels `988fa5de…` |
| C2 | sky_crop96x64.bmp (96×64) | "make it bigger" | **UPSCALE-2X** | upscale-hits 1 > edit-hits 0, no four-word | trace `62787fc1…`, 2x `427bb3c3…` (= A stage 1, same input+op), labels `b4c8011b…` |
| C3 | sky_crop96x64.bmp (96×64) | "remove the brightest spot" | **EDIT-FILL**, mask (0,16) 48×48 | edit-hits 1 > upscale-hits 0, brightest 16×16 measured at (16,40) | trace `dfb32297…`, fill `033d0a42…`, masked `a3fddebc…`, labels `15c97338…` |

- Determinism: every file byte-identical across the two runs of each case
  (16/16 identical). Cross-check: C2's 2× output SHA equals A's stage-1 SHA
  (`427bb3c3…`) — same input through the same learned pass gives the same
  bytes regardless of the goal words, as it must.
- Operation-choice score: 2/2 (C2 → UPSCALE-2X, C3 → EDIT-FILL), traces differ
  sensibly (see `OPS_TRACE.txt` in each outdir; gallery embeds them).

## Scores (GT exists only for Case A)

| | PSNR | SSIM |
|---|---|---|
| TNN UPSCALE-4X (96×64 → 384×256), `generation/src/metrics.py` vs GT crop | **24.14 dB** | **0.6088** |
| PIL BICUBIC 4× baseline (same input, not a generation path) | 36.32 dB | 0.9262 |

Bicubic wins by ~12 dB on this smooth-sky crop — the same honest pattern as
azgen's 2× results (sky: TNN 22.75 vs bicubic 33.20). No dB is claimed for any
edit; edits are eyes-only.

## What the traces show (mechanism, measured)

- Case A: both 2× stages REVERTED the SHAPES layer (G=0, takes=0 — no learned
  shape passed the 9/value bar on this crop) and COMMITTED LINES (74 takes in
  stage 1, 698 in stage 2). Labels stage 2: 0(known)=24576, 2(lines)=5446,
  3(shapes)=0, 4(invented)=0, 6(no-fit block-mean)=68282.
- Case B: 1024 cells — tier1=63 (atom-taken 8), tier2=961 (atom-taken 0),
  tier3=0. Labels: 7(atom-fill)=512 px, 8(mean-fill)=65024 px. On smooth sky the
  NULL atom wins the key-SSD almost everywhere: the bar is doing its job, so
  the fill is honestly mostly measured means.
- Case C3: 36 cells — tier1=11 (atom-taken 3), tier2=25 (atom-taken 0).

## Visible failures (stated plainly)

1. **Case C3 fill artifact (bad choice by the matcher, kept visible):** the
   three tier-1 cells at the mask's top row took learned atom 27
   (gains 6721/31323/5966 vs bar 1728 — the ring context genuinely matched).
   Atom 27 is a high-contrast atom (std 40–74, range −134…+107; its cell-area
   deviations average +26/+42/+46, max +88) — a scene-inappropriate texture
   (brownish/reddish with a white block) pasted into blue sky. This is the
   known key-ambiguity failure (low-resolution keys select scene-inappropriate
   textures), now visible in the edit path. The driver behaved correctly; the
   discipline-0 matcher is the weak link — exactly what the sibling crew's
   matcher replaces via `cfg[0]`.
2. **Case A 4× is visibly blocky:** with SHAPES reverted, most pixels are
   measured 8×8 block means (label 6) plus LINES dots; the second 2× pass
   amplifies the stage-1 block structure. 24.14 dB / 0.6088, far under bicubic.
3. **Case B fill is flat with a slight seam:** the cloud streak is gone and the
   color matches surrounding sky, but the 256×256 region is visibly smoother
   than its surroundings (mostly label-8 mean fills) with a faint boundary at
   the mask's lower edge where it meets textured cloud.

## Prohibited-mechanism audit (generation sources)

- `grep -i "bicubic|rand|noise|synth|bresenham"` over `opgen.zag`,
  `opfill.zag`, `azops.zag`: clean. The only hits are a comment stating the
  bicubic baseline was removed, and `tl_walks` (azgen's walk-histogram,
  used only for the SHAPES-vs-LINES ordering affinity — a measurement, not a
  generation path; the LINES construction itself is measured-Sobel + thin
  atoms, no walks/DDA/Bresenham).
- Every constructed pixel in every output is `measured region mean +
  measured learned-atom deviation`, or a measured mean alone (labels 4/6/8);
  label 4 (invented) = 0 px in all upscale outputs.

## Matcher-agnostic separation

All matching flows through `m_shapes_match` / `m_thin_match`
(`src/opgen.zag`) / `m_ring_match` (`src/opfill.zag`), selected by `cfg[0]`
(0 = current key-SSD best-wins; 1 = reserved). The driver (`azops.zag`) never
touches atom internals. A sibling crew's improved matcher drops into the three
functions; `REFUSED` is emitted if `cfg[0] != 0` today.

## Deliverables

- `src/azops.zag`, `src/opgen.zag`, `src/opfill.zag` (+ unchanged
  `R33_NATIVE_IO_V1.zag`, `common_az.zag`, `azlayers.zag`)
- `OPS_PREREG.md` (frozen pre-run), this `RUNLOG.md`
- Gallery: `~/workspace/your_files/tnn_general_ops_NEW.html`
  (self-contained, data URIs, zero external loads — grep-verified)

## Recommended next generalization step

The driver/deliberation/generalization layer works (2/2 choices, honest
traces, byte-identical reruns, matcher-agnostic). The binding constraint is
the discipline-0 matcher's key ambiguity: it leaves SHAPES with nothing above
bar on real content (Case A) and picks scene-inappropriate atoms when it does
fire (Case C3). Priority: the sibling crew's improved matcher behind `cfg[0]=1`,
then re-run these frozen cases unchanged and diff the traces.
