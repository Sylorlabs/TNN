#!/usr/bin/env python3
"""Analyze D results: K5 (home) and K2 (gap closure)."""
import os, re
from collections import defaultdict

WORK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNS2 = os.path.join(WORK, 'runs', 'phase2', 'results.txt')
RUNS1 = os.path.join(WORK, 'runs', 'phase1', 'results.txt')

def parse(path):
    data = defaultdict(list)
    with open(path) as f:
        content = f.read()
    # D1: RESULT d d1_h0 0 600 0 147 6 54 429 0 3 (ticks at position 4)
    # D2/D3: RESULT d d2_h0 0 600 4500 (reward at position 5)
    for m in re.finditer(r'\[(d\d)\]\[(\w+)\]\[(d\d_\w\d?)\]\[(\d)\]\[rc=(\d+)\]\nRESULT \w+ \S+ \d+ (\d+)', content):
        d, arm, v, rerun, rc, ticks = m.groups()
        data[(d, arm, v)].append(int(ticks))
    # For D2/D3, get reward (5th field)
    for m in re.finditer(r'\[(d[23])\]\[(\w+)\]\[(d[23]_\w\d?)\]\[(\d)\]\[rc=(\d+)\]\nRESULT \w+ \S+ \d+ \d+ (-?\d+)', content):
        d, arm, v, rerun, rc, reward = m.groups()
        # Replace ticks with reward for d2/d3
        data[(d, arm, v)] = [int(reward) if i==len(data[(d,arm,v)])-1 else x for i, x in enumerate(data[(d,arm,v)])]
    return data

# Simpler: parse manually
def get_scores(path, domain):
    scores = defaultdict(list)
    with open(path) as f:
        lines = f.readlines()
    i = 0
    while i < len(lines):
        m = re.match(r'\[(d\d)\]\[(\w+)\]\[(d\d_\w\d?)\]\[(\d)\]\[rc=(\d+)\]', lines[i].strip())
        if m:
            d, arm, v, rerun, rc = m.groups()
            if d == domain and i+1 < len(lines):
                parts = lines[i+1].strip().split()
                if len(parts) >= 6:
                    # D1: ticks=parts[4], D2/D3: reward=parts[5]
                    if domain == 'd1':
                        scores[(arm, v)].append(int(parts[4]))
                    else:
                        scores[(arm, v)].append(int(parts[5]))
            i += 2
        else:
            i += 1
    return scores

print("="*70)
print("K5: D_home >= 0.9 * R_home (home regime)")
print("="*70)
for d in ['d1', 'd2', 'd3']:
    s1 = get_scores(RUNS1, d)
    s2 = get_scores(RUNS2, d)
    # Home variants
    home_vs = [v for (arm, v) in s1 if arm=='r_home' and '_h' in v]
    r_home = sorted([min(s1[('r_home', v)]) for v in home_vs])
    d_home = sorted([min(s2[('d', v)]) for v in home_vs if ('d', v) in s2])
    if r_home and d_home:
        rh_med = r_home[len(r_home)//2]
        d_med = d_home[len(d_home)//2]
        thresh = 0.9 * rh_med
        status = "PASS" if d_med >= thresh else "FAIL"
        print(f"{d.upper()}: R_home median={rh_med}, D median={d_med}, 0.9*R={thresh:.1f} -> {status}")

print("\n" + "="*70)
print("K2: D closes >=50% of R_home->R_true gap (shifted)")
print("="*70)
for d in ['d1', 'd2', 'd3']:
    s1 = get_scores(RUNS1, d)
    s2 = get_scores(RUNS2, d)
    shift_vs = [v for (arm, v) in s1 if arm=='r_home' and ('_s' in v or '_a' in v or '_b' in v)]
    print(f"\n{d.upper()}:")
    for v in sorted(shift_vs)[:3]:  # show first 3
        if ('r_home', v) in s1 and ('r_true', v) in s1 and ('d', v) in s2:
            rh = min(s1[('r_home', v)])
            rt = min(s1[('r_true', v)])
            dd = min(s2[('d', v)])
            gap = rt - rh
            if gap == 0:
                print(f"  {v}: no gap (rh={rh}, rt={rt})")
            else:
                closure = (dd - rh) / gap
                status = "PASS" if closure >= 0.5 else "FAIL"
                print(f"  {v}: rh={rh}, rt={rt}, d={dd}, closure={closure:.1%} -> {status}")
