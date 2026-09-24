#!/usr/bin/env python3
# FS-E4b: apply the frozen selection rule to fresh-draw judgments.
# F-fooled := adv candidate with formF != truth (first 2000 in idx order).
# TRUE     := norm candidate (first 1000 in idx order).
# Qualification: >=2000 F-fooled AND >=1000 TRUE per task.
# Usage: select_battery.py <cand_dir> <evidence_dir> <lists_dir>
# Writes evidence/battery_e4b.tsv + per-task battery list files; prints counts.
import sys, os, hashlib, json

TASKS = ['colordisc', 'colorconst', 'pitchdisc', 'timbredisc', 'motiondir']

def main():
    cand, ev, lists = sys.argv[1:4]
    os.makedirs(lists, exist_ok=True)
    batt = []  # (task, split, trial, idx, truth, formF, sha256)
    report = {}
    for task in TASKS:
        rows = []
        with open(os.path.join(ev, 'judgments_cand_%s.tsv' % task)) as f:
            head = f.readline()
            for line in f:
                p = line.rstrip('\n').split('\t')
                rows.append(dict(zip(head.rstrip('\n').split('\t'), p)))
        adv = sorted([r for r in rows if r['kind'] == 'adv'], key=lambda r: int(r['idx']))
        norm = sorted([r for r in rows if r['kind'] == 'norm'], key=lambda r: int(r['idx']))
        fooled = [r for r in adv if r['formF'] != r['truth']]
        report[task] = {'n_adv': len(adv), 'n_fooled': len(fooled), 'n_norm': len(norm)}
        qual = len(fooled) >= 2000 and len(norm) >= 1000
        report[task]['qualifies'] = qual
        if not qual:
            continue
        with open(os.path.join(lists, 'batt_adv_%s.txt' % task), 'w') as f:
            for r in fooled[:2000]:
                fid = r['trial']
                p = '%s/%s/%s.r2fx' % (cand, task, fid)
                f.write('%s %s\n' % (p, fid))
                h = hashlib.sha256(open(p, 'rb').read()).hexdigest()
                batt.append((task, 'adv', fid, r['idx'], r['truth'], r['formF'], h))
        with open(os.path.join(lists, 'batt_ctrl_%s.txt' % task), 'w') as f:
            for r in norm[:1000]:
                fid = r['trial']
                p = '%s/%s/%s.r2fx' % (cand, task, fid)
                f.write('%s %s\n' % (p, fid))
                h = hashlib.sha256(open(p, 'rb').read()).hexdigest()
                batt.append((task, 'ctrl', fid, r['idx'], r['truth'], r['formF'], h))
    with open(os.path.join(ev, 'battery_e4b.tsv'), 'w') as f:
        f.write('task\tsplit\ttrial\tidx\ttruth\tformF\tsha256\n')
        for b in batt:
            f.write('\t'.join(str(x) for x in b) + '\n')
    print(json.dumps(report, indent=1))
    q = [t for t in TASKS if report[t]['qualifies']]
    print('QUALIFYING TASKS: %s' % q, flush=True)
    print('battery rows: %d' % len(batt), flush=True)

if __name__ == '__main__':
    main()
