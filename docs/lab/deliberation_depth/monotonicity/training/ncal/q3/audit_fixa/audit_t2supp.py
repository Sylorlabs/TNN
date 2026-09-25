#!/usr/bin/env python3
"""T2-SUPP (FIX-A audit): cap-level binding on FIX-A-augmented trap_t1.
For every cell with tp>=1 and deficit>0 (class_rate > p_raw), the cap binds
iff conf_mil < class_rate_mil. Tabulate bind rate by current correctness.
m11's stated principle: binds identically regardless of correctness.
Usage: audit_t2supp.py <trap_t1_FIXA.tsv>
"""
import sys
sys.path.insert(0, "/home/hatch/workspace/tnn-lab/deliberation_depth/monotonicity/training/ncal/q2_analysis")
from sim_m11 import run as sim_run

in_tsv = sys.argv[1]
corr = {}
for line in open(in_tsv):
    c = line.rstrip("\n").split("\t")
    if c[5] == "1" and c[0].startswith("T1"):
        corr[(c[0], int(c[2]))] = int(c[6])
_, diag = sim_run(in_tsv)
tab = {}
for iid, dep, cr, cp, tp, pr, cm in diag:
    if not iid.startswith("T1"):
        continue
    if tp >= 1 and pr >= 0 and cr > pr:  # deficit > 0
        bound = 1 if cm < cr else 0
        k = (corr[(iid, dep)], bound)
        tab[k] = tab.get(k, 0) + 1
for cc in (1, 0):
    z = tab.get((cc, 0), 0); o = tab.get((cc, 1), 0)
    print(f"deficit>0 & {'correct' if cc else 'wrong  '}: cap-bound {o}/{z+o} = {o/(z+o) if z+o else 0:.3f}")
ok = all(tab.get((cc, 0), 0) == 0 for cc in (0, 1))
print("T2-SUPP FIX-A:", "BINDS-UNIFORMLY (calibrating)" if ok else "SELECTIVE (gaming)")
