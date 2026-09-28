#!/usr/bin/env python3
"""Scan the 134 s field recording for laugh-like episodes:
sequences of >=4 voiced bursts with inter-burst intervals in [110, 260] ms
(laugh syllable rate 4-9 Hz). Reports ranked candidates with offsets.
"""
import wave, sys
import numpy as np
from scipy.signal import butter, sosfilt

SRC = '/home/hatch/workspace/tnn-lab/imagination_discovery/aud/b_alpha/consistency_gate/calibration/aporee_kids_play_area.wav'

def load(p):
    w = wave.open(p, 'rb')
    sr = w.getframerate(); n = w.getnframes(); ch = w.getnchannels()
    d = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float64)
    if ch == 2: d = d.reshape(-1, 2).mean(axis=1)
    w.close()
    return d, sr

def main():
    x, sr = load(SRC)
    print(f"loaded {len(x)/sr:.1f}s @ {sr}Hz", file=sys.stderr)
    sos = butter(4, [300, 3400], btype='band', fs=sr, output='sos')
    y = sosfilt(sos, x)
    env = np.sqrt(np.convolve(y ** 2, np.ones(sr // 100) / (sr // 100), mode='same'))
    thr = np.percentile(env, 97)
    # peak-pick bursts
    peaks = []
    i = 0
    min_gap = int(0.09 * sr)
    while i < len(env):
        if env[i] > thr:
            j = i
            while j < len(env) and env[j] > thr * 0.5: j += 1
            peaks.append((i + j) // 2)
            i = j + min_gap
        else:
            i += 1
    print(f"n bursts: {len(peaks)}", file=sys.stderr)
    # chain into episodes: consecutive peaks with gaps in [110,260] ms
    eps = []
    cur = [peaks[0]] if peaks else []
    for p in peaks[1:]:
        gap = (p - cur[-1]) / sr * 1000
        if 110 <= gap <= 260:
            cur.append(p)
        else:
            if len(cur) >= 4: eps.append(cur)
            cur = [p]
    if len(cur) >= 4: eps.append(cur)
    # rank by burst count then mean burst energy
    ranked = []
    for e in eps:
        t0, t1 = e[0] / sr, e[-1] / sr
        seg = x[int(e[0] - 0.15 * sr):int(e[-1] + 0.25 * sr)]
        e_db = 20 * np.log10(np.sqrt((seg ** 2).mean()) / 32768 + 1e-12)
        ranked.append((len(e), e_db, t0, t1))
    ranked.sort(key=lambda r: (-r[0], -r[1]))
    print("LAUGH EPISODE CANDIDATES (n_bursts, level_dBFS, t0_s, t1_s):")
    for r in ranked[:12]:
        print(f"  bursts={r[0]} level={r[1]:.1f}dB t0={r[2]:.2f} t1={r[3]:.2f} dur={r[3]-r[2]:.2f}s")

if __name__ == '__main__':
    main()
