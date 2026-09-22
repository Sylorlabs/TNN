#!/usr/bin/env python3
"""measure_test1.py — machine-blind signal analysis for audio BLIND TEST-1.

Pure analysis tooling (not TNN decision machinery): computes synth-smell
fingerprint metrics from AUDIO_DEBATE.md (regularity / stationarity /
symmetry) plus A-NATIVE quality checks, for 30s mono 44.1kHz WAV clips.

Usage: measure_test1.py clip1.wav clip2.wav ...
Output: JSON object with per-clip metrics.

Metrics (all 0..1 unless noted; higher S-component = more synth-like):
  s1 envelope_periodicity : event-rhythm regularity — max normalized
      autocorrelation peak of the RMS envelope at lags 0.05..3.0 s.
  s2 stationarity         : 1 - clipped spectral-flux CV / RMS-env CV.
      A stationary bed (filtered-noise texture) scores near 1.
  s3 loop_score           : fraction of distant 1 s chunk pairs (>= 2 s apart)
      with log-mel cosine > 0.999. Looped/assembly repetition => high.
  s4 transient_symmetry   : mean attack/decay symmetry of detected
      transients (1 = perfectly symmetric envelope, synth-boom smell).
  s5 formant_stability    : 1 - clipped spectral-centroid CV on high-energy
      frames. Fixed ring / static formants => near 1.
  S                       : mean(s1..s5), the syntheticity index.

A-NATIVE checks (raw values):
  dc_offset, hiss_ratio (8-20 kHz / 0.3-8 kHz energy), hf_flatness
  (spectral flatness of the 8-20 kHz band), clip_count (|x| >= 0.999),
  click_count (derivative spikes > 6 sigma), transients_per_s.
"""
import sys, json, wave
import numpy as np

SR = 44100

def read_wav(path):
    w = wave.open(path, 'rb')
    n = w.getnframes(); ch = w.getnchannels(); r = w.getframerate()
    assert r == SR and ch == 1, f"expected 30s mono 44.1k: {path} got {r}Hz {ch}ch"
    raw = w.readframes(n); w.close()
    x = np.frombuffer(raw, dtype=np.int16).astype(np.float64) / 32768.0
    return x

def frames(x, L=2048, hop=512):
    n = 1 + (len(x) - L) // hop
    idx = np.arange(L)[None, :] + hop * np.arange(n)[:, None]
    return x[idx] * np.hanning(L)

def logmel(fr, nmel=24):
    spec = np.abs(np.fft.rfft(fr, axis=1))
    nb = spec.shape[1]
    fb = np.zeros((nmel, nb))
    for m in range(nmel):
        lo = int(nb * m / nmel); hi = min(nb, int(nb * (m + 1.5) / nmel))
        fb[m, lo:hi] = np.linspace(0, 1, hi - lo) if hi > lo else 0
    mel = np.log10(spec @ fb.T + 1e-12)
    return mel

def autocorr_peak(env, sr_env, lo_s=0.05, hi_s=3.0):
    e = env - env.mean()
    n = len(e)
    ac = np.correlate(e, e, mode='full')[n - 1:]
    if ac[0] <= 0: return 0.0
    ac = ac / ac[0]
    lo, hi = int(lo_s * sr_env), min(int(hi_s * sr_env), n - 1)
    if hi <= lo: return 0.0
    return float(np.max(ac[lo:hi]))

def measure(path):
    x = read_wav(path)
    out = {"file": path, "dur_s": round(len(x) / SR, 2)}

    # ---- A-NATIVE checks ----
    out["dc_offset"] = float(abs(np.mean(x)))
    out["clip_count"] = int(np.sum(np.abs(x) >= 0.999))
    d = np.diff(x); sdd = d.std()
    out["click_count"] = int(np.sum(np.abs(d) > 6 * sdd)) if sdd > 0 else 0
    fr = frames(x)
    spec = np.abs(np.fft.rfft(fr, axis=1))
    freqs = np.fft.rfftfreq(2048, 1 / SR)
    lo = spec[:, (freqs >= 300) & (freqs < 8000)].sum()
    hi = spec[:, (freqs >= 8000) & (freqs <= 20000)].sum()
    out["hiss_ratio"] = float(hi / (lo + 1e-12))
    hb = spec[:, (freqs >= 8000) & (freqs <= 20000)]
    gm = np.exp(np.log(hb + 1e-12).mean(axis=1))
    am = hb.mean(axis=1)
    out["hf_flatness"] = float(np.mean(gm / (am + 1e-12)))

    # ---- s1: envelope periodicity (event-rhythm regularity) ----
    env_fr = np.sqrt((fr ** 2).mean(axis=1))
    t_env = np.arange(len(env_fr)) * 512 / SR
    # downsample env to ~100 Hz by block mean
    k = max(1, int(SR / 100 / 512))
    env100 = env_fr[:len(env_fr) - len(env_fr) % k].reshape(-1, k).mean(axis=1)
    s1 = autocorr_peak(env100, 100)
    out["s1_envelope_periodicity"] = round(float(np.clip(s1, 0, 1)), 4)

    # ---- s2: stationarity ----
    mel = logmel(fr)
    flux = np.sqrt(((np.diff(mel, axis=0)) ** 2).sum(axis=1))
    flux_cv = float(flux.std() / (flux.mean() + 1e-12))
    rms_cv = float(env_fr.std() / (env_fr.mean() + 1e-12))
    s2 = 1.0 - min(1.0, (flux_cv + rms_cv) / 2 / 0.8)
    out["flux_cv"] = round(flux_cv, 4); out["rms_cv"] = round(rms_cv, 4)
    out["s2_stationarity"] = round(float(np.clip(s2, 0, 1)), 4)

    # ---- s3: loop / repetition score ----
    # 1 s chunk vectors (log-mel mean per chunk); near-exact repetition
    # means MANY distant chunk pairs are almost identical. s3 = fraction
    # of distant pairs with cosine > 0.999.
    cps = SR // 512  # chunks per second in frame units
    nch = len(mel) // cps
    vecs = mel[:nch * cps].reshape(nch, cps, -1).mean(axis=1)
    norms = np.linalg.norm(vecs, axis=1, keepdims=True) + 1e-12
    vn = vecs / norms
    sim = vn @ vn.T
    iu = np.triu_indices(nch, k=2)  # chunks >= 2 s apart
    pairs = sim[iu]
    out["s3_loop_score"] = round(float(np.mean(pairs > 0.999)) if len(pairs) else 0.0, 4)

    # ---- s4: transient symmetry ----
    thr = flux.mean() + 4 * flux.std()
    peaks = []
    last = -1000
    for i in range(1, len(flux) - 1):
        if flux[i] > thr and flux[i] >= flux[i - 1] and flux[i] > flux[i + 1] and i - last > int(0.2 * SR / 512):
            peaks.append(i); last = i
    out["transients_per_s"] = round(len(peaks) / (len(x) / SR), 2)
    syms = []
    w = int(0.1 * SR)  # 100 ms half-window
    loge = np.log(env_fr + 1e-9)
    for p in peaks:
        c = p * 512 + 256
        a0, a1 = max(0, c - w), min(len(x), c + w)
        seg = np.abs(x[a0:a1])
        if len(seg) < 20: continue
        pk = np.argmax(seg)
        att = seg[pk] - seg[0]; dec = seg[pk] - seg[-1]
        if att + dec <= 1e-9: continue
        syms.append(1.0 - abs(att - dec) / (att + dec))
    out["s4_transient_symmetry"] = round(float(np.mean(syms)) if syms else 0.5, 4)
    out["n_transients"] = len(syms)

    # ---- s5: formant / spectral-centroid stability ----
    cent = (spec * freqs).sum(axis=1) / (spec.sum(axis=1) + 1e-12)
    hot = env_fr > np.median(env_fr) * 1.5
    cc = cent[hot] if hot.sum() > 10 else cent
    cent_cv = float(cc.std() / (cc.mean() + 1e-12))
    s5 = 1.0 - min(1.0, cent_cv / 0.35)
    out["centroid_cv"] = round(cent_cv, 4)
    out["s5_formant_stability"] = round(float(np.clip(s5, 0, 1)), 4)

    S = np.mean([out["s1_envelope_periodicity"], out["s2_stationarity"],
                 out["s3_loop_score"], out["s4_transient_symmetry"],
                 out["s5_formant_stability"]])
    out["S_syntheticity"] = round(float(S), 4)
    return out

if __name__ == "__main__":
    res = [measure(p) for p in sys.argv[1:]]
    print(json.dumps(res, indent=1))
