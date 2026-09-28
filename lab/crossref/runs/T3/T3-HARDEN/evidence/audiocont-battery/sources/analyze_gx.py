#!/usr/bin/env python3
"""grok46 G1/G2/G3 machine tests.
G1: oceanwf boundary floors (200-800 Hz, 10 ms RMS) vs kids median 0.0418.
G2: long180 boundary floors (0-1 kHz, 1 ms) vs B-alpha v2 5th-pct control floor.
G3: kids full vs ablation at 5 bridge midpoints: 125 ms correlation + 10 ms
    floors vs B-alpha v2 5th-pct (10 ms RMS full-band) control floor.
Per PREREG_ROUND2.md."""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analyze_common import read_wav, env_1ms, rms_10ms, bandpass

W = "/home/hatch/workspace/tnn-lab/imagination_discovery/aud/continuity_round2/work/renders"
SR = 44100
BAV2 = "/home/hatch/workspace/tnn-lab/imagination_discovery/aud/b_alpha/clips/b_alpha_kids_v2.wav"
KIDS_MED = 0.0418

def floor_10ms(x, t, band=None):
    if band:
        x = bandpass(x, *band)
    r = rms_10ms(x)
    i0 = max(0, int((t - 0.25) * 100)); i1 = int((t + 0.25) * 100)
    return float(r[i0:i1].min())

def floor_1ms(x, t, band=None):
    if band:
        x = bandpass(x, *band)
    e = env_1ms(x)
    i0 = max(0, int((t - 0.25) * 1000)); i1 = int((t + 0.25) * 1000)
    return float(e[i0:i1].min())

def g1():
    print("== G1: oceanwf world-bed uniformity ==")
    edges = [0.0, 2.4, 10.8, 26.8]
    ratios = []
    for r in (1, 2, 3):
        p = f"{W}/g1/g1_oceanwf_r{r}.wav"
        if not os.path.exists(p):
            print(f"  MISSING {p}"); continue
        x = read_wav(p)
        fl = [floor_10ms(x, t, (200, 800)) for t in edges]
        ra = [f / KIDS_MED for f in fl]
        ratios.extend(ra)
        print(f"  run{r}: floors={[f'{f:.4f}' for f in fl]} ratios={[f'{v:.2f}' for v in ra]}")
    if not ratios:
        print("  no renders"); return
    mn = min(ratios)
    if mn < 2.4:
        v = "SURVIVES"
    elif all(r >= 3.0 for r in ratios):
        v = "KILLED"
    else:
        v = "INDETERMINATE"
    print(f"  min ratio {mn:.2f} -> machine verdict: {v}")

def g2():
    print("== G2: long180 scoring drift ==")
    xb = read_wav(BAV2)
    ctrl_floor = float(np.percentile(env_1ms(bandpass(xb, 0, 1000)), 5))
    print(f"  B-alpha v2 control floor (0-1kHz 1ms, 5th pct): {ctrl_floor:.5f}")
    edges = [30, 45, 60, 90, 120, 135, 150]
    ratios = []
    for r in (1, 2, 3):
        p = f"{W}/g2/g2_long180_r{r}.wav"
        if not os.path.exists(p):
            print(f"  MISSING {p}"); continue
        x = read_wav(p)
        fl = [floor_1ms(x, t, (0, 1000)) for t in edges]
        ra = [f / ctrl_floor for f in fl]
        ratios.extend(ra)
        print(f"  run{r}: floors={[f'{f:.4f}' for f in fl]} ratios={[f'{v:.2f}' for v in ra]}")
    if not ratios:
        print("  no renders"); return
    mn = min(ratios)
    if mn < 2.7:
        v = "SURVIVES"
    elif all(r >= 3.0 for r in ratios):
        v = "KILLED"
    else:
        v = "INDETERMINATE"
    print(f"  min ratio {mn:.2f} -> machine verdict: {v}")

def g3():
    print("== G3: bridge authoring seams under density stress ==")
    mids = [1.2, 9.8, 15.4, 19.85, 25.8]
    xb = read_wav(BAV2)
    ctrl_floor = float(np.percentile(rms_10ms(xb), 5))
    print(f"  B-alpha v2 control floor (10ms RMS full-band, 5th pct): {ctrl_floor:.5f}")
    corrs = []; full_r = []; abl_r = []
    for r in (1, 2, 3):
        pf = f"{W}/g3/g3_kids_b0_r{r}.wav"; pa = f"{W}/g3/g3_kids_b2_r{r}.wav"
        if not (os.path.exists(pf) and os.path.exists(pa)):
            print(f"  MISSING run{r}"); continue
        xf, xa = read_wav(pf), read_wav(pa)
        n = int(0.125 * SR)
        for t in mids:
            i0 = int(t * SR)
            s1 = xf[i0:i0 + n]; s2 = xa[i0:i0 + n]
            c = float(np.corrcoef(s1, s2)[0, 1]) if s1.std() and s2.std() else 0.0
            corrs.append(c)
        ff = [floor_10ms(xf, t) for t in mids]
        af = [floor_10ms(xa, t) for t in mids]
        full_r.extend(f / ctrl_floor for f in ff)
        abl_r.extend(f / ctrl_floor for f in af)
        print(f"  run{r}: corr={[f'{c:.3f}' for c in corrs[-5:]]}")
        print(f"         full floors={[f'{f:.4f}' for f in ff]} ratios={[f'{v:.2f}' for v in full_r[-5:]]}")
        print(f"         abl  floors={[f'{f:.4f}' for f in af]} ratios={[f'{v:.2f}' for v in abl_r[-5:]]}")
    if not corrs:
        print("  no renders"); return
    mc = float(np.median(corrs))
    print(f"  median 125ms correlation: {mc:.3f}")
    cond_surv_a = (mc >= 0.90 and all(v >= 3.0 for v in abl_r))
    cond_surv_b = any(v < 2.5 for v in full_r)
    cond_kill = (mc < 0.88 and all(v >= 3.0 for v in full_r)
                 and any(v < 2.5 for v in abl_r))
    if cond_surv_a or cond_surv_b:
        v = "SURVIVES"
    elif cond_kill:
        v = "KILLED"
    else:
        v = "INDETERMINATE"
    print(f"  survive-A(corr>=.90 & abl>=3x): {cond_surv_a}; "
          f"survive-B(any full<2.5x): {cond_surv_b}; kill-cond: {cond_kill}")
    print(f"  machine verdict: {v}")

if __name__ == '__main__':
    g1(); print()
    g2(); print()
    g3()
