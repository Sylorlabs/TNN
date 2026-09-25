#!/usr/bin/env python3
"""Package 4: BAR search. Enumerate ALL grammar-legal 1-rule L1 policies,
feed each to the REAL fixed proposer (empty champion, frozen 22/2/424 args),
collect verdicts. Goal: find policies with novel_diff=0 AND improved>=2 that
reach BAR (dacc<1 or dwrong>0) -> T-WEAK-2a/b real verdicts.
Deterministic. No RNG."""
import subprocess, os, csv

BASE = os.path.expanduser('~/workspace/tnn-lab/rsi/autonomous_run_2')
R4 = f'{BASE}/work/r4'
PROPOSER = f'{R4}/proposer_fixed'

with open(f'{BASE}/build/proxy_battery.csv') as f:
    GT = ''
    for row in csv.DictReader(f):
        g = row['gt']
        GT += '1' if g == 'NEW' else ('2' if g == 'OLD' else '0')

TMPL = open(f'{BASE}/work/redo_run/delb_rev1.txt').read().split('\n')
PI = TMPL.index('POLICY d1pick')
PE = TMPL.index('END', PI)

ATOMS = {1: ('pre_is', [0, 1, 2]), 2: ('chan_present', [None]),
         3: ('chan_silent', [None]), 4: ('sm_le', range(-6, 7)),
         5: ('sm_ge', range(-6, 7)), 6: ('sm_eq', range(-6, 7)),
         7: ('dir_is', [0, 1, 2]), 8: ('sn_ge', range(-3, 4)),
         9: ('so_ge', range(-3, 4)), 10: ('chan_agree_old', [None]),
         11: ('chan_agree_new', [None]), 12: ('post_is', [0, 1, 2]),
         13: ('psm_le', range(-6, 7)), 14: ('psm_ge', range(-6, 7)),
         15: ('psm_eq', range(-6, 7))}
NAMES = {0: 'HOLD', 1: 'NEW', 2: 'OLD'}
DNAMES = {0: 'TIE', 1: 'NEW_LEAD', 2: 'OLD_LEAD'}

def atom_text(aid, prm):
    nm, _ = ATOMS[aid]
    if prm is None:
        return nm
    if aid == 1:
        return f'{nm}({NAMES[prm]})'
    if aid == 7:
        return f'{nm}({DNAMES[prm]})'
    if aid == 12:
        return f'{nm}({NAMES[prm]})'
    return f'{nm}({prm})'

def act_text(acid, aprm):
    if acid == 1:
        return 'force_consult'
    if acid == 2:
        return 'block_consult'
    if acid == 3:
        return 'force_withhold'
    if acid == 4:
        return f'force_install({NAMES[aprm]})'
    return f'recompute_only({aprm:03b})'

cands = []  # (l1_rule, aid, prm, acid, aprm)
# stage 1: atoms 1-11 x actions 1,2
for aid in range(1, 12):
    for prm in ATOMS[aid][1]:
        for acid in (1, 2):
            cands.append((f'RULE 1 IF {atom_text(aid, prm)} THEN {act_text(acid, 0)}', aid, prm, acid, 0))
# stage 2: atoms 12-15 x actions 3,4(prm 1,2)
for aid in range(12, 16):
    for prm in ATOMS[aid][1]:
        cands.append((f'RULE 1 IF {atom_text(aid, prm)} THEN {act_text(3, 0)}', aid, prm, 3, 0))
        for aprm in (1, 2):
            cands.append((f'RULE 1 IF {atom_text(aid, prm)} THEN {act_text(4, aprm)}', aid, prm, 4, aprm))
# stage 4: atoms 1-11 x action 5 (masks 0-7)
for aid in range(1, 12):
    for prm in ATOMS[aid][1]:
        for mask in range(8):
            cands.append((f'RULE 1 IF {atom_text(aid, prm)} THEN {act_text(5, mask)}', aid, prm, 5, mask))

print(f'# BAR search: {len(cands)} candidates, proposer 55f5999d (P1 sign-fix)')
tallies = {}
bar_hits = []
accepts = []
for idx, (rule, aid, prm, acid, aprm) in enumerate(cands):
    body = TMPL[:PI] + ['POLICY d1pick', rule, 'END'] + TMPL[PE + 1:]
    delb = '\n'.join(body)
    args = [PROPOSER, delb] + [''] * 8 + ['22', '2', '424', GT, 'barsearch']
    r = subprocess.run(args, capture_output=True, text=True)
    out = r.stdout.strip().split('\n')[0] if r.stdout.strip() else 'EMPTY'
    key = out.split(',')[0] if ',' in out else out
    # normalize: keep full check=... detail
    tallies[out] = tallies.get(out, 0) + 1
    if out.startswith('REJECTED,check=BAR'):
        bar_hits.append((rule, out))
    if out.startswith('ACCEPT') or out.startswith('PROPOSE'):
        accepts.append((rule, out))

print('# verdict tallies:')
for k in sorted(tallies):
    print(f'    {tallies[k]:4d}  {k}')
print(f'# BAR hits: {len(bar_hits)}')
for rule, out in bar_hits:
    print(f'  BAR {out} :: {rule}')
print(f'# ACCEPT/PROPOSE (constitutional findings): {len(accepts)}')
for rule, out in accepts:
    print(f'  FINDING {out} :: {rule}')

with open(f'{R4}/bar_search.txt', 'w') as f:
    f.write(f'# BAR search: {len(cands)} candidates\n')
    for k in sorted(tallies):
        f.write(f'    {tallies[k]:4d}  {k}\n')
    f.write(f'# BAR hits: {len(bar_hits)}\n')
    for rule, out in bar_hits:
        f.write(f'  BAR {out} :: {rule}\n')
    f.write(f'# findings: {len(accepts)}\n')
    for rule, out in accepts:
        f.write(f'  FINDING {out} :: {rule}\n')
print('wrote work/r4/bar_search.txt')
