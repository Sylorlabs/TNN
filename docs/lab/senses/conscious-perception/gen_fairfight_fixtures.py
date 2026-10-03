#!/usr/bin/env python3
"""FAIR FIGHT frozen fixture generator (deterministic, splitmix64).

Generates fixtures/test/ (the frozen battery) and fixtures/train/ (the
frozen training pool). Disjoint parameter sets; same generator code.
Master seed 20260923. No wall-clock, no os.urandom.

Fixture formats (per senses/rebuild INTERFACE.md):
  .img: u32 w, u32 h, W*H*3 RGB24        .pcm: u32 sr, u32 count, int16 mono
  .vid: u32 nf, u32 w, u32 h, frames RGB24
Each fixture gets a sibling .truth file: truth=<value>.

Legs:
  omission/      late-onset events beyond the autopilot's 2048-sample window
  inattentional/ goal-relevant small target swamped by a big distractor
  ambiguity/     first-pass judgments at/below the decision boundary
  illusion/      TNN optical-illusion analogs (fooled estimators)
  redteam/       attention traps: maximally ambiguous, budget-burning
"""
import math, os, struct, hashlib

MASTER_SEED = 20260923
ROOT = os.path.dirname(os.path.abspath(__file__))
FX = os.path.join(ROOT, "fixtures")

MASK64 = (1 << 64) - 1
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
    def int(self, n):
        return self.u64() % n

def stream_seed(stream, index):
    def sm(s):
        s = (s + 0x9E3779B97F4A7C15) & MASK64
        z = s
        z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & MASK64
        z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & MASK64
        return z ^ (z >> 31)
    h = sm(MASTER_SEED ^ (stream * 0x9E3779B97F4A7C15))
    return sm(h ^ (index * 0xBF58476D1CE4E5B9))

SR = 44100
def sine(f, n, A, ph=0.0):
    return [int(round(A * math.sin(2 * math.pi * f * i / SR + ph))) for i in range(n)]

def bright(f, n, A):
    # fundamental + 6 harmonics, near-flat falloff -> spectral centroid
    # well above the 3000 BRIGHT boundary (target r ~= 3300+)
    out = [0.0] * n
    for h in range(1, 7):
        a = A / (h ** 0.15)
        for i in range(n):
            out[i] += a * math.sin(2 * math.pi * f * h * i / SR)
    peak = max(1.0, max(abs(v) for v in out))
    return [int(round(v / peak * A)) for v in out]

def clamp16(v):
    return max(-32768, min(32767, v))

def write_pcm(path, samples):
    with open(path, "wb") as f:
        f.write(struct.pack("<II", SR, len(samples)))
        f.write(struct.pack("<%dh" % len(samples), *[clamp16(s) for s in samples]))

def write_img(path, w, h, px):
    # px: list of (r,g,b) length w*h
    with open(path, "wb") as f:
        f.write(struct.pack("<II", w, h))
        f.write(bytes(b for p in px for b in p))

def write_vid(path, w, h, frames):
    # frames: list of px lists
    with open(path, "wb") as f:
        f.write(struct.pack("<III", len(frames), w, h))
        for px in frames:
            f.write(bytes(b for p in px for b in p))

def write_truth(path, truth, note=""):
    with open(path + ".truth", "w") as f:
        f.write("truth=%s\n" % truth)
        if note:
            f.write("note=%s\n" % note)

def blit_halves(w, h, left, right):
    # left/right: lists of (r,g,b) length (w//2)*h, row-major within the half
    hw = w // 2
    px = [None] * (w * h)
    for y in range(h):
        for x in range(w):
            if x < hw:
                px[y * w + x] = left[y * hw + x]
            else:
                px[y * w + x] = right[y * hw + (x - hw)]
    return px

# ------------------------------------------------------------------ builders
def b_om_pitch_late(dirpath, name, fA, fB_early, fB_late, truth, stream, idx, half=8192, A=12000):
    rng = Rng(stream_seed(stream, idx))
    ph = rng.uniform() * 2 * math.pi
    a = sine(fA, half, A, ph)
    b = sine(fB_early, 2048, A, ph) + sine(fB_late, half - 2048, A, ph)
    p = os.path.join(dirpath, name + ".pcm")
    write_pcm(p, a + b)
    write_truth(p, truth, "pitchdisc omission: late-onset event in half B beyond 2048-sample first-pass window")

def b_om_timbre_late(dirpath, name, f, truth, stream, idx, n=8192, A=12000):
    rng = Rng(stream_seed(stream, idx))
    ph = rng.uniform() * 2 * math.pi
    pure = sine(f, 2048, A, ph)
    br = bright(f, n - 2048, A)
    p = os.path.join(dirpath, name + ".pcm")
    write_pcm(p, pure + br)
    write_truth(p, truth, "timbredisc omission: timbre turns BRIGHT after 2048 samples")

def b_om_timbre_const(dirpath, name, f, truth, stream, idx, n=8192, A=12000):
    br = bright(f, n, A)
    p = os.path.join(dirpath, name + ".pcm")
    write_pcm(p, br)
    write_truth(p, truth, "timbredisc control: constant BRIGHT")

def b_amb_pitch(dirpath, name, fA, fB, truth, stream, idx, half=8192, A=12000):
    rng = Rng(stream_seed(stream, idx))
    ph = rng.uniform() * 2 * math.pi
    p = os.path.join(dirpath, name + ".pcm")
    write_pcm(p, sine(fA, half, A, ph) + sine(fB, half, A, ph))
    write_truth(p, truth, "pitchdisc ambiguity: |d| near the 2%% decision boundary")

def b_amb_color(dirpath, name, d_rgb, truth, stream, idx, w=64, h=64):
    left = [(128, 128, 128)] * ((w // 2) * h)
    right = [tuple(128 + d for d in d_rgb)] * ((w // 2) * h)
    p = os.path.join(dirpath, name + ".img")
    write_img(p, w, h, blit_halves(w, h, left, right))
    write_truth(p, truth, "colordisc ambiguity: euclidean dist near the 40-unit boundary")

def b_ill_spike(dirpath, name, spike_ch, truth, stream, idx, w=64, h=64):
    # checkerboard {100,200} gray texture both halves; half A gets one
    # blown-out pixel in spike_ch. von Kries white-patch max is corrupted.
    def checker(half):
        px = []
        for y in range(h):
            for x in range(half):
                v = 100 if ((x + y) % 2 == 0) else 200
                px.append((v, v, v))
        return px
    A = checker(w // 2)
    B = checker(w // 2)
    i = (h // 2) * (w // 2) + (w // 4)
    r, g, b = A[i]
    ch = [r, g, b]
    ch[spike_ch] = 255
    A[i] = tuple(ch)
    p = os.path.join(dirpath, name + ".img")
    write_img(p, w, h, blit_halves(w, h, A, B))
    write_truth(p, truth, "colorconst illusion: single saturated-pixel spike corrupts the white-patch illuminant estimate; same surface")

def b_ill_levels(dirpath, name, truth, stream, idx, w=64, h=64):
    # different surfaces whose von Kries discounted means coincide
    def checker(half, lo, hi):
        px = []
        for y in range(h):
            for x in range(half):
                v = lo if ((x + y) % 2 == 0) else hi
                px.append((v, v, v))
        return px
    A = checker(w // 2, 100, 200)   # mean 150, max 200 -> 750 permille
    B = checker(w // 2, 75, 150)    # mean 112.5, max 150 -> 750 permille
    p = os.path.join(dirpath, name + ".img")
    write_img(p, w, h, blit_halves(w, h, A, B))
    write_truth(p, truth, "colorconst illusion: different absolute levels, identical discounted means; discount-only decoder blind")

def b_ib(dirpath, name, rect_dir, dot_dir, truth, stream, idx, w=64, h=64, nf=8, with_rect=True):
    # big dim rect drifts rect_dir slowly (dominates centroid); small bright
    # dot moves dot_dir fast (goal-relevant). truth names the DOT's motion.
    frames = []
    for t in range(nf):
        px = [(0, 0, 0)] * (w * h)
        if with_rect:
            rx = 4 + rect_dir * 2 * t
            for y in range(20, 44):
                for x in range(rx, rx + 40):
                    if 0 <= x < w:
                        px[y * w + x] = (48, 48, 48)
        dx = 56 + dot_dir * 3 * t
        for y in range(30, 33):
            for x in range(dx, dx + 3):
                if 0 <= x < w:
                    px[y * w + x] = (255, 255, 255)
        frames.append(px)
    p = os.path.join(dirpath, name + ".vid")
    write_vid(p, w, h, frames)
    write_truth(p, truth, "motiondir inattentional: goal = motion of the small bright target; big dim distractor dominates the centroid")

def b_rt_pitch(dirpath, name, fA, fB, truth, stream, idx):
    b_amb_pitch(dirpath, name, fA, fB, truth, stream, idx)
    p = os.path.join(dirpath, name + ".pcm")
    write_truth(p, truth, "pitchdisc redteam: d exactly at the 20000ppm boundary; maximally ambiguous, budget-burning")

def b_rt_color(dirpath, name, d_rgb, truth, stream, idx):
    b_amb_color(dirpath, name, d_rgb, truth, stream, idx)
    p = os.path.join(dirpath, name + ".img")
    write_truth(p, truth, "colordisc redteam: dist just under the 40-unit boundary; maximally ambiguous, budget-burning")

# ------------------------------------------------------------------ assemble
def build():
    # streams: test legs 11..15, train legs 21..25
    T = os.path.join(FX, "test"); R = os.path.join(FX, "train")
    legs = ["omission", "inattentional", "ambiguity", "illusion", "redteam"]
    for base in (T, R):
        for leg in legs:
            os.makedirs(os.path.join(base, leg), exist_ok=True)

    # ---- TEST battery (frozen) ----
    d = os.path.join(T, "omission")
    b_om_pitch_late(d, "om_p1", 440, 440, 660, "HIGHER", 11, 1)
    b_om_pitch_late(d, "om_p2", 660, 660, 440, "LOWER", 11, 2)
    b_om_pitch_late(d, "om_p3", 440, 440, 440, "SAME", 11, 3)      # control
    b_om_pitch_late(d, "om_p4", 440, 880, 880, "HIGHER", 11, 4)    # control
    b_om_timbre_late(d, "om_t1", 440, "BRIGHT", 11, 5)
    b_om_timbre_const(d, "om_t2", 520, "BRIGHT", 11, 6)            # control

    d = os.path.join(T, "inattentional")
    b_ib(d, "ib_m1", +1, -1, "W", 12, 1)
    b_ib(d, "ib_m2", +1, -1, "W", 12, 2, with_rect=False)         # control

    d = os.path.join(T, "ambiguity")
    b_amb_pitch(d, "am_p1", 440, 449.24, "HIGHER", 13, 1)         # 21000 ppm
    b_amb_color(d, "am_c1", (24, 24, 24), "DIFFERENT", 13, 2)     # dist ~41.6

    d = os.path.join(T, "illusion")
    b_ill_spike(d, "il_c1", 0, "SAME_SURFACE", 14, 1)
    b_ill_levels(d, "il_c2", "DIFFERENT", 14, 2)

    d = os.path.join(T, "redteam")
    b_rt_pitch(d, "rt_p1", 440, 448.8, "HIGHER", 15, 1)           # 20000 ppm exactly
    b_rt_color(d, "rt_c1", (28, 20, 20), "DIFFERENT", 15, 2)      # dist ~39.8

    # ---- TRAINING pool (frozen, disjoint params) ----
    d = os.path.join(R, "omission")
    b_om_pitch_late(d, "tr_om_p1", 330, 330, 495, "HIGHER", 21, 1)
    b_om_pitch_late(d, "tr_om_p2", 550, 550, 367, "LOWER", 21, 2)
    b_om_timbre_late(d, "tr_om_t1", 520, "BRIGHT", 21, 3)
    b_om_pitch_late(d, "tr_om_p3", 392, 392, 392, "SAME", 21, 4)  # control

    d = os.path.join(R, "inattentional")
    b_ib(d, "tr_ib_m1", -1, +1, "E", 22, 1)
    b_ib(d, "tr_ib_m2", -1, +1, "E", 22, 2, with_rect=False)      # control

    d = os.path.join(R, "ambiguity")
    b_amb_pitch(d, "tr_am_p1", 520, 531.44, "HIGHER", 23, 1)      # 22000 ppm
    b_amb_color(d, "tr_am_c1", (25, 25, 25), "DIFFERENT", 23, 2)  # dist ~43.3

    d = os.path.join(R, "illusion")
    b_ill_spike(d, "tr_il_c1", 1, "SAME_SURFACE", 24, 1)
    b_ill_levels(d, "tr_il_c2", "DIFFERENT", 24, 2)

    d = os.path.join(R, "redteam")
    b_rt_pitch(d, "tr_rt_p1", 520, 530.4, "HIGHER", 25, 1)
    b_rt_color(d, "tr_rt_c1", (27, 21, 21), "DIFFERENT", 25, 2)

    # ---- manifest ----
    entries = []
    for base in (T, R):
        for leg in legs:
            dd = os.path.join(base, leg)
            for fn in sorted(os.listdir(dd)):
                fp = os.path.join(dd, fn)
                h = hashlib.sha256(open(fp, "rb").read()).hexdigest()
                entries.append("%s  %s" % (h, os.path.relpath(fp, FX)))
    with open(os.path.join(FX, "MANIFEST.sha256"), "w") as f:
        f.write("# FAIR FIGHT fixtures, master seed 20260923, generated %s\n" % "2026-09-23")
        f.write("\n".join(entries) + "\n")
    print("wrote %d fixture files" % len(entries))

if __name__ == "__main__":
    build()
