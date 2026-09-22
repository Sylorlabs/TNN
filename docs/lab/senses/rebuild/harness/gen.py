#!/usr/bin/env python3
"""TNN senses-rebuild fixture generator — HARNESS-CREW.

Deterministic: every random draw comes from splitmix64(MASTER_SEED ^ stream).
No wall-clock, no os.urandom. Regenerating with the same code + photos yields
byte-identical fixtures.

Seeds (documented, frozen):
  MASTER_SEED = 20260921
  stream ids: photo pool = 11, per-task primary = 100+task, noise = 200+task,
  adversarial = 300+task. Fixture index mixes into every draw so each fixture
  is reproducible in isolation.
"""
import math, os, struct, sys, time, urllib.request

MASTER_SEED = 20260921
ROOT = os.path.dirname(os.path.abspath(__file__))
FIX = os.path.join(ROOT, "fixtures")
PHOTOS = os.path.join(FIX, "_photos")

TASKS = ["colordisc", "colorconst", "shapetrans", "pitchdisc", "timbredisc", "motiondir"]

# ---------------------------------------------------------------- PRNG
MASK64 = (1 << 64) - 1
def splitmix64(state):
    state = (state + 0x9E3779B97F4A7C15) & MASK64
    z = state
    z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & MASK64
    z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & MASK64
    z = z ^ (z >> 31)
    return z

class Rng:
    def __init__(self, seed):
        self.s = seed & MASK64
    def u64(self):
        self.s = (self.s + 0x9E3779B97F4A7C15) & MASK64
        z = self.s
        z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & MASK64
        z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & MASK64
        return z ^ (z >> 31)
    def uniform(self):
        return (self.u64() >> 11) * (1.0 / (1 << 53))
    def range(self, lo, hi):
        return lo + (hi - lo) * self.uniform()
    def int(self, n):
        return self.u64() % n
    def pick(self, seq):
        return seq[self.u64() % len(seq)]

def stream_seed(master, stream, index):
    h = splitmix64(master ^ (stream * 0x9E3779B97F4A7C15))
    return splitmix64(h ^ (index * 0xBF58476D1CE4E5B9))

# ------------------------------------------------------- color math
def srgb_to_linear(c):
    c /= 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

def linear_to_srgb(c):
    c = max(0.0, min(1.0, c))
    v = 12.92 * c if c <= 0.0031308 else 1.055 * (c ** (1.0 / 2.4)) - 0.055
    return int(round(max(0.0, min(1.0, v)) * 255))

XYZ_M = ((0.4124564, 0.3575761, 0.1804375),
         (0.2126729, 0.7151522, 0.0721750),
         (0.0193339, 0.1191920, 0.9503041))
XYZ_MI = (( 3.2404542, -1.5371385, -0.4985314),
          (-0.9692660,  1.8760108,  0.0415560),
          ( 0.0556434, -0.2040259,  1.0572252))
BRAD = ((0.8951, 0.2664, -0.1614),
        (-0.7502, 1.7135, 0.0367),
        (0.0389, -0.0685, 1.0296))
BRAD_I = ((0.9869929, -0.1470543, 0.1599627),
          (0.4323053, 0.5183603, 0.0492912),
          (-0.0085287, 0.0400428, 0.9684867))

def rgb_to_xyz(r, g, b):
    rl, gl, bl = srgb_to_linear(r), srgb_to_linear(g), srgb_to_linear(b)
    return tuple(XYZ_M[i][0]*rl + XYZ_M[i][1]*gl + XYZ_M[i][2]*bl for i in range(3))

def xyz_to_lab(x, y, z):
    xn, yn, zn = 0.95047, 1.0, 1.08883
    def f(t):
        return t ** (1/3) if t > 0.008856 else 7.787 * t + 16/116
    fx, fy, fz = f(x/xn), f(y/yn), f(z/zn)
    return (116*fy - 16, 500*(fx - fy), 200*(fy - fz))

def rgb_to_lab(r, g, b):
    return xyz_to_lab(*rgb_to_xyz(r, g, b))

def delta_e_2000(lab1, lab2):
    L1, a1, b1 = lab1; L2, a2, b2 = lab2
    kL = kC = kH = 1.0
    C1 = math.hypot(a1, b1); C2 = math.hypot(a2, b2)
    Cb = (C1 + C2) / 2
    G = 0.5 * (1 - math.sqrt(Cb**7 / (Cb**7 + 25**7)))
    ap1 = (1 + G) * a1; ap2 = (1 + G) * a2
    Cp1 = math.hypot(ap1, b1); Cp2 = math.hypot(ap2, b2)
    def hp(ap, b):
        if ap == 0 and b == 0: return 0.0
        h = math.degrees(math.atan2(b, ap))
        return h + 360 if h < 0 else h
    hp1, hp2 = hp(ap1, b1), hp(ap2, b2)
    dL = L2 - L1; dC = Cp2 - Cp1
    if Cp1 * Cp2 == 0:
        dh = 0.0
    else:
        dh = hp2 - hp1
        if dh > 180: dh -= 360
        elif dh < -180: dh += 360
    dH = 2 * math.sqrt(Cp1 * Cp2) * math.sin(math.radians(dh / 2))
    Lbp = (L1 + L2) / 2; Cbp = (Cp1 + Cp2) / 2
    if Cp1 * Cp2 == 0:
        hbp = hp1 + hp2
    else:
        hbp = (hp1 + hp2) / 2 if abs(hp1 - hp2) <= 180 else (hp1 + hp2 + 360) / 2 if hp1 + hp2 < 360 else (hp1 + hp2 - 360) / 2
    T = (1 - 0.17*math.cos(math.radians(hbp-30)) + 0.24*math.cos(math.radians(2*hbp))
         + 0.32*math.cos(math.radians(3*hbp+6)) - 0.20*math.cos(math.radians(4*hbp-63)))
    dRo = 30 * math.exp(-((hbp - 275) / 25) ** 2)
    Rc = 2 * math.sqrt(Cbp**7 / (Cbp**7 + 25**7))
    Sl = 1 + 0.015 * (Lbp - 50) ** 2 / math.sqrt(20 + (Lbp - 50) ** 2)
    Sc = 1 + 0.045 * Cbp
    Sh = 1 + 0.015 * Cbp * T
    Rt = -math.sin(math.radians(2 * dRo)) * Rc
    return math.sqrt((dL/(kL*Sl))**2 + (dC/(kC*Sc))**2 + (dH/(kH*Sh))**2 + Rt*(dC/(kC*Sc))*(dH/(kH*Sh)))

# Illuminants as white-point XYZ (D65 neutral, A warm, F2 cool, + 2 extreme)
ILLUM = {
    "d65":  (0.95047, 1.00000, 1.08883),
    "warm": (1.09850, 1.00000, 0.35585),   # illuminant A
    "cool": (0.99180, 1.00000, 0.67390),   # F2-ish
    "xblue": (0.62000, 0.85000, 1.75000),  # adversarial: extreme blue cast
    "xred":  (1.70000, 0.90000, 0.45000),  # adversarial: extreme red cast
}

def apply_illuminant(rgb, illum_xyz):
    """von-Kries chromatic adaptation: render rgb (captured under D65) as seen
    under the target illuminant. Real color math, Bradford CAT."""
    x, y, z = rgb_to_xyz(*rgb)
    src = (0.95047, 1.0, 1.08883)
    lms_s = [sum(BRAD[i][j]*v for j, v in enumerate((x, y, z))) for i in range(3)]
    lms_wsrc = [sum(BRAD[i][j]*v for j, v in enumerate(src)) for i in range(3)]
    lms_wdst = [sum(BRAD[i][j]*v for j, v in enumerate(illum_xyz)) for i in range(3)]
    lms = [lms_s[i] * lms_wdst[i] / lms_wsrc[i] for i in range(3)]
    xa = sum(BRAD_I[0][j]*lms[j] for j in range(3))
    ya = sum(BRAD_I[1][j]*lms[j] for j in range(3))
    za = sum(BRAD_I[2][j]*lms[j] for j in range(3))
    rl = XYZ_MI[0][0]*xa + XYZ_MI[0][1]*ya + XYZ_MI[0][2]*za
    gl = XYZ_MI[1][0]*xa + XYZ_MI[1][1]*ya + XYZ_MI[1][2]*za
    bl = XYZ_MI[2][0]*xa + XYZ_MI[2][1]*ya + XYZ_MI[2][2]*za
    return (linear_to_srgb(rl), linear_to_srgb(gl), linear_to_srgb(bl))

# ------------------------------------------------------- binary writers
def _flat(px):
    out = bytearray()
    for p in px:
        if isinstance(p, (tuple, list)):
            out.extend(p)
        else:
            out.append(p)
    return bytes(out)

def write_img(path, w, h, px):
    with open(path, "wb") as f:
        f.write(struct.pack("<II", w, h))
        f.write(_flat(px))

def write_pcm(path, rate, samples):
    with open(path, "wb") as f:
        f.write(struct.pack("<II", rate, len(samples)))
        f.write(struct.pack("<%dh" % len(samples), *samples))

def write_vid(path, w, h, frames):
    with open(path, "wb") as f:
        f.write(struct.pack("<III", len(frames), w, h))
        for fr in frames:
            f.write(_flat(fr))

def write_truth(path, value):
    with open(path + ".truth", "w") as f:
        f.write("truth=%s\n" % value)

# ------------------------------------------------------- photo pool
def fetch_photos(n=170):
    os.makedirs(PHOTOS, exist_ok=True)
    have = 0
    for i in range(n):
        p = os.path.join(PHOTOS, "ph%03d.jpg" % i)
        if os.path.exists(p) and os.path.getsize(p) > 500:
            have += 1
            continue
        url = "https://picsum.photos/seed/tnnsr%d/160/120" % i
        ok = False
        for attempt in range(4):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "tnn-lab/1.0"})
                with urllib.request.urlopen(req, timeout=25) as r:
                    data = r.read()
                if len(data) > 2000 and data[:2] == b"\xff\xd8":
                    with open(p, "wb") as f:
                        f.write(data)
                    ok = True
                    break
            except Exception as e:
                time.sleep(1.5)
        if ok:
            have += 1
        time.sleep(0.25)
    return have

_photo_cache = {}
def load_photo(i, w=160, h=120):
    from PIL import Image
    if i in _photo_cache:
        return _photo_cache[i]
    p = os.path.join(PHOTOS, "ph%03d.jpg" % i)
    im = Image.open(p).convert("RGB")
    if im.size != (w, h):
        im = im.resize((w, h))
    px = list(im.getdata())
    _photo_cache[i] = px
    return px

def crop_photo(photo, pw, ox, oy, w, h):
    return [photo[(oy+y)*pw + (ox+x)] for y in range(h) for x in range(w)]

# ------------------------------------------------------- T1 colordisc
# 128x64: two 64x64 patches. Truth boundary: SAME iff dE2000 < 2.3 (JND).
def _rand_color(rng):
    return (rng.int(256), rng.int(256), rng.int(256))

def _color_at_distance(rng, base, target_de, tol=0.15, tries=400):
    """Find a color at ~target_de dE2000 from base by Lab-space walking."""
    L0, a0, b0 = rgb_to_lab(*base)
    best = None
    for _ in range(tries):
        ang = rng.uniform() * 2 * math.pi
        # Lab step sized from target: larger steps for larger targets
        step = target_de * rng.range(0.35, 0.7)
        L1 = max(0.0, min(100.0, L0 + step * math.cos(ang) * rng.range(0.4, 1.0)))
        C = step * math.sin(ang)
        a1 = a0 + C * math.cos(rng.uniform() * 2 * math.pi)
        b1 = b0 + C * math.sin(rng.uniform() * 2 * math.pi)
        # Lab -> sRGB approx: go via XYZ inverse (simple iterative clamp)
        rgb = _lab_to_srgb(L1, a1, b1)
        de = delta_e_2000((L0, a0, b0), rgb_to_lab(*rgb))
        if abs(de - target_de) / target_de < tol:
            return rgb
        if best is None or abs(de - target_de) < abs(best[0] - target_de):
            best = (de, rgb)
    return best[1]

def _lab_to_srgb(L, a, b):
    xn, yn, zn = 0.95047, 1.0, 1.08883
    fy = (L + 16) / 116.0
    fx = fy + a / 500.0
    fz = fy - b / 200.0
    def fi(t):
        return t**3 if t**3 > 0.008856 else (t - 16/116) / 7.787
    x, y, z = xn*fi(fx), yn*fi(fy), zn*fi(fz)
    rl = XYZ_MI[0][0]*x + XYZ_MI[0][1]*y + XYZ_MI[0][2]*z
    gl = XYZ_MI[1][0]*x + XYZ_MI[1][1]*y + XYZ_MI[1][2]*z
    bl = XYZ_MI[2][0]*x + XYZ_MI[2][1]*y + XYZ_MI[2][2]*z
    return (linear_to_srgb(rl), linear_to_srgb(gl), linear_to_srgb(bl))

def _patch_img(c1, c2):
    px = []
    for y in range(64):
        for x in range(128):
            px.append(c1 if x < 64 else c2)
    return px

def gen_t1(task_i, variant, idx):
    rng = Rng(stream_seed(MASTER_SEED, 100 + task_i * 10 + (0 if variant == "primary" else 1 if variant == "noise" else 2), idx))
    d = os.path.join(FIX, "t1_colordisc", variant)
    os.makedirs(d, exist_ok=True)
    name = "p%03d" % idx
    if variant == "primary":
        if idx < 20:  # SAME: 10 identical, 10 near-identical
            base = _rand_color(rng)
            c2 = base if idx < 10 else _color_at_distance(rng, base, rng.range(0.4, 1.6))
            truth = "SAME"
        else:  # DIFFERENT, graded
            k = idx - 20
            base = _rand_color(rng)
            if k < 14: de = rng.range(10, 28)      # easy
            elif k < 27: de = rng.range(4, 10)      # medium
            else: de = rng.range(2.4, 4.0)          # hard
            c2 = _color_at_distance(rng, base, de)
            truth = "DIFFERENT"
    else:  # adversarial: straddle the 2.3 boundary
        base = _rand_color(rng)
        if idx < 15:
            c2 = _color_at_distance(rng, base, rng.range(1.6, 2.25)); truth = "SAME"
        else:
            c2 = _color_at_distance(rng, base, rng.range(2.35, 3.2)); truth = "DIFFERENT"
    path = os.path.join(d, name + ".img")
    write_img(path, 128, 64, _patch_img(base, c2))
    write_truth(path, truth)
    return truth

# ------------------------------------------------------- T2 colorconst
# 128x64: two 64x64 photo panels. SAME_SURFACE iff same photo.
ILLUM_TRIO = ["d65", "warm", "cool"]
def _render_panel(photo, illum, exposure=1.0):
    out = []
    xyz = ILLUM[illum]
    for (r, g, b) in photo:
        if exposure != 1.0:
            r = min(255, int(r * exposure)); g = min(255, int(g * exposure)); b = min(255, int(b * exposure))
        out.append(apply_illuminant((r, g, b), xyz))
    return out

def gen_t2(task_i, variant, idx, photo_count):
    rng = Rng(stream_seed(MASTER_SEED, 100 + task_i * 10 + (0 if variant == "primary" else 2), idx))
    d = os.path.join(FIX, "t2_colorconst", variant)
    os.makedirs(d, exist_ok=True)
    name = "p%03d" % idx
    adv = variant == "adversarial"
    illums = ILLUM_TRIO if not adv else ["xblue", "xred", "warm"]
    if idx % 2 == 0:  # SAME_SURFACE
        ph = rng.int(photo_count)
        ox, oy = rng.int(160 - 64), rng.int(120 - 64)
        crop = crop_photo(load_photo(ph), 160, ox, oy, 64, 64)
        i1, i2 = rng.int(3), rng.int(3)
        while i2 == i1: i2 = rng.int(3)
        p1 = _render_panel(crop, illums[i1], 0.55 if adv else 1.0)
        p2 = _render_panel(crop, illums[i2], 0.55 if adv else 1.0)
        truth = "SAME_SURFACE"
    else:  # DIFFERENT surfaces
        ph1, ph2 = rng.int(photo_count), rng.int(photo_count)
        while ph2 == ph1: ph2 = rng.int(photo_count)
        c1 = crop_photo(load_photo(ph1), 160, rng.int(160-64), rng.int(120-64), 64, 64)
        c2 = crop_photo(load_photo(ph2), 160, rng.int(160-64), rng.int(120-64), 64, 64)
        p1 = _render_panel(c1, rng.pick(illums), 0.55 if adv else 1.0)
        p2 = _render_panel(c2, rng.pick(illums), 0.55 if adv else 1.0)
        truth = "DIFFERENT"
    px = []
    for y in range(64):
        for x in range(128):
            px.append(p1[y*64+x] if x < 64 else p2[y*64+(x-64)])
    path = os.path.join(d, name + ".img")
    write_img(path, 128, 64, px)
    write_truth(path, truth)
    return truth

# ------------------------------------------------------- T3 shapetrans
# 96x96: anti-aliased shape (supersampled rasterization) on photo background.
def _point_in_shape(kind, x, y):
    # shapes defined in unit space centered at origin, size ~1.0
    if kind == "circle":
        return x*x + y*y <= 0.25
    if kind == "square":
        return abs(x) <= 0.5 and abs(y) <= 0.5
    # triangle: equilateral, centroid at origin, circumradius 0.62
    R = 0.62
    verts = []
    for k in range(3):
        a = math.pi/2 + k * 2*math.pi/3
        verts.append((R*math.cos(a), -R*math.sin(a)))
    def sign(p1, p2, p3):
        return (p1[0]-p3[0])*(p2[1]-p3[1]) - (p2[0]-p3[0])*(p1[1]-p3[1])
    d1 = sign((x,y), verts[0], verts[1]); d2 = sign((x,y), verts[1], verts[2]); d3 = sign((x,y), verts[2], verts[0])
    neg = (d1 < 0) or (d2 < 0) or (d3 < 0); pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
    return not (neg and pos)

def gen_t3(task_i, variant, idx, photo_count):
    rng = Rng(stream_seed(MASTER_SEED, 100 + task_i * 10 + (0 if variant == "primary" else 2), idx))
    d = os.path.join(FIX, "t3_shapetrans", variant)
    os.makedirs(d, exist_ok=True)
    name = "p%03d" % idx
    adv = variant == "adversarial"
    kinds = ["circle", "triangle", "square"]
    kind = kinds[idx % 3] if not adv else kinds[rng.int(3)]
    W = 96
    # background: photographic, dimmed (primary) or full-strength clutter (adv)
    crop = crop_photo(load_photo(rng.int(photo_count)), 160,
                      rng.int(160 - W), rng.int(120 - W), W, W)
    dim = 0.45 if not adv else 1.0
    bg_px = [tuple(int(c*dim) for c in p) for p in crop]
    # shape params
    rot = rng.uniform() * 2*math.pi
    scale = rng.range(30, 44) if not adv else rng.range(16, 26)
    cx = W/2 + rng.range(-14, 14); cy = W/2 + rng.range(-14, 14)
    fg = (235, 235, 235) if not adv else tuple(int(rng.range(120, 175)) for _ in range(3))
    occl = adv and (idx % 3 == 0)  # occlusion bar on some adversarial
    cosr, sinr = math.cos(rot), math.sin(rot)
    px = []
    SS = 3
    for y in range(W):
        for x in range(W):
            bgc = bg_px[y*W + x]
            hit = 0
            for sy in range(SS):
                for sx in range(SS):
                    fx = x + (sx + 0.5)/SS - 0.5 - cx
                    fy = y + (sy + 0.5)/SS - 0.5 - cy
                    ux = (fx*cosr + fy*sinr) / scale
                    uy = (-fx*sinr + fy*cosr) / scale
                    if _point_in_shape(kind, ux, uy):
                        hit += 1
            a = hit / (SS*SS)
            col = tuple(int(fg[i]*a + bgc[i]*(1-a)) for i in range(3))
            if occl and 30 <= y <= 44:
                col = tuple(min(255, int(bgc[i]*0.9 + 40)) for i in range(3))
            px.append(col)
    path = os.path.join(d, name + ".img")
    write_img(path, W, W, px)
    truth = {"circle": "CIRCLE", "triangle": "TRIANGLE", "square": "SQUARE"}[kind]
    write_truth(path, truth)
    return truth

# ------------------------------------------------------- audio synthesis
SR = 16000
def _tone(freq, dur, harmonics, amp=0.75):
    """harmonics: list of (multiple, amplitude). Raised-cosine 20ms ramps."""
    n = int(SR * dur)
    out = [0.0] * n
    for k, a in harmonics:
        w = 2 * math.pi * freq * k / SR
        for i in range(n):
            out[i] += a * math.sin(w * i)
    ramp = int(SR * 0.02)
    for i in range(ramp):
        e = 0.5 - 0.5 * math.cos(math.pi * i / ramp)
        out[i] *= e; out[n-1-i] *= e
    peak = max(1e-9, max(abs(v) for v in out))
    g = amp / peak
    return [int(max(-32768, min(32767, round(v * g * 32767)))) for v in out]

RICH_H = [(1, 1.0), (2, 0.30), (3, 0.15)]

# ------------------------------------------------------- T4 pitchdisc
# two 0.4s tones, 0.08s gap. SAME iff |df|/f < 0.005 (0.5% pitch JND).
def gen_t4(task_i, variant, idx):
    rng = Rng(stream_seed(MASTER_SEED, 100 + task_i * 10 + (0 if variant == "primary" else 2), idx))
    d = os.path.join(FIX, "t4_pitchdisc", variant)
    os.makedirs(d, exist_ok=True)
    name = "p%03d" % idx
    f0 = rng.range(220, 660)
    if variant == "primary":
        cls = idx % 3  # 0 SAME, 1 HIGHER, 2 LOWER
        if cls == 0:
            f1 = f0; truth = "SAME"
        else:
            band = idx % 4
            rel = [rng.range(0.10, 0.25), rng.range(0.02, 0.05), rng.range(0.005, 0.008), rng.range(0.10, 0.25)][band]
            f1 = f0 * (1 + rel) if cls == 1 else f0 * (1 - rel)
            truth = "HIGHER" if cls == 1 else "LOWER"
    else:  # adversarial: near-threshold straddling 0.5%
        r = rng.uniform()
        if r < 0.4:
            f1 = f0 * (1 + rng.range(0.001, 0.0045)); truth = "SAME"
        elif r < 0.7:
            f1 = f0 * (1 + rng.range(0.0055, 0.009)); truth = "HIGHER"
        else:
            f1 = f0 * (1 - rng.range(0.0055, 0.009)); truth = "LOWER"
    gap = [0] * int(SR * 0.08)
    samples = _tone(f0, 0.4, RICH_H) + gap + _tone(f1, 0.4, RICH_H)
    path = os.path.join(d, name + ".pcm")
    write_pcm(path, SR, samples)
    write_truth(path, truth)
    return truth

# ------------------------------------------------------- T5 timbredisc
# single 0.8s tone at 440Hz. Classes by harmonic profile (spectral centroid).
TIMBRES = {
    "PURE":   [(1, 1.0)],
    "BRIGHT": [(1, 1.0), (2, 0.80), (3, 0.65), (4, 0.55), (5, 0.45), (6, 0.38), (7, 0.32), (8, 0.28)],
    "DARK":   [(1, 1.0), (2, 0.40), (3, 0.10), (4, 0.03)],
    "RICH":   [(1, 1.0), (2, 0.55), (3, 0.40), (4, 0.28), (5, 0.20), (6, 0.14)],
}
def gen_t5(task_i, variant, idx):
    rng = Rng(stream_seed(MASTER_SEED, 100 + task_i * 10 + (0 if variant == "primary" else 2), idx))
    d = os.path.join(FIX, "t5_timbredisc", variant)
    os.makedirs(d, exist_ok=True)
    name = "p%03d" % idx
    if variant == "primary":
        cls = ["PURE", "BRIGHT", "DARK", "RICH"][idx % 4]
        harm = TIMBRES[cls]
    else:  # adversarial: distractor harmonics straddling class boundaries
        r = rng.uniform()
        if r < 0.25:   # BRIGHT with weak fundamental (distractor)
            harm = [(1, 0.5), (2, 0.9), (3, 0.8), (4, 0.7), (5, 0.6), (6, 0.5)]; cls = "BRIGHT"
        elif r < 0.5:  # DARK with extra 3rd (distractor)
            harm = [(1, 1.0), (2, 0.45), (3, 0.35), (4, 0.08)]; cls = "DARK"
        elif r < 0.75:  # RICH pushed bright
            harm = [(1, 1.0), (2, 0.7), (3, 0.6), (4, 0.5), (5, 0.4), (6, 0.3)]; cls = "RICH"
        else:          # near-PURE with faint 2nd
            harm = [(1, 1.0), (2, 0.06)]; cls = "PURE"
    samples = _tone(440.0, 0.8, harm)
    path = os.path.join(d, name + ".pcm")
    write_pcm(path, SR, samples)
    write_truth(path, cls)
    return cls

# ------------------------------------------------------- T6 motiondir
# 8 frames 64x64: photo window translated 2px/frame (adv: 1px, low contrast).
DIRS = {"N": (0,-1), "NE": (1,-1), "E": (1,0), "SE": (1,1),
        "S": (0,1), "SW": (-1,1), "W": (-1,0), "NW": (-1,-1)}
def gen_t6(task_i, variant, idx, photo_count):
    rng = Rng(stream_seed(MASTER_SEED, 100 + task_i * 10 + (0 if variant == "primary" else 2), idx))
    d = os.path.join(FIX, "t6_motiondir", variant)
    os.makedirs(d, exist_ok=True)
    name = "p%03d" % idx
    adv = variant == "adversarial"
    if variant == "primary":
        if idx < 4:
            truth, vec = "STILL", (0, 0)
        else:
            truth = sorted(DIRS)[(idx - 4) % 8]; vec = DIRS[truth]
    else:
        truth = rng.pick(sorted(DIRS) + ["STILL"]); vec = DIRS.get(truth, (0, 0))
    photo = load_photo(rng.int(photo_count))
    W = 64
    step = 1 if adv else 2
    contrast = 0.25 if adv else 1.0
    mean = [0, 0, 0]
    for p in photo:
        for i in range(3): mean[i] += p[i]
    mean = [m / len(photo) for m in mean]
    ox, oy = rng.int(40), rng.int(24)
    frames = []
    for f in range(8):
        # sampling window moves OPPOSITE to vec so the visible content
        # translates in the labeled direction (screen coords, +y down)
        dx = int(round(-vec[0] * step * f)); dy = int(round(-vec[1] * step * f))
        fr = []
        for y in range(W):
            for x in range(W):
                sx = (ox + x + dx) % 160; sy = (oy + y + dy) % 120
                r, g, b = photo[sy*160 + sx]
                fr.append(tuple(int(max(0, min(255, mean[i] + (c - mean[i]) * contrast)))
                               for i, c in enumerate((r, g, b))))
        frames.append(fr)
    path = os.path.join(d, name + ".vid")
    write_vid(path, W, W, frames)
    write_truth(path, truth)
    return truth

# ------------------------------------------------------- noise variants
# Deterministic precomputed noise baked into fixture files. Stream = 200+task.
def _add_noise_bytes(data, rng, amp):
    out = bytearray(len(data))
    for i, v in enumerate(data):
        n = int(rng.uniform() * (2*amp + 1)) - amp
        out[i] = max(0, min(255, v + n))
    return bytes(out)

def gen_noise(task, task_i, idx, ext):
    rng = Rng(stream_seed(MASTER_SEED, 200 + task_i * 10, idx))
    src = os.path.join(FIX, task, "primary", "p%03d%s" % (idx, ext))
    dst_d = os.path.join(FIX, task, "noise")
    os.makedirs(dst_d, exist_ok=True)
    dst = os.path.join(dst_d, "p%03d%s" % (idx, ext))
    with open(src, "rb") as f:
        raw = f.read()
    truth_v = open(src + ".truth").read().strip().split("=")[1]
    if ext == ".pcm":
        rate, count = struct.unpack("<II", raw[:8])
        samps = struct.unpack("<%dh" % count, raw[8:8+2*count])
        noisy = []
        for s in samps:
            n = int(rng.uniform() * 601) - 300
            noisy.append(max(-32768, min(32767, s + n)))
        with open(dst, "wb") as f:
            f.write(struct.pack("<II", rate, count))
            f.write(struct.pack("<%dh" % count, *noisy))
    else:
        # header 8 (.img) or 12 (.vid) bytes preserved, payload noised
        hlen = 8 if ext == ".img" else 12
        head, payload = raw[:hlen], raw[hlen:]
        with open(dst, "wb") as f:
            f.write(head)
            f.write(_add_noise_bytes(payload, rng, 8))
    write_truth(dst, truth_v)
    return truth_v

# ------------------------------------------------------- main
COUNTS = {"primary": [60, 40, 90, 60, 60, 60],
          "noise":   [60, 40, 90, 60, 60, 60],
          "adversarial": [30, 20, 45, 30, 30, 30]}
DIRS_T = ["t1_colordisc", "t2_colorconst", "t3_shapetrans",
          "t4_pitchdisc", "t5_timbredisc", "t6_motiondir"]
EXTS = {0: ".img", 1: ".img", 2: ".img", 3: ".pcm", 4: ".pcm", 5: ".vid"}

def main():
    print("fetching photo pool...", flush=True)
    n = fetch_photos(170)
    print("photos cached: %d" % n, flush=True)
    if n < 60:
        print("FATAL: photo pool too small", flush=True); sys.exit(1)
    inv = {}
    for ti, tdir in enumerate(DIRS_T):
        inv[tdir] = {}
        for variant in ("primary", "noise", "adversarial"):
            cnt = COUNTS[variant][ti]
            truths = {}
            for idx in range(cnt):
                if variant == "primary":
                    if ti == 0: t = gen_t1(ti, variant, idx)
                    elif ti == 1: t = gen_t2(ti, variant, idx, n)
                    elif ti == 2: t = gen_t3(ti, variant, idx, n)
                    elif ti == 3: t = gen_t4(ti, variant, idx)
                    elif ti == 4: t = gen_t5(ti, variant, idx)
                    else: t = gen_t6(ti, variant, idx, n)
                elif variant == "noise":
                    t = gen_noise(tdir, ti, idx, EXTS[ti])
                else:
                    if ti == 0: t = gen_t1(ti, variant, idx)
                    elif ti == 1: t = gen_t2(ti, variant, idx, n)
                    elif ti == 2: t = gen_t3(ti, variant, idx, n)
                    elif ti == 3: t = gen_t4(ti, variant, idx)
                    elif ti == 4: t = gen_t5(ti, variant, idx)
                    else: t = gen_t6(ti, variant, idx, n)
                truths[t] = truths.get(t, 0) + 1
            inv[tdir][variant] = (cnt, truths)
            print("%s/%s: %d  %s" % (tdir, variant, cnt, truths), flush=True)
    total = sum(c for v in inv.values() for c, _ in v.values())
    print("TOTAL fixtures: %d" % total, flush=True)

if __name__ == "__main__":
    main()
