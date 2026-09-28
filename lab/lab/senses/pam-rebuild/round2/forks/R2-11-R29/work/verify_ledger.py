#!/usr/bin/env python3
"""B6: verify the hash-chained ledger.

Reconstructs each ledger entry from percepts.tsv (trial, task, j-code via
reverse jname, conf, disp-code, ops, nsel, sel, claim, warrant) and checks:
  nh[i] == sha256(prev_bytes[i] || entry[i])
where prev_bytes[0] = 32 zero bytes and prev_bytes[i] = bytes(nh[i-1]).

Usage: verify_ledger.py <run_base>   (checks both shards)
"""
import hashlib, sys, glob

JMAP = {
    'colordisc': {'SAME': 0, 'DIFFERENT': 1},
    'colorconst': {'SAME_SURFACE': 0, 'DIFFERENT': 1},
    'shapetrans': {'CIRCLE': 0, 'TRIANGLE': 1, 'SQUARE': 2},
    'pitchdisc': {'SAME': 0, 'HIGHER': 1, 'LOWER': 2},
    'timbredisc': {'PURE': 0, 'BRIGHT': 1, 'DARK': 2, 'RICH': 3},
    'motiondir': {'STILL': 0, 'N': 1, 'NE': 2, 'E': 3, 'SE': 4, 'S': 5,
                  'SW': 6, 'W': 7, 'NW': 8},
}

def main():
    base = sys.argv[1]
    total = bad = 0
    for lpath in sorted(glob.glob(base + '_sh?/LEDGER.jsonl')):
        ppath = lpath.replace('LEDGER.jsonl', 'percepts.tsv')
        # NB: trial ids repeat across tasks; match ledger lines to percepts
        # rows IN ORDER (the binary writes them in the same loop).
        Prows = [l.split('\t') for l in open(ppath).read().splitlines()[1:]]
        Llines = open(lpath).read().splitlines()
        assert len(Prows) == len(Llines), (lpath, len(Prows), len(Llines))
        prev = bytes(32)
        for line, r in zip(Llines, Prows):
            total += 1
            hexh, rest = line.split(' ', 1)
            fields = dict(f.split('=', 1) for f in rest.split(' '))
            trial = fields['trial']
            assert r[0] == trial, (trial, r[0])
            task, jname, conf, disp, ops, nsel, sel, claim, warrant = \
                r[1], r[3], r[4], r[5], r[6], r[7], r[8], r[9], r[10]
            j = JMAP[task][jname]
            d = 1 if disp == 'INSTALL' else 0
            entry = (f"v=1|trial={trial}|task={task}|j={j}|conf={conf}|disp={d}"
                     f"|ops={ops}|nsel={nsel}|sel={sel}|claim={claim}|warrant={warrant}")
            h = hashlib.sha256(prev + entry.encode()).hexdigest()
            if h != hexh:
                bad += 1
                if bad <= 3:
                    print('CHAIN BREAK', lpath, trial, h[:16], hexh[:16])
            prev = bytes.fromhex(hexh)
    print(f"ledger entries={total} chain_breaks={bad}")
    print('B6 ledger:', 'PASS' if bad == 0 else 'FAIL')

main()
