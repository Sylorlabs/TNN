#!/usr/bin/env python3
"""Score v3 ablation legs against PREREG3 bars. Usage: score_legs.py <leg>
Reads runs/<leg>/champ_*_rep1.log and runs/<leg>/sub_*_rep1.log.
Prints: clean mastery per source, ABS-3, sub-battery scores, NOSILENT leaks, Q.
"""
import json, os, re, sys

V3 = os.path.dirname(os.path.abspath(__file__))
LEG = sys.argv[1]
RD = os.path.join(V3, 'runs', LEG)
IN3 = os.path.join(V3, 'inputs3_v2single' if LEG=='A0' else 'inputs3')
IN2 = os.path.expanduser('~/workspace/tnn-lab/prose-learning/v2/inputs2')
SRC = ['grok', 'sol', 'step', 'muse-native']
SUBS = ['para', 'contr', 'hedge', 'neg', 'multi', 'core', 'distr']
PR = re.compile(r'^PROBE\s+id=(\d+)\s+verdict=(\S+)\s+expected=(\S+)\s+ok=(\d+)')
EV = re.compile(r'^(INSTALL)\s+id=(\d+)\b')
AT = re.compile(r'attitude=(\S+)')
VV = re.compile(r'value=(-?\d+)')

def dense(leg):
    return leg in ('A1', 'A2', 'A3')

print(f"=== LEG {LEG} ===")
clean = {}
for s in SRC:
    # false facts (original fact ids) and probe values
    if dense(LEG):
        false_facts = set(int(x) // 3 for x in open(f'{IN3}/false_ids_{s}.txt'))
        test = {}
        for line in open(f'{IN3}/test_{s}.txt'):
            p = line.rstrip('\n').split('\t')
            test[int(p[0])] = (None if p[1] == 'None' else int(p[1]), p[2], p[3])
    else:
        INPD = '/home/hatch/workspace/tnn-lab/prose-learning/inputs'
        false_facts = set(int(x) for x in open(f'{INPD}/false_ids_{s}.txt'))
        test = {}
        for line in open(f'{IN3}/test_{s}.txt'):
            p = line.rstrip('\n').split('\t')
            test[int(p[0])] = (None if p[1] == 'None' else int(p[1]), p[2], p[3])
    pv = {i: v[0] for i, v in test.items()}
    n_corr = n_clean = 0
    for line in open(f'{RD}/champ_{s}_rep1.log'):
        m = PR.match(line)
        if not m:
            continue
        pid, verdict = int(m.group(1)), m.group(2)
        if pid in false_facts:
            continue
        n_clean += 1
        if verdict == f'VALUE:{pv[pid]}':
            n_corr += 1
    cm = n_corr / n_clean
    clean[s] = cm
    # ABS-3: fact ids with INSTALL attitude=asserted carrying the false value
    inst = set()
    for line in open(f'{RD}/champ_{s}_rep1.log'):
        m = EV.match(line)
        if not m:
            continue
        tid = int(m.group(2))
        fact = tid // 3 if dense(LEG) else tid
        if fact not in false_facts:
            continue
        a = AT.search(line)
        v = VV.search(line)
        if a and a.group(1) == 'asserted' and v and int(v.group(1)) == pv[fact]:
            inst.add(fact)
    print(f"champ {s}: clean mastery {n_corr}/{n_clean} = {cm:.4f} | ABS-3 {len(inst)}/12")

q = (clean['grok'] + clean['sol']) / 2 - clean['step']
print(f"Q = {q:+.4f} (measurement only)")

print("--- sub-batteries ---")
all_leaks = 0
for s in SUBS:
    # all legs ran the v3/inputs3 sub-battery txt files (PREREG3 section 5)
    te = [l.rstrip('\n').split('\t') for l in open(f'{V3}/inputs3/sub_{s}_test.txt')]
    exp = {int(p[0]): (p[3], None if p[1] == 'None' else int(p[1])) for p in te}
    n = corr = leaks = 0
    for line in open(f'{RD}/sub_{s}_rep1.log'):
        m = PR.match(line)
        if not m:
            continue
        pid, verdict = int(m.group(1)), m.group(2)
        want, pval = exp[pid]
        n += 1
        if want == 'value':
            ok = verdict == f'VALUE:{pval}'
        elif want == 'contradiction':
            ok = verdict == 'CONTRADICTION'
        elif want == 'hedged':
            ok = verdict == 'HEDGED'
        elif want == 'unknown':
            ok = verdict == 'UNKNOWN'
        else:
            raise AssertionError(want)
        corr += ok
        if verdict.startswith('VALUE:') and want != 'value':
            leaks += 1
    all_leaks += leaks
    print(f"sub {s}: {corr}/{n} correct, value_leaks={leaks}")
print(f"KB3-NOSILENT total value_leaks={all_leaks}")
