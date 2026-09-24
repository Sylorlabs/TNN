#!/usr/bin/env python3
# score.py — score an F2 battery run against .truth sidecars + ref_f1 baseline.
# Usage: score.py <rundir>
import os, re, subprocess, sys, struct

rundir = sys.argv[1]
fxdir = os.path.expanduser('~/workspace/conscious_perception/fixtures')
ref = os.path.expanduser('~/workspace/conscious_perception/forks/autopilot/gen/ref_f1.py')

def kv_parse(path):
    d = {}
    for tok in open(path).read().strip().split(','):
        if '=' in tok:
            k, v = tok.split('=', 1)
            d[k] = v
    return d

def truth_of(fixture_path):
    t = {}
    for line in open(fixture_path + '.truth'):
        line = line.strip()
        if '=' in line and not line.startswith('#'):
            k, v = line.split('=', 1)
            t[k.strip()] = v.strip()
    return t.get('truth', '?')

# F1 baseline via ref_f1.py
fixtures = sorted(f for f in os.listdir(rundir) if f.endswith('.verdict'))
f1res = {}
paths = [os.path.join(fxdir, 'test', f[:-8]) if os.path.exists(os.path.join(fxdir, 'test', f[:-8]))
         else os.path.join(fxdir, 'train', f[:-8]) for f in fixtures]
# map verdict name -> real fixture path (test/ or train/)
real = {}
for f in fixtures:
    base = f[:-8]
    for sub in ('test', 'train'):
        for cat in ('omission', 'ambiguity', 'redteam', 'illusion', 'inattentional'):
            p = os.path.join(fxdir, sub, cat, base)
            if os.path.exists(p):
                real[f] = p
out = subprocess.run(['python3', ref] + [real[f] for f in fixtures],
                     capture_output=True, text=True).stdout
for line in out.splitlines():
    m = re.match(r'RESULT fixture=(\S+) task=(\S+) percept=(\S+) conf=(\d+) ops=(\d+)', line)
    if m:
        f1res[os.path.basename(m.group(1))] = (m.group(3), int(m.group(4)), int(m.group(5)))

print(f"{'fixture':22} {'truth':12} {'F1':10} {'F2':10} {'auth':11} {'ops':>7} {'note'}")
recov = finstall = f1ok = f2ok = prov = capture = 0
ops_tot = 0
for f in fixtures:
    base = f[:-8]
    v = kv_parse(os.path.join(rundir, f))
    truth = truth_of(real[f])
    f1p, f1c, f1o = f1res.get(base, ('?', 0, 0))
    f2p, auth, ops = v.get('final', '?'), v.get('authority', '?'), int(v.get('ops_total', 0))
    ops_tot += ops
    f1_hit = (f1p == truth); f2_hit = (f2p == truth)
    f1ok += f1_hit; f2ok += f2_hit
    note = ''
    if not f1_hit and f2_hit:
        recov += 1; note = 'RECOVERED'
    if f2_hit and auth == 'provisional':
        prov += 1
    if not f2_hit:
        finstall += 1; note = ('FALSE-INSTALL' + ('(prov)' if auth == 'provisional' else '(DIRECT!)'))
    if v.get('budget_hit') == '1':
        capture += 1; note += ' CAPTURE'
    print(f"{base:22} {truth:12} {f1p:10} {f2p:10} {auth:11} {ops:7} {note}")
print()
print(f"n={len(fixtures)} F1_correct={f1ok} F2_correct={f2ok} recovered(F1miss->F2hit)={recov} "
      f"F2_false_install={finstall} provisional_hits={prov} capture_events={capture} total_ops={ops_tot}")
