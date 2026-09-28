#!/usr/bin/env python3
"""gen_cp.py -- R2-14 B-cp: challenge-prediction (registry-adversarial) suite.

The adversary knows the frozen registry (REGISTRY.md: every challenge's
algorithm, thresholds, and margins) and the union binary. Per task it runs a
deterministic search (seed 20260923 + task id, budget 5,000 candidate scenes)
for scenes that make the REAL union binary INSTALL a claim != truth.

A candidate is KEPT iff BOTH hold:
  (i)  the union binary (r213, mode union) INSTALLS a claim != truth, and
  (ii) truth is unambiguous under the per-task strong-truth criterion below.

Kept scenes (<=100 per task, in candidate order) are written as R2FX fixtures
with family=4 (the CP family) plus .truth files, a sha256 manifest, and a
generator ledger. A task whose search finds nothing gets an EMPTY family
(documented in the verdict -- an empty family is a finding, not a gap).

Python is fixture generation only -- it never appears in any decision path.

Per-task attack (all reuse gen_r2a.py's renderers; the mutations are the new
adversarial part):

  t0 colordisc : CH-COL-1 computes s = u16 spectral L1, which is (up to <=6
      counts of u16 rounding) the same quantity as the truth criterion, so the
      wedge is nearly closed. Search: nullspace-move pairs spanning the spec
      range with randomized RGB-visible nudges and F-side illuminants.
      Expected: EMPTY.
  t1 colorconst: CH-CCN-1 is mean-RGB distance on D65 views -- NOT a function
      of truth (crop identity). Attack: mean-RGB collisions -- crop pairs from
      different photos whose D65 mean-RGB distance is <=12 (the challenge's
      SAME band), with F rendered under extreme illuminants to fool the
      white-patch-normalized formation. Keep INSTALL-SAME on true DIFFERENT.
  t2 shapetrans: CH-SHP-1 is a ray-profile harmonic classifier on the clean
      48x48 G. Attack: inter-class morphs (lambda in [0.1,0.4] u [0.6,0.9]),
      extreme rotations/scales, and clutter in the target quadrant; F is an
      occluded/distractor render to fool formation. Truth = lambda-majority
      class, strong iff lambda<=0.35 or >=0.65.
  t3 pitchdisc : CH-PTC-1 estimates endpoint freqs by interpolated
      autocorrelation. Attack: vibrato (sinusoidal FM) and inharmonic partials
      in G to bias the endpoint estimates, while F uses glide/harmonic
      distractors (PTC-2/PTC-3 patterns) to fool formation. Truth = exact
      endpoint ratio, strong iff |fb/fa-1| >= 0.01.
  t4 timbredisc: CH-TMB-1 is Goertzel m=1,2,3 power ratios vs templates.
      Attack: profiles with strong high harmonics (k=4..8) that leak into the
      Goertzel bins, plus interpolations near template boundaries. Truth =
      exact-ratio template class, strong iff template margin >= 200000.
  t5 motiondir : CH-MOT-1 is block matching on the clean high-contrast G.
      Attack: periodic gratings at the aliasing period (motion 2px/frame vs
      grating period 4px), low-contrast textures, and flicker in F; G is the
      high-contrast version of the same motion. Truth = true direction.
"""
import sys, os, math, json, struct, hashlib, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
FORK = os.path.normpath(os.path.join(HERE, ".."))
R27_SRC = os.path.normpath(os.path.join(HERE, "..", "..", "R2-7", "src"))
sys.path.insert(0, R27_SRC)
import gen_r2a as G
import numpy as np

CP_MASTER = 20260923
CP_BUDGET = 5000
CP_KEEP = 100
CP_FAMILY = 4
CP_INDEX_BASE = 9000
BIN = os.path.join(FORK, "build", "r213")
OUTDIR = os.path.join(FORK, "fixtures_cp")
SCRATCH = os.path.join(FORK, "scratch_cp")
TASK_NAMES = ["colordisc", "colorconst", "shapetrans",
              "pitchdisc", "timbredisc", "motiondir"]

# ---------------- fast deterministic noise ----------------
# Vectorized splitmix64: produces values IDENTICAL to sequential Rng.u64()
# draws (draw k uses state s0 + k*C1, then the same mixer), advancing rng.s
# by n steps. ~50x faster than the Python-level generator loop.

_C1 = 0x9E3779B97F4A7C15
_C2 = 0xBF58476D1CE4E5B9
_C3 = 0x94D049BB133111EB
_M64 = (1 << 64) - 1

def _znoise(rng, low, high, shape):
    n = 1
    for d in shape:
        n *= d
    span = high - low
    k = np.arange(1, n + 1, dtype=np.uint64)
    st = np.uint64(rng.s) + k * np.uint64(_C1)  # wraps mod 2^64
    z = st
    z = (z ^ (z >> np.uint64(30))) * np.uint64(_C2)
    z = (z ^ (z >> np.uint64(27))) * np.uint64(_C3)
    vals = z ^ (z >> np.uint64(31))
    rng.s = int(st[-1]) & _M64
    return (low + (vals % np.uint64(span))).astype(np.int16).reshape(shape)

# ---------------- t0 colordisc candidates ----------------

def _fast_patch(rng, srgb, size=32, noise=3):
    """Batched equivalent of gen_r2a._render_patch (same noise distribution,
    uniform ints in [-noise, noise]; vectorized splitmix draws)."""
    px = np.zeros((size, size, 3), dtype=np.int16)
    px[:, :] = srgb
    if noise:
        px += _znoise(rng, -noise, noise + 1, (size, size, 3))
    return np.clip(px, 0, 255).astype(np.uint8).tobytes()

def _fast_cd_pair(rng, s1, s2, illum_a="d65", illum_b="d65", noise=3):
    a = _fast_patch(rng, G.spec_to_srgb(s1, illum_a), noise=noise)
    b = _fast_patch(rng, G.spec_to_srgb(s2, illum_b), noise=noise)
    return a + b

def cand_colordisc(rng, _idx):
    """Nullspace-move pairs spanning the spec range; randomized RGB nudges."""
    G._nullspace()  # populate the module-global _NN
    s1 = G._draw_spec(rng)
    z = np.array([rng.frange(-0.6, 0.6) for _ in range(3)])
    s2 = np.clip(np.array(s1) + G._NN @ z, 0.05, 0.95)
    nudge = rng.frange(0.0, 0.12)
    s2 = np.clip(s2 + np.array([rng.frange(-nudge, nudge) for _ in range(6)]),
                 0.05, 0.95)
    s2 = list(s2)
    c1, c2 = G.spec_to_srgb(s1), G.spec_to_srgb(s2)
    de = G.delta_e_2000(G.rgb_to_lab(*c1), G.rgb_to_lab(*c2))
    l1 = G.spec_l1_u16(s1, s2)
    if l1 >= 40000 and 2.6 <= de <= 8.0:
        truth, strong = "DIFFERENT", True
    elif l1 <= 8000:
        truth, strong = "SAME", True
    else:
        truth = "DIFFERENT" if l1 >= 40000 else "SAME"
        strong = False
    illum_b = rng.pick(["d65", "warm", "cool", "d65"])
    f = _fast_cd_pair(rng, s1, s2, illum_a="d65", illum_b=illum_b)
    g = _fast_cd_pair(rng, s1, s2) + G._cd_spectra_bytes(s1, s2)
    return f, g, truth, strong

# ---------------- t1 colorconst candidates ----------------

def _cp_cc_view(rng, crop, illum, exposure=1.0, noise=2):
    """Same as gen_r2a._cc_view but with vectorized noise draws."""
    v = G.apply_illum_np(crop, G.ILLUM[illum], exposure)
    if noise:
        n = _znoise(rng, -noise, noise + 1, v.shape)
        v = np.clip(v.astype(np.int16) + n, 0, 255).astype(np.uint8)
    return v.tobytes()

def _cc_mean_dist(g):
    a = np.frombuffer(g[:6912], dtype=np.uint8).reshape(-1, 3).mean(axis=0)
    b = np.frombuffer(g[6912:], dtype=np.uint8).reshape(-1, 3).mean(axis=0)
    return float(np.sqrt(((a - b) ** 2).sum()))

_CC_POOL = None
def _cc_pool():
    """Deterministic pool of 2,000 photo crops with mean RGB. The adversary
    knows CH-CCN-1 is mean-RGB distance, so it picks nearest-neighbor pairs
    (different photos) -- a strictly stronger collision search than random
    pairs, and far cheaper per candidate."""
    global _CC_POOL
    if _CC_POOL is None:
        rng = G.Rng(G.stream_seed(CP_MASTER, 150, 0))
        phs = G.photos()
        ids = [id(ph) for ph in phs]
        pool = []
        means = []
        for _ in range(2000):
            ph = rng.pick(phs)
            pidx = ids.index(id(ph))
            h, w = ph.shape[:2]
            x = rng.irange(0, w - 48 + 1); y = rng.irange(0, h - 48 + 1)
            crop = ph[y:y + 48, x:x + 48].copy()
            pool.append((crop, pidx))
            means.append(crop.reshape(-1, 3).mean(axis=0))
        _CC_POOL = (pool, np.array(means))
    return _CC_POOL

def cand_colorconst(rng, cand_index):
    """Mean-RGB collision search via the deterministic crop pool."""
    pool, means = _cc_pool()
    if rng.coin(0.25):
        # control arm: identical crop -> unambiguous SAME_SURFACE
        c1, _ = pool[rng.u64() % 2000]
        c2 = c1.copy()
        truth, strong = "SAME_SURFACE", True
    else:
        # nearest-neighbor pair from different photos -> unambiguous DIFFERENT
        a_idx = (cand_index * 7919) % 2000
        d2 = ((means - means[a_idx]) ** 2).sum(axis=1)
        order = np.argsort(d2)
        pa = pool[a_idx][1]
        b_idx = next(b for b in order[1:] if pool[b][1] != pa)
        c1, _ = pool[a_idx]; c2, _ = pool[b_idx]
        truth, strong = "DIFFERENT", True
    g = _cp_cc_view(rng, c1, "d65") + _cp_cc_view(rng, c2, "d65")
    i1 = rng.pick(["xblue", "xred", "warm", "cool", "d65"])
    i2 = rng.pick(["xblue", "xred", "warm", "cool", "d65"])
    expo = rng.frange(0.5, 1.0)
    f = _cp_cc_view(rng, c1, i1, expo) + _cp_cc_view(rng, c2, i2, expo)
    return f, g, truth, strong

# ---------------- t2 shapetrans candidates ----------------

def _shp_morph_cov(rng, ca, cb, lam, cx, cy, scale, rot, size, fg):
    a = G._raster(ca, cx, cy, scale, rot, size, fg)
    b = G._raster(cb, cx, cy, scale, rot, size, fg)
    return (1 - lam) * a + lam * b

def cand_shapetrans(rng, _idx):
    kind = rng.irange(0, 4)
    cls = rng.irange(0, 3)
    rot = rng.frange(0, 2 * math.pi)
    if kind == 0:
        # inter-class morph; truth = lambda-majority class
        other = (cls + rng.irange(1, 3)) % 3
        lam = rng.pick([rng.frange(0.10, 0.35), rng.frange(0.65, 0.90)])
        truth = G.SH_CLASSES[cls if lam < 0.5 else other]
        strong = True
        cx = 48 + rng.frange(-10, 10); cy = 48 + rng.frange(-10, 10)
        scale = rng.frange(30, 44)
        morph = (cls, other, lam)
    else:
        truth = G.SH_CLASSES[cls]
        strong = True
        morph = None
        if kind == 1:  # extreme rotation / scale
            rot = rng.pick([rng.frange(0, 0.6), rng.frange(math.pi - 0.6, math.pi + 0.6)])
            scale = rng.pick([rng.frange(20, 26), rng.frange(44, 52)])
        elif kind == 2:  # off-center
            scale = rng.frange(30, 44)
        else:  # heavy clutter
            scale = rng.frange(30, 44)
        cx = 48 + rng.frange(-14, 14); cy = 48 + rng.frange(-14, 14)
    ph, _ = G.photo_crop(rng, 96, 96)
    bg = (np.asarray(G.Image.fromarray(ph).convert("L"), dtype=np.float64)) * 0.45
    fg = 235
    if morph is not None:
        ca, cb, lam = morph
        cov = _shp_morph_cov(rng, ca, cb, lam, cx, cy, scale, rot, 96, fg)
        img = (bg * (1 - cov) + fg * cov)
        img = np.clip(img.astype(np.int16) + _znoise(rng, -4, 5, img.shape),
                      0, 255).astype(np.uint8)
    else:
        img = G._shape_frame(rng, cls, cx, cy, scale, rot, 96, bg, fg)
    if kind != 2:
        # occlusion bar / distractor blob to fool formation
        if rng.coin(0.5):
            by = int(cy + rng.frange(-8, 8))
            img[max(0, by - 7):min(96, by + 7), :] = 20
        else:
            for _ in range(20):
                bx = rng.frange(16, 80); by = rng.frange(16, 80)
                if math.hypot(bx - cx, by - cy) > scale:
                    break
            cov = G._raster(0, bx, by, scale * rng.frange(0.7, 1.0), 0.0, 96, fg)
            img = np.clip(bg * (1 - cov) + fg * cov, 0, 255)
            img = G._shape_frame(rng, cls, cx, cy, scale, rot, 96,
                                 img.astype(np.float64), fg, noise=0)
            img = np.clip(img.astype(np.int16) + _znoise(rng, -4, 5, img.shape),
                          0, 255).astype(np.uint8)
    f = img.tobytes()
    # G: clean 48x48 render of the (possibly morphed) target
    gbg = np.full((48, 48), 100.0)
    if morph is not None:
        ca, cb, lam = morph
        cov = _shp_morph_cov(rng, ca, cb, lam, 24, 24, 16, rot, 48, 235)
        gimg = gbg * (1 - cov) + 235 * cov
        gimg = np.clip(gimg.astype(np.int16) + _znoise(rng, -2, 3, gimg.shape),
                       0, 255).astype(np.uint8)
    else:
        gimg = G._shape_frame(rng, cls, 24, 24, 16, rot, 48, gbg, 235, noise=2)
    g = gimg.tobytes()
    assert len(f) == G.SH_F and len(g) == G.SH_G
    return f, g, truth, strong

# ---------------- t3 pitchdisc candidates ----------------

def _vibrato_tone(f, dur, rng, depth, rate, phase, inharmonic):
    n = int(G.RATE * dur)
    t = np.arange(n) / G.RATE
    fi = f * (1 + depth * np.sin(2 * math.pi * rate * t + phase))
    ph = 2 * math.pi * np.cumsum(fi) / G.RATE
    sig = np.sin(ph)
    if inharmonic:
        sig = sig + 0.35 * np.sin(2.03 * ph + rng.frange(0, 6.283)) \
                  + 0.20 * np.sin(2.97 * ph + rng.frange(0, 6.283))
    sig = sig * G._ramps(n)
    return sig

def cand_pitchdisc(rng, _idx):
    fa = rng.frange(220, 660)
    r = rng.pick([-1.0, 1.0]) * rng.frange(0.01, 0.25)
    fb = fa * (1 + r)
    truth = G._ptc_truth(fa, fb)
    strong = True  # |r| >= 0.01, away from the 0.005 threshold
    # F: glide / harmonic-distractor patterns to fool formation (PTC-2/PTC-3)
    sub = rng.irange(0, 3)
    if sub == 0:
        delta = rng.frange(0.015, 0.03) * rng.pick([-1, 1])
        fbuf = G._ptc_render(fa, fa, G._ptc_harms(rng), G._ptc_harms(rng), rng,
                             glide_b=(fa, fa * (1 + delta)))
    elif sub == 1:
        fbuf = G._ptc_render(fa, fb, G._ptc_harms(rng),
                             G._ptc_harms(rng, distractor=True), rng)
    else:
        fbuf = G._ptc_render(fa, fb, G._ptc_harms(rng), G._ptc_harms(rng), rng)
    # G: true endpoints, but vibrato + inharmonic partials attack the
    # interpolated-autocorrelation endpoint estimator
    depth = rng.frange(0.0, 0.04)
    rate = rng.frange(3.0, 9.0)
    ga = _vibrato_tone(fa, 1.0, rng, depth, rate, rng.frange(0, 6.283),
                       rng.coin(0.6))
    gb = _vibrato_tone(fb, 1.0, rng, depth, rate, rng.frange(0, 6.283),
                       rng.coin(0.6))
    gbuf = np.concatenate([ga, gb])
    return G.tone_bytes(fbuf), G.tone_bytes(gbuf), truth, strong

# ---------------- t4 timbredisc candidates ----------------

def _tmb_margin(profile):
    a1 = profile.get(1, 1e-9)
    p2 = (profile.get(2, 0.0) / a1) ** 2 * 1000
    p3 = (profile.get(3, 0.0) / a1) ** 2 * 1000
    ds = sorted((p2 - t2) ** 2 + (p3 - t3) ** 2
                for t2, t3 in G.TMB_TMPL.values())
    return ds[1] - ds[0]

def cand_timbredisc(rng, _idx):
    ca = rng.pick(G.TMB_CLASSES); cb = rng.pick(G.TMB_CLASSES)
    lam = rng.uniform()
    profile = G._interp_profile(G.TMB_PROFILES[ca], G.TMB_PROFILES[cb], lam)
    # adversarial high harmonics: leak into the Goertzel m=1..3 bins
    for k in range(4, 9):
        if rng.coin(0.5):
            profile[k] = profile.get(k, 0.0) + rng.frange(0.1, 1.0)
    truth = G._tmb_template_class(profile)
    strong = _tmb_margin(profile) >= 200000
    f = G.tone_bytes(G._tmb_render(profile, rng))
    g = G.tone_bytes(G._tmb_render(profile, rng))
    return f, g, truth, strong

# ---------------- t5 motiondir candidates ----------------

def _cp_mot_frames(region, direction, nframes, contrast=1.0, rng=None,
                   flicker=None):
    """Same scene model as gen_r2a._mot_frames (32x32 window drifting across
    the 48x48 region with wraparound in the 16px slack) but with vectorized
    noise draws; the slow per-pixel Python loop in _mot_frames is the only
    difference."""
    dx, dy = G.MOT_VEC[direction]
    mdx, mdy = (G.MOT_VEC[flicker[1]][0], G.MOT_VEC[flicker[1]][1]) \
        if flicker else (0, 0)
    sx = rng.frange(0, 16); sy = rng.frange(0, 16)
    mean = region.mean()
    reg = np.clip(mean + (region - mean) * contrast, 0, 255)
    frames = []
    for t in range(nframes):
        if flicker and rng.uniform() < flicker[0]:
            wx = (sx + mdx * t) % 16; wy = (sy + mdy * t) % 16
        else:
            wx = (sx + dx * t) % 16; wy = (sy + dy * t) % 16
        ix, iy = int(wx), int(wy)
        fr = reg[iy:iy + 32, ix:ix + 32].copy()
        fr += _znoise(rng, -3, 4, fr.shape)
        frames.append(np.clip(fr, 0, 255).astype(np.uint8))
    return frames

def _grating_region(rng, direction, period):
    dx, dy = G.MOT_VEC[direction]
    n = math.hypot(dx, dy)
    ux, uy = dx / n, dy / n
    ys, xs = np.mgrid[0:48, 0:48].astype(np.float64)
    ph = 2 * math.pi * (xs * ux + ys * uy) / period + rng.frange(0, 2 * math.pi)
    return 128 + 100 * np.sin(ph)

def cand_motiondir(rng, _idx):
    direction = rng.pick(G.MOT_DIRS)
    truth = direction
    strong = True  # exact displacement by construction
    kind = rng.irange(0, 3)
    if kind == 0:
        # aliasing grating: 2px/frame motion vs 4px period -> pi phase/frame
        period = rng.pick([4, 6, 8])
        region = _grating_region(rng, direction, period)
    else:
        region = G._mot_region(rng)
    if kind == 1:
        F = _cp_mot_frames(region, direction, 50, contrast=0.15, rng=rng)
    elif kind == 2:
        mdir = rng.pick(G.MOT_DIRS)
        F = _cp_mot_frames(region, direction, 50, rng=rng, flicker=(0.3, mdir))
    else:
        F = _cp_mot_frames(region, direction, 50, rng=rng)
    Gf = G._mot_high_contrast(_cp_mot_frames(region, direction, 50, rng=rng))
    f = b"".join(fr.tobytes() for fr in F)
    g = b"".join(fr.tobytes() for fr in Gf)
    assert len(f) == G.MOT_F and len(g) == G.MOT_G
    return f, g, truth, strong

CAND = [cand_colordisc, cand_colorconst, cand_shapetrans,
        cand_pitchdisc, cand_timbredisc, cand_motiondir]

# ---------------- driver ----------------

def parse_ledger(path):
    rows = []
    for line in open(path):
        p = dict(kv.split("=", 1) for kv in line.strip().split(" ")
                 if "=" in kv and not kv.startswith("hash="))
        idx = int(p["fixture"].split("_i")[1].split("_")[0])
        rows.append((idx, p["disp"], p["judgment"]))
    return rows

def run_task(task):
    tname = TASK_NAMES[task]
    tdir = os.path.join(SCRATCH, tname)
    os.makedirs(tdir, exist_ok=True)
    # 1. generate candidates
    cands = []
    for i in range(CP_BUDGET):
        crng = G.Rng(G.stream_seed(CP_MASTER, 100 + task, i))
        cands.append(CAND[task](crng, i))
    # 2. write scratch fixtures (family 40 = scratch marker)
    paths = []
    for i, (f, g, truth, strong) in enumerate(cands):
        p = os.path.join(tdir, "cand_%d.r2fx" % i)
        G.write_r2fx(p, task, 8000 + i, 40, f, g)
        G.write_truth(p + ".truth", truth)
        paths.append(p)
    listf = os.path.join(tdir, "list.txt")
    with open(listf, "w") as fh:
        fh.write("\n".join(paths) + "\n")
    ledger = os.path.join(tdir, "ledger.txt")
    with open(os.path.join(tdir, "stdout.txt"), "w") as out:
        subprocess.run([BIN, "runlist", listf, ledger, "union"],
                       stdout=out, stderr=subprocess.STDOUT, check=True)
    # 3. select: INSTALL + wrong + strong truth
    kept = []
    for idx, disp, judg in parse_ledger(ledger):
        i = idx - 8000
        truth = cands[i][2]
        if disp == "INSTALL" and judg != truth and cands[i][3]:
            kept.append(i)
            if len(kept) >= CP_KEEP:
                break
    # 4. write final fixtures (family 4)
    os.makedirs(OUTDIR, exist_ok=True)
    man = open(os.path.join(OUTDIR, "MANIFEST_%s.sha256" % tname), "w")
    for k, i in enumerate(kept):
        f, g, truth, _ = cands[i]
        rel = "cp_%s_%d.r2fx" % (tname, k)
        p = os.path.join(OUTDIR, rel)
        G.write_r2fx(p, task, CP_INDEX_BASE + k, CP_FAMILY, f, g)
        G.write_truth(p + ".truth", truth)
        h = hashlib.sha256(open(p, "rb").read()).hexdigest()
        man.write("%s  ./%s\n" % (h, rel))
    man.close()
    # 5. generator ledger
    with open(os.path.join(OUTDIR, "gen_cp_%s.jsonl" % tname), "w") as lg:
        lg.write(json.dumps({"event": "search", "task": tname, "task_id": task,
                             "seed": CP_MASTER, "budget": CP_BUDGET,
                             "kept": len(kept)}) + "\n")
        for k, i in enumerate(kept):
            lg.write(json.dumps({"event": "keep", "task": tname,
                                 "cand": i, "slot": k,
                                 "truth": cands[i][2]}) + "\n")
    # 6. clean scratch fixtures (keep ledger + stdout for audit)
    for p in paths:
        os.remove(p)
        os.remove(p + ".truth")
    print("task %s: budget=%d kept=%d" % (tname, CP_BUDGET, len(kept)), flush=True)
    return len(kept)

def main():
    which = sys.argv[1:] or [str(t) for t in range(6)]
    total = 0
    for w in which:
        ti = int(w)
        # skip tasks already completed (gen_cp_<name>.jsonl with a search event)
        tname = TASK_NAMES[ti]
        jpath = os.path.join(OUTDIR, "gen_cp_%s.jsonl" % tname)
        if os.path.exists(jpath):
            try:
                first = open(jpath).readline()
                if '"event": "search"' in first:
                    print("SKIP %s (already complete)" % tname, flush=True)
                    continue
            except OSError:
                pass
        total += run_task(ti)
    print("TOTAL kept: %d" % total)

if __name__ == "__main__":
    main()
