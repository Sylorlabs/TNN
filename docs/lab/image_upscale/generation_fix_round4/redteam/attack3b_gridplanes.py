#!/usr/bin/env python3
"""ATTACK 3b — DIAGNOSTIC: fixed-grid planes, no vocabulary at all.
Uniform non-overlapping 32x32 LR blocks; per-channel least-squares plane
fit on each block's LR pixels (same centered-coords math as the Zag plane
code: u=2xx-(bw-1), v=2yy-(bh-1), c=mean, slopes=sum(d*u)/sum(u^2)); the
plane is evaluated at the 2x output positions. Even output positions keep
the observed input pixel (the pipeline's KNOWN convention: construction
never overwrites observed pixels); odd positions get the plane value.
No atom matching, no lineage, no vocab file read at all.
Question: does this dumb fixed-grid plane render match P2plane's sealed
mean +0.539 dB? If yes, the vocabulary contributes nothing even as a
geometry decider.
"""
import numpy as np, os, shutil, sys

RT = "/home/hatch/workspace/upscale_r4/redteam_r4"
sys.path.insert(0, RT)
from rt_common import BIN_BASE, VOC2, prep, run_bin, psnr
sys.path.insert(0, "/home/hatch/workspace/selfpam_run/tnn-lab/docs/lab/image_upscale/diverse_set")
from eval_all import write_bmp  # noqa
sys.path.insert(0, "/home/hatch/workspace/upscale_r4/battery_build")
import run_matrix as M  # noqa

SEALED = [f"sealed_{i:02d}" for i in range(1, 11)]
GB = 32

def grid_planes(lr):
    h, w, _ = lr.shape
    out = np.zeros((2 * h, 2 * w, 3), dtype=np.float64)
    out[0::2, 0::2] = lr  # KNOWN even positions
    f = lr.astype(np.float64)
    for y0 in range(0, h, GB):
        for x0 in range(0, w, GB):
            bw, bh = min(GB, w - x0), min(GB, h - y0)
            blk = f[y0:y0 + bh, x0:x0 + bw]
            xx = np.arange(bw); yy = np.arange(bh)
            u = 2 * xx - (bw - 1); v = 2 * yy - (bh - 1)
            da = bh * (u * u).sum(); db = bw * (v * v).sum()
            c = blk.mean(axis=(0, 1))
            d = blk - c
            na = (d * u[None, :, None]).sum(axis=(0, 1))
            nb = (d * v[:, None, None]).sum(axis=(0, 1))
            sa = na / da if da > 0 else np.zeros(3)
            sb = nb / db if db > 0 else np.zeros(3)
            oy2 = np.arange(2 * bh); ox2 = np.arange(2 * bw)
            up = ox2 - (bw - 1); vp = oy2 - (bh - 1)
            plane = (c[None, None, :]
                     + sa[None, None, :] * up[None, :, None]
                     + sb[None, None, :] * vp[:, None, None])
            plane = np.clip(np.round(plane), 0, 255)
            osec = out[2 * y0:2 * y0 + 2 * bh, 2 * x0:2 * x0 + 2 * bw]
            mask = np.zeros((2 * bh, 2 * bw), bool)
            mask[1::2, :] = True; mask[:, 1::2] = True
            osec[mask] = plane[mask]
    return np.clip(np.round(out), 0, 255).astype(np.uint8)

def main():
    os.chdir(os.path.join(RT, "work", "attack3"))
    print(f"{'image':10s} {'baseline':>8s} {'gridplane':>9s} {'delta':>7s}", flush=True)
    deltas = []
    for name in SEALED:
        indir = f"gind_{name}"
        shutil.rmtree(indir, ignore_errors=True)
        prep("sealed", name, VOC2, indir)  # vocab unused by grid; baseline needs VOC2
        lr = M.bmp_gt(os.path.join(indir, "input.bmp"))
        gen = grid_planes(lr)
        gp = os.path.join(indir, "grid_gen.bmp"); write_bmp(gp, gen)
        pg = psnr(os.path.join(indir, "gt.bmp"), gp)
        # baseline PSNR for reference: run the real baseline binary
        outd = f"gout_{name}"
        shutil.rmtree(outd, ignore_errors=True)
        p = run_bin(BIN_BASE, indir, outd)
        assert p.returncode == 0, (name, p.stderr[-1000:])
        pb = psnr(os.path.join(indir, "gt.bmp"), os.path.join(outd, "upscale_gen.bmp"))
        d = pg - pb
        deltas.append(d)
        print(f"{name:10s} {pb:8.2f} {pg:9.2f} {d:+7.2f}", flush=True)
        shutil.rmtree(indir); shutil.rmtree(outd)
    print(f"gridplane mean delta vs baseline: {sum(deltas)/len(deltas):+.3f} dB "
          f"(P2plane sealed mean: +0.539)", flush=True)

if __name__ == "__main__":
    main()
