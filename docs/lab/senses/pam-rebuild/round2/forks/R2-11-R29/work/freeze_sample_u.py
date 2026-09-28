#!/usr/bin/env python3
"""Freeze a CLEAN 200-trial human sample with UNIQUE trial ids.

Deviation from prereg (documented): the prereg specifies 100 clean from the
harness primary/noise pool, but harness trial ids repeat across tasks
(colliding artifact names). This sample uses 100 clean from the generated
normal pool (R2N, split='normal') and 100 adversarial stratified across the
17 R2A families, all with unique ids. Seed 20260923 (same as before).
"""
import random, hashlib
from collections import Counter

seed = 20260923
rng = random.Random(seed)
rows = [l.rstrip('\n').split('\t') for l in open('trials.tsv')][1:]
c = Counter(r[0] for r in rows)
uniq = [r for r in rows if c[r[0]] == 1]

clean = [r for r in uniq if r[3] == 'R2N']
adv_fams = sorted({r[3] for r in uniq if r[2] == 'adversarial'})
print('adv families:', len(adv_fams))

clean_s = rng.sample(clean, 100)
adv_by_fam = {f: [r for r in uniq if r[3] == f] for f in adv_fams}
quota, rem = divmod(100, len(adv_fams))
fams = adv_fams[:]
rng.shuffle(fams)
adv_s = []
for i, f in enumerate(fams):
    q = quota + (1 if i < rem else 0)
    adv_s += rng.sample(adv_by_fam[f], q)
assert len(adv_s) == 100

def ensure(fam):
    if any(x[3] == fam for x in adv_s):
        return
    pool = adv_by_fam[fam]
    drop_pool = [x for x in adv_s if x[1] == pool[0][1] and x[3] != fam]
    drop = rng.choice(drop_pool)
    adv_s.remove(drop)
    adv_s.append(rng.choice(pool))

for f in ('R2A-COL-1', 'R2A-SHP-1', 'R2A-MOT-1', 'R2A-TMB-2'):
    ensure(f)

sample = clean_s + adv_s
rng.shuffle(sample)
hdr = open('trials.tsv').readline()
open('human/sample200u.tsv', 'w').write(hdr + ''.join('\t'.join(r) + '\n' for r in sample))
h = hashlib.sha256(open('human/sample200u.tsv', 'rb').read()).hexdigest()
open('human/sample200u.sha256', 'w').write(h + '  sample200u.tsv\n')
print('sample200u sha256:', h)
print('clean tasks:', Counter(r[1] for r in clean_s))
print('adv tasks:', Counter(r[1] for r in adv_s))
print('injections:', all(any(r[3] == f for r in adv_s) for f in
      ('R2A-COL-1', 'R2A-SHP-1', 'R2A-MOT-1', 'R2A-TMB-2')))
