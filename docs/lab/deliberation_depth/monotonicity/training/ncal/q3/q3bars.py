#!/usr/bin/env python3
"""B13 exact counter + bar summary for a converted leg directory.
Usage: q3bars.py <legdir> <mech>
Prints B13 violations (G < -0.100, n_rel>=8) and frozen-analyzer-style totals.
"""
import os, sys, glob
from collections import defaultdict

def main():
    d, mech = sys.argv[1], sys.argv[2]
    cells = defaultdict(list)
    for fn in glob.glob(os.path.join(d, f"*_m{mech}_d*_A.tsv")):
        base = os.path.basename(fn)
        parts = base.split(f"_m{mech}_d")
        fam = parts[0]; depth = int(parts[1].split("_")[0])
        with open(fn) as f:
            for line in f:
                c = line.rstrip("\n").split("\t")
                if c[6] == "RELEASE" and c[7] in ("0", "1"):
                    cells[(fam, depth)].append((int(c[7]), int(c[8]) / 1000))
    nv = 0
    for (fam, depth), v in sorted(cells.items()):
        n = len(v)
        if n < 8:
            continue
        acc = sum(x[0] for x in v) / n
        mc = sum(x[1] for x in v) / n
        G = mc - acc
        if G < -0.100:
            nv += 1
            print(f"  VIOL {fam} d{depth}: n={n} acc={acc:.3f} mc={mc:.4f} G={G:.4f}")
    print(f"B13 violations: {nv}")

if __name__ == "__main__":
    main()
