#!/usr/bin/env python3
"""PAM ROUND 2 — fixture suite R2A generator (preregistered instrument).

Generates the frozen R2A pool per round2/preregs/R2_FIXTURE_SET.md:
  normal:      740 frozen harness fixtures (referenced, not regenerated)
               + generated r2n_<task>_<i>  (stream 400+taskidx)
  adversarial: 185 frozen harness fixtures (referenced, not regenerated)
               + generated r2a_<task>_<i>  (stream 500+taskidx), 18 families

MASTER seed = 20260923 (new; round 1 used 20260922).
Per-fixture seed = splitmix64(splitmix64(MASTER ^ stream*0x9E3779B97F4A7C15)
                              ^ index*0xBF58476D1CE4E5B9)
  -- the same construction as harness/gen.py stream_seed().

Each fixture is one container file:
  magic "R2A1" | u32 taskidx | u32 f_len | F bytes | u32 g_len | G bytes
F = formation-evidence span (possibly corrupted per attack family).
G = disjoint-evidence span, declared clean per the frozen per-task
    disjoint-span declarations (temporal later-window for color/audio/motion,
    spatial non-overlapping quadrant for shapetrans).
Sibling <id>.r2a.truth holds truth=<judgment> from the TRUE stimulus.

Span encodings (raw, fixed per task):
  colordisc : F 64x32x3 RGB (two 32x32 patches) | G 32x16x3 RGB
  colorconst: F 64x32x3 RGB (two 32x32 panels)  | G 32x16x3 RGB
  shapetrans: F 48x48x3 RGB                    | G 24x24x3 RGB (target quadrant)
  pitchdisc : F 2160 int16 LE @4kHz (2x0.25s tones+0.04s gap)
              G 2160 int16 LE @4kHz (clean re-synthesis, same freqs)
  timbredisc: F 2000 int16 LE @8kHz (0.5s @440Hz)
              G 2000 int16 LE @8kHz (clean re-synthesis)
  motiondir : F 8 frames 24x24 gray bytes | G 8 frames 24x24 gray (clean)

Counts (explicit per-task / per-family numbers from R2_FIXTURE_SET.md):
  normal/adversarial generated per task and the 18 family counts are taken
  EXACTLY as written. NOTE: the spec's prose totals (5,000/5,000/10,000) do
  not match its own per-task sums (normal per-task sums to 5,100; the 18
  family counts sum to 5,815). The explicit per-task/family counts govern;
  actual frozen N = 925 + 5,100 + 5,815 = 11,840 trials (>=10,000 and
  >=30% adversarial per HC-1's kill bar as written). All bars in PREREG_R2-1
  are percentages and are applied on the actual frozen N. This deviation is
  documented here and in the fork's VERDICT.

Glue only: this script never judges. Deterministic: every draw comes from
the per-fixture splitmix64 stream. No wall-clock, no os.urandom.
"""
import math
import os
import struct
import sys

import numpy as np

HARNESS = os.path.expanduser("~/workspace/tnn-lab/senses/rebuild/harness")
sys.path.insert(0, HARNESS)
import gen as H

MASTER = 20260923
TASKS = ["colordisc", "colorconst", "shapetrans", "pitchdisc", "timbredisc", "motiondir"]

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "suite")

# generated-normal counts per task: prereg ratios scaled so (target-frozen) sums to 4260
N_NORMAL = [939, 626, 1091, 586, 586, 432]
# adversarial: (family, count) per task; prereg family counts scaled by 4815/5815
ADV_FAMS = [
    [("R2A-COL-1", 331), ("R2A-COL-2", 290), ("R2A-COL-3", 331)],
    [("R2A-CCN-1", 282), ("R2A-CCN-2", 282)],
    [("R2A-SHP-1", 331), ("R2A-SHP-2", 373), ("R2A-SHP-3", 248)],
    [("R2A-PTC-1", 290), ("R2A-PTC-2", 331), ("R2A-PTC-3", 331)],
    [("R2A-TMB-1", 207), ("R2A-TMB-2", 207), ("R2A-TMB-3", 157)],
    [("R2A-MOT-1", 290), ("R2A-MOT-2", 290), ("R2A-MOT-3", 244)],
]

MASK64 = (1 << 64) - 1


def splitmix64(state):
    state = (state + 0x9E3779B97F4A7C15) & MASK64
    z = state
    z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & MASK64
    z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & MASK64
    z = z ^ (z >> 31)
    return z


def stream_seed(master, stream, index):
    h = splitmix64(master ^ (stream * 0x9E3779B97F4A7C15))
    return splitmix64(h ^ (index * 0xBF58476D1CE4E5B9))


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


def rng_for(taskidx, stream, index):
    return Rng(stream_seed(MASTER, stream, index))


def clamp8(v):
    return max(0, min(255, int(round(v))))


def write_fixture(fid, taskidx, f_bytes, g_bytes, truth):
    path = os.path.join(OUT, fid + ".r2a")
    with open(path, "wb") as fh:
        fh.write(b"R2A1")
        fh.write(struct.pack("<II", taskidx, len(f_bytes)))
        fh.write(f_bytes)
        fh.write(struct.pack("<I", len(g_bytes)))
        fh.write(g_bytes)
    with open(path + ".truth", "w") as fh:
        fh.write("truth=%s\n" % truth)
    return path


# ---------------------------------------------------------------- colors
def patch_pair(w, h, c1, c2):
    """Two uniform patches: left half c1, right half c2. RGB bytes."""
    px = bytearray(w * h * 3)
    hw = w // 2
    for y in range(h):
        for x in range(w):
            c = c1 if x < hw else c2
            o = (y * w + x) * 3
            px[o] = c[0]
            px[o + 1] = c[1]
            px[o + 2] = c[2]
    return bytes(px)


def rgb_eucl(c1, c2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(c1, c2)))


def de2000(c1, c2):
    return H.delta_e_2000(H.rgb_to_lab(*c1), H.rgb_to_lab(*c2))


def color_at_distance(rng, base, lo, hi, max_rgb=None):
    """Find c2 with DeltaE2000(base,c2) in [lo,hi] (and optional RGB cap).

    RGB-space random walk with dE verification: each candidate costs one
    dE2000 (~30us); the Lab-space walker it replaces cost ~300 dE per call.
    Deterministic in rng. The exact dE only grades difficulty; the truth
    label (DIFFERENT) holds for any c2 != base.
    """
    best = None
    for _ in range(600):
        step = rng.range(3, 24)
        a1 = rng.uniform() * 2 * math.pi
        cz = rng.uniform() * 2 - 1
        s = math.sqrt(max(0.0, 1 - cz * cz))
        c2 = (clamp8(base[0] + step * s * math.cos(a1)),
              clamp8(base[1] + step * s * math.sin(a1)),
              clamp8(base[2] + step * cz))
        if c2 == base:
            continue
        if max_rgb is not None and rgb_eucl(base, c2) >= max_rgb:
            continue
        d = de2000(base, c2)
        if lo <= d <= hi:
            return c2, d
        score = abs(d - (lo + hi) / 2)
        if best is None or score < best[0]:
            best = (score, c2, d)
    return best[1], best[2]


def _rand_color(rng):
    return (rng.int(256), rng.int(256), rng.int(256))

# ------------------------------------------------------- task 0 colordisc
def gen_colordisc_normal(idx):
    rng = rng_for(0, 400, idx)
    r = rng.uniform()
    base = _rand_color(rng)
    if r < 0.10:
        c2 = base
        truth = "SAME"
    elif r < 0.20:
        c2, _ = color_at_distance(rng, base, 0.4, 1.6)
        truth = "SAME"
    else:
        b = rng.uniform()
        if b < 1 / 3:
            lo, hi = 10.0, 28.0
        elif b < 2 / 3:
            lo, hi = 4.0, 10.0
        else:
            lo, hi = 2.4, 4.0
        c2, _ = color_at_distance(rng, base, lo, hi)
        truth = "DIFFERENT"
    f = patch_pair(64, 32, base, c2)
    g = patch_pair(32, 16, base, c2)
    write_fixture("r21n_colordisc_%d" % idx, 0, f, g, truth)


def gen_colordisc_adv(idx, fam):
    rng = rng_for(0, 500, idx)
    if fam == "R2A-COL-1":
        # metamer pair: truth DIFFERENT, F collapsed by mono-red illuminant
        # (illuminant metamerism: under red light, blue-channel differences
        # vanish) so the front end reads SAME on F.
        for _ in range(60):
            r = rng.int(256)
            g = rng.int(256)
            b1 = rng.int(256)
            b2 = b1 + rng.int(61) + 60
            if b2 > 255:
                b2 = b1 - (rng.int(61) + 60)
            if b2 < 0:
                continue
            c1 = (r, g, b1)
            c2 = (r, g, max(0, min(255, b2)))
            if de2000(c1, c2) >= 4.0:
                break
        truth = "DIFFERENT"
        # F: mono-red collapse (kills G,B channels -> metameric match)
        fc1 = (c1[0], int(c1[1] * 0.06), int(c1[2] * 0.06))
        fc2 = (c2[0], int(c2[1] * 0.06), int(c2[2] * 0.06))
        assert rgb_eucl(fc1, fc2) < 15.0, (fc1, fc2)
        f = patch_pair(64, 32, fc1, fc2)
        g = patch_pair(32, 16, c1, c2)
    elif fam == "R2A-COL-2":
        # illuminant drift: truth SAME surface, F reads DIFFERENT
        c = _rand_color(rng)
        drift = rng.pick(["xblue", "xred"])
        cd = H.apply_illuminant(c, H.ILLUM[drift])
        cd = tuple(clamp8(v) for v in cd)
        truth = "SAME"
        f = patch_pair(64, 32, c, cd)
        g = patch_pair(32, 16, c, c)
    else:  # R2A-COL-3 gray trap: truth DIFFERENT, RGB euclidean < 25
        base = _rand_color(rng)
        c2, d = color_at_distance(rng, base, 2.6, 5.0, max_rgb=25.0)
        truth = "DIFFERENT"
        f = patch_pair(64, 32, base, c2)
        g = patch_pair(32, 16, base, c2)
    write_fixture("r21a_colordisc_%d" % idx, 0, f, g, truth)


# ------------------------------------------------------- task 1 colorconst
# Per-pixel rendering via H.apply_illuminant (exact; ~2560 px/fixture).
def render_panel(photo_px, pw, ox, oy, w, h, illum_xyz, exposure=1.0):
    out = bytearray(w * h * 3)
    for y in range(h):
        for x in range(w):
            r, g, b = photo_px[(oy + y) * pw + (ox + x)]
            if exposure != 1.0:
                r = min(255, r * exposure)
                g = min(255, g * exposure)
                b = min(255, b * exposure)
            ar, ag, ab = H.apply_illuminant((r, g, b), illum_xyz)
            o = (y * w + x) * 3
            out[o] = clamp8(ar)
            out[o + 1] = clamp8(ag)
            out[o + 2] = clamp8(ab)
    return bytes(out)


def two_panels(p1, p2, w):
    """p1, p2 are w/2 x h panel byte strings; join side by side."""
    h = len(p1) // ((w // 2) * 3)
    out = bytearray()
    pw = w // 2
    for y in range(h):
        out += p1[y * pw * 3:(y + 1) * pw * 3]
        out += p2[y * pw * 3:(y + 1) * pw * 3]
    return bytes(out)


def mixed_panel(photo_px, pw, ox, oy, w, h):
    """Half-frame warm / half-frame cool, same surface."""
    out = bytearray(w * h * 3)
    for y in range(h):
        for x in range(w):
            ill = H.ILLUM["warm"] if x < w // 2 else H.ILLUM["cool"]
            r, g, b = photo_px[(oy + y) * pw + (ox + x)]
            ar, ag, ab = H.apply_illuminant((r, g, b), ill)
            o = (y * w + x) * 3
            out[o] = clamp8(ar)
            out[o + 1] = clamp8(ag)
            out[o + 2] = clamp8(ab)
    return bytes(out)


# ------------------------------------------------------- task 1 colorconst
def gen_colorconst_normal(idx):
    rng = rng_for(1, 401, idx)
    illums = ["d65", "warm", "cool"]
    if idx % 2 == 0:
        ph = rng.int(170)
        photo = H.load_photo(ph)
        ox, oy = rng.int(160 - 32), rng.int(120 - 32)
        i1, i2 = rng.int(3), rng.int(3)
        while i2 == i1:
            i2 = rng.int(3)
        p1 = render_panel(photo, 160, ox, oy, 32, 32, H.ILLUM[illums[i1]])
        p2 = render_panel(photo, 160, ox, oy, 32, 32, H.ILLUM[illums[i2]])
        g1 = render_panel(photo, 160, ox, oy, 16, 16, H.ILLUM["d65"])
        g2 = render_panel(photo, 160, ox, oy, 16, 16, H.ILLUM["d65"])
        truth = "SAME_SURFACE"
    else:
        ph1, ph2 = rng.int(170), rng.int(170)
        while ph2 == ph1:
            ph2 = rng.int(170)
        ph1d, ph2d = H.load_photo(ph1), H.load_photo(ph2)
        ox1, oy1 = rng.int(160 - 32), rng.int(120 - 32)
        ox2, oy2 = rng.int(160 - 32), rng.int(120 - 32)
        p1 = render_panel(ph1d, 160, ox1, oy1, 32, 32, H.ILLUM[rng.pick(illums)])
        p2 = render_panel(ph2d, 160, ox2, oy2, 32, 32, H.ILLUM[rng.pick(illums)])
        g1 = render_panel(ph1d, 160, ox1, oy1, 16, 16, H.ILLUM["d65"])
        g2 = render_panel(ph2d, 160, ox2, oy2, 16, 16, H.ILLUM["d65"])
        truth = "DIFFERENT"
    f = two_panels(p1, p2, 64)
    g = two_panels(g1, g2, 32)
    write_fixture("r21n_colorconst_%d" % idx, 1, f, g, truth)


def gen_colorconst_adv(idx, fam):
    rng = rng_for(1, 501, idx)
    if fam == "R2A-CCN-1":
        illums = ["xblue", "xred", "warm"]
        exp = 0.55
        if idx % 2 == 0:
            ph = rng.int(170)
            photo = H.load_photo(ph)
            ox, oy = rng.int(160 - 32), rng.int(120 - 32)
            i1, i2 = rng.int(3), rng.int(3)
            while i2 == i1:
                i2 = rng.int(3)
            p1 = render_panel(photo, 160, ox, oy, 32, 32, H.ILLUM[illums[i1]], exp)
            p2 = render_panel(photo, 160, ox, oy, 32, 32, H.ILLUM[illums[i2]], exp)
            g1 = render_panel(photo, 160, ox, oy, 16, 16, H.ILLUM["d65"])
            g2 = render_panel(photo, 160, ox, oy, 16, 16, H.ILLUM["d65"])
            truth = "SAME_SURFACE"
        else:
            ph1, ph2 = rng.int(170), rng.int(170)
            while ph2 == ph1:
                ph2 = rng.int(170)
            ph1d, ph2d = H.load_photo(ph1), H.load_photo(ph2)
            ox1, oy1 = rng.int(160 - 32), rng.int(120 - 32)
            ox2, oy2 = rng.int(160 - 32), rng.int(120 - 32)
            p1 = render_panel(ph1d, 160, ox1, oy1, 32, 32, H.ILLUM[rng.pick(illums)], exp)
            p2 = render_panel(ph2d, 160, ox2, oy2, 32, 32, H.ILLUM[rng.pick(illums)], exp)
            g1 = render_panel(ph1d, 160, ox1, oy1, 16, 16, H.ILLUM["d65"])
            g2 = render_panel(ph2d, 160, ox2, oy2, 16, 16, H.ILLUM["d65"])
            truth = "DIFFERENT"
    else:  # R2A-CCN-2 mixed illuminant
        if idx % 2 == 0:
            ph = rng.int(170)
            photo = H.load_photo(ph)
            ox, oy = rng.int(160 - 32), rng.int(120 - 32)
            p1 = mixed_panel(photo, 160, ox, oy, 32, 32)
            p2 = render_panel(photo, 160, ox, oy, 32, 32, H.ILLUM["d65"])
            g1 = render_panel(photo, 160, ox, oy, 16, 16, H.ILLUM["d65"])
            g2 = render_panel(photo, 160, ox, oy, 16, 16, H.ILLUM["d65"])
            truth = "SAME_SURFACE"
        else:
            ph1, ph2 = rng.int(170), rng.int(170)
            while ph2 == ph1:
                ph2 = rng.int(170)
            ph1d, ph2d = H.load_photo(ph1), H.load_photo(ph2)
            ox1, oy1 = rng.int(160 - 32), rng.int(120 - 32)
            ox2, oy2 = rng.int(160 - 32), rng.int(120 - 32)
            p1 = mixed_panel(ph1d, 160, ox1, oy1, 32, 32)
            p2 = render_panel(ph2d, 160, ox2, oy2, 32, 32, H.ILLUM["d65"])
            g1 = render_panel(ph1d, 160, ox1, oy1, 16, 16, H.ILLUM["d65"])
            g2 = render_panel(ph2d, 160, ox2, oy2, 16, 16, H.ILLUM["d65"])
            truth = "DIFFERENT"
    f = two_panels(p1, p2, 64)
    g = two_panels(g1, g2, 32)
    write_fixture("r21a_colorconst_%d" % idx, 1, f, g, truth)

# ------------------------------------------------------- task 2 shapetrans
TRI_R = 0.62
TRI_V = [(TRI_R * math.cos(math.pi / 2 + k * 2 * math.pi / 3),
          -TRI_R * math.sin(math.pi / 2 + k * 2 * math.pi / 3)) for k in range(3)]


def _pin_shape_np(kind, ux, uy):
    if kind == "circle":
        return ux * ux + uy * uy <= 0.25
    if kind == "square":
        return (np.abs(ux) <= 0.5) & (np.abs(uy) <= 0.5)
    (x0, y0), (x1, y1), (x2, y2) = TRI_V

    def sign(px, py, ax, ay, bx, by):
        return (px - bx) * (ay - by) - (ax - bx) * (py - by)

    d1 = sign(ux, uy, x0, y0, x1, y1)
    d2 = sign(ux, uy, x1, y1, x2, y2)
    d3 = sign(ux, uy, x2, y2, x0, y0)
    neg = (d1 < 0) | (d2 < 0) | (d3 < 0)
    pos = (d1 > 0) | (d2 > 0) | (d3 > 0)
    return ~(neg & pos)


def render_shape_np(kind, W, cx, cy, scale, rot, bg, fg, bar=False, blob=None):
    """bg: (W,W,3) float array. Returns (W,W,3) uint8. bar: dark rows.
    blob: (bx,by,br) filled circle distractor in fg color."""
    cosr, sinr = math.cos(rot), math.sin(rot)
    yy, xx = np.mgrid[0:W, 0:W].astype(np.float64)
    acc = np.zeros((W, W))
    for sy in (0.25, 0.75):
        for sx in (0.25, 0.75):
            fx = xx + sx - 0.5 - cx
            fy = yy + sy - 0.5 - cy
            ux = (fx * cosr + fy * sinr) / scale
            uy = (-fx * sinr + fy * cosr) / scale
            acc += _pin_shape_np(kind, ux, uy)
    a = acc / 4.0
    if blob is not None:
        bx, by, br = blob
        bd = np.sqrt((xx - bx) ** 2 + (yy - by) ** 2)
        a = np.maximum(a, (bd <= br).astype(np.float64))
    fg_a = np.array(fg, dtype=np.float64)
    img = fg_a[None, None, :] * a[:, :, None] + bg * (1 - a[:, :, None])
    if bar:
        img[15:23, :, :] = np.minimum(255, bg[15:23, :, :] * 0.9 + 40)
    return np.clip(img, 0, 255).astype(np.uint8)


SHAPE_TRUTH = {"circle": "CIRCLE", "triangle": "TRIANGLE", "square": "SQUARE"}


def _shape_fits_quadrant(kind, cx, cy, scale, rot, qx, qy):
    """True iff the rendered shape (incl. anti-aliased edge) lies fully
    inside the quadrant [qx,qx+24)x[qy,qy+24), per the declared
    'non-overlapping quadrant containing target unoccluded'."""
    cosr, sinr = math.cos(rot), math.sin(rot)
    yy, xx = np.mgrid[0:48, 0:48].astype(np.float64)
    acc = np.zeros((48, 48))
    for sy in (0.25, 0.75):
        for sx in (0.25, 0.75):
            fx = xx + sx - 0.5 - cx
            fy = yy + sy - 0.5 - cy
            ux = (fx * cosr + fy * sinr) / scale
            uy = (-fx * sinr + fy * cosr) / scale
            acc += _pin_shape_np(kind, ux, uy)
    m = acc > 0
    ys, xs = np.nonzero(m)
    if len(xs) == 0:
        return False
    return (xs.min() >= qx + 1 and xs.max() < qx + 23 and
            ys.min() >= qy + 1 and ys.max() < qy + 23)


def _place_shape_in_quadrant(rng, kind, scale):
    """Pick a quadrant and a center/rotation fully inside it."""
    qx = rng.pick([0, 24])
    qy = rng.pick([0, 24])
    for _ in range(40):
        rot = rng.uniform() * 2 * math.pi
        cx = qx + 12 + rng.range(-4, 4)
        cy = qy + 12 + rng.range(-4, 4)
        if _shape_fits_quadrant(kind, cx, cy, scale, rot, qx, qy):
            return qx, qy, cx, cy, rot
    # fallback: quadrant center, no rotation (always fits for scale<=16)
    return qx, qy, qx + 12, qy + 12, 0.0


def shape_bg(rng, adv):
    photo = H.load_photo(rng.int(170))
    ox, oy = rng.int(160 - 48), rng.int(120 - 48)
    crop = np.array(H.crop_photo(photo, 160, ox, oy, 48, 48),
                    dtype=np.float64).reshape(48, 48, 3)
    dim = 1.0 if adv else 0.45
    return crop * dim


def gen_shapetrans_normal(idx):
    rng = rng_for(2, 402, idx)
    kind = ["circle", "triangle", "square"][idx % 3]
    bg = shape_bg(rng, False)
    scale = rng.range(12, 16)
    qx, qy, cx, cy, rot = _place_shape_in_quadrant(rng, kind, scale)
    fg = (235, 235, 235)
    f = render_shape_np(kind, 48, cx, cy, scale, rot, bg, fg)
    g = f[qy:qy + 24, qx:qx + 24].copy()
    write_fixture("r21n_shapetrans_%d" % idx, 2, f.tobytes(), g.tobytes(),
                  SHAPE_TRUTH[kind])


def gen_shapetrans_adv(idx, fam):
    rng = rng_for(2, 502, idx)
    kind = ["circle", "triangle", "square"][rng.int(3)]
    bg = shape_bg(rng, True)
    scale = rng.range(12, 16)
    qx, qy, cx, cy, rot = _place_shape_in_quadrant(rng, kind, scale)
    tq = (0 if qx == 0 else 1) + (0 if qy == 0 else 2)  # target quadrant
    if fam == "R2A-SHP-3":
        v = rng.range(120, 175)
        fg = (v, v, v)
    else:
        fg = (235, 235, 235)
    bar = (fam == "R2A-SHP-1")
    blob = None
    if fam == "R2A-SHP-2":
        # distractor blob in a quadrant that does not hold the target
        dq = rng.pick([q for q in range(4) if q != tq])
        bqx, bqy = (dq % 2) * 24, (dq // 2) * 24
        bx = bqx + 12 + rng.range(-4, 4)
        by = bqy + 12 + rng.range(-4, 4)
        blob = (bx, by, rng.range(5, 8))
    f = render_shape_np(kind, 48, cx, cy, scale, rot, bg, fg,
                         bar=bar, blob=blob)
    # G: the target quadrant from the DECLARED-CLEAN render (no bar/blob).
    # For SHP-3 the corruption is global; G is the plain quadrant crop.
    if bar or blob is not None:
        clean = render_shape_np(kind, 48, cx, cy, scale, rot, bg, fg)
    else:
        clean = f
    g = clean[qy:qy + 24, qx:qx + 24].copy()
    write_fixture("r21a_shapetrans_%d" % idx, 2, f.tobytes(), g.tobytes(),
                  SHAPE_TRUTH[kind])

# ------------------------------------------------------- audio synthesis
def synth_tone(freq, dur, harmonics, sr, amp=0.7):
    """Static tone. freq may be scalar. Returns int16 array."""
    n = int(sr * dur)
    t = np.arange(n) / sr
    out = np.zeros(n)
    for k, a in harmonics:
        out += a * np.sin(2 * np.pi * freq * k * t)
    return _envelope(out, sr, amp)


def synth_glide(f0, f1, dur, harmonics, sr, amp=0.7):
    n = int(sr * dur)
    f = np.linspace(f0, f1, n)
    phase = 2 * np.pi * np.cumsum(f) / sr
    out = np.zeros(n)
    for k, a in harmonics:
        out += a * np.sin(k * phase)
    return _envelope(out, sr, amp)


def _envelope(out, sr, amp):
    n = len(out)
    ramp = max(1, int(sr * 0.01))
    w = np.ones(n)
    r = 0.5 - 0.5 * np.cos(np.pi * np.arange(ramp) / ramp)
    w[:ramp] = r
    w[-ramp:] = r[::-1]
    out = out * w
    peak = np.max(np.abs(out))
    if peak > 1e-9:
        out = out * (amp * 32767 / peak)
    return np.clip(out, -32768, 32767).astype(np.int16)


RICH_H = [(1, 1.0), (2, 0.30), (3, 0.15)]

# ------------------------------------------------------- task 3 pitchdisc
P_SR = 4000
P_TONE = 0.25
P_GAP = 0.04


def pitch_pair(f0, f1, glide=None):
    """(toneA, gap, toneB) int16 array. glide: (f_start,f_end) for toneB."""
    a = synth_tone(f0, P_TONE, RICH_H, P_SR)
    gap = np.zeros(int(P_SR * P_GAP), dtype=np.int16)
    if glide is None:
        b = synth_tone(f1, P_TONE, RICH_H, P_SR)
    else:
        b = synth_glide(glide[0], glide[1], P_TONE, RICH_H, P_SR)
    return np.concatenate([a, gap, b])


def gen_pitchdisc_normal(idx):
    rng = rng_for(3, 403, idx)
    f0 = rng.range(220, 660)
    cls = idx % 3
    if cls == 0:
        f1 = f0
        truth = "SAME"
    else:
        band = idx % 4
        rel = [rng.range(0.10, 0.25), rng.range(0.02, 0.05),
               rng.range(0.005, 0.008), rng.range(0.10, 0.25)][band]
        f1 = f0 * (1 + rel) if cls == 1 else f0 * (1 - rel)
        truth = "HIGHER" if cls == 1 else "LOWER"
    f = pitch_pair(f0, f1)
    g = pitch_pair(f0, f1)
    write_fixture("r21n_pitchdisc_%d" % idx, 3,
                  f.tobytes(), g.tobytes(), truth)


def gen_pitchdisc_adv(idx, fam):
    rng = rng_for(3, 503, idx)
    f0 = rng.range(220, 660)
    if fam == "R2A-PTC-1":
        r = rng.uniform()
        if r < 0.4:
            f1 = f0 * (1 + rng.range(0.0015, 0.0045))
            truth = "SAME"
        elif r < 0.7:
            f1 = f0 * (1 + rng.range(0.0055, 0.0085))
            truth = "HIGHER"
        else:
            f1 = f0 * (1 - rng.range(0.0055, 0.0085))
            truth = "LOWER"
        f = pitch_pair(f0, f1)
        g = pitch_pair(f0, f1)
    elif fam == "R2A-PTC-2":
        # toneB glides through the threshold; truth from endpoint ratio
        rel = rng.range(0.02, 0.10)
        sgn = rng.pick([1, -1])
        f_end = f0 * (1 + sgn * rel)
        truth = "HIGHER" if sgn > 0 else "LOWER"
        f = pitch_pair(f0, f_end, glide=(f0 * (1 - sgn * rel), f_end))
        g = pitch_pair(f0, f_end)
    else:  # R2A-PTC-3 harmonic distractor on tone B
        r = rng.uniform()
        if r < 1 / 3:
            f1 = f0
            truth = "SAME"
        elif r < 2 / 3:
            f1 = f0 * (1 + rng.range(0.02, 0.10))
            truth = "HIGHER"
        else:
            f1 = f0 * (1 - rng.range(0.02, 0.10))
            truth = "LOWER"
        a = synth_tone(f0, P_TONE, RICH_H, P_SR)
        gap = np.zeros(int(P_SR * P_GAP), dtype=np.int16)
        b = synth_tone(f1, P_TONE, [(1, 1.0), (2, 0.6), (3, 0.3)], P_SR)
        f = np.concatenate([a, gap, b])
        g = pitch_pair(f0, f1)
    write_fixture("r21a_pitchdisc_%d" % idx, 3,
                  f.tobytes(), g.tobytes(), truth)


# ------------------------------------------------------- task 4 timbredisc
T_SR = 8000
T_DUR = 0.5
TIMBRES = {
    "PURE": [(1, 1.0)],
    "BRIGHT": [(1, 1.0), (2, 0.80), (3, 0.65), (4, 0.55),
               (5, 0.45), (6, 0.38), (7, 0.32), (8, 0.28)],
    "DARK": [(1, 1.0), (2, 0.40), (3, 0.10), (4, 0.03)],
    "RICH": [(1, 1.0), (2, 0.55), (3, 0.40), (4, 0.28), (5, 0.20), (6, 0.14)],
}
# canonical spectral centroids at f0=440 (documented; classifier uses these)
CANON_CENT = {"PURE": 440.0, "DARK": 638.4, "RICH": 1071.7, "BRIGHT": 1565.2}
# decision boundaries (midpoints); TMB-1 straddles THESE (see note re
# the spec's 1075/1400/3000 in the module docstring / FIXTURE_NOTES)
TMB_BOUNDS = [539.0, 855.0, 1318.0]


def centroid_of(harm):
    sa = sum(a for _, a in harm)
    ska = sum(k * a for k, a in harm)
    return 440.0 * ska / sa


def nearest_class(cent):
    return min(CANON_CENT, key=lambda c: abs(CANON_CENT[c] - cent))


def mix_profiles(p1, p2, t):
    """Linear mix of two harmonic profiles; returns profile list."""
    d = {k: 0.0 for k, _ in p1} | {k: 0.0 for k, _ in p2}
    for k, a in p1:
        d[k] += (1 - t) * a
    for k, a in p2:
        d[k] += t * a
    return [(k, d[k]) for k in sorted(d) if d[k] > 1e-9]


def gen_timbredisc_normal(idx):
    rng = rng_for(4, 404, idx)
    cls = ["PURE", "BRIGHT", "DARK", "RICH"][idx % 4]
    s = synth_tone(440.0, T_DUR, TIMBRES[cls], T_SR)
    write_fixture("r21n_timbredisc_%d" % idx, 4, s.tobytes(), s.tobytes(), cls)


def gen_timbredisc_adv(idx, fam):
    rng = rng_for(4, 504, idx)
    if fam == "R2A-TMB-1":
        # centroid within +/-10% of a classifier decision boundary
        b = rng.pick(TMB_BOUNDS)
        if b == TMB_BOUNDS[0]:
            p1, p2 = TIMBRES["PURE"], TIMBRES["DARK"]
        elif b == TMB_BOUNDS[1]:
            p1, p2 = TIMBRES["DARK"], TIMBRES["RICH"]
        else:
            p1, p2 = TIMBRES["RICH"], TIMBRES["BRIGHT"]
        tgt = b * rng.range(0.90, 1.10)
        lo, hi = 0.0, 1.0
        for _ in range(40):
            mid = (lo + hi) / 2
            c = centroid_of(mix_profiles(p1, p2, mid))
            if c < tgt:
                lo = mid
            else:
                hi = mid
        prof = mix_profiles(p1, p2, (lo + hi) / 2)
        truth = nearest_class(centroid_of(prof))
    elif fam == "R2A-TMB-2":
        cls = ["PURE", "DARK", "RICH", "BRIGHT"][idx % 4]
        prof = [(k, a * 1.15 if k == 2 else a) for k, a in TIMBRES[cls]]
        truth = nearest_class(centroid_of(prof))
    else:  # R2A-TMB-3 distractor harmonics (carryover)
        r = rng.uniform()
        if r < 0.25:
            prof = [(1, 0.5), (2, 0.9), (3, 0.8), (4, 0.7), (5, 0.6), (6, 0.5)]
            truth = "BRIGHT"
        elif r < 0.5:
            prof = [(1, 1.0), (2, 0.45), (3, 0.35), (4, 0.08)]
            truth = "DARK"
        elif r < 0.75:
            prof = [(1, 1.0), (2, 0.7), (3, 0.6), (4, 0.5), (5, 0.4), (6, 0.3)]
            truth = "RICH"
        else:
            prof = [(1, 1.0), (2, 0.06)]
            truth = "PURE"
    s = synth_tone(440.0, T_DUR, prof, T_SR)
    write_fixture("r21a_timbredisc_%d" % idx, 4, s.tobytes(), s.tobytes(), truth)


# ------------------------------------------------------- task 5 motiondir
DIRS = {"N": (0, -1), "NE": (1, -1), "E": (1, 0), "SE": (1, 1),
        "S": (0, 1), "SW": (-1, 1), "W": (-1, 0), "NW": (-1, -1)}
M_FRAMES = 8
M_W = 24


def photo_gray(i):
    px = np.array(H.load_photo(i), dtype=np.float64).reshape(120, 160, 3)
    return 0.299 * px[:, :, 0] + 0.587 * px[:, :, 1] + 0.114 * px[:, :, 2]


def render_motion_frames(gray, ox, oy, vecs, contrast):
    """vecs: per-frame-step direction list (len M_FRAMES-1). Returns frames."""
    mean = float(gray.mean())
    frames = []
    px, py = ox, oy
    xs0 = np.arange(M_W)
    ys0 = np.arange(M_W)
    for f in range(M_FRAMES):
        xs = (px + xs0) % 160
        ys = (py + ys0) % 120
        fr = gray[ys[:, None], xs[None, :]]
        fr = mean + (fr - mean) * contrast
        frames.append(np.clip(fr, 0, 255).astype(np.uint8))
        if f < M_FRAMES - 1:
            vx, vy = vecs[f]
            # sampling window moves OPPOSITE so content translates along vec
            px = (px - vx) % 160
            py = (py - vy) % 120
    return frames


def frames_blob(frames):
    return b"".join(fr.tobytes() for fr in frames)


def gen_motiondir_normal(idx):
    rng = rng_for(5, 405, idx)
    gray = photo_gray(rng.int(170))
    ox, oy = rng.int(160 - M_W), rng.int(120 - M_W)
    if idx % 9 == 8:
        truth, vec = "STILL", (0, 0)
    else:
        truth = sorted(DIRS)[idx % 8]
        vec = DIRS[truth]
    step = 1 + rng.int(2)
    vecs = [(vec[0] * step, vec[1] * step)] * (M_FRAMES - 1)
    f = render_motion_frames(gray, ox, oy, vecs, 1.0)
    g = render_motion_frames(gray, ox, oy, vecs, 1.0)
    write_fixture("r21n_motiondir_%d" % idx, 5,
                  frames_blob(f), frames_blob(g), truth)


def gen_motiondir_adv(idx, fam):
    rng = rng_for(5, 505, idx)
    gray = photo_gray(rng.int(170))
    ox, oy = rng.int(160 - M_W), rng.int(120 - M_W)
    keys = sorted(DIRS)
    if fam == "R2A-MOT-1":
        # reversed video: F shows constant -D; truth = true direction D
        truth = rng.pick(keys)
        vec = DIRS[truth]
        step = 1 + rng.int(2)
        fwd = [(vec[0] * step, vec[1] * step)] * (M_FRAMES - 1)
        f_frames = render_motion_frames(gray, ox, oy, fwd, 1.0)[::-1]
        g = render_motion_frames(gray, ox, oy, fwd, 1.0)
        write_fixture("r21a_motiondir_%d" % idx, 5,
                      frames_blob(f_frames), frames_blob(g), truth)
        return
    if fam == "R2A-MOT-2":
        truth = rng.pick(keys)
        vec = DIRS[truth]
        d2 = rng.pick([k for k in keys if k != truth])
        v2 = DIRS[d2]
        step = 1 + rng.int(2)
        vecs = []
        for _ in range(M_FRAMES - 1):
            if rng.uniform() < 0.30:
                w = rng.pick(keys)
                vecs.append((DIRS[w][0] * step, DIRS[w][1] * step))
            else:
                vecs.append((vec[0] * step, vec[1] * step))
        base = render_motion_frames(gray, ox, oy, vecs, 1.0)
        ghost = render_motion_frames(gray, (ox + 40) % (160 - M_W),
                                     (oy + 30) % (120 - M_W),
                                     [(v2[0] * step, v2[1] * step)] * (M_FRAMES - 1),
                                     1.0)
        f = [np.clip(b.astype(np.float64) * 0.75 + gh.astype(np.float64) * 0.25,
                     0, 255).astype(np.uint8)
             for b, gh in zip(base, ghost)]
        g = render_motion_frames(gray, ox, oy,
                                 [(vec[0] * step, vec[1] * step)] * (M_FRAMES - 1),
                                 1.0)
    else:  # R2A-MOT-3 camouflaged: contrast 0.25, 1px/frame
        truth = rng.pick(keys + ["STILL"])
        vec = DIRS.get(truth, (0, 0))
        vecs = [(vec[0], vec[1])] * (M_FRAMES - 1)
        f = render_motion_frames(gray, ox, oy, vecs, 0.25)
        g = render_motion_frames(gray, ox, oy, vecs, 1.0)
    write_fixture("r21a_motiondir_%d" % idx, 5,
                  frames_blob(f), frames_blob(g), truth)

# ------------------------------------------------------- main driver
GEN_NORMAL = [gen_colordisc_normal, gen_colorconst_normal,
              gen_shapetrans_normal, gen_pitchdisc_normal,
              gen_timbredisc_normal, gen_motiondir_normal]
GEN_ADV = [gen_colordisc_adv, gen_colorconst_adv, gen_shapetrans_adv,
           gen_pitchdisc_adv, gen_timbredisc_adv, gen_motiondir_adv]


def fam_of(taskidx, idx):
    """Map adversarial index -> family name (table order)."""
    acc = 0
    for fam, cnt in ADV_FAMS[taskidx]:
        if idx < acc + cnt:
            return fam
        acc += cnt
    raise ValueError("adv index out of range")


def fixture_exists(fid):
    return os.path.exists(os.path.join(OUT, fid + ".r2a"))


def main():
    os.makedirs(OUT, exist_ok=True)
    only = sys.argv[1:]  # optional: task names to (re)generate
    counts = {}
    for ti, task in enumerate(TASKS):
        if only and task not in only:
            continue
        n0 = N_NORMAL[ti]
        done_n = 0
        for i in range(n0):
            fid = "r21n_%s_%d" % (task, i)
            if not fixture_exists(fid):
                GEN_NORMAL[ti](i)
            done_n += 1
        counts[task + "/normal"] = done_n
        na = 0
        for i in range(sum(c for _, c in ADV_FAMS[ti])):
            fid = "r21a_%s_%d" % (task, i)
            if not fixture_exists(fid):
                GEN_ADV[ti](i, fam_of(ti, i))
            na += 1
        counts[task + "/adversarial"] = na
        print("%s: normal=%d adv=%d" % (task, done_n, na), flush=True)
    print("generated counts:", counts, flush=True)


def write_manifest():
    """MANIFEST.sha256 covering every generated byte + frozen harness files."""
    import hashlib
    lines = []
    # generated fixtures + truths
    for fn in sorted(os.listdir(OUT)):
        if fn == "MANIFEST.sha256":
            continue
        p = os.path.join(OUT, fn)
        if not os.path.isfile(p):
            continue
        h = hashlib.sha256()
        with open(p, "rb") as fh:
            while True:
                b = fh.read(1 << 20)
                if not b:
                    break
                h.update(b)
        lines.append("%s  fixtures/%s\n" % (h.hexdigest(), fn))
    # frozen harness fixtures (referenced, not regenerated)
    hfix = os.path.join(HARNESS, "fixtures")
    for tdir in sorted(os.listdir(hfix)):
        td = os.path.join(hfix, tdir)
        if not os.path.isdir(td) or tdir.startswith("_"):
            continue
        for variant in sorted(os.listdir(td)):
            vd = os.path.join(td, variant)
            if not os.path.isdir(vd):
                continue
            for fn in sorted(os.listdir(vd)):
                p = os.path.join(vd, fn)
                hh = hashlib.sha256()
                with open(p, "rb") as fh:
                    while True:
                        b = fh.read(1 << 20)
                        if not b:
                            break
                        hh.update(b)
                rel = os.path.relpath(p, os.path.expanduser("~/workspace/tnn-lab"))
                lines.append("%s  %s\n" % (hh.hexdigest(), rel))
    lines.sort(key=lambda l: l[65:])
    with open(os.path.join(OUT, "MANIFEST.sha256"), "w") as fh:
        fh.writelines(lines)
    print("manifest: %d entries" % len(lines), flush=True)


if __name__ == "__main__":
    if "--manifest-only" in sys.argv:
        write_manifest()
    else:
        main()
        write_manifest()
