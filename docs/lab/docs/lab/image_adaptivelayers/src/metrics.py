#!/usr/bin/env python3
# metrics.py — PSNR (mean of per-channel dB) + SSIM (Gaussian window, per-channel mean)
# for the image_zoom_fork. Reads 24-bit BMPs directly (no external decoder).
import sys, math
import numpy as np

def read_bmp(path):
    with open(path, 'rb') as f:
        d = f.read()
    assert d[0:2] == b'BM', path
    off = int.from_bytes(d[10:14], 'little')
    w = int.from_bytes(d[18:22], 'little', signed=True)
    h = int.from_bytes(d[22:26], 'little', signed=True)
    bpp = int.from_bytes(d[28:30], 'little')
    assert bpp == 24, (path, bpp)
    stride = (w * 3 + 3) // 4 * 4
    img = np.zeros((h, w, 3), dtype=np.float64)
    for y in range(h):
        src = h - 1 - y
        row = d[off + src * stride: off + src * stride + w * 3]
        px = np.frombuffer(row, dtype=np.uint8).reshape(w, 3)
        img[y, :, 0] = px[:, 2]  # R
        img[y, :, 1] = px[:, 1]  # G
        img[y, :, 2] = px[:, 0]  # B
    return img

def psnr_mean(a, b):
    mses = []
    for c in range(3):
        diff = a[:, :, c] - b[:, :, c]
        mses.append(float(np.mean(diff * diff)))
    psnrs = []
    for m in mses:
        if m == 0:
            psnrs.append(float('inf'))
        else:
            psnrs.append(10.0 * math.log10(255.0 * 255.0 / m))
    if any(math.isinf(p) for p in psnrs):
        return float('inf'), mses
    return sum(psnrs) / 3.0, mses

def _gauss_kernel(size=11, sigma=1.5):
    ax = np.arange(size) - size // 2
    k = np.exp(-0.5 * (ax / sigma) ** 2)
    k = k / k.sum()
    return np.outer(k, k)

_GK = _gauss_kernel()

def _conv2(img, k):
    # separable-ish direct convolution via cumsum trick; small images so direct is fine
    kh, kw = k.shape
    ph, pw = kh // 2, kw // 2
    padded = np.pad(img, ((ph, ph), (pw, pw)), mode='reflect')
    out = np.zeros_like(img)
    for i in range(kh):
        for j in range(kw):
            out += k[i, j] * padded[i:i + img.shape[0], j:j + img.shape[1]]
    return out

def ssim_channel(a, b):
    K1, K2, L = 0.01, 0.03, 255.0
    C1 = (K1 * L) ** 2
    C2 = (K2 * L) ** 2
    mu_a = _conv2(a, _GK)
    mu_b = _conv2(b, _GK)
    mu_a2 = mu_a * mu_a
    mu_b2 = mu_b * mu_b
    mu_ab = mu_a * mu_b
    sig_a2 = _conv2(a * a, _GK) - mu_a2
    sig_b2 = _conv2(b * b, _GK) - mu_b2
    sig_ab = _conv2(a * b, _GK) - mu_ab
    num = (2 * mu_ab + C1) * (2 * sig_ab + C2)
    den = (mu_a2 + mu_b2 + C1) * (sig_a2 + sig_b2 + C2)
    return float(np.mean(num / den))

def ssim_mean(a, b):
    return sum(ssim_channel(a[:, :, c], b[:, :, c]) for c in range(3)) / 3.0

def main():
    ref = read_bmp(sys.argv[1])
    print(f"reference: {sys.argv[1]}  {ref.shape[1]}x{ref.shape[0]}")
    for path in sys.argv[2:]:
        img = read_bmp(path)
        assert img.shape == ref.shape, (path, img.shape)
        p, mses = psnr_mean(ref, img)
        s = ssim_mean(ref, img)
        ps = "inf" if math.isinf(p) else f"{p:.2f}"
        print(f"{path}: PSNR {ps} dB  SSIM {s:.4f}  mse_ch {mses[0]:.2f}/{mses[1]:.2f}/{mses[2]:.2f}")

if __name__ == '__main__':
    main()
