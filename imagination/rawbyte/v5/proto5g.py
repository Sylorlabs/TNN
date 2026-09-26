#!/usr/bin/env python3
"""proto5e.py — v5 LONG-MEMORY prototype, harmonic+noise excitation.

The excitation's pitch (+20 dB harmonic lines, only 3.4% of residual
variance) is too weak for any prototype-walk prior to reproduce honestly:
 - phase histogram: entropy 3.83/4.16 (flat)
 - PL1 skip-lag tables: max cond 0.032 vs 0.016 uniform (flat)
 - integer-period phase: half-cycle drift smear (T0=127.49 vs pT=128)
 - fractional phase: sharper but still only 3.4% variance explained
The old build's pitch came from argmax modal-locking AMPLIFYING the weak
structure (0.21 -> 0.62) -- a nonlinearity, not a faithful reproduction.

v5e: HARMONIC+NOISE DECOMPOSITION of the excitation.
 - hear: fractional period T0 (spectral), phase-locked mean plm (the
   harmonic waveform, NBINS samples), period-jitter PMF (autocorr profile).
   nres = res - plm[phase]. The prototype walk (K-means, bigram, EP,
   onset, energy) is learned on nres (the noise part).
 - imagine: the walk generates the noise part (proportional fmix32
   traversal, energy-matched); the harmonic part plm[bin]*g is added
   with the SAME gain g (preserves the learned harmonic/noise ratio).
   Phase advances 1/L per sample; L redrawn per cycle from the PMF
   (deterministic fmix32) -> natural jitter, decaying harmonic multiples.
Long memory = the explicit periodic component (horizon = pitch period,
derived from the signal) + the jitter distribution. Zero RNG.
"""
import struct, sys, math
import numpy as np
from proto5b import read_wav, write_wav, autocorr_nomean, fmix32


def measure_period_pmf(res, plm, pT):
    """True period distribution via plm matched-filter peak picking.
    (The residual-autocorr profile overestimates jitter; this measures
    actual inter-period intervals.)"""
    tmpl = plm - plm.mean()
    full = res  # res here already includes the harmonic part
    corr = np.correlate(full, tmpl, mode='valid')
    th = corr.max() * 0.25
    peaks = []; i = pT - 30
    while i < len(corr) - (pT - 30):
        lo = max(0, i - (pT - 30)); hi = min(len(corr), i + (pT - 30))
        if corr[i] > th and corr[i] >= corr[lo:hi].max():
            peaks.append(i); i += pT - 30
        else:
            i += 1
    peaks = np.array(peaks)
    iv = np.diff(peaks)
    iv = iv[(iv >= pT - 8) & (iv <= pT + 8)]
    pmf = np.zeros(17)
    for v in iv:
        pmf[int(v) - (pT - 8)] += 1
    s = pmf.sum()
    return pmf / s if s > 0 else np.ones(17) / 17.0

def refine_T0(res, sr, pT):
    n = len(res); N = 1
    while N < 8 * n: N <<= 1
    w = res * np.hanning(n)
    W = np.zeros(N); W[:n] = w
    X = np.abs(np.fft.rfft(W)); fr = np.fft.rfftfreq(N, 1.0 / sr)
    fguess = sr / pT
    band = (fr > fguess * 0.85) & (fr < fguess * 1.18)
    if not band.any(): return float(pT)
    i = int(np.argmax(X[band])); idx = np.where(band)[0][i]
    if 0 < idx < len(X) - 1:
        y0, y1, y2 = np.log(X[idx-1] + 1e-12), np.log(X[idx]), np.log(X[idx+1] + 1e-12)
        den = (y0 - 2 * y1 + y2)
        d = 0.5 * (y0 - y2) / den if abs(den) > 1e-12 else 0.0
        f0 = fr[idx] + max(-1.0, min(1.0, d)) * (fr[1] - fr[0])
    else:
        f0 = fr[idx]
    return sr / f0 if f0 > 1 else float(pT)

def hear(x, sr, K=64, P=64):
    n = len(x)
    R = autocorr_nomean(x, np.arange(0, P + 1))
    a = np.zeros(P); E = R[0]
    for m in range(1, P + 1):
        acc = np.dot(a[:m-1], R[m-1:0:-1]) if m > 1 else 0.0
        kk = (R[m] - acc) / E
        assert abs(kk) < 1.0, ('reflection', m, kk)
        anew = a.copy(); anew[m-1] = kk
        if m > 1:
            anew[:m-1] = a[:m-1] - kk * a[m-2::-1][:m-1]
        a = anew
        E = E * (1.0 - kk * kk)
        if E <= 0: E = R[0] * 1e-6
    nr = n - P
    res = np.empty(nr)
    for i in range(nr):
        seg = x[P+i-1:i-1:-1] if i > 0 else x[P-1::-1][:P]
        res[i] = x[P+i] - np.dot(a, seg)
    # pitch detection on the residual
    LMAX = sr // 20
    rl = np.arange(50, LMAX + 1)
    rr = autocorr_nomean(res, rl, stride=4)
    r0 = float(np.dot(res[::4], res[::4])) + 1e-12
    pT, best = 0, 0.15
    for lag, v in zip(rl, rr / r0):
        if v > best: best, pT = v, int(lag)
    # harmonic part: fractional period + phase-locked mean
    T0, NBINS = 0.0, 0
    plm = np.zeros(0); PMF = np.zeros(0)
    nres = res
    if pT > 0:
        T0 = refine_T0(res, sr, pT)
        NBINS = int(round(T0))
        bins = (np.floor((np.arange(nr) / T0) % 1.0 * NBINS).astype(np.int64)) % NBINS
        plm = np.array([res[bins == b].mean() for b in range(NBINS)])
        nres = res - plm[bins]
        PMF = measure_period_pmf(res, plm, pT)
    # walk model on the NOISE remainder
    qs = np.quantile(nres, np.linspace(0.5 / K, 1 - 0.5 / K, K))
    proto = qs.copy()
    q = np.zeros(nr, dtype=np.int64)
    for it in range(40):
        d = np.abs(nres[:, None] - proto[None, :])
        qn = d.argmin(axis=1)
        done = np.array_equal(qn, q)
        q = qn
        for c in range(K):
            msk = q == c
            if msk.any(): proto[c] = nres[msk].mean()
        if done: break
    uni = np.bincount(q, minlength=K).astype(np.int64)
    bg = np.zeros((K, K, K), dtype=np.int64)
    np.add.at(bg, (q[:-2], q[1:-1], q[2:]), 1)
    m0 = min(sr * 30 // 1000, nr)
    ob = np.zeros((K, K), dtype=np.int64)
    np.add.at(ob, (q[:m0-1], q[1:m0]), 1)
    oi = int(ob.argmax()); ob0, ob1 = oi // K, oi % K
    tail = min(sr * 100 // 1000, nr)
    floorv = float(np.abs(nres[-tail:]).mean())
    attackv = float(np.abs(nres[:m0]).mean())
    frlen = max(1, sr // 100)
    nf = (nr + frlen - 1) // frlen
    EP = np.array([np.abs(nres[f*frlen:min((f+1)*frlen, nr)]).mean() for f in range(nf)])
    m = dict(P=P, K=K, a=a, proto=proto, q=q, uni=uni, bg=bg, pT=pT,
               T0=T0, NBINS=NBINS, plm=plm, PMF=PMF,
               ob0=ob0, ob1=ob1, floorv=floorv,
               attackv=attackv, EP=EP, frlen=frlen, n=n, sr=sr)
    m['boost'] = calibrate_boost(m, x)
    return m

def calibrate_boost(m, x):
    """Learn the harmonic boost: match the heard AUDIO's pitch strength.
    Bisection search on boost using short test renders. Deterministic.
    x is the heard audio."""
    if m['pT'] <= 0 or len(m['plm']) == 0:
        return 1.0
    pT = m['pT']
    # heard harmonic decay (first lag) of the AUDIO
    n = len(x); xf = x.astype(float); xf -= xf.mean()
    r0 = float(np.dot(xf, xf)) + 1e-12
    h_heard = float(np.dot(xf[:n-pT], xf[pT:]) / r0)
    if h_heard < 0.05:
        return 1.0
    tN = min(12000, m['n'] - m['P'])
    def h_of_boost(b):
        y = imagine_test(m, tN, boost=b)
        n2 = len(y); yf = y.astype(float); yf -= yf.mean()
        r02 = float(np.dot(yf, yf)) + 1e-12
        return float(np.dot(yf[:n2-pT], yf[pT:]) / r02) if n2 > pT else 0.0
    lo, hi = 1.0, 12.0
    h_lo, h_hi = h_of_boost(lo), h_of_boost(hi)
    if h_hi < h_heard * 0.7:
        # even max boost can't approach the target: harmonic model not viable
        return 1.0
    for _ in range(4):
        mid = (lo + hi) / 2
        h_mid = h_of_boost(mid)
        if h_mid < h_heard: lo = mid
        else: hi = mid
    return (lo + hi) / 2

def draw_period(PMF, pT, ndraw):
    u = fmix32(ndraw + 1) / 4294967296.0
    cum = np.cumsum(PMF)
    idx = int(np.searchsorted(cum, u, side='right'))
    return pT - 8 + min(idx, 16)


def imagine_test(m, N, boost=1.0):
    """Short deterministic render for boost calibration."""
    P, K, sr = m['P'], m['K'], m['sr']
    a, proto, bg = m['a'], m['proto'], m['bg']
    pT, NBINS, plm, PMF = m['pT'], m['NBINS'], m['plm'], m['PMF']
    T0 = m['T0']
    use_h = pT > 0 and T0 > 0 and len(plm) == NBINS and NBINS > 0
    est = np.zeros(N); out = np.zeros(N)
    prev2, prev1 = m['ob0'], m['ob1']
    ewalk = max(m['attackv'], 1.0)
    phase = 0.0; L = float(pT) if pT > 0 else 1.0; ndraw = 0
    for i in range(N):
        fr = min(i // m['frlen'], len(m['EP']) - 1)
        epr = m['EP'][fr]
        lo, hi = epr * 0.2, max(epr * 5.0, 1.0)
        ap = np.abs(proto)
        mask = ((ap >= lo) & (ap <= hi)) if epr >= 1.0 else np.ones(K, bool)
        if not mask.any(): mask[:] = True
        w = (bg[prev2, prev1, :].astype(np.float64) + 1.0) * mask
        tot = w.sum()
        u = fmix32(i + 1) / 4294967296.0
        bi = int(np.searchsorted(np.cumsum(w), u * tot, side='right'))
        bi = min(bi, K - 1)
        rv0 = proto[bi]
        ewalk = 0.99 * ewalk + 0.01 * abs(rv0)
        if epr < 1.0: g = 0.02
        elif ewalk > 0.5: g = min(8.0, max(0.125, epr / ewalk))
        else: g = 1.0
        rv = rv0 * g
        if use_h:
            hbin = int(phase * NBINS) % NBINS
            rv = rv + plm[hbin] * g * boost
            phase += 1.0 / L
            if phase >= 1.0:
                phase -= 1.0; ndraw += 1
                L = float(draw_period(PMF, pT, ndraw))
        take = min(i, P) if i > 0 else 0
        pred = np.dot(a[:take], est[i-1::-1][:take]) if take > 0 else 0.0
        ev = pred + rv
        est[i] = ev
        out[i] = np.clip(round(ev), -32768, 32767)
        prev2, prev1 = prev1, bi
    return out.astype(np.int16)

def imagine(m, dur_s, mode):
    P, K, sr = m['P'], m['K'], m['sr']
    a, proto = m['a'], m['proto']
    bg, pT = m['bg'], m['pT']
    T0, NBINS, plm, PMF = m['T0'], m['NBINS'], m['plm'], m['PMF']
    use_h = pT > 0 and T0 > 0 and len(plm) == NBINS and NBINS > 0
    N = max(64, min(int(round(dur_s * sr)), sr * 12))
    est = np.zeros(N); out = np.zeros(N)
    prev2, prev1 = m['ob0'], m['ob1']
    floorv, attackv = m['floorv'], m['attackv']
    thresh = max(attackv * 0.03, floorv * 2.0, 2.0)
    ewalk = max(attackv, 1.0)
    RW = 2048
    ring = np.zeros(RW); rsum = 0.0; rpos = 0
    stop = N
    phase = 0.0; L = float(pT) if pT > 0 else 1.0; ndraw = 0
    for i in range(N):
        fr = min(i // m['frlen'], len(m['EP']) - 1)
        epr = m['EP'][fr]
        lo, hi = epr * 0.2, max(epr * 5.0, 1.0)
        ap = np.abs(proto)
        mask = ((ap >= lo) & (ap <= hi)) if epr >= 1.0 else np.ones(K, bool)
        if not mask.any(): mask[:] = True
        w = (bg[prev2, prev1, :].astype(np.float64) + 1.0) * mask
        tot = w.sum()
        u = fmix32(i + 1) / 4294967296.0
        bi = int(np.searchsorted(np.cumsum(w), u * tot, side='right'))
        bi = min(bi, K - 1)
        rv0 = proto[bi]
        ewalk = 0.99 * ewalk + 0.01 * abs(rv0)
        if epr < 1.0:
            g = 0.02
        elif ewalk > 0.5:
            g = min(8.0, max(0.125, epr / ewalk))
        else:
            g = 1.0
        rv = rv0 * g
        if use_h:
            hbin = int(phase * NBINS) % NBINS
            rv = rv + plm[hbin] * g * m.get('boost', 1.0)
            phase += 1.0 / L
            if phase >= 1.0:
                phase -= 1.0
                ndraw += 1
                L = float(draw_period(PMF, pT, ndraw))
        if i > 0:
            take = min(i, P)
            pred = np.dot(a[:take], est[i-1::-1][:take])
        else:
            pred = 0.0
        ev = pred + rv
        est[i] = ev
        out[i] = np.clip(round(ev), -32768, 32767)
        ar = abs(rv)
        rsum += ar - ring[rpos]; ring[rpos] = ar; rpos = (rpos + 1) % RW
        if mode == 0 and i > sr // 10 and i >= RW and rsum / RW < thresh:
            stop = i + 1
            break
        prev2, prev1 = prev1, bi
    return out[:stop].astype(np.int16)

def reemit(m):
    P, N, sr = m['P'], m['n'], m['sr']
    a, proto, q = m['a'], m['proto'], m['q']
    # only re-add plm if the harmonic model was viable (boost in sane range);
    # a struggled calibration (boost~1 or capped) means plm is unreliable
    boost = float(m.get('boost', 1.0))
    use_h = (m['pT'] > 0 and m['T0'] > 0 and len(m['plm']) == m['NBINS']
             and 1.5 < boost < 10.0)
    T0, NBINS, plm = m['T0'], m['NBINS'], m['plm']
    est = np.zeros(N); out = np.zeros(N)
    for i in range(N):
        # re-emit must reconstruct the ORIGINAL residual: nres proto + plm
        rv = proto[q[i-P]] if i >= P else proto[q[i]]
        if use_h:
            hbin = int(((i / T0) % 1.0) * NBINS) % NBINS
            rv = rv + plm[hbin]
        if i < P:
            ev = rv
        else:
            ev = np.dot(a, est[i-P:i][::-1]) + rv
        est[i] = ev
        out[i] = np.clip(round(ev), -32768, 32767)
    return out.astype(np.int16)

def save(m, path):
    np.savez(path, **dict(m))

def load(path):
    m = dict(np.load(path, allow_pickle=True))
    for k in ('q', 'uni', 'bg'):
        if k in m: m[k] = m[k].astype(np.int64)
    for k in ('P', 'K', 'pT', 'NBINS', 'ob0', 'ob1', 'frlen', 'n', 'sr'):
        m[k] = int(m[k])
    return m

if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'hear':
        x, sr = read_wav(sys.argv[2])
        m = hear(x, sr)
        save(m, sys.argv[3])
        print(f"P={m['P']} pT={m['pT']} T0={m['T0']:.3f} attack={m['attackv']:.1f} floor={m['floorv']:.2f}")
        if len(m['PMF']): print('period PMF:', np.round(m['PMF'], 3))
        if len(m['plm']): print('plm std:', round(float(m['plm'].std()),2))
    elif cmd == 'imagine':
        m = load(sys.argv[2])
        y = imagine(m, float(sys.argv[3]), int(sys.argv[4]))
        write_wav(sys.argv[5], y.astype(np.float64), m['sr'])
        print('wrote', sys.argv[5], len(y))
    elif cmd == 'reemit':
        m = load(sys.argv[2])
        y = reemit(m)
        write_wav(sys.argv[3], y.astype(np.float64), m['sr'])
        print('wrote', sys.argv[3], len(y))
