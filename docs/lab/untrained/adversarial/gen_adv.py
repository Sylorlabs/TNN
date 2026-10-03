#!/usr/bin/env python3
"""
Adversarial fixture generator for the abstention-capable analyzer.
ALL FIXTURES ARE ANALYTICAL AND ZERO-RNG: every sample is defined by a
closed-form formula with fixed parameters. No random module, no noise
seeds, no stochastic processes.

Audio: 16 kHz mono 16-bit PCM WAV.
Image: 320x200 binary PPM (P6).
Video: 320x200 binary PPM frames, f_001..f_00N.

The 10 fixtures target specific forced-choice failure modes:
  A1 faint_clicks      near-silence with faint irregular clicks
  A2 wobble_am         AM period wobbles around the rhythm boundary
  A3 two_rhythms       two competing AM rates (2 Hz vs 3 Hz)
  A4 inharmonic        inharmonic metallic partials (not a harmonic stack)
  A5 slow_drift        slow linear pitch drift, no stable period
  I6 mid_texture       texture near the 0.200 gate (calibrated via prototype)
  I7 s_ridge           S-curved ridge (orientation must abstain, not force)
  I8 isotropic         concentric rings (no preferred orientation)
  I9 near_blank        very low contrast (valid blank finding, not NO_MATCH)
  V10 conflict_motion  motion reverses direction mid-clip (heading abstains)
"""
import math, struct, sys, os

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
SR = 16000

def write_wav(path, samples):
    n = len(samples)
    with open(path, "wb") as f:
        f.write(b"RIFF")
        f.write(struct.pack("<I", 36 + n * 2))
        f.write(b"WAVEfmt ")
        f.write(struct.pack("<IHHIIHH", 16, 1, 1, SR, SR * 2, 2, 16))
        f.write(b"data")
        f.write(struct.pack("<I", n * 2))
        for s in samples:
            v = int(s)
            if v > 32767: v = 32767
            if v < -32768: v = -32768
            f.write(struct.pack("<h", v))

def write_ppm(path, w, h, px):
    # px: list of (r,g,b) ints
    with open(path, "wb") as f:
        f.write(f"P6\n{w} {h}\n255\n".encode())
        for (r, g, b) in px:
            f.write(bytes([r & 255, g & 255, b & 255]))

def gray(v):
    v = int(v)
    if v < 0: v = 0
    if v > 255: v = 255
    return (v, v, v)

# ---------------- A1: faint irregular clicks on near-silence ----------------
def gen_a1():
    dur = 10.0
    n = int(SR * dur)
    out = [0.0] * n
    # near-silent bed: 90 Hz sine at amplitude 40
    for i in range(n):
        t = i / SR
        out[i] = 40.0 * math.sin(2 * math.pi * 90.0 * t)
    # faint clicks at IRREGULAR times (s): intervals 1.5, 1.4, 2.7, 0.5, 1.8
    clicks = [1.2, 2.7, 4.1, 6.8, 7.3, 9.1]
    for ct in clicks:
        s0 = int(ct * SR)
        # 6 ms decaying click: alternating-sign impulse train decaying
        for k in range(int(0.006 * SR)):
            if s0 + k < n:
                decay = math.exp(-k / 12.0)
                out[s0 + k] += 900.0 * decay * (1.0 if k % 2 == 0 else -1.0)
    return out

# ---------------- A2: wobbling AM period ----------------
def gen_a2():
    dur = 10.0
    n = int(SR * dur)
    out = [0.0] * n
    # carrier 440 Hz; AM rate wobbles 2.0 +/- 0.35 Hz on a 0.1 Hz wobble
    # period wobbles between ~0.43 s and ~0.61 s: borderline stable
    phase = 0.0
    for i in range(n):
        t = i / SR
        fam = 2.0 + 0.35 * math.sin(2 * math.pi * 0.1 * t)
        phase += 2 * math.pi * fam / SR
        am = 0.55 + 0.45 * math.sin(phase)
        out[i] = 8000.0 * am * math.sin(2 * math.pi * 440.0 * t)
    return out

# ---------------- A3: two competing rhythms ----------------
def gen_a3():
    dur = 10.0
    n = int(SR * dur)
    out = [0.0] * n
    # carrier 330 Hz with TWO AM rates: 2 Hz and 3 Hz, equal depth
    for i in range(n):
        t = i / SR
        am = 0.5 + 0.25 * math.sin(2 * math.pi * 2.0 * t) + 0.25 * math.sin(2 * math.pi * 3.0 * t)
        out[i] = 9000.0 * am * math.sin(2 * math.pi * 330.0 * t)
    return out

# ---------------- A4: inharmonic metallic wash ----------------
def gen_a4():
    dur = 10.0
    n = int(SR * dur)
    # inharmonic partials (ratios NOT integers): like a metal bar
    partials = [(211.0, 1.0), (359.0, 0.7), (547.0, 0.5), (733.0, 0.35), (941.0, 0.25)]
    out = [0.0] * n
    for i in range(n):
        t = i / SR
        v = 0.0
        for (fr, amp) in partials:
            v += amp * math.sin(2 * math.pi * fr * t)
        # slow global swell to keep it "wash"-like, not rhythmic
        v *= 0.7 + 0.3 * math.sin(2 * math.pi * 0.23 * t)
        out[i] = 6000.0 * v
    return out

# ---------------- A5: slow drift, no stable period ----------------
def gen_a5():
    dur = 10.0
    n = int(SR * dur)
    out = [0.0] * n
    # linear pitch drift 180 -> 420 Hz over 10 s; phase integrated
    # analytically: phase(t) = 2*pi*(180*t + 12*t^2)
    for i in range(n):
        t = i / SR
        phase = 2 * math.pi * (180.0 * t + 12.0 * t * t)
        out[i] = 8000.0 * math.sin(phase)
    return out

# ---------------- I6: mid-variance texture ----------------
def gen_i6():
    # Textured band on smooth background: the band covers ~20% of the area,
    # placing the native high-variance-cell fraction at the 0.200 gate.
    # Calibrated via /tmp prototype (different band position/frequencies
    # here). The texture question must withhold, not force textured/smooth.
    w, h = 320, 200
    px = []
    for y in range(h):
        for x in range(w):
            v = 128.0 + 4.0 * math.sin(x * 0.043 + 0.7)
            if 60 <= y < 100:  # textured band: 40px of 200 = 20%
                v += 38.0 * math.sin(x * 0.47 + 1.3) * math.sin(y * 0.39 + 0.2)
            v = int(v)
            if v < 0: v = 0
            if v > 255: v = 255
            px.append((v, v, v))
    return w, h, px

# ---------------- I7: S-ridge ----------------
def gen_i7():
    # S-curved ridge. DIFFERS from design prototypes (/tmp/proto):
    # different center, radii, band width, and phase.
    # Center (150,105), hook radius 52, band half-width 7.
    w, h = 320, 200
    base = 45
    ridge = 225
    grid = [[base] * w for _ in range(h)]
    pts = []
    # left hook: center (150,105), r=52, angles 95..285 deg
    for deg in range(95, 286, 2):
        r = deg * math.pi / 180.0
        pts.append((150 + 52 * math.cos(r), 105 + 52 * math.sin(r)))
    # right hook: center (150,105) offset: use center (205,105), r=52,
    # angles 265..445 deg (wraps past 360)
    deg = 265
    while deg <= 445:
        r = deg * math.pi / 180.0
        pts.append((205 + 52 * math.cos(r), 105 + 52 * math.sin(r)))
        deg += 2
    for (fx, fy) in pts:
        for dy in range(-7, 8):
            for dx in range(-7, 8):
                if dx * dx + dy * dy <= 49:
                    x, y = int(fx + dx), int(fy + dy)
                    if 0 <= x < w and 0 <= y < h:
                        grid[y][x] = ridge
    px = []
    for y in range(h):
        for x in range(w):
            px.append(gray(grid[y][x]))
    return w, h, px

# ---------------- I8: isotropic (concentric rings) ----------------
def gen_i8():
    # Concentric rings about (160,100): perfectly isotropic, no direction.
    w, h = 320, 200
    cx, cy = 160.0, 100.0
    px = []
    for y in range(h):
        for x in range(w):
            r = math.sqrt((x - cx) ** 2 + (y - cy) ** 2)
            v = 128.0 + 90.0 * math.sin(r * 0.35)
            px.append(gray(v))
    return w, h, px

# ---------------- I9: near-blank ----------------
def gen_i9():
    # Very low contrast: base 128 +/- 4 deterministic undulation.
    w, h = 320, 200
    px = []
    for y in range(h):
        for x in range(w):
            v = 128.0 + 3.0 * math.sin(x * 0.05 + 1.0) + 2.0 * math.sin(y * 0.07)
            px.append(gray(v))
    return w, h, px

# ---------------- V10: conflicting motion ----------------
def gen_v10():
    # 8 frames: 2D texture pans in a triangle wave (right then left).
    # Pairwise motion vectors conflict (opposite directions); the mean
    # cancels, so no single heading can be claimed. The analyzer must
    # not force a direction.
    w, h = 320, 200
    # triangle wave positions: 0, 12, 24, 12, 0, -12, -24, -12
    shifts = [0, 12, 24, 12, 0, -12, -24, -12]
    frames = []
    for shift in shifts:
        px = []
        for y in range(h):
            for x in range(w):
                v = 128.0
                v += 35.0 * math.sin((x - shift) * 0.12 + 1.0) * math.sin(y * 0.14 + 0.5)
                v += 25.0 * math.sin((x - shift) * 0.25 + 2.0) * math.sin(y * 0.21 + 1.0)
                v = int(v)
                if v < 0: v = 0
                if v > 255: v = 255
                px.append((v, v, v))
        frames.append(px)
    return w, h, frames

def main():
    os.makedirs(OUT, exist_ok=True)
    write_wav(os.path.join(OUT, "A1_faint_clicks.wav"), gen_a1())
    print("A1 done")
    write_wav(os.path.join(OUT, "A2_wobble_am.wav"), gen_a2())
    print("A2 done")
    write_wav(os.path.join(OUT, "A3_two_rhythms.wav"), gen_a3())
    print("A3 done")
    write_wav(os.path.join(OUT, "A4_inharmonic.wav"), gen_a4())
    print("A4 done")
    write_wav(os.path.join(OUT, "A5_slow_drift.wav"), gen_a5())
    print("A5 done")
    w, h, px = gen_i6()
    write_ppm(os.path.join(OUT, "I6_mid_texture.ppm"), w, h, px)
    print("I6 done")
    w, h, px = gen_i7()
    write_ppm(os.path.join(OUT, "I7_s_ridge.ppm"), w, h, px)
    print("I7 done")
    w, h, px = gen_i8()
    write_ppm(os.path.join(OUT, "I8_isotropic.ppm"), w, h, px)
    print("I8 done")
    w, h, px = gen_i9()
    write_ppm(os.path.join(OUT, "I9_near_blank.ppm"), w, h, px)
    print("I9 done")
    w, h, frames = gen_v10()
    for i, px in enumerate(frames):
        write_ppm(os.path.join(OUT, f"V10_conflict_f_{i+1:03d}.ppm"), w, h, px)
    print("V10 done")

if __name__ == "__main__":
    main()
