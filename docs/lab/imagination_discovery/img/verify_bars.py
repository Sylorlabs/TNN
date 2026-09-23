#!/usr/bin/env python3
"""Mechanical bar verification for imagination_discovery image pipeline.
VERIFY ONLY — never generates. Reads Zag-emitted BMPs.
Bars: D-RES, D-SHARP, D-DET (via sha file), D-COMP (grep audit).
"""
import struct, sys, hashlib, re, os
import numpy as np
from PIL import Image

IMGDIR = os.path.dirname(os.path.abspath(__file__))

def read_bmp_24(path):
    with open(path, 'rb') as f:
        data = f.read()
    assert data[0:2] == b'BM', 'not a BMP'
    off = struct.unpack('<I', data[10:14])[0]
    w = struct.unpack('<i', data[18:22])[0]
    h = struct.unpack('<i', data[22:26])[0]
    bpp = struct.unpack('<H', data[28:30])[0]
    assert bpp == 24, f'bpp={bpp}'
    stride = (w * 3 + 3) // 4 * 4
    img = np.zeros((h, w, 3), dtype=np.uint8)
    for row in range(h):
        src = off + (h - 1 - row) * stride
        px = np.frombuffer(data[src:src + w * 3], dtype=np.uint8).reshape(w, 3)
        img[row, :, 0] = px[:, 2]  # BGR -> R
        img[row, :, 1] = px[:, 1]
        img[row, :, 2] = px[:, 0]
    return img, w, h

def mean_grad(img):
    luma = 0.299 * img[:, :, 0] + 0.587 * img[:, :, 1] + 0.114 * img[:, :, 2]
    gx = np.abs(np.diff(luma, axis=1))
    gy = np.abs(np.diff(luma, axis=0))
    return (gx.mean() + gy.mean()) / 2.0

def box_down2_up2(img):
    h, w, _ = img.shape
    h2, w2 = h // 2, w // 2
    small = img[:h2*2, :w2*2].reshape(h2, 2, w2, 2, 3).mean(axis=(1, 3))
    return np.repeat(np.repeat(small, 2, axis=0), 2, axis=1).astype(np.float64)

def check_file(path):
    img, w, h = read_bmp_24(path)
    res_ok = (w >= 1024 and h >= 1024)
    go = mean_grad(img.astype(np.float64))
    gb = mean_grad(box_down2_up2(img))
    ratio = go / gb if gb > 0 else 0
    sharp_ok = ratio >= 1.20
    return {
        'path': path, 'w': w, 'h': h, 'res_ok': res_ok,
        'grad_o': go, 'grad_b': gb, 'ratio': ratio, 'sharp_ok': sharp_ok,
    }

BANNED = [r'\brect\b', r'\bband\b', r'\bblotch\b', r'\bfill_rect\b',
          r'\bfill\b', r'\bstroke\b', r'\bcircle\b', r'\bellipse\b']

def check_comp(srcdir):
    hits = []
    for fn in sorted(os.listdir(srcdir)):
        if not fn.endswith('.zag'):
            continue
        p = os.path.join(srcdir, fn)
        with open(p) as f:
            for ln, line in enumerate(f, 1):
                code = line.split('//')[0]
                for pat in BANNED:
                    if re.search(pat, code):
                        hits.append((fn, ln, pat, line.strip()[:80]))
    return hits

def main():
    files = sys.argv[1:]
    print('=== D-RES / D-SHARP ===')
    allok = True
    for f in files:
        r = check_file(f)
        print(f"{os.path.basename(f)}: {r['w']}x{r['h']} "
              f"D-RES={'PASS' if r['res_ok'] else 'FAIL'} "
              f"grad(O)={r['grad_o']:.3f} grad(B)={r['grad_b']:.3f} "
              f"ratio={r['ratio']:.3f} D-SHARP={'PASS' if r['sharp_ok'] else 'FAIL'}")
        allok = allok and r['res_ok'] and r['sharp_ok']
        # preview PNG (lossless re-encode, allowed)
        img, _, _ = read_bmp_24(f)
        png = os.path.splitext(f)[0] + '.png'
        Image.fromarray(img).save(png)
        print(f'  preview -> {os.path.basename(png)}')
    print('=== D-COMP (grep audit of scene builders) ===')
    hits = check_comp(IMGDIR)
    if hits:
        print('D-COMP FAIL — banned primitive tokens found:')
        for fn, ln, pat, line in hits:
            print(f'  {fn}:{ln} [{pat}] {line}')
        allok = False
    else:
        print('D-COMP PASS — zero axis-aligned filled-primitive placement tokens')
    print('OVERALL:', 'PASS' if allok else 'FAIL')
    return 0 if allok else 1

if __name__ == '__main__':
    sys.exit(main())
