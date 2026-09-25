#!/usr/bin/env python3
"""Independent Python replica of train_f33.zag (exact integer rules).

Replicates the single-pass training to verify the Zag implementation, and
provides the moment-recompute used by falsifiers (a) and (b) on eval data.
"""
import csv, sys

def tdiv(a, b):
    # truncation toward zero, b > 0
    assert b > 0
    if a >= 0: return a // b
    return -((-a) // b)

def rho(k, n): return (k + 1) * 1000 // (n + 2)
def clamp(v, lo, hi): return max(lo, min(hi, v))
def dslot(d): return {1:0, 2:1, 4:2, 8:3, 16:4, 32:5, 64:6}.get(d, -1)

def newdelta(nstay, sstay, nall, sall, kstay, kall):
    if nstay == 0 or nall == 0: return 0
    e = tdiv(sstay, nstay) - tdiv(sall, nall)
    da = tdiv(kstay * 1000, nstay) - tdiv(kall * 1000, nall)
    return clamp(da - e - 3, -40, 40)

def train(path):
    led_n = [0]*20; led_k = [0]*20
    S = {k: [0]*(20*7) for k in ('nstay','sstay','nall','sall','kstay','kall')}
    delta = [[0]*7 for _ in range(20)]
    items = {}  # id -> dict(key,cstar,f81,relp,cp,yp)
    nrel = 0
    with open(path) as f:
        for row in csv.reader(f, delimiter='\t'):
            if not row or row[0].startswith('#'): continue
            iid, fam, ho = row[0], row[1], int(row[2])
            if ho == 1: continue
            depth = int(row[3]); ds = dslot(depth)
            assert ds >= 0
            rel = int(row[5])
            y = 1 if (rel == 1 and row[6] == '1') else 0
            f1, f3, f6, f8 = int(row[7]), int(row[9]), int(row[12]), int(row[14])
            if ds == 0:
                m = min(4, f1//200); s = min(3, f6//250); key = m*4+s
                cstar = rho(led_k[key], led_n[key])
                C = cstar
                if rel == 1:
                    nrel += 1
                    led_n[key] += 1; led_k[key] += y
                items[iid] = dict(key=key, cstar=cstar, f81=f8,
                                  relp=rel, cp=C, yp=y)
            else:
                st = items[iid]
                key, cstar, f81 = st['key'], st['cstar'], st['f81']
                relp, cp, yp = st['relp'], st['cp'], st['yp']
                if relp == 1:
                    S['nall'][key*7+ds] if False else None
                    i = key*7+ds
                    S['nall'][i] += 1; S['sall'][i] += cp; S['kall'][i] += yp
                    if rel == 1:
                        S['nstay'][i] += 1; S['sstay'][i] += cp; S['kstay'][i] += yp
                    delta[key][ds] = newdelta(S['nstay'][i], S['sstay'][i],
                                             S['nall'][i], S['sall'][i],
                                             S['kstay'][i], S['kall'][i])
                C = 0; pi = 0
                if rel == 1:
                    flip = 50 if f3 > 0 else 0
                    trauma = max(0, f8 - f81)//8
                    pi = min(400, flip + trauma)
                    cum = sum(delta[key][j] for j in range(1, ds+1))
                    C = clamp(cstar + cum - pi, 1, 999)
                    nrel += 1
                st['relp'] = rel; st['cp'] = C; st['yp'] = y
    cstars = [rho(led_k[k], led_n[k]) for k in range(20)]
    return dict(led_n=led_n, led_k=led_k, delta=delta, cstars=cstars,
                S=S, nrel=nrel, items=items)

def main():
    r = train(sys.argv[1])
    print("nrel =", r['nrel'])
    for key in range(20):
        print(f"key {key} n={r['led_n'][key]} k={r['led_k'][key]} "
              f"cstar={r['cstars'][key]} delta={r['delta'][key][1:]} "
              f"nall={[r['S']['nall'][key*7+j] for j in range(1,7)]}")

if __name__ == '__main__':
    main()
