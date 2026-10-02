#!/usr/bin/env python3
"""sol-H1 machine test: 10 ms envelope dips under sparse/dense conditions.
Per PREREG_ROUND2.md: 1 ms rectified envelope; per-10 ms windows (min1, rms10);
classes from the deterministic placement log; F = 5th pct of within-phrase
rms10 per render; dip = min1 < F."""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analyze_common import read_wav, env_1ms, rms_10ms, sign_test_greater

R = "/home/hatch/workspace/tnn-lab/imagination_discovery/aud/continuity_round2/work/renders/h1"
BOUNDARIES = [5.0, 13.0, 15.0, 26.0]
BW = 0.25  # +-250 ms boundary half-width

def load_log(path):
    ev = []  # (start_ms, end_ms, target)
    with open(path) as f:
        for line in f:
            p = line.split()
            if len(p) < 7:
                continue
            dst = int(p[0]); s1 = int(p[3]); tgt = int(p[5])
            ev.append((dst, s1, tgt))
    return ev

def classify(nwin, events):
    """0=within, 1=boundary, 2=overlap."""
    cls = np.zeros(nwin, dtype=np.int8)
    fg = [(s, e) for s, e, t in events if t > 2500]
    for w in range(nwin):
        tc = (w + 0.5) * 0.01
        if any(abs(tc - b) <= BW for b in BOUNDARIES):
            cls[w] = 1
            continue
        nact = sum(1 for s, e in fg if s / 1000.0 <= tc < e / 1000.0)
        if nact >= 2:
            cls[w] = 2
    return cls

def analyze_one(wavpath, logpath):
    x = read_wav(wavpath)
    e1 = env_1ms(x)          # per 1 ms
    r10 = rms_10ms(x)        # per 10 ms
    nwin = len(r10)
    e1 = e1[:nwin * 10]
    assert len(e1) == nwin * 10, (len(e1), nwin)
    min1 = e1.reshape(nwin, 10).min(axis=1)
    events = load_log(logpath)
    cls = classify(nwin, events)
    wth = cls == 0
    F = np.percentile(r10[wth], 5)
    dip = min1 < F
    rates = {}
    counts = {}
    for c, name in ((0, 'within'), (1, 'boundary'), (2, 'overlap')):
        m = cls == c
        counts[name] = int(m.sum())
        rates[name] = dip[m].sum() / m.sum() * 6000 / 60 if m.sum() else 0.0
    # dip durations: run lengths of consecutive dip windows (x10 ms)
    maxrun = 0; run = 0
    for d in dip:
        if d:
            run += 1; maxrun = max(maxrun, run)
        else:
            run = 0
    return {'F': F, 'rates': rates, 'counts': counts,
            'maxrun_win': maxrun, 'ndip': int(dip.sum())}

def main():
    rows = []
    for k in range(20):
        for m, mname in ((0, 'normal'), (1, 'permuted'), (2, 'bedonly')):
            w = f"{R}/h1_k{k}_m{m}.wav"; lg = f"{R}/h1_k{k}_m{m}.log"
            if not (os.path.exists(w) and os.path.exists(lg)):
                print(f"MISSING k{k} m{m}"); continue
            r = analyze_one(w, lg)
            r.update(k=k, mode=mname)
            rows.append(r)
            print(f"k={k:2d} {mname:8s} F={r['F']:.5f} "
                  f"within={r['rates']['within']:.1f}/min(n={r['counts']['within']}) "
                  f"bnd={r['rates']['boundary']:.1f}/min(n={r['counts']['boundary']}) "
                  f"ovl={r['rates']['overlap']:.1f}/min(n={r['counts']['overlap']}) "
                  f"maxrun={r['maxrun_win']*10}ms ndip={r['ndip']}", flush=True)
    # kill criteria
    for mname in ('normal', 'permuted'):
        sub = [r for r in rows if r['mode'] == mname]
        db = [r['rates']['boundary'] - r['rates']['within'] for r in sub]
        do = [r['rates']['overlap'] - r['rates']['within'] for r in sub]
        kb, nb, pb = sign_test_greater(db)
        ko, no, po = sign_test_greater(do)
        med = lambda kk: float(np.median([r['rates'][kk] for r in sub]))
        maxrun = max(r['maxrun_win'] for r in sub)
        medok = med('boundary') <= med('within') and med('overlap') <= med('within')
        print(f"\n== {mname}: n={len(sub)} ==")
        print(f"  median within={med('within'):.2f} boundary={med('boundary'):.2f} overlap={med('overlap'):.2f} dips/min")
        print(f"  median inequalities (bnd<=wth, ovl<=wth): {medok}")
        print(f"  sign test boundary>within: {kb}/{nb} p={pb:.4f} (kill needs p>=0.05 i.e. NOT signif)")
        print(f"  sign test overlap>within:   {ko}/{no} p={po:.4f}")
        print(f"  max dip run: {maxrun*10} ms (kill needs <=10 ms)")
        kill = (medok and pb >= 0.05 and po >= 0.05 and maxrun <= 1)
        print(f"  machine verdict: {'KILLED' if kill else 'SURVIVES'}")
    # bedonly descriptive
    sub = [r for r in rows if r['mode'] == 'bedonly']
    if sub:
        med = lambda kk: float(np.median([r['rates'][kk] for r in sub]))
        print(f"\n== bedonly (descriptive): median within={med('within'):.2f} "
              f"boundary={med('boundary'):.2f} overlap={med('overlap'):.2f}")

if __name__ == '__main__':
    main()
