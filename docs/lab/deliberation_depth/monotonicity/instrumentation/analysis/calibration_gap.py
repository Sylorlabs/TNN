#!/usr/bin/env python3
"""Micah's law baseline: G(d) = mean(conf)/1000 - accuracy per family per depth,
plus per-item overconfidence violations across depth steps.
Deterministic inputs: all cells A/B byte-diffed."""
import json
from collections import defaultdict

D = '/home/hatch/workspace/tnn-lab/deliberation_depth/monotonicity/instrumentation/run'

def fam(i):
    if i.startswith('H5B-P-'): return 'P'
    if i.startswith('H5B-O-'): return 'O'
    if i.startswith('H5B-D-'): return 'D'
    if i.startswith('TRAP-'): return 'trap'
    return 'logic_ne1'

def load(cell):
    out = {}
    with open(f'{D}/{cell}_A.jsonl') as f:
        for line in f:
            r = json.loads(line)
            out[r['id']] = (r['confidence'] / 1000.0, r['correct'])
    return out

SWEEPS = {
    'ceiling': [('c64_d1',1),('c64_d2',2),('c64_d4',4),('c64_d8',8),('c64_d16',16),('c64_d32',32),('c64_d64',64)],
    'trap':    [('fz_d1',1),('fz_d2',2),('fz_d4',4),('fz_d8',8),('fz_deep16',16)],
    'logic':   [('fz_d1',1),('fz_deep16',16)],
}
CELLP = {'ceiling':'ceil_','trap':'trap_','logic':'logicne1_'}

print('=== G(d) = mean(conf)/1000 - accuracy  [law requires G(d+1)<=G(d)] ===')
G = {}
for bank, cells in SWEEPS.items():
    print(f'--- {bank} ---')
    prev = {}
    for cell, d in cells:
        data = load(CELLP[bank]+cell)
        byfam = defaultdict(list)
        for i,(c,a) in data.items(): byfam[fam(i)].append((c,a))
        for f in sorted(byfam):
            v = byfam[f]; mc = sum(x[0] for x in v)/len(v); acc = sum(x[1] for x in v)/len(v)
            g = mc-acc; G[(bank,f,d)] = g
            flag = ''
            if f in prev and g > prev[f] + 1e-9: flag = '  <-- LAW VIOLATION: G increased'
            print(f'  d={d:>2} fam={f:>9} n={len(v):>3} mean_conf={mc:.3f} acc={acc:.3f} G={g:+.3f}{flag}')
            prev[f] = g

print()
print('=== current release policy (residual-flip bound / adaptive) as single points ===')
for cell, label in [('ceil_c64_bound','bound'),('ceil_c64_adaptive','adaptive')]:
    data = load(cell)
    byfam = defaultdict(list)
    for i,(c,a) in data.items(): byfam[fam(i)].append((c,a))
    for f in sorted(byfam):
        v = byfam[f]; mc = sum(x[0] for x in v)/len(v); acc = sum(x[1] for x in v)/len(v)
        print(f'  {label:>8} fam={f}: n={len(v)} mean_conf={mc:.3f} acc={acc:.3f} G={mc-acc:+.3f}')

print()
print('=== per-item violations across consecutive depth steps ===')
print('unforgivable: correct 1->0 AND conf(d+1)>=conf(d)')
print('theater:      correct 0->0 AND conf(d+1)>conf(d)')
tot_u = defaultdict(int); tot_t = defaultdict(int); tot_n = defaultdict(int)
for bank, cells in SWEEPS.items():
    print(f'--- {bank} ---')
    for (c1,d1),(c2,d2) in zip(cells, cells[1:]):
        A = load(CELLP[bank]+c1); B = load(CELLP[bank]+c2)
        u = defaultdict(int); t = defaultdict(int); n = defaultdict(int)
        for i in A:
            if i not in B: continue
            f = fam(i); n[f]+=1; tot_n[(bank,f)]+=1
            ca, aa = A[i]; cb, ab = B[i]
            if aa==1 and ab==0 and cb>=ca: u[f]+=1; tot_u[(bank,f)]+=1
            if aa==0 and ab==0 and cb>ca:  t[f]+=1; tot_t[(bank,f)]+=1
        for f in sorted(n):
            print(f'  d{d1}->d{d2} fam={f:>9}: unforgivable {u[f]}/{n[f]}  theater {t[f]}/{n[f]}')
print()
print('=== totals per (bank, family) across all steps ===')
for k in sorted(tot_n):
    print(f'  {k[0]:>7} {k[1]:>9}: unforgivable {tot_u[k]}/{tot_n[k]}  theater {tot_t[k]}/{tot_n[k]}')
