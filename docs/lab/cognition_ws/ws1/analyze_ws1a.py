#!/usr/bin/env python3
"""WS1-A analysis per frozen PREREG_WS1A.md. Reads runs/raw/*.log."""
import os, glob, re, statistics, sys

LOGDIR = os.path.expanduser("~/workspace/cognition_ws/ws1/runs/raw")

def parse(log):
    d = {}
    for line in log.splitlines():
        line = line.strip()
        m = re.match(r"WS1A,cell=(\S+),probe,arm=(\S+),correct=(\d+),wrong=(\d+),abstain=(\d+),spurious=(\d+)", line)
        if m:
            d['cell'], d['arm'] = m.group(1), m.group(2)
            d['correct'], d['wrong'], d['abstain'], d['spurious'] = map(int, m.groups()[2:])
            continue
        m = re.match(r"WS1A,cell=(\S+),arm=(\S+),cost,(.*)$", line)
        if m:
            for kv in m.group(3).split(","):
                k, v = kv.split("=")
                d[k] = int(v)
            continue
        m = re.match(r"WS1A,cell=(\S+),arm=(\S+),time,wall_ns=(\d+),episodes=(\d+)", line)
        if m:
            d['wall_ns'], d['episodes'] = int(m.group(3)), int(m.group(4))
            continue
        m = re.match(r"WS1A,cell=(\S+),arm=(\S+),digest=(\d+)", line)
        if m:
            d['digest'] = int(m.group(3))
            continue
        m = re.match(r"WS1A,cell=(\S+),arm=(\S+),determinism,match=(\d+)", line)
        if m:
            d['match'] = int(m.group(3))
    d['W'] = d.get('find_steps', 0) + d.get('scan_steps', 0) + d.get('mutops', 0)
    d['nt'] = {'cap32': 16, 'cap128': 64, 'cap512': 256}[re.match(r'cap(\d+)', d['cell']).group(0)]
    d['acc'] = d['correct'] / d['nt']
    d['wall_ep'] = d['wall_ns'] / d['episodes']
    return d

cells = {}
nfiles = 0
for f in glob.glob(os.path.join(LOGDIR, "*.log")):
    nfiles += 1
    d = parse(open(f).read())
    key = (d['cell'], d['arm'])
    cells.setdefault(key, []).append(d)

assert nfiles == 162, f"expected 162 logs, got {nfiles}"
assert len(cells) == 54, f"expected 54 cell-arms, got {len(cells)}"
for k, v in cells.items():
    assert len(v) == 3, f"{k}: {len(v)} reruns"
    dg = set(x['digest'] for x in v)
    assert len(dg) == 1, f"{k}: digests differ {dg}"
    assert all(x['match'] == 1 for x in v), f"{k}: determinism match!=1"

# median per cell-arm
med = {k: {f: statistics.median([x.get(f, 0) for x in v]) for f in
      ['W', 'find_steps', 'scan_steps', 'mutops', 'suppress', 'acc', 'wall_ep',
       'add', 'kill', 'pin', 'promote', 'overwrite', 'evict', 'replay', 'clean',
       'arena_bytes', 'ledger_bytes', 'episodes', 'spurious', 'wrong', 'abstain',
       'collateral', 'audit_n', 'consol', 'dropped']}
       for k, v in cells.items()}

def cell_parts(cell):
    cap = int(re.match(r"cap(\d+)", cell).group(1))
    adv = int(re.search(r"a(\d+)r", cell).group(1))
    rep = int(re.search(r"r(\d+)$", cell).group(1))
    return cap, adv, rep

cellnames = sorted({k[0] for k in cells}, key=lambda c: (int(re.match(r"cap(\d+)", c).group(1)),
                    int(re.search(r"a(\d+)r", c).group(1)), int(re.search(r"r(\d+)$", c).group(1))))

print("== PER-CELL W (median of 3 reruns), R=auto/trained ==")
print(f"{'cell':<14}{'W_tr':>12}{'W_naive':>12}{'W_auto':>12}{'R':>8}{'acc_tr':>8}{'acc_naive':>10}{'acc_auto':>9}")
R, Rmatch = {}, {}
for c in cellnames:
    wt = med[(c, 'trained')]['W']; wn = med[(c, 'naive')]['W']; wa = med[(c, 'auto')]['W']
    r = wa / wt
    R[c] = r
    cap, adv, rep = cell_parts(c)
    if cap in (128, 512) and adv in (15, 35):
        Rmatch[c] = r
    print(f"{c:<14}{wt:>12.0f}{wn:>12.0f}{wa:>12.0f}{r:>8.2f}"
          f"{med[(c,'trained')]['acc']:>8.3f}{med[(c,'naive')]['acc']:>10.3f}{med[(c,'auto')]['acc']:>9.3f}")

allR = sorted(R.values())
medianR = statistics.median(allR)
print(f"\nmedian R over 18 cells = {medianR:.3f}")
print(f"matching-regime cells (cap in 128/512, adv in 15/35): {len(Rmatch)}")
n_ge2 = sum(1 for r in Rmatch.values() if r >= 2.0)
print(f"R>=2.0 in matching regime: {n_ge2}/{len(Rmatch)} ({n_ge2/len(Rmatch)*100:.1f}% >=75% needed)")

print("\n== K2 accuracy gate: any cell D1 < A2 - 0.05?")
k2bad = [c for c in cellnames if med[(c, 'trained')]['acc'] < med[(c, 'auto')]['acc'] - 0.05]
print("violations:", k2bad if k2bad else "none")

print("\n== K4 mechanism attribution: W_gap = W(auto)-W(trained), family = scan_steps + overwrite-churn ==")
print("   overwrite-churn approx: (auto.add+auto.kill+auto.overwrite+auto.evict) - (trained.add+trained.kill+trained.overwrite+trained.evict)")
print(f"{'cell':<14}{'W_gap':>10}{'scan_gap':>10}{'churn_gap':>10}{'fam_gap':>10}{'frac':>7}")
fracs = []
for c in cellnames:
    t, a = med[(c, 'trained')], med[(c, 'auto')]
    gap = a['W'] - t['W']
    scan_gap = a['scan_steps'] - t['scan_steps']
    churn_gap = (a['add'] + a['kill'] + a['overwrite'] + a['evict']) - (t['add'] + t['kill'] + t['overwrite'] + t['evict'])
    fam = scan_gap + churn_gap
    frac = fam / gap if gap else 0
    fracs.append(frac)
    print(f"{c:<14}{gap:>10.0f}{scan_gap:>10.0f}{churn_gap:>10.0f}{fam:>10.0f}{frac:>7.3f}")
print(f"median attribution fraction = {statistics.median(fracs):.3f}")

print("\n== naive-arm damage: collateral true-kills total across cells (median per cell); naive-vs-trained acc gaps")
tot_coll = sum(med[(c, 'naive')]['collateral'] for c in cellnames)
print(f"total naive collateral (sum of medians) = {tot_coll:.0f}")
print(f"{'cell':<14}{'coll_naive':>11}{'acc_gap(tr-naive)':>16}{'W_naive/W_tr':>12}")
for c in cellnames:
    n_, t = med[(c, 'naive')], med[(c, 'trained')]
    print(f"{c:<14}{n_['collateral']:>11.0f}{(t['acc']-n_['acc']):>16.3f}{(n_['W']/t['W']):>12.2f}")

print("\n== wall-vs-W: median wall_ep(auto)/wall_ep(trained) vs R")
wr = {c: med[(c, 'auto')]['wall_ep'] / med[(c, 'trained')]['wall_ep'] for c in cellnames}
for c in cellnames:
    print(f"{c:<14} wall_ratio={wr[c]:>7.2f}  W_ratio={R[c]:>7.2f}")
print(f"median wall_ratio = {statistics.median(wr.values()):.2f}")

print("\n== suppressions (trained) vs installations by arm")
for c in cellnames:
    t, a = med[(c, 'trained')], med[(c, 'auto')]
    print(f"{c:<14} tr: suppress={t['suppress']:.0f} add={t['add']:.0f} kill={t['kill']:.0f} | "
          f"auto: add={a['add']:.0f} kill={a['kill']:.0f} overwrite={a['overwrite']:.0f} evict={a['evict']:.0f} scan={a['scan_steps']:.0f}")

print("\n== memory: arena/ledger bytes (median, max arm per cell)")
for c in cellnames:
    mx_a = max(med[(c, x)]['arena_bytes'] for x in ('trained', 'naive', 'auto'))
    mx_l = max(med[(c, x)]['ledger_bytes'] for x in ('trained', 'naive', 'auto'))
    print(f"{c:<14} arena={mx_a:.0f} ledger={mx_l:.0f}")
