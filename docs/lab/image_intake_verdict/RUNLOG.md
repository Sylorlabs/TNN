# RUNLOG — image intake fidelity (2026-09-26)

## Setup
- Repo: worktree `~/workspace/wt_intake` on `origin/tnn-native-lab` (was 1de59c334 at commit time).
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
- Fixture: `docs/lab/image-repro/original_512.bmp` — sealed Albi photo,
  SHA-256 `4ee3414bddd289ca7c9544a91ec39b8885f8dcde96fa0ffa0d56aebc38da1b00`
  (matches the zoom fork's committed fixture SHA).
- CWD-relative @import: all builds run from this dir so `./common.zag` →
  `./R33_NATIVE_IO_V1.zag` resolves.

## Intake survey
`git grep 'pix[p] = fbuf[q + 2]'` and `git grep 'fbuf[0] != 66'` over
`origin/tnn-native-lab -- '*.zag'`: exactly 6 hits, all in the image program
(`image-repro/repro.zag`, `image_exact_work/v0..v3/ingest.zag`,
`image_zoom_fork/ingest.zag`). One intake idiom, shared verbatim.

## Probe build
`./build.sh` → `intake_probe` (native binary, built 2026-09-26 16:42 PDT).

## Measurements (see evidence/measure.log)
1. `intake_probe albi_original.bmp rt1.bmp` → held 512x187 npix=95744
   fnv1a=-5213046547628462979
2. `intake_probe albi_original.bmp rt2.bmp` → same fnv1a; rt1/rt2/input all
   SHA `4ee3414b…b00` — bit-exact, deterministic ×2.
3. `circles.bmp` (Python-generated: white ring r=60 @ (140,93), filled red disc
   r=40 @ (360,93), green concentric rings r=25/38 @ (260,40), blue disc r=28 @
   (420,150) w/ subpixel edge, gray bg; generator: `circles_gen.py`) →
   `circ_rt.bmp` SHA-identical to input; pixel bytes 287232/287232 equal.
4. `odd.bmp` (511×199, stride 1536 with padding, deterministic pattern + ring;
   generator: `odd_gen.py`) → `odd_rt.bmp` SHA-identical to input.

## Faceting attribution runs
- v0/v1 ingests (from `image_exact_work`, import path adjusted to `./common.zag`,
  machinery untouched) on `circles.bmp`: v0 → 1 leaf (threshold-correct,
  verified by recomputation: vmax=7.087e12 < thresh·nn²=1.833e13; Albi splits at
  4.132e13 → 1,849 leaves), v1 → 368 straight edge segments.
- Zoom fork `ingest_bin` on `circles.bmp`: leaves 1, edges 368,
  zoom motifs L0/L1/L2 = 94/4/1, residuals 71,321/95,744 px.
- Albi arch crops from the zoom fork's committed run artifacts
  (`~/workspace/image_zoom_fork/run/`: renderA/B SHA-verified against the
  fork's VERDICT.md evidence SHAs).

## Numbers cited in VERDICT.md
- Intake ring pixels: r = 60.02 ± 0.41 (rasterization, not faceting).
- v1 red-disc outline: 316 px at r = 39.83 ± 0.54 (interior's 5,025 px erased).
- Arch apex sagitta (40 px span): orig 4.20 px vs understanding 4.45 px —
  dome depth preserved; faceting is in the chord-segmented arch *sides*.
