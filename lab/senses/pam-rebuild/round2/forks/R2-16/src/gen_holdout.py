#!/usr/bin/env python3
"""gen_holdout.py -- R2-16 novel-family holdout generator (B-holdout).

10 novel families x 1,000 fixtures, adversarial (each targets its task's
formation), truth labels by construction. Generated AFTER the challenge
freeze; the challenge registry is not touched.

Family plan (2 per task except colordisc/motiondir 1 each + 2 extra
timbredisc = 10; all novel, none in the enumerated R2A 16):
  t0 colordisc : R2H16-COL-1  gain-shift SAME (digital gain on viewB)
  t1 colorconst: R2H16-CCN-1  local-patch doppelganger (DIFFERENT)
                 R2H16-CCN-2  cross-crop chromaticity collision (DIFFERENT)
  t2 shapetrans: R2H16-SHP-1  hollow shapes (formation fill-ratio fooled)
                 R2H16-SHP-2  dual shape (bbox covers both)
  t3 pitchdisc : R2H16-PTC-1  overmodulated AM on toneB (extra crossings)
                 R2H16-PTC-2  subharmonic toneB (count halved)
  t4 timbredisc: R2H16-TMB-1  formant-boosted k>=4 x3 (centroid shift)
                 R2H16-TMB-2  vibrato +-3% @6Hz (Goertzel detune)
  t5 motiondir : R2H16-MOT-1  checkerboard drift (periodic-texture aliasing)

Determinism: MASTER=20260923, STREAM=960+taskidx (fresh; no collision with
400/500/700/900), per-fixture seed = splitmix64(splitmix64(MASTER ^
stream*0x9E3779B97F4A7C15) ^ index*0xBF58476D1CE4E5B9). No RNG anywhere;
numpy only for arithmetic. Reuses the frozen R2-7 per-task renderers
(gen_r2a.py) for byte-exact F/G span formats.

Output: fixtures_holdout/r2h16_<task>_<i>.r2fx + .truth,
        fixtures_holdout/gen_ledger.jsonl, fixtures_holdout/MANIFEST.sha256,
        evidence/b_holdout.list (10,000 paths, family-major order).
"""
import math, os, struct, sys, hashlib, json
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
FORK = os.path.normpath(os.path.join(HERE, ".."))
R27SRC = os.path.normpath(os.path.join(FORK, "..", "R2-7", "src"))
sys.path.insert(0, R27SRC)
import gen_r2a as G  # noqa: E402  (frozen R2-7 generator: renderers + PRNG)

MASTER = 20260923
STREAM_BASE = 960
TASKS = ["colordisc", "colorconst", "shapetrans", "pitchdisc", "timbredisc", "motiondir"]
OUTDIR = os.path.join(FORK, "fixtures_holdout")
EV = os.path.join(FORK, "evidence")
N_PER_FAMILY = 1000

def rng_for(taskidx, index):
    return G.Rng(G.stream_seed(MASTER, STREAM_BASE + taskidx, index))

# ============================================================ t0 colordisc
# R2H16-COL-1: gain-shift SAME. Same spectrum both views (truth=SAME);
# viewB gets a digital x1.3 gain (sensor-processing corruption, NOT an
# illuminant change like R2A-COL-2). Formation mean-RGB distance is fooled;
# challenge sees identical spectra -> SAME -> WITHHOLD expected.
def gen_col(rng, idx):
    N = G._nullspace()
    s = G._draw_spec(rng)
    f = G._cd_pair(rng, s, list(s))  # 6144 B: patchA + patchB
    fa = np.frombuffer(f[:3072], dtype=np.uint8).astype(np.float64)
    fb = np.frombuffer(f[3072:], dtype=np.uint8).astype(np.float64)
    fb = np.clip(fb * 1.3, 0, 255)
    f2 = fa.astype(np.uint8).tobytes() + fb.astype(np.uint8).tobytes()
    g = G._cd_pair(rng, s, list(s)) + G._cd_spectra_bytes(s, list(s))
    return f2, g, "SAME"

# ============================================================ t1 colorconst
# R2H16-CCN-1: local-patch doppelganger. c2 = c1 with an 8x8 patch replaced
# by a strongly-different color; truth=DIFFERENT (different surface content)
# but both mean-quantities are blind to the small patch.
def _ccn1_patch_color(rng, region):
    # pick a solid color far from the region's mean RGB
    mean = region.reshape(-1, 3).mean(axis=0)
    best, bd = (255, 0, 0), -1.0
    for _ in range(12):
        c = (rng.irange(0, 256), rng.irange(0, 256), rng.irange(0, 256))
        d = sum((a - b) ** 2 for a, b in zip(c, mean))
        if d > bd:
            bd, best = d, c
    return best

def gen_ccn1(rng, idx):
    c1, _ = G.photo_crop(rng, 48, 48)
    c2 = c1.copy()
    px, py = rng.irange(0, 41), rng.irange(0, 41)
    col = _ccn1_patch_color(rng, c1[py:py + 8, px:px + 8])
    c2[py:py + 8, px:px + 8] = np.array(col, dtype=np.uint8)
    f = G._cc_view(rng, c1, "d65") + G._cc_view(rng, c2, "d65")
    g = G._cc_view(rng, c1, "d65") + G._cc_view(rng, c2, "d65")
    return f, g, "DIFFERENT"

# R2H16-CCN-2: cross-crop collision. Different photo crops whose mean-RGB
# (challenge quantity, d65) and mean-chromaticity (formation quantity, under
# the F illuminants) both collide. Found by deterministic pool search.
_CCN2_POOL = None
def _ccn2_pool(rng):
    global _CCN2_POOL
    if _CCN2_POOL is not None:
        return _CCN2_POOL
    feats = []
    for i in range(1500):
        r2 = G.Rng(G.stream_seed(MASTER, 961, 10_000_000 + i))
        c, _ = G.photo_crop(r2, 48, 48)
        mrgb = c.reshape(-1, 3).mean(axis=0)  # d65 mean RGB
        # formation feature: mean chromaticity x1000 under warm
        vw = np.asarray(G.apply_illum_np(c, G.ILLUM["warm"]), dtype=np.float64)
        tot = vw.sum()
        chroma = vw.reshape(-1, 3).sum(axis=0) * 1000.0 / tot
        feats.append((mrgb, chroma, i))
    _CCN2_POOL = feats
    return feats

def _ccn2_find_pair(rng):
    pool = _ccn2_pool(rng)
    # deterministic scan: random start offset, first pair with both collisions
    n = len(pool)
    start = rng.irange(0, n)
    for a in range(start, start + n):
        i = a % n
        mi, ci, _ = pool[i]
        for b in range(i + 1, min(i + 400, n + start)):
            j = b % n
            if j == i:
                continue
            mj, cj, _ = pool[j]
            drgb = float(np.sqrt(((mi - mj) ** 2).sum()))
            dch = float(np.abs(ci - cj).sum())
            if drgb < 10.0 and dch < 55.0:
                return i, j
    # fallback: relax (still DIFFERENT crops; document if hit)
    for a in range(n):
        mi, ci, _ = pool[a]
        for b in range(a + 1, n):
            mj, cj, _ = pool[b]
            if float(np.sqrt(((mi - mj) ** 2).sum())) < 16.0 and \
               float(np.abs(ci - cj).sum()) < 75.0:
                return a, b
    raise RuntimeError("CCN-2 pool search failed")

def gen_ccn2(rng, idx):
    i, j = _ccn2_find_pair(rng)
    pool = _ccn2_pool(rng)
    r2 = G.Rng(G.stream_seed(MASTER, 961, 10_000_000 + i))
    c1, _ = G.photo_crop(r2, 48, 48)
    r3 = G.Rng(G.stream_seed(MASTER, 961, 10_000_000 + j))
    c2, _ = G.photo_crop(r3, 48, 48)
    i1 = rng.pick(["d65", "warm", "cool"])
    i2 = rng.pick(["d65", "warm", "cool"])
    f = G._cc_view(rng, c1, i1) + G._cc_view(rng, c2, i2)
    g = G._cc_view(rng, c1, "d65") + G._cc_view(rng, c2, "d65")
    return f, g, "DIFFERENT"

# ============================================================ t2 shapetrans
# R2H16-SHP-1: hollow shapes. Truth = shape class by construction; the
# formation's bbox fill-ratio sees a thin ring (low fill -> TRIANGLE);
# G is the clean FILLED re-render so the challenge reports truth.
def _hollow_frame(rng, cls, cx, cy, scale, rot, size, bg, fg, wall=6.0):
    n = size * 3
    ys, xs = np.mgrid[0:n, 0:n].astype(np.float64) / 3.0
    dx = xs - cx; dy = ys - cy
    ca, sa = math.cos(rot), math.sin(rot)
    lx = dx * ca + dy * sa; ly = -dx * sa + dy * ca
    if cls == 0:  # ring: outer circle minus inner
        d = np.sqrt(lx * lx + ly * ly)
        inside = (d <= scale / 2) & (d >= scale / 2 - wall)
    elif cls == 2:  # square outline
        ax, ay = np.abs(lx), np.abs(ly)
        inside = (ax <= scale / 2) & (ay <= scale / 2) & \
                 ((ax >= scale / 2 - wall) | (ay >= scale / 2 - wall))
    else:  # triangle outline: barycentric, edge = near an edge
        R = scale / 2
        v = [(R * math.cos(a), R * math.sin(a))
             for a in (-math.pi / 2, math.pi / 6, 5 * math.pi / 6)]
        (x0, y0), (x1, y1), (x2, y2) = v
        dd = (y1 - y2) * (x0 - x2) + (x2 - x1) * (y0 - y2)
        l0 = ((y1 - y2) * (lx - x2) + (x2 - x1) * (ly - y2)) / dd
        l1 = ((y2 - y0) * (lx - x2) + (x0 - x2) * (ly - y2)) / dd
        l2 = 1 - l0 - l1
        edge = np.minimum(np.minimum(l0, l1), l2)
        inside = (l0 >= 0) & (l1 >= 0) & (l2 >= 0) & (edge * scale < wall)
    cov = inside.reshape(size, 3, size, 3).mean(axis=(1, 3))
    img = bg * (1 - cov) + fg * cov
    img += G._sm_integers(rng, -4, 5, img.shape)
    return np.clip(img, 0, 255).astype(np.uint8)

def gen_shp1(rng, idx):
    cls = rng.irange(0, 3)
    scale = rng.frange(30, 44)
    rot = rng.frange(0, 2 * math.pi)
    cx = 48 + rng.frange(-14, 14); cy = 48 + rng.frange(-14, 14)
    ph, _ = G.photo_crop(rng, 96, 96)
    bg = (np.asarray(Image.fromarray(ph).convert("L"), dtype=np.float64)) * 0.45
    img = _hollow_frame(rng, cls, cx, cy, scale, rot, 96, bg, 235)
    f = img.tobytes()
    gbg = np.full((48, 48), 100.0)
    gimg = G._shape_frame(rng, cls, 24, 24, 16, rot, 48, gbg, 235, noise=2)
    return f, gimg.tobytes(), G.SH_CLASSES[cls]

# R2H16-SHP-2: dual shape. Target + distractor of a different class, well
# separated; the formation's bbox covers both. G = clean filled target.
def gen_shp2(rng, idx):
    cls = rng.irange(0, 3)
    dcls = (cls + rng.irange(1, 3)) % 3
    scale = rng.frange(26, 36)
    rot = rng.frange(0, 2 * math.pi)
    # place target left, distractor right (separated)
    cx, cy = 30 + rng.frange(-6, 6), 48 + rng.frange(-10, 10)
    dx, dy = 68 + rng.frange(-6, 6), 48 + rng.frange(-10, 10)
    ph, _ = G.photo_crop(rng, 96, 96)
    bg = (np.asarray(Image.fromarray(ph).convert("L"), dtype=np.float64)) * 0.45
    img = G._shape_frame(rng, dcls, dx, dy, scale, rot, 96, bg, 235)
    img = G._shape_frame(rng, cls, cx, cy, scale, rot, 96,
                         img.astype(np.float64), 235, noise=0)
    img = np.clip(img.astype(np.int16) + G._sm_integers(rng, -4, 5, img.shape),
                  0, 255).astype(np.uint8)
    f = img.tobytes()
    gbg = np.full((48, 48), 100.0)
    gimg = G._shape_frame(rng, cls, 24, 24, 16, rot, 48, gbg, 235, noise=2)
    return f, gimg.tobytes(), G.SH_CLASSES[cls]

# ============================================================ t3 pitchdisc
# R2H16-PTC-1: overmodulated AM on toneB. Carrier fb=fa (truth=SAME); the
# envelope (1+1.5*sin(2*pi*30*t)) crosses zero -> extra zero-crossings ->
# formation's count ratio explodes. G = clean tones.
def _am_tone(freq, dur, harms, rng, mod_f=30.0, mod_idx=1.5):
    n = int(G.RATE * dur)
    t = np.arange(n) / G.RATE
    sig = np.zeros(n)
    for k, a, pha in harms:
        sig += a * np.sin(k * 2 * math.pi * freq * t + pha)
    env = 1.0 + mod_idx * np.sin(2 * math.pi * mod_f * t)
    sig = sig * env
    sig *= G._ramps(n)
    return sig

def gen_ptc1(rng, idx):
    fa = rng.frange(220, 660)
    fb = fa  # truth SAME
    buf = np.zeros(G.AU_N)
    bdur = (G.PTC_B1 - G.PTC_B0) / G.RATE
    buf[0:G.PTC_GAP0] = G.synth_tone(fa, 0.9, G._ptc_harms(rng), rng)
    buf[G.PTC_B0:G.PTC_B1] = _am_tone(fb, bdur, G._ptc_harms(rng), rng)
    gbuf = G._ptc_render(fa, fb, G._ptc_harms(rng), G._ptc_harms(rng), rng)
    return G.tone_bytes(buf), G.tone_bytes(gbuf), "SAME"

# R2H16-PTC-2: subharmonic toneB. Strong f/2 partial halves the
# zero-crossing count -> formation reads LOWER; truth=SAME (pitch = fa).
def gen_ptc2(rng, idx):
    fa = rng.frange(220, 660)
    fb = fa
    harms_b = [(0.5, 1.0, rng.uniform() * 6.283),
               (1, 0.8, rng.uniform() * 6.283),
               (2, 0.3, rng.uniform() * 6.283)]
    fbuf = G._ptc_render(fa, fb, G._ptc_harms(rng), harms_b, rng)
    gbuf = G._ptc_render(fa, fb, G._ptc_harms(rng), G._ptc_harms(rng), rng)
    return G.tone_bytes(fbuf), G.tone_bytes(gbuf), "SAME"

# ============================================================ t4 timbredisc
# R2H16-TMB-1: formant-boosted. Harmonics k>=4 x3.0 (spectral-envelope shift
# that the centroid formation feels but the (p2,p3) challenge ratios don't).
# Truth = template class of the unboosted base profile.
def gen_tmb1(rng, idx):
    cls = G.TMB_CLASSES[idx % 4]
    base = dict(G.TMB_PROFILES[cls])
    boosted = {k: (a * 3.0 if k >= 4 else a) for k, a in base.items()}
    truth = G._tmb_template_class(base)
    fbuf = G._tmb_render(boosted, rng)
    gbuf = G._tmb_render(boosted, rng)
    return G.tone_bytes(fbuf), G.tone_bytes(gbuf), truth

# R2H16-TMB-2: vibrato. +-3% frequency wobble at 6 Hz detunes the exact
# Goertzel resonators (0.5 Hz bins); truth = base class by construction.
def _vibrato_tone(profile, rng, dep=0.03, rate=6.0):
    n = G.AU_N
    t = np.arange(n) / G.RATE
    f = 440.0 * (1.0 + dep * np.sin(2 * math.pi * rate * t))
    ph = 2 * math.pi * np.cumsum(f) / G.RATE
    sig = np.zeros(n)
    for k, a, pha in G._tmb_harms(profile, rng):
        sig += a * np.sin(k * ph + pha)
    sig *= G._ramps(n)
    return sig

def gen_tmb2(rng, idx):
    cls = G.TMB_CLASSES[idx % 4]
    profile = dict(G.TMB_PROFILES[cls])
    fbuf = _vibrato_tone(profile, rng)
    gbuf = _vibrato_tone(profile, rng)
    return G.tone_bytes(fbuf), G.tone_bytes(gbuf), cls

# ============================================================ t5 motiondir
# R2H16-MOT-1: checkerboard drift. 4px-period checkerboard region drifting at
# 2px/frame; the t->t+2 block-match sees period-ambiguous SAD (0 and +-4px
# all near-zero) -> votes scatter / lock wrong. Truth = window direction.
def gen_mot1(rng, idx):
    direction = rng.pick(G.MOT_DIRS)
    yy, xx = np.mgrid[0:48, 0:48]
    checker = (((xx // 4) + (yy // 4)) % 2 * 255).astype(np.float64)
    F = G._mot_frames(checker, direction, 50, rng=rng)
    Greg = G._mot_high_contrast(G._mot_frames(checker, direction, 50, rng=rng))
    f = b"".join(fr.tobytes() for fr in F)
    g = b"".join(fr.tobytes() for fr in Greg)
    assert len(f) == G.MOT_F and len(g) == G.MOT_G
    return f, g, direction

# ============================================================ driver
FAMS = [
    (0, "R2H16-COL-1", gen_col),
    (1, "R2H16-CCN-1", gen_ccn1),
    (1, "R2H16-CCN-2", gen_ccn2),
    (2, "R2H16-SHP-1", gen_shp1),
    (2, "R2H16-SHP-2", gen_shp2),
    (3, "R2H16-PTC-1", gen_ptc1),
    (3, "R2H16-PTC-2", gen_ptc2),
    (4, "R2H16-TMB-1", gen_tmb1),
    (4, "R2H16-TMB-2", gen_tmb2),
    (5, "R2H16-MOT-1", gen_mot1),
]
FAM_IDS = {"R2H16-COL-1": 10, "R2H16-CCN-1": 11, "R2H16-CCN-2": 12,
           "R2H16-SHP-1": 13, "R2H16-SHP-2": 14, "R2H16-PTC-1": 15,
           "R2H16-PTC-2": 16, "R2H16-TMB-1": 17, "R2H16-TMB-2": 18,
           "R2H16-MOT-1": 19}

def main():
    os.makedirs(OUTDIR, exist_ok=True)
    manifest = []
    ledger_path = os.path.join(OUTDIR, "gen_ledger.jsonl")
    list_path = os.path.join(EV, "b_holdout.list")
    with open(ledger_path, "w") as lf, open(list_path, "w") as lst:
        for taskidx, famtag, gen in FAMS:
            task = TASKS[taskidx]
            famid = FAM_IDS[famtag]
            for i in range(N_PER_FAMILY):
                rng = rng_for(taskidx, i)
                f, g, truth = gen(rng, i)
                fid = "r2h16_%s_%d" % (famtag, i)
                path = os.path.join(OUTDIR, fid + ".r2fx")
                G.write_r2fx(path, taskidx, i, famid, f, g)
                with open(path + ".truth", "w") as tf:
                    tf.write("truth=%s\n" % truth)
                h = hashlib.sha256(open(path, "rb").read()).hexdigest()
                manifest.append("%s  ./%s.r2fx\n" % (h, fid))
                lf.write(json.dumps({"id": fid, "task": task, "split": "r2h16",
                                     "family": famtag, "truth": truth,
                                     "sha256": h}) + "\n")
                lst.write(path + "\n")
                if (i + 1) % 250 == 0:
                    print("  %s %d/%d" % (famtag, i + 1, N_PER_FAMILY), flush=True)
            print("DONE %s" % famtag, flush=True)
    with open(os.path.join(OUTDIR, "MANIFEST.sha256"), "w") as mf:
        mf.writelines(sorted(manifest))
    print("WROTE %d fixtures" % (len(FAMS) * N_PER_FAMILY))

if __name__ == "__main__":
    main()
