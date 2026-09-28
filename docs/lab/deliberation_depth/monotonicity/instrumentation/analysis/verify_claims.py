#!/usr/bin/env python3
"""White-box verification of the 4 overconfidence decoupling points.
Parses TRACE rows from instrumented ledgers. All inputs deterministic (A/B diffed)."""
import json, glob, re, sys
from collections import Counter, defaultdict

D = '/home/hatch/workspace/tnn-lab/deliberation_depth/monotonicity/instrumentation/run'

def fam(item):
    if item.startswith('H5B-P-'): return 'P'
    if item.startswith('H5B-O-'): return 'O'
    if item.startswith('H5B-D-'): return 'D'
    if item.startswith('TRAP-'): return 'trap'
    return 'logic_ne1'

TR = re.compile(r'r=(\d+) leader=(\S+) conf=(\d+) margin=(-?\d+) lscore=(-?\d+) rscore=(-?\d+) ev=(\d+) nalive=(\d+) elim=(\d+) bound=(\d+) gtrank=(-?\d+) correct=(\d+) gain=(\d+)')

def load(cell):
    """-> dict item -> list of trace dicts (in round order)"""
    out = {}
    with open(f'{D}/{cell}_A.ledger') as f:
        for line in f:
            d = json.loads(line)
            if d.get('action') == 'TRACE':
                m = TR.fullmatch(d['detail'])
                assert m, d['detail']
                keys = ['r','leader','conf','margin','lscore','rscore','ev','nalive','elim','bound','gtrank','correct','gain']
                row = dict(zip(keys, [int(m.group(1)), m.group(2)] + [int(m.group(i)) for i in range(3,14)]))
                out.setdefault(d['item'], []).append(row)
    for v in out.values():
        v.sort(key=lambda x: x['r'])
    return out

CELLS = ['trap_fz_d1','trap_fz_d2','trap_fz_d4','trap_fz_d8','trap_fz_deep16',
         'ceil_c64_d1','ceil_c64_d2','ceil_c64_d4','ceil_c64_d8','ceil_c64_d16',
         'ceil_c64_d32','ceil_c64_d64','ceil_c64_adaptive','ceil_c64_bound',
         'logicne1_fz_d1','logicne1_fz_deep16']
DATA = {c: load(c) for c in CELLS}

print('=== CLAIM 4: distinct confidence values across ALL trace rows ===')
vals = Counter()
nrows = 0
for c, items in DATA.items():
    for it, rows in items.items():
        for r in rows:
            vals[r['conf']] += 1; nrows += 1
print('total trace rows:', nrows)
print('distinct conf values:', sorted(vals))
print('counts:', dict(sorted(vals.items())))
print('n distinct:', len(vals))

print()
print('=== CLAIM 1: sole-survivor pin at 1000 ===')
tot1 = sum(1 for items in DATA.values() for rows in items.values() for r in rows if r['nalive'] == 1)
pin1 = sum(1 for items in DATA.values() for rows in items.values() for r in rows if r['nalive'] == 1 and r['conf'] == 1000)
print(f'rounds with nalive=1: {tot1}; with conf=1000: {pin1} ({100*pin1/max(1,tot1):.2f}%)')
# exact elimination rounds: first round where nalive==1 and previous round (if any) had nalive>1, or r==1
elims = []
gt_kills = []
for c, items in DATA.items():
    for it, rows in items.items():
        for i, r in enumerate(rows):
            prev_n = rows[i-1]['nalive'] if i > 0 else 99
            if r['nalive'] == 1 and prev_n > 1:
                elims.append((c, it, r))
                if i > 0 and rows[i-1]['gtrank'] >= 1 and r['gtrank'] == -1:
                    gt_kills.append((c, it, r, rows[i-1]))
print(f'elimination events (nalive drops to 1): {len(elims)}')
print(f'  of those, conf=1000 at the elimination round: {sum(1 for _,_,r in elims if r["conf"]==1000)}')
print(f'GT-kill events (GT alive before, dead after): {len(gt_kills)}')
print(f'  of those, conf=1000 at the kill round: {sum(1 for _,_,r,_ in gt_kills if r["conf"]==1000)}')
print(f'  of those, correct=0 at the kill round: {sum(1 for _,_,r,_ in gt_kills if r["correct"]==0)}')
# show a sample GT-kill
shown = 0
for c, it, r, prev in gt_kills:
    if shown < 3 and fam(it) == 'O':
        print(f'  sample {c} {it}: r{r["r"]} conf={r["conf"]} margin={r["margin"]} lscore={r["lscore"]} rscore={r["rscore"]} ev={r["ev"]} elim={r["elim"]} correct={r["correct"]} (prev gtrank={prev["gtrank"]} conf={prev["conf"]})')
        shown += 1

print()
print('=== CLAIM 2: margin = distance-to-runner-up, not evidence quality ===')
hi_wrong = Counter(); max_wrong = Counter(); tot = Counter()
for c, items in DATA.items():
    for it, rows in items.items():
        f = fam(it); tot[f] += len(rows)
        for r in rows:
            if r['correct'] == 0:
                if r['conf'] >= 500: hi_wrong[f] += 1
                if r['conf'] == 1000: max_wrong[f] += 1
print('rounds with conf>=500 AND correct=0 (large margin on poisoned/thin evidence):')
for f in ['trap','O','P','D','logic_ne1']:
    print(f'  {f}: {hi_wrong[f]}/{tot[f]} rounds')
print('rounds with conf==1000 AND correct=0 (max confidence while wrong):')
for f in ['trap','O','P','D','logic_ne1']:
    print(f'  {f}: {max_wrong[f]}/{tot[f]} rounds')
# margin overlap: correct=1 vs correct=0 margin distributions
mc1 = Counter(); mc0 = Counter()
for items in DATA.values():
    for rows in items.values():
        for r in rows:
            b = r['margin'] // 100 * 100
            (mc1 if r['correct'] == 1 else mc0)[b] += 1
print('margin histogram correct=1:', dict(sorted(mc1.items())))
print('margin histogram correct=0:', dict(sorted(mc0.items())))

print()
print('=== CLAIM 3: irreversible elimination; margin never re-audited ===')
# code check done by grep separately; here trace evidence:
# O items where GT eliminated then margin only measures survivors (rscore=-1 afterwards)
post = 0; post_items = set()
for c in ['ceil_c64_d64','ceil_c64_bound','ceil_c64_d32','ceil_c64_d16']:
    for it, rows in DATA[c].items():
        if fam(it) != 'O': continue
        kill = None
        for i, r in enumerate(rows):
            if i > 0 and rows[i-1]['gtrank'] >= 1 and r['gtrank'] == -1:
                kill = i; break
        if kill is not None:
            post_items.add(it)
            for r in rows[kill:]:
                if r['rscore'] == -1: post += 1
print(f'O items with GT eliminated (d16/d32/d64/bound legs): {len(post_items)}')
print(f'post-kill rounds where rscore=-1 (margin measures survivors only): {post}')
# sample trace: one O item through the flip
for c in ['ceil_c64_d64']:
    for it, rows in DATA[c].items():
        if fam(it)=='O' and it.endswith('-00'):
            print(f'  sample {it}:')
            for r in rows[:10]:
                print(f"    r{r['r']} leader={r['leader']} conf={r['conf']} margin={r['margin']} lscore={r['lscore']} rscore={r['rscore']} elim={r['elim']} gtrank={r['gtrank']} correct={r['correct']}")
            break
    break

print()
print('=== EXTRA Q1: trap conf trajectory while wrong (theater-while-wrong) ===')
# per-item conf at d1,d2,d4,d8,deep16 from results (final conf) — use TRACE round1..N
for c in ['trap_fz_d1','trap_fz_d2','trap_fz_d4','trap_fz_d8','trap_fz_deep16']:
    acc = sum(r[-1]['correct'] for r in DATA[c].values())/len(DATA[c])
    mc = sum(r[-1]['conf'] for r in DATA[c].values())/len(DATA[c])
    print(f'  {c}: acc={acc:.3f} mean_final_conf={mc:.0f}')
# items where final conf non-decreasing d1->d2->d4 while correct=0 at all three
n = 0
items1 = DATA['trap_fz_d1']; items2 = DATA['trap_fz_d2']; items4 = DATA['trap_fz_d4']
for it in items1:
    c1 = items1[it][-1]['conf']; c2 = items2[it][-1]['conf']; c4 = items4[it][-1]['conf']
    if items1[it][-1]['correct']==0 and items2[it][-1]['correct']==0 and items4[it][-1]['correct']==0 and c1<=c2<=c4:
        n += 1
print(f'  trap items with conf non-decreasing d1->d2->d4 while wrong throughout: {n}/127')

print()
print('=== CLAIM 4b: distinct FINAL confidences (apples-to-apples vs audit) ===')
fvals = Counter()
for c, items in DATA.items():
    for it, rows in items.items():
        fvals[rows[-1]['conf']] += 1
print('distinct final conf values:', sorted(fvals), 'n=', len(fvals))

print()
print('=== CLAIM 2b: confidence actively RISING while wrong (gain>0, correct=0) ===')
rise_wrong = Counter(); rise_gtworse = Counter(); totr = Counter()
for c, items in DATA.items():
    for it, rows in items.items():
        f = fam(it)
        for i, r in enumerate(rows):
            totr[f] += 1
            if r['gain'] > 0 and r['correct'] == 0:
                rise_wrong[f] += 1
            if i > 0 and r['gain'] > 0 and r['gtrank'] > rows[i-1]['gtrank'] >= 1:
                rise_gtworse[f] += 1
for f in ['trap','O','P','D','logic_ne1']:
    print(f'  {f}: conf-rising-while-wrong rounds {rise_wrong[f]}/{totr[f]}; conf-rising-while-GT-rank-worsens {rise_gtworse[f]}')

print()
print('=== EXTRA Q4: logic ne1 theater (conf rises after provable finality) ===')
cell = 'logicne1_fz_deep16'
risers = 0; bound1 = 0; still1000 = 0; corr1 = 0
for it, rows in DATA[cell].items():
    if len(rows) >= 2 and rows[0]['correct'] == 1:
        corr1 += 1
        if rows[0]['bound'] == 1: bound1 += 1
        if any(r['conf'] > rows[0]['conf'] for r in rows[1:]): risers += 1
    if rows[-1]['conf'] == 1000: still1000 += 1
print(f'  items correct at r1: {corr1}/{len(DATA[cell])}; bound=1 at r1: {bound1}/{len(DATA[cell])}')
print(f'  items where conf rises after r1 while verdict static+correct: {risers}')
print(f'  items ending at conf=1000: {still1000}/{len(DATA[cell])}')

print()
print('=== CLAIM 2c: confidence rising with ZERO new evidence (gain>0, ev unchanged) ===')
zero_ev = Counter(); zero_ev_wrong = Counter()
for c, items in DATA.items():
    for it, rows in items.items():
        f = fam(it)
        for i, r in enumerate(rows):
            if i > 0 and r['gain'] > 0 and r['ev'] == rows[i-1]['ev']:
                zero_ev[f] += 1
                if r['correct'] == 0: zero_ev_wrong[f] += 1
for f in ['trap','O','P','D','logic_ne1']:
    print(f'  {f}: gain>0 with no new evidence: {zero_ev[f]} rounds, of which wrong: {zero_ev_wrong[f]}')

print()
print('=== d1 trap catastrophe detail (sensor silence) ===')
import statistics
confs = [rows[0]['conf'] for rows in DATA['trap_fz_d1'].values()]
ev1 = [rows[0]['ev'] for rows in DATA['trap_fz_d1'].values()]
print(f'  n=127, correct=0: {sum(r[0]["correct"]==0 for r in DATA["trap_fz_d1"].values())}, conf values: {sorted(set(confs))}, ev values: {sorted(set(ev1))}')

print()
print('=== bound vs six on O (residual-flip on overthinking) ===')
for c in ['ceil_c64_adaptive','ceil_c64_bound']:
    acc = sum(r[-1]['correct'] for it,r in DATA[c].items() if fam(it)=='O')/40
    mr = sum(int(r[-1]['r']) for it,r in DATA[c].items() if fam(it)=='O')/40
    print(f'  {c}: O-acc={acc:.3f} mean_rounds={mr:.2f}')
