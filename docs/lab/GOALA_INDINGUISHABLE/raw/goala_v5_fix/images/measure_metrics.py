#!/usr/bin/env python3
"""GOAL-A G-series image metrics (harness-only measurement, Python).
Per image: unique colors, raw H-mirror correlation, gradient-detrended
H-mirror correlation (detrend = subtract per-column vertical linear fit,
then correlate with horizontal mirror). Bars: raw < 0.60, detrended < 0.30.
"""
import sys
import numpy as np
from PIL import Image


def hsym_corr(g):
    """Pearson correlation between grayscale image and its horizontal mirror."""
    a = g.ravel()
    b = np.fliplr(g).ravel()
    return float(np.corrcoef(a, b)[0, 1])


def detrend_columns(g):
    """Subtract per-column vertical linear fit (least squares over rows)."""
    h, w = g.shape
    yy = np.arange(h, dtype=np.float64)
    my = yy.mean()
    denom = ((yy - my) ** 2).sum()
    col_mean = g.mean(axis=0)
    slope = (((yy[:, None] - my) * (g - col_mean[None, :])).sum(axis=0)) / denom
    fit = slope[None, :] * yy[:, None] + (col_mean - slope * my)[None, :]
    return g - fit


def metrics(path):
    im = Image.open(path).convert("RGB")
    a = np.asarray(im)
    h, w, _ = a.shape
    uc = len(np.unique(a.reshape(-1, 3), axis=0))
    g = a.mean(axis=2).astype(np.float64)
    raw = hsym_corr(g)
    det = hsym_corr(detrend_columns(g))
    return h, w, uc, raw, det


def main():
    print(f"{'file':12} {'WxH':9} {'uniq':>7} {'raw':>8} {'detr':>8}  bar")
    allpass = True
    for p in sys.argv[1:]:
        h, w, uc, raw, det = metrics(p)
        ok = (abs(raw) < 0.60) and (abs(det) < 0.30)
        allpass = allpass and ok
        name = p.rsplit("/", 1)[-1]
        print(f"{name:12} {w}x{h:<6} {uc:>7} {raw:>8.3f} {det:>8.3f}  {'PASS' if ok else 'FAIL'}")
    print("ALL PASS" if allpass else "SOME FAILED")
    return 0 if allpass else 1


if __name__ == "__main__":
    sys.exit(main())
