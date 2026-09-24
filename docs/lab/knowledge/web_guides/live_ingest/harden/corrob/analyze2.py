#!/usr/bin/env python3
"""Full comparative analysis: CORROB-1 vs prior BF1, per-mode tables, expectation checks."""
import os, re, glob, hashlib

EV = os.path.expanduser('~/workspace/liharden/corrob/evidence/battery')
RT = os.path.expanduser('~/workspace/tnn-lab/knowledge/web_guides/live_ingest/redteam_bf1/cases')
FX = os.path.expanduser('~/workspace/liharden/corrob/fixtures')
SUM = os.path.expanduser('~/workspace/tnn-lab/knowledge/web_guides/live_ingest/redteam_bf1/SUMMARY.tsv')

def parse_log(path):
    d = {}
    txt = open(path).read()
    for line in txt.split('\n'):
        if line.startswith('==CB|'):
            _, d['mode'], d['case'], rp = line.split('|')[:4]
            d['rep'] = rp.split('=')[1]
        elif line.startswith('OPENED|'):
            d['opened'] = line[7:]
        elif line.startswith('ANSWER|'):
            d['answer'] = line[7:]
        elif line.startswith('GATE|'):
            d.setdefault('gates', []).append(line)
        elif line.startswith('CLAIM|'):
            d.setdefault('claims', []).append(line)
    vout = '\n'.join(l for l in txt.split('\n')
                     if l.startswith(('ANSWER|', 'GATE|', 'CLAIM|', 'PROV|', 'INFO|')))
    d['vsha'] = hashlib.sha256(vout.encode()).hexdigest()[:16]
    d['installed'] = d.get('answer', '') != 'UNCHECKABLE' and bool(d.get('claims'))
    return d

def prohibited(case):
    for base in (RT, FX):
        fp = os.path.join(base, case, 'prohibited.txt')
        if os.path.exists(fp):
            return open(fp).read().strip().lower()
    return ''

rows = {}
for p in glob.glob(os.path.join(EV, 'cb_*.log')):
    d = parse_log(p)
    rows.setdefault((d['case'], d['mode']), {})[d['rep']] = d
for (c, m), r in rows.items():
    for rep in ('1', '2'):
        d = r[rep]
        pro = prohibited(c)
        d['atk'] = d['installed'] and bool(pro) and pro in (
            d.get('answer', '') + ' ' + ' '.join(
                cl.split('|')[2] for cl in d.get('claims', []))).lower()

# prior BF1 results
prior = {}
for line in open(SUM):
    f = line.rstrip('\n').split('\t')
    if len(f) >= 6 and f[2] == 'bf1':
        prior[f[1]] = (f[3] == 'True', f[4] == 'True', f[6][:50] if len(f) > 6 else '')

print('=== CORROB-1 (verdict) vs prior BF1 on 38 redteam cases ===')
print(f"{'case':28} {'prior':12} {'corrob':20} note")
n_prior_false = n_corrob_false = 0
for c in sorted(prior):
    pi, pf, pans = prior[c]
    d = rows[(c, 'verdict')]['1']
    ps = f"inst={pi} fi={pf}"
    cs = f"inst={d['installed']} atk={d['atk']}"
    gates = ';'.join(g.split('|')[1] for g in d.get('gates', []))
    if pf:
        n_prior_false += 1
    if d['atk']:
        n_corrob_false += 1
    flag = ''
    if pf and not d['atk']:
        flag = 'KILLED'
    elif not pf and d['atk']:
        flag = 'NEW-MISS'
    print(f"{c:28} {ps:12} {cs:20} {gates} {flag}")
print(f'\nprior false installs: {n_prior_false}/38; corrob false installs: {n_corrob_false}/38')
