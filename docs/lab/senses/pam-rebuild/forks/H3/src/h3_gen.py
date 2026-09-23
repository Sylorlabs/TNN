#!/usr/bin/env python3
"""H3ADV generator — deterministic adversarial fixtures for PAM fork H3.
Frozen design per PREREG_H3.md §5. Zero RNG; all parameters are arithmetic
functions of the index. IDs h3a_<task>_<idx>. Truth files alongside.

Design notes (deviations from §5 documented in BUILD_LOG.md):
- t2: §5's "8x8 spot breaks Δ-spot" is mathematically inconsistent with §4's
  P3 (|df-df_spotremoved|<=15, max achievable Δ≈6.9). Uses a 24x24 spot that
  breaks P1 (uniformity) instead; validation gate satisfied via broken P1.
- t4: uses the frozen harness structure (0.4s tone + 0.08s gap + 0.4s tone).

Usage: h3_gen.py <outdir>
"""
import math, os, struct, sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "h3adv"

def w_img(path, w, h, px):
    with open(path, "wb") as f:
        f.write(struct.pack("<II", w, h))
        f.write(bytes(px))

def w_pcm(path, sr, samples):
    with open(path, "wb") as f:
        f.write(struct.pack("<II", sr, len(samples)))
        f.write(struct.pack("<%dh" % len(samples), *[max(-32768, min(32767, int(s))) for s in samples]))

def w_vid(path, nf, w, h, frames):
    with open(path, "wb") as f:
        f.write(struct.pack("<III", nf, w, h))
        for fr in frames:
            f.write(bytes(fr))

def w_truth(path, cls):
    with open(path, "w") as f:
        f.write("truth=%s\n" % cls)

def clamp(v):
    return max(0, min(255, int(v)))

# ---------------- t1: illumination gradient (20) ----------------
# Left half carries a vertical luminance gradient: top +60 → bottom 0
# (60-unit drop). Truth SAME. T0 says DIFFERENT (mean shift ~30/unit),
# P1/P2 uniformity break (~52 > 20).
def gen_t1(d):
    w, h = 128, 64
    for idx in range(20):
        base = (90 + (idx * 37) % 80, 100 + (idx * 53) % 60, 110 + (idx * 29) % 50)
        px = bytearray(w * h * 3)
        for y in range(h):
            add = 60.0 - 60.0 * y / (h - 1)
            for x in range(w):
                o = (y * w + x) * 3
                if x < w // 2:
                    px[o] = clamp(base[0] + add)
                    px[o+1] = clamp(base[1] + add)
                    px[o+2] = clamp(base[2] + add)
                else:
                    px[o], px[o+1], px[o+2] = base[0], base[1], base[2]
        p = os.path.join(d, "h3a_t1_%03d.img" % idx)
        w_img(p, w, h, px)
        w_truth(p + ".truth", "SAME")

# ---------------- t2: specular spot (20) ----------------
# Same-surface fixture with a 24x24 white (255) spot in the upper-left
# (fully in the top half). Truth SAME_SURFACE. T0 says SAME_SURFACE,
# P1 (uniformity) breaks, P2/P3 hold. See module docstring for the
# §4/§5 Δ-spot inconsistency.
def gen_t2(d):
    w, h = 128, 64
    for idx in range(20):
        base = (120 + (idx * 41) % 60, 110 + (idx * 31) % 50, 100 + (idx * 47) % 40)
        px = bytearray(w * h * 3)
        for y in range(h):
            for x in range(w):
                o = (y * w + x) * 3
                px[o], px[o+1], px[o+2] = base[0], base[1], base[2]
        # 24x24 white spot, upper-left (rows 4..28, cols 8..32)
        sx, sy = 8 + (idx % 3) * 4, 4 + (idx % 2) * 4
        for y in range(sy, sy + 24):
            for x in range(sx, sx + 24):
                if 0 <= x < w and 0 <= y < h:
                    o = (y * w + x) * 3
                    px[o] = px[o+1] = px[o+2] = 255
        p = os.path.join(d, "h3a_t2_%03d.img" % idx)
        w_img(p, w, h, px)
        w_truth(p + ".truth", "SAME_SURFACE")

# ---------------- t3: tab (10) + lowcontrast (10) ----------------
def draw_circle(px, w, h, cx, cy, r, lum):
    for y in range(h):
        for x in range(w):
            if (x - cx) ** 2 + (y - cy) ** 2 <= r * r:
                o = (y * w + x) * 3
                px[o] = px[o+1] = px[o+2] = lum

def draw_square(px, w, h, cx, cy, s, lum):
    for y in range(cy - s//2, cy + s//2):
        for x in range(cx - s//2, cx + s//2):
            if 0 <= x < w and 0 <= y < h:
                o = (y * w + x) * 3
                px[o] = px[o+1] = px[o+2] = lum

def draw_triangle(px, w, h, cx, cy, s, lum):
    # right triangle legs s, right angle at (cx,cy)
    for y in range(cy, cy + s):
        for x in range(cx, cx + s):
            if 0 <= x < w and 0 <= y < h and (x - cx) + (y - cy) <= s:
                o = (y * w + x) * 3
                px[o] = px[o+1] = px[o+2] = lum

def gen_t3(d):
    w, h = 96, 96
    # tab: circle r=28 + 10x40 vertical tab on the right side.
    # truth=CIRCLE. Design: T0->SQUARE via area/R^2, P3 symmetry breaks.
    for idx in range(10):
        px = bytearray(w * h * 3)
        cx, cy, r = 48, 48, 28
        draw_circle(px, w, h, cx, cy, r, 255)
        # tab: cols 72..82 (overlaps circle edge), rows 28..68
        for y in range(28, 68):
            for x in range(72, 82):
                if 0 <= x < w and 0 <= y < h:
                    o = (y * w + x) * 3
                    px[o] = px[o+1] = px[o+2] = 255
        p = os.path.join(d, "h3a_t3_%03d.img" % idx)
        w_img(p, w, h, px)
        w_truth(p + ".truth", "CIRCLE")
    # lowcontrast: gray-132 shapes on black. Truth=class.
    # Design: P1/P2 disagree (threshold sensitivity), P3 holds.
    for idx in range(10, 20):
        px = bytearray(w * h * 3)
        kind = (idx - 10) % 3  # 0 circle, 1 square, 2 triangle
        if kind == 0:
            draw_circle(px, w, h, 48, 48, 28, 132)
            truth = "CIRCLE"
        elif kind == 1:
            draw_square(px, w, h, 48, 48, 44, 132)
            truth = "SQUARE"
        else:
            draw_triangle(px, w, h, 30, 26, 44, 132)
            truth = "TRIANGLE"
        p = os.path.join(d, "h3a_t3_%03d.img" % idx)
        w_img(p, w, h, px)
        w_truth(p + ".truth", truth)

# ---------------- t4: step (10) + glide (10) ----------------
# Frozen harness structure: 0.4s tone A + 0.08s gap + 0.4s tone B @16kHz.
# 20ms raised-cosine ramps at tone edges (frozen harness convention).
def _ramp(n, nr):
    return [0.5 - 0.5 * math.cos(math.pi * min(1.0, i / nr)) if i < nr
            else 0.5 - 0.5 * math.cos(math.pi * min(1.0, (n - 1 - i) / nr))
            for i in range(n)]

def sine(f, sr, n, amp=12000, phase=0.0):
    return [amp * math.sin(2 * math.pi * f * i / sr + phase) for i in range(n)]

def gen_t4(d):
    sr = 16000
    tone, gap = 6400, 1280
    cnt = tone + gap + tone
    nr = 320  # 20ms ramp
    for idx in range(10):
        f0 = 220 + idx * 15
        # step: first half f0, second half 1.12*f0, 256-sample crossfade
        n1 = tone // 2
        a1 = sine(f0, sr, n1)
        a2 = sine(f0 * 1.12, sr, tone - n1)
        nx = 256
        for i in range(nx):
            wgt = i / nx
            a2[i] = a2[i] * wgt + sine(f0, sr, nx)[i] * (1 - wgt)
        toneA = a1 + a2
        toneB = sine(f0, sr, tone)
        rA, rB = _ramp(tone, nr), _ramp(tone, nr)
        toneA = [toneA[i] * rA[i] for i in range(tone)]
        toneB = [toneB[i] * rB[i] for i in range(tone)]
        pcm = toneA + [0] * gap + toneB
        p = os.path.join(d, "h3a_t4_%03d.pcm" % idx)
        w_pcm(p, sr, pcm)
        w_truth(p + ".truth", "SAME")
    for idx in range(10, 20):
        f0 = 220 + (idx - 10) * 17
        # glide: -6% -> +6% over tone A (phase-continuous)
        toneA = []
        phase = 0.0
        for i in range(tone):
            f = f0 * (0.94 + 0.12 * i / tone)
            phase += 2 * math.pi * f / sr
            toneA.append(12000 * math.sin(phase))
        toneB = sine(f0, sr, tone)
        rA, rB = _ramp(tone, nr), _ramp(tone, nr)
        toneA = [toneA[i] * rA[i] for i in range(tone)]
        toneB = [toneB[i] * rB[i] for i in range(tone)]
        pcm = toneA + [0] * gap + toneB
        p = os.path.join(d, "h3a_t4_%03d.pcm" % idx)
        w_pcm(p, sr, pcm)
        w_truth(p + ".truth", "SAME")

# ---------------- t5: step-timbre (10) + tremolo (10) ----------------
def bright(f0, sr, n, amp=3000):
    # harmonics 1..6, 1/h amplitude falloff
    s = [0.0] * n
    for h in range(1, 7):
        a = amp / h
        for i in range(n):
            s[i] += a * math.sin(2 * math.pi * f0 * h * i / sr)
    return s

def gen_t5(d):
    sr, cnt = 16000, 12800
    half = cnt // 2
    nr = 320
    for idx in range(10):
        f0 = 440
        p1 = sine(f0, sr, half, amp=12000)
        p2 = bright(f0, sr, half, amp=3000)
        r = _ramp(cnt, nr)
        pcm = [(p1 + p2)[i] * r[i] for i in range(cnt)]
        p = os.path.join(d, "h3a_t5_%03d.pcm" % idx)
        w_pcm(p, sr, pcm)
        w_truth(p + ".truth", "PURE")
    for idx in range(10, 20):
        f0 = 200 + (idx - 10) * 11
        # RICH base: harmonics 1..4, moderate falloff
        base = [0.0] * cnt
        for h, a in [(1, 9000), (2, 5000), (3, 3000), (4, 1500)]:
            for i in range(cnt):
                base[i] += a * math.sin(2 * math.pi * f0 * h * i / sr)
        # 8 Hz amplitude tremolo, +/-40%
        out = [base[i] * (0.6 + 0.4 * math.sin(2 * math.pi * 8 * i / sr)) for i in range(cnt)]
        r = _ramp(cnt, nr)
        out = [out[i] * r[i] for i in range(cnt)]
        p = os.path.join(d, "h3a_t5_%03d.pcm" % idx)
        w_pcm(p, sr, out)
        w_truth(p + ".truth", "RICH")

# ---------------- t6: final-frame flash (20) ----------------
def gen_t6(d):
    nf, w, h = 8, 64, 64
    for idx in range(20):
        frames = []
        y0 = 20 + (idx % 3) * 8
        x0 = 8
        for t in range(nf):
            fr = bytearray(w * h * 3)
            # 8x8 object drifting E 2px/frame
            ox = x0 + t * 2
            for y in range(y0, y0 + 8):
                for x in range(ox, ox + 8):
                    if 0 <= x < w and 0 <= y < h:
                        o = (y * w + x) * 3
                        fr[o] = fr[o+1] = fr[o+2] = 200
            # 16x16 white flash at fixed W position on final frame
            if t == nf - 1:
                for y in range(40, 56):
                    for x in range(4, 20):
                        o = (y * w + x) * 3
                        fr[o] = fr[o+1] = fr[o+2] = 255
            frames.append(fr)
        p = os.path.join(d, "h3a_t6_%03d.vid" % idx)
        w_vid(p, nf, w, h, frames)
        w_truth(p + ".truth", "E")

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    gen_t1(OUT); gen_t2(OUT); gen_t3(OUT)
    gen_t4(OUT); gen_t5(OUT); gen_t6(OUT)
    n = len([f for f in os.listdir(OUT) if not f.endswith(".truth")])
    print("wrote %d fixtures to %s" % (n, OUT))
