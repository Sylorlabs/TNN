#!/usr/bin/env python3
"""Convert nec 6-col output (id,fam,depth,release,correct,conf) to analyzer 11-col legs."""
import sys, os, collections
src, outdir, mech = sys.argv[1], sys.argv[2], sys.argv[3]
legs = collections.defaultdict(list)
with open(src) as f:
    for line in f:
        line=line.rstrip("\n")
        if not line: continue
        iid,fam,depth,rel,corr,conf = line.split("\t")
        if rel=="1":
            legs[(fam,depth)].append(f"{iid}\t{depth}\t0\t0\t0\t0\tRELEASE\t{corr}\t{conf}\t0\t0")
        else:
            legs[(fam,depth)].append(f"{iid}\t{depth}\t0\t0\t0\t0\tABSTAIN\tA\t0\t0\t0")
os.makedirs(outdir, exist_ok=True)
for (fam,depth), rows in sorted(legs.items()):
    fn = os.path.join(outdir, f"{fam}_m{mech}_d{depth}_A.tsv")
    with open(fn,"w") as f:
        f.write("\n".join(rows)+"\n")
print("legs:", len(legs), "rows:", sum(len(v) for v in legs.values()))
