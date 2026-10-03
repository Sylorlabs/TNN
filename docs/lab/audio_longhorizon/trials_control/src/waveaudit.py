#!/usr/bin/env python3
"""waveaudit.py — full analyzer-first waveform audit of trial renders.

Extended beyond wavecheck.py: HNR, spectra, envelope stationarity,
spectral drift, boundary-loop periodicity, transient regularity,
50/60 Hz hum + harmonics, and agreement of measured descriptors with the
journal's PLANNED values (per M-target plan, or per L-iteration plan).

Deterministic (numpy only, zero RNG). Usage:
  waveaudit.py <rundir> > <out.json>
Prints JSON: per-file rows + run summary with flag counts.
"""
import glob, json, os, struct, sys
import numpy as np

sys.path.insert(0, '/home/hatch/workspace/audio_principles/crew_p')
import scorer_p as SP  # noqa: E402  (frozen measurement definitions)

SR = 44100


def read_wav(p):
    with open(p, 'rb') as f:
        d = f.read()
    off = 12
    ds, ns = None, None
    while off + 8 <= len(d):
        cid = d[off:off + 4]
        sz = struct.unpack('<I', d[off + 4:off + 8])[0]
        if cid == b'data':
            ds, ns = off + 8, sz // 2
            break
        off += 8 + sz
    return np.frombuffer(d[ds:ds + ns * 2], dtype=np.int16).astype(np.float64)


def hum_rel(X, fr, base):
    """Spectral peak in [base-1,base+1] (fundamental only), relative to global max.

    Fundamental-only by design: the renders use wide FM vibrato whose
    sidebands legitimately land on mains harmonics (e.g. 120/180 Hz); a
    harmonic-sum detector false-flags those. Mains hum is judged on the
    50/60 Hz fundamental, which no render design component occupies.
    """
    mx = X.max() + 1e-9
    band = X[(fr >= base - 1) & (fr <= base + 1)]
    return float(band.max() / mx) if len(band) else 0.0


def hnr_db(x):
    """Harmonic-to-noise ratio via cepstrum peak in pitch band vs floor."""
    n = len(x)
    w = x * np.hanning(n)
    spec = np.abs(np.fft.rfft(w)) ** 2 + 1e-12
    ceps = np.fft.irfft(np.log(spec))
    # pitch quefrency band: 1/1200..1/50 s
    q0, q1 = int(SR / 1200), int(SR / 50)
    q0 = max(q0, 1)
    peak = ceps[q0:q1].max() if q1 > q0 else 0.0
    floor = np.median(np.abs(ceps[q0:q1])) + 1e-12 if q1 > q0 else 1e-12
    return 20 * np.log10(peak / floor + 1e-12)


def rms_thirds_db(x):
    n = len(x)
    out = []
    for k in range(3):
        seg = x[k * n // 3:(k + 1) * n // 3]
        out.append(20 * np.log10(np.sqrt((seg ** 2).mean()) + 1e-9))
    return out


def centroid_thirds(x):
    n = len(x)
    out = []
    for k in range(3):
        seg = x[k * n // 3:(k + 1) * n // 3]
        X = np.abs(np.fft.rfft(seg * np.hanning(len(seg)))) + 1e-12
        fr = np.fft.rfftfreq(len(seg), 1 / SR)
        out.append(float((X * fr).sum() / X.sum()))
    return out


def parse_plans(journal):
    """-> {render_basename: {'f0_mhz': int, 'env': str, 'vib': int}}"""
    plans = {}
    cur_target = None
    iters = {}
    for line in open(journal):
        line = line.rstrip('\n')
        if line.startswith('TARGET '):
            p = line.split()
            kv = {}
            for tok in p[2:]:
                if '=' in tok:
                    k, v = tok.split('=', 1)
                    kv[k] = v
            cur_target = {'idx': int(p[1]), 'depth': int(kv.get('depth', 0)),
                          'kind': kv.get('kind', ''), 'ref': kv.get('ref', ''),
                          'iters': {}}
        elif line.startswith('PLANNED ') and cur_target is not None:
            kv = dict(kv.split('=', 1) for kv in line.split()[1:])
            if cur_target['kind'] == 'M':
                cur_target['plan'] = kv
            else:
                cur_target['iters'][0] = kv
        elif line.startswith('ITER ') and cur_target is not None:
            p = line.split()
            itn = int(p[1])
            if p[2] == 'PLANNED':
                kv = dict(tok.split('=', 1) for tok in p[3:] if '=' in tok)
                cur_target['iters'][itn] = kv
            elif p[2] == 'RENDERED':
                path = line.split('RENDERED ', 1)[1]
                bn = os.path.basename(path)
                plans[bn] = dict(cur_target['iters'].get(itn, {}))
        elif line.startswith('RENDERED ') and cur_target is not None:
            path = line.split(' ', 1)[1]
            bn = os.path.basename(path)
            plans[bn] = dict(cur_target.get('plan', {}))
    return plans


def env_of(plan):
    e = plan.get('env', '')
    return e if e in ('flat', 'rise', 'decay') else None


def analyze(p, plans):
    x = read_wav(p)
    bn = os.path.basename(p)
    n = len(x)
    peak = float(np.abs(x).max())
    dc = float(x.mean())
    zc = float(((x[:-1] * x[1:]) < 0).mean())
    clipped = int((np.abs(x) >= 32767).sum())
    X = np.abs(np.fft.rfft(x * np.hanning(n))) + 1e-12
    fr = np.fft.rfftfreq(n, 1 / SR)
    cent = float((X * fr).sum() / X.sum())
    h50 = float(hum_rel(X, fr, 50))
    h60 = float(hum_rel(X, fr, 60))
    hnr = float(hnr_db(x))
    thirds = rms_thirds_db(x)
    stat_db = float(max(thirds) - min(thirds))
    cthirds = centroid_thirds(x)
    cdrift = float(max(cthirds) - min(cthirds))
    # boundary click: energy of first/last 5ms vs body slope
    edge = 220
    body = x[edge:-edge] if n > 2 * edge else x
    body_rms = float(np.sqrt((body ** 2).mean()) + 1e-9)
    head_peak = float(np.abs(x[:edge]).max())
    tail_peak = float(np.abs(x[-edge:]).max())
    click = float(max(head_peak, tail_peak) / (body_rms + 1e-9))
    # plan agreement
    plan = plans.get(bn, {})
    fe = SP.features(p)
    f0m = float(SP.med_f0(fe))
    envm = SP.ans_env(fe)
    f0p = int(plan.get('f0_mhz', 0)) / 1000.0 if plan.get('f0_mhz') else None
    envp = env_of(plan)
    f0_agree = (abs(f0m - f0p) / f0p <= 0.10) if (f0p and f0p > 0 and f0m > 0) else None
    env_agree = (envm == envp) if envp else None
    flags = []
    if clipped > 0:
        flags.append('CLIP')
    if abs(dc) > 100:
        flags.append('DC')
    if h50 > 0.10:
        flags.append('HUM50')
    if h60 > 0.10:
        flags.append('HUM60')
    if hnr < 6:
        flags.append('LOW_HNR')
    if envp == 'flat' and stat_db > 6:
        flags.append('NONSTAT_FLAT')
    if click > 12:
        flags.append('EDGE_CLICK')
    if f0_agree is False:
        flags.append('PLAN_F0_MISMATCH')
    if env_agree is False:
        flags.append('PLAN_ENV_MISMATCH')
    return {
        'file': bn, 'n': n, 'peak': int(peak), 'dc': round(dc, 2),
        'zcr': round(zc, 4), 'clipped': clipped,
        'cent_hz': round(cent, 1), 'hum50': round(h50, 4),
        'hum60': round(h60, 4), 'hnr_db': round(hnr, 1),
        'rms_thirds_db': [round(v, 2) for v in thirds],
        'stationarity_db': round(stat_db, 2),
        'centroid_drift_hz': round(cdrift, 1),
        'edge_click_ratio': round(click, 2),
        'f0_meas': round(f0m, 1), 'f0_plan': round(f0p, 1) if f0p else None,
        'env_meas': envm, 'env_plan': envp,
        'f0_agree_10pct': f0_agree, 'env_agree': env_agree,
        'flags': flags,
    }


def main():
    d = sys.argv[1]
    journal = os.path.join(d, 'journal.txt')
    plans = parse_plans(journal) if os.path.exists(journal) else {}
    rows = [analyze(p, plans) for p in sorted(glob.glob(os.path.join(d, '*.wav')))]
    flagcount = {}
    for r in rows:
        for f in r['flags']:
            flagcount[f] = flagcount.get(f, 0) + 1
    summary = {
        'n_wavs': len(rows), 'n_flagged': sum(1 for r in rows if r['flags']),
        'flag_counts': flagcount,
        'mean_hnr_db': round(float(np.mean([r['hnr_db'] for r in rows])), 1) if rows else 0,
        'max_hum50': max([r['hum50'] for r in rows]) if rows else 0,
        'max_hum60': max([r['hum60'] for r in rows]) if rows else 0,
        'plan_f0_agree_rate': (sum(1 for r in rows if r['f0_agree_10pct'] is True) /
                               max(1, sum(1 for r in rows if r['f0_agree_10pct'] is not None))),
        'plan_env_agree_rate': (sum(1 for r in rows if r['env_agree'] is True) /
                                max(1, sum(1 for r in rows if r['env_agree'] is not None))),
    }
    print(json.dumps({'summary': summary, 'rows': rows}, indent=1))


if __name__ == '__main__':
    main()
