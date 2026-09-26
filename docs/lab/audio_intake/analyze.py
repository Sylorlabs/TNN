#!/usr/bin/env python3
"""Intake-fidelity analyzer: fixture (source) vs re-emit (intake-held) vs imagined (downstream).
Waveform analysis first, per standing rule. Pure measurement, no decisions.
"""
import wave, hashlib, json, math
import numpy as np

SR = 44100

def load(p):
    w = wave.open(p, 'rb')
    assert w.getnchannels() == 1 and w.getsampwidth() == 2 and w.getframerate() == SR
    x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64)
    w.close()
    return x

def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()

def spectrum(x):
    n = len(x)
    N = 1
    while N < n: N <<= 1
    X = np.abs(np.fft.rfft(x * np.hanning(n), N)) ** 2
    fr = np.fft.rfftfreq(N, 1.0 / SR)
    return fr, X

def centroid(x):
    fr, X = spectrum(x)
    return float(np.sum(fr * X) / (np.sum(X) + 1e-30))

def band_energy_frac(x, lo, hi):
    fr, X = spectrum(x)
    tot = np.sum(X) + 1e-30
    return float(np.sum(X[(fr >= lo) & (fr < hi)]) / tot)

def f0_autocorr(x, lo=60, hi=1500):
    x = x - x.mean()
    n = len(x)
    lmin = max(2, int(SR / hi)); lmax = min(n - 1, int(SR / lo))
    if lmax <= lmin: return 0.0
    lags = np.arange(lmin, lmax + 1)
    r = np.array([np.dot(x[:n - l], x[l:]) for l in lags])
    r /= (r[0] + 1e-30)
    # first strong peak above 0.3 after the initial descent
    i = int(np.argmax(r > 0.3)) if (r > 0.3).any() else int(np.argmax(r))
    if i <= 0 or i >= len(r) - 1: return 0.0
    y0, y1, y2 = r[i-1], r[i], r[i+1]
    den = (y0 - 2*y1 + y2)
    d = 0.5 * (y0 - y2) / den if abs(den) > 1e-12 else 0.0
    lag = lags[i] + max(-1.0, min(1.0, d))
    return float(SR / lag)

def hnr(x):
    """HNR via autocorrelation peak (dB)."""
    x = x - x.mean()
    n = len(x)
    f0 = f0_autocorr(x)
    if f0 <= 0: return float('-inf')
    lag = int(round(SR / f0))
    if lag >= n: return float('-inf')
    r0 = np.dot(x, x)
    rl = np.dot(x[:n-lag], x[lag:])
    rho = rl / (r0 + 1e-30)
    rho = min(rho, 0.999999)
    if rho <= 0: return float('-inf')
    return float(10 * math.log10(rho / (1 - rho)))

def zcr(x):
    s = np.sign(x); s[s == 0] = 1
    return float(np.mean(s[1:] != s[:-1]))

def corr(a, b):
    n = min(len(a), len(b))
    a, b = a[:n] - a[:n].mean(), b[:n] - b[:n].mean()
    d = math.sqrt(np.dot(a, a) * np.dot(b, b)) + 1e-30
    return float(np.dot(a, b) / d)

def metrics(x):
    return dict(
        n=int(len(x)), peak=int(np.abs(x).max()),
        rms=round(float(np.sqrt(np.mean(x**2))), 2),
        dc=round(float(x.mean()), 3),
        centroid_hz=round(centroid(x), 1),
        f0_hz=round(f0_autocorr(x), 1),
        hnr_db=round(hnr(x), 2),
        zcr=round(zcr(x), 4),
        e_0_2k=round(band_energy_frac(x, 0, 2000), 4),
        e_2k_8k=round(band_energy_frac(x, 2000, 8000), 4),
        e_8k_16k=round(band_energy_frac(x, 8000, 16000), 4),
        e_16k=round(band_energy_frac(x, 16000, 22050), 4),
    )

def hum(x):
    """50/60 Hz + harmonics energy fraction."""
    fr, X = spectrum(x)
    tot = np.sum(X) + 1e-30
    e = 0.0
    for f in [50, 60, 100, 120, 150, 180]:
        e += np.sum(X[np.abs(fr - f) < 3])
    return round(float(e / tot), 6)

if __name__ == '__main__':
    import sys
    FX = '/home/hatch/workspace/rawbyte_longmem'
    GAL = '/home/hatch/workspace/your_files/rawbyte_longmem_NEW'
    RE = '/tmp/intake'
    out = {}
    for name in ['strike', 'cry', 'clang', 'vowel']:
        fx = load(f'{FX}/fixture_{name}.wav')
        re_ = load(f'{RE}/reemit_{name}_r1.wav')
        row = {'sha_fixture': sha(f'{FX}/fixture_{name}.wav'),
               'sha_reemit': sha(f'{RE}/reemit_{name}_r1.wav'),
               'fixture': metrics(fx), 'reemit': metrics(re_),
               'hum_fixture': hum(fx), 'hum_reemit': hum(re_)}
        n = min(len(fx), len(re_))
        d = fx[:n] - re_[:n]
        row['intake_diff'] = dict(
            max_abs=int(np.abs(d).max()),
            rms_diff=round(float(np.sqrt(np.mean(d**2))), 2),
            corr=round(corr(fx, re_), 5),
            n_common=int(n), n_fixture=int(len(fx)), n_reemit=int(len(re_)))
        if name in ('strike', 'cry', 'clang'):
            im = load(f'{GAL}/{name}_imagined.wav')
            row['sha_imagined'] = sha(f'{GAL}/{name}_imagined.wav')
            row['imagined'] = metrics(im)
            row['hum_imagined'] = hum(im)
        out[name] = row
    json.dump(out, open('/tmp/intake/metrics.json', 'w'), indent=1)
    for name, row in out.items():
        f, r = row['fixture'], row['reemit']
        print(f"== {name} ==")
        print(f"  fixture : N={f['n']} peak={f['peak']} rms={f['rms']} dc={f['dc']} centroid={f['centroid_hz']} f0={f['f0_hz']} hnr={f['hnr_db']} zcr={f['zcr']}")
        print(f"  re-emit : N={r['n']} peak={r['peak']} rms={r['rms']} dc={r['dc']} centroid={r['centroid_hz']} f0={r['f0_hz']} hnr={r['hnr_db']} zcr={r['zcr']}")
        d = row['intake_diff']
        print(f"  INTAKE DIFF: max|d|={d['max_abs']} rms_diff={d['rms_diff']} corr={d['corr']}")
        if 'imagined' in row:
            im = row['imagined']
            print(f"  imagined: N={im['n']} peak={im['peak']} rms={im['rms']} dc={im['dc']} centroid={im['centroid_hz']} f0={im['f0_hz']} hnr={im['hnr_db']} zcr={im['zcr']}")
    print('wrote /tmp/intake/metrics.json')
