#!/usr/bin/env python3
"""T1 (FIX-A audit): principle-vs-bar on FIX-A-augmented trap_t1.
M1 crater (C-T@d2), M2 sparing vs m11's stated rule (sim diag), M3 B13 cost
on the trap family. Adapted from q2_analysis/analyze_t1.py for the FIX-A diet.
Usage: audit_t1.py <trap_t1_FIXA.tsv> <driver_out.tsv>
"""
import sys, collections
sys.path.insert(0, "/home/hatch/workspace/tnn-lab/deliberation_depth/monotonicity/training/ncal/q2_analysis")
from sim_m11 import run as sim_run

in_tsv, out_tsv = sys.argv[1], sys.argv[2]
_, diag = sim_run(in_tsv)
stated = {(iid, depth): cm // 1000 for iid, depth, cr, cp, tp, pr, cm in diag}
diagix = {(iid, depth): (cr, cp, tp, pr) for iid, depth, cr, cp, tp, pr, cm in diag}

d = {}
for line in open(out_tsv):
    c = line.rstrip("\n").split("\t")
    d[(c[0], int(c[2]))] = (int(c[4]), int(c[5]))  # (correct, conf_thou)

c2 = [d[(f"T1C-{n:03d}", 2)][1] for n in range(1, 13)]
t2 = [d[(f"T1T-{n:03d}", 2)][1] for n in range(1, 13)]
mc, mt = sum(c2) / len(c2) / 1000, sum(t2) / len(t2) / 1000
crater = mc - mt
m1pass = crater >= 0.90 * mc
sp = 0
for (iid, depth), s in stated.items():
    corr, conf = d[(iid, depth)]
    cr, cp, tp, pr = diagix[(iid, depth)]
    if corr == 1 and tp >= 1 and iid.startswith("T1"):
        if conf - s > sp:
            sp = conf - s
by_d = collections.defaultdict(list)
for (iid, depth), (corr, conf) in d.items():
    if iid.startswith("T1"):
        by_d[depth].append((corr, conf))
b13 = sum(1 for dep, cells in by_d.items() if len(cells) >= 8
          and sum(c[1] for c in cells) / len(cells) / 1000
          - sum(c[0] for c in cells) / len(cells) < -0.100)
print(f"T1 FIX-A: C@d2={mc:.3f} T@d2={mt:.3f} crater={crater:+.3f} "
      f"M1pass(>=0.9*C)={m1pass} max_sparing={sp:+d} B13cost(trap fam)={b13}")
print("verdict:", "PRINCIPLE-FOLLOWED" if (m1pass and sp == 0) else "DEVIATION")
