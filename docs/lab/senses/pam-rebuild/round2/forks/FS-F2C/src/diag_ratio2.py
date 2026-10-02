#!/usr/bin/env python3
"""FS-F2C Phase 0h — finalize the RATIO-DISPERSION rule.

1. Exact flat-threshold region for lmin=100 (min/max T with max accuracy).
2. Full error list at the chosen T (both directions) with per-fixture diagnostics.
3. Hybrid check: frozen rule's verdict on the ratio rule's errors
   (informs whether a degenerate-fallback is worth the complexity).
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

def d_ratio(path, lmin=100):
    img = load(path); n = len(img) // 6
    tot = 0
    kept = []
    for c in range(3):
        s1 = 0; s2 = 0; cnt = 0
        for i in range(n):
            ra = img[3*i+c]; rb = img[6912+3*i+c]
            if ra >= 250 or rb >= 250: continue
            la = LUT[ra]; lb = LUT[rb]
            if la < lmin or lb < lmin: continue
            r = lb * 1000 // la
            s1 += r; s2 += r*r; cnt += 1
        kept.append(cnt)
        if cnt < 64: continue
        var_num = s2*cnt - s1*s1
        if var_num < 0: var_num = 0
        den = s1*s1 if s1*s1 >= 1 else 1
        tot += var_num * 1000000 // den
    return tot, kept

def frozen_d(img):
    n = len(img) // 6
    ar=ag=ab=br=bg=bb=0
    for i in range(n):
        ar+=img[3*i]; ag+=img[3*i+1]; ab+=img[3*i+2]
        br+=img[6912+3*i]; bg+=img[6912+3*i+1]; bb+=img[6912+3*i+2]
    ta=max(ar+ag+ab,1); tc=max(br+bg+bb,1)
    return (abs(ar*1000//ta-br*1000//tc)+abs(ag*1000//ta-bg*1000//tc)
            +abs(ab*1000//ta-bb*1000//tc))

def truth_of(path):
    t = open(path+".truth").read().strip()
    return t[6:] if t.startswith("truth=") else t

data = []
for line in open(TSV):
    p = line.rstrip("\n").split("\t")
    path = os.path.normpath(os.path.join(FIX, p[0]))
    data.append((path, truth_of(path)))

vals = []
for (path, truth) in data:
    d, kept = d_ratio(path)
    vals.append((d, truth, path, kept))

# flat region: all T achieving max accuracy
cand = sorted(set(v[0] for v in vals))
scored = []
for T in cand:
    a = sum(1 for v in vals if (v[0] >= T) == (v[1] == "DIFFERENT")) / len(vals)
    scored.append((a, T))
mx = max(a for a, _ in scored)
flat = [T for a, T in scored if a == mx]
print("max acc=%.4f%% flat T in [%d, %d] (%d distinct T values)" %
      (100*mx, flat[0], flat[-1], len(flat)))
# nearest fixture d values around the flat region
below = sorted(v[0] for v in vals if v[0] < flat[0])[-3:]
above = sorted(v[0] for v in vals if v[0] > flat[-1])[:3]
print("nearest d below flat region:", below)
print("nearest d above flat region:", above)

T = 150000  # round candidate inside the flat region?
ok = flat[0] <= 150000 <= flat[-1]
print("T=150000 inside flat region:", ok)
if not ok:
    # pick midpoint of flat region, rounded
    T = (flat[0] + flat[-1]) // 2
    print("using T=%d (midpoint)" % T)

errs = [(v[0], v[1], v[2], v[3]) for v in vals
        if (v[0] >= T) != (v[1] == "DIFFERENT")]
print("errors at T=%d: %d/720 (acc=%.2f%%)" % (T, len(errs), 100*(1-len(errs)/720)))
for d, truth, path, kept in sorted(errs):
    img = load(path)
    df = frozen_d(img)
    fn = os.path.basename(path)
    print("  %s d=%d kept=%s truth=%s frozen_d=%d frozen_judg=%s" %
          (fn, d, kept, truth, df,
           "DIFFERENT" if df >= 80 else "SAME_SURFACE"))
