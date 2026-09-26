#!/usr/bin/env python3
"""Phase-3 step 1c: quantify candidate mechanisms in numpy BEFORE writing Zag.
Candidates:
  B1: tail-level extension - 16 extra scalar levels at tail quantiles, refit q
  B2: sparse impulse channel - top-M spikes as (pos, amp), M by energy budget
  A1: consistent per-period amp - q refit vs res-amp*plm, emit uses amp*plm
  D1: HF hash after B1 (measure only)
Metric: excitation-domain RMS of semantic-vs-true residual, and output-domain
proxy (LPC gain). Also residual-share RMS.
"""
import struct, sys, os, math, json, csv
import numpy as np

P2RUN = os.path.expanduser('~/workspace/exact_audio_replication/phase2/run/full_v6')
sys.path.insert(0, os.path.expanduser('~/workspace/exact_audio_replication/phase3/src'))
from decompose import read_wav_samples, parse_v6

def lpc_gain(a, sr):
    # synthesis filter 1/A(z) RMS gain proxy via impulse response energy
    P = len(a); h = np.zeros(4096); h[0] = 1.0
    for i in range(1, 4096):
        s = 0.0
        for k in range(min(P, i)): s += a[k]*h[i-1-k]
        h[i] = s
    return float(np.sqrt((h**2).sum()))

def run_clip(name, clip):
    wd = os.path.join(P2RUN, name)
    m = parse_v6(os.path.join(wd, 'm.v6'))
    x = read_wav_samples(clip)
    y = read_wav_samples(os.path.join(wd, 'sem.wav'))
    n = min(len(x), len(y), m['n']); x, y = x[:n], y[:n]
    P, nr, a, K = m['P'], m['nr'], m['a'], m['K']
    res = x[P:P+nr].copy()
    for k in range(P): res -= a[k]*x[P-1-k:P-1-k+nr]
    proto = m['proto'][:K]
    out = dict(name=name, cls=name.split('-')[0])
    # baseline: current semantic excitation (what mode 11 renders)
    if m['use_h'] == 1 and m['NBINS'] > 0:
        jj = np.arange(nr)
        hb = ((jj/m['T0']) % 1.0 * m['NBINS']).astype(np.int64) % m['NBINS']
        h_base = m['plm'][hb]
    else:
        h_base = np.zeros(nr)
    qq = np.clip(m['q'], 0, K-1)
    sem_exc_base = proto[qq] + h_base
    out['base_exc_rms'] = float(np.sqrt(((res-sem_exc_base)**2).mean()))
    # ---- B1: tail levels ----
    e_q = (res - h_base) - proto[qq]
    sig = e_q.std()
    tmask = np.abs(e_q) > 4*sig
    te = e_q[tmask]
    if len(te) > 32:
        qs = np.quantile(te, np.linspace(0.02, 0.98, 16))
        # dedupe near-duplicates, keep sorted
        lv = []
        for v in qs:
            if not lv or abs(v-lv[-1]) > 1e-9: lv.append(float(v))
        ext = np.concatenate([proto, np.array(lv)])
        tgt = res - h_base
        # nearest-level assignment (vectorized via broadcasting on chunks)
        best = np.empty(nr, dtype=np.int64); bestd = np.full(nr, np.inf)
        CH = 1 << 16
        for s in range(0, nr, CH):
            d = np.abs(tgt[s:s+CH, None] - ext[None, :])
            bi = d.argmin(axis=1)
            best[s:s+CH] = bi; bestd[s:s+CH] = d.min(axis=1)
        sem_b1 = ext[best] + h_base
        out['b1_exc_rms'] = float(np.sqrt(((res-sem_b1)**2).mean()))
        out['b1_nextra'] = len(lv)
        out['b1_tailfrac'] = float(tmask.mean())
    else:
        out['b1_exc_rms'] = out['base_exc_rms']; out['b1_nextra'] = 0; out['b1_tailfrac'] = 0.0
    # ---- B2: sparse impulse channel on top of B1 ----
    # top-M spikes of remaining error, M = 0.1% of nr, store exact values
    if len(te) > 32:
        rem = res - sem_b1
        M = max(16, nr//1000)
        idx = np.argpartition(np.abs(rem), -M)[-M:]
        imp = np.zeros(nr); imp[idx] = rem[idx]
        sem_b2 = sem_b1 + imp
        out['b2_exc_rms'] = float(np.sqrt(((res-sem_b2)**2).mean()))
        out['b2_M'] = M
        out['b2_bytes'] = M*16  # pos i64 + amp f64
    else:
        out['b2_exc_rms'] = out['b1_exc_rms']; out['b2_M'] = 0; out['b2_bytes'] = 0
    # ---- A1: consistent amp (use_h=1 clips only) ----
    if m['use_h'] == 1 and m['nper'] > 0 and m['NBINS'] > 0:
        jj = np.arange(nr)
        hb = ((jj/m['T0']) % 1.0 * m['NBINS']).astype(np.int64) % m['NBINS']
        pT, nper = m['pT'], m['nper']
        per = np.minimum(jj//pT, nper-1)
        pl = m['plm'][hb]
        num = np.zeros(nper); den = np.zeros(nper)
        np.add.at(num, per, res*pl); np.add.at(den, per, pl*pl)
        amp = np.where(den > 1e-12, num/den, 1.0)
        h_amp = amp[per]*pl
        tgt = res - h_amp
        ext = proto if len(te) <= 32 else np.concatenate([proto, np.array(lv)])
        best = np.empty(nr, dtype=np.int64)
        CH = 1 << 16
        for s in range(0, nr, CH):
            d = np.abs(tgt[s:s+CH, None] - ext[None, :])
            best[s:s+CH] = d.argmin(axis=1)
        sem_a1 = ext[best] + h_amp
        out['a1_exc_rms'] = float(np.sqrt(((res-sem_a1)**2).mean()))
        out['a1_gain_vs_base'] = out['base_exc_rms'] - out['a1_exc_rms']
    else:
        out['a1_exc_rms'] = float('nan'); out['a1_gain_vs_base'] = 0.0
    out['lpc_gain'] = lpc_gain(a, m['sr'])
    out['nres_rms'] = float(np.sqrt((m['nres']**2).mean()))
    return out

def main():
    rows = list(csv.DictReader(open(os.path.expanduser(
        '~/workspace/exact_audio_replication/phase2/results/corpus_results_v6intake.csv'))))
    # stratified sample: 6 clips per class for speed (full run later in Zag)
    import collections
    by = collections.defaultdict(list)
    for r in rows: by[r['name'].split('-')[0]].append(r)
    sample = []
    for c in sorted(by): sample += by[c][:6]
    print(f'sample: {len(sample)} clips')
    res = [run_clip(r['name'], r['clip']) for r in sample]
    json.dump(res, open(os.path.expanduser(
        '~/workspace/exact_audio_replication/phase3/results/candidate_gains.json'), 'w'))
    agg = collections.defaultdict(list)
    for o in res: agg[o['cls']].append(o)
    print(f"{'class':<8} {'base':>8} {'B1':>8} {'B1%':>7} {'B2':>8} {'A1gain':>8} {'lpcG':>6}")
    for c in sorted(agg):
        v = agg[c]
        b = np.mean([o['base_exc_rms'] for o in v])
        b1 = np.mean([o['b1_exc_rms'] for o in v])
        b2 = np.mean([o['b2_exc_rms'] for o in v])
        a1 = np.nanmean([o['a1_gain_vs_base'] for o in v if o['a1_gain_vs_base'] != 0] or [0])
        lg = np.mean([o['lpc_gain'] for o in v])
        print(f"{c:<8} {b:>8.1f} {b1:>8.1f} {100*(b-b1)/b:>6.1f}% {b2:>8.1f} {a1:>8.1f} {lg:>6.1f}")
    # output-domain projection: exc_rms * lpc_gain
    print('--- output-domain projected semantic RMS (exc*lpcG) ---')
    for c in sorted(agg):
        v = agg[c]
        for o in v:
            pass
        b = np.mean([o['base_exc_rms']*o['lpc_gain'] for o in v])
        b1 = np.mean([o['b1_exc_rms']*o['lpc_gain'] for o in v])
        print(f"  {c:<8} base~{b:8.1f} B1~{b1:8.1f}  (measured sem_rms baseline in JSON for reference)")

if __name__ == '__main__':
    main()
