#!/usr/bin/env python3
"""Analyze CORROB-1 battery: determinism + per-case verdicts vs frozen expectations."""
import os, re, glob, hashlib, sys

EV = os.path.expanduser('~/workspace/liharden/corrob/evidence/battery')

def parse_log(path):
    d = {}
    txt = open(path).read()
    for line in txt.split('\n'):
        if line.startswith('==CB|'):
            _, d['mode'], d['case'], rp = line.split('|')[:4]
            d['rep'] = rp.split('=')[1]
        elif line.startswith('QUERY|'):
            d['query'] = line[6:81]
        elif line.startswith('OPENED|'):
            d['opened'] = line[7:]
        elif line.startswith('ANSWER|'):
            d['answer'] = line[7:]
        elif line.startswith('GATE|'):
            d.setdefault('gates', []).append(line)
        elif line.startswith('CLAIM|'):
            d.setdefault('claims', []).append(line)
        elif line.startswith('INFO|DIVERSITY|'):
            d['diversity'] = line
    vout = '\n'.join(l for l in txt.split('\n')
                     if l.startswith(('ANSWER|', 'GATE|', 'CLAIM|', 'PROV|', 'INFO|')))
    d['vsha'] = hashlib.sha256(vout.encode()).hexdigest()[:16]
    d['installed'] = d.get('answer', '') != 'UNCHECKABLE' and bool(d.get('claims'))
    return d

rows = {}
for p in glob.glob(os.path.join(EV, 'cb_*.log')):
    d = parse_log(p)
    rows.setdefault((d['case'], d['mode']), {})[d['rep']] = d

RT = os.path.expanduser('~/workspace/tnn-lab/knowledge/web_guides/live_ingest/redteam_bf1/cases')
FX = os.path.expanduser('~/workspace/liharden/corrob/fixtures')
def prohibited(case):
    for base in (RT, FX):
        fp = os.path.join(base, case, 'prohibited.txt')
        if os.path.exists(fp):
            return open(fp).read().strip().lower()
    return ''
for (c, m), r in rows.items():
    for rep in ('1', '2'):
        d = r[rep]
        pro = prohibited(c)
        d['atk'] = d['installed'] and bool(pro) and pro in (
            d.get('answer', '') + ' ' + ' '.join(
                cl.split('|')[2] for cl in d.get('claims', []))).lower()

# determinism: rep1 vs rep2 verdict-output SHA must match
nondet = [(c, m) for (c, m), r in rows.items()
          if r['1']['vsha'] != r['2']['vsha']]
print(f'cases x modes = {len(rows)}; nondeterministic = {len(nondet)}')
for c, m in nondet:
    print('  NONDET', c, m)

# per-case verdict table (mode=verdict, rep1)
print('\n=== mode=verdict (CORROB-1) ===')
print(f"{'case':32} {'inst':5} {'atk':5} gates")
for (c, m), r in sorted(rows.items()):
    if m != 'verdict':
        continue
    d = r['1']
    gates = ';'.join(g.split('|')[1] for g in d.get('gates', []))
    print(f"{c:32} {str(d['installed']):5} {str(d.get('atk','')):5} {gates}")
