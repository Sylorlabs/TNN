#!/usr/bin/env python3
"""Round-4 mechanism scorer. Compares a variant frame pair against the
round-3 baseline: crops 3 regions, builds side-by-sides, reports edge
energy / V-SHARP / temporal delta. Usage: score_mech.py <ID>"""
import sys, os, numpy as np
from PIL import Image

MID = sys.argv[1]
BASE = os.path.expanduser("~/workspace/tnn-lab/imagination_discovery/vid/frames/dvid1_f23.bmp")
BASE22 = os.path.expanduser("~/workspace/tnn-lab/imagination_discovery/vid/frames/dvid1_f22.bmp")
VDIR = os.path.expanduser("~/workspace/tmp_vid/r4v")
CROPS = os.path.expanduser("~/workspace/tnn-lab/imagination_discovery/vid/r4/crops")
REGIONS = {"fg": (384, 700, 640, 956), "mid": (384, 430, 640, 686),
           "spire": (440, 300, 696, 556)}

def L(p): return np.asarray(Image.open(p).convert("L"), dtype=np.float64)
def edge(a):
    gx = np.abs(np.diff(a, axis=1)).mean(); gy = np.abs(np.diff(a, axis=0)).mean()
    return gx, gy

def vsharp(p):
    a = L(p); h, w = a.shape; out = np.zeros_like(a)
    for yy in range(2, h - 2):
        for xx in range(2, w - 2):
            out[yy, xx] = abs(2*a[yy,xx]-a[yy,xx-2]-a[yy,xx+2]) + abs(2*a[yy,xx]-a[yy-2,xx]-a[yy+2,xx])
    return out.mean()

b23, b22 = L(BASE), L(BASE22)
v23p = os.path.join(VDIR, MID, "f23.bmp"); v22p = os.path.join(VDIR, MID, "f22.bmp")
v23, v22 = L(v23p), L(v22p)
print(f"=== {MID} ===")
for name, box in REGIONS.items():
    x0, y0, x1, y1 = box
    bh, bv = edge(b23[y0:y1, x0:x1]); vh, vv = edge(v23[y0:y1, x0:x1])
    bc = Image.open(BASE).crop(box); vc = Image.open(v23p).crop(box)
    bc.save(f"{CROPS}/{MID}_{name}_base.png"); vc.save(f"{CROPS}/{MID}_{name}_var.png")
    w, h = bc.size
    side = Image.new("RGB", (w*2+8, h), (0, 0, 0))
    side.paste(bc, (0, 0)); side.paste(vc, (w+8, 0))
    side.save(f"{CROPS}/{MID}_{name}_sidebyside.png")
    side.resize((w*4+16, h*2), Image.NEAREST).save(f"{CROPS}/{MID}_{name}_sidebyside_2x.png")
    print(f"  {name}: base H={bh:.2f} V={bv:.2f} | var H={vh:.2f} V={vv:.2f} | dV={vv-bv:+.2f} dH={vh-bh:+.2f}")
print(f"  V-SHARP var f23: ratio={vsharp(v23p)/vsharp(BASE):.3f} (>=1.20: {'PASS' if vsharp(v23p)/vsharp(BASE)>=1.20 else 'FAIL'})")
td_b = np.abs(b23-b22).mean()/255*100; td_v = np.abs(v23-v22).mean()/255*100
print(f"  f22->f23 mean|d|/255: base={td_b:.2f}% var={td_v:.2f}%")
