#!/usr/bin/env python3
"""FS-F2C Phase 0e — linear von Kries with illuminant-estimate FLOOR.

Principled fix for degenerate channels (fixture 331: ~zero blue mean):
e_c = max(e_c, E_MIN) bounds the noise amplification (q = lin*10000/e)
without discarding any channel's signal (gating hurt: 81.67% < 83.19%).

Variant LCf: d = mean_i L1(chroma(qA_i), chroma(qB_i)), all 3 channels,
clip exclusion (>=250 in either view), e floored at E_MIN.
Also re-tests dark-pixel exclusion on top (LCfd): skip pixels with
(qA_r+qA_g+qA_b < 1500) or (qB sum < 1500) — normalized brightness floor.
"""
import struct, os, sys

FIX = os.path.expanduser("~/workspace/tnn-lab/senses/pam-rebuild/round2/forks/FS-E2")
TSV = os.path.expanduser("~/workspace/tnn-lab/senses/pam-rebuild/round2/forks/FS-E2/evidence/phase0/form_r2n_colorconst.tsv")

LUT = []
for c in range(256):
    x = c / 255.0
    lin = x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4
    LUT.append(int(round(lin * 10000)))

def load(path):
    b = open(path, "rb").read()
    magic, task, idx, family, fo, fl, go, gl = struct.unpack("<8I", b[:32])
    return b[fo:fo + fl]

def variant(path, emin, darkex):
    img = load(path); n = len(img) // 6
    # pass 1: linear means
    ea = [0, 0, 0]; eb = [0, 0, 0]
    for i in range(n):
        for c in range(3):
            ea[c] += LUT[img[3*i+c]]; eb[c] += LUT[img[6912+3*i+c]]
    ea = [max(e // n, emin) for e in ea]
    eb = [max(e // n, emin) for e in eb]
    # pass 2: per-pixel normalized chromaticity L1
    tot = 0; cnt = 0
    for i in range(n):
        ra = [img[3*i+c] for c in range(3)]; rb = [img[6912+3*i+c] for c in range(3)]
        if max(ra) >= 250 or max(rb) >= 250:
            continue
        qa = [LUT[ra[c]] * 10000 // ea[c] for c in range(3)]
        qb = [LUT[rb[c]] * 10000 // eb[c] for c in range(3)]
        if darkex and (sum(qa) < 1500 or sum(qb) < 1500):
            continue
        sa, sb = sum(qa), sum(qb)
        if sa < 1: sa = 1
        if sb < 1: sb = 1
        for c in range(3):
            tot += abs(qa[c]*1000//sa - qb[c]*1000//sb)
        cnt += 1
    if cnt < 1:
        return 0
    return tot // cnt

def truth_of(path):
    t = open(path + ".truth").read().strip()
    return t[6:] if t.startswith("truth=") else t

data = []
for line in open(TSV):
    p = line.rstrip("\n").split("\t")
    path = os.path.normpath(os.path.join(FIX, p[0]))
    data.append((path, truth_of(path)))

for emin, darkex, name in ((200, False, "LCf"), (200, True, "LCfd"),
                           (400, False, "LCf400"), (100, False, "LCf100")):
    vals = [(variant(p, emin, darkex), t) for (p, t) in data]
    s = sorted(x[0] for x in vals if x[1] == "SAME_SURFACE")
    d = sorted(x[0] for x in vals if x[1] == "DIFFERENT")
    cand = sorted(set(x[0] for x in vals))
    best = (0, 0)
    # accuracy-vs-T curve: record acc at best and flatness (+/-15 around T)
    for T in cand:
        acc = sum(1 for x in vals if (x[0] >= T) == (x[1] == "DIFFERENT")) / len(vals)
        if acc > best[0]: best = (acc, T)
    accs = {}
    for T in cand:
        if abs(T - best[1]) <= 15:
            accs[T] = sum(1 for x in vals if (x[0] >= T) == (x[1] == "DIFFERENT")) / len(vals)
    lo = min(accs.values()); hi = max(accs.values())
    print("variant %s emin=%d darkex=%s:" % (name, emin, darkex))
    print("  SAME: min=%d p10=%d med=%d p90=%d max=%d" %
          (s[0], s[len(s)//10], s[len(s)//2], s[9*len(s)//10], s[-1]))
    print("  DIFF: min=%d p10=%d med=%d p90=%d max=%d" %
          (d[0], d[len(d)//10], d[len(d)//2], d[9*len(d)//10], d[-1]))
    print("  best acc=%.2f%% at T=%d; acc in [T-15,T+15]: %.2f%%..%.2f%%" %
          (100*best[0], best[1], 100*lo, 100*hi))
    bad = sorted(((x[0], os.path.basename(p)) for (p, t), x in zip(data, vals)
                  if t == "SAME_SURFACE"), reverse=True)[:3]
    print("  worst SAME:", bad)
    sys.stdout.flush()
