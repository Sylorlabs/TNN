#!/usr/bin/env python3
"""WALL-RED crack-2 verification: candidate-set expansion.
Builds two bundles per case:
  top3 : only the first 3 pids in order.txt (Crew B production behavior)
  all  : every page (expanded candidate set)
Runs base (and ch1) on both. A top3=INSTALL / all=WITHHOLD split proves the
dissent existed in the corpus but was cut by selection (wallsel.zag's
hidden_dissent=1), i.e. M3-as-ranking is partly a SELECTION bug.
Also runs the stale-pin control: T4_supersede with pin1 (pre-supersession
snapshot) under g1 -> expected WITHHOLD|ARCHVETO (grok's pin-discipline caveat).
"""
import os, sys
sys.path.insert(0, os.path.expanduser("~/workspace/liharden/beyond/work"))
from run_beyond import bundle, run, pin_lines

WORK = os.path.expanduser("~/workspace/liharden/beyond/work")
FIX1 = os.path.expanduser("~/workspace/liharden/corrob/fixtures")

def bundle_top3(casedir, case):
    data = bundle(casedir, case).decode()
    order = open(os.path.join(casedir, "order.txt")).read().split()
    keep = set(order[:3])
    out = []
    cur = None
    for line in data.split("\n"):
        if line.startswith("P|"):
            cur = line[2:]
            if cur in keep:
                out.append(line)
        elif line.startswith(("NEED|", "U|", "ARCH|", "REG|", "SENT|", "M|")):
            # keep M lines only for kept pids
            if line.startswith("M|"):
                pid = line.split("|")[1]
                if pid in keep:
                    out.append(line)
            else:
                out.append(line)
        else:
            if cur in keep:
                out.append(line)
    return ("\n".join(out) + "\n").encode()

CASES = ["X_SATUR1_crowdout", "C_numD_dissent", "X_SATUR1b_honest_open",
         "X_BOILER1_widget", "H8_wire_truth"]

print("case\tbundle\tmech\tverdict")
for case in CASES:
    cdir = os.path.join(FIX1, case)
    for name, b in (("top3", bundle_top3(cdir, case)), ("all", bundle(cdir, case))):
        for mech in ("base", "ch1"):
            o1, o2 = run(mech, b), run(mech, b)
            assert o1 == o2, "NONDETERMINISM"
            print(f"{case}\t{name}\t{mech}\t{o1}")

# stale-pin control: T4 with pin1
import run_beyond
orig = run_beyond.pin_lines
def pin1_only(case):
    lines = []
    for fn, prefix in (("pin1.txt", "ARCH"), ("registry.txt", "REG")):
        p = os.path.join(os.path.expanduser("~/workspace/liharden/beyond/pins"), fn)
        for l in open(p):
            l = l.strip()
            if l:
                lines.append(prefix + "|" + l)
    return lines
run_beyond.pin_lines = pin1_only
data = bundle(os.path.expanduser("~/workspace/liharden/beyond/fixtures/T4_supersede"), "T4_supersede")
o = run("g1", data)
print(f"T4_supersede\tstale-pin1\tg1\t{o}")
o2 = run("g6", data)
print(f"T4_supersede\tstale-reg1\tg6\t{o2}")
