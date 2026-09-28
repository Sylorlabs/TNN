#!/usr/bin/env python3
"""Calibration prototype for the R2-11 Zag PAMs.

Implements the EXACT integer algorithms planned for the Zag build, in Python,
to calibrate decision thresholds on the frozen 370 harness primary fixtures
before porting to Zag. The Zag port must reproduce these judgments exactly
(verified by cross-check after the build).
"""
import os, struct, math, sys
import numpy as np

FIX = os.path.expanduser("~/workspace/tnn-lab/senses/rebuild/harness/fixtures")
TASKS = ["colordisc", "colorconst", "shapetrans", "pitchdisc", "timbredisc", "motiondir"]
TDIRS = {"colordisc": "t1_colordisc", "colorconst": "t2_colorconst",
         "shapetrans": "t3_shapetrans", "pitchdisc": "t4_pitchdisc",
         "timbredisc": "t5_timbredisc", "motiondir": "t6_motiondir"}
EXTS = {"colordisc": ".img", "colorconst": ".img", "shapetrans": ".img",
        "pitchdisc": ".pcm", "timbredisc": ".pcm", "motiondir": ".vid"}

def isqrt(x):
    return math.isqrt(x) if x > 0 else 0

def load_fixture(task, path):
    raw = open(path, "rb").read()
    if EXTS[task] == ".img":
        w, h = struct.unpack("<II", raw[:8])
        px = np.frombuffer(raw[8:], dtype=np.uint8).reshape(h, w, 3).astype(np.int64)
        return ("img", w, h, px)
    if EXTS[task] == ".pcm":
        rate, n = struct.unpack("<II", raw[:8])
        s = np.frombuffer(raw[8:8+2*n], dtype=np.int16).astype(np.int64)
        return ("pcm", rate, n, s)
    nfr, w, h = struct.unpack("<III", raw[:12])
    px = np.frombuffer(raw[12:], dtype=np.uint8).reshape(nfr, h, w, 3).astype(np.int64)
    return ("vid", nfr, w, h, px)

def truth_of(path):
    return open(path + ".truth").read().strip().split("=", 1)[1]

# ---- T1: mean-RGB euclidean^2 between the two 64x64 patches
def t1(fx, T1):
    _, w, h, px = fx
    A = px[:, :64, :].reshape(-1, 3).sum(axis=0)
    B = px[:, 64:, :].reshape(-1, 3).sum(axis=0)
    n = 64 * 64
    mA = A // n; mB = B // n
    d2 = int(((mA - mB) ** 2).sum())
    judg = "SAME" if d2 < T1 else "DIFFERENT"
    return judg, d2

# ---- T2: pearson r of grayscale, two-pass, fixed x1000
def t2(fx, T2):
    _, w, h, px = fx
    g = (77*px[:, :, 0] + 150*px[:, :, 1] + 29*px[:, :, 2]) >> 8
    A = g[:, :64].reshape(-1); B = g[:, 64:].reshape(-1)
    n = A.shape[0]
    ma = int(A.sum()) // n; mb = int(B.sum()) // n
    da = A - ma; db = B - mb
    num = int((da*db).sum()); va = int((da*da).sum()); vb = int((db*db).sum())
    den = isqrt(va*vb)
    r = (1000*num//den) if den > 0 else 0
    judg = "SAME_SURFACE" if r >= T2 else "DIFFERENT"
    return judg, r

# ---- T3: largest CC, area-ratio A/(pi*R^2) vs anchors (x1000)
def t3(fx):
    _, w, h, px = fx
    g = (77*px[:, :, 0] + 150*px[:, :, 1] + 29*px[:, :, 2]) >> 8
    fg = (g >= 150)
    seen = np.zeros((h, w), dtype=bool)
    best = 0; best_seed = None
    for y in range(h):
        for x in range(w):
            if fg[y, x] and not seen[y, x]:
                stack = [(x, y)]; seen[y, x] = True; cnt = 0
                while stack:
                    cx0, cy0 = stack.pop(); cnt += 1
                    for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
                        nx, ny = cx0+dx, cy0+dy
                        if 0 <= nx < w and 0 <= ny < h and fg[ny, nx] and not seen[ny, nx]:
                            seen[ny, nx] = True; stack.append((nx, ny))
                if cnt > best: best, best_seed = cnt, (x, y)
    if best == 0: return "CIRCLE", 0
    sx, sy = best_seed
    stack = [(sx, sy)]; comp = np.zeros((h, w), dtype=bool); comp[sy, sx] = True
    coords = []
    while stack:
        cx0, cy0 = stack.pop(); coords.append((cx0, cy0))
        for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
            nx, ny = cx0+dx, cy0+dy
            if 0 <= nx < w and 0 <= ny < h and fg[ny, nx] and not comp[ny, nx]:
                comp[ny, nx] = True; stack.append((nx, ny))
    A = len(coords)
    xs = np.array([c[0] for c in coords]); ys = np.array([c[1] for c in coords])
    # centroid x16 fixed
    cx16 = (xs.sum()*16)//A; cy16 = (ys.sum()*16)//A
    R2 = int(max(((xs*16-cx16)**2 + (ys*16-cy16)**2).max(), 1))
    # R2 in (px/16)^2 units -> ratio = 256*A/(pi*R2); x1000 fixed
    ratio = (256000000*A)//(3142*R2) if R2 > 0 else 0
    anchors = {"CIRCLE": 1000, "SQUARE": 637, "TRIANGLE": 414}
    judg = min(anchors, key=lambda k: abs(anchors[k]-ratio))
    return judg, ratio

# ---- T4: autocorr f0 per tone, parabolic interp, smallest-lag rule
# NOTE: analysis window excludes the 20ms raised-cosine ramps (stationary
# middle 5760 of 6400 samples) so the autocorr peak is clean for the parabola.
def _f0_est(x):
    x = x[320:6080]
    N = len(x)
    rs = {}
    gmax = -1
    for L in range(16, 101):
        r = int((x[:N-L]*x[L:]).sum())
        rs[L] = r
        if r > gmax: gmax = r
    # fundamental = global max, divided down while a subharmonic is strong
    Lp = max(rs, key=lambda L: rs[L])
    for k in (2, 3):
        half = Lp / k
        L0 = int(round(half))
        if L0 < 16:
            continue
        cand = [(L0+d, rs.get(L0+d, -1)) for d in (-1, 0, 1) if 16 <= L0+d <= 100]
        bl, bv = max(cand, key=lambda t: t[1])
        if bv*100 >= rs[Lp]*97:
            Lp = bl
    best_r = rs[Lp]
    y0 = rs.get(Lp-1, best_r); y1 = best_r; y2 = rs.get(Lp+1, best_r)
    den = 2*(y0 - 2*y1 + y2)
    d1000 = (1000*(y0-y2)//den) if den != 0 else 0
    P1000 = Lp*1000 + d1000
    f_mHz = 16000000000//P1000 if P1000 > 0 else 0
    return f_mHz

def t4(fx):
    _, rate, n, s = fx
    f0 = _f0_est(s[0:6400]); f1 = _f0_est(s[7680:14080])
    df = abs(f1-f0)
    judg = "SAME" if df*200 < f0 else ("HIGHER" if f1 > f0 else "LOWER")
    return judg, (f0, f1)

# ---- T5: zc + hf-ratio
def t5(fx, hf1, zc1, hf2):
    _, rate, n, s = fx
    x = s[:12800]
    zc = int((((x[:-1] > 0) != (x[1:] > 0))).sum())
    d = np.diff(x)
    hf = int((d*d).sum()); e = int((x*x).sum())
    hfr = (10000*hf//e) if e > 0 else 0
    if hfr < 370: judg = "PURE"
    elif hfr < 800: judg = "DARK"
    elif hfr < 2000: judg = "RICH"
    else: judg = "BRIGHT"
    return judg, (zc, hfr)

# ---- T6: SAD over (dir, shift)
DIRS = {"N": (0,-1), "NE": (1,-1), "E": (1,0), "SE": (1,1),
        "S": (0,1), "SW": (-1,1), "W": (-1,0), "NW": (-1,-1)}
def t6(fx, still_ratio):
    _, nfr, w, h, px = fx
    g = ((77*px[:, :, :, 0] + 150*px[:, :, :, 1] + 29*px[:, :, :, 2]) >> 8)
    f0 = g[0].astype(np.int64); f7 = g[7].astype(np.int64)
    def sad_shift(dx, dy):
        # shift f0 by (dx,dy), compare overlap with f7
        x0 = max(0, -dx); x1 = min(w, w-dx)
        y0 = max(0, -dy); y1 = min(h, h-dy)
        a = f0[y0:y1, x0:x1]
        b = f7[y0+dy:y1+dy, x0+dx:x1+dx]
        return int(np.abs(a-b).sum()), (x1-x0)*(y1-y0)
    s0, n0 = sad_shift(0, 0)
    best = None
    for d, (vx, vy) in DIRS.items():
        for s in (4, 5, 6, 7, 8, 10, 12, 14, 16):
            v, nn = sad_shift(vx*s, vy*s)
            vn = v*1000//nn if nn else v
            if best is None or vn < best[1]: best = (d, vn, s)
    s0n = s0*1000//n0
    if s0n*1000 <= best[1]*still_ratio:
        return "STILL", (s0n, best)
    return best[0], (s0n, best)

def main():
    import json
    T1 = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    T2 = int(sys.argv[2]) if len(sys.argv) > 2 else 900
    out = {}
    for task in TASKS:
        d = os.path.join(FIX, TDIRS[task], "primary")
        files = sorted(f for f in os.listdir(d) if f.endswith(EXTS[task]))
        n = c = 0; det = []
        for fn in files:
            fp = os.path.join(d, fn)
            fx = load_fixture(task, fp)
            t = truth_of(fp)
            if task == "colordisc": j, _ = t1(fx, T1)
            elif task == "colorconst": j, _ = t2(fx, T2)
            elif task == "shapetrans": j, _ = t3(fx)
            elif task == "pitchdisc": j, _ = t4(fx)
            elif task == "timbredisc": j, _ = t5(fx, 600, 1200, 2500)
            elif task == "motiondir": j, _ = t6(fx, 1100)
            n += 1; c += (j == t)
            if j != t: det.append((fn, t, j))
        out[task] = (c, n)
        print("%-12s %d/%d = %.1f%%" % (task, c, n, 100.0*c/n))
        for fn, t, j in det[:12]: print("   miss %-28s truth=%-12s got=%s" % (fn, t, j))
    tot_c = sum(c for c, n in out.values()); tot_n = sum(n for c, n in out.values())
    print("MEAN %.1f%%  (%d/%d)" % (100.0*tot_c/tot_n, tot_c, tot_n))

if __name__ == "__main__":
    main()
