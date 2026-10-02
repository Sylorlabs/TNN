#!/usr/bin/env python3
"""Measurement harness for the fast-loop: the lead's speed-vs-quality question.

Runs:
  1. Budget sweep: the full battery at iteration budgets {1,3,6,12}.
     Does more budget help (converge) or just burn time (thrash)?
  2. Determinism: 3 full runs at budget 6; canonical digests must match.

Metrics (all from driver JSON reports):
  - iterations/hour      = total loop iterations / total wall hours
  - time to first working build = per-item wall time until first pass (median)
  - defect rate/iteration  = iterations ending in failure / total iterations
  - first-attempt pass rate = items passing on iteration 1 / all items
  - convergence table    = iters-used per item per budget; flat => converge,
                           growing-with-budget => thrash

Writes RESULTS.md with the numbers and the honest answer.
"""
import json, os, subprocess, sys, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
BUDGETS = [1, 3, 6, 12]


def canon_digest(report):
    sys.path.insert(0, HERE)
    import driver as D
    return D.sha(D.canonical(report).encode())


def run_budget(budget, tag):
    workdir = os.path.join(HERE, 'work', 'sweep', 'b%d' % budget, tag)
    out = os.path.join(HERE, 'work', 'sweep', 'b%d_%s.json' % (budget, tag))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    subprocess.run([sys.executable, os.path.join(HERE, 'driver.py'),
                    os.path.join(HERE, 'battery.json'),
                    '--budget', str(budget), '--workdir', workdir, '--out', out],
                   check=True, capture_output=True, text=True)
    with open(out) as f:
        return json.load(f)


def metrics(report):
    items = report['items']
    n = len(items)
    passed = [i for i in items if i['outcome'] == 'pass']
    total_iters = sum(i['iters_used'] for i in items)
    total_time = sum(i['time_s'] for i in items)
    # an iteration "ends in failure" unless it is the passing iteration
    defect_iters = sum(1 for i in items for it in i['iters']
                       if not (it.get('result') == 'pass'))
    first_try = sum(1 for i in items if i['outcome'] == 'pass' and i['iters_used'] == 1)
    ttfb = sorted(i['time_s'] for i in passed)
    median_ttfb = ttfb[len(ttfb) // 2] if ttfb else None
    return {
        'n': n, 'passed': len(passed),
        'pass_rate': round(len(passed) / n, 4),
        'total_iters': total_iters,
        'iter_per_hour': round(total_iters / total_time * 3600, 1) if total_time else 0,
        'median_ttfb_s': median_ttfb,
        'defect_rate': round(defect_iters / total_iters, 4) if total_iters else 0,
        'first_try_rate': round(first_try / n, 4),
        'halts': {i['id']: i['outcome'] for i in items if i['outcome'].startswith('halt')},
    }


def main():
    os.makedirs(os.path.join(HERE, 'work', 'sweep'), exist_ok=True)
    sweep = {}
    print("=== budget sweep ===", flush=True)
    for b in BUDGETS:
        rep = run_budget(b, 'sweep')
        sweep[b] = rep
        m = metrics(rep)
        print("budget=%2d pass=%2d/%d iters=%3d iter/h=%7.1f defect=%5.1f%% first-try=%5.1f%% halts=%d" % (
            b, m['passed'], m['n'], m['total_iters'], m['iter_per_hour'],
            m['defect_rate'] * 100, m['first_try_rate'] * 100, len(m['halts'])), flush=True)

    print("=== determinism: 3x budget 6 ===", flush=True)
    digests = []
    for k in (1, 2, 3):
        rep = run_budget(6, 'det%d' % k)
        d = canon_digest(rep)
        digests.append(d)
        print("run %d digest %s" % (k, d), flush=True)
    det_ok = len(set(digests)) == 1
    print("determinism:", "IDENTICAL" if det_ok else "MISMATCH", flush=True)

    # convergence table: iters_used per item per budget
    ids = [i['id'] for i in sweep[6]['items']]
    conv = {}
    for iid in ids:
        conv[iid] = {str(b): next(i for i in sweep[b]['items'] if i['id'] == iid)['iters_used']
                     for b in BUDGETS}
        conv[iid]['outcome_b12'] = next(i for i in sweep[12]['items'] if i['id'] == iid)['outcome']

    with open(os.path.join(HERE, 'work', 'sweep_summary.json'), 'w') as f:
        json.dump({'metrics': {str(b): metrics(sweep[b]) for b in BUDGETS},
                   'convergence': conv, 'determinism': {'digests': digests, 'identical': det_ok}},
                  f, indent=1, sort_keys=True)
    print("wrote work/sweep_summary.json", flush=True)


if __name__ == '__main__':
    main()
