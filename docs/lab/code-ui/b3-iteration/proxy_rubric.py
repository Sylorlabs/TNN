#!/usr/bin/env python3
"""Blind human-proxy rubric for B3 (preregistered in PROXY_RUBRIC.md).

Deterministic pixel measurements, independent implementation from the frozen
judge (different thresholds/algorithms). Reads BLIND_A.img / BLIND_B.img,
prints measurements for both. The mapping (which is v1/v2) is recorded
separately in blinding.txt and unsealed AFTER measurements are recorded.
"""
import math, struct, sys

def load(path):
    b = open(path, "rb").read()
    w, h = struct.unpack("<II", b[:8])
    px = b[8:]
    assert len(px) == w * h * 3
    return w, h, px

def lum(r, g, bl):
    return 0.299 * r + 0.587 * g + 0.114 * bl

def measure(path):
    w, h, px = load(path)
    n = w * h
    ls = [lum(px[i], px[i + 1], px[i + 2]) for i in range(0, len(px), 3)]
    srt = sorted(ls)
    bg = srt[n // 2]
    if bg > 128:
        ink = [1 if L < bg - 60 else 0 for L in ls]
    else:
        # dark theme: ink is lighter than the background
        ink = [1 if L > bg + 60 else 0 for L in ls]
    # bands: rows with >2% ink, merged across gaps <= 8px
    rows = []
    for y in range(h):
        c = sum(ink[y * w:(y + 1) * w])
        rows.append(c > 0.02 * w)
    bands = []
    y = 0
    while y < h:
        if rows[y]:
            y0 = y
            while y < h and (rows[y] or (y - y0 < 8 and any(rows[y:y + 8]))):
                y += 1
            bands.append((y0, y))
        else:
            y += 1
    # merge bands separated by <8px gaps
    merged = []
    for b0, b1 in bands:
        if merged and b0 - merged[-1][1] < 8:
            merged[-1] = (merged[-1][0], b1)
        else:
            merged.append((b0, b1))
    bands = merged
    ink_total = sum(ink) / n
    # gaps between bands
    gaps = [bands[i + 1][0] - bands[i][1] for i in range(len(bands) - 1)]
    if len(gaps) >= 2:
        m = sum(gaps) / len(gaps)
        var = sum((g - m) ** 2 for g in gaps) / len(gaps)
        gap_cv = math.sqrt(var) / m if m > 0 else 0.0
    else:
        gap_cv = 0.0
    # margin ink: top/bottom 10% rows
    mrows = h // 10
    marg = (sum(ink[:mrows * w]) + sum(ink[(h - mrows) * w:])) / max(1, sum(ink))
    # ink_total deviation from [0.005, 0.15]
    if ink_total < 0.005:
        ink_dev = 0.005 - ink_total
    elif ink_total > 0.15:
        ink_dev = ink_total - 0.15
    else:
        ink_dev = 0.0
    # type modes: distinct band heights clustered within 3px
    hs = sorted(b1 - b0 for b0, b1 in bands)
    modes = 0
    last = -100
    for x in hs:
        if x - last > 3:
            modes += 1
            last = x
    # contrast
    ink_ls = [L for L, k in zip(ls, ink) if k]
    ink_mean = sum(ink_ls) / max(1, len(ink_ls))
    contrast = (max(bg, ink_mean) + 10) / (min(bg, ink_mean) + 10)
    # alignment: distinct left-ink-edge x positions per band (clustered 4px)
    edges = []
    for b0, b1 in bands:
        found = None
        for x in range(w):
            col = sum(ink[(b0 + dy) * w + x] for dy in range(b1 - b0))
            if col >= 0.10 * (b1 - b0):
                found = x
                break
        if found is not None:
            edges.append(found)
    edges.sort()
    amodes = 0
    last = -100
    for x in edges:
        if x - last > 4:
            amodes += 1
            last = x
    # hierarchy
    masses = [sum(ink[b0 * w:b1 * w]) for b0, b1 in bands]
    tot = max(1, sum(masses))
    hero_ratio = max(masses) / tot if masses else 0.0
    med_h = hs[len(hs) // 2] if hs else 1
    size_ratio = (max(hs) / med_h) if hs and med_h else 0.0
    # color restraint
    sat_n = 0
    huebins = set()
    for i in range(0, len(px), 3):
        r, g, bl = px[i] / 255.0, px[i + 1] / 255.0, px[i + 2] / 255.0
        mx, mn = max(r, g, bl), min(r, g, bl)
        s = 0.0 if mx == 0 else (mx - mn) / mx
        if s * 255 > 48:
            sat_n += 1
            if mx == mn:
                hb = -1
            elif mx == r:
                hb = int(6 * ((g - bl) / (mx - mn + 1e-9))) % 6
            elif mx == g:
                hb = int(2 + 6 * ((bl - r) / (mx - mn + 1e-9))) % 6
            else:
                hb = int(4 + 6 * ((r - g) / (mx - mn + 1e-9))) % 6
            huebins.add(hb)
    satcov = sat_n / n
    return {
        "bands": len(bands), "gap_cv": round(gap_cv, 4),
        "margin_ink": round(marg, 4), "ink_total": round(ink_total, 4),
        "ink_dev": round(ink_dev, 5), "type_modes": modes,
        "contrast": round(contrast, 3), "align_modes": amodes,
        "hero_ratio": round(hero_ratio, 4), "size_ratio": round(size_ratio, 3),
        "satcov": round(satcov, 4), "hues": len(huebins),
    }

if __name__ == "__main__":
    for tag in ("BLIND_A", "BLIND_B"):
        m = measure(sys.argv[1] + "/%s.img" % tag)
        print("## %s" % tag)
        for k, v in m.items():
            print("%s=%s" % (k, v))
