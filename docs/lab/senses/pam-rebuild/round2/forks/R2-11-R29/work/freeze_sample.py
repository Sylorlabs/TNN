#!/usr/bin/env python3
"""Re-freeze the 200-trial double-blind human sample for R2-11 (R2-9 lineage).

Deterministic glue seed 20260923 (same as pre-collision procedure):
  100 clean from the harness primary/noise pool (families harness-primary,
    harness-noise; clean = split 'normal');
  100 adversarial stratified across all 18 adversarial families
    (17 R2A-* families + harness-adversarial), incl. COL-1, SHP-1, MOT-1,
    TMB-2 by construction.
Writes human/sample200.tsv + sample200.sha256.
"""
import random, hashlib
from collections import Counter

seed = 20260923
rng = random.Random(seed)
rows = [l.rstrip('\n').split('\t') for l in open('trials.tsv')][1:]

clean = [r for r in rows if r[3] in ('harness-primary', 'harness-noise')]
adv_fams = sorted({r[3] for r in rows if r[2] == 'adversarial'})
print('adversarial families:', len(adv_fams), adv_fams)

clean_s = rng.sample(clean, 100)

# stratify 100 across families: base quota + remainder by seeded shuffle
adv_by_fam = {f: [r for r in rows if r[3] == f] for f in adv_fams}
quota, rem = divmod(100, len(adv_fams))
adv_s = []
fams = adv_fams[:]
rng.shuffle(fams)
for i, f in enumerate(fams):
    q = quota + (1 if i < rem else 0)
    adv_s += rng.sample(adv_by_fam[f], q)
assert len(adv_s) == 100

# guarantee the four required injections
def ensure(fam, code):
    pool = [r for r in adv_by_fam[fam]]
    if any(r[0] in {x[0] for x in adv_s} for r in pool):
        return
    drop_pool = [x for x in adv_s if x[1] == pool[0][1] and x[3] != fam]
    drop = rng.choice(drop_pool)
    adv_s.remove(drop)
    adv_s.append(rng.choice(pool))

ensure('R2A-COL-1', 'COL-1')
ensure('R2A-SHP-1', 'SHP-1')
ensure('R2A-MOT-1', 'MOT-1')
ensure('R2A-TMB-2', 'TMB-2')

sample = clean_s + adv_s
rng.shuffle(sample)
blob = '\t'.join(rows[0] if False else '')  # placeholder
hdr = open('trials.tsv').readline()
open('human/sample200.tsv', 'w').write(hdr + ''.join('\t'.join(r) + '\n' for r in sample))
h = hashlib.sha256(open('human/sample200.tsv', 'rb').read()).hexdigest()
open('human/sample200.sha256', 'w').write(h + '  sample200.tsv\n')
print('sample200 sha256:', h)
print('clean splits:', Counter(r[2] for r in clean_s))
print('adv tasks:', Counter(r[1] for r in adv_s))
print('injections present:', all(any(r[3] == f for r in adv_s) for f in
      ('R2A-COL-1', 'R2A-SHP-1', 'R2A-MOT-1', 'R2A-TMB-2')))
