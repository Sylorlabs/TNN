#!/usr/bin/env python3
"""Analyze Phase 1 results."""
import os, re
from collections import defaultdict

WORK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNS = os.path.join(WORK, 'runs', 'phase1', 'results.txt')

# Parse results
data = defaultdict(list)  # (domain, arm, variant) -> [scores]
with open(RUNS) as f:
    content = f.read()

# Format: [d][arm][v][rerun][rc=0]\nRESULT ...
blocks = re.findall(r'\[(d\d)\]\[(\w+)\]\[(d\d_\w\d?)\]\[(\d)\]\[rc=(\d+)\]\nRESULT (\w+) (\S+) (\d+) (\d+) (-?\d+)', content)
for d, arm, v, rerun, rc, r_arm, r_var, r_rerun, ticks, score in blocks:
    # For D1, score is final_e? No, let's get ticks for D1, reward for D2/D3.
    # D1 RESULT: arm variant rerun ticks alive final_e n_take n_eat n_comb n_drop n_move
    # D2/D3 RESULT: arm variant rerun ticks total_reward
    data[(d, arm, v)].append((int(ticks), int(score), int(rc)))

# For D1, use ticks as the metric. For D2/D3, use score (total_reward).
print("="*70)
print("PHASE 1 SUMMARY (median of 2 reruns)")
print("="*70)

for d in ['d1', 'd2', 'd3']:
    print(f"\n--- {d.upper()} ---")
    # Group by arm and regime
    arms = sorted(set(arm for (dd, arm, v) in data if dd == d))
    for arm in arms:
        home_vs = [v for (dd, a, v) in data if dd == d and a == arm and ('_h' in v)]
        shift_vs = [v for (dd, a, v) in data if dd == d and a == arm and ('_s' in v or '_a' in v or '_b' in v)]
        # Get metric: ticks for d1, score for d2/d3
        def metric(v):
            vals = data[(d, arm, v)]
            if d == 'd1':
                return sorted([t for t, s, rc in vals])[0]  # ticks (min of 2)
            else:
                return sorted([s for t, s, rc in vals])[0]  # reward (min of 2)
        if home_vs:
            hm = sorted([metric(v) for v in home_vs])
            med = hm[len(hm)//2]
            print(f"  {arm:8s} home: median={med}, all={hm}")
        if shift_vs:
            sm = sorted([metric(v) for v in shift_vs])
            med = sm[len(sm)//2]
            print(f"  {arm:8s} shifted: median={med}, all={sm}")

# Harm check: R_home vs R_true on shifted
print("\n" + "="*70)
print("HARM CHECK (R_home vs R_true on shifted variants)")
print("="*70)
for d in ['d1', 'd2', 'd3']:
    print(f"\n{d.upper()}:")
    # Find shifted variants with both r_home and r_true
    shift_vs = set(v for (dd, a, v) in data if dd == d and a == 'r_home' and ('_s' in v or '_a' in v or '_b' in v))
    for v in sorted(shift_vs):
        if (d, 'r_true', v) in data:
            def get(d, arm, v):
                vals = data[(d, arm, v)]
                if d == 'd1':
                    return min(t for t, s, rc in vals)
                else:
                    return min(s for t, s, rc in vals)
            rh = get(d, 'r_home', v)
            rt = get(d, 'r_true', v)
            gap = rt - rh
            print(f"  {v}: R_home={rh}, R_true={rt}, gap={gap}")
