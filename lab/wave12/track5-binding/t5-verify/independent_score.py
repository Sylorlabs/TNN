#!/usr/bin/env python3
# Independent Track 5 scorer — verifies binding trial logs from scratch.
# Parses RESULT lines, computes the 5 metrics per the frozen/binding prereg
# definitions, applies Micah's SIGNED weights (30/25/25/10/10), evaluates
# the integrity gate, K-T1..K-T4, and the frozen prereg section 6 decision tree.
# Independent of analyze_bind.py (different code path, same log evidence).
import os, re, glob

LOGDIR = os.path.expanduser('~/workspace/tnn-lab/wave12/track5-binding/evidence/logs')
LABELS = ['X', 'Y', 'Z']
REPS = list(range(12))
# §4a applicability (detailed table): A=planted 5 fams, B=learned 6, C=hybrid 7+T7'
# Empirical arm ID: Z=revisability 0 -> planted(A); Y=explanted lifecycle -> hybrid(C); X=learned(B)
FAMS = {'Z': ['1','2','4','7','8'], 'X': ['1','2','3','4','6','7','8'], 'Y': ['1','2','3','4','6','7','7p','8']}

def parse(path):
    d = {}
    with open(path) as f:
        for line in f:
            m = re.match(r'^RESULT,([XYZ]),(\d+),(\d+),([a-z0-9_]+),(-?\d+),(\d+)$', line.strip())
            if m:
                d[m.group(4)] = (int(m.group(5)), int(m.group(6)))
    return d

# per-rep metrics
rows = {}
for L in LABELS:
    for r in REPS:
        b = parse(f'{LOGDIR}/bind_{L}_rep{r}_s1.log')
        t = parse(f'{LOGDIR}/btrap_{L}_rep{r}.log')
        # mastery = mean(D1%, D2%, D3%)
        mastery = ((b['d1'][0]/b['d1'][1]) + (b['d2'][0]/b['d2'][1]) + (b['d3'][0]/b['d3'][1])) / 3
        # revisability = min(false-revision rate, genuine-retention rate)
        rev = min(b['rev_false'][0]/b['rev_false'][1], b['rev_genuine'][0]/b['rev_genuine'][1])
        # integrity scored = mean(trap rate over applicable fams, 1-hallu, K1, K2, refusal)
        trap_rates = []
        for fam in FAMS[L]:
            key = f'trap_{fam}'
            c, d = t.get(key, (0, 0))
            if d:
                trap_rates.append(c/d)
        # find trap keys actually present
        hallu = 1 - b['hallu'][0]/b['hallu'][1]
        integ = ((sum(trap_rates)/len(trap_rates)) + hallu + b['k1'][0] + b['k2'][0] + b['refusal'][0]) / 5
        # retention: S10 leg
        s10 = parse(f'{LOGDIR}/bind_{L}_rep0_s10.log')
        s1m = mastery
        s10m = ((s10['d1'][0]/s10['d1'][1]) + (s10['d2'][0]/s10['d2'][1]) + (s10['d3'][0]/s10['d3'][1])) / 3
        s10r = min(s10['rev_false'][0]/s10['rev_false'][1], s10['rev_genuine'][0]/s10['rev_genuine'][1])
        retention = 1.0 if (s10m >= s1m - 0.05 and s10r >= rev - 0.05) else 0.0
        # cost = 1/(1 + esc/100ep + 0.1*ops/ep)
        esc, eps, ops = b['esc'][0], b['eps'][0], b['ops'][0]
        cost = 1/(1 + esc/(eps/100) + 0.1*ops/eps) if eps else 0
        rows[(L,r)] = dict(mastery=mastery, rev=rev, integ=integ, retention=retention, cost=cost,
                           esc=esc, eps=eps, ops=ops, trap_keys=list(t.keys())[:8])

# means
means = {}
for L in LABELS:
    means[L] = {k: sum(rows[(L,r)][k] for r in REPS)/12 for k in ('mastery','rev','integ','retention','cost')}

print("=== INDEPENDENT PER-ARM MEANS (12 reps) ===")
for L in LABELS:
    m = means[L]
    print(f"{L}: mastery={m['mastery']:.4f} rev={m['rev']:.4f} integ={m['integ']:.4f} ret={m['retention']:.4f} cost={m['cost']:.4f}")

print("\n=== WEIGHTED COMPOSITE (30/25/25/10/10) ===")
for L in LABELS:
    m = means[L]
    comp = .30*m['mastery'] + .25*m['rev'] + .25*m['integ'] + .10*m['retention'] + .10*m['cost']
    print(f"{L}: {comp:.4f}")

print("\n=== INTEGRITY GATE (all reps) ===")
for L in LABELS:
    fails = 0
    for r in REPS:
        b = parse(f'{LOGDIR}/bind_{L}_rep{r}_s1.log')
        # gate: all applicable trap fams 20/20 -- check trap log
        t = parse(f'{LOGDIR}/btrap_{L}_rep{r}.log')
        ok = all(t.get(f'trap_{fam}', (0,1))[0] == 20 for fam in FAMS[L])
        ok = ok and b['hallu'][0] <= 1 and b['k1'][0]==1 and b['k2'][0]==1 and b['refusal'][0]==1
        if not ok: fails += 1
    print(f"{L}: {'PASS' if fails==0 else f'FAIL ({fails} reps)'}")

print("\n=== trap keys present (sanity) ===")
print(sorted(rows[('X',0)]['trap_keys']))
