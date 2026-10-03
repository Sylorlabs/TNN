#!/usr/bin/env python3
"""FAM-NOM runner: adaptation of run_d4fix.py for the D4-RESID FAM-NOM family.

Arms: 'control' (unmodified D4-FIX binary, byte-identical rebuild) vs
'fam_nom' (R0+R1 fork). Batteries: frozen B1..B5 + FAM-NOM battery +
governing wolves/hawks pair. 2 passes per arm; all five artifacts must be
byte-identical across passes. No RNG anywhere.

Usage: run_fam_nom.py <outdir> [--only nom|wb|blind|full] [--arm control|fam_nom]
  --only nom   : FAM-NOM battery only (hole demo / family check)
  --only wb    : W probes only (smoke)
  --only blind : blind battery only (smoke)
  --only full  : everything (B1..B5 + gov + nom)
  --arm X      : run only arm X (default: both arms for --only full,
                 control only otherwise)
"""
import os, sys, hashlib, filecmp, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = '/home/hatch/workspace/d4resid/fam_nom'
BUILD = os.path.join(WORK, 'build')
NOMBAT = os.path.join(WORK, 'battery')

spec = importlib.util.spec_from_file_location('run_d4fix', '/tmp/run_d4fix.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

ARMS = {
    'control': dict(
        webg=os.path.join(BUILD, 'd4fix_bin'),
        guides=m.GUIDES,
        teach_exact=sorted(['G1', 'G2', 'G3', 'G4', 'G5', 'G6']),
    ),
    'fam_nom': dict(
        webg=os.path.join(BUILD, 'fam_nom_bin'),
        guides=m.GUIDES,
        teach_exact=sorted(['G1', 'G2', 'G3', 'G4', 'G5', 'G6']),
    ),
}

NOMCLS = ['nom-1', 'nom-2', 'nom-3', 'nom-4']

# Governing pair (prereg 3.1): wolves/hawks role-swap, inline direct cluster.
GOV = [[
    'gov',
    'who beat the hillcrest hawks last winter',
    [
        ('gov-p1', 'Riverside win report',
         'https://govalpha.example/gov-p1',
         ['The Riverside Wolves beat the Hillcrest Hawks last winter.']),
        ('gov-p2', 'Hillcrest win report',
         'https://govbeta.example/gov-p2',
         ['The Hillcrest Hawks beat the Riverside Wolves last winter.']),
    ],
]]


def load_all(which):
    fixtures, direct = [], []
    if which in ('full',):
        fixtures = m.load_manifest(m.MANIFEST)
        fstat = m.load_fetch_status(m.SNAPDIR)
        fid = m.load_fidelity(m.SNAPDIR)
    else:
        fstat, fid = {}, {}
    if which in ('full',):
        direct += m.load_direct_battery(m.PBAT, m.PCLS)
        direct += m.load_direct_battery(m.S1BAT, m.S1H, cid_prefix='s1-')
        direct += m.load_direct_battery(m.S1BAT, m.S1A, cid_prefix='s1-')
    if which in ('wb', 'full'):
        direct += m.load_direct_battery(m.WBBAT, m.WBCLS)
    if which in ('blind', 'full'):
        direct += m.load_direct_battery(m.BLINDBAT, m.BLH, cid_prefix='bl-')
        direct += m.load_direct_battery(m.BLINDBAT, m.BLA, cid_prefix='bl-')
    if which in ('nom', 'full'):
        direct += m.load_direct_battery(NOMBAT, NOMCLS)
    if which in ('full',):
        direct += GOV
    n_fix = len(fixtures)
    n_dir = len(direct)
    print('LOADED|mode=%s|fixtures=%d|direct=%d' % (which, n_fix, n_dir))
    return fixtures, direct, fstat, fid


def main():
    outdir = os.path.abspath(sys.argv[1])
    which = 'full'
    for a in sys.argv[2:]:
        if a.startswith('--only='):
            which = a.split('=', 1)[1]
        elif a == '--only' :
            pass
    if '--only' in sys.argv:
        i = sys.argv.index('--only')
        if i + 1 < len(sys.argv):
            which = sys.argv[i + 1]
    fixtures, direct, fstat, fid = load_all(which)

    arms = ARMS
    if '--arm' in sys.argv:
        i = sys.argv.index('--arm')
        arms = {sys.argv[i + 1]: ARMS[sys.argv[i + 1]]}
    elif which in ('nom', 'wb', 'blind'):
        # hole demo / smoke: control arm only
        arms = {'control': ARMS['control']}

    for arm, cfg in arms.items():
        for p in (1, 2):
            passdir = os.path.join(outdir, arm, 'pass%d' % p)
            if not m.run_pass(arm, cfg, passdir, fixtures, direct, fstat, fid):
                sys.exit(3)

    ok = True
    for arm in arms:
        p1 = os.path.join(outdir, arm, 'pass1')
        p2 = os.path.join(outdir, arm, 'pass2')
        for f in ('knowledge_ledger.txt', 'refusal_ledger.txt',
                  'undetermined_ledger.txt', 'pending_import.txt', 'run_li.log'):
            same = filecmp.cmp(os.path.join(p1, f), os.path.join(p2, f), shallow=False)
            print('DET|arm=%s|%s|%s' % (arm, f, 'IDENTICAL' if same else 'DIFFER'))
            ok = ok and same
    print('DETERMINISM|%s' % ('PASS' if ok else 'FAIL'))
    sys.exit(0 if ok else 4)


if __name__ == '__main__':
    main()
