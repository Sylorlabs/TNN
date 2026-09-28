#!/usr/bin/env python3
"""SI Arm 3 analysis: metrics per run, winner diffs, determinism digests.

Usage:
  python3 analyze.py <run.json>                  -> metrics table row
  python3 analyze.py --diff <base.json> <var.json> -> per-diagnose winner diff
  python3 analyze.py --digest <run.json>           -> canonical digest
"""
import json, sys, hashlib


def canonical(obj):
    def strip(o):
        if isinstance(o, dict):
            return {k: strip(v) for k, v in sorted(o.items())
                    if k not in ('ms', 'time_s', 'compile_ms', 'test_ms', 'diag_ms')}
        if isinstance(o, list):
            return [strip(v) for v in o]
        return o
    return json.dumps(strip(obj), sort_keys=True, separators=(',', ':'))


def rule_evals(rec):
    """Hypothesis-evaluations for runs without the learner-reported evals field
    (original driver): COMPILE always scores all 5 classes; TEST fires at a
    cascade position read from the trace; GEN is a single direct decision."""
    et = rec.get('evtype')
    if et == 'COMPILE':
        return 5
    if et == 'GEN':
        return 1
    if et == 'TEST':
        tr = rec.get('trace', '')
        if 'stderr-nonempty' in tr:
            return 1
        if 'rc-mismatch-no-stderr' in tr:
            return 2
        if 'equal-modulo-trailing-ws' in tr:
            return 3
        if 'integer-outputs-differ' in tr:
            return 4
        return 5  # LOTHER: all checks exhausted
    return 0  # evtype NONE (pass): no deliberation


def evals_of(rec):
    e = rec.get('evals', '?')
    if e == '?' or e is None:
        return rule_evals(rec)
    return int(e)


def znc_of(rec):
    z = rec.get('znc')
    if z is not None:
        return int(z)
    # original driver: znc ran on every iteration except GEN-evtype
    return 0 if rec.get('evtype') == 'GEN' else 1


def metrics(path):
    r = json.load(open(path))
    items = r['items']
    n = len(items)
    passes = sum(1 for i in items if i['outcome'] == 'pass')
    iters = sum(i['iters_used'] for i in items)
    znc = 0
    evals = 0
    diags = 0
    for i in items:
        for rec in i['iters']:
            znc += znc_of(rec)
            if 'class' in rec:
                diags += 1
                evals += evals_of(rec)
    return {'file': path, 'n': n, 'pass': passes, 'pass_rate': passes / n,
            'iters': iters, 'znc': znc, 'evals': evals, 'diags': diags,
            'precheck': r.get('stats', {}).get('precheck_fail', 0)}


def winner_key(rec):
    return (rec.get('class'), rec.get('strategy'), rec.get('score'),
            rec.get('new_src_sha256'))


def diff_winners(base_path, var_path):
    b = json.load(open(base_path))
    v = json.load(open(var_path))
    bmap = {}
    for i in b['items']:
        for rec in i['iters']:
            if 'class' in rec:
                bmap[(i['id'], rec['n'])] = (rec.get('evtype'), winner_key(rec), rec.get('trace', ''))
    mism = []
    total = 0
    for i in v['items']:
        for rec in i['iters']:
            if 'class' in rec:
                total += 1
                k = (i['id'], rec['n'])
                if k not in bmap:
                    mism.append((k, 'missing-in-baseline', None))
                    continue
                bet, bkey, btr = bmap[k]
                vkey = winner_key(rec)
                if bkey != vkey:
                    mism.append((k, 'WINNER-MISMATCH base=%s(%s) var=%s(%s)' %
                                 (bkey, bet, vkey, rec.get('evtype')), None))
    return total, mism


def main():
    a = sys.argv[1:]
    if a[0] == '--digest':
        r = json.load(open(a[1]))
        print(hashlib.sha256(canonical(r).encode()).hexdigest())
    elif a[0] == '--diff':
        total, mism = diff_winners(a[1], a[2])
        print('diagnose calls compared: %d, winner mismatches: %d' % (total, len(mism)))
        for k, msg, _ in mism:
            print(' ', k, msg)
    else:
        m = metrics(a[0])
        print('file=%(file)s n=%(n)d pass=%(pass)d/%(n)d (%(pass_pct).1f%%) '
              'iters=%(iters)d znc=%(znc)d evals=%(evals)d diags=%(diags)d '
              'precheck_fail=%(precheck)d' % dict(m, pass_pct=100 * m['pass_rate']))


if __name__ == '__main__':
    main()
