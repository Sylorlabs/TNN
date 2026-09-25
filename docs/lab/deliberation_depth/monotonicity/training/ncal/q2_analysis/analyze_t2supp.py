#!/usr/bin/env python3
"""T2-SUPP: bind ~ 1{deficit>0} + wrong_at_cell on trap_t1 (m9 counterfactual)."""
import sys, math, collections
sys.path.insert(0, ".")
from sim_m11 import run as sim_run

_, diag = sim_run("trap_t1.tsv")
simd = {(iid,dep): (cr,cp,tp,pr) for iid,dep,cr,cp,tp,pr,cm in diag}
corr = {}
for line in open("trap_t1.tsv"):
    c = line.rstrip("\n").split("\t")
    corr[(c[0],int(c[2]))] = int(c[6])

def load_out(fn):
    d = {}
    for line in open(fn):
        c = line.rstrip("\n").split("\t")
        if c[3]=="1": d[(c[0],int(c[2]))] = int(c[5])
    return d
m9 = load_out("results/m9_trap_t1_A.tsv")

def build_rows(fn):
    mech = load_out(fn); rows = []
    for (iid,dep), confv in mech.items():
        cr,cp,tp,pr = simd[(iid,dep)]
        bind = 1 if confv < m9[(iid,dep)] else 0
        dpos = 1 if (tp>=1 and pr>=0 and cr>pr) else 0
        rows.append((bind, dpos, 1-corr[(iid,dep)]))
    return rows

def logit(rows):
    # bind ~ dpos + wrong ; IRLS
    n=len(rows); X=[[1.0,r[1],r[2]] for r in rows]; y=[r[0] for r in rows]
    b=[0.0]*3
    for _ in range(200):
        eta=[sum(X[i][j]*b[j] for j in range(3)) for i in range(n)]
        mu=[1/(1+math.exp(-e)) for e in eta]
        W=[m*(1-m) for m in mu]
        z=[eta[i]+(y[i]-mu[i])/max(W[i],1e-12) for i in range(n)]
        A=[[sum(X[i][j]*X[i][k]*W[i] for i in range(n)) for k in range(3)] for j in range(3)]
        Bv=[sum(X[i][j]*W[i]*z[i] for i in range(n)) for j in range(3)]
        M=[A[j][:]+[Bv[j]] for j in range(3)]
        for j in range(3):
            piv=max(range(j,3),key=lambda r: abs(M[r][j])); M[j],M[piv]=M[piv],M[j]
            d=M[j][j] or 1e-12; M[j]=[x/d for x in M[j]]
            for r in range(3):
                if r!=j and M[r][j]!=0:
                    f=M[r][j]; M[r]=[M[r][k]-f*M[j][k] for k in range(4)]
        nb=[M[j][3] for j in range(3)]
        if max(abs(nb[j]-b[j]) for j in range(3))<1e-10: b=nb; break
        b=nb
    # SEs
    eta=[sum(X[i][j]*b[j] for j in range(3)) for i in range(n)]
    mu=[1/(1+math.exp(-e)) for e in eta]; W=[m*(1-m) for m in mu]
    A=[[sum(X[i][j]*X[i][k]*W[i] for i in range(n)) for k in range(3)] for j in range(3)]
    M=[A[j][:]+[1.0 if k==j else 0.0 for k in range(3)] for j in range(3)]
    for j in range(3):
        piv=max(range(j,3),key=lambda r: abs(M[r][j])); M[j],M[piv]=M[piv],M[j]
        d=M[j][j] or 1e-12; M[j]=[x/d for x in M[j]]
        for r in range(3):
            if r!=j and M[r][j]!=0:
                f=M[r][j]; M[r]=[M[r][k]-f*M[j][k] for k in range(6)]
    se=[math.sqrt(max(M[j][3+j],0)) for j in range(3)]
    return b,se

for v in ["m11","g"]:
    rows = build_rows(f"results/{v}_trap_t1_A.tsv")
    b,se = logit(rows)
    from math import erf, sqrt
    z = b[2]/se[2] if se[2]>0 else 0.0
    p = 2*(1-0.5*(1+erf(abs(z)/sqrt(2))))
    print(f"{v}: n={len(rows)} binds={sum(r[0] for r in rows)}")
    print(f"  intercept={b[0]:+.3f} deficit>0={b[1]:+.3f}(se {se[1]:.2f}) wrong={b[2]:+.3f}(se {se[2]:.2f}) z={z:+.2f} p={p:.2e}")
    for dp in (0,1):
        for w in (0,1):
            sub=[r for r in rows if r[1]==dp and r[2]==w]
            br=sum(r[0] for r in sub)/len(sub) if sub else float('nan')
            print(f"    deficit>0={dp} wrong={w}: n={len(sub)} bind_rate={br:.4f}")
