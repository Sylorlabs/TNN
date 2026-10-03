#!/usr/bin/env python3
"""FE1 audit: per-family deterministic separators on the frozen sealed fixtures.

Implements PREREG_FE1_AUDIT.md section 4 exactly. Zero RNG. Deterministic:
fixture order sorted, no timestamps, fixed float formatting. numpy is used
only as a vectorized multiply-accumulate evaluator for the correlator banks
(same arithmetic as the specified bounded MAC loops, directly portable to
pure Zag).

Usage: audit_fe1.py <data-dir> <predictions.csv>
Prints per-family accuracy and the sha256 of the predictions file.
"""
import sys, os, hashlib
import numpy as np

DATA = sys.argv[1]
OUT = sys.argv[2]

FAMILIES = ["PTC-4", "PTC-5", "TMB-4", "TMB-5", "COL-4", "COL-5",
            "CCN-3", "CCN-4", "SHP-4", "SHP-5", "MOT-4", "MOT-5"]
EXT = {"PTC-4": "pcm", "PTC-5": "pcm", "TMB-4": "pcm", "TMB-5": "pcm",
       "COL-4": "img", "COL-5": "img", "CCN-3": "img", "CCN-4": "img",
       "SHP-4": "img", "SHP-5": "img", "MOT-4": "vid", "MOT-5": "vid"}

# ---------------- parsers (frozen R2A contract) ----------------
def u32(b, at):
    return int(b[at]) | (int(b[at+1]) << 8) | (int(b[at+2]) << 16) | (int(b[at+3]) << 24)

def parse_pcm(path):
    b = open(path, "rb").read()
    sr, n = u32(b, 0), u32(b, 4)
    s = np.frombuffer(b, dtype="<i2", offset=8, count=n).astype(np.float64)
    return sr, s

def parse_img(path):
    b = open(path, "rb").read()
    w, h = u32(b, 0), u32(b, 4)
    px = np.frombuffer(b, dtype=np.uint8, offset=8, count=w*h*3).reshape(h, w, 3)
    return w, h, px

def parse_vid(path):
    b = open(path, "rb").read()
    nf, w, h = u32(b, 0), u32(b, 4), u32(b, 8)
    fr = np.frombuffer(b, dtype=np.uint8, offset=12, count=nf*w*h*3).reshape(nf, h, w, 3)
    return nf, w, h, fr

def read_truth(path):
    t = open(path).read().strip()
    assert t.startswith("truth=")
    return t[len("truth="):]

# ---------------- correlator bank (bounded MAC loops, vectorized) ----------------
def corr_bank(freqs, samples, sr=16000.0):
    """C(f) = (s.cos)^2 + (s.sin)^2 for each f. Chunked to bound memory."""
    freqs = np.asarray(freqs, dtype=np.float64)
    n = samples.shape[0]
    idx = np.arange(n, dtype=np.float64)
    out = np.empty(freqs.shape[0], dtype=np.float64)
    CH = 256
    for a in range(0, len(freqs), CH):
        f = freqs[a:a+CH]
        ang = (2.0 * np.pi / sr) * np.outer(f, idx)   # (CH, n)
        c = np.cos(ang); s_ = np.sin(ang)
        rc = samples @ c.T
        rs = samples @ s_.T
        out[a:a+CH] = rc * rc + rs * rs
    return out

def argmax_freq(freqs, samples):
    p = corr_bank(freqs, samples)
    return freqs[int(np.argmax(p))]

# ---------------- PTC-4 / PTC-5 ----------------
def sep_ptc(segs, gap_excl=None):
    segA, segB = segs
    grid = np.arange(280.0, 540.0 + 0.25, 0.5)
    fA = argmax_freq(grid, segA)
    if gap_excl is not None:
        lo, hi = gap_excl
        mask = np.ones(segB.shape[0], dtype=bool)
        mask[lo:hi] = False
        segBv = segB[mask]
    else:
        segBv = segB
    pB = corr_bank(grid, segBv)
    f1 = grid[int(np.argmax(pB))]
    if gap_excl is None:
        # detune-beats: two equal partials; second peak outside +/-2 Hz
        keep = np.abs(grid - f1) >= 2.0
        f2 = grid[np.argmax(np.where(keep, pB, -1.0))]
        fB = 0.5 * (f1 + f2)
    else:
        fB = f1
    d = fB - fA
    if abs(d) < 2.5:
        pred = "SAME"
    elif d > 0:
        pred = "HIGHER"
    else:
        pred = "LOWER"
    return pred, f"fA={fA:.1f} fB={fB:.1f} d={d:.2f}"

def sep_ptc4(path):
    sr, s = parse_pcm(path)
    return sep_ptc((s[0:8000], s[8000:16000]))

def sep_ptc5(path):
    sr, s = parse_pcm(path)
    return sep_ptc((s[0:8000], s[8000:16000]), gap_excl=(3400, 4600))

# ---------------- TMB-4 ----------------
def sep_tmb4(path):
    sr, s = parse_pcm(path)
    grid = np.arange(280.0, 660.0 + 0.25, 0.5)
    # harmonic-sum f0 estimate
    best_f, best_s = 0.0, -1.0
    CH = 64
    for a in range(0, len(grid), CH):
        f = grid[a:a+CH]
        tot = np.zeros(len(f))
        for k in (1, 2, 3, 4):
            tot += np.sqrt(corr_bank(f * k, s))
        j = int(np.argmax(tot))
        if tot[j] > best_s:
            best_s, best_f = tot[j], f[j]
    f0 = best_f
    A = [np.sqrt(corr_bank(np.array([k * f0]), s))[0] for k in (1, 2, 3, 4)]
    r2 = A[1] / A[0] if A[0] > 0 else 0.0
    if r2 < 0.42:
        pred = "DARK"
    elif r2 > 0.65:
        pred = "BRIGHT"
    else:
        pred = "RICH"
    return pred, f"f0={f0:.1f} r2={r2:.3f}"

# ---------------- TMB-5 ----------------
def sep_tmb5(path):
    sr, s = parse_pcm(path)
    X = np.abs(np.fft.rfft(s))
    freqs = np.fft.rfftfreq(s.shape[0], d=1.0 / 16000.0)
    tot = np.sum(X)
    cent = float(np.sum(freqs * X) / tot) if tot > 0 else 0.0
    pred = "DARK" if cent < 1600.0 else "BRIGHT"
    return pred, f"cent={cent:.0f}"

# ---------------- COL-4 ----------------
def sep_col4(path):
    w, h, px = parse_img(path)
    L = px[:, 0:64, :].astype(np.float64).mean(axis=(0, 1))
    R = px[:, 64:68, :].astype(np.float64).mean(axis=(0, 1))
    d = float(np.sum(np.abs(L - R)))
    pred = "DIFFERENT" if d > 25.0 else "SAME"
    return pred, f"d={d:.1f}"

# ---------------- COL-5 ----------------
def col5_pred(S2c, j, S1c):
    # exact replication of the generator's f64 drift math (op order preserved)
    t = S1c * 255.0 / S2c
    t2 = t + float(j)
    v = S2c * t2 / 255.0
    return int(v)  # truncation toward zero == Zag `as i64` for v > 0

def sep_col5(path):
    w, h, px = parse_img(path)
    br, bg, bb = (int(px[0, 0, 0]), int(px[0, 0, 1]), int(px[0, 0, 2]))
    rr, gg, b2 = (int(px[0, 64, 0]), int(px[0, 64, 1]), int(px[0, 64, 2]))
    S1 = (br, bg, bb)
    obs = (rr, gg, b2)
    same_js, diff_js = [], []
    for j in range(-5, 6):
        ps = tuple(col5_pred(S1[c], j, S1[c]) for c in range(3))
        if ps == obs:
            same_js.append(j)
        S2 = (br + 18, bg - 12, bb + 9)
        pd = tuple(col5_pred(S2[c], j, S1[c]) for c in range(3))
        if pd == obs:
            diff_js.append(j)
    if same_js and not diff_js:
        pred = "SAME"
    elif diff_js and not same_js:
        pred = "DIFFERENT"
    else:
        pred = "MISS"
    return pred, f"same_js={same_js} diff_js={diff_js}"

# ---------------- CCN-3 / CCN-4 ----------------
def invert_tint(obs_c, illum_c, mult):
    # obs = int(u * illum/255), u = (v*mult)//10 ; recover v
    u = round(obs_c * 255.0 / illum_c)
    return round(u * 10.0 / mult)

def sep_ccn(path, mode):
    w, h, px = parse_img(path)
    assert (w, h) == (128, 64)
    L = px[:, 0:64, 0].astype(np.float64)  # left R channel == v under neutral
    Rp = px[:, 64:128, :].astype(np.float64)
    vest = np.zeros((64, 64), dtype=np.float64)
    for y in range(64):
        for x in range(64):
            o = Rp[y, x]
            if mode == "checker":
                qx, qy = x // 32, y // 32
                ill = (255.0, 220.0, 180.0) if (qx + qy) % 2 == 0 else (180.0, 210.0, 255.0)
                vr = round(o[0] * 255.0 / ill[0])
                vg = invert_tint(o[1], ill[1], 9)
                vb = invert_tint(o[2], ill[2], 8)
            else:  # bands
                e = 0.55 if (y // 22) == 1 else 1.0
                vr = round(o[0] / e)
                vg = invert_tint(o[1] / e, 255.0, 9)
                vb = invert_tint(o[2] / e, 255.0, 8)
            vest[y, x] = (vr + vg + vb) / 3.0
    mad = float(np.mean(np.abs(vest - L)))
    pred = "SAME_SURFACE" if mad < 4.0 else "DIFFERENT"
    return pred, f"mad={mad:.2f}"

def sep_ccn3(path):
    return sep_ccn(path, "checker")

def sep_ccn4(path):
    return sep_ccn(path, "bands")

# ---------------- shape rasterization (bit-exact replica of draw_shape) ----------------
def draw_shape_mask(sh, cx=48, cy=48, s=26, W=96, H=96):
    yy, xx = np.mgrid[0:H, 0:W]
    dx = xx - cx
    dy = yy - cy
    inside = np.zeros((H, W), dtype=bool)
    if sh == 0:
        inside = dx * dx + dy * dy <= s * s
    elif sh == 1:
        hs = s // 2
        inside = (dx >= -hs) & (dx <= hs) & (dy >= -hs) & (dy <= hs)
    else:
        yt = yy - (cy - s)
        ok = (yt >= 0) & (yt <= (3 * s) // 2)
        half = (s // 2 * ((3 * s) // 2 - yt)) // ((3 * s) // 2)
        inside = ok & (dx >= -half) & (dx <= half)
    return inside

def iou(a, b):
    inter = np.sum(a & b)
    union = np.sum(a | b)
    return float(inter) / float(union) if union else 0.0

SHAPE_NAMES = ["CIRCLE", "SQUARE", "TRIANGLE"]

def sep_shp4(path):
    w, h, px = parse_img(path)
    p = px.astype(np.int32)
    M = ((p[:, :, 2] - p[:, :, 0]) > 50) & ((p[:, :, 2] - p[:, :, 1]) > 30)
    best, best_iou = None, -1.0
    for sh in range(3):
        T = draw_shape_mask(sh, 48, 48, 26)
        v = iou(M, T)
        if v > best_iou:
            best_iou, best = v, sh
    return SHAPE_NAMES[best], f"iou={best_iou:.4f}"

TILE_OFFSETS = [(6, -4), (-6, 5), (5, 6), (-5, -5)]

def forward_tiles(shape_img):
    """Bit-exact replica of gen_shp5's tile displacement (bg 210)."""
    buf = np.full((96, 96), 210, dtype=np.uint8)
    for ty in range(2):
        for tx in range(2):
            ox, oy = TILE_OFFSETS[ty * 2 + tx]
            for y in range(48):
                for x in range(48):
                    sx, sy = tx * 48 + x, ty * 48 + y
                    dx, dy = sx + ox, sy + oy
                    if 0 <= dx < 96 and 0 <= dy < 96:
                        buf[dy, dx] = shape_img[sy, sx]
    return buf

def sep_shp5(path):
    w, h, px = parse_img(path)
    p = px.astype(np.int32)
    M = (p[:, :, 0] - p[:, :, 2]) > 50
    best, best_iou = None, -1.0
    for sh in range(3):
        base = np.full((96, 96), 210, dtype=np.uint8)
        m = draw_shape_mask(sh, 48, 48, 30)
        base[m] = 0  # mark shape pixels; color irrelevant, mask is what matters
        F = forward_tiles(base)
        Tm = F < 128
        v = iou(M, Tm)
        if v > best_iou:
            best_iou, best = v, sh
    return SHAPE_NAMES[best], f"iou={best_iou:.4f}"

# ---------------- MOT-4 / MOT-5 ----------------
DIRS8 = {"E": (1, 0), "W": (-1, 0), "S": (0, 1), "N": (0, -1),
         "SE": (1, 1), "SW": (-1, 1), "NE": (1, -1), "NW": (-1, -1)}

def centroid(mask):
    ys, xs = np.nonzero(mask)
    if len(xs) == 0:
        return None
    return (float(np.mean(xs)), float(np.mean(ys)))

def sep_mot4(path):
    nf, w, h, fr = parse_vid(path)
    f0 = fr[0].astype(np.int32)
    R = f0[:, :, 0]
    H = centroid(R >= 220)
    assert H is not None
    hx, hy = H
    yy, xx = np.mgrid[0:h, 0:w]
    near = (np.abs(xx - hx) <= 16) & (np.abs(yy - hy) <= 16)
    tail = near & (R >= 40) & (R < 200)
    T = centroid(tail)
    assert T is not None
    dx, dy = hx - T[0], hy - T[1]
    norm = (dx * dx + dy * dy) ** 0.5
    best, best_c = None, -2.0
    for name, (ux, uy) in DIRS8.items():
        c = (dx * ux + dy * uy) / (norm * (ux * ux + uy * uy) ** 0.5)
        if c > best_c:
            best_c, best = c, name
    return best, f"cos={best_c:.3f} d=({dx:.1f},{dy:.1f})"

def sep_mot5(path):
    nf, w, h, fr = parse_vid(path)
    D = []
    for f in range(nf):
        R = fr[f].astype(np.int32)[:, :, 0]
        c = centroid(R >= 220)
        assert c is not None
        D.append(c)
    dx = D[7][0] - D[0][0]
    dy = D[7][1] - D[0][1]
    if abs(dx) + abs(dy) < 3.0:
        pred = "STILL"
    elif abs(dx) > abs(dy):
        pred = "E" if dx > 0 else "W"
    else:
        pred = "S" if dy > 0 else "N"
    return pred, f"dx={dx:.1f} dy={dy:.1f}"

SEPS = {"PTC-4": sep_ptc4, "PTC-5": sep_ptc5, "TMB-4": sep_tmb4, "TMB-5": sep_tmb5,
        "COL-4": sep_col4, "COL-5": sep_col5, "CCN-3": sep_ccn3, "CCN-4": sep_ccn4,
        "SHP-4": sep_shp4, "SHP-5": sep_shp5, "MOT-4": sep_mot4, "MOT-5": sep_mot5}

def main():
    rows = ["family,fixture,truth,prediction,correct,detail"]
    summary = []
    for fam in FAMILIES:
        ext = EXT[fam]
        ok = 0
        for idx in range(24):
            name = f"rt3_{fam}_{idx:04d}.{ext}"
            truth = read_truth(os.path.join(DATA, name + ".truth"))
            pred, detail = SEPS[fam](os.path.join(DATA, name))
            c = 1 if pred == truth else 0
            ok += c
            rows.append(f"{fam},{name},{truth},{pred},{c},{detail}")
        summary.append((fam, ok))
        print(f"{fam}: {ok}/24", flush=True)
    with open(OUT, "w") as f:
        f.write("\n".join(rows) + "\n")
    d = hashlib.sha256(open(OUT, "rb").read()).hexdigest()
    print("predictions sha256:", d)
    tot = sum(ok for _, ok in summary)
    print(f"TOTAL: {tot}/288")

if __name__ == "__main__":
    main()
