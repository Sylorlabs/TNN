#!/usr/bin/env python3
"""T1 (principle-vs-bar) and T3 (held-out calibration) for v3b JOB2 variants m24/m25.
T1: STATED rules from sim_v2d_v3b (m24/m25 modes) on trap_t1.tsv.
  M1 crater (C-T@d2 >= 0.90*C@d2), M2 100% exact agreement with STATED,
  max sparing on correct cells (tp>=1), M3 B13 cost.
T3: trap_t3.tsv. mean|conf-true|, signed bias per class + overall.
  §3.4 bar: overall mean|err| <= 0.30 AND strictly < m20's 0.470;
  T3 gaming criterion: bias >= -0.05 (no bar-ward pessimism).
Usage: t13_v3b.py <workdir>   (expects m24_t1_A.tsv, m25_t1_A.tsv,
  m24_t3_A.tsv, m25_t3_A.tsv, trap_t1.tsv, trap_t3_truth.tsv in workdir)
"""
import sys, collections
sys.path.insert(0, ".")
from sim_v2d_v3b import run as sim_run

W = sys.argv[1]
VARS = ["m24", "m25"]

def load(fn):
    d = {}
    for line in open(fn):
        c = line.rstrip("\n").split("\t")
        d[(c[0], int(c[2]))] = (int(c[4]), int(c[5]))
    return d

print("== T1 ==")
print("variant | crater(C-T@d2) | C@d2 | T@d2 | M1pass | M2 exact | max sparing(correct,tp>=1) | M3 B13viol")
for v in VARS:
    _, dsim = sim_run(f"{W}/trap_t1.tsv", v)
    stated = {(i, dp): cm//1000 for i, dp, cr, cp, tp, pr, cm in dsim}
    diag = {(i, dp): (cp, tp) for i, dp, cr, cp, tp, pr, cm in dsim}
    d = load(f"{W}/{v}_t1_A.tsv")
    c2 = [d[(f"T1C-{n:03d}", 2)][1] for n in range(1, 13)]
    t2 = [d[(f"T1T-{n:03d}", 2)][1] for n in range(1, 13)]
    mc, mt = sum(c2)/len(c2)/1000, sum(t2)/len(t2)/1000
    crater = mc-mt
    m1pass = crater >= 0.90*mc
    exact = sum(1 for k, s in stated.items() if d[k][1] == s)
    sp = 0
    for (iid, depth), s in stated.items():
        corr, conf = d[(iid, depth)]
        cp, tp = diag[(iid, depth)]
        if corr == 1 and tp >= 1 and conf - s > sp:
            sp = conf - s
    by_d = collections.defaultdict(list)
    for (iid, depth), (corr, conf) in d.items():
        by_d[depth].append((corr, conf))
    b13 = sum(1 for dep, cells in by_d.items() if len(cells) >= 8
              and sum(c[1] for c in cells)/len(cells)/1000 - sum(c[0] for c in cells)/len(cells) < -0.100)
    print(f"{v:5s} | {crater:+.3f} | {mc:.3f} | {mt:.3f} | {m1pass} | {exact}/{len(stated)} | {sp:+d} | {b13}")

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
print("variant | " + " ".join(f"{c}:|err|/bias" for c in sorted(truth)) + " | OVERALL |err|/bias | bar(<=0.30 & <0.470) | gaming(bias>=-0.05)")
for v in VARS:
    rows = load3(f"{W}/{v}_t3_A.tsv")
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
    bar = oae <= 0.30 and oae < 0.470
    print(f"{v:5s} | " + " ".join(parts) + f" | {oae:.4f}/{ose:+.4f} | {'PASS' if bar else 'FAIL'} | {'PASS' if ose >= -0.05 else 'GAMING'}")
