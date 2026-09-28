#!/usr/bin/env python3
"""FROZEN scorer for Crew L (audio principles, closed loop). Committed with the
first commit; never changed afterward.

Measurement DEFINITIONS (public, per prereg 3.4):
- F0: 2048-sample Hann frames, hop 1024; mean-remove; FFT autocorrelation;
  normalized peak over lags int(44100/1200)..int(44100/80); parabolic
  interpolation (shift = 0.5*(a-c)/(a-2b+c) when interior); VOICED iff
  r >= 0.40 and frame RMS > -50 dBFS; file F0 = median over voiced frames
  (lower-middle convention, matching the Zag organ).
- Env 3-class: frame RMS thirds by index; rise if E3 >= 2*E1, decay if
  E1 >= 2*E3, else flat; silence guard max(E1,E3) < 200 -> flat.
- ERR(k) = |F0_meas - F0_target|/F0_target + 0.5 * [env_meas != env_target].

Deterministic (numpy only), zero RNG.
"""
import wave, math, json, sys
import numpy as np

SR = 44100
N, HOP = 2048, 1024
F0MIN, F0MAX = 80.0, 1200.0
R_VOICED = 0.40
RMS_FLOOR_DB = -50.0
ENV_NAMES = {0: "flat", 1: "rise", 2: "decay"}

def load_wav(path):
    w = wave.open(path, 'rb')
    assert w.getnchannels() == 1 and w.getsampwidth() == 2 and w.getframerate() == SR
    d = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64)
    w.close()
    return d

def frame_grid(x):
    idx = np.arange(N)[None, :] + HOP * np.arange((len(x) - N) // HOP + 1)[:, None]
    return x[idx]

def measure_f0(x):
    xf = frame_grid(x)
    nfr = xf.shape[0]
    rms = np.sqrt((xf ** 2).mean(axis=1))
    rms_db = 20 * np.log10(rms / 32768.0 + 1e-12)
    # FFT autocorrelation, same as frozen Round-2 analyzer
    xw = (xf - xf.mean(axis=1, keepdims=True)) * np.hanning(N)
    nfft = 1
    while nfft < 2 * N:
        nfft *= 2
    S = np.abs(np.fft.rfft(xw, nfft)) ** 2
    r = np.fft.irfft(S, nfft)[:, :N]
    rn = r / (r[:, 0:1] + 1e-12)
    lmin, lmax = int(SR / F0MAX), int(SR / F0MIN)
    seg = rn[:, lmin:lmax + 1]
    pk = seg.argmax(axis=1)
    ar = np.arange(nfr)
    a = seg[ar, np.clip(pk - 1, 0, seg.shape[1] - 1)]
    b = seg[ar, pk]
    c = seg[ar, np.clip(pk + 1, 0, seg.shape[1] - 1)]
    den = a - 2 * b + c
    shift = np.where(np.abs(den) > 1e-12, 0.5 * (a - c) / den, 0.0)
    interior = (pk > 0) & (pk < seg.shape[1] - 1)
    lag = lmin + pk.astype(float) + np.where(interior, shift, 0.0)
    f0 = SR / lag
    rpeak = b
    voiced = (rpeak >= R_VOICED) & (rms_db > RMS_FLOOR_DB)
    vf0 = f0[voiced]
    f0_med = float(np.sort(vf0)[(len(vf0) - 1) // 2]) if len(vf0) else 0.0
    return f0_med, int(voiced.sum()), nfr, rms

def measure_env(rms_frames):
    nfr = len(rms_frames)
    third = nfr // 3
    e1 = float(rms_frames[:third].mean()) if third else 0.0
    e3 = float(rms_frames[2 * third:].mean()) if nfr - 2 * third else 0.0
    if max(e1, e3) < 200:
        return 0
    if e3 >= 2 * e1:
        return 1
    if e1 >= 2 * e3:
        return 2
    return 0

def score_file(path, target_hz, target_env):
    x = load_wav(path)
    f0, voiced, nfr, rms = measure_f0(x)
    env = measure_env(rms)
    err = abs(f0 - target_hz) / target_hz + 0.5 * (1 if env != target_env else 0)
    return {"f0": f0, "voiced": voiced, "nfr": nfr, "env": env,
            "env_name": ENV_NAMES[env], "err": err}

def main():
    # scorer_l.py <wav> <target_hz> <target_env_int>  -> JSON line
    path, thz, tenv = sys.argv[1], float(sys.argv[2]), int(sys.argv[3])
    print(json.dumps(score_file(path, thz, tenv)))

if __name__ == "__main__":
    main()
