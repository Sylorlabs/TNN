#!/usr/bin/env python3
# measure.py — PSNR + SSIM per channel (original vs reproduction).
# Pure measurement; not part of the TNN mechanism.
import sys, math
import numpy as np
from PIL import Image

def load_bmp_rgb(path):
    im = Image.open(path).convert('RGB')
    return np.asarray(im).astype(np.float64)

def psnr(a, b):
    mse = np.mean((a - b) ** 2)
    if mse == 0:
        return float('inf')
    return 10 * math.log10(255.0 ** 2 / mse)

def _gauss_window(size=11, sigma=1.5):
    ax = np.arange(size) - size // 2
    w = np.exp(-(ax ** 2) / (2 * sigma ** 2))
    w = w / w.sum()
    return np.outer(w, w)

def _conv2(a, w):
    # separable-ish direct convolution via cumsum trick is overkill; use FFT-free
    # sliding window with stride tricks
    kh, kw = w.shape
    ph, pw = kh // 2, kw // 2
    ap = np.pad(a, ((ph, ph), (pw, pw)), mode='reflect')
    s = np.lib.stride_tricks.sliding_window_view(ap, (kh, kw))
    return np.sum(s * w, axis=(-2, -1))

_WIN = _gauss_window()
K1, K2, L = 0.01, 0.03, 255.0
C1 = (K1 * L) ** 2
C2 = (K2 * L) ** 2

def ssim_channel(a, b):
    mu_a = _conv2(a, _WIN)
    mu_b = _conv2(b, _WIN)
    s_aa = _conv2(a * a, _WIN) - mu_a * mu_a
    s_bb = _conv2(b * b, _WIN) - mu_b * mu_b
    s_ab = _conv2(a * b, _WIN) - mu_a * mu_b
    num = (2 * mu_a * mu_b + C1) * (2 * s_ab + C2)
    den = (mu_a * mu_a + mu_b * mu_b + C1) * (s_aa + s_bb + C2)
    return float(np.mean(num / den))

def report(orig_path, test_path, label):
    o = load_bmp_rgb(orig_path)
    t = load_bmp_rgb(test_path)
    assert o.shape == t.shape, (o.shape, t.shape)
    print(f"--- {label} ---")
    names = ['R', 'G', 'B']
    ps, ss = [], []
    for c in range(3):
        p = psnr(o[:, :, c], t[:, :, c])
        s = ssim_channel(o[:, :, c], t[:, :, c])
        ps.append(p); ss.append(s)
        print(f"  {names[c]}: PSNR={p:7.2f} dB  SSIM={s:.4f}")
    pm = psnr(o, t)
    sm = sum(ss) / 3
    print(f"  mean: PSNR={pm:7.2f} dB  SSIM={sm:.4f}")
    return pm, sm

if __name__ == '__main__':
    d = sys.argv[1] if len(sys.argv) > 1 else '.'
    orig = f"{d}/original_512.bmp"
    report(orig, f"{d}/repro_flat.bmp", "TNN repro FLAT (region means)")
    report(orig, f"{d}/repro_grad.bmp", "TNN repro GRAD (region means+planar)")
    report(orig, f"{d}/control.bmp", "CONTROL (r11-idiom from text description)")
