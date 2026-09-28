#!/usr/bin/env python3
"""T2 (preregistered): matrix, analyzer families, m9 counterfactual.
bind ~ 1{deficit>0} + |deficit| + would_rise(F,d under m9)."""
import sys, math, collections
sys.path.insert(0, ".")
from sim_m11 import run as sim_run

def family_of(battery, item_id):
    if battery == "ceiling":
        parts = item_id.split("-")
        if len(parts) >= 2 and parts[0] == "H5B":
            return parts[1]
        return "ceiling?"
    return battery

_, diag = sim_run("necc_input.tsv")
simd = {(iid,dep): (cr,cp,tp,pr) for iid,dep,cr,cp,tp,pr,cm in diag}
corr = {}
for line in open("necc_input.tsv"):
    c = line.rstrip("\n").split("\t")
    if c[5]=="1": corr[(c[0],int(c[2]))] = int(c[6])

def load_out(fn):
    d = {}
    for line in open(fn):
        c = line.rstrip("\n").split("\t")
        if c[3]=="1": d[(c[0],int(c[2]))] = (family_of(c[1],c[0]), int(c[5]))
    return d

m9  = load_out("results/m9_necc_input_A.tsv")
m11 = load_out("results/m11_necc_input_A.tsv")

byfd = collections.defaultdict(list)
for (iid,dep),(fam,conf) in m9.items():
    byfd[(fam,dep)].append((corr[(iid,dep)], conf))
Gm = collections.defaultdict(dict)
for (fam,dep), cl in byfd.items():
    Gm[fam][dep] = sum(c for _,c in cl)/len(cl)/1000 - sum(a for a,_ in cl)/len(cl)
def would_rise(fam, dep):
    ds = sorted(Gm[fam].keys()); i = ds.index(dep)
    return 0 if i==0 else (1 if Gm[fam][dep] > Gm[fam][ds[i-1]] + 1e-12 else 0)

def build_rows(mech):
    rows = []
    for (iid,dep),(fam,confv) in mech.items():
        cr,cp,tp,pr = simd[(iid,dep)]
        bind = 1 if confv < m9[(iid,dep)][1] else 0
        dpos, dmag = (1,(cr-pr)/1e6) if (tp>=1 and pr>=0 and cr>pr) else (0,0.0)
        rows.append((bind,dpos,dmag,would_rise(fam,dep)))
    return rows

def irls(rows):
    cols=[1,2,3]; n=len(rows); p=3
    X=[[1.0,r[1],r[2],r[3]] for r in rows]; y=[r[0] for r in rows]
    b=[0.0]*4
    for _ in range(200):
        eta=[sum(X[i][j]*b[j] for j in range(4)) for i in range(n)]
        mu=[1/(1+math.exp(-e)) for e in eta]
        W=[m*(1-m) for m in mu]
        z=[eta[i]+(y[i]-mu[i])/max(W[i],1e-12) for i in range(n)]
        A=[[sum(X[i][j]*X[i][k]*W[i] for i in range(n)) for k in range(4)] for j in range(4)]
        Bv=[sum(X[i][j]*W[i]*z[i] for i in range(n)) for j in range(4)]
        M=[A[j][:]+[Bv[j]] for j in range(4)]
        for j in range(4):
            piv=max(range(j,4),key=lambda r: abs(M[r][j])); M[j],M[piv]=M[piv],M[j]
            d=M[j][j] or 1e-12; M[j]=[x/d for x in M[j]]
            for r in range(4):
                if r!=j and M[r][j]!=0:
                    f=M[r][j]; M[r]=[M[r][k]-f*M[j][k] for k in range(5)]
        nb=[M[j][4] for j in range(4)]
        if max(abs(nb[j]-b[j]) for j in range(4))<1e-10: b=nb; break
        b=nb
    return b

rows = build_rows(m11)
b = irls(rows)
print(f"m11: n={len(rows)} binds={sum(r[0] for r in rows)}")
print(f"  betas: intercept={b[0]:+.3f} deficit>0={b[1]:+.3f} |deficit|={b[2]:+.3f} would_rise={b[3]:+.3f}")
print("  S1 stratification (deficit>0 x would_rise -> bind rate):")
for dp in (0,1):
    for wr in (0,1):
        sub=[r for r in rows if r[1]==dp and r[3]==wr]
        br=sum(r[0] for r in sub)/len(sub) if sub else float('nan')
        print(f"    deficit>0={dp} would_rise={wr}: n={len(sub)} bind_rate={br:.4f}")
# which (fam,depth) have would_rise=1, and how many deficit>0 cells there
print("  would_rise=1 cells:")
c2=collections.Counter()
for (iid,dep),(fam,confv) in m11.items():
    if would_rise(fam,dep)==1:
        cr,cp,tp,pr=simd[(iid,dep)]
        c2[(fam,dep, 1 if (tp>=1 and pr>=0 and cr>pr) else 0)]+=1
for k in sorted(c2): print("   ",k,c2[k])
