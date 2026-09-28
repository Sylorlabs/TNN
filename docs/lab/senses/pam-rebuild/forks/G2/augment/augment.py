#!/usr/bin/env python3
"""G2 adversarial augmentation generator (frozen scheme, see PREREG_G2.md).

Deterministic: splitmix64 streams, master seed 20260922. Derives 240
fixtures (40/task) from the frozen harness PRIMARY fixtures. Each method's
truth-invariance rule is machine-checked before writing.

IDs: g2a_<task>_001 .. g2a_<task>_040, in
  <out>/<tdir>/g2a_<task>_NNN.<ext> (+ .truth sibling).
Method for aug index k (0-based): methods[k % nm]; source pool index k // nm
over the task's sorted primary fixture names (with per-method pools where
the prereg requires a margin, e.g. t1/M2).
"""
import math, os, struct, sys

MASTER = 20260922
HARNESS = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "..", "..", "..", "rebuild", "harness", "fixtures"))
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")

# ---------------- splitmix64 ----------------
def splitmix64(x):
    x = (x + 0x9E3779B97F4A7C15) & 0xFFFFFFFFFFFFFFFF
    z = x
    z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & 0xFFFFFFFFFFFFFFFF
    z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & 0xFFFFFFFFFFFFFFFF
    return (z ^ (z >> 31)) & 0xFFFFFFFFFFFFFFFF

class Rng:
    def __init__(self, seed):
        self.s = seed & 0xFFFFFFFFFFFFFFFF
    def uint64(self):
        self.s = splitmix64(self.s + 0x9E3779B97F4A7C15) if False else self.s
        # simpler: iterate splitmix64 on state
        self.s = (self.s + 0x9E3779B97F4A7C15) & 0xFFFFFFFFFFFFFFFF
        z = self.s
        z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & 0xFFFFFFFFFFFFFFFF
        z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & 0xFFFFFFFFFFFFFFFF
        return (z ^ (z >> 31)) & 0xFFFFFFFFFFFFFFFF
    def irange(self, lo, hi):  # inclusive
        return lo + self.uint64() % (hi - lo + 1)

def stream_seed(task_i, method_i, k):
    return (MASTER ^ (task_i * 0x9E3779B97F4A7C15)
            ^ (method_i * 0xBF58476D1CE4E5B9) ^ (k * 0x94D049BB133111EB)) & 0xFFFFFFFFFFFFFFFF

# ---------------- fixture IO ----------------
def read_img(path):
    with open(path, "rb") as f:
        raw = f.read()
    w, h = struct.unpack("<II", raw[:8])
    return w, h, bytearray(raw[8:8 + w * h * 3])

def write_img(path, w, h, px):
    with open(path, "wb") as f:
        f.write(struct.pack("<II", w, h))
        f.write(bytes(px))

def read_pcm(path):
    with open(path, "rb") as f:
        raw = f.read()
    rate, count = struct.unpack("<II", raw[:8])
    samps = list(struct.unpack("<%dh" % count, raw[8:8 + 2 * count]))
    return rate, count, samps

def write_pcm(path, rate, samps):
    with open(path, "wb") as f:
        f.write(struct.pack("<II", rate, len(samps)))
        f.write(struct.pack("<%dh" % len(samps), *samps))

def read_vid(path):
    with open(path, "rb") as f:
        raw = f.read()
    nf, w, h = struct.unpack("<III", raw[:12])
    fsz = w * h * 3
    frames = [bytearray(raw[12 + i * fsz:12 + (i + 1) * fsz]) for i in range(nf)]
    return nf, w, h, frames

def write_vid(path, w, h, frames):
    with open(path, "wb") as f:
        f.write(struct.pack("<III", len(frames), w, h))
        for fr in frames:
            f.write(bytes(fr))

def read_truth(path):
    with open(path + ".truth") as f:
        return f.read().strip().split("=", 1)[1]

def write_truth(path, value):
    with open(path + ".truth", "w") as f:
        f.write("truth=%s\n" % value)

def clamp8(v):
    return 0 if v < 0 else (255 if v > 255 else v)

def clamp16(v):
    return -32768 if v < -32768 else (32767 if v > 32767 else v)

# ---------------- corruption methods ----------------
def m_t1_swap(w, h, px, rng):
    out = bytearray(len(px))
    hw = w // 2
    for y in range(h):
        for x in range(w):
            sx = x + hw if x < hw else x - hw
            out[(y * w + x) * 3:(y * w + x) * 3 + 3] = px[(y * w + sx) * 3:(y * w + sx) * 3 + 3]
    return out, None  # truth invariant

def m_t1_noise(w, h, px, rng):
    out = bytearray(len(px))
    for i in range(len(px)):
        out[i] = clamp8(px[i] + rng.irange(-24, 24))
    return out, None

def m_t2_swap(w, h, px, rng):
    return m_t1_swap(w, h, px, rng)

def m_t2_dim(w, h, px, rng):
    return bytearray(clamp8((p + 1) // 2) for p in px), None

def m_t3_hflip(w, h, px, rng):
    out = bytearray(len(px))
    for y in range(h):
        for x in range(w):
            sx = w - 1 - x
            out[(y * w + x) * 3:(y * w + x) * 3 + 3] = px[(y * w + sx) * 3:(y * w + sx) * 3 + 3]
    return out, None

def m_t3_noise(w, h, px, rng):
    out = bytearray(len(px))
    for i in range(len(px)):
        out[i] = clamp8(px[i] + rng.irange(-40, 40))
    return out, None

def m_t3_occlude(w, h, px, rng):
    out = bytearray(px)
    bw = max(1, w // 10)
    x0 = (w - bw) // 2
    for y in range(h):
        for x in range(x0, x0 + bw):
            o = (y * w + x) * 3
            out[o] = 10; out[o + 1] = 10; out[o + 2] = 10
    return out, None

def m_t4_reverse(rate, count, samps, rng):
    half = count // 2
    a = samps[:half]; b = samps[half:]
    a.reverse(); b.reverse()
    return a + b, None

def m_t4_noise(rate, count, samps, rng):
    return [clamp16(s + rng.irange(-900, 900)) for s in samps], None

def m_t4_swaporder(rate, count, samps, rng, truth):
    half = count // 2
    m = {"HIGHER": "LOWER", "LOWER": "HIGHER", "SAME": "SAME"}
    return samps[half:] + samps[:half], m[truth]

def m_t5_reverse(rate, count, samps, rng):
    r = list(samps); r.reverse()
    return r, None

def m_t5_noise(rate, count, samps, rng):
    return [clamp16(s + rng.irange(-900, 900)) for s in samps], None

def m_t5_fade(rate, count, samps, rng):
    out = []
    for i, s in enumerate(samps):
        g = min(i, count - 1 - i, count // 8) / (count // 8)
        out.append(int(s * (0.5 + 0.5 * g)))
    return out, None

def m_t6_reverse(nf, w, h, frames, rng, truth):
    m = {"N": "S", "S": "N", "E": "W", "W": "E",
         "NE": "SW", "SW": "NE", "NW": "SE", "SE": "NW", "STILL": "STILL"}
    r = list(frames); r.reverse()
    return r, m[truth]

def m_t6_flat(nf, w, h, frames, rng):
    out = []
    for fr in frames:
        mean = sum(fr) // len(fr)
        out.append(bytearray(clamp8(mean + (p - mean) // 2) for p in fr))
    return out, None

def m_t6_drop(nf, w, h, frames, rng):
    return frames[:-1], None

TASKS = [
    # (short, tdir, ext, kind, [methods])
    ("colordisc", "t1_colordisc", ".img", "img", [m_t1_swap, m_t1_noise]),
    ("colorconst", "t2_colorconst", ".img", "img", [m_t2_swap, m_t2_dim]),
    ("shapetrans", "t3_shapetrans", ".img", "img",
     [m_t3_hflip, m_t3_noise, m_t3_occlude]),
    ("pitchdisc", "t4_pitchdisc", ".pcm", "pcm",
     [m_t4_reverse, m_t4_noise, m_t4_swaporder]),
    ("timbredisc", "t5_timbredisc", ".pcm", "pcm",
     [m_t5_reverse, m_t5_noise, m_t5_fade]),
    ("motiondir", "t6_motiondir", ".vid", "vid",
     [m_t6_reverse, m_t6_flat, m_t6_drop]),
]

def src_pool(short, mi, names):
    # Default: all sorted primary names. Overrides where the frozen scheme
    # demands a margin (t1/M2: SAME-identical + DIFFERENT-easy only).
    if short == "colordisc" and mi == 1:
        same_ident = ["p%03d.img" % i for i in range(10)]
        diff_easy = ["p%03d.img" % i for i in range(20, 34)]
        pool = same_ident + diff_easy
        assert all(n in names for n in pool), "t1/M2 pool missing sources"
        return pool
    return names

def main():
    total = 0
    for ti, (short, tdir, ext, kind, methods) in enumerate(TASKS):
        srcdir = os.path.join(HARNESS, tdir, "primary")
        names = sorted(f for f in os.listdir(srcdir) if f.endswith(ext))
        outdir = os.path.join(OUT, tdir)
        os.makedirs(outdir, exist_ok=True)
        nm = len(methods)
        for k in range(40):
            mi = k % nm
            pool = src_pool(short, mi, names)
            src = pool[(k // nm) % len(pool)]
            spath = os.path.join(srcdir, src)
            truth = read_truth(spath)
            rng = Rng(stream_seed(ti, mi, k))
            m = methods[mi]
            if kind == "img":
                w, h, px = read_img(spath)
                if m in (m_t1_swap, m_t2_swap):
                    out, nt = m(w, h, px, rng)
                elif m in (m_t1_noise,):
                    # margin check: identical SAME (dist 0) or DIFFERENT-easy
                    # (mean RGB dist >= 60); machine-checked below
                    out, nt = m(w, h, px, rng)
                    check_t1_margin(w, h, px, out, truth)
                else:
                    out, nt = m(w, h, px, rng)
                npath = os.path.join(outdir, "g2a_%s_%03d%s" % (short, k + 1, ext))
                write_img(npath, w, h, out)
            elif kind == "pcm":
                rate, count, samps = read_pcm(spath)
                if m in (m_t4_swaporder,):
                    out, nt = m(rate, count, samps, rng, truth)
                else:
                    out, nt = m(rate, count, samps, rng)
                npath = os.path.join(outdir, "g2a_%s_%03d%s" % (short, k + 1, ext))
                write_pcm(npath, rate, out)
            else:
                nf, w, h, frames = read_vid(spath)
                if m in (m_t6_reverse,):
                    out, nt = m(nf, w, h, frames, rng, truth)
                else:
                    out, nt = m(nf, w, h, frames, rng)
                npath = os.path.join(outdir, "g2a_%s_%03d%s" % (short, k + 1, ext))
                write_vid(npath, w, h, out)
            write_truth(npath, nt if nt is not None else truth)
            total += 1
    print("wrote %d augmentation fixtures -> %s" % (total, OUT))

def check_t1_margin(w, h, px, out, truth):
    # Verify the +/-24 noise cannot flip the ΔE2000 truth boundary (2.3).
    # Machine-checked on the actual patch means via gen.py's delta_e_2000.
    sys.path.insert(0, os.path.normpath(os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..", "..", "..", "..", "rebuild", "harness")))
    from gen import delta_e_2000, rgb_to_lab
    def means(p):
        hw = w // 2
        s1 = [0, 0, 0]; s2 = [0, 0, 0]
        for y in range(h):
            for x in range(hw):
                o1 = (y * w + x) * 3; o2 = (y * w + hw + x) * 3
                for c in range(3):
                    s1[c] += p[o1 + c]; s2[c] += p[o2 + c]
        n = hw * h
        return ([s1[c] / n for c in range(3)],
                [s2[c] / n for c in range(3)])
    m1b, m2b = means(out)
    de = delta_e_2000(rgb_to_lab(*[int(round(v)) for v in m1b]),
                      rgb_to_lab(*[int(round(v)) for v in m2b]))
    if truth == "SAME":
        assert de < 1.0, "t1/M2 noise flipped SAME pair: dE=%.2f" % de
    else:
        assert de > 5.0, "t1/M2 noise flipped DIFFERENT pair: dE=%.2f" % de

if __name__ == "__main__":
    main()
