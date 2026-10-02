#!/usr/bin/env python3
# join_percepts.py — Python fixture glue for the R2-8 mapping-freeze battery.
#
# Joins trial lists with the pure-Zag percept dump to produce AUGMENTED trial
# TSVs for gate2.zag (stage 2). The percepts themselves are computed by pure
# Zag (dump.zag); this script is only data plumbing (allowed: Python for
# fixture/analysis glue). The gate, ledger, and bars remain pure Zag.
#
# Usage: join_percepts.py <mapping_freeze_dir>
#   Reads: trials/trials_p.tsv, trials_q.tsv, recall_p.tsv, primary.tsv
#          percepts/percept_p.tsv, percept_q.tsv, percept_r.tsv, percept_prim.tsv
#   Writes: percepts/aug_p.tsv, aug_q.tsv, aug_r.tsv, aug_prim.tsv
#
# Augmented adversarial/recall row (22 fields):
#   trial_id task relX relS relP1 relP2 relP3 truth
#   jX cX fX jS cS jP1 cP1 fP1 jP2 cP2 fP2 jP3 cP3 fP3
# Note: fS (feature of S) is NOT included — the gate never uses it.
# Augmented primary row (8 fields):
#   task rel truth judgment confidence margin feature ops
import sys, os

mf = sys.argv[1]
td = os.path.join(mf, 'trials')
pd = os.path.join(mf, 'percepts')

def load_percepts(path):
    d = {}
    with open(path) as f:
        for line in f:
            p = line.rstrip('\n').split('\t')
            # task, rel, judgment, confidence, margin, feature, ops
            d[(p[0], p[1])] = (p[2], p[3], p[4], p[5], p[6])
    return d

pp = load_percepts(os.path.join(pd, 'percept_p.tsv'))
pq = load_percepts(os.path.join(pd, 'percept_q.tsv'))
pr = load_percepts(os.path.join(pd, 'percept_r.tsv'))
pm = load_percepts(os.path.join(pd, 'percept_prim.tsv'))
print(f"loaded percepts: p={len(pp)} q={len(pq)} r={len(pr)} prim={len(pm)}", flush=True)

def get(d, task, rel):
    k = (task, rel)
    if k not in d:
        raise KeyError(f"missing percept for {k}")
    return d[k]

# p-adv: all from percept_p (fS excluded — gate never uses it)
n = 0
with open(os.path.join(td, 'trials_p.tsv')) as fin, \
     open(os.path.join(pd, 'aug_p.tsv'), 'w') as out:
    for line in fin:
        f = line.rstrip('\n').split('\t')
        tid, task, relX, relS, p1, p2, p3, truth = f
        jX, cX, mX, fX, oX = get(pp, task, relX)
        jS, cS, mS, fS, oS = get(pp, task, relS)
        j1, c1, m1, f1, o1 = get(pp, task, p1)
        j2, c2, m2, f2, o2 = get(pp, task, p2)
        j3, c3, m3, f3, o3 = get(pp, task, p3)
        out.write('\t'.join([tid, task, relX, relS, p1, p2, p3, truth,
                             jX, cX, fX, jS, cS,
                             j1, c1, f1, j2, c2, f2, j3, c3, f3]) + '\n')
        n += 1
print(f"aug_p.tsv: {n}", flush=True)

# q-adv: X from percept_p, S/P1..P3 from percept_q (fS excluded)
n = 0
with open(os.path.join(td, 'trials_q.tsv')) as fin, \
     open(os.path.join(pd, 'aug_q.tsv'), 'w') as out:
    for line in fin:
        f = line.rstrip('\n').split('\t')
        tid, task, relX, relS, p1, p2, p3, truth = f
        jX, cX, mX, fX, oX = get(pp, task, relX)
        jS, cS, mS, fS, oS = get(pq, task, relS)
        j1, c1, m1, f1, o1 = get(pq, task, p1)
        j2, c2, m2, f2, o2 = get(pq, task, p2)
        j3, c3, m3, f3, o3 = get(pq, task, p3)
        out.write('\t'.join([tid, task, relX, relS, p1, p2, p3, truth,
                             jX, cX, fX, jS, cS,
                             j1, c1, f1, j2, c2, f2, j3, c3, f3]) + '\n')
        n += 1
print(f"aug_q.tsv: {n}", flush=True)

# recall: all from percept_r (fS excluded)
n = 0
with open(os.path.join(td, 'recall_p.tsv')) as fin, \
     open(os.path.join(pd, 'aug_r.tsv'), 'w') as out:
    for line in fin:
        f = line.rstrip('\n').split('\t')
        tid, task, relX, relS, p1, p2, p3, truth = f
        jX, cX, mX, fX, oX = get(pr, task, relX)
        jS, cS, mS, fS, oS = get(pr, task, relS)
        j1, c1, m1, f1, o1 = get(pr, task, p1)
        j2, c2, m2, f2, o2 = get(pr, task, p2)
        j3, c3, m3, f3, o3 = get(pr, task, p3)
        out.write('\t'.join([tid, task, relX, relS, p1, p2, p3, truth,
                             jX, cX, fX, jS, cS,
                             j1, c1, f1, j2, c2, f2, j3, c3, f3]) + '\n')
        n += 1
print(f"aug_r.tsv: {n}", flush=True)

# primary: from percept_prim
n = 0
with open(os.path.join(td, 'primary.tsv')) as fin, \
     open(os.path.join(pd, 'aug_prim.tsv'), 'w') as out:
    for line in fin:
        f = line.rstrip('\n').split('\t')
        task, rel, truth = f
        j, c, m, fv, o = get(pm, task, rel)
        out.write('\t'.join([task, rel, truth, j, c, m, fv, o]) + '\n')
        n += 1
print(f"aug_prim.tsv: {n}", flush=True)
print("JOIN OK", flush=True)
