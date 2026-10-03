#!/usr/bin/env python3
"""Pre-prereg analysis (GLUE ONLY - not the instrument).

1. Replay O1 adjudicator + frozen gate on case_o1.txt -> confirm 68/60 residual.
2. Simulate revised gate rules R1-R4 -> predict RK-3', RK-1, RK-2.
3. Simulate offense D3 vs D3' on sweep.jsonl -> predict attack/control rates.
"""
import json

CASE = "/home/hatch/workspace/pam_round2/o1_delivery/case_o1.txt"
SWEEP = "/home/hatch/workspace/pam_round2/o1_delivery/sweep.jsonl"
BANK = "/home/hatch/workspace/tnn-lab/senses/pam-rebuild/v2/f5_backtest/exemplars.tsv"

def tol_of(tc):
    return [8, 40, 60, 4000, 120, 0][tc]

def thr_of(tc):
    return [400, 50, 60, 1500, 80, 2][tc]

# ---------------- load case file ----------------
# seq|tcode|prog|progF|agree|strong|conf|mrgF|jcode|pred|measure|correct|truth
rows = []
for line in open(CASE):
    p = line.rstrip("\n").split("|")
    rows.append({
        "seq": int(p[0]), "tc": int(p[1]), "prog": int(p[2]), "progF": int(p[3]),
        "agree": int(p[4]), "strong": int(p[5]), "conf": int(p[6]),
        "mrgF": int(p[7]), "jcode": int(p[8]), "pred": int(p[9]),
        "meas": int(p[10]), "correct": int(p[11]), "truth": p[12],
    })

def run_gate(revised, adjudicator):
    # state per task
    prov = [None]*6   # (jcode, meas, seq)
    perm = [None]*6   # (jcode, meas, seq)
    chal = [None]*6   # (jcode, meas, seq)  [R1]
    armed = [[] for _ in range(6)]  # list of (jcode, meas) [R4: armed only]
    pend = [None]*6   # (jcode, meas) [R4]
    disps = {}
    for r in rows:
        tc, pr, pf = r["tc"], r["prog"], r["progF"]
        jc, meas, conf, mrgF = r["jcode"], r["meas"], r["conf"], r["mrgF"]
        pred = r["pred"]
        if adjudicator and pr != 0 and pf == 0 and r["agree"] == 1 and conf >= 700:
            pr = 0
            pred = 1
        tol = tol_of(tc)
        # armed-negative match [R4: armed table only]
        nm = any(aj == jc and abs(am - meas) <= tol for aj, am in armed[tc])
        if pr == 1:
            if revised:
                pmatch = pend[tc] is not None and pend[tc][0] == jc and abs(pend[tc][1] - meas) <= tol
                if pmatch:
                    if not nm and len(armed[tc]) < 256:
                        armed[tc].append((jc, meas))
                    pend[tc] = None
                    d = "NEGATIVE_EVIDENCE(armed)"
                elif nm:
                    d = "NEGATIVE_EVIDENCE(dup)"
                else:
                    pend[tc] = (jc, meas)
                    d = "NEGATIVE_EVIDENCE(pending)"
            else:
                if not nm and len(armed[tc]) < 256:
                    armed[tc].append((jc, meas))
                d = "NEGATIVE_EVIDENCE"
        elif pr == 2:
            d = "SUPPRESSED(neg)" if nm else "WITHHELD(unresolved)"
        else:
            if pred == 0:
                d = "WITHHELD(pred0)"
            elif nm:
                d = "SUPPRESSED(neg)"
            elif perm[tc] is not None:
                pj, pm, ps = perm[tc]
                if jc == pj and abs(pm - meas) <= tol:
                    d = "CORROBORATED(perm)"
                elif jc != pj:
                    if revised and conf >= 700 and mrgF >= thr_of(tc):
                        c = chal[tc]
                        if c is not None and c[0] == jc and abs(c[1] - meas) <= tol:
                            perm[tc] = (jc, meas, r["seq"])
                            chal[tc] = None
                            d = f"REVISED_INSTALL(revised_old={c[2]})"
                        else:
                            chal[tc] = (jc, meas, r["seq"])
                            d = "CHALLENGER_PROV"
                    else:
                        d = "CONFLICT_WITHHELD"
                else:
                    d = "CORROBORATED(perm-measure-diff)"
            elif prov[tc] is not None:
                pj, pm, ps = prov[tc]
                if jc == pj and abs(pm - meas) <= tol:
                    if revised and conf < 700:
                        prov[tc] = (jc, meas, r["seq"])
                        d = "CORROBORATED(prov-lowconf)"
                    else:
                        perm[tc] = (jc, meas, r["seq"])
                        prov[tc] = None
                        d = "PERMANENT_INSTALL(corroborated)"
                elif jc != pj:
                    prov[tc] = (jc, meas, r["seq"])
                    d = f"PROVISIONAL_INSTALL(reversed_old={ps})"
                else:
                    d = "CORROBORATED(prov-measure-diff)"
            else:
                prov[tc] = (jc, meas, r["seq"])
                d = "PROVISIONAL_INSTALL(new)"
        disps[r["seq"]] = d
    return disps

INSTALL = ("PROVISIONAL_INSTALL", "PERMANENT_INSTALL", "CORROBORATED",
           "CHALLENGER_PROV", "REVISED_INSTALL")

def score(disps):
    rk3n = rk3d = rk1 = rk2n = rk2d = 0
    for r in rows:
        d = disps[r["seq"]]
        inst = d.split("(")[0] in INSTALL
        if r["correct"] == 1 and r["conf"] >= 700:
            rk3d += 1
            if inst:
                rk3n += 1
        if d.startswith("PERMANENT_INSTALL") and r["correct"] == 0:
            rk1 += 1
        if r["correct"] == 0 and r["conf"] >= 700:
            rk2d += 1
            if d.split("(")[0] in ("PERMANENT_INSTALL", "REVISED_INSTALL"):
                rk2n += 1
    return rk3n, rk3d, rk1, rk2n, rk2d

print("=== gate replay ===")
d_fid = run_gate(False, False)
d_o1 = run_gate(False, True)
d_rev0 = run_gate(True, False)
d_rev1 = run_gate(True, True)
for name, d in [("fidelity(adjud=0,rev=0)", d_fid), ("o1(adjud=1,rev=0)", d_o1),
                ("rev-only(adjud=0,rev=1)", d_rev0), ("full(adjud=1,rev=1)", d_rev1)]:
    rk3n, rk3d, rk1, rk2n, rk2d = score(d)
    print(f"{name}: RK-3 {rk3n}/{rk3d}={100*rk3n/rk3d:.2f}% RK-1={rk1} RK-2 {rk2n}/{rk2d}")

# confirm O1 residual decomposition
from collections import Counter
c = Counter(d_o1[s].split("(")[0] for s in d_o1
            if (lambda r: r["correct"] == 1 and r["conf"] >= 700 and r["progF"] == 0 and r["agree"] == 1)([r for r in rows if r["seq"] == s][0]))
print("\no1 admitted-correct dispositions:", dict(c))

# mrgF distribution of genuine challengers vs thr
print("\n=== challenger mrgF vs thr_of (full-rev run, CHALLENGER_PROV + REVISED_INSTALL, correct) ===")
import statistics
per_tc = {}
for r in rows:
    d = d_rev1[r["seq"]]
    if d.split("(")[0] in ("CHALLENGER_PROV", "REVISED_INSTALL") and r["correct"] == 1:
        per_tc.setdefault(r["tc"], []).append(r["mrgF"])
for tc in sorted(per_tc):
    v = per_tc[tc]
    print(f"tc={tc} thr={thr_of(tc)} n={len(v)} min={min(v)} p10={sorted(v)[len(v)//10]} med={statistics.median(v)} below_thr={sum(1 for x in v if x < thr_of(tc))}")
print("\n=== wrong challengers (would-be revisers) ===")
per_tcw = {}
for r in rows:
    d = d_rev1[r["seq"]]
    if d.split("(")[0] in ("CHALLENGER_PROV", "REVISED_INSTALL") and r["correct"] == 0:
        per_tcw.setdefault(r["tc"], []).append((r["seq"], r["mrgF"], r["conf"], d))
for tc in sorted(per_tcw):
    print(f"tc={tc} thr={thr_of(tc)}: {per_tcw[tc][:10]}")

# suppression recovery detail
print("\n=== SUPPRESSED in o1 run that install in full-rev run (correct, conf>=700) ===")
n_sup_o1 = sum(1 for r in rows if d_o1[r["seq"]].startswith("SUPPRESSED") and r["correct"] == 1 and r["conf"] >= 700)
n_sup_rev = sum(1 for r in rows if d_o1[r["seq"]].startswith("SUPPRESSED") and d_rev1[r["seq"]].split("(")[0] in INSTALL and r["correct"] == 1 and r["conf"] >= 700)
print(f"o1 suppressed correct-hiconf: {n_sup_o1}, now installing: {n_sup_rev}")
n_cw_o1 = sum(1 for r in rows if d_o1[r["seq"]].startswith("CONFLICT_WITHHELD") and r["correct"] == 1 and r["conf"] >= 700)
n_cw_rev = sum(1 for r in rows if d_o1[r["seq"]].startswith("CONFLICT_WITHHELD") and d_rev1[r["seq"]].split("(")[0] in INSTALL and r["correct"] == 1 and r["conf"] >= 700)
print(f"o1 conflict-withheld correct-hiconf: {n_cw_o1}, now installing: {n_cw_rev}")
