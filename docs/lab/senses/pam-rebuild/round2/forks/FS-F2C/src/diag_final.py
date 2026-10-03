#!/usr/bin/env python3
"""FS-F2C Phase 0i — FINAL integer spec calibration (bit-exact Zag mirror).

FINAL RULE (frozen for the prereg):
  per channel c in {0,1,2}:
    S1=S2=n=0
    for each pixel i in 0..2303:
      ra = viewA[3i+c]; rb = viewB[3i+c]          (bytes)
      if ra >= 250 or rb >= 250: continue          (clip exclusion)
      la = LUT[ra]; lb = LUT[rb]                   (linear x10000)
      if la < 100 or lb < 100: continue            (L_MIN dark/noise gate)
      r = lb*1000 // la                            (0 <= r <= 100000)
      S1 += r; S2 += r*r; n += 1
    if n < 64: contrib = 0
    else:
      num = S2*n - S1*S1; if num < 0: num = 0
      den = S1*S1;        if den < 1: den = 1
      contrib = num*300 // den                     (proven: num<=2.654e16,
                                                   num*300<=7.96e18 < 2^63-1)
  d = contrib_r + contrib_g + contrib_b
  DIFFERENT iff d >= T.

Overflow proof: lb<=10000 -> lb*1000<=1e7; la>=100 -> r<=100000; r*r<=1e10;
S1<=2304*1e5=2.304e8 -> S1*S1<=5.31e16; S2<=2304*1e10=2.304e13;
S2*n<=5.31e16; num=1/2*sum (r_i-r_j)^2 <= 2.654e16; num*300<=7.96e18<9.223e18.

Calibrates T on the 720 r2n controls; reports the max-accuracy T band.
"""
import struct, os

FIX = os.path.expanduser("~/workspace/tnn-lab/senses/pam-rebuild/round2/forks/FS-E2")
TSV = os.path.expanduser("~/workspace/tnn-lab/senses/pam-rebuild/round2/forks/FS-E2/evidence/phase0/form_r2n_colorconst.tsv")

LUT = []
for c in range(256):
    x = c / 255.0
    lin = x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4
    LUT.append(int(round(lin * 10000)))
assert max(LUT) == 10000 and LUT[0] == 0

def load(path):
    b = open(path, "rb").read()
    magic, task, idx, family, fo, fl, go, gl = struct.unpack("<8I", b[:32])
    assert fl == 13824
    return b[fo:fo+fl]

def final_d(img):
    n = len(img) // 6
    d = 0
    for c in range(3):
        s1 = 0; s2 = 0; cnt = 0
        for i in range(n):
            ra = img[3*i+c]; rb = img[6912+3*i+c]
            if ra >= 250 or rb >= 250: continue
            la = LUT[ra]; lb = LUT[rb]
            if la < 100 or lb < 100: continue
            r = lb*1000 // la
            assert 0 <= r <= 100000
            s1 += r; s2 += r*r; cnt += 1
        if cnt < 64: continue
        num = s2*cnt - s1*s1
        if num < 0: num = 0
        assert num*300 < 9223372036854775807, num
        den = s1*s1
        if den < 1: den = 1
        d += num*300 // den
    return d

def truth_of(path):
    t = open(path+".truth").read().strip()
    return t[6:] if t.startswith("truth=") else t

data = []
for line in open(TSV):
    p = line.rstrip("\n").split("\t")
    path = os.path.normpath(os.path.join(FIX, p[0]))
    data.append((path, truth_of(path)))

print("computing final-spec d on 720 fixtures...")
vals = [(final_d(load(p)), t, p) for (p, t) in data]
print("done.")
s = sorted(v[0] for v in vals if v[1] == "SAME_SURFACE")
d = sorted(v[0] for v in vals if v[1] == "DIFFERENT")
print("SAME: n=%d min=%d p10=%d med=%d p90=%d max=%d" %
      (len(s), s[0], s[len(s)//10], s[len(s)//2], s[9*len(s)//10], s[-1]))
print("DIFF: n=%d min=%d p10=%d med=%d p90=%d max=%d" %
      (len(d), d[0], d[len(d)//10], d[len(d)//2], d[9*len(d)//10], d[-1]))
cand = sorted(set(v[0] for v in vals))
scored = []
for T in cand:
    a = sum(1 for v in vals if (v[0] >= T) == (v[1] == "DIFFERENT")) / len(vals)
    scored.append((a, T))
mx = max(a for a, _ in scored)
band = [T for a, T in scored if a == mx]
print("max acc=%.4f%%; T band for max acc: [%d, %d]" % (100*mx, band[0], band[-1]))
# check a few round T candidates inside the band
for Tcand in (40, 45, 50):
    if band[0] <= Tcand <= band[-1]:
        print("  T=%d in band -> acc=%.4f%%" % (Tcand, 100*mx))
# errors at T=45 (if in band)
T = 45
if band[0] <= T <= band[-1]:
    errs = [(v[0], v[1], os.path.basename(v[2])) for v in vals
            if (v[0] >= T) != (v[1] == "DIFFERENT")]
    print("errors at T=%d: %d -> acc=%.2f%%" % (T, len(errs), 100*(1-len(errs)/720)))
    for e in sorted(errs): print("   d=%d truth=%s %s" % e)
# persist d values for the Zag cross-check
with open(os.path.expanduser("~/workspace/tnn-lab/senses/pam-rebuild/round2/forks/FS-F2C/evidence/diag/final_d_720.tsv"), "w") as fh:
    for v in vals:
        fh.write("%s\t%d\t%s\n" % (os.path.basename(v[2]), v[0], v[1]))
print("wrote evidence/diag/final_d_720.tsv")
