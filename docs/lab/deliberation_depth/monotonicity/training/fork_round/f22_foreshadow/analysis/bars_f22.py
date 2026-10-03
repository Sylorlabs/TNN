#!/usr/bin/env python3
"""F22 bar metrics: B1-B9, B4b, B8 (amended), B12, B13, B3pi + F22 kill-bar (a) leg detail.
Reads results_f22/*_m22_d*_A.tsv and M4 refs. Replicates frozen analyze.py semantics.
"""
import os, glob, math
from collections import defaultdict

RES = os.path.expanduser("~/workspace/tnn-lab/deliberation_depth/monotonicity/training/results_f22")
M4R = os.path.expanduser("~/workspace/tnn-lab/deliberation_depth/monotonicity/mechanisms/results")
BATTERY_DEPTHS = {"admit":[1,2,4,8,16],"revoke":[1,2,4,8,16],"logic":[1,2,4,8,16],
                  "trap":[1,2,4,8,16],"cost":[1,2,4,8,16],"redteam":[1,2,4,8,16],
                  "ceiling":[1,2,4,8,16,32,64]}
HONEST = {"admit","revoke","logic","cost","D","O","P"}

def family_of(battery, iid):
    if battery=="ceiling":
        p=iid.split("-")
        if len(p)>=2 and p[0]=="H5B": return p[1]
        return "ceiling?"
    return battery

# data[battery][fam][iid][depth] = (correct, conf, release)
data=defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
for battery,depths in BATTERY_DEPTHS.items():
    for d in depths:
        for fn in glob.glob(os.path.join(RES,f"{battery}_m22_d{d}_A.tsv")):
            for line in open(fn):
                line=line.rstrip("\n")
                if not line: continue
                c=line.split("\t")
                fam=family_of(battery,c[0])
                data[battery][fam][c[0]][int(c[1])]=(c[7],int(c[8]),c[6])

# ---- per-item transitions (B1, B2, B3pi) ----
n10=v1=v2=0
b3pi_viol=0; b3pi_tot=0
for battery in data:
    for fam in data[battery]:
        for iid,dd in data[battery][fam].items():
            seq=sorted(dd.items())
            for i in range(len(seq)-1):
                d0,(c0,f0,_)=seq[i]; d1,(c1,f1,_)=seq[i+1]
                if c0=="1" and c1=="0": n10+=1
                if c0=="1" and c1=="0" and f1>=f0: v1+=1
                if c0=="0" and c1=="0" and f1>f0: v2+=1
                # B3pi: per-item G_i(d)=conf/1000-acc_i must not rise (released only)
                if c0 in ("1","0") and c1 in ("1","0"):
                    b3pi_tot+=1
                    g0=f0/1000.0-(1.0 if c0=="1" else 0.0)
                    g1=f1/1000.0-(1.0 if c1=="1" else 0.0)
                    if g1>g0+1e-12: b3pi_viol+=1

# ---- per (battery,fam,depth): n_rel, G, acc, conf stats ----
legs={}  # (battery,fam,d) -> dict
for battery in data:
    for fam in data[battery]:
        for d in BATTERY_DEPTHS[battery]:
            rel=[(c,f) for iid,dd in data[battery][fam].items() if d in dd
                 for (c,f,r) in [dd[d]] if c in ("1","0")]
            nrel=len(rel)
            if nrel:
                mc=sum(f for _,f in rel)/nrel/1000.0
                acc=sum(1 for c,_ in rel if c=="1")/nrel
                G=mc-acc
            else: mc=acc=G=None
            # conf correct/wrong (released)
            cc=[f/1000.0 for c,f in rel if c=="1"]; cw=[f/1000.0 for c,f in rel if c=="0"]
            legs[(battery,fam,d)]={"nrel":nrel,"G":G,"mc":mc,"acc":acc,
                "mcc":sum(cc)/len(cc) if cc else None,"mcw":sum(cw)/len(cw) if cw else None,
                "ncc":len(cc),"ncw":len(cw)}

# ---- B3 G-violations per family ----
print("=== B3 G-violations per family ===")
b3_fail=[]
for battery in sorted(data):
    for fam in sorted(data[battery]):
        ds=sorted(BATTERY_DEPTHS[battery])
        gv=0; prev=None
        for d in ds:
            G=legs[(battery,fam,d)]["G"]
            if G is not None and prev is not None and G>prev+1e-12: gv+=1
            if G is not None: prev=G
        flag="FAIL" if gv>0 else "ok"
        if gv>0: b3_fail.append((battery,fam))
        print(f"  {battery}/{fam}: Gviol={gv} {flag}")
print("B3:", "FAIL families:", b3_fail if b3_fail else "none (all zero)")

# ---- B13 underconfidence floor ----
print("=== B13 (G>=-0.100 where n_rel>=8) ===")
b13_fail=[]
for k,v in sorted(legs.items()):
    if v["nrel"]>=8 and v["G"] is not None and v["G"]<-0.100-1e-12:
        b13_fail.append((k,v["G"]))
        print(f"  FAIL {k}: G={v['G']:.4f} nrel={v['nrel']}")
print("B13:", "FAIL" if b13_fail else "PASS (no violations)")

# ---- B12 G>0 crossings (recorded) ----
print("=== B12 G>0 crossings ===")
for battery in sorted(data):
    for fam in sorted(data[battery]):
        ds=sorted(BATTERY_DEPTHS[battery]); cross=0
        for d in ds:
            G=legs[(battery,fam,d)]["G"]
            if G is not None and G>0: cross+=1
        if cross: print(f"  {battery}/{fam}: {cross} depths with G>0")

# ---- B4 aggregate meanConfCorrect ----
num=den=0
for k,v in legs.items():
    if v["mcc"] is not None:
        num+=v["mcc"]*v["ncc"]; den+=v["ncc"]
b4=num/den if den else float("nan")
print(f"=== B4 aggregate meanConfCorrect = {b4:.4f} (thr >=0.50) -> {'PASS' if b4>=0.50 else 'FAIL'}")

# ---- B4b honest-family floor ----
print("=== B4b per honest family (n_rel_correct>=10) ===")
for battery in sorted(data):
    for fam in sorted(data[battery]):
        if fam not in HONEST: continue
        cc=[]
        for d in BATTERY_DEPTHS[battery]:
            cc+= [f/1000.0 for iid,dd in data[battery][fam].items() if d in dd
                  for (c,f,r) in [dd[d]] if c=="1"]
        if len(cc)>=10:
            m=sum(cc)/len(cc)
            print(f"  {battery}/{fam}: n={len(cc)} meanC={m:.4f} -> {'PASS' if m>=0.50 else 'FAIL'}")
        else:
            print(f"  {battery}/{fam}: n={len(cc)} (<10, bar n/a)")

# ---- B5 separation ----
numc=denc=numw=denw=0
for k,v in legs.items():
    if v["mcc"] is not None: numc+=v["mcc"]*v["ncc"]; denc+=v["ncc"]
    if v["mcw"] is not None: numw+=v["mcw"]*v["ncw"]; denw+=v["ncw"]
b5=numc/denc-numw/denw
print(f"=== B5 separation = {b5:.4f} (thr >=0.20) -> {'PASS' if b5>=0.20 else 'FAIL'}")

# ---- B6 recall vs M4 ----
print("=== B6 released-correct / M4 released-correct per family ===")
m4=defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
for battery,depths in BATTERY_DEPTHS.items():
    for d in depths:
        for fn in glob.glob(os.path.join(M4R,f"{battery}_m4_d{d}_A.tsv")):
            for line in open(fn):
                line=line.rstrip("\n")
                if not line: continue
                c=line.split("\t")
                m4[battery][family_of(battery,c[0])][c[0]][int(c[1])]=(c[7],c[6])
for battery in sorted(data):
    for fam in sorted(data[battery]):
        n_f=n_m=0
        for iid,dd in data[battery][fam].items():
            for d,(c,f,r) in dd.items():
                if c=="1": n_f+=1
                mc=m4[battery][fam].get(iid,{}).get(d)
                if mc and mc[0]=="1": n_m+=1
        ratio=n_f/n_m if n_m else float("nan")
        print(f"  {battery}/{fam}: F22={n_f} M4={n_m} ratio={ratio:.4f} -> {'PASS' if ratio>=0.95 else 'FAIL'}")

# ---- B7 abstention volume ----
tot_cells=abst=0
for battery in data:
    for fam in data[battery]:
        for iid,dd in data[battery][fam].items():
            for d,(c,f,r) in dd.items():
                tot_cells+=1
                if c=="A": abst+=1
print(f"=== B7 abstained/total = {abst}/{tot_cells} = {abst/tot_cells:.4f} (thr <=0.30) -> {'PASS' if abst/tot_cells<=0.30 else 'FAIL'}")

# ---- B9 release+correct identity vs M4 ----
print("=== B9 release+correct identity vs M4 ===")
mm=tot9=0
for battery in sorted(data):
    for fam in sorted(data[battery]):
        for iid,dd in data[battery][fam].items():
            for d,(c,f,r) in dd.items():
                tot9+=1
                mc=m4[battery][fam].get(iid,{}).get(d)
                if mc and (r,c)==(mc[1],mc[0]): mm+=1
print(f"  identical {mm}/{tot9} = {mm/tot9:.4f} -> {'PASS' if mm==tot9 else 'FAIL'}")

# ---- B1/B2 summary ----
print(f"=== B1 1->0 transitions = {n10} (thr 0) -> {'PASS' if n10==0 else 'FAIL'}")
print(f"=== B2 V1={v1} V2={v2} (thr 0) -> {'PASS' if v1==0 and v2==0 else 'FAIL'}")
print(f"=== B3pi per-item violations = {b3pi_viol}/{b3pi_tot} (recorded)")

# ---- F22 kill bar (a): per-leg n_rel and V1+V2 ----
print("=== F22 kill bar (a): legs with n_rel>=16 and per-leg V1+V2 ===")
for battery in sorted(data):
    for fam in sorted(data[battery]):
        for d in BATTERY_DEPTHS[battery]:
            # transitions INTO d from previous depth
            ds=sorted(BATTERY_DEPTHS[battery]); i=ds.index(d)
            if i==0: continue
            d0=ds[i-1]; lv1=lv2=0; nrel=legs[(battery,fam,d)]["nrel"]
            for iid,dd in data[battery][fam].items():
                if d0 in dd and d in dd:
                    c0,f0,_=dd[d0]; c1,f1,_=dd[d]
                    if c0=="1" and c1=="0" and f1>=f0: lv1+=1
                    if c0=="0" and c1=="0" and f1>f0: lv2+=1
            if nrel>=16 and lv1+lv2>0:
                print(f"  KILL-TRIGGER {battery}/{fam} d{d}: n_rel={nrel} V1={lv1} V2={lv2}")
print("  (no output above = no kill trigger)")
