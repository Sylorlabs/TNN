#!/usr/bin/env python3
"""FS-F2C Phase 0 — white-box diagnosis of colorconst formation errors.

Reads FS-E2's committed Phase-0 TSV (form_r2n_colorconst.tsv, byte-identical x2,
2000/2000 cross-checked vs FS-E1's frozen ledger) as the judgment baseline,
recomputes the frozen formation statistic d (L1 x1000 mean-chromaticity distance)
in Python to verify the implementation matches (expect 720/720 judgment
agreement), then decomposes every error into white-box error modes:

  E1 illuminant-shift false-DIFFERENT: truth SAME_SURFACE, judgment DIFFERENT
  E2 missed real difference:          truth DIFFERENT,   judgment SAME_SURFACE
  E3 borderline (noise-suspect):       |d - 80| <= 20  (either direction)
  E4 extreme-d miss:                   |d - 80| > 150 on the wrong side

Also reports the d65 implication: SAME_SURFACE error rate vs estimated
illuminant shift magnitude between the two views (diagnostic only;
FS-E1b owns the CH-CCN-3 challenge-quantity repair, formation only here).

Analysis only — no decisions, no fixes. All formation decisions stay in Zag.
"""
import struct, math, os

FIX = os.path.expanduser("~/workspace/tnn-lab/senses/pam-rebuild/round2/forks/FS-E2")
TSV = os.path.expanduser("~/workspace/tnn-lab/senses/pam-rebuild/round2/forks/FS-E2/evidence/phase0/form_r2n_colorconst.tsv")

def hdr(path):
    b = open(path, "rb").read(32)
    magic, task, idx, family, fo, fl, go, gl = struct.unpack("<8I", b)
    return fo, fl

def stats(path):
    """frozen formation statistic + auxiliaries, pure mirror of f_colorconst.
    Layout: viewA = img[0:6912], viewB = img[6912:13824] (48x48x3 each)."""
    fo, fl = hdr(path)
    raw = open(path, "rb").read()
    img = raw[fo:fo + fl]
    n = len(img) // 6          # pixels per view
    assert len(img) == 13824 and n == 2304
    ar = ag = ab = br = bg = bb = 0
    for i in range(n):
        ar += img[3 * i];         ag += img[3 * i + 1];     ab += img[3 * i + 2]
        br += img[6912 + 3 * i];  bg += img[6912 + 3 * i + 1]; bb += img[6912 + 3 * i + 2]
    ta = ar + ag + ab; tc = br + bg + bb
    if ta < 1: ta = 1
    if tc < 1: tc = 1
    d = (abs(ar * 1000 // ta - br * 1000 // tc)
         + abs(ag * 1000 // ta - bg * 1000 // tc)
         + abs(ab * 1000 // ta - bb * 1000 // tc))
    judg = "DIFFERENT" if d >= 80 else "SAME_SURFACE"
    mA = (ar / n, ag / n, ab / n); mB = (br / n, bg / n, bb / n)
    return d, judg, mA, mB, n

def truth_of(path):
    t = open(path + ".truth").read().strip()
    return t[6:] if t.startswith("truth=") else t

rows = []
agree = 0
for line in open(TSV):
    p = line.rstrip("\n").split("\t")
    rel, task, judg, truth, correct = p[0], p[1], p[2], p[3], int(p[4])
    path = os.path.normpath(os.path.join(FIX, rel))
    d, myjudg, mA, mB, n = stats(path)
    mytruth = truth_of(path)
    assert mytruth == truth, (path, mytruth, truth)
    if myjudg == judg:
        agree += 1
    else:
        print("MISMATCH vs committed TSV:", path, myjudg, judg)
    rows.append(dict(path=path, truth=truth, judg=judg, d=d, mA=mA, mB=mB, n=n))

print("recomputed-vs-committed-TSV judgment agreement: %d/%d" % (agree, len(rows)))

# ---------- error-mode categorization ----------
E1 = [r for r in rows if r["truth"] == "SAME_SURFACE" and r["judg"] == "DIFFERENT"]
E2 = [r for r in rows if r["truth"] == "DIFFERENT" and r["judg"] == "SAME_SURFACE"]
print("total=%d correct=%d acc=%.2f%%" % (len(rows),
      sum(1 for r in rows if r["truth"] == r["judg"]),
      100.0 * sum(1 for r in rows if r["truth"] == r["judg"]) / len(rows)))
print("E1 illuminant-shift false-DIFFERENT (SAME_SURFACE judged DIFFERENT): %d" % len(E1))
print("E2 missed real difference (DIFFERENT judged SAME_SURFACE):            %d" % len(E2))
print("truth base rates: SAME_SURFACE=%d DIFFERENT=%d" %
      (sum(1 for r in rows if r["truth"] == "SAME_SURFACE"),
       sum(1 for r in rows if r["truth"] == "DIFFERENT")))

def margin_hist(errs, name):
    print("--- %s: |d-80| margins ---" % name)
    bins = {"borderline<=20": 0, "20-60": 0, "60-150": 0, ">150": 0}
    for r in errs:
        m = abs(r["d"] - 80)
        if m <= 20: bins["borderline<=20"] += 1
        elif m <= 60: bins["20-60"] += 1
        elif m <= 150: bins["60-150"] += 1
        else: bins[">150"] += 1
    for k, v in bins.items():
        print("   %s: %d" % (k, v))

margin_hist(E1, "E1")
margin_hist(E2, "E2")

# ---------- d65 / illuminant implication ----------
# Estimate per-view illuminant-shift signature: channel ratio mB/mA.
# Illuminant-shifted SAME_SURFACE: ratios spread across channels (e.g. warm:
# R up, B down); exposure-only: ratios ~equal across channels.
def ratio_spread(r):
    mA, mB = r["mA"], r["mB"]
    rat = [ (mB[c] + 1) / (mA[c] + 1) for c in range(3) ]
    return max(rat) / min(rat)

print("--- E1: channel-ratio spread (illuminant signature) ---")
sp = sorted(ratio_spread(r) for r in E1)
print("   n=%d min=%.3f p25=%.3f median=%.3f p75=%.3f max=%.3f" %
      (len(sp), sp[0], sp[len(sp)//4], sp[len(sp)//2], sp[3*len(sp)//4], sp[-1]))
print("   spread>1.25 (clear illuminant shift): %d/%d" %
      (sum(1 for r in E1 if ratio_spread(r) > 1.25), len(E1)))

# For E1, check: is the chromaticity shift direction consistent with warm/cool
# d65-relative shifts? mean chromaticity delta sign pattern.
print("--- E1: mean-chromaticity delta sign patterns (r,g,b) x1000 ---")
from collections import Counter
pat = Counter()
for r in rows:
    if r["truth"] != "SAME_SURFACE" or r["judg"] != "DIFFERENT":
        continue
    mA, mB = r["mA"], r["mB"]
    sA, sB = sum(mA), sum(mB)
    dc = tuple(1 if (mB[c]/sB - mA[c]/sA) * 1000 > 0 else -1 for c in range(3))
    pat[dc] += 1
for k, v in pat.most_common():
    print("   %s: %d" % (k, v))

# E2: how sub-threshold are the misses? d distribution
print("--- E2: d distribution ---")
ds = sorted(r["d"] for r in E2)
if ds:
    print("   n=%d min=%d p25=%d median=%d max=%d" %
          (len(ds), ds[0], ds[len(ds)//4], ds[len(ds)//2], ds[-1]))
# E2 illuminant-masking: do the missed DIFFERENT pairs show big illuminant
# shift that could have masked a real surface difference?
print("   E2 with spread>1.25 (illuminant-masked misses): %d/%d" %
      (sum(1 for r in E2 if ratio_spread(r) > 1.25), len(E2)))

# ---------- von Kries preview (DIAGNOSTIC ONLY, Python mirror) ----------
# Per-view gray-world: q = pix*1000/mean; surface chroma = mean_i chroma(q_i);
# d_vk = L1 x1000 of surface-chroma vectors. Computed here only to size the
# improvement; the frozen rule is what the prereg bars measure against.
def vonkries(path):
    fo, fl = hdr(path)
    raw = open(path, "rb").read()
    img = raw[fo:fo + fl]
    n = len(img) // 6
    def view(off):
        sr = sg = sb = 0
        px = []
        for i in range(n):
            r, g, b = img[off + 3*i], img[off + 3*i+1], img[off + 3*i+2]
            px.append((r, g, b)); sr += r; sg += g; sb += b
        er, eg, eb = max(sr // n, 1), max(sg // n, 1), max(sb // n, 1)
        cr = cg = cb = 0
        for (r, g, b) in px:
            qr, qg, qb = r * 1000 // er, g * 1000 // eg, b * 1000 // eb
            s = qr + qg + qb
            if s < 1: s = 1
            cr += qr * 1000 // s; cg += qg * 1000 // s; cb += qb * 1000 // s
        return (cr // n, cg // n, cb // n)
    hA, hB = view(0), view(6912)
    return abs(hA[0]-hB[0]) + abs(hA[1]-hB[1]) + abs(hA[2]-hB[2])

print("--- von Kries diagnostic d_vk distribution (preview only) ---")
for grp, name in [([r for r in rows if r["truth"]=="SAME_SURFACE"], "SAME_SURFACE"),
                  ([r for r in rows if r["truth"]=="DIFFERENT"], "DIFFERENT")]:
    dvs = sorted(vonkries(r["path"]) for r in grp)
    print("   %s: n=%d min=%d p10=%d median=%d p90=%d max=%d" %
          (name, len(dvs), dvs[0], dvs[len(dvs)//10], dvs[len(dvs)//2],
           dvs[9*len(dvs)//10], dvs[-1]))
