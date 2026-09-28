#!/usr/bin/env python3
"""O1 leg scorer: asserts the frozen gate trace produced EXACTLY the
prereg-predicted metrics on the three synthetic cases (the construction is
the test of the bar), then applies the REPAIRED O1 bar:
  KILL iff (K2' not within 2pp of K1) OR (K2' within 2pp AND RK-3' - RK-3 < 3pp).
Any deviation fails loud (exit 1)."""
import sys

def read(path):
    d = {}
    for line in open(path):
        line = line.strip()
        if '=' in line:
            k, v = line.split('=', 1)
            d[k] = v
    return d

def frac(num, den):
    return 100.0 * num / den

# (case, mode) -> predicted (trials, k1n,k1d, k2n,k2d, rk3n,rk3d, repaired)
PRED = {
    ('real', 0): (200, 190,200, 140,200, 20,200, 0),
    ('real', 1): (200, 190,200, 190,200, 32,200, 50),
    ('sham', 0): (200, 190,200, 140,200, 20,200, 0),
    ('sham', 1): (200, 190,200, 190,200, 20,200, 50),
    ('null', 0): (200, 190,200, 140,200, 20,200, 0),
    ('null', 1): (200, 190,200, 140,200, 20,200, 0),
}
# existing-evidence fidelity (committed round2 evidence, §4.1)
PRED_FID = {
    0: (11840, 1062,1102, 824,1102, 104,1102, 0),
    1: (11840, 1062,1102, 954,1102, 106,1102, 130),
}

fails = []
def check(label, path, pred):
    d = read(path)
    got = (int(d['trials']), int(d['k1_num']), int(d['k1_den']),
           int(d['k2_num']), int(d['k2_den']),
           int(d['rk3_num']), int(d['rk3_den']), int(d['repaired']))
    if got != pred:
        fails.append(f"{label}: got {got} want {pred}")
        return None
    return d

results = {}
for case in ['real', 'sham', 'null']:
    for m in [0, 1]:
        d = check(f"{case} m{m}", f"runs/{case}_m{m}_run0.txt", PRED[(case, m)])
        if d: results[(case, m)] = d
for m in [0, 1]:
    d = check(f"fidelity m{m}", f"runs/fidelity_m{m}_run0.txt", PRED_FID[m])
    if d: results[('fid', m)] = d

def bar(label, d0, d1):
    k1 = frac(int(d1['k1_num']), int(d1['k1_den']))          # K1 (mode1 == mode0 by construction)
    k2p = frac(int(d1['k2_num']), int(d1['k2_den']))         # K2'
    rk3 = frac(int(d0['rk3_num']), int(d0['rk3_den']))       # RK-3 (mode 0)
    rk3p = frac(int(d1['rk3_num']), int(d1['rk3_den']))      # RK-3'
    gap = k1 - k2p                                          # pp short of K1
    rise = rk3p - rk3                                       # pp rise
    closed = gap <= 2.0 + 1e-9
    if not closed:
        v = 'KILL-clause1'
    elif rise < 3.0 - 1e-9:
        v = 'KILL-clause2'
    else:
        v = 'SURVIVE'
    print(f"{label:8} K1={k1:6.2f}% K2'={k2p:6.2f}% gap={gap:5.2f}pp "
          f"RK3={rk3:5.2f}% RK3'={rk3p:5.2f}% rise={rise:+5.2f}pp -> {v}")
    return v, gap, rise

print("== repaired-bar verdicts ==")
v_real, g_real, r_real = bar('real', results[('real', 0)], results[('real', 1)])
v_sham, g_sham, r_sham = bar('sham', results[('sham', 0)], results[('sham', 1)])
v_null, g_null, r_null = bar('null', results[('null', 0)], results[('null', 1)])
v_fid, g_fid, r_fid = bar('fid-4.1', results[('fid', 0)], results[('fid', 1)])

# original-bar comparison on the real case: old rule killed if
# (RK3' - RK3) < (K2'-K2)/2 i.e. rise < half the closed gap
d0, d1 = results[('real', 0)], results[('real', 1)]
closed_gap = frac(int(d1['k2_num']), int(d1['k2_den'])) - frac(int(d0['k2_num']), int(d0['k2_den']))
orig = 'KILL' if r_real < closed_gap / 2 else 'SURVIVE'
print(f"real under ORIGINAL bar: closed_gap={closed_gap:.2f}pp, rise={r_real:+.2f}pp "
      f"< half-gap={closed_gap/2:.2f}pp -> {orig} (demonstrates the FATAL defect)")

exp = {'real': 'SURVIVE', 'sham': 'KILL-clause2', 'null': 'KILL-clause1', 'fid-4.1': 'KILL-clause1'}
got = {'real': v_real, 'sham': v_sham, 'null': v_null, 'fid-4.1': v_fid}
for k in exp:
    if got[k] != exp[k]:
        fails.append(f"bar verdict {k}: got {got[k]} want {exp[k]}")

if fails:
    print("FAILURES:")
    for f in fails:
        print("  " + f)
    sys.exit(1)
print("ALL ASSERTIONS PASS")
