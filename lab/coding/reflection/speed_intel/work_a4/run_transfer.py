#!/usr/bin/env python3
"""Arm 4 transfer check + baseline cells.

Cells (3 reruns each, canonical digests must be byte-identical):
  b2_none : budget 2, mech none   (1x baseline)      via driver_si.py
  b4_none : budget 4, mech none   (knee baseline)    via driver_si.py
  b4_a    : budget 4, mech a      (3a transfer)      via driver_si.py
  b4_b    : budget 4, mech b      (3b transfer)      via driver_si.py
  b4_c    : budget 4, mech c      (3c transfer)      via driver_si.py
  b4_combo: budget 4, mech combo  (integrated)       via driver_si4.py

Battery: work_a1/battery_si.json (frozen SI battery), 69-entry KB patterns
per item (knowledge-first, as in Arm 1).
"""
import json, subprocess, hashlib, os, sys

SI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BATTERY = os.path.join(SI, 'work_a1', 'battery_si.json')
RUNS = os.path.join(SI, 'work_a4', 'runs')

CELLS = [
    ('b2_none', 2, 'none', 'driver_si.py'),
    ('b4_none', 4, 'none', 'driver_si.py'),
    ('b4_a', 4, 'a', 'driver_si.py'),
    ('b4_b', 4, 'b', 'driver_si.py'),
    ('b4_c', 4, 'c', 'driver_si.py'),
    ('b4_combo', 4, 'combo', 'driver_si4.py'),
]
HALT_OK = {'halt-genfail', 'halt-no-patch', 'halt-unknown', 'halt-runtime',
           'halt-noregen', 'halt-thrash', 'halt-cycle'}


def canonical(obj):
    def strip(o):
        if isinstance(o, dict):
            return {k: strip(v) for k, v in sorted(o.items())
                    if k not in ('ms', 'time_s', 'compile_ms', 'test_ms', 'diag_ms')}
        if isinstance(o, list):
            return [strip(v) for v in o]
        return o
    return json.dumps(strip(obj), sort_keys=True, separators=(',', ':'))


def run_cell(cell, budget, mech, driver):
    procs = []
    for r in (1, 2, 3):
        wd = os.path.join(RUNS, '%s_r%d' % (cell, r), 'work')
        out = os.path.join(RUNS, '%s_r%d.json' % (cell, r))
        os.makedirs(wd, exist_ok=True)
        log = os.path.join(RUNS, '%s_r%d.log' % (cell, r))
        # driver_si.py lives at SI/; driver_si4.py lives at SI/work_a4/
        drvdir = SI if driver == 'driver_si.py' else os.path.join(SI, 'work_a4')
        cmd = [sys.executable, os.path.join(drvdir, driver), BATTERY,
               '--budget', str(budget), '--mech', mech,
               '--workdir', wd, '--out', out]
        lf = open(log, 'w')
        procs.append((cell, r, out, lf,
                      subprocess.Popen(cmd, cwd=drvdir, stdout=lf, stderr=subprocess.STDOUT)))
    for cell, r, out, lf, p in procs:
        rc = p.wait()
        lf.close()
        if rc != 0:
            print('FAILED %s r%d (see log)' % (cell, r), flush=True)
            sys.exit(1)
        print('done %s r%d' % (cell, r), flush=True)


def metrics(rep):
    items = rep['items']
    fixable = [i for i in items if not i['id'].startswith('X')]
    unfix = [i for i in items if i['id'].startswith('X')]
    passes = sum(1 for i in fixable if i['outcome'] == 'pass')
    hh = sum(1 for i in unfix if i['outcome'] in HALT_OK)
    iters = sum(i['iters_used'] for i in items)
    znc = rep['stats']['znc_invocations']
    evals = 0
    for i in items:
        for rec in i['iters']:
            e = rec.get('evals', '?')
            if isinstance(e, str) and e.isdigit():
                evals += int(e)
            elif isinstance(e, int):
                evals += e
    return {'Qc': '%d/%d' % (passes, len(fixable)),
            'Qc_n': passes, 'Qc_d': len(fixable),
            'honest_halt': '%d/2' % hh, 'hh_n': hh,
            'iters': iters, 'znc': znc, 'evals': evals,
            'digest': hashlib.sha256(canonical(rep).encode()).hexdigest()}


def main():
    os.makedirs(RUNS, exist_ok=True)
    summary = {}
    for cell, budget, mech, driver in CELLS:
        print('== cell %s (budget %d, mech %s) ==' % (cell, budget, mech), flush=True)
        run_cell(cell, budget, mech, driver)
        ms = []
        for r in (1, 2, 3):
            rep = json.load(open(os.path.join(RUNS, '%s_r%d.json' % (cell, r))))
            ms.append(metrics(rep))
        det = 'IDENTICAL' if len({m['digest'] for m in ms}) == 1 else 'DIFFER'
        s = dict(ms[0])
        s['determinism'] = det
        summary[cell] = s
        print(cell, {k: v for k, v in s.items() if k != 'digest'}, flush=True)
    json.dump(summary, open(os.path.join(SI, 'work_a4', 'transfer_summary.json'), 'w'),
              indent=1, sort_keys=True)
    print('wrote transfer_summary.json')


if __name__ == '__main__':
    main()
