#!/usr/bin/env python3
"""Analyze trial metrics: defect slope, role use, throughput, per-component time."""
import json, os

WORKDIR = os.path.expanduser("~/workspace/lh_trial")
metrics = [json.loads(l) for l in open(os.path.join(WORKDIR, "metrics.jsonl"))]

# --- Defect slope: 10-cycle windows ---
# Defect = defect==1 in any metric
cycles = sorted(set(m["cycle"] for m in metrics))
max_cycle = max(cycles)
windows = []
for w in range(0, max_cycle + 1, 10):
    w_cycles = [c for c in cycles if w <= c < w + 10]
    w_metrics = [m for m in metrics if m["cycle"] in w_cycles]
    defects = sum(1 for m in w_metrics if m.get("defect", 0) == 1)
    total = len([m for m in w_metrics if "defect" in m])
    rate = defects / total if total else 0
    windows.append((w // 10, rate, defects, total))

# Least-squares slope
n = len(windows)
xs = [w[0] for w in windows]
ys = [w[1] for w in windows]
mx, my = sum(xs)/n, sum(ys)/n
num = sum((x-mx)*(y-my) for x,y in zip(xs,ys))
den = sum((x-mx)**2 for x in xs)
slope = num/den if den else 0

print("=== DEFECT SLOPE ===")
print(f"Windows: {n} (10 cycles each)")
for i, rate, d, t in windows:
    print(f"  W{i:2d}: rate={rate:.3f} ({d}/{t})")
print(f"Slope: {slope:.6f}")
print(f"Bar: {'PASS (slope <= 0)' if slope <= 0 else 'FAIL (slope > 0)'}")

# --- Role use by run third ---
# Count PROPOSER/CRITIC/COMPOSER episodes from ledger
ledger = open(os.path.join(WORKDIR, "ledger.txt")).read()
# Tertiles by cycle
third = max_cycle // 3
roles = {"PROPOSER": [0,0,0], "CRITIC": [0,0,0], "COMPOSER": [0,0,0]}
# Parse ledger for EP lines with cycle info (we'll approximate by order)
# Actually, count from metrics: propose/critique/compose events
for m in metrics:
    ev = m["event"]
    c = m["cycle"]
    t = 0 if c <= third else (1 if c <= 2*third else 2)
    if ev == "propose":
        roles["PROPOSER"][t] += 1
    elif ev == "critique":
        roles["CRITIC"][t] += 1
    elif ev == "compose":
        roles["COMPOSER"][t] += 1

print("\n=== ROLE USE BY RUN THIRD ===")
print(f"Tertile boundaries: 1-{third}, {third+1}-{2*third}, {2*third+1}-{max_cycle}")
for role, counts in roles.items():
    print(f"  {role:8s}: {counts[0]:3d} | {counts[1]:3d} | {counts[2]:3d}")

# --- Throughput ---
t_start = min(m["t"] for m in metrics)
t_end = max(m["t"] for m in metrics)
elapsed_h = (t_end - t_start) / 3600
print(f"\n=== THROUGHPUT ===")
print(f"Cycles: {max_cycle}")
print(f"Wall time: {(t_end-t_start):.1f}s ({elapsed_h:.3f}h)")
print(f"Cycles/hour: {max_cycle/elapsed_h:.1f}")

# --- Per-component first-working-build time ---
print(f"\n=== PER-COMPONENT FIRST-WORKING-BUILD TIME ===")
times = []
for m in metrics:
    if m["event"] == "stage_accept":
        times.append((m["stage"], m["first_working_s"]))
times.sort()
for stage, t in times:
    print(f"  {stage}: {t:.2f}s")
if times:
    vals = [t for _, t in times]
    print(f"Mean: {sum(vals)/len(vals):.2f}s, Max: {max(vals):.2f}s")

# --- Halt verification ---
halts = [m for m in metrics if m["event"] == "halt"]
print(f"\n=== HONEST HALT ===")
for h in halts:
    print(f"  {h['stage']}: {h['kind']} (defect={h['defect']})")
print(f"Bar: {'PASS' if len(halts)==1 and halts[0]['stage']=='F1' and halts[0]['kind']=='KB-MISS' else 'FAIL'}")
