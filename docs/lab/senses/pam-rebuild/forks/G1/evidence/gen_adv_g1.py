#!/usr/bin/env python3
"""G1 adversarial augmentation generator (frozen by PREREG_G1.md).

75 deliberately misleading high-confidence symmetry spoofs, master seed
20260922, splitmix64 streams. Output: evidence/adv/g1_<task>_m<M>_<i>.<ext>
+ sibling .truth files + MANIFEST_G1_ADV.sha256.

Methods (M1-M6 per PREREG_G1.md section 6):
  M1 shapetrans occlusion bar at shape centroid x (breaks REFL/ROT)
  M2 shapetrans contrast flatten 50% (symmetry scores -> near threshold)
  M3 colorconst panel-B extreme-blue illuminant + 0.55 exposure
  M4 pitchdisc fresh pairs, tone B at f0*1.006 / f0*0.994 (baits SAME)
  M5 timbredisc distractor harmonic profiles at class boundaries
  M6 motiondir whole-clip contrast flatten to 25%
"""
import hashlib
import math
import os
import struct
import sys

sys.path.insert(0, os.path.expanduser("~/workspace/tnn-lab/senses/rebuild/harness"))
from gen import _tone, RICH_H  # noqa: E402  (frozen harness synthesis)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "adv")
FIX = os.path.expanduser("~/workspace/tnn-lab/senses/rebuild/harness/fixtures")
MASTER = 20260922


def splitmix64(state):
    state = (state + 0x9E3779B97F4A7C15) & 0xFFFFFFFFFFFFFFFF
    z = state
    z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & 0xFFFFFFFFFFFFFFFF
    z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & 0xFFFFFFFFFFFFFFFF
    return (z ^ (z >> 31)) & 0xFFFFFFFFFFFFFFFF


class Rng:
    def __init__(self, seed):
        self.s = seed & 0xFFFFFFFFFFFFFFFF

    def u64(self):
        self.s = splitmix64(self.s)
        return self.s

    def range(self, lo, hi):
        return lo + (self.u64() % (hi - lo))


def stream_seed(stream, index):
    return (MASTER ^ (stream * 0x9E3779B97F4A7C15) ^ (index * 0xBF58476D1CE4E5B9)) & 0xFFFFFFFFFFFFFFFF


def read_img(path):
    with open(path, "rb") as f:
        raw = f.read()
    w, h = struct.unpack("<II", raw[:8])
    px = [tuple(raw[8 + 3 * i:8 + 3 * i + 3]) for i in range(w * h)]
    return w, h, px


def write_img(path, w, h, px):
    with open(path, "wb") as f:
        f.write(struct.pack("<II", w, h))
        for (r, g, b) in px:
            f.write(bytes((r, g, b)))


def write_pcm(path, rate, samples):
    with open(path, "wb") as f:
        f.write(struct.pack("<II", rate, len(samples)))
        f.write(struct.pack("<%dh" % len(samples), *samples))


def write_vid(path, w, h, frames):
    with open(path, "wb") as f:
        f.write(struct.pack("<III", len(frames), w, h))
        for fr in frames:
            for (r, g, b) in fr:
                f.write(bytes((r, g, b)))


def read_vid(path):
    with open(path, "rb") as f:
        raw = f.read()
    nf, w, h = struct.unpack("<III", raw[:12])
    frames = []
    o = 12
    for _ in range(nf):
        fr = [tuple(raw[o + 3 * i:o + 3 * i + 3]) for i in range(w * h)]
        frames.append(fr)
        o += 3 * w * h
    return nf, w, h, frames


def write_truth(path, value):
    with open(path + ".truth", "w") as f:
        f.write("truth=%s\n" % value)


def truth_of(path):
    with open(path + ".truth") as f:
        return f.read().strip().split("=", 1)[1]


def shape_centroid(w, h, px):
    lum = [(r + g + b) // 3 for (r, g, b) in px]
    mean = sum(lum) // len(lum)
    nbright = sum(1 for v in lum if v > mean)
    bright_is_shape = nbright * 2 <= len(lum)
    sx = sy = n = 0
    for y in range(h):
        for x in range(w):
            is_shape = (lum[y * w + x] > mean) == bright_is_shape
            if is_shape:
                sx += x
                sy += y
                n += 1
    if n == 0:
        return w // 2, h // 2, mean
    return sx // n, sy // n, mean


def main():
    os.makedirs(OUT, exist_ok=True)
    made = []

    # M1: occlusion bar at shape centroid x (20)
    for i in range(20):
        base = os.path.join(FIX, "t3_shapetrans", "primary", "p%03d.img" % i)
        w, h, px = read_img(base)
        cx, cy, mean = shape_centroid(w, h, px)
        bar = (40, 40, 40) if mean > 128 else (235, 235, 235)
        out = []
        for y in range(h):
            for x in range(w):
                if abs(x - cx) <= 4:
                    out.append(bar)
                else:
                    out.append(px[y * w + x])
        name = "g1_t3_m1_%02d.img" % i
        p = os.path.join(OUT, name)
        write_img(p, w, h, out)
        write_truth(p, truth_of(base))
        made.append(name)

    # M2: contrast flatten 50% toward mean (10)
    for i in range(20, 30):
        base = os.path.join(FIX, "t3_shapetrans", "primary", "p%03d.img" % i)
        w, h, px = read_img(base)
        mean = sum((r + g + b) // 3 for (r, g, b) in px) // len(px)
        out = [tuple(mean + (c - mean) // 2 for c in q) for q in px]
        name = "g1_t3_m2_%02d.img" % (i - 20)
        p = os.path.join(OUT, name)
        write_img(p, w, h, out)
        write_truth(p, truth_of(base))
        made.append(name)

    # M3: panel-B extreme blue illuminant + 0.55 exposure (10, SAME_SURFACE)
    for k, i in enumerate([0, 2, 4, 6, 8, 10, 12, 14, 16, 18]):
        base = os.path.join(FIX, "t2_colorconst", "primary", "p%03d.img" % i)
        w, h, px = read_img(base)
        out = []
        for y in range(h):
            for x in range(w):
                (r, g, b) = px[y * w + x]
                if x >= 64:
                    r = min(255, int(r * 0.45 * 0.55))
                    g = min(255, int(g * 0.70 * 0.55))
                    b = min(255, int(b * 1.50 * 0.55))
                out.append((r, g, b))
        name = "g1_t2_m3_%02d.img" % k
        p = os.path.join(OUT, name)
        write_img(p, w, h, out)
        t = truth_of(base)
        assert t == "SAME_SURFACE", (base, t)
        write_truth(p, t)
        made.append(name)

    # M4: fresh pitch pairs, tone B at f0*1.006 (HIGHER) / f0*0.994 (LOWER)
    SR = 16000
    for i in range(15):
        rng = Rng(stream_seed(400 + i, i))
        f0 = 220 + (rng.u64() % 44000) / 100.0
        if i % 2 == 0:
            f1, truth = f0 * 1.006, "HIGHER"
        else:
            f1, truth = f0 * 0.994, "LOWER"
        gap = [0] * int(SR * 0.08)
        samples = _tone(f0, 0.4, RICH_H) + gap + _tone(f1, 0.4, RICH_H)
        name = "g1_t4_m4_%02d.pcm" % i
        p = os.path.join(OUT, name)
        write_pcm(p, SR, samples)
        write_truth(p, truth)
        made.append(name)

    # M5: timbre distractor profiles at class boundaries (10)
    DISTR = {
        "PURE": [(1, 1.0), (2, 0.06)],
        "BRIGHT": [(1, 0.5), (2, 0.9), (3, 0.8), (4, 0.7), (5, 0.6), (6, 0.5)],
        "DARK": [(1, 1.0), (2, 0.45), (3, 0.35), (4, 0.08)],
        "RICH": [(1, 1.0), (2, 0.7), (3, 0.6), (4, 0.5), (5, 0.4), (6, 0.3)],
    }
    for i in range(10):
        base = os.path.join(FIX, "t5_timbredisc", "primary", "p%03d.pcm" % i)
        cls = truth_of(base)
        name = "g1_t5_m5_%02d.pcm" % i
        p = os.path.join(OUT, name)
        write_pcm(p, 16000, _tone(440.0, 0.8, DISTR[cls]))
        write_truth(p, cls)
        made.append(name)

    # M6: motiondir contrast flatten to 25% (10)
    for i in range(10):
        base = os.path.join(FIX, "t6_motiondir", "primary", "p%03d.vid" % i)
        nf, w, h, frames = read_vid(base)
        flat = []
        for fr in frames:
            mean = sum((r + g + b) // 3 for (r, g, b) in fr) // len(fr)
            flat.append([tuple(max(0, min(255, mean + (c - mean) // 4)) for c in q) for q in fr])
        name = "g1_t6_m6_%02d.vid" % i
        p = os.path.join(OUT, name)
        write_vid(p, w, h, flat)
        write_truth(p, truth_of(base))
        made.append(name)

    # manifest
    man = os.path.join(OUT, "MANIFEST_G1_ADV.sha256")
    with open(man, "w") as f:
        for name in sorted(made):
            for suf in ("", ".truth"):
                p = os.path.join(OUT, name + suf)
                h = hashlib.sha256(open(p, "rb").read()).hexdigest()
                f.write("%s  %s\n" % (h, name + suf))
    print("G1-adv fixtures: %d (+ truth), manifest written" % len(made))


if __name__ == "__main__":
    main()
