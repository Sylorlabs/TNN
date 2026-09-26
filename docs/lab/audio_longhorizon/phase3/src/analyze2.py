#!/usr/bin/env python3
"""Phase-3 step 1b: deep per-mechanism error attribution (waveform-first).
Answers, per class:
  1. boost distribution -> why is use_h ~2%? which refused clips would PLM help?
  2. tail waveform analysis: decay, spectra, HNR of |e|>4sig segments
  3. HF band errors (finer bands 4-8k, 8-12k, 12-16k, 16k+)
  4. envelope error structure (10ms envelope vs true envelope)
"""
import struct, sys, os, math, json, csv
import numpy as np

P2RUN = os.path.expanduser('~/workspace/exact_audio_replication/phase2/run/full_v6')
CORPUS = os.path.expanduser('~/workspace/audio_longhorizon/corpus')
RES = os.path.expanduser('~/workspace/exact_audio_replication/phase3/results')
sys.path.insert(0, os.path.expanduser('~/workspace/exact_audio_replication/phase3/src'))
from decompose import read_wav_samples, parse_v6, band_fracs

def fine_bands(x, sr):
    n = len(x); w = np.hanning(n)
    X = np.abs(np.fft.rfft(x * w)) ** 2
    fr = np.fft.rfftfreq(n, 1.0 / sr)
    edges = [0, 250, 500, 1000, 2000, 4000, 8000, 12000, 16000, sr/2]
    tot = X.sum() + 1e-30
    return np.array([X[(fr >= edges[i]) & (fr < edges[i+1])].sum() / tot for i in range(9)])

def hnr_est(x, sr, f0):
    # harmonic-to-noise ratio via comb filtering around f0
    if f0 <= 0 or f0 > sr/4: return float('nan')
    T = int(round(sr / f0))
    if T < 2 or 3*T >= len(x): return float('nan')
    seg = x[:3*T]
    harm = np.zeros(T)
    for k in range(3): harm += seg[k*T:(k+1)*T]
    harm /= 3.0
    sig = np.tile(harm, 3)[:len(seg)]
    noise = seg - sig
    return float(10*np.log10((sig**2).sum()/((noise**2).sum()+1e-30)))

def main():
    rows = list(csv.DictReader(open(os.path.expanduser(
        '~/workspace/exact_audio_replication/phase2/results/corpus_results_v6intake.csv'))))
    boost_all = []
    refused_detail = []   # (name, cls, boost, pT, f0, r2_plm_on_res, g_if_accepted_rms)
    tail_stats = []       # per-clip tail waveform facts
    hf_rows = []
    env_rows = []
    for r in rows:
        name = r['name']
        wd = os.path.join(P2RUN, name)
        try:
            m = parse_v6(os.path.join(wd, 'm.v6'))
            x = read_wav_samples(r['clip'])
            y = read_wav_samples(os.path.join(wd, 'sem.wav'))
            n = min(len(x), len(y), m['n'])
            x, y, n = x[:n], y[:n], n
            P, nr, a = m['P'], m['nr'], m['a']
            res = x[P:P+nr].copy()
            for k in range(P):
                res -= a[k] * x[P-1-k:P-1-k+nr]
            cls = name.split('-')[0]
            boost_all.append((m['boost'], cls, name))
            # ---- refused-clip PLM potential ----
            if m['pT'] > 0 and m['use_h'] == 0 and m['NBINS'] > 0:
                jj = np.arange(nr)
                hb = ((jj / m['T0']) % 1.0 * m['NBINS']).astype(np.int64) % m['NBINS']
                h = m['plm'][hb]
                vr = ((res-res.mean())**2).mean()
                # LS-fit amp per period, as resid would
                pT = m['pT']; nper = (nr + pT - 1)//pT
                num = np.zeros(nper); den = np.zeros(nper)
                per = np.minimum(jj // pT, nper-1)
                np.add.at(num, per, res*h); np.add.at(den, per, h*h)
                amp = np.where(den > 1e-12, num/den, 1.0)
                hfit = amp[per]*h
                r2 = 1.0 - ((res-hfit)**2).mean()/(vr+1e-30)
                refused_detail.append(dict(name=name, cls=cls, boost=m['boost'],
                                          f0=m['sr']/pT, r2_plm=r2,
                                          g_if_acc=float(np.sqrt(((hfit)**2).mean()))))
            # ---- tail waveform analysis ----
            if m['NBINS'] > 0:
                jj = np.arange(nr)
                hb = ((jj / m['T0']) % 1.0 * m['NBINS']).astype(np.int64) % m['NBINS']
                h_old = m['plm'][hb] if m['use_h'] == 1 else np.zeros(nr)
            else:
                h_old = np.zeros(nr)
            t_old = res - h_old
            qq = np.clip(m['q'], 0, m['K']-1)
            e_q = t_old - m['proto'][qq]
            sig = e_q.std()
            tmask = np.abs(e_q) > 4*sig
            if tmask.sum() > 32:
                te = e_q[tmask]
                # runs of consecutive tail samples (events)
                idx = np.where(tmask)[0]
                breaks = np.where(np.diff(idx) > 1)[0]
                runs = np.split(idx, breaks+1)
                runlens = [len(rr) for rr in runs]
                # longest event: decay + spectrum + HNR
                lr = max(runs, key=len)
                seg = e_q[max(0,lr[0]-64):lr[-1]+256]
                f0 = m['sr']/m['pT'] if m['pT'] > 0 else 0
                # spectral centroid of longest event
                w = np.hanning(len(seg)); X = np.abs(np.fft.rfft(seg*w))
                fr = np.fft.rfftfreq(len(seg), 1.0/m['sr'])
                cent = float((X*fr).sum()/(X.sum()+1e-30))
                # decay: envelope of |seg| after peak, log-slope per ms
                env = np.abs(seg); pk = int(np.argmax(env))
                tail = env[pk:pk+int(0.01*m['sr'])]
                if len(tail) > 8 and tail[0] > 1e-9:
                    lg = np.log(tail+1e-12)
                    sl = float((lg[-1]-lg[0])/(len(tail)/m['sr']*1000.0))  # nepers/ms
                else:
                    sl = float('nan')
                tail_stats.append(dict(name=name, cls=cls, nevents=len(runs),
                                       maxrun=int(max(runlens)), meanrun=float(np.mean(runlens)),
                                       tail_rms=float(np.sqrt((te**2).mean())),
                                       centroid=cent, decay_np_per_ms=sl,
                                       hnr=hnr_est(seg, m['sr'], f0)))
            # ---- HF finer bands ----
            bx, by = fine_bands(x, m['sr']), fine_bands(y, m['sr'])
            hf_rows.append(dict(name=name, cls=cls,
                                e48=float((by[5]-bx[5])/(bx[5]+1e-30)),
                                e812=float((by[6]-bx[6])/(bx[6]+1e-30)),
                                e1216=float((by[7]-bx[7])/(bx[7]+1e-30)),
                                e16p=float((by[8]-bx[8])/(bx[8]+1e-30))))
            # ---- envelope: 10ms true vs sem ----
            hop = int(m['sr']*0.01)
            def env10(s):
                nn = len(s)//hop
                return np.array([np.sqrt((s[i*hop:(i+1)*hop]**2).mean()) for i in range(nn)])
            ex, ey = env10(x), env10(y)
            L = min(len(ex), len(ey)); ex, ey = ex[:L], ey[:L]
            env_rows.append(dict(name=name, cls=cls,
                                 env_relerr=float(np.sqrt(((ey-ex)**2).mean())/(ex.mean()+1e-30)),
                                 env_corr=float(np.corrcoef(ex, ey)[0,1]) if L > 2 else 0.0))
        except Exception as ex:
            print('FAIL', name, repr(ex)[:160], file=sys.stderr)
    # ===== report =====
    print('=== boost distribution (gate: 1.5 < boost < 10.0) ===')
    b = np.array([t[0] for t in boost_all])
    print(f'n={len(b)} median={np.median(b):.2f} p10={np.percentile(b,10):.2f} p90={np.percentile(b,90):.2f} max={b.max():.2f}')
    import collections
    hist, edges = np.histogram(b, bins=[0,1,1.5,3,5,7,10,12,15,20,1e9])
    for i in range(len(hist)):
        print(f'  boost in [{edges[i]:.1f},{edges[i+1]:.1f}): {hist[i]}')
    print('=== refused clips: PLM potential (LS-fit amp, as resid would) ===')
    print(f'n_refused={len(refused_detail)}')
    rd = sorted(refused_detail, key=lambda d: -d['r2_plm'])
    for d in rd[:12]:
        print(f"  {d['name'][:34]:<34} cls={d['cls']:<7} boost={d['boost']:7.2f} f0={d['f0']:7.1f} r2_plm={d['r2_plm']:+.3f}")
    r2pos = [d for d in refused_detail if d['r2_plm'] > 0.05]
    print(f'  refused clips where PLM explains >5% of residual variance: {len(r2pos)}/{len(refused_detail)}')
    print('=== tail events (per class) ===')
    tc = collections.defaultdict(list)
    for t in tail_stats: tc[t['cls']].append(t)
    for c in sorted(tc):
        v = tc[c]
        print(f'  {c:<7} clips_w_tails={len(v)} med_events={np.median([t["nevents"] for t in v]):.0f} '
              f'med_maxrun={np.median([t["maxrun"] for t in v]):.0f}samples '
              f'med_centroid={np.nanmedian([t["centroid"] for t in v]):.0f}Hz '
              f'med_decay={np.nanmedian([t["decay_np_per_ms"] for t in v]):.2f}Np/ms '
              f'med_hnr={np.nanmedian([t["hnr"] for t in v]):.1f}dB')
    json.dump(dict(refused=refused_detail, tails=tail_stats, hf=hf_rows, env=env_rows,
                   boost=[dict(boost=t[0],cls=t[1],name=t[2]) for t in boost_all]),
              open(os.path.join(RES,'mechanism_attrib.json'),'w'))
    print('=== HF band relative errors (sem vs src), per class ===')
    hc = collections.defaultdict(list)
    for h in hf_rows: hc[h['cls']].append(h)
    for c in sorted(hc):
        v = hc[c]
        print(f'  {c:<7} 4-8k:{np.mean([t["e48"] for t in v]):+.3f} 8-12k:{np.mean([t["e812"] for t in v]):+.3f} '
              f'12-16k:{np.mean([t["e1216"] for t in v]):+.3f} 16k+:{np.mean([t["e16p"] for t in v]):+.3f}')
    print('=== 10ms envelope error, per class ===')
    ec = collections.defaultdict(list)
    for e in env_rows: ec[e['cls']].append(e)
    for c in sorted(ec):
        v = ec[c]
        print(f'  {c:<7} env_relerr={np.mean([t["env_relerr"] for t in v]):.3f} env_corr={np.mean([t["env_corr"] for t in v]):.4f}')
    print('analyzed OK')

if __name__ == '__main__':
    main()
