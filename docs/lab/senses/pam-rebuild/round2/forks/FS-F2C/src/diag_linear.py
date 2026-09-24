#!/usr/bin/env python3
"""FS-F2C Phase 0c — linear-space von Kries diagnosis.

The generator applies the illuminant DIAGONALLY IN LINEAR RGB (exact Bradford
chain) with clipping at 1.0, then gamma-encodes to sRGB. Gray-world in sRGB
space is therefore a crude approximation. This diagnostic mirrors a
linear-space pipeline:

  LUT: sRGB byte -> linear x10000 (integer, exact inverse of the generator's
       gamma: c<=0.04045 -> c/12.92 else ((c+0.055)/1.055)^2.4, x10000)
  per view: e = mean linear per channel (gray-world in linear)
  q(i) = pix_lin(i) * 10000 // e   (von Kries in linear)
  clip exclusion: skip pixels with any raw channel >= 250 in either view
                  (clipped pixels carry no surface information)
  variants:
    L_C:  d = mean_i L1(chroma(qA_i), chroma(qB_i)) over kept pixels
    L_A:  d = L1(mean kept chroma A, mean kept chroma B)

Reports separation + best-threshold accuracy on the 720 r2n colorconst controls.
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

def lin_view(img, off, n):
    px = []
    sr = sg = sb = 0
    for i in range(n):
        r, g, b = img[off + 3*i], img[off + 3*i+1], img[off + 3*i+2]
        lr, lg, lb = LUT[r], LUT[g], LUT[b]
        px.append((lr, lg, lb, r, g, b))
        sr += lr; sg += lg; sb += lb
    er, eg, eb = max(sr // n, 1), max(sg // n, 1), max(sb // n, 1)
    q = []
    for (lr, lg, lb, r, g, b) in px:
        q.append((lr * 10000 // er, lg * 10000 // eg, lb * 10000 // eb, r, g, b))
    return q

def chroma(q):
    s = q[0] + q[1] + q[2]
    if s < 1: s = 1
    return (q[0]*1000//s, q[1]*1000//s, q[2]*1000//s)

def variant(path, which, clipthr=250):
    img = load(path); n = len(img) // 6
    A = lin_view(img, 0, n); B = lin_view(img, 6912, n)
    def clipped(q): return q[3] >= clipthr or q[4] >= clipthr or q[5] >= clipthr
    idx = [i for i in range(n) if not clipped(A[i]) and not clipped(B[i])]
    if not idx: idx = list(range(n))
    if which == "L_C":
        tot = 0
        for i in idx:
            ca, cb = chroma(A[i]), chroma(B[i])
            tot += abs(ca[0]-cb[0]) + abs(ca[1]-cb[1]) + abs(ca[2]-cb[2])
        return tot // len(idx)
    sr = sg = sb = tr = tg = tb = 0
    for i in idx:
        ca, cb = chroma(A[i]), chroma(B[i])
        sr += ca[0]; sg += ca[1]; sb += ca[2]
        tr += cb[0]; tg += cb[1]; tb += cb[2]
    m = len(idx)
    return abs(sr//m - tr//m) + abs(sg//m - tg//m) + abs(sb//m - tb//m)

def truth_of(path):
    t = open(path + ".truth").read().strip()
    return t[6:] if t.startswith("truth=") else t

data = []
for line in open(TSV):
    p = line.rstrip("\n").split("\t")
    path = os.path.normpath(os.path.join(FIX, p[0]))
    data.append((path, truth_of(path)))

for v in ("L_C", "L_A"):
    vals = [(variant(p, v), t) for (p, t) in data]
    s = sorted(x[0] for x in vals if x[1] == "SAME_SURFACE")
    d = sorted(x[0] for x in vals if x[1] == "DIFFERENT")
    cand = sorted(set(x[0] for x in vals))
    best = (0, 0)
    for T in cand:
        acc = sum(1 for x in vals if (x[0] >= T) == (x[1] == "DIFFERENT")) / len(vals)
        if acc > best[0]: best = (acc, T)
    print("variant %s:" % v)
    print("  SAME_SURFACE: n=%d min=%d p10=%d med=%d p90=%d max=%d" %
          (len(s), s[0], s[len(s)//10], s[len(s)//2], s[9*len(s)//10], s[-1]))
    print("  DIFFERENT:    n=%d min=%d p10=%d med=%d p90=%d max=%d" %
          (len(d), d[0], d[len(d)//10], d[len(d)//2], d[9*len(d)//10], d[-1]))
    print("  best-threshold acc=%.2f%% at T=%d" % (100*best[0], best[1]))
    bad = sorted(((x[0], p) for (p, t), x in zip(data, vals) if t == "SAME_SURFACE"),
                 reverse=True)[:5]
    print("  worst SAME_SURFACE:", [(b, os.path.basename(p)) for b, p in bad])
