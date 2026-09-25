#!/usr/bin/env python3
# pareto.py — compute the measured Pareto frontier + apply B.3 decision rule mechanically.
import os

CREW = os.path.expanduser("~/workspace/pam_gov_lh/crew6_held")
EV = os.path.join(CREW, "evidence")

rows = []
with open(os.path.join(EV, "sweep_table.tsv")) as f:
    hdr = f.readline()
    for line in f:
        p = line.strip().split("\t")
        rc, rm = int(p[0]), int(p[1])
        rows.append((rc, rm, int(p[2]), int(p[4]), int(p[6]), int(p[8])))

# frontier: maximize retention, minimize over-block; dominated iff another point
# has ret >= mine, over <= mine, and strictly better on at least one axis.
front = []
for a in rows:
    dominated = False
    for b in rows:
        if b[4] >= a[4] and b[2] <= a[2] and (b[4] > a[4] or b[2] < a[2]):
            dominated = True
            break
    if not dominated:
        front.append(a)
front.sort(key=lambda r: (r[4], r[2]))

with open(os.path.join(EV, "pareto_frontier.tsv"), "w") as f:
    f.write("rc\trm\tretention\tret_n\tover_block\tover_n\tfar_blocked\tfar_n\n")
    for rc, rm, nb, fb, ret, tb in front:
        f.write(f"{rc}\t{rm}\t{ret}\t9\t{nb}\t300\t{fb}\t60\n")

print("PARETO FRONTIER (non-dominated retention vs over-block):")
for rc, rm, nb, fb, ret, tb in front:
    print(f"  rc={rc:3d} rm={rm:4d} retention={ret}/9 over_block={nb}/300 ({100*nb/300:.1f}%) far={fb}/60 true_blocked={tb}/34")

# B.3 decision rule, applied mechanically:
# OVERTURN iff EXISTS a swept window with ALL THREE:
#   retention >= 8/9, over-block <= 25% (<=75/300), far-control 0/60.
qualifiers = []
for rc, rm, nb, fb, ret, tb in rows:
    if ret >= 8 and nb <= 75 and fb == 0:
        qualifiers.append((rc, rm, nb, fb, ret, tb))

print()
if qualifiers:
    print("B.3 OVERTURN qualifiers (retention>=8/9, over-block<=75/300, far=0/60):")
    for rc, rm, nb, fb, ret, tb in qualifiers:
        print(f"  rc={rc} rm={rm}: retention={ret}/9, over_block={nb}/300, far={fb}/60")
    print("DECISION: OVERTURN the NO-GO")
else:
    print("No window satisfies all three B.3 conditions.")
    print("DECISION: CONFIRM the NO-GO")

with open(os.path.join(EV, "b3_decision.txt"), "w") as f:
    f.write("B.3 mechanical decision input:\n")
    f.write(f"  qualifying windows: {[(r[0], r[1]) for r in qualifiers]}\n")
    f.write("DECISION: " + ("OVERTURN the NO-GO" if qualifiers else "CONFIRM the NO-GO") + "\n")
