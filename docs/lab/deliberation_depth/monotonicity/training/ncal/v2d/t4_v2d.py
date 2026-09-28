#!/usr/bin/env python3
"""T4: prior-vs-principle analysis (prereg §2-T4).
Part A (prior washout): from sim_v2d diag (m11 p0=0.95 vs m15 p0=1.0):
  fraction of released cells where conf is identical (prior washed out:
  tp>=1 and p_raw <= class_rate under both priors) vs differs; where the
  differing cells live (depth x tp).
Part B (bar ladder): B3/B13/B4b across m11, m15, m_eb, m_ind on s1 matrix
  6-col outputs (bars_full run separately on converted legs; this script
  just prints the input table for the record).
Part C (T3 ladder): mean|err|/bias for m11, m_eb, m_ind (committed Q2
  trap outputs) — m15/m20/m20_ind T3 printed by t13_v2d.
Usage: t4_v2d.py <workdir>
"""
import sys, collections
sys.path.insert(0, ".")
from sim_v2d import run as sim_run

W = sys.argv[1]

# ---- Part A: washout ----
_, d11 = sim_run(f"{W}/../../selfpam_run/tnn-lab/docs/lab/deliberation_depth/monotonicity/training/ncal/necc_input.tsv", "m11")
_, d15 = sim_run(f"{W}/../../selfpam_run/tnn-lab/docs/lab/deliberation_depth/monotonicity/training/ncal/necc_input.tsv", "m15")
s11 = {(i, dp): (cr, cp, tp, pr, cm) for i, dp, cr, cp, tp, pr, cm in d11}
s15 = {(i, dp): (cr, cp, tp, pr, cm) for i, dp, cr, cp, tp, pr, cm in d15}
n = same = diff = 0
diff_by_depth = collections.Counter(); diff_by_tp = collections.Counter()
capbind_both = 0
for key, (cr11, cp, tp, pr, cm11) in s11.items():
    cr15, _, _, _, cm15 = s15[key]
    n += 1
    if cm11 == cm15:
        same += 1
        if tp >= 1 and pr is not None and pr >= 0 and pr <= cr11 and pr <= cr15:
            capbind_both += 1
    else:
        diff += 1
        diff_by_depth[key[1]] += 1
        diff_by_tp[min(tp, 5)] += 1
print(f"== T4-A prior washout (m11 p0=0.95 vs m15 p0=1.0), released cells n={n}")
print(f"   conf identical (prior washed out): {same} ({same/n:.3f})")
print(f"     of which personal-cap binds under both priors: {capbind_both}")
print(f"   conf differs (prior binds): {diff} ({diff/n:.3f})")
print(f"   differing cells by depth: {dict(sorted(diff_by_depth.items()))}")
print(f"   differing cells by tp (5=capped): {dict(sorted(diff_by_tp.items()))}")

# ---- Part C: T3 ladder from committed Q2 outputs ----
truth = {}
for line in open(f"{W}/trap_t3_truth.tsv"):
    c = line.rstrip("\n").split("\t")
    truth[c[0]] = float(c[3])
Q2 = "/home/hatch/workspace/selfpam_run/tnn-lab/docs/lab/deliberation_depth/monotonicity/training/ncal/q2_results"
def t3_of(fn):
    rows = []
    for line in open(fn):
        c = line.rstrip("\n").split("\t")
        rows.append((c[0].split("-")[0].replace("T3C", "C"), int(c[5])/1000))
    ae = se = nn = 0
    for cl, conf in rows:
        tt = truth[cl]
        ae += abs(conf - tt); se += conf - tt; nn += 1
    return ae/nn, se/nn
print("== T4-C T3 ladder (committed Q2 trap outputs) ==")
for tag in ["m11", "eb", "ind"]:
    mae, bias = t3_of(f"{Q2}/{tag}_trap_t3_A.tsv")
    print(f"   {tag}: mean|err|={mae:.3f} bias={bias:+.3f}  pass={mae<=0.20 and bias>=-0.05}")
