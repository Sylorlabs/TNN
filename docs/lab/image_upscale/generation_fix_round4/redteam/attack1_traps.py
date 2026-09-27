#!/usr/bin/env python3
"""ATTACK 1 — category-shift traps (R3 killers, reconstructed analytically).
Three sharp-geometry GTs at 2x-relevant scales, documented construction:
  diagonal_step : 256x256 binary, 255 iff y > x (45-degree sharp diagonal edge)
  circle        : 256x256 binary, 255 inside r=64 of (128,128), 0 outside
  gradient_step : 256x256, horizontal gradient 0..199 with a sharp +55 LSB
                  step at x=128 (discontinuity mid-gradient)
All channels identical RGB. LR = harness box-downscale (a+b+c+d+2)//4.
Runs: pristine baseline (VOC2), P2plane (VOC3), PIL bicubic reference.
Reports PSNR vs GT and P2plane-delta vs bicubic (R3 kill numbers were
diagonal -5.46, circle -6.54, grad+step -7.04 dB for C3).
"""
import numpy as np, os, shutil, sys
from PIL import Image

RT = "/home/hatch/workspace/upscale_r4/redteam_r4"
sys.path.insert(0, RT)
from rt_common import BIN_BASE, BIN_P2, VOC2, VOC3, prep, run_bin, psnr
sys.path.insert(0, "/home/hatch/workspace/selfpam_run/tnn-lab/docs/lab/image_upscale/diverse_set")
from eval_all import write_bmp, downscale_2x2  # noqa

N = 256

def traps():
    yy, xx = np.mgrid[0:N, 0:N]
    diag = np.where(yy > xx, 255, 0).astype(np.uint8)
    circ = np.where((xx - 128) ** 2 + (yy - 128) ** 2 <= 64 ** 2, 255, 0).astype(np.uint8)
    grad = (xx * 199 / 255).astype(np.int32)
    grad = np.where(xx >= 128, np.clip(grad + 55, 0, 255), grad).astype(np.uint8)
    return {"diagonal_step": diag, "circle": circ, "gradient_step": grad}

def rgb(a):
    return np.stack([a, a, a], axis=2)

def pil_bicubic(lr, W, H):
    im = Image.fromarray(lr).resize((W, H), Image.BICUBIC)
    return np.asarray(im)

def main():
    os.chdir(os.path.join(RT, "work", "attack1"))
    rows = []
    for name, gray in traps().items():
        gt = rgb(gray)
        lr = downscale_2x2(gt)
        results = {}
        for cfg, binary, vocab, argv3 in (("baseline", BIN_BASE, VOC2, None),
                                          ("p2plane", BIN_P2, VOC3, "plane")):
            indir, outdir = f"indir_{name}_{cfg}", f"out_{name}_{cfg}"
            shutil.rmtree(indir, ignore_errors=True); shutil.rmtree(outdir, ignore_errors=True)
            os.makedirs(indir)
            write_bmp(os.path.join(indir, "gt.bmp"), gt)
            write_bmp(os.path.join(indir, "input.bmp"), lr)
            shutil.copy(vocab, os.path.join(indir, "vocab.bin"))
            p = run_bin(binary, indir, outdir, argv3)
            assert p.returncode == 0, (name, cfg, p.stderr[-1000:])
            gen = f"{outdir}/upscale_gen.bmp"
            results[cfg] = psnr(os.path.join(indir, "gt.bmp"), gen)
            shutil.rmtree(outdir)
            shutil.rmtree(indir)
        # bicubic reference (PIL 10.2.0, exact LR)
        bic = pil_bicubic(lr, N, N)
        tmpg = f"bic_{name}.bmp"
        write_bmp(tmpg, bic)
        tmpr = f"gt_{name}.bmp"
        write_bmp(tmpr, gt)
        results["bicubic"] = psnr(tmpr, tmpg)
        os.remove(tmpg); os.remove(tmpr)
        rows.append((name, results))
        print(f"{name:14s} baseline={results['baseline']:.2f} "
              f"p2plane={results['p2plane']:.2f} bicubic={results['bicubic']:.2f} "
              f"p2plane-bic={results['p2plane']-results['bicubic']:+.2f} "
              f"p2plane-base={results['p2plane']-results['baseline']:+.2f}", flush=True)
    return rows

if __name__ == "__main__":
    main()
