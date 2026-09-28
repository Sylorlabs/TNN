#!/usr/bin/env python3
"""Self-PAM push-to-100% ROUND 2 - adversarial expansion corpus generator.

FROZEN 2026-09-27. Deterministic, zero RNG: combinatorial construction from
fixed seeds via splitmix64. No `random` module, no wall-clock, no dict-order
dependence. Two runs on the same machine produce byte-identical output
(verified: see FAMILIES.md).

Output: <outdir>/xp_<family>_<task>_<NNN>.pair + .pair.truth, plus
MANIFEST.expansion.sha256 (written by the finalize step below).

Pair format (matches round2/fixtures/r2p on-disk layout):
  64-byte header: b"R2P1"@0, task<i32@4, idx<i32@8, scene<u64@12,
                  f_len<i32@20, g_len<i32@24, 36 zero pad bytes@28..63,
  then F bytes (f_len), then G bytes (g_len).
Truth file: truth=<value>\\nfamily=<slug>\\ntask=<name>\\nscene=<u64>\\n
            note=<text>\\n (+ calibration=1 for family 7).

Task ids: colordisc=0, colorconst=1, shapetrans=2, pitchdisc=3, timbredisc=4,
motiondir=5 (same as round2/fixtures/gen_r2p.py TASKS).

Usage:
  gen_expansion.py <outdir>          # generate corpus into <outdir>
  (run twice into two dirs and diff -r to verify determinism)

This generator NEVER runs any gate against the corpus. It only asserts
construction well-formedness (F/G genuinely differ in the stated fact,
multisets/rotations/swaps exact where claimed).
"""
import hashlib
import math
import os
import struct
import sys

MASTER = 20260927
MASK64 = 0xFFFFFFFFFFFFFFFF

TASKS = ["colordisc", "colorconst", "shapetrans", "pitchdisc", "timbredisc",
         "motiondir"]
TASK_ID = {t: i for i, t in enumerate(TASKS)}

# --------------------------------------------------------------------------
# deterministic RNG: splitmix64 (no `random` module anywhere)


def splitmix64(x):
    x = (x + 0x9E3779B97F4A7C15) & MASK64
    z = x
    z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & MASK64
    z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & MASK64
    return (z ^ (z >> 31)) & MASK64


class Rng:
    def __init__(self, seed):
        self.s = seed & MASK64

    def u64(self):
        self.s = splitmix64(self.s)
        return self.s

    def below(self, n):
        assert n > 0
        return self.u64() % n


FAM_STREAM = {
    "fshuffle": 11,
    "audiorev": 12,
    "pxperm": 13,
    "cycshift": 14,
    "blkswap": 15,
    "sumswap": 16,
    "calib": 17,
    "wsumcol": 18,
}


def pair_rng(fam, task_id, idx):
    s = splitmix64(MASTER ^ ((FAM_STREAM[fam] * 0x9E3779B97F4A7C15) & MASK64))
    s ^= (task_id * 0xBF58476D1CE4E5B9) & MASK64
    s ^= (idx * 0x94D049BB133111EB) & MASK64
    return Rng(splitmix64(s))


# --------------------------------------------------------------------------
# payload builders (mirror round2/fixtures/gen_r2p.py encodings)


def frames_payload(frames, w, h):
    return struct.pack("<IHH", len(frames), w, h) + b"".join(frames)


def pcm_payload(rate, samples):
    return (struct.pack("<II", rate, len(samples)) +
            struct.pack("<%dh" % len(samples), *samples))


def pcm_samples(payload):
    rate, ns = struct.unpack("<II", payload[:8])
    assert len(payload) == 8 + 2 * ns, "pcm payload length mismatch"
    return rate, list(struct.unpack("<%dh" % ns, payload[8:]))


def motiondir_frames(rng):
    """8 frames, 16x8 RGB: white 2x2 dot moving E (x=0,2,...,14)."""
    w, h, nf = 16, 8, 8
    bg, dot = (10, 10, 18), (235, 235, 235)
    y = 3 + rng.below(3)
    frames = []
    for k in range(nf):
        fr = bytearray(bg * (w * h))
        x = 2 * k
        for dy in range(2):
            for dx in range(2):
                p = (y + dy) * w + (x + dx)
                fr[3 * p:3 * p + 3] = bytes(dot)
        frames.append(bytes(fr))
    return frames, w, h


def shapetrans_frames(rng):
    """8 frames, 16x8 RGB: red 3x3 square translating E (x=0..7)."""
    w, h, nf = 16, 8, 8
    bg, sq = (12, 14, 12), (200, 60, 60)
    y = 2 + rng.below(3)
    frames = []
    for k in range(nf):
        fr = bytearray(bg * (w * h))
        x = k
        for dy in range(3):
            for dx in range(3):
                p = (y + dy) * w + (x + dx)
                fr[3 * p:3 * p + 3] = bytes(sq)
        frames.append(bytes(fr))
    return frames, w, h


def splitfield_frame():
    """1 frame, 16x8 RGB: left half red, right half blue."""
    w, h = 16, 8
    a, b = (200, 30, 30), (30, 30, 200)
    fr = bytearray()
    for _ in range(h):
        for x in range(w):
            fr += bytes(a if x < w // 2 else b)
    return [bytes(fr)], w, h


def glide_samples(f0=400.0, f1=800.0, dur=0.25, rate=8000):
    """Sine + 2nd harmonic, linear pitch glide f0->f1, 10 ms ramps."""
    n = int(rate * dur)
    out = [0.0] * n
    ph = 0.0
    for i in range(n):
        fr = f0 + (f1 - f0) * i / n
        ph += 2.0 * math.pi * fr / rate
        out[i] = math.sin(ph) + 0.3 * math.sin(2.0 * ph)
    r = int(rate * 0.01)
    for i in range(r):
        e = 0.5 - 0.5 * math.cos(math.pi * i / r)
        out[i] *= e
        out[n - 1 - i] *= e
    peak = max(1e-9, max(abs(v) for v in out))
    return [int(max(-32768, min(32767, round(v * 30000.0 / peak)))) for v in out]


def pluck_samples(freq=440.0, dur=0.25, rate=8000):
    """Bright pluck: 4 harmonics, 5 ms attack, 60 ms exp decay."""
    n = int(rate * dur)
    out = []
    for i in range(n):
        t = i / rate
        env = min(1.0, t / 0.005) * math.exp(-t / 0.06)
        ph = 2.0 * math.pi * freq * t
        v = (math.sin(ph) + 0.5 * math.sin(2 * ph) +
             0.25 * math.sin(3 * ph) + 0.12 * math.sin(4 * ph))
        out.append(v * env)
    peak = max(1e-9, max(abs(v) for v in out))
    return [int(max(-32768, min(32767, round(v * 30000.0 / peak)))) for v in out]


# --------------------------------------------------------------------------
# permutation helpers


def derangement(rng, n):
    """Uniform-ish derangement via rejection-sampled Fisher-Yates.

    Guarantees: no fixed points, not the identity, not the reversal."""
    rev = list(range(n - 1, -1, -1))
    while True:
        p = list(range(n))
        for i in range(n - 1, 0, -1):
            j = rng.below(i + 1)
            p[i], p[j] = p[j], p[i]
        if any(p[i] == i for i in range(n)):
            continue
        if p == rev:
            continue
        return p  # identity excluded: derangement => no fixed points, n>1


def apply_frame_perm(frames, p):
    return [frames[p[i]] for i in range(len(frames))]


def permute_pixels(frames, q):
    out = []
    for fr in frames:
        px = [fr[3 * i:3 * i + 3] for i in range(len(fr) // 3)]
        assert len(px) == len(q)
        out.append(b"".join(px[q[i]] for i in range(len(px))))
    return out


def plain_sum(b):
    return sum(b)


def weighted_sum(b):
    # exact (big-int) position-weighted sum; /8 quantization collides iff
    # exact values share the same floor(.../8) for non-negative inputs
    return sum((i + 1) * v for i, v in enumerate(b))


# --------------------------------------------------------------------------
# pair emission + generic well-formedness assertions


class Emitter:
    def __init__(self, outdir):
        self.outdir = outdir
        self.names = set()
        self.counts = {}
        os.makedirs(outdir, exist_ok=True)

    def emit(self, fam, task, idx, f_bytes, g_bytes, truth, note,
             calibration=False, allow_identical=False):
        name = "xp_%s_%s_%03d.pair" % (fam, task, idx)
        assert name not in self.names, "duplicate pair name " + name
        self.names.add(name)
        tid = TASK_ID[task]
        rng = pair_rng(fam, tid, idx)
        scene = rng.u64()  # derived AFTER construction draws: still deterministic
        # NOTE: pair_rng is re-seeded per pair, so drawing scene from a fresh
        # Rng with the same seed is independent of how many draws the builder
        # consumed. Deterministic by construction.
        if allow_identical:
            assert f_bytes == g_bytes, "calib-identical pair not identical"
        else:
            assert f_bytes != g_bytes, "F and G must differ"
        hdr = b"R2P1"
        hdr += struct.pack("<i", tid) + struct.pack("<i", idx)
        hdr += struct.pack("<Q", scene)
        hdr += struct.pack("<i", len(f_bytes)) + struct.pack("<i", len(g_bytes))
        hdr += bytes(36)
        assert len(hdr) == 64
        path = os.path.join(self.outdir, name)
        with open(path, "wb") as f:
            f.write(hdr)
            f.write(f_bytes)
            f.write(g_bytes)
        # read-back verification of the header + lengths
        d = open(path, "rb").read()
        assert d[0:4] == b"R2P1"
        assert struct.unpack("<i", d[4:8])[0] == tid
        assert struct.unpack("<i", d[8:12])[0] == idx
        assert struct.unpack("<Q", d[12:20])[0] == scene
        assert struct.unpack("<i", d[20:24])[0] == len(f_bytes)
        assert struct.unpack("<i", d[24:28])[0] == len(g_bytes)
        assert d[28:64] == bytes(36)
        assert d[64:64 + len(f_bytes)] == f_bytes
        assert d[64 + len(f_bytes):] == g_bytes
        tpath = path + ".truth"
        with open(tpath, "w") as f:
            f.write("truth=%s\n" % truth)
            f.write("family=%s\n" % fam)
            f.write("task=%s\n" % task)
            f.write("scene=%d\n" % scene)
            if calibration:
                f.write("calibration=1\n")
            f.write("note=%s\n" % note)
        # read-back verification of the truth file
        t = open(tpath).read()
        assert ("truth=%s\n" % truth) in t and ("note=%s\n" % note) in t
        self.counts[fam] = self.counts.get(fam, 0) + 1
        return path


# --------------------------------------------------------------------------
# Family 1: frame-shuffle (order-only, deranged non-reversal permutation)


def build_fshuffle(em):
    for task, n in (("motiondir", 24), ("shapetrans", 24)):
        tid = TASK_ID[task]
        for idx in range(n):
            rng = pair_rng("fshuffle", tid, idx)
            if task == "motiondir":
                frames, w, h = motiondir_frames(rng)
                desc = "dot moves E (x=0,2,...,14)"
            else:
                frames, w, h = shapetrans_frames(rng)
                desc = "3x3 square translates E (x=0..7)"
            p = derangement(rng, len(frames))
            g = frames_payload(frames, w, h)
            f = frames_payload(apply_frame_perm(frames, p), w, h)
            # assertions: genuine derangement, multiset preserved, F != G
            assert all(p[i] != i for i in range(len(p)))
            assert p != list(range(len(p) - 1, -1, -1)), "reversal forbidden"
            assert sorted(frames) == sorted(apply_frame_perm(frames, p))
            assert len(set(frames)) == len(frames), "frames must be distinct"
            assert f != g
            note = ("frame-shuffle attack: G frames in order [%s]; F frames in "
                    "deranged order p=%s (no fixed points, not identity, not "
                    "reversal); identical frame multiset, order-only difference"
                    % (desc, p))
            em.emit("fshuffle", task, idx, f, g, "DIFFERENT", note)


# --------------------------------------------------------------------------
# Family 2: audio time-reversal


def build_audiorev(em):
    for task, n in (("pitchdisc", 24), ("timbredisc", 24)):
        tid = TASK_ID[task]
        for idx in range(n):
            rng = pair_rng("audiorev", tid, idx)
            _ = rng.u64()  # consume deterministically; content is fixed
            if task == "pitchdisc":
                samp = glide_samples()
                desc = "G glide rises 400->800 Hz; F falls 800->400 Hz"
            else:
                samp = pluck_samples()
                desc = ("G sharp-attack/exp-decay pluck; F slow-swell/"
                        "abrupt-cutoff")
            g = pcm_payload(8000, samp)
            f = pcm_payload(8000, samp[::-1])
            # assertions: exact time reversal at the sample level
            _, fs = pcm_samples(f)
            assert fs == samp[::-1], "F is not the sample-reversed G"
            assert f != g
            assert sorted(samp) == sorted(fs), "sample multiset changed"
            note = ("audio time-reversal attack: %s; %d samples, identical "
                    "sample multiset, reversed temporal order"
                    % (desc, len(samp)))
            em.emit("audiorev", task, idx, f, g, "DIFFERENT", note)


# --------------------------------------------------------------------------
# Family 3: pixel permutation within each frame


def build_pxperm(em):
    plan = (("colordisc", 16), ("colorconst", 16), ("shapetrans", 16))
    for task, n in plan:
        tid = TASK_ID[task]
        for idx in range(n):
            rng = pair_rng("pxperm", tid, idx)
            if task == "shapetrans":
                frames, w, h = shapetrans_frames(rng)
                desc = "translating-square frames"
            else:
                frames, w, h = splitfield_frame()
                desc = "left-red/right-blue split field"
            npix = len(frames[0]) // 3
            q = derangement(rng, npix)
            g = frames_payload(frames, w, h)
            f = frames_payload(permute_pixels(frames, q), w, h)
            # assertions: per-frame pixel multiset preserved, layout destroyed
            pf = permute_pixels(frames, q)
            for a, b in zip(frames, pf):
                assert sorted(a[i:i + 3] for i in range(0, len(a), 3)) == \
                       sorted(b[i:i + 3] for i in range(0, len(b), 3))
            assert all(q[i] != i for i in range(npix)), "q not deranged"
            assert f != g
            note = ("pixel-permutation attack: %d pixels deranged within each "
                    "frame (q fixed, no fixed points); %s; identical pixel "
                    "multiset, spatial structure destroyed"
                    % (npix, desc))
            em.emit("pxperm", task, idx, f, g, "DIFFERENT", note)


# --------------------------------------------------------------------------
# Family 4: cyclic phase shift (byte rotation by len//3)


def build_cycshift(em):
    plan = (("shapetrans", 24), ("pitchdisc", 24))
    for task, n in plan:
        tid = TASK_ID[task]
        for idx in range(n):
            rng = pair_rng("cycshift", tid, idx)
            if task == "shapetrans":
                frames, w, h = shapetrans_frames(rng)
                g = frames_payload(frames, w, h)
            else:
                g = pcm_payload(8000, glide_samples())
            N = len(g) // 3
            f = g[N:] + g[:N]
            assert f == g[N:] + g[:N]
            assert sorted(f) == sorted(g), "byte multiset changed"
            assert f != g, "rotation is a fixed point (periodic G)"
            note = ("cyclic-shift attack: F = G rotated left by N=%d "
                    "(len//3, len=%d); identical byte multiset, order-only "
                    "difference; sum-blind" % (N, len(g)))
            em.emit("cycshift", task, idx, f, g, "DIFFERENT", note)


# --------------------------------------------------------------------------
# Family 5: block swap (second half + first half)


def build_blkswap(em):
    plan = (("shapetrans", 24), ("pitchdisc", 24))
    for task, n in plan:
        tid = TASK_ID[task]
        for idx in range(n):
            rng = pair_rng("blkswap", tid, idx)
            if task == "shapetrans":
                frames, w, h = shapetrans_frames(rng)
                g = frames_payload(frames, w, h)
            else:
                g = pcm_payload(8000, glide_samples())
            assert len(g) % 2 == 0
            m = len(g) // 2
            f = g[m:] + g[:m]
            assert f[:len(g) - m] == g[m:] and f[len(g) - m:] == g[:m]
            assert sorted(f) == sorted(g), "byte multiset changed"
            assert f != g, "block swap is a fixed point"
            note = ("block-swap attack: F = G[%d:]+G[:%d] (len=%d); identical "
                    "byte multiset, order-only difference; sum-blind"
                    % (m, m, len(g)))
            em.emit("blkswap", task, idx, f, g, "DIFFERENT", note)


# --------------------------------------------------------------------------
# Family 6: sum-preserving targeted swap (attacks the current sum directly)


def build_sumswap(em):
    plan = (("shapetrans", 24), ("pitchdisc", 24))
    for task, n in plan:
        tid = TASK_ID[task]
        for idx in range(n):
            rng = pair_rng("sumswap", tid, idx)
            if task == "shapetrans":
                frames, w, h = shapetrans_frames(rng)
                g = frames_payload(frames, w, h)
            else:
                g = pcm_payload(8000, glide_samples())
            L = len(g)
            # deterministic search for two positions with differing values
            i = rng.below(L)
            j = rng.below(L)
            guard = 0
            while (j == i or g[j] == g[i]) and guard < 10000:
                j = rng.below(L)
                guard += 1
            assert j != i and g[j] != g[i], "no swappable pair found"
            fb = bytearray(g)
            fb[i], fb[j] = fb[j], fb[i]
            f = bytes(fb)
            # assertions: plain sum preserved EXACTLY, exactly 2 bytes differ
            assert plain_sum(f) == plain_sum(g), "byte sum not preserved"
            diffs = [k for k in range(L) if f[k] != g[k]]
            assert diffs == sorted([i, j]) or set(diffs) == {i, j}
            assert len(diffs) == 2
            assert f != g
            note = ("sum-preserving swap attack: bytes at i=%d (%d) and j=%d "
                    "(%d) exchanged; plain byte sum identical (%d); depicted "
                    "content differs at 2 positions"
                    % (i, g[i], j, g[j], plain_sum(g)))
            em.emit("sumswap", task, idx, f, g, "DIFFERENT", note)


# --------------------------------------------------------------------------
# Family 7: tolerance probes (CALIBRATION, not attacks)


def build_calib(em):
    # 7a: byte-identical must-admit controls
    for idx in range(20):
        tid = TASK_ID["shapetrans"] if idx % 2 == 0 else TASK_ID["pitchdisc"]
        task = TASKS[tid]
        rng = pair_rng("calib", tid, idx)
        if task == "shapetrans":
            frames, w, h = shapetrans_frames(rng)
            g = frames_payload(frames, w, h)
        else:
            g = pcm_payload(8000, glide_samples())
        f = g  # byte-identical
        note = ("CALIBRATION must-admit control: F and G byte-identical "
                "(len=%d); any correct gate judges them identically"
                % len(g))
        em.emit("calib", task, idx, f, g, "SAME", note, calibration=True,
                allow_identical=True)
    # 7b: single-byte +/-1 tolerance-boundary probes
    for k in range(20):
        idx = 20 + k
        tid = TASK_ID["shapetrans"] if k % 2 == 0 else TASK_ID["pitchdisc"]
        task = TASKS[tid]
        rng = pair_rng("calib", tid, idx)
        if task == "shapetrans":
            frames, w, h = shapetrans_frames(rng)
            g = frames_payload(frames, w, h)
        else:
            g = pcm_payload(8000, glide_samples())
        pos = rng.below(len(g))
        old = g[pos]
        delta = -1 if old == 255 else (1 if old == 0 else (1 if rng.below(2) else -1))
        fb = bytearray(g)
        fb[pos] = (old + delta) & 0xFF
        f = bytes(fb)
        # assertions: exactly one byte differs, by exactly +/-1
        diffs = [p for p in range(len(g)) if f[p] != g[p]]
        assert diffs == [pos]
        assert abs(f[pos] - g[pos]) == 1
        assert f != g
        note = ("CALIBRATION tolerance-boundary probe: single byte at pos=%d "
                "%d->%d (%+d); underlying fact effectively unchanged; probes "
                "the sum/8 quantization boundary" % (pos, old, f[pos], delta))
        em.emit("calib", task, idx, f, g, "SAME", note, calibration=True)


# --------------------------------------------------------------------------
# Family 8: weighted-sum collision attempts (for the future fixed gate)
#
# Construction: pick positions p0 < p1 < p2 in arithmetic progression
# (p1 = p0+d, p2 = p0+2d) holding values (x, z, y) with 2y = x+z
# (y the midpoint). F applies the 3-cycle p0<-p2, p1<-p0, p2<-p1, i.e.
#   F[p0]=y, F[p1]=x, F[p2]=z.
# Weighted-sum delta: with A = p0+1,
#   dW = A(y-x) + (A+d)(x-z) + (A+2d)(z-y)
#      = A(y-x+x-z+z-y) + d(x-z+2z-2y)
#      = d(x+z-2y) = 0   since 2y = x+z.
# So BOTH the plain byte sum (permutation) and the position-weighted sum
# are preserved EXACTLY, while 3 bytes genuinely change value. Chaining 4
# disjoint triples changes 12 bytes. /8 quantization therefore collides
# trivially (exact equality implies equal floors).


def build_wsumcol(em):
    tid = TASK_ID["shapetrans"]
    for idx in range(24):
        rng = pair_rng("wsumcol", tid, idx)
        frames, w, h = shapetrans_frames(rng)
        g = bytearray(frames_payload(frames, w, h))
        L = len(g)
        d = 151
        triples = []
        base = 64
        x0 = [16, 32, 48][rng.below(3)]  # deterministic per-pair variation
        for k in range(4):
            a = base + k * 640
            p0, p1, p2 = a, a + d, a + 2 * d
            assert p2 < L, "triple exceeds payload"
            triples.append((p0, p1, p2))
        # triples must be pairwise disjoint
        used = [p for t in triples for p in t]
        assert len(set(used)) == 12, "triples overlap"
        x = x0
        z = x + 200
        y = x + 100  # 2y = x+z  <=>  y = x+100
        assert 2 * y == x + z
        assert z <= 255
        f = bytearray(g)
        for (p0, p1, p2) in triples:
            g[p0], g[p1], g[p2] = x, z, y   # embed the AP-valued pattern
            f[p0], f[p1], f[p2] = y, x, z   # 3-cycle
        g, f = bytes(g), bytes(f)
        # assertions: the honest collision claim, verified exactly
        assert plain_sum(f) == plain_sum(g), "plain sum not preserved"
        wf, wg = weighted_sum(f), weighted_sum(g)
        assert wf == wg, "weighted sum not preserved: %d vs %d" % (wf, wg)
        assert wf // 8 == wg // 8, "/8 quantization differs"
        diffs = [p for p in range(L) if f[p] != g[p]]
        assert len(diffs) == 12, "expected 12 changed bytes, got %d" % len(diffs)
        assert f != g
        note = ("weighted-sum COLLISION (constructed): 4 disjoint 3-cycles at "
                "AP positions %s (d=%d) with midpoint values x=%d,z=%d,y=%d "
                "(2y=x+z); plain sum=%d and weighted sum=%d identical EXACTLY "
                "(hence /8 quantization collides); 12 bytes genuinely differ"
                % ([t[0] for t in triples], d, x, z, y, plain_sum(g), wg))
        em.emit("wsumcol", "shapetrans", idx, f, g, "DIFFERENT", note)


# --------------------------------------------------------------------------


def main():
    outdir = sys.argv[1] if len(sys.argv) > 1 else "pairs"
    em = Emitter(outdir)
    build_fshuffle(em)
    build_audiorev(em)
    build_pxperm(em)
    build_cycshift(em)
    build_blkswap(em)
    build_sumswap(em)
    build_calib(em)
    build_wsumcol(em)
    total = sum(em.counts.values())
    print("family counts: " +
          ", ".join("%s=%d" % (k, em.counts[k]) for k in sorted(em.counts)))
    print("total pairs: %d (%d files)" % (total, 2 * total))
    assert total == 352, "expected 352 pairs, got %d" % total


if __name__ == "__main__":
    main()
