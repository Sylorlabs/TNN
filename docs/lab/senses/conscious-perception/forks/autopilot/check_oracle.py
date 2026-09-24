#!/usr/bin/env python3
"""Compare native F1 RESULT lines against the integer-exact Python oracle.
Usage: check_oracle.py <fixtures-root> <stdout_run1.txt>
Compares task, percept, conf, ops, detail on every fixture. rc=0 iff all match.
"""
import sys, re, importlib.util

def main():
    fixroot, runpath = sys.argv[1], sys.argv[2]
    spec = importlib.util.spec_from_file_location('ref_f1', 'gen/ref_f1.py')
    ref = importlib.util.module_from_spec(spec); spec.loader.exec_module(ref)
    nat = {}
    for line in open(runpath):
        line = line.rstrip('\n')
        if not line.startswith('RESULT'):
            continue
        m = re.match(r'RESULT n=(\d+) fixture=(\S+) task=(\S+) percept=(\S+) '
                     r'conf=(\d+) ops=(\d+) match=(\d+) detail=(.*)', line)
        assert m, 'unparseable RESULT: ' + line[:80]
        n, fix, task, perc, conf, ops, mt, det = m.groups()
        nat[fix] = (task, perc, int(conf), int(ops), det)
    paths = [l.strip() for l in open('battery_all.txt') if l.strip()]
    assert len(nat) == len(paths) == 26, (len(nat), len(paths))
    bad = 0
    for p in paths:
        task, perc, conf, det, ops = ref.perceive(fixroot + '/' + p)
        nt, np_, nc, no, nd = nat[p]
        if not (task == nt and perc == np_ and conf == nc
                and ops == no and det.replace(' ', ',') == nd):
            bad += 1
            print('MISMATCH', p)
            print('  oracle:', task, perc, conf, ops, det)
            print('  native:', nt, np_, nc, no, nd)
    print(f'ORACLE-CHECK fixtures={len(paths)} mismatches={bad}')
    return 1 if bad else 0

sys.exit(main())
