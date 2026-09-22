#!/usr/bin/env python3
"""Adaptive deliberation trial sweep (epistemic arm), per OPER_SPEC_ADAPTIVE.md.
Policies {2(control),a,b,c,d,e,f} x batteries {frozen94, fresh52} x 3 reps.
Glue only: invocation, parsing, scoring, digests. All reasoning is in Zag.
"""
import subprocess, os, re, json, hashlib, time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
AD = os.path.join(HERE, 'delib_ad')
SI = os.path.join(HERE, '..', 'work_a1', 'delib_si')

FROZEN_FAMS = {
    'joke':           ['W%03d' % i for i in range(1, 11)],
    'sarcasm':        ['W%03d' % i for i in range(23, 33)],
    'hypothetical':   ['W%03d' % i for i in range(45, 55)],
    'analogy':        ['W%03d' % i for i in range(67, 77)],
    'counterfactual': ['W%03d' % i for i in range(109, 119)],
    'poetry':         ['W%03d' % i for i in range(89, 99)],
    'implicature':    ['W%03d' % i for i in range(131, 141)],
}
FRESH_FAMS = {
    'joke':           ['FW%03d' % i for i in range(1, 5)],
    'sarcasm':        ['FW%03d' % i for i in range(5, 9)],
    'hypothetical':   ['FW%03d' % i for i in range(9, 13)],
    'analogy':        ['FW%03d' % i for i in range(13, 17)],
    'counterfactual': ['FW%03d' % i for i in range(17, 21)],
    'poetry':         ['FW%03d' % i for i in range(21, 25)],
    'implicature':    ['FW%03d' % i for i in range(25, 29)],
}

BATTERIES = {
    'frozen94': {'workdir': os.path.join(HERE, '..', 'work_a1', 'epi'),
                 'files': ['b12_false.txt', 'b12_true.txt', 'c70.txt'],
                 'fams': FROZEN_FAMS,
                 'false_pre': ('F',), 'true_pre': ('BC',)},
    'fresh52':  {'workdir': os.path.join(HERE, 'fresh'),
                 'files': ['fresh_false.txt', 'fresh_true.txt', 'fresh_weird.txt'],
                 'fams': FRESH_FAMS,
                 'false_pre': ('FFF',), 'true_pre': ('FTT',)},
}

POLICIES = ['2', 'a', 'b', 'c', 'd', 'e', 'f']

def correct(iid, ver, bat):
    if iid.startswith(bat['false_pre']):
        return ver == 'WITHHOLD'
    if iid.startswith(bat['true_pre']):
        return ver == 'ENDORSE'
    return ver == 'WITHHOLD'

def parse(out, extended):
    items = {}
    for line in out.splitlines():
        if extended:
            m = re.match(r'^(\S+)\|(ENDORSE|WITHHOLD)\|preds=(\d+)\|recon=(\d)\|vflip=(\d)\|rounds=(\d+)$', line)
            if m:
                items[m.group(1)] = {'v': m.group(2), 'p': int(m.group(3)),
                                     'r': int(m.group(4)), 'vf': int(m.group(5)),
                                     'rd': int(m.group(6))}
        else:
            m = re.match(r'^(\S+)\|(ENDORSE|WITHHOLD)\|preds=(\d+)\|recon=(\d)\|vflip=(\d)$', line)
            if m:
                items[m.group(1)] = {'v': m.group(2), 'p': int(m.group(3)),
                                     'r': int(m.group(4)), 'vf': int(m.group(5)),
                                     'rd': 2}  # control: full pipeline = rounds 0+1 by definition
    return items

def run_cell(policy, batname):
    bat = BATTERIES[batname]
    reps = []
    for rep in (1, 2, 3):
        logdir = os.path.join(HERE, 'logs', '%s_%s' % (policy, batname))
        os.makedirs(logdir, exist_ok=True)
        t0 = time.perf_counter()
        combined = []
        for fname in bat['files']:
            if policy == '2':
                cmd = [SI, bat['workdir'], '2', fname]
            else:
                cmd = [AD, bat['workdir'], policy, fname]
            r = subprocess.run(cmd, capture_output=True, text=True)
            assert r.returncode == 0, (policy, batname, fname, r.stderr[:200])
            combined.append(r.stdout)
        wall = time.perf_counter() - t0
        raw = ''.join(combined)
        with open(os.path.join(logdir, 'r%d.log' % rep), 'w') as f:
            f.write(raw)
        dg = hashlib.sha256(raw.encode()).hexdigest()
        reps.append({'digest': dg, 'wall_s': round(wall, 2), 'raw': raw})
    return reps

def score_cell(policy, batname, reps):
    bat = BATTERIES[batname]
    id2fam = {i: k for k, ids in bat['fams'].items() for i in ids}
    out = []
    for rep in reps:
        items = parse(rep['raw'], extended=(policy != '2'))
        n = len(items)
        f_ok = t_ok = 0
        fam = {k: [0, 0] for k in bat['fams']}
        for iid, it in items.items():
            ok = correct(iid, it['v'], bat)
            if iid.startswith(bat['false_pre']):
                f_ok += ok
            elif iid.startswith(bat['true_pre']):
                t_ok += ok
            else:
                k = id2fam.get(iid)
                if k:
                    fam[k][1] += 1
                    fam[k][0] += ok
        total = f_ok + t_ok + sum(v[0] for v in fam.values())
        preds = sum(it['p'] for it in items.values())
        rounds = [it['rd'] for it in items.values()]
        hist = dict(sorted(Counter(rounds).items()))
        maxr = max(rounds)
        maxids = sorted(iid for iid, it in items.items() if it['rd'] == maxr)
        out.append({
            'total': total, 'n': n,
            'false': f_ok, 'true': t_ok,
            'fams': {k: v[0] for k, v in fam.items()},
            'fam_den': {k: v[1] for k, v in fam.items()},
            'mean_preds': round(preds / n, 3),
            'mean_rounds': round(sum(rounds) / n, 3),
            'rounds_hist': hist,
            'max_rounds': maxr,
            'max_round_ids': maxids,
            'recon_items': sum(it['r'] for it in items.values()),
            'vflips': sum(it['vf'] for it in items.values()),
            'digest': rep['digest'],
            'wall_s': rep['wall_s'],
        })
    det = 'IDENTICAL' if len({r['digest'] for r in out}) == 1 else 'DIFFER'
    return {'reps': out, 'determinism': det}

def main():
    os.chdir(HERE)
    results = {}
    for policy in POLICIES:
        for batname in BATTERIES:
            cell = '%s_%s' % (policy, batname)
            print('== cell %s ==' % cell, flush=True)
            reps = run_cell(policy, batname)
            results[cell] = score_cell(policy, batname, reps)
            r0 = results[cell]['reps'][0]
            print('  total=%d/%d false=%d true=%d mean_preds=%.3f mean_rounds=%.3f '
                  'hist=%s maxr=%d vflips=%d det=%s' % (
                      r0['total'], r0['n'], r0['false'], r0['true'],
                      r0['mean_preds'], r0['mean_rounds'], r0['rounds_hist'],
                      r0['max_rounds'], r0['vflips'], results[cell]['determinism']),
                  flush=True)
    json.dump(results, open('results_adaptive.json', 'w'), indent=1, sort_keys=True)
    print('wrote results_adaptive.json')

if __name__ == '__main__':
    main()
