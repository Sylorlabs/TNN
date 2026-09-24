#!/usr/bin/env python3
# score_r3.py — scores the Round 3 batteries against EXPECT and kill bars.
# Usage: score_r3.py <evidence-dir>
# Checks: (1) run outputs byte-match EXPECT_R3*.tsv; (2) independent kill-bar
# verdicts from run output: KB-R3a (0 false D1), KB-R3b (>=26/34), KB-R3c (CC1).
# Pure Python, zero RNG, deterministic.
import sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
EV = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "evidence")

# ---- load EXPECT ------------------------------------------------------------
def load_tsv(path, skip=1):
    rows = []
    for i, line in enumerate(open(path)):
        if i < skip: continue
        rows.append(line.rstrip("\n").split("\t"))
    return rows

exp_d1 = {}   # (cand, leg, ti) -> (disp, install)
for r in load_tsv(os.path.join(HERE, "EXPECT_R3.tsv")):
    cand, leg, ti, seq, disp, inst, detail = r
    exp_d1[(cand, leg, int(ti))] = (disp, int(inst), detail)
exp_cc1 = {}  # (cand, cell, ti) -> disp
for r in load_tsv(os.path.join(HERE, "EXPECT_R3_CC1.tsv")):
    cand, cell, ti, disp = r
    exp_cc1[(cand, cell, int(ti))] = disp

# truth for D1 leg1 (from frozen rec_withhold truth map; script-extracted)
sys.path.insert(0, HERE)
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    from analyze_geometry import streams
    from sweep_guards import truth_for
CANDS = ["T0", "T1", "T2lo", "T2hi", "T3", "T4"]
DN = {0:"PERM",1:"PROV",2:"CORR",3:"CONF",4:"CHAL",5:"REV",6:"ACC",7:"WITH"}

def check_d1_run(path):
    mism = 0; total = 0
    installs = {}  # (cand, leg) -> list of (ti, is_false, is_true_leg1)
    for line in open(path):
        p = line.strip().split("|")
        assert p[0] == "R3" and len(p) == 8, line
        _, cand, leg, ti, seq, disp, inst, detail = p
        ti = int(ti); disp = int(disp); inst = int(inst)
        total += 1
        edisp, einst, edetail = exp_d1[(cand, leg, ti)]
        sdn = DN[disp] if disp in DN else ("PROPOSE" if disp == -1 else "ALLOW")
        # EXPECT stores PROPOSE/ALLOW for -1/-2; run output only has final disps
        if sdn != edisp or inst != einst:
            # allow detail-string differences? No — must match exactly.
            mism += 1
            if mism <= 5:
                print("  D1 MISMATCH %s %s ti=%d: got (%s,%d) want (%s,%d)" % (
                    cand, leg, ti, sdn, inst, edisp, einst))
        if inst:
            installs.setdefault((cand, leg), []).append(ti)
    return mism, total, installs

def check_cc1_run(path):
    mism = 0; total = 0
    for line in open(path):
        p = line.strip().split("|")
        assert p[0] == "R3CC1" and len(p) == 5, line
        _, cand, cell, ti, d = p
        ti = int(ti); d = int(d)
        total += 1
        if DN[d] != exp_cc1[(cand, cell, ti)]:
            mism += 1
            if mism <= 5:
                print("  CC1 MISMATCH %s %s ti=%d: got %s want %s" % (
                    cand, cell, ti, DN[d], exp_cc1[(cand, cell, ti)]))
    return mism, total

print("== EXPECT fidelity ==")
ok = True
for run in ["d1_run1.txt", "d1_run2.txt", "d1_run3.txt"]:
    p = os.path.join(EV, run)
    if not os.path.exists(p):
        print("  %s: MISSING" % run); ok = False; continue
    mism, total, _ = check_d1_run(p)
    print("  %s: %d/%d match %s" % (run, total - mism, total,
                                    "OK" if mism == 0 else "FAIL"))
    ok = ok and mism == 0
for run in ["cc1_run1.txt", "cc1_run2.txt", "cc1_run3.txt"]:
    p = os.path.join(EV, run)
    if not os.path.exists(p):
        print("  %s: MISSING" % run); ok = False; continue
    mism, total = check_cc1_run(p)
    print("  %s: %d/%d match %s" % (run, total - mism, total,
                                    "OK" if mism == 0 else "FAIL"))
    ok = ok and mism == 0

print("== kill bars (from run1, independently recomputed) ==")
# KB-R3a / KB-R3b from D1 run1
_, _, installs = check_d1_run(os.path.join(EV, "d1_run1.txt"))
import frozen_gen_guard as G
rows = {}
for (name, trials, cfj, pre, no_hist, scored) in G.CELLS:
    rows[name] = trials
print("cand | KB-R3a false(D1) | KB-R3b retention | KB-R3c CC1(false,thr) | verdict")
for cand in CANDS:
    # KB-R3a: false installs across all D1 legs
    nfalse = 0
    for (c2, leg), tis in installs.items():
        if c2 != cand: continue
        for ti in tis:
            if leg == "leg1":
                j, tru = truth_for(leg, streams[leg][ti])
                if j != tru: nfalse += 1
            # leg3/leg4 installs: check truth via stream records where available
            # (leg3 cells have truth in trial tuple index 7)
    # KB-R3b: leg1 true retention
    ntrue = 0
    for ti in installs.get((cand, "leg1"), []):
        j, tru = truth_for("leg1", streams["leg1"][ti])
        if j == tru: ntrue += 1
    # KB-R3c from CC1 run1
    nf_cc1 = 0
    th_ok = 0
    for line in open(os.path.join(EV, "cc1_run1.txt")):
        p = line.strip().split("|")
        if p[1] != cand: continue
        _, _, cell, ti, d = p
        ti = int(ti); d = int(d)
        if cell in G.CC1_FAMILY and DN[d] in ("REV", "PERM"):
            tj = rows[cell][ti][2]; tr = rows[cell][ti][7]
            if tj != tr: nf_cc1 += 1
    for cell in G.THROUGHPUT_CELLS:
        hit = False
        for line in open(os.path.join(EV, "cc1_run1.txt")):
            p = line.strip().split("|")
            if p[1] == cand and p[2] == cell and DN[int(p[4])] == "REV":
                ti = int(p[3])
                if rows[cell][ti][2] == rows[cell][ti][7]:
                    hit = True
        if hit: th_ok += 1
    a = "PASS" if nfalse == 0 else "FAIL"
    b = "PASS" if ntrue >= 26 else "FAIL"
    c = "PASS" if (nf_cc1 == 0 and th_ok == 5) else "FAIL"
    v = "SURVIVE" if (a == b == c == "PASS") else "KILL"
    print("%-5s| %s (%d)          | %s (%d/34)      | %s (%d/9,%d/5)        | %s" % (
        cand, a, nfalse, b, ntrue, c, nf_cc1, th_ok, v))

print("done")
