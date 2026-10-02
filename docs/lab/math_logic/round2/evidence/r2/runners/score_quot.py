#!/usr/bin/env python3
"""Score QUOT vs round-1 parents on the frozen primary bars.
Reads: results_formal_quot.json (QUOT), results_formal_all.json (parents),
       results_kb2_quot.json, results_kb2.json.
Prints: per-battery table, PB1/PB2/PB3 vs ONE-R1 and DUAL-R1, decision.
"""
import json, hashlib

Q = json.load(open("/home/hatch/workspace/math_r2/eval/results_formal_quot.json"))
P = json.load(open("/home/hatch/workspace/math_r2/eval/results_formal_all.json"))
KQ = json.load(open("/home/hatch/workspace/math_r2/eval/results_kb2_quot.json"))
K = json.load(open("/home/hatch/workspace/math_r2/eval/results_kb2.json"))

print("=== QUOT per-battery ===")
for b in ["B2R", "B3R", "B4R", "B4X", "B5X", "B6X"]:
    e = Q[b]
    a = e["agg"]
    ps = [p for p in e["problems"].values() if p.get("status") == "ok"]
    comm = [int(p["committed"]) for p in ps if p.get("committed", "?") != "?"]
    to = sum(1 for p in e["problems"].values() if p.get("status") == "TIMEOUT")
    ex = sum(1 for p in e["problems"].values()
             if p.get("status", "").startswith("EXIT"))
    miss = [pid for pid, p in e["problems"].items()
            if p.get("status") == "ok" and p["incorrect"]]
    print(f"{b}: solved {a['solved']}/{a['n']} incorrect {a['incorrect']} "
          f"(fd {a['false_derived']}, fw {a['false_withheld']}) "
          f"timeouts {to} exitfail {ex} divergent {a['divergent']} "
          f"wall {a['wall_total_s']}s committed_total {sum(comm)} "
          f"miss={miss}")

print("\n=== parents (reference) ===")
for b in ["B2R", "B3R", "B4R", "B4X", "B5X", "B6X"]:
    for e in ["ONE-R1", "DUAL-R1"]:
        a = P[b][e]["agg"]
        print(f"{b} {e}: solved {a['solved']}/{a['n']} incorrect {a['incorrect']}")

# PB1: B3R pairwise wins (QUOT solves and parent does not)
print("\n=== PB1 (B3R pairwise wins, bar >=7/10) ===")
qp = Q["B3R"]["problems"]
for parent in ["ONE-R1", "DUAL-R1"]:
    pp = P["B3R"][parent]["problems"]
    wins = sum(1 for pid in qp
               if qp[pid].get("status") == "ok" and qp[pid]["solved"]
               and pp.get(pid, {}).get("status") == "ok" and not pp[pid]["solved"])
    losses = sum(1 for pid in qp
                 if pp.get(pid, {}).get("status") == "ok" and pp[pid]["solved"]
                 and qp[pid].get("status") == "ok" and not qp[pid]["solved"])
    print(f"QUOT vs {parent}: wins {wins}/10 -> {'PASS' if wins >= 7 else 'FAIL'} "
          f"(parent-won {losses})")

# PB2: KB2
print("\n=== PB2 (KB2 contrast) ===")
for name, d in [("QUOT", KQ), ("ONE-R1", K), ("DUAL-R1", K)]:
    r = d if name == "QUOT" else d[name]
    print(f"{name}: dual_wins {r['dual_wins']}/20 -> "
          f"{'PASS' if r['dual_bar'] else 'FAIL'}")

# PB3: B5X incorrect <= half of worse parent (ONE-R1 36 -> 18)
print("\n=== PB3 (B5X incorrect <= 18) ===")
for name, src in [("QUOT", Q), ("ONE-R1", P), ("DUAL-R1", P)]:
    a = src["B5X"]["agg"] if name == "QUOT" else src["B5X"][name]["agg"]
    fd = a.get("false_derived", "?"); fw = a.get("false_withheld", "?")
    print(f"{name}: incorrect {a['incorrect']} (fd {fd}, fw {fw}) -> "
          f"{'PASS' if a['incorrect'] <= 18 else 'FAIL'}")

# B5X per-level split for QUOT
print("\n=== QUOT B5X by level/kind ===")
sealed = {}
for line in open("/home/hatch/workspace/tnn-lab/math_logic/round2/batteries/sealed/SEALED_B5X.sol"):
    line = line.strip()
    if line and not line.startswith("#") and ":" in line:
        pid, v = line.split(":"); sealed[pid.strip()] = v.strip()
for lvl in ["L2", "L3", "L4"]:
    for kind, sv in [("D", "DERIVED"), ("W", "WITHHELD")]:
        ids = [pid for pid in sealed if pid.startswith(f"B5X_{lvl}") and sealed[pid] == sv]
        got = [pid for pid in ids
               if Q["B5X"]["problems"].get(pid, {}).get("status") == "ok"
               and Q["B5X"]["problems"][pid]["solved"]]
        print(f"  {lvl} kind-{kind} (sealed {sv}): {len(got)}/{len(ids)} correct")

print("\n=== output SHAs ===")
print("results_formal_quot.json:",
      hashlib.sha256(open("/home/hatch/workspace/math_r2/eval/results_formal_quot.json","rb").read()).hexdigest())
print("binary_sha256:", Q.get("binary_sha256"))
