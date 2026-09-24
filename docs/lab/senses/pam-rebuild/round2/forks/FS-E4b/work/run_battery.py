#!/usr/bin/env python3
# FS-E4b: run the frozen battery twice (adv + ctrl per task), byte-compare.
# Usage: run_battery.py <lists_dir> <evidence_dir> <e4b_bin>
# Writes evidence/run{1,2}_{adv,ctrl}_<task>.txt(.out); prints cmp results.
import sys, os, subprocess, hashlib

TASKS = ['colordisc', 'colorconst', 'pitchdisc', 'timbredisc', 'motiondir']

def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()

def main():
    lists, ev, e4b = sys.argv[1:4]
    quals = [t for t in TASKS
             if os.path.exists(os.path.join(lists, 'batt_adv_%s.txt' % t))]
    print('running tasks: %s' % quals, flush=True)
    files = []
    for r in (1, 2):
        for t in quals:
            for split in ('adv', 'ctrl'):
                lp = os.path.join(lists, 'batt_%s_%s.txt' % (split, t))
                led = os.path.join(ev, 'run%d_%s_%s.txt' % (r, split, t))
                rc = subprocess.run([e4b, 'judge_list', lp, led]).returncode
                if rc != 0:
                    print('DRIVER FAILED run%d %s %s' % (r, split, t), flush=True)
                    sys.exit(1)
                files.append(led)
                files.append(led + '.out')
        print('run %d complete' % r, flush=True)
    ok = True
    for t in quals:
        for split in ('adv', 'ctrl'):
            a = os.path.join(ev, 'run1_%s_%s.txt' % (split, t))
            b = os.path.join(ev, 'run2_%s_%s.txt' % (split, t))
            for suf in ('', '.out'):
                sa, sb = sha(a + suf), sha(b + suf)
                match = (sa == sb)
                ok = ok and match
                print('%s%s run1==run2: %s' % (os.path.basename(a) + suf,
                                               '', match), flush=True)
    # line counts sanity
    for t in quals:
        for split in ('adv', 'ctrl'):
            n = sum(1 for _ in open(os.path.join(ev, 'run1_%s_%s.txt.out' % (split, t))))
            exp = 2000 if split == 'adv' else 1000
            print('%s %s trials: %d (expected %d)' % (t, split, n, exp), flush=True)
    print('BYTE_IDENTICAL_X2: %s' % ok, flush=True)
    sys.exit(0 if ok else 1)

if __name__ == '__main__':
    main()
