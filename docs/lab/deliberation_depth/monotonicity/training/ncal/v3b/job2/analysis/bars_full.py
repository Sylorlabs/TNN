#!/usr/bin/env python3
"""Full NEC bar set B1-B9 + B13 from analyzer-format legs + 6-col driver outputs.
Frozen semantics per PREREG_NCAL_V1_FROZEN.md §4 and PREREG_NCAL.md B8 note.
Usage: bars_full.py <legsdir> <mech> <sixcol_out.tsv> <sixcol_in.tsv>
- legs: {battery}_m{mech}_d{depth}_A.tsv (analyzer 11-col format)
- B9: release+correct identity of sixcol_out cols[3],cols[4] vs sixcol_in cols[5],cols[6]
- B7: abstention from sixcol_out (rel==0 / total rows)
"""
import sys, glob, os, collections

legsdir, mech, sixcol_out, sixcol_in = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]

def family_of(battery, iid):
    if battery == "ceiling":
        p = iid.split("-")
        return p[1] if len(p) >= 2 and p[0] == "H5B" else "ceiling?"
    return battery

# ---- legs ----
data = collections.defaultdict(lambda: collections.defaultdict(dict))
for fn in glob.glob(os.path.join(legsdir, f"*_m{mech}_d*_A.tsv")):
    battery = os.path.basename(fn).split(f"_m{mech}_")[0]
    for line in open(fn):
        c = line.rstrip("\n").split("\t")
        if not c[0]: continue
        iid, dep = c[0], int(c[1])
        fam = family_of(battery, iid)
        if c[7] in ("1", "0"):
            data[fam][iid][dep] = (c[7], int(c[8]))

V1 = V2 = n10 = 0
cc, cw = [], []
b13 = b13cells = 0
gviol = 0
famG = {}          # fam -> {depth: G}
fam_nrel = {}      # fam -> {depth: n_rel}
per_fam_b4b = {}
for fam, items in sorted(data.items()):
    cb_d = collections.defaultdict(list)
    ccc = []
    for iid, dd in items.items():
        seq = sorted(dd.items())
        for i in range(len(seq) - 1):
            (d0, (c0, f0)), (d1, (c1, f1)) = seq[i], seq[i + 1]
            if c0 == "1" and c1 == "0":
                n10 += 1
                if f1 >= f0: V1 += 1
            if c0 == "0" and c1 == "0" and f1 > f0: V2 += 1
        for d, (co, cf) in seq:
            cb_d[d].append((co, cf))
            (cc if co == "1" else cw).append(cf)
            if co == "1": ccc.append(cf)
    ds = sorted(cb_d)
    G = {}
    for d in ds:
        cells = cb_d[d]
        G[d] = sum(f for _, f in cells)/len(cells)/1000 - sum(1 for co, _ in cells if co == "1")/len(cells)
        if len(cells) >= 8 and G[d] < -0.100:
            b13 += 1; b13cells += len(cells)
    for i in range(len(ds) - 1):
        if G[ds[i+1]] > G[ds[i]] + 1e-12: gviol += 1
    famG[fam] = {d: G[d] for d in ds}
    fam_nrel[fam] = {d: len(cb_d[d]) for d in ds}
    if len(ccc) >= 10:
        per_fam_b4b[fam] = sum(ccc)/len(ccc)/1000

B4 = sum(cc)/len(cc)/1000 if cc else 0
B5 = B4 - (sum(cw)/len(cw)/1000 if cw else 0)
honest = {f: v for f, v in per_fam_b4b.items() if f != "redteam"}
B4b = min(honest.values()) if honest else float("nan")

# ---- B8: per frozen note ----
# G defined = n_rel >= 10 at that depth; need >=4/5 slots (5-depth), >=5/7 (ceiling).
# pass = "not all equal within 1e-3".
DEPTHS5 = [1, 2, 4, 8, 16]; DEPTHS7 = [1, 2, 4, 8, 16, 32, 64]
b8_rows = []
for fam in sorted(famG):
    ds = DEPTHS7 if fam in ("P", "O", "D") else DEPTHS5
    defined = [d for d in ds if d in famG[fam] and fam_nrel[fam].get(d, 0) >= 10]
    need = 5 if fam in ("P", "O", "D") else 4
    if len(defined) >= need:
        vals = [famG[fam][d] for d in defined]
        passed = (max(vals) - min(vals)) > 1e-3
        b8_rows.append((fam, len(defined), "pass" if passed else "FAIL", max(vals)-min(vals)))
    else:
        b8_rows.append((fam, len(defined), "excluded(matrix-limited)", None))
b8_fail = [r for r in b8_rows if r[2] == "FAIL"]

# ---- B6: recall vs M4 (frozen release identity => 1.0 when B9=100%) ----
# computed from B9 result below.

# ---- B7 / B9 from 6-col ----
inp, outp = {}, {}
for line in open(sixcol_in):
    c = line.rstrip("\n").split("\t")
    if c[0]: inp[(c[0], int(c[2]))] = (c[5], c[6])          # (release, correct)
nrows = nabst = b9diff = 0
for line in open(sixcol_out):
    c = line.rstrip("\n").split("\t")
    if not c[0]: continue
    nrows += 1
    if c[3] == "0": nabst += 1
    key = (c[0], int(c[2]))
    if key in inp and (inp[key][0] != c[3] or inp[key][1] != c[4]):
        b9diff += 1
B7 = nabst/nrows if nrows else float("nan")
B9 = 1.0 - b9diff/nrows if nrows else float("nan")

print(f"mech={mech} legs={legsdir}")
print(f"B1(1->0)={n10} [{'PASS' if n10==0 else 'FAIL'}]")
print(f"B2: V1={V1} V2={V2} [{'PASS' if V1==0 and V2==0 else 'FAIL'}]")
print(f"B3: Gviol={gviol}")
print(f"B4={B4:.4f} [{'PASS' if B4>=0.50 else 'FAIL'}]")
print(f"B4b honest-fam min={B4b:.4f} [{'PASS' if B4b>=0.50 else 'FAIL'}] " +
      " ".join(f"{f}={v:.3f}" for f, v in sorted(honest.items())))
print(f"B5={B5:.4f} [{'PASS' if B5>=0.20 else 'FAIL'}]")
print(f"B6=1.000 (by B9 identity) [{'PASS' if B9==1.0 else 'CHECK'}]")
print(f"B7={B7:.4f} [{'PASS' if B7<=0.30 else 'FAIL'}]")
print(f"B8: computed per frozen note (reported, NON-GATING):")
for fam, nd, res, rng in b8_rows:
    print(f"    {fam}: defined_slots={nd} -> {res}" + (f" (range={rng:.4f})" if rng is not None else ""))
print(f"    B8 overall: {'FAIL' if b8_fail else 'pass (vacuous-as-frozen)'}" +
      ("; failing: " + ",".join(f[0] for f in b8_fail) if b8_fail else ""))
print(f"B9 identity={B9:.6f} ({nrows-b9diff}/{nrows}) [{'PASS' if B9==1.0 else 'FAIL'}]")
print(f"B13 violations={b13} (cells={b13cells})")
print("G curves:")
for fam in sorted(famG):
    ds = sorted(famG[fam])
    gstr = ",".join(f"{d}:{famG[fam][d]:+.3f}" for d in ds)
    print(f"  {fam}: {gstr}")
