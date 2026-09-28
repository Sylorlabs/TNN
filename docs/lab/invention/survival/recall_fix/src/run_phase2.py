#!/usr/bin/env python3
"""Run D (deliberative) battery: D_home and D on shifted."""
import os, subprocess

WORK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD = os.path.join(WORK, 'build')
WORLDS = os.path.join(WORK, 'worlds')
KB = os.path.join(WORK, 'kb')
RUNS = os.path.join(WORK, 'runs', 'phase2')
os.makedirs(RUNS, exist_ok=True)

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    # Extract RESULT line (not trace)
    for line in r.stdout.split('\n'):
        if line.startswith('RESULT'):
            return line.strip(), r.returncode
    return "", r.returncode

results = []

# D1
for v in [f'd1_h{i}' for i in range(6)] + [f'd1_a{i}' for i in range(3)] + [f'd1_b{i}' for i in range(3)]:
    vp = os.path.join(WORLDS, v + '.txt')
    for rerun in [0, 1]:
        out, rc = run([os.path.join(BUILD, 'agent_d_d1'), vp, v, str(rerun), os.path.join(KB, 'home_d1.txt')])
        results.append(('d1', 'd', v, rerun, out, rc))

# D2
for v in [f'd2_h{i}' for i in range(6)] + [f'd2_s{i}' for i in range(6)]:
    vp = os.path.join(WORLDS, v + '.txt')
    for rerun in [0, 1]:
        out, rc = run([os.path.join(BUILD, 'agent_d_d2'), vp, v, str(rerun), os.path.join(KB, 'home_d2.txt')])
        results.append(('d2', 'd', v, rerun, out, rc))

# D3
for v in [f'd3_h{i}' for i in range(4)] + [f'd3_s{i}' for i in range(4)]:
    vp = os.path.join(WORLDS, v + '.txt')
    for rerun in [0, 1]:
        out, rc = run([os.path.join(BUILD, 'agent_d_d3'), vp, v, str(rerun), os.path.join(KB, 'home_d3.txt')])
        results.append(('d3', 'd', v, rerun, out, rc))

with open(os.path.join(RUNS, 'results.txt'), 'w') as f:
    for d, arm, v, rerun, out, rc in results:
        f.write(f"[{d}][{arm}][{v}][{rerun}][rc={rc}]\n{out}\n")

print(f"Ran {len(results)} D runs.")
