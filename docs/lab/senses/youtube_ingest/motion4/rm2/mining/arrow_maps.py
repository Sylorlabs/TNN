#!/usr/bin/env python3
"""arrow_maps.py — per-block 8x8 direction-arrow maps for RM2 candidates.
Distinguishes uniform translation (all arrows one way), expansion flow
(radial), multi-motion (patchwork). Zero RNG."""
import math
import os
import struct
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m3_numpy as N  # noqa: E402

MINE = os.path.dirname(os.path.abspath(__file__))
OUTD = os.path.join(MINE, "arrow_maps")
FSZ = 64 * 64 * 3
NAMES = ["STILL", "N", "NE", "E", "SE", "S", "SW", "W", "NW"]

_cache = {}


def raw_frames(vid):
    if vid not in _cache:
        with open(os.path.join(MINE, vid + ".raw"), "rb") as f:
            data = f.read()
        n = len(data) // FSZ
        _cache[vid] = [data[i * FSZ:(i + 1) * FSZ] for i in range(n)]
    return _cache[vid]


def draw_arrows(name, vid, b, t):
    frames = raw_frames(vid)
    clip = [frames[t + j * b] for j in range(8)]
    lums = [N.lum_plane(f) for f in clip]
    S = 4
    im = Image.new("RGB", (64 * S, 64 * S), (20, 20, 20))
    d = ImageDraw.Draw(im)
    base = Image.frombytes("RGB", (64, 64), clip[0]).resize((64 * S, 64 * S), Image.NEAREST)
    im.paste(base, (0, 0))
    for t2 in range(7):
        eb, nv, et, gn, pw, bx, by, e, vote = N.pair_result(lums[t2], lums[t2 + 1])
        for j in range(8):
            for i in range(8):
                if not vote[j, i]:
                    continue
                ox, oy = int(bx[j, i]), int(by[j, i])
                if ox == 0 and oy == 0:
                    continue
                cx, cy = (i * 8 + 4) * S, (j * 8 + 4) * S
                ang = math.atan2(-oy, ox)
                L = 14
                ex, ey = cx + L * math.cos(ang), cy - L * math.sin(ang)
                d.line([cx, cy, ex, ey], fill=(255, 40, 40), width=2)
                d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=(255, 220, 40))
    im.save(os.path.join(OUTD, name + "_arrows.png"))
    # per-block offset histogram (all 7 pairs)
    hist = {}
    for t2 in range(7):
        _, _, _, _, _, bx, by, e, vote = N.pair_result(lums[t2], lums[t2 + 1])
        for j in range(8):
            for i in range(8):
                if vote[j, i]:
                    key = (int(bx[j, i]), int(by[j, i]))
                    hist[key] = hist.get(key, 0) + 1
    return hist


def main():
    os.makedirs(OUTD, exist_ok=True)
    for line in open(os.path.join(MINE, "rm2_mine_top.tsv")):
        if line.startswith("#"):
            continue
        kind, vid, b, t, dir_lab, pair_wins, e_total = line.rstrip("\n").split("\t")
        b, t = int(b), int(t)
        name = "rm2_%s_b%d_t%04d" % (vid, b, t)
        hist = draw_arrows(name, vid, b, t)
        top = sorted(hist.items(), key=lambda x: -x[1])[:6]
        print("%s dir=%s %s" % (name, dir_lab, top))


if __name__ == "__main__":
    sys.exit(main())
