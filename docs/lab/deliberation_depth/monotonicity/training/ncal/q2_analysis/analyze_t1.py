#!/usr/bin/env python3
"""T1: principle-vs-bar. M1 crater, M2 sparing vs m11's stated rule, M3 B13 cost."""
import sys
sys.path.insert(0, ".")
from sim_m11 import run as sim_run

_, diag = sim_run("trap_t1.tsv")  # stated-rule diagnostics (m11's rule)
# diag: (iid,depth,class_rate_mil,cp,tp,p_raw_mil,conf_mil)
stated = {(iid,depth): cm//1000 for iid,depth,cr,cp,tp,pr,cm in diag}

def load(fn):
    d = {}
    for line in open(fn):
        c = line.rstrip("\n").split("\t")
        d[(c[0],int(c[2]))] = (int(c[4]),int(c[5]))  # -> (correct, conf)
    return d

print("variant | M1 crater (C-T@d2) | C@d2 | T@d2 | M1pass | max sparing (correct,tp>=1) | M3 B13viol")
for v in ["m11","floor","u1","u2","g","eb","ind"]:
    d = load(f"results/{v}_trap_t1_A.tsv")
    c2 = [d[(f"T1C-{n:03d}",2)][1] for n in range(1,13)]
    t2 = [d[(f"T1T-{n:03d}",2)][1] for n in range(1,13)]
    mc, mt = sum(c2)/len(c2)/1000, sum(t2)/len(t2)/1000
    crater = mc-mt
    m1pass = crater >= 0.90*mc
    # sparing: conf_variant - STATED_m11 on correct cells with tp>=1
    sp = 0
    for (iid,depth), s in stated.items():
        corr, conf = d[(iid,depth)]
        _,_,cr,cp,tp,pr,cm = [x for x in diag if x[0]==iid and x[1]==depth][0]
        if corr==1 and tp>=1:
            if conf - s > sp: sp = conf - s
    # M3: B13-style violations on t1trap family per depth (n_rel>=8)
    import collections
    by_d = collections.defaultdict(list)
    for (iid,depth),(corr,conf) in d.items():
        by_d[depth].append((corr,conf))
    b13 = sum(1 for dep,cells in by_d.items() if len(cells)>=8
              and sum(c[1] for c in cells)/len(cells)/1000 - sum(c[0] for c in cells)/len(cells) < -0.100)
    print(f"{v:5s} | {crater:+.3f} | {mc:.3f} | {mt:.3f} | {m1pass} | {sp:+d} | {b13}")
