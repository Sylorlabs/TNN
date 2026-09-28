#!/usr/bin/env python3
"""Pitch meter for RT-LONG: ZCR-based frequency on a window of an .s32 mix.
Mirrors the binary's analyze(): zcr Q6M -> fm = zcr/2e6 * 22050.
Reports Hz + honest cents vs a reference.
"""
import sys, math
import numpy as np

SR = 44100

def load(p):
    return np.fromfile(p, dtype='<i4').astype(np.float64) / 65536.0

def zcr_hz(x):
    n = len(x)
    if n < 2:
        return 0.0
    zc = np.sum((x[:-1] < 0) != (x[1:] < 0))
    return (zc * 1e6 / n) / 2e6 * 22050.0

def cents(f, fref):
    return 1200.0 * math.log2(f / fref) if f > 0 and fref > 0 else float('nan')

def acf_hz(x, sr=SR, fmin=40, fmax=4000):
    x = x - x.mean()
    n = len(x)
    L = 1
    while L < 2 * n:
        L *= 2
    ac = np.fft.irfft(np.abs(np.fft.rfft(x, L)) ** 2, L)[:n]
    ac = ac / (ac[0] + 1e-18)
    lo, hi = max(1, int(sr / fmax)), min(n - 1, int(sr / fmin))
    seg = ac[lo:hi + 1]
    k = int(np.argmax(seg)) + lo
    if seg[k - lo] < 0.3:
        return 0.0
    if 0 < k < len(ac) - 1:
        a, b, c = ac[k - 1], ac[k], ac[k + 1]
        den = a - 2 * b + c
        shift = 0.5 * (a - c) / den if den != 0 else 0.0
        k = k + shift
    return sr / k

def main():
    # args: file t0s t1s fref_hz [label]
    path, t0, t1, fref = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])
    label = sys.argv[5] if len(sys.argv) > 5 else path
    x = load(path)
    seg = x[int(t0 * SR):int(t1 * SR)]
    # two halves like the latch (stationarity view)
    mid = len(seg) // 2
    f1, f2, fa = zcr_hz(seg[:mid]), zcr_hz(seg[mid:]), zcr_hz(seg)
    fac = acf_hz(seg)
    # FFT peak in 300-600 Hz band (isolates the response voice from the bed)
    n = len(seg)
    w = seg * np.hanning(n)
    sp = np.abs(np.fft.rfft(w))
    fr = np.fft.rfftfreq(n, 1.0 / SR)
    m = (fr >= 50) & (fr <= 2000)
    fpk = float(fr[m][np.argmax(sp[m])]) if np.any(m) else 0.0
    print("%s: zcr=%.2f acf=%.2f fftpk50-2000=%.2f Hz cents_vs_%.0f(fftpk)=%+.1f" %
          (label, fa, fac, fpk, fref, cents(fpk, fref)))

if __name__ == "__main__":
    main()
