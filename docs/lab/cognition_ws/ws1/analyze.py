#!/usr/bin/env python3
"""WS1-A analyzer: parse r1 raw logs (reruns byte-identical modulo wall_ns),
compute prereg metrics: W, W/ep, wall/ep, accuracy, ratios, attribution,
conditions map, gates."""
import re, csv, statistics, sys

RAW = 'runs/raw'
CAPS = [32, 128, 512]; ADVS = [0, 15, 35]; REPS = [1, 3]
ARMS = ['trained', 'naive', 'auto']

def parse(log):
    d = {}
    for line in open(log):
        line = line.strip()
        m = re.search(r'correct=(\d+),wrong=(\d+),abstain=(\d+),spurious=(\d+)', line)
        if m:
            d['correct'], d['wrong'], d['abstain'], d['spurious'] = map(int, m.groups())
        m = re.search(r'find_steps=(\d+),scan_steps=(\d+),mutops=(\d+),suppress=(\d+)', line)
        if m:
            d['find'], d['scan'], d['mutops'], d['suppress'] = map(int, m.groups())
        m = re.search(r'collateral=(\d+)', line)
        if m: d['collateral'] = int(m.group(1))
        m = re.search(r'consol=(\d+),overwrite=(\d+),evict=(\d+),dropped=(\d+)', line)
        if m:
            d['consol'], d['overwrite'], d['evict'], d['dropped'] = map(int, m.groups())
        m = re.search(r'add=(\d+),kill=(\d+),pin=(\d+),promote=(\d+)', line)
        if m:
            d['add'], d['kill'], d['pin'], d['promote'] = map(int, m.groups())
        m = re.search(r'audit_n=(\d+),ledger_bytes=(\d+)', line)
        if m: d['audit_n'], d['ledger_bytes'] = map(int, m.groups())
        m = re.search(r'arena_bytes=(\d+)', line)
        if m: d['arena_bytes'] = int(m.group(1))
        m = re.search(r'wall_ns=(\d+),episodes=(\d+)', line)
        if m: d['wall_ns'], d['episodes'] = int(m.group(1)), int(m.group(2))
    d['W'] = d['find'] + d['scan'] + d['mutops'] + d['suppress']
    d['W_ep'] = d['W'] / d['episodes']
    d['wall_ep'] = d['wall_ns'] / d['episodes']
    return d

rows = []
for cap in CAPS:
    for adv in ADVS:
        for rep in REPS:
            cell = f'cap{cap}a{adv}r{rep}'
            nt = cap // 2
            rec = {'cell': cell, 'cap': cap, 'adv': adv, 'rep': rep, 'nt': nt}
            for arm in ARMS:
                d = parse(f'{RAW}/{cell}_{arm}_r1.log')
                d['acc'] = d['correct'] / nt
                rec[arm] = d
            rows.append(rec)

print("cell             | arm     | acc      | spur | coll  | W/ep    | wall/ep(ns) | find/ep | scan/ep | mut/ep | sup/ep")
print("-" * 118)
for r in rows:
    for arm in ARMS:
        d = r[arm]
        coll = d.get('collateral', '-')
        print(f"{r['cell']:16s} | {arm:7s} | {d['acc']:.4f}   | {d['spurious']:4d} | {str(coll):5s} | "
              f"{d['W_ep']:7.2f} | {d['wall_ep']:11.0f} | {d['find']/d['episodes']:7.2f} | "
              f"{d['scan']/d['episodes']:7.2f} | {d['mutops']/d['episodes']:6.2f} | {d['suppress']/d['episodes']:6.2f}")

print()
print("=== RATIO TABLE: auto/trained per cell ===")
print("cell             | W_ratio | wall_ratio | acc_gap(t-a) | auto_scan_share | auto_churn_share")
ratios = []
adv_large_ratios = []
ge2 = 0; ge2_al = 0; al_n = 0
acc_fails = []
for r in rows:
    t, a = r['trained'], r['auto']
    wr = a['W'] / t['W']
    wallr = a['wall_ns'] / t['wall_ns']
    gap = t['acc'] - a['acc']
    scan_share = a['scan'] / a['W']
    churn_share = a['mutops'] / a['W']
    ratios.append(wr)
    if r['adv'] >= 15 and r['cap'] >= 128:
        adv_large_ratios.append(wr); al_n += 1
        if wr >= 2.0: ge2_al += 1
    if wr >= 2.0: ge2 += 1
    flag = ''
    if abs(gap) > 0.05:
        acc_fails.append((r['cell'], gap)); flag = '  <-- ACC GATE FAIL'
    print(f"{r['cell']:16s} | {wr:7.2f} | {wallr:10.2f} | {gap:+.4f}        | {scan_share:13.2%} | {churn_share:14.2%}{flag}")

print()
print("median W(auto)/W(trained) overall: %.2f (n=%d)" % (statistics.median(ratios), len(ratios)))
print("min/max: %.2f / %.2f" % (min(ratios), max(ratios)))
print("adversarial+large subregime (adv>=15, cap>=128): median %.2f, >=2.0 in %d/%d (%.0f%%)" %
      (statistics.median(adv_large_ratios), ge2_al, al_n, 100*ge2_al/al_n))
print("cells with W ratio >= 2.0: %d/%d" % (ge2, len(ratios)))
print("accuracy-gate failures (|acc_t-auto|>0.05): %d %s" % (len(acc_fails), acc_fails))

print()
print("=== TRAINED vs NAIVE (WS1-B: A1 vs A2 direction + collateral) ===")
for r in rows:
    t, n = r['trained'], r['naive']
    print(f"{r['cell']:16s} | trained W/ep={t['W_ep']:7.2f} acc={t['acc']:.4f} | "
          f"naive W/ep={n['W_ep']:7.2f} acc={n['acc']:.4f} | naive collateral={n.get('collateral',0)} spurious={n['spurious']} | W ratio n/t={n['W']/t['W']:.2f}")

print()
print("=== WALL-vs-W DECOMPOSITION (per-step accessor cost) ===")
for r in rows:
    for arm in ARMS:
        d = r[arm]
        if d['W'] > 0:
            print(f"{r['cell']:16s} {arm:7s} ns/W-step={d['wall_ns']/d['W']:8.1f} W/ep={d['W_ep']:.2f} wall/ep={d['wall_ep']:.0f}")
    print()
    if r['cell'] == 'cap128a35r3':
        break
