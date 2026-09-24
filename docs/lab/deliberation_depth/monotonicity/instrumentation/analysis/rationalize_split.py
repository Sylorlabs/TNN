#!/usr/bin/env python3
"""H-RATIONALIZE allocation split: per round, relative to the current leader,
(a) attack weight  = attacks[leader] consumed that round
(b) defend weight  = supports[leader] consumed that round
(c) sniping        = kills that round (TRACE elim field)
Plus structural checks: leader never targeted by kill ops (code), pool fixed."""
import json, re
from collections import defaultdict

D = '/home/hatch/workspace/tnn-lab/deliberation_depth/monotonicity/instrumentation/run'
CEIL = '/home/hatch/workspace/tnn-lab/deliberation_depth/ceiling/items/ceiling_battery.jsonl'
TRAP = '/home/hatch/workspace/tnn-lab/deliberation_depth/items_v2/trap.jsonl'

def fam(i):
    if i.startswith('H5B-P-'): return 'P'
    if i.startswith('H5B-O-'): return 'O'
    if i.startswith('H5B-D-'): return 'D'
    return 'trap'

# input evidence: item -> {eid: (supports dict, attacks dict)}
EV = {}
for path in (CEIL, TRAP):
    for line in open(path):
        d = json.loads(line)
        m = {}
        for e in d['input']['evidence']:
            m[e['id']] = (e.get('supports', {}), e.get('attacks', {}))
        EV[d['id']] = m

TR = re.compile(r'r=(\d+) leader=(\S+) conf=(\d+) margin=(-?\d+) lscore=(-?\d+) rscore=(-?\d+) ev=(\d+) nalive=(\d+) elim=(\d+) bound=(\d+) gtrank=(-?\d+) correct=(\d+) gain=(\d+)')

def load_traces(cell):
    out = {}
    with open(f'{D}/{cell}_A.ledger') as f:
        for line in f:
            d = json.loads(line)
            a = d.get('action')
            if a == 'TRACE':
                m = TR.fullmatch(d['detail'])
                row = {'r': int(m.group(1)), 'leader': m.group(2), 'conf': int(m.group(3)),
                       'elim': int(m.group(9)), 'gtrank': int(m.group(11)), 'correct': int(m.group(12)),
                       'nalive': int(m.group(8))}
                out.setdefault(d['item'], {})[row['r']] = row
            elif a == 'EVIDENCE':
                m2 = re.fullmatch(r'e=(\S+) c=(\d+)', d['detail'])
                out.setdefault(d['item'], {}).setdefault('evmap', {})[d['round']] = m2.group(1)
    return out

def analyze(cell, label):
    T = load_traces(cell)
    agg = defaultdict(lambda: [0, 0, 0, 0])  # key -> [attack_w, defend_w, kills, rounds]
    for it, info in T.items():
        f = fam(it); evmap = info.get('evmap', {})
        rows = {k: v for k, v in info.items() if k != 'evmap'}
        # flip round: first round with correct=0 (O items)
        flipr = min([r for r, x in rows.items() if x['correct'] == 0], default=None)
        for r, x in sorted(rows.items()):
            eid = evmap.get(r)
            a = b = 0
            # pre-round leader: whoever led coming INTO this round (r-1's post leader)
            lpre = rows[r-1]['leader'] if r - 1 in rows else None
            if eid and lpre and it in EV and eid in EV[it]:
                sup, att = EV[it][eid]
                b = sup.get(lpre, 0)
                a = att.get(lpre, 0)
            key = f
            if f == 'O' and flipr is not None:
                key = 'O_pre' if r < flipr else 'O_post'
            agg[key][0] += a; agg[key][1] += b; agg[key][2] += x['elim']; agg[key][3] += 1
    print(f'--- {label} ({cell}) ---')
    print('  key: attack_w  defend_w  kills  rounds | defend share of (a+b)')
    for k in sorted(agg):
        a, b, c, n = agg[k]
        share = b / max(1, a + b)
        print(f'  {k:>6}: {a:>8} {b:>8} {c:>5} {n:>6} | {share:.2f}')
    return T

T64 = analyze('ceil_c64_d64', 'ceiling d64')
analyze('trap_fz_d8', 'trap d8')

print()
print('=== grok prediction checks ===')
# 1. wrong answer already in pool at r1 (reweighting not birth): O items, ADMIT alive?
#    pool is fixed (nh=2 always); check ADMIT==leader at no point before flip is falsehood;
#    instead: was the false leader ever eliminated before becoming leader? use gtrank/nalive.
#    Direct: on O items the false leader ADMIT is a hypothesis from r1 (nh=2 fixed).
o_items = [it for it in T64 if fam(it) == 'O']
print(f'O items: {len(o_items)}; hypotheses fixed at 2 (pool never gains members) by construction')
# 2. at flip round, truth alive but outscored (discriminator vs H-ELIM-ASYM)
n_flip_alive = 0; n_flip = 0
for it in o_items:
    rows = {k: v for k, v in T64[it].items() if k != 'evmap'}
    fr = min([r for r, x in rows.items() if x['correct'] == 0], default=None)
    if fr is not None:
        n_flip += 1
        if rows[fr]['gtrank'] >= 1 and rows[fr]['nalive'] == 2:
            n_flip_alive += 1
print(f'O flips where truth still alive-but-outscored at flip round: {n_flip_alive}/{n_flip}')
# 3. kills after flip (H-ELIM-ASYM irreversibility)
kills_post = sum(x['elim'] for it in o_items for k, x in T64[it].items()
                 if k != 'evmap' and x['correct'] == 0)
print(f'kill events on O items in post-flip rounds: {kills_post}')
