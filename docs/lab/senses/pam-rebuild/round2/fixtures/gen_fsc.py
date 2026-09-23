#!/usr/bin/env python3
"""gen_fsc.py — frozen fixture generator for R2-15 (FS-C cross-modal booster).

Multimodal battery FSC-BATT. Each trial = visual (48x48 RGB) + audio (2.0s @8kHz
i16 PCM) evidence for a symbol S in {S0,S1,S2}:
  S0 = (visual CIRCLE,  audio SAME   / toneB 440.00 Hz)
  S1 = (visual TRIANGLE, audio HIGHER / toneB 528.00 Hz)
  S2 = (visual SQUARE,  audio LOWER  / toneB 366.67 Hz)

Families: M-N normal (400), M-U uncorrelated spoof (200), M-W within-modality
persistent spoof (200), M-C correlated cross-modal fooling (200), M-WA
audio-channel persistent spoof diagnostic (150).

Corruptions:
  FSC-VIS-1: tonal inversion (photographic negative) of the 48x48 render —
    the R2-3-proven deterministic fooler of the template matcher.
  FSC-AUD-1: pitch-shift of the symbol tone (tone-B regenerated at the lie
    symbol's frequency).

Every DISTINCT blob is VERIFIED once against a Python mirror of the exact naive
front-ends in forks/R2-3/src/r2p_front.zag (integer-identical algorithms);
renders are deterministic per (symbol, colors), so trials assemble verified
blobs by reference. A blob that cannot be verified is never written.

Master seed 20260923 (frozen, per R2_FIXTURE_SET.md). Stream ids 700+family —
new, no overlap with 400/500/600/900 streams. Construction is fully
deterministic from (family, idx).

Output: round2/fixtures/fsc/fsc_<fam>_b<batch>.fsc — batches of <=200 trials.
Trial layout: u32 LE trial_len, then:
  magic "FSC1" (4), truth u8, family u8, idx u32 LE,
  4 x (u32 LE blob_len + blob):
    visual-F image, visual-G image, audio-F pcm, audio-G pcm.
  image payload: u16 LE w, u16 LE h, then w*h*3 RGB bytes.
  pcm payload: u32 LE rate, u32 LE ns, then ns i16 LE samples.
"""
import math
import os
import re
import struct

import numpy as np

MASTER = 20260923
RATE = 8000
NS = 2 * RATE  # 2.0 s tokens
W = H = 48
BLK = 4  # downsample block for w=48 (front_shapetrans: blk=4 when w != 96)

SYMS = {0: ("CIRCLE", 440.00), 1: ("TRIANGLE", 528.00), 2: ("SQUARE", 366.67)}
TONEA_HZ = 440.00
AMP = 12000

FAMS = {"N": (0, 400), "U": (1, 200), "W": (2, 200), "C": (3, 200), "WA": (4, 150)}
BATCH = 200

LAB = os.path.expanduser("~/workspace/tnn-lab")
R23SRC = os.path.join(LAB, "senses/pam-rebuild/round2/forks/R2-3/src")
OUTDIR = os.path.join(LAB, "senses/pam-rebuild/round2/fixtures/fsc")


def load_protos():
    src = open(os.path.join(R23SRC, "r2p_protos.zag")).read()
    protos = {}
    for name in ("circle", "triangle", "square"):
        m = re.search(r"fn proto_p48_" + name + r"\(out:\[\]u8\) void \{(.*?)\n\}",
                      src, re.S)
        cells = set(int(x) for x in re.findall(r"out\[(\d+)\]=255", m.group(1)))
        protos[name] = cells
    return [protos[n] for n in ("circle", "triangle", "square")]


PROTOS = load_protos()
# 12x12 prototype grids as numpy arrays (255/0)
PGRID = []
for cells in PROTOS:
    g = np.zeros(144, dtype=np.int64)
    for c in cells:
        g[c] = 255
    PGRID.append(g)


def naive_shape(payload):
    """Exact mirror of front_shapetrans for w=48."""
    w, h = struct.unpack_from("<HH", payload, 0)
    assert (w, h) == (48, 48)
    px = np.frombuffer(payload[4:], dtype=np.uint8).reshape(h, w, 3).astype(np.int64)
    # 12x12 cells of 4x4 blocks; avg = s // (3*16); cell = 255 iff avg >= 128
    blk = px.reshape(12, BLK, 12, BLK, 3).sum(axis=(1, 3, 4))
    avg = blk // (3 * BLK * BLK)
    grid = np.where(avg >= 128, 255, 0).reshape(144)
    best, bestv = 0, None
    for proto in range(3):
        sad = int(np.abs(grid - PGRID[proto]).sum())
        if bestv is None or sad < bestv:  # ties keep lowest index (Zag logic)
            bestv, best = sad, proto
    return best


def zc_freq(smp, n, rate):
    """Exact mirror of zc_freq: smp = int16 array, base already applied."""
    a = smp[:n - 1].astype(np.int64)
    b = smp[1:n].astype(np.int64)
    sa = (a >= 0).astype(np.int64)
    sb = (b >= 0).astype(np.int64)
    gate = (np.abs(a) > 800) | (np.abs(b) > 800)
    zc = int(np.sum((sa != sb) & gate))
    if n <= 1:
        return 0
    return (zc * rate) // (2 * n)


def naive_pitch(payload):
    """Exact mirror of front_pitchdisc."""
    rate, ns = struct.unpack_from("<II", payload, 0)
    smp = np.frombuffer(payload[8:], dtype="<i2")
    a0 = (rate * 10) // 100
    a1 = (rate * 80) // 100
    b0 = (rate * 110) // 100
    b1 = (rate * 190) // 100
    fA = zc_freq(smp[a0:], a1 - a0, rate)
    fB = zc_freq(smp[b0:], b1 - b0, rate)
    if fA <= 0:
        return 0
    rel = abs(fB - fA) * 1000 // fA
    if rel < 5:
        return 0
    return 1 if fB > fA else 2


def render_shape(sym, fg, bg):
    name = SYMS[sym][0].lower()
    cells = PROTOS[["circle", "triangle", "square"].index(name)]
    cell = np.full(144, bg, dtype=np.uint8)
    for c in cells:
        cell[c] = fg
    img = np.repeat(np.repeat(cell.reshape(12, 12), BLK, axis=0), BLK, axis=1)
    rgb = np.stack([img, img, img], axis=-1)
    return struct.pack("<HH", W, H) + rgb.tobytes()


_TONE_CACHE = {}


def render_tone(sym):
    if sym in _TONE_CACHE:
        return _TONE_CACHE[sym]
    fB = SYMS[sym][1]
    t = np.arange(NS) / RATE
    env = np.zeros(NS)
    env[t < 0.9] = 1.0
    m = (t >= 1.1) & (t < 1.9)
    sig = np.zeros(NS)
    sig[t < 0.9] = AMP * np.sin(2 * np.pi * TONEA_HZ * t[t < 0.9])
    sig[m] = AMP * np.sin(2 * np.pi * fB * (t[m] - 1.1))
    pcm = np.clip(np.round(sig), -32768, 32767).astype("<i2")
    blob = struct.pack("<II", RATE, NS) + pcm.tobytes()
    _TONE_CACHE[sym] = blob
    return blob


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    # ---- verify every distinct blob once ----
    V = {}  # (kind, sym, fg, bg) -> blob ; A[(kind, sym)] -> blob
    for sym in (0, 1, 2):
        for key, fg, bg, expect in (
            ("clean60", 255, 60, sym), ("clean64", 255, 64, sym),
        ):
            b = render_shape(sym, fg, bg)
            got = naive_shape(b)
            assert got == expect, (key, sym, got, expect)
            V[("v", sym, key)] = b
        # FSC-VIS-1: tonal inversion variants in fixed order
        lied = False
        for key, fg, bg in (("inv200", 10, 200), ("inv255", 0, 255)):
            b = render_shape(sym, fg, bg)
            got = naive_shape(b)
            if not lied and got != sym:
                V[("v", sym, "lie")] = b
                V[("vlie", sym)] = got
                lied = True
            if got != sym:
                V[("v", sym, key)] = b
        assert lied, f"inversion failed to flip symbol {sym}"
        bc = render_tone(sym)
        got = naive_pitch(bc)
        assert got == sym, ("audio clean", sym, got)
        V[("a", sym, "clean")] = bc
    # audio lies: tone of lie symbol, verified per (truth->lie) pair used below
    for truth in (0, 1, 2):
        lie = V[("vlie", truth)]
        b = render_tone(lie)
        assert naive_pitch(b) == lie, ("audio lie", truth, lie)
        V[("a", truth, "lieC")] = b  # M-C: audio fooled to visual lie
        alie = (truth + 1) % 3
        b2 = render_tone(alie)
        assert naive_pitch(b2) == alie
        V[("a", truth, "lieWA")] = b2  # M-WA: audio fooled, visual clean
    print("distinct-blob verification OK:",
          {s: V[("vlie", s)] for s in (0, 1, 2)}, "(visual lie per truth)")

    total = 0
    for fam, (fid, count) in FAMS.items():
        trials = []
        for idx in range(count):
            truth = idx % 3
            if fam in ("U", "W", "C"):
                visF = V[("v", truth, "lie")]
                visG = (V[("v", truth, "inv200")] if fam == "W"
                        else V[("v", truth, "clean60")])
                # M-W gate span: second corrupted render (different gray)
                if fam == "W":
                    alt = V.get(("v", truth, "inv255"))
                    visG = alt if (alt is not None
                                   and naive_shape(alt) == V[("vlie", truth)]) \
                        else V[("v", truth, "inv200")]
            else:
                visF = V[("v", truth, "clean60")]
                visG = V[("v", truth, "clean64")]
            if fam == "C":
                audF, audG = V[("a", truth, "lieC")], V[("a", truth, "clean")]
            elif fam == "WA":
                audF = audG = V[("a", truth, "lieWA")]
            else:
                audF = audG = V[("a", truth, "clean")]
            body = (b"FSC1" + struct.pack("<BBI", truth, fid, idx)
                    + b"".join(struct.pack("<I", len(b)) + b
                               for b in (visF, visG, audF, audG)))
            trials.append(struct.pack("<I", len(body)) + body)
            total += 1
        for bnum, start in enumerate(range(0, len(trials), BATCH)):
            path = os.path.join(OUTDIR, f"fsc_{fam}_b{bnum}.fsc")
            with open(path, "wb") as f:
                f.write(b"".join(trials[start:start + BATCH]))
        print(f"family {fam}: {count} trials, "
              f"{(len(trials) + BATCH - 1) // BATCH} batch file(s)")
    print(f"TOTAL {total} trials in {OUTDIR}")


if __name__ == "__main__":
    main()
