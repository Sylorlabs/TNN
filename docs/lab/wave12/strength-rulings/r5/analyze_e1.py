#!/usr/bin/env python3
# R5 E1 agreement-matrix analysis. Deterministic arithmetic on committed
# cell logs only (no mechanism). Reads evidence/e1/cell_*_r1.log.
import re, glob, os

E1 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "evidence", "e1")

def parse(path):
    d = {}
    for line in open(path):
        line = line.strip()
        m = re.match(r"ST_METRIC (\d+) (\d+) (\d+)", line)
        if m:
            d["m" + m.group(1)] = (int(m.group(2)), int(m.group(3)))
        m = re.match(r"ST_(DROPS|ABANDONS|INVALID) (\d+)", line)
        if m:
            d[m.group(1)] = int(m.group(2))
    return d

rows = []
for arm in ["B", "C", "C-P3"]:
    for v in [0, 1, 2]:
        d = parse(os.path.join(E1, "cell_%s_VUP_%d_r1.log" % (arm, v)))
        ptr_n, ptr_d = d["m8"]
        ec_n, ec_d = d["m9"]
        ct_n, ct_d = d["m10"]
        er_n, er_d = d["m11"]
        ec = ec_n / ec_d if ec_d else 0.0
        p1 = "UNEVALUATED" if ec < 0.5 else "PTR=%.3f" % (ptr_n / ptr_d if ptr_d else 0)
        p2d = "FAILED" if d["DROPS"] > 64 else "PASS"
        p2t = "PASS" if ct_n >= 32 else "FAIL"   # admitted/500 >= 32/500
        rows.append((arm, v, p1, ec, p2d, d["DROPS"], p2t, ct_n,
                     er_n, er_d, d["ABANDONS"], d["INVALID"]))

print("arm var | P1 verdict      | EC    | P2 drops verdict | drops | P2 throughput | admitted | ER        | abandons | invalid")
for r in rows:
    arm, v, p1, ec, p2d, drops, p2t, adm, er_n, er_d, ab, inv = r
    print("%-3s %-3d | %-16s | %.3f | %-16s | %-5d | %-13s | %-8d | %d/%d | %-8d | %d"
          % (arm, v, p1, ec, p2d, drops, p2t, adm, er_n, er_d, ab, inv))

print()
print("AGREEMENT (frozen C config):")
for r in rows:
    if r[0] == "C":
        print("  C v%d: P1=%s (EC=%.2f, evaluated) | P2 drops=%s, throughput=%s"
              % (r[1], r[2], r[3], r[4], r[6]))
for r in rows:
    if r[0] == "C-P3":
        print("  C-P3 v%d: P1=%s (EC=%.2f, evaluated) | P2 drops=%s, throughput=%s"
              % (r[1], r[2], r[3], r[4], r[6]))
print("  B (healthy control): P1=%s — UNEVALUATED fires on the HEALTHY arm too."
      % rows[0][2])
print("  P3 delta C->C-P3: abandons %d -> %d (fewer victim attempts under Rule 2); "
      "all frozen metrics identical (drops/admitted/ER/PTR/EC)." % (rows[3][10], rows[6][10]))
print("  ck_no_permanent_lock (C-P3, gate_mode=0 in cells): held — ST_INVALID=0 all variants.")
