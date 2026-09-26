#!/usr/bin/env python3
"""Scene-specific measurements: voice identities, polyphony, bed delta, regularity."""
import sys, math
import numpy as np
from analyze import read_wav, f0_track, hum_audit

def band_energy(x, sr, f0, bw=25, win=0.1):
    nwin = int(len(x) / (sr*win))
    out = np.zeros(nwin)
    t = np.arange(int(sr*win)) / sr
    for w in range(nwin):
        seg = x[int(w*sr*win):int((w+1)*sr*win)]
        if len(seg) < 10: break
        # quadrature demod at f0
        c = np.cos(2*np.pi*f0*t[:len(seg)]); s = np.sin(2*np.pi*f0*t[:len(seg)])
        # crude bandpass via FFT
        X = np.abs(np.fft.rfft(seg*np.hanning(len(seg))))
        fr = np.fft.rfftfreq(len(seg), 1/sr)
        m = (fr > f0-bw) & (fr < f0+bw)
        out[w] = X[m].sum() / (X.sum()+1e-12)
    return out

def main(p_bed, p_nobed):
    xb, sr = read_wav(p_bed); xn, sr2 = read_wav(p_nobed)
    assert sr == sr2
    dur = len(xb)/sr
    print(f"== scene bed vs nobed ==")
    print(f"  dur={dur:.2f}s bed_peak={np.abs(xb).max():.0f} nobed_peak={np.abs(xn).max():.0f}")
    print(f"  bed_rms={np.sqrt((xb**2).mean()):.1f} nobed_rms={np.sqrt((xn**2).mean()):.1f}")
    # bed-only estimate: bed - nobed (same deterministic mix otherwise)
    d = xb.astype(float) - xn.astype(float)
    print(f"  bed-only rms={np.sqrt((d**2).mean()):.1f} ({20*math.log10(np.sqrt((d**2).mean())/(np.sqrt((xn**2).mean())+1e-9)):+.1f} dB rel mix)")
    print(f"  hum audit bed: " + " ".join(f"{k}:{v*100:.3f}%" for k,v in hum_audit(xb,sr).items()))
    print(f"  hum audit nobed: " + " ".join(f"{k}:{v*100:.3f}%" for k,v in hum_audit(xn,sr).items()))
    # F0 variety over time (bed version)
    tr = f0_track(xb, sr)
    bands = [(295,325),(330,360),(355,380),(385,410)]
    names = ["310-child2","345-child0","365-child1","396-child3"]
    for (lo,hi),nm in zip(bands,names):
        wins = [t for t,f,c in tr if lo < f < hi]
        print(f"  F0 band {nm} ({lo}-{hi}Hz): present in {len(wins)}/{len(tr)} windows, times={[round(t,1) for t in wins[:12]]}{'...' if len(wins)>12 else ''}")
    # energy continuity: fraction of 100ms windows above -40dBFS
    w = int(sr*0.1); nw = len(xb)//w
    e = np.array([np.sqrt((xb[i*w:(i+1)*w]**2).mean()) for i in range(nw)])
    active = (e > 32768*10**(-40/20)).mean()
    print(f"  100ms windows above -40dBFS: {active*100:.1f}% (continuity: high=one unbroken world)")
    # envelope regularity (loop detection) on 100ms env
    ev = e - e.mean(); r0 = np.dot(ev,ev)+1e-12
    lags = range(5, min(len(ev)-2, 120))
    rr = [np.dot(ev[:len(ev)-l], ev[l:])/r0 for l in lags]
    i = int(np.argmax(rr))
    print(f"  env periodicity: max autocorr {rr[i]:.3f} at lag {lags[i]*0.1:.1f}s (high=loop-like)")
    # onset clustering: spectral flux peaks
    hop = int(sr*0.02); fl = []
    prev = None
    for s in range(0, len(xb)-2048, hop):
        X = np.abs(np.fft.rfft(xb[s:s+2048]*np.hanning(2048)))
        if prev is not None:
            fl.append(np.maximum(0, X-prev).sum())
        prev = X
    fl = np.array(fl); th = fl.mean()+2*fl.std()
    onsets = [k*0.02 for k in range(len(fl)) if fl[k] > th]
    print(f"  spectral-flux onsets: {len(onsets)} events, first times={[round(t,2) for t in onsets[:16]]}")
    # check onset times aren't on a rigid grid: diff histogram
    if len(onsets) > 4:
        diffs = np.diff(sorted(onsets))
        print(f"  onset interval: median={np.median(diffs):.2f}s min={diffs.min():.2f}s (>0.05s: no machine-gun grid)")

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
