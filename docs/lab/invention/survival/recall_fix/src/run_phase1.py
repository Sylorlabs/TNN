#!/usr/bin/env python3
"""Phase 1 battery runner: all arms x all variants x 2 reruns.
Outputs results to runs/phase1/.
"""
import os, subprocess, hashlib, json

WORK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD = os.path.join(WORK, 'build')
WORLDS = os.path.join(WORK, 'worlds')
KB = os.path.join(WORK, 'kb')
RUNS = os.path.join(WORK, 'runs', 'phase1')
os.makedirs(RUNS, exist_ok=True)

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.stdout.strip(), r.returncode

results = []
manifest = []

# D1: arms z, p, r (with home KB), r_true (with true KBs)
d1_vars = [f'd1_h{i}' for i in range(6)] + [f'd1_a{i}' for i in range(3)] + [f'd1_b{i}' for i in range(3)]
for v in d1_vars:
    vp = os.path.join(WORLDS, v + '.txt')
    for rerun in [0, 1]:
        # Z
        out, rc = run([os.path.join(BUILD, 'agent_z_d1'), vp, v, str(rerun), str(100+int(v[-1]))])
        results.append(('d1', 'z', v, rerun, out, rc))
        # P
        out, rc = run([os.path.join(BUILD, 'agent_p_d1'), vp, v, str(rerun)])
        results.append(('d1', 'p', v, rerun, out, rc))
        # R_home
        out, rc = run([os.path.join(BUILD, 'agent_r_d1'), vp, v, str(rerun), os.path.join(KB, 'home_d1.txt')])
        results.append(('d1', 'r_home', v, rerun, out, rc))
        # R_true (shifted only, with regime KB)
        if v.startswith('d1_a'):
            kb = os.path.join(KB, 'true_d1_storm.txt')
            out, rc = run([os.path.join(BUILD, 'agent_r_d1'), vp, v, str(rerun), kb])
            results.append(('d1', 'r_true', v, rerun, out, rc))
        elif v.startswith('d1_b'):
            kb = os.path.join(KB, 'true_d1_move.txt')
            out, rc = run([os.path.join(BUILD, 'agent_r_d1'), vp, v, str(rerun), kb])
            results.append(('d1', 'r_true', v, rerun, out, rc))

# D2
d2_vars = [f'd2_h{i}' for i in range(6)] + [f'd2_s{i}' for i in range(6)]
for v in d2_vars:
    vp = os.path.join(WORLDS, v + '.txt')
    for rerun in [0, 1]:
        out, rc = run([os.path.join(BUILD, 'agent_z_d2'), vp, v, str(rerun), str(200+int(v[-1]))])
        results.append(('d2', 'z', v, rerun, out, rc))
        out, rc = run([os.path.join(BUILD, 'agent_p_d2'), vp, v, str(rerun)])
        results.append(('d2', 'p', v, rerun, out, rc))
        out, rc = run([os.path.join(BUILD, 'agent_r_d2'), vp, v, str(rerun), os.path.join(KB, 'home_d2.txt')])
        results.append(('d2', 'r_home', v, rerun, out, rc))
        if v.startswith('d2_s'):
            out, rc = run([os.path.join(BUILD, 'agent_r_d2'), vp, v, str(rerun), os.path.join(KB, 'true_d2.txt')])
            results.append(('d2', 'r_true', v, rerun, out, rc))

# D3
d3_vars = [f'd3_h{i}' for i in range(4)] + [f'd3_s{i}' for i in range(4)]
for v in d3_vars:
    vp = os.path.join(WORLDS, v + '.txt')
    for rerun in [0, 1]:
        out, rc = run([os.path.join(BUILD, 'agent_z_d3'), vp, v, str(rerun), str(300+int(v[-1]))])
        results.append(('d3', 'z', v, rerun, out, rc))
        out, rc = run([os.path.join(BUILD, 'agent_p_d3'), vp, v, str(rerun)])
        results.append(('d3', 'p', v, rerun, out, rc))
        out, rc = run([os.path.join(BUILD, 'agent_r_d3'), vp, v, str(rerun), os.path.join(KB, 'home_d3.txt')])
        results.append(('d3', 'r_home', v, rerun, out, rc))
        if v.startswith('d3_s'):
            out, rc = run([os.path.join(BUILD, 'agent_r_d3'), vp, v, str(rerun), os.path.join(KB, 'true_d3.txt')])
            results.append(('d3', 'r_true', v, rerun, out, rc))

# Write results and manifest
with open(os.path.join(RUNS, 'results.txt'), 'w') as f:
    for d, arm, v, rerun, out, rc in results:
        f.write(f"[{d}][{arm}][{v}][{rerun}][rc={rc}]\n{out}\n")

# SHA-256 of results (determinism check: run twice, compare)
h = hashlib.sha256()
with open(os.path.join(RUNS, 'results.txt'), 'rb') as f:
    h.update(f.read())
sha = h.hexdigest()
with open(os.path.join(RUNS, 'sha.txt'), 'w') as f:
    f.write(sha + '\n')

print(f"Ran {len(results)} runs. SHA: {sha}")
