#!/usr/bin/env python3
"""FORK B scorer: verdicts from evidence/runs vs sealed solutions (read-only)."""
import os, re, sys

RUNS = os.path.expanduser("~/workspace/n5_fork_b/evidence/runs")
R4B = os.path.expanduser("~/workspace/tnn-lab/math_logic/round4/batteries")
R3B = os.path.expanduser("~/workspace/tnn-lab/math_logic/round3/batteries")

def verdict(bat, name):
    p = os.path.join(RUNS, bat, name + "_r1.out")
    try:
        txt = open(p, encoding="utf-8", errors="replace").read()
    except FileNotFoundError:
        return "MISSING"
    m = re.search(r"^VERDICT:\s+(DERIVED|WITHHELD)", txt, re.M)
    return m.group(1) if m else "NO-VERDICT"

def load_map(path):
    d = {}
    for line in open(path, encoding="utf-8"):
        m = re.match(r"^(\S+):\s+(DERIVED|WITHHELD)", line)
        if m: d[m.group(1)] = m.group(2)
    return d

r3n_sol = load_map(os.path.join(R3B, "sealed/SEALED_R3N.sol"))
# PB4: expected DERIVED for all 20, verified from sealed solution type fields
import json, glob
chain_sol = {}
for f in glob.glob(os.path.join(R4B, "sealed/CHAIN_NL_*.sol.json")):
    d = json.load(open(f))
    name = d["id"]
    chain_sol[name] = "DERIVED" if d["type"] == "derivation" else "WITHHELD"
assert len(chain_sol) == 20, chain_sol.keys()

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
    print("== %s ==" % label)
    print("  correct %d/%d, false_derived=%d, false_withheld=%d" % (correct, len(names), fd, fw))
    if bar_n is not None:
        print("  bar: %s (need %d/%d)" % ("CLEAR" if correct >= bar_n else "MISS", bar_n, bar_of))
    return correct, fd, fw, detail

pb1_names = ["R3N_%02d" % i for i in range(1, 25)]
pb4_names = ["CHAIN_NL_%02d" % i for i in range(1, 21)]

c1, fd1, fw1, d1 = score("pb1", pb1_names, r3n_sol, "PB1 R3N (bar >=12/24)", 12, 24)
c4, fd4, fw4, d4 = score("pb4", pb4_names, chain_sol, "PB4 CHAIN-NL (bar >=12/20)", 12, 20)

print("== PB1 misses (n5 vs sealed) ==")
for n, v, t in d1:
    if v != t: print("  %s: n5=%s sealed=%s" % (n, v, t))
print("== PB4 misses (n5 vs sealed) ==")
for n, v, t in d4:
    if v != t: print("  %s: n5=%s sealed=%s" % (n, v, t))

# crash count: any non-rc-0 run (no VERDICT line at all counts as crash here)
crashes = [n for n in pb1_names + pb4_names
           if verdict("pb1" if n.startswith("R3N") else "pb4", n) == "NO-VERDICT"]
print("CRASHES (no verdict): %d %s" % (len(crashes), crashes))
