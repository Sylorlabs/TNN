#!/usr/bin/env python3
"""QB coding results summarizer: per-arm table + determinism digests."""
import json, glob
from collections import Counter

def load(cell, r):
    return json.load(open('runs/qb_%s_r%d.json' % (cell, r)))

def cell_stats(cell):
    reps = [load(cell, r) for r in (1, 2, 3)]
    digests = []
    for r in (1, 2, 3):
        with open('runs/qb_%s_r%d.log' % (cell, r)) as f:
            for line in f:
                if 'digest' in line:
                    digests.append(line.split('digest')[1].split()[0])
    d = reps[0]
    oc = Counter(i['outcome'] for i in d['items'])
    passes = sum(1 for i in d['items'] if i['outcome'] == 'pass')
    halts = sum(1 for i in d['items'] if i['outcome'] in ('halt-genfail', 'halt-no-patch'))
    iters = sum(i['iters_used'] for i in d['items'])
    znc = d['stats']['znc_invocations']
    evals = sum(int(x.get('evals', '0')) for i in d['items'] for x in i['iters']
                if str(x.get('evals', '?')).isdigit())
    wall = sum(i['time_s'] for i in d['items'])
    cpu = sum(i['cpu_s'] for i in d['items'])
    det = len(set(digests)) == 1 and len(digests) == 3
    return {'outcomes': dict(oc), 'pass': passes, 'halts': halts, 'iters': iters,
            'znc': znc, 'evals': evals, 'wall': wall, 'cpu': cpu,
            'digests': digests, 'det': det}

cells = ['d0', 'd1', 'd2', 'd3', 'd4', 'd5']
rows = {c: cell_stats(c) for c in cells}
base = rows['d0']
print('| arm | Q_c | halts | iters | znc | hyp-evals | wall_s | cpu_s | d_evals | d_znc | digest |')
print('|---|---|---|---|---|---|---|---|---|---|---|')
for c in cells:
    r = rows[c]
    de = r['evals'] - base['evals']
    dz = r['znc'] - base['znc']
    print('| %s | %d/18 | %d/2 | %d | %d | %d | %.1f | %.1f | %+d | %+d | %s |' % (
        c.upper(), r['pass'], r['halts'], r['iters'], r['znc'], r['evals'],
        r['wall'], r['cpu'], de, dz, r['digests'][0][:12]))
print()
for c in cells:
    r = rows[c]
    print('%s determinism: %s digests=%s' % (c.upper(), 'IDENTICAL' if r['det'] else 'MISMATCH', r['digests'][0][:12]))
print()
for c in cells:
    r = rows[c]
    print('%s outcomes: %s' % (c.upper(), r['outcomes']))
