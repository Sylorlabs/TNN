#!/usr/bin/env python3
"""CHOP-3 detail: spike times + magnitudes, for cross-file comparison."""
import sys, wave
import numpy as np
from scipy.signal import stft
path, evpath = sys.argv[1], sys.argv[2]
w = wave.open(path); n = w.getnframes(); sr = w.getframerate()
s = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float64) / 32768.0
events = [float(x.strip()) for x in open(evpath) if x.strip()]
f, t, Z = stft(s, fs=sr, nperseg=2048, noverlap=1536)
mag = np.abs(Z)
flux = np.sqrt(np.mean(np.diff(np.log1p(mag), axis=1) ** 2, axis=0))
med = np.median(flux); mad = np.median(np.abs(flux - med))
thr = med + 6 * (mad + 1e-12)
spikes = t[1:][flux > thr]
print(f"sr={sr} median_flux={med:.6f} mad={mad:.6f} thr={thr:.6f}", file=sys.stderr)
clustered = []
for sp in spikes:
    if not clustered or sp - clustered[-1] > 0.08:
        clustered.append(sp)
for sp in clustered:
    # magnitude: max flux within 40 ms of spike center
    idx = np.argmin(np.abs(t[1:] - sp))
    magv = flux[max(0,idx-2):idx+3].max()
    unexp = not any(abs(sp - e) < 0.12 for e in events)
    print(f"{sp:.4f} {magv:.6f} {'UNEXPLAINED' if unexp else 'explained'}")
