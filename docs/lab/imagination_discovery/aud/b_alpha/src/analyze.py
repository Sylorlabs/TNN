#!/usr/bin/env python3
"""SPECSTAT analysis (Fork C, AUDIO V10).

One-time analysis of a real playground recording into slowly-varying
band-energy statistics. Hand-built 12-band resonator bank (2nd-order
constant-skirt bandpass biquads, time-domain difference equation via
lfilter -- no FFT anywhere). NO audio atoms kept: only statistics.

Outputs stats_v10_specstat.txt:
  SPECSTAT1
  NB NF
  12 band centers (Hz)
  12 x 5 biquad coeffs (b0 b1 b2 a1 a2) with y=b0x+b1x1+b2x2-a1y1-a2y2
  12 noise gains (mean y^2 driving the filter with the Zag h01 stream)
  12 modulation rates (Hz), 12 modulation depths (linear fraction)
  5 phase segment picks (start_frame n_frames), 10 Hz frame grid
  NF lines x 12 linear band energies (mean y^2 per 0.1 s frame)

Deterministic: no RNG; hash stream is the exact h32 used by the Zag renderer.
"""
import math
import numpy as np
import wave
from scipy.signal import lfilter

SR = 44100
NB = 12
FRAME = 4410  # 0.1 s

# ---- deterministic hash stream: identical to common.zag h32/h01 ----
def h32(s, st):
    z = (s * 2654435761 + st * 40503 + 1) & 0xFFFFFFFF
    z = (z ^ (z >> 16)) & 0xFFFFFFFF
    z = (z * 2246822519) & 0xFFFFFFFF
    z = (z ^ (z >> 13)) & 0xFFFFFFFF
    z = (z * 3266489917) & 0xFFFFFFFF
    z = (z ^ (z >> 16)) & 0xFFFFFFFF
    return z

def h01(seed, k):
    return h32(seed, k) / 4294967296.0

# ---- 12-band log-spaced resonator bank, 0.6-octave bandwidth ----
ratio = (8360.0 / 180.0) ** (1.0 / (NB - 1))
centers = [180.0 * ratio ** i for i in range(NB)]

def band_coeffs(c):
    flo = c * 2 ** -0.3
    fhi = c * 2 ** 0.3
    df = fhi - flo
    r = math.exp(-math.pi * df / SR)
    w = 2.0 * math.pi * c / SR
    cw = math.cos(w)
    b0 = (1.0 - r) / 2.0
    b2 = -(1.0 - r) / 2.0
    a1 = -2.0 * r * cw
    a2 = r * r
    return b0, 0.0, b2, a1, a2

coeffs = [band_coeffs(c) for c in centers]

# ---- load w2 ----
w = wave.open('/home/hatch/workspace/tnn-lab/imagination_discovery/aud/b_alpha/study/w2.wav')
n = w.getnframes()
x = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float64) / 32768.0
NF = n // FRAME
x = x[:NF * FRAME]

# ---- per-band energy at 10 Hz ----
E = np.zeros((NF, NB))
for b, (b0, b1, b2, a1, a2) in enumerate(coeffs):
    y = lfilter([b0, b1, b2], [1.0, a1, a2], x)
    E[:, b] = (y.reshape(NF, FRAME) ** 2).mean(axis=1)

# ---- noise gains: same filters driven by the Zag h01 stream (uniform [-1,1]) ----
NOISE_SEED = 910273
nn = SR * 10
nz = np.array([2.0 * h01(NOISE_SEED, k) - 1.0 for k in range(nn)])
noise_gain = np.zeros(NB)
for b, (b0, b1, b2, a1, a2) in enumerate(coeffs):
    y = lfilter([b0, b1, b2], [1.0, a1, a2], nz)
    noise_gain[b] = (y[int(SR):] ** 2).mean()  # skip 1 s settle

# ---- modulation stats: per-band dB series ----
db = 10.0 * np.log10(E + 1e-12)
dbm = db.mean(axis=0)
mod_depth = db.std(axis=0) / 20.0          # linear-ish fractional depth
mod_depth = np.clip(mod_depth, 0.02, 0.60)
dm = db - dbm
sgn = np.sign(dm)
zc = ((sgn[1:] * sgn[:-1]) < 0).sum(axis=0)
mod_rate = np.clip(zc / (2.0 * NF * 0.1), 0.3, 3.0)  # Hz

# ---- phase segment picks (deterministic, strict first-wins) ----
# Spectral-flux guard: the G-FLUXm audit caps 1 s -> 1 s normalized spectral
# change. Prefer windows whose own 1 s proxy flux is tame, so the composed
# scene stays under the bar. (Proxy: 12-band 1 s spectra, same formula.)
def win_maxflux(s, L):
    seg = E[s:s + L]
    n1 = L // 10
    sp = np.sqrt(seg[:n1 * 10].reshape(n1, 10, 12).sum(axis=1) + 1e-18)
    sp = sp / sp.max(axis=1, keepdims=True)
    fl = np.sqrt(((np.diff(sp, axis=0) ** 2).mean(axis=1))) * 1000
    return fl.max()
# phases: alive 6.5s, chase 6.0s, trip 4.0s, laugh 6.5s, wind 7.0s
phase_spec = [
    ("alive", 65), ("chase", 60), ("trip", 40), ("laugh", 65), ("wind", 70),
]
tot = E.sum(axis=1)
lo_mid = E[:, 3:6].sum(axis=1)      # 514-1034 Hz voice presence
hi_mid = E[:, 5:8].sum(axis=1)      # 1034-2081 Hz laugh band
burst = np.abs(np.diff(db, axis=0)).mean(axis=1)  # frame-to-frame change
burst = np.concatenate([[burst[0]], burst])

def score(name, s, L):
    seg = slice(s, s + L)
    e = tot[seg].mean()
    if name == "alive":
        return (0.40 < np.searchsorted(np.sort(tot), e) / NF < 0.75) * 1.0 + 0.001 * (lo_mid[seg].mean() / (e + 1e-12))
    if name == "chase":
        return (np.searchsorted(np.sort(tot), e) / NF > 0.70) * 1.0 + 0.5 * burst[seg].mean()
    if name == "trip":
        pct = np.searchsorted(np.sort(tot), e) / NF
        if not (0.30 < pct < 0.65):
            return -1e18
        calm = 1.0 / (1.0 + db[seg].std())
        fx = win_maxflux(s, L)
        return 0.3 * calm - 2.0 * (fx / 100.0)
    if name == "laugh":
        return (np.searchsorted(np.sort(tot), e) / NF > 0.60) * 1.0 + 1.0 * (hi_mid[seg].mean() / (e + 1e-12)) + 0.3 * db[seg].std()
    if name == "wind":
        return -(e)  # quietest
    return 0.0

segs = []
for name, L in phase_spec:
    best, bs = -1, -1e18
    for s in range(0, NF - L + 1, 5):  # 0.5 s step
        sc = score(name, s, L)
        if sc > bs:
            bs, best = sc, s
    segs.append((name, best, L))

for (name, s, L) in segs:
    print(f"{name:6s} frames {s:3d}..{s+L:3d}  t={s/10:5.1f}s..{(s+L)/10:5.1f}s  meanE={tot[s:s+L].mean():.2e}")

# ---- phase amplitude trims: equalize each phase's mean energy to the
# recording's global mean (k=1.0, energy domain). Residual dynamics are the
# recording's own second-to-second variation; keeps composed G-STA inside
# the real-anchor envelope. Written into the stats file. ----
tot_all = E.sum(axis=1)
mp_all = np.array([tot_all[s:s + L].mean() for (_, s, L) in segs])
M_all = tot_all.mean()
trims = (mp_all / M_all) ** (-1.0)
print("trims(energy):", " ".join(f"{t:.4f}" for t in trims))
out = '/home/hatch/workspace/aud_v10/fork_specstat/stats_v10_specstat.txt'
with open(out, 'w') as f:
    f.write("SPECSTAT1\n")
    f.write(f"{NB} {NF}\n")
    f.write(" ".join(f"{c:.3f}" for c in centers) + "\n")
    for (b0, b1, b2, a1, a2) in coeffs:
        f.write(f"{b0:.9f} {b1:.9f} {b2:.9f} {a1:.9f} {a2:.9f}\n")
    f.write(" ".join(f"{g:.9e}" for g in noise_gain) + "\n")
    f.write(" ".join(f"{r:.4f}" for r in mod_rate) + "\n")
    f.write(" ".join(f"{d:.4f}" for d in mod_depth) + "\n")
    for (name, s, L) in segs:
        f.write(f"{s} {L}\n")
    f.write(" ".join(f"{t:.6f}" for t in trims) + "\n")
    for i in range(NF):
        f.write(" ".join(f"{v:.6e}" for v in E[i]) + "\n")
print("wrote", out)
# sanity: overall band balance
print("band mean energies:", " ".join(f"{E[:,b].mean():.1e}" for b in range(NB)))
