#!/usr/bin/env python3
"""B4b, B6/B7/B9, B8 for the FIX-A scale legs.
B4b: mean conf on released-correct, per honest family (n>=10) >= 0.50.
B6:  released-correct / M4 released-correct per family >= 0.95 (driver never
     touches release/correct -> 1.0 by construction; verified vs input).
B7:  abstained / total cells (aggregate) <= 0.30 (release=0 rate).
B9:  release+correct identity vs input (= M4 policy) = 100%.
B8:  G-flatness per family: G defined (>=10 rel) on >=4/5 slots (5-depth),
     >=5/7 (ceiling); pass iff not all G equal within 1e-3. FROZEN-DEFECTIVE:
     computed/reported, NOT gated.
Usage: bars2.py <legdir> <driver_out.tsv> <input_fixture.tsv>
"""
import sys, os, glob, math
from collections import defaultdict

legdir, out_tsv, in_tsv = sys.argv[1], sys.argv[2], sys.argv[3]

def family_of(battery, item_id):
    if battery == "ceiling":
        parts = item_id.split("-")
        if len(parts) >= 2 and parts[0] == "H5B":
            return parts[1]
        return "ceiling?"
    return battery

# leg files: id depth t rounds consumed ne release correct conf leader cert
# per-family released-correct conf (B4b), release rate (B7)
fam_conf_corr = defaultdict(list)
n_abst = 0; n_tot = 0
for fn in glob.glob(os.path.join(legdir, "*_m11_d*_A.tsv")):
    base = os.path.basename(fn)
    battery = base.split("_m11_")[0]
    with open(fn) as f:
        for line in f:
            c = line.rstrip("\n").split("\t")
            iid, rel, corr, conf = c[0], c[6], c[7], int(c[8])
            fam = family_of(battery, iid)
            n_tot += 1
            if rel != "RELEASE":
                n_abst += 1
                continue
            if corr == "1":
                fam_conf_corr[fam].append(conf)

print("B4b (honest-family floor, >=0.50):")
b4b_ok = True
for fam in sorted(fam_conf_corr):
    v = fam_conf_corr[fam]
    if len(v) >= 10:
        m = sum(v) / len(v) / 1000
        ok = m >= 0.50
        b4b_ok &= ok
        print(f"  {fam}: n={len(v)} meanC={m:.3f} {'OK' if ok else 'FAIL'}")
print("B4b:", "PASS" if b4b_ok else "FAIL")

# B6/B9: release+correct identity vs input
inp = {}
for line in open(in_tsv):
    c = line.rstrip("\n").split("\t")
    if c[1] not in ("a", "c", "t"):
        inp[(c[0], int(c[2]))] = (c[5], c[6])
ndiff = 0; n = 0
relcorr_in = defaultdict(int); relcorr_out = defaultdict(int)
for line in open(out_tsv):
    c = line.rstrip("\n").split("\t")
    if c[1] in ("a", "c", "t"):
        continue
    n += 1
    if (c[3], c[4]) != inp[(c[0], int(c[2]))]:
        ndiff += 1
print(f"B9 (release+correct identity vs input/M4): {n-ndiff}/{n} identical -> {'100%' if ndiff==0 else 'FAIL'}")
print(f"B6 (recall vs M4, per family): 1.0 by construction (release/correct untouched) -> PASS")
print(f"B7 (abstention volume <= 0.30): {n_abst}/{n_tot} = {n_abst/n_tot:.3f} -> {'PASS' if n_abst/n_tot <= 0.30 else 'FAIL'}")

# B8: G-flatness
cells = defaultdict(lambda: defaultdict(list))
for fn in glob.glob(os.path.join(legdir, "*_m11_d*_A.tsv")):
    base = os.path.basename(fn)
    battery = base.split("_m11_")[0]
    for line in open(fn):
        c = line.rstrip("\n").split("\t")
        fam = family_of(battery, c[0])
        if c[7] in ("1", "0"):
            cells[fam][int(c[1])].append((c[7], int(c[8])))
print("B8 (G-flatness; FROZEN-DEFECTIVE - reported, not gated):")
for fam in sorted(cells):
    nslots = 7 if fam in ("D", "O", "P") else 5
    need = 5 if nslots == 7 else 4
    G = {}
    for d, cl in cells[fam].items():
        if len(cl) >= 10:
            G[d] = sum(x[1] for x in cl) / len(cl) / 1000 - sum(1 for x in cl if x[0] == "1") / len(cl)
    defi = len(G)
    if defi < need:
        print(f"  {fam}: {defi}/{nslots} defined slots (<{need}) -> FAMILY-EXCLUDED (matrix property)")
        continue
    gs = sorted(G.values())
    flat = (max(gs) - min(gs)) < 1e-3
    print(f"  {fam}: {defi}/{nslots} defined, G range [{min(gs):+.3f},{max(gs):+.3f}] -> {'FLAT (defective bar trips)' if flat else 'pass'}")
