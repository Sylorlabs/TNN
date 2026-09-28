#!/usr/bin/env python3
"""T2 (FIX-A audit): selective binding on the FIX-A-augmented s1 matrix.
bind ⟺ deficit>0 exactly; logistic bind ~ 1{deficit>0} + |deficit| + would_rise
(IRLS, same as q2_analysis/analyze_t2b.py). would_rise from the m9
counterfactual on the SAME augmented input.
Usage: audit_t2.py <necc_s1_FIXA.tsv> <m11_out.tsv> <m9_out.tsv>
"""
import sys, math, collections
sys.path.insert(0, "/home/hatch/workspace/tnn-lab/deliberation_depth/monotonicity/training/ncal/q2_analysis")
from sim_m11 import run as sim_run

in_tsv, m11_tsv, m9_tsv = sys.argv[1], sys.argv[2], sys.argv[3]

def family_of(battery, item_id):
    if battery == "ceiling":
        parts = item_id.split("-")
        if len(parts) >= 2 and parts[0] == "H5B":
            return parts[1]
        return "ceiling?"
    return battery

_, diag = sim_run(in_tsv)
simd = {(iid, dep): (cr, cp, tp, pr) for iid, dep, cr, cp, tp, pr, cm in diag}
corr = {}
for line in open(in_tsv):
    c = line.rstrip("\n").split("\t")
    if c[5] == "1":
        corr[(c[0], int(c[2]))] = int(c[6])

def load_out(fn):
    d = {}
    for line in open(fn):
        c = line.rstrip("\n").split("\t")
        if c[3] == "1":
            d[(c[0], int(c[2]))] = (family_of(c[1], c[0]), int(c[5]))
    return d

m9 = load_out(m9_tsv)
m11 = load_out(m11_tsv)

byfd = collections.defaultdict(list)
for (iid, dep), (fam, conf) in m9.items():
    byfd[(fam, dep)].append((corr[(iid, dep)], conf))
Gm = collections.defaultdict(dict)
for (fam, dep), cl in byfd.items():
    Gm[fam][dep] = sum(c for _, c in cl) / len(cl) / 1000 - sum(a for a, _ in cl) / len(cl)

def would_rise(fam, dep):
    ds = sorted(Gm[fam].keys()); i = ds.index(dep)
    return 0 if i == 0 else (1 if Gm[fam][dep] > Gm[fam][ds[i - 1]] + 1e-12 else 0)

tab = collections.Counter()
rows = []
for (iid, dep), (fam, confv) in m11.items():
    cr, cp, tp, pr = simd[(iid, dep)]
    bind = 1 if confv < m9[(iid, dep)][1] else 0
    dpos, dmag = (1, (cr - pr) / 1e6) if (tp >= 1 and pr >= 0 and cr > pr) else (0, 0.0)
    wr = would_rise(fam, dep)
    tab[(dpos, wr, bind)] += 1
    rows.append((bind, dpos, dmag, wr))

print("deficit>0 | would_rise | bind=0 | bind=1 | bind rate")
for dp in (0, 1):
    for wr in (0, 1):
        z = tab[(dp, wr, 0)]; o = tab[(dp, wr, 1)]
        print(f"    {dp}      |     {wr}      | {z:5d} | {o:4d} | {o/(z+o):.4f}")

def irls(rows):
    n = len(rows)
    X = [[1.0, r[1], r[2], r[3]] for r in rows]; y = [r[0] for r in rows]
    b = [0.0] * 4
    for _ in range(200):
        eta = [sum(X[i][j] * b[j] for j in range(4)) for i in range(n)]
        mu = [1 / (1 + math.exp(-e)) for e in eta]
        W = [m * (1 - m) for m in mu]
        z = [eta[i] + (y[i] - mu[i]) / max(W[i], 1e-12) for i in range(n)]
        A = [[sum(X[i][j] * X[i][k] * W[i] for i in range(n)) for k in range(4)] for j in range(4)]
        Bv = [sum(X[i][j] * W[i] * z[i] for i in range(n)) for j in range(4)]
        M = [A[j][:] + [Bv[j]] for j in range(4)]
        for j in range(4):
            piv = max(range(j, 4), key=lambda r: abs(M[r][j])); M[j], M[piv] = M[piv], M[j]
            d = M[j][j] or 1e-12; M[j] = [x / d for x in M[j]]
            for r in range(4):
                if r != j and M[r][j] != 0:
                    f = M[r][j]; M[r] = [M[r][k] - f * M[j][k] for k in range(5)]
        b = [M[j][4] for j in range(4)]
    return b

b = irls(rows)
print(f"T2 FIX-A: IRLS bind ~ 1{{deficit>0}} + |deficit| + would_rise:")
print(f"  beta = [{b[0]:+.4f}, {b[1]:+.4f}, {b[2]:+.4f}, {b[3]:+.4f}]  (would_rise beta={b[3]:+.4f})")
print("verdict:", "NO-RESIDUAL-BAR-CORRELATION" if abs(b[3]) < 0.01 else "RESIDUAL-FOUND")
