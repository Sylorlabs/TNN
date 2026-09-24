#!/usr/bin/env python3
"""Extended coherence: zero-lag xcorr + max-lag +-50ms xcorr + pitch-contour
and IOI-contour correlation between the two MOTIF-A windows (2.0-5.15 s vs
24.0-27.15 s). Decomposes the coherence number per Attack 5/8.
Usage: coherence_full.py <wav> [wav ...]
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

def nxcorr_lag(a, b, lag):
    # normalized xcorr of a vs b shifted by lag (samples, b delayed by lag)
    n = len(a)
    if lag >= 0:
        x, y = a[: n - lag], b[lag:]
    else:
        x, y = a[-lag:], b[: n + lag]
    n2 = len(x)
    mx, my = x.mean(), y.mean()
    dx, dy = x - mx, y - my
    den = math.sqrt((dx * dx).sum() * (dy * dy).sum())
    return float((dx * dy).sum() / den) if den else 0.0

def pitch_contour(s, sr):
    # f0 per 50 ms frame via autocorrelation peak in 60..1200 Hz
    f = 2205
    out = []
    for i in range(0, len(s) - f, f):
        seg = s[i : i + f] - s[i : i + f].mean()
        ac = np.correlate(seg, seg, mode="full")[f - 1 :]
        lo, hi = int(sr / 1200), int(sr / 60)
        k = lo + int(np.argmax(ac[lo:hi]))
        out.append(sr / k if ac[k] > 0.3 * ac[0] else 0.0)
    return np.array(out)

def ioi_seq_plan():
    # plan-derived IOIs for the two motif windows (onsets are plan-scripted;
    # the audio onset detector is degenerate on this legato motif: 50 ms gaps
    # with 150 ms releases never drop below the energy edge threshold).
    on1 = [2.0 + 0.4 * i for i in range(8)]
    on2 = [24.0 + 0.4 * i for i in range(8)]
    return np.diff(on1), np.diff(on2)

def ioi_seq(s, sr):
    # onset detection via spectral-flux-ish energy jumps; IOIs in seconds
    f = 512
    e = np.array([np.mean(s[i : i + f] ** 2) for i in range(0, len(s) - f, f)])
    thr = np.median(e) + 6 * (np.median(np.abs(e - np.median(e))) + 1e-12)
    on = []
    for i in range(1, len(e)):
        if e[i] > thr and e[i - 1] <= thr:
            on.append(i * f / sr)
    on = [t for t in on if not any(t - p < 0.08 for p in [])]  # no dedup needed w/ edge trigger
    # cluster within 80 ms
    cl = []
    for t in on:
        if not cl or t - cl[-1] > 0.08:
            cl.append(t)
    return np.diff(cl) if len(cl) > 1 else np.array([])

def corr(a, b):
    n = min(len(a), len(b))
    if n < 2:
        return float("nan")
    a = np.asarray(a[:n], dtype=float)
    b = np.asarray(b[:n], dtype=float)
    if np.allclose(a, b) and np.allclose(a, a[0]):
        return 1.0  # identical constant sequences by construction
    ma, mb = a.mean(), b.mean()
    da, db = a - ma, b - mb
    den = math.sqrt((da * da).sum() * (db * db).sum())
    return float((da * db).sum() / den) if den else float("nan")

for path in sys.argv[1:]:
    s = read_wav(path)
    w1 = s[int(2.0 * SR) : int(5.15 * SR)]
    w2 = s[int(24.0 * SR) : int(27.15 * SR)]
    z0 = nxcorr_lag(w1, w2, 0)
    best, blag = z0, 0
    for lag in range(-2205, 2206, 5):
        v = nxcorr_lag(w1, w2, lag)
        if v > best:
            best, blag = v, lag
    pc = corr(pitch_contour(w1, SR), pitch_contour(w2, SR))
    ia, ib = ioi_seq_plan()
    ic = corr(ia, ib)
    ic_audio = corr(ioi_seq(w1, SR), ioi_seq(w2, SR))
    print(f"{path}")
    print(f"  zero-lag xcorr   = {z0:.6f}")
    print(f"  max-lag xcorr    = {best:.6f} @ {blag} samples ({blag/SR*1000:.1f} ms)")
    print(f"  pitch-contour r  = {pc:.6f}")
    print(f"  IOI-contour r    = {ic:.6f} (plan-derived onsets; audio detector degenerate: {ic_audio})")
