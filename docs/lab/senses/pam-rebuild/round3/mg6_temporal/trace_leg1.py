#!/usr/bin/env python3
"""trace_leg1.py — full leg1 stream trace with gate dispositions and history.

Shows WHY only 7 proposals form, and what a set-level statistic could see.
"""
import sys
sys.path.insert(0, "/home/hatch/workspace/pam_round3/mg6_temporal")
from analyze_geometry import (streams, gtags, run_stream, guard_arms,
                              TOLS, D_PERM, D_PROV, D_CORR, D_CONF, D_CHAL,
                              D_REV, D_ACC, D_WITH)
import importlib

DNAMES = {0: "PERM", 1: "PROV", 2: "CORR", 3: "CONF", 4: "CHAL",
          5: "REV", 6: "ACC", 7: "WITH"}

V2 = "/home/hatch/workspace/tnn-lab/senses/pam-rebuild/v2"
rec_info = {}
for line in open(V2 + "/redteam/evidence/rec_withhold.records"):
    f = line.rstrip("\n").split("|")
    rec_info[f[2]] = (f[5], f[10], int(f[6]))  # fixture -> (judgment, truth, conf)

out = run_stream(streams["leg1"], gtags["leg1"], guard_arms)
print("idx seq tcode jcode conf meas   truth  disp detail")
for ti, t in enumerate(streams["leg1"]):
    j, tru, conf = rec_info[t["fixture"]]
    disp, detail, inst = out[ti][1], out[ti][2], out[ti][3]
    mark = " <-- install" if inst else ""
    print("%3d %3d t%d %-9s %4d %5d %-8s %-4s %s%s" % (
        ti, t["seq"], t["tcode"], j, t["conf"], t["meas"], tru,
        DNAMES[disp] if isinstance(disp, int) else disp, detail, mark))
