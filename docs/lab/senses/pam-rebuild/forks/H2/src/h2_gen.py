#!/usr/bin/env python3
"""PAM fork H2 — augmentation fixture generator (h2_gen.py).

Builds the frozen augmentation sets from PREREG_H2.md section 3:
  normal:      4,260 h2n_<task>_<i>  (SAME distributions as frozen primary)
  adversarial: 4,815 h2a_<task>_<i>  (KB4-targeted, deliberately misleading)

Deterministic: MASTER=20260922; stream ids normal-ext=400+taskidx,
adversarial=500+taskidx (taskidx 0..5 = colordisc..motiondir, same as the
harness gen.py convention); per-fixture seed =
splitmix64(splitmix64(MASTER ^ stream*0x9E3779B97F4A7C15) ^ index*0xBF58476D1CE4E5B9)
which is exactly harness gen.stream_seed(MASTER, stream, index).

Truth files h2n_*/h2a_*.truth written alongside every fixture.
Fixtures live in forks/H2/fixtures/ (lab-local, NOT committed; committed
artifacts are this script + FIXTURES_MANIFEST.sha256 in evidence/).

Color math, tone synthesis, photo pool, and binary writers are imported from
the frozen harness generator (senses/rebuild/harness/gen.py) so the normal
set shares its distributions exactly.
"""
import math
import os
import sys

LAB = os.path.expanduser("~/workspace/tnn-lab")
sys.path.insert(0, os.path.join(LAB, "senses/rebuild/harness"))
import gen as G  # noqa: E402  (frozen harness generator)

MASTER = 20260922
OUT = os.path.join(LAB, "senses/pam-rebuild/forks/H2/fixtures")
TASKS = ["colordisc", "colorconst", "shapetrans", "pitchdisc", "timbredisc", "motiondir"]

N_NORMAL = [900, 600, 1080, 600, 600, 480]
N_ADV = [900, 480, 1080, 900, 900, 555]

fallback_count = 0  # trap searches that exhausted 200 resamples


def rng_for(taskidx, adv, index):
    stream = (500 if adv else 400) + taskidx
    return G.Rng(G.stream_seed(MASTER, stream, index))


def wpath(task, adv, index, ext):
    tag = "h2a" if adv else "h2n"
    return os.path.join(OUT, "%s_%s_%04d%s" % (tag, task, index, ext))


# ------------------------------------------------------- T1 colordisc
def gen_colordisc_normal(idx):
    rng = rng_for(0, False, idx)
    base = G._rand_color(rng)
    if idx < 300:  # SAME (mirrors primary ratios: 1/2 identical, 1/2 near)
        c2 = base if idx < 150 else G._color_at_distance(rng, base, rng.range(0.4, 1.6))
        truth = "SAME"
    else:  # DIFFERENT, graded like primary (35% easy / 32.5% med / 32.5% hard)
        k = idx - 300
        if k < 210:
            de = rng.range(10, 28)
        elif k < 405:
            de = rng.range(4, 10)
        else:
            de = rng.range(2.4, 4.0)
        c2 = G._color_at_distance(rng, base, de)
        truth = "DIFFERENT"
    p = wpath("colordisc", False, idx, ".img")
    G.write_img(p, 128, 64, G._patch_img(base, c2))
    G.write_truth(p, truth)
    return truth


def _rgb_dist(c1, c2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(c1, c2)))


def gen_colordisc_adv(idx):
    """KB4 traps. rgb-trap: truth SAME (dE2000 in [0.8,2.0]) but mean-RGB
    Euclidean > 60 (fools mean-RGB features). gray-trap: truth DIFFERENT
    (dE2000 in [2.6,5.0]) but mean-RGB Euclidean < 25."""
    global fallback_count
    rng = rng_for(0, True, idx)
    rgb_trap = idx < 450
    hit = None
    if rgb_trap:
        # rgb-trap: truth SAME (dE2000 in [0.8,2.0]) but mean-RGB Euclidean
        # > 60. Constructed by walking hue/chroma INTO the gamut from a
        # saturated corner: near the sRGB boundary (green/cyan) a Lab step
        # moves RGB fast while dE2000's chroma/hue weighting discounts it.
        # (Empirically mapped 2026-09-22; <=200 deterministic resamples.)
        corners = [(0, 255, 0), (0, 255, 255), (40, 255, 40), (0, 235, 140),
                   (90, 255, 0), (0, 255, 180), (120, 255, 60), (0, 210, 255)]
        best = None
        for t in range(200):
            c2 = corners[rng.int(len(corners))]
            L2, a2, b2 = G.rgb_to_lab(*c2)
            C2 = math.hypot(a2, b2)
            h2 = math.degrees(math.atan2(b2, a2))
            dL = rng.range(-5, 3)
            dC = -rng.range(2, 16)
            dh = rng.range(-10, 10)
            C1 = max(1.0, C2 + dC)
            a1 = C1 * math.cos(math.radians(h2 + dh))
            b1 = C1 * math.sin(math.radians(h2 + dh))
            L1 = max(0.0, min(100.0, L2 + dL))
            base = G._lab_to_srgb(L1, a1, b1)
            de = G.delta_e_2000((L2, a2, b2), G.rgb_to_lab(*base))
            rd = _rgb_dist(base, c2)
            if 0.8 <= de <= 2.0 and rd > 60 and (best is None or rd > best[0]):
                best = (rd, base, c2)
        if best is not None:
            hit = (best[1], best[2], "SAME")
    else:
        for t in range(200):
            # gray-trap: lightness walk on near-grays; dE2000 ~ dL, RGB small
            g = rng.int(256)
            base = (g, g, g)
            L0, a0, b0 = G.rgb_to_lab(*base)
            dL = rng.range(2.5, 8) * (1 if rng.uniform() < 0.5 else -1)
            L1 = max(0.0, min(100.0, L0 + dL))
            c2 = G._lab_to_srgb(L1, a0, b0)
            de = G.delta_e_2000((L0, a0, b0), G.rgb_to_lab(*c2))
            if 2.6 <= de <= 5.0 and _rgb_dist(base, c2) < 25:
                hit = (base, c2, "DIFFERENT")
                break
    if hit is None:
        fallback_count += 1
        base = G._rand_color(rng)
        # in-band but not a trap: still a valid labeled fixture
        de = rng.range(0.8, 2.0) if rgb_trap else rng.range(2.6, 5.0)
        c2 = G._color_at_distance(rng, base, de)
        truth = "SAME" if rgb_trap else "DIFFERENT"
    else:
        base, c2, truth = hit
    p = wpath("colordisc", True, idx, ".img")
    G.write_img(p, 128, 64, G._patch_img(base, c2))
    G.write_truth(p, truth)
    return truth


# ------------------------------------------------------- T2 colorconst
def gen_colorconst_normal(idx):
    rng = rng_for(1, False, idx)
    return _colorconst_body(rng, idx, adv=False, photo_count=170)


def gen_colorconst_adv(idx):
    # photo pool index offset +5000 (frozen design)
    rng = rng_for(1, True, idx)
    return _colorconst_body(rng, idx, adv=True, photo_count=170)


def _colorconst_body(rng, idx, adv, photo_count):
    illums = ["d65", "warm", "cool"] if not adv else ["xblue", "xred", "warm"]
    expo = 1.0 if not adv else 0.55

    def photo_at(i):
        return G.load_photo((i + (5000 if adv else 0)) % photo_count)

    if idx % 2 == 0:  # SAME_SURFACE
        ph = rng.int(photo_count)
        ox, oy = rng.int(160 - 64), rng.int(120 - 64)
        crop = G.crop_photo(photo_at(ph), 160, ox, oy, 64, 64)
        i1, i2 = rng.int(3), rng.int(3)
        while i2 == i1:
            i2 = rng.int(3)
        p1 = G._render_panel(crop, illums[i1], expo)
        p2 = G._render_panel(crop, illums[i2], expo)
        truth = "SAME_SURFACE"
    else:  # DIFFERENT
        ph1, ph2 = rng.int(photo_count), rng.int(photo_count)
        while ph2 == ph1:
            ph2 = rng.int(photo_count)
        c1 = G.crop_photo(photo_at(ph1), 160, rng.int(160 - 64), rng.int(120 - 64), 64, 64)
        c2 = G.crop_photo(photo_at(ph2), 160, rng.int(160 - 64), rng.int(120 - 64), 64, 64)
        p1 = G._render_panel(c1, rng.pick(illums), expo)
        p2 = G._render_panel(c2, rng.pick(illums), expo)
        truth = "DIFFERENT"
    px = []
    for y in range(64):
        for x in range(128):
            px.append(p1[y * 64 + x] if x < 64 else p2[y * 64 + (x - 64)])
    p = wpath("colorconst", adv, idx, ".img")
    G.write_img(p, 128, 64, px)
    G.write_truth(p, truth)
    return truth


# ------------------------------------------------------- T3 shapetrans
def _shape_img(rng, kind, adv, occl_bar, photo_count):
    W = 96
    crop = G.crop_photo(G.load_photo(rng.int(photo_count)), 160,
                        rng.int(160 - W), rng.int(120 - W), W, W)
    dim = 0.45 if not adv else 1.0
    bg_px = [tuple(int(c * dim) for c in p) for p in crop]
    rot = rng.uniform() * 2 * math.pi
    scale = rng.range(30, 44) if not adv else rng.range(16, 26)
    cx = W / 2 + rng.range(-14, 14)
    cy = W / 2 + rng.range(-14, 14)
    fg = (235, 235, 235) if not adv else tuple(int(rng.range(120, 175)) for _ in range(3))
    cosr, sinr = math.cos(rot), math.sin(rot)
    px = []
    SS = 3
    for y in range(W):
        for x in range(W):
            bgc = bg_px[y * W + x]
            hit = 0
            for sy in range(SS):
                for sx in range(SS):
                    fx = x + (sx + 0.5) / SS - 0.5 - cx
                    fy = y + (sy + 0.5) / SS - 0.5 - cy
                    ux = (fx * cosr + fy * sinr) / scale
                    uy = (-fx * sinr + fy * cosr) / scale
                    if G._point_in_shape(kind, ux, uy):
                        hit += 1
            a = hit / (SS * SS)
            col = tuple(int(fg[i] * a + bgc[i] * (1 - a)) for i in range(3))
            if occl_bar and 38 <= y <= 54:
                col = (25, 25, 25)  # solid dark occlusion bar across the shape
            px.append(col)
    return px


def gen_shapetrans_normal(idx):
    rng = rng_for(2, False, idx)
    kind = ["circle", "triangle", "square"][idx % 3]
    px = _shape_img(rng, kind, adv=False, occl_bar=False, photo_count=170)
    truth = {"circle": "CIRCLE", "triangle": "TRIANGLE", "square": "SQUARE"}[kind]
    p = wpath("shapetrans", False, idx, ".img")
    G.write_img(p, 96, 96, px)
    G.write_truth(p, truth)
    return truth


def gen_shapetrans_adv(idx):
    rng = rng_for(2, True, idx)
    occl = idx < 540  # occlusion-bar x540, else low-contrast gray + full clutter
    sub = idx if occl else idx - 540
    kind = ["circle", "triangle", "square"][(sub // 180) % 3]
    px = _shape_img(rng, kind, adv=True, occl_bar=occl, photo_count=170)
    truth = {"circle": "CIRCLE", "triangle": "TRIANGLE", "square": "SQUARE"}[kind]
    p = wpath("shapetrans", True, idx, ".img")
    G.write_img(p, 96, 96, px)
    G.write_truth(p, truth)
    return truth

# ------------------------------------------------------- T4 pitchdisc
def _pitch_pair(rng, adv, idx):
    f0 = rng.range(220, 660)
    harm_b = G.RICH_H
    if not adv:
        cls = idx % 3
        if cls == 0:
            f1, truth = f0, "SAME"
        else:
            band = idx % 4
            rel = [rng.range(0.10, 0.25), rng.range(0.02, 0.05),
                   rng.range(0.005, 0.008), rng.range(0.10, 0.25)][band]
            f1 = f0 * (1 + rel) if cls == 1 else f0 * (1 - rel)
            truth = "HIGHER" if cls == 1 else "LOWER"
    else:
        if idx < 450:  # near-threshold: straddle the 0.5% JND
            i = idx
            if i < 225:
                f1, truth = f0 * (1 + rng.range(0.0015, 0.0045)), "SAME"
            elif i % 2 == 0:
                f1, truth = f0 * (1 + rng.range(0.0055, 0.0085)), "HIGHER"
            else:
                f1, truth = f0 * (1 - rng.range(0.0055, 0.0085)), "LOWER"
        else:  # harmonic-distractor: tone B carries 0.6x 2nd + 0.3x 3rd;
            # truth from the TRUE f0 ratio, classes balanced
            harm_b = [(1, 1.0), (2, 0.6), (3, 0.3)]
            j = (idx - 450) % 3
            if j == 0:
                f1, truth = f0, "SAME"
            elif j == 1:
                f1, truth = f0 * (1 + rng.range(0.02, 0.10)), "HIGHER"
            else:
                f1, truth = f0 * (1 - rng.range(0.02, 0.10)), "LOWER"
    gap = [0] * int(G.SR * 0.08)
    samples = G._tone(f0, 0.4, G.RICH_H) + gap + G._tone(f1, 0.4, harm_b)
    return samples, truth


def gen_pitchdisc(idx, adv):
    rng = rng_for(3, adv, idx)
    samples, truth = _pitch_pair(rng, adv, idx)
    p = wpath("pitchdisc", adv, idx, ".pcm")
    G.write_pcm(p, G.SR, samples)
    G.write_truth(p, truth)
    return truth


# ------------------------------------------------------- T5 timbredisc
def _centroid_float(samples, sr=16000, f0=440.0, w=2048):
    """Float reference centroid mirroring A's integer harmonic-DFT method:
    r = 1000 * sum(h*E_h)/sum(E_h), h = 1..8 below Nyquist."""
    se = she = 0.0
    for h in range(1, 9):
        if 2 * h * f0 >= sr:
            break
        re = im = 0.0
        ph = 2 * math.pi * f0 * h / sr
        for i in range(w):
            s = samples[i]
            re += s * math.cos(ph * i)
            im += s * math.sin(ph * i)
        e = re * re + im * im
        se += e
        she += h * e
    return 1000.0 * she / se if se > 0 else 0.0


def _boundary_straddle_profile(rng):
    """Random harmonic profile whose measured centroid lands within +-10%
    of one of the 1075/1400/3000 boundaries. <=200 resamples."""
    global fallback_count
    best = None
    for _ in range(200):
        n = 2 + rng.int(7)
        amps = [1.0]
        for h in range(2, n + 1):
            amps.append(rng.range(0.0, 0.9 / (h ** 0.7)))
        harm = [(h, a) for h, a in enumerate(amps, start=1)]
        samples = G._tone(440.0, 0.8, harm)
        r = _centroid_float(samples)
        ok = any(abs(r - b) / b <= 0.10 for b in (1075, 1400, 3000))
        if ok:
            return harm, r
        if best is None or min(abs(r - b) / b for b in (1075, 1400, 3000)) < best[0]:
            best = (min(abs(r - b) / b for b in (1075, 1400, 3000)), harm, r)
    fallback_count += 1
    return best[1], best[2]


def _class_of_r(r):
    if r < 1075:
        return "PURE"
    if r < 1400:
        return "DARK"
    if r < 3000:
        return "RICH"
    return "BRIGHT"


def gen_timbredisc_normal(idx):
    rng = rng_for(4, False, idx)
    cls = ["PURE", "BRIGHT", "DARK", "RICH"][idx % 4]
    samples = G._tone(440.0, 0.8, G.TIMBRES[cls])
    p = wpath("timbredisc", False, idx, ".pcm")
    G.write_pcm(p, G.SR, samples)
    G.write_truth(p, cls)
    return cls


def gen_timbredisc_adv(idx):
    rng = rng_for(4, True, idx)
    if idx < 450:  # boundary-straddling
        harm, r = _boundary_straddle_profile(rng)
        cls = _class_of_r(r)
    else:  # distractor harmonics (same design as harness adversarial)
        u = rng.uniform()
        if u < 0.25:
            harm = [(1, 0.5), (2, 0.9), (3, 0.8), (4, 0.7), (5, 0.6), (6, 0.5)]
            cls = "BRIGHT"
        elif u < 0.5:
            harm = [(1, 1.0), (2, 0.45), (3, 0.35), (4, 0.08)]
            cls = "DARK"
        elif u < 0.75:
            harm = [(1, 1.0), (2, 0.7), (3, 0.6), (4, 0.5), (5, 0.4), (6, 0.3)]
            cls = "RICH"
        else:
            harm = [(1, 1.0), (2, 0.06)]
            cls = "PURE"
    samples = G._tone(440.0, 0.8, harm)
    p = wpath("timbredisc", True, idx, ".pcm")
    G.write_pcm(p, G.SR, samples)
    G.write_truth(p, cls)
    return cls


# ------------------------------------------------------- T6 motiondir
def _motion_clip(rng, adv, truth):
    from PIL import Image  # noqa
    photo = G.load_photo(rng.int(170))
    W = 64
    step = 1 if adv else 2
    contrast = 0.25 if adv else 1.0
    mean = [0.0, 0.0, 0.0]
    for p in photo:
        for i in range(3):
            mean[i] += p[i]
    mean = [m / len(photo) for m in mean]
    vec = G.DIRS.get(truth, (0, 0))
    ox, oy = rng.int(40), rng.int(24)
    frames = []
    for f in range(8):
        dx = int(round(-vec[0] * step * f))
        dy = int(round(-vec[1] * step * f))
        fr = []
        for y in range(W):
            for x in range(W):
                sx = (ox + x + dx) % 160
                sy = (oy + y + dy) % 120
                r, g, b = photo[sy * 160 + sx]
                fr.append(tuple(int(max(0, min(255, mean[i] + (c - mean[i]) * contrast)))
                               for i, c in enumerate((r, g, b))))
        frames.append(fr)
    return frames


def gen_motiondir_normal(idx):
    rng = rng_for(5, False, idx)
    if idx < 32:
        truth = "STILL"
    else:
        truth = sorted(G.DIRS)[(idx - 32) % 8]
    frames = _motion_clip(rng, adv=False, truth=truth)
    p = wpath("motiondir", False, idx, ".vid")
    G.write_vid(p, 64, 64, frames)
    G.write_truth(p, truth)
    return truth


def gen_motiondir_adv(idx):
    rng = rng_for(5, True, idx)
    order = sorted(G.DIRS) + ["STILL"]  # 9 classes
    # 555 = 6*62 + 3*61, balanced
    counts = [62] * 6 + [61] * 3
    cum = 0
    truth = order[-1]
    for cls, c in zip(order, counts):
        if idx < cum + c:
            truth = cls
            break
        cum += c
    frames = _motion_clip(rng, adv=True, truth=truth)
    p = wpath("motiondir", True, idx, ".vid")
    G.write_vid(p, 64, 64, frames)
    G.write_truth(p, truth)
    return truth


# ------------------------------------------------------- main
GEN = [
    (gen_colordisc_normal, gen_colordisc_adv),
    (None, None),  # colorconst handled via body wrapper (needs no extra args)
    (gen_shapetrans_normal, gen_shapetrans_adv),
    (None, None),
    (gen_timbredisc_normal, gen_timbredisc_adv),
    (gen_motiondir_normal, gen_motiondir_adv),
]


def main():
    global fallback_count
    os.makedirs(OUT, exist_ok=True)
    inv = {}
    for ti, task in enumerate(TASKS):
        for adv, n in ((False, N_NORMAL[ti]), (True, N_ADV[ti])):
            truths = {}
            for idx in range(n):
                if ti == 1:
                    t = gen_colorconst_adv(idx) if adv else gen_colorconst_normal(idx)
                elif ti == 3:
                    t = gen_pitchdisc(idx, adv)
                else:
                    t = GEN[ti][1 if adv else 0](idx)
                truths[t] = truths.get(t, 0) + 1
            key = "%s/%s" % (task, "adv" if adv else "normal")
            inv[key] = (n, truths)
            print("%s: %d  %s" % (key, n, truths), flush=True)
    total = sum(c for c, _ in inv.values())
    print("TOTAL: %d  fallbacks: %d" % (total, fallback_count), flush=True)
    assert total == 4260 + 4815, total


if __name__ == "__main__":
    main()
