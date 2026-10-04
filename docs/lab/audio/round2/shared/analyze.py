#!/usr/bin/env python3
"""AUDIO ROUND 2 — shared analyzer. Waveform analysis BEFORE any ear claim.
Implements all shared gates from ROUND2_PREREG.md + per-fork metric hooks.
Deterministic (numpy only). Usage:
  analyze.py <wav> [--f0min 80] [--f0max 1200] [--seg-min-ms 100] [--json-out p]
Prints a gate table; exits 0 iff all shared gates pass (kill bars evaluated
by per-fork scripts on top of the JSON metrics).
"""
import wave, sys, json, math
import numpy as np

SR_EXPECT = 44100

def load_wav(path):
    w = wave.open(path, 'rb')
    assert w.getnchannels() == 1 and w.getsampwidth() == 2 and w.getframerate() == SR_EXPECT, \
        f"bad format: ch={w.getnchannels()} sw={w.getsampwidth()} sr={w.getframerate()}"
    d = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64)
    w.close()
    return d

def frame(x, n=1102, hop=441):
    idx = np.arange(n)[None, :] + hop * np.arange((len(x) - n) // hop + 1)[:, None]
    return x[idx]

def autocorr_period(xf, sr, f0min, f0max):
    """per-frame: normalized autocorr peak in [sr/f0max, sr/f0min]; returns (f0, r)."""
    n = xf.shape[1]
    w = np.hanning(n)
    xw = (xf - xf.mean(axis=1, keepdims=True)) * w
    # FFT autocorr
    N = 1
    while N < 2 * n: N *= 2
    S = np.abs(np.fft.rfft(xw, N)) ** 2
    r = np.fft.irfft(S, N)[:, :n]
    r0 = r[:, 0:1] + 1e-12
    rn = r / r0
    lmin, lmax = int(sr / f0max), int(sr / f0min)
    seg = rn[:, lmin:lmax + 1]
    pk = seg.argmax(axis=1)
    # parabolic interpolation around the peak (vectorized): removes
    # integer-lag quantization that otherwise reads as ~0.5% fake
    # "prosody" on perfectly static tones.
    ar = np.arange(len(seg))
    pkm = np.clip(pk - 1, 0, seg.shape[1] - 1)
    pkp = np.clip(pk + 1, 0, seg.shape[1] - 1)
    a = seg[ar, pkm]; b = seg[ar, pk]; c = seg[ar, pkp]
    den = a - 2 * b + c
    shift = np.where(np.abs(den) > 1e-12, 0.5 * (a - c) / den, 0.0)
    interior = (pk > 0) & (pk < seg.shape[1] - 1)
    lag = lmin + pk.astype(float) + np.where(interior, shift, 0.0)
    return sr / lag, seg[ar, pk]

def formant_bandpeaks(x, sr, nf=4096):
    """cepstrum-liftered spectrum, peak-pick F1..F3 in 200..4000 Hz. Returns list."""
    w = x * np.hanning(len(x))
    S = np.abs(np.fft.rfft(w, nf))
    logS = np.log(S + 1e-9)
    ceps = np.fft.irfft(logS)
    lif = np.zeros_like(ceps); lif[:40] = 1.0  # keep slow envelope only
    env = np.exp(np.fft.rfft(ceps * lif, nf).real)
    freqs = np.fft.rfftfreq(nf, 1 / sr)
    band = (freqs >= 200) & (freqs <= 4000)
    e, f = env[band], freqs[band]
    peaks = []
    for i in range(1, len(e) - 1):
        if e[i] > e[i - 1] and e[i] >= e[i + 1]:
            peaks.append((e[i], f[i]))
    peaks.sort(reverse=True)
    out, used = [], []
    for mag, fr in peaks:
        if all(abs(fr - u) > 250 for u in used):
            out.append(fr); used.append(fr)
        if len(out) == 3: break
    out += [0.0] * (3 - len(out))
    return sorted(out)

def spectral_centroid(x, sr):
    S = np.abs(np.fft.rfft(x * np.hanning(len(x)))) ** 2
    f = np.fft.rfftfreq(len(x), 1 / sr)
    return float((S * f).sum() / (S.sum() + 1e-12))

def analyze(path, f0min=80, f0max=1200, seg_min_ms=100):
    x = load_wav(path)
    dur = len(x) / SR_EXPECT
    peak = float(np.abs(x).max())
    peak_dbfs = 20 * math.log10(peak / 32768.0 + 1e-12)
    xf = frame(x)
    nfr = xf.shape[0]
    rms = np.sqrt((xf ** 2).mean(axis=1))
    rms_db = 20 * np.log10(rms / 32768.0 + 1e-12)
    f0, rper = autocorr_period(xf, SR_EXPECT, f0min, f0max)
    voiced = (rper >= 0.40) & (rms_db > -50)
    # ---- frac_static: voiced frames stable within 5% of LOCAL median F0
    # (±15 frames ≈ ±150 ms). Measures "held pitch" per note — the anti-
    # "accelerator"/glide bar — not deviation from a global median (which
    # would punish any multi-note phrase by design).
    f0v = f0[voiced]
    f0med = float(np.median(f0v)) if len(f0v) else 0.0
    W = 15
    f0pad = np.pad(f0, W, mode='edge')
    lmed = np.array([np.median(f0pad[i:i + 2 * W + 1]) for i in range(nfr)])
    static = voiced & (np.abs(f0 - lmed) / (lmed + 1e-9) <= 0.05)
    frac_static = float(static.sum() / nfr)
    # ---- HNR (de Krom): r/(1-r), median over voiced
    hnr = 10 * np.log10(np.clip(rper[voiced], 1e-6, 0.999999) / np.clip(1 - rper[voiced], 1e-6, 1))
    hnr_med = float(np.median(hnr)) if len(hnr) else -99.0
    # ---- PERIODICITY: median r at intended period (global median F0 lag)
    lag = int(round(SR_EXPECT / f0med)) if f0med > 0 else 0
    periodicity = float(np.median(rper[voiced])) if len(f0v) else 0.0
    # ---- HF_ROLLOFF: E(>8k)/max 500Hz-band energy, whole clip
    X = np.abs(np.fft.rfft(x)) ** 2
    fr = np.fft.rfftfreq(len(x), 1 / SR_EXPECT)
    e_hi = X[fr > 8000].sum()
    bands = [X[(fr >= b) & (fr < b + 500)].sum() for b in range(0, 20000, 500)]
    e_max = max(bands) + 1e-12
    hf_db = 10 * math.log10(e_hi / e_max + 1e-12)
    # ---- PROSODY: per voiced-run F0 std/median, median across runs
    runs, cur = [], []
    for i in range(nfr):
        if voiced[i]: cur.append(i)
        else:
            if cur: runs.append(cur); cur = []
    if cur: runs.append(cur)
    minlen = int(seg_min_ms / 10)
    pros, runw = [], []
    for r in runs:
        if len(r) >= minlen:
            # trim 50 ms from each end (attack/release + note-boundary
            # artifacts inflate std; prosody = STEADY-part variation)
            idx = r[5:-5] if len(r) > 12 else r
            seg = f0[idx]
            # median-5 filter: removes octave-jump outliers from the tracker
            # under heavy breath noise; preserves 5.5 Hz vibrato (18 frames/cycle)
            if len(seg) >= 5:
                sp = np.pad(seg, 2, mode='edge')
                seg = np.array([np.median(sp[i:i + 5]) for i in range(len(seg))])
            pros.append(float(np.std(seg) / (np.median(seg) + 1e-9)))
            runw.append(len(r))
    prosody = float(np.average(pros, weights=runw)) if pros else 0.0
    voiced_frac = float(voiced.sum() / nfr)
    # ---- TRANSIENT: onsets via 10 ms energy rise; crest in first 20 ms
    hop = 441
    env = np.sqrt(np.convolve(x ** 2, np.ones(hop) / hop, mode='same'))
    env_db = 20 * np.log10(env / 32768.0 + 1e-12)
    onsets = []
    last = -10**9
    i = hop
    while i < len(env_db) - hop:
        rise10 = env_db[i] - env_db[i - hop]  # dB rise over 10 ms
        if rise10 > 6 and env_db[i] > -45 and i - last > 13230:
            onsets.append(i); last = i
        i += 1
    crests = []
    for o in onsets:
        seg = x[o:o + 882]
        if len(seg) < 882: continue
        pk = np.abs(seg).max() + 1e-9
        rm = math.sqrt((seg ** 2).mean()) + 1e-9
        crests.append(20 * math.log10(pk / rm))
    crest_med = float(np.median(crests)) if crests else 0.0
    # ---- formant tracks (voiced frames, 100ms windows)
    f1s, f2s, f3s = [], [], []
    step = 10  # every 10th voiced frame
    for i in range(0, nfr, step):
        if voiced[i]:
            s = xf[i]
            a, b, c = formant_bandpeaks(s, SR_EXPECT)
            if a > 0: f1s.append(a)
            if b > 0: f2s.append(b)
            if c > 0: f3s.append(c)
    fmt = dict(f1_med=float(np.median(f1s)) if f1s else 0.0,
               f2_med=float(np.median(f2s)) if f2s else 0.0,
               f3_med=float(np.median(f3s)) if f3s else 0.0,
               f1_std=float(np.std(f1s)) if f1s else 0.0,
               f2_std=float(np.std(f2s)) if f2s else 0.0,
               n_fmt=len(f1s))
    centroid = spectral_centroid(x, SR_EXPECT)
    m = dict(path=path, dur_s=round(dur, 3), peak_dbfs=round(peak_dbfs, 2),
             frac_static=round(frac_static, 4), hnr_db=round(hnr_med, 2),
             periodicity=round(periodicity, 4), f0_med_voiced=round(f0med, 1),
             voiced_frac=round(voiced_frac, 4), hf_rolloff_db=round(hf_db, 2),
             prosody=round(prosody, 5), n_onsets=len(onsets),
             crest_med_db=round(crest_med, 2),
             crest_all_db=[round(c, 2) for c in crests],
             centroid_hz=round(centroid, 1), formants=fmt)
    gates = {
        'frac_static>=0.25': m['frac_static'] >= 0.25,
        'HNR 3.7+-3dB': 0.7 <= m['hnr_db'] <= 6.7,
        'PERIODICITY>=0.5': m['periodicity'] >= 0.5,
        'HF_ROLLOFF in [-40,-12]dB': -40 <= m['hf_rolloff_db'] <= -12,
        'PROSODY in [0.3%,3%]': 0.003 <= m['prosody'] <= 0.03,
        'TRANSIENT crest med in [3,20]dB': 3 <= m['crest_med_db'] <= 20,
        'peak < -1 dBFS': m['peak_dbfs'] < -1.0,
    }
    return m, gates

if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('wav')
    ap.add_argument('--f0min', type=float, default=80)
    ap.add_argument('--f0max', type=float, default=1200)
    ap.add_argument('--json-out')
    a = ap.parse_args()
    m, gates = analyze(a.wav, a.f0min, a.f0max)
    print(f"== {a.wav}")
    for k, v in m.items():
        if k not in ('crest_all_db',):
            print(f"  {k}: {v}")
    print("  -- gates --")
    allok = True
    for k, v in gates.items():
        print(f"  [{'PASS' if v else 'FAIL'}] {k}")
        allok = allok and v
    print(f"  ALL SHARED GATES: {'PASS' if allok else 'FAIL'}")
    if a.json_out:
        json.dump({'metrics': m, 'gates': gates}, open(a.json_out, 'w'), indent=1)
    sys.exit(0 if allok else 1)
