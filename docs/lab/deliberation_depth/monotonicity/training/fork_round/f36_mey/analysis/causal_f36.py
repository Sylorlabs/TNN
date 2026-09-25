#!/usr/bin/env python3
"""F36 MEY causal test (kill (a)): family yield <-> C-slope.

Prereg §3 F36 kill: "nondecreasing-f5 items still show C-slope >
accuracy-slope at n>=30 (causal claim wrong)".

Method (per family):
  1. Load sidecars: id depth t correct rel f1 f5 my y m C0 C (12 cols).
  2. Subset S = items whose f5 is nondecreasing across adjacent released
     depths (f5(d+1) >= f5(d)).
  3. Qualifying depth cells: (family, depth) with n_rel >= 30 within S.
  4. Per qualifying cell: mean C (emitted, /1000) and mean accuracy.
  5. Least-squares slopes of mean-C and mean-accuracy vs d_idx.
  6. Kill (a) fires iff C-slope > 0 AND C-slope > accuracy-slope.

Also reports, per family: |S|, qualifying cells, per-depth means.
"""
import sys, os, glob, re
from collections import defaultdict

BATTERY_DEPTHS = {"admit":[1,2,4,8,16],"revoke":[1,2,4,8,16],"logic":[1,2,4,8,16],
                  "trap":[1,2,4,8,16],"cost":[1,2,4,8,16],"redteam":[1,2,4,8,16],
                  "ceiling":[1,2,4,8,16,32,64]}

def family_of(battery, iid):
    if battery == "ceiling":
        parts = iid.split("-")
        if len(parts) >= 2 and parts[0] == "H5B":
            return parts[1]
        return "ceiling?"
    return battery

def ls_slope(xs, ys):
    n = len(xs)
    if n < 2: return float("nan")
    mx = sum(xs)/n; my = sum(ys)/n
    den = sum((x-mx)**2 for x in xs)
    if den == 0: return float("nan")
    return sum((x-mx)*(y-my) for x,y in zip(xs,ys))/den

def main():
    resdir = sys.argv[1]
    # per family -> per item -> depth -> (f5, C, acc, rel)
    fam_items = defaultdict(lambda: defaultdict(dict))
    for battery, depths in BATTERY_DEPTHS.items():
        for d in depths:
            pat = os.path.join(resdir, f"{battery}_m36_d{d}_A.feat.tsv")
            for fn in glob.glob(pat):
                for line in open(fn):
                    p = line.rstrip("\n").split("\t")
                    if len(p) < 12: continue
                    iid, depth = p[0], int(p[1])
                    corr, rel = p[3], int(p[4])
                    f5, C = int(p[6]), int(p[11])
                    fam = family_of(battery, iid)
                    # keep one row per (id, depth): t=depth rows are the release rows;
                    # sidecar has one row per (id, depth, t); use the released t row.
                    # Actually sidecar emits one row per t; take max t (the release t).
                    prev = fam_items[(battery,fam)][iid].get(depth)
                    # rows are in t order; later t overwrites -> keep last
                    fam_items[(battery,fam)][iid][depth] = (f5, C, corr, rel)
    print("=== F36 causal test: nondecreasing-f5 subset, C-slope vs accuracy-slope ===")
    any_kill = False
    for key in sorted(fam_items):
        battery, fam = key
        items = fam_items[key]
        # subset S: f5 nondecreasing across released depths
        S = {}
        for iid, dd in items.items():
            rel_depths = sorted(d for d,(f5,C,corr,rel) in dd.items() if rel==1)
            if len(rel_depths) < 2: continue
            f5s = [dd[d][0] for d in rel_depths]
            if all(b >= a for a,b in zip(f5s, f5s[1:])):
                S[iid] = dd
        # qualifying depth cells: n_rel>=30 within S
        depths = BATTERY_DEPTHS[battery]
        qcells = []
        for di, d in enumerate(depths):
            rows = [(dd[d][1], dd[d][2]) for iid, dd in S.items() if d in dd and dd[d][3]==1]
            if len(rows) >= 30:
                mc = sum(c for c,_ in rows)/len(rows)/1000.0
                ma = sum(1 for _,corr in rows if corr=="1")/len(rows)
                qcells.append((di, d, len(rows), mc, ma))
        if len(qcells) < 2:
            print(f"{key}: |S|={len(S)} nondecreasing-f5 items, qualifying cells={len(qcells)} (<2 -> VOID)")
            continue
        xs = [di for di,_,_,_,_ in qcells]
        cs = [mc for _,_,_,mc,_ in qcells]
        ac = [ma for _,_,_,_,ma in qcells]
        sc = ls_slope(xs, cs); sa = ls_slope(xs, ac)
        kill = (sc > 0) and (sc > sa)
        any_kill = any_kill or kill
        print(f"{key}: |S|={len(S)} items, {len(qcells)} qualifying cells (n_rel>=30)")
        for di,d,n,mc,ma in qcells:
            print(f"    d_idx={di} d={d}: n={n} meanC={mc:.4f} meanAcc={ma:.4f}")
        print(f"    C-slope={sc:+.5f}/d_idx  acc-slope={sa:+.5f}/d_idx -> {'KILL (a) FIRES' if kill else 'clear'}")
    print()
    print(f"OVERALL kill (a): {'KILL' if any_kill else 'CLEAR'}")

main()
