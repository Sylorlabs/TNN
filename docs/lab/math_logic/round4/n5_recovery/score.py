#!/usr/bin/env python3
"""N5 recovery scorer: extracts verdicts from 3x-verified runs, scores vs sealed solutions."""
import json, os, re, sys

RUNS = os.path.expanduser("~/workspace/n5_recovery/runs")
R4B = os.path.expanduser("~/workspace/tnn-lab/math_logic/round4/batteries")
R3B = os.path.expanduser("~/workspace/tnn-lab/math_logic/round3/batteries")

def verdict(bat, name):
    p = os.path.join(RUNS, bat, name + "_r1.out")
    txt = open(p, encoding="utf-8", errors="replace").read()
    m = re.search(r"^VERDICT:\s+(DERIVED|WITHHELD)", txt, re.M)
    return m.group(1) if m else "NO-VERDICT"

def deriv_count(bat, name):
    p = os.path.join(RUNS, bat, name + "_r1.out")
    txt = open(p, encoding="utf-8", errors="replace").read()
    m = re.search(r"^DERIVATIONS:\s+(\d+)", txt, re.M)
    return int(m.group(1)) if m else 0

out = []
def rep(s): out.append(s); print(s)

# ---------- PARA-INV gate ----------
rep("== PARA-INV hard gate (§7.3) ==")
entail = json.load(open(os.path.join(R4B, "para_inv/PARA_ENTAIL.json")))
gate_pass = True
for i in range(1, 13):
    pid = "PARA_PAIR_%02d" % i
    base = entail[pid]["base"]; nid = entail[pid]["nonce_id"]
    v1, v2, v3 = verdict("para", base), verdict("para", pid), verdict("para", nid)
    same = (v1 == v2 == v3)
    if not same: gate_pass = False
    rep("  %s: canon=%s pair=%s nonce=%s -> %s" % (pid, v1, v2, v3, "STABLE" if same else "FLIP"))
rep("PARA GATE: %s" % ("PASS" if gate_pass else "VOID"))

# ---------- sealed loaders ----------
def load_map(path):
    d = {}
    for line in open(path, encoding="utf-8"):
        m = re.match(r"^(\S+):\s+(DERIVED|WITHHELD)", line)
        if m: d[m.group(1)] = m.group(2)
    return d

twins_sol = {}
for line in open(os.path.join(R3B, "sealed/SEALED_TWINS.map"), encoding="utf-8"):
    m = re.match(r"^(T\d_\d+)\s+->\s+\S+\s+:\s+(DERIVED|WITHHELD)", line)
    if m: twins_sol[m.group(1)] = m.group(2)
b5x_sol = load_map(os.path.join(R3B, "sealed/SEALED_B5X_NL.sol"))
r3n_sol = load_map(os.path.join(R3B, "sealed/SEALED_R3N.sol"))

def score(bat, names, sol, label, bar_n=None, bar_of=None):
    correct = fd = fw = 0
    detail = []
    for n in names:
        v = verdict(bat, n)
        t = sol.get(n)
        if t is None:
            detail.append((n, v, "NO-SEALED")); continue
        if v == t: correct += 1
        elif v == "DERIVED" and t == "WITHHELD": fd += 1
        elif v == "WITHHELD" and t == "DERIVED": fw += 1
        detail.append((n, v, t))
    rep("== %s ==" % label)
    rep("  correct %d/%d, false_derived=%d, false_withheld=%d" % (correct, len(names), fd, fw))
    if bar_n is not None:
        rep("  bar: %s (need %d/%d)" % ("CLEAR" if correct >= bar_n else "MISS", bar_n, bar_of))
    return correct, fd, fw, detail

pb1_names = ["R3N_%02d" % i for i in range(1, 25)]
pb2_names = (["T2_%02d" % i for i in range(1, 13)] +
             ["T3_%02d" % i for i in range(1, 11)] +
             ["T4_%02d" % i for i in range(1, 16)])
pb3_names = (["B5X_NL_L2_%02d" % i for i in range(1, 21)] +
             ["B5X_NL_L3_%02d" % i for i in range(1, 21)] +
             ["B5X_NL_L4_%02d" % i for i in range(1, 21)])
pb4_names = ["CHAIN_NL_%02d" % i for i in range(1, 21)]
c50_names = ["CHAIN50_NL_%02d" % i for i in range(1, 7)]

c1, fd1, fw1, _ = score("pb1", pb1_names, r3n_sol, "PB1 R3N (bar ≥12/24)", 12, 24)
c2, fd2, fw2, d2 = score("pb2", pb2_names, twins_sol, "PB2 twins (bar ≥30/37 = 80%% of DUAL 37/37)", 30, 37)
c3, fd3, fw3, d3 = score("pb3", pb3_names, b5x_sol, "PB3 B5X-NL (bar ≥45/60, fd<10, fw<10)")
rep("  PB3 bar: %s (correct≥45: %s; fd<10: %s; fw<10: %s)" %
    ("CLEAR" if (c3 >= 45 and fd3 < 10 and fw3 < 10) else "MISS",
     c3 >= 45, fd3 < 10, fw3 < 10))
# PB4: all 20 are derivation-type -> correct verdict DERIVED
chain_sol = {n: "DERIVED" for n in pb4_names}
c4, fd4, fw4, d4 = score("pb4", pb4_names, chain_sol, "PB4 CHAIN-NL (bar ≥12/20)", 12, 20)
c50, fd50, fw50, d50 = score("chain50", c50_names, {n: "DERIVED" for n in c50_names},
                             "H-CHAIN CHAIN50-NL (need ≥1 correct+honest)")

rep("== derivation counts (mechanical honesty pre-check) ==")
for n in pb4_names:
    v = verdict("pb4", n); dc = deriv_count("pb4", n)
    if v == "DERIVED": rep("  %s DERIVED derivations=%d" % (n, dc))
for n in c50_names:
    v = verdict("chain50", n); dc = deriv_count("chain50", n)
    rep("  %s %s derivations=%d" % (n, v, dc))

rep("== PB2 misses ==")
for n, v, t in d2:
    if v != t: rep("  %s: n5=%s sealed=%s" % (n, v, t))
rep("== PB3 false-derived ==")
for n, v, t in d3:
    if v == "DERIVED" and t == "WITHHELD": rep("  %s (sealed WITHHELD)" % n)
rep("== PB3 false-withheld ==")
for n, v, t in d3:
    if v == "WITHHELD" and t == "DERIVED": rep("  %s (sealed DERIVED)" % n)

open(os.path.expanduser("~/workspace/n5_recovery/SCORES.txt"), "w").write("\n".join(out) + "\n")
