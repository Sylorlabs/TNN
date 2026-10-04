#!/usr/bin/env python3
"""FS-F2C Phase 0b — compare principled illuminant-discounted formation variants.

All variants: per-view gray-world von Kries (q = pix*1000/viewmean, integer),
then a NON-mean-based statistic (mean-based stats degenerate under any
per-view mean-matching normalization). Variants:

  A: d = L1( mean_i chroma(qA_i), mean_i chroma(qB_i) )            [signature]
  C: d = mean_i L1( chroma(qA_i), chroma(qB_i) )                   [disagreement]
  Ax: A with dark-pixel exclusion (s_i = qr+qg+qb < 900 excluded)
  Cx: C with dark-pixel exclusion

chroma in x1000 units (cr+cq+cb = 1000 per pixel by construction).
Reports separation quality on the 720 r2n colorconst controls and the
max-accuracy threshold per variant (diagnostic: threshold frozen in prereg,
bars measured on a FRESH draw).
"""
import struct, os

FIX = os.path.expanduser("~/workspace/tnn-lab/senses/pam-rebuild/round2/forks/FS-E2")
TSV = os.path.expanduser("~/workspace/tnn-lab/senses/pam-rebuild/round2/forks/FS-E2/evidence/phase0/form_r2n_colorconst.tsv")

def load(path):
    b = open(path, "rb").read()
    magic, task, idx, family, fo, fl, go, gl = struct.unpack("<8I", b[:32])
    return b[fo:fo + fl]

def norm_view(img, off, n):
    """returns list of (qr,qg,qb) von Kries-normalized pixels, integer math."""
    sr = sg = sb = 0
    px = []
    for i in range(n):
        r, g, b = img[off + 3 * i], img[off + 3 * i + 1], img[off + 3 * i + 2]
        px.append((r, g, b)); sr += r; sg += g; sb += b
    er, eg, eb = max(sr // n, 1), max(sg // n, 1), max(sb // n, 1)
    out = []
    for (r, g, b) in px:
        qr, qg, qb = r * 1000 // er, g * 1000 // eg, b * 1000 // eb
        out.append((qr, qg, qb))
    return out

def chroma(q):
    s = q[0] + q[1] + q[2]
    if s < 1: s = 1
    return (q[0] * 1000 // s, q[1] * 1000 // s, q[2] * 1000 // s)

def variant(path, which):
    img = load(path); n = len(img) // 6
    A = norm_view(img, 0, n); B = norm_view(img, 6912, n)
    dark = 900  # normalized-unit brightness floor (mean bright pixel s ~= 3000)
    if which in ("A", "Ax"):
        sr = sg = sb = tr = tg = tb = 0; cnt = 0
        for i in range(n):
            qa, qb = A[i], B[i]
            if which == "Ax" and (qa[0]+qa[1]+qa[2] < dark or qb[0]+qb[1]+qb[2] < dark):
                continue
            ca, cb = chroma(qa), chroma(qb)
            sr += ca[0]; sg += ca[1]; sb += ca[2]
            tr += cb[0]; tg += cb[1]; tb += cb[2]
            cnt += 1
        if cnt < 1: cnt = 1
        return (abs(sr // cnt - tr // cnt) + abs(sg // cnt - tg // cnt)
                + abs(sb // cnt - tb // cnt))
    # C / Cx
    tot = 0; cnt = 0
    for i in range(n):
        qa, qb = A[i], B[i]
        if which == "Cx" and (qa[0]+qa[1]+qa[2] < dark or qb[0]+qb[1]+qb[2] < dark):
            continue
        ca, cb = chroma(qa), chroma(qb)
        tot += abs(ca[0]-cb[0]) + abs(ca[1]-cb[1]) + abs(ca[2]-cb[2])
        cnt += 1
    if cnt < 1: cnt = 1
    return tot // cnt

def truth_of(path):
    t = open(path + ".truth").read().strip()
    return t[6:] if t.startswith("truth=") else t

data = []
for line in open(TSV):
    p = line.rstrip("\n").split("\t")
    path = os.path.normpath(os.path.join(FIX, p[0]))
    data.append((path, truth_of(path)))

print("computing variants (slow, pure python)...")
vals = {v: [] for v in ("A", "C", "Ax", "Cx")}
for k, (path, truth) in enumerate(data):
    for v in vals:
        vals[v].append((variant(path, v), truth))
    if k % 120 == 119:
        print("  %d/720" % (k + 1), flush=True)

for v in ("A", "C", "Ax", "Cx"):
    s = sorted(x[0] for x in vals[v] if x[1] == "SAME_SURFACE")
    d = sorted(x[0] for x in vals[v] if x[1] == "DIFFERENT")
    # best threshold by accuracy on this set (diagnostic)
    cand = sorted(set(x[0] for x in vals[v]))
    best = (0, 0)
    for t in cand:
        acc = (sum(1 for x in vals[v] if (x[0] >= t) == (x[1] == "DIFFERENT"))
               / len(vals[v]))
        if acc > best[0]:
            best = (acc, t)
    print("variant %s:" % v)
    print("  SAME_SURFACE: n=%d min=%d p10=%d med=%d p90=%d max=%d" %
          (len(s), s[0], s[len(s)//10], s[len(s)//2], s[9*len(s)//10], s[-1]))
    print("  DIFFERENT:    n=%d min=%d p10=%d med=%d p90=%d max=%d" %
          (len(d), d[0], d[len(d)//10], d[len(d)//2], d[9*len(d)//10], d[-1]))
    print("  best-threshold acc=%.2f%% at T=%d" % (100 * best[0], best[1]))
    # worst SAME_SURFACE offenders
    bad = sorted(((x[0], p) for (p, t), x in
                  zip(data, vals[v]) if t == "SAME_SURFACE"), reverse=True)[:5]
    print("  worst SAME_SURFACE d values:", [b[0] for b in bad])
