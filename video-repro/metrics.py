#!/usr/bin/env python3
"""Per-frame PSNR + SSIM vs the original clip, for every condition.
SSIM: standard Wang et al., 11x11 Gaussian sigma 1.5, per channel, mean.
Writes metrics/metrics.csv + prints summary table.
Usage: metrics.py <srcdir> <runsdir> <outcsv>
"""
import os, sys, math, csv
import numpy as np
from PIL import Image

SRC, RUNS, OUTCSV = sys.argv[1], sys.argv[2], sys.argv[3]

def load_rgb(path, size=None):
    im = Image.open(path).convert("RGB")
    if size is not None and im.size != size:
        im = im.resize(size, Image.BILINEAR)
    return np.asarray(im, dtype=np.float64)

_gk = None
def gauss_kernel():
    global _gk
    if _gk is None:
        x = np.arange(11) - 5
        k = np.exp(-(x ** 2) / (2 * 1.5 ** 2))
        _gk = k / k.sum()
    return _gk

def conv_separable(a):
    k = gauss_kernel()
    # reflect-pad then convolve along each axis (valid)
    p = 5
    b = np.pad(a, ((p, p), (p, p)), mode="reflect")
    tmp = np.apply_along_axis(lambda r: np.convolve(r, k, mode="valid"), 1, b)
    out = np.apply_along_axis(lambda c: np.convolve(c, k, mode="valid"), 0, tmp)
    return out

def ssim(a, b):
    K1, K2, L = 0.01, 0.03, 255.0
    C1, C2 = (K1 * L) ** 2, (K2 * L) ** 2
    vals = []
    for ch in range(3):
        x, y = a[:, :, ch], b[:, :, ch]
        mu1, mu2 = conv_separable(x), conv_separable(y)
        mu1_sq, mu2_sq, mu12 = mu1**2, mu2**2, mu1 * mu2
        s1_sq = conv_separable(x * x) - mu1_sq
        s2_sq = conv_separable(y * y) - mu2_sq
        s12 = conv_separable(x * y) - mu12
        m = ((2 * mu12 + C1) * (2 * s12 + C2)) / ((mu1_sq + mu2_sq + C1) * (s1_sq + s2_sq + C2))
        vals.append(m.mean())
    return float(np.mean(vals))

def psnr(a, b):
    mse = float(np.mean((a - b) ** 2))
    if mse == 0:
        return float("inf")
    return 10 * math.log10(255.0 ** 2 / mse)

CONDS = {
    "native-verbatim": ("out_verbatim", "frame_{:02d}.ppm", None),
    "native-encoded": ("out_encoded", "frame_{:02d}.ppm", None),
    "byte-copy": ("bytecopy", "frame_{:02d}.ppm", None),
    "floor": ("floor240", "floor_{:02d}.ppm", (320, 240)),  # stretch = part of the floor's gap
}

rows = []
print(f"{'cond':16s} {'frame':5s} {'PSNR':>10s} {'SSIM':>8s}")
for cond, (subdir, pat, size) in CONDS.items():
    for f in range(24):
        ref = load_rgb(os.path.join(SRC, f"frame_{f:02d}.ppm"))
        tst = load_rgb(os.path.join(RUNS, subdir, pat.format(f)), size)
        p, s = psnr(ref, tst), ssim(ref, tst)
        rows.append((cond, f, p, s))
        ps = "inf" if math.isinf(p) else f"{p:8.2f}"
        print(f"{cond:16s} {f:5d} {ps:>10s} {s:8.4f}")

os.makedirs(os.path.dirname(OUTCSV), exist_ok=True)
with open(OUTCSV, "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["condition", "frame", "psnr_db", "ssim"])
    for cond, f, p, s in rows:
        w.writerow([cond, f, "inf" if math.isinf(p) else f"{p:.4f}", f"{s:.6f}"])

print("\n== means (inf excluded from PSNR mean) ==")
for cond in CONDS:
    ps = [p for c, f_, p, s in rows if c == cond and not math.isinf(p)]
    ss = [s for c, f_, p, s in rows if c == cond]
    ninf = sum(1 for c, f_, p, s in rows if c == cond and math.isinf(p))
    pm = f"{sum(ps)/len(ps):.2f}" if ps else f"inf x{ninf}"
    print(f"{cond:16s} PSNR mean={pm}  SSIM mean={sum(ss)/len(ss):.4f}  minSSIM={min(ss):.4f}")
