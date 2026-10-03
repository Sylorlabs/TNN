#!/usr/bin/env python3
"""Arm 4 analysis: transfer verdicts, winner diff-proofs, FP validation."""
import json, subprocess, hashlib, os, sys, tempfile

SI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNS = os.path.join(SI, 'work_a4', 'runs')
ZNC = '/home/hatch/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1'
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


def load(cell, r=1):
    return json.load(open(os.path.join(RUNS, '%s_r%d.json' % (cell, r))))


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
    return {'Qc': '%d/%d' % (passes, len(fixable)), 'Qc_n': passes,
            'hh': '%d/2' % hh, 'iters': iters, 'znc': znc, 'evals': evals,
            'digest': hashlib.sha256(canonical(rep).encode()).hexdigest()}


def diag_events(rep):
    """Ordered (item, n, evtype, class, strategy, score, src_sha, new_src_sha)
    for every diagnose call (result=revised)."""
    evs = []
    for i in rep['items']:
        for rec in i['iters']:
            if rec.get('result') == 'revised':
                evs.append((i['id'], rec['n'], rec['evtype'], rec.get('class'),
                            rec.get('strategy'), rec.get('score'),
                            rec.get('src_sha256'), rec.get('new_src_sha256')))
    return evs


def winner_tuple(e):
    return e[3], e[4], e[5], e[7]  # class, strategy, score, new_src_sha


print('=== metrics (r1; all cells IDENTICAL x3 per transfer_summary) ===')
cells = ['b2_none', 'b4_none', 'b4_a', 'b4_b', 'b4_c', 'b4_combo']
M = {c: metrics(load(c)) for c in cells}
for c in cells:
    print('%-9s' % c, {k: v for k, v in M[c].items() if k != 'digest'})

base = diag_events(load('b4_none'))
print('\n=== winner diff-proof vs knee baseline (b4_none), %d diagnose calls ===' % len(base))
for c in ['b4_a', 'b4_b']:
    evs = diag_events(load(c))
    same_len = len(evs) == len(base)
    mism = [(b, e) for b, e in zip(base, evs)
            if (b[0], b[1], b[2], winner_tuple(b)) != (e[0], e[1], e[2], winner_tuple(e))]
    print('%s: calls=%d seq_equal=%s mismatches=%d' % (c, len(evs), same_len and not mism, len(mism)))
    for b, e in mism[:5]:
        print('   base', b, '\n   var ', e)

# combo: match on (item, n, src_sha) since precheck changes evtype envelopes
bev = {(b[0], b[1], b[6]): b for b in base}
cev = diag_events(load('b4_combo'))
unmatched, mism = [], []
for e in cev:
    key = (e[0], e[1], e[6])
    if key not in bev:
        unmatched.append(e)
    elif winner_tuple(bev[key]) != winner_tuple(e) or bev[key][2] != e[2] and False:
        mism.append((bev[key], e))
    elif winner_tuple(bev[key]) != winner_tuple(e):
        mism.append((bev[key], e))
print('b4_combo: calls=%d matched=%d unmatched=%d winner_mismatches=%d'
      % (len(cev), len(cev) - len(unmatched), len(unmatched), len(mism)))
for b, e in mism[:5]:
    print('   base', b, '\n   combo', e)
for e in unmatched[:5]:
    print('   unmatched combo call', e)
# evtype shift check: every PRECHECK call should sit where baseline had COMPILE
pev = [e for e in cev if e[2] == 'PRECHECK']
pev_base = [bev[(e[0], e[1], e[6])][2] for e in pev if (e[0], e[1], e[6]) in bev]
from collections import Counter
print('   combo PRECHECK calls:', len(pev), 'baseline evtype at same (item,iter,src):', dict(Counter(pev_base)))

# 3c outcome equality per item
bo = {i['id']: i['outcome'] for i in load('b4_none')['items']}
co = {i['id']: i['outcome'] for i in load('b4_c')['items']}
ko = {i['id']: i['outcome'] for i in load('b4_combo')['items']}
print('\n=== outcome equality vs baseline ===')
print('b4_c  :', 'IDENTICAL' if bo == co else 'DIFFER ' + str([k for k in bo if bo[k] != co[k]]))
print('combo :', 'IDENTICAL' if bo == ko else 'DIFFER ' + str([k for k in bo if bo[k] != ko[k]]))

print('\n=== false-positive validation: compile every precheck-FAIL source ===')
for c in ['b4_c', 'b4_combo']:
    fps, total = 0, 0
    for r in (1, 2, 3):
        fp_path = os.path.join(RUNS, '%s_r%d.json.fp_candidates.jsonl' % (c, r))
        seen = set()
        for line in open(fp_path):
            e = json.loads(line)
            key = (e['id'], e['iter'], e['src'])
            if key in seen:
                continue
            seen.add(key)
            total += 1
            with tempfile.NamedTemporaryFile('w', suffix='.zag', delete=False) as f:
                f.write(e['src'])
                zp = f.name
            bp = zp + '.bin'
            pr = subprocess.run([ZNC, zp, '-o', bp, '--no-analyze', '--no-zagd'],
                                capture_output=True, timeout=60)
            os.unlink(zp)
            if os.path.exists(bp):
                os.unlink(bp)
            if pr.returncode == 0:
                fps += 1
                print('   FALSE POSITIVE', e['id'], 'iter', e['iter'])
    print('%s: %d unique precheck-FAIL sources x3 reruns, false positives = %d' % (c, total, fps))

print('\n=== transfer verdicts (bars from prereg §5, new substrate: SI battery @ budget 4) ===')
b = M['b4_none']
for c, mech, bar in [('b4_a', '3a prune', 'evals -20%, winner byte-identical'),
                     ('b4_b', '3b bnb', 'evals -20%, winner byte-identical')]:
    m = M[c]
    de = (m['evals'] - b['evals']) / b['evals'] * 100
    print('%s: Q %s->%s  evals %d->%d (%+.1f%%)  bar [%s]' % (
        mech, b['Qc'], m['Qc'], b['evals'], m['evals'], de, bar))
m = M['b4_c']
dz = (m['znc'] - b['znc']) / b['znc'] * 100
print('3c precheck: Q %s->%s  znc %d->%d (%+.1f%%)  bar [znc -20%%, quality +-1pp, FP=0]' % (
    b['Qc'], m['Qc'], b['znc'], m['znc'], dz))
m = M['b4_combo']
de = (m['evals'] - b['evals']) / b['evals'] * 100
dz = (m['znc'] - b['znc']) / b['znc'] * 100
print('combo: Q %s->%s  evals %d->%d (%+.1f%%)  znc %d->%d (%+.1f%%)' % (
    b['Qc'], m['Qc'], b['evals'], m['evals'], de, b['znc'], m['znc'], dz))
