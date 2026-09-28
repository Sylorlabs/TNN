# Eval harness — diverse held-out set

`eval_all.py` runs generation-vs-bicubic on EVERY image in `MANIFEST.tsv` and
emits a per-image PSNR/SSIM table (TSV).

## Usage

```
cd diverse_set
python3 eval_all.py --binary PATH_TO_GEN_BINARY [--outdir DIR] [--timeout SEC]
```

Options (all with sane defaults relative to this directory):
- `--binary` (required): the generation binary under test. Works with the
  current baseline build AND any fixed variant — just point at the other path.
- `--outdir` (default: `diverse_set/results`): per-image `run_<stem>/` dirs
  (each with `in/` and `out/`) plus `RESULTS.tsv`.
- `--metrics` (default: `../generation/src/metrics.py`): the frozen scorer.
- `--vocab` (default: `../generation/teach_out/vocab.bin`): shared vocabulary
  copied into each indir (the binary must read `vocab.bin` from indir).
- `--timeout` (default: 1200s per image).

## Binary contract

The binary is invoked as `<binary> <indir> <outdir_run>` and must:
- read `indir/input.bmp`, `indir/vocab.bin`, `indir/gt.bmp`
- write `outdir_run/upscale_gen.bmp` and `outdir_run/upscale_bicubic.bmp`
  (both 2x of input = the sealed 768px GT size)

Anything else it writes (trace files, labelmaps) is ignored.

## Pipeline per image

1. Decode the sealed JPEG (768px wide) → GT RGB array.
2. **Odd-height rule (documented):** if the GT height is odd, the last row is
   dropped (768x511 → 768x510). All photos are 768px wide and even-height
   after this step.
3. `gt.bmp` = 24-bit BMP of the GT. `input.bmp` = 2x2 box average,
   round-half-up `(a+b+c+d+2)//4` per channel — the sealed pipeline
   convention (RUNLOG.md: "2x2 box, round-half-up").
4. Binary runs; outputs scored with the frozen `metrics.py` (PSNR = mean of
   per-channel dB; SSIM = Gaussian-window per-channel mean).
5. One row appended to `RESULTS.tsv`: filename, category, gt_w, gt_h,
   gen_psnr_db, gen_ssim, bicubic_psnr_db, bicubic_ssim.

The harness is resume-safe: images already present in `RESULTS.tsv` are
skipped (re-run with a fresh `--outdir` to redo everything). It exits
non-zero if any image fails; successful rows are still recorded.

`results/run_<stem>/` dirs are regenerable scratch (reproduced by re-running);
`RESULTS.tsv` is the verdict evidence.

## Baseline reference (current binary, 2026-09-27)

Binary: `azgen.zag` built with the pinned toolchain
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
(built for harness testing; see the fixing crew for the variant under test).

| Image | Category | Generation PSNR | Generation SSIM | Bicubic PSNR | Bicubic SSIM |
|---|---|---|---|---|---|
| fabric.jpg | texture | 21.47 dB | 0.3662 | 26.73 dB | 0.6588 |
| woodgrain.jpg | texture | 18.37 dB | 0.5408 | 25.51 dB | 0.9065 |
| treebark.jpg | texture | 18.94 dB | 0.5375 | 27.97 dB | 0.9287 |
| calmwaters.jpg | smooth | 19.46 dB | 0.6327 | 22.06 dB | 0.7532 |
| portrait.jpg | people | 21.19 dB | 0.4391 | 27.46 dB | 0.6767 |
| car.jpg | object | 22.92 dB | 0.6698 | 32.44 dB | 0.9178 |
| building.jpg | object | 14.96 dB | 0.2675 | 16.29 dB | 0.3187 |
| cat.jpg | animal | 16.60 dB | 0.3594 | 20.15 dB | 0.5626 |
| market.jpg | mixed | 18.36 dB | 0.4343 | 22.92 dB | 0.7812 |

Generation loses to bicubic on all 9 — consistent with the bridge/sky verdict
in `../generation/HONEST_RESULT.md` (cross-image atoms hallucinate
scene-inappropriate textures; MSE punishes sharp-but-wrong more than
blurry-but-close). Full run took ~133s for all 9.
