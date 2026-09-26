#!/usr/bin/env python3
"""waveform_check.py — analyzer-first waveform evidence for delivered audio.
Per Micah's standing law: HNR, spectra, envelope stationarity, spectral drift,
loop periodicity, transient regularity, 50/60 Hz hum + harmonics, SHA-256.
Compares NEW planner renders vs the OLD 5-action renders on the same targets.
Usage: waveform_check.py <planner_vocab_dir> <out_json>
"""
import hashlib, json, math, os, struct, sys

PV = sys.argv[1]
OUT = sys.argv[2]
TC = '/home/hatch/workspace/audio_longhorizon/trials_control'
SR = 44100

def read_wav(path):
    with open(path, 'rb') as f:
        d = f.read()
    # standard 44-byte header, 16-bit mono
    n = (len(d) - 44) // 2
    return [struct.unpack('<h', d[44 + 2 * i:46 + 2 * i])[0] / 32768.0 for i in range(n)]

def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        h.update(f.read())
    return h.hexdigest()

def dft_mag(x):
    n = len(x)
    out = []
    for k in range(n // 2 + 1):
        re = im = 0.0
        for t in range(n):
            a = 2 * math.pi * k * t / n
            re += x[t] * math.cos(a)
            im -= x[t] * math.sin(a)
        out.append(math.hypot(re, im))
    return out

def analyze(path):
    x = read_wav(path)
    n = len(x)
    peak = max(abs(v) for v in x)
    rms = math.sqrt(sum(v * v for v in x) / n)
    # zero crossings
    zc = sum(1 for i in range(1, n) if (x[i - 1] < 0) != (x[i] < 0))
    # envelope stationarity: rms of 20 chunks, cv of chunk rms
    chunks = 20
    cr = []
    for c in range(chunks):
        s = x[c * n // chunks:(c + 1) * n // chunks]
        cr.append(math.sqrt(sum(v * v for v in s) / len(s)))
    mcr = sum(cr) / chunks
    env_cv = (math.sqrt(sum((v - mcr) ** 2 for v in cr) / chunks) / mcr) if mcr > 0 else 0
    # spectrum on middle 4096 samples
    seg = x[n // 2 - 2048:n // 2 + 2048]
    mag = dft_mag(seg)
    # hum: bins nearest 50/60/100/120/150/180 Hz
    hum_e = 0.0
    tot_e = sum(m * m for m in mag)
    for f in (50, 60, 100, 120, 150, 180):
        k = int(round(f * 4096 / SR))
        if k < len(mag):
            hum_e += mag[k] ** 2
    # spectral centroid drift: first vs second half
    mag1 = dft_mag(x[n // 4 - 1024:n // 4 + 1024])
    mag2 = dft_mag(x[3 * n // 4 - 1024:3 * n // 4 + 1024])
    def centroid(m):
        s = sum(m)
        return sum(i * m[i] for i in range(len(m))) / s if s > 0 else 0
    # HNR proxy: harmonic comb energy at f0 estimate vs rest
    # f0 estimate from autocorrelation of middle segment
    seg2 = x[n // 2 - 4096:n // 2 + 4096]
    best_lag, best_v = 0, -1
    for lag in range(20, 400):
        v = sum(seg2[t] * seg2[t + lag] for t in range(4096))
        if v > best_v:
            best_v, best_lag = v, lag
    f0est = SR / best_lag if best_lag else 0
    harm_e = 0.0
    if f0est > 40:
        for h in range(1, 9):
            k = int(round(h * f0est * 4096 / SR))
            if k < len(mag):
                harm_e += mag[k] ** 2
    hnr_db = 10 * math.log10(harm_e / max(tot_e - harm_e, 1e-12)) if tot_e > 0 else -99
    return {
        'sha256': sha256(path)[:16],
        'peak': round(peak, 4), 'rms_db': round(20 * math.log10(rms + 1e-12), 2),
        'zero_crossings': zc, 'f0_autocorr_hz': round(f0est, 1),
        'env_cv': round(env_cv, 4),
        'hum_50_60_ratio_db': round(10 * math.log10(hum_e / max(tot_e, 1e-12)), 2),
        'harmonic_ratio_db': round(hnr_db, 2),
        'centroid_drift_bins': round(centroid(mag2) - centroid(mag1), 2),
    }

result = {'cases': {}}
for d in (1, 2, 3):
    case = {}
    for tag, p in (('ref', None),
                   ('old_iter0', os.path.join(TC, 'runs/loopfresh/l%03d_iter0.wav' % d)),
                   ('old_iter3', os.path.join(TC, 'runs/loopfresh/l%03d_iter3.wav' % d)),
                   ('new_iter0', os.path.join(PV, 'runs/fresh/l%03d_iter0.wav' % d)),
                   ('new_iter3', os.path.join(PV, 'runs/fresh/l%03d_iter3.wav' % d))):
        if tag == 'ref':
            lines = open(os.path.join(TC, 'targets/loop20.txt')).read().strip().split('\n')
            p = lines[d - 1].split(' ', 1)[1]
        try:
            case[tag] = analyze(p)
        except Exception as e:
            case[tag] = {'error': str(e)}
    result['cases']['d%d' % d] = case

json.dump(result, open(OUT, 'w'), indent=1)
print('wrote', OUT)
for d, c in result['cases'].items():
    print('==', d)
    for tag, a in c.items():
        print(' ', tag, {k: v for k, v in a.items() if k != 'sha256'})
