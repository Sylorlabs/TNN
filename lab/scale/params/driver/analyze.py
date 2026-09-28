#!/usr/bin/env python3
"""Efficiency-frontier + kill-bar analysis for the parameter sweep."""
import sys

rows = []
with open(sys.argv[1]) as f:
    hdr = f.readline()
    for line in f:
        p = line.rstrip("\n").split("\t")
        rows.append(dict(cfg=p[0], cn=int(p[1]), cd=int(p[2]), flaw=int(p[3]),
                         abn=int(p[4]), abd=int(p[5]), ops=float(p[6]) / 1000.0,
                         bpf=int(p[7]), digest=p[8], det=p[9]))

base = next(r for r in rows if r["cfg"] == "base")
print("=== kill bars ===")
alldet = all(r["det"] == "OK" for r in rows)
print(f"KB-P-DET: {'NOT TRIPPED' if alldet else 'TRIPPED — HALT'} ({sum(r['det']=='OK' for r in rows)}/{len(rows)} configs byte-identical)")
emerge = [r for r in rows if r["abn"] < r["abd"]]
print(f"KB-P-EMERGE: {'NOT TRIPPED' if not emerge else 'TRIPPED: ' + ','.join(r['cfg'] for r in emerge)} (absorption<1.0)")
s05 = next(r for r in rows if r["cfg"] == "slot05")
# taught subset at slot05: ids [0,12000); clean facts among them
taught_clean = s05["cd"]  # clean_den counts all clean ids; need taught-only
print(f"KB-P-GRACE: slot05 clean {s05['cn']}/{s05['cd']} (expect ~0.5 of all-fact; taught-subset check below)")

print("\n=== per-config ===")
print(f"{'cfg':8} {'clean':>13} {'flaw':>5} {'absorb':>11} {'ops/f':>7} {'B/f':>6} {'digest_prefix'}")
for r in rows:
    print(f"{r['cfg']:8} {r['cn']:>6}/{r['cd']:<6} {r['flaw']:>2}/96 {r['abn']:>6}/{r['abd']:<5} {r['ops']:>7.3f} {r['bpf']:>6} {r['digest'][:12]}")

print("\n=== efficiency: mastery gain per cost vs baseline ===")
for r in rows:
    if r["cfg"] == "base":
        continue
    dm = r["cn"] / r["cd"] - base["cn"] / base["cd"]
    dcost_ops = r["ops"] / base["ops"]
    dcost_b = r["bpf"] / base["bpf"]
    dead = (dcost_ops >= 2 or dcost_b >= 2) and dm < 0.01
    print(f"{r['cfg']:8} dMastery={dm:+.4f}  cost x{dcost_ops:.2f} ops  x{dcost_b:.2f} B  {'EFFICIENCY-DEAD' if dead else ''}")

print("\n=== pareto frontier (max mastery, min B/fact) ===")
pts = [(r["bpf"], r["cn"] / r["cd"], r["cfg"]) for r in rows]
front = []
for b, m, c in pts:
    if not any(b2 <= b and m2 >= m and (b2, m2) != (b, m) for b2, m2, _ in pts):
        front.append((b, m, c))
for b, m, c in sorted(front):
    print(f"  {c:8} B/fact={b} mastery={m:.4f}")
