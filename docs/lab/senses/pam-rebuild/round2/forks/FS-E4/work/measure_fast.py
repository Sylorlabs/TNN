#!/usr/bin/env python3
"""FS-E4 feasibility measurement, vectorized (analysis only)."""
import os
import struct
import sys

import numpy as np

sys.path.insert(0, os.path.expanduser(
    "~/workspace/tnn-lab/senses/pam-rebuild/round2/forks/R2-3/src/mirror"))
import t3_protos as TP

FIX = os.path.expanduser(
    "~/workspace/tnn-lab/senses/pam-rebuild/round2/forks/R2-7/fixtures_R2A")
TASKS = ["colordisc", "shapetrans", "pitchdisc"]
TRUTH2CODE = {
    "colordisc": {"SAME": 0, "DIFFERENT": 1},
    "shapetrans": {"CIRCLE": 0, "TRIANGLE": 1, "SQUARE": 2},
    "pitchdisc": {"SAME": 0, "HIGHER": 1, "LOWER": 2},
}
P96 = [np.frombuffer(TP.P96_CIRCLE, dtype=np.uint8).astype(np.int32),
       np.frombuffer(TP.P96_TRIANGLE, dtype=np.uint8).astype(np.int32),
       np.frombuffer(TP.P96_SQUARE, dtype=np.uint8).astype(np.int32)]
P48 = [np.frombuffer(TP.P48_CIRCLE, dtype=np.uint8).astype(np.int32),
       np.frombuffer(TP.P48_TRIANGLE, dtype=np.uint8).astype(np.int32),
       np.frombuffer(TP.P48_SQUARE, dtype=np.uint8).astype(np.int32)]

def parse_r2fx(path):
    with open(path, "rb") as f:
        data = f.read()
    magic, task, index, family, fo, fl, go, gl = struct.unpack("<8I", data[:32])
    assert magic == 0x52324658, path
    with open(path + ".truth") as f:
        truth = f.read().split("=")[1].strip().split()[0]
    return index, family, data[fo:fo + fl], data[go:go + gl], truth

def j_colordisc(span):
    rgb = np.frombuffer(span[:6144], dtype=np.uint8).astype(np.int64)
    # 6144B = 2 patches of 32x32x3; as a 64x32 frame: left = patch A, right = patch B
    img = rgb.reshape(32, 64, 3)
    ml = img[:, :32, :].reshape(-1, 3).mean(axis=0)
    mr = img[:, 32:, :].reshape(-1, 3).mean(axis=0)
    d2 = int(((ml - mr) ** 2).sum())
    return 0 if d2 < 400 else 1

def j_shapetrans(span, w):
    g = np.frombuffer(span, dtype=np.uint8).astype(np.int32).reshape(w, w)
    blk = 8 if w == 96 else 4
    ds = g.reshape(12, blk, 12, blk).mean(axis=(1, 3))
    grid = np.where(ds >= 128, 255, 0).astype(np.int32).ravel()
    protos = P96 if w == 96 else P48
    sads = [int(np.abs(grid - p).sum()) for p in protos]
    return int(np.argmin(sads))

def j_pitchdisc(span):
    samps = np.frombuffer(span, dtype=np.int16).astype(np.int64)
    rate = 16000
    a = samps[int(0.10 * rate):int(0.80 * rate)]
    b = samps[int(1.10 * rate):int(1.90 * rate)]
    def zcf(s):
        sa = s[:-1] >= 0
        sb = s[1:] >= 0
        cross = sa != sb
        big = (np.abs(s[:-1]) > 800) | (np.abs(s[1:]) > 800)
        zc = int((cross & big).sum())
        n = len(s)
        return (zc * rate) // (2 * n) if n > 1 else 0
    fA, fB = zcf(a), zcf(b)
    if fA <= 0:
        return 0
    rel = abs(fB - fA) * 1000 // fA
    if rel < 5:
        return 0
    return 1 if fB > fA else 2

def main():
    for task in TASKS:
        print("=" * 70, flush=True)
        print("TASK", task, flush=True)
        for split in ("r2n", "r2a", "r2a2"):
            d = os.path.join(FIX, split)
            files = sorted(f for f in os.listdir(d)
                           if f.startswith(split + "_" + task + "_")
                           and f.endswith(".r2fx"))
            n = both = f_fooled = ff_gok = ff_gsame = 0
            fool_targets = {}
            for fn in files:
                idx, fam, fs, gs, truth = parse_r2fx(os.path.join(d, fn))
                tc = TRUTH2CODE[task][truth]
                if task == "colordisc":
                    fj, gj = j_colordisc(fs), j_colordisc(gs)
                elif task == "shapetrans":
                    fj, gj = j_shapetrans(fs, 96), j_shapetrans(gs, 48)
                else:
                    fj, gj = j_pitchdisc(fs), j_pitchdisc(gs)
                n += 1
                if fj == tc and gj == tc:
                    both += 1
                if fj != tc:
                    f_fooled += 1
                    fool_targets[fj] = fool_targets.get(fj, 0) + 1
                    if gj == tc:
                        ff_gok += 1
                    elif gj == fj:
                        ff_gsame += 1
            print(f"  {split}: n={n} both_ok={both} ({100.*both/n:.1f}%) "
                  f"F_fooled={f_fooled} (G_ok|fooled={ff_gok}, "
                  f"G_same_lie|fooled={ff_gsame})", flush=True)
            if fool_targets:
                print(f"    fool targets: {fool_targets}", flush=True)

if __name__ == "__main__":
    main()
