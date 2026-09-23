#!/usr/bin/env python3
"""R2A fixture generator for R2-4 (H2-gate + calibrated percept self-flagging).

Frozen spec: senses/pam-rebuild/round2/preregs/R2_FIXTURE_SET.md (2026-09-22).

SPEC AMBIGUITY R2A-001 (recorded 2026-09-23): the prereg states both
  (a) "10,000 trials (5,000 normal + 5,000 adversarial)" and
  (b) per-family adversarial counts summing to 5,815 and a per-task normal
      distribution summing to 5,100.
(5,815 + 5,100 + 925 frozen harness = 11,840 trials.)
The 4,260/4,815/10,000 totals match round-1's numbers exactly and are stale
copies; the 18-family table is the load-bearing anti-post-hoc instrument
(its exact counts are what prevent family-convenience sampling), so this
generator implements (b) exactly. All kill bars are rates, so the verdict
mechanics are unaffected. Normal-extension counts are exact per the frozen
per-task distribution. This deviation is flagged in VERDICT_R2-4.md.

Determinism: MASTER=20260923, streams normal=400+taskidx / adv=500+taskidx,
seed = splitmix64(splitmix64(MASTER ^ stream*0x9E3779B97F4A7C15)
                  ^ index*0xBF58476D1CE4E5B9). Zero RNG in the generated
fixtures' labels: every attack family is a deterministic construction.

File format (.r24), all little-endian:
  u32 magic = 0x41343252 ("R24A"), u32 task_code (0..5),
  F payload: the verdict-span item in the frozen harness layout
             (img: u32 w,u32 h, w*h*3 bytes; pcm: u32 sr,u32 n, n*i16;
              vid: u32 nframes,u32 w,u32 h, frames of w*h bytes),
  G payload: the disjoint holdout span (same layouts; see per-task notes),
  sibling <name>.truth with "truth=<value>".
Per-task G layouts (fixed, asserted by sense_r24.zag):
  colordisc/colorconst: u32 w,u32 h, px | u32 w,u32 h, px   (128x64 panels)
  shapetrans:           u32 w,u32 h, px                      (96x96)
  pitchdisc:            u32 sr,u32 n, n*i16                  (2.0 s token)
  timbredisc:           u32 sr,u32 n, n*i16                  (2.0 s token)
  motiondir:            u32 nframes,u32 w,u32 h, frames      (8x64x64)
"""
import os, sys, math, struct, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.expanduser("~/workspace/tnn-lab/senses/rebuild/harness"))
import gen as G

MASTER = 20260923
TASKS = ["colordisc", "colorconst", "shapetrans", "pitchdisc", "timbredisc", "motiondir"]

# Frozen per-task normal-extension counts (sum 5100)
NORMAL_COUNTS = {"colordisc": 1080, "colorconst": 720, "shapetrans": 1296,
                 "pitchdisc": 720, "timbredisc": 720, "motiondir": 564}
# Frozen per-family adversarial counts (sum 5815)
ADV_FAMILIES = {
    "colordisc":  [("COL-1", 400), ("COL-2", 350), ("COL-3", 400)],
    "colorconst": [("CCN-1", 340), ("CCN-2", 340)],
    "shapetrans": [("SHP-1", 400), ("SHP-2", 450), ("SHP-3", 300)],
    "pitchdisc":  [("PTC-1", 350), ("PTC-2", 400), ("PTC-3", 400)],
    "timbredisc": [("TMB-1", 250), ("TMB-2", 250), ("TMB-3", 190)],
    "motiondir":  [("MOT-1", 350), ("MOT-2", 350), ("MOT-3", 295)],
}

def seed_for(stream, index):
    return G.stream_seed(MASTER, stream, index)

def write_r24(path, task_code, f_bytes, g_bytes):
    with open(path, "wb") as f:
        f.write(struct.pack("<II", 0x41343252, task_code))
        f.write(f_bytes)
        f.write(g_bytes)

def write_truth(path, value):
    with open(path + ".truth", "w") as f:
        f.write("truth=%s\n" % value)

def resumable(template):
    """Skip regeneration when the fixture + truth already exist (byte-identical
    generator: re-running reproduces the same bytes, so skipping is safe)."""
    def deco(fn):
        def wrapper(i, outdir):
            p = os.path.join(outdir, template % i)
            if (os.path.exists(p) and os.path.getsize(p) > 0
                    and os.path.exists(p + ".truth")):
                with open(p + ".truth") as fh:
                    return fh.read().strip().split("=", 1)[1]
            return fn(i, outdir)
        wrapper.__name__ = fn.__name__
        return wrapper
    return deco

def clamp(v, lo, hi):
    return max(lo, min(hi, v))

def flat(px):
    out = bytearray()
    for p in px:
        if isinstance(p, (tuple, list)):
            out.extend(int(clamp(round(v), 0, 255)) for v in p)
        else:
            out.append(int(clamp(round(p), 0, 255)))
    return bytes(out)

# ------------------------------------------------------- T1 colordisc
W, H = 128, 64

def _chip_pair(c1, c2):
    px = []
    for y in range(H):
        for x in range(W):
            px.append(c1 if x < W // 2 else c2)
    return px

def _img_payload(pairs_f, pairs_g):
    f = struct.pack("<II", W, H) + flat(_chip_pair(*pairs_f))
    g = struct.pack("<II", W, H) + flat(_chip_pair(*pairs_g))
    return f, g

@resumable("r2n_colordisc_%04d.r24")
def gen_t1_normal(i, outdir):
    rng = G.Rng(seed_for(400 + 0, i))
    base = G._rand_color(rng)
    if i < 540:  # SAME half
        if i < 270:
            c2 = base
        else:
            c2 = G._color_at_distance(rng, base, rng.range(0.4, 1.6))
        truth = "SAME"
    else:  # DIFFERENT graded third
        r = rng.uniform()
        if r < 0.35:
            c2 = G._color_at_distance(rng, base, rng.range(10, 28))
        elif r < 0.675:
            c2 = G._color_at_distance(rng, base, rng.range(4, 10))
        else:
            c2 = G._color_at_distance(rng, base, rng.range(2.4, 4))
        truth = "DIFFERENT"
    f, g = _img_payload((base, c2), (base, c2))
    p = os.path.join(outdir, "r2n_colordisc_%04d.r24" % i)
    write_r24(p, 0, f, g); write_truth(p, truth)
    return truth

def _de_warm_pair(c1, c2):
    w1 = G.apply_illuminant(c1, G.ILLUM["warm"])
    w2 = G.apply_illuminant(c2, G.ILLUM["warm"])
    return w1, w2

@resumable("r2a_colordisc_COL-1_%03d.r24")
def gen_t1_col1(i, outdir):
    # metamer trap: warm-illuminant render reads SAME, D65 surfaces DIFFERENT
    rng = G.Rng(seed_for(500 + 0, i))
    best = None
    for _ in range(200):
        base = G._rand_color(rng)
        L0, a0, b0 = G.rgb_to_lab(*base)
        ang = rng.uniform() * 2 * math.pi
        L1 = clamp(L0 + rng.range(-1.0, 1.0), 0, 100)
        a1 = a0 + 4.5 * math.cos(ang); b1 = b0 + 4.5 * math.sin(ang)
        c2 = G._lab_to_srgb(L1, a1, b1)
        deN = G.delta_e_2000((L0, a0, b0), G.rgb_to_lab(*c2))
        if not (4.0 <= deN <= 6.0):
            continue
        w1, w2 = _de_warm_pair(base, c2)
        deW = G.delta_e_2000(G.rgb_to_lab(*w1), G.rgb_to_lab(*w2))
        eucl = math.sqrt(sum((a - b) ** 2 for a, b in zip(w1, w2)))
        cand = (deW, base, c2, w1, w2)
        if deW < 1.5 and eucl < 15:
            best = cand
            break
        if best is None or deW < best[0]:
            best = cand
    _, base, c2, w1, w2 = best
    w1b = tuple(int(clamp(round(v), 0, 255)) for v in w1)
    w2b = tuple(int(clamp(round(v), 0, 255)) for v in w2)
    f, g = _img_payload((w1b, w2b), (base, c2))
    p = os.path.join(outdir, "r2a_colordisc_COL-1_%03d.r24" % i)
    write_r24(p, 0, f, g); write_truth(p, "DIFFERENT")
    return "DIFFERENT"

@resumable("r2a_colordisc_COL-2_%03d.r24")
def gen_t1_col2(i, outdir):
    # illuminant drift mid-item: same surface warm vs cool
    rng = G.Rng(seed_for(500 + 0, 400 + i))
    surf = G._rand_color(rng)
    w1 = G.apply_illuminant(surf, G.ILLUM["warm"])
    w2 = G.apply_illuminant(surf, G.ILLUM["cool"])
    w1b = tuple(int(clamp(round(v), 0, 255)) for v in w1)
    w2b = tuple(int(clamp(round(v), 0, 255)) for v in w2)
    f, g = _img_payload((w1b, w2b), (surf, surf))
    p = os.path.join(outdir, "r2a_colordisc_COL-2_%03d.r24" % i)
    write_r24(p, 0, f, g); write_truth(p, "SAME")
    return "SAME"

@resumable("r2a_colordisc_COL-3_%03d.r24")
def gen_t1_col3(i, outdir):
    # gray trap: DIFFERENT by 2.6..5.0 dE, RGB eucl < 25
    rng = G.Rng(seed_for(500 + 0, 750 + i))
    base = G._rand_color(rng)
    c2 = None
    for _ in range(60):
        cand = G._color_at_distance(rng, base, rng.range(2.6, 5.0))
        if math.sqrt(sum((a - b) ** 2 for a, b in zip(base, cand))) < 25:
            c2 = cand
            break
    if c2 is None:
        c2 = G._color_at_distance(rng, base, 3.5)
    f, g = _img_payload((base, c2), (base, c2))
    p = os.path.join(outdir, "r2a_colordisc_COL-3_%03d.r24" % i)
    write_r24(p, 0, f, g); write_truth(p, "DIFFERENT")
    return "DIFFERENT"

# ------------------------------------------------------- T2 colorconst
CW, CH = 128, 64
PW = 64

def _surface_lab(rng):
    # two Lab anchor colors -> radial blend + fine texture; returns base sRGB px
    cA = G._rand_color(rng); cB = G._rand_color(rng)
    LA = G.rgb_to_lab(*cA); LB = G.rgb_to_lab(*cB)
    px = []
    for y in range(PW):
        for x in range(PW):
            t = min(1.0, math.sqrt((x - 32) ** 2 + (y - 32) ** 2) / 45.0)
            tex = (rng.uniform() - 0.5) * 6.0
            L = LA[0] + (LB[0] - LA[0]) * t + tex
            a = LA[1] + (LB[1] - LA[1]) * t + tex * 0.5
            b = LA[2] + (LB[2] - LA[2]) * t + tex * 0.5
            px.append(G._lab_to_srgb(L, a, b))
    return px

def _mean_rgb_dist(px1, px2):
    # mean RGB Euclidean distance between two pixel lists
    n = len(px1)
    r1 = sum(p[0] for p in px1) / n; g1 = sum(p[1] for p in px1) / n; b1 = sum(p[2] for p in px1) / n
    r2 = sum(p[0] for p in px2) / n; g2 = sum(p[1] for p in px2) / n; b2 = sum(p[2] for p in px2) / n
    return math.sqrt((r1-r2)**2 + (g1-g2)**2 + (b1-b2)**2)

def _render_surface(px, illum, exposure):
    xyz = G.ILLUM[illum]
    out = []
    for (r, g, b) in px:
        rr, gg, bb = G.apply_illuminant((r, g, b), xyz)
        out.append((rr * exposure, gg * exposure, bb * exposure))
    return out

def _ccn_payload(p1f, p2f, p1g, p2g):
    # panels: [p1 64x64][divider][p2 64x64]; px are float triples
    def panels(p1, p2):
        px = []
        for y in range(CH):
            for x in range(CW):
                if x == PW:
                    px.append((0, 0, 0))
                elif x < PW:
                    px.append(p1[y * PW + x])
                else:
                    px.append(p2[y * PW + (x - PW - 1)])
        return px
    f = struct.pack("<II", CW, CH) + flat(panels(p1f, p2f))
    g = struct.pack("<II", CW, CH) + flat(panels(p1g, p2g))
    return f, g

@resumable("r2n_colorconst_%04d.r24")
def gen_t2_normal(i, outdir):
    rng = G.Rng(seed_for(400 + 1, i))
    same = (i % 2 == 0)
    sA = _surface_lab(rng)
    if same:
        sB = sA
    else:
        # ensure visually distinct surfaces (mean RGB dist > 60 on base
        # surfaces; the d65 illuminant preserves relative distances).
        # (5 tries max; random surfaces are distinct w.h.p.)
        sB = _surface_lab(rng)
        for _ in range(5):
            if _mean_rgb_dist(sA, sB) > 60:
                break
            sB = _surface_lab(rng)
    trio = ["d65", "warm", "cool"]
    i1, i2 = rng.int(3), rng.int(3)
    if same:
        while i2 == i1:
            i2 = rng.int(3)
    f, g = _ccn_payload(
        _render_surface(sA, trio[i1], 1.0), _render_surface(sB, trio[i2], 1.0),
        _render_surface(sA, "d65", 1.0), _render_surface(sB, "d65", 1.0))
    p = os.path.join(outdir, "r2n_colorconst_%04d.r24" % i)
    write_r24(p, 1, f, g)
    truth = "SAME_SURFACE" if same else "DIFFERENT"
    write_truth(p, truth)
    return truth

@resumable("r2a_colorconst_CCN-1_%03d.r24")
def gen_t2_ccn1(i, outdir):
    # extreme illuminants + low exposure; truth SAME_SURFACE
    rng = G.Rng(seed_for(500 + 1, i))
    sA = _surface_lab(rng)
    f, g = _ccn_payload(
        _render_surface(sA, "xblue", 0.55), _render_surface(sA, "xred", 0.55),
        _render_surface(sA, "d65", 1.0), _render_surface(sA, "d65", 1.0))
    p = os.path.join(outdir, "r2a_colorconst_CCN-1_%03d.r24" % i)
    write_r24(p, 1, f, g); write_truth(p, "SAME_SURFACE")
    return "SAME_SURFACE"

@resumable("r2a_colorconst_CCN-2_%03d.r24")
def gen_t2_ccn2(i, outdir):
    # mixed illuminant within panel 1 (left warm / right cool); truth SAME
    rng = G.Rng(seed_for(500 + 1, 340 + i))
    sA = _surface_lab(rng)
    p1 = []
    rw = _render_surface(sA, "warm", 1.0)
    rc = _render_surface(sA, "cool", 1.0)
    for y in range(PW):
        for x in range(PW):
            p1.append(rw[y * PW + x] if x < PW // 2 else rc[y * PW + x])
    f, g = _ccn_payload(
        p1, _render_surface(sA, "d65", 1.0),
        _render_surface(sA, "d65", 1.0), _render_surface(sA, "d65", 1.0))
    p = os.path.join(outdir, "r2a_colorconst_CCN-2_%03d.r24" % i)
    write_r24(p, 1, f, g); write_truth(p, "SAME_SURFACE")
    return "SAME_SURFACE"

# ------------------------------------------------------- T3 shapetrans
SW = 96
SHAPE_TRUTH = {"square": "SQUARE", "triangle": "TRIANGLE", "circle": "CIRCLE"}

def _render_shape(kind, rot, scale, cx, cy, bg_px, fg, occl_bar=False,
                  blob=None):
    cosr, sinr = math.cos(rot), math.sin(rot)
    px = []
    SS = 3
    for y in range(SW):
        for x in range(SW):
            bgc = bg_px[y * SW + x]
            hit = 0
            for sy in range(SS):
                for sx in range(SS):
                    fx = x + (sx + 0.5) / SS - 0.5 - cx
                    fy = y + (sy + 0.5) / SS - 0.5 - cy
                    ux = (fx * cosr + fy * sinr) / scale
                    uy = (-fx * sinr + fy * cosr) / scale
                    if G._point_in_shape(kind, ux, uy):
                        hit += 1
            if blob is not None:
                bx, by, br = blob
                if (x - bx) ** 2 + (y - by) ** 2 <= br * br:
                    hit = SS * SS
            a = hit / (SS * SS)
            col = tuple(int(fg[i] * a + bgc[i] * (1 - a)) for i in range(3))
            if occl_bar and 38 <= y <= 54:
                col = (20, 20, 20)
            px.append(col)
    return px

def _photo_bg(rng, dim):
    photo = G.load_photo(rng.int(170))
    ox = rng.int(160 - SW)
    oy = rng.int(120 - SW)
    crop = G.crop_photo(photo, 160, ox, oy, SW, SW)
    return [tuple(int(c * dim) for c in p) for p in crop]

def _flat_bg(v):
    return [(v, v, v)] * (SW * SW)

def _shape_g(kind):
    # clean canonical holdout: centered, rot 0, scale 36, dark flat bg,
    # bright fg (luminance contrast for the grid shape_measure: bg lum=96
    # < 382 < fg lum=705).
    return _render_shape(kind, 0.0, 36.0, SW / 2, SW / 2, _flat_bg(32),
                         (235, 235, 235))

def _shape_payload(px_f, px_g):
    f = struct.pack("<II", SW, SW) + flat(px_f)
    g = struct.pack("<II", SW, SW) + flat(px_g)
    return f, g

@resumable("r2n_shapetrans_%04d.r24")
def gen_t3_normal(i, outdir):
    rng = G.Rng(seed_for(400 + 2, i))
    kind = ["square", "triangle", "circle"][i % 3]
    bg = _photo_bg(rng, 0.45)
    px = _render_shape(kind, rng.uniform() * 2 * math.pi, rng.range(30, 44),
                       SW / 2 + rng.range(-8, 8), SW / 2 + rng.range(-8, 8),
                       bg, (235, 235, 235))
    f, g = _shape_payload(px, _shape_g(kind))
    p = os.path.join(outdir, "r2n_shapetrans_%04d.r24" % i)
    write_r24(p, 2, f, g); write_truth(p, SHAPE_TRUTH[kind])
    return SHAPE_TRUTH[kind]

@resumable("r2a_shapetrans_SHP-1_%03d.r24")
def gen_t3_shp1(i, outdir):
    # occlusion bar across the shape's middle
    rng = G.Rng(seed_for(500 + 2, i))
    kind = ["square", "triangle", "circle"][rng.int(3)]
    bg = _photo_bg(rng, 0.45)
    px = _render_shape(kind, rng.uniform() * 2 * math.pi, rng.range(30, 44),
                       SW / 2 + rng.range(-8, 8), SW / 2 + rng.range(-8, 8),
                       bg, (235, 235, 235), occl_bar=True)
    f, g = _shape_payload(px, _shape_g(kind))
    p = os.path.join(outdir, "r2a_shapetrans_SHP-1_%03d.r24" % i)
    write_r24(p, 2, f, g); write_truth(p, SHAPE_TRUTH[kind])
    return SHAPE_TRUTH[kind]

@resumable("r2a_shapetrans_SHP-2_%03d.r24")
def gen_t3_shp2(i, outdir):
    # distractor blob: second same-color region at a deterministic offset
    rng = G.Rng(seed_for(500 + 2, 400 + i))
    kind = ["square", "triangle", "circle"][rng.int(3)]
    bg = _photo_bg(rng, 0.45)
    blob = (rng.range(60, 80), rng.range(60, 80), rng.range(12, 16))
    px = _render_shape(kind, rng.uniform() * 2 * math.pi, rng.range(30, 44),
                       SW / 2 + rng.range(-8, 8), SW / 2 + rng.range(-8, 8),
                       bg, (235, 235, 235), blob=blob)
    f, g = _shape_payload(px, _shape_g(kind))
    p = os.path.join(outdir, "r2a_shapetrans_SHP-2_%03d.r24" % i)
    write_r24(p, 2, f, g); write_truth(p, SHAPE_TRUTH[kind])
    return SHAPE_TRUTH[kind]

@resumable("r2a_shapetrans_SHP-3_%03d.r24")
def gen_t3_shp3(i, outdir):
    # low-contrast gray shape on full photo background
    rng = G.Rng(seed_for(500 + 2, 850 + i))
    kind = ["square", "triangle", "circle"][rng.int(3)]
    bg = _photo_bg(rng, 1.0)
    px = _render_shape(kind, rng.uniform() * 2 * math.pi, rng.range(30, 44),
                       SW / 2 + rng.range(-8, 8), SW / 2 + rng.range(-8, 8),
                       bg, (150, 150, 150))
    f, g = _shape_payload(px, _shape_g(kind))
    p = os.path.join(outdir, "r2a_shapetrans_SHP-3_%03d.r24" % i)
    write_r24(p, 2, f, g); write_truth(p, SHAPE_TRUTH[kind])
    return SHAPE_TRUTH[kind]

# ------------------------------------------------------- T4 pitchdisc
def _tone_pair_payload(fa, fb, ga, gb, gap_f=0.08, gap_g=0.2, harm_f=G.RICH_H,
                       harm_g=G.RICH_H, amp=0.75):
    tA = G._tone(fa, 0.4, harm_f, amp)
    tB = G._tone(fb, 0.4, harm_f, amp)
    gap = [0] * int(G.SR * gap_f)
    f = struct.pack("<II", G.SR, len(tA) + len(gap) + len(tB)) + \
        struct.pack("<%dh" % (len(tA) + len(gap) + len(tB)), *(tA + gap + tB))
    gA = G._tone(ga, 0.9, harm_g, 0.75)
    gB = G._tone(gb, 0.9, harm_g, 0.75)
    gap2 = [0] * int(G.SR * gap_g)
    n = len(gA) + len(gap2) + len(gB)
    g = struct.pack("<II", G.SR, n) + \
        struct.pack("<%dh" % n, *(gA + gap2 + gB))
    return f, g

@resumable("r2n_pitchdisc_%04d.r24")
def gen_t4_normal(i, outdir):
    rng = G.Rng(seed_for(400 + 3, i))
    f0 = rng.range(220, 660)
    c = i % 3
    if c == 0:
        f1 = f0 * (1 + rng.range(-0.0015, 0.0015)); truth = "SAME"
    elif c == 1:
        f1 = f0 * (1 + rng.range(0.01, 0.03)); truth = "HIGHER"
    else:
        f1 = f0 * (1 - rng.range(0.01, 0.03)); truth = "LOWER"
    f, g = _tone_pair_payload(f0, f1, f0, f1)
    p = os.path.join(outdir, "r2n_pitchdisc_%04d.r24" % i)
    write_r24(p, 3, f, g); write_truth(p, truth)
    return truth

@resumable("r2a_pitchdisc_PTC-1_%03d.r24")
def gen_t4_ptc1(i, outdir):
    # near-threshold: true offset straddles the 0.5% boundary
    rng = G.Rng(seed_for(500 + 3, i))
    f0 = rng.range(220, 660)
    if i < 175:
        # |offset| in [0.15%, 0.45%]: truly SAME, straddles the noise floor
        off = rng.range(0.0015, 0.0045) * (1 if rng.int(2) else -1)
        f1 = f0 * (1 + off); truth = "SAME"
    else:
        off = rng.range(0.0055, 0.0085) * (1 if rng.int(2) else -1)
        f1 = f0 * (1 + off); truth = "HIGHER" if off > 0 else "LOWER"
    f, g = _tone_pair_payload(f0, f1, f0, f1)
    p = os.path.join(outdir, "r2a_pitchdisc_PTC-1_%03d.r24" % i)
    write_r24(p, 3, f, g); write_truth(p, truth)
    return truth

@resumable("r2a_pitchdisc_PTC-2_%03d.r24")
def gen_t4_ptc2(i, outdir):
    # step-glide: tone B dwells 0.3 s at +4% then 0.1 s at endpoint -1%;
    # truth from the endpoint ratio; a static-tone model reads the dwell.
    rng = G.Rng(seed_for(500 + 3, 350 + i))
    f0 = rng.range(220, 660)
    f_start, f_end = f0 * 1.04, f0 * 0.99
    tA = G._tone(f0, 0.4, G.RICH_H, 0.75)
    tB = G._tone(f_start, 0.3, G.RICH_H, 0.75) + G._tone(f_end, 0.1, G.RICH_H, 0.75)
    gap = [0] * int(G.SR * 0.08)
    n = len(tA) + len(gap) + len(tB)
    f = struct.pack("<II", G.SR, n) + struct.pack("<%dh" % n, *(tA + gap + tB))
    gA = G._tone(f0, 0.9, G.RICH_H, 0.75)
    gB = G._tone(f_end, 0.9, G.RICH_H, 0.75)
    gap2 = [0] * int(G.SR * 0.2)
    m = len(gA) + len(gap2) + len(gB)
    g = struct.pack("<II", G.SR, m) + struct.pack("<%dh" % m, *(gA + gap2 + gB))
    p = os.path.join(outdir, "r2a_pitchdisc_PTC-2_%03d.r24" % i)
    write_r24(p, 3, f, g); write_truth(p, "LOWER")
    return "LOWER"

@resumable("r2a_pitchdisc_PTC-3_%03d.r24")
def gen_t4_ptc3(i, outdir):
    # harmonic distractor: strong 2nd/3rd on tone B invites octave error
    rng = G.Rng(seed_for(500 + 3, 750 + i))
    f0 = rng.range(220, 660)
    c = i % 3
    if c == 0:
        f1 = f0 * (1 + rng.range(-0.002, 0.002)); truth = "SAME"
    elif c == 1:
        f1 = f0 * (1 + rng.range(0.01, 0.02)); truth = "HIGHER"
    else:
        f1 = f0 * (1 - rng.range(0.01, 0.02)); truth = "LOWER"
    dist = [(1, 1.0), (2, 0.6), (3, 0.3)]
    f, g = _tone_pair_payload(f0, f1, f0, f1, harm_f=dist, harm_g=G.RICH_H)
    p = os.path.join(outdir, "r2a_pitchdisc_PTC-3_%03d.r24" % i)
    write_r24(p, 3, f, g); write_truth(p, truth)
    return truth

# ------------------------------------------------------- T5 timbredisc
def _timbre_payload(profile, amp_f, profile_g=None, amp_g=0.75):
    tF = G._tone(440.0, 0.8, profile, amp_f)
    f = struct.pack("<II", G.SR, len(tF)) + struct.pack("<%dh" % len(tF), *tF)
    tG = G._tone(440.0, 2.0, profile_g or profile, amp_g)
    g = struct.pack("<II", G.SR, len(tG)) + struct.pack("<%dh" % len(tG), *tG)
    return f, g

def _centroid_true(profile):
    se = sum(a * a for _, a in profile)
    she = sum(k * a * a for k, a in profile)
    return 1000.0 * she / se

def _timbre_class(r):
    if r < 900: return "PURE"
    if r < 1400: return "DARK"
    if r < 2600: return "RICH"
    return "BRIGHT"

@resumable("r2n_timbredisc_%04d.r24")
def gen_t5_normal(i, outdir):
    rng = G.Rng(seed_for(400 + 4, i))
    cls = ["PURE", "BRIGHT", "DARK", "RICH"][i % 4]
    f, g = _timbre_payload(G.TIMBRES[cls], 0.75)
    p = os.path.join(outdir, "r2n_timbredisc_%04d.r24" % i)
    write_r24(p, 4, f, g); write_truth(p, cls)
    return cls

def _boundary_straddle_profile(rng):
    # from H2 h2_gen: harmonic centroid lands within +-10% of a class boundary
    bounds = [900, 1400, 2600]
    bnd = bounds[rng.int(3)]
    lo, hi = bnd * 0.90, bnd * 1.10
    harm = []
    for _ in range(400):
        n = rng.int(4) + 2
        prof = [(1, 1.0)]
        for k in range(2, n + 1):
            prof.append((k, rng.range(0.05, 0.9)))
        r = _centroid_true(prof)
        if lo <= r <= hi:
            return prof, r
        if not harm or abs(r - bnd) < abs(harm[1] - bnd):
            harm = (prof, r)
    return harm[0], harm[1]

@resumable("r2a_timbredisc_TMB-1_%03d.r24")
def gen_t5_tmb1(i, outdir):
    rng = G.Rng(seed_for(500 + 4, i))
    prof, r = _boundary_straddle_profile(rng)
    truth = _timbre_class(r)
    f, g = _timbre_payload(prof, 0.75)
    p = os.path.join(outdir, "r2a_timbredisc_TMB-1_%03d.r24" % i)
    write_r24(p, 4, f, g); write_truth(p, truth)
    return truth

@resumable("r2a_timbredisc_TMB-2_%03d.r24")
def gen_t5_tmb2(i, outdir):
    # harmonic boost: 2nd x1.15 moves the true class without moving coarse bins
    rng = G.Rng(seed_for(500 + 4, 250 + i))
    prof = [(1, 1.0), (2, 0.36 * 1.15), (3, 0.10)]
    truth = _timbre_class(_centroid_true(prof))
    f, g = _timbre_payload(prof, 0.35)
    p = os.path.join(outdir, "r2a_timbredisc_TMB-2_%03d.r24" % i)
    write_r24(p, 4, f, g); write_truth(p, truth)
    return truth

def _distractor_profile(rng):
    r = rng.uniform()
    if r < 0.25:
        return [(1, 0.5), (2, 0.9), (3, 0.8), (4, 0.7), (5, 0.6), (6, 0.5)], "BRIGHT"
    elif r < 0.5:
        return [(1, 1.0), (2, 0.45), (3, 0.35), (4, 0.08)], "DARK"
    elif r < 0.75:
        return [(1, 1.0), (2, 0.7), (3, 0.6), (4, 0.5), (5, 0.4), (6, 0.3)], "RICH"
    else:
        return [(1, 1.0), (2, 0.06)], "PURE"

@resumable("r2a_timbredisc_TMB-3_%03d.r24")
def gen_t5_tmb3(i, outdir):
    rng = G.Rng(seed_for(500 + 4, 500 + i))
    prof, truth = _distractor_profile(rng)
    f, g = _timbre_payload(prof, 0.75)
    p = os.path.join(outdir, "r2a_timbredisc_TMB-3_%03d.r24" % i)
    write_r24(p, 4, f, g); write_truth(p, truth)
    return truth

# ------------------------------------------------------- T6 motiondir
MW, MH, NF = 64, 64, 8
DIRS8 = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
DIRV = {"N": (0, -1), "NE": (1, -1), "E": (1, 0), "SE": (1, 1),
        "S": (0, 1), "SW": (-1, 1), "W": (-1, 0), "NW": (-1, -1)}

def _motion_frames(rng, direction, step, contrast, flicker=None):
    # photo window translated step px/frame; contrast scaled; optional
    # flicker=(dir2, weight) blended on even frames only
    photo = G.load_photo(rng.int(170))
    mox = rng.int(160 - 72)
    moy = rng.int(120 - 72)
    base = G.crop_photo(photo, 160, mox, moy, 72, 72)
    dx, dy = DIRV[direction]
    frames = []
    for j in range(NF):
        ox = 4 + dx * step * j
        oy = 4 + dy * step * j
        fr = []
        for y in range(MH):
            for x in range(MW):
                px, py = x + ox, y + oy
                px = clamp(px, 0, 71); py = clamp(py, 0, 71)
                r, g, b = base[py * 72 + px]
                v = (r + g + b) // 3
                v = int(128 + (v - 128) * contrast)
                if flicker is not None and j % 2 == 0:
                    d2x, d2y = DIRV[flicker[0]]
                    qx, qy = x + 4 + d2x * step * j, y + 4 + d2y * step * j
                    qx = clamp(qx, 0, 71); qy = clamp(qy, 0, 71)
                    r2, g2, b2 = base[qy * 72 + qx]
                    v2 = (r2 + g2 + b2) // 3
                    v2 = int(128 + (v2 - 128) * contrast)
                    w = flicker[1]
                    v = int(v * (1 - w) + v2 * w)
                fr.append(clamp(v, 0, 255))
                fr.append(clamp(v, 0, 255))
                fr.append(clamp(v, 0, 255))
        frames.append(fr)
    return frames

def _vid_payload(frames_f, frames_g):
    f = struct.pack("<III", NF, MW, MH)
    for fr in frames_f:
        f += bytes(fr)
    g = struct.pack("<III", NF, MW, MH)
    for fr in frames_g:
        g += bytes(fr)
    return f, g

@resumable("r2n_motiondir_%04d.r24")
def gen_t6_normal(i, outdir):
    rng = G.Rng(seed_for(400 + 5, i))
    if i < 36:
        direction, step, truth = "N", 0, "STILL"
    else:
        direction = DIRS8[(i - 36) % 8]; step = 2; truth = direction
    ff = _motion_frames(rng, direction, step, 1.0)
    gf = _motion_frames(rng, direction, 0 if truth == "STILL" else 3, 1.0)
    f, g = _vid_payload(ff, gf)
    p = os.path.join(outdir, "r2n_motiondir_%04d.r24" % i)
    write_r24(p, 5, f, g); write_truth(p, truth)
    return truth

@resumable("r2a_motiondir_MOT-1_%03d.r24")
def gen_t6_mot1(i, outdir):
    # reversed frame order: F shows the opposite motion; truth = true direction
    rng = G.Rng(seed_for(500 + 5, i))
    direction = DIRS8[i % 8]
    ff = _motion_frames(rng, direction, 2, 1.0)
    ff = ff[::-1]
    gf = _motion_frames(rng, direction, 3, 1.0)
    f, g = _vid_payload(ff, gf)
    p = os.path.join(outdir, "r2a_motiondir_MOT-1_%03d.r24" % i)
    write_r24(p, 5, f, g); write_truth(p, direction)
    return direction

@resumable("r2a_motiondir_MOT-2_%03d.r24")
def gen_t6_mot2(i, outdir):
    # two-motion flicker: dominant D + 30% opposite-direction on even frames
    rng = G.Rng(seed_for(500 + 5, 350 + i))
    direction = DIRS8[i % 8]
    opp = DIRS8[(i + 4) % 8]
    ff = _motion_frames(rng, direction, 2, 1.0, flicker=(opp, 0.3))
    gf = _motion_frames(rng, direction, 3, 1.0)
    f, g = _vid_payload(ff, gf)
    p = os.path.join(outdir, "r2a_motiondir_MOT-2_%03d.r24" % i)
    write_r24(p, 5, f, g); write_truth(p, direction)
    return direction

@resumable("r2a_motiondir_MOT-3_%03d.r24")
def gen_t6_mot3(i, outdir):
    # camouflaged: low contrast + 1px/frame; truth = true direction
    rng = G.Rng(seed_for(500 + 5, 700 + i))
    direction = DIRS8[i % 8]
    ff = _motion_frames(rng, direction, 1, 0.25)
    gf = _motion_frames(rng, direction, 3, 1.0)
    f, g = _vid_payload(ff, gf)
    p = os.path.join(outdir, "r2a_motiondir_MOT-3_%03d.r24" % i)
    write_r24(p, 5, f, g); write_truth(p, direction)
    return direction

# ------------------------------------------------------- driver
GEN_TABLE = {
    # (kind, taskidx) -> list of (fn, count)
    ("normal", 0): [(gen_t1_normal, NORMAL_COUNTS["colordisc"])],
    ("normal", 1): [(gen_t2_normal, NORMAL_COUNTS["colorconst"])],
    ("normal", 2): [(gen_t3_normal, NORMAL_COUNTS["shapetrans"])],
    ("normal", 3): [(gen_t4_normal, NORMAL_COUNTS["pitchdisc"])],
    ("normal", 4): [(gen_t5_normal, NORMAL_COUNTS["timbredisc"])],
    ("normal", 5): [(gen_t6_normal, NORMAL_COUNTS["motiondir"])],
    ("adv", 0): [(gen_t1_col1, 400), (gen_t1_col2, 350), (gen_t1_col3, 400)],
    ("adv", 1): [(gen_t2_ccn1, 340), (gen_t2_ccn2, 340)],
    ("adv", 2): [(gen_t3_shp1, 400), (gen_t3_shp2, 450), (gen_t3_shp3, 300)],
    ("adv", 3): [(gen_t4_ptc1, 350), (gen_t4_ptc2, 400), (gen_t4_ptc3, 400)],
    ("adv", 4): [(gen_t5_tmb1, 250), (gen_t5_tmb2, 250), (gen_t5_tmb3, 190)],
    ("adv", 5): [(gen_t6_mot1, 350), (gen_t6_mot2, 350), (gen_t6_mot3, 295)],
}

def main():
    outdir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "fixtures")
    only = sys.argv[2] if len(sys.argv) > 2 else None  # e.g. "adv:3" or "normal:0"
    os.makedirs(outdir, exist_ok=True)
    total = 0
    counts = {}
    for (kind, ti), fns in sorted(GEN_TABLE.items()):
        for fn, cnt in fns:
            tag = "%s:%d" % (kind, ti)
            if only and only != tag and only != fn.__name__:
                continue
            for i in range(cnt):
                truth = fn(i, outdir)
                total += 1
                key = (TASKS[ti], kind, fn.__name__)
                c = counts.get(key, {})
                c[truth] = c.get(truth, 0) + 1
                counts[key] = c
            print("done %s %s x%d" % (TASKS[ti], fn.__name__, cnt), flush=True)
    print("TOTAL %d" % total)
    for k in sorted(counts):
        print(k, counts[k])

if __name__ == "__main__":
    main()
