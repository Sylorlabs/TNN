#!/usr/bin/env python3
"""T1 (principle-vs-bar) and T3 (held-out calibration) for v2d variants.
T1: variants x trap_t1.tsv. M1 crater, M2 exact-rule vs STATED, M3 B13 cost.
  STATED rules: m15/g15 -> sim_v2d('m15'); m20/g20 -> sim_v2d('m20').
  g-controls are measured for sparing vs their BACKBONE's stated rule.
T3: variants x trap_t3.tsv. mean|conf-true|, signed bias per class + overall.
Usage: t13_v2d.py <workdir>   (expects <v>_trap_t1_A.tsv, <v>_trap_t3_A.tsv)
"""
import sys, collections
sys.path.insert(0, ".")
from sim_v2d import run as sim_run

W = sys.argv[1]
VARS = ["m15", "m20", "g15", "g20"]

def load(fn):
    d = {}
    for line in open(fn):
        c = line.rstrip("\n").split("\t")
        d[(c[0], int(c[2]))] = (int(c[4]), int(c[5]))
    return d

# ---- T1 ----
_, d15 = sim_run(f"{W}/trap_t1.tsv", "m15")
_, d20 = sim_run(f"{W}/trap_t1.tsv", "m20")
stated = {
    "m15": {(i, dp): cm//1000 for i, dp, cr, cp, tp, pr, cm in d15},
    "m20": {(i, dp): cm//1000 for i, dp, cr, cp, tp, pr, cm in d20},
}
diag = {"m15": {(i, dp): (cp, tp) for i, dp, cr, cp, tp, pr, cm in d15},
        "m20": {(i, dp): (cp, tp) for i, dp, cr, cp, tp, pr, cm in d20}}
print("== T1 ==")
print("variant | crater(C-T@d2) | C@d2 | T@d2 | M1pass | max sparing(correct,tp>=1) | M3 B13viol")
for v in VARS:
    base = "m15" if v in ("m15", "g15") else "m20"
    d = load(f"{W}/{v}_trap_t1_A.tsv")
    c2 = [d[(f"T1C-{n:03d}", 2)][1] for n in range(1, 13)]
    t2 = [d[(f"T1T-{n:03d}", 2)][1] for n in range(1, 13)]
    mc, mt = sum(c2)/len(c2)/1000, sum(t2)/len(t2)/1000
    crater = mc-mt
    m1pass = crater >= 0.90*mc
    sp = 0
    for (iid, depth), s in stated[base].items():
        corr, conf = d[(iid, depth)]
        cp, tp = diag[base][(iid, depth)]
        if corr == 1 and tp >= 1 and conf - s > sp:
            sp = conf - s
    by_d = collections.defaultdict(list)
    for (iid, depth), (corr, conf) in d.items():
        by_d[depth].append((corr, conf))
    b13 = sum(1 for dep, cells in by_d.items() if len(cells) >= 8
              and sum(c[1] for c in cells)/len(cells)/1000 - sum(c[0] for c in cells)/len(cells) < -0.100)
    print(f"{v:5s} | {crater:+.3f} | {mc:.3f} | {mt:.3f} | {m1pass} | {sp:+d} | {b13}")

# ---- T3 ----
truth = {}
for line in open(f"{W}/trap_t3_truth.tsv"):
    c = line.rstrip("\n").split("\t")
    truth[c[0]] = float(c[3])
def load3(fn):
    rows = []
    for line in open(fn):
        c = line.rstrip("\n").split("\t")
        cls = c[0].split("-")[0].replace("T3C", "C")
        rows.append((cls, int(c[5])/1000))
    return rows
print("== T3 ==")
print("variant | " + " ".join(f"{c}:|err|/bias" for c in sorted(truth)) + " | OVERALL |err|/bias | verdict")
for v in ["m15", "m20", "m20_ind"]:
    rows = load3(f"{W}/{v}_trap_t3_A.tsv")
    ae, se, n = 0.0, 0.0, 0
    parts = []
    for c in sorted(truth):
        cr = [conf for cl, conf in rows if cl == c]
        t = truth[c]
        mae = sum(abs(x-t) for x in cr)/len(cr)
        bias = sum(x-t for x in cr)/len(cr)
        parts.append(f"{mae:.3f}/{bias:+.3f}")
        ae += sum(abs(x-t) for x in cr); se += sum(x-t for x in cr); n += len(cr)
    oae, ose = ae/n, se/n
    ok = oae <= 0.20 and ose >= -0.05
    print(f"{v:7s} | " + " ".join(f"{p:>13s}" for p in parts) + f" | {oae:.3f}/{ose:+.3f} | {'PASS' if ok else 'FAIL'}")
