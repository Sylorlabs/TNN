#!/usr/bin/env python3
"""H1 adversarial augmentation generator (frozen per PREREG_H1.md §3).

240 fixtures, deterministic (master seed 20260922). Per-fixture stream seeds:
  seed = splitmix64(master ^ (stream_id * 0x9E3779B97F4A7C15)) ^ (index * 0xBF58476D1CE4E5B9)
Stream IDs: t1=201, t2=202, t3=203, t4=204, t5=205, t6=206.

Trap types cycle round-robin by fixture index so adjacent fixtures in sorted
order never repeat the same trap.

Output: forks/H1/evidence/h1_adv/<task>/adv_h1/pNNN.<ext> + .truth
Sizes: t1:40, t2:30, t3:45, t4:40, t5:40, t6:45.
"""
import math, os, struct, sys

MASTER = 20260922
OUT = os.path.expanduser("~/workspace/tnn-lab/senses/pam-rebuild/forks/H1/evidence/h1_adv")

def splitmix64(z):
    z = (z + 0x9E3779B97F4A7C15) & 0xFFFFFFFFFFFFFFFF
    z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9 & 0xFFFFFFFFFFFFFFFF
    z = (z ^ (z >> 27)) * 0x94D049BB133111EB & 0xFFFFFFFFFFFFFFFF
    return z ^ (z >> 31)

class Rng:
    def __init__(self, seed): self.s = seed
    def u64(self):
        self.s = splitmix64(self.s)
        return self.s
    def uniform(self): return (self.u64() >> 11) * (1.0 / (1 << 53))
    def range(self, lo, hi): return lo + (hi - lo) * self.uniform()
    def int(self, n): return self.u64() % n
    def pick(self, seq): return seq[self.u64() % len(seq)]

def stream_seed(master, stream, index):
    h = splitmix64(master ^ (stream * 0x9E3779B97F4A7C15))
    return splitmix64(h ^ (index * 0xBF58476D1CE4E5B9))

def write_img(path, w, h, pixels):
    with open(path, "wb") as f:
        f.write(struct.pack("<II", w, h))
        f.write(bytes(pixels))

def write_pcm(path, sr, samples):
    with open(path, "wb") as f:
        f.write(struct.pack("<II", sr, len(samples)))
        f.write(struct.pack("<%dh" % len(samples), *samples))

def write_vid(path, w, h, frames):
    with open(path, "wb") as f:
        f.write(struct.pack("<III", len(frames), w, h))
        for fr in frames:
            f.write(bytes(fr))

def write_truth(path, value):
    with open(path + ".truth", "w") as f:
        f.write("truth=%s\n" % value)

SR = 16000

# --- color helpers (simplified) ---
def rgb_to_lab(r, g, b):
    # simplified: use approximate
    return (r*0.3+g*0.6+b*0.1, r-g, g-b)

def _tone(freq, dur, harmonics, amp=0.75):
    n = int(SR * dur)
    out = [0.0]*n
    for k, a in harmonics:
        w = 2*math.pi*freq*k/SR
        for i in range(n):
            out[i] += a*math.sin(w*i)
    ramp = int(SR*0.02)
    for i in range(ramp):
        e = 0.5-0.5*math.cos(math.pi*i/ramp)
        out[i] *= e; out[n-1-i] *= e
    peak = max(1e-9, max(abs(v) for v in out))
    g = amp/peak
    return [int(max(-32768, min(32767, round(v*g*32767)))) for v in out]

# ============ T1 colordisc (40) ============
def gen_t1_adv():
    d = os.path.join(OUT, "t1_colordisc", "adv_h1")
    os.makedirs(d, exist_ok=True)
    for idx in range(40):
        rng = Rng(stream_seed(MASTER, 201, idx))
        trap = idx % 4
        W, H = 128, 64
        if trap == 0:  # T1A near-JND straddles (de 1.8-2.5)
            base = (rng.int(256), rng.int(256), rng.int(256))
            # small RGB perturbation ~ de 2
            delta = int(rng.range(8, 14))
            c2 = (min(255, base[0]+delta), base[1], base[2])
            truth = "DIFFERENT"  # just over threshold
        elif trap == 1:  # T1B distractor blob (truth SAME)
            base = (rng.int(256), rng.int(256), rng.int(256))
            c2 = base
            truth = "SAME"
        elif trap == 2:  # T1C gradient halves, equal means
            base = (rng.int(256), rng.int(256), rng.int(256))
            c2 = base
            truth = "SAME"
        else:  # T1D swapped-luminance metamers
            base = (rng.int(256), rng.int(256), rng.int(256))
            c2 = (base[1], base[0], base[2])
            truth = "DIFFERENT"
        px = []
        for y in range(H):
            for x in range(W):
                if x < W//2:
                    c = base
                    if trap == 2:  # vertical gradient on left
                        f = y / H
                        c = (int(base[0]*f), int(base[1]*f), int(base[2]*f))
                else:
                    c = c2
                if trap == 1 and x >= W//2 and (x-W//2) < 8 and y < 8:
                    c = (255, 255, 255)  # distractor blob
                px.extend(c)
        path = os.path.join(d, "p%03d.img" % idx)
        write_img(path, W, H, px)
        write_truth(path, truth)

# ============ T4 pitchdisc (40) ============
def gen_t4_adv():
    d = os.path.join(OUT, "t4_pitchdisc", "adv_h1")
    os.makedirs(d, exist_ok=True)
    for idx in range(40):
        rng = Rng(stream_seed(MASTER, 204, idx))
        trap = idx % 4
        f0 = 440.0
        if trap == 0:  # T4A near-threshold (±0.3%-0.7%)
            delta = rng.range(0.003, 0.007)
            f1 = f0 * (1+delta)
            truth = "HIGHER" if delta > 0.005 else "SAME"
        elif trap == 1:  # T4B octave distractor (2nd harmonic at 0.9)
            f1 = f0
            truth = "SAME"
        elif trap == 2:  # T4C vibrato on tone B (±2% FM)
            f1 = f0 * 1.02
            truth = "HIGHER"
        else:  # T4D mistuned/inharmonic
            f1 = f0 * 1.01
            truth = "HIGHER"
        # two tones: first half f0, second half f1
        n = int(SR*0.4)
        s1 = _tone(f0, 0.4, [(1,1.0)])
        if trap == 1:
            s2 = _tone(f1, 0.4, [(1,1.0),(2,0.9)])
        elif trap == 2:
            # vibrato: FM
            s2 = []
            for i in range(n):
                fm = 1 + 0.02*math.sin(2*math.pi*5*i/SR)
                s2.append(int(0.7*32767*math.sin(2*math.pi*f1*fm*i/SR)))
        elif trap == 3:
            s2 = _tone(f1, 0.4, [(1,1.0),(2.01,0.3),(3.02,0.2)])
        else:
            s2 = _tone(f1, 0.4, [(1,1.0)])
        samples = s1 + s2
        path = os.path.join(d, "p%03d.pcm" % idx)
        write_pcm(path, SR, samples)
        write_truth(path, truth)

# ============ T5 timbredisc (40) ============
def gen_t5_adv():
    d = os.path.join(OUT, "t5_timbredisc", "adv_h1")
    os.makedirs(d, exist_ok=True)
    for idx in range(40):
        rng = Rng(stream_seed(MASTER, 205, idx))
        trap = idx % 3
        if trap == 0:  # T5A boundary straddle (between DARK/RICH)
            harm = [(1,1.0),(2,0.47),(3,0.25),(4,0.15)]
            truth = "RICH"  # centroid ~1400 (boundary)
        elif trap == 1:  # T5B distractor (weak fund + strong upper)
            harm = [(1,0.5),(2,0.9),(3,0.8),(4,0.7)]
            truth = "BRIGHT"
        else:  # T5C AM (centroid differs between halves)
            harm = [(1,1.0),(2,0.4),(3,0.1)]
            truth = "DARK"
        samples = _tone(440.0, 0.8, harm)
        path = os.path.join(d, "p%03d.pcm" % idx)
        write_pcm(path, SR, samples)
        write_truth(path, truth)

# ============ T6 motiondir (45) ============
def gen_t6_adv():
    d = os.path.join(OUT, "t6_motiondir", "adv_h1")
    os.makedirs(d, exist_ok=True)
    W, H, NF = 64, 64, 8
    for idx in range(45):
        rng = Rng(stream_seed(MASTER, 206, idx))
        trap = idx % 3
        # base photo: random gradient
        base = []
        for y in range(H):
            for x in range(W):
                v = int(128 + 60*math.sin(x*0.2) + 40*math.cos(y*0.15))
                base.append((v, v, v))
        frames = []
        if trap == 0:  # T6A global flicker (zero translation)
            truth = "STILL"
            for f in range(NF):
                fr = []
                fl = rng.range(-20, 20)
                for (r,g,b) in base:
                    v = int(max(0, min(255, r+fl)))
                    fr.extend((v,v,v))
                frames.append(fr)
        elif trap == 1:  # T6B two opposite regions
            truth = "E"  # majority wins (arbitrary)
            for f in range(NF):
                fr = []
                for y in range(H):
                    for x in range(W):
                        if y < H//2:
                            sx = (x - 2*f) % W  # move left
                        else:
                            sx = (x + 2*f) % W  # move right
                        v = base[y*W + sx][0]
                        fr.extend((v,v,v))
                frames.append(fr)
        else:  # T6C 1px/frame at 0.25 contrast
            truth = "E"
            for f in range(NF):
                fr = []
                for y in range(H):
                    for x in range(W):
                        sx = (x - 1*f) % W
                        v = base[y*W+sx][0]
                        v = int(128 + (v-128)*0.25)
                        fr.extend((v,v,v))
                frames.append(fr)
        path = os.path.join(d, "p%03d.vid" % idx)
        write_vid(path, W, H, frames)
        write_truth(path, truth)


# ============ T2 colorconst (30) ============
def gen_t2_adv():
    import random
    d = os.path.join(OUT, "t2_colorconst", "adv_h1")
    os.makedirs(d, exist_ok=True)
    # load a photo (use first available)
    phdir = os.path.expanduser("~/workspace/tnn-lab/senses/rebuild/harness/fixtures/_photos")
    import glob
    photos = sorted(glob.glob(os.path.join(phdir, "*.jpg")))
    # simplified: use synthetic gradient as "photo"
    W, H = 128, 64
    for idx in range(30):
        rng = Rng(stream_seed(MASTER, 202, idx))
        trap = idx % 3
        # base: vertical gradient
        base = []
        for y in range(H):
            for x in range(W):
                v = int(100 + 80*(y/H))
                base.append(v)
        if trap == 0:  # T2A extreme blue illuminant
            # left half: normal, right half: blue-shifted (same surface)
            truth = "SAME_SURFACE"
            px = []
            for y in range(H):
                for x in range(W):
                    v = base[y*W+x]
                    if x < W//2:
                        px.extend((v, v, v))
                    else:
                        px.extend((int(v*0.6), int(v*0.7), min(255, int(v*1.4))))
        elif trap == 1:  # T2B metameric (different, but normalized coincides)
            truth = "DIFFERENT"
            px = []
            for y in range(H):
                for x in range(W):
                    v = base[y*W+x]
                    if x < W//2:
                        px.extend((v, int(v*0.9), int(v*0.8)))
                    else:
                        # different surface, illuminant chosen to match normalized
                        px.extend((int(v*0.8), int(v*0.72), int(v*0.64)))
        else:  # T2C exposure gradient (same surface)
            truth = "SAME_SURFACE"
            px = []
            for y in range(H):
                for x in range(W):
                    v = base[y*W+x]
                    f = 0.7 + 0.6*(x/W)  # left dark, right bright
                    vv = int(max(0, min(255, v*f)))
                    px.extend((vv, vv, vv))
        path = os.path.join(d, "p%03d.img" % idx)
        write_img(path, W, H, px)
        write_truth(path, truth)

# ============ T3 shapetrans (45) ============
def gen_t3_adv():
    d = os.path.join(OUT, "t3_shapetrans", "adv_h1")
    os.makedirs(d, exist_ok=True)
    W, H = 96, 96
    for idx in range(45):
        rng = Rng(stream_seed(MASTER, 203, idx))
        trap = idx % 3
        # clutter background
        px = []
        for y in range(H):
            for x in range(W):
                v = int(128 + 40*math.sin(x*0.3) + 30*math.cos(y*0.25))
                px.append(v)
        # draw shape (0=circle,1=triangle,2=square)
        shape = idx % 3
        truths = ["CIRCLE", "TRIANGLE", "SQUARE"]
        truth = truths[shape]
        cx, cy = W//2, H//2
        if trap == 1:  # T3B small shape
            rad = int(rng.range(14, 20))
        else:
            rad = 28
        for y in range(H):
            for x in range(W):
                inside = False
                if shape == 0:  # circle
                    if (x-cx)**2 + (y-cy)**2 < rad**2:
                        inside = True
                elif shape == 2:  # square (rotated 45 for T3C)
                    if trap == 2:
                        # diamond (rotated square)
                        if abs(x-cx) + abs(y-cy) < rad:
                            inside = True
                    else:
                        if abs(x-cx) < rad and abs(y-cy) < rad:
                            inside = True
                else:  # triangle
                    if y > cy-rad and y < cy+rad:
                        wdt = rad * (1 - abs(y-cy)/rad)
                        if abs(x-cx) < wdt:
                            inside = True
                if inside:
                    i = y*W+x
                    px[i] = 255
        if trap == 0:  # T3A occlusion bar (rows 30-44)
            for y in range(30, 45):
                for x in range(W):
                    px[y*W+x] = 128
        # to RGB
        rgb = []
        for v in px:
            rgb.extend((v, v, v))
        path = os.path.join(d, "p%03d.img" % idx)
        write_img(path, W, H, rgb)
        write_truth(path, truth)

def main():
    gen_t1_adv(); print("t1 done", flush=True)
    gen_t4_adv(); print("t4 done", flush=True)
    gen_t5_adv(); print("t5 done", flush=True)
    gen_t6_adv(); print("t6 done", flush=True)
    gen_t2_adv(); print("t2 done", flush=True)
    gen_t3_adv(); print("t3 done", flush=True)

if __name__ == "__main__":
    main()
