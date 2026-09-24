#!/usr/bin/env python3
"""FS-F2C Phase 0f — robust variants against degenerate-channel failures.

Tests on the 720 r2n colorconst controls:
 1. LCcap<C>: unfloored L_C with per-pixel L1 contribution capped at C
    (degenerate-channel pixels produce huge per-pixel L1; capping bounds
    their influence without discarding any channel).
 2. HYB: if min over views/channels of linear mean < 30 (degenerate ->
    noise-dominated normalization), fall back to the frozen statistic
    (threshold 80); else L_C (threshold T). Rationale: degenerate-channel
    fixtures are exactly where von Kries is unreliable and where the frozen
    mean-chromaticity rule is safe (no signal to amplify).
 3. LAf30: signature variant L_A with small floor emin=30.

All deterministic, integer-mirrorable.
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

def frozen_d(img):
    n = len(img) // 6
    ar = ag = ab = br = bg = bb = 0
    for i in range(n):
        ar += img[3*i]; ag += img[3*i+1]; ab += img[3*i+2]
        br += img[6912+3*i]; bg += img[6912+3*i+1]; bb += img[6912+3*i+2]
    ta = max(ar+ag+ab, 1); tc = max(br+bg+bb, 1)
    return (abs(ar*1000//ta - br*1000//tc) + abs(ag*1000//ta - bg*1000//tc)
            + abs(ab*1000//ta - bb*1000//tc))

def linprep(img):
    n = len(img) // 6
    ea = [0, 0, 0]; eb = [0, 0, 0]
    for i in range(n):
        for c in range(3):
            ea[c] += LUT[img[3*i+c]]; eb[c] += LUT[img[6912+3*i+c]]
    ea = [max(e // n, 1) for e in ea]; eb = [max(e // n, 1) for e in eb]
    return ea, eb, n

def pix_l1_capped(img, ea, eb, n, cap):
    tot = 0; cnt = 0
    for i in range(n):
        ra = [img[3*i+c] for c in range(3)]; rb = [img[6912+3*i+c] for c in range(3)]
        if max(ra) >= 250 or max(rb) >= 250:
            continue
        sa = sb = 0
        qa = [0, 0, 0]; qb = [0, 0, 0]
        for c in range(3):
            qa[c] = LUT[ra[c]] * 10000 // ea[c]
            qb[c] = LUT[rb[c]] * 10000 // eb[c]
            sa += qa[c]; sb += qb[c]
        sa = max(sa, 1); sb = max(sb, 1)
        pl1 = 0
        for c in range(3):
            pl1 += abs(qa[c]*1000//sa - qb[c]*1000//sb)
        if pl1 > cap: pl1 = cap
        tot += pl1; cnt += 1
    return (tot // cnt) if cnt else 0

def truth_of(path):
    t = open(path + ".truth").read().strip()
    return t[6:] if t.startswith("truth=") else t

data = []
for line in open(TSV):
    p = line.rstrip("\n").split("\t")
    path = os.path.normpath(os.path.join(FIX, p[0]))
    data.append((path, truth_of(path)))

# precompute per-fixture values
pre = []
for k, (path, truth) in enumerate(data):
    img = load(path)
    ea, eb, n = linprep(img)
    dfr = frozen_d(img)
    dcap300 = pix_l1_capped(img, ea, eb, n, 300)
    dcap400 = pix_l1_capped(img, ea, eb, n, 400)
    dcap500 = pix_l1_capped(img, ea, eb, n, 500)
    dnocap = pix_l1_capped(img, ea, eb, n, 10**9)
    degen = min(ea + eb) < 30
    pre.append(dict(truth=truth, dfr=dfr, c300=dcap300, c400=dcap400,
                    c500=dcap500, nocap=dnocap, degen=degen))
    if (k+1) % 180 == 0:
        print("  pre %d/720" % (k+1), flush=True)

def acc_of(vals):
    # vals: list of (d, truth); best threshold accuracy
    cand = sorted(set(v[0] for v in vals))
    best = (0, 0)
    for T in cand:
        a = sum(1 for v in vals if (v[0] >= T) == (v[1] == "DIFFERENT")) / len(vals)
        if a > best[0]: best = (a, T)
    return best

for key, name in (("c300", "LCcap300"), ("c400", "LCcap400"),
                  ("c500", "LCcap500"), ("nocap", "LCnocap")):
    vals = [(p[key], p["truth"]) for p in pre]
    a, T = acc_of(vals)
    print("%s: best acc=%.2f%% at T=%d" % (name, 100*a, T))

# HYB: degenerate -> frozen (thr 80); else L_C nocap (thr T)
# score: correct if (degen and (dfr>=80)==isdiff) or (not degen and (dnocap>=T)==isdiff)
cand = sorted(set(p["nocap"] for p in pre))
best = (0, 0)
for T in cand:
    ok = 0
    for p in pre:
        isdiff = p["truth"] == "DIFFERENT"
        if p["degen"]:
            ok += ((p["dfr"] >= 80) == isdiff)
        else:
            ok += ((p["nocap"] >= T) == isdiff)
    a = ok / len(pre)
    if a > best[0]: best = (a, T)
print("HYB(degen->frozen80 else LCnocap): best acc=%.2f%% at T=%d" % (100*best[0], best[1]))
print("  degenerate fixtures: %d/720" % sum(1 for p in pre if p["degen"]))
# how does frozen do on the degenerate subset alone?
sub = [p for p in pre if p["degen"]]
a = sum(1 for p in sub if (p["dfr"] >= 80) == (p["truth"] == "DIFFERENT")) / len(sub)
print("  frozen rule on degenerate subset: %.2f%% (%d fixtures)" % (100*a, len(sub)))
sub2 = [p for p in pre if not p["degen"]]
a2, T2 = acc_of([(p["nocap"], p["truth"]) for p in sub2])
print("  LCnocap on non-degenerate subset: %.2f%% at T=%d (%d fixtures)" % (100*a2, T2, len(sub2)))
