#!/usr/bin/env python3
"""FROZEN scorer for Crew P (audio principles). Measurement DEFINITIONS only.

Implements the Section 2 hit criteria / Section 3.3 constants:
  - 2048-sample Hann frames, hop 1024, SR 44100
  - RMS dBFS per frame; autocorr F0 over lags 36..551 (80..1200 Hz),
    parabolic interpolation; voiced iff r>=0.40 and rms_db>-50
  - onset: frame RMS rise > 6 dB with frame rms > -50 dBFS, 80 ms refractory
  - HF band: |rFFT|**2 over 8..16 kHz bins, max over frames / peak total (g4c-style)
Zero RNG. Deterministic (numpy only).
"""
import wave, math, struct, sys
import numpy as np

SR = 44100
N, HOP = 2048, 1024
LMIN, LMAX = SR // 1200, SR // 80   # 36, 551
R_VOICED = 0.40
RMS_FLOOR_DB = -50.0

def load_wav(path):
    w = wave.open(path, 'rb')
    assert w.getnchannels() == 1 and w.getsampwidth() == 2 and w.getframerate() == SR
    d = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64)
    w.close()
    return d

def features(path):
    x = load_wav(path)
    if len(x) < N:
        x = np.pad(x, (0, N - len(x)))
    nfr = (len(x) - N) // HOP + 1
    idx = np.arange(N)[None, :] + HOP * np.arange(nfr)[:, None]
    xf = x[idx]
    rms = np.sqrt((xf ** 2).mean(axis=1))
    rms_db = 20 * np.log10(rms / 32768.0 + 1e-12)
    # autocorr F0
    w = np.hanning(N)
    xw = (xf - xf.mean(axis=1, keepdims=True)) * w
    Nf = 1
    while Nf < 2 * N:
        Nf *= 2
    S = np.abs(np.fft.rfft(xw, Nf)) ** 2
    r = np.fft.irfft(S, Nf)[:, :N]
    rn = r / (r[:, 0:1] + 1e-12)
    # YIN period selection on d[lag] = 2*(r0 - r[lag]):
    # cumulative-mean-normalized deficit; first dip below 0.10 then local min.
    # (Plain autocorr argmax provably fails 80-112 Hz under the 2048 Hann
    # window: the true long-lag peak is window-attenuated below short-lag
    # harmonic correlation. d = 2(r0-r) is autocorrelation-derived.)
    rlag = rn[:, 1:LMAX + 1]                      # (nfr, 551)
    d = 2.0 * (1.0 - rlag)
    run = np.cumsum(d, axis=1)
    denom = run / np.arange(1, LMAX + 1)[None, :]
    dp = np.ones_like(d)
    nz = denom > 1e-12
    dp[nz] = (d[nz] / denom[nz])
    seg = dp[:, LMIN - 1:LMAX]                    # lags LMIN..LMAX
    nfr = seg.shape[0]
    sel = np.full(nfr, -1)
    for f in range(nfr):
        s = -1
        for li in range(seg.shape[1]):
            if s < 0 and seg[f, li] < 0.10:
                s = li
            elif s >= 0:
                if seg[f, li] < seg[f, s]:
                    s = li
                else:
                    break
        if s < 0:
            s = int(np.argmin(seg[f]))
        sel[f] = s
    lag = LMIN + sel.astype(float)
    # parabolic interpolation on dp around the selected minimum
    ar = np.arange(nfr)
    si = sel.astype(int)
    pkm = np.clip(si - 1, 0, seg.shape[1] - 1)
    pkp = np.clip(si + 1, 0, seg.shape[1] - 1)
    a, b, c = seg[ar, pkm], seg[ar, si], seg[ar, pkp]
    den = a - 2 * b + c
    shift = np.where(np.abs(den) > 1e-12, 0.5 * (a - c) / np.where(np.abs(den) > 1e-12, den, 1.0), 0.0)
    interior = (si > 0) & (si < seg.shape[1] - 1)
    lag = lag + np.where(interior, shift, 0.0)
    f0 = np.where(b < 1.0, SR / np.maximum(lag, 1e-9), 0.0)
    rpeak = rn[ar, np.clip(LMIN + si, 0, N - 1)]
    voiced = (rpeak >= R_VOICED) & (rms_db > RMS_FLOOR_DB)
    # onsets
    onsets = []
    last = -1e9
    for f in range(1, nfr):
        rise = rms_db[f] - rms_db[f - 1]
        tms = (f + 1) * HOP * 1000.0 / SR
        if rise > 6.0 and rms_db[f] > -50.0 and tms - last > 80:
            onsets.append(tms); last = tms
    onsets = np.array(onsets)
    # HF band 8..16 kHz (g4c-style A metric)
    W = np.hanning(N)
    X = np.abs(np.fft.rfft(xf * W, N)) ** 2
    freqs = np.fft.rfftfreq(N, 1 / SR)
    bmask = (freqs >= 8000) & (freqs <= 16000)
    band = X[:, bmask].sum(axis=1)
    tot = X.sum(axis=1)
    peak_total = float(tot.max()) + 1e-12
    hf_db = 10 * np.log10(band.max() / peak_total + 1e-12)
    return dict(f0=f0, rpeak=rpeak, voiced=voiced, rms_db=rms_db,
                onsets=onsets, hf_db=hf_db, nfr=nfr)

def med_f0(fe):
    v = fe['f0'][fe['voiced']]
    return float(np.median(v)) if len(v) else 0.0

def ans_pitchrel(fa, fb):
    a, b = med_f0(fa), med_f0(fb)
    return 'A' if a >= b else 'B'

def ans_pitchabs(fe):
    f0 = med_f0(fe)
    if f0 <= 0:
        return 0
    idx = int(round(12 * math.log2(f0 / 110.0)))
    return max(0, min(23, idx))

def ans_env(fe):
    nfr = fe['nfr']
    n1, n2 = nfr // 3, 2 * nfr // 3
    if n1 <= 0 or nfr - n2 <= 0:
        return 'flat'
    d = fe['rms_db'][n2:].mean() - fe['rms_db'][:n1].mean()
    if d > 4.0:
        return 'rise'
    if d < -4.0:
        return 'decay'
    return 'flat'

def asym(onsets):
    if len(onsets) < 4:
        return 1.0
    ioi = np.diff(onsets)
    ioi = np.maximum(ioi, 1e-9)
    r = np.maximum(ioi[:-1], ioi[1:]) / np.minimum(ioi[:-1], ioi[1:])
    return float(np.median(r))

def ans_rhy(fa, fb):
    return 'A' if asym(fa['onsets']) >= asym(fb['onsets']) else 'B'

def ans_hf(fa, fb):
    return 'A' if fa['hf_db'] >= fb['hf_db'] else 'B'

DISPATCH = {'pitchrel': ans_pitchrel, 'pitchabs': ans_pitchabs, 'env': ans_env,
            'rhy': ans_rhy, 'hf': ans_hf}

if __name__ == '__main__':
    # scorer_p.py <qtype> <wavA> [wavB]  -> prints answer (self-test / sanity use)
    qt, wa = sys.argv[1], sys.argv[2]
    wb = sys.argv[3] if len(sys.argv) > 3 else None
    fa = features(wa)
    if wb:
        print(DISPATCH[qt](fa, features(wb)))
    else:
        print(DISPATCH[qt](fa))
