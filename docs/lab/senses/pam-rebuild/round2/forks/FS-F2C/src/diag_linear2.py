#!/usr/bin/env python3
"""FS-F2C Phase 0d — channel-gated linear von Kries variants.

Adds CHANNEL GATING: a channel is active iff BOTH views' linear means >= E_MIN.
Degenerate channels (e.g. ~zero blue in a red crop, fixture 331) carry only
noise and are excluded from the comparison; chromaticity renormalizes over
active channels only. Plus clipped-pixel exclusion (>=250 in either view).

Variants (all integer-mirrorable):
  LCg: mean_i L1(chroma_active(qA_i), chroma_active(qB_i))
  LAg: L1(mean chroma_active A, mean chroma_active B)
  QCg: mean_i sum_{c active} |qA_c(i)-qB_c(i)| // 10   (normalized-linear, /10
       to keep the statistic in a chromaticity-like range)

E_MIN scanned in linear x10000 units.
"""
import struct, os

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

def prep(img):
    n = len(img) // 6
    A = []; B = []
    ea = [0, 0, 0]; eb = [0, 0, 0]
    for i in range(n):
        pa = [LUT[img[3*i+c]] for c in range(3)]
        pb = [LUT[img[6912+3*i+c]] for c in range(3)]
        ra = [img[3*i+c] for c in range(3)]
        rb = [img[6912+3*i+c] for c in range(3)]
        A.append((pa, ra)); B.append((pb, rb))
        for c in range(3):
            ea[c] += pa[c]; eb[c] += pb[c]
    ea = [max(e // n, 1) for e in ea]; eb = [max(e // n, 1) for e in eb]
    return A, B, ea, eb, n

def variant(path, which, emin):
    img = load(path)
    A, B, ea, eb, n = prep(img)
    act = [c for c in range(3) if ea[c] >= emin and eb[c] >= emin]
    if not act:
        act = [c for c in range(3) if ea[c] + eb[c] == max(ea[c] + eb[c] for c in range(3))]
        # fallback: single strongest channel
        act = [max(range(3), key=lambda c: ea[c] + eb[c])]
    qa = []; qb = []
    for i in range(n):
        (pa, ra), (pb, rb) = A[i], B[i]
        if max(ra) >= 250 or max(rb) >= 250:
            continue
        qa.append(tuple(pa[c] * 10000 // ea[c] for c in act))
        qb.append(tuple(pb[c] * 10000 // eb[c] for c in act))
    if not qa:
        return 0
    m = len(qa); K = len(act)
    def chroma(q):
        s = sum(q)
        if s < 1: s = 1
        return tuple(v * 1000 // s for v in q)
    if which == "LCg":
        tot = 0
        for a, b in zip(qa, qb):
            ca, cb = chroma(a), chroma(b)
            tot += sum(abs(x - y) for x, y in zip(ca, cb))
        return tot // m
    if which == "LAg":
        sa = [0]*K; sb = [0]*K
        for a, b in zip(qa, qb):
            ca, cb = chroma(a), chroma(b)
            for k in range(K):
                sa[k] += ca[k]; sb[k] += cb[k]
        return sum(abs(sa[k]//m - sb[k]//m) for k in range(K))
    # QCg
    tot = 0
    for a, b in zip(qa, qb):
        tot += sum(abs(x - y) for x, y in zip(a, b))
    return tot // m // 10

def truth_of(path):
    t = open(path + ".truth").read().strip()
    return t[6:] if t.startswith("truth=") else t

data = []
for line in open(TSV):
    p = line.rstrip("\n").split("\t")
    path = os.path.normpath(os.path.join(FIX, p[0]))
    data.append((path, truth_of(path)))

import sys
which = sys.argv[1] if len(sys.argv) > 1 else "LCg"
for emin in (100, 200, 400):
    vals = [(variant(p, which, emin), t) for (p, t) in data]
    s = sorted(x[0] for x in vals if x[1] == "SAME_SURFACE")
    d = sorted(x[0] for x in vals if x[1] == "DIFFERENT")
    cand = sorted(set(x[0] for x in vals))
    best = (0, 0)
    for T in cand:
        acc = sum(1 for x in vals if (x[0] >= T) == (x[1] == "DIFFERENT")) / len(vals)
        if acc > best[0]: best = (acc, T)
    print("variant %s emin=%d:" % (which, emin))
    print("  SAME: min=%d p10=%d med=%d p90=%d max=%d" %
          (s[0], s[len(s)//10], s[len(s)//2], s[9*len(s)//10], s[-1]))
    print("  DIFF: min=%d p10=%d med=%d p90=%d max=%d" %
          (d[0], d[len(d)//10], d[len(d)//2], d[9*len(d)//10], d[-1]))
    print("  best acc=%.2f%% at T=%d" % (100*best[0], best[1]))
