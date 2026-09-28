#!/usr/bin/env python3
"""Arm 1 coding sweep: budgets 2/4/8/16 x 3 reruns on battery_si.json.
Writes per-cell run JSON + a digests file with canonical sha256 digests.
"""
import json, subprocess, hashlib, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))

def canonical(obj):
    def strip(o):
        if isinstance(o, dict):
            return {k: strip(v) for k, v in sorted(o.items())
                    if k not in ('ms', 'time_s', 'compile_ms', 'test_ms', 'diag_ms')}
        if isinstance(o, list):
            return [strip(v) for v in o]
        return o
    return json.dumps(strip(obj), sort_keys=True, separators=(',', ':'))

def main():
    os.chdir(HERE)
    cells = []
    for budget in (2, 4, 8, 16):
        for rep in (1, 2, 3):
            cells.append((budget, rep))
    summary = {}
    for budget, rep in cells:
        cell = 'b%d_r%d' % (budget, rep)
        wd = os.path.join('sweep_si', cell, 'run')
        out = os.path.join('sweep_si', cell, 'run.json')
        os.makedirs(wd, exist_ok=True)
        print('== cell %s ==' % cell, flush=True)
        r = subprocess.run([sys.executable, 'driver_si.py', 'battery_si.json',
                            '--budget', str(budget), '--workdir', wd, '--out', out])
        if r.returncode != 0:
            print('FAILED cell %s' % cell); sys.exit(1)
        rep_data = json.load(open(out))
        dg = hashlib.sha256(canonical(rep_data).encode()).hexdigest()
        # metrics
        items = rep_data['items']
        fixable = [i for i in items if not i['id'].startswith('X')]
        unfix = [i for i in items if i['id'].startswith('X')]
        passes = sum(1 for i in fixable if i['outcome'] == 'pass')
        first_try = sum(1 for i in fixable if i['outcome'] == 'pass' and i['iters_used'] == 1)
        hh = sum(1 for i in unfix if i['outcome'] in ('halt-genfail','halt-no-patch','halt-unknown','halt-runtime','halt-noregen'))
        iters = sum(i['iters_used'] for i in items)
        znc = 0
        for i in items:
            for rec in i['iters']:
                if rec.get('evtype') in ('COMPILE','TEST'):
                    znc += 1
        summary[cell] = {'digest': dg, 'budget': budget,
                         'Qc': '%d/%d' % (passes, len(fixable)),
                         'first_try': '%d/%d' % (first_try, len(fixable)),
                         'honest_halt': '%d/2' % hh,
                         'iters': iters, 'znc_invocations': znc,
                         'wall_s': round(sum(i.get('time_s',0) for i in items),1)}
        print(cell, summary[cell], flush=True)
    json.dump(summary, open('sweep_si/summary.json','w'), indent=1, sort_keys=True)
    # determinism check: 3 reruns per budget byte-identical canonical?
    for budget in (2,4,8,16):
        ds = [summary['b%d_r%d'%(budget,r)]['digest'] for r in (1,2,3)]
        print('budget %d determinism: %s' % (budget, 'IDENTICAL' if len(set(ds))==1 else 'DIFFER '+str(ds)))

if __name__ == '__main__':
    main()
