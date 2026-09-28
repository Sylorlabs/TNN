#!/usr/bin/env python3
"""Score math.zag output against frozen expected.json. Usage: score.py <runfile>"""
import json, sys
from fractions import Fraction

exp = json.load(open('/home/hatch/workspace/tnn-lab/math/expected.json'))
lines = [l.rstrip('\n') for l in open(sys.argv[1]) if l.strip()]
got = {}
for l in lines:
    if l.startswith('INSTALL') or l.startswith('FACTS'):
        continue
    parts = l.split('\t')
    if len(parts) != 4:
        print("MALFORMED:", l); continue
    got[parts[0]] = (parts[1], parts[2], parts[3])

def canon(s):
    s = s.strip()
    if '/' in s:
        n, d = s.split('/')
        return Fraction(int(n), int(d))
    return Fraction(s)

groups = {'B1': 'B1', 'W': 'B2', 'P': 'B2', 'E': 'B3', 'M': 'B4'}
bats = {'B1': [], 'B2': [], 'B3': [], 'B4': []}
miss = []
for bid, e in exp.items():
    b = groups[bid.split('-')[0]]
    g = got.get(bid)
    if g is None:
        miss.append((bid, 'MISSING', e, '')); bats[b].append(0); continue
    mode, ans, trace = g
    ok = True
    reason = ''
    want_mode, want_ans = e['mode'], e['answer']
    if want_mode == 'ABSTAIN':
        if mode != 'ABSTAIN' or ans != 'ABSTAIN':
            ok = False; reason = f"got {mode} {ans}, want ABSTAIN"
    elif want_mode == 'EITHER':
        if mode not in ('RETRIEVE', 'COMPUTE'):
            ok = False; reason = f"mode {mode} not RETRIEVE/COMPUTE"
        else:
            try:
                if canon(ans) != canon(want_ans):
                    ok = False; reason = f"ans {ans} != {want_ans}"
            except Exception as ex:
                ok = False; reason = f"unparseable {ans}: {ex}"
    else:
        if mode != want_mode:
            ok = False; reason = f"mode {mode} != {want_mode}"
        else:
            try:
                if canon(ans) != canon(want_ans):
                    ok = False; reason = f"ans {ans} != {want_ans}"
            except Exception as ex:
                ok = False; reason = f"unparseable {ans}: {ex}"
    bats[b].append(1 if ok else 0)
    if not ok:
        miss.append((bid, reason, e, f"got {mode} {ans} [{trace}]"))

print("=== per-battery ===")
for b, rs in bats.items():
    print(f"{b}: {sum(rs)}/{len(rs)}")
print("=== misses ===")
for m in miss:
    print(m[0], '|', m[1], '| expected:', m[2], '|', m[3])
print("=== totals ===")
print(f"TOTAL {sum(sum(v) for v in bats.values())}/84")
