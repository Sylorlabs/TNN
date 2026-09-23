#!/usr/bin/env python3
"""Metrics + determinism digests for the promotion runs. Usage:
   python3 metrics.py <run.json> [<run2.json> ...]"""
import json, sys, hashlib

TEST_EVALS = {  # old-binary TEST-branch evals, keyed by trace reason
    'stderr-nonempty': 1, 'rc-mismatch-no-stderr': 2,
    'equal-modulo-trailing-ws': 3, 'integer-outputs-differ': 4,
    'non-integer-difference': 5}

def canonical(obj):
    def strip(o):
        if isinstance(o, dict):
            return {k: strip(v) for k, v in sorted(o.items())
                    if k not in ('ms', 'time_s', 'compile_ms', 'test_ms', 'diag_ms')}
        if isinstance(o, list):
            return [strip(v) for v in o]
        return o
    return json.dumps(strip(obj), sort_keys=True, separators=(',', ':'))

def ev_of(rec):
    e = rec.get('evals', '?')
    if isinstance(e, int):
        return e
    if isinstance(e, str) and e.isdigit():
        return int(e)
    # old binary (no evals=): reconstruct deterministically
    if rec.get('evtype') == 'COMPILE':
        return 5
    if rec.get('evtype') == 'GEN':
        return 1
    if rec.get('evtype') == 'TEST':
        tr = rec.get('trace', '')
        for k, v in TEST_EVALS.items():
            if k in tr:
                return v
    return 0

def metrics(path):
    rep = json.load(open(path))
    items = rep['items']
    n_pass = sum(1 for i in items if i['outcome'] == 'pass')
    halts = [i['outcome'] for i in items if i['outcome'].startswith('halt-')]
    iters = sum(i['iters_used'] for i in items)
    znc = sum(1 for i in items for r in i['iters']
              if r.get('evtype') in ('COMPILE', 'TEST', 'PRECHECK', 'NONE')
              or ('znc' in r and r['znc'] == 1))
    # znc field present in new driver; for old driver infer: every non-GEN iter invoked znc
    znc = sum(1 for i in items for r in i['iters']
              if r.get('znc', 1 if r.get('evtype') in ('COMPILE', 'TEST', 'NONE') else 0) == 1)
    hyp = sum(ev_of(r) for i in items for r in i['iters'] if r.get('result') == 'revised')
    wall = sum(i.get('time_s', 0) for i in items)
    digest = hashlib.sha256(canonical(rep).encode()).hexdigest()
    return {'file': path, 'budget': rep.get('budget'), 'pass': '%d/%d' % (n_pass, len(items)),
            'halts': '%d (%s)' % (len(halts), ','.join(sorted(set(halts)))),
            'iters': iters, 'znc': znc, 'hyp_evals': hyp,
            'wall_s': round(wall, 1), 'digest': digest}

if __name__ == '__main__':
    rows = [metrics(p) for p in sys.argv[1:]]
    for r in rows:
        print('%-28s budget=%s pass=%-7s halts=%-28s iters=%-3d znc=%-3d hyp=%-4d wall=%6.1fs digest=%s'
              % (r['file'].split('/')[-1], r['budget'], r['pass'], r['halts'],
                 r['iters'], r['znc'], r['hyp_evals'], r['wall_s'], r['digest'][:16]))
    ds = set(r['digest'] for r in rows)
    print('byte-identical reruns:', 'YES' if len(ds) == 1 else 'NO (%d distinct)' % len(ds))
