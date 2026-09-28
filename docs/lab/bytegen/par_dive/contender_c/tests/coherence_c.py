#!/usr/bin/env python3
"""Contender C coherence battery (prereg section 2 COHERENCE + Attack 5/8).
Motif windows: 2.0-5.4 s vs 24.0-27.4 s.
numpy-accelerated.
"""
import struct, sys, math
import numpy as np

SR = 44100

def read_wav(path):
    with open(path, "rb") as f:
        data = f.read()
    assert data[0:4] == b"RIFF" and data[8:12] == b"WAVE", "not a wav"
    raw = data[44:]
    n = len(raw) // 2
    return np.array(struct.unpack("<%dh" % n, raw[: n * 2]), dtype=np.float64)

def xcorr_zerolag(a, b):
    n = min(len(a), len(b))
    a, b = a[:n] - a[:n].mean(), b[:n] - b[:n].mean()
    return float(a @ b / math.sqrt((a @ a) * (b @ b)))

def xcorr_maxlag(a, b, maxlag):
    # FFT-based cross-correlation, normalized per lag
    n = min(len(a), len(b))
    a, b = a[:n].copy(), b[:n].copy()
    L = 1
    while L < 2 * n:
        L *= 2
    Fa = np.fft.rfft(a - a.mean(), L)
    Fb = np.fft.rfft(b - b.mean(), L)
    cc = np.fft.irfft(Fa * np.conj(Fb), L)[:n]
    # normalize by local energies
    a2 = np.concatenate([[0.0], np.cumsum(a * a)])
    b2 = np.concatenate([[0.0], np.cumsum(b * b)])
    ea = a2[n] - a2[0]
    eb = b2[n] - b2[0]
    best, blag = -2.0, 0
    # lags: cc[k] = sum a[i+k]*b[i] ; check k in [-maxlag, maxlag]
    for lag in range(0, maxlag + 1):
        m = n - lag
        na = a2[n] - a2[lag]
        nb = b2[m] - b2[0]
        c = cc[lag] / math.sqrt(na * nb) if na > 0 and nb > 0 else 0.0
        if c > best:
            best, blag = c, lag
    # negative lags via reversed roles
    cc2 = np.fft.irfft(np.conj(Fa) * Fb, L)[:n]
    for lag in range(1, maxlag + 1):
        m = n - lag
        na = a2[m] - a2[0]
        nb = b2[n] - b2[lag]
        c = cc2[lag] / math.sqrt(na * nb) if na > 0 and nb > 0 else 0.0
        if c > best:
            best, blag = c, -lag
    return best, blag

def autocorr_f0(frame):
    n = len(frame)
    x = frame - frame.mean()
    e0 = x @ x
    if e0 <= 0:
        return 0.0
    lo = max(1, int(SR / 4000))
    hi = min(n - 1, int(SR / 40))
    # vectorized autocorrelation via FFT
    L = 1
    while L < 2 * n:
        L *= 2
    ac = np.fft.irfft(np.abs(np.fft.rfft(x, L)) ** 2, L)[:hi + 1] / e0
    seg = ac[lo:hi + 1]
    bp = int(np.argmax(seg)) + lo
    if seg[bp - lo] < 0.3:
        return 0.0
    return SR / bp

def spectral_centroid(frame):
    e = frame @ frame
    if e <= 0:
        return 0.0
    d = np.diff(frame)
    return float(math.sqrt((d @ d) / e))

def corr(xs, ys):
    xs = np.array(xs, dtype=np.float64)
    ys = np.array(ys, dtype=np.float64)
    n = min(len(xs), len(ys))
    xs, ys = xs[:n] - xs[:n].mean(), ys[:n] - ys[:n].mean()
    dx, dy = xs @ xs, ys @ ys
    return float(xs @ ys / math.sqrt(dx * dy)) if dx > 0 and dy > 0 else 0.0

def contour(s, fn, flen=1764):
    return [fn(s[i:i + flen]) for i in range(0, len(s) - flen, flen)]

def onsets(s, thresh_ratio=0.30, min_sep_s=0.25):
    # flux onsets: 10 ms hop RMS, positive-flux peak-picking
    hop = 441
    nb = (len(s) - hop) // hop
    rms = np.array([math.sqrt(float(s[i*hop:(i+1)*hop] @ s[i*hop:(i+1)*hop]) / hop)
                    for i in range(nb)])
    flux = np.maximum(0.0, np.diff(rms))
    pk = flux.max() if len(flux) else 1.0
    th = pk * thresh_ratio
    min_sep = int(min_sep_s * SR / hop)
    ons, last = [], -10**9
    for i in range(1, len(flux) - 1):
        if flux[i] > th and flux[i] >= flux[i-1] and flux[i] >= flux[i+1] \
           and i - last >= min_sep:
            ons.append(i * hop / SR)
            last = i
    return ons

for path in sys.argv[1:]:
    s = read_wav(path)
    w1 = s[int(2.0 * SR):int(5.4 * SR)]
    w2 = s[int(24.0 * SR):int(27.4 * SR)]
    z = xcorr_zerolag(w1, w2)
    ml, lag = xcorr_maxlag(w1, w2, 2205)
    f1 = contour(w1, autocorr_f0)
    f2 = contour(w2, autocorr_f0)
    pc = corr(f1, f2)
    c1 = contour(w1, spectral_centroid)
    c2 = contour(w2, spectral_centroid)
    cc = corr(c1, c2)
    o1, o2 = onsets(w1), onsets(w2)
    ic = float("nan")
    if len(o1) > 2 and len(o2) > 2:
        ic = corr(np.diff(o1).tolist(), np.diff(o2).tolist())
    print(path)
    print("  xcorr_zero=%.6f  xcorr_maxlag50ms=%.6f (lag %d)" % (z, ml, lag))
    print("  pitch_contour_corr=%.6f  centroid_corr=%.6f  ioi_corr=%.6f" % (pc, cc, ic))
    print("  onsets w1=%d w2=%d" % (len(o1), len(o2)))
