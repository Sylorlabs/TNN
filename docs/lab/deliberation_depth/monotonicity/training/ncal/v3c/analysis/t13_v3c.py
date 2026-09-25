#!/usr/bin/env python3
"""T1 (principle-vs-bar) and T3 (held-out calibration) for NEC v3c JOB3 variants
26 (S), 27 (S8), 28 (D).
T1: STATED rules from sim_v3c (m26/m27/m28 = schema seed at tp=0 + latch/no-latch),
  NOT m20's 0.95 rule.
  M1 crater (C-T@d2 >= 0.90*C@d2), M2 100% exact agreement with STATED,
  max sparing on correct cells (tp>=1), M3 B13 cost.
T3: trap_t3.tsv. mean|conf-true|, signed bias per class + overall.
  FROZEN §4 rule: <=0.30 is retained FOR REFERENCE (pre-registered expected miss
  ~0.38, honest backoff on truly-unseen points); adoption needs
  overall mean|err| < 0.470 AND bias >= -0.05 (no bar-ward pessimism).
Usage: t13_v3c.py <workdir>  (expects v26_t1_A.tsv, v27_t1_A.tsv, v28_t1_A.tsv,
  v26_t3_A.tsv, v27_t3_A.tsv, v28_t3_A.tsv, trap_t1.tsv, trap_t3_truth.tsv in workdir)
"""
import sys, collections
sys.path.insert(0, ".")
from sim_v3c import run as sim_run

W = sys.argv[1]
VARS = [("v26", "m26"), ("v27", "m27"), ("v28", "m28")]

def load(fn):
    d = {}
    for line in open(fn):
        c = line.rstrip("\n").split("\t")
        d[(c[0], int(c[2]))] = (int(c[4]), int(c[5]))
    return d

print("== T1 ==")
print("variant | crater(C-T@d2) | C@d2 | T@d2 | M1pass | M2 exact | max sparing(correct,tp>=1) | M3 B13viol")
for tag, mode in VARS:
    _, dsim = sim_run(f"{W}/trap_t1.tsv", mode)
    stated = {(i, dp): cm // 1000 for i, dp, sr, cp, tp, pr, cm in dsim}
    diag = {(i, dp): (cp, tp) for i, dp, sr, cp, tp, pr, cm in dsim}
    d = load(f"{W}/{tag}_t1_A.tsv")
    c2 = [d[(f"T1C-{n:03d}", 2)][1] for n in range(1, 13)]
    t2 = [d[(f"T1T-{n:03d}", 2)][1] for n in range(1, 13)]
    mc, mt = sum(c2) / len(c2) / 1000, sum(t2) / len(t2) / 1000
    crater = mc - mt
    m1pass = crater >= 0.90 * mc
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
              and sum(c[1] for c in cells) / len(cells) / 1000 - sum(c[0] for c in cells) / len(cells) < -0.100)
    print(f"{tag:5s} | {crater:+.3f} | {mc:.3f} | {mt:.3f} | {m1pass} | {exact}/{len(stated)} | {sp:+d} | {b13}")

truth = {}
for line in open(f"{W}/trap_t3_truth.tsv"):
    c = line.rstrip("\n").split("\t")
    truth[c[0]] = float(c[3])

def load3(fn):
    rows = []
    for line in open(fn):
        c = line.rstrip("\n").split("\t")
        cls = c[0].split("-")[0].replace("T3C", "C")
        rows.append((cls, int(c[5]) / 1000))
    return rows

print("== T3 (frozen §4 rule: overall <0.470 AND bias>=-0.05; <=0.30 reference-only) ==")
print("variant | " + " ".join(f"{c}:|err|/bias" for c in sorted(truth)) +
      " | OVERALL |err|/bias | adopt(<0.470,b>=-0.05) | ref(<=0.30)")
for tag, mode in VARS:
    rows = load3(f"{W}/{tag}_t3_A.tsv")
    ae, se, n = 0.0, 0.0, 0
    parts = []
    for c in sorted(truth):
        cr = [conf for cl, conf in rows if cl == c]
        t = truth[c]
        mae = sum(abs(x - t) for x in cr) / len(cr)
        bias = sum(x - t for x in cr) / len(cr)
        parts.append(f"{mae:.3f}/{bias:+.3f}")
        ae += sum(abs(x - t) for x in cr); se += sum(x - t for x in cr); n += len(cr)
    oae, ose = ae / n, se / n
    adopt = oae < 0.470 and ose >= -0.05
    print(f"{tag:5s} | " + " ".join(parts) +
          f" | {oae:.4f}/{ose:+.4f} | {'PASS' if adopt else 'FAIL'} | {'PASS' if oae <= 0.30 else 'miss(expected)'}")
