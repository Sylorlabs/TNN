#!/usr/bin/env python3
"""Aggregate corpus results.jsonl -> corpus_aggregate.json + summary CSV."""
import json, csv, os
from collections import defaultdict

P2 = '/home/hatch/workspace/exact_audio_replication/phase2'
IN = os.path.join(P2, 'run', 'full', 'results.jsonl')
OUTD = os.path.join(P2, 'results')
os.makedirs(OUTD, exist_ok=True)

rows = [json.loads(l) for l in open(IN)]
by_class = defaultdict(list)
for r in rows:
    cls = r['clip'].split('/corpus/')[1].split('/')[0]
    by_class[cls].append(r)

agg = {'total': len(rows), 'pass': 0, 'by_class': {}}
for cls, rs in sorted(by_class.items()):
    p = sum(1 for r in rs if r.get('byte_identical'))
    det = sum(1 for r in rs if r.get('deterministic'))
    seal = sum(1 for r in rs if r.get('seal_match'))
    rms = [r['sem_rms'] for r in rs if 'sem_rms' in r]
    cor = [r['sem_corr'] for r in rs if 'sem_corr' in r]
    agg['pass'] += p
    agg['by_class'][cls] = {
        'n': len(rs), 'pass': p, 'deterministic': det, 'seal_match': seal,
        'sem_rms_mean': sum(rms)/len(rms), 'sem_rms_max': max(rms),
        'sem_corr_mean': sum(cor)/len(cor), 'sem_corr_min': min(cor),
    }

json.dump(agg, open(os.path.join(OUTD, 'corpus_aggregate.json'), 'w'), indent=1)

# compact per-clip CSV (evidence, no WAVs)
with open(os.path.join(OUTD, 'corpus_results.csv'), 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['clip', 'class', 'seal_match', 'byte_identical', 'deterministic',
                'sem_rms_LSB', 'sem_corr', 'use_h', 'n'])
    for r in rows:
        cls = r['clip'].split('/corpus/')[1].split('/')[0]
        use_h = ''
        for line in r.get('resid_log', []):
            if 'use_h=' in line:
                use_h = line.split('use_h=')[1].split()[0]
        w.writerow([r['name'], cls, r.get('seal_match'), r.get('byte_identical'),
                    r.get('deterministic'),
                    round(r.get('sem_rms', -1), 2), round(r.get('sem_corr', -1), 5),
                    use_h, ''])

print(json.dumps(agg, indent=1))
fails = [r['name'] for r in rows if not r.get('byte_identical')]
print('FAILURES:', fails if fails else 'none')
