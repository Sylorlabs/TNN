#!/usr/bin/env python3
"""Deterministic fixture generator for the upscale concept probe->teach->re-probe.
No RNG anywhere: all patterns are closed-form formulas or integer hashes.
Layout:
  fixtures/teach/pair{i}/low.ppm, high.ppm      (i=0..3, 32x32 / 64x64)
  fixtures/probe_before/case{i}/{low,correct,v_shift,v_invent,v_object,v_dims}.ppm
  fixtures/probe_after/case{i}/...               (different images + violator params)
Plus fixtures/SHA256SUMS manifest.
"""
import hashlib, math, os, sys
from PIL import Image

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")

def ihash(x, y, seed):
    # deterministic integer hash -> 0..2^31 (same family as pf_hash2)
    v = (x * 374761393 + y * 668265263 + seed * 2246822519) & 0xFFFFFFFF
    v = (v ^ (v >> 13)) * 1274126177 & 0xFFFFFFFF
    v = (v ^ (v >> 16)) & 0xFFFFFFFF
    return v

def clamp(v): return 0 if v < 0 else (255 if v > 255 else v)

def gray_ppm(path, px, w, h):
    with open(path, "wb") as f:
        f.write(f"P6\n{w} {h}\n255\n".encode())
        for v in px:
            f.write(bytes((v, v, v)))

def box_down(px, w, h):
    W, H = w // 2, h // 2
    out = []
    for y in range(H):
        for x in range(W):
            s = px[(2*y)*w + 2*x] + px[(2*y)*w + 2*x+1] + px[(2*y+1)*w + 2*x] + px[(2*y+1)*w + 2*x+1]
            out.append((s + 2) // 4)  # round-half-up; documented in PREREG rounding analysis
    return out, W, H

# ---- teaching high-res images (64x64), non-periodic (see PREREG M2a note) ----
def t0(x, y): return int(255 * (x + y) / 126)                                  # smooth gradient
def t1(x, y):
    d = math.hypot(x - 32, y - 32); return clamp(int(128 + 100 * math.sin(d * 0.5)))  # circles
def t2(x, y):
    base = 128 + 60 * math.sin(x * 0.3); g = (ihash(x, y, 7) % 17) - 8
    return clamp(int(base + g))                                                 # stripes + grain
def t3(x, y): return clamp(int(128 + 90 * math.sin((x + y) * 0.25)))           # diagonal bands
TEACH = [t0, t1, t2, t3]

# ---- held-out high-res images (different images) ----
def h0(x, y): return int(255 * (x + 2*y) / 189)                                # diagonal gradient
def h1(x, y):
    d = math.hypot(x - 20, y - 44); return clamp(int(128 + 100 * math.sin(d * 0.4)))  # offset circles
def h2(x, y):
    base = 128 + 60 * math.sin(y * 0.35); g = (ihash(x, y, 99) % 13) - 6
    return clamp(int(base + g))                                                 # h-stripes + grain
def heldout_real():
    im = Image.open(os.path.expanduser("~/workspace/image_upscale/stage/gt_512x184.bmp")).convert("L")
    crop = im.crop((100, 60, 164, 124))  # fixed 64x64 region
    return list(crop.tobytes())
HELDOUT = [h0, h1, h2, None]

def synth(fn, w=64, h=64):
    # +x//2: gentle non-periodic gradient breaking translational symmetry
    # (without it, checker/hash structure aliases and M2a SAD ties).
    return [clamp(fn(x, y) + x // 2) for y in range(h) for x in range(w)]

def shift_edge(px, w, h, dx, dy):
    out = []
    for y in range(h):
        for x in range(w):
            sx = min(max(x - dx, 0), w - 1); sy = min(max(y - dy, 0), h - 1)
            out.append(px[sy * w + sx])
    return out

def paste_square(px, w, h, x0, y0, s, v):
    out = px[:]
    for y in range(y0, min(y0 + s, h)):
        for x in range(x0, min(x0 + s, w)):
            out[y * w + x] = v
    return out

def invent(px, w, h, amp, mode):
    # Zero-mean per 2x2 block: block means (hence M2b/F3) untouched, alignment
    # (M2a/F2) untouched; only high-frequency detail is fabricated -> targets F4.
    out = []
    for y in range(h):
        for x in range(w):
            v = px[y * w + x]
            if mode == 0:
                if x % 2 == 1 and y % 2 == 0: v += amp
                elif x % 2 == 0 and y % 2 == 1: v -= amp
            else:
                if x % 2 == 1 and y % 2 == 0: v -= amp
                elif x % 2 == 0 and y % 2 == 1: v += amp
            out.append(clamp(v))
    return out

def build_case(d, high, vparams):
    lo, W, H = box_down(high, 64, 64)
    os.makedirs(d, exist_ok=True)
    gray_ppm(f"{d}/low.ppm", lo, W, H)
    gray_ppm(f"{d}/correct.ppm", high, 64, 64)
    dx, dy, sq, sx, sy, amp, mode = vparams
    gray_ppm(f"{d}/v_shift.ppm", shift_edge(high, 64, 64, dx, dy), 64, 64)
    gray_ppm(f"{d}/v_object.ppm", paste_square(high, 64, 64, sx, sy, sq, 20), 64, 64)
    gray_ppm(f"{d}/v_invent.ppm", invent(high, 64, 64, amp, mode), 64, 64)
    gray_ppm(f"{d}/v_dims.ppm", high[:60*64], 60, 64)  # wrong-dims violator (top-left crop)
    return lo

def main():
    man = []
    # teach pairs
    for i, fn in enumerate(TEACH):
        d = f"{ROOT}/teach/pair{i}"; os.makedirs(d, exist_ok=True)
        high = synth(fn); lo, W, H = box_down(high, 64, 64)
        gray_ppm(f"{d}/high.ppm", high, 64, 64); gray_ppm(f"{d}/low.ppm", lo, W, H)
    # probe_before cases (teach images; violator set A: varied per case)
    VA = [(2, 0, 12, 10, 10, 60, 0),
          (0, 2, 12, 40, 30, 60, 0),
          (-2, 0, 16, 24, 24, 60, 0),
          (0, -2, 10, 30, 10, 60, 0)]
    for i, fn in enumerate(TEACH):
        build_case(f"{ROOT}/probe_before/case{i}", synth(fn), VA[i])
    # probe_after cases (held-out images; violator set B: different params)
    VB = [(0, 2, 12, 30, 40, 50, 1),
          (2, 0, 16, 24, 24, 50, 1),
          (0, -2, 12, 10, 30, 50, 1),
          (-2, 0, 10, 40, 10, 50, 1)]
    for i, fn in enumerate(HELDOUT):
        high = heldout_real() if fn is None else synth(fn)
        build_case(f"{ROOT}/probe_after/case{i}", high, VB[i])
    # manifest
    files = []
    for dp, _, fns in os.walk(ROOT):
        for fn in sorted(fns):
            if fn.endswith(".ppm"): files.append(os.path.join(dp, fn))
    with open(f"{ROOT}/SHA256SUMS", "w") as m:
        for p in sorted(files):
            h = hashlib.sha256(open(p, "rb").read()).hexdigest()
            m.write(f"{h}  {os.path.relpath(p, ROOT)}\n"); man.append(p)
    print(f"wrote {len(man)} fixtures + manifest")

if __name__ == "__main__": main()
