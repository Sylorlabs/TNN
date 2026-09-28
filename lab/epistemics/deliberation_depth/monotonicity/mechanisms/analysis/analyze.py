#!/usr/bin/env python3
"""Analyze monotonicity mechanism TSVs: accuracy, abstention, G(d), transitions, L-OVERCONF."""
import os, sys, glob
from collections import defaultdict

RES = os.path.expanduser("~/workspace/tnn-lab/deliberation_depth/monotonicity/mechanisms/results")
MECHS = {0:"M0",1:"M1",2:"M2",3:"M3",4:"M4",5:"M5",6:"M6",7:"BASE",8:"M7"}
FAMS = ["admit","revoke","logic","trap","cost","ceiling","redteam"]

def fam_of(battery, item_id):
    if battery=="ceiling":
        if item_id.startswith("H5B-P-"): return "P"
        if item_id.startswith("H5B-O-"): return "O"
        if item_id.startswith("H5B-D-"): return "D"
        return "ceiling?"
    return battery

def load(battery, mech, depth):
    pat = f"{RES}/{battery}_m{mech}_d{depth}_A.tsv"
    rows=[]
    for ln in open(pat):
        p=ln.rstrip("\n").split("\t")
        # id depth t rounds consumed ne release correct conf leader_idx cert
        rows.append(dict(id=p[0],depth=int(p[1]),t=int(p[2]),rounds=int(p[3]),
                         consumed=int(p[4]),ne=int(p[5]),release=p[6],
                         correct=p[7],conf=int(p[8])/1000.0,leader=int(p[9]),cert=p[10]))
    return rows

def main():
    depths_of = {"admit":[1,2,4,8,16],"revoke":[1,2,4,8,16],"logic":[1,2,4,8,16],
                 "trap":[1,2,4,8,16],"cost":[1,2,4,8,16],"ceiling":[1,2,4,8,16,32,64],
                 "redteam":[1,2,4,8,16]}
    # per (mech,fam): depth -> list of (correct, conf)
    data=defaultdict(lambda: defaultdict(list))
    for batt in FAMS:
        for mech in MECHS:
            for d in depths_of[batt]:
                try: rows=load(batt,mech,d)
                except FileNotFoundError: continue
                for r in rows:
                    fam=fam_of(batt,r["id"])
                    data[(mech,fam)][d].append(r)
    out=[]
    out.append("# Per-design per-family summary")
    out.append("mech | family | depth | n | acc | abst | G(d) | mean_conf(rel)")
    kill_10=defaultdict(int); reg_a0=defaultdict(int)
    v1=defaultdict(int); v2=defaultdict(int)
    g_viol=defaultdict(list)
    # transitions need per-item across depths
    for (mech,fam), dd in sorted(data.items()):
        ds=sorted(dd.keys())
        # per-item sequences
        seq=defaultdict(dict)
        for d in ds:
            for r in dd[d]:
                seq[r["id"]][d]=(r["correct"],r["conf"])
        # summary per depth
        for d in ds:
            rs=dd[d]
            n=len(rs)
            rel=[r for r in rs if r["correct"] in ("1","0")]
            acc=sum(1 for r in rel if r["correct"]=="1")/len(rel) if rel else float("nan")
            abst=sum(1 for r in rs if r["correct"]=="A")/n if n else 0
            mc=sum(r["conf"] for r in rel)/len(rel) if rel else float("nan")
            g=mc-acc if rel else float("nan")
            out.append(f"{MECHS[mech]:4s} | {fam:7s} | d{d:2d} | {n:3d} | {acc:.3f} | {abst:.3f} | {g:+.3f} | {mc:.3f}")
        # transitions + violations across adjacent depths
        for i in range(len(ds)-1):
            d1,d2=ds[i],ds[i+1]
            for iid,s in seq.items():
                if d1 not in s or d2 not in s: continue
                c1,f1=s[d1]; c2,f2=s[d2]
                if c1=="1" and c2=="0": kill_10[(mech,fam)]+=1
                if c1=="A" and c2=="0": reg_a0[(mech,fam)]+=1
                if c1=="1" and c2=="0" and f2>=f1: v1[(mech,fam)]+=1
                if c1=="0" and c2=="0" and f2>f1: v2[(mech,fam)]+=1
        # G violations
        for i in range(len(ds)-1):
            d1,d2=ds[i],ds[i+1]
            r1=[r for r in dd[d1] if r["correct"] in ("1","0")]
            r2=[r for r in dd[d2] if r["correct"] in ("1","0")]
            if not r1 or not r2: continue
            g1=sum(r["conf"] for r in r1)/len(r1)-sum(1 for r in r1 if r["correct"]=="1")/len(r1)
            g2=sum(r["conf"] for r in r2)/len(r2)-sum(1 for r in r2 if r["correct"]=="1")/len(r2)
            if g2>g1+1e-9: g_viol[(mech,fam)].append((d1,d2,g1,g2))
    out.append("\n# 1->0 kill counts (accuracy bar)")
    for k in sorted(kill_10):
        if kill_10[k]: out.append(f"{MECHS[k[0]]} {k[1]}: {kill_10[k]}")
    out.append("\n# A->0 regression counts")
    for k in sorted(reg_a0):
        if reg_a0[k]: out.append(f"{MECHS[k[0]]} {k[1]}: {reg_a0[k]}")
    out.append("\n# V1 violations (1->0 with conf non-decreasing)")
    for k in sorted(v1):
        if v1[k]: out.append(f"{MECHS[k[0]]} {k[1]}: {v1[k]}")
    out.append("\n# V2 violations (0->0 with conf rising)")
    for k in sorted(v2):
        if v2[k]: out.append(f"{MECHS[k[0]]} {k[1]}: {v2[k]}")
    out.append("\n# G(d+1)>G(d) violations (L-OVERCONF)")
    for k in sorted(g_viol):
        steps="; ".join(f"d{a}->{b} ({x:+.3f}->{y:+.3f})" for a,b,x,y in g_viol[k])
        out.append(f"{MECHS[k[0]]} {k[1]}: {steps}")
    sys.stdout.write("\n".join(out)+"\n")

main()
