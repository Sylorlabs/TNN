#!/usr/bin/env python3
# Summarize WS2-A trace files into the failure map.
import sys, glob
from collections import Counter, defaultdict

def qclass(qid):
    if qid.startswith('QPA') or qid.startswith('QPZ'): return 'P-AGE'
    if qid.startswith('QPC'): return 'P-COLL-C1'
    if qid.startswith('QPD'): return 'P-COLL-C2'
    if qid.startswith('QX1'): return 'P-CTX-X1'
    if qid.startswith('QX2'): return 'P-CTX-X2'
    if qid.startswith('QX3'): return 'P-CTX-X3'
    if qid.startswith('QP'): return 'P-PARA'
    if qid.startswith('QN'): return 'P-NEG'
    return '??'

for path in sorted(glob.glob(sys.argv[1])):
    arm = path.split('trace_')[1].split('.')[0]
    print(f'=== {arm} ===')
    oc = Counter(); fp = Counter()
    byclass = defaultdict(Counter)
    fails = []
    for ln in open(path):
        f = ln.rstrip('\n').split('|')
        # qid|kind|scheme|installed|candidate|m0,m1,m2|score|rank|top1|nret|outcome|fail
        qid, kind, scheme, inst, cand, lv, score, rank, top1, nret, outcome, fail = f
        oc[outcome] += 1; fp[fail] += 1
        byclass[qclass(qid)][outcome] += 1
        if outcome != 'FOUND' and outcome != 'CORRECT_ABSTAIN':
            fails.append((qid, scheme, inst, cand, lv, score, rank, top1, nret, outcome, fail))
    print('outcomes:', dict(oc))
    print('fail_points:', dict(fp))
    for c in sorted(byclass):
        print(f'  {c}:', dict(byclass[c]))
    for row in fails:
        print('  FAIL', '|'.join(row))
    print()
