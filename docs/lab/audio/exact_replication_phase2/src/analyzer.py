#!/usr/bin/env python3
"""Analyzer-first measurements: source vs exact vs semantic (fixtures).
Reports waveform stats, HNR proxy, spectral centroid, hum (50/60Hz)."""
import struct
import numpy as np

def read_wav(path):
    d = open(path, 'rb').read()
    off = 12
    while off + 8 < len(d):
        if d[off:off+4] == b'data':
            sz = struct.unpack('<I', d[off+4:off+8])[0]
            n = sz // 2
            x = np.frombuffer(d[off+8:off+8+2*n], dtype='<i2').astype(np.float64)
            sr = struct.unpack('<I', d[24:28])[0]
            return x, sr
        sz = struct.unpack('<I', d[off+4:off+8])[0]
        off += 8 + sz
    raise ValueError('no data')

def analyze(x, sr, tag):
    n = len(x)
    rms = float(np.sqrt((x**2).mean()))
    peak = float(np.abs(x).max())
    zc = int(((x[:-1] >= 0) != (x[1:] >= 0)).sum())
    # spectral centroid + hum via rfft
    X = np.abs(np.fft.rfft(x * np.hanning(n)))
    freqs = np.fft.rfftfreq(n, 1/sr)
    cent = float((freqs * X).sum() / (X.sum() + 1e-12))
    def band(f0, w=2.0):
        m = (freqs >= f0-w) & (freqs <= f0+w)
        return float(X[m].sum() / (X.sum() + 1e-12))
    hum50, hum60 = band(50), band(60)
    # HNR proxy: harmonic comb vs residual (autocorr peak)
    a = x - x.mean()
    ac = np.correlate(a, a, mode='full')[n-1:]
    ac = ac / (ac[0] + 1e-12)
    lo, hi = int(sr/500), int(sr/50)
    pk = float(ac[lo:hi].max()) if hi > lo else 0.0
    print(f"{tag}: rms={rms:.1f} peak={peak:.0f} zc={zc} centroid={cent:.1f}Hz "
          f"hum50={hum50:.4f} hum60={hum60:.4f} acpeak={pk:.4f}")

R = '/home/hatch/workspace/exact_audio_replication/phase2/run'
F = '/home/hatch/workspace/rawbyte_longmem'
for c in ['strike', 'vowel', 'cry', 'clang']:
    src, sr = read_wav(f'{F}/fixture_{c}.wav')
    ex, _ = read_wav(f'{R}/t_{c}/{c}_exact.wav')
    se, _ = read_wav(f'{R}/t_{c}/{c}_sem.wav')
    print(f'=== {c} (sr={sr}) ===')
    analyze(src, sr, 'source ')
    analyze(ex, sr, 'exact  ')
    analyze(se, sr, 'sem    ')
    print(f'  exact-vs-source max|d| = {np.abs(ex[:len(src)]-src).max():.1f} LSB')
