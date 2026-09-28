#!/usr/bin/env python3
"""Phase-3 step 1: baseline decomposition of the mode-11 semantic error.
Reads sealed corpus source wavs + phase-2 run workdirs (sem.wav, m.v6).
No re-runs: decomposes WHERE the semantic error lives per class:
  tails vs per-period amp vs refused harmonics vs HF vs filter coloring.
"""
import struct, sys, os, math, json, csv
import numpy as np

P2RUN = os.path.expanduser('~/workspace/exact_audio_replication/phase2/run/full_v6')
CORPUS = os.path.expanduser('~/workspace/audio_longhorizon/corpus')
OUT = os.path.expanduser('~/workspace/exact_audio_replication/phase3/results')

def read_wav_samples(path):
    d = open(path, 'rb').read()
    off = 12
    while off + 8 < len(d):
        if d[off:off+4] == b'data':
            sz = struct.unpack('<I', d[off+4:off+8])[0]
            n = sz // 2
            return np.frombuffer(d[off+8:off+8+2*n], dtype='<i2').astype(np.float64)
        sz = struct.unpack('<I', d[off+4:off+8])[0]
        off += 8 + sz
    raise ValueError('no data chunk: ' + path)

def parse_v6(path):
    d = open(path, 'rb').read()
    assert d[:8] == b'RBLMEMv6', path
    P = struct.unpack('<q', d[8:16])[0]
    K = struct.unpack('<q', d[16:24])[0]
    sr = struct.unpack('<q', d[32:40])[0]
    a_off = 40
    a = np.frombuffer(d[a_off:a_off+8*P], dtype='<f8')
    proto_off = a_off + 8*P
    proto = np.frombuffer(d[proto_off:proto_off+8*K], dtype='<f8')
    bg_off = proto_off + 8*K
    tail = bg_off + 8*K*K*K
    eplen = struct.unpack('<q', d[tail+40:tail+48])[0]
    EP_off = tail + 48
    pT = struct.unpack('<q', d[EP_off+8*eplen:EP_off+8*eplen+8])[0]
    T0 = struct.unpack('<d', d[EP_off+8*eplen+8:EP_off+8*eplen+16])[0]
    NBINS = struct.unpack('<q', d[EP_off+8*eplen+16:EP_off+8*eplen+24])[0]
    plm_off = EP_off + 8*eplen + 24
    plm = np.frombuffer(d[plm_off:plm_off+8*NBINS], dtype='<f8') if NBINS > 0 else np.zeros(0)
    PMF_off = plm_off + 8*NBINS
    boost = struct.unpack('<d', d[PMF_off+136:PMF_off+144])[0]
    q_off = PMF_off + 144 + 2*P
    n = struct.unpack('<q', d[len(d)-16:len(d)-8])[0]
    nr = n - P
    q = np.frombuffer(d[q_off:q_off+8*nr], dtype='<i8')
    ext = q_off + 8*nr
    use_h = struct.unpack('<q', d[ext+8:ext+16])[0]
    nper = struct.unpack('<q', d[ext+16:ext+24])[0]
    amp = np.frombuffer(d[ext+24:ext+24+8*nper], dtype='<f8') if nper > 0 else np.zeros(0)
    nres_off = ext + 24 + 8*nper + 8*P
    nres = np.frombuffer(d[nres_off:nres_off+8*nr], dtype='<f8')
    return dict(P=P, K=K, sr=sr, a=a, proto=proto, q=q, pT=pT, T0=T0,
                NBINS=NBINS, plm=plm, boost=boost, use_h=use_h, nper=nper,
                amp=amp, nres=nres, n=n, nr=nr)

def band_fracs(x, sr):
    n = len(x)
    w = np.hanning(n)
    X = np.abs(np.fft.rfft(x * w)) ** 2
    fr = np.fft.rfftfreq(n, 1.0 / sr)
    edges = [0, 250, 500, 1000, 2000, 4000, 8000, 12000, 16000, sr/2]
    tot = X.sum() + 1e-30
    return np.array([X[(fr >= edges[i]) & (fr < edges[i+1])].sum() / tot
                     for i in range(len(edges)-1)])

def main():
    rows = list(csv.DictReader(open(os.path.expanduser(
        '~/workspace/exact_audio_replication/phase2/results/corpus_results_v6intake.csv'))))
    out_rows = []
    for r in rows:
        name = r['name']
        wd = os.path.join(P2RUN, name)
        src = r['clip']
        try:
            m = parse_v6(os.path.join(wd, 'm.v6'))
            x = read_wav_samples(src)
            y = read_wav_samples(os.path.join(wd, 'sem.wav'))
            n = min(len(x), len(y), m['n'])
            x, y = x[:n], y[:n]
            dlt = y - x
            P, nr = m['P'], m['nr']
            # true residual via analysis filter (same op order as resid):
            # res[j] = x[P+j] - sum_k a[k]*x[P+j-1-k]
            a = m['a']
            res = x[P:P+nr].copy()
            for k in range(P):
                res -= a[k] * x[P-1-k:P-1-k+nr]
            o = dict(name=name, cls=name.split('-')[0])
            o['sem_rms'] = float(np.sqrt((dlt**2).mean()))
            o['sem_maxd'] = float(np.abs(dlt).max())
            xm, ym = x - x.mean(), y - y.mean()
            o['sem_corr'] = float((xm*ym).sum() / math.sqrt((xm**2).sum()*(ym**2).sum() + 1e-30))
            # residual-share baseline: RMS of the stored closure residual
            o['nres_rms'] = float(np.sqrt((m['nres']**2).mean()))
            o['use_h'] = int(m['use_h'])
            o['pT'] = int(m['pT'])
            o['boost'] = float(m['boost'])
            o['nper'] = int(m['nper'])
            # gap-6 size: error from amp=1 in the semantic path
            if m['use_h'] == 1 and m['nper'] > 0 and m['NBINS'] > 0:
                jj = np.arange(nr)
                hb = ((jj / m['T0']) % 1.0 * m['NBINS']).astype(np.int64) % m['NBINS']
                per = np.minimum(jj // m['pT'], m['nper'] - 1)
                g6 = (m['amp'][per] - 1.0) * m['plm'][hb]
                o['g6_rms'] = float(np.sqrt((g6**2).mean()))
                am = m['amp']
                o['amp_cv'] = float(am.std() / (abs(am.mean()) + 1e-30))
                # r2 of amp-aware harmonic
                h = am[per] * m['plm'][hb]
                vr = float(((res - res.mean())**2).mean())
                o['r2_amp'] = float(1.0 - ((res - h)**2).mean() / (vr + 1e-30))
                o['r2_raw'] = float(1.0 - ((res - m['plm'][hb])**2).mean() / (vr + 1e-30))
            else:
                o['g6_rms'] = 0.0
                o['amp_cv'] = 0.0
                o['r2_amp'] = 0.0
                o['r2_raw'] = 0.0
            # quantization-only error (excitation domain, old target)
            if m['use_h'] == 1 and m['NBINS'] > 0:
                jj = np.arange(nr)
                hb = ((jj / m['T0']) % 1.0 * m['NBINS']).astype(np.int64) % m['NBINS']
                h_old = m['plm'][hb]
            else:
                h_old = np.zeros(nr)
            t_old = res - h_old
            qq = np.clip(m['q'], 0, m['K'] - 1)
            e_q = t_old - m['proto'][qq]
            o['eq_rms'] = float(np.sqrt((e_q**2).mean()))
            o['eq_max'] = float(np.abs(e_q).max())
            thr = 4.0 * o['eq_rms']
            tail_e = e_q[np.abs(e_q) > thr]
            o['tail_energy_frac'] = float((tail_e**2).sum() / ((e_q**2).sum() + 1e-30))
            o['tail_frac'] = float(len(tail_e) / nr)
            # HF band fractions (semantic vs source)
            bf_x = band_fracs(x, m['sr'])
            bf_y = band_fracs(y, m['sr'])
            o['hf_src'] = float(bf_x[5:].sum())   # >4kHz
            o['hf_sem'] = float(bf_y[5:].sum())
            o['hf_ratio'] = float(o['hf_sem'] / (o['hf_src'] + 1e-30))
            # f0-band error for refused-harmonic clips
            o['f0band_relerr'] = 0.0
            if m['pT'] > 0 and m['use_h'] == 0:
                f0 = m['sr'] / m['pT']
                # nearest band edge index
                edges = [0, 250, 500, 1000, 2000, 4000, 8000, 12000, 16000, m['sr']/2]
                bi = next(i for i in range(9) if edges[i] <= f0 < edges[i+1])
                o['f0band_relerr'] = float((bf_y[bi] - bf_x[bi]) / (bf_x[bi] + 1e-30))
                o['f0'] = float(f0)
            out_rows.append(o)
        except Exception as ex:
            print('FAIL', name, repr(ex)[:200], file=sys.stderr)
    json.dump(out_rows, open(os.path.join(OUT, 'baseline_decomp.json'), 'w'))
    # per-class summary
    cls = {}
    for o in out_rows:
        c = cls.setdefault(o['cls'], [])
        c.append(o)
    print(f"{'class':<8} {'n':>4} {'sem_rms':>9} {'nres_rms':>9} {'eq_rms':>8} {'tailE%':>7} "
          f"{'use_h%':>7} {'refused(pT>0)':>12} {'g6_rms':>8} {'amp_cv':>7} {'r2_amp':>7} {'hf_ratio':>9}")
    for cname in sorted(cls):
        v = cls[cname]
        n = len(v)
        refused = sum(1 for o in v if o['pT'] > 0 and o['use_h'] == 0)
        useh = sum(1 for o in v if o['use_h'] == 1)
        print(f"{cname:<8} {n:>4} "
              f"{np.mean([o['sem_rms'] for o in v]):>9.1f} "
              f"{np.mean([o['nres_rms'] for o in v]):>9.1f} "
              f"{np.mean([o['eq_rms'] for o in v]):>8.1f} "
              f"{100*np.mean([o['tail_energy_frac'] for o in v]):>6.1f}% "
              f"{100*useh/n:>6.1f}% {refused:>12} "
              f"{np.mean([o['g6_rms'] for o in v if o['use_h']==1] or [0]):>8.1f} "
              f"{np.mean([o['amp_cv'] for o in v if o['use_h']==1] or [0]):>7.2f} "
              f"{np.mean([o['r2_amp'] for o in v if o['use_h']==1] or [0]):>7.3f} "
              f"{np.mean([o['hf_ratio'] for o in v]):>9.3f}")
    print('clips analyzed:', len(out_rows))

if __name__ == '__main__':
    main()
