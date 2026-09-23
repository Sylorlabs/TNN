#!/usr/bin/env python3
"""PL-1 scorer: runs the three arms on batteries, scores verdicts.
Usage: score_pl.py <outdir> ; expects batteries/work/{frozen94,a1r94,b188,fresh94,novel94}.txt
Reads arm binaries from the script's dir.
"""
import json, os, subprocess, sys, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, 'batteries', 'work')
LESSONS = os.path.join(HERE, 'lessons')
ARMS = {
    'a_plearn': [os.path.join(HERE, 'delib_plearn'), '{work}', '2', '{bat}', LESSONS],
    'b_hinject': [os.path.join(HERE, 'delib_hinject'), '{work}', '2', '{bat}'],
    'c_base': [os.path.join(HERE, 'delib_base'), '{work}', '2', '{bat}'],
}

def correct_of(iid):
    if iid.startswith('F'): return 'WITHHOLD'
    if iid.startswith('BC') or iid.startswith('B'): return 'ENDORSE'
    return 'WITHHOLD'  # W

def run_arm(arm, batfile, rep):
    cmd = [c.format(work=WORK, bat=batfile) for c in ARMS[arm]]
    r = subprocess.run(cmd, capture_output=True, text=True)
    assert r.returncode == 0, (arm, batfile, r.stderr[:300])
    verdicts = {}
    learn_lines = []
    for line in r.stdout.split('\n'):
        if line.startswith('LEARN|'):
            learn_lines.append(line)
        elif '|' in line and (line.startswith('W') or line.startswith('F') or line.startswith('BC') or line.startswith('B')):
            parts = line.split('|')
            verdicts[parts[0]] = parts[1]
    return verdicts, learn_lines, hashlib.sha256(r.stdout.encode()).hexdigest()

def score(verdicts):
    tot = {'n': 0, 'ok': 0}
    slices = {}
    wrong_install = 0   # should-WITHHOLD -> ENDORSE
    bc_withheld = 0     # BC -> WITHHOLD
    for iid, v in verdicts.items():
        c = correct_of(iid)
        sl = 'W' if iid.startswith('W') else ('F' if iid.startswith('F') else 'BC')
        s = slices.setdefault(sl, {'n': 0, 'ok': 0})
        s['n'] += 1; tot['n'] += 1
        if v == c:
            s['ok'] += 1; tot['ok'] += 1
        else:
            if c == 'WITHHOLD': wrong_install += 1
            if sl == 'BC': bc_withheld += 1
    return tot, slices, wrong_install, bc_withheld

def main():
    outdir = sys.argv[1]
    os.makedirs(outdir, exist_ok=True)
    bats = ['frozen94', 'a1r94', 'b188', 'fresh94', 'novel94']
    report = {}
    for bat in bats:
        bf = bat + '.txt'
        if not os.path.exists(os.path.join(WORK, bf)):
            print('skip', bat, '(no battery file)'); continue
        report[bat] = {}
        for arm in ARMS:
            reps = [run_arm(arm, bf, i) for i in range(3)]
            det = len(set(h for _, _, h in reps)) == 1
            v = reps[0][0]
            tot, slices, wi, bcw = score(v)
            report[bat][arm] = {
                'acc': round(100.0 * tot['ok'] / tot['n'], 2),
                'n': tot['n'], 'ok': tot['ok'],
                'slices': {k: {'acc': round(100.0 * x['ok'] / x['n'], 2), 'ok': x['ok'], 'n': x['n']} for k, x in slices.items()},
                'wrong_install': wi, 'bc_withheld': bcw,
                'deterministic_3x': det,
                'learn': reps[0][1],
            }
            print('%s %s: acc=%.1f%% W=%s F=%s BC=%s wi=%d bcw=%d det=%s' % (
                bat, arm, report[bat][arm]['acc'],
                report[bat][arm]['slices'].get('W'), report[bat][arm]['slices'].get('F'),
                report[bat][arm]['slices'].get('BC'), wi, bcw, det))
    json.dump(report, open(os.path.join(outdir, 'scores.json'), 'w'), indent=1)
    print('wrote', os.path.join(outdir, 'scores.json'))

main()
