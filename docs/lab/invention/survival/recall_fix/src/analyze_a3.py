#!/usr/bin/env python3
"""A3(i): Count contested turns (VERDICT != heuristic action) from D traces."""
import os, subprocess, re

WORK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD = os.path.join(WORK, 'build')
WORLDS = os.path.join(WORK, 'worlds')
KB = os.path.join(WORK, 'kb')

def analyze(domain, variant, kb, agent):
    vp = os.path.join(WORLDS, variant + '.txt')
    kbp = os.path.join(KB, kb)
    r = subprocess.run([os.path.join(BUILD, agent), vp, variant, '0', kbp],
                       capture_output=True, text=True)
    lines = r.stdout.split('\n')
    # Parse trace: RECALL <hid>, EVAL <hid> <score>, VERDICT <act>
    # Heuristic action mapping (from KB)
    # For D2: d00->2, d01->1, d10->1, d11->0
    # For D3: t0->0, t1->1, t2->2, t0b->1, t1b->2, t2b->0
    h_act = {}
    if domain == 'd2':
        h_act = {'d00': 2, 'd01': 1, 'd10': 1, 'd11': 0}
    else:
        h_act = {'t0': 0, 't1': 1, 't2': 2, 't0b': 1, 't1b': 2, 't2b': 0}
    
    contested = 0
    total = 0
    i = 0
    while i < len(lines):
        if lines[i].startswith('RECALL'):
            hid = lines[i].split()[1]
            # Next: EVAL
            i += 1
            if i < len(lines) and lines[i].startswith('EVAL'):
                # Next: VERDICT
                i += 1
                if i < len(lines) and lines[i].startswith('VERDICT'):
                    act = int(lines[i].split()[1])
                    total += 1
                    if hid in h_act and act != h_act[hid]:
                        contested += 1
        i += 1
    return total, contested

for d, v, kb, ag in [('d2', 'd2_s0', 'home_d2.txt', 'agent_d_d2'),
                     ('d3', 'd3_s0', 'home_d3.txt', 'agent_d_d3')]:
    total, contested = analyze(d, v, kb, ag)
    frac = contested / total if total else 0
    print(f"{d} {v}: {contested}/{total} contested ({frac:.1%})")
