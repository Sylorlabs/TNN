#!/usr/bin/env python3
"""PAR_DIVE analysis toolkit: mix diffs, xcorr, pitch-in-cents. Measurement only."""
import numpy as np

SR = 44100

def load(p):
    return np.fromfile(p, dtype='<i4').astype(np.float64)

def diff_stats(a, b):
    d = a != b
    n = int(np.sum(d))
    m = float(np.max(np.abs(a - b))) if n else 0.0
    return n, m

def znxcorr(x, y):
    x = x - x.mean(); y = y - y.mean()
    d = np.linalg.norm(x) * np.linalg.norm(y)
    if d == 0: return 0.0
    return float(np.dot(x, y) / d)

def maxlag_xcorr(x, y, maxlag):
    best, bl = -2.0, 0
    for lag in range(-maxlag, maxlag + 1):
        if lag < 0: xx, yy = x[-lag:], y[:len(y)+lag]
        elif lag > 0: xx, yy = x[:len(x)-lag], y[lag:]
        else: xx, yy = x, y
        c = znxcorr(xx, yy)
        if c > best: best, bl = c, lag
    return best, bl

def pitch_hz(x, sr=SR, fmin=60, fmax=2000):
    x = x - x.mean()
    n = len(x)
    ac = np.correlate(x, x, mode='full')[n-1:]
    ac = ac / (ac[0] + 1e-18)
    lo, hi = int(sr / fmax), int(sr / fmin)
    seg = ac[lo:hi+1]
    k = int(np.argmax(seg)) + lo
    if 0 < k < len(ac) - 1:
        a, b, c = ac[k-1], ac[k], ac[k+1]
        den = a - 2*b + c
        shift = 0.5 * (a - c) / den if den != 0 else 0.0
        k = k + shift
    return sr / k

def cents(f1, f0):
    return 1200.0 * np.log2(f1 / f0)

def zcr(x):
    return float(np.mean(np.abs(np.diff(np.sign(x)))) / 2.0)

def rms(x):
    return float(np.sqrt(np.mean(x**2)))
