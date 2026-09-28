#!/usr/bin/env python3
"""Full mandated waveform analysis for the de-synth battery (Micah's law:
waveform FIRST, before any quality claim).

Per target: final render (iter3) vs reference. Measures:
  basic integrity: peak, rms, dc, clipping fraction
  envelope: 10ms RMS windows -> mean/std/CV/min/max
  f0: autocorrelation on loudest 100ms window (60..600 Hz)
  HNR: de Krom 10*log10(r/(1-r)) on same window
  spectrum: dominant peak + top-5 peaks (central window)
  spectral drift: dominant peak first-third vs last-third
  hum: band energy at 50/60 Hz and harmonics (100,120,150,180,200,240,300)
  zcr, periodicity strength (max norm autocorr in 60..600 Hz lag range)
  transients: onset count via frame-RMS-derivative threshold

Usage: waveform_full.py <targets_manifest> <render_dir> <out_tsv>
  render files: <render_dir>/l{NNN}_iter3.wav
"""
import sys, wave, os
import numpy as np

def read_wav(path):
    with wave.open(path, 'rb') as w:
        n = w.getnframes(); sr = w.getframerate()
        ch = w.getnchannels(); sw = w.getsampwidth()
        raw = w.readframes(n)
    if sw == 2:
        x = np.frombuffer(raw, dtype=np.int16).astype(np.float64)
    elif sw == 1:
        x = (np.frombuffer(raw, dtype=np.uint8).astype(np.float64) - 128) * 256
    else:
        raise ValueError(f"bad sampwidth {sw}")
    if ch > 1:
        x = x.reshape(-1, ch).mean(axis=1)
    return sr, x

def loudest_seg(x, sr, ms=100):
    win = int(sr * ms / 1000)
    if len(x) <= win:
        return x.copy()
    best_e, best_i = -1, 0
    step = win // 4
    for i in range(0, len(x) - win, step):
        e = np.sum(x[i:i+win] ** 2)
        if e > best_e:
            best_e, best_i = e, i
    return x[best_i:best_i+win]

def f0_hnr(seg, sr, fmin=60, fmax=600):
    seg = seg - np.mean(seg)
    e = np.sum(seg ** 2)
    if e < 1e-9:
        return 0.0, float('-inf'), 0.0, 0
    ac = np.correlate(seg, seg, mode='full')[len(seg)-1:]
    ac = ac / (ac[0] + 1e-12)
    lo = max(2, int(sr / fmax)); hi = min(int(sr / fmin), len(ac) - 1)
    best_r, best_lag = -1, 0
    for lag in range(lo + 1, hi):
        if ac[lag] > ac[lag-1] and ac[lag] >= ac[lag+1] and ac[lag] > best_r:
            best_r, best_lag = ac[lag], lag
    if best_lag == 0:
        return 0.0, float('-inf'), float(np.max(ac[lo:hi])) if hi > lo else 0.0, 0
    f0 = sr / best_lag
    r = min(best_r, 0.999999)
    hnr = 10 * np.log10(r / (1 - r)) if r > 0 else float('-inf')
    return f0, hnr, best_r, best_lag

def spectrum_peaks(x, sr, n_peaks=5):
    n = len(x)
    win = min(n, sr)  # up to 1s central
    seg = x[n//2 - win//2: n//2 + win//2].astype(np.float64)
    seg = seg - np.mean(seg)
    seg = seg * np.hanning(len(seg))
    spec = np.abs(np.fft.rfft(seg))
    freqs = np.fft.rfftfreq(len(seg), 1/sr)
    # peak-pick above 40 Hz
    idx = np.where(freqs >= 40)[0]
    s = spec[idx]; f = freqs[idx]
    peaks = []
    for i in range(1, len(s)-1):
        if s[i] > s[i-1] and s[i] >= s[i+1]:
            peaks.append((s[i], f[i]))
    peaks.sort(reverse=True)
    tot = np.sum(spec ** 2) + 1e-12
    out = []
    for amp, fr in peaks[:n_peaks]:
        out.append((fr, 10*np.log10((amp**2)/tot)))
    dom = peaks[0][1] if peaks else 0.0
    return dom, out

def hum_db(x, sr):
    n = len(x)
    seg = x[:min(n, 4*sr)].astype(np.float64)
    seg = seg - np.mean(seg)
    spec = np.abs(np.fft.rfft(seg * np.hanning(len(seg)))) ** 2
    freqs = np.fft.rfftfreq(len(seg), 1/sr)
    tot = np.sum(spec) + 1e-12
    res = {}
    for hf in (50, 60, 100, 120, 150, 180, 200, 240, 300):
        m = (freqs >= hf-2) & (freqs <= hf+2)
        res[hf] = 10*np.log10(np.sum(spec[m])/tot)
    return res

def envelope_stats(x, sr):
    wlen = sr // 100
    if len(x) < wlen:
        return 0, 0, 0, 0, 0
    env = np.array([np.sqrt(np.mean(x[i:i+wlen]**2)) for i in range(0, len(x)-wlen, wlen)])
    env = env[env > 1.0]
    if len(env) == 0:
        return 0, 0, 0, 0, 0
    m = np.mean(env)
    return m, np.std(env), (np.std(env)/m if m > 0 else 0), np.min(env), np.max(env)

def onset_count(x, sr):
    wlen = sr // 100
    fr = np.array([np.sqrt(np.mean(x[i:i+wlen]**2)) for i in range(0, len(x)-wlen, wlen)])
    if len(fr) < 3:
        return 0
    db = 20*np.log10(fr + 1e-9)
    cnt, last = 0, -10**9
    for i in range(1, len(db)):
        tms = i * 10
        if db[i] - db[i-1] > 6 and db[i] > -50 and tms - last > 80:
            cnt += 1; last = tms
    return cnt

def analyze(path):
    sr, x = read_wav(path)
    n = len(x)
    peak = np.max(np.abs(x))
    rms = np.sqrt(np.mean(x**2))
    dc = np.mean(x)
    clip = np.mean(np.abs(x) >= 32760)
    emean, estd, ecv, emin, emax = envelope_stats(x, sr)
    seg = loudest_seg(x, sr)
    f0, hnr, pstr, plag = f0_hnr(seg, sr)
    dom, peaks = spectrum_peaks(x, sr)
    # drift: dominant peak first third vs last third
    third = n // 3
    d1, _ = spectrum_peaks(x[:third], sr) if third > sr//10 else (0, [])
    d2, _ = spectrum_peaks(x[2*third:], sr) if third > sr//10 else (0, [])
    hum = hum_db(x, sr)
    zc = np.sum((x[:-1]*x[1:]) < 0)
    zcr = zc / (n / sr) if n > 0 else 0
    onc = onset_count(x, sr)
    return dict(sr=sr, dur=n/sr, peak=peak, rms=rms, dc=dc, clip=clip,
                emean=emean, estd=estd, ecv=ecv, emin=emin, emax=emax,
                f0=f0, hnr=hnr, pstr=pstr, plag=plag,
                dom=dom, peaks=peaks, drift1=d1, drift2=d2, hum=hum,
                zcr=zcr, onsets=onc)

def main():
    manifest, rdir, out = sys.argv[1], sys.argv[2], sys.argv[3]
    lines = [l.split() for l in open(manifest) if l.strip()]
    hdr = ["tgt", "side", "ref",
           "dur", "peak", "rms", "dc", "clip",
           "env_mean", "env_cv", "env_min", "env_max",
           "f0", "hnr_db", "per_str", "per_lag",
           "dom_hz", "drift_hz_1", "drift_hz_2",
           "hum50", "hum60", "hum100", "hum120", "hum150", "hum180",
           "zcr", "onsets"]
    rows = []
    for i, (kind, ref) in enumerate(lines, 1):
        rpath = os.path.join(rdir, f"l{i:03d}_iter3.wav")
        for side, p in (("render", rpath), ("ref", ref)):
            try:
                a = analyze(p)
                peaks_s = ";".join(f"{f:.0f}:{d:.1f}" for f, d in a["peaks"])
                rows.append([i, side, os.path.basename(ref),
                             f"{a['dur']:.2f}", f"{a['peak']:.0f}", f"{a['rms']:.1f}",
                             f"{a['dc']:.2f}", f"{a['clip']:.4f}",
                             f"{a['emean']:.1f}", f"{a['ecv']:.3f}",
                             f"{a['emin']:.1f}", f"{a['emax']:.1f}",
                             f"{a['f0']:.1f}", f"{a['hnr']:.1f}",
                             f"{a['pstr']:.3f}", f"{a['plag']}",
                             f"{a['dom']:.0f}", f"{a['drift1']:.0f}", f"{a['drift2']:.0f}",
                             f"{a['hum'][50]:.1f}", f"{a['hum'][60]:.1f}",
                             f"{a['hum'][100]:.1f}", f"{a['hum'][120]:.1f}",
                             f"{a['hum'][150]:.1f}", f"{a['hum'][180]:.1f}",
                             f"{a['zcr']:.0f}", f"{a['onsets']}", peaks_s])
            except Exception as e:
                rows.append([i, side, os.path.basename(ref), f"ERR {e}"])
        print(f"target {i}/20 done", flush=True)
    with open(out, "w") as f:
        f.write("\t".join(hdr + ["top_peaks_hz:db"]) + "\n")
        for r in rows:
            f.write("\t".join(map(str, r)) + "\n")
    print(f"wrote {out}", flush=True)

if __name__ == "__main__":
    main()
