#!/usr/bin/env python3
"""corrupt.py — G3-specific deterministic attack fixtures (90 total, 15/task).

Reads harness PRIMARY fixtures, applies one frozen corruption per task,
writes attack/<task>/cNNN.<ext> + .truth. Fully deterministic: selection is
by sorted fixture path; every transformation is integer-exact (except the
two resynthesis attacks, which use float math but are byte-deterministic
given the same interpreter — verified by re-running).

Corruptions (parameters were concretized post-freeze during implementation;
they are NOT part of any frozen prereg amendment — see the dev-log note in
PREREG_G3.md for the exact deviations and rationale):
  t1 colordisc : bin-edge nudge — darker half of a DIFFERENT fixture +12/ch.
                 truth DIFFERENT (halves still differ by >=28/ch).
  t2 colorconst : illuminant tilt — right half R x1.25 (clamp 255).
                 truth = original (same surfaces, different light).
  t3 shapetrans : occlusion — black bar rows 40..55. truth = original shape.
  t4 pitchdisc  : octave-up — tone B resynthesized at 2x f0, only HIGHER
                 primaries (so the direction truth is preserved).
                 truth HIGHER.
  t5 timbredisc : 2nd-harmonic boost x1.15 — largest factor that keeps all
                 four class truths under the frozen readout rule (x1.6 would
                 flip DARK->RICH). truth = original.
  t6 motiondir  : reversed frame order. truth = flipped direction
                 (N<->S, E<->W, NE<->SW, NW<->SE, STILL->STILL).
"""
import os, struct, math, hashlib

HARN = os.path.expanduser("~/workspace/tnn-lab/senses/rebuild/harness/fixtures")
OUT = os.path.dirname(os.path.abspath(__file__))
ATK = os.path.join(OUT, "attack")

TASKS = ["t1_colordisc", "t2_colorconst", "t3_shapetrans",
         "t4_pitchdisc", "t5_timbredisc", "t6_motiondir"]
EXT = {"t1_colordisc": ".img", "t2_colorconst": ".img", "t3_shapetrans": ".img",
       "t4_pitchdisc": ".pcm", "t5_timbredisc": ".pcm", "t6_motiondir": ".vid"}

FLIP = {"N": "S", "S": "N", "E": "W", "W": "E", "NE": "SW", "SW": "NE",
        "NW": "SE", "SE": "NW", "STILL": "STILL"}

def read_truth(path):
    with open(path + ".truth") as f:
        return f.read().strip().split("=", 1)[1]

def primaries(task, truth_filter=None):
    d = os.path.join(HARN, task, "primary")
    names = sorted(n for n in os.listdir(d) if n.endswith(EXT[task]))
    out = []
    for n in names:
        p = os.path.join(d, n)
        t = read_truth(p)
        if truth_filter is None or t == truth_filter:
            out.append((p, t))
    return out

# ---- image helpers ----
def read_img(p):
    b = open(p, "rb").read()
    w, h = struct.unpack("<II", b[:8])
    return w, h, bytearray(b[8:8 + w * h * 3])

def write_img(p, w, h, px):
    open(p, "wb").write(struct.pack("<II", w, h) + bytes(px))

# ---- pcm helpers ----
def read_pcm(p):
    b = open(p, "rb").read()
    rate, cnt = struct.unpack("<II", b[:8])
    s = struct.unpack("<%dh" % cnt, b[8:8 + cnt * 2])
    return rate, cnt, list(s)

def write_pcm(p, rate, samples):
    open(p, "wb").write(struct.pack("<II", rate, len(samples)) +
                        struct.pack("<%dh" % len(samples),
                                    *[max(-32768, min(32767, int(round(x)))) for x in samples]))

def f0_est(samples, sr=16000):
    # upward zero-crossing estimate (float mirror of the Zag estimator)
    first = last = None
    k = 0
    for i in range(1, len(samples)):
        if samples[i-1] < 0 <= samples[i]:
            pos = (i-1) + (-samples[i-1]) / (samples[i] - samples[i-1])
            if first is None:
                first = pos
            last = pos
            k += 1
    if k < 2 or last <= first:
        return 0.0
    return sr * (k - 1) / (last - first)

# ---- t1: bin-edge nudge ----
def c_t1(items):
    d = os.path.join(ATK, "t1_colordisc")
    os.makedirs(d, exist_ok=True)
    for j, (p, t) in enumerate(items[:15]):
        w, h, px = read_img(p)
        hw = w // 2
        n = hw * h
        m1 = sum(px[(y*w+x)*3] + px[(y*w+x)*3+1] + px[(y*w+x)*3+2]
                 for y in range(h) for x in range(hw)) / n
        m2 = sum(px[(y*w+hw+x)*3] + px[(y*w+hw+x)*3+1] + px[(y*w+hw+x)*3+2]
                 for y in range(h) for x in range(hw)) / n
        dark_right = m2 < m1
        for y in range(h):
            for x in range(hw):
                xx = hw + x if dark_right else x
                o = (y * w + xx) * 3
                for c in range(3):
                    px[o+c] = min(255, px[o+c] + 12)
        q = os.path.join(d, "c%03d.img" % j)
        write_img(q, w, h, px)
        open(q + ".truth", "w").write("truth=" + t + "\n")

# ---- t2: illuminant tilt ----
def c_t2(items):
    d = os.path.join(ATK, "t2_colorconst")
    os.makedirs(d, exist_ok=True)
    for j, (p, t) in enumerate(items[:15]):
        w, h, px = read_img(p)
        hw = w // 2
        for y in range(h):
            for x in range(hw):
                o = (y * w + hw + x) * 3
                px[o] = min(255, int(round(px[o] * 1.25)))
        q = os.path.join(d, "c%03d.img" % j)
        write_img(q, w, h, px)
        open(q + ".truth", "w").write("truth=" + t + "\n")

# ---- t3: occlusion bar ----
def c_t3(items):
    d = os.path.join(ATK, "t3_shapetrans")
    os.makedirs(d, exist_ok=True)
    for j, (p, t) in enumerate(items[:15]):
        w, h, px = read_img(p)
        for y in range(40, 56):
            for x in range(w):
                o = (y * w + x) * 3
                px[o] = px[o+1] = px[o+2] = 0
        q = os.path.join(d, "c%03d.img" % j)
        write_img(q, w, h, px)
        open(q + ".truth", "w").write("truth=" + t + "\n")

# ---- t4: octave-up tone B ----
def c_t4(items):
    d = os.path.join(ATK, "t4_pitchdisc")
    os.makedirs(d, exist_ok=True)
    for j, (p, t) in enumerate(items[:15]):
        rate, cnt, s = read_pcm(p)
        assert rate == 16000 and cnt == 14080
        bseg = s[7680:14080]
        f0b = f0_est(bseg)
        peak = max(abs(x) for x in bseg)
        nb = [peak * math.sin(2 * math.pi * (2 * f0b) * i / rate) for i in range(6400)]
        s2 = s[:7680] + nb + s[14080:]
        q = os.path.join(d, "c%03d.pcm" % j)
        write_pcm(q, rate, s2)
        open(q + ".truth", "w").write("truth=" + t + "\n")

# ---- t5: 2nd-harmonic boost x1.15 ----
def c_t5(items):
    d = os.path.join(ATK, "t5_timbredisc")
    os.makedirs(d, exist_ok=True)
    for j, (p, t) in enumerate(items[:15]):
        rate, cnt, s = read_pcm(p)
        assert rate == 16000 and cnt == 12800
        seg = s[400:12400]
        n = len(seg)
        # estimate harmonic amplitude/phase by exact 440 Hz correlation
        amps = {}
        for h in range(1, 9):
            re = im = 0.0
            for i, x in enumerate(seg):
                ph = 2 * math.pi * h * 440.0 * i / rate
                re += x * math.cos(ph)
                im += x * math.sin(ph)
            amps[h] = (2 * math.hypot(re, im) / n, math.atan2(re, im))
        a2, p2 = amps[2]
        # add 15% more 2nd harmonic (phase-aligned -> x1.15 total)
        add = [(0.15 * a2) * math.sin(2 * math.pi * 2 * 440.0 * i / rate + p2)
               for i in range(cnt)]
        s2 = [x + a for x, a in zip(s, add)]
        q = os.path.join(d, "c%03d.pcm" % j)
        write_pcm(q, rate, s2)
        open(q + ".truth", "w").write("truth=" + t + "\n")

# ---- t6: reversed frames ----
def c_t6(items):
    d = os.path.join(ATK, "t6_motiondir")
    os.makedirs(d, exist_ok=True)
    for j, (p, t) in enumerate(items[:15]):
        b = open(p, "rb").read()
        nf, w, h = struct.unpack("<III", b[:12])
        fsz = w * h * 3
        frames = [b[12 + k * fsz:12 + (k + 1) * fsz] for k in range(nf)]
        q = os.path.join(d, "c%03d.vid" % j)
        open(q, "wb").write(struct.pack("<III", nf, w, h) + b"".join(reversed(frames)))
        open(q + ".truth", "w").write("truth=" + FLIP[t] + "\n")

def main():
    counts = {}
    c_t1(primaries("t1_colordisc", "DIFFERENT")); counts["t1"] = 15
    c_t2(primaries("t2_colorconst")); counts["t2"] = 15
    c_t3(primaries("t3_shapetrans")); counts["t3"] = 15
    c_t4(primaries("t4_pitchdisc", "HIGHER")); counts["t4"] = 15
    c_t5(primaries("t5_timbredisc")); counts["t5"] = 15
    c_t6(primaries("t6_motiondir")); counts["t6"] = 15
    # manifest
    lines = []
    for task in TASKS:
        d = os.path.join(ATK, task)
        for n in sorted(os.listdir(d)):
            if n.endswith(EXT[task]):
                p = os.path.join(d, n)
                h = hashlib.sha256(open(p, "rb").read()).hexdigest()
                t = read_truth(p)
                lines.append("%s  %s" % (h, os.path.join(task, n)))
    open(os.path.join(ATK, "MANIFEST.sha256"), "w").write("\n".join(lines) + "\n")
    print("attack fixtures:", counts)

if __name__ == "__main__":
    main()
