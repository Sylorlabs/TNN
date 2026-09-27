#!/usr/bin/env python3
"""Waveform analysis for de-synth renders. Micah's law: waveform FIRST."""
import sys, wave, struct
import numpy as np

def read_wav(path):
    with wave.open(path, 'rb') as w:
        n = w.getnframes()
        sr = w.getframerate()
        raw = w.readframes(n)
    x = np.frombuffer(raw, dtype=np.int16).astype(np.float64)
    return sr, x

def estimate_f0(x, sr):
    win = sr // 10
    best_e, best_i = -1, 0
    for i in range(0, len(x) - win, win // 2):
        e = np.sum(x[i:i+win] ** 2)
        if e > best_e:
            best_e, best_i = e, i
    seg = x[best_i:best_i + win].astype(np.float64)
    seg = seg - np.mean(seg)
    ac = np.correlate(seg, seg, mode='full')[len(seg)-1:]
    ac = ac / (ac[0] + 1e-12)
    lo, hi = int(sr / 600), min(int(sr / 60), len(ac) - 1)
    pk = -1
    for i in range(lo + 1, hi):
        if ac[i] > ac[i-1] and ac[i] >= ac[i+1] and ac[i] > 0.3:
            pk = i
            break
    if pk < 0:
        return 0
    return sr / pk

def main():
    path = sys.argv[1]
    target_f0 = float(sys.argv[2]) if len(sys.argv) > 2 else 0
    sr, x = read_wav(path)
    x = x - np.mean(x)
    n = len(x)
    print(f"=== {path} ===")
    print(f"sr={sr} n={n} dur={n/sr:.2f}s peak={np.max(np.abs(x)):.0f} rms={np.sqrt(np.mean(x**2)):.1f}")

    # f0
    f0 = estimate_f0(x, sr)
    print(f"measured f0={f0:.1f} Hz", end="")
    if target_f0 > 0:
        print(f" target={target_f0:.1f} Hz err={(f0-target_f0)/target_f0*100:+.1f}%")
    else:
        print()

    # Spectrum: harmonic stack vs single sine?
    # Take a central 100ms window, FFT, find peaks
    win = sr // 10
    seg = x[n//2 - win//2 : n//2 + win//2].astype(np.float64)
    seg = seg * np.hanning(len(seg))
    spec = np.abs(np.fft.rfft(seg))
    freqs = np.fft.rfftfreq(len(seg), 1/sr)
    # Find harmonic peaks relative to f0
    if f0 > 0:
        print("harmonic amplitudes (dB rel to H1):")
        h1_amp = 0
        for h in range(1, 11):
            f = f0 * h
            idx = int(f * len(seg) / sr)
            lo, hi = max(0, idx-2), min(len(spec), idx+3)
            amp = np.max(spec[lo:hi]) if hi > lo else 0
            if h == 1:
                h1_amp = amp
            db = 20 * np.log10(amp / (h1_amp + 1e-12)) if h1_amp > 0 else -99
            print(f"  H{h} ({f:.0f} Hz): {db:+.1f} dB")
        # Single-sine test: is H1 dominant by >40dB over H2?
        # (A pure sine would have H2+ at -inf; a rich harmonic has multiple audible)
        idx2 = int(f0 * 2 * len(seg) / sr)
        h2 = np.max(spec[max(0,idx2-2):idx2+3])
        ratio_db = 20 * np.log10(h1_amp / (h2 + 1e-12)) if h1_amp > 0 else 0
        print(f"H1/H2 ratio: {ratio_db:.1f} dB (pure sine = inf; rich = <30dB)")

    # Envelope stationarity: RMS in 10ms windows, CV of envelope
    wlen = sr // 100
    env = np.array([np.sqrt(np.mean(x[i:i+wlen]**2)) for i in range(0, n - wlen, wlen)])
    env = env[env > 1.0]  # ignore silence
    if len(env) > 0:
        print(f"envelope: mean={np.mean(env):.1f} cv={np.std(env)/np.mean(env):.3f} min={np.min(env):.1f} max={np.max(env):.1f}")

    # Zero crossings (voicing check)
    zc = np.sum((x[:-1] * x[1:]) < 0)
    print(f"zero_crossings={zc} expected_for_{f0:.0f}Hz={(f0*n/sr*2):.0f}")

    # DC offset
    print(f"dc_offset={np.mean(x):.2f}")

    # SHA-256
    import hashlib
    with open(path, 'rb') as f:
        print(f"sha256={hashlib.sha256(f.read()).hexdigest()[:16]}...")

if __name__ == '__main__':
    main()
