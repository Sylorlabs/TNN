#!/usr/bin/env python3
"""PL-2 scorer: four arms x three batteries x three deterministic reruns.

Arms:
  a1_v1lessons : delib_plearn binary + v1 narrow lessons (same engine as a2)
  a2_v2lessons : delib_plearn binary + v2 broad lessons
  b_hinject    : frozen hand-trigger baseline (v1 binary)
  c_base       : frozen no-knowledge baseline (v1 binary)

Batteries (batteries/work/): frozen94.txt, fresh2_94.txt, novel2_94.txt
Family map for fresh2/novel2 W ids: Wx01-Wx10=P1 ... Wx61-Wx70=P7.
"""
import json, os, subprocess, sys, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, 'batteries', 'work')
V1 = os.path.join(HERE, '..', 'principles_learned')
PLEARN = os.path.join(HERE, 'work', 'build', 'delib_plearn')
ARMS = {
    'a1_v1lessons': [PLEARN, '{work}', '2', '{bat}',
                     os.path.join(V1, 'lessons')],
    'a2_v2lessons': [PLEARN, '{work}', '2', '{bat}',
                     os.path.join(HERE, 'lessons')],
    'b_hinject': [os.path.join(V1, 'delib_hinject'), '{work}', '2', '{bat}'],
    'c_base': [os.path.join(V1, 'delib_base'), '{work}', '2', '{bat}'],
}
FAMS = ['sarcasm', 'analogy', 'joke', 'hypothetical', 'poetry',
        'implicature', 'counterfactual']

def correct_of(iid):
    if iid.startswith('F'): return 'WITHHOLD'
    if iid.startswith('BC') or iid.startswith('B'): return 'ENDORSE'
    return 'WITHHOLD'

def family_of(iid):
    # fresh2 W701-W770, novel2 W801-W870: tens encode family
    if iid.startswith('W') and len(iid) == 4 and iid[1:].isdigit():
        n = int(iid[1:])
        if 701 <= n <= 770 or 801 <= n <= 870:
            return FAMS[((n % 100) - 1) // 10]
    return None

def run_arm(arm, batfile):
    cmd = [c.format(work=WORK, bat=batfile) for c in ARMS[arm]]
    r = subprocess.run(cmd, capture_output=True, text=True)
    assert r.returncode == 0, (arm, batfile, r.stderr[:300])
    verdicts, learn = {}, []
    for line in r.stdout.split('\n'):
        if line.startswith('LEARN|'):
            learn.append(line)
        elif '|' in line and (line.startswith('W') or line.startswith('F')
                              or line.startswith('BC') or line.startswith('B')):
            p = line.split('|')
            verdicts[p[0]] = p[1]
    return verdicts, learn, hashlib.sha256(r.stdout.encode()).hexdigest()

def score(verdicts):
    tot = {'n': 0, 'ok': 0}
    slices, fams = {}, {}
    wi = bcw = 0
    for iid, v in verdicts.items():
        c = correct_of(iid)
        sl = 'W' if iid.startswith('W') else ('F' if iid.startswith('F') else 'BC')
        s = slices.setdefault(sl, {'n': 0, 'ok': 0})
        s['n'] += 1; tot['n'] += 1
        fam = family_of(iid)
        if fam and sl == 'W':
            fs = fams.setdefault(fam, {'n': 0, 'ok': 0})
            fs['n'] += 1
            if v == c: fs['ok'] += 1
        if v == c:
            s['ok'] += 1; tot['ok'] += 1
        else:
            if c == 'WITHHOLD': wi += 1
            if sl == 'BC': bcw += 1
    return tot, slices, fams, wi, bcw

def main():
    outdir = sys.argv[1]
    os.makedirs(outdir, exist_ok=True)
    bats = ['frozen94', 'fresh2_94', 'novel2_94']
    report = {}
    for bat in bats:
        bf = bat + '.txt'
        if not os.path.exists(os.path.join(WORK, bf)):
            print('skip', bat, '(no battery file)'); continue
        report[bat] = {}
        for arm in ARMS:
            reps = [run_arm(arm, bf) for _ in range(3)]
            det = len(set(h for _, _, h in reps)) == 1
            v = reps[0][0]
            tot, slices, fams, wi, bcw = score(v)
            report[bat][arm] = {
                'acc': round(100.0 * tot['ok'] / tot['n'], 2),
                'n': tot['n'], 'ok': tot['ok'],
                'slices': {k: {'acc': round(100.0 * x['ok'] / x['n'], 2),
                               'ok': x['ok'], 'n': x['n']}
                           for k, x in slices.items()},
                'families': {k: {'acc': round(100.0 * x['ok'] / x['n'], 2),
                                 'ok': x['ok'], 'n': x['n']}
                             for k, x in fams.items()},
                'wrong_install': wi, 'bc_withheld': bcw,
                'deterministic_3x': det,
                'learn': reps[0][1],
            }
            w = report[bat][arm]['slices'].get('W', {})
            print('%s %s: acc=%.1f%% W=%d/%d F=%s BC=%s wi=%d bcw=%d det=%s' % (
                bat, arm, report[bat][arm]['acc'], w.get('ok', 0),
                w.get('n', 0),
                report[bat][arm]['slices'].get('F'),
                report[bat][arm]['slices'].get('BC'), wi, bcw, det))
    json.dump(report, open(os.path.join(outdir, 'scores.json'), 'w'), indent=1)
    print('wrote', os.path.join(outdir, 'scores.json'))

main()
