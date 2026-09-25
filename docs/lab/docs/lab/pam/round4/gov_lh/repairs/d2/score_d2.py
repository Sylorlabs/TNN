#!/usr/bin/env python3
"""Applies the REPAIRED KB-D2(b) bar (and the ORIGINAL bar on B20) to the
run0 summaries. Decision procedure (frozen):
  n = blocked trues in battery; if n < 10 -> UNDECISIVE;
  if n >= 10: released/n < 0.50 -> KILL else PASS.
Original bar: same rule with n >= 20 required (B20 only)."""
import re
rows = []
for path in ['B20','B12','B6','B110','B10x','B100x']:
    for org in ['D','R','W','N']:
        line = [l for l in open(f'runs/{org}_{path}_run0.out') if l.startswith('BT=')][0]
        m = re.match(r'BT=(\d+) REL=(\d+) BF=(\d+) FREL=(\d+)', line).groups()
        bt, rel, bf, fr = map(int, m)
        rows.append((org, path, bt, rel, bf, fr))

def bar(bt, rel, minn):
    if bt < minn: return 'UNDECISIVE'
    return 'KILL' if rel/bt < 0.50 else 'PASS'

print(f"{'org':4} {'batt':6} {'n':>7} {'rel':>7} {'frac':>7}  {'repaired':10} {'orig(B20)':9} clauseA")
for org, path, bt, rel, bf, fr in rows:
    rep = bar(bt, rel, 10)
    orig = bar(bt, rel, 20) if path=='B20' else '-'
    cla = f"FREL={fr}/8" + (' KILL-D-clauseA' if org=='D' and fr>0 else '')
    print(f"{org:4} {path:6} {bt:>7} {rel:>7} {rel/bt*100:6.1f}%  {rep:10} {orig:9} {cla}")
