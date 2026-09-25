#!/usr/bin/env python3
"""B2/B3/B4/B4b/B5/B13 from analyzer-format legs (frozen bar semantics)."""
import sys, glob, os, collections
legsdir, mech = sys.argv[1], sys.argv[2]
# data[fam][iid][depth] = (correct, conf)
data = collections.defaultdict(lambda: collections.defaultdict(dict))
for fn in glob.glob(os.path.join(legsdir, f"*_m{mech}_d*_A.tsv")):
    base = os.path.basename(fn)
    battery = base.split(f"_m{mech}_")[0]
    for line in open(fn):
        c = line.rstrip("\n").split("\t")
        if not c[0]: continue
        iid, dep = c[0], int(c[1])
        fam = battery
        if battery=="ceiling":
            p = iid.split("-")
            fam = p[1] if len(p)>=2 and p[0]=="H5B" else "ceiling?"
        if c[7] in ("1","0"):
            data[fam][iid][dep] = (c[7], int(c[8]))
V1=V2=n10=0
cc=[]; cw=[]
b13=0
gviol=0
for fam, items in data.items():
    cb_d = collections.defaultdict(list)
    for iid, dd in items.items():
        seq = sorted(dd.items())
        for i in range(len(seq)-1):
            (d0,(c0,f0)),(d1,(c1,f1)) = seq[i], seq[i+1]
            if c0=="1" and c1=="0":
                n10+=1
                if f1>=f0: V1+=1
            if c0=="0" and c1=="0" and f1>f0: V2+=1
        for d,(co,cf) in seq:
            cb_d[d].append((co,cf))
            (cc if co=="1" else cw).append(cf)
    ds = sorted(cb_d)
    G = {}
    for d in ds:
        cells = cb_d[d]
        G[d] = sum(f for _,f in cells)/len(cells)/1000 - sum(1 for co,_ in cells if co=="1")/len(cells)
        if len(cells)>=8 and G[d] < -0.100: b13+=1
    for i in range(len(ds)-1):
        if G[ds[i+1]] > G[ds[i]] + 1e-12: gviol+=1
B4 = sum(cc)/len(cc)/1000 if cc else 0
B5 = B4 - (sum(cw)/len(cw)/1000 if cw else 0)
print(f"B1(1->0)={n10} B2:V1={V1} V2={V2} B3 Gviol={gviol} B4={B4:.3f} B5={B5:.3f} B13={b13}")
