#!/usr/bin/env python3
"""Generate FRESH confirmatory inputs for the untrained-analysis binding run.

All generation is analytical and deterministic (zero RNG). Formulas chosen to
exercise the repaired dimensions: slow swells, soft-note onsets, continuous
tonal+bed mixtures, native-resolution texture, diagonal orientation, coherent
video motion. These inputs have never existed before; novelty is proven by the
Git-blob audit (all must 404) before sealing.
"""
import math, struct, os

SR = 16000
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "inputs")
os.makedirs(OUT, exist_ok=True)

def write_wav(path, samples):
    n = len(samples)
    data = struct.pack("<%dh" % n, *[max(-32768, min(32767, int(round(s * 32767)))) for s in samples])
    with open(path, "wb") as f:
        f.write(b"RIFF")
        f.write(struct.pack("<I", 36 + len(data)))
        f.write(b"WAVEfmt ")
        f.write(struct.pack("<IHHIIHH", 16, 1, 1, SR, SR * 2, 2, 16))
        f.write(b"data")
        f.write(struct.pack("<I", len(data)))
        f.write(data)

def write_ppm(path, w, h, rgb):
    with open(path, "wb") as f:
        f.write(("P6\n%d %d\n255\n" % (w, h)).encode())
        f.write(bytes(rgb))

# ---------------------------------------------------------------- audio
# C1: slow 4 s AM on a tonal dyad (330 + 495 Hz + harmonics). 12 s.
#     Slow swells, strongly tonal, single process, no transients.
def gen_c1():
    T = 12.0
    n = int(T * SR)
    out = []
    for i in range(n):
        t = i / SR
        env = 0.35 + 0.65 * (0.5 + 0.5 * math.sin(2 * math.pi * t / 4.0))
        s = (0.60 * math.sin(2 * math.pi * 330 * t)
             + 0.30 * math.sin(2 * math.pi * 660 * t)
             + 0.45 * math.sin(2 * math.pi * 495 * t)
             + 0.20 * math.sin(2 * math.pi * 990 * t))
        out.append(0.42 * env * s)
    return out

# C2: four irregular SOFT tonal phrases (880->840 Hz glide), raised-cosine
#     80 ms attack/release, silence between. 10 s. Soft onsets, no transients.
def gen_c2():
    T = 10.0
    n = int(T * SR)
    out = [0.0] * n
    phrases = [(0.50, 0.40), (2.10, 0.65), (4.75, 0.50), (6.65, 0.55)]
    atk = int(0.08 * SR)
    for (st, dur) in phrases:
        s0 = int(st * SR)
        ns = int(dur * SR)
        for j in range(ns):
            t = j / SR
            f = 880.0 - 40.0 * (j / ns)          # gentle downward glide
            sig = (0.55 * math.sin(2 * math.pi * f * t)
                   + 0.22 * math.sin(2 * math.pi * 2 * f * t)
                   + 0.10 * math.sin(2 * math.pi * 3 * f * t))
            if j < atk:
                w = 0.5 - 0.5 * math.cos(math.pi * j / atk)
            elif j >= ns - atk:
                w = 0.5 - 0.5 * math.cos(math.pi * (ns - 1 - j) / atk)
            else:
                w = 1.0
            out[s0 + j] += 0.62 * w * sig
    return out

# C3: continuous rumble bed + steady 250 Hz tone, flat envelope, no onsets. 15 s.
def gen_c3():
    T = 15.0
    n = int(T * SR)
    out = []
    fk = [40.0 + 9.3 * k for k in range(9)]   # inharmonic rumble partials
    for i in range(n):
        t = i / SR
        bed = sum(0.11 * math.sin(2 * math.pi * f * t + 0.7 * k) for k, f in enumerate(fk))
        tone = (0.30 * math.sin(2 * math.pi * 250 * t)
                + 0.14 * math.sin(2 * math.pi * 500 * t)
                + 0.07 * math.sin(2 * math.pi * 750 * t))
        out.append(0.55 * (bed + tone))
    return out

for name, gen in (("C1_dyad_swells", gen_c1), ("C2_soft_phrases", gen_c2),
                  ("C3_rumble_hum", gen_c3)):
    p = os.path.join(OUT, name + ".wav")
    write_wav(p, gen())
    print("wrote", p)

# ---------------------------------------------------------------- images
# deterministic speckle: fract(sin(i*12.9898)*43758.5453) in [-1,1]
def speckle(i):
    return 2.0 * (math.sin(i * 12.9898) * 43758.5453 % 1.0) - 1.0

# C4: vertical picket bars on dark gray + fine speckle everywhere. 320x200.
def gen_c4():
    w, h = 320, 200
    px = bytearray()
    for y in range(h):
        for x in range(w):
            in_bar = (x % 40) < 12
            base = 220 if in_bar else 40
            v = base + int(25 * speckle(y * w + x))
            v = max(0, min(255, v))
            px += bytes((v, v, v))
    return w, h, px

# C5: diagonal wedge — dark top-left, light bottom-right, smooth. 320x200.
# Boundary from (40,200) to (280,0): ~40 deg from horizontal.
def gen_c5():
    w, h = 320, 200
    px = bytearray()
    # line: through (40,200) and (280,0): y = 200 - (200/240)(x-40)
    for y in range(h):
        for x in range(w):
            yl = 200.0 - (200.0 / 240.0) * (x - 40)
            d = (y - yl) / h   # signed distance from diagonal
            if d < -0.02:
                v = 200 - int(20 * (1 - y / h))
            elif d > 0.02:
                v = 30 + int(12 * y / h)
            else:
                v = 115
            r, g, b = v, max(0, v - 8), max(0, v - 18)
            px += bytes((r, g, b))
    return w, h, px

for name, gen in (("C4_pickets", gen_c4), ("C5_diag_wedge", gen_c5)):
    w, h, px = gen()
    p = os.path.join(OUT, name + ".ppm")
    write_ppm(p, w, h, px)
    print("wrote", p)

# ---------------------------------------------------------------- video
# C6: dark square drifting diagonally on light bg, 8 frames 160x90,
#     brightness ramping down slightly across frames.
def gen_c6():
    w, h, nf = 160, 90, 8
    for f in range(nf):
        px = bytearray()
        dim = 1.0 - 0.02 * f
        x0 = 10 + 12 * f
        y0 = 8 + 9 * f
        for y in range(h):
            for x in range(w):
                inside = (x0 <= x < x0 + 30) and (y0 <= y < y0 + 30)
                v = 40 if inside else 180
                v = int(v * dim)
                px += bytes((v, v, v))
        p = os.path.join(OUT, "C6_drift_f_%03d.ppm" % (f + 1))
        write_ppm(p, w, h, px)
        print("wrote", p)

gen_c6()
print("DONE")
