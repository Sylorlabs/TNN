#!/usr/bin/env python3
"""R2A frozen fixture suite generator — PAM round 2 (seed 20260923).

Deterministic: every draw from splitmix64(MASTER ^ stream). No wall-clock,
no os.urandom. Regenerating with the same code + photo pool yields
byte-identical fixtures.

Seeds (frozen):
  MASTER = 20260923
  stream ids: normal-extended = 400+taskidx, adversarial = 500+taskidx.
  per-fixture seed = splitmix64(splitmix64(MASTER ^ stream*0x9E3779B97F4A7C15)
                                ^ index*0xBF58476D1CE4E5B9)
Task index: colordisc=0, colorconst=1, shapetrans=2, pitchdisc=3,
            timbredisc=4, motiondir=5.

Suite (see LEDGER_suite.md for prereg-count reconciliation):
  normal-extended: 4,260 generated (colordisc 600, colorconst 400,
    shapetrans 1100, pitchdisc 600, timbredisc 1100, motiondir 460).
    SAME distributions as the frozen harness primary (replicated below).
  adversarial: 5,815 generated across the 18 frozen families
    (COL-1 400, COL-2 350, COL-3 400, CCN-1 340, CCN-2 340,
     SHP-1 400, SHP-2 450, SHP-3 300,
     PTC-1 350, PTC-2 400, PTC-3 400,
     TMB-1 250, TMB-2 250, TMB-3 190,
     MOT-1 350, MOT-2 350, MOT-3 295).

Output: <out>/normal/r2n_<task>_<i:04d>.{img,pcm,vid}[.truth]
        <out>/adversarial/r2a_<task>_<i:04d>.{img,pcm,vid}[.truth]
        <out>/MANIFEST.sha256  (sha256 of every fixture+truth file)

Photo pool: the 170 cached JPEGs from the harness
  (~/workspace/tnn-lab/senses/rebuild/harness/fixtures/_photos).
"""
import math, os, struct, sys, hashlib

sys.path.insert(0, os.path.expanduser("~/workspace/tnn-lab/senses/rebuild/harness"))
import gen as H  # noqa: E402  (harness generator: Rng, splitmix64, writers, ...)

MASTER = 20260923
TASKS = ["colordisc", "colorconst", "shapetrans", "pitchdisc", "timbredisc", "motiondir"]
EXTS = [".img", ".img", ".img", ".pcm", ".pcm", ".vid"]

N_NORMAL = [600, 400, 1100, 600, 1100, 460]          # = 4260
FAMS = {  # taskidx -> list of (family, count)
    0: [("COL-1", 400), ("COL-2", 350), ("COL-3", 400)],
    1: [("CCN-1", 340), ("CCN-2", 340)],
    2: [("SHP-1", 400), ("SHP-2", 450), ("SHP-3", 300)],
    3: [("PTC-1", 350), ("PTC-2", 400), ("PTC-3", 400)],
    4: [("TMB-1", 250), ("TMB-2", 250), ("TMB-3", 190)],
    5: [("MOT-1", 350), ("MOT-2", 350), ("MOT-3", 295)],
}

def sseed(stream, index):
    return H.stream_seed(MASTER, stream, index)

def rgb_euc(c1, c2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(c1, c2)))

def _write(out_dir, stem, ext, payload_fn, truth):
    """payload_fn(path) writes the fixture bytes; then truth + manifest."""
    path = os.path.join(out_dir, stem + ext)
    payload_fn(path)
    H.write_truth(path, truth)
    return path

# ============================================================ NORMAL (extended)
# Replicates the frozen harness PRIMARY distributions (see
# harness/FIXTURE_SOURCES.md), drawn from fresh R2A streams.

def n_colordisc(idx, out_dir, n_photos):
    rng = H.Rng(sseed(400 + 0, idx))
    r = rng.uniform()
    if r < 1.0/3.0:  # SAME (1/3): half identical, half near-identical
        base = H._rand_color(rng)
        c2 = base if rng.uniform() < 0.5 else H._color_at_distance(rng, base, rng.range(0.4, 1.6))
        truth = "SAME"
    else:  # DIFFERENT (2/3): easy/medium/hard like primary 14/13/13 of 40
        base = H._rand_color(rng)
        q = rng.uniform()
        de = rng.range(10, 28) if q < 14.0/40 else (rng.range(4, 10) if q < 27.0/40 else rng.range(2.4, 4.0))
        c2 = H._color_at_distance(rng, base, de)
        truth = "DIFFERENT"
    return _write(out_dir, "r2n_colordisc_%04d" % idx, ".img",
                  lambda p: H.write_img(p, 128, 64, H._patch_img(base, c2)), truth)

def n_colorconst(idx, out_dir, n_photos):
    rng = H.Rng(sseed(400 + 1, idx))
    if rng.uniform() < 0.5:  # SAME_SURFACE: same crop, two illuminants
        ph = rng.int(n_photos)
        crop = H.crop_photo(H.load_photo(ph), 160, rng.int(160-64), rng.int(120-64), 64, 64)
        i1, i2 = rng.int(3), rng.int(3)
        while i2 == i1: i2 = rng.int(3)
        p1 = H._render_panel(crop, H.ILLUM_TRIO[i1]); p2 = H._render_panel(crop, H.ILLUM_TRIO[i2])
        truth = "SAME_SURFACE"
    else:  # DIFFERENT: two photos
        ph1, ph2 = rng.int(n_photos), rng.int(n_photos)
        while ph2 == ph1: ph2 = rng.int(n_photos)
        c1 = H.crop_photo(H.load_photo(ph1), 160, rng.int(160-64), rng.int(120-64), 64, 64)
        c2 = H.crop_photo(H.load_photo(ph2), 160, rng.int(160-64), rng.int(120-64), 64, 64)
        p1 = H._render_panel(c1, H.ILLUM_TRIO[rng.int(3)]); p2 = H._render_panel(c2, H.ILLUM_TRIO[rng.int(3)])
        truth = "DIFFERENT"
    px = [p1[y*64+x] if x < 64 else p2[y*64+(x-64)] for y in range(64) for x in range(128)]
    return _write(out_dir, "r2n_colorconst_%04d" % idx, ".img",
                  lambda p: H.write_img(p, 128, 64, px), truth)

def n_shapetrans(idx, out_dir, n_photos):
    rng = H.Rng(sseed(400 + 2, idx))
    kinds = ["circle", "triangle", "square"]
    kind = kinds[idx % 3]
    W = 96
    crop = H.crop_photo(H.load_photo(rng.int(n_photos)), 160, rng.int(160-W), rng.int(120-W), W, W)
    bg_px = [tuple(int(c*0.45) for c in p) for p in crop]
    rot = rng.uniform()*2*math.pi; scale = rng.range(30, 44)
    cx = W/2 + rng.range(-14, 14); cy = W/2 + rng.range(-14, 14)
    fg = (235, 235, 235)
    px = _raster_shape(kind, rng, W, bg_px, fg, rot, scale, cx, cy, occl=False)
    truth = {"circle": "CIRCLE", "triangle": "TRIANGLE", "square": "SQUARE"}[kind]
    return _write(out_dir, "r2n_shapetrans_%04d" % idx, ".img",
                  lambda p: H.write_img(p, W, W, px), truth)

def _raster_shape(kind, rng, W, bg_px, fg, rot, scale, cx, cy, occl):
    cosr, sinr = math.cos(rot), math.sin(rot)
    px = []
    SS = 3
    for y in range(W):
        for x in range(W):
            bgc = bg_px[y*W + x]
            hit = 0
            for sy in range(SS):
                for sx in range(SS):
                    fx = x + (sx+0.5)/SS - 0.5 - cx
                    fy = y + (sy+0.5)/SS - 0.5 - cy
                    ux = (fx*cosr + fy*sinr)/scale; uy = (-fx*sinr + fy*cosr)/scale
                    if H._point_in_shape(kind, ux, uy): hit += 1
            a = hit/(SS*SS)
            col = tuple(int(fg[i]*a + bgc[i]*(1-a)) for i in range(3))
            if occl and 30 <= y <= 44:
                col = tuple(min(255, int(bgc[i]*0.9 + 40)) for i in range(3))
            px.append(col)
    return px

def n_pitchdisc(idx, out_dir, n_photos):
    rng = H.Rng(sseed(400 + 3, idx))
    f0 = rng.range(220, 660)
    cls = idx % 3
    if cls == 0:
        f1, truth = f0, "SAME"
    else:
        band = idx % 4
        rel = [rng.range(0.10, 0.25), rng.range(0.02, 0.05), rng.range(0.005, 0.008), rng.range(0.10, 0.25)][band]
        f1 = f0*(1+rel) if cls == 1 else f0*(1-rel)
        truth = "HIGHER" if cls == 1 else "LOWER"
    gap = [0]*int(H.SR*0.08)
    samples = H._tone(f0, 0.4, H.RICH_H) + gap + H._tone(f1, 0.4, H.RICH_H)
    return _write(out_dir, "r2n_pitchdisc_%04d" % idx, ".pcm",
                  lambda p: H.write_pcm(p, H.SR, samples), truth)

# Corrected timbre profiles for R2A normal-extended. The harness's BRIGHT
# profile yields r=2759 (<3000 boundary -> misclassified as RICH by the
# frozen front-end). This corrected BRIGHT yields r=3781 (>=3000).
# PURE/DARK/RICH are unchanged from the harness (r=1000/1157/1698).
R2A_TIMBRES = {
    "PURE":   [(1, 1.0)],
    "BRIGHT": [(1, 1.0), (2, 0.90), (3, 0.85), (4, 0.80), (5, 0.75), (6, 0.70), (7, 0.65), (8, 0.60)],
    "DARK":   [(1, 1.0), (2, 0.40), (3, 0.10), (4, 0.03)],
    "RICH":   [(1, 1.0), (2, 0.55), (3, 0.40), (4, 0.28), (5, 0.20), (6, 0.14)],
}

def n_timbredisc(idx, out_dir, n_photos):
    rng = H.Rng(sseed(400 + 4, idx))
    cls = ["PURE", "BRIGHT", "DARK", "RICH"][idx % 4]
    samples = H._tone(440.0, 0.8, R2A_TIMBRES[cls])
    return _write(out_dir, "r2n_timbredisc_%04d" % idx, ".pcm",
                  lambda p: H.write_pcm(p, H.SR, samples), cls)

def _motion_frames(rng, photo, truth, vec, W, step, contrast):
    mean = [0, 0, 0]
    for p in photo:
        for i in range(3): mean[i] += p[i]
    mean = [m/len(photo) for m in mean]
    ox, oy = rng.int(40), rng.int(24)
    frames = []
    for f in range(8):
        dx = int(round(-vec[0]*step*f)); dy = int(round(-vec[1]*step*f))
        fr = []
        for y in range(W):
            for x in range(W):
                sx = (ox+x+dx) % 160; sy = (oy+y+dy) % 120
                r, g, b = photo[sy*160+sx]
                fr.append(tuple(int(max(0, min(255, mean[i]+(c-mean[i])*contrast)))
                                for i, c in enumerate((r, g, b))))
        frames.append(fr)
    return frames

def n_motiondir(idx, out_dir, n_photos):
    rng = H.Rng(sseed(400 + 5, idx))
    q = rng.uniform()
    if q < 4.0/60: truth, vec = "STILL", (0, 0)
    else: truth = sorted(H.DIRS)[rng.int(8)]; vec = H.DIRS[truth]
    photo = H.load_photo(rng.int(n_photos))
    frames = _motion_frames(rng, photo, truth, vec, 64, 2, 1.0)
    return _write(out_dir, "r2n_motiondir_%04d" % idx, ".vid",
                  lambda p: H.write_vid(p, 64, 64, frames), truth)

N_GEN = [n_colordisc, n_colorconst, n_shapetrans, n_pitchdisc, n_timbredisc, n_motiondir]

# ============================================================ ADVERSARIAL
# 18 frozen families. Each returns (path, truth, family).

def a_COL1(idx, out_dir):  # metamer-pairs: DIFFERENT, RGB Euc<15, dE in [2.6,8]
    rng = H.Rng(sseed(500 + 0, idx))
    base = H._rand_color(rng)
    c2 = None
    for _ in range(600):
        cand = H._color_at_distance(rng, base, rng.range(2.6, 8.0))
        if rgb_euc(base, cand) < 15:
            c2 = cand; break
    if c2 is None:  # deterministic fallback: nearest found
        c2 = H._color_at_distance(rng, base, 2.6)
    p = _write(out_dir, "r2a_colordisc_%04d" % idx, ".img",
               lambda p: H.write_img(p, 128, 64, H._patch_img(base, c2)), "DIFFERENT")
    return p, "DIFFERENT", "COL-1", {"c1": base, "c2": c2}

def a_COL2(idx, out_dir):  # illuminant-drift: SAME surface, RGB Euc in [60,120]
    rng = H.Rng(sseed(500 + 0, idx))
    base = H._rand_color(rng)
    illums = ["warm", "cool", "d65"]
    i1 = rng.int(3)
    i2 = rng.int(3)
    while i2 == i1: i2 = rng.int(3)
    c1 = H.apply_illuminant(base, H.ILLUM[illums[i1]])
    c2 = H.apply_illuminant(base, H.ILLUM[illums[i2]])
    d = rgb_euc(c1, c2)
    if not (60 <= d <= 120):  # nudge: try the other pair deterministically
        i2 = 3 - i1 - i2 if (3 - i1 - i2) not in (i1,) and (3-i1-i2) >= 0 else (i1+1) % 3
        if i2 == i1: i2 = (i1+1) % 3
        c2 = H.apply_illuminant(base, H.ILLUM[illums[i2]])
    p = _write(out_dir, "r2a_colordisc_%04d" % idx, ".img",
               lambda p: H.write_img(p, 128, 64, H._patch_img(c1, c2)), "SAME")
    return p, "SAME", "COL-2", {"c1": c1, "c2": c2}

def a_COL3(idx, out_dir):  # gray-trap: DIFFERENT, dE in [2.6,5], RGB Euc<25
    rng = H.Rng(sseed(500 + 0, idx))
    base = H._rand_color(rng)
    c2 = None
    for _ in range(600):
        cand = H._color_at_distance(rng, base, rng.range(2.6, 5.0))
        if rgb_euc(base, cand) < 25:
            c2 = cand; break
    if c2 is None:
        c2 = H._color_at_distance(rng, base, 2.6)
    p = _write(out_dir, "r2a_colordisc_%04d" % idx, ".img",
               lambda p: H.write_img(p, 128, 64, H._patch_img(base, c2)), "DIFFERENT")
    return p, "DIFFERENT", "COL-3", {"c1": base, "c2": c2}

def a_CCN1(idx, out_dir, n_photos):  # extreme illuminants, like harness adv t2
    rng = H.Rng(sseed(500 + 1, idx))
    illums = ["xblue", "xred", "warm"]
    if idx % 2 == 0:
        ph = rng.int(n_photos)
        ox, oy = rng.int(160-64), rng.int(120-64)
        crop = H.crop_photo(H.load_photo(ph), 160, ox, oy, 64, 64)
        i1, i2 = rng.int(3), rng.int(3)
        while i2 == i1: i2 = rng.int(3)
        p1 = H._render_panel(crop, illums[i1], 0.55); p2 = H._render_panel(crop, illums[i2], 0.55)
        truth = "SAME_SURFACE"
        scene = {"photo": ph, "ox": ox, "oy": oy, "photo2": None}
    else:
        ph1, ph2 = rng.int(n_photos), rng.int(n_photos)
        while ph2 == ph1: ph2 = rng.int(n_photos)
        ox1, oy1 = rng.int(160-64), rng.int(120-64)
        ox2, oy2 = rng.int(160-64), rng.int(120-64)
        c1 = H.crop_photo(H.load_photo(ph1), 160, ox1, oy1, 64, 64)
        c2 = H.crop_photo(H.load_photo(ph2), 160, ox2, oy2, 64, 64)
        p1 = H._render_panel(c1, illums[rng.int(3)], 0.55); p2 = H._render_panel(c2, illums[rng.int(3)], 0.55)
        truth = "DIFFERENT"
        scene = {"photo": ph1, "ox": ox1, "oy": oy1, "photo2": ph2, "ox2": ox2, "oy2": oy2}
    px = [p1[y*64+x] if x < 64 else p2[y*64+(x-64)] for y in range(64) for x in range(128)]
    p = _write(out_dir, "r2a_colorconst_%04d" % idx, ".img",
               lambda p: H.write_img(p, 128, 64, px), truth)
    return p, truth, "CCN-1", scene

def a_CCN2(idx, out_dir, n_photos):  # mixed-illuminant: same surface, split renders
    rng = H.Rng(sseed(500 + 1, idx))
    ph = rng.int(n_photos)
    ox, oy = rng.int(160-64), rng.int(120-64)
    crop = H.crop_photo(H.load_photo(ph), 160, ox, oy, 64, 64)
    # panel A: top warm / bottom cool; panel B: top cool / bottom warm
    def split_render(illum_top, illum_bot):
        out = []
        xt, xb = H.ILLUM[illum_top], H.ILLUM[illum_bot]
        for j, (r, g, b) in enumerate(crop):
            y = j // 64
            out.append(H.apply_illuminant((r, g, b), xt if y < 32 else xb))
        return out
    p1 = split_render("warm", "cool"); p2 = split_render("cool", "warm")
    px = [p1[y*64+x] if x < 64 else p2[y*64+(x-64)] for y in range(64) for x in range(128)]
    p = _write(out_dir, "r2a_colorconst_%04d" % idx, ".img",
               lambda p: H.write_img(p, 128, 64, px), "SAME_SURFACE")
    return p, "SAME_SURFACE", "CCN-2", {"photo": ph, "ox": ox, "oy": oy}

def a_SHP1(idx, out_dir, n_photos):  # occlusion-bar (carryover)
    rng = H.Rng(sseed(500 + 2, idx))
    kinds = ["circle", "triangle", "square"]
    kind = kinds[idx % 3]
    W = 96
    crop = H.crop_photo(H.load_photo(rng.int(n_photos)), 160, rng.int(160-W), rng.int(120-W), W, W)
    bg_px = [tuple(int(c*1.0) for c in p) for p in crop]  # full-strength clutter
    rot = rng.uniform()*2*math.pi; scale = rng.range(16, 26)
    cx = W/2 + rng.range(-14, 14); cy = W/2 + rng.range(-14, 14)
    fg = tuple(int(rng.range(120, 175)) for _ in range(3))
    px = _raster_shape(kind, rng, W, bg_px, fg, rot, scale, cx, cy, occl=True)
    truth = {"circle": "CIRCLE", "triangle": "TRIANGLE", "square": "SQUARE"}[kind]
    p = _write(out_dir, "r2a_shapetrans_%04d" % idx, ".img",
               lambda p: H.write_img(p, W, W, px), truth)
    return p, truth, "SHP-1", {"kind": kind}

def a_SHP2(idx, out_dir, n_photos):  # distractor-blob beside the target
    rng = H.Rng(sseed(500 + 2, idx))
    kinds = ["circle", "triangle", "square"]
    kind = kinds[idx % 3]
    W = 96
    crop = H.crop_photo(H.load_photo(rng.int(n_photos)), 160, rng.int(160-W), rng.int(120-W), W, W)
    bg_px = [tuple(int(c*0.45) for c in p) for p in crop]
    rot = rng.uniform()*2*math.pi; scale = rng.range(30, 44)
    cx = W/2 + rng.range(-14, 14); cy = W/2 + rng.range(-14, 14)
    fg = (235, 235, 235)
    px = _raster_shape(kind, rng, W, bg_px, fg, rot, scale, cx, cy, occl=False)
    # distractor blob: same-color circle, non-overlapping
    ang = rng.uniform()*2*math.pi
    dist = scale + 22 + rng.range(0, 10)
    bx = min(W-12, max(12, cx + dist*math.cos(ang)))
    by = min(W-12, max(12, cy + dist*math.sin(ang)))
    brad = rng.range(10, 16)
    for y in range(W):
        for x in range(W):
            if (x-bx)**2 + (y-by)**2 <= brad*brad:
                px[y*W+x] = fg
    truth = {"circle": "CIRCLE", "triangle": "TRIANGLE", "square": "SQUARE"}[kind]
    p = _write(out_dir, "r2a_shapetrans_%04d" % idx, ".img",
               lambda p: H.write_img(p, W, W, px), truth)
    return p, truth, "SHP-2", {"kind": kind}

def a_SHP3(idx, out_dir, n_photos):  # low-contrast gray + full clutter (carryover)
    rng = H.Rng(sseed(500 + 2, idx))
    kinds = ["circle", "triangle", "square"]
    kind = kinds[idx % 3]
    W = 96
    crop = H.crop_photo(H.load_photo(rng.int(n_photos)), 160, rng.int(160-W), rng.int(120-W), W, W)
    bg_px = [tuple(int(c*1.0) for c in p) for p in crop]
    rot = rng.uniform()*2*math.pi; scale = rng.range(16, 26)
    cx = W/2 + rng.range(-14, 14); cy = W/2 + rng.range(-14, 14)
    fg = tuple(int(rng.range(120, 175)) for _ in range(3))
    px = _raster_shape(kind, rng, W, bg_px, fg, rot, scale, cx, cy, occl=False)
    truth = {"circle": "CIRCLE", "triangle": "TRIANGLE", "square": "SQUARE"}[kind]
    p = _write(out_dir, "r2a_shapetrans_%04d" % idx, ".img",
               lambda p: H.write_img(p, W, W, px), truth)
    return p, truth, "SHP-3", {"kind": kind}

def _chirp(f_start, f_end, dur, harmonics, amp=0.75):
    """Linear frequency glide. Raised-cosine 20ms ramps, peak-normalized."""
    n = int(H.SR*dur)
    out = [0.0]*n
    for k, a in harmonics:
        for i in range(n):
            f = f_start + (f_end-f_start)*i/max(1, n-1)
            # phase = integral of freq: use closed form for linear chirp
            phase = 2*math.pi*k*(f_start*i/H.SR + (f_end-f_start)*i*i/(2*max(1, n-1)*H.SR))
            out[i] += a*math.sin(phase)
    ramp = int(H.SR*0.02)
    for i in range(ramp):
        e = 0.5 - 0.5*math.cos(math.pi*i/ramp)
        out[i] *= e; out[n-1-i] *= e
    peak = max(1e-9, max(abs(v) for v in out))
    g = amp/peak
    return [int(max(-32768, min(32767, round(v*g*32767)))) for v in out]

def a_PTC1(idx, out_dir):  # near-threshold (carryover)
    rng = H.Rng(sseed(500 + 3, idx))
    f0 = rng.range(220, 660)
    r = rng.uniform()
    if r < 0.4:
        f1, truth = f0*(1+rng.range(0.0015, 0.0045)), "SAME"
    elif r < 0.7:
        f1, truth = f0*(1+rng.range(0.0055, 0.0085)), "HIGHER"
    else:
        f1, truth = f0*(1-rng.range(0.0055, 0.0085)), "LOWER"
    gap = [0]*int(H.SR*0.08)
    samples = H._tone(f0, 0.4, H.RICH_H) + gap + H._tone(f1, 0.4, H.RICH_H)
    p = _write(out_dir, "r2a_pitchdisc_%04d" % idx, ".pcm",
               lambda p: H.write_pcm(p, H.SR, samples), truth)
    return p, truth, "PTC-1", {"f0": f0, "f1": f1}

def a_PTC2(idx, out_dir):  # glide-through-threshold; truth from ENDPOINT ratio
    rng = H.Rng(sseed(500 + 3, idx))
    f0 = rng.range(220, 660)
    delta = rng.range(0.02, 0.05)
    # tone B glides from f0*(1-d) to f0*(1+d) (ends HIGHER) or reverse
    if idx % 2 == 0:
        fs, fe, truth = f0*(1-delta), f0*(1+delta), "HIGHER"
    else:
        fs, fe, truth = f0*(1+delta), f0*(1-delta), "LOWER"
    gap = [0]*int(H.SR*0.08)
    samples = H._tone(f0, 0.4, H.RICH_H) + gap + _chirp(fs, fe, 0.4, H.RICH_H)
    p = _write(out_dir, "r2a_pitchdisc_%04d" % idx, ".pcm",
               lambda p: H.write_pcm(p, H.SR, samples), truth)
    return p, truth, "PTC-2", {"f0": f0, "fs": fs, "fe": fe}

def a_PTC3(idx, out_dir):  # harmonic-distractor (carryover): 0.6x 2nd + 0.3x 3rd
    rng = H.Rng(sseed(500 + 3, idx))
    f0 = rng.range(220, 660)
    rel = rng.range(0.02, 0.05)
    if idx % 2 == 0:
        f1, truth = f0*(1+rel), "HIGHER"
    else:
        f1, truth = f0*(1-rel), "LOWER"
    harm = [(1, 1.0), (2, 0.6), (3, 0.3)]
    gap = [0]*int(H.SR*0.08)
    samples = H._tone(f0, 0.4, H.RICH_H) + gap + H._tone(f1, 0.4, harm)
    p = _write(out_dir, "r2a_pitchdisc_%04d" % idx, ".pcm",
               lambda p: H.write_pcm(p, H.SR, samples), truth)
    return p, truth, "PTC-3", {"f0": f0, "f1": f1, "harm": harm}

# TMB-1 / TMB-2 profiles are empirically verified (r measured via the frozen
# Approach A binary). Each entry: (harmonics, truth, r, front-end judgment).
# TMB-1: boundary-straddling (r within +/-10% of 1075/1400/3000).
TMB1_PROFILES = [
    ([(1,1.0),(2,0.20),(3,0.05),(4,0.015)], "DARK"),      # r=1044 FE=PURE wrong
    ([(1,1.0),(2,0.28),(3,0.07),(4,0.021)], "DARK"),      # r=1083 FE=DARK
    ([(1,1.0),(2,0.34),(3,0.085),(4,0.0255)], "DARK"),    # r=1118 FE=DARK
    ([(1,1.0),(2,0.60),(3,0.15),(4,0.045)], "DARK"),      # r=1297 FE=DARK
    ([(1,1.0),(2,0.385),(3,0.28),(4,0.196),(5,0.14),(6,0.098)], "RICH"),  # r=1423 FE=RICH
    ([(1,1.0),(2,0.80),(3,0.20),(4,0.06)], "DARK"),       # r=1434 FE=RICH wrong
    ([(1,1.0),(2,0.92),(3,0.7475),(4,0.6325),(5,0.5175),(6,0.437),(7,0.368),(8,0.322)], "BRIGHT"),  # r=2920 FE=RICH wrong
    ([(1,1.0),(2,0.80),(3,0.65),(4,0.55),(5,0.5175),(6,0.437),(7,0.368),(8,0.322)], "BRIGHT"),      # r=2945 FE=RICH wrong
    ([(1,1.0),(2,1.04),(3,0.845),(4,0.715),(5,0.585),(6,0.494),(7,0.416),(8,0.364)], "BRIGHT"),     # r=3047 FE=BRIGHT
    ([(1,1.0),(2,0.80),(3,0.65),(4,0.55),(5,0.585),(6,0.494),(7,0.416),(8,0.364)], "BRIGHT"),       # r=3133 FE=BRIGHT
]
# TMB-2: x1.15 boost on 2nd harmonic crosses a boundary; fixture is the
# BOOSTED version, truth = class after boost.
TMB2_PROFILES = [
    ([(1,1.0),(2,0.276),(3,0.06),(4,0.018)], "DARK"),     # from DARK s=0.6, r=1079
    ([(1,1.0),(2,0.299),(3,0.065),(4,0.0195)], "DARK"),   # from DARK s=0.65, r=1091
    ([(1,1.0),(2,0.782),(3,0.17),(4,0.051)], "RICH"),     # from DARK s=1.7, r=1412
    ([(1,1.0),(2,0.828),(3,0.18),(4,0.054)], "RICH"),     # from DARK s=1.8, r=1441
    ([(1,1.0),(2,1.15),(3,0.8125),(4,0.6875),(5,0.5625),(6,0.475),(7,0.4),(8,0.35)], "RICH"),  # from BRIGHT s=1.25, r=2932
]

def a_TMB1(idx, out_dir):
    harm, truth = TMB1_PROFILES[idx % len(TMB1_PROFILES)]
    samples = H._tone(440.0, 0.8, harm)
    p = _write(out_dir, "r2a_timbredisc_%04d" % idx, ".pcm",
               lambda p: H.write_pcm(p, H.SR, samples), truth)
    return p, truth, "TMB-1", {"harm": harm}

def a_TMB2(idx, out_dir):
    harm, truth = TMB2_PROFILES[idx % len(TMB2_PROFILES)]
    samples = H._tone(440.0, 0.8, harm)
    p = _write(out_dir, "r2a_timbredisc_%04d" % idx, ".pcm",
               lambda p: H.write_pcm(p, H.SR, samples), truth)
    return p, truth, "TMB-2", {"harm": harm}

def a_TMB3(idx, out_dir):  # distractor (carryover): harness adv t5 profiles
    rng = H.Rng(sseed(500 + 4, idx))
    r = rng.uniform()
    if r < 0.25:
        harm, cls = [(1, 0.5), (2, 0.9), (3, 0.8), (4, 0.7), (5, 0.6), (6, 0.5)], "BRIGHT"
    elif r < 0.5:
        harm, cls = [(1, 1.0), (2, 0.45), (3, 0.35), (4, 0.08)], "DARK"
    elif r < 0.75:
        harm, cls = [(1, 1.0), (2, 0.7), (3, 0.6), (4, 0.5), (5, 0.4), (6, 0.3)], "RICH"
    else:
        harm, cls = [(1, 1.0), (2, 0.06)], "PURE"
    samples = H._tone(440.0, 0.8, harm)
    p = _write(out_dir, "r2a_timbredisc_%04d" % idx, ".pcm",
               lambda p: H.write_pcm(p, H.SR, samples), cls)
    return p, cls, "TMB-3", {"harm": harm}

def a_MOT1(idx, out_dir, n_photos):  # reversed-video; truth = pre-reversal direction
    rng = H.Rng(sseed(500 + 5, idx))
    truth = sorted(H.DIRS)[rng.int(8)]; vec = H.DIRS[truth]
    photo_idx = rng.int(n_photos)
    photo = H.load_photo(photo_idx)
    frames = _motion_frames(rng, photo, truth, vec, 64, 2, 1.0)
    frames = frames[::-1]  # play backward: the manipulation
    p = _write(out_dir, "r2a_motiondir_%04d" % idx, ".vid",
               lambda p: H.write_vid(p, 64, 64, frames), truth)
    return p, truth, "MOT-1", {"photo": photo_idx, "dir": truth}

def a_MOT2(idx, out_dir, n_photos):  # two-motion: dominant D + 30% ghost in D'
    rng = H.Rng(sseed(500 + 5, idx))
    truth = sorted(H.DIRS)[rng.int(8)]; vec = H.DIRS[truth]
    others = [d for d in sorted(H.DIRS) if d != truth]
    ghost_d = others[rng.int(len(others))]
    gvec = H.DIRS[ghost_d]
    photo_idx = rng.int(n_photos)
    photo = H.load_photo(photo_idx)
    base = _motion_frames(rng, photo, truth, vec, 64, 2, 1.0)
    # ghost: same photo, fresh offset draw, moving in gvec
    ghost = _motion_frames(rng, photo, ghost_d, gvec, 64, 2, 1.0)
    frames = []
    for fb, fg in zip(base, ghost):
        frames.append([tuple(int(0.7*b + 0.3*g) for b, g in zip(pb, pg))
                       for pb, pg in zip(fb, fg)])
    p = _write(out_dir, "r2a_motiondir_%04d" % idx, ".vid",
               lambda p: H.write_vid(p, 64, 64, frames), truth)
    return p, truth, "MOT-2", {"photo": photo_idx, "dir": truth}

def a_MOT3(idx, out_dir, n_photos):  # camouflaged (carryover): 1px, 25% contrast
    rng = H.Rng(sseed(500 + 5, idx))
    if rng.uniform() < 0.2:
        truth, vec = "STILL", (0, 0)
    else:
        truth = sorted(H.DIRS)[rng.int(8)]; vec = H.DIRS[truth]
    photo_idx = rng.int(n_photos)
    photo = H.load_photo(photo_idx)
    frames = _motion_frames(rng, photo, truth, vec, 64, 1, 0.25)
    p = _write(out_dir, "r2a_motiondir_%04d" % idx, ".vid",
               lambda p: H.write_vid(p, 64, 64, frames), truth)
    return p, truth, "MOT-3", {"photo": photo_idx, "dir": truth}

# ============================================================ dispatch
A_GEN = {
    "COL-1": a_COL1, "COL-2": a_COL2, "COL-3": a_COL3,
    "CCN-1": a_CCN1, "CCN-2": a_CCN2,
    "SHP-1": a_SHP1, "SHP-2": a_SHP2, "SHP-3": a_SHP3,
    "PTC-1": a_PTC1, "PTC-2": a_PTC2, "PTC-3": a_PTC3,
    "TMB-1": a_TMB1, "TMB-2": a_TMB2, "TMB-3": a_TMB3,
    "MOT-1": a_MOT1, "MOT-2": a_MOT2, "MOT-3": a_MOT3,
}
NEEDS_PHOTOS = {"CCN-1", "CCN-2", "SHP-1", "SHP-2", "SHP-3",
                "MOT-1", "MOT-2", "MOT-3"}

def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser(
        "~/workspace/tnn-lab/senses/pam-rebuild/round2/fixtures/r2a")
    ndir = os.path.join(out, "normal"); adir = os.path.join(out, "adversarial")
    os.makedirs(ndir, exist_ok=True); os.makedirs(adir, exist_ok=True)
    n_photos = 170  # harness photo pool (already cached)
    manifest = []
    def rec(path):
        h = hashlib.sha256(open(path, "rb").read()).hexdigest()
        manifest.append((h, os.path.relpath(path, out)))
    # normal
    for ti in range(6):
        for idx in range(N_NORMAL[ti]):
            p = N_GEN[ti](idx, ndir, n_photos)
            rec(p); rec(p + ".truth")
        print("normal %s: %d" % (TASKS[ti], N_NORMAL[ti]), flush=True)
    # adversarial
    scenes = {}
    for ti in range(6):
        idx = 0
        for fam, cnt in FAMS[ti]:
            fn = A_GEN[fam]
            for _ in range(cnt):
                if fam in NEEDS_PHOTOS:
                    p, t, f, scene = fn(idx, adir, n_photos)
                else:
                    p, t, f, scene = fn(idx, adir)
                assert f == fam, (f, fam)
                rec(p); rec(p + ".truth")
                scenes[os.path.basename(p)] = {"family": fam, "truth": t, "scene": scene}
                idx += 1
        print("adversarial %s: %d" % (TASKS[ti], idx), flush=True)
    import json
    with open(os.path.join(out, "SCENES.json"), "w") as f:
        json.dump(scenes, f, sort_keys=True)
    manifest.sort(key=lambda x: x[1])
    with open(os.path.join(out, "MANIFEST.sha256"), "w") as f:
        for h, rel in manifest:
            f.write("%s  %s\n" % (h, rel))
    print("TOTAL files: %d  manifest: %s" % (len(manifest), os.path.join(out, "MANIFEST.sha256")))

if __name__ == "__main__":
    main()
