#!/usr/bin/env python3
"""Round-1 autopsy step 2: byte-level mechanism proof for each admit class.
Class A: motiondir/reversed — prove F frames == G frames reversed (exact).
Class B: colordisc/illuminant-drift — characterize the exact sum collision.
"""
import struct, os

PAIRS = "/home/hatch/workspace/selfpam_consumer/pairs_full"
TASKS = ["colordisc", "colorconst", "shapetrans", "pitchdisc", "timbredisc", "motiondir"]

def parse_pair(path):
    data = open(path, "rb").read()
    assert data[:4] == b"R2P1", path
    task, idx, scene, flen, glen, fkind = struct.unpack("<iiQiii", data[4:32])
    return task, idx, scene, fkind, data[64:64 + flen], data[64 + flen:]

def frames_payload(blob):
    nframes, w, h = struct.unpack("<IHH", blob[:8])
    fsize = w * h * 3
    assert len(blob) == 8 + nframes * fsize, (len(blob), nframes, w, h)
    return nframes, w, h, [blob[8 + i * fsize:8 + (i + 1) * fsize] for i in range(nframes)]

# ---- Class A: all motiondir admits must be exact frame reversals
import csv
rows = list(csv.DictReader(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "admitted_raw.tsv")), delimiter="\t"))
mot = [r for r in rows if r["task"] == "motiondir"]
print("motiondir admits:", len(mot))
assert all(r["mode"] == "0" and r["note"] == "reversed" for r in mot), "non-mode0 motiondir admit!"
assert all(r["byte_perm"] == "True" for r in mot)
n_exact_rev = 0
for r in mot:
    p = os.path.join(PAIRS, "r2p_motiondir_%03d.pair" % int(r["pair_idx"]))
    task, idx, scene, fkind, F, G = parse_pair(p)
    nf, w, h, FF = frames_payload(F)
    ng, wg, hg, GG = frames_payload(G)
    assert (nf, w, h) == (ng, wg, hg) == (50, 24, 24)
    assert F[:8] == G[:8], "payload headers differ"
    if FF == GG[::-1]:
        n_exact_rev += 1
    else:
        print("NOT exact reversal:", r["pair_idx"])
print("exact frame-reversal F==reverse(G): %d/%d" % (n_exact_rev, len(mot)))
# also: no two frames identical (reversal is nontrivial)
p0 = os.path.join(PAIRS, "r2p_motiondir_000.pair")
_, _, _, _, F0, G0 = parse_pair(p0)
_, _, _, FF0 = frames_payload(F0)
print("sample pair 0: distinct frames in G:", len(set(frames_payload(G0)[3])))

# ---- Class B: colordisc_135 exact sum collision anatomy
r = [x for x in rows if x["task"] == "colordisc"][0]
print("\nClass B:", r["ledger_idx"], r["task"], r["pair_idx"], "truth=? (from repo fixture)")
p = os.path.join(PAIRS, "r2p_colordisc_%03d.pair" % int(r["pair_idx"]))
task, idx, scene, fkind, F, G = parse_pair(p)
nf, w, h, FF = frames_payload(F)
_, _, _, GG = frames_payload(G)
print("frames: F=%d G=%d size=%dx%d" % (nf, len(GG), w, h))
print("all F frames identical:", len(set(FF)) == 1, "| all G frames identical:", len(set(GG)) == 1)
f0, g0 = FF[0], GG[0]
# left/right halves (16 wide -> 8+8 cols, 8 rows, 3 bytes/px)
def half_sums(fr):
    sl = sr = 0
    for y in range(8):
        for x in range(16):
            o = (y * 16 + x) * 3
            s = fr[o] + fr[o + 1] + fr[o + 2]
            if x < 8: sl += s
            else: sr += s
    return sl, sr
fL, fR = half_sums(f0)
gL, gR = half_sums(g0)
print("F frame: left-half sum=%d right-half sum=%d total=%d" % (fL, fR, fL + fR))
print("G frame: left-half sum=%d right-half sum=%d total=%d" % (gL, gR, gL + gR))
print("per-frame sums equal:", fL + fR == gL + gR)
print("F left == G left (d65 half):", f0[:8*8*3] == g0[:8*8*3])
# the actual colors
c1 = tuple(f0[0:3]); c2 = tuple(f0[(8)*3:(8)*3+3]); c0 = tuple(g0[0:3])
print("F left color (d65):", c1, "sum/px=", sum(c1))
print("F right color (warm):", c2, "sum/px=", sum(c2))
print("G color (d65):", c0, "sum/px=", sum(c0))
print("sum(c1)+sum(c2) == 2*sum(c0):", sum(c1) + sum(c2) == 2 * sum(c0))
print("total: sumF=%d sumG=%d exact-equal=%s" % (sum(F) % 2**31, sum(G) % 2**31, sum(F) == sum(G)))
print("/8 tolerance involved:", (sum(F) % 2**31) // 8 == (sum(G) % 2**31) // 8, "(sums exactly equal, tolerance irrelevant)")
# symlink or regenerated?
print("pair file is symlink:", os.path.islink(p))
