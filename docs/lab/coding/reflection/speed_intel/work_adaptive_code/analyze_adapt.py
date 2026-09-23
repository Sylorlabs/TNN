#!/usr/bin/env python3
"""Analyze adaptive-deliberation sweep cells. See OPER_SPEC_ADAPTIVE.md §8."""
import json, sys, os, hashlib
from collections import Counter

ADAPT = os.path.dirname(os.path.abspath(__file__))
SWEEP = os.path.join(ADAPT, 'sweep_adapt')

FROZEN_X = {'X3-unprovable', 'X4-undefloop'}
FRESH_X = {'X5-undefaccum'}


def canonical(obj):
    def strip(o):
        if isinstance(o, dict):
            return {k: strip(v) for k, v in sorted(o.items())
                    if k not in ('ms', 'time_s', 'compile_ms', 'test_ms', 'diag_ms')}
        if isinstance(o, list):
            return [strip(v) for v in o]
        return o
    return json.dumps(strip(obj), sort_keys=True, separators=(',', ':'))


def load(cell):
    p = os.path.join(SWEEP, cell, 'run.json')
    with open(p) as f:
        return json.load(f)


def analyze(cell, battery_kind):
    r = load(cell)
    items = r['items']
    x_ids = FROZEN_X if battery_kind == 'frozen' else FRESH_X
    fixable = [it for it in items if it['id'] not in x_ids]
    xitems = [it for it in items if it['id'] in x_ids]
    q = sum(1 for it in fixable if it['outcome'] == 'pass')
    hh = sum(1 for it in xitems if (it['outcome'] or '').startswith('halt-'))
    iters = [it['iters_used'] for it in items]
    mean_it = sum(iters) / len(iters)
    hist = dict(sorted(Counter(iters).items()))
    max_it = max(iters)
    max_ids = [it['id'] for it in items if it['iters_used'] == max_it]
    znc = sum(1 for it in items for rd in it['iters']
              if rd.get('evtype') in ('COMPILE', 'TEST'))
    wall = sum(it.get('time_s', 0) for it in items)
    digest = hashlib.sha256(canonical(r).encode()).hexdigest()
    # adaptive-specific
    req_grant = [(it['id'], it.get('requested'), it.get('granted')) for it in items]
    verify_multi = sum(1 for it in items for rd in it['iters']
                       if rd.get('strategy') == 'verify-multi')
    verify_ext = sum(rd.get('trace', '').count('VERIFY-EXTEND')
                     for it in items for rd in it['iters'])
    hopeless = sum(1 for it in items for rd in it['iters']
                   if rd.get('strategy') == 'halt-hopeless')
    ceil_n = sum(1 for it in items if it['iters_used'] == max_it)
    return {
        'cell': cell, 'n': len(items), 'q': q, 'q_denom': len(fixable),
        'honest_halt': hh, 'hh_denom': len(xitems),
        'mean_iters': round(mean_it, 3), 'total_iters': sum(iters),
        'hist': hist, 'max_iters': max_it, 'max_ids': max_ids,
        'ceil_count': ceil_n, 'ceil_frac': round(ceil_n / len(items), 3),
        'znc': znc, 'wall_s': round(wall, 1), 'digest': digest,
        'req_grant': req_grant, 'verify_multi': verify_multi,
        'verify_ext': verify_ext, 'halt_hopeless': hopeless,
    }


def main():
    cells = [c for c in sys.argv[1:] if not c.startswith('--')]
    rows = []
    for cell in cells:
        kind = 'frozen' if 'frozen' in cell else 'fresh'
        rows.append(analyze(cell, kind))
    print(json.dumps(rows, indent=1))
    if '--json-only' in sys.argv:
        return
    # summary table
    print("\n%-22s %8s %8s %10s %8s %6s %s" %
          ('cell', 'Q', 'halt', 'mean_it', 'znc', 'max', 'hist'))
    for a in rows:
        print("%-22s %4d/%-3d %4d/%-3d %10.3f %8d %6d %s" % (
            a['cell'], a['q'], a['q_denom'], a['honest_halt'], a['hh_denom'],
            a['mean_iters'], a['znc'], a['max_iters'], a['hist']))


if __name__ == '__main__':
    main()
