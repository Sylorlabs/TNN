#!/usr/bin/env python3
"""Analyze Crew P battery results: hits, exact binomial p-values, pool gaps.

Reads evidence/run{1,2,3}/answers_run{N}.json. Checks byte-identity across runs.
"""
import json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
EV = os.path.join(HERE, 'evidence')

def binom_sf(k, n, p):
    # P(X >= k), exact
    s = 0.0
    for j in range(k, n + 1):
        s += math.comb(n, j) * (p ** j) * ((1 - p) ** (n - j))
    return s

man = json.load(open(os.path.join(HERE, 'manifest_p.json')))
runs = {}
for t in ['run1', 'run2', 'run3']:
    runs[t] = json.load(open(os.path.join(EV, t, 'answers_%s.json' % t)))

# byte-identity: compare answer dicts
r1, r2, r3 = runs['run1'], runs['run2'], runs['run3']
ident12 = json.dumps(r1, sort_keys=True) == json.dumps(r2, sort_keys=True)
ident13 = json.dumps(r1, sort_keys=True) == json.dumps(r3, sort_keys=True)
print('byte-identical run1==run2:', ident12, ' run1==run3:', ident13)

bars = {'pitchrel': (100, 0.50, 63), 'pitchabs': (60, 1/24, 8),
        'env': (60, 1/3, 30), 'rhy': (100, 0.50, 63), 'hf': (20, 0.50, None)}
for name, (n, p, bar) in bars.items():
    qs = man['batteries'][name]
    hits = sum(r1[q['qid']]['hit'] for q in qs)
    pv = binom_sf(hits, n, p)
    status = 'PASS' if bar and hits >= bar else ('n/a' if not bar else 'FAIL')
    print('%s: %d/%d (chance %.4f) p=%.6f bar=%s -> %s' % (name, hits, n, p, pv, bar, status))
    # pool gap (P-R2): first half p0, second half p1
    h0 = sum(r1[q['qid']]['hit'] for q in qs[:n//2])
    h1 = sum(r1[q['qid']]['hit'] for q in qs[n//2:])
    gap = abs(h0 - h1) / (n // 2) * 100
    flag = 'POOL-BRITTLE' if gap > 15 else 'ok'
    print('  pool p0: %d/%d p1: %d/%d gap=%.1fpp %s' % (h0, n//2, h1, n//2, gap, flag))

# P-R5
pr5 = man['pr5']
hits = sum(r1[q['qid']]['hit'] for q in pr5)
print('pr5: %d/%d' % (hits, len(pr5)))
# P-R4
pr4 = man['pr4']
ag = sum(r1[q['qid']]['agree'] for q in pr4) / len(pr4)
print('pr4: mean bit-agreement %.3f (target >=0.90)' % ag)
