#!/usr/bin/env python3
"""sol-H2 machine test: bridge_world seams via source/room/texture discontinuity.
Per PREREG_ROUND2.md: 4 measures at the 10 nominal bridge edges per scene
(30 scenes x 2 conditions), vs 1:1 RMS-matched ordinary transitions from the
placement log. One-sided Mann-Whitney U (bridge > ordinary), alpha=0.05."""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analyze_common import (read_wav, env_1ms, stft_logmag, spectral_flux,
                            mann_whitney_u_greater)

R = "/home/hatch/workspace/tnn-lab/imagination_discovery/aud/continuity_round2/work/renders/h2"
SR = 44100
BRIDGES = [(0.0, 2.4), (8.8, 10.8), (14.4, 16.4), (18.3, 21.4), (24.8, 26.8)]
EDGES = sorted({e for b in BRIDGES for e in b})  # 10 edges

def load_onsets(path):
    ts = []
    with open(path) as f:
        for line in f:
            p = line.split()
            if len(p) < 3:
                continue
            ts.append(int(p[0]) / SR)
    return np.array(ts)

def local_rms_db(x, t, win=0.5):
    i0 = max(0, int((t - win / 2) * SR)); i1 = int((t + win / 2) * SR)
    seg = x[i0:i1]
    r = np.sqrt((seg ** 2).mean()) if len(seg) else 0.0
    return 20 * np.log10(r + 1e-12)

def measure(edge_t, x, S, flux):
    """Return dict of 4 measures at edge_t (seconds). None where undefined."""
    out = {}
    # 1. 1 ms amplitude slope: max |d(env)/dt| in +-50 ms
    i0 = max(0, int((edge_t - 0.05) * 1000)); i1 = int((edge_t + 0.05) * 1000)
    e = env_1ms(x)
    seg = e[i0:i1]
    out['slope'] = float(np.abs(np.diff(seg)).max()) if len(seg) > 1 else 0.0
    # 2. spectral flux peak in +-200 ms (frame centers)
    hop = 0.010
    f0 = int(np.ceil((edge_t - 0.2 - 0.023) / hop)); f1 = int((edge_t + 0.2 - 0.023) / hop)
    f0 = max(0, f0); f1 = min(len(flux) - 1, f1)
    out['flux'] = float(flux[f0:f1 + 1].max()) if f1 >= f0 else 0.0
    # 3 & 4 need both flanks
    if edge_t >= 0.05:
        pre = S[int((edge_t - 0.05 - 0.023) / hop):int((edge_t - 0.023) / hop)]
        post = S[int((edge_t - 0.023) / hop):int((edge_t + 0.05 - 0.023) / hop)]
        if len(pre) and len(post):
            out['specdist50'] = float(np.sqrt(((pre.mean(0) - post.mean(0)) ** 2).sum()))
        else:
            out['specdist50'] = None
    else:
        out['specdist50'] = None
    if edge_t >= 1.0 and edge_t + 1.0 <= len(x) / SR:
        out['modchange'] = modchange(x, edge_t)
    else:
        out['modchange'] = None
    return out

def modchange(x, t):
    """|Delta| of 2-20 Hz modulation-spectrum centroid of the 1 s flanks."""
    def centroid(t0):
        seg = x[int(t0 * SR):int((t0 + 1.0) * SR)]
        n1 = SR // 100
        m = len(seg) // n1
        env = np.abs(seg[:m * n1].reshape(m, n1)).mean(axis=1)
        env = env - env.mean()
        M = np.abs(np.fft.rfft(env))
        fr = np.fft.rfftfreq(len(env), 0.01)
        sel = (fr >= 2) & (fr <= 20)
        if M[sel].sum() <= 0:
            return 0.0
        return float((fr[sel] * M[sel]).sum() / M[sel].sum())
    return abs(centroid(t - 1.0) - centroid(t))

def match_ordinary(edge_ts, edge_rms, onsets, x):
    """Greedy 1:1 match of ordinary onsets to edges by local 500 ms RMS (+-1 dB).
    Returns list of (edge_idx, onset_t) matches."""
    cands = [t for t in onsets if all(abs(t - e) > 0.25 for e in EDGES)]
    cand_rms = [local_rms_db(x, t) for t in cands]
    used = set(); matches = []
    for ei, (et, er) in enumerate(zip(edge_ts, edge_rms)):
        best = None; bestd = 1.0
        for ci, (ct, cr) in enumerate(zip(cands, cand_rms)):
            if ci in used:
                continue
            d = abs(cr - er)
            if d <= 1.0 and d < bestd:
                bestd = d; best = ci
        if best is not None:
            used.add(best); matches.append((ei, cands[best]))
    return matches

def main():
    meas_names = ['slope', 'flux', 'specdist50', 'modchange']
    bridge = {m: [] for m in meas_names}   # standard-condition edges
    ordin = {m: [] for m in meas_names}    # matched ordinary transitions
    ctrl = {m: [] for m in meas_names}     # control-condition nominal edges
    n_match = 0; n_edge = 0
    for s in range(1, 31):
        w0 = f"{R}/h2_s{s}_b0.wav"; l0 = f"{R}/h2_s{s}_b0.log"
        w1 = f"{R}/h2_s{s}_b1.wav"
        if not (os.path.exists(w0) and os.path.exists(l0) and os.path.exists(w1)):
            print(f"MISSING scene {s}", flush=True); continue
        x0 = read_wav(w0); x1 = read_wav(w1)
        S0 = stft_logmag(x0); F0 = spectral_flux(S0)
        S1 = stft_logmag(x1); F1 = spectral_flux(S1)
        onsets = load_onsets(l0)
        edge_rms = [local_rms_db(x0, t) for t in EDGES]
        matches = match_ordinary(EDGES, edge_rms, onsets, x0)
        n_match += len(matches); n_edge += len(EDGES)
        mb = {e: measure(t, x0, S0, F0) for e, t in enumerate(EDGES)}
        mc = {e: measure(t, x1, S1, F1) for e, t in enumerate(EDGES)}
        for m in meas_names:
            for e in range(len(EDGES)):
                if mb[e][m] is not None:
                    bridge[m].append(mb[e][m])
                if mc[e][m] is not None:
                    ctrl[m].append(mc[e][m])
        mo = {}
        for ei, ot in matches:
            mo[(ei, ot)] = measure(ot, x0, S0, F0)
        for m in meas_names:
            for v in mo.values():
                if v[m] is not None:
                    ordin[m].append(v[m])
        print(f"scene {s}: matched {len(matches)}/{len(EDGES)}", flush=True)
    print(f"\ntotal matched {n_match}/{n_edge}")
    print("\nmeasure      n_br  n_ord  med_br   med_ord  U        z      p(one-sided)")
    verdicts = {}
    for m in meas_names:
        b = np.array(bridge[m]); o = np.array(ordin[m])
        U, z, p = mann_whitney_u_greater(b, o)
        medb, medo = np.median(b), np.median(o)
        sig = p < 0.05
        verdicts[m] = (sig, medb <= medo)
        print(f"{m:10s} {len(b):5d} {len(o):5d} {medb:8.4f} {medo:8.4f} "
              f"{U:8.1f} {z:6.2f} {p:.4f} {'SIGNIFICANT' if sig else 'n.s.'}")
    # control descriptive
    print("\ncontrol nominal edges (descriptive):")
    for m in meas_names:
        c = np.array(ctrl[m]); b = np.array(bridge[m])
        print(f"  {m:10s} n={len(c):4d} med_ctrl={np.median(c):8.4f} med_std={np.median(b):8.4f}")
    any_sig = any(v[0] for v in verdicts.values())
    all_med_le = all(v[1] for v in verdicts.values())
    kill = (not any_sig) and all_med_le
    print(f"\nmachine verdict: {'KILLED' if kill else 'SURVIVES'} "
          f"(any significant: {any_sig}; all medians br<=ord: {all_med_le})")

if __name__ == '__main__':
    main()
