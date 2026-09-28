#!/usr/bin/env python3
"""Frozen R4 bicubic reference: PIL 10.2.0 Image.BICUBIC 2x of the exact LR
input the harness feeds the binaries.

LR derivation (byte-exact copy of eval_all.py convention):
  1. GT: JPEG decoded via PIL -> RGB; if height is odd, drop the last row.
  2. input.bmp = 2x2 box average, round-half-up: (a+b+c+d+2)//4 per channel.
  3. Bicubic ref: input (uint8 RGB, PIL) -> resize((2w,2h), Image.BICUBIC).
PSNR: mean of per-channel dB, identical formula to frozen metrics.py.
For bridge/sky: GT and input read from the existing indir BMPs directly.
"""
import math
import sys
import numpy as np
from PIL import Image

def read_bmp(path):
    with open(path, "rb") as f:
        d = f.read()
    assert d[0:2] == b"BM", path
    off = int.from_bytes(d[10:14], "little")
    w = int.from_bytes(d[18:22], "little", signed=True)
    h = int.from_bytes(d[22:26], "little", signed=True)
    assert int.from_bytes(d[28:30], "little") == 24, path
    stride = (w * 3 + 3) // 4 * 4
    img = np.zeros((h, w, 3), dtype=np.uint8)
    for y in range(h):
        src = h - 1 - y
        row = d[off + src * stride: off + src * stride + w * 3]
        px = np.frombuffer(row, dtype=np.uint8).reshape(w, 3)
        img[y, :, 0] = px[:, 2]
        img[y, :, 1] = px[:, 1]
        img[y, :, 2] = px[:, 0]
    return img  # RGB uint8

def downscale_2x2(img):
    h, w, _ = img.shape
    a = img[0:h:2, 0:w:2].astype(np.int32)
    b = img[0:h:2, 1:w:2].astype(np.int32)
    c = img[1:h:2, 0:w:2].astype(np.int32)
    d = img[1:h:2, 1:w:2].astype(np.int32)
    return ((a + b + c + d + 2) // 4).astype(np.uint8)

def psnr_mean(a, b):
    ds = []
    for c in range(3):
        diff = a[:, :, c].astype(np.float64) - b[:, :, c].astype(np.float64)
        mse = float(np.mean(diff * diff))
        if mse == 0:
            return float("inf")
        ds.append(10.0 * math.log10(65025.0 / mse))
    return sum(ds) / 3.0

def jpg_pair(jpg):
    im = Image.open(jpg).convert("RGB")
    arr = np.asarray(im)
    h, w, _ = arr.shape
    if h % 2 == 1:
        arr = arr[:-1]
    return arr

def main():
    for jpg in sys.argv[1:]:
        gt = jpg_pair(jpg)
        inp = downscale_2x2(gt)
        up = np.asarray(Image.fromarray(inp).resize((inp.shape[1] * 2, inp.shape[0] * 2), Image.BICUBIC))
        print(f"{jpg}: bicubic {psnr_mean(up, gt):.4f} dB  (GT {gt.shape[1]}x{gt.shape[0]}, in {inp.shape[1]}x{inp.shape[0]})")

if __name__ == "__main__":
    main()
