#!/usr/bin/env python3
"""FS-F2C Phase 0g — RATIO-DISPERSION formation statistic (white-box design).

Generative truth: SAME_SURFACE = same crop under two illuminants that are
DIAGONAL IN LINEAR RGB (exact Bradford chain). Therefore, in linear space,
  viewB_lin(i) / viewA_lin(i) = gainB/gainA  (constant across pixels)
up to noise/clipping — REGARDLESS of the illuminant values. No illuminant
estimation (no gray-world assumption) is needed: the test is "are the two
views related by a global per-channel gain?".

Statistic (integer-exact):
  kept pixel for channel c: max raw byte < 250 (both views), linA_c >= L_MIN,
      linB_c >= L_MIN   (L_MIN in linear x10000)
  r(i) = linB_c(i)*1000 // linA_c(i)
  S1 = sum r, S2 = sum r*r, n = count  (per channel)
  CV2_c = (S2*n - S1*S1) * 10^6 // max(S1*S1, 1)   (0 if n < 64)
  d_ratio = CV2_r + CV2_g + CV2_b
  DIFFERENT iff d_ratio >= T.

SAME_SURFACE -> ratio field constant -> d_ratio ~ noise floor.
DIFFERENT    -> ratio field varies with the two surfaces -> d_ratio large.
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

def d_ratio(path, lmin):
    img = load(path); n = len(img) // 6
    tot = 0
    for c in range(3):
        s1 = 0; s2 = 0; cnt = 0
        for i in range(n):
            ra = img[3*i+c]; rb = img[6912+3*i+c]
            if ra >= 250 or rb >= 250:
                continue
            la = LUT[ra]; lb = LUT[rb]
            if la < lmin or lb < lmin:
                continue
            r = lb * 1000 // la
            s1 += r; s2 += r * r; cnt += 1
        if cnt < 64:
            continue
        var_num = s2 * cnt - s1 * s1
        if var_num < 0: var_num = 0
        den = s1 * s1
        if den < 1: den = 1
        tot += var_num * 1000000 // den
    return tot

def truth_of(path):
    t = open(path + ".truth").read().strip()
    return t[6:] if t.startswith("truth=") else t

data = []
for line in open(TSV):
    p = line.rstrip("\n").split("\t")
    path = os.path.normpath(os.path.join(FIX, p[0]))
    data.append((path, truth_of(path)))

for lmin in (50, 100, 200):
    vals = [(d_ratio(p, lmin), t) for (p, t) in data]
    s = sorted(x[0] for x in vals if x[1] == "SAME_SURFACE")
    d = sorted(x[0] for x in vals if x[1] == "DIFFERENT")
    cand = sorted(set(x[0] for x in vals))
    best = (0, 0)
    for T in cand:
        a = sum(1 for x in vals if (x[0] >= T) == (x[1] == "DIFFERENT")) / len(vals)
        if a > best[0]: best = (a, T)
    accs = [sum(1 for x in vals if (x[0] >= T) == (x[1] == "DIFFERENT")) / len(vals)
            for T in cand if abs(T - best[1]) <= max(15, best[1] // 10)]
    print("RATIO lmin=%d:" % lmin)
    print("  SAME: min=%d p10=%d med=%d p90=%d max=%d" %
          (s[0], s[len(s)//10], s[len(s)//2], s[9*len(s)//10], s[-1]))
    print("  DIFF: min=%d p10=%d med=%d p90=%d max=%d" %
          (d[0], d[len(d)//10], d[len(d)//2], d[9*len(d)//10], d[-1]))
    print("  best acc=%.2f%% at T=%d; flat range %.2f%%..%.2f%%" %
          (100*best[0], best[1], 100*min(accs), 100*max(accs)))
    bad = sorted(((x[0], os.path.basename(p)) for (p, t), x in zip(data, vals)
                  if t == "SAME_SURFACE"), reverse=True)[:3]
    print("  worst SAME:", bad)
    miss = sorted(((x[0], os.path.basename(p)) for (p, t), x in zip(data, vals)
                   if t == "DIFFERENT"), )[:3]
    print("  worst DIFF misses:", miss)
    sys.stdout.flush()
