#!/usr/bin/env python3
"""r2gen.py — R2A frozen fixture generator for PAM round 2 (PREREG_R2-2).

Implements `senses/pam-rebuild/round2/preregs/R2_FIXTURE_SET.md` exactly:
  MASTER seed = 20260923 (new; round 1 used 20260921).
  Streams: normal-extended = 400+taskidx, adversarial = 500+taskidx.
  Per-fixture seed = splitmix64(splitmix64(MASTER ^ stream*0x9E3779B97F4A7C15)
                                ^ index*0xBF58476D1CE4E5B9)
  (same construction as harness/gen.py).
  Task index: colordisc=0, colorconst=1, shapetrans=2, pitchdisc=3,
              timbredisc=4, motiondir=5.

Fixture ID prefixes: r2n_<task>_<i> (normal), r2a_<task>_<i> (adversarial).
Truth files <id>.truth written alongside each fixture, from the true
stimulus, never from the corrupted appearance.

File formats are byte-compatible with harness/gen.py:
  .img : u32 LE w, u32 LE h, then w*h RGB bytes
  .pcm : u32 LE rate, u32 LE count, then count int16 LE samples (16000 Hz)
  .vid : u32 LE nframes, u32 LE w, u32 LE h, then frames of w*h RGB bytes

FROZEN-SPEC ARITHMETIC NOTE (recorded here, in GEN_LEDGER.md, and in the
verdict — not silently patched): the fixture spec's per-family / per-task
count tables are self-consistent but disagree with its summary totals:
  - normal: tables sum to 1080+720+1296+720+720+564 = 5100 generated
    (spec text says 4,260; 740 frozen + 5100 = 5840 normal total);
  - adversarial: family table sums to 5815 generated (spec text says 4,815;
    185 frozen + 5815 = 6000 adversarial total);
  - signature-targeted subset (SHP-1+TMB-2+MOT-1+COL-1+SHP-2) sums to
    400+250+350+400+450 = 1850 (prereg text says 2,000).
Resolution rule applied: the most granular frozen tables govern; summary
arithmetic in the text is reported as-is and flagged. B5's bar is a rate
(<=1%), so its meaning is unchanged; the evaluated denominator (1850) is
reported with every B5 number.

Determinism: every draw comes from the seeded splitmix64 streams; numpy is
used only as a vectorized arithmetic engine (no np.random anywhere).
Zero RNG in the fixtures' truth assignment beyond the seeded streams.
"""

import os, sys, math, struct, hashlib, time, json
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
R22 = os.path.dirname(HERE)
WORK = os.environ.get("R2GEN_WORK", os.path.join(R22, "work"))
FIX = os.path.join(WORK, "fixtures", "r2a")
HARN = os.path.expanduser("~/workspace/tnn-lab/senses/rebuild/harness/fixtures")
PHOTOS = os.path.join(HARN, "_photos")

MASTER = 20260923
TASKS = ["colordisc", "colorconst", "shapetrans", "pitchdisc", "timbredisc", "motiondir"]
TIDX = {t: i for i, t in enumerate(TASKS)}

# ---------------- deterministic RNG (same construction as harness/gen.py) ---
MASK64 = (1 << 64) - 1

def splitmix64(state):
    state = (state + 0x9E3779B97F4A7C15) & MASK64
    z = state
    z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & MASK64
    z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & MASK64
    return (z ^ (z >> 31)) & MASK64

class Rng:
    def __init__(self, seed):
        self.s = seed & MASK64
    def u64(self):
        self.s = splitmix64(self.s)
        return self.s
    def uniform(self):
        return (self.u64() >> 11) * (1.0 / (1 << 53))
    def range(self, lo, hi):
        return lo + (hi - lo) * self.uniform()
    def int(self, n):
        return self.u64() % n
    def pick(self, seq):
        return seq[self.u64() % len(seq)]

def stream_seed(master, stream, index):
    h = splitmix64((master ^ (stream * 0x9E3779B97F4A7C15)) & MASK64)
    return splitmix64((h ^ (index * 0xBF58476D1CE4E5B9)) & MASK64)

def mk_rng(kind, task, index):
    stream = (400 if kind == "normal" else 500) + TIDX[task]
    return Rng(stream_seed(MASTER, stream, index))

# ---------------- writers ----------------------------------------------------
def write_img(path, w, h, px):
    with open(path, "wb") as f:
        f.write(struct.pack("<II", w, h))
        f.write(px if isinstance(px, (bytes, bytearray)) else bytes(px))

def write_pcm(path, rate, samples):
    arr = np.asarray(samples, dtype=np.int16)
    with open(path, "wb") as f:
        f.write(struct.pack("<II", rate, len(arr)))
        f.write(arr.tobytes())

def write_vid(path, w, h, frames):
    with open(path, "wb") as f:
        f.write(struct.pack("<III", len(frames), w, h))
        for fr in frames:
            f.write(fr if isinstance(fr, (bytes, bytearray)) else bytes(fr))

def write_truth(path, value):
    with open(path + ".truth", "w") as f:
        f.write("truth=%s\n" % value)

# ---------------- photos -----------------------------------------------------
_photo_cache = {}
def load_photo(i, w=160, h=120):
    if (i, w, h) not in _photo_cache:
        im = Image.open(os.path.join(PHOTOS, "ph%03d.jpg" % (i % 170))).convert("RGB")
        im = im.resize((w, h), Image.BILINEAR)
        _photo_cache[(i, w, h)] = np.asarray(im, dtype=np.uint8)
    return _photo_cache[(i, w, h)]

# ---------------- color math (numpy-vectorized von Kries / Lab) --------------
XYZ_M = np.array(((0.4124564, 0.3575761, 0.1804375),
                  (0.2126729, 0.7151522, 0.0721750),
                  (0.0193339, 0.1191920, 0.9503041)))
XYZ_MI = np.array((( 3.2404542, -1.5371385, -0.4985314),
                   (-0.9692660,  1.8760108,  0.0415560),
                   ( 0.0556434, -0.2040259,  1.0572252)))
BRAD = np.array(((0.8951, 0.2664, -0.1614),
                 (-0.7502, 1.7135, 0.0367),
                 (0.0389, -0.0685, 1.0296)))
BRAD_I = np.array(((0.9869929, -0.1470543, 0.1599627),
                   (0.4323053, 0.5183603, 0.0492912),
                   (-0.0085287, 0.0400428, 0.9684867)))
ILLUM = {
    "d65":   (0.95047, 1.00000, 1.08883),
    "warm":  (1.09850, 1.00000, 0.35585),
    "cool":  (0.99180, 1.00000, 0.67390),
    "xblue": (0.62000, 0.85000, 1.75000),
    "xred":  (1.70000, 0.90000, 0.45000),
}
ILLUM_TRIO = ["d65", "warm", "cool"]

def srgb_to_linear(a):
    a = np.asarray(a, dtype=np.float64) / 255.0
    return np.where(a <= 0.04045, a / 12.92, ((a + 0.055) / 1.055) ** 2.4)

def linear_to_srgb(a):
    a = np.clip(np.asarray(a, dtype=np.float64), 0.0, 1.0)
    v = np.where(a <= 0.0031308, 12.92 * a, 1.055 * (a ** (1.0 / 2.4)) - 0.055)
    return np.rint(np.clip(v, 0, 1) * 255).astype(np.uint8)

def apply_illuminant_np(rgb, illum_xyz):
    """rgb: (N,3) uint8 under D65 -> as seen under illum_xyz (Bradford CAT)."""
    rl = srgb_to_linear(np.asarray(rgb, dtype=np.float64).reshape(-1, 3))
    xyz = rl @ XYZ_M.T
    src = np.array((0.95047, 1.0, 1.08883))
    lms_s = xyz @ BRAD.T
    lms_wsrc = src @ BRAD.T
    lms_wdst = np.array(illum_xyz) @ BRAD.T
    lms = lms_s * (lms_wdst / lms_wsrc)
    xyz2 = lms @ BRAD_I.T
    lin = xyz2 @ XYZ_MI.T
    return linear_to_srgb(lin).reshape(-1, 3)

def rgb_to_lab_np(rgb):
    rl = srgb_to_linear(np.asarray(rgb, dtype=np.float64).reshape(-1, 3))
    x, y, z = (rl @ XYZ_M.T).T
    xn, yn, zn = 0.95047, 1.0, 1.08883
    def f(t):
        return np.where(t > 0.008856, t ** (1/3), 7.787 * t + 16/116)
    fx, fy, fz = f(x/xn), f(y/yn), f(z/zn)
    return np.stack([116*fy - 16, 500*(fx - fy), 200*(fy - fz)], axis=1)

def delta_e_2000_np(lab1, lab2):
    (L1, a1, b1), (L2, a2, b2) = lab1, lab2
    C1 = math.hypot(a1, b1); C2 = math.hypot(a2, b2)
    Cb = (C1 + C2) / 2
    G = 0.5 * (1 - math.sqrt(Cb**7 / (Cb**7 + 25**7)))
    ap1, ap2 = (1+G)*a1, (1+G)*a2
    Cp1, Cp2 = math.hypot(ap1, b1), math.hypot(ap2, b2)
    def hp(ap, b):
        if ap == 0 and b == 0: return 0.0
        h = math.degrees(math.atan2(b, ap)); return h + 360 if h < 0 else h
    hp1, hp2 = hp(ap1, b1), hp(ap2, b2)
    dL, dC = L2-L1, Cp2-Cp1
    if Cp1*Cp2 == 0: dh = 0.0
    else:
        dh = hp2-hp1
        if dh > 180: dh -= 360
        elif dh < -180: dh += 360
    dH = 2*math.sqrt(Cp1*Cp2)*math.sin(math.radians(dh/2))
    Lbp, Cbp = (L1+L2)/2, (Cp1+Cp2)/2
    if Cp1*Cp2 == 0: hbp = hp1+hp2
    else:
        hbp = (hp1+hp2)/2 if abs(hp1-hp2) <= 180 else ((hp1+hp2+360)/2 if hp1+hp2 < 360 else (hp1+hp2-360)/2)
    T = (1 - 0.17*math.cos(math.radians(hbp-30)) + 0.24*math.cos(math.radians(2*hbp))
         + 0.32*math.cos(math.radians(3*hbp+6)) - 0.20*math.cos(math.radians(4*hbp-63)))
    dRo = 30*math.exp(-((hbp-275)/25)**2)
    Rc = 2*math.sqrt(Cbp**7/(Cbp**7+25**7))
    Sl = 1 + 0.015*(Lbp-50)**2/math.sqrt(20+(Lbp-50)**2)
    Sc, Sh = 1+0.045*Cbp, 1+0.015*Cbp*T
    Rt = -math.sin(math.radians(2*dRo))*Rc
    return math.sqrt((dL/Sl)**2 + (dC/Sc)**2 + (dH/Sh)**2 + Rt*(dC/Sc)*(dH/Sh))

def _lab_to_srgb_scalar(L, a, b):
    xn, yn, zn = 0.95047, 1.0, 1.08883
    fy = (L+16)/116.0; fx = fy + a/500.0; fz = fy - b/200.0
    def fi(t): return t**3 if t**3 > 0.008856 else (t-16/116)/7.787
    x, y, z = xn*fi(fx), yn*fi(fy), zn*fi(fz)
    rl = XYZ_MI[0][0]*x + XYZ_MI[0][1]*y + XYZ_MI[0][2]*z
    gl = XYZ_MI[1][0]*x + XYZ_MI[1][1]*y + XYZ_MI[1][2]*z
    bl = XYZ_MI[2][0]*x + XYZ_MI[2][1]*y + XYZ_MI[2][2]*z
    return tuple(int(v) for v in linear_to_srgb([rl, gl, bl]))

def color_at_distance(rng, base, target_de, tol=0.15, tries=400):
    L0, a0, b0 = rgb_to_lab_np([base])[0]
    best = None
    for _ in range(tries):
        ang = rng.uniform()*2*math.pi
        step = target_de*rng.range(0.35, 0.7)
        L1 = max(0.0, min(100.0, L0 + step*math.cos(ang)*rng.range(0.4, 1.0)))
        C = step*math.sin(ang)
        pa = rng.uniform()*2*math.pi
        rgb = _lab_to_srgb_scalar(L1, a0 + C*math.cos(pa), b0 + C*math.sin(pa))
        de = delta_e_2000_np((L0, a0, b0), rgb_to_lab_np([rgb])[0])
        if abs(de-target_de)/target_de < tol:
            return rgb
        if best is None or abs(de-target_de) < abs(best[0]-target_de):
            best = (de, rgb)
    return best[1]

def rgb_eucl(c1, c2):
    return math.sqrt(sum((a-b)**2 for a, b in zip(c1, c2)))

def chroma_milli(c):
    s = c[0]+c[1]+c[2]
    if s == 0: return (0, 0)
    return (1000*c[0]/s, 1000*c[1]/s)

# ---------------- audio synthesis (numpy-vectorized) -------------------------
SR = 16000
RICH_H = [(1, 1.0), (2, 0.30), (3, 0.15)]
TIMBRES = {
    "PURE":   [(1, 1.0)],
    "BRIGHT": [(1, 1.0), (2, 0.80), (3, 0.65), (4, 0.55), (5, 0.45), (6, 0.38), (7, 0.32), (8, 0.28)],
    "DARK":   [(1, 1.0), (2, 0.40), (3, 0.10), (4, 0.03)],
    "RICH":   [(1, 1.0), (2, 0.55), (3, 0.40), (4, 0.28), (5, 0.20), (6, 0.14)],
}

def tone_np(freq, dur, harmonics, amp=0.75, freq_end=None):
    """freq_end: optional linear glide target (Hz) for glide tones."""
    n = int(SR*dur)
    t = np.arange(n, dtype=np.float64)/SR
    if freq_end is None:
        fr = np.full(n, freq)
    else:
        fr = freq + (freq_end-freq)*(t/dur)
    ph = 2*np.pi*np.cumsum(fr)/SR
    out = np.zeros(n)
    for k, a in harmonics:
        out += a*np.sin(k*ph)
    ramp = int(SR*0.02)
    e = 0.5-0.5*np.cos(np.pi*np.arange(ramp)/ramp)
    out[:ramp] *= e; out[n-ramp:] *= e[::-1]
    peak = max(1e-9, np.max(np.abs(out)))
    return np.rint(np.clip(out*(amp/peak), -1, 1)*32767).astype(np.int16)

def centroid_ratio_np(harmonics):
    """Approach-A harmonic centroid ratio r = 1000*sum(h*E)/sum(E), E~a^2."""
    se = sum(a*a for _, a in harmonics)
    she = sum(h*a*a for h, a in harmonics)
    return 1000.0*she/se if se > 0 else 0.0

# ---------------- shape rasterization (numpy-vectorized) ---------------------
def shape_mask_np(kind, W, scale, rot, cx, cy, ss=3):
    """Anti-aliased shape mask on a WxW grid, supersampled ss x ss."""
    g = np.arange(W*ss, dtype=np.float64)/ss
    yy, xx = np.meshgrid(g, g, indexing="ij")
    fx = xx - 0.5 - cx + 0.5
    fy = yy - 0.5 - cy + 0.5
    cosr, sinr = math.cos(rot), math.sin(rot)
    ux = (fx*cosr + fy*sinr)/scale
    uy = (-fx*sinr + fy*cosr)/scale
    if kind == "circle":
        hit = ux*ux + uy*uy <= 0.25
    elif kind == "square":
        hit = (np.abs(ux) <= 0.5) & (np.abs(uy) <= 0.5)
    else:  # triangle: equilateral, centroid at origin, circumradius 0.62
        R = 0.62
        vx = np.array([R*math.cos(math.pi/2 + k*2*math.pi/3) for k in range(3)])
        vy = np.array([-R*math.sin(math.pi/2 + k*2*math.pi/3) for k in range(3)])
        def sign(px, py, ax, ay, bx, by):
            return (px-bx)*(ay-by) - (ax-bx)*(py-by)
        d1 = sign(ux, uy, vx[0], vy[0], vx[1], vy[1])
        d2 = sign(ux, uy, vx[1], vy[1], vx[2], vy[2])
        d3 = sign(ux, uy, vx[2], vy[2], vx[0], vy[0])
        neg = (d1 < 0) | (d2 < 0) | (d3 < 0)
        pos = (d1 > 0) | (d2 > 0) | (d3 > 0)
        hit = ~(neg & pos)
    hit = hit.reshape(W, ss, W, ss).mean(axis=(1, 3))
    return hit  # float WxW alpha

def draw_shape_np(kind, scale, rot, cx, cy, bg, fg, bar=None, blob=None):
    """bg: (H,W,3) uint8; fg: (r,g,b). bar: (y0,y1,dark) occlusion bar.
    blob: (bx,by,br) distractor blob in fg color."""
    W = bg.shape[0]
    a = shape_mask_np(kind, W, scale, rot, cx, cy)[..., None]
    fg_a = np.array(fg, dtype=np.float64)
    px = bg.astype(np.float64)*(1-a) + fg_a*a
    if bar is not None:
        y0, y1, dark = bar
        px[y0:y1, :, :] = np.clip(bg[y0:y1].astype(np.float64)*0.25 + dark, 0, 255)
    if blob is not None:
        bx, by, br = blob
        yy, xx = np.mgrid[0:W, 0:W]
        m = (xx-bx)**2 + (yy-by)**2 <= br*br
        px[m] = fg_a
    return np.rint(np.clip(px, 0, 255)).astype(np.uint8)

# ---------------- normal generators (mirror frozen primary distributions) ----
def g_norm_colordisc(rng, i):
    base = (rng.int(256), rng.int(256), rng.int(256))
    k = i % 60
    if k < 20:
        c2 = base if k < 10 else color_at_distance(rng, base, rng.range(0.4, 1.6))
        truth = "SAME"
    else:
        q = k - 20
        de = rng.range(10, 28) if q < 14 else (rng.range(4, 10) if q < 27 else rng.range(2.4, 4.0))
        c2 = color_at_distance(rng, base, de)
        truth = "DIFFERENT"
    px = np.zeros((64, 128, 3), dtype=np.uint8)
    px[:, :64] = base; px[:, 64:] = c2
    return px, truth

def g_norm_colorconst(rng, i):
    ph = load_photo(rng.int(170))
    if (i % 40) % 2 == 0:
        ox, oy = rng.int(160-64), rng.int(120-64)
        crop = ph[oy:oy+64, ox:ox+64].reshape(-1, 3)
        i1, i2 = rng.int(3), rng.int(3)
        while i2 == i1: i2 = rng.int(3)
        p1 = apply_illuminant_np(crop, ILLUM[ILLUM_TRIO[i1]])
        p2 = apply_illuminant_np(crop, ILLUM[ILLUM_TRIO[i2]])
        truth = "SAME_SURFACE"
    else:
        ph1, ph2 = rng.int(170), rng.int(170)
        while ph2 == ph1: ph2 = rng.int(170)
        a = load_photo(ph1); b = load_photo(ph2)
        ox1, oy1 = rng.int(160-64), rng.int(120-64)
        ox2, oy2 = rng.int(160-64), rng.int(120-64)
        c1 = a[oy1:oy1+64, ox1:ox1+64].reshape(-1, 3)
        c2 = b[oy2:oy2+64, ox2:ox2+64].reshape(-1, 3)
        p1 = apply_illuminant_np(c1, ILLUM[rng.pick(ILLUM_TRIO)])
        p2 = apply_illuminant_np(c2, ILLUM[rng.pick(ILLUM_TRIO)])
        truth = "DIFFERENT"
    px = np.zeros((64, 128, 3), dtype=np.uint8)
    px[:, :64] = p1.reshape(64, 64, 3); px[:, 64:] = p2.reshape(64, 64, 3)
    return px, truth

KINDS = ["circle", "triangle", "square"]
KTRUTH = {"circle": "CIRCLE", "triangle": "TRIANGLE", "square": "SQUARE"}

def g_norm_shapetrans(rng, i):
    kind = KINDS[i % 3]
    W = 96
    ph = load_photo(rng.int(170))
    ox, oy = rng.int(160-W), rng.int(120-W)
    bg = (ph[oy:oy+W, ox:ox+W].astype(np.float64)*0.45)
    rot = rng.uniform()*2*math.pi
    scale = rng.range(30, 44)
    cx = W/2 + rng.range(-14, 14); cy = W/2 + rng.range(-14, 14)
    px = draw_shape_np(kind, scale, rot, cx, cy, bg, (235, 235, 235))
    return px, KTRUTH[kind]

def g_norm_pitchdisc(rng, i):
    f0 = rng.range(220, 660)
    cls = i % 3
    if cls == 0:
        f1, truth = f0, "SAME"
    else:
        band = i % 4
        rel = [rng.range(0.10, 0.25), rng.range(0.02, 0.05),
               rng.range(0.005, 0.008), rng.range(0.10, 0.25)][band]
        f1 = f0*(1+rel) if cls == 1 else f0*(1-rel)
        truth = "HIGHER" if cls == 1 else "LOWER"
    gap = np.zeros(int(SR*0.08), dtype=np.int16)
    samples = np.concatenate([tone_np(f0, 0.4, RICH_H), gap, tone_np(f1, 0.4, RICH_H)])
    return samples, truth

def g_norm_timbredisc(rng, i):
    cls = ["PURE", "BRIGHT", "DARK", "RICH"][i % 4]
    return tone_np(440.0, 0.8, TIMBRES[cls]), cls

DIRS = {"N": (0,-1), "NE": (1,-1), "E": (1,0), "SE": (1,1),
        "S": (0,1), "SW": (-1,1), "W": (-1,0), "NW": (-1,-1)}

def motion_frames(photo, ox, oy, vec, step, contrast, W=64, nf=8, pos_fn=None):
    """Window translates so content moves in `vec` direction (screen coords)."""
    mean = photo.astype(np.float64).mean(axis=(0, 1))
    frames = []
    for f in range(nf):
        if pos_fn is not None:
            dx, dy = pos_fn(f)
        else:
            dx = int(round(-vec[0]*step*f)); dy = int(round(-vec[1]*step*f))
        yy, xx = np.mgrid[0:W, 0:W]
        sx = (ox + xx + dx) % 160; sy = (oy + yy + dy) % 120
        fr = photo[sy, sx].astype(np.float64)
        fr = mean + (fr-mean)*contrast
        frames.append(np.rint(np.clip(fr, 0, 255)).astype(np.uint8))
    return frames

def g_norm_motiondir(rng, i):
    k = i % 60
    photo = load_photo(rng.int(170))
    ox, oy = rng.int(40), rng.int(24)
    if k < 4:
        truth, vec = "STILL", (0, 0)
    else:
        truth = sorted(DIRS)[(k-4) % 8]; vec = DIRS[truth]
    return motion_frames(photo, ox, oy, vec, 2, 1.0), truth

# ================= ADVERARIAL FAMILIES (stream 500+taskidx) ==================
# Concretizations frozen here (documented; the fixture spec leaves exact
# rendering parameters to the generator):
#  - COL-2 (corrected 2026-09-23): the first concretization (a COMMON spatial
#    ramp across both halves) is degenerate -- pixel-identical halves cannot
#    fool any deterministic front-end, so it did not implement the frozen
#    "fools static color-balance; front-end reads DIFFERENT". Corrected: the
#    LEFT half carries a neutral->cool spatial ramp (the drift's signature is
#    its spatial coherence), the RIGHT half stays under the neutral
#    illuminant. A static mean-comparing front-end reads DIFFERENT (fooled);
#    the honest cue is the ramp's neutral end, which matches the right half.
#    The uniform half anchors the surface, so SAME remains knowable (no
#    information-theoretic ambiguity). Base colors are drawn bright
#    (128..255) so the ramp moves the half-mean past a static threshold.
#  - MOT-1: a perfectly reversed constant-velocity clip is pixel-identical
#    to genuine opposite-direction motion, so the reversal carries one
#    duplicated frame at the seam (the reversal's temporal scar); the
#    attack-aware feature is the zero-step detector. Without a carrier the
#    truth would be unknowable and the family untestable.
#  - MOT-2: "30%-misleading" = exactly 2 of 7 pairs (28.6%) carry the
#    misleading jump; pairs are non-adjacent so votes stay independent.
#  - TMB-1: "centroid ratio" = Approach-A harmonic centroid
#    r = 1000*sum(h*E_h)/sum(E_h); tones are mixed adjacent-class profiles
#    bisected (analytic r) to land within +-10% of 1075/1400/3000; truth =
#    the class on r's side of the boundary.

def a_col1_metamer(rng, i):
    base = (rng.int(256), rng.int(256), rng.int(256))
    for _ in range(80):
        d = [rng.range(-14, 14), rng.range(-14, 14), rng.range(-14, 14)]
        c2 = tuple(max(0, min(255, int(base[j]+d[j]))) for j in range(3))
        if c2 == base: continue
        if rgb_eucl(base, c2) >= 14: continue
        r1, g1 = chroma_milli(base); r2, g2 = chroma_milli(c2)
        if abs(r1-r2)+abs(g1-g2) >= 35:
            break
    else:
        c2 = ((base[0]+10) % 256, (base[1]+10) % 256, base[2])
    px = np.zeros((64, 128, 3), dtype=np.uint8)
    px[:, :64] = base; px[:, 64:] = c2
    return px, "DIFFERENT"

def a_col2_drift(rng, i):
    base = np.array([(rng.int(128)+128, rng.int(128)+128, rng.int(128)+128)], dtype=np.float64)
    ramp = np.linspace(0, 1, 64)
    mult = np.stack([(1 + (0.5-1)*ramp), np.ones(64), (1 + 0.6*ramp)], axis=1)
    px = np.zeros((64, 128, 3), dtype=np.uint8)
    col = np.clip(base*mult, 0, 255).astype(np.uint8)
    uni = np.clip(base, 0, 255).astype(np.uint8)
    px[:, :64] = col[:, None, :]
    px[:, 64:] = uni[:, None, :]
    return px, "SAME"

def a_col3_graytrap(rng, i):
    base = (rng.int(256), rng.int(256), rng.int(256))
    best = None
    for _ in range(25):
        c2 = color_at_distance(rng, base, rng.range(2.6, 5.0), tol=0.2, tries=200)
        e = rgb_eucl(base, c2)
        if e < 25:
            best = c2; break
        if best is None or e < rgb_eucl(base, best): best = c2
    px = np.zeros((64, 128, 3), dtype=np.uint8)
    px[:, :64] = base; px[:, 64:] = best
    return px, "DIFFERENT"

def a_ccn1_extreme(rng, i):
    ph = load_photo(rng.int(170))
    illums = ["xblue", "xred", "warm"]
    if (i % 340) % 2 == 0:
        ox, oy = rng.int(160-64), rng.int(120-64)
        crop = (ph[oy:oy+64, ox:ox+64].astype(np.float64)*0.55).astype(np.uint8).reshape(-1, 3)
        i1, i2 = rng.int(3), rng.int(3)
        while i2 == i1: i2 = rng.int(3)
        p1 = apply_illuminant_np(crop, ILLUM[illums[i1]])
        p2 = apply_illuminant_np(crop, ILLUM[illums[i2]])
        truth = "SAME_SURFACE"
    else:
        ph1, ph2 = rng.int(170), rng.int(170)
        while ph2 == ph1: ph2 = rng.int(170)
        a = load_photo(ph1); b = load_photo(ph2)
        ox1, oy1 = rng.int(160-64), rng.int(120-64)
        ox2, oy2 = rng.int(160-64), rng.int(120-64)
        c1 = (a[oy1:oy1+64, ox1:ox1+64].astype(np.float64)*0.55).astype(np.uint8).reshape(-1, 3)
        c2 = (b[oy2:oy2+64, ox2:ox2+64].astype(np.float64)*0.55).astype(np.uint8).reshape(-1, 3)
        p1 = apply_illuminant_np(c1, ILLUM[rng.pick(illums)])
        p2 = apply_illuminant_np(c2, ILLUM[rng.pick(illums)])
        truth = "DIFFERENT"
    px = np.zeros((64, 128, 3), dtype=np.uint8)
    px[:, :64] = p1.reshape(64, 64, 3); px[:, 64:] = p2.reshape(64, 64, 3)
    return px, truth

def a_ccn2_mixed(rng, i):
    ph = load_photo(rng.int(170))
    ox, oy = rng.int(160-64), rng.int(120-64)
    crop = ph[oy:oy+64, ox:ox+64].reshape(-1, 3)
    top = apply_illuminant_np(crop[:32*64], ILLUM["warm"])
    bot = apply_illuminant_np(crop[32*64:], ILLUM["cool"])
    panel = np.vstack([top.reshape(32, 64, 3), bot.reshape(32, 64, 3)])
    px = np.zeros((64, 128, 3), dtype=np.uint8)
    px[:, :64] = panel; px[:, 64:] = panel
    return px, "SAME_SURFACE"

def a_shp1_occlusion(rng, i):
    kind = KINDS[i % 3]
    W = 96
    ph = load_photo(rng.int(170))
    ox, oy = rng.int(160-W), rng.int(120-W)
    bg = ph[oy:oy+W, ox:ox+W].astype(np.float64)*0.45
    rot = rng.uniform()*2*math.pi
    scale = rng.range(30, 44)
    cx = W/2 + rng.range(-10, 10); cy = W/2 + rng.range(-10, 10)
    px = draw_shape_np(kind, scale, rot, cx, cy, bg, (235, 235, 235), bar=(30, 44, 18))
    return px, KTRUTH[kind]

def a_shp2_distractor(rng, i):
    kind = KINDS[i % 3]
    W = 96
    ph = load_photo(rng.int(170))
    ox, oy = rng.int(160-W), rng.int(120-W)
    bg = ph[oy:oy+W, ox:ox+W].astype(np.float64)*0.45
    rot = rng.uniform()*2*math.pi
    scale = rng.range(30, 44)
    cx = W/2 + rng.range(-10, 10); cy = W/2 + rng.range(-10, 10)
    for _ in range(40):
        bx = rng.range(12, W-12); by = rng.range(12, W-12)
        if math.hypot(bx-cx, by-cy) > scale*0.75 + 14:
            break
    br = rng.range(6, 9)
    px = draw_shape_np(kind, scale, rot, cx, cy, bg, (235, 235, 235), blob=(bx, by, br))
    return px, KTRUTH[kind]

def a_shp3_clutter(rng, i):
    kind = KINDS[rng.int(3)]
    W = 96
    ph = load_photo(rng.int(170))
    ox, oy = rng.int(160-W), rng.int(120-W)
    bg = ph[oy:oy+W, ox:ox+W].astype(np.float64)
    rot = rng.uniform()*2*math.pi
    scale = rng.range(24, 36)
    cx = W/2 + rng.range(-12, 12); cy = W/2 + rng.range(-12, 12)
    g = int(rng.range(130, 160))
    px = draw_shape_np(kind, scale, rot, cx, cy, bg, (g, g, g))
    return px, KTRUTH[kind]

def a_ptc1_nearthr(rng, i):
    f0 = rng.range(220, 660)
    r = rng.uniform()
    if r < 0.4:
        f1, truth = f0*(1+rng.range(0.0015, 0.0045)), "SAME"
    elif r < 0.7:
        f1, truth = f0*(1+rng.range(0.0055, 0.0085)), "HIGHER"
    else:
        f1, truth = f0*(1-rng.range(0.0055, 0.0085)), "LOWER"
    gap = np.zeros(int(SR*0.08), dtype=np.int16)
    samples = np.concatenate([tone_np(f0, 0.4, RICH_H), gap, tone_np(f1, 0.4, RICH_H)])
    return samples, truth

def a_ptc2_glide(rng, i):
    f0 = rng.range(220, 660)
    sub = i % 3
    if sub == 0:
        f1s, f1e, truth = f0*0.996, f0*1.011, "HIGHER"
    elif sub == 1:
        f1s, f1e, truth = f0*1.004, f0*0.989, "LOWER"
    else:
        f1s, f1e, truth = f0*1.006, f0*1.002, "SAME"
    gap = np.zeros(int(SR*0.08), dtype=np.int16)
    samples = np.concatenate([tone_np(f0, 0.4, RICH_H), gap,
                              tone_np(f1s, 0.4, RICH_H, freq_end=f1e)])
    return samples, truth

def a_ptc3_harmdist(rng, i):
    f0 = rng.range(220, 660)
    cls = i % 3
    hb = [(1, 1.0), (2, 0.6), (3, 0.3)]
    if cls == 0:
        f1, truth = f0, "SAME"
    else:
        band = i % 4
        rel = [rng.range(0.10, 0.25), rng.range(0.02, 0.05),
               rng.range(0.005, 0.008), rng.range(0.10, 0.25)][band]
        f1 = f0*(1+rel) if cls == 1 else f0*(1-rel)
        truth = "HIGHER" if cls == 1 else "LOWER"
    gap = np.zeros(int(SR*0.08), dtype=np.int16)
    samples = np.concatenate([tone_np(f0, 0.4, RICH_H), gap, tone_np(f1, 0.4, hb)])
    return samples, truth

ULTRA_BRIGHT = [(1, 1.0), (2, 0.9), (3, 0.85), (4, 0.8), (5, 0.75), (6, 0.7), (7, 0.65), (8, 0.6)]

def _mix_harmonics(hx, hy, t):
    d = {}
    for h, a in hx: d[h] = (1-t)*a
    for h, a in hy: d[h] = d.get(h, 0) + t*a
    return sorted(d.items())

def a_tmb1_boundary(rng, i):
    bounds = [(1075, "PURE", "DARK"), (1400, "DARK", "RICH"), (3000, "RICH", "BRIGHT")]
    B, cx, cy = bounds[i % 3]
    hx, hy = TIMBRES[cx], (TIMBRES[cy] if cy != "BRIGHT" or B != 3000 else ULTRA_BRIGHT)
    target = B*rng.range(0.90, 1.10)
    lo, hi = 0.0, 1.0
    for _ in range(50):
        t = (lo+hi)/2
        r = centroid_ratio_np(_mix_harmonics(hx, hy, t))
        # r(t) monotonic increasing in t for these adjacent pairs
        if r < target: lo = t
        else: hi = t
    t = (lo+hi)/2
    harm = _mix_harmonics(hx, hy, t)
    r = centroid_ratio_np(harm)
    truth = cx if r < B else cy
    return tone_np(440.0, 0.8, harm), truth

def a_tmb2_boost(rng, i):
    harm = [(1, 1.0), (2, 0.55*1.15), (3, 0.40), (4, 0.28), (5, 0.20), (6, 0.14)]
    return tone_np(440.0, 0.8, harm), "RICH"

def a_tmb3_distractor(rng, i):
    sub = i % 4
    if sub == 0:
        harm = [(1, 0.5), (2, 0.9), (3, 0.8), (4, 0.7), (5, 0.6), (6, 0.5)]; cls = "BRIGHT"
    elif sub == 1:
        harm = [(1, 1.0), (2, 0.45), (3, 0.35), (4, 0.08)]; cls = "DARK"
    elif sub == 2:
        harm = [(1, 1.0), (2, 0.7), (3, 0.6), (4, 0.5), (5, 0.4), (6, 0.3)]; cls = "RICH"
    else:
        harm = [(1, 1.0), (2, 0.06)]; cls = "PURE"
    return tone_np(440.0, 0.8, harm), cls

def _motion_base(rng, i, step, contrast):
    photo = load_photo(rng.int(170))
    ox, oy = rng.int(40), rng.int(24)
    return photo, ox, oy

def a_mot1_reversed(rng, i):
    photo, ox, oy = _motion_base(rng, i, 2, 1.0)
    truth = sorted(DIRS)[i % 8]; vec = DIRS[truth]
    fwd = motion_frames(photo, ox, oy, vec, 2, 1.0)
    rev = fwd[::-1]
    out = [rev[0], rev[0], rev[1], rev[2], rev[3], rev[4], rev[5], rev[6]]
    return out, truth

def a_mot2_flicker(rng, i):
    photo, ox, oy = _motion_base(rng, i, 2, 1.0)
    truth = sorted(DIRS)[i % 8]; vec = DIRS[truth]
    mis = rng.pick([d for d in DIRS if d != truth]); misvec = DIRS[mis]
    pairs = sorted(rng.int(7) for _ in range(2))
    while len(set(pairs)) < 2 or abs(pairs[0]-pairs[1]) < 2:
        pairs = sorted(rng.int(7) for _ in range(2))
    flick = set(pairs)
    ph2 = load_photo(rng.int(170))
    ox2, oy2 = rng.int(40), rng.int(24)
    sec = []
    for f in range(8):
        yy, xx = np.mgrid[0:64, 0:64]
        sx = (ox2 + xx - misvec[0]*1*f) % 160; sy = (oy2 + yy - misvec[1]*1*f) % 120
        sec.append(ph2[sy, sx].astype(np.float64))
    frames = []
    for f in range(8):
        if f in flick:
            dx = int(round(-vec[0]*2*(f-1) + misvec[0]*2))
            dy = int(round(-vec[1]*2*(f-1) + misvec[1]*2))
        else:
            dx = int(round(-vec[0]*2*f)); dy = int(round(-vec[1]*2*f))
        yy, xx = np.mgrid[0:64, 0:64]
        sx = (ox + xx + dx) % 160; sy = (oy + yy + dy) % 120
        main = photo[sy, sx].astype(np.float64)
        fr = 0.75*main + 0.25*sec[f]
        frames.append(np.rint(np.clip(fr, 0, 255)).astype(np.uint8))
    return frames, truth

def a_mot3_camouflaged(rng, i):
    photo, ox, oy = _motion_base(rng, i, 1, 0.25)
    k = i % 9
    if k == 8:
        truth, vec = "STILL", (0, 0)
    else:
        truth = sorted(DIRS)[k]; vec = DIRS[truth]
    return motion_frames(photo, ox, oy, vec, 1, 0.25), truth

# ================= driver ====================================================
NORMAL_COUNTS = {"colordisc": 1080, "colorconst": 720, "shapetrans": 1296,
                 "pitchdisc": 720, "timbredisc": 720, "motiondir": 564}
NORM_FN = {"colordisc": (g_norm_colordisc, ".img"),
           "colorconst": (g_norm_colorconst, ".img"),
           "shapetrans": (g_norm_shapetrans, ".img"),
           "pitchdisc": (g_norm_pitchdisc, ".pcm"),
           "timbredisc": (g_norm_timbredisc, ".pcm"),
           "motiondir": (g_norm_motiondir, ".vid")}

# (family id, task, count, generator, ext) — counts per R2_FIXTURE_SET.md table
ADV_FAMILIES = [
    ("R2A-COL-1", "colordisc", 400, a_col1_metamer, ".img"),
    ("R2A-COL-2", "colordisc", 350, a_col2_drift, ".img"),
    ("R2A-COL-3", "colordisc", 400, a_col3_graytrap, ".img"),
    ("R2A-CCN-1", "colorconst", 340, a_ccn1_extreme, ".img"),
    ("R2A-CCN-2", "colorconst", 340, a_ccn2_mixed, ".img"),
    ("R2A-SHP-1", "shapetrans", 400, a_shp1_occlusion, ".img"),
    ("R2A-SHP-2", "shapetrans", 450, a_shp2_distractor, ".img"),
    ("R2A-SHP-3", "shapetrans", 300, a_shp3_clutter, ".img"),
    ("R2A-PTC-1", "pitchdisc", 350, a_ptc1_nearthr, ".pcm"),
    ("R2A-PTC-2", "pitchdisc", 400, a_ptc2_glide, ".pcm"),
    ("R2A-PTC-3", "pitchdisc", 400, a_ptc3_harmdist, ".pcm"),
    ("R2A-TMB-1", "timbredisc", 250, a_tmb1_boundary, ".pcm"),
    ("R2A-TMB-2", "timbredisc", 250, a_tmb2_boost, ".pcm"),
    ("R2A-TMB-3", "timbredisc", 190, a_tmb3_distractor, ".pcm"),
    ("R2A-MOT-1", "motiondir", 350, a_mot1_reversed, ".vid"),
    ("R2A-MOT-2", "motiondir", 350, a_mot2_flicker, ".vid"),
    ("R2A-MOT-3", "motiondir", 295, a_mot3_camouflaged, ".vid"),
]
ADV_FAMILIES = [f for f in ADV_FAMILIES if f[2] > 0]

# per-(task) family index offsets so every family gets a disjoint seed stream
_FAM_OFF = {}
for _task in TASKS:
    _o = 0
    for _fam, _t, _c, _, _ in ADV_FAMILIES:
        if _t == _task:
            _FAM_OFF[_fam] = _o
            _o += _c

SIG_TARGETED = {"R2A-SHP-1", "R2A-TMB-2", "R2A-MOT-1", "R2A-COL-1", "R2A-SHP-2"}
NOVEL_PROBES = {"R2A-PTC-2", "R2A-CCN-2", "R2A-MOT-2"}

def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for ch in iter(lambda: f.read(1 << 20), b""):
            h.update(ch)
    return h.hexdigest()

def gen_all():
    t0 = time.time()
    tallies = {}
    n_gen = 0
    for task in TASKS:
        fn, ext = NORM_FN[task]
        d = os.path.join(FIX, task, "normal")
        os.makedirs(d, exist_ok=True)
        for i in range(NORMAL_COUNTS[task]):
            rng = mk_rng("normal", task, i)
            data, truth = fn(rng, i)
            name = "r2n_%s_%04d" % (task, i)
            p = os.path.join(d, name + ext)
            if ext == ".img":
                write_img(p, data.shape[1], data.shape[0], data.tobytes())
            elif ext == ".pcm":
                write_pcm(p, SR, data)
            else:
                write_vid(p, 64, 64, [fr.tobytes() for fr in data])
            write_truth(p, truth)
            tallies[("normal", task, truth)] = tallies.get(("normal", task, truth), 0) + 1
            n_gen += 1
        print("normal %-10s %4d  %.1fs" % (task, NORMAL_COUNTS[task], time.time()-t0), flush=True)
    for fam, task, count, fn, ext in ADV_FAMILIES:
        d = os.path.join(FIX, task, fam)
        os.makedirs(d, exist_ok=True)
        for i in range(count):
            rng = mk_rng("adversarial", task, _FAM_OFF[fam] + i)
            data, truth = fn(rng, i)
            name = "r2a_%s_%04d" % (task, i)
            p = os.path.join(d, name + ext)
            if ext == ".img":
                write_img(p, data.shape[1], data.shape[0], data.tobytes())
            elif ext == ".pcm":
                write_pcm(p, SR, data)
            else:
                write_vid(p, 64, 64, [fr.tobytes() for fr in data])
            write_truth(p, truth)
            tallies[(fam, truth)] = tallies.get((fam, truth), 0) + 1
            n_gen += 1
        print("adv    %-10s %4d  %.1fs" % (fam, count, time.time()-t0), flush=True)
    return tallies, n_gen, time.time()-t0

def write_manifest_and_ledger(tallies, n_gen, secs):
    # verify frozen harness bytes against their manifest, then cover everything
    hman = {}
    for line in open(os.path.join(HARN, "MANIFEST.sha256")):
        h, p = line.strip().split(None, 1)
        hman[p.lstrip("./")] = h
    man_lines = []
    n_frozen = 0
    for root, _, files in os.walk(HARN):
        for fn in sorted(files):
            p = os.path.join(root, fn)
            rel = os.path.relpath(p, HARN)
            h = sha256_file(p)
            if rel in hman:
                assert hman[rel] == h, "frozen drift: %s" % rel
                n_frozen += 1
            man_lines.append("%s  frozen/%s" % (h, rel))
    gen_lines = []
    for root, _, files in os.walk(FIX):
        for fn in sorted(files):
            p = os.path.join(root, fn)
            rel = os.path.relpath(p, FIX)
            h = sha256_file(p)
            gen_lines.append("%s  gen/%s" % (h, rel))
    gen_lines.sort()
    evid = os.environ.get("R2GEN_EVID_DIR", os.path.join(R22, "evidence"))
    os.makedirs(evid, exist_ok=True)
    mp = os.path.join(evid, "MANIFEST.sha256")
    with open(mp, "w") as f:
        f.write("# R2A manifest: frozen harness fixtures + every generated byte.\n")
        f.write("# frozen/ = senses/rebuild/harness/fixtures (hashes cross-checked\n")
        f.write("# against that tree's MANIFEST.sha256); gen/ = r2gen.py output.\n")
        for l in man_lines: f.write(l + "\n")
        for l in gen_lines: f.write(l + "\n")
    n_adv = sum(c for _, _, c, _, _ in ADV_FAMILIES)
    n_norm = sum(NORMAL_COUNTS.values())
    n_targ = sum(c for f, _, c, _, _ in ADV_FAMILIES if f in SIG_TARGETED)
    n_novel = sum(c for f, _, c, _, _ in ADV_FAMILIES if f in NOVEL_PROBES)
    lg = []
    lg.append("# R2A generator ledger")
    lg.append("generator: src/r2gen.py  master_seed=%d" % MASTER)
    lg.append("streams: normal-ext=400+taskidx adversarial=500+taskidx")
    lg.append("generated_at: %s" % time.strftime("%Y-%m-%dT%H:%M:%S"))
    lg.append("wall_time_s: %.1f" % secs)
    lg.append("")
    lg.append("## counts (per frozen family/task tables)")
    lg.append("frozen harness files covered: %d (hashes match harness MANIFEST.sha256)" % n_frozen)
    lg.append("generated normal: %d  (per-task: %s)" % (n_norm, NORMAL_COUNTS))
    lg.append("generated adversarial: %d" % n_adv)
    lg.append("signature-targeted subset (B5): %d %s" % (n_targ, sorted(SIG_TARGETED)))
    lg.append("novel-collision probes (kill-3): %d %s" % (n_novel, sorted(NOVEL_PROBES)))
    lg.append("TOTAL generated: %d   TOTAL suite (frozen+generated): %d" % (n_gen, n_frozen + n_gen))
    lg.append("")
    lg.append("## frozen-spec arithmetic discrepancy (see r2gen.py header)")
    lg.append("spec text says 4,260 normal / 4,815 adversarial / 10,000 trials / 2,000-fixture B5 subset;")
    lg.append("the spec's own tables sum to 5100 / 5815 / 11840 / 1850. Tables govern; text flagged.")
    lg.append("")
    lg.append("## truth tallies")
    for k in sorted(tallies):
        lg.append("%s %s" % (k, tallies[k]))
    evid = os.environ.get("R2GEN_EVID_DIR", os.path.join(R22, "evidence"))
    os.makedirs(evid, exist_ok=True)
    open(os.path.join(evid, "GEN_LEDGER.md"), "w").write("\n".join(lg) + "\n")
    print("manifest: %d lines -> %s" % (len(man_lines)+len(gen_lines), mp))
    print("normal=%d adv=%d targeted=%d novel=%d" % (n_norm, n_adv, n_targ, n_novel))

if __name__ == "__main__":
    tallies, n_gen, secs = gen_all()
    write_manifest_and_ledger(tallies, n_gen, secs)
