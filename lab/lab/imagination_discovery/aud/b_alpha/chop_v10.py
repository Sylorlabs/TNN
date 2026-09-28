#!/usr/bin/env python3
"""CHOP instrument — forensic choppiness audit for V10 synthesis forks.

Forensic/measurement only (never committed as evidence of the render itself).
Usage: chop.py <wav> [events.txt]
  events.txt: one scene-scripted transient timestamp per line (seconds).
Reports CHOP-1..3. Exit 0 if CHOP-1 and CHOP-2 pass; CHOP-3 is an audit count.
"""
import sys, wave
import numpy as np
from scipy.signal import stft

def load(path):
    w = wave.open(path)
    n = w.getnframes(); sr = w.getframerate()
    s = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float64) / 32768.0
    return s, sr

def chop1_hard_discontinuities(s):
    d1 = np.abs(np.diff(s, prepend=s[0]))
    # jump > 0.35 FS in one sample while the 5-sample neighborhood is smooth
    jumps = np.where(d1 > 0.35)[0]
    bad = []
    for i in jumps:
        lo = max(0, i - 3); hi = min(len(s), i + 4)
        neigh = np.abs(np.diff(s[lo:hi]))
        if len(neigh) > 3:
            # drop the diff that spans the jump itself; the rest must be smooth
            neigh = np.delete(neigh, min(3, len(neigh) - 1))
        if len(neigh) and np.max(neigh) < 0.06:
            bad.append(i)
    return bad

def chop2_silent_gaps(s, sr):
    win = int(sr * 0.05)
    gaps = []
    i = 0
    n = len(s)
    while i < n:
        seg = s[i:i + win]
        rms = np.sqrt(np.mean(seg ** 2) + 1e-18)
        db = 20 * np.log10(rms)
        if db < -60:
            j = i
            while j < n:
                seg2 = s[j:j + win]
                rms2 = np.sqrt(np.mean(seg2 ** 2) + 1e-18)
                if 20 * np.log10(rms2) >= -60:
                    break
                j += win
            dur = (j - i) / sr
            t0 = i / sr
            # ignore the 30 ms end fades
            if dur >= 0.15 and not (t0 < 0.05 or t0 + dur > n / sr - 0.05):
                gaps.append((round(t0, 2), round(dur, 2)))
            i = j
        else:
            i += win
    return gaps

def chop3_flux_spikes(s, sr, events):
    f, t, Z = stft(s, fs=sr, nperseg=2048, noverlap=1536)
    mag = np.abs(Z)
    flux = np.sqrt(np.mean(np.diff(np.log1p(mag), axis=1) ** 2, axis=0))
    thr = np.median(flux) + 6 * (np.median(np.abs(flux - np.median(flux))) + 1e-12)
    spikes = t[1:][flux > thr]
    # cluster spikes within 80 ms
    clustered = []
    for sp in spikes:
        if not clustered or sp - clustered[-1] > 0.08:
            clustered.append(sp)
    unexplained = []
    for sp in clustered:
        if not any(abs(sp - e) < 0.12 for e in events):
            unexplained.append(round(float(sp), 3))
    return len(clustered), [round(float(x), 3) for x in clustered], unexplained

def main():
    path = sys.argv[1]
    events = []
    if len(sys.argv) > 2:
        with open(sys.argv[2]) as f:
            events = [float(x.strip()) for x in f if x.strip()]
    s, sr = load(path)
    bad = chop1_hard_discontinuities(s)
    gaps = chop2_silent_gaps(s, sr)
    nsp, spikes, unexpl = chop3_flux_spikes(s, sr, events)
    print(f"CHOP-1 hard discontinuities: {len(bad)} {'PASS' if not bad else 'FAIL ' + str(bad[:10])}")
    print(f"CHOP-2 silent gaps >=150ms: {gaps if gaps else 'NONE'} {'PASS' if not gaps else 'FAIL'}")
    print(f"CHOP-3 flux spikes: {nsp} total, {len(unexpl)} unexplained")
    if unexpl:
        print(f"  unexplained at s: {unexpl[:20]}")
    ok = (not bad) and (not gaps)
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
