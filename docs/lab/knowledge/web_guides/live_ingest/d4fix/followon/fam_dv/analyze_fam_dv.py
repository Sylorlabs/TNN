#!/usr/bin/env python3
"""FAM-DV analyzer: checks G1-G6 + FAM-DV family bars from run artifacts.

Usage: python3 analyze_fam_dv.py <rundir>
  rundir contains control/pass1, control/pass2, fam_dv/pass1, fam_dv/pass2.
Prints PASS/FAIL per bar with evidence. Exit 0 iff all pass.
"""
import os, sys, re

def load_ledger(path):
    rows = []
    if os.path.exists(path):
        with open(path) as f:
            for line in f:
                line = line.rstrip('\n')
                if line:
                    rows.append(line.split('|'))
    return rows

def main():
    rundir = sys.argv[1]
    fails = []
    notes = []
    def check(name, cond, detail=''):
        notes.append('%s|%s|%s' % ('PASS' if cond else 'FAIL', name, detail))
        if not cond:
            fails.append(name)

    arms = {}
    for arm in ('control', 'fam_dv'):
        p1 = os.path.join(rundir, arm, 'pass1')
        k = load_ledger(os.path.join(p1, 'knowledge_ledger.txt'))
        u = load_ledger(os.path.join(p1, 'undetermined_ledger.txt'))
        r = load_ledger(os.path.join(p1, 'refusal_ledger.txt'))
        installs = {}   # cid -> claim sentence
        for row in k:
            if row[0] == 'K' and len(row) >= 4:
                installs[row[2]] = row[3]
        ures = {}       # cid -> reason
        for row in u:
            if row[0] == 'U' and len(row) >= 6:
                ures[row[2]] = row[3]
        arms[arm] = dict(installs=installs, ures=ures)

    fam = arms['fam_dv']
    ctl = arms['control']

    # ---- FAM-DV family bars ----
    dv_installs = [c for c in ('dv-1', 'dv-2', 'dv-3', 'dv-4') if c in fam['installs']]
    check('DV-0install', len(dv_installs) == 0, 'dv installs=%s' % dv_installs)
    check('DV-dv2-PRED', fam['ures'].get('dv-2') == 'PRED',
          'dv-2 reason=%s' % fam['ures'].get('dv-2'))
    for c in ('dv-1', 'dv-3', 'dv-4'):
        check('DV-%s-withhold' % c, c not in fam['installs'], 'reason=%s' % fam['ures'].get(c))
    check('DV-bl-a5-withhold', 'bl-a5' not in fam['installs'],
          'reason=%s' % fam['ures'].get('bl-a5'))
    check('DV-w1-PRED', fam['ures'].get('w1') == 'PRED',
          'w1 reason=%s' % fam['ures'].get('w1'))
    check('DV-dv2-notinstalled', 'dv-2' not in fam['installs'], '')

    # ---- G1: Type-B installs exactly 2/24 (nf-b-12, nf-b-17); control 0/24 ----
    # installs dict keys for B1 are fixture cids like 'nf-b-12'
    fb = sorted(c for c in fam['installs'] if c.startswith('nf-b-'))
    cb = sorted(c for c in ctl['installs'] if c.startswith('nf-b-'))
    check('G1-fam-typeB', fb == ['nf-b-12', 'nf-b-17'], 'fam installs=%s' % fb)
    check('G1-control-typeB', cb == [], 'control installs=%s' % cb)

    # ---- G2: blind honest 6/6; attacks a1/a2/a6 + w2/w3 ledgered correctly ----
    bh = ['bl-h%d' % i for i in range(1, 7)]
    bh_ok = [c for c in bh if c in fam['installs']]
    check('G2-blind-honest-6/6', len(bh_ok) == 6, 'installed=%s' % bh_ok)
    exp_reasons = {'bl-a1': 'ROLE-SWAP', 'bl-a2': 'MODAL', 'bl-a6': 'REFERENCE',
                   'w2': 'ROLE-SWAP', 'w3': 'MODAL'}
    for cid, rsn in sorted(exp_reasons.items()):
        check('G2-%s-ledger' % cid, fam['ures'].get(cid) == rsn,
              'reason=%s' % fam['ures'].get(cid))
        check('G2-%s-noinstall' % cid, cid not in fam['installs'], '')

    # ---- G3: Type-A 20/20; Type-C identical to control ----
    fa = sorted(c for c in fam['installs'] if c.startswith('nf-a-'))
    check('G3-typeA-20/20', len(fa) == 20, 'n=%d' % len(fa))
    fc = sorted(c for c in fam['installs'] if c.startswith('nf-c-'))
    cc = sorted(c for c in ctl['installs'] if c.startswith('nf-c-'))
    check('G3-typeC-identical', fc == cc, 'fam=%d control=%d' % (len(fc), len(cc)))

    # ---- G4: governing pair ROLE-SWAP, both undetermined/pending, neither installed ----
    check('G4-gov-roleswap', fam['ures'].get('gov') == 'ROLE-SWAP',
          'reason=%s' % fam['ures'].get('gov'))
    check('G4-gov-noinstall', 'gov' not in fam['installs'], '')

    # ---- G5: w1 WITHHOLD; p3 WITHHOLD no install ----
    check('G5-w1-withhold', 'w1' not in fam['installs'],
          'reason=%s' % fam['ures'].get('w1'))
    check('G5-p3-withhold', 'p3' not in fam['installs'],
          'reason=%s' % fam['ures'].get('p3'))

    # ---- G6: determinism already checked by runner; report pass dirs present ----
    det_ok = True
    for arm in ('control', 'fam_dv'):
        for p in ('pass1', 'pass2'):
            for fn in ('knowledge_ledger.txt', 'refusal_ledger.txt',
                       'undetermined_ledger.txt', 'pending_import.txt', 'run_li.log'):
                if not os.path.exists(os.path.join(rundir, arm, p, fn)):
                    det_ok = False
    check('G6-artifacts-present', det_ok, '')

    for n in notes:
        print(n)
    print('ANALYZER|%s|fails=%d' % ('PASS' if not fails else 'FAIL', len(fails)))
    sys.exit(0 if not fails else 1)

if __name__ == '__main__':
    main()
