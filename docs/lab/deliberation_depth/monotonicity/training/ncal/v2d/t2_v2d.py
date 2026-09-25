#!/usr/bin/env python3
"""T2 selective-binding for m15/m20 (+ m_g15/m_g20 probe-power controls).
Preregistered stats: S1 stratified bind rates (within 1pp), S2 logistic
bind ~ 1{deficit>0} + |deficit| + would_rise with Wald p on would_rise.
Usage: t2_v2d.py <workdir>
workdir holds: necc_input.tsv, necc_out_A2.tsv (m9), m15_6col_A.tsv,
  m20_6col_A.tsv, g15_6col_A.tsv, g20_6col_A.tsv, pool via sim.
"""
import sys, math, collections
sys.path.insert(0, ".")
from sim_v2d import run as sim_run

W = sys.argv[1]

def family_of(battery, iid):
    if battery == "ceiling":
        p = iid.split("-")
        return p[1] if len(p) >= 2 and p[0] == "H5B" else "ceiling?"
    return battery

def load6(fn):
    d = {}
    for line in open(fn):
        c = line.rstrip("\n").split("\t")
        if c[3] == "1": d[(c[0], int(c[2]))] = (family_of(c[1], c[0]), int(c[5]))
    return d

m9  = load6(f"{W}/necc_out_A2.tsv")
m15 = load6(f"{W}/m15_6col_A.tsv")
m20 = load6(f"{W}/m20_6col_A.tsv")
g15 = load6(f"{W}/g15_6col_A.tsv")
g20 = load6(f"{W}/g20_6col_A.tsv")

_, d15 = sim_run(f"{W}/necc_input.tsv", "m15")
_, d20 = sim_run(f"{W}/necc_input.tsv", "m20")
_, dpool = sim_run(f"{W}/necc_input.tsv", "pool")
s15 = {(i, dp): (cr, cp, tp, pr, cm) for i, dp, cr, cp, tp, pr, cm in d15}
s20 = {(i, dp): (cr, cp, tp, pr, cm) for i, dp, cr, cp, tp, pr, cm in d20}
spool = {(i, dp): cm for i, dp, cr, cp, tp, pr, cm in dpool}

def G_of(outd):
    byfd = collections.defaultdict(list)
    corr = {}
    for line in open(f"{W}/necc_input.tsv"):
        c = line.rstrip("\n").split("\t")
        if c[5] == "1": corr[(c[0], int(c[2]))] = int(c[6])
    for (iid, dep), (fam, conf) in outd.items():
        byfd[(fam, dep)].append((corr[(iid, dep)], conf))
    G = collections.defaultdict(dict)
    for (fam, dep), cl in byfd.items():
        G[fam][dep] = sum(c for _, c in cl)/len(cl)/1000 - sum(a for a, _ in cl)/len(cl)
    return G

Gm9 = G_of(m9)
Gpool = G_of({k: (f, spool[k]//1000) for k, (f, _) in m9.items()})

def would_rise(G, fam, dep):
    ds = sorted(G[fam].keys()); i = ds.index(dep)
    return 0 if i == 0 else (1 if G[fam][dep] > G[fam][ds[i-1]] + 1e-12 else 0)

def build(mech_out, simd, counter_out, Gcf, tag):
    rows = []
    for (iid, dep), (fam, confv) in mech_out.items():
        cr, cp, tp, pr, cm = simd[(iid, dep)]
        bind = 1 if confv < counter_out[(iid, dep)][1] else 0
        dpos, dmag = (1, (cr-pr)/1e6) if (tp >= 1 and pr >= 0 and cr > pr) else (0, 0.0)
        rows.append((bind, dpos, dmag, would_rise(Gcf, fam, dep)))
    return rows

def irls_wald(rows):
    n = len(rows); p = 4
    X = [[1.0, r[1], r[2], r[3]] for r in rows]; y = [r[0] for r in rows]
    b = [0.0]*4
    for _ in range(200):
        eta = [sum(X[i][j]*b[j] for j in range(p)) for i in range(n)]
        mu = [1/(1+math.exp(-max(-500, min(500, e)))) for e in eta]
        Wd = [m*(1-m) for m in mu]
        z = [eta[i]+(y[i]-mu[i])/max(Wd[i], 1e-12) for i in range(n)]
        A = [[sum(X[i][j]*X[i][k]*Wd[i] for i in range(n)) for k in range(p)] for j in range(p)]
        Bv = [sum(X[i][j]*Wd[i]*z[i] for i in range(n)) for j in range(p)]
        # solve with ridge for stability under separation
        for j in range(p): A[j][j] += 1e-8
        M = [A[j][:]+[Bv[j]] for j in range(p)]
        for j in range(p):
            piv = max(range(j, p), key=lambda r: abs(M[r][j])); M[j], M[piv] = M[piv], M[j]
            d = M[j][j] or 1e-12; M[j] = [x/d for x in M[j]]
            for r in range(p):
                if r != j and M[r][j] != 0:
                    f = M[r][j]; M[r] = [M[r][k]-f*M[j][k] for k in range(p+1)]
        nb = [M[j][p] for j in range(p)]
        if max(abs(nb[j]-b[j]) for j in range(p)) < 1e-10: b = nb; break
        b = nb
    # Wald SEs from final X'WX inverse
    eta = [sum(X[i][j]*b[j] for j in range(p)) for i in range(n)]
    mu = [1/(1+math.exp(-max(-500, min(500, e)))) for e in eta]
    Wd = [m*(1-m) for m in mu]
    A = [[sum(X[i][j]*X[i][k]*Wd[i] for i in range(n)) for k in range(p)] for j in range(p)]
    for j in range(p): A[j][j] += 1e-8
    # invert A
    M = [A[j][:]+[1.0 if k == j else 0.0 for k in range(p)] for j in range(p)]
    for j in range(p):
        piv = max(range(j, p), key=lambda r: abs(M[r][j])); M[j], M[piv] = M[piv], M[j]
        d = M[j][j] or 1e-12; M[j] = [x/d for x in M[j]]
        for r in range(p):
            if r != j and M[r][j] != 0:
                f = M[r][j]; M[r] = [M[r][k]-f*M[j][k] for k in range(2*p)]
    se = [math.sqrt(max(M[j][p+j], 0)) for j in range(p)]
    z = [b[j]/se[j] if se[j] > 0 else 0.0 for j in range(p)]
    pval = [2*(1-0.5*(1+math.erf(abs(v)/math.sqrt(2)))) for v in z]
    return b, se, pval

tests = [
    ("m15", build(m15, s15, m9, Gm9, "m15"), "counterfactual m9"),
    ("m20", build(m20, s20, {k: (f, spool[k]//1000) for k, (f, _) in m20.items()}, Gpool, "m20"),
     "counterfactual pool"),
    ("m_g15", build(g15, s15, m9, Gm9, "m_g15"), "counterfactual m9"),
    ("m_g20", build(g20, s20, {k: (f, spool[k]//1000) for k, (f, _) in g20.items()}, Gpool, "m_g20"),
     "counterfactual pool"),
]
for name, rows, cf in tests:
    b, se, pval = irls_wald(rows)
    print(f"== {name} ({cf}): n={len(rows)} binds={sum(r[0] for r in rows)}")
    print(f"   betas: int={b[0]:+.3f} d>0={b[1]:+.3f} |d|={b[2]:+.3f} would_rise={b[3]:+.3f}")
    print(f"   SE:    int={se[0]:.3f} d>0={se[1]:.3f} |d|={se[2]:.3f} would_rise={se[3]:.3f}")
    print(f"   p:     int={pval[0]:.3g} d>0={pval[1]:.3g} |d|={pval[2]:.3g} would_rise={pval[3]:.3g}")
    print("   S1 stratification:")
    for dp in (0, 1):
        for wr in (0, 1):
            sub = [r for r in rows if r[1] == dp and r[3] == wr]
            br = sum(r[0] for r in sub)/len(sub) if sub else float("nan")
            print(f"     deficit>0={dp} would_rise={wr}: n={len(sub)} bind_rate={br:.4f}")
